import http.server
import socketserver
import json
import os
import sys
import threading
import time
from datetime import datetime

PORT = 8088
BASE_DIR = "/Users/user/.gemini/antigravity/scratch/tep_dashboard"
CONFIG_FILE = os.path.join(BASE_DIR, "demo_config.json")
CACHE_FILE = os.path.join(BASE_DIR, "live_data.json")

# Import extraction logic
sys.path.insert(0, BASE_DIR)
import sync_service

def background_sync_worker():
    while True:
        try:
            time.sleep(300) # sync every 5 minutes
            print("[AutoSync] Starting scheduled Google Drive sync...")
            sync_service.extract_all()
            print("[AutoSync] Scheduled sync complete.")
        except Exception as e:
            print("[AutoSync] Error in worker:", e)

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_GET(self):
        if self.path.startswith("/api/data"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            if os.path.exists(CACHE_FILE):
                with open(CACHE_FILE, "r", encoding="utf-8") as f:
                    self.wfile.write(f.read().encode("utf-8"))
            else:
                data = sync_service.extract_all()
                self.wfile.write(json.dumps(data).encode("utf-8"))
            return
        
        super().do_GET()

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_len) if content_len > 0 else b"{}"

        # 1. Trigger live refresh from Google Drive
        if self.path == "/api/refresh":
            print("[API] Manual refresh requested...")
            try:
                data = sync_service.extract_all()
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "data": data}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))
            return

        # 2. Check demo access (PIN & Expiration)
        if self.path == "/api/check-access":
            req = {}
            try:
                req = json.loads(post_data.decode("utf-8"))
            except Exception:
                pass
            pin = str(req.get("pin", "")).strip()

            resp = {"valid": False, "message": "Неверный PIN-код"}
            try:
                if os.path.exists(CONFIG_FILE):
                    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                        cfg = json.load(f)
                    
                    if not cfg.get("require_auth", True):
                        resp = {"valid": True, "client_name": "Гостевой режим", "expires_at": None}
                    else:
                        now = datetime.now()
                        matched = None
                        for d in cfg.get("active_demos", []):
                            if str(d.get("pin", "")).strip() == pin:
                                matched = d
                                break
                        
                        if matched:
                            exp_str = matched.get("expires_at")
                            exp_dt = datetime.fromisoformat(exp_str)
                            if now > exp_dt:
                                resp = {
                                    "valid": False,
                                    "expired": True,
                                    "client_name": matched.get("client_name"),
                                    "message": f"Срок действия демо-доступа для {matched.get('client_name')} истек ({exp_dt.strftime('%d.%m.%Y')}). Для продления обратитесь к менеджеру: +7 (800) 555-20-26"
                                }
                            else:
                                days_left = (exp_dt - now).days
                                resp = {
                                    "valid": True,
                                    "expired": False,
                                    "client_name": matched.get("client_name"),
                                    "expires_at": exp_dt.strftime("%d.%m.%Y %H:%M"),
                                    "days_left": days_left,
                                    "message": f"Демо-доступ активен до {exp_dt.strftime('%d.%m.%Y')}"
                                }
            except Exception as ex:
                resp = {"valid": False, "message": f"Ошибка проверки доступа: {ex}"}

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

class ThreadingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

if __name__ == "__main__":
    # Start background auto-sync thread
    t = threading.Thread(target=background_sync_worker, daemon=True)
    t.start()
    
    server_address = ('', PORT)
    httpd = ThreadingServer(server_address, DashboardHandler)
    print(f"[Server] Live Dashboard Server running on http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("[Server] Shutting down...")
