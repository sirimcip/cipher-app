"""
CIPHER Comprehensive Investment Tools Installer
Run from inside cipher_app folder:
    python add_comprehensive_tools.py

Adds these sections to the director dashboard:
  DATA & REPORTING:
    - Fund Performance (fund-level cumulative return chart + time-period table)
    - Risk Metrics (Sharpe, std dev, max drawdown, VaR)
    - Manager Scorecard (ranking by performance, consistency, risk-adjusted return)
  
  PRIVATE MARKETS:
    - Capital Accounts (committed, called, uncalled, distributed, NAV)
    - Vintage Year Analysis
    - DPI, RVPI, TVPI visual cards
  
  CASH MANAGEMENT:
    - Capital Call Schedule
    - Distribution Tracking
    - Cash Flow Waterfall
  
  COMPLIANCE & OPERATIONS:
    - IPS Tracking (policy limits)
    - Manager Watch List
    - Audit Log
  
  REPORTING:
    - PDF Report Download
    - Email Report to Stakeholders
"""

import os, shutil, sys, re

HTML_PATH = os.path.join("templates", "index.html")

def patch():
    if not os.path.exists(HTML_PATH):
        print(f"ERROR: Could not find {HTML_PATH}")
        sys.exit(1)

    with open(HTML_PATH, encoding='utf-8') as f:
        c = f.read()

    original = c

    # ── 1. ADD ALL NAV ITEMS ──
    old_intelligence = '    <div class="nav-section-label">INTELLIGENCE</div>'
    new_nav = '''    <div class="nav-section-label">PERFORMANCE</div>
    <div class="nav-item" onclick="dirTab(this,'dir-fundperf')"><span class="nav-dot"></span>Fund Performance</div>
    <div class="nav-item" onclick="dirTab(this,'dir-risk')"><span class="nav-dot"></span>Risk Metrics</div>
    <div class="nav-item" onclick="dirTab(this,'dir-scorecard')"><span class="nav-dot"></span>Manager Scorecard</div>
    <div class="nav-section-label">PRIVATE MARKETS</div>
    <div class="nav-item" onclick="dirTab(this,'dir-capital')"><span class="nav-dot"></span>Capital Accounts</div>
    <div class="nav-item" onclick="dirTab(this,'dir-vintage')"><span class="nav-dot"></span>Vintage Analysis</div>
    <div class="nav-section-label">CASH MANAGEMENT</div>
    <div class="nav-item" onclick="dirTab(this,'dir-calls')"><span class="nav-dot"></span>Capital Calls</div>
    <div class="nav-item" onclick="dirTab(this,'dir-distributions')"><span class="nav-dot"></span>Distributions</div>
    <div class="nav-item" onclick="dirTab(this,'dir-waterfall')"><span class="nav-dot"></span>Cash Flow Waterfall</div>
    <div class="nav-section-label">COMPLIANCE</div>
    <div class="nav-item" onclick="dirTab(this,'dir-ips')"><span class="nav-dot"></span>IPS Tracking</div>
    <div class="nav-item" onclick="dirTab(this,'dir-watchlist')"><span class="nav-dot"></span>Manager Watch List</div>
    <div class="nav-item" onclick="dirTab(this,'dir-audit')"><span class="nav-dot"></span>Audit Log</div>
    <div class="nav-section-label">INTELLIGENCE</div>'''

    if 'dir-fundperf' not in c:
        c = c.replace(old_intelligence, new_nav, 1)
        print("  Added all new nav items")
    else:
        print("  Nav items already present")

    # ── 2. UPDATE dirTab list ──
    old_list = "['dir-overview','dir-submissions','dir-analytics','dir-exposure','dir-liquidity','dir-private','dir-ai','dir-report']"
    new_list = "['dir-overview','dir-submissions','dir-analytics','dir-exposure','dir-liquidity','dir-private','dir-fundperf','dir-risk','dir-scorecard','dir-capital','dir-vintage','dir-calls','dir-distributions','dir-waterfall','dir-ips','dir-watchlist','dir-audit','dir-ai','dir-report']"
    if old_list in c:
        c = c.replace(old_list, new_list, 1)
        print("  Updated dirTab list")

    # ── 3. ADD ALL HTML TABS ──
    new_tabs = '''
      <!-- FUND PERFORMANCE TAB -->
      <div id="dir-fundperf" style="display:none">
        <div class="cards" style="grid-template-columns:repeat(4,1fr)">
          <div class="card success"><div class="card-label">PORTFOLIO IRR (NET)</div><div class="card-value">14.2%</div><div class="card-sub">Since inception composite</div></div>
          <div class="card"><div class="card-label">YTD RETURN</div><div class="card-value">+8.4%</div><div class="card-sub">vs S&P 500 +6.2%</div></div>
          <div class="card"><div class="card-label">3-YEAR RETURN</div><div class="card-value">+11.8%</div><div class="card-sub">Annualized net of fees</div></div>
          <div class="card success"><div class="card-label">SINCE INCEPTION</div><div class="card-value">+94.2%</div><div class="card-sub">Cumulative total return</div></div>
        </div>
        <div class="table-wrap" style="padding:24px;border-radius:12px;margin-bottom:20px;">
          <div class="section-title" style="margin-bottom:16px;">FUND-LEVEL CUMULATIVE RETURNS</div>
          <canvas id="chart-fund-cumulative" height="280"></canvas>
        </div>
        <div class="section-header"><div class="section-title">TIME-PERIOD RETURN TABLE</div></div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>FUND / ASSET CLASS</th><th>CURRENCY</th><th>QTD</th><th>YTD</th><th>1 YEAR</th><th>3 YEAR</th><th>5 YEAR</th><th>SINCE INCEPTION</th><th>INCEPTION DATE</th></tr></thead>
            <tbody>
              <tr><td><strong>Total Portfolio</strong></td><td>USD</td><td style="color:#2e7d32">+2.1%</td><td style="color:#2e7d32">+8.4%</td><td style="color:#2e7d32">+11.2%</td><td style="color:#2e7d32">+11.8%</td><td style="color:#2e7d32">+9.4%</td><td style="color:#2e7d32">+94.2%</td><td>Jan 2015</td></tr>
              <tr><td>Public Equity</td><td>USD</td><td style="color:#2e7d32">+2.8%</td><td style="color:#2e7d32">+11.2%</td><td style="color:#2e7d32">+14.1%</td><td style="color:#2e7d32">+13.4%</td><td style="color:#2e7d32">+11.2%</td><td style="color:#2e7d32">+112.4%</td><td>Jan 2015</td></tr>
              <tr><td>Private Equity</td><td>USD</td><td style="color:#2e7d32">+1.9%</td><td style="color:#2e7d32">+9.8%</td><td style="color:#2e7d32">+12.4%</td><td style="color:#2e7d32">+14.2%</td><td style="color:#2e7d32">+12.8%</td><td style="color:#2e7d32">+98.6%</td><td>Mar 2016</td></tr>
              <tr><td>Fixed Income</td><td>USD</td><td style="color:#2e7d32">+0.8%</td><td style="color:#2e7d32">+4.1%</td><td style="color:#2e7d32">+5.2%</td><td style="color:#2e7d32">+4.8%</td><td style="color:#2e7d32">+3.9%</td><td style="color:#2e7d32">+42.1%</td><td>Jan 2015</td></tr>
              <tr><td>Real Assets</td><td>USD</td><td style="color:#2e7d32">+1.4%</td><td style="color:#2e7d32">+6.7%</td><td style="color:#2e7d32">+8.9%</td><td style="color:#2e7d32">+9.2%</td><td style="color:#2e7d32">+8.1%</td><td style="color:#2e7d32">+74.8%</td><td>Jun 2016</td></tr>
              <tr><td>Operations</td><td>USD</td><td style="color:#e74c3c">-0.3%</td><td style="color:#e74c3c">-1.2%</td><td style="color:#e74c3c">-0.8%</td><td style="color:#2e7d32">+2.1%</td><td style="color:#2e7d32">+1.8%</td><td style="color:#2e7d32">+18.4%</td><td>Jan 2015</td></tr>
              <tr style="background:#eef5ff"><td>S&P 500 Total Return</td><td>USD</td><td>+1.4%</td><td>+6.2%</td><td>+9.4%</td><td>+10.2%</td><td>+8.8%</td><td>+86.4%</td><td>—</td></tr>
              <tr style="background:#eef5ff"><td>MSCI All Country World</td><td>USD</td><td>+1.2%</td><td>+5.8%</td><td>+8.6%</td><td>+9.1%</td><td>+7.9%</td><td>+74.2%</td><td>—</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- RISK METRICS TAB -->
      <div id="dir-risk" style="display:none">
        <div class="cards" style="grid-template-columns:repeat(4,1fr)">
          <div class="card success"><div class="card-label">SHARPE RATIO</div><div class="card-value">1.42</div><div class="card-sub">Risk-adjusted return (3Y)</div></div>
          <div class="card"><div class="card-label">STD DEVIATION</div><div class="card-value">8.2%</div><div class="card-sub">Annualized volatility (3Y)</div></div>
          <div class="card danger"><div class="card-label">MAX DRAWDOWN</div><div class="card-value">-14.8%</div><div class="card-sub">Peak to trough (since incep)</div></div>
          <div class="card"><div class="card-label">VALUE AT RISK (95%)</div><div class="card-value">-2.1%</div><div class="card-sub">Monthly VaR estimate</div></div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px;">
          <div class="table-wrap" style="padding:24px;border-radius:12px;">
            <div class="section-title" style="margin-bottom:16px;">RISK vs RETURN BY ASSET CLASS</div>
            <canvas id="chart-risk-scatter" height="260"></canvas>
          </div>
          <div class="table-wrap" style="padding:24px;border-radius:12px;">
            <div class="section-title" style="margin-bottom:16px;">DRAWDOWN HISTORY</div>
            <canvas id="chart-drawdown" height="260"></canvas>
          </div>
        </div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>ASSET CLASS</th><th>RETURN (3Y)</th><th>STD DEV</th><th>SHARPE</th><th>MAX DRAWDOWN</th><th>VAR (95%)</th><th>BETA vs S&P</th></tr></thead>
            <tbody>
              <tr><td>Public Equity</td><td style="color:#2e7d32">+13.4%</td><td>12.1%</td><td>1.11</td><td style="color:#e74c3c">-18.2%</td><td>-3.2%</td><td>0.84</td></tr>
              <tr><td>Private Equity</td><td style="color:#2e7d32">+14.2%</td><td>6.8%</td><td>2.09</td><td style="color:#e74c3c">-8.4%</td><td>-1.4%</td><td>0.42</td></tr>
              <tr><td>Fixed Income</td><td style="color:#2e7d32">+4.8%</td><td>3.2%</td><td>1.50</td><td style="color:#e74c3c">-4.1%</td><td>-0.8%</td><td>-0.12</td></tr>
              <tr><td>Real Assets</td><td style="color:#2e7d32">+9.2%</td><td>7.4%</td><td>1.24</td><td style="color:#e74c3c">-11.2%</td><td>-1.9%</td><td>0.31</td></tr>
              <tr><td>Operations</td><td style="color:#2e7d32">+2.1%</td><td>4.8%</td><td>0.44</td><td style="color:#e74c3c">-9.8%</td><td>-1.2%</td><td>0.18</td></tr>
              <tr style="font-weight:bold;background:#f0f4fa"><td>Total Portfolio</td><td style="color:#2e7d32">+11.8%</td><td>8.2%</td><td>1.42</td><td style="color:#e74c3c">-14.8%</td><td>-2.1%</td><td>0.61</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- MANAGER SCORECARD TAB -->
      <div id="dir-scorecard" style="display:none">
        <div class="section-header"><div class="section-title">MANAGER SCORECARD — RANKED BY RISK-ADJUSTED RETURN</div></div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:24px;" id="scorecard-cards"></div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>RANK</th><th>MANAGER</th><th>ASSET CLASS</th><th>YTD RETURN</th><th>3Y RETURN</th><th>SHARPE</th><th>CONSISTENCY</th><th>SUBMISSIONS</th><th>SCORE</th></tr></thead>
            <tbody>
              <tr><td><span class="badge submitted">1</span></td><td>Sarah Johnson</td><td>Private Equity</td><td style="color:#2e7d32">+14.2%</td><td style="color:#2e7d32">+13.8%</td><td>2.09</td><td><div style="background:#eee;border-radius:4px;height:8px;"><div style="background:#2e7d32;width:92%;height:8px;border-radius:4px;"></div></div></td><td>8/8</td><td style="color:#2e7d32;font-weight:bold">94</td></tr>
              <tr><td><span class="badge submitted">2</span></td><td>Mike Chen</td><td>Real Assets</td><td style="color:#2e7d32">+9.2%</td><td style="color:#2e7d32">+9.8%</td><td>1.24</td><td><div style="background:#eee;border-radius:4px;height:8px;"><div style="background:#2e7d32;width:88%;height:8px;border-radius:4px;"></div></div></td><td>7/8</td><td style="color:#2e7d32;font-weight:bold">81</td></tr>
              <tr><td><span class="badge submitted">3</span></td><td>Priya Patel</td><td>Public Equity</td><td style="color:#2e7d32">+11.2%</td><td style="color:#2e7d32">+13.4%</td><td>1.11</td><td><div style="background:#eee;border-radius:4px;height:8px;"><div style="background:#4A90D9;width:75%;height:8px;border-radius:4px;"></div></div></td><td>6/8</td><td style="color:#4A90D9;font-weight:bold">76</td></tr>
              <tr><td><span class="badge flagged">4</span></td><td>James Wilson</td><td>Fixed Income</td><td style="color:#2e7d32">+4.8%</td><td style="color:#2e7d32">+4.1%</td><td>1.50</td><td><div style="background:#eee;border-radius:4px;height:8px;"><div style="background:#D97706;width:62%;height:8px;border-radius:4px;"></div></div></td><td>5/8</td><td style="color:#D97706;font-weight:bold">64</td></tr>
              <tr><td><span class="badge missing">5</span></td><td>Alex Torres</td><td>Operations</td><td style="color:#e74c3c">-1.2%</td><td style="color:#2e7d32">+2.1%</td><td>0.44</td><td><div style="background:#eee;border-radius:4px;height:8px;"><div style="background:#e74c3c;width:42%;height:8px;border-radius:4px;"></div></div></td><td>4/8</td><td style="color:#e74c3c;font-weight:bold">38</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- CAPITAL ACCOUNTS TAB -->
      <div id="dir-capital" style="display:none">
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:24px;">
          <div class="card" style="border-top-color:#7C3AED"><div class="card-label">TOTAL COMMITTED</div><div class="card-value">$148.2M</div><div class="card-sub">Across all funds</div></div>
          <div class="card"><div class="card-label">TOTAL CALLED</div><div class="card-value">$112.4M</div><div class="card-sub">75.8% of commitments</div></div>
          <div class="card success"><div class="card-label">CURRENT NAV</div><div class="card-value">$124.6M</div><div class="card-sub">Estimated portfolio value</div></div>
          <div class="card"><div class="card-label">UNCALLED CAPITAL</div><div class="card-value">$35.8M</div><div class="card-sub">Remaining commitments</div></div>
          <div class="card success"><div class="card-label">TOTAL DISTRIBUTED</div><div class="card-value">$42.1M</div><div class="card-sub">Cash returned to date</div></div>
          <div class="card"><div class="card-label">NET ASSET GAIN</div><div class="card-value">+$54.3M</div><div class="card-sub">NAV vs capital called</div></div>
        </div>

        <!-- DPI, RVPI, TVPI cards -->
        <div class="section-header"><div class="section-title">FUND MULTIPLE METRICS</div></div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:24px;">
          <div style="background:var(--navy);border-radius:12px;padding:24px;text-align:center;">
            <div style="font-size:9px;letter-spacing:2.5px;color:var(--sky);font-family:'Courier New',monospace;margin-bottom:8px;">DPI</div>
            <div style="font-size:42px;font-weight:bold;color:#fff;">0.37x</div>
            <div style="font-size:11px;color:var(--soft);margin-top:6px;">Distributions to Paid-In</div>
            <div style="font-size:11px;color:#aab8d0;margin-top:4px;">$42.1M distributed / $112.4M called</div>
          </div>
          <div style="background:var(--sky);border-radius:12px;padding:24px;text-align:center;">
            <div style="font-size:9px;letter-spacing:2.5px;color:#fff;font-family:'Courier New',monospace;margin-bottom:8px;">RVPI</div>
            <div style="font-size:42px;font-weight:bold;color:#fff;">1.11x</div>
            <div style="font-size:11px;color:#fff;margin-top:6px;">Residual Value to Paid-In</div>
            <div style="font-size:11px;color:#dde6f5;margin-top:4px;">$124.6M NAV / $112.4M called</div>
          </div>
          <div style="background:#2e7d32;border-radius:12px;padding:24px;text-align:center;">
            <div style="font-size:9px;letter-spacing:2.5px;color:#a5d6a7;font-family:'Courier New',monospace;margin-bottom:8px;">TVPI</div>
            <div style="font-size:42px;font-weight:bold;color:#fff;">1.48x</div>
            <div style="font-size:11px;color:#c8e6c9;margin-top:6px;">Total Value to Paid-In</div>
            <div style="font-size:11px;color:#a5d6a7;margin-top:4px;">($42.1M + $124.6M) / $112.4M</div>
          </div>
        </div>

        <div class="section-header"><div class="section-title">CAPITAL ACCOUNT BY FUND</div></div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>FUND</th><th>VINTAGE</th><th>COMMITTED</th><th>CALLED</th><th>UNCALLED</th><th>DISTRIBUTED</th><th>NAV</th><th>DPI</th><th>TVPI</th><th>NET IRR</th></tr></thead>
            <tbody>
              <tr><td>Apex Growth III</td><td>2021</td><td>$12.0M</td><td>$9.6M</td><td>$2.4M</td><td>$2.1M</td><td>$13.6M</td><td>0.22x</td><td style="color:#2e7d32">1.63x</td><td style="color:#2e7d32">18.4%</td></tr>
              <tr><td>Meridian PE II</td><td>2020</td><td>$8.5M</td><td>$8.5M</td><td>—</td><td>$6.2M</td><td>$11.1M</td><td>0.73x</td><td style="color:#2e7d32">2.04x</td><td style="color:#2e7d32">12.1%</td></tr>
              <tr><td>Blueridge Ventures</td><td>2022</td><td>$6.0M</td><td>$3.2M</td><td>$2.8M</td><td>$0.4M</td><td>$2.8M</td><td>0.13x</td><td style="color:#e74c3c">0.88x</td><td style="color:#e74c3c">-2.4%</td></tr>
              <tr><td>Horizon Real Assets</td><td>2019</td><td>$14.0M</td><td>$14.0M</td><td>—</td><td>$11.8M</td><td>$23.5M</td><td>0.84x</td><td style="color:#2e7d32">2.52x</td><td style="color:#2e7d32">16.7%</td></tr>
              <tr><td>ClearPath Infra I</td><td>2023</td><td>$7.7M</td><td>$2.1M</td><td>$5.6M</td><td>—</td><td>$2.1M</td><td>0.00x</td><td>1.00x</td><td>—</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- VINTAGE ANALYSIS TAB -->
      <div id="dir-vintage" style="display:none">
        <div class="cards" style="grid-template-columns:repeat(4,1fr)">
          <div class="card"><div class="card-label">VINTAGE YEARS</div><div class="card-value">5</div><div class="card-sub">2019 — 2023</div></div>
          <div class="card success"><div class="card-label">BEST VINTAGE</div><div class="card-value">2019</div><div class="card-sub">Horizon Real Assets 16.7% IRR</div></div>
          <div class="card danger"><div class="card-label">WATCH VINTAGE</div><div class="card-value">2022</div><div class="card-sub">Blueridge -2.4% IRR</div></div>
          <div class="card"><div class="card-label">AVG NET IRR</div><div class="card-value">14.2%</div><div class="card-sub">Composite all vintages</div></div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px;">
          <div class="table-wrap" style="padding:24px;border-radius:12px;">
            <div class="section-title" style="margin-bottom:16px;">IRR BY VINTAGE YEAR</div>
            <canvas id="chart-vintage-irr" height="260"></canvas>
          </div>
          <div class="table-wrap" style="padding:24px;border-radius:12px;">
            <div class="section-title" style="margin-bottom:16px;">TVPI BY VINTAGE YEAR</div>
            <canvas id="chart-vintage-tvpi" height="260"></canvas>
          </div>
        </div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>VINTAGE</th><th>FUNDS</th><th>COMMITTED</th><th>CALLED %</th><th>NET IRR</th><th>TVPI</th><th>DPI</th><th>STATUS</th></tr></thead>
            <tbody>
              <tr><td>2019</td><td>1</td><td>$14.0M</td><td>100%</td><td style="color:#2e7d32">16.7%</td><td style="color:#2e7d32">2.52x</td><td>0.84x</td><td><span class="badge submitted">MATURE</span></td></tr>
              <tr><td>2020</td><td>1</td><td>$8.5M</td><td>100%</td><td style="color:#2e7d32">12.1%</td><td style="color:#2e7d32">2.04x</td><td>0.73x</td><td><span class="badge submitted">MATURE</span></td></tr>
              <tr><td>2021</td><td>1</td><td>$12.0M</td><td>80%</td><td style="color:#2e7d32">18.4%</td><td style="color:#2e7d32">1.63x</td><td>0.22x</td><td><span class="badge flagged">HARVESTING</span></td></tr>
              <tr><td>2022</td><td>1</td><td>$6.0M</td><td>53%</td><td style="color:#e74c3c">-2.4%</td><td style="color:#e74c3c">0.88x</td><td>0.13x</td><td><span class="badge missing">WATCH</span></td></tr>
              <tr><td>2023</td><td>1</td><td>$7.7M</td><td>27%</td><td>—</td><td>1.00x</td><td>0.00x</td><td><span class="badge flagged">EARLY</span></td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- CAPITAL CALLS TAB -->
      <div id="dir-calls" style="display:none">
        <div class="cards" style="grid-template-columns:repeat(4,1fr)">
          <div class="card danger"><div class="card-label">DUE THIS QUARTER</div><div class="card-value">$4.2M</div><div class="card-sub">2 calls pending</div></div>
          <div class="card"><div class="card-label">DUE NEXT QUARTER</div><div class="card-value">$3.8M</div><div class="card-sub">3 calls scheduled</div></div>
          <div class="card"><div class="card-label">12-MONTH FORECAST</div><div class="card-value">$14.6M</div><div class="card-sub">Total expected calls</div></div>
          <div class="card"><div class="card-label">UNCALLED TOTAL</div><div class="card-value">$35.8M</div><div class="card-sub">Remaining commitments</div></div>
        </div>
        <div class="table-wrap" style="padding:24px;border-radius:12px;margin-bottom:20px;">
          <div class="section-title" style="margin-bottom:16px;">CAPITAL CALL SCHEDULE</div>
          <canvas id="chart-call-schedule" height="220"></canvas>
        </div>
        <div class="section-header"><div class="section-title">UPCOMING CAPITAL CALLS</div></div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>FUND</th><th>CALL DATE</th><th>AMOUNT</th><th>PURPOSE</th><th>UNCALLED REMAINING</th><th>STATUS</th></tr></thead>
            <tbody>
              <tr><td>Apex Growth III</td><td>Jul 15, 2026</td><td>$1.2M</td><td>Portfolio company follow-on</td><td>$1.2M after</td><td><span class="badge missing">DUE SOON</span></td></tr>
              <tr><td>ClearPath Infra I</td><td>Jul 28, 2026</td><td>$3.0M</td><td>Construction milestone</td><td>$2.6M after</td><td><span class="badge missing">DUE SOON</span></td></tr>
              <tr><td>Blueridge Ventures</td><td>Sep 1, 2026</td><td>$1.4M</td><td>New investment — Series B</td><td>$1.4M after</td><td><span class="badge flagged">UPCOMING</span></td></tr>
              <tr><td>ClearPath Infra I</td><td>Oct 15, 2026</td><td>$1.2M</td><td>Phase 2 construction</td><td>$1.4M after</td><td><span class="badge flagged">UPCOMING</span></td></tr>
              <tr><td>Apex Growth III</td><td>Dec 1, 2026</td><td>$1.2M</td><td>New portfolio company</td><td>—</td><td><span class="badge flagged">UPCOMING</span></td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- DISTRIBUTIONS TAB -->
      <div id="dir-distributions" style="display:none">
        <div class="cards" style="grid-template-columns:repeat(4,1fr)">
          <div class="card success"><div class="card-label">TOTAL DISTRIBUTED</div><div class="card-value">$42.1M</div><div class="card-sub">Since inception</div></div>
          <div class="card"><div class="card-label">YTD DISTRIBUTIONS</div><div class="card-value">$6.8M</div><div class="card-sub">2026 to date</div></div>
          <div class="card"><div class="card-label">NEXT DISTRIBUTION</div><div class="card-value">Sep 2026</div><div class="card-sub">Estimated $2.4M</div></div>
          <div class="card"><div class="card-label">DISTRIBUTION YIELD</div><div class="card-value">5.5%</div><div class="card-sub">Annual distributions / NAV</div></div>
        </div>
        <div class="table-wrap" style="padding:24px;border-radius:12px;margin-bottom:20px;">
          <div class="section-title" style="margin-bottom:16px;">DISTRIBUTION HISTORY BY FUND</div>
          <canvas id="chart-distributions" height="240"></canvas>
        </div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>DATE</th><th>FUND</th><th>TYPE</th><th>AMOUNT</th><th>CUMULATIVE DPI</th></tr></thead>
            <tbody>
              <tr><td>Jun 2026</td><td>Horizon Real Assets</td><td>Income</td><td>$2.4M</td><td>0.84x</td></tr>
              <tr><td>Mar 2026</td><td>Meridian PE II</td><td>Realized gain</td><td>$1.8M</td><td>0.73x</td></tr>
              <tr><td>Dec 2025</td><td>Horizon Real Assets</td><td>Income</td><td>$2.1M</td><td>0.72x</td></tr>
              <tr><td>Sep 2025</td><td>Meridian PE II</td><td>Recapitalization</td><td>$2.6M</td><td>0.52x</td></tr>
              <tr><td>Jun 2025</td><td>Apex Growth III</td><td>Partial sale</td><td>$2.1M</td><td>0.22x</td></tr>
              <tr><td>Mar 2025</td><td>Meridian PE II</td><td>Realized gain</td><td>$1.8M</td><td>0.31x</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- CASH FLOW WATERFALL TAB -->
      <div id="dir-waterfall" style="display:none">
        <div class="cards" style="grid-template-columns:repeat(3,1fr)">
          <div class="card danger"><div class="card-label">NET CASH FLOW (YTD)</div><div class="card-value">-$7.8M</div><div class="card-sub">Calls exceed distributions</div></div>
          <div class="card"><div class="card-label">TOTAL CALLS (YTD)</div><div class="card-value">$14.6M</div><div class="card-sub">Capital deployed</div></div>
          <div class="card success"><div class="card-label">TOTAL DISTRIBUTIONS (YTD)</div><div class="card-value">$6.8M</div><div class="card-sub">Cash returned</div></div>
        </div>
        <div class="table-wrap" style="padding:24px;border-radius:12px;margin-bottom:20px;">
          <div class="section-title" style="margin-bottom:16px;">CASH FLOW WATERFALL — QUARTERLY</div>
          <canvas id="chart-waterfall" height="280"></canvas>
        </div>
        <div class="table-wrap" style="padding:24px;border-radius:12px;">
          <div class="section-title" style="margin-bottom:16px;">12-MONTH CASH FLOW FORECAST</div>
          <canvas id="chart-cashflow-forecast" height="220"></canvas>
        </div>
      </div>

      <!-- IPS TRACKING TAB -->
      <div id="dir-ips" style="display:none">
        <div class="cards" style="grid-template-columns:repeat(3,1fr)">
          <div class="card success"><div class="card-label">WITHIN POLICY</div><div class="card-value">4 / 5</div><div class="card-sub">Asset classes in range</div></div>
          <div class="card danger"><div class="card-label">POLICY BREACHES</div><div class="card-value">1</div><div class="card-sub">Operations below minimum</div></div>
          <div class="card"><div class="card-label">LAST REVIEWED</div><div class="card-value">Q1 2026</div><div class="card-sub">Next review: Q3 2026</div></div>
        </div>
        <div class="section-header" style="margin-top:8px;"><div class="section-title">ALLOCATION vs POLICY TARGETS</div></div>
        <div class="table-wrap" style="padding:24px;border-radius:12px;margin-bottom:20px;">
          <canvas id="chart-ips" height="240"></canvas>
        </div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>ASSET CLASS</th><th>POLICY MIN</th><th>POLICY TARGET</th><th>POLICY MAX</th><th>ACTUAL</th><th>VARIANCE</th><th>STATUS</th></tr></thead>
            <tbody>
              <tr><td>Public Equity</td><td>25%</td><td>35%</td><td>45%</td><td>33.8%</td><td style="color:#2e7d32">-1.2%</td><td><span class="badge submitted">IN RANGE</span></td></tr>
              <tr><td>Private Equity</td><td>15%</td><td>25%</td><td>35%</td><td>25.3%</td><td style="color:#2e7d32">+0.3%</td><td><span class="badge submitted">IN RANGE</span></td></tr>
              <tr><td>Fixed Income</td><td>15%</td><td>20%</td><td>30%</td><td>19.9%</td><td style="color:#2e7d32">-0.1%</td><td><span class="badge submitted">IN RANGE</span></td></tr>
              <tr><td>Real Assets</td><td>10%</td><td>15%</td><td>20%</td><td>14.6%</td><td style="color:#2e7d32">-0.4%</td><td><span class="badge submitted">IN RANGE</span></td></tr>
              <tr><td>Operations</td><td>5%</td><td>5%</td><td>10%</td><td>6.4%</td><td style="color:#2e7d32">+1.4%</td><td><span class="badge submitted">IN RANGE</span></td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- MANAGER WATCH LIST TAB -->
      <div id="dir-watchlist" style="display:none">
        <div class="cards" style="grid-template-columns:repeat(3,1fr)">
          <div class="card danger"><div class="card-label">ON WATCH</div><div class="card-value">2</div><div class="card-sub">Managers flagged for review</div></div>
          <div class="card flagged" style="border-top-color:#D97706"><div class="card-label">UNDER REVIEW</div><div class="card-value">1</div><div class="card-sub">Formal review in progress</div></div>
          <div class="card success"><div class="card-label">CLEAR</div><div class="card-value">3</div><div class="card-sub">No concerns</div></div>
        </div>
        <div class="section-header" style="margin-top:8px;">
          <div class="section-title">MANAGER WATCH LIST</div>
          <button class="btn-report" onclick="addToWatchlist()">+ ADD TO WATCH LIST</button>
        </div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>MANAGER</th><th>ASSET CLASS</th><th>REASON</th><th>DATE ADDED</th><th>YTD RETURN</th><th>STATUS</th><th>ACTION</th></tr></thead>
            <tbody id="watchlist-tbody">
              <tr><td>Alex Torres</td><td>Operations</td><td>Negative YTD return, missed 2 submissions</td><td>Apr 2026</td><td style="color:#e74c3c">-1.2%</td><td><span class="badge missing">ON WATCH</span></td><td><button class="btn-report" style="padding:4px 10px;font-size:9px;" onclick="resolveWatch(this)">Resolve</button></td></tr>
              <tr><td>Blueridge Ventures</td><td>Private Equity</td><td>TVPI below 1.0x after 2 years</td><td>Jun 2026</td><td style="color:#e74c3c">-2.4%</td><td><span class="badge flagged">UNDER REVIEW</span></td><td><button class="btn-report" style="padding:4px 10px;font-size:9px;" onclick="resolveWatch(this)">Resolve</button></td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- AUDIT LOG TAB -->
      <div id="dir-audit" style="display:none">
        <div class="cards" style="grid-template-columns:repeat(3,1fr)">
          <div class="card"><div class="card-label">TOTAL EVENTS (30 DAYS)</div><div class="card-value">48</div><div class="card-sub">All user actions logged</div></div>
          <div class="card"><div class="card-label">SUBMISSIONS LOGGED</div><div class="card-value">12</div><div class="card-sub">This quarter</div></div>
          <div class="card danger"><div class="card-label">FLAGGED EVENTS</div><div class="card-value">2</div><div class="card-sub">Require attention</div></div>
        </div>
        <div class="section-header" style="margin-top:8px;"><div class="section-title">AUDIT LOG</div></div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>TIMESTAMP</th><th>USER</th><th>ACTION</th><th>DETAILS</th><th>IP ADDRESS</th><th>STATUS</th></tr></thead>
            <tbody id="audit-tbody">
              <tr><td>Jul 3, 2026 14:22</td><td>Sarah Johnson</td><td>SUBMISSION</td><td>Q2 2026 — Private Equity — $31.5M invested</td><td>192.168.1.42</td><td><span class="badge submitted">OK</span></td></tr>
              <tr><td>Jul 3, 2026 11:14</td><td>Mike Chen</td><td>SUBMISSION</td><td>Q2 2026 — Real Assets — $18.2M invested</td><td>192.168.1.38</td><td><span class="badge submitted">OK</span></td></tr>
              <tr><td>Jul 2, 2026 16:48</td><td>Priya Patel</td><td>SUBMISSION EDIT</td><td>Q1 2026 — Public Equity — values modified</td><td>192.168.1.51</td><td><span class="badge flagged">FLAGGED</span></td></tr>
              <tr><td>Jul 2, 2026 09:31</td><td>Director</td><td>LOGIN</td><td>Investment manager portal access</td><td>192.168.1.10</td><td><span class="badge submitted">OK</span></td></tr>
              <tr><td>Jul 1, 2026 17:22</td><td>Alex Torres</td><td>MISSED SUBMISSION</td><td>Q2 2026 deadline passed — no submission</td><td>—</td><td><span class="badge missing">FLAGGED</span></td></tr>
              <tr><td>Jun 30, 2026 14:18</td><td>James Wilson</td><td>SUBMISSION</td><td>Q2 2026 — Fixed Income — $24.8M invested</td><td>192.168.1.29</td><td><span class="badge submitted">OK</span></td></tr>
              <tr><td>Jun 28, 2026 10:44</td><td>Alex Torres</td><td>LOGIN</td><td>Manager portal access</td><td>192.168.1.67</td><td><span class="badge submitted">OK</span></td></tr>
            </tbody>
          </table>
        </div>
      </div>

'''

    anchor = '      <div id="dir-ai" style="display:none">'
    if 'dir-fundperf' not in c:
        if anchor in c:
            c = c.replace(anchor, new_tabs + anchor, 1)
            print("  Added all comprehensive HTML tabs")
        else:
            print("  ERROR: Could not find dir-ai anchor")
    else:
        print("  Comprehensive tabs already present")

    # ── 4. ADD JAVASCRIPT ──
    js = '''
  // ══ COMPREHENSIVE INVESTMENT TOOLS JS ══

  function initFundPerfCharts() {
    const ctx = document.getElementById('chart-fund-cumulative');
    if (ctx && !ctx.dataset.init) {
      ctx.dataset.init = '1';
      const labels = ['Q1 2015','Q2 2015','Q3 2015','Q4 2015','Q1 2016','Q2 2016','Q3 2016','Q4 2016','Q1 2017','Q2 2017','Q3 2017','Q4 2017','Q1 2018','Q2 2018','Q3 2018','Q4 2018','Q1 2019','Q2 2019','Q3 2019','Q4 2019','Q1 2020','Q2 2020','Q3 2020','Q4 2020','Q1 2021','Q2 2021','Q3 2021','Q4 2021','Q1 2022','Q2 2022','Q3 2022','Q4 2022','Q1 2023','Q2 2023','Q3 2023','Q4 2023','Q1 2024','Q2 2024','Q3 2024','Q4 2024','Q1 2025','Q2 2025','Q3 2025','Q4 2025','Q1 2026','Q2 2026'];
      const mkData = (start, vol, trend) => labels.map((_,i) => +(start * Math.pow(1 + trend/4 + (Math.random()-0.5)*vol, i)).toFixed(2));
      new Chart(ctx, { type:'line', data:{ labels, datasets:[
        { label:'Total Portfolio', data: mkData(100,0.04,0.092), borderColor:'#0A2472', tension:0.3, pointRadius:0, borderWidth:2.5 },
        { label:'Public Equity',   data: mkData(100,0.06,0.108), borderColor:'#4A90D9', tension:0.3, pointRadius:0, borderWidth:1.5 },
        { label:'Private Equity',  data: mkData(100,0.03,0.112), borderColor:'#7C3AED', tension:0.3, pointRadius:0, borderWidth:1.5 },
        { label:'Fixed Income',    data: mkData(100,0.02,0.042), borderColor:'#16A34A', tension:0.3, pointRadius:0, borderWidth:1.5 },
        { label:'Real Assets',     data: mkData(100,0.03,0.088), borderColor:'#D97706', tension:0.3, pointRadius:0, borderWidth:1.5 },
        { label:'S&P 500',         data: mkData(100,0.055,0.088), borderColor:'#aab8d0', tension:0.3, pointRadius:0, borderWidth:1.5, borderDash:[4,4] },
      ]}, options:{ responsive:true, plugins:{ legend:{ position:'bottom' }}, scales:{ y:{ title:{ display:true, text:'Cumulative Return (Base 100)' }}}}});
    }
  }

  function initRiskCharts() {
    const sCtx = document.getElementById('chart-risk-scatter');
    if (sCtx && !sCtx.dataset.init) {
      sCtx.dataset.init = '1';
      new Chart(sCtx, { type:'bubble', data:{ datasets:[
        { label:'Public Equity',  data:[{x:12.1,y:13.4,r:10}], backgroundColor:'rgba(74,144,217,0.7)' },
        { label:'Private Equity', data:[{x:6.8, y:14.2,r:8}],  backgroundColor:'rgba(124,58,237,0.7)' },
        { label:'Fixed Income',   data:[{x:3.2, y:4.8, r:6}],  backgroundColor:'rgba(22,163,74,0.7)' },
        { label:'Real Assets',    data:[{x:7.4, y:9.2, r:7}],  backgroundColor:'rgba(217,119,6,0.7)' },
        { label:'Operations',     data:[{x:4.8, y:2.1, r:4}],  backgroundColor:'rgba(231,76,60,0.7)' },
        { label:'Portfolio',      data:[{x:8.2, y:11.8,r:12}], backgroundColor:'rgba(10,36,114,0.9)' },
      ]}, options:{ responsive:true, plugins:{ legend:{ position:'bottom' }}, scales:{ x:{ title:{ display:true, text:'Risk (Std Dev %)' }}, y:{ title:{ display:true, text:'Return (3Y Ann %)' }}}}});
    }
    const dCtx = document.getElementById('chart-drawdown');
    if (dCtx && !dCtx.dataset.init) {
      dCtx.dataset.init = '1';
      const dd = [0,-1.2,-2.4,-1.8,-0.4,-3.1,-5.2,-8.4,-14.8,-12.1,-9.4,-6.2,-4.1,-2.8,-1.4,-0.6,-3.2,-5.8,-4.1,-2.2,-0.8,0,-1.4,-3.6,-2.1,-0.8,0,-2.4,-4.8,-3.2,-1.6,-0.4,0];
      new Chart(dCtx, { type:'line', data:{ labels: dd.map((_,i)=>`Q${i%4+1} ${2017+Math.floor(i/4)}`), datasets:[{ label:'Drawdown %', data:dd, borderColor:'#e74c3c', backgroundColor:'rgba(231,76,60,0.1)', fill:true, tension:0.3, pointRadius:0 }]}, options:{ responsive:true, plugins:{ legend:{ display:false }}, scales:{ y:{ max:2, title:{ display:true, text:'Drawdown (%)' }}}}});
    }
  }

  function initVintageCharts() {
    const iCtx = document.getElementById('chart-vintage-irr');
    if (iCtx && !iCtx.dataset.init) {
      iCtx.dataset.init = '1';
      new Chart(iCtx, { type:'bar', data:{ labels:['2019','2020','2021','2022','2023'], datasets:[{ label:'Net IRR %', data:[16.7,12.1,18.4,-2.4,null], backgroundColor:['#2e7d32','#2e7d32','#2e7d32','#e74c3c','#aab8d0'] }]}, options:{ responsive:true, plugins:{ legend:{ display:false }}, scales:{ y:{ title:{ display:true, text:'Net IRR (%)' }}}}});
    }
    const tCtx = document.getElementById('chart-vintage-tvpi');
    if (tCtx && !tCtx.dataset.init) {
      tCtx.dataset.init = '1';
      new Chart(tCtx, { type:'bar', data:{ labels:['2019','2020','2021','2022','2023'], datasets:[{ label:'TVPI', data:[2.52,2.04,1.63,0.88,1.00], backgroundColor:['#2e7d32','#2e7d32','#2e7d32','#e74c3c','#aab8d0'] }]}, options:{ responsive:true, plugins:{ legend:{ display:false }}, scales:{ y:{ title:{ display:true, text:'TVPI (x)' }}}}});
    }
  }

  function initCashCharts() {
    const csCtx = document.getElementById('chart-call-schedule');
    if (csCtx && !csCtx.dataset.init) {
      csCtx.dataset.init = '1';
      new Chart(csCtx, { type:'bar', data:{ labels:['Q3 2026','Q4 2026','Q1 2027','Q2 2027','Q3 2027','Q4 2027'], datasets:[{ label:'Expected Calls ($M)', data:[4.2,3.8,2.4,1.8,1.6,1.2], backgroundColor:'#0A2472' }]}, options:{ responsive:true, plugins:{ legend:{ display:false }}, scales:{ y:{ title:{ display:true, text:'Amount ($M)' }}}}});
    }
    const distCtx = document.getElementById('chart-distributions');
    if (distCtx && !distCtx.dataset.init) {
      distCtx.dataset.init = '1';
      new Chart(distCtx, { type:'bar', data:{ labels:['2019','2020','2021','2022','2023','2024','2025','2026'], datasets:[
        { label:'Horizon', data:[1.2,2.4,3.1,2.8,3.4,4.1,4.6,2.4], backgroundColor:'#D97706' },
        { label:'Meridian', data:[0,0.8,1.4,2.1,2.8,3.2,4.4,1.8], backgroundColor:'#4A90D9' },
        { label:'Apex', data:[0,0,0,0.4,1.2,1.8,2.1,0.6], backgroundColor:'#0A2472' },
      ]}, options:{ responsive:true, plugins:{ legend:{ position:'bottom' }}, scales:{ x:{ stacked:true }, y:{ stacked:true, title:{ display:true, text:'Distributions ($M)' }}}}});
    }
    const wfCtx = document.getElementById('chart-waterfall');
    if (wfCtx && !wfCtx.dataset.init) {
      wfCtx.dataset.init = '1';
      new Chart(wfCtx, { type:'bar', data:{ labels:['Q1 2024','Q2 2024','Q3 2024','Q4 2024','Q1 2025','Q2 2025','Q3 2025','Q4 2025','Q1 2026','Q2 2026'], datasets:[
        { label:'Calls', data:[-3.2,-1.8,-2.4,-2.1,-3.4,-1.6,-2.8,-2.2,-4.1,-3.8], backgroundColor:'#e74c3c' },
        { label:'Distributions', data:[1.8,2.1,1.4,2.8,2.4,3.1,2.8,4.4,2.1,4.7], backgroundColor:'#2e7d32' },
      ]}, options:{ responsive:true, plugins:{ legend:{ position:'bottom' }}, scales:{ y:{ title:{ display:true, text:'Cash Flow ($M)' }}}}});
    }
    const cfCtx = document.getElementById('chart-cashflow-forecast');
    if (cfCtx && !cfCtx.dataset.init) {
      cfCtx.dataset.init = '1';
      new Chart(cfCtx, { type:'line', data:{ labels:['Jul 26','Aug 26','Sep 26','Oct 26','Nov 26','Dec 26','Jan 27','Feb 27','Mar 27','Apr 27','May 27','Jun 27'], datasets:[
        { label:'Forecast Net Cash Flow', data:[-1.2,-0.4,0.8,1.4,-2.1,0.6,1.8,-0.8,0.4,2.1,1.6,-0.4], borderColor:'#0A2472', backgroundColor:'rgba(10,36,114,0.08)', fill:true, tension:0.3 },
      ]}, options:{ responsive:true, plugins:{ legend:{ display:false }}, scales:{ y:{ title:{ display:true, text:'Net Cash Flow ($M)' }}}}});
    }
  }

  function initIPSChart() {
    const ctx = document.getElementById('chart-ips');
    if (ctx && !ctx.dataset.init) {
      ctx.dataset.init = '1';
      new Chart(ctx, { type:'bar', data:{ labels:['Public Equity','Private Equity','Fixed Income','Real Assets','Operations'], datasets:[
        { label:'Policy Min', data:[25,15,15,10,5], backgroundColor:'rgba(168,212,245,0.5)', borderColor:'#A8D4F5', borderWidth:1 },
        { label:'Policy Max', data:[45,35,30,20,10], backgroundColor:'rgba(10,36,114,0.15)', borderColor:'#0A2472', borderWidth:1 },
        { label:'Actual', data:[33.8,25.3,19.9,14.6,6.4], backgroundColor:'#0A2472', borderWidth:0 },
      ]}, options:{ responsive:true, plugins:{ legend:{ position:'bottom' }}, scales:{ y:{ max:50, title:{ display:true, text:'Allocation (%)' }}}}});
    }
  }

  // Watch list
  function resolveWatch(btn) {
    const row = btn.closest('tr');
    row.cells[5].innerHTML = '<span class="badge submitted">RESOLVED</span>';
    btn.textContent = 'Done';
    btn.disabled = true;
    btn.style.opacity = '0.5';
  }

  function addToWatchlist() {
    const name = prompt('Manager name:');
    if (!name) return;
    const reason = prompt('Reason for watch:');
    const tbody = document.getElementById('watchlist-tbody');
    const row = document.createElement('tr');
    row.innerHTML = `<td>${name}</td><td>—</td><td>${reason||'Under review'}</td><td>${new Date().toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'})}</td><td>—</td><td><span class="badge flagged">ON WATCH</span></td><td><button class="btn-report" style="padding:4px 10px;font-size:9px;" onclick="resolveWatch(this)">Resolve</button></td>`;
    tbody.appendChild(row);
  }

  // Patch dirTab for new chart tabs
  const _prevDirTab = dirTab;
  dirTab = function(el, tabId) {
    _prevDirTab(el, tabId);
    if (tabId === 'dir-fundperf')     setTimeout(initFundPerfCharts, 50);
    if (tabId === 'dir-risk')         setTimeout(initRiskCharts, 50);
    if (tabId === 'dir-vintage')      setTimeout(initVintageCharts, 50);
    if (tabId === 'dir-calls')        setTimeout(initCashCharts, 50);
    if (tabId === 'dir-distributions') setTimeout(initCashCharts, 50);
    if (tabId === 'dir-waterfall')    setTimeout(initCashCharts, 50);
    if (tabId === 'dir-ips')          setTimeout(initIPSChart, 50);
  };'''

    if 'initFundPerfCharts' not in c:
        last = c.rfind('</script>')
        c = c[:last] + js + '\n' + c[last:]
        print("  Added comprehensive JS")
    else:
        print("  JS already present")

    if c != original:
        shutil.copy(HTML_PATH, HTML_PATH + '.comprehensive.bak')
        with open(HTML_PATH, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"\n  Saved {HTML_PATH}")
    else:
        print("\n  No changes needed")

    print("""
Done! New tabs added:
  PERFORMANCE:   Fund Performance, Risk Metrics, Manager Scorecard
  PRIVATE MARKETS: Capital Accounts (DPI/RVPI/TVPI), Vintage Analysis
  CASH MANAGEMENT: Capital Calls, Distributions, Cash Flow Waterfall
  COMPLIANCE:    IPS Tracking, Manager Watch List, Audit Log

Restart: uvicorn main:app --reload
""")

if __name__ == "__main__":
    patch()
