"""
CIPHER - Make new accounts start fresh (no more "Sarah Johnson" demo data
showing up on every new signup).

What this does:
- The Portfolio Analytics, Exposure, Liquidity, Private Markets, Benchmarks,
  and Opportunity Pipeline tabs had hardcoded example numbers/names baked
  directly into the page. Every account saw the same fake data.
- After this patch: only your one real test account (Sarah Johnson,
  sarah@childrens.org) still sees that example data. Every other account —
  new or existing — sees a clean "No data yet" state instead.

Run this from inside your cipher_app folder:
    python fix_fresh_accounts.py
"""
import re
import os

FILE = os.path.join("templates", "index.html")

if not os.path.exists(FILE):
    print(f"ERROR: Could not find {FILE}")
    print("Make sure you run this script from inside your cipher_app folder.")
    raise SystemExit(1)

with open(FILE, "r", encoding="utf-8") as f:
    content = f.read()

if "DEMO_ACCOUNT_ID" in content:
    print("Already patched — no changes made.")
    raise SystemExit(0)

changes = 0

# ── 1. Give the 5 unlabeled demo tables unique IDs so we can target them ──
tbody_targets = [
    ("<thead><tr><th>ASSET CLASS</th><th>VALUE</th><th>WEIGHT</th><th>RETURN (YTD)</th><th>BENCHMARK</th><th>ALPHA</th></tr></thead>\n            <tbody>",
     "analytics-tbody", 6),
    ("<thead><tr><th>SECTOR</th><th>EXPOSURE</th><th>% OF PORTFOLIO</th><th>LONG</th><th>SHORT</th><th>NET</th></tr></thead>\n            <tbody>",
     "exposure-tbody", 6),
    ("<thead><tr><th>FUND / HOLDING</th><th>VALUE (USD)</th><th>CURRENCY</th><th>FX RATE</th><th>LIQUIDITY</th><th>NEXT REDEMPTION</th></tr></thead>\n            <tbody>",
     "liquidity-tbody", 6),
    ("<thead><tr><th>FUND</th><th>VINTAGE</th><th>COMMITTED</th><th>CALLED</th><th>DISTRIBUTED</th><th>NET IRR</th><th>TVPI</th><th>FEES (YTD)</th></tr></thead>\n            <tbody>",
     "vintage-tbody", 8),
    ("<thead><tr><th>ASSET CLASS</th><th>WEIGHT</th><th>RETURN</th><th>CONTRIBUTION</th><th>BENCHMARK</th><th>ACTIVE RETURN</th></tr></thead>\n          <tbody>",
     "benchmark-tbody", 6),
]

for thead_snippet, new_id, colspan in tbody_targets:
    if thead_snippet not in content:
        print(f"WARNING: could not find table for {new_id} — skipping (check manually).")
        continue
    replacement = thead_snippet.replace("<tbody>", f'<tbody id="{new_id}">')
    content = content.replace(thead_snippet, replacement, 1)
    changes += 1

# ── 2. Add the gating JS right after the "PORTAL NAV" section marker ──
gate_js = """
  // ══ FRESH ACCOUNT GATING ══
  // Only this one seeded test account keeps the demo example data.
  // Every other account sees a clean, empty state instead.
  const DEMO_ACCOUNT_ID = 2;
  function isDemoAccount() { return currentUser && currentUser.user_id === DEMO_ACCOUNT_ID; }

  function emptyStateRow(colspan, msg) {
    return `<tr><td colspan="${colspan}" style="text-align:center;color:#aab8d0;font-family:'Courier New',monospace;font-size:12px;padding:30px;">${msg}</td></tr>`;
  }

  function emptyChart(canvasId) {
    const c = document.getElementById(canvasId);
    if (!c || c.dataset.emptied) return;
    c.dataset.emptied = '1';
    c.style.display = 'none';
    const msg = document.createElement('div');
    msg.style.cssText = 'text-align:center;color:#aab8d0;font-family:Courier New,monospace;font-size:12px;padding:40px;';
    msg.textContent = 'No data yet — this will populate once your institution submits portfolio data.';
    c.parentNode.appendChild(msg);
  }

  function applyFreshAccountState() {
    if (isDemoAccount()) return; // real test account keeps its example data

    const emptyTables = [
      ['analytics-tbody', 6, 'No portfolio analytics yet.'],
      ['exposure-tbody', 6, 'No exposure data yet.'],
      ['liquidity-tbody', 6, 'No liquidity data yet.'],
      ['vintage-tbody', 8, 'No private markets data yet.'],
      ['benchmark-tbody', 6, 'No benchmark data yet.'],
      ['pipeline-tbody', 8, 'No opportunities in your pipeline yet.'],
    ];
    emptyTables.forEach(([id, colspan, msg]) => {
      const el = document.getElementById(id);
      if (el) el.innerHTML = emptyStateRow(colspan, msg);
    });

    ['chart-perf-class','chart-port-value','chart-sector','chart-geo','chart-type',
     'chart-liquidity','chart-currency','chart-jcurve','chart-cashflow',
     'chart-benchmark','chart-attribution'].forEach(emptyChart);
  }

  // ══ PORTAL NAV ══"""

content = content.replace("  // ══ PORTAL NAV ══", gate_js, 1)
if "FRESH ACCOUNT GATING" in content:
    changes += 1
else:
    print("WARNING: could not insert gating JS block — check manually.")

# ── 3. Stop initAnalyticsCharts / initBenchmarkCharts from drawing fake charts for non-demo accounts ──
content, n = content.replace(
    "function initAnalyticsCharts() {\n    // Performance by asset class",
    "function initAnalyticsCharts() {\n    if (!isDemoAccount()) { applyFreshAccountState(); return; }\n    // Performance by asset class",
    1
), None
if "if (!isDemoAccount()) { applyFreshAccountState(); return; }" in content:
    changes += 1
else:
    print("WARNING: could not patch initAnalyticsCharts — check manually.")

content = content.replace(
    "function initBenchmarkCharts() {\n    const bCtx",
    "function initBenchmarkCharts() {\n    if (!isDemoAccount()) { applyFreshAccountState(); return; }\n    const bCtx",
    1
)
if "function initBenchmarkCharts() {\n    if (!isDemoAccount())" in content:
    changes += 1
else:
    print("WARNING: could not patch initBenchmarkCharts — check manually.")

# ── 4. Call applyFreshAccountState() once when the director dashboard loads ──
content = content.replace(
    "function enterDashboard() {\n    if (currentUser.role === 'investment_manager') {\n      show('director-dash');\n      loadDirectorData();",
    "function enterDashboard() {\n    if (currentUser.role === 'investment_manager') {\n      show('director-dash');\n      loadDirectorData();\n      applyFreshAccountState();",
    1
)
if "loadDirectorData();\n      applyFreshAccountState();" in content:
    changes += 1
else:
    print("WARNING: could not hook applyFreshAccountState() into enterDashboard — check manually.")

with open(FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Applied {changes}/8 patches.")
print("Done. Now upload templates/index.html to GitHub to deploy.")
