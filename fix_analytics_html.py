with open('templates/index.html', encoding='utf-8') as f:
    c = f.read()

analytics_html = '''      <!-- PORTFOLIO ANALYTICS TAB -->
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

'''

# Insert all 4 tab divs right before dir-ai
anchor = '      <div id="dir-ai" style="display:none">'
if 'id="dir-analytics"' not in c:
    c = c.replace(anchor, analytics_html + anchor, 1)
    print('Added analytics tab HTML')
else:
    print('Already present, skipping')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Done — restart uvicorn and refresh')
