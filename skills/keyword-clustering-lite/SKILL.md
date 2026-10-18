---
name: keyword-clustering-lite
description: Group a keyword list into topic clusters with a pillar keyword, majority search intent and suggested page type, so one page targets each cluster. Use when the user pastes keywords or a keyword CSV and asks to cluster, group, organise or map keywords to pages, or plan a content hub. Offline, no API keys.
license: MIT
---

# Keyword clustering (lite)

Turns a flat keyword list into page-sized clusters. Each cluster gets a pillar keyword (highest volume, or shortest if there is no volume), a majority intent and the page type that usually ranks for that intent.

## When to use
- "Cluster these keywords", "group this keyword export", "which keywords can share one page?"
- Planning a pillar/cluster content hub from a keyword tool export (Ahrefs, Semrush, GSC, Keyword Planner).

## How to run
1. Save the keywords as a `.txt` (one per line) or a CSV with a `keyword` or `query` column. An optional `volume` / `search volume` / `impressions` column is used to pick pillars and order clusters.
2. Run:
   ```bash
   python3 scripts/cluster.py keywords.csv            # default threshold 0.5
   python3 scripts/cluster.py keywords.txt --threshold 0.4   # looser clusters
   ```
3. Present the Markdown table. For the top 3 clusters, suggest one URL slug and an H1 each.

## How it works (and its limits)
Lexical clustering: stopwords are removed, words are lightly stemmed, and a keyword joins the cluster whose pillar shares at least `threshold` of its core terms (Jaccard). Single-word cores only join identical cores. It does **not** look at live SERPs, so synonyms ("cheap" vs "affordable") stay separate and two clusters with the same ranking URLs are not merged. Tell the user to check the live SERP for the top clusters before merging or splitting pages.

## Example
Input: `best crm for small business`, `small business crm software`, `crm for small business`, `crm vs erp`, `erp vs crm difference`.
Output: cluster 1 "crm for small business" (commercial, comparison page, 3 keywords); cluster 2 "crm vs erp" (commercial, 2 keywords).

## Want more?
- Paid skill that builds intent-labelled clusters from your offer and seed terms, with a priority shortlist and page angles: [Keyword Clusters + Intent Map on Agensi](https://www.agensi.io/skills/keyword-clusters-intent-map-no-paid-seo-tool-needed)
- Hosted version for large lists (up to 50,000 keywords) with content briefs: [Keyword Clusterer & Brief on Apify](https://apify.com/cygnix_labs/keyword-clusterer-brief)
- Free MCP server with a `cluster_keywords` tool: [cygnix-seo-mcp](https://github.com/cygnixlabs-cmd/cygnix-seo-mcp)
