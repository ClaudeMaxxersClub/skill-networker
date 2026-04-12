# library/

This folder holds **your personal context** that the Networker skill reads at
invocation time and substitutes into agent prompts. Everything in here except
`README.md` and `*.template.md` is gitignored — your profile never leaves your
machine.

## First-time setup

```bash
cp library/user-profile.template.md library/user-profile.md
```

Then edit `library/user-profile.md` and fill in every section. The richer
you make it, the better Agent 9 (Social Path & Proximity) and Agent 14 (Needs
& Value) perform, because those two agents are the ones that actually
personalize outreach to YOU.

## Files

| File | Purpose |
|------|---------|
| `user-profile.template.md` | Committed template you copy to `user-profile.md` |
| `user-profile.md` | **Your private profile.** Gitignored. |
| `README.md` | This file. |

## What to put in user-profile.md

At minimum:

- **Name + company** — substituted into `{{USER_NAME}}` / `{{USER_COMPANY}}`
- **Location** — substituted into `{{USER_LOCATION}}`
- **Value proposition** — the one-sentence "what your company does and who you help" — substituted into `{{USER_VALUE_PROP}}`
- **Network notes** — accelerators, investors, past employers, alma maters, conferences you attend, specific people you know in common industries — substituted into `{{USER_NETWORK_NOTES}}` and used by Agent 9 to find warm paths

The template has guided prompts for each section.

## Why this isn't committed

Networker is a framework. The framework (14 agents, search queries, dossier
template, synthesis logic) is valuable to everyone. Your personal profile
(specific clients, warm connections, company metrics, pitch positioning) is
valuable *only to you* and may be confidential. Keeping them separate is how
this skill stays shareable while still being personalized.
