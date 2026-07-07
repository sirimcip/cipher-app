with open('templates/index.html', encoding='utf-8') as f:
    c = f.read()

# Replace the static market data card values and chart JS with live fetching
old_js = "  // Market data charts\n  function initMarketCharts() {"

new_js = """  // ── LIVE MARKET DATA ──
  const AV_KEY = "JPSR2HXKEFAJ9M3W";
  const AV = "https://www.alphavantage.co/query";

  async function fetchQuote(symbol) {
    try {
      const res = await fetch(`${AV}?function=GLOBAL_QUOTE&symbol=${symbol}&apikey=${AV_KEY}`);
      const data = await res.json();
      return data['Global Quote'] || null;
    } catch(e) { return null; }
  }

  async function fetchTreasury(maturity) {
    try {
      const res = await fetch(`${AV}?function=TREASURY_YIELD&interval=monthly&maturity=${maturity}&apikey=${AV_KEY}`);
      const data = await res.json();
      return data.data?.[0]?.value || null;
    } catch(e) { return null; }
  }

  async function fetchInflation() {
    try {
      const res = await fetch(`${AV}?function=CPI&interval=monthly&apikey=${AV_KEY}`);
      const data = await res.json();
      return data.data?.[0]?.value || null;
    } catch(e) { return null; }
  }

  async function loadLiveMarketData() {
    // Show loading state
    const cards = document.querySelectorAll('#dir-market .card-value');
    cards.forEach(c => c.textContent = '...');

    // Fetch all in parallel
    const [spy, qqq, iwm, treasury10, treasury2, cpi] = await Promise.all([
      fetchQuote('SPY'),
      fetchQuote('QQQ'),
      fetchQuote('IWM'),
      fetchTreasury('10year'),
      fetchTreasury('2year'),
      fetchInflation()
    ]);

    // Update cards
    if (spy) {
      const spyPrice  = parseFloat(spy['05. price']).toFixed(2);
      const spyChange = parseFloat(spy['10. change percent']).toFixed(2);
      document.getElementById('live-sp500').textContent = `$${spyPrice}`;
      document.getElementById('live-sp500-change').textContent = `${spyChange}% today`;
      document.getElementById('live-sp500-change').style.color = spyChange >= 0 ? '#2e7d32' : '#e74c3c';
    }
    if (qqq) {
      const qqqChange = parseFloat(qqq['10. change percent']).toFixed(2);
      document.getElementById('live-nasdaq').textContent = `${qqqChange > 0 ? '+' : ''}${qqqChange}%`;
    }
    if (iwm) {
      const iwmChange = parseFloat(iwm['10. change percent']).toFixed(2);
      document.getElementById('live-russell').textContent = `${iwmChange > 0 ? '+' : ''}${iwmChange}%`;
    }
    if (treasury10) {
      document.getElementById('live-10yr').textContent = `${parseFloat(treasury10).toFixed(2)}%`;
    }
    if (cpi) {
      document.getElementById('live-cpi').textContent = `${parseFloat(cpi).toFixed(1)}%`;
    }

    // Update market reference table
    updateMarketTable(spy, qqq, iwm, treasury10, treasury2);
  }

  function updateMarketTable(spy, qqq, iwm, t10, t2) {
    const tbody = document.getElementById('live-market-tbody');
    if (!tbody) return;
    const rows = [];
    if (spy) rows.push(`<tr><td>S&P 500 (SPY)</td><td>$${parseFloat(spy['05. price']).toFixed(2)}</td><td>${parseFloat(spy['09. change']).toFixed(2)}</td><td style="color:${parseFloat(spy['10. change percent']) >= 0 ? '#2e7d32' : '#e74c3c'}">${parseFloat(spy['10. change percent']).toFixed(2)}%</td></tr>`);
    if (qqq) rows.push(`<tr><td>NASDAQ 100 (QQQ)</td><td>$${parseFloat(qqq['05. price']).toFixed(2)}</td><td>${parseFloat(qqq['09. change']).toFixed(2)}</td><td style="color:${parseFloat(qqq['10. change percent']) >= 0 ? '#2e7d32' : '#e74c3c'}">${parseFloat(qqq['10. change percent']).toFixed(2)}%</td></tr>`);
    if (iwm) rows.push(`<tr><td>Russell 2000 (IWM)</td><td>$${parseFloat(iwm['05. price']).toFixed(2)}</td><td>${parseFloat(iwm['09. change']).toFixed(2)}</td><td style="color:${parseFloat(iwm['10. change percent']) >= 0 ? '#2e7d32' : '#e74c3c'}">${parseFloat(iwm['10. change percent']).toFixed(2)}%</td></tr>`);
    if (t10) rows.push(`<tr><td>10-Year Treasury</td><td>${parseFloat(t10).toFixed(2)}%</td><td>—</td><td>—</td></tr>`);
    if (t2)  rows.push(`<tr><td>2-Year Treasury</td><td>${parseFloat(t2).toFixed(2)}%</td><td>—</td><td>—</td></tr>`);
    tbody.innerHTML = rows.join('') || '<tr><td colspan="4" style="text-align:center;color:#aab8d0;">Loading live data...</td></tr>';
  }

  // Market data charts\n  function initMarketCharts() {"""

