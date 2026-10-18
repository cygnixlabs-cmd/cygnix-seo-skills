#!/usr/bin/env python3
"""AI visibility quick score (lite): one page, 0-100, read-only.
Usage: python3 quick_score.py https://example.com/
Scores the server-rendered HTML the way most AI crawlers see it (no JavaScript):
AI crawler access 25, Organization/WebSite entity 15, other JSON-LD 10, title+meta 10,
one H1 + question headings 15, answer-first opening + text volume 15, llms.txt 5, freshness date 5."""
import sys, re, json, html as htmllib
from html.parser import HTMLParser
import urllib.request, urllib.parse, urllib.robotparser, ssl, re
UA = "Mozilla/5.0 (compatible; CygnixSEOSkills/1.0; +https://github.com/cygnixlabs-cmd/cygnix-seo-skills)"
AI_BOTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "CCBot"]
def fetch(url, timeout=15, method="GET", limit=2_000_000):
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ssl.create_default_context()) as r:
            body = r.read(limit).decode("utf-8", "replace") if method == "GET" else ""
            return r.status, body, r.headers.get("content-type", ""), r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, "", e.headers.get("content-type", "") if e.headers else "", url
    except Exception as e:
        return 0, str(e), "", url
def origin_of(url):
    if "://" not in url: url = "https://" + url
    p = urllib.parse.urlparse(url)
    return f"{p.scheme}://{p.netloc}", url
def robots_report(origin):
    st, body, _, _ = fetch(origin + "/robots.txt")
    if st != 200 or "<html" in body[:300].lower():
        return st, {b: "allowed (no robots.txt)" for b in AI_BOTS}, False
    rp = urllib.robotparser.RobotFileParser(); rp.parse(body.splitlines())
    res = {b: ("allowed" if rp.can_fetch(b, origin + "/") else "BLOCKED") for b in AI_BOTS}
    has_sitemap = bool(re.search(r"(?im)^\s*sitemap\s*:", body))
    return st, res, has_sitemap
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.title = ""; s.meta = {}; s.h = []; s.ld = []; s.text = []; s.ps = []
        s._t = None; s._buf = []; s._skip = 0
    def handle_starttag(s, t, at):
        at = dict(at)
        if t in ("script", "style", "noscript"):
            s._skip += 1
            if t == "script" and (at.get("type") or "").lower() == "application/ld+json": s._t = "ld"; s._buf = []
            return
        if t == "meta":
            k = (at.get("name") or at.get("property") or "").lower()
            if k: s.meta[k] = at.get("content") or ""
        if t in ("title", "h1", "h2", "h3", "p"): s._t = t; s._buf = []
        if t == "time" and at.get("datetime"): s.meta.setdefault("time", at["datetime"])
    def handle_endtag(s, t):
        if t in ("script", "style", "noscript"):
            s._skip = max(0, s._skip - 1)
            if s._t == "ld": s.ld.append("".join(s._buf)); s._t = None
            return
        if s._t == t:
            txt = " ".join("".join(s._buf).split())
            if t == "title": s.title = txt
            elif t == "p": s.ps.append(txt)
            else: s.h.append((t, txt))
            s._t = None
    def handle_data(s, d):
        if s._t == "ld": s._buf.append(d); return
        if s._skip: return
        if s._t: s._buf.append(d)
        s.text.append(d)
def types_of(o, acc):
    if isinstance(o, dict):
        t = o.get("@type")
        if isinstance(t, list): acc.update(map(str, t))
        elif t: acc.add(str(t))
        for v in o.values(): types_of(v, acc)
    elif isinstance(o, list):
        for v in o: types_of(v, acc)
    return acc
if len(sys.argv) < 2: sys.exit(__doc__)
origin, url = origin_of(sys.argv[1])
st, body, ctype, final = fetch(url)
if st != 200: sys.exit(f"Could not fetch {url}: HTTP {st} {body[:120]}")
p = P(); p.feed(body)
rows, fixes, score = [], [], 0
def add(name, pts, got, fix):
    global score
    score += got; rows.append((name, got, pts))
    if got < pts: fixes.append((pts - got, fix))
