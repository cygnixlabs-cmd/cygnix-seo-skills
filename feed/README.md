# Cygnix Labs listings feed

A single JSON file listing every live Cygnix Labs product:
- Agensi skills and bundles (agensi.io)
- Public Apify actors (apify.com/cygnix_labs)

**Stable URL (latest):**
https://raw.githubusercontent.com/cygnixlabs-cmd/cygnix-seo-skills/main/feed/cygnix-listings.json

## Schema
Top level: `publisher`, `contact`, `updated` (YYYY-MM-DD), `count`, `counts`, `items[]`.

Each item has:
| field | meaning |
|---|---|
| `type` | `skill`, `bundle` or `apify_actor` |
| `title` | listing title |
| `slug` | platform slug (use it as the page slug on the site) |
| `price` | e.g. `$7`, or Apify pay-per-event pricing |
| `url` | canonical buy/run link |
| `short_description` | one line for cards and meta descriptions |
| `category` | SEO, AEO / AI search, Content, Social media, Lead generation, Developer, Productivity |
| `platform` | Agensi or Apify |

## Publish plan
1. **Source of truth:** Cygnix Labs regenerates the feed from the Agensi seller API (live listings) and the Apify API (public actors), then commits it here. It refreshes whenever a listing goes live or changes, and at least weekly.
2. **Website use:** fetch the raw URL at build time, or on the client with a cache of 1 hour or more. Render one page per item at `/tools/{slug}` with Product or SoftwareApplication JSON-LD, plus category hub pages.
3. **AI discovery:** generate `/llms.txt` on the site from the same feed (title, URL, short_description).
4. **Stability:** fields are only ever added, never renamed or removed. Pin a commit URL if you need a frozen copy.
