with open('routes.py', encoding='utf-8') as f:
    c = f.read()

# Add import for urllib at top if not there
if 'import urllib' not in c:
    c = 'import urllib.request\nimport json as json_lib\n' + c
    print("Added urllib import")

new_route = '''

# ── MARKET DATA PROXY (Alpha Vantage) ──
AV_KEY = "JPSR2HXKEFAJ9M3W"
AV_BASE = "https://www.alphavantage.co/query"

@router.get("/market/quote/{symbol}")
def get_quote(symbol: str):
    try:
        url = f"{AV_BASE}?function=GLOBAL_QUOTE&symbol={symbol}&apikey={AV_KEY}"
        with urllib.request.urlopen(url, timeout=8) as r:
            data = json_lib.loads(r.read())
        return data.get("Global Quote", {})
    except Exception as e:
        return {"error": str(e)}

@router.get("/market/treasury/{maturity}")
def get_treasury(maturity: str):
    try:
        url = f"{AV_BASE}?function=TREASURY_YIELD&interval=monthly&maturity={maturity}&apikey={AV_KEY}"
        with urllib.request.urlopen(url, timeout=8) as r:
            data = json_lib.loads(r.read())
        items = data.get("data", [])
        return {"value": items[0]["value"] if items else None}
    except Exception as e:
        return {"error": str(e)}

@router.get("/market/cpi")
def get_cpi():
    try:
        url = f"{AV_BASE}?function=CPI&interval=monthly&apikey={AV_KEY}"
        with urllib.request.urlopen(url, timeout=8) as r:
            data = json_lib.loads(r.read())
        items = data.get("data", [])
        return {"value": items[0]["value"] if items else None}
    except Exception as e:
        return {"error": str(e)}
'''

if '/market/quote' not in c:
    c += new_route
    print("Added market data routes")
else:
    print("Market routes already present")

with open('routes.py', 'w', encoding='utf-8') as f:
    f.write(c)

# Now update the frontend JS to call our backend instead of Alpha Vantage directly
with open('templates/index.html', encoding='utf-8') as f:
    h = f.read()

old_fetch = '''  async function fetchQuote(symbol) {
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
  }'''

new_fetch = '''  async function fetchQuote(symbol) {
    try {
      const res = await fetch(`${API}/market/quote/${symbol}`);
      return await res.json();
    } catch(e) { return null; }
  }

  async function fetchTreasury(maturity) {
    try {
      const res = await fetch(`${API}/market/treasury/${maturity}`);
      const data = await res.json();
      return data.value || null;
    } catch(e) { return null; }
  }

  async function fetchInflation() {
    try {
      const res = await fetch(`${API}/market/cpi`);
      const data = await res.json();
      return data.value || null;
    } catch(e) { return null; }
  }'''

if old_fetch in h:
    h = h.replace(old_fetch, new_fetch, 1)
    print("Updated frontend to use backend proxy")
elif 'market/quote' in h:
    print("Frontend already using backend proxy")
else:
    print("WARNING: Could not find fetch functions to update")

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(h)

print("Done — restart uvicorn and open Market Data tab")
