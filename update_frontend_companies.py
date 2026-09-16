path = "/Users/user/.gemini/antigravity/scratch/tep_dashboard/index.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()

# Update company options in header
old_select = '''        <select id="companySelect" class="bg-brand-card border border-brand-border text-slate-200 text-xs rounded-lg px-3 py-1.5 focus:ring-1 focus:ring-cyan-500 outline-none">
          <option value="all" selected>Группа компаний (Все)</option>
          <option value="tep">ООО «ТЭП»</option>
          <option value="smu">ООО «СМУ Промстрой»</option>
        </select>'''

new_select = '''        <select id="companySelect" onchange="onCompanyChange()" class="bg-brand-card border border-brand-border text-slate-200 text-xs rounded-lg px-3 py-1.5 focus:ring-1 focus:ring-cyan-500 outline-none">
          <option value="all" selected>Группа компаний (Все)</option>
          <option value="tep">ООО «ТЭП»</option>
          <option value="mpb">ООО «МПБ» / СМУ</option>
        </select>'''

if old_select in html:
    html = html.replace(old_select, new_select)

# Replace applyLiveData logic to handle companies
old_apply = '''    function applyLiveData(data) {
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
      }'''

new_apply = '''    let cachedGlobalData = null;

    function onCompanyChange() {
      if (cachedGlobalData) {
        applyLiveData(cachedGlobalData);
      }
    }

    function applyLiveData(data) {
      if (!data) return;
      cachedGlobalData = data;
      
      const comp = document.getElementById('companySelect') ? document.getElementById('companySelect').value : 'all';
      let fin = data.finance;
      if (data.finance_by_company && data.finance_by_company[comp]) {
        fin = data.finance_by_company[comp];
      }

      // Update Finance
      if (fin) {
        const elBal = document.getElementById('kpi-balance');
        if (elBal && fin.balance_actual !== undefined) {
          elBal.innerText = Number(fin.balance_actual).toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' ₽';
        }
        const elInc = document.getElementById('kpi-income');
        if (elInc && fin.income_actual !== undefined) {
          elInc.innerText = Number(fin.income_actual).toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' ₽';
        }
        // Plan text
        const elPlan = elBal ? elBal.parentElement.nextElementSibling.querySelector('span:first-child') : null;
        if (elPlan && fin.balance_plan !== undefined) {
          elPlan.innerText = 'План: ' + Number(fin.balance_plan).toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' ₽';
        }
      }'''

if old_apply in html:
    html = html.replace(old_apply, new_apply)
else:
    print("Warning: old_apply pattern not found directly, replacing via function signature...")
    import re
    html = re.sub(r'function applyLiveData\(data\) \{[\s\S]*?if \(data\.finance\) \{[\s\S]*?\}\s*\}', new_apply + '\n      }', html)

with open(path, "w", encoding="utf-8") as f:
    f.write(html)

print("Updated index.html with live company switching logic!")
