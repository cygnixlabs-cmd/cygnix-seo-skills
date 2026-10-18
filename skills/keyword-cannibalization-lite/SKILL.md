---
name: keyword-cannibalization-lite
description: Find queries where two or more of your own pages split Google impressions, from a Google Search Console query+page export, and rank them HIGH/MEDIUM/LOW. Use when the user asks about keyword cannibalization, competing pages, pages fighting for the same keyword, or uploads a GSC export with query and page columns. Offline, no API keys.
license: MIT
---

# Keyword cannibalization finder (lite)

Reads a Search Console export with both **query** and **page** columns and lists the queries where more than one of your URLs gets a real share of impressions.

## When to use
- "Are my pages cannibalizing each other?", "two pages rank for the same keyword", "why does Google swap which page ranks?"
- The user has a GSC performance export (or a Looker Studio / API export) at query + page level.

## How to run
1. Export from GSC: Performance → add both Query and Page dimensions (the API, Looker Studio or a GSC export tool; the UI alone exports one dimension at a time). Columns needed: query, page, clicks, impressions, position. Names are auto-detected.
2. Run:
   ```bash
   python3 scripts/cannibalization.py gsc.csv
   python3 scripts/cannibalization.py gsc.csv --min-impressions 50 --min-share 15 --exclude "brand name"
   ```
3. Present the table. For each HIGH row, recommend one action: merge and 301 the weaker page, de-optimise its title/H1 for the query, or differentiate intent. Ask the user before suggesting a redirect of a page that earns clicks.

## Severity
- **HIGH**: the second page gets ≥30% of the query's impressions and ranks within 10 positions of the first.
- **MEDIUM**: the second page gets ≥20%.
- **LOW**: anything else above the thresholds (often harmless, such as a homepage plus a product page).

## Limits
It does not fetch the pages or judge intent overlap, and it does not choose a fix for each page. Some splits are fine (different intents served by different pages), so treat LOW as informational.

## Example
`best running shoes` → primary `/best-running-shoes` (6.2) and `/blog/running-shoes-guide` (14.8, 31% of impressions) → HIGH.

## Want a fix per page?
- Paid skill that gives a merge, canonical or differentiate action for each competing page: [Fix Keyword Cannibalization Using Google Search Console on Agensi](https://www.agensi.io/skills/fix-keyword-cannibalization-using-google-search-console)
- Hosted version: [Keyword Cannibalization Finder on Apify](https://apify.com/cygnix_labs/keyword-cannibalization-finder)
- Free MCP server with a `find_keyword_cannibalization` tool: [cygnix-seo-mcp](https://github.com/cygnixlabs-cmd/cygnix-seo-mcp)
