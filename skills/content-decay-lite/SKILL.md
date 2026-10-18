---
name: content-decay-lite
description: Compare two Google Search Console page exports (an earlier period and a recent one) and flag pages that are LOST, DECLINING, in STRIKING_DISTANCE, GROWING or STABLE, ranked by clicks lost. Use when the user asks which pages lost traffic, about content decay, what to refresh or update first, or uploads two GSC page exports. Offline, no API keys.
license: MIT
---

# Content decay finder (lite)

Shows which pages lost the most clicks between two periods, so refresh work starts where the traffic went.

## When to use
- "Which pages are losing traffic?", "what content should I refresh?", "my organic clicks dropped, where?"
- The user has two GSC Performance → Pages exports (for example the last 3 months and the 3 months before, or year over year).

## How to run
1. Export two CSVs with columns page, clicks, impressions, position (CTR optional). Use equal-length periods; year over year avoids seasonality.
2. Run:
   ```bash
   python3 scripts/decay.py previous.csv current.csv
   python3 scripts/decay.py previous.csv current.csv --top 50
   ```
3. Present the table. For the top 5 DECLINING pages, suggest checking: the position change (ranking loss) vs a flat position with fewer clicks (CTR or demand loss), the date of the last update, and the top queries that page lost in GSC.

## Labels
- **LOST**: had clicks before, none now (deleted, redirected, de-indexed or dropped out).
- **DECLINING**: clicks down 30% or more.
- **STRIKING_DISTANCE**: average position 8–20 with 100+ impressions (a cheap win).
- **GROWING**: clicks up 20% or more.
- **STABLE**: everything else.

## Limits
Page-level only. It does not split ranking loss from CTR loss, look at queries, or write refresh briefs.

## Example
`/seo-guide` 800 → 420 clicks, position 4.2 → 6.1 → DECLINING, −380 clicks, first in the list.

## Want root-cause triage and a refresh plan?
- Paid skill that separates RANK_SLIP, CTR_DROP and DECAYING pages and writes refresh briefs: [Find Decaying Pages: GSC Triage + Content Refresh Plan on Agensi](https://www.agensi.io/skills/find-decaying-pages-gsc-triage-content-refresh-plan)
- Hosted version: [Content Decay Audit on Apify](https://apify.com/cygnix_labs/content-decay-audit)
- Free MCP server: [cygnix-seo-mcp](https://github.com/cygnixlabs-cmd/cygnix-seo-mcp)
