# Networker Phases

## Phase 0: Scope, Ethics, and Footprint Score

Confirm this is a legitimate professional target. Stop if the target is a minor,
private individual with no professional public footprint, or an opt-out subject.

Run three quick searches:

- `"{full_name}" "{company}"`
- `"{full_name}" site:linkedin.com`
- `"{full_name}" (podcast OR blog OR medium OR conference OR speaker OR twitter OR substack)`

Score 0-15 across LinkedIn depth, public voice, company exposure, social presence,
and news coverage.

| Score | Profile | Default response |
|---|---|---|
| 0-3 | Ghost | Upgrade to `deep`, rely on company/ecosystem/local context, avoid personal speculation |
| 4-7 | Low-profile | All core passes, heavier fetch protocol |
| 8-11 | Visible | Standard workflow |
| 12-15 | Prolific | Focus on recency, quotes, and signal quality |

## Phase 1: Load Ground Truth

Read local files before external search:

- `config.yaml`
- `library/user-profile.md`
- `library/network.yaml`
- `library/icp.md`
- `library/tov.md`
- `library/case-studies.md`
- `library/competitors.md`
- `library/rules.md`
- `library/verified-clients.md`

Treat local files as hypotheses. Check timeline consistency before citing them.

## Phase 2: Golden Request and Fetch Protocol

Fetch the company About, Team, Leadership, Careers, Blog, and News pages first.

If a URL is used as evidence, fetch it and record it in `sources.jsonl`.
Search snippets are leads, not sources.

Fallback chain:

1. canonical URL
2. public cache or archive
3. alternate source carrying the same fact
4. mark blocked with reason

## Phase 3: Specialist Research

Generate prompts:

```bash
python3 ~/.claude/skills/networker/networker-cli.py prompts {slug}
```

Run the agents in parallel when available. If parallel execution is not available,
run them sequentially and note the limitation in `recon-state.json`.

Each agent returns JSON:

```json
{
  "agent": "person-background",
  "findings": [],
  "claims": [],
  "sources": [],
  "gaps": [],
  "next_actions": []
}
```

## Phase 4: Wave 2 Follow-Ups

Trigger targeted follow-up when Wave 1 reveals:

- a specific school, cohort, investor, or conference that may overlap with the user network
- a co-founder or advisor who explains the target's trajectory
- a product launch, funding event, or hiring cluster that changes timing
- thin results across multiple agents
- conflicting claims about title, dates, location, or company status

Skip Wave 2 if time-sensitive, but document the skipped opportunities.

## Phase 5: Synthesis

Before drafting:

- reconcile conflicting claims
- compute temporal overlap for every bridge
- remove claims without sources
- apply suppression and verified-client rules
- separate "know but don't say" from outreach-safe material

## Phase 6: Report and Outreach

Validate:

```bash
python3 ~/.claude/skills/networker/networker-cli.py validate {slug}
```

Generate:

```bash
python3 ~/.claude/skills/networker/networker-cli.py report {slug}
```

Only draft outreach when the evidence supports a legitimate, low-friction ask.
