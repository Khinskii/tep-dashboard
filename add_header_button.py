with open("/Users/user/.gemini/antigravity/scratch/tep_dashboard/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace Live Badge to also include the prominent Refresh button right next to it
old_badge = '''        <!-- Live Badge -->
        <div class="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-emerald-950/40 border border-emerald-800/50 text-emerald-400 text-xs font-medium badge-pulse">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
          <span>Google Drive Online</span>
        </div>'''

new_badge = '''        <!-- Live Badge -->
        <div class="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-emerald-950/40 border border-emerald-800/50 text-emerald-400 text-xs font-medium badge-pulse">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
          <span id="liveStatusText">Google Drive Online</span>
        </div>

        <!-- YARKAYA KNOPKA OBNOVLENIYA -->
        <button onclick="triggerManualSync()" id="mainHeaderRefreshBtn" class="flex items-center gap-2 px-4 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 active:scale-95 text-white text-xs font-bold shadow-lg shadow-cyan-500/30 transition ring-1 ring-cyan-400/50 cursor-pointer">
          <i data-lucide="refresh-cw" class="w-3.5 h-3.5" id="headerSyncIcon"></i>
          <span id="headerSyncText">🔄 Обновить данные</span>
        </button>'''

if old_badge in html:
    html = html.replace(old_badge, new_badge)
    print("Header button successfully inserted!")
else:
    print("Old badge pattern not found, trying regex...")
    import re
    html = re.sub(r'<!-- Live Badge -->\s*<div[^>]*>.*?</div>', new_badge, html, flags=re.DOTALL)
    print("Regex replacement completed!")

# Also update triggerManualSync in JS to spin both icons and update texts
old_js_sync = "const text = document.getElementById('syncText');"
new_js_sync = """const text = document.getElementById('syncText');
      const hIcon = document.getElementById('headerSyncIcon');
      const hText = document.getElementById('headerSyncText');
      if (hIcon) hIcon.classList.add('animate-spin');
      if (hText) hText.innerText = 'Синхронизация...';"""

if old_js_sync in html:
    html = html.replace(old_js_sync, new_js_sync)

old_js_end = "text.innerText = 'Обновить данные';"
new_js_end = """text.innerText = 'Обновить данные';
        if (hIcon) hIcon.classList.remove('animate-spin');
        if (hText) hText.innerText = '🔄 Обновить данные';"""

if old_js_end in html:
    html = html.replace(old_js_end, new_js_end)

with open("/Users/user/.gemini/antigravity/scratch/tep_dashboard/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Saved index.html successfully!")
