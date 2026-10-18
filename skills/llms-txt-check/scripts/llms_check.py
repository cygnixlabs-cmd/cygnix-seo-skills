#!/usr/bin/env python3
"""llms.txt + AI crawler access check (read-only).
Usage: python3 llms_check.py example.com [--max-links 20]
Checks: /llms.txt exists and is Markdown (not an HTML soft-404), follows the llmstxt.org shape
(H1 title, > summary, H2 sections with link lists), its links resolve, /llms-full.txt, and robots.txt rules for 8 AI crawlers.
Makes at most ~25 polite requests. Prints a Markdown report."""
import sys, argparse, re, time
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
ap = argparse.ArgumentParser(); ap.add_argument("site"); ap.add_argument("--max-links", type=int, default=20)
a = ap.parse_args()
origin, _ = origin_of(a.site)
print(f"# llms.txt + AI crawler check: {origin}\n")
st, body, ctype, final = fetch(origin + "/llms.txt")
is_html = "<html" in body[:500].lower() or "<!doctype" in body[:500].lower() or "text/html" in ctype
ok = st == 200 and body.strip() and not is_html
print("## /llms.txt")
if not ok:
    why = f"HTTP {st}" if st != 200 else "returns an HTML page (soft-404), not Markdown"
    print(f"- **Missing** ({why}).")
else:
    lines = body.splitlines()
    h1 = [l for l in lines if l.startswith("# ")]
    quote = [l for l in lines if l.startswith("> ")]
    h2 = [l for l in lines if l.startswith("## ")]
    links = re.findall(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", body)
    checks = [("Exactly one H1 title", len(h1) == 1), ("A `>` summary line", bool(quote)),
              ("At least one `##` section", bool(h2)), ("Contains Markdown links", bool(links)),
              ("Under ~50 KB (fits an agent context)", len(body.encode()) < 50_000)]
    print(f"- Found: {len(body.encode())} bytes, {len(h2)} sections, {len(links)} links. Served as `{ctype or 'unknown'}`.")
    for name, passed in checks: print(f"- {'PASS' if passed else 'FAIL'}: {name}")
    bad = []
    for _, url in links[: a.max_links]:
        s, *_ = fetch(url, timeout=10, method="HEAD")
        if s in (405, 403, 0): s, *_ = fetch(url, timeout=10, limit=2048)
        if not (200 <= s < 400): bad.append((url, s))
        time.sleep(0.3)
    print(f"- Links checked: {min(len(links), a.max_links)}; broken: {len(bad)}")
    for u, s in bad: print(f"  - {u} → HTTP {s}")
fst, fbody, fct, _ = fetch(origin + "/llms-full.txt", limit=200_000)
print(f"- /llms-full.txt: {'present' if fst == 200 and '<html' not in fbody[:300].lower() else 'not found (optional)'}")
print("\n## AI crawler access (robots.txt, site root)")
rst, res, sm = robots_report(origin)
print(f"- robots.txt: {'found' if rst == 200 else f'HTTP {rst}'}; Sitemap line: {'yes' if sm else 'no'}")
print("| crawler | access to / |\n|---|---|")
for b, v in res.items(): print(f"| {b} | {v} |")
blocked = [b for b, v in res.items() if v == "BLOCKED"]
print("\n## Verdict")
if not ok: print("- Publish `/llms.txt`: an H1 with your site name, a `>` one-line summary, then `##` sections listing your 10-20 most useful pages as `- [Title](url): one-line description`.")
if blocked: print(f"- robots.txt blocks {', '.join(blocked)} at the root. If you want to appear in those AI answers, add an explicit `User-agent: <bot>` / `Allow: /` group.")
if ok and not blocked: print("- llms.txt is present and no major AI crawler is blocked at the root.")
print("- Note: AI search crawlers rarely fetch llms.txt today; coding agents do. Crawler access in robots.txt matters more for AI search.")
