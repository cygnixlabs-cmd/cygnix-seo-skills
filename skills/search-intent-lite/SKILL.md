---
name: search-intent-lite
description: Classify keywords by search intent (informational, commercial, transactional, navigational, plus a local flag) and suggest the page type that should target each one. Use when the user asks for search intent, keyword intent, what kind of page to build for a keyword, or why a page type does not rank. Offline, rule-based, no API keys.
license: MIT
---

# Search intent classifier (lite)

Labels each keyword with its likely intent and the page type that usually matches it, so a blog post is not aimed at a "buy" query (or the reverse).

## When to use
- "What's the intent of these keywords?", "should this be a product page or a blog post?", "map keywords to page types".

## How to run
```bash
python3 scripts/intent.py keywords.txt
python3 scripts/intent.py keywords.csv --brands "acme,acmecorp" --locations "riyadh,dubai"
cat keywords.txt | python3 scripts/intent.py -
```
Input is one keyword per line, or a CSV with a `keyword` or `query` column. Pass your brand names so brand queries are labelled navigational.

Present the table and the totals. Point out any `unclear` or `mixed` rows: those need a look at the live SERP.

## How it works (and its limits)
Rule-based modifiers ("how", "what" → informational; "best", "vs", "review", "software" → commercial; "buy", "price", "coupon" → transactional; brand + "login" → navigational; "near me" or a city → local). It reads the words, not the SERP. Google can treat a query differently from its wording, so the confidence column is honest about that.

## Example
| keyword | intent | page type |
|---|---|---|
| what is a crm | informational | guide / FAQ article |
| crm vs erp | commercial | comparison page |
| crm pricing | transactional | pricing page |
| hubspot login | navigational | brand / login page |

## Want more?
- Paid skill that maps keyword → page type and flags existing pages built in the wrong format: [SERP Intent Mapper on Agensi](https://www.agensi.io/skills/serp-intent-mapper-keyword-page-type-match)
- Hosted version for large keyword lists, by API or MCP: [SERP Intent Mapper on Apify](https://apify.com/cygnix_labs/serp-intent-mapper)
- Free MCP server with a `classify_search_intent` tool: [cygnix-seo-mcp](https://github.com/cygnixlabs-cmd/cygnix-seo-mcp)
