with open('templates/index.html', encoding='utf-8') as f:
    c = f.read()

# Fix 1: sidebar scroll
c = c.replace(
    'width: 240px; background: var(--navy); display: flex; flex-direction: column; padding: 0; flex-shrink: 0; }',
    'width: 240px; background: var(--navy); display: flex; flex-direction: column; padding: 0; flex-shrink: 0; overflow-y: auto; max-height: 100vh; }'
)
print("Fixed sidebar scroll")

# Fix 2: insert investment tools tab HTML if missing
if 'id="dir-benchmark"' not in c:
    tools_html = '''
      <div id="dir-benchmark" style="display:none">
        <div class="cards" style="grid-template-columns:repeat(4,1fr)">
          <div class="card success"><div class="card-label">PORTFOLIO RETURN (YTD)</div><div class="card-value">+8.4%</div><div class="card-sub">Net of fees</div></div>
          <div class="card"><div class="card-label">S&P 500 (YTD)</div><div class="card-value">+6.2%</div><div class="card-sub">Benchmark</div></div>
          <div class="card"><div class="card-label">MSCI WORLD (YTD)</div><div class="card-value">+5.8%</div><div class="card-sub">Benchmark</div></div>
          <div class="card success"><div class="card-label">ALPHA GENERATED</div><div class="card-value">+2.2%</div><div class="card-sub">vs S&P 500</div></div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px;">
          <div class="table-wrap" style="padding:24px;border-radius:12px;"><div class="section-title" style="margin-bottom:16px;">PORTFOLIO vs BENCHMARKS</div><canvas id="chart-benchmark" height="240"></canvas></div>
          <div class="table-wrap" style="padding:24px;border-radius:12px;"><div class="section-title" style="margin-bottom:16px;">RETURN ATTRIBUTION BY ASSET CLASS</div><canvas id="chart-attribution" height="240"></canvas></div>
        </div>
        <div class="table-wrap"><table>
          <thead><tr><th>ASSET CLASS</th><th>WEIGHT</th><th>RETURN</th><th>CONTRIBUTION</th><th>BENCHMARK</th><th>ACTIVE RETURN</th></tr></thead>
          <tbody>
            <tr><td>Public Equity</td><td>33.8%</td><td>+11.2%</td><td style="color:#2e7d32">+3.79%</td><td>9.4%</td><td style="color:#2e7d32">+1.8%</td></tr>
            <tr><td>Private Equity</td><td>25.3%</td><td>+9.8%</td><td style="color:#2e7d32">+2.48%</td><td>8.1%</td><td style="color:#2e7d32">+1.7%</td></tr>
            <tr><td>Fixed Income</td><td>19.9%</td><td>+4.1%</td><td style="color:#2e7d32">+0.82%</td><td>3.8%</td><td style="color:#2e7d32">+0.3%</td></tr>
            <tr><td>Real Assets</td><td>14.6%</td><td>+6.7%</td><td style="color:#2e7d32">+0.98%</td><td>5.9%</td><td style="color:#2e7d32">+0.8%</td></tr>
            <tr><td>Operations</td><td>6.4%</td><td>-1.2%</td><td style="color:#e74c3c">-0.08%</td><td>2.0%</td><td style="color:#e74c3c">-3.2%</td></tr>
            <tr style="font-weight:bold;background:#f0f4fa"><td>TOTAL</td><td>100%</td><td>+8.4%</td><td style="color:#2e7d32">+8.4%</td><td>6.2%</td><td style="color:#2e7d32">+2.2%</td></tr>
          </tbody>
        </table></div>
      </div>

      <div id="dir-market" style="display:none">
        <div class="cards" style="grid-template-columns:repeat(4,1fr)">
          <div class="card"><div class="card-label">S&P 500 (SPY)</div><div class="card-value" id="live-sp500">—</div><div class="card-sub" id="live-sp500-change">Loading...</div></div>
          <div class="card"><div class="card-label">10-YR TREASURY</div><div class="card-value" id="live-10yr">—</div><div class="card-sub">Live yield</div></div>
          <div class="card danger"><div class="card-label">CPI INFLATION</div><div class="card-value" id="live-cpi">—</div><div class="card-sub">YOY</div></div>
          <div class="card"><div class="card-label">NASDAQ 100 (QQQ)</div><div class="card-value" id="live-nasdaq">—</div><div class="card-sub">Daily change</div></div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px;">
          <div class="table-wrap" style="padding:24px;border-radius:12px;"><div class="section-title" style="margin-bottom:16px;">MAJOR INDICES (YTD)</div><canvas id="chart-indices" height="240"></canvas></div>
          <div class="table-wrap" style="padding:24px;border-radius:12px;"><div class="section-title" style="margin-bottom:16px;">INTEREST RATE ENVIRONMENT</div><canvas id="chart-rates" height="240"></canvas></div>
        </div>
        <div class="section-header"><div class="section-title">LIVE MARKET REFERENCE DATA</div><div style="font-size:10px;color:#aab8d0;font-family:'Courier New',monospace;">Powered by Alpha Vantage</div></div>
        <div class="table-wrap"><table>
          <thead><tr><th>INDEX / INDICATOR</th><th>PRICE / VALUE</th><th>CHANGE</th><th>CHANGE %</th></tr></thead>
          <tbody id="live-market-tbody"><tr><td colspan="4" style="text-align:center;color:#aab8d0;padding:20px;">Loading live data...</td></tr></tbody>
        </table></div>
      </div>

      <div id="dir-pipeline" style="display:none">
        <div class="cards" style="grid-template-columns:repeat(4,1fr)">
          <div class="card"><div class="card-label">TOTAL OPPORTUNITIES</div><div class="card-value">12</div><div class="card-sub">In active pipeline</div></div>
          <div class="card"><div class="card-label">UNDER REVIEW</div><div class="card-value">5</div><div class="card-sub">Pending IC decision</div></div>
          <div class="card success"><div class="card-label">APPROVED (YTD)</div><div class="card-value">3</div><div class="card-sub">$24.5M committed</div></div>
          <div class="card danger"><div class="card-label">REJECTED (YTD)</div><div class="card-value">4</div><div class="card-sub">Did not meet criteria</div></div>
        </div>
        <div class="section-header" style="margin-top:8px;">
          <div class="section-title">DEAL PIPELINE</div>
          <button class="btn-report" onclick="showAddDeal()">+ ADD OPPORTUNITY</button>
        </div>
        <div id="add-deal-form" style="display:none;background:#fff;border-radius:12px;padding:28px;margin-bottom:20px;">
          <div class="section-title" style="margin-bottom:16px;">NEW INVESTMENT OPPORTUNITY</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <div class="input-group"><label>OPPORTUNITY NAME</label><input type="text" id="deal-name" placeholder="e.g. Apex Growth Fund IV"/></div>
            <div class="input-group"><label>FIRM / SPONSOR</label><input type="text" id="deal-firm" placeholder="e.g. Apex Capital Partners"/></div>
            <div class="input-group"><label>ASSET CLASS</label><select id="deal-class"><option>Private Equity</option><option>Venture Capital</option><option>Real Estate</option><option>Fixed Income</option><option>Public Equity</option><option>Infrastructure</option><option>Other</option></select></div>
            <div class="input-group"><label>DEAL SIZE</label><input type="text" id="deal-size" placeholder="e.g. $10M"/></div>
            <div class="input-group"><label>EXPECTED CLOSE</label><input type="text" id="deal-close" placeholder="e.g. Q3 2026"/></div>
            <div class="input-group"><label>SUBMITTED BY</label><input type="text" id="deal-submitter" placeholder="Manager name"/></div>
          </div>
          <div class="input-group" style="margin-top:12px;"><label>NOTES</label><textarea id="deal-notes" placeholder="Brief description..." style="width:100%;padding:10px;border:1.5px solid #dde6f5;border-radius:8px;font-family:Georgia,serif;min-height:70px;resize:vertical;"></textarea></div>
          <div style="display:flex;gap:12px;margin-top:16px;">
            <button class="btn-report" onclick="addDeal()">ADD TO PIPELINE</button>
            <button class="btn-report" style="background:#f0f4fa;color:#0A2472;" onclick="document.getElementById('add-deal-form').style.display='none'">CANCEL</button>
          </div>
        </div>
        <div class="table-wrap"><table>
          <thead><tr><th>OPPORTUNITY</th><th>FIRM</th><th>ASSET CLASS</th><th>SIZE</th><th>EXPECTED CLOSE</th><th>SUBMITTED BY</th><th>STATUS</th><th>ACTION</th></tr></thead>
          <tbody id="pipeline-tbody">
            <tr><td>Apex Growth Fund IV</td><td>Apex Capital</td><td>Private Equity</td><td>$10.0M</td><td>Q3 2026</td><td>Sarah Johnson</td><td><span class="badge flagged">UNDER REVIEW</span></td><td><button class="btn-report" style="padding:4px 10px;font-size:9px;" onclick="moveDeal(this,'APPROVED')">Approve</button> <button class="btn-report" style="padding:4px 10px;font-size:9px;background:#e74c3c;" onclick="moveDeal(this,'REJECTED')">Reject</button></td></tr>
            <tr><td>Meridian RE Fund III</td><td>Meridian Capital</td><td>Real Estate</td><td>$7.5M</td><td>Q4 2026</td><td>Mike Chen</td><td><span class="badge flagged">UNDER REVIEW</span></td><td><button class="btn-report" style="padding:4px 10px;font-size:9px;" onclick="moveDeal(this,'APPROVED')">Approve</button> <button class="btn-report" style="padding:4px 10px;font-size:9px;background:#e74c3c;" onclick="moveDeal(this,'REJECTED')">Reject</button></td></tr>
            <tr><td>Blueridge Series B</td><td>Blueridge Ventures</td><td>Venture Capital</td><td>$3.0M</td><td>Q2 2026</td><td>Priya Patel</td><td><span class="badge submitted">APPROVED</span></td><td>—</td></tr>
          </tbody>
        </table></div>
      </div>

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
            <div style="text-align:center;color:#aab8d0;font-family:'Courier New',monospace;font-size:12px;padding:60px 0;">Select sections and click Generate to see your IC-ready report here.</div>
          </div>
        </div>
      </div>

'''
    anchor = '      <div id="dir-ai" style="display:none">'
    c = c.replace(anchor, tools_html + anchor, 1)
    print("Added investment tools HTML")
else:
    print("Investment tools HTML already present")

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Done — restart uvicorn and hard refresh (Ctrl+Shift+R)")
