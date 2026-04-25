# Research Agents

Agents are specialist workstreams. They do not own final conclusions. They emit
structured evidence for synthesis.

Generate current prompts with:

```bash
python3 ~/.claude/skills/networker/networker-cli.py prompts {slug}
```

## Core Agents

| Agent | Purpose |
|---|---|
| Person Background | Career, education, awards, public quotes, professional spine |
| Company Intelligence | Products, funding, hiring, customers, competitors, tech stack |
| Public Voice | Writing, talks, themes, evidence style, tone |
| Network Bridges | Shared schools, cohorts, employers, investors, boards, events, hobbies |
| Social Path & Proximity | Warm paths, intro scripts, proximity plays |
| Location & Event Intelligence | Public location, upcoming events, timing windows |
| Needs & Pain Points | Business and professional needs mapped to verified user capabilities |
| Friction Map | Aversions, criticized practices, topics to avoid |
| Connection Plan | Ranked paths, channels, timing, messages, fallback plan |

## Shared Rules

- Use public professional sources only.
- Fetch URLs before citing.
- Mark confidence as `HIGH`, `MEDIUM`, or `LOW`.
- Return unknown categories with queries tried.
- Do not fabricate personal details.
- Do not include sensitive private material merely because it is technically findable.

## Bridge Taxonomy

Every target gets checked against:

1. secondary school
2. university program and year
3. faculty or lab
4. exchange program
5. accelerator or cohort
6. employer overlap
7. investor or cap table
8. board or advisor
9. physical workspace or precinct
10. publisher or program
11. awards
12. hometown or diaspora
13. language
14. hobby community
15. conference circuit
16. professional association

For every category, output one of:

- confirmed bridge plus source
- plausible bridge plus confidence and follow-up
- unknown plus queries tried
- blocked plus reason