rst, bots, sm = robots_report(origin)
blocked = [b for b, v in bots.items() if v == "BLOCKED"]
add("AI crawler access (robots.txt)", 25, max(0, 25 - 5 * len(blocked)), f"Unblock {', '.join(blocked)} in robots.txt if you want AI answers to cite you")
types = set(); bad_ld = 0
for blk in p.ld:
    try: types_of(json.loads(blk), types)
    except Exception: bad_ld += 1
ent = types & {"Organization", "Corporation", "LocalBusiness", "Person", "WebSite", "OnlineStore"}
add("Organization / WebSite entity (JSON-LD)", 15, 15 if ent else 0, "Add Organization JSON-LD with name, url, logo and sameAs links to official profiles")
other = types - ent
add("Other structured data", 10, 10 if other and not bad_ld else 5 if other else 0, "Add JSON-LD that matches the page (Article, Product, FAQPage, BreadcrumbList…)" + (f"; fix {bad_ld} invalid JSON-LD block(s)" if bad_ld else ""))
md = p.meta.get("description", "")
tm = (5 if 15 <= len(p.title) <= 65 else 2 if p.title else 0) + (5 if 70 <= len(md) <= 170 else 2 if md else 0)
add("Title + meta description", 10, tm, "; ".join(x for x in [f"Title should be 15-65 chars (now {len(p.title)})" if not 15 <= len(p.title) <= 65 else "", f"Meta description should be 70-170 chars (now {len(md)})" if not 70 <= len(md) <= 170 else ""] if x))
h1 = [h for t, h in p.h if t == "h1"]; qh = [h for t, h in p.h if t in ("h2", "h3") and (h.endswith("?") or re.match(r"(?i)(how|what|why|when|which|who|can|does|is|are)\b", h))]
add("One H1 + question-style headings", 15, (7 if len(h1) == 1 else 0) + min(8, 4 * len(qh)), "Use exactly one H1 and phrase 2+ H2/H3s as the questions buyers ask")
words = len(" ".join(p.text).split())
first = next((x for x in p.ps if len(x.split()) >= 12), "")
fw = len(first.split())
af = 8 if 15 <= fw <= 80 else 3 if first else 0
add("Answer-first opening + server-rendered text", 15, af + (7 if words >= 300 else 3 if words >= 120 else 0), "; ".join(x for x in [f"Open with a 15-80 word direct answer (first real paragraph is {fw} words)" if af < 8 else "", f"Server HTML has only {words} words; render 300+ words without JavaScript" if words < 300 else ""] if x))
lst, lb, lct, _ = fetch(origin + "/llms.txt", limit=100_000)
has_llms = lst == 200 and lb.strip() and "<html" not in lb[:300].lower()
add("/llms.txt", 5, 5 if has_llms else 0, "Publish /llms.txt listing your 10-20 key pages (cheap; coding agents read it)")
date = p.meta.get("article:modified_time") or p.meta.get("article:published_time") or p.meta.get("time") or ("dateModified" in body and "dateModified")
add("Freshness date signal", 5, 5 if date else 0, "Show a visible Updated date and add dateModified in JSON-LD")
band = "STRONG" if score >= 80 else "GOOD" if score >= 65 else "FAIR" if score >= 50 else "POOR" if score >= 35 else "CRITICAL"
print(f"# AI visibility quick score: {final}\n\n**{score}/100 ({band})**, one page, server HTML only.\n")
print("| check | points |\n|---|---|")
for n, g, m in rows: print(f"| {n} | {g}/{m} |")
print("\n## Top fixes")
for i, (_, f) in enumerate(sorted(fixes, key=lambda x: -x[0])[:5], 1): print(f"{i}. {f}")
print(f"\nAI crawlers: " + ", ".join(f"{b} {'blocked' if v == 'BLOCKED' else 'ok'}" for b, v in bots.items()))
print(f"JSON-LD types: {', '.join(sorted(types)) or 'none'}")
print("\nThis measures readiness (can AI crawlers fetch, parse and trust this page), not rankings or citations.")
