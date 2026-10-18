#!/usr/bin/env python3
"""Keyword clustering (lite). Groups keywords by shared core terms, labels intent, picks a pillar.
Usage: python3 cluster.py keywords.txt [--threshold 0.5]
Input: one keyword per line, or a CSV export with keyword/query and optional volume columns.
Output: Markdown table of clusters, biggest first. No network, no API keys."""
import sys, csv, io, re, argparse
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
STOP = set("a an the for to of in on and or with without by from at is are be how what why when where who which best top vs versus near me my your our free cheap online 2024 2025 2026".split())
def stem(w):
    for suf in ("ies", "es", "s", "ing", "ed"):
        if len(w) > 4 and w.endswith(suf):
            return w[: -len(suf)] + ("y" if suf == "ies" else "")
    return w
def core(k):
    return frozenset(stem(w) for w in re.findall(r"[a-z0-9]+", k.lower()) if w not in STOP) or frozenset(re.findall(r"[a-z0-9]+", k.lower()))
def jac(a, b):
    return len(a & b) / len(a | b) if a | b else 0
def read(path):
    text = sys.stdin.read() if path == "-" else open(path, encoding="utf-8-sig").read()
    lines = [l for l in text.splitlines() if l.strip()]
    if lines and "," in lines[0] and any(h in lines[0].lower() for h in ("keyword", "query")):
        rows = list(csv.DictReader(io.StringIO(text)))
        cols = {c.lower().strip(): c for c in rows[0]}
        kc = next(cols[c] for c in cols if c in ("keyword", "query", "keywords", "top queries"))
        vc = next((cols[c] for c in cols if "volume" in c or c in ("impressions", "search volume")), None)
        out = []
        for r in rows:
            k = r[kc].strip()
            if not k: continue
            try: v = float(str(r.get(vc, "") or 0).replace(",", "")) if vc else None
            except ValueError: v = None
            out.append((k, v))
        return out
    return [(l.strip(), None) for l in lines]
if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("path"); ap.add_argument("--threshold", type=float, default=0.5)
    a = ap.parse_args()
    seen, kws = set(), []
    for k, v in read(a.path):
        if k.lower() not in seen: seen.add(k.lower()); kws.append((k, v))
    kws.sort(key=lambda x: (-(x[1] or 0), len(x[0])))
    clusters = []  # each: {"terms": set, "items": [(k,v,core)]}
    for k, v in kws:
        c = core(k); best, score = None, 0
        for cl in clusters:
            pc = cl["items"][0][2]
            if len(c) == 1 or len(pc) == 1:
                s = 1.0 if c == pc else 0.0   # single-term keywords only join an identical core
            else:
                s = jac(c, pc)
            if s > score: best, score = cl, s
        if best is not None and score >= a.threshold:
            best["items"].append((k, v, c))
        else:
            clusters.append({"items": [(k, v, c)]})
    def vol(cl): return sum(i[1] or 0 for i in cl["items"])
    clusters.sort(key=lambda cl: (-vol(cl), -len(cl["items"])))
    has_vol = any(v for _, v in kws)
    print("| # | pillar keyword | intent | page type | keywords | " + ("total volume | " if has_vol else "") + "members |")
    print("|---|---|---|---|---|" + ("---|" if has_vol else "") + "---|")
    for n, cl in enumerate(clusters, 1):
        pillar = cl["items"][0][0]
        intents = [classify(i[0])["intent"] for i in cl["items"]]
        intent = max(set(intents), key=intents.count)
        members = "; ".join(i[0] for i in cl["items"][1:8]) + (" …" if len(cl["items"]) > 8 else "")
        print(f"| {n} | {pillar} | {intent} | {PAGE_TYPE[intent]} | {len(cl['items'])} | " + (f"{int(vol(cl))} | " if has_vol else "") + f"{members} |")
    print(f"\n{len(kws)} keywords -> {len(clusters)} clusters (threshold {a.threshold}). Lexical clustering: check top clusters against the live SERP before merging pages.")
