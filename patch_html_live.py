import re

path = "/Users/user/.gemini/antigravity/scratch/tep_dashboard/index.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add Demo Access Banner & Lock Screen Modal
gate_html = '''
  <!-- ================= DEMO ACCESS FLOATING BANNER ================= -->
  <div id="demoAccessBanner" class="bg-gradient-to-r from-blue-950 via-slate-900 to-indigo-950 border-b border-cyan-800/40 px-4 py-2 text-xs flex flex-wrap items-center justify-between text-slate-300">
    <div class="flex items-center gap-2">
      <span class="px-2 py-0.5 rounded bg-cyan-900/60 text-cyan-300 border border-cyan-700/50 font-semibold text-[11px]">ДЕМО-РЕЖИМ</span>
      <span id="demoClientBadge" class="font-medium text-white">ООО «Северсталь-Пром»</span>
      <span class="text-slate-500">•</span>
      <span id="demoExpiresBadge" class="text-emerald-400 font-medium">Активен до 01.10.2026</span>
    </div>
    <div class="flex items-center gap-3">
      <button onclick="triggerManualSync()" id="manualSyncBtn" class="flex items-center gap-1.5 text-cyan-400 hover:text-cyan-300 font-medium">
        <i data-lucide="refresh-cw" class="w-3.5 h-3.5" id="syncIcon"></i>
        <span id="syncText">Обновить данные</span>
      </button>
      <span class="text-slate-600">|</span>
      <button onclick="logoutDemo()" class="text-slate-400 hover:text-rose-400">Сменить код</button>
    </div>
  </div>

  <!-- ================= DEMO LOCK SCREEN MODAL ================= -->
  <div id="demoLockModal" class="fixed inset-0 bg-[#0B1120]/95 backdrop-blur-xl z-50 flex items-center justify-center p-4 hidden">
    <div class="glass-panel w-full max-w-md p-8 rounded-3xl border border-cyan-800/60 shadow-2xl text-center space-y-6 relative overflow-hidden">
      <div class="w-16 h-16 rounded-2xl bg-gradient-to-tr from-cyan-600 to-blue-700 mx-auto flex items-center justify-center text-white shadow-xl shadow-cyan-600/30">
        <i data-lucide="lock" class="w-8 h-8"></i>
      </div>
      
      <div>
        <h2 class="text-xl font-bold text-white">Демо-доступ к дашборду</h2>
        <p class="text-xs text-slate-400 mt-1">Введите персональный PIN-код компании для входа в систему операционного контроля</p>
      </div>

      <div class="space-y-3">
        <input type="password" id="pinInput" placeholder="Введите PIN-код..." 
               class="w-full text-center tracking-widest text-lg font-bold font-mono-num bg-slate-900 border border-brand-border rounded-xl py-3 text-white focus:outline-none focus:border-cyan-500 placeholder:text-slate-600 placeholder:text-sm"
               maxlength="8" onkeydown="if(event.key === 'Enter') submitPin()">
        
        <div id="pinErrorMsg" class="hidden text-xs text-rose-400 bg-rose-950/40 p-2.5 rounded-lg border border-rose-800/60 font-medium"></div>

        <button onclick="submitPin()" class="w-full py-3 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-bold uppercase tracking-wider transition shadow-lg shadow-cyan-600/30">
          Войти в дашборд
        </button>
      </div>

      <div class="pt-4 border-t border-brand-border/60 text-[11px] text-slate-500 space-y-1">
        <p>Для партнеров и клиентов ООО «ТЭП» & СМУ Промстрой</p>
        <p class="text-slate-400">Тестовый PIN для демонстрации: <code class="text-cyan-400 font-mono-num bg-slate-800 px-1.5 py-0.5 rounded">2026</code></p>
      </div>
    </div>
  </div>
'''

# Insert banner right after <body>
html = html.replace("<body class=\"min-h-screen flex flex-col antialiased selection:bg-cyan-500 selection:text-white\">", 
                    "<body class=\"min-h-screen flex flex-col antialiased selection:bg-cyan-500 selection:text-white\">\n" + gate_html)

# Add IDs to KPI elements for dynamic updating
html = html.replace('287 184 ₽</div>', '<span id="kpi-balance">287 184 ₽</span></div>')
html = html.replace('315 800 ₽</div>', '<span id="kpi-income">315 800 ₽</span></div>')
html = html.replace('335 079 ₽</div>', '<span id="kpi-fio-paid">335 079 ₽</span></div>')

