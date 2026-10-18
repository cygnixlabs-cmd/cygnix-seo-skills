# Cygnix SEO Skills: free SEO, GEO and AEO agent skills

Six free, MIT-licensed [Agent Skills](https://agentskills.io) (`SKILL.md`) for Claude Code, Codex, Cursor and other agents that support skills. They cluster keywords, classify search intent, find keyword cannibalization and content decay in Google Search Console exports, check `llms.txt` and AI crawler access, and give a page a quick 0-100 AI search visibility score.

Each skill is a short `SKILL.md` plus one standard-library Python 3 script. No API keys, no accounts, no paid SEO tool. The four GSC/keyword skills run fully offline on your CSVs; the two site checks only read public URLs.

## Install

Install all six with [`npx skills`](https://github.com/vercel-labs/skills):

```bash
npx skills add cygnixlabs-cmd/cygnix-seo-skills
```

Or pick one:

| Skill | What it does | Install |
|---|---|---|
| [keyword-clustering-lite](skills/keyword-clustering-lite/SKILL.md) | Groups a keyword list into clusters with a pillar keyword, intent and page type | `npx skills add cygnixlabs-cmd/cygnix-seo-skills --skill keyword-clustering-lite` |
| [search-intent-lite](skills/search-intent-lite/SKILL.md) | Labels keywords informational / commercial / transactional / navigational (+ local) | `npx skills add cygnixlabs-cmd/cygnix-seo-skills --skill search-intent-lite` |
| [keyword-cannibalization-lite](skills/keyword-cannibalization-lite/SKILL.md) | Finds queries where your own pages split impressions (GSC query+page CSV) | `npx skills add cygnixlabs-cmd/cygnix-seo-skills --skill keyword-cannibalization-lite` |
| [content-decay-lite](skills/content-decay-lite/SKILL.md) | Compares two GSC page exports and ranks pages by clicks lost | `npx skills add cygnixlabs-cmd/cygnix-seo-skills --skill content-decay-lite` |
| [llms-txt-check](skills/llms-txt-check/SKILL.md) | Validates `/llms.txt` and checks robots.txt for 8 AI crawlers | `npx skills add cygnixlabs-cmd/cygnix-seo-skills --skill llms-txt-check` |
| [ai-visibility-quick-score](skills/ai-visibility-quick-score/SKILL.md) | One-page 0-100 AI search (GEO/AEO) readiness score with the top 5 fixes | `npx skills add cygnixlabs-cmd/cygnix-seo-skills --skill ai-visibility-quick-score` |

List them without installing: `npx skills add cygnixlabs-cmd/cygnix-seo-skills --list`.

Manual install for Claude Code: copy a folder from `skills/` into `~/.claude/skills/` (personal) or `.claude/skills/` (project).

## Use

Ask in plain language; the agent picks the skill:

- "Cluster these keywords and tell me which page each cluster should be" (paste a list or attach a CSV)
- "Which of my pages are cannibalizing each other?" (attach a GSC query+page export)
- "Which pages lost the most traffic since last quarter?" (attach two GSC page exports)
- "Is example.com blocking ChatGPT or Claude? Does it have a valid llms.txt?"
- "Give https://example.com/ an AI visibility score"

Or run a script directly; every script prints a Markdown table:

```bash
python3 skills/keyword-clustering-lite/scripts/cluster.py examples/keywords.txt
python3 skills/search-intent-lite/scripts/intent.py examples/keywords.txt --brands hubspot
python3 skills/keyword-cannibalization-lite/scripts/cannibalization.py examples/gsc-query-page.csv
python3 skills/content-decay-lite/scripts/decay.py examples/gsc-pages-previous.csv examples/gsc-pages-current.csv
python3 skills/llms-txt-check/scripts/llms_check.py example.com
python3 skills/ai-visibility-quick-score/scripts/quick_score.py https://example.com/
```

Requires Python 3.8+. No third-party packages.

## Free lite vs paid vs hosted

The lite skills are complete tools for their scope. The paid Agensi skills go deeper. The Apify actors run larger versions of the same analysis (bigger inputs, more labels, multi-page crawls) on a schedule, by API, or from an agent over Apify's MCP server.

| Job | Free here (lite) | Paid Agensi skill adds | Hosted Apify actor (runs at scale, by API or MCP) |
|---|---|---|---|
| Keyword clustering | Lexical clusters, pillar, majority intent | [Clusters from your offer and seeds, priority shortlist, page angles; no invented volumes](https://www.agensi.io/skills/keyword-clusters-intent-map-no-paid-seo-tool-needed) | [Keyword Clusterer & Brief](https://apify.com/cygnix_labs/keyword-clusterer-brief) |
| Search intent | Rule-based labels from keyword wording | [Flags existing pages built in the wrong format for the intent](https://www.agensi.io/skills/serp-intent-mapper-keyword-page-type-match) | [SERP Intent Mapper](https://apify.com/cygnix_labs/serp-intent-mapper) |
| Cannibalization | Competing pages per query, HIGH/MEDIUM/LOW | [A merge, canonical or differentiate action per page](https://www.agensi.io/skills/fix-keyword-cannibalization-using-google-search-console) | [Keyword Cannibalization Finder](https://apify.com/cygnix_labs/keyword-cannibalization-finder) |
| Content decay | 5 page labels, ranked by clicks lost | [RANK_SLIP vs CTR_DROP vs DECAYING triage, refresh briefs](https://www.agensi.io/skills/find-decaying-pages-gsc-triage-content-refresh-plan) | [Content Decay Audit](https://apify.com/cygnix_labs/content-decay-audit) |
| llms.txt / AI crawlers | Check only (format, links, 8 bots) | [Writes a starter llms.txt, robots.txt fixes and a checklist](https://www.agensi.io/skills/ship-llms-txt-unlock-ai-crawlers-access-fix-pack) | [AEO & GEO Readiness Checker](https://apify.com/cygnix_labs/aeo-readiness-checker) |
| AI visibility score | One page, 8 checks | [Site-level GEO score, white-label client report, fix plan](https://www.agensi.io/skills/ai-search-visibility-suite-0-100-geo-score-report) | [Website SEO Audit + AEO/GEO Checker](https://apify.com/cygnix_labs/site-seo-aeo-audit) |

Prefer MCP tools to skills? [cygnix-seo-mcp](https://github.com/cygnixlabs-cmd/cygnix-seo-mcp) is a free, local MCP server (`npx -y cygnix-seo-mcp`) with `cluster_keywords`, `classify_search_intent`, `find_keyword_cannibalization`, `check_title_meta` and `content_brief_outline`.

## Limits (read before trusting a number)

- Clustering and intent are lexical and rule-based; they do not read the live SERP. Check the top clusters against Google before merging pages.
- GSC exports are sampled and anonymised; small queries are missing.
- The AI visibility score measures readiness (can AI crawlers fetch, parse and trust a page), not whether you are cited today.
- AI search crawlers rarely fetch `llms.txt` today; robots.txt access and server-rendered content matter more.

## Disclosure

These skills are made by [Cygnix Labs](https://github.com/cygnixlabs-cmd), which also sells the paid Agensi skills and Apify actors linked above. The free skills here are not trials and do not expire, phone home or collect data. The site checks send requests only to the URL you give them, with the user agent `CygnixSEOSkills/1.0`.

## Contributing

Issues and pull requests are welcome: bug reports with a sample CSV (anonymised), new intent modifiers, or other languages.

## License

[MIT](LICENSE)
