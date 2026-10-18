#!/usr/bin/env python3
"""Content decay finder (lite): compare two Google Search Console "Pages" exports.
Usage: python3 decay.py previous.csv current.csv [--min-prev-clicks 10] [--top 30]
Input: two CSVs with page + clicks (impressions, position optional). Column names auto-detected.
Output: Markdown table of pages ranked by clicks lost, labelled LOST / DECLINING / STRIKING_DISTANCE / GROWING / STABLE."""
import csv, argparse
def num(x):
    try: return float(str(x).replace(",", "").replace("%", "").strip() or 0)
    except ValueError: return 0.0
def load(path):
    rows = list(csv.DictReader(open(path, encoding="utf-8-sig")))
    cols = list(rows[0].keys()) if rows else []
    def f(*n): return next((c for c in cols if any(x == c.lower().strip() or x in c.lower() for x in n)), None)
    pc, cc, ic, poc = f("page", "url", "top pages", "landing page"), f("clicks"), f("impressions"), f("position")
    if not pc or not cc: raise SystemExit(f"{path}: need page and clicks columns, found {cols}")
    return {r[pc].strip(): (num(r[cc]), num(r.get(ic, 0)) if ic else 0, num(r.get(poc, 0)) if poc else None) for r in rows if r[pc].strip()}
ap = argparse.ArgumentParser(); ap.add_argument("previous"); ap.add_argument("current")
ap.add_argument("--min-prev-clicks", type=float, default=10); ap.add_argument("--top", type=int, default=30)
a = ap.parse_args()
prev, cur = load(a.previous), load(a.current)
out = []
for page in set(prev) | set(cur):
    c0, i0, p0 = prev.get(page, (0, 0, None)); c1, i1, p1 = cur.get(page, (0, 0, None))
    lost = c0 - c1; pct = (100 * (c1 - c0) / c0) if c0 else None
    if c0 >= a.min_prev_clicks and c1 == 0: lab = "LOST"
    elif c0 >= a.min_prev_clicks and pct is not None and pct <= -30: lab = "DECLINING"
    elif p1 and 8 <= p1 <= 20 and i1 >= 100: lab = "STRIKING_DISTANCE"
    elif c0 and pct is not None and pct >= 20: lab = "GROWING"
    else: lab = "STABLE"
    out.append((page, lab, c0, c1, lost, pct, p0, p1))
rank = {"LOST": 0, "DECLINING": 0, "STRIKING_DISTANCE": 1, "GROWING": 2, "STABLE": 3}
out.sort(key=lambda r: (rank[r[1]], -r[4]))
print("| page | status | clicks before | clicks now | click change | % change | position before → now |\n|---|---|---|---|---|---|---|")
for page, lab, c0, c1, lost, pct, p0, p1 in [r for r in out if r[1] != "STABLE"][: a.top]:
    pos = f"{p0:.1f} → {p1:.1f}" if p0 and p1 else ""
    print(f"| {page} | {lab} | {int(c0)} | {int(c1)} | {int(-lost):+d} | {'' if pct is None else f'{pct:+.0f}%'} | {pos} |")
tot = sum(r[4] for r in out if r[1] in ("LOST", "DECLINING"))
counts = {}
for r in out: counts[r[1]] = counts.get(r[1], 0) + 1
print(f"\n{len(out)} pages compared. Clicks lost on declining pages: {int(tot)}. " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
