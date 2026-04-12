# skill-networker

Deep person intelligence for Claude Code. Researches any named individual at a named company across ~25+ public sources in parallel (14 research agents), then produces a structured relationship dossier: who they are, what they need, how to reach them, what to say, when to say it, and what to avoid.

Built for **legitimate professional networking, sales preparation, partnership evaluation, and relationship-building.** Ships with an explicit scope-and-ethics block — this skill uses public sources only and refuses to fabricate personal details.

Maintained by [ClaudeMaxxersClub](https://github.com/ClaudeMaxxersClub).

---

## What it does

One command:

```
/networker Jane Smith Acme Corp --outreach
```

...produces a ~2-5 page dossier containing:

- **Career arc** — jobs, education, patents, publications, awards
- **Company deep dive** — funding, hiring, customers, competitors, government contracts
- **Inner circle** — publicly-documented co-founder history, mentors, life-decision trace
- **Digital presence** — platforms, posting patterns, tone, engagement network
- **Location & movement** — current city, upcoming conferences, travel patterns
- **Financial posture** — equity model, liquidity assessment (for calibrating outreach, not surveillance)
- **Friction map** — things they've publicly criticized, topics to AVOID
- **Communication playbook** — exactly how to talk to them (tone, length, evidence style)
- **Timing assessment** — momentum score, product windows, STRIKE WINDOW recommendation
- **Needs assessment** — what they actually need right now, and how you uniquely help
- **Connection strategy** — warm paths ranked HOT → WARM → LUKEWARM → STRATEGIC
- **Outreach drafts** — LinkedIn DM, warm intro request, direct email (with `--outreach` flag)

Dossiers are saved to `~/Documents/person-intel/{lastname}-{company}.md` by default and optionally sent to your Telegram or Slack.

## Install

```bash
git clone https://github.com/ClaudeMaxxersClub/skill-networker ~/.claude/skills/networker
```

Claude Code auto-discovers it. Invoke with `/networker` in any Claude Code session.

## First-time setup

Networker is a framework — your personal context stays on your machine.

```bash
cd ~/.claude/skills/networker

# 1. Copy runtime config (output path, local search paths, notification settings)
cp config.template.yaml config.yaml
# edit config.yaml

# 2. Copy your personal user profile (who you are, your value prop, your warm network)
cp library/user-profile.template.md library/user-profile.md
# edit library/user-profile.md
```

Both `config.yaml` and `library/user-profile.md` are gitignored. They never leave your machine. The skill reads them at invocation time and substitutes `{{USER_NAME}}`, `{{USER_COMPANY}}`, `{{USER_LOCATION}}`, `{{USER_VALUE_PROP}}`, and `{{USER_NETWORK_NOTES}}` into each research agent's prompt preamble.

## Usage

```
/networker <Person Name> <Company> [optional context] [--outreach]
```

**Examples:**
```
/networker Jane Smith Acme
/networker Jane Smith Acme Corp --outreach
/networker Alex Rivera OpenAI focus on her AI safety research and Stanford connections
/networker Marie Dupont BioTech I'm meeting her at JPM next week --outreach
```

Parsing rules:
- First 2-4 words = person name (supports compound names like "Anne-Sophie Martin")
- Next word(s) = company name (supports multi-word like "Horizon Materials Corp")
- Remaining text = optional context hints (focus areas, meeting timing, relationship goals)
- `--outreach` flag = also draft 2-3 personalized messages at the end

## How it works

**Phase 1: PARSE & LOAD** — extracts person, company, context, flags; reads `config.yaml` and `library/user-profile.md`; generates name/company variations.

**Phase 2: RESEARCH** — launches all 14 research agents **in a single message** so they run in parallel. Each agent has a specific goal, 5+ search queries, and a structured extract list. A Wave 2 follow-up wave fires targeted searches based on Wave 1 discoveries.

| # | Agent | Focus |
|---|-------|-------|
| 1 | Person Background | Career, education, patents, awards, quotes |
| 2 | Company Intelligence | Funding, team, products, customers, competitors |
| 3 | Inner Circle | Co-founder history, mentors, life decisions |
| 4 | Local Knowledge Base | Grep over your own files for existing relationship |
| 5 | Ecosystem & Industry | Geographic bridges, conferences, communities |
| 6 | Social & Digital | Platforms, posting patterns, digital persona |
| 7 | Deep Personal Enrichment | Schooling, origin, alumni networks |
| 8 | Location Intelligence | Current city, travel patterns, next events |
| 9 | Social Path & Proximity | Warm connection paths HOT → STRATEGIC |
| 10 | Financial Profile | Equity, liquidity, posture (for outreach calibration) |
| 11 | Friction Map | Things they dislike, landmines to avoid |
| 12 | Communication Profile | How to talk to them — tone, evidence, humor |
| 13 | Timing & Momentum | 90-day momentum score, STRIKE WINDOW |
| 14 | Needs & Pain Points | What they need NOW that you uniquely solve |

**Phase 3: SYNTHESIZE & DELIVER** — merges agent outputs, generates the connection playbook, drafts outreach messages (if `--outreach`), saves the dossier locally, optionally sends a Telegram/Slack notification, and presents the full dossier in the conversation.

## Scope & Ethics

**This skill researches publicly-available information only** — LinkedIn, Crunchbase, news, press releases, company websites, academic profiles, public social media, government contract databases, SEC filings. It does NOT scrape authenticated sources, bypass paywalls, fabricate personal details, or guess at non-public information.

**Use responsibly:**
- For legitimate professional networking, sales prep, partnership evaluation, and relationship-building.
- **Not** for stalking, harassment, doxxing, or building profiles on private individuals.
- Respect digital-privacy signals — some people are private *on purpose*.
- Never repeat inferred-but-unconfirmed personal details (net worth, nationality, family) as fact. The dossier uses explicit confidence markers (HIGH/MED/LOW) for a reason.

If a target is a minor, a private individual with no public professional profile, or someone who has explicitly asked not to be researched — **stop.**

## Customize locally (collective workflow)

This repo uses **branches-per-person**, not forks:

```bash
cd ~/.claude/skills/networker
git checkout -b <yourname>
git push -u origin <yourname>
```

Commit freely to your branch. When you have an improvement worth sharing, open a PR from your branch into `main`.

Pull canon updates weekly:

```bash
git fetch origin
git merge origin/main
```

See [skills-hub/CONTRIBUTING.md](https://github.com/ClaudeMaxxersClub/skills-hub/blob/main/CONTRIBUTING.md) for the full workflow.

## Dependencies

| Tool | Required for |
|------|-------------|
| `WebSearch` + `WebFetch` | Agents 1-3, 5-14 |
| `Grep` + `Glob` | Agent 4 (local knowledge base) |
| `Agent` (Task tool) | Parallel Wave 1 dispatch |
| `Bash` | Phase 3 notification (urllib HTTP POST) |
| `Read` / `Write` / `Edit` | Loading config, saving dossier |

No external MCP servers are required. Everything is stdlib + built-in Claude Code tools.

## Known limitations

- **Sub-agent rate limits:** if your account is rate-limited when launching 14 parallel agents, the skill falls back to running research serially from the main conversation. Breadth is comparable; depth on niche questions is lower. This is noted in the dossier's GAPS section when it happens.
- **Common names:** "John Smith" at "Smith Consulting" will produce many false-positive matches. The skill presents a disambiguation list when this happens and asks the user to pick the right match.
- **Extremely private targets:** if the target has no LinkedIn, no press, no published work, and no public social accounts, the skill will produce a thin dossier and clearly flag the gaps. Agent 4 (local knowledge) and Agent 5 (ecosystem) become more valuable in this case.
- **Non-English sources:** search queries are English-only by default. If a target operates primarily in another language, you may want to add localized queries to the agent prompts in your personal branch.

## Current version

`v1.0.0` — see `SKILL.md` frontmatter for the authoritative version.

## License

MIT. See [LICENSE](./LICENSE).
