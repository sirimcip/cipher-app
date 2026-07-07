"""
CIPHER Analytics Installer
Run from inside cipher_app folder:
    python add_analytics.py

Adds 4 new tabs to the director dashboard:
  - Portfolio Analytics
  - Exposure Analysis
  - Liquidity
  - Private Markets
"""

import os, shutil, sys

HTML_PATH = os.path.join("templates", "index.html")

def backup(path):
    bak = path + ".analytics.bak"
    shutil.copy(path, bak)
    print(f"  Backed up {path} -> {bak}")

def patch():
    if not os.path.exists(HTML_PATH):
        print(f"ERROR: Could not find {HTML_PATH}. Run from inside cipher_app/.")
        sys.exit(1)

    with open(HTML_PATH, encoding='utf-8') as f:
        c = f.read()

    original = c

    # ── 1. ADD NAV ITEMS ──
    old_nav = '    <div class="nav-section-label">INTELLIGENCE</div>\n    <div class="nav-item" onclick="dirTab(this,\'dir-ai\')"><span class="nav-dot"></span>AI Insights</div>\n    <div class="nav-item" onclick="dirTab(this,\'dir-report\')"><span class="nav-dot"></span>Generate Report</div>'
    new_nav = '''    <div class="nav-section-label">ANALYTICS</div>
    <div class="nav-item" onclick="dirTab(this,'dir-analytics')"><span class="nav-dot"></span>Portfolio Analytics</div>
    <div class="nav-item" onclick="dirTab(this,'dir-exposure')"><span class="nav-dot"></span>Exposure Analysis</div>
    <div class="nav-item" onclick="dirTab(this,'dir-liquidity')"><span class="nav-dot"></span>Liquidity</div>
    <div class="nav-item" onclick="dirTab(this,'dir-private')"><span class="nav-dot"></span>Private Markets</div>
    <div class="nav-section-label">INTELLIGENCE</div>
    <div class="nav-item" onclick="dirTab(this,'dir-ai')"><span class="nav-dot"></span>AI Insights</div>
    <div class="nav-item" onclick="dirTab(this,'dir-report')"><span class="nav-dot"></span>Generate Report</div>'''

    if 'dir-analytics' not in c:
        if old_nav not in c:
            print("ERROR: Could not find nav items anchor.")
            sys.exit(1)
        c = c.replace(old_nav, new_nav, 1)
        print("  Added analytics nav items")
    else:
        print("  Nav items already present, skipping")

    # ── 2. UPDATE dirTab FUNCTION ──
    old_dirtab = "    ['dir-overview','dir-submissions','dir-ai','dir-report'].forEach(id => {"
    new_dirtab = "    ['dir-overview','dir-submissions','dir-analytics','dir-exposure','dir-liquidity','dir-private','dir-ai','dir-report'].forEach(id => {"

    if old_dirtab in c:
        c = c.replace(old_dirtab, new_dirtab, 1)
        print("  Updated dirTab function")

    # ── 3. ADD ANALYTICS HTML TABS ──
    old_ai = '      <div id="dir-ai" style="display:none">'
    new_tabs = '''      <!-- PORTFOLIO ANALYTICS TAB -->
      <div id="dir-analytics" style="display:none">
        <div class="cards" style="grid-template-columns:repeat(4,1fr)">
          <div class="card"><div class="card-label">TOTAL PORTFOLIO VALUE</div><div class="card-value">$124.6M</div><div class="card-sub">Across all asset classes</div></div>
          <div class="card success"><div class="card-label">TOTAL RETURN (YTD)</div><div class="card-value">+8.4%</div><div class="card-sub">vs 6.2% benchmark</div></div>
          <div class="card"><div class="card-label">WEIGHTED AVG RETURN</div><div class="card-value">7.1%</div><div class="card-sub">Net of fees</div></div>
          <div class="card danger"><div class="card-label">PORTFOLIO RISK SCORE</div><div class="card-value">Moderate</div><div class="card-sub">Based on allocation mix</div></div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px;">
          <div class="table-wrap" style="padding:24px;border-radius:12px;">
            <div class="section-title" style="margin-bottom:16px;">PERFORMANCE BY ASSET CLASS</div>
            <canvas id="chart-perf-class" height="220"></canvas>
          </div>
          <div class="table-wrap" style="padding:24px;border-radius:12px;">
            <div class="section-title" style="margin-bottom:16px;">PORTFOLIO VALUE OVER TIME</div>
            <canvas id="chart-port-value" height="220"></canvas>
          </div>
        </div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>ASSET CLASS</th><th>VALUE</th><th>WEIGHT</th><th>RETURN (YTD)</th><th>BENCHMARK</th><th>ALPHA</th></tr></thead>
            <tbody>
              <tr><td>Public Equity</td><td>$42.1M</td><td>33.8%</td><td style="color:#2e7d32">+11.2%</td><td>9.4%</td><td style="color:#2e7d32">+1.8%</td></tr>
              <tr><td>Private Equity</td><td>$31.5M</td><td>25.3%</td><td style="color:#2e7d32">+9.8%</td><td>8.1%</td><td style="color:#2e7d32">+1.7%</td></tr>
              <tr><td>Fixed Income</td><td>$24.8M</td><td>19.9%</td><td style="color:#2e7d32">+4.1%</td><td>3.8%</td><td style="color:#2e7d32">+0.3%</td></tr>
              <tr><td>Real Assets</td><td>$18.2M</td><td>14.6%</td><td style="color:#2e7d32">+6.7%</td><td>5.9%</td><td style="color:#2e7d32">+0.8%</td></tr>
              <tr><td>Operations</td><td>$8.0M</td><td>6.4%</td><td style="color:#e74c3c">-1.2%</td><td>2.0%</td><td style="color:#e74c3c">-3.2%</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- EXPOSURE ANALYSIS TAB -->
      <div id="dir-exposure" style="display:none">
        <div class="cards" style="grid-template-columns:repeat(3,1fr)">
          <div class="card"><div class="card-label">SECTORS TRACKED</div><div class="card-value">8</div><div class="card-sub">Across all holdings</div></div>
          <div class="card"><div class="card-label">GEOGRAPHIES</div><div class="card-value">12</div><div class="card-sub">Countries represented</div></div>
          <div class="card danger"><div class="card-label">CONCENTRATION RISK</div><div class="card-value">High</div><div class="card-sub">Healthcare >35% of portfolio</div></div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px;margin-bottom:20px;">
          <div class="table-wrap" style="padding:24px;border-radius:12px;">
            <div class="section-title" style="margin-bottom:16px;">BY SECTOR</div>
            <canvas id="chart-sector" height="240"></canvas>
          </div>
          <div class="table-wrap" style="padding:24px;border-radius:12px;">
            <div class="section-title" style="margin-bottom:16px;">BY GEOGRAPHY</div>
            <canvas id="chart-geo" height="240"></canvas>
          </div>
          <div class="table-wrap" style="padding:24px;border-radius:12px;">
            <div class="section-title" style="margin-bottom:16px;">BY ASSET TYPE</div>
            <canvas id="chart-type" height="240"></canvas>
          </div>
        </div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>SECTOR</th><th>EXPOSURE</th><th>% OF PORTFOLIO</th><th>LONG</th><th>SHORT</th><th>NET</th></tr></thead>
            <tbody>
              <tr><td>Healthcare</td><td>$43.6M</td><td>35.0%</td><td>$43.6M</td><td>—</td><td style="color:#2e7d32">$43.6M</td></tr>
              <tr><td>Technology</td><td>$24.9M</td><td>20.0%</td><td>$24.9M</td><td>$2.1M</td><td style="color:#2e7d32">$22.8M</td></tr>
              <tr><td>Real Estate</td><td>$18.7M</td><td>15.0%</td><td>$18.7M</td><td>—</td><td style="color:#2e7d32">$18.7M</td></tr>
              <tr><td>Infrastructure</td><td>$12.5M</td><td>10.0%</td><td>$12.5M</td><td>—</td><td style="color:#2e7d32">$12.5M</td></tr>
              <tr><td>Other</td><td>$24.9M</td><td>20.0%</td><td>$24.9M</td><td>$1.2M</td><td style="color:#2e7d32">$23.7M</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- LIQUIDITY TAB -->
      <div id="dir-liquidity" style="display:none">
        <div class="cards" style="grid-template-columns:repeat(4,1fr)">
          <div class="card success"><div class="card-label">AVAILABLE LIQUIDITY</div><div class="card-value">$18.4M</div><div class="card-sub">Immediately accessible</div></div>
          <div class="card"><div class="card-label">30-DAY LIQUIDITY</div><div class="card-value">$31.2M</div><div class="card-sub">Redeemable within 30 days</div></div>
          <div class="card danger"><div class="card-label">ILLIQUID ASSETS</div><div class="card-value">$74.8M</div><div class="card-sub">Lock-up > 1 year</div></div>
          <div class="card"><div class="card-label">NEXT REDEMPTION</div><div class="card-value">Sep 2026</div><div class="card-sub">$4.2M available</div></div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px;">
          <div class="table-wrap" style="padding:24px;border-radius:12px;">
            <div class="section-title" style="margin-bottom:16px;">LIQUIDITY PROFILE</div>
            <canvas id="chart-liquidity" height="220"></canvas>
          </div>
          <div class="table-wrap" style="padding:24px;border-radius:12px;">
            <div class="section-title" style="margin-bottom:16px;">CURRENCY EXPOSURE (BASE: USD)</div>
            <canvas id="chart-currency" height="220"></canvas>
          </div>
        </div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>FUND / HOLDING</th><th>VALUE (USD)</th><th>CURRENCY</th><th>FX RATE</th><th>LIQUIDITY</th><th>NEXT REDEMPTION</th></tr></thead>
            <tbody>
              <tr><td>US Equity Fund</td><td>$42.1M</td><td>USD</td><td>1.00</td><td><span class="badge submitted">LIQUID</span></td><td>Daily</td></tr>
              <tr><td>European Growth PE</td><td>$18.3M</td><td>EUR</td><td>1.08</td><td><span class="badge missing">ILLIQUID</span></td><td>Dec 2027</td></tr>
              <tr><td>Asia Pacific Fund</td><td>$9.7M</td><td>JPY</td><td>0.0067</td><td><span class="badge flagged">SEMI-LIQUID</span></td><td>Sep 2026</td></tr>
              <tr><td>Fixed Income</td><td>$24.8M</td><td>USD</td><td>1.00</td><td><span class="badge submitted">LIQUID</span></td><td>Monthly</td></tr>
              <tr><td>Real Assets Fund</td><td>$18.2M</td><td>USD</td><td>1.00</td><td><span class="badge missing">ILLIQUID</span></td><td>Mar 2028</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- PRIVATE MARKETS TAB -->
      <div id="dir-private" style="display:none">
        <div class="cards" style="grid-template-columns:repeat(4,1fr)">
          <div class="card"><div class="card-label">TOTAL PE COMMITMENTS</div><div class="card-value">$48.2M</div><div class="card-sub">Across 6 funds</div></div>
          <div class="card success"><div class="card-label">NET IRR (COMPOSITE)</div><div class="card-value">14.2%</div><div class="card-sub">Since inception</div></div>
          <div class="card"><div class="card-label">TOTAL FEES (YTD)</div><div class="card-value">$1.24M</div><div class="card-sub">Mgmt + carried interest</div></div>
          <div class="card"><div class="card-label">PME BENCHMARK</div><div class="card-value">1.28x</div><div class="card-sub">vs S&P 500 equivalent</div></div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px;">
          <div class="table-wrap" style="padding:24px;border-radius:12px;">
            <div class="section-title" style="margin-bottom:16px;">J-CURVE ANALYSIS</div>
            <canvas id="chart-jcurve" height="220"></canvas>
          </div>
          <div class="table-wrap" style="padding:24px;border-radius:12px;">
            <div class="section-title" style="margin-bottom:16px;">CASH FLOW FORECAST</div>
            <canvas id="chart-cashflow" height="220"></canvas>
          </div>
        </div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>FUND</th><th>VINTAGE</th><th>COMMITTED</th><th>CALLED</th><th>DISTRIBUTED</th><th>NET IRR</th><th>TVPI</th><th>FEES (YTD)</th></tr></thead>
            <tbody>
              <tr><td>Apex Growth III</td><td>2021</td><td>$12.0M</td><td>$9.6M</td><td>$2.1M</td><td style="color:#2e7d32">18.4%</td><td>1.42x</td><td>$184K</td></tr>
              <tr><td>Meridian PE II</td><td>2020</td><td>$8.5M</td><td>$8.5M</td><td>$6.2M</td><td style="color:#2e7d32">12.1%</td><td>1.31x</td><td>$127K</td></tr>
              <tr><td>Blueridge Ventures</td><td>2022</td><td>$6.0M</td><td>$3.2M</td><td>$0.4M</td><td style="color:#e74c3c">-2.4%</td><td>0.89x</td><td>$96K</td></tr>
              <tr><td>Horizon Real Assets</td><td>2019</td><td>$14.0M</td><td>$14.0M</td><td>$11.8M</td><td style="color:#2e7d32">16.7%</td><td>1.68x</td><td>$210K</td></tr>
              <tr><td>ClearPath Infra I</td><td>2023</td><td>$7.7M</td><td>$2.1M</td><td>$0.0M</td><td>—</td><td>—</td><td>$62K</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <div id="dir-ai" style="display:none">'''

    if 'dir-analytics' not in c:
        if old_ai not in c:
            print("ERROR: Could not find dir-ai anchor.")
            sys.exit(1)
        c = c.replace(old_ai, new_tabs, 1)
        print("  Added analytics HTML tabs")
    else:
        print("  Analytics HTML already present, skipping")

    # ── 4. ADD CHART JS ──
    chart_js = '''
  // ══ ANALYTICS CHARTS ══
  const PALETTE8 = ["#0A2472","#4A90D9","#A8D4F5","#7C3AED","#16A34A","#DC2626","#D97706","#0891B2"];

  function initAnalyticsCharts() {
    // Performance by asset class
    const perfCtx = document.getElementById('chart-perf-class');
    if (perfCtx && !perfCtx.dataset.init) {
      perfCtx.dataset.init = '1';
      new Chart(perfCtx, { type:'bar', data:{ labels:['Public Equity','Private Equity','Fixed Income','Real Assets','Operations'], datasets:[{ label:'Return %', data:[11.2,9.8,4.1,6.7,-1.2], backgroundColor:["#2e7d32","#2e7d32","#2e7d32","#2e7d32","#e74c3c"] }]}, options:{ responsive:true, plugins:{legend:{display:false}}, scales:{y:{title:{display:true,text:'Return (%)'}}} }});
    }
    // Portfolio value over time
    const pvCtx = document.getElementById('chart-port-value');
    if (pvCtx && !pvCtx.dataset.init) {
      pvCtx.dataset.init = '1';
      new Chart(pvCtx, { type:'line', data:{ labels:['Q1 2024','Q2 2024','Q3 2024','Q4 2024','Q1 2025','Q2 2025','Q3 2025','Q4 2025','Q1 2026','Q2 2026'], datasets:[{ label:'Portfolio Value ($M)', data:[98.2,101.4,104.8,107.1,110.3,113.9,116.2,119.7,122.1,124.6], borderColor:'#0A2472', backgroundColor:'rgba(10,36,114,0.08)', tension:0.3, fill:true }]}, options:{ responsive:true, plugins:{legend:{display:false}}, scales:{y:{title:{display:true,text:'Value ($M)'}}} }});
    }
    // Sector exposure
    const secCtx = document.getElementById('chart-sector');
    if (secCtx && !secCtx.dataset.init) {
      secCtx.dataset.init = '1';
      new Chart(secCtx, { type:'doughnut', data:{ labels:['Healthcare','Technology','Real Estate','Infrastructure','Other'], datasets:[{ data:[35,20,15,10,20], backgroundColor:PALETTE8 }]}, options:{ responsive:true, plugins:{legend:{position:'bottom'}} }});
    }
    // Geography exposure
    const geoCtx = document.getElementById('chart-geo');
    if (geoCtx && !geoCtx.dataset.init) {
      geoCtx.dataset.init = '1';
      new Chart(geoCtx, { type:'doughnut', data:{ labels:['North America','Europe','Asia Pacific','Latin America','Other'], datasets:[{ data:[62,18,12,5,3], backgroundColor:PALETTE8 }]}, options:{ responsive:true, plugins:{legend:{position:'bottom'}} }});
    }
    // Asset type
    const typeCtx = document.getElementById('chart-type');
    if (typeCtx && !typeCtx.dataset.init) {
      typeCtx.dataset.init = '1';
      new Chart(typeCtx, { type:'doughnut', data:{ labels:['Public Equity','Private Equity','Fixed Income','Real Assets','Cash'], datasets:[{ data:[34,25,20,15,6], backgroundColor:PALETTE8 }]}, options:{ responsive:true, plugins:{legend:{position:'bottom'}} }});
    }
    // Liquidity profile
    const liqCtx = document.getElementById('chart-liquidity');
    if (liqCtx && !liqCtx.dataset.init) {
      liqCtx.dataset.init = '1';
      new Chart(liqCtx, { type:'bar', data:{ labels:['Immediate','30 Days','90 Days','1 Year','1-3 Years','>3 Years'], datasets:[{ label:'Value ($M)', data:[18.4,12.8,8.6,6.4,24.2,50.6], backgroundColor:['#2e7d32','#4A90D9','#A8D4F5','#D97706','#e74c3c','#7C3AED'] }]}, options:{ responsive:true, plugins:{legend:{display:false}}, scales:{y:{title:{display:true,text:'Value ($M)'}}} }});
    }
    // Currency exposure
    const curCtx = document.getElementById('chart-currency');
    if (curCtx && !curCtx.dataset.init) {
      curCtx.dataset.init = '1';
      new Chart(curCtx, { type:'doughnut', data:{ labels:['USD','EUR','JPY','GBP','Other'], datasets:[{ data:[68,14,8,6,4], backgroundColor:PALETTE8 }]}, options:{ responsive:true, plugins:{legend:{position:'bottom'}} }});
    }
    // J-Curve
    const jCtx = document.getElementById('chart-jcurve');
    if (jCtx && !jCtx.dataset.init) {
      jCtx.dataset.init = '1';
      new Chart(jCtx, { type:'line', data:{ labels:['Year 0','Year 1','Year 2','Year 3','Year 4','Year 5','Year 6','Year 7'], datasets:[{ label:'Net Cash Flow ($M)', data:[-4.2,-6.8,-5.1,-2.3,1.8,6.4,11.2,16.8], borderColor:'#0A2472', backgroundColor:'rgba(10,36,114,0.08)', tension:0.4, fill:true, pointBackgroundColor: d => d.raw < 0 ? '#e74c3c' : '#2e7d32' }]}, options:{ responsive:true, plugins:{legend:{display:false}}, scales:{y:{title:{display:true,text:'Net Cash Flow ($M)'}}} }});
    }
    // Cash flow forecast
    const cfCtx = document.getElementById('chart-cashflow');
    if (cfCtx && !cfCtx.dataset.init) {
      cfCtx.dataset.init = '1';
      new Chart(cfCtx, { type:'bar', data:{ labels:['Q3 2026','Q4 2026','Q1 2027','Q2 2027','Q3 2027','Q4 2027'], datasets:[{ label:'Contributions', data:[-2.1,-1.8,-3.2,-1.4,-0.8,-1.2], backgroundColor:'#e74c3c' },{ label:'Distributions', data:[1.4,2.8,1.2,4.6,3.1,5.8], backgroundColor:'#2e7d32' }]}, options:{ responsive:true, plugins:{legend:{position:'bottom'}}, scales:{y:{title:{display:true,text:'Cash Flow ($M)'}}} }});
    }
  }

  // Patch dirTab to init charts when analytics tabs are opened
  const _origDirTab = dirTab;
  dirTab = function(el, tabId) {
    _origDirTab(el, tabId);
    if (['dir-analytics','dir-exposure','dir-liquidity','dir-private'].includes(tabId)) {
      setTimeout(initAnalyticsCharts, 50);
    }
  };'''

    if 'initAnalyticsCharts' not in c:
        # Insert before closing </script>
        if '</script>\n</body>' in c:
            c = c.replace('</script>\n</body>', chart_js + '\n</script>\n</body>', 1)
            print("  Added analytics chart JavaScript")
        elif '</script>' in c:
            last = c.rfind('</script>')
            c = c[:last] + chart_js + '\n' + c[last:]
            print("  Added analytics chart JavaScript")
    else:
        print("  Chart JS already present, skipping")

    # ── SAVE ──
    if c != original:
        backup(HTML_PATH)
        with open(HTML_PATH, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"\n  Saved {HTML_PATH}")
    else:
        print(f"\n  No changes needed")

    print("""
Done! 
  1. Restart: uvicorn main:app --reload
  2. Log in as director
  3. You'll see 4 new tabs in the sidebar: Portfolio Analytics, Exposure Analysis, Liquidity, Private Markets
""")

if __name__ == "__main__":
    patch()
