"""
CIPHER Investment Tools Installer
Run from inside cipher_app folder:
    python add_investment_tools.py

Adds 5 new tabs to the director dashboard:
  1. Benchmarks & Attribution
  2. Market Data
  3. Opportunity Pipeline
  4. Due Diligence
  5. Report Builder
"""

import os, shutil, sys

HTML_PATH = os.path.join("templates", "index.html")

def patch():
    if not os.path.exists(HTML_PATH):
        print(f"ERROR: Could not find {HTML_PATH}")
        sys.exit(1)

    with open(HTML_PATH, encoding='utf-8') as f:
        c = f.read()

    original = c

    # ── 1. ADD NAV ITEMS ──
    old_nav = '    <div class="nav-section-label">INTELLIGENCE</div>'
    new_nav = '''    <div class="nav-section-label">INVESTMENT TOOLS</div>
    <div class="nav-item" onclick="dirTab(this,'dir-benchmark')"><span class="nav-dot"></span>Benchmarks</div>
    <div class="nav-item" onclick="dirTab(this,'dir-market')"><span class="nav-dot"></span>Market Data</div>
    <div class="nav-item" onclick="dirTab(this,'dir-pipeline')"><span class="nav-dot"></span>Opportunity Pipeline</div>
    <div class="nav-item" onclick="dirTab(this,'dir-diligence')"><span class="nav-dot"></span>Due Diligence</div>
    <div class="nav-item" onclick="dirTab(this,'dir-builder')"><span class="nav-dot"></span>Report Builder</div>
    <div class="nav-section-label">INTELLIGENCE</div>'''

    if 'dir-benchmark' not in c:
        c = c.replace(old_nav, new_nav, 1)
        print("  Added investment tools nav items")
    else:
        print("  Nav items already present, skipping")

    # ── 2. UPDATE dirTab ──
    old_tabs = "['dir-overview','dir-submissions','dir-analytics','dir-exposure','dir-liquidity','dir-private','dir-ai','dir-report']"
    new_tabs = "['dir-overview','dir-submissions','dir-analytics','dir-exposure','dir-liquidity','dir-private','dir-benchmark','dir-market','dir-pipeline','dir-diligence','dir-builder','dir-ai','dir-report']"
    if old_tabs in c:
        c = c.replace(old_tabs, new_tabs, 1)
        print("  Updated dirTab function")

    # ── 3. ADD HTML TABS ──
    new_html = '''
      <!-- BENCHMARKS & ATTRIBUTION TAB -->
      <div id="dir-benchmark" style="display:none">
        <div class="cards" style="grid-template-columns:repeat(4,1fr)">
          <div class="card success"><div class="card-label">PORTFOLIO RETURN (YTD)</div><div class="card-value">+8.4%</div><div class="card-sub">Net of fees</div></div>
          <div class="card"><div class="card-label">S&P 500 (YTD)</div><div class="card-value">+6.2%</div><div class="card-sub">Benchmark</div></div>
          <div class="card"><div class="card-label">MSCI WORLD (YTD)</div><div class="card-value">+5.8%</div><div class="card-sub">Benchmark</div></div>
          <div class="card success"><div class="card-label">ALPHA GENERATED</div><div class="card-value">+2.2%</div><div class="card-sub">vs S&P 500</div></div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px;">
          <div class="table-wrap" style="padding:24px;border-radius:12px;">
            <div class="section-title" style="margin-bottom:16px;">PORTFOLIO vs BENCHMARKS</div>
            <canvas id="chart-benchmark" height="240"></canvas>
          </div>
          <div class="table-wrap" style="padding:24px;border-radius:12px;">
            <div class="section-title" style="margin-bottom:16px;">RETURN ATTRIBUTION BY ASSET CLASS</div>
            <canvas id="chart-attribution" height="240"></canvas>
          </div>
        </div>
        <div class="section-header"><div class="section-title">ATTRIBUTION ANALYSIS</div></div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>ASSET CLASS / MANAGER</th><th>WEIGHT</th><th>RETURN</th><th>CONTRIBUTION</th><th>BENCHMARK</th><th>ACTIVE RETURN</th></tr></thead>
            <tbody>
              <tr><td>Public Equity</td><td>33.8%</td><td>+11.2%</td><td style="color:#2e7d32">+3.79%</td><td>+9.4%</td><td style="color:#2e7d32">+1.8%</td></tr>
              <tr><td>Private Equity</td><td>25.3%</td><td>+9.8%</td><td style="color:#2e7d32">+2.48%</td><td>+8.1%</td><td style="color:#2e7d32">+1.7%</td></tr>
              <tr><td>Fixed Income</td><td>19.9%</td><td>+4.1%</td><td style="color:#2e7d32">+0.82%</td><td>+3.8%</td><td style="color:#2e7d32">+0.3%</td></tr>
              <tr><td>Real Assets</td><td>14.6%</td><td>+6.7%</td><td style="color:#2e7d32">+0.98%</td><td>+5.9%</td><td style="color:#2e7d32">+0.8%</td></tr>
              <tr><td>Operations</td><td>6.4%</td><td>-1.2%</td><td style="color:#e74c3c">-0.08%</td><td>+2.0%</td><td style="color:#e74c3c">-3.2%</td></tr>
              <tr style="font-weight:bold;background:#f0f4fa"><td>TOTAL PORTFOLIO</td><td>100%</td><td>+8.4%</td><td style="color:#2e7d32">+8.4%</td><td>+6.2%</td><td style="color:#2e7d32">+2.2%</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- MARKET DATA TAB -->
      <div id="dir-market" style="display:none">
        <div class="cards" style="grid-template-columns:repeat(4,1fr)">
          <div class="card"><div class="card-label">FED FUNDS RATE</div><div class="card-value">4.75%</div><div class="card-sub">Last set Mar 2026</div></div>
          <div class="card"><div class="card-label">10-YR TREASURY</div><div class="card-value">4.32%</div><div class="card-sub">As of Q2 2026</div></div>
          <div class="card danger"><div class="card-label">CPI INFLATION (YOY)</div><div class="card-value">3.1%</div><div class="card-sub">Above 2% target</div></div>
          <div class="card"><div class="card-label">GDP GROWTH (YOY)</div><div class="card-value">2.4%</div><div class="card-sub">Q1 2026 estimate</div></div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px;">
          <div class="table-wrap" style="padding:24px;border-radius:12px;">
            <div class="section-title" style="margin-bottom:16px;">MAJOR INDICES (YTD)</div>
            <canvas id="chart-indices" height="240"></canvas>
          </div>
          <div class="table-wrap" style="padding:24px;border-radius:12px;">
            <div class="section-title" style="margin-bottom:16px;">INTEREST RATE ENVIRONMENT</div>
            <canvas id="chart-rates" height="240"></canvas>
          </div>
        </div>
        <div class="section-header"><div class="section-title">MARKET REFERENCE DATA</div></div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>INDEX / INDICATOR</th><th>CURRENT</th><th>Q1 2026</th><th>Q4 2025</th><th>YTD CHANGE</th></tr></thead>
            <tbody>
              <tr><td>S&P 500</td><td>5,842</td><td>5,611</td><td>5,424</td><td style="color:#2e7d32">+6.2%</td></tr>
              <tr><td>Russell 2000</td><td>2,184</td><td>2,098</td><td>2,041</td><td style="color:#2e7d32">+3.8%</td></tr>
              <tr><td>MSCI World</td><td>3,612</td><td>3,481</td><td>3,402</td><td style="color:#2e7d32">+5.8%</td></tr>
              <tr><td>Bloomberg US Agg</td><td>2,241</td><td>2,198</td><td>2,176</td><td style="color:#2e7d32">+2.1%</td></tr>
              <tr><td>VIX (Volatility)</td><td>18.4</td><td>22.1</td><td>16.8</td><td style="color:#e74c3c">+9.5%</td></tr>
              <tr><td>Gold ($/oz)</td><td>$2,418</td><td>$2,312</td><td>$2,198</td><td style="color:#2e7d32">+10.0%</td></tr>
              <tr><td>USD Index (DXY)</td><td>104.2</td><td>106.8</td><td>108.1</td><td style="color:#e74c3c">-3.6%</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- OPPORTUNITY PIPELINE TAB -->
      <div id="dir-pipeline" style="display:none">
        <div class="cards" style="grid-template-columns:repeat(4,1fr)">
          <div class="card"><div class="card-label">TOTAL OPPORTUNITIES</div><div class="card-value">12</div><div class="card-sub">In active pipeline</div></div>
          <div class="card"><div class="card-label">UNDER REVIEW</div><div class="card-value">5</div><div class="card-sub">Pending IC decision</div></div>
          <div class="card success"><div class="card-label">APPROVED (YTD)</div><div class="card-value">3</div><div class="card-sub">Total: $24.5M committed</div></div>
          <div class="card danger"><div class="card-label">REJECTED (YTD)</div><div class="card-value">4</div><div class="card-sub">Did not meet criteria</div></div>
        </div>
        <div class="section-header" style="margin-top:8px;">
          <div class="section-title">DEAL PIPELINE</div>
          <button class="btn-report" onclick="showAddDeal()">+ ADD OPPORTUNITY</button>
        </div>

        <!-- Add Deal Form -->
        <div id="add-deal-form" style="display:none;background:#fff;border-radius:12px;padding:28px;margin-bottom:20px;box-shadow:0 1px 4px rgba(10,36,114,0.08);">
          <div class="section-title" style="margin-bottom:16px;">NEW INVESTMENT OPPORTUNITY</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div class="input-group"><label>OPPORTUNITY NAME</label><input type="text" id="deal-name" placeholder="e.g. Apex Growth Fund IV"/></div>
            <div class="input-group"><label>FIRM / SPONSOR</label><input type="text" id="deal-firm" placeholder="e.g. Apex Capital Partners"/></div>
            <div class="input-group"><label>ASSET CLASS</label><select id="deal-class"><option>Private Equity</option><option>Venture Capital</option><option>Real Estate</option><option>Fixed Income</option><option>Public Equity</option><option>Infrastructure</option><option>Other</option></select></div>
            <div class="input-group"><label>DEAL SIZE</label><input type="text" id="deal-size" placeholder="e.g. $10M commitment"/></div>
            <div class="input-group"><label>EXPECTED CLOSE</label><input type="text" id="deal-close" placeholder="e.g. Q3 2026"/></div>
            <div class="input-group"><label>SUBMITTED BY</label><input type="text" id="deal-submitter" placeholder="Manager name"/></div>
          </div>
          <div class="input-group" style="margin-top:12px;"><label>NOTES</label><textarea id="deal-notes" placeholder="Brief description of the opportunity..." style="width:100%;padding:10px;border:1.5px solid #dde6f5;border-radius:8px;font-family:Georgia,serif;min-height:70px;resize:vertical;"></textarea></div>
          <div style="display:flex;gap:12px;margin-top:16px;">
            <button class="btn-report" onclick="addDeal()">ADD TO PIPELINE</button>
            <button class="btn-report" style="background:#f0f4fa;color:#0A2472;" onclick="document.getElementById('add-deal-form').style.display='none'">CANCEL</button>
          </div>
        </div>

        <div class="table-wrap">
          <table>
            <thead><tr><th>OPPORTUNITY</th><th>FIRM</th><th>ASSET CLASS</th><th>SIZE</th><th>EXPECTED CLOSE</th><th>SUBMITTED BY</th><th>STATUS</th><th>ACTION</th></tr></thead>
            <tbody id="pipeline-tbody">
              <tr><td>Apex Growth Fund IV</td><td>Apex Capital</td><td>Private Equity</td><td>$10.0M</td><td>Q3 2026</td><td>Sarah Johnson</td><td><span class="badge flagged">UNDER REVIEW</span></td><td><button class="btn-report" style="padding:4px 10px;font-size:9px;" onclick="moveDeal(this,'APPROVED')">Approve</button> <button class="btn-report" style="padding:4px 10px;font-size:9px;background:#e74c3c;" onclick="moveDeal(this,'REJECTED')">Reject</button></td></tr>
              <tr><td>Meridian RE Fund III</td><td>Meridian Capital</td><td>Real Estate</td><td>$7.5M</td><td>Q4 2026</td><td>Mike Chen</td><td><span class="badge flagged">UNDER REVIEW</span></td><td><button class="btn-report" style="padding:4px 10px;font-size:9px;" onclick="moveDeal(this,'APPROVED')">Approve</button> <button class="btn-report" style="padding:4px 10px;font-size:9px;background:#e74c3c;" onclick="moveDeal(this,'REJECTED')">Reject</button></td></tr>
              <tr><td>Blueridge Series B</td><td>Blueridge Ventures</td><td>Venture Capital</td><td>$3.0M</td><td>Q2 2026</td><td>Priya Patel</td><td><span class="badge submitted">APPROVED</span></td><td>—</td></tr>
              <tr><td>ClearPath Infra II</td><td>ClearPath Partners</td><td>Infrastructure</td><td>$12.0M</td><td>Q1 2027</td><td>Sarah Johnson</td><td><span class="badge missing">REJECTED</span></td><td>—</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- DUE DILIGENCE TAB -->
      <div id="dir-diligence" style="display:none">
        <div class="section-header">
          <div class="section-title">DUE DILIGENCE CHECKLISTS</div>
          <select id="dd-select" onchange="loadDDChecklist(this.value)" style="padding:8px 14px;border:1.5px solid #dde6f5;border-radius:8px;font-family:Georgia,serif;color:#0A2472;">
            <option value="">Select Opportunity</option>
            <option value="apex">Apex Growth Fund IV</option>
            <option value="meridian">Meridian RE Fund III</option>
          </select>
        </div>
        <div id="dd-content" style="background:#fff;border-radius:12px;padding:28px;box-shadow:0 1px 4px rgba(10,36,114,0.08);">
          <div style="text-align:center;color:#aab8d0;font-family:'Courier New',monospace;font-size:12px;padding:40px;">Select an opportunity above to load its due diligence checklist.</div>
        </div>
      </div>

      <!-- REPORT BUILDER TAB -->
      <div id="dir-builder" style="display:none">
        <div class="section-header"><div class="section-title">REPORT BUILDER</div></div>
        <div style="display:grid;grid-template-columns:1fr 2fr;gap:24px;">
          <div style="background:#fff;border-radius:12px;padding:24px;box-shadow:0 1px 4px rgba(10,36,114,0.08);">
            <div class="section-title" style="margin-bottom:16px;">SELECT SECTIONS</div>
            <div style="display:flex;flex-direction:column;gap:10px;">
              <label style="display:flex;align-items:center;gap:10px;font-size:13px;color:#0A2472;cursor:pointer;"><input type="checkbox" id="rb-summary" checked> Executive Summary</label>
              <label style="display:flex;align-items:center;gap:10px;font-size:13px;color:#0A2472;cursor:pointer;"><input type="checkbox" id="rb-perf" checked> Portfolio Performance</label>
              <label style="display:flex;align-items:center;gap:10px;font-size:13px;color:#0A2472;cursor:pointer;"><input type="checkbox" id="rb-benchmark" checked> Benchmark Comparison</label>
              <label style="display:flex;align-items:center;gap:10px;font-size:13px;color:#0A2472;cursor:pointer;"><input type="checkbox" id="rb-attribution"> Attribution Analysis</label>
              <label style="display:flex;align-items:center;gap:10px;font-size:13px;color:#0A2472;cursor:pointer;"><input type="checkbox" id="rb-exposure"> Exposure Analysis</label>
              <label style="display:flex;align-items:center;gap:10px;font-size:13px;color:#0A2472;cursor:pointer;"><input type="checkbox" id="rb-liquidity"> Liquidity Summary</label>
              <label style="display:flex;align-items:center;gap:10px;font-size:13px;color:#0A2472;cursor:pointer;"><input type="checkbox" id="rb-private"> Private Markets</label>
              <label style="display:flex;align-items:center;gap:10px;font-size:13px;color:#0A2472;cursor:pointer;"><input type="checkbox" id="rb-pipeline"> Opportunity Pipeline</label>
              <label style="display:flex;align-items:center;gap:10px;font-size:13px;color:#0A2472;cursor:pointer;"><input type="checkbox" id="rb-market"> Market Data</label>
            </div>
            <div style="margin-top:20px;">
              <div class="input-group" style="margin-bottom:12px;"><label>REPORT TITLE</label><input type="text" id="rb-title" value="Investment Portfolio Report — Q2 2026" style="width:100%;padding:10px 12px;border:1.5px solid #dde6f5;border-radius:8px;font-family:Georgia,serif;color:#0A2472;"/></div>
              <div class="input-group"><label>REPORTING PERIOD</label><select id="rb-period" style="width:100%;padding:10px 12px;border:1.5px solid #dde6f5;border-radius:8px;font-family:Georgia,serif;color:#0A2472;"><option>Q2 2026</option><option>Q1 2026</option><option>Q4 2025</option><option>Q3 2025</option></select></div>
            </div>
            <button class="btn-report" style="width:100%;margin-top:20px;padding:12px;" onclick="buildReport()">GENERATE REPORT PREVIEW</button>
          </div>
          <div id="report-preview" style="background:#fff;border-radius:12px;padding:32px;box-shadow:0 1px 4px rgba(10,36,114,0.08);min-height:400px;">
            <div style="text-align:center;color:#aab8d0;font-family:'Courier New',monospace;font-size:12px;padding:60px 0;">Select sections and click Generate Report Preview to see your IC-ready report here.</div>
          </div>
        </div>
      </div>

'''

    anchor = '      <div id="dir-ai" style="display:none">'
    if 'dir-benchmark' not in c:
        c = c.replace(anchor, new_html + anchor, 1)
        print("  Added investment tools HTML tabs")
    else:
        print("  HTML tabs already present, skipping")

    # ── 4. ADD JAVASCRIPT ──
    js = '''
  // ══ INVESTMENT TOOLS JS ══

  // Benchmark charts
  function initBenchmarkCharts() {
    const bCtx = document.getElementById('chart-benchmark');
    if (bCtx && !bCtx.dataset.init) {
      bCtx.dataset.init = '1';
      new Chart(bCtx, { type:'bar', data:{ labels:['Q1 2025','Q2 2025','Q3 2025','Q4 2025','Q1 2026','Q2 2026'], datasets:[
        { label:'Portfolio', data:[2.1,1.8,2.4,1.9,2.2,2.8], backgroundColor:'#0A2472' },
        { label:'S&P 500',   data:[1.4,1.6,1.9,1.2,1.8,2.1], backgroundColor:'#4A90D9' },
        { label:'MSCI World',data:[1.2,1.4,1.7,1.0,1.6,1.9], backgroundColor:'#A8D4F5' }
      ]}, options:{ responsive:true, plugins:{ legend:{ position:'bottom' }}, scales:{ y:{ title:{ display:true, text:'Return (%)' }}}}});
    }
    const aCtx = document.getElementById('chart-attribution');
    if (aCtx && !aCtx.dataset.init) {
      aCtx.dataset.init = '1';
      new Chart(aCtx, { type:'bar', data:{ labels:['Public Eq','Private Eq','Fixed Inc','Real Assets','Operations'], datasets:[
        { label:'Contribution to Return', data:[3.79,2.48,0.82,0.98,-0.08], backgroundColor:['#2e7d32','#2e7d32','#2e7d32','#2e7d32','#e74c3c'] }
      ]}, options:{ responsive:true, plugins:{ legend:{ display:false }}, scales:{ y:{ title:{ display:true, text:'Contribution (%)' }}}}});
    }
  }

  // Market data charts
  function initMarketCharts() {
    const iCtx = document.getElementById('chart-indices');
    if (iCtx && !iCtx.dataset.init) {
      iCtx.dataset.init = '1';
      new Chart(iCtx, { type:'bar', data:{ labels:['S&P 500','Russell 2000','MSCI World','Bloomberg Agg','Portfolio'], datasets:[
        { label:'YTD Return %', data:[6.2,3.8,5.8,2.1,8.4], backgroundColor:['#4A90D9','#4A90D9','#4A90D9','#4A90D9','#0A2472'] }
      ]}, options:{ responsive:true, plugins:{ legend:{ display:false }}, scales:{ y:{ title:{ display:true, text:'YTD Return (%)' }}}}});
    }
    const rCtx = document.getElementById('chart-rates');
    if (rCtx && !rCtx.dataset.init) {
      rCtx.dataset.init = '1';
      new Chart(rCtx, { type:'line', data:{ labels:['Q1 2024','Q2 2024','Q3 2024','Q4 2024','Q1 2025','Q2 2025','Q3 2025','Q4 2025','Q1 2026','Q2 2026'], datasets:[
        { label:'Fed Funds Rate', data:[5.25,5.25,5.00,4.75,4.50,4.25,4.25,4.50,4.75,4.75], borderColor:'#0A2472', tension:0.3 },
        { label:'10-Yr Treasury',  data:[4.20,4.36,4.18,4.57,4.28,4.14,4.22,4.45,4.38,4.32], borderColor:'#4A90D9', tension:0.3 }
      ]}, options:{ responsive:true, plugins:{ legend:{ position:'bottom' }}, scales:{ y:{ title:{ display:true, text:'Rate (%)' }}}}});
    }
  }

  // Pipeline
  function showAddDeal() {
    const f = document.getElementById('add-deal-form');
    f.style.display = f.style.display === 'none' ? 'block' : 'none';
  }

  function addDeal() {
    const name      = document.getElementById('deal-name').value.trim();
    const firm      = document.getElementById('deal-firm').value.trim();
    const cls       = document.getElementById('deal-class').value;
    const size      = document.getElementById('deal-size').value.trim();
    const close     = document.getElementById('deal-close').value.trim();
    const submitter = document.getElementById('deal-submitter').value.trim();
    if (!name || !firm || !size) { alert('Please fill in Name, Firm, and Size.'); return; }
    const tbody = document.getElementById('pipeline-tbody');
    const row = document.createElement('tr');
    row.innerHTML = `<td>${name}</td><td>${firm}</td><td>${cls}</td><td>${size}</td><td>${close || '—'}</td><td>${submitter || '—'}</td><td><span class="badge flagged">UNDER REVIEW</span></td><td><button class="btn-report" style="padding:4px 10px;font-size:9px;" onclick="moveDeal(this,'APPROVED')">Approve</button> <button class="btn-report" style="padding:4px 10px;font-size:9px;background:#e74c3c;" onclick="moveDeal(this,'REJECTED')">Reject</button></td>`;
    tbody.appendChild(row);
    document.getElementById('add-deal-form').style.display = 'none';
    ['deal-name','deal-firm','deal-size','deal-close','deal-submitter','deal-notes'].forEach(id => { const el = document.getElementById(id); if(el) el.value=''; });
  }

  function moveDeal(btn, status) {
    const row = btn.closest('tr');
    const statusCell = row.cells[6];
    const actionCell = row.cells[7];
    statusCell.innerHTML = status === 'APPROVED'
      ? '<span class="badge submitted">APPROVED</span>'
      : '<span class="badge missing">REJECTED</span>';
    actionCell.innerHTML = '—';
  }

  // Due Diligence
  const ddChecklists = {
    apex: { name:'Apex Growth Fund IV', items:[
      { section:'Legal & Compliance', checks:['Fund formation documents reviewed','LP agreement reviewed','Regulatory filings verified','No pending litigation confirmed'] },
      { section:'Investment Strategy', checks:['Investment thesis documented','Target sectors identified','Historical deal flow reviewed','Co-investment rights confirmed'] },
      { section:'Team & Operations', checks:['GP team backgrounds verified','Key person provisions reviewed','Operational infrastructure assessed','Reference checks completed'] },
      { section:'Financial', checks:['Audited financials reviewed','Fee structure documented (2/20)','Waterfall mechanics confirmed','Capital call schedule reviewed'] },
    ]},
    meridian: { name:'Meridian RE Fund III', items:[
      { section:'Legal & Compliance', checks:['Fund structure verified','Real estate licenses confirmed','Environmental assessments reviewed','Title insurance confirmed'] },
      { section:'Property & Assets', checks:['Asset locations reviewed','Occupancy rates documented','Lease terms summarized','Cap rates benchmarked'] },
      { section:'Financial', checks:['Pro forma reviewed','Debt structure analyzed','Distribution waterfall confirmed','Exit strategy documented'] },
    ]}
  };

  const ddProgress = {};

  function loadDDChecklist(key) {
    const container = document.getElementById('dd-content');
    if (!key) { container.innerHTML = '<div style="text-align:center;color:#aab8d0;font-family:Courier New,monospace;font-size:12px;padding:40px;">Select an opportunity above to load its due diligence checklist.</div>'; return; }
    const dd = ddChecklists[key];
    if (!ddProgress[key]) ddProgress[key] = {};
    let html = `<div style="font-size:16px;font-weight:bold;color:#0A2472;margin-bottom:20px;">${dd.name}</div>`;
    dd.items.forEach((section, si) => {
      html += `<div style="margin-bottom:20px;"><div class="section-title" style="margin-bottom:10px;">${section.section}</div>`;
      section.checks.forEach((check, ci) => {
        const id = `${key}-${si}-${ci}`;
        const checked = ddProgress[key][id] ? 'checked' : '';
        html += `<label style="display:flex;align-items:center;gap:10px;font-size:13px;color:#333;margin-bottom:8px;cursor:pointer;"><input type="checkbox" ${checked} onchange="saveDDCheck('${key}','${id}',this.checked)"> ${check}</label>`;
      });
      html += '</div>';
    });
    const total = dd.items.reduce((s,sec) => s + sec.checks.length, 0);
    const done  = Object.values(ddProgress[key]).filter(Boolean).length;
    html += `<div style="margin-top:16px;padding-top:16px;border-top:1px solid #f0f4fa;font-family:Courier New,monospace;font-size:11px;color:#aab8d0;">${done} of ${total} items completed</div>`;
    container.innerHTML = html;
  }

  function saveDDCheck(key, id, val) {
    if (!ddProgress[key]) ddProgress[key] = {};
    ddProgress[key][id] = val;
    const dd = ddChecklists[key];
    const total = dd.items.reduce((s,sec) => s + sec.checks.length, 0);
    const done  = Object.values(ddProgress[key]).filter(Boolean).length;
    const footer = document.querySelector('#dd-content > div:last-child');
    if (footer) footer.textContent = `${done} of ${total} items completed`;
  }

  // Report Builder
  function buildReport() {
    const title  = document.getElementById('rb-title').value;
    const period = document.getElementById('rb-period').value;
    const sections = {
      'Executive Summary':    document.getElementById('rb-summary').checked,
      'Portfolio Performance':document.getElementById('rb-perf').checked,
      'Benchmark Comparison': document.getElementById('rb-benchmark').checked,
      'Attribution Analysis': document.getElementById('rb-attribution').checked,
      'Exposure Analysis':    document.getElementById('rb-exposure').checked,
      'Liquidity Summary':    document.getElementById('rb-liquidity').checked,
      'Private Markets':      document.getElementById('rb-private').checked,
      'Opportunity Pipeline': document.getElementById('rb-pipeline').checked,
      'Market Data':          document.getElementById('rb-market').checked,
    };
    const sectionData = {
      'Executive Summary':    '<p style="font-size:13px;color:#333;line-height:1.8;">The portfolio delivered a net return of <strong>+8.4%</strong> for the period ending ' + period + ', outperforming the S&P 500 benchmark by <strong>+2.2%</strong>. Total portfolio value stands at <strong>$124.6M</strong> across five asset classes. All managers submitted data for this period. No material concerns flagged.</p>',
      'Portfolio Performance':'<table style="width:100%;border-collapse:collapse;font-size:12px;"><thead style="background:#0A2472;color:#fff;"><tr><th style="padding:8px;">Asset Class</th><th>Value</th><th>Return</th><th>Benchmark</th></tr></thead><tbody><tr><td style="padding:8px;border-bottom:1px solid #f0f4fa;">Public Equity</td><td>$42.1M</td><td style="color:#2e7d32">+11.2%</td><td>9.4%</td></tr><tr><td style="padding:8px;border-bottom:1px solid #f0f4fa;">Private Equity</td><td>$31.5M</td><td style="color:#2e7d32">+9.8%</td><td>8.1%</td></tr><tr><td style="padding:8px;border-bottom:1px solid #f0f4fa;">Fixed Income</td><td>$24.8M</td><td style="color:#2e7d32">+4.1%</td><td>3.8%</td></tr><tr><td style="padding:8px;border-bottom:1px solid #f0f4fa;">Real Assets</td><td>$18.2M</td><td style="color:#2e7d32">+6.7%</td><td>5.9%</td></tr><tr><td style="padding:8px;">Operations</td><td>$8.0M</td><td style="color:#e74c3c">-1.2%</td><td>2.0%</td></tr></tbody></table>',
      'Benchmark Comparison': '<table style="width:100%;border-collapse:collapse;font-size:12px;"><thead style="background:#0A2472;color:#fff;"><tr><th style="padding:8px;">Benchmark</th><th>YTD Return</th><th>vs Portfolio</th></tr></thead><tbody><tr><td style="padding:8px;border-bottom:1px solid #f0f4fa;">Portfolio</td><td style="color:#2e7d32">+8.4%</td><td>—</td></tr><tr><td style="padding:8px;border-bottom:1px solid #f0f4fa;">S&P 500</td><td>+6.2%</td><td style="color:#2e7d32">+2.2% alpha</td></tr><tr><td style="padding:8px;">MSCI World</td><td>+5.8%</td><td style="color:#2e7d32">+2.6% alpha</td></tr></tbody></table>',
      'Attribution Analysis': '<table style="width:100%;border-collapse:collapse;font-size:12px;"><thead style="background:#0A2472;color:#fff;"><tr><th style="padding:8px;">Asset Class</th><th>Weight</th><th>Return</th><th>Contribution</th></tr></thead><tbody><tr><td style="padding:8px;border-bottom:1px solid #f0f4fa;">Public Equity</td><td>33.8%</td><td>+11.2%</td><td style="color:#2e7d32">+3.79%</td></tr><tr><td style="padding:8px;border-bottom:1px solid #f0f4fa;">Private Equity</td><td>25.3%</td><td>+9.8%</td><td style="color:#2e7d32">+2.48%</td></tr><tr><td style="padding:8px;">Operations</td><td>6.4%</td><td>-1.2%</td><td style="color:#e74c3c">-0.08%</td></tr></tbody></table>',
      'Exposure Analysis':    '<p style="font-size:13px;color:#333;">Healthcare: 35% | Technology: 20% | Real Estate: 15% | Infrastructure: 10% | Other: 20%. Concentration risk flagged in Healthcare sector (>35% threshold).</p>',
      'Liquidity Summary':    '<p style="font-size:13px;color:#333;">Available liquidity: $18.4M (14.8% of portfolio). 30-day liquidity: $31.2M. Illiquid assets: $74.8M. Next redemption: Sep 2026 ($4.2M).</p>',
      'Private Markets':      '<p style="font-size:13px;color:#333;">Total PE commitments: $48.2M across 6 funds. Composite net IRR: 14.2%. PME vs S&P 500: 1.28x. Total fees YTD: $1.24M.</p>',
      'Opportunity Pipeline': '<p style="font-size:13px;color:#333;">12 opportunities in pipeline. 5 under review. 3 approved YTD ($24.5M committed). 4 rejected YTD.</p>',
      'Market Data':          '<p style="font-size:13px;color:#333;">Fed Funds Rate: 4.75% | 10-Yr Treasury: 4.32% | CPI: 3.1% | GDP Growth: 2.4%. S&P 500 YTD: +6.2%.</p>',
    };

    let html = `
      <div style="border-bottom:3px solid #0A2472;padding-bottom:16px;margin-bottom:24px;">
        <div style="font-size:9px;letter-spacing:3px;color:#4A90D9;font-family:Courier New,monospace;">CIPHER PLATFORM — CONFIDENTIAL</div>
        <div style="font-size:22px;font-weight:bold;color:#0A2472;margin-top:6px;">${title}</div>
        <div style="font-size:11px;color:#aab8d0;font-family:Courier New,monospace;margin-top:4px;">Prepared for Investment Committee Presentation · ${period}</div>
      </div>`;

    Object.entries(sections).forEach(([name, included]) => {
      if (!included) return;
      html += `<div style="margin-bottom:24px;"><div style="font-size:10px;letter-spacing:2px;color:#4A90D9;font-family:Courier New,monospace;margin-bottom:10px;border-bottom:1px solid #f0f4fa;padding-bottom:6px;">${name.toUpperCase()}</div>${sectionData[name]}</div>`;
    });

    html += `<div style="margin-top:32px;padding-top:16px;border-top:1px solid #f0f4fa;font-size:10px;color:#ccc;font-family:Courier New,monospace;">This report is for informational purposes only and does not constitute investment advice. Generated by CIPHER Platform.</div>`;
    document.getElementById('report-preview').innerHTML = html;
  }

  // Patch dirTab to init charts
  const _origDirTabTools = dirTab;
  dirTab = function(el, tabId) {
    _origDirTabTools(el, tabId);
    if (tabId === 'dir-benchmark') setTimeout(initBenchmarkCharts, 50);
    if (tabId === 'dir-market')    setTimeout(initMarketCharts, 50);
  };'''

    if 'initBenchmarkCharts' not in c:
        last = c.rfind('</script>')
        c = c[:last] + js + '\n' + c[last:]
        print("  Added investment tools JavaScript")
    else:
        print("  JavaScript already present, skipping")

    if c != original:
        shutil.copy(HTML_PATH, HTML_PATH + '.invest.bak')
        with open(HTML_PATH, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"\n  Saved {HTML_PATH}")
    else:
        print("\n  No changes needed")

    print("""
Done!
  1. Restart: uvicorn main:app --reload
  2. Log in as director
  3. New tabs under INVESTMENT TOOLS: Benchmarks, Market Data, Opportunity Pipeline, Due Diligence, Report Builder
""")

if __name__ == "__main__":
    patch()
