import re

path = "/Users/user/.gemini/antigravity/scratch/tep_dashboard/index.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Add floating personal agent widget and update AI tab with personal executive assistant features

personal_widget = '''
  <!-- ================= FLOATING PERSONAL AGENT BUTTON ================= -->
  <div class="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-2">
    <!-- Mini Popup hint -->
    <div id="agentFloatingHint" class="px-3.5 py-2 rounded-xl bg-cyan-950/90 border border-cyan-700/60 text-cyan-200 text-xs shadow-2xl backdrop-blur-md flex items-center gap-2 animate-bounce">
      <span class="w-2 h-2 rounded-full bg-cyan-400 animate-ping"></span>
      <span><b>Личный агент руководителя</b> на связи</span>
      <button onclick="document.getElementById('agentFloatingHint').style.display='none'" class="text-slate-400 hover:text-white ml-1">×</button>
    </div>

    <!-- Floating Trigger Button -->
    <button onclick="togglePersonalAgentDrawer()" class="w-14 h-14 rounded-2xl bg-gradient-to-tr from-cyan-600 via-blue-600 to-indigo-600 text-white shadow-xl shadow-cyan-500/30 flex items-center justify-center hover:scale-105 active:scale-95 transition group border border-white/20">
      <i data-lucide="bot" class="w-7 h-7 group-hover:rotate-12 transition transform"></i>
    </button>
  </div>

  <!-- ================= PERSONAL AGENT DRAWER / MODAL ================= -->
  <div id="personalAgentDrawer" class="fixed inset-y-0 right-0 w-full sm:w-[460px] bg-[#0F172A]/98 border-l border-brand-border z-50 shadow-2xl backdrop-blur-xl transform translate-x-full transition-transform duration-300 flex flex-col">
    <!-- Drawer Header -->
    <div class="p-5 border-b border-brand-border flex items-center justify-between bg-brand-card/50">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center text-white shadow-md">
          <i data-lucide="user-check" class="w-5 h-5"></i>
        </div>
        <div>
          <h3 class="font-bold text-white text-sm">Личный агент руководителя</h3>
          <p class="text-[11px] text-emerald-400 flex items-center gap-1.5 font-medium">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> Mac mini Core • Почта • WhatsApp • Документы
          </p>
        </div>
      </div>
      <button onclick="togglePersonalAgentDrawer()" class="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-brand-card transition">
        <i data-lucide="x" class="w-5 h-5"></i>
      </button>
    </div>

    <!-- Mode Switcher -->
    <div class="px-5 py-3 border-b border-brand-border/60 bg-brand-card/30 flex gap-2">
      <button id="modeBtnCorp" onclick="setAgentMode('corp')" class="flex-1 py-1.5 rounded-lg bg-cyan-950 text-cyan-300 border border-cyan-800 text-xs font-medium flex items-center justify-center gap-1.5">
        <i data-lucide="building" class="w-3.5 h-3.5"></i> Корпоративный
      </button>
      <button id="modeBtnPersonal" onclick="setAgentMode('personal')" class="flex-1 py-1.5 rounded-lg bg-brand-card text-slate-400 border border-brand-border text-xs font-medium flex items-center justify-center gap-1.5 hover:text-white">
        <i data-lucide="user" class="w-3.5 h-3.5"></i> Личный помощник
      </button>
    </div>

    <!-- Quick Action Chips for Executive -->
    <div class="p-4 border-b border-brand-border/60 bg-brand-card/10 space-y-2">
      <span class="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Быстрые поручения директора:</span>
      <div class="flex flex-wrap gap-1.5 text-[11px]">
        <button onclick="sendDrawerPrompt('mail')" class="px-2.5 py-1 rounded-lg bg-brand-card hover:bg-cyan-950/60 border border-brand-border text-slate-200 hover:text-cyan-300 transition flex items-center gap-1">
          ✉️ Проверь почту (Северсталь)
        </button>
        <button onclick="sendDrawerPrompt('whatsapp')" class="px-2.5 py-1 rounded-lg bg-brand-card hover:bg-cyan-950/60 border border-brand-border text-slate-200 hover:text-cyan-300 transition flex items-center gap-1">
          💬 Отправь WhatsApp прорабу
        </button>
        <button onclick="sendDrawerPrompt('report')" class="px-2.5 py-1 rounded-lg bg-brand-card hover:bg-cyan-950/60 border border-brand-border text-slate-200 hover:text-cyan-300 transition flex items-center gap-1">
          📄 Сформируй Word-отчет
        </button>
        <button onclick="sendDrawerPrompt('spotlight')" class="px-2.5 py-1 rounded-lg bg-brand-card hover:bg-cyan-950/60 border border-brand-border text-slate-200 hover:text-cyan-300 transition flex items-center gap-1">
          🔍 Найди смету на Mac
        </button>
      </div>
    </div>

    <!-- Chat Messages Container -->
    <div id="drawerChatHistory" class="flex-1 overflow-y-auto p-4 space-y-3.5 text-xs">
      <div class="flex items-start gap-2.5">
        <div class="w-7 h-7 rounded-lg bg-cyan-950 text-cyan-400 flex items-center justify-center shrink-0 border border-cyan-800/60">
          <i data-lucide="bot" class="w-4 h-4"></i>
        </div>
        <div class="p-3 rounded-2xl rounded-tl-none bg-brand-card border border-brand-border text-slate-200 leading-relaxed max-w-[85%]">
          Добрый день! Я ваш личный ИИ-ассистент руководителя.<br><br>
          В отличие от обычных чат-ботов, я подключен напрямую к вашей операционной системе Mac mini, почтовым ящикам, Google Диску и WhatsApp.<br><br>
          <b>Чем могу помочь прямо сейчас?</b>
        </div>
      </div>
    </div>

    <!-- Drawer Input Area -->
    <div class="p-4 border-t border-brand-border bg-brand-card/40">
      <div class="flex gap-2">
        <input type="text" id="drawerUserInput" placeholder="Дать поручение агенту..." 
               class="flex-1 bg-brand-card border border-brand-border rounded-xl px-3.5 py-2.5 text-xs text-white placeholder:text-slate-500 focus:outline-none focus:border-cyan-500"
               onkeydown="if(event.key === 'Enter') sendDrawerQuery()">
        <button onclick="sendDrawerQuery()" class="px-4 py-2.5 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold flex items-center gap-1.5 transition shadow-lg shadow-cyan-600/20">
          <i data-lucide="send" class="w-3.5 h-3.5"></i>
        </button>
      </div>
    </div>
  </div>
'''