# Append dynamic Live Sync Script & Access Manager
live_js = '''
  <script>
    // ================= DEMO ACCESS LOGIC =================
    async function checkAccess(pin) {
      try {
        const res = await fetch('/api/check-access', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ pin })
        });
        return await res.json();
      } catch(e) {
        return { valid: true, client_name: "Офлайн-режим", expires_at: "Без ограничений" };
      }
    }

    async function submitPin() {
      const pin = document.getElementById('pinInput').value.trim();
      const errBox = document.getElementById('pinErrorMsg');
      errBox.classList.add('hidden');

      const res = await checkAccess(pin);
      if (res.valid) {
        localStorage.setItem('tep_demo_pin', pin);
        document.getElementById('demoLockModal').classList.add('hidden');
        document.getElementById('demoClientBadge').innerText = res.client_name;
        document.getElementById('demoExpiresBadge').innerText = res.message;
      } else {
        errBox.innerText = res.message || "Неверный PIN-код";
        errBox.classList.remove('hidden');
      }
    }

    function logoutDemo() {
      localStorage.removeItem('tep_demo_pin');
      document.getElementById('pinInput').value = '';
      document.getElementById('demoLockModal').classList.remove('hidden');
      lucide.createIcons();
    }

    // ================= REAL-TIME DATA SYNC =================
    async function fetchLiveData() {
      try {
        const res = await fetch('/api/data');
        if (!res.ok) return;
        const data = await res.json();
        applyLiveData(data);
      } catch(e) {
        console.warn("[LiveSync] Failed to fetch data:", e);
      }
    }

    function applyLiveData(data) {
      if (!data) return;
      
      // Update Finance
      if (data.finance) {
        const elBal = document.getElementById('kpi-balance');
        if (elBal && data.finance.balance_actual) {
          elBal.innerText = Number(data.finance.balance_actual).toLocaleString('ru-RU') + ' ₽';
        }
        const elInc = document.getElementById('kpi-income');
        if (elInc && data.finance.income_actual) {
          elInc.innerText = Number(data.finance.income_actual).toLocaleString('ru-RU') + ' ₽';
        }
      }

      // Update Payroll
      if (data.payroll) {
        const elPaid = document.getElementById('kpi-fio-paid');
        if (elPaid && data.payroll.paid_actual) {
          elPaid.innerText = Number(data.payroll.paid_actual).toLocaleString('ru-RU') + ' ₽';
        }
      }

      // Update Header Timestamp
      const syncBadge = document.querySelector('.badge-pulse span:last-child');
      if (syncBadge && data.updated_at) {
        syncBadge.innerText = 'Обновлено: ' + data.updated_at.split(' ')[1];
      }
    }

    async function triggerManualSync() {
      const btn = document.getElementById('manualSyncBtn');
      const icon = document.getElementById('syncIcon');
      const text = document.getElementById('syncText');

      icon.classList.add('animate-spin');
      text.innerText = 'Опрос Google Drive...';

      try {
        const res = await fetch('/api/refresh', { method: 'POST' });
        const json = await res.json();
        if (json.data) {
          applyLiveData(json.data);
          text.innerText = 'Синхронизировано!';
        } else {
          text.innerText = 'Готово';
        }
      } catch(e) {
        text.innerText = 'Ошибка связи';
      }

      setTimeout(() => {
        icon.classList.remove('animate-spin');
        text.innerText = 'Обновить данные';
      }, 1500);
    }

    // Init on Page Load
    document.addEventListener('DOMContentLoaded', async () => {
      // 1. Check URL param ?pin=... or localStorage
      const urlParams = new URLSearchParams(window.location.search);
      const urlPin = urlParams.get('pin');
      const savedPin = urlPin || localStorage.getItem('tep_demo_pin') || '2026';

      const res = await checkAccess(savedPin);
      if (res.valid) {
        localStorage.setItem('tep_demo_pin', savedPin);
        document.getElementById('demoClientBadge').innerText = res.client_name;
        document.getElementById('demoExpiresBadge').innerText = res.message;
        document.getElementById('demoLockModal').classList.add('hidden');
      } else {
        document.getElementById('demoLockModal').classList.remove('hidden');
        if (res.expired) {
          const errBox = document.getElementById('pinErrorMsg');
          errBox.innerText = res.message;
          errBox.classList.remove('hidden');
        }
      }

      // 2. Fetch live data & start 30s polling
      fetchLiveData();
      setInterval(fetchLiveData, 30000);
    });
  </script>
'''

html = html.replace("</body>", live_js + "\n</body>")

with open(path, "w", encoding="utf-8") as f:
    f.write(html)

print("[Patch] Live Sync and Demo Access Gate successfully added to index.html!")
