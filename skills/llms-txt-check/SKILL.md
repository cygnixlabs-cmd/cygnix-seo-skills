---
name: llms-txt-check
description: Check whether a website has a valid /llms.txt (llmstxt.org format, working links, size) and whether robots.txt lets AI crawlers such as GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot and Google-Extended in. Use when the user asks about llms.txt, AI crawler access, blocking or allowing AI bots, or whether ChatGPT/Claude/Perplexity can read their site. Read-only.
license: MIT
---

# llms.txt and AI crawler access check

A read-only check of two files: `/llms.txt` and `/robots.txt`. It reports problems and does not write or change anything.

## When to use
- "Do I have a valid llms.txt?", "is my site blocking ChatGPT / Claude / Perplexity?", "can AI crawlers read my site?"

## How to run
```bash
python3 scripts/llms_check.py example.com
python3 scripts/llms_check.py https://docs.example.com --max-links 40
```
Needs outbound HTTPS. Makes about 25 requests at most (it checks up to `--max-links` links from llms.txt, with a short pause between them).

## What it checks
- `/llms.txt` returns 200 and is text, not an HTML soft-404 page.
- Format per llmstxt.org: one `#` H1, a `>` summary, `##` sections, Markdown links.
- Size under ~50 KB, so an agent can load it.
- Up to N links resolve (HEAD, falling back to GET).
- `/llms-full.txt` presence (optional).
- robots.txt access to `/` for GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-SearchBot, PerplexityBot, Google-Extended and CCBot.

## Read the result honestly
AI search crawlers rarely fetch llms.txt today; coding agents and IDE assistants do. For appearing in AI answers, robots.txt access and server-rendered content matter more. Say this to the user rather than overselling llms.txt.

## Example
`python3 scripts/llms_check.py plausible.io` → llms.txt missing (404), all 8 AI crawlers allowed, sitemap declared → "Publish /llms.txt" as the only fix.

## Want the files written for you?
- Paid skill that writes a starter llms.txt, audits robots.txt for AI bots and ships a fix checklist: [Ship llms.txt + Unlock AI Crawlers on Agensi](https://www.agensi.io/skills/ship-llms-txt-unlock-ai-crawlers-access-fix-pack)
- Hosted multi-page check: [AEO & GEO Readiness Checker on Apify](https://apify.com/cygnix_labs/aeo-readiness-checker)