if 'AV_KEY' not in c:
    c = c.replace(old_js, new_js, 1)
    print("Added live market data JS")
else:
    print("Live market JS already present, skipping")

# Replace static market data cards with live IDs
old_cards = '''        <div class="cards" style="grid-template-columns:repeat(4,1fr)">
          <div class="card"><div class="card-label">FED FUNDS RATE</div><div class="card-value">4.75%</div><div class="card-sub">Last set Mar 2026</div></div>
          <div class="card"><div class="card-label">10-YR TREASURY</div><div class="card-value">4.32%</div><div class="card-sub">As of Q2 2026</div></div>
          <div class="card danger"><div class="card-label">CPI INFLATION (YOY)</div><div class="card-value">3.1%</div><div class="card-sub">Above 2% target</div></div>
          <div class="card"><div class="card-label">GDP GROWTH (YOY)</div><div class="card-value">2.4%</div><div class="card-sub">Q1 2026 estimate</div></div>
        </div>'''

new_cards = '''        <div class="cards" style="grid-template-columns:repeat(4,1fr)">
          <div class="card"><div class="card-label">S&P 500 (SPY)</div><div class="card-value" id="live-sp500">—</div><div class="card-sub" id="live-sp500-change">Loading...</div></div>
          <div class="card"><div class="card-label">10-YR TREASURY</div><div class="card-value" id="live-10yr">—</div><div class="card-sub">Live yield</div></div>
          <div class="card danger"><div class="card-label">CPI INFLATION (YOY)</div><div class="card-value" id="live-cpi">—</div><div class="card-sub">Above 2% target</div></div>
          <div class="card"><div class="card-label">NASDAQ 100 (QQQ)</div><div class="card-value" id="live-nasdaq">—</div><div class="card-sub">Daily change</div></div>
        </div>'''

if 'live-sp500' not in c:
    c = c.replace(old_cards, new_cards, 1)
    print("Updated market data cards with live IDs")

# Replace static market table with live table
old_table = '''        <div class="section-header"><div class="section-title">MARKET REFERENCE DATA</div></div>
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
        </div>'''

new_table = '''        <div class="section-header">
          <div class="section-title">LIVE MARKET REFERENCE DATA</div>
          <div style="font-size:10px;color:#aab8d0;font-family:'Courier New',monospace;">Powered by Alpha Vantage · Refreshes on tab open</div>
        </div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>INDEX / INDICATOR</th><th>PRICE / VALUE</th><th>CHANGE</th><th>CHANGE %</th></tr></thead>
            <tbody id="live-market-tbody"><tr><td colspan="4" style="text-align:center;color:#aab8d0;padding:20px;">Loading live market data...</td></tr></tbody>
          </table>
        </div>'''

if 'live-market-tbody' not in c:
    c = c.replace(old_table, new_table, 1)
    print("Updated market table with live data")

# Patch dirTab to call loadLiveMarketData when market tab opens
old_dirtab_patch = "    if (tabId === 'dir-benchmark') setTimeout(initBenchmarkCharts, 50);\n    if (tabId === 'dir-market')    setTimeout(initMarketCharts, 50);"
new_dirtab_patch = "    if (tabId === 'dir-benchmark') setTimeout(initBenchmarkCharts, 50);\n    if (tabId === 'dir-market')    { setTimeout(initMarketCharts, 50); loadLiveMarketData(); }"

if 'loadLiveMarketData' not in c:
    c = c.replace(old_dirtab_patch, new_dirtab_patch, 1)
    print("Patched dirTab to load live data")

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Done — restart uvicorn and open Market Data tab")
