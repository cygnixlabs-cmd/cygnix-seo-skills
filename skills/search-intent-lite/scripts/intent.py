#!/usr/bin/env python3
"""Search intent classifier (lite). Rule-based, no network.
Usage: python3 intent.py keywords.txt [--brands acme,acmecorp] [--locations "new york,london"]
       cat keywords.txt | python3 intent.py -
Input: one keyword per line, or a CSV with a keyword/query column. Output: Markdown table."""
import sys, csv, io, argparse
INTENT_RULES = [
    ("navigational", ["login", "log in", "sign in", "signin", "account", "dashboard", "official site", "customer service", "support", "contact", "app download"]),
    ("transactional", ["buy", "price", "prices", "pricing", "cost", "cheap", "discount", "coupon", "deal", "order", "for sale", "subscribe", "free trial", "quote", "hire", "book", "download"]),
    ("commercial", ["best", "top", "vs", "versus", "review", "reviews", "compare", "comparison", "alternative", "alternatives", "recommended", "which", "software", "tool", "tools", "app", "apps", "platform", "free", "services", "agency", "companies"]),
    ("informational", ["how", "what", "why", "when", "where", "who", "guide", "tutorial", "examples", "ideas", "tips", "meaning", "definition", "learn", "is", "does", "can"]),
]
LOCAL = ["near me", "nearby", "open now", "in my area", "local"]
PAGE_TYPE = {
    "navigational": "brand, login or support page",
    "transactional": "product, pricing or service page",
    "commercial": "comparison, 'best X' list or review page",
    "informational": "guide, how-to or FAQ article",
    "unclear": "check the live SERP before choosing",
}
def _has(q, term):
    q = f" {q} "
    return f" {term} " in q
def classify(keyword, brands=(), locations=()):
    q = " ".join(keyword.lower().replace("?", " ").split())
    hits = []
    for b in brands:
        if b and _has(q, b.lower()):
            hits.append("navigational")
            break
    for intent, terms in INTENT_RULES:
        if any(_has(q, t) for t in terms):
            hits.append(intent)
    local = any(_has(q, t) for t in LOCAL) or any(l and _has(q, l.lower()) for l in locations)
    order = ["transactional", "commercial", "navigational", "informational"]
    uniq = [i for i in order if i in hits]
    if not uniq:
        return {"intent": "unclear", "confidence": "low", "local": local, "pageType": "local landing page" if local else PAGE_TYPE["unclear"]}
    intent = uniq[0]
    conf = "high" if len(uniq) == 1 else "mixed"
    pt = "local landing / service-area page" if local and intent in ("transactional", "commercial", "unclear") else PAGE_TYPE[intent]
    return {"intent": intent, "confidence": conf, "local": local, "pageType": pt}
def read_keywords(path):
    text = sys.stdin.read() if path == "-" else open(path, encoding="utf-8-sig").read()
    lines = [l for l in text.splitlines() if l.strip()]
    if lines and "," in lines[0] and any(h in lines[0].lower() for h in ("keyword", "query")):
        rows = list(csv.DictReader(io.StringIO(text)))
        col = next(c for c in rows[0] if c.lower().strip() in ("keyword", "query", "keywords", "top queries"))
        return [r[col].strip() for r in rows if r.get(col, "").strip()]
    return [l.strip() for l in lines]
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("path"); ap.add_argument("--brands", default=""); ap.add_argument("--locations", default="")
    a = ap.parse_args()
    brands = [b.strip() for b in a.brands.split(",") if b.strip()]
    locs = [l.strip() for l in a.locations.split(",") if l.strip()]
    seen, rows = set(), []
    for k in read_keywords(a.path):
        if k.lower() in seen: continue
        seen.add(k.lower()); rows.append((k, classify(k, brands, locs)))
    print("| keyword | intent | confidence | local | page type |\n|---|---|---|---|---|")
    for k, r in rows:
        print(f"| {k} | {r['intent']} | {r['confidence']} | {'yes' if r['local'] else ''} | {r['pageType']} |")
    counts = {}
    for _, r in rows: counts[r["intent"]] = counts.get(r["intent"], 0) + 1
    print("\nTotals: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items(), key=lambda x: -x[1])))
