#!/usr/bin/env python3
"""Keyword cannibalization finder (lite) for a Google Search Console export.
Usage: python3 cannibalization.py gsc_query_page.csv [--min-impressions 10] [--min-share 10] [--exclude brand1,brand2]
Input: CSV with query + page columns (clicks, impressions, position optional). Column names are auto-detected.
Output: Markdown table of queries where 2+ of your pages compete, worst first. No network."""
import csv, sys, argparse
def num(x):
    try: return float(str(x).replace(",", "").replace("%", "").strip() or 0)
    except ValueError: return 0.0
def find(cols, *names):
    for c in cols:
        if c.lower().strip() in names: return c
    for c in cols:
        if any(n in c.lower() for n in names): return c
    return None
ap = argparse.ArgumentParser(); ap.add_argument("path")
ap.add_argument("--min-impressions", type=float, default=10); ap.add_argument("--min-share", type=float, default=10)
ap.add_argument("--exclude", default="")
a = ap.parse_args()
rows = list(csv.DictReader(open(a.path, encoding="utf-8-sig")))
if not rows: sys.exit("Empty CSV")
cols = list(rows[0].keys())
qc, pc = find(cols, "query", "keyword", "top queries"), find(cols, "page", "url", "landing page", "top pages")
cc, ic, poc = find(cols, "clicks"), find(cols, "impressions"), find(cols, "position", "avg. position")
if not qc or not pc: sys.exit(f"Need query and page columns; found {cols}. Export with both dimensions (GSC API, Looker Studio or Search Analytics for Sheets).")
excl = [e.strip().lower() for e in a.exclude.split(",") if e.strip()]
by = {}
for r in rows:
    q = r[qc].strip().lower()
    if not q or any(e in q for e in excl): continue
    by.setdefault(q, []).append({"page": r[pc].strip(), "clicks": num(r.get(cc, 0)) if cc else 0,
        "impr": num(r.get(ic, 0)) if ic else 0, "pos": num(r.get(poc, 0)) if poc else None})
issues = []
for q, pages in by.items():
    tot = sum(p["impr"] for p in pages) or 1
    comp = [p for p in pages if p["impr"] >= a.min_impressions and 100 * p["impr"] / tot >= a.min_share]
    if len(comp) < 2: continue
    comp.sort(key=lambda p: (-p["clicks"], -p["impr"]))
    prim, sec = comp[0], comp[1]
    share2 = 100 * sec["impr"] / tot
    gap = abs((sec["pos"] or 0) - (prim["pos"] or 0)) if prim["pos"] and sec["pos"] else None
    sev = "HIGH" if share2 >= 30 and (gap is None or gap <= 10) else "MEDIUM" if share2 >= 20 else "LOW"
    issues.append((sev, q, prim, comp[1:], sum(p["clicks"] for p in comp[1:]), share2, gap))
order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
issues.sort(key=lambda i: (order[i[0]], -i[4], -i[5]))
print("| severity | query | primary page (most clicks) | competing pages | clicks on competitors | #2 impression share | position gap |")
print("|---|---|---|---|---|---|---|")
for sev, q, prim, others, ck, sh, gap in issues:
    print(f"| {sev} | {q} | {prim['page']} | {'<br>'.join(o['page'] for o in others)} | {int(ck)} | {sh:.0f}% | {'' if gap is None else f'{gap:.1f}'} |")
print(f"\n{len(by)} queries checked, {len(issues)} cannibalized ({sum(1 for i in issues if i[0]=='HIGH')} HIGH). Thresholds: >= {a.min_impressions:g} impressions and >= {a.min_share:g}% share per page.")
