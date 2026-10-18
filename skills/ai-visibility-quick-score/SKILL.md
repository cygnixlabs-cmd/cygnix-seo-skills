---
name: ai-visibility-quick-score
description: Give one web page a quick 0-100 AI search visibility (GEO/AEO readiness) score from its server-rendered HTML - AI crawler access, Organization/WebSite JSON-LD, structured data, title/meta, question headings, answer-first opening, llms.txt and freshness - with the top 5 fixes. Use when the user asks if a page is ready for ChatGPT, Perplexity, Google AI Overviews or other AI search, or wants a GEO/AEO score.
license: MIT
---

# AI visibility quick score (one page)

Scores a single URL the way most AI crawlers see it: raw HTML, no JavaScript. It returns a 0–100 score, a band and the five fixes worth the most points.

## When to use
- "Is my homepage ready for AI search?", "GEO score for this URL", "why doesn't ChatGPT mention us?" (as a first check).

## How to run
```bash
python3 scripts/quick_score.py https://example.com/
```
Needs outbound HTTPS; makes 3 requests (the page, robots.txt, llms.txt).

## Scoring (100 points)
| check | points |
|---|---|
| AI crawlers allowed in robots.txt (−5 per blocked bot) | 25 |
| Organization / WebSite / Person entity in JSON-LD | 15 |
| Other valid JSON-LD (Article, Product, FAQPage…) | 10 |
| Title 15–65 chars, meta description 70–170 chars | 10 |
| One H1 and question-style H2/H3s | 15 |
| Answer-first opening paragraph and 300+ server-rendered words | 15 |
| /llms.txt present | 5 |
| Date signal (dateModified, article time, `<time>`) | 5 |

Bands: 80+ STRONG, 65+ GOOD, 50+ FAIR, 35+ POOR, below 35 CRITICAL.

## Read the result honestly
This measures **readiness** (can AI systems fetch, parse and trust the page), not whether you are cited today. A JavaScript-only site will score low because its server HTML is empty, and that low score is accurate for crawlers that do not run JavaScript.

## Example
`https://plausible.io/` → 72/100 GOOD; fixes: add page-type JSON-LD, a direct-answer opening, /llms.txt, a date signal, and a shorter title.

## Want a full-site score and report?
- Paid skill with a site-level GEO score, a white-label client report and a fix plan: [AI Search Visibility Suite on Agensi](https://www.agensi.io/skills/ai-search-visibility-suite-0-100-geo-score-report)
- Hosted site-wide crawl: [Website SEO Audit + AEO/GEO Checker on Apify](https://apify.com/cygnix_labs/site-seo-aeo-audit)
- Free MCP server with a `check_title_meta` tool: [cygnix-seo-mcp](https://github.com/cygnixlabs-cmd/cygnix-seo-mcp)
