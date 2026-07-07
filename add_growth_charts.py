"""
CIPHER Growth Chart Auto-Installer
-----------------------------------
Run this ONCE from inside your cipher_app folder:

    python add_growth_charts.py

It will:
  1. Back up index.html and routes.py (as .bak files) before touching anything.
  2. Insert the Chart.js <script> tag into <head> of templates/index.html.
  3. Insert the manager growth chart HTML into the My History tab.
  4. Insert the director growth chart HTML into the Dashboard (overview) tab.
  5. Insert the JavaScript that draws both charts, right before </script></body>.
  6. Insert the new /submissions/history/all route into routes.py.

If any expected anchor text is not found, it will stop and tell you exactly
what it couldn't find, without changing anything in that file.
"""

import os
import shutil
import sys

HTML_PATH = os.path.join("templates", "index.html")
ROUTES_PATH = "routes.py"


def backup(path):
    bak = path + ".bak"
    shutil.copy(path, bak)
    print(f"  Backed up {path} -> {bak}")


def patch_html():
    if not os.path.exists(HTML_PATH):
        print(f"ERROR: Could not find {HTML_PATH}. Run this script from inside cipher_app/.")
        sys.exit(1)

    with open(HTML_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # ── 1. Insert Chart.js into <head> ──
    head_anchor = "</head>"
    chartjs_tag = '<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>\n</head>'
    if head_anchor not in content:
        print("ERROR: Could not find </head> in index.html. No changes made.")
        sys.exit(1)
    if "chart.umd.min.js" not in content:
        content = content.replace(head_anchor, chartjs_tag, 1)
        print("  Added Chart.js script tag to <head>")
    else:
        print("  Chart.js tag already present, skipping")

    # ── 2. Insert manager chart HTML inside mgr-history, after its table-wrap closes ──
    mgr_anchor = """            </tbody>
          </table>
        </div>
      </div>

    </div>
  </div>
</div>

<script>"""
    mgr_chart_block = """            </tbody>
          </table>
        </div>

        <div class="section-header" style="margin-top:32px">
          <div class="section-title">MY GROWTH OVER TIME</div>
        </div>
        <div style="background:var(--white);border-radius:12px;padding:24px;">
          <div style="display:flex;gap:8px;margin-bottom:16px;">
            <button class="btn-report" onclick="setMgrChartMetric('cumulative_value', this)" style="background:var(--navy)">Cumulative Value</button>
            <button class="btn-report" onclick="setMgrChartMetric('net_change', this)" style="background:var(--soft);color:var(--navy)">Gain / Loss</button>
            <button class="btn-report" onclick="setMgrChartMetric('pct_return', this)" style="background:var(--soft);color:var(--navy)">% Return</button>
          </div>
          <canvas id="managerGrowthChart" height="280"></canvas>
        </div>
      </div>

    </div>
  </div>
</div>

<script>"""
    if "managerGrowthChart" not in content:
        if mgr_anchor not in content:
            print("ERROR: Could not find the manager-history closing block. No HTML changes made.")
            print("       (The file may have been edited since this script was written.)")
            sys.exit(1)
        content = content.replace(mgr_anchor, mgr_chart_block, 1)
        print("  Added manager growth chart HTML")
    else:
        print("  Manager chart HTML already present, skipping")

    # ── 3. Insert director chart HTML at end of dir-overview, before SUBMISSIONS TAB comment ──
    dir_anchor = """            </tbody>
          </table>
        </div>
      </div>

      <!-- SUBMISSIONS TAB -->"""
    dir_chart_block = """            </tbody>
          </table>
        </div>

        <div class="section-header" style="margin-top:32px">
          <div class="section-title">PORTFOLIO GROWTH OVER TIME</div>
        </div>
        <div style="background:var(--white);border-radius:12px;padding:24px;">
          <div style="display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap;">
            <button class="btn-report" onclick="setDirChartGroup('manager', this)" style="background:var(--navy)">By Manager</button>
            <button class="btn-report" onclick="setDirChartGroup('asset_class', this)" style="background:var(--soft);color:var(--navy)">By Asset Class</button>
          </div>
          <div style="display:flex;gap:8px;margin-bottom:16px;">
            <button class="btn-report" onclick="setDirChartMetric('cumulative_value', this)" style="background:var(--navy)">Cumulative Value</button>
            <button class="btn-report" onclick="setDirChartMetric('net_change', this)" style="background:var(--soft);color:var(--navy)">Gain / Loss</button>
            <button class="btn-report" onclick="setDirChartMetric('pct_return', this)" style="background:var(--soft);color:var(--navy)">% Return</button>
          </div>
          <canvas id="directorGrowthChart" height="320"></canvas>
        </div>
      </div>

      <!-- SUBMISSIONS TAB -->"""
    if "directorGrowthChart" not in content:
        if dir_anchor not in content:
            print("ERROR: Could not find the dir-overview closing block. No HTML changes made past this point.")
            sys.exit(1)
        content = content.replace(dir_anchor, dir_chart_block, 1)
        print("  Added director growth chart HTML")
    else:
        print("  Director chart HTML already present, skipping")

    # ── 4. Insert chart JavaScript right before the final </script></body> ──
    js_anchor = """    } catch (e) {
      console.error("Could not load director data", e);
    }
  }
</script>
</body>
</html>"""
    chart_js = """    } catch (e) {
      console.error("Could not load director data", e);
    }
  }

  // ══════════════════════════════
  // GROWTH CHARTS
  // ══════════════════════════════
  let fullHistory = [];
  let mgrChartMetric = 'cumulative_value';
  let dirChartMetric = 'cumulative_value';
  let dirChartGroup = 'manager';
  let mgrChartInstance = null;
  let dirChartInstance = null;

  const METRIC_LABELS = {
    cumulative_value: "Cumulative Value ($)",
    net_change: "Gain / Loss ($)",
    pct_return: "% Return"
  };
  const NAVY = "#0A2472", SKY = "#4A90D9", SOFT = "#A8D4F5";
  const PALETTE = [NAVY, SKY, SOFT, "#7C3AED", "#16A34A", "#DC2626", "#D97706", "#0891B2"];

  async function fetchFullHistory() {
    try {
      const res = await fetch(`${API}/submissions/history/all`);
      const data = await res.json();
      fullHistory = data.history || [];
    } catch (e) {
      console.error("Could not load growth history", e);
      fullHistory = [];
    }
  }

  function getPeriods(rows) {
    return [...new Set(rows.map(r => r.period))];
  }

  function average(arr) {
    if (!arr.length) return 0;
    return arr.reduce((a, b) => a + b, 0) / arr.length;
  }

  function setMgrChartMetric(metric, btn) {
    mgrChartMetric = metric;
    document.querySelectorAll('#mgr-history .btn-report').forEach(b => {
      b.style.background = 'var(--soft)'; b.style.color = 'var(--navy)';
    });
    btn.style.background = 'var(--navy)'; btn.style.color = '#fff';
    renderManagerChart();
  }

  function setDirChartMetric(metric, btn) {
    dirChartMetric = metric;
    const row = btn.closest('div').parentElement.querySelectorAll('div')[1];
    document.querySelectorAll('#dir-overview .btn-report').forEach(b => {
      if (['cumulative_value','net_change','pct_return'].some(m => b.getAttribute('onclick')?.includes(m))) {
        b.style.background = 'var(--soft)'; b.style.color = 'var(--navy)';
      }
    });
    btn.style.background = 'var(--navy)'; btn.style.color = '#fff';
    renderDirectorChart();
  }

  function setDirChartGroup(group, btn) {
    dirChartGroup = group;
    document.querySelectorAll('#dir-overview .btn-report').forEach(b => {
      if (['manager','asset_class'].some(g => b.getAttribute('onclick')?.includes(`'${g}'`) && b.getAttribute('onclick')?.includes('setDirChartGroup'))) {
        b.style.background = 'var(--soft)'; b.style.color = 'var(--navy)';
      }
    });
    btn.style.background = 'var(--navy)'; btn.style.color = '#fff';
    renderDirectorChart();
  }

  function renderManagerChart() {
    const canvas = document.getElementById('managerGrowthChart');
    if (!canvas || !currentUser) return;
    const myRows = fullHistory.filter(h => h.manager_id === currentUser.user_id);
    const myAssetClass = myRows[0]?.asset_class;
    const peerRows = fullHistory.filter(h => h.asset_class === myAssetClass);
    const periods = getPeriods(peerRows.length ? peerRows : myRows);

    const myData = periods.map(p => myRows.find(r => r.period === p)?.[mgrChartMetric] ?? null);
    const benchmarkData = periods.map(p => {
      const peers = peerRows.filter(r => r.period === p && r.manager_id !== currentUser.user_id);
      return peers.length ? average(peers.map(r => r[mgrChartMetric])) : null;
    });

    if (mgrChartInstance) mgrChartInstance.destroy();
    mgrChartInstance = new Chart(canvas, {
      type: 'line',
      data: {
        labels: periods,
        datasets: [
          { label: 'You', data: myData, borderColor: NAVY, backgroundColor: NAVY, tension: 0.3, spanGaps: true },
          { label: (myAssetClass || 'Peer') + ' Average', data: benchmarkData, borderColor: SKY, backgroundColor: SKY, borderDash: [6,4], tension: 0.3, spanGaps: true }
        ]
      },
      options: {
        responsive: true,
        plugins: { legend: { position: 'bottom' } },
        scales: { y: { title: { display: true, text: METRIC_LABELS[mgrChartMetric] } } }
      }
    });
  }

  function renderDirectorChart() {
    const canvas = document.getElementById('directorGrowthChart');
    if (!canvas) return;
    const periods = getPeriods(fullHistory);
    let datasets = [];

    if (dirChartGroup === 'manager') {
      const managerIds = [...new Set(fullHistory.map(h => h.manager_id))];
      datasets = managerIds.map((id, i) => {
        const rows = fullHistory.filter(h => h.manager_id === id);
        return {
          label: rows[0]?.manager_name || `Manager ${id}`,
          data: periods.map(p => rows.find(r => r.period === p)?.[dirChartMetric] ?? null),
          borderColor: PALETTE[i % PALETTE.length],
          backgroundColor: PALETTE[i % PALETTE.length],
          tension: 0.3, spanGaps: true
        };
      });
    } else {
      const assetClasses = [...new Set(fullHistory.map(h => h.asset_class).filter(Boolean))];
      datasets = assetClasses.map((ac, i) => {
        const rows = fullHistory.filter(h => h.asset_class === ac);
        return {
          label: ac,
          data: periods.map(p => {
            const atP = rows.filter(r => r.period === p);
            return atP.length ? average(atP.map(r => r[dirChartMetric])) : null;
          }),
          borderColor: PALETTE[i % PALETTE.length],
          backgroundColor: PALETTE[i % PALETTE.length],
          tension: 0.3, spanGaps: true
        };
      });
    }

    if (dirChartInstance) dirChartInstance.destroy();
    dirChartInstance = new Chart(canvas, {
      type: 'line',
      data: { labels: periods, datasets },
      options: {
        responsive: true,
        plugins: { legend: { position: 'bottom' } },
        scales: { y: { title: { display: true, text: METRIC_LABELS[dirChartMetric] } } }
      }
    });
  }

  // Hook into existing load functions so charts populate automatically
  const _origLoadManagerHistory = loadManagerHistory;
  loadManagerHistory = async function() {
    await _origLoadManagerHistory();
    await fetchFullHistory();
    renderManagerChart();
  };

  const _origLoadDirectorData = loadDirectorData;
  loadDirectorData = async function() {
    await _origLoadDirectorData();
    await fetchFullHistory();
    renderDirectorChart();
  };
</script>
</body>
</html>"""
    if "GROWTH CHARTS" not in content:
        if js_anchor not in content:
            print("ERROR: Could not find the end-of-script anchor. No JS changes made.")
            sys.exit(1)
        content = content.replace(js_anchor, chart_js, 1)
        print("  Added growth chart JavaScript")
    else:
        print("  Chart JavaScript already present, skipping")

    if content != original:
        backup(HTML_PATH)
        with open(HTML_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  Saved {HTML_PATH}")
    else:
        print(f"  No changes needed for {HTML_PATH}")


def patch_routes():
    if not os.path.exists(ROUTES_PATH):
        print(f"ERROR: Could not find {ROUTES_PATH}. Run this script from inside cipher_app/.")
        sys.exit(1)

    with open(ROUTES_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    if "history/all" in content:
        print(f"  /submissions/history/all already present in {ROUTES_PATH}, skipping")
        return

    addition = '''

def _period_sort_key(period: str):
    """Turns 'Q2 2026' into (2026, 2) so periods sort chronologically, not alphabetically."""
    try:
        q_part, year_part = period.split(" ")
        quarter = int(q_part.replace("Q", ""))
        year = int(year_part)
        return (year, quarter)
    except (ValueError, AttributeError):
        return (9999, 9)


@router.get("/submissions/history/all")
def get_all_submission_history(db: Session = Depends(get_db)):
    submissions = db.query(Submission).filter(Submission.submitted == True).all()

    history = []
    for s in submissions:
        manager = db.query(User).filter(User.id == s.manager_id).first()
        if not manager:
            continue
        net_change = s.total_gained - s.total_lost
        pct_return = (net_change / s.total_invested * 100) if s.total_invested else 0
        cumulative_value = s.total_invested + net_change

        history.append({
            "manager_id": s.manager_id,
            "manager_name": manager.name,
            "asset_class": manager.asset_class,
            "period": s.period,
            "total_invested": s.total_invested,
            "total_gained": s.total_gained,
            "total_lost": s.total_lost,
            "net_change": net_change,
            "pct_return": round(pct_return, 2),
            "cumulative_value": cumulative_value
        })

    history.sort(key=lambda h: _period_sort_key(h["period"]))

    return {"history": history}
'''
    backup(ROUTES_PATH)
    with open(ROUTES_PATH, "a", encoding="utf-8") as f:
        f.write(addition)
    print(f"  Appended new route to {ROUTES_PATH}")


if __name__ == "__main__":
    print("Patching routes.py...")
    patch_routes()
    print("\\nPatching templates/index.html...")
    patch_html()
    print("\\nDone! Next steps:")
    print("  1. Delete cipher.db if it exists (schema didn't change, but doesn't hurt to be safe)")
    print("  2. Restart your server: uvicorn main:app --reload")
    print("  3. Refresh your browser, log in, and check My History (manager) and Dashboard (director)")
    print("  4. If something looks wrong, your original files are saved as .bak — just rename them back")