# Replace before </body>
content = content.replace("</body>", personal_widget + "\n</body>")

# Add JS functions for drawer
js_code = '''
    // Personal Agent Drawer Handlers
    let currentAgentMode = 'corp';

    function togglePersonalAgentDrawer() {
      const drawer = document.getElementById('personalAgentDrawer');
      const isClosed = drawer.classList.contains('translate-x-full');
      if (isClosed) {
        drawer.classList.remove('translate-x-full');
      } else {
        drawer.classList.add('translate-x-full');
      }
      lucide.createIcons();
    }

    function setAgentMode(mode) {
      currentAgentMode = mode;
      const btnCorp = document.getElementById('modeBtnCorp');
      const btnPers = document.getElementById('modeBtnPersonal');
      if (mode === 'corp') {
        btnCorp.className = "flex-1 py-1.5 rounded-lg bg-cyan-950 text-cyan-300 border border-cyan-800 text-xs font-medium flex items-center justify-center gap-1.5";
        btnPers.className = "flex-1 py-1.5 rounded-lg bg-brand-card text-slate-400 border border-brand-border text-xs font-medium flex items-center justify-center gap-1.5 hover:text-white";
      } else {
        btnPers.className = "flex-1 py-1.5 rounded-lg bg-purple-950 text-purple-300 border border-purple-800 text-xs font-medium flex items-center justify-center gap-1.5";
        btnCorp.className = "flex-1 py-1.5 rounded-lg bg-brand-card text-slate-400 border border-brand-border text-xs font-medium flex items-center justify-center gap-1.5 hover:text-white";
      }
    }

    const drawerPresetResponses = {
      mail: `<b>✉️ Проверка входящих писем (Apple Mail & Gmail):</b><br><br>
• Найдено <b>3 новых письма</b> по контракту с ПАО «Северсталь» (Куратор: Смирнов А.В.):<br>
  1. <i>«Согласование изменений кабельного журнала по объекту 101»</i> — скан вложен в папку ТЭП на Google Диске.<br>
  2. <i>«Акт сверки расчетов за август»</i> — передано в бухгалтерию.<br>
  3. Уведомление о готовности пропуска на промплощадку для бригады сварщиков.<br>
• Подготовить проект ответного письма по объекту 101?`,

      whatsapp: `<b>💬 Автономная отправка сообщения в WhatsApp:</b><br><br>
• <b>Получатель:</b> Главный инженер Лещинин А.В. (контакт из адресной книги Mac).<br>
• <b>Текст поручения:</b> <i>«Александр Владимирович, по объекту 101 устраните отставание 4 дня до четверга. Протокол согласован куратором цеха.»</i><br>
• <b>Статус:</b> Готово к отправке в фоновом режиме через локальный шлюз WhatsApp на Mac mini. <b>[Отправить прямо сейчас]</b>`,

      report: `<b>📄 Генерация Word-документа:</b><br><br>
• Создан документ: <code>/Users/user/Desktop/Отчет_СМР_ТЭП_Сентябрь_2026.docx</code>.<br>
• В отчет включены: сводная таблица выполнения по 4 объектам, расчеты ФОТ и статус подписания КС-2.<br>
• Ссылка для скачивания подготовлена. Открыть файл на Mac?`,

      spotlight: `<b>🔍 Поиск файлов через системный Spotlight Mac:</b><br><br>
• Найдено 4 файла по запросу <i>«Смета Кислородный цех»</i>:<br>
  1. <code>~/Documents/Сметная документация/Смета-расчет М390414_v3.xlsx</code> (изменен 3 дня назад)<br>
  2. <code>~/Downloads/ТКП ТЭП-1000-24.pdf</code><br>
• Открыть файл в Excel?`
    };

    function sendDrawerPrompt(key) {
      const history = document.getElementById('drawerChatHistory');
      
      const promptTitles = {
        mail: "Проверь входящую почту по объектам Северстали",
        whatsapp: "Отправь поручение в WhatsApp главному инженеру",
        report: "Сформируй официальный Word-отчет за сентябрь",
        spotlight: "Найди на Mac смету по Кислородному цеху"
      };

      // Add user message
      const uDiv = document.createElement('div');
      uDiv.className = 'flex items-start gap-2.5 justify-end';
      uDiv.innerHTML = `
        <div class="p-3 rounded-2xl rounded-tr-none bg-cyan-950/70 border border-cyan-800/80 text-slate-100 max-w-[85%] leading-relaxed">
          ${promptTitles[key]}
        </div>
        <div class="w-7 h-7 rounded-lg bg-blue-600 text-white flex items-center justify-center shrink-0">
          <i data-lucide="user" class="w-4 h-4"></i>
        </div>
      `;
      history.appendChild(uDiv);
      history.scrollTop = history.scrollHeight;
      lucide.createIcons();

      // Bot response
      setTimeout(() => {
        const bDiv = document.createElement('div');
        bDiv.className = 'flex items-start gap-2.5';
        bDiv.innerHTML = `
          <div class="w-7 h-7 rounded-lg bg-cyan-950 text-cyan-400 flex items-center justify-center shrink-0 border border-cyan-800/60">
            <i data-lucide="bot" class="w-4 h-4"></i>
          </div>
          <div class="p-3 rounded-2xl rounded-tl-none bg-brand-card border border-brand-border text-slate-200 leading-relaxed max-w-[85%]">
            ${drawerPresetResponses[key]}
          </div>
        `;
        history.appendChild(bDiv);
        history.scrollTop = history.scrollHeight;
        lucide.createIcons();
      }, 500);
    }

    function sendDrawerQuery() {
      const input = document.getElementById('drawerUserInput');
      const text = input.value.trim();
      if (!text) return;

      const history = document.getElementById('drawerChatHistory');

      const uDiv = document.createElement('div');
      uDiv.className = 'flex items-start gap-2.5 justify-end';
      uDiv.innerHTML = `
        <div class="p-3 rounded-2xl rounded-tr-none bg-cyan-950/70 border border-cyan-800/80 text-slate-100 max-w-[85%] leading-relaxed">
          ${text}
        </div>
        <div class="w-7 h-7 rounded-lg bg-blue-600 text-white flex items-center justify-center shrink-0">
          <i data-lucide="user" class="w-4 h-4"></i>
        </div>
      `;
      history.appendChild(uDiv);
      input.value = '';
      history.scrollTop = history.scrollHeight;
      lucide.createIcons();

      setTimeout(() => {
        const bDiv = document.createElement('div');
        bDiv.className = 'flex items-start gap-2.5';
        let resp = `Принято к исполнению! Запрос обработан вашим локальным агентом на Mac mini. Синхронизировано с базой данных ТЭП и почтовым клиентом.`;
        const lower = text.toLowerCase();
        if (lower.includes("почт") || lower.includes("письм")) {
          resp = `Проверил входящую почту по подключенным ящикам. Новых срочных запросов от заказчиков не обнаружено. Последнее письмо от «Северстали» обработано сегодня в 14:15.`;
        } else if (lower.includes("ватсап") || lower.includes("whatsapp")) {
          resp = `Шлюз WhatsApp активен. Кому отправить сообщение и какой текст подготовить?`;
        } else if (lower.includes("файл") || lower.includes("найти") || lower.includes("документ")) {
          resp = `Запустил поиск через Spotlight на Mac. Найдено 2 релевантных документа в папке <code>~/Documents/СМУ Промстрой</code>.`;
        }
        bDiv.innerHTML = `
          <div class="w-7 h-7 rounded-lg bg-cyan-950 text-cyan-400 flex items-center justify-center shrink-0 border border-cyan-800/60">
            <i data-lucide="bot" class="w-4 h-4"></i>
          </div>
          <div class="p-3 rounded-2xl rounded-tl-none bg-brand-card border border-brand-border text-slate-200 leading-relaxed max-w-[85%]">
            ${resp}
          </div>
        `;
        history.appendChild(bDiv);
        history.scrollTop = history.scrollHeight;
        lucide.createIcons();
      }, 600);
    }
'''

content = content.replace("</body>", f"<script>{js_code}</script>\n</body>")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated index.html with Personal AI Agent successfully!")
