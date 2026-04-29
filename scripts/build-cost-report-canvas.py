#!/usr/bin/env python3
"""
build-cost-report-canvas.py
Reads usage.jsonl + model-pricing.json and generates ~/.openclaw/canvas/cost-report.html
with data embedded inline as JS variables.

Run this script any time usage.jsonl is updated.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone

WORKSPACE = Path(__file__).resolve().parent.parent
USAGE_FILE = WORKSPACE / "logs" / "usage.jsonl"
PRICING_FILE = Path(__file__).resolve().parent / "model-pricing.json"
CANVAS_DIR = Path.home() / ".openclaw" / "canvas"
OUT_FILE = CANVAS_DIR / "cost-report.html"

DAILY_BUDGET_USD = 50.0


def load_usage():
    records = []
    if not USAGE_FILE.exists():
        print(f"Warning: {USAGE_FILE} not found", file=sys.stderr)
        return records
    with open(USAGE_FILE) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Warning: skipping bad line: {e}", file=sys.stderr)
    return records


def load_pricing():
    if not PRICING_FILE.exists():
        print(f"Warning: {PRICING_FILE} not found", file=sys.stderr)
        return {}
    with open(PRICING_FILE) as f:
        return json.load(f)


def build_html(usage_data, pricing):
    usage_json = json.dumps(usage_data, indent=2)
    pricing_json = json.dumps(pricing, indent=2)
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    html = f"""<!doctype html>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Cost Report — OpenClaw Canvas</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; }}
  html, body {{
    height: 100%; margin: 0;
    background: #000; color: #fff;
    font: 14px/1.5 -apple-system, BlinkMacSystemFont, system-ui, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
  }}
  a {{ color: #24e08a; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}

  .page {{ max-width: 1100px; margin: 0 auto; padding: 24px 20px 48px; }}

  /* Header */
  .header {{ display: flex; align-items: baseline; justify-content: space-between; flex-wrap: wrap; gap: 10px; margin-bottom: 24px; }}
  .header h1 {{ margin: 0; font-size: 22px; letter-spacing: 0.2px; }}
  .header .back {{ font-size: 13px; opacity: 0.65; }}
  .header .back:hover {{ opacity: 1; }}
  .generated {{ font-size: 11px; opacity: 0.4; }}

  /* Period toggle */
  .period-bar {{ display: flex; gap: 8px; margin-bottom: 20px; }}
  .period-btn {{
    appearance: none; border: 1px solid rgba(255,255,255,0.14);
    background: rgba(255,255,255,0.08); color: rgba(255,255,255,0.7);
    padding: 7px 16px; border-radius: 8px; font-size: 13px; font-weight: 600;
    cursor: pointer; transition: all 0.15s;
  }}
  .period-btn:hover {{ background: rgba(255,255,255,0.13); color: #fff; }}
  .period-btn.active {{
    background: rgba(36,224,138,0.15); border-color: rgba(36,224,138,0.5);
    color: #24e08a;
  }}

  /* Filters */
  .filter-bar {{ display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 20px; align-items: center; }}
  .filter-bar label {{ font-size: 12px; opacity: 0.55; }}
  .filter-bar select {{
    appearance: none; background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.14); color: #fff;
    padding: 6px 28px 6px 10px; border-radius: 8px; font-size: 13px;
    cursor: pointer;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='rgba(255,255,255,0.4)'/%3E%3C/svg%3E");
    background-repeat: no-repeat; background-position: right 10px center;
  }}
  .filter-bar select:focus {{ outline: none; border-color: rgba(36,224,138,0.5); }}

  /* Card */
  .card {{
    background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.10);
    border-radius: 12px; padding: 16px 18px; margin-bottom: 16px;
  }}
  .card-title {{ font-size: 11px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; opacity: 0.45; margin-bottom: 12px; }}

  /* Summary row */
  .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; margin-bottom: 16px; }}
  .stat {{
    background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.10);
    border-radius: 12px; padding: 14px 16px;
  }}
  .stat-label {{ font-size: 11px; opacity: 0.45; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.06em; }}
  .stat-value {{ font: 700 22px/1.2 ui-monospace, Menlo, monospace; }}
  .stat-value.green {{ color: #24e08a; }}
  .stat-value.red {{ color: #ff5c5c; }}
  .stat-sub {{ font-size: 11px; opacity: 0.45; margin-top: 2px; }}

  /* Tables */
  .table-wrap {{ overflow-x: auto; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th {{
    text-align: left; font-size: 11px; font-weight: 600; letter-spacing: 0.06em;
    text-transform: uppercase; opacity: 0.45; padding: 0 8px 8px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
  }}
  td {{ padding: 9px 8px; border-bottom: 1px solid rgba(255,255,255,0.05); }}
  tr:last-child td {{ border-bottom: none; }}
  tr:hover td {{ background: rgba(255,255,255,0.03); }}
  .num {{ font-family: ui-monospace, Menlo, monospace; text-align: right; }}
  th.num {{ text-align: right; }}

  /* Status dot */
  .dot {{
    display: inline-block; width: 7px; height: 7px; border-radius: 50%;
    margin-right: 5px; vertical-align: middle;
  }}
  .dot.ok {{ background: #24e08a; }}
  .dot.err {{ background: #ff5c5c; }}

  /* No data */
  .empty {{ opacity: 0.35; font-size: 13px; padding: 12px 0; }}

  /* Budget bar */
  .budget-bar-wrap {{ margin-top: 8px; }}
  .budget-bar-bg {{ background: rgba(255,255,255,0.08); border-radius: 4px; height: 6px; overflow: hidden; }}
  .budget-bar-fill {{ height: 6px; border-radius: 4px; transition: width 0.3s; }}
</style>

<div class="page">
  <div class="header">
    <div>
      <h1>💸 Cost Report</h1>
      <div class="generated">Generated {generated_at}</div>
    </div>
    <a class="back" href="./">← OpenClaw Canvas</a>
  </div>

  <div class="period-bar">
    <button class="period-btn active" data-period="daily">Daily</button>
    <button class="period-btn" data-period="weekly">Weekly</button>
    <button class="period-btn" data-period="monthly">Monthly</button>
  </div>

  <div class="filter-bar">
    <label>Model</label>
    <select id="filter-model"><option value="">All</option></select>
    <label>Task type</label>
    <select id="filter-task"><option value="">All</option></select>
  </div>

  <div class="summary" id="summary-row"></div>

  <div class="card">
    <div class="card-title">By Model</div>
    <div class="table-wrap"><table id="model-table">
      <thead><tr>
        <th>Model</th><th>Provider</th>
        <th class="num">Runs</th><th class="num">Input tokens</th>
        <th class="num">Output tokens</th><th class="num">Est. cost</th>
      </tr></thead>
      <tbody></tbody>
    </table></div>
  </div>

  <div class="card">
    <div class="card-title">By Task Type</div>
    <div class="table-wrap"><table id="task-table">
      <thead><tr>
        <th>Task type</th>
        <th class="num">Runs</th><th class="num">Total tokens</th><th class="num">Est. cost</th>
      </tr></thead>
      <tbody></tbody>
    </table></div>
  </div>

  <div class="card">
    <div class="card-title">Recent Runs (last 20)</div>
    <div class="table-wrap"><table id="runs-table">
      <thead><tr>
        <th>Date</th><th>Job name</th><th>Model</th>
        <th class="num">Tokens</th><th class="num">Cost</th><th>Status</th>
      </tr></thead>
      <tbody></tbody>
    </table></div>
  </div>
</div>

<script>
const USAGE_DATA = {usage_json};
const PRICING = {pricing_json};
const DAILY_BUDGET = {DAILY_BUDGET_USD};

// ---- helpers ----
const fmt = (n) => n == null ? '—' : n.toLocaleString();
const fmtCost = (n) => n == null ? '—' : '$' + n.toFixed(4);
const fmtCostShort = (n) => n == null ? '—' : '$' + n.toFixed(2);

function getDateRange(period) {{
  const now = new Date();
  const todayStr = now.toISOString().slice(0, 10);

  if (period === 'daily') {{
    return {{ start: todayStr, end: todayStr }};
  }}
  if (period === 'weekly') {{
    const d = new Date(now);
    d.setDate(d.getDate() - 6);
    return {{ start: d.toISOString().slice(0, 10), end: todayStr }};
  }}
  if (period === 'monthly') {{
    const d = new Date(now);
    d.setDate(d.getDate() - 29);
    return {{ start: d.toISOString().slice(0, 10), end: todayStr }};
  }}
  return {{ start: todayStr, end: todayStr }};
}}

function filterData(period, modelFilter, taskFilter) {{
  const {{ start, end }} = getDateRange(period);
  return USAGE_DATA.filter(r => {{
    if (r.date < start || r.date > end) return false;
    if (modelFilter && r.model !== modelFilter) return false;
    if (taskFilter && r.task_type !== taskFilter) return false;
    return true;
  }});
}}

// ---- populate filter dropdowns ----
function populateFilters() {{
  const models = [...new Set(USAGE_DATA.map(r => r.model))].sort();
  const tasks  = [...new Set(USAGE_DATA.map(r => r.task_type).filter(Boolean))].sort();
  const mSel = document.getElementById('filter-model');
  const tSel = document.getElementById('filter-task');
  models.forEach(m => {{ const o = document.createElement('option'); o.value = m; o.textContent = m; mSel.appendChild(o); }});
  tasks.forEach(t  => {{ const o = document.createElement('option'); o.value = t; o.textContent = t; tSel.appendChild(o); }});
}}

// ---- render summary ----
function renderSummary(data, period) {{
  const totalRuns  = data.length;
  const totalTok   = data.reduce((s, r) => s + (r.total_tokens || 0), 0);
  const totalCost  = data.reduce((s, r) => s + (r.estimated_cost_usd || 0), 0);
  const remaining  = DAILY_BUDGET - totalCost;
  const pct        = Math.min(100, (totalCost / DAILY_BUDGET) * 100);

  let html = `
    <div class="stat"><div class="stat-label">Total runs</div><div class="stat-value">${{fmt(totalRuns)}}</div></div>
    <div class="stat"><div class="stat-label">Total tokens</div><div class="stat-value">${{fmt(totalTok)}}</div></div>
    <div class="stat"><div class="stat-label">Est. cost</div><div class="stat-value ${{totalCost > DAILY_BUDGET * 0.8 ? 'red' : 'green'}}">${{fmtCostShort(totalCost)}}</div></div>
  `;
  if (period === 'daily') {{
    const barColor = pct > 80 ? '#ff5c5c' : pct > 50 ? '#f5a623' : '#24e08a';
    html += `
      <div class="stat">
        <div class="stat-label">Remaining (daily ${{fmtCostShort(DAILY_BUDGET)}})</div>
        <div class="stat-value ${{remaining < 0 ? 'red' : 'green'}}">${{fmtCostShort(remaining)}}</div>
        <div class="budget-bar-wrap">
          <div class="budget-bar-bg"><div class="budget-bar-fill" style="width:${{pct}}%;background:${{barColor}}"></div></div>
        </div>
        <div class="stat-sub">${{pct.toFixed(1)}}% of daily budget used</div>
      </div>
    `;
  }}
  document.getElementById('summary-row').innerHTML = html;
}}

// ---- render by model ----
function renderModelTable(data) {{
  const map = {{}};
  data.forEach(r => {{
    if (!map[r.model]) map[r.model] = {{ provider: r.provider, runs: 0, input: 0, output: 0, cost: 0 }};
    const m = map[r.model];
    m.runs++;
    m.input  += (r.input_tokens  || 0);
    m.output += (r.output_tokens || 0);
    m.cost   += (r.estimated_cost_usd || 0);
  }});
  const rows = Object.entries(map).sort((a,b) => b[1].cost - a[1].cost);
  const tbody = document.querySelector('#model-table tbody');
  if (!rows.length) {{ tbody.innerHTML = '<tr><td colspan="6" class="empty">No data</td></tr>'; return; }}
  tbody.innerHTML = rows.map(([model, m]) => `
    <tr>
      <td>${{model}}</td>
      <td style="opacity:0.55">${{m.provider}}</td>
      <td class="num">${{fmt(m.runs)}}</td>
      <td class="num">${{fmt(m.input)}}</td>
      <td class="num">${{fmt(m.output)}}</td>
      <td class="num">${{fmtCost(m.cost)}}</td>
    </tr>
  `).join('');
}}

// ---- render by task type ----
function renderTaskTable(data) {{
  const map = {{}};
  data.forEach(r => {{
    const key = r.task_type || 'unknown';
    if (!map[key]) map[key] = {{ runs: 0, tokens: 0, cost: 0 }};
    map[key].runs++;
    map[key].tokens += (r.total_tokens || 0);
    map[key].cost   += (r.estimated_cost_usd || 0);
  }});
  const rows = Object.entries(map).sort((a,b) => b[1].cost - a[1].cost);
  const tbody = document.querySelector('#task-table tbody');
  if (!rows.length) {{ tbody.innerHTML = '<tr><td colspan="4" class="empty">No data</td></tr>'; return; }}
  tbody.innerHTML = rows.map(([task, m]) => `
    <tr>
      <td>${{task}}</td>
      <td class="num">${{fmt(m.runs)}}</td>
      <td class="num">${{fmt(m.tokens)}}</td>
      <td class="num">${{fmtCost(m.cost)}}</td>
    </tr>
  `).join('');
}}

// ---- render recent runs ----
function renderRunsTable(data) {{
  const sorted = [...data].sort((a,b) => (b.ts||0) - (a.ts||0)).slice(0, 20);
  const tbody = document.querySelector('#runs-table tbody');
  if (!sorted.length) {{ tbody.innerHTML = '<tr><td colspan="6" class="empty">No data</td></tr>'; return; }}
  tbody.innerHTML = sorted.map(r => {{
    const isOk = r.status === 'ok';
    return `<tr>
      <td style="white-space:nowrap;opacity:0.65">${{r.date}}</td>
      <td>${{r.jobName || r.jobId || '—'}}</td>
      <td style="opacity:0.65;white-space:nowrap">${{r.model || '—'}}</td>
      <td class="num">${{fmt(r.total_tokens)}}</td>
      <td class="num">${{fmtCost(r.estimated_cost_usd)}}</td>
      <td><span class="dot ${{isOk ? 'ok' : 'err'}}"></span>${{r.status || '—'}}</td>
    </tr>`;
  }}).join('');
}}

// ---- main render ----
let currentPeriod = 'daily';

function render() {{
  const modelFilter = document.getElementById('filter-model').value;
  const taskFilter  = document.getElementById('filter-task').value;
  const data = filterData(currentPeriod, modelFilter, taskFilter);
  renderSummary(data, currentPeriod);
  renderModelTable(data);
  renderTaskTable(data);
  renderRunsTable(data);
}}

// ---- event wiring ----
document.querySelectorAll('.period-btn').forEach(btn => {{
  btn.addEventListener('click', () => {{
    document.querySelectorAll('.period-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentPeriod = btn.dataset.period;
    render();
  }});
}});
document.getElementById('filter-model').addEventListener('change', render);
document.getElementById('filter-task').addEventListener('change', render);

// ---- init ----
populateFilters();
render();
</script>
"""
    return html


def main():
    CANVAS_DIR.mkdir(parents=True, exist_ok=True)
    usage_data = load_usage()
    pricing = load_pricing()

    print(f"Loaded {len(usage_data)} usage records")
    print(f"Loaded {len(pricing)} pricing entries")

    html = build_html(usage_data, pricing)
    OUT_FILE.write_text(html, encoding="utf-8")
    print(f"Written: {OUT_FILE}")
    print(f"Records embedded: {len(usage_data)}")


if __name__ == "__main__":
    main()
