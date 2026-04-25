# Networker Architecture

## Purpose

Networker is a skill-centric person-intelligence system for legitimate
professional relationship building. It combines:

- operator-facing workflow docs in markdown
- a stdlib-first Python automation layer for config, prompts, gates, validation, and reports
- local library files for user context, network graph, ICP, tone, competitors, case studies, and suppression rules
- filesystem artifacts that preserve evidence, claims, research state, and final deliverables

Design principle: deterministic work is scripted; judgment stays with the operator.

## Layout

```text
networker/
  SKILL.md
  ARCHITECTURE.md
  PHASES.md
  RESEARCH-AGENTS.md
  ETHICS.md
  OUTPUTS.md
  TOOLBELT.md
  LIBRARY-SCHEMAS.md
  LESSONS.md
  networker-cli.py
  networker_lib/
  tests/
  library/
```

## Runtime Model

1. Operator creates an engagement with `networker-cli.py init`.
2. Config is written to `~/person-intel/{slug}/.networker-config.json`.
3. Agent prompts are rendered deterministically from `networker_lib.dispatch`.
4. Agents gather public-source evidence and save JSON outputs under `agents/`.
5. Sources and claims are normalized into `sources.jsonl` and `claims.json`.
6. Gates validate minimum artifacts before report generation.
7. Dossier and connection plan are assembled from artifacts.
8. Sales Nav or CRM feedback can be merged later without re-running research.

## Artifact Root

Runtime artifacts live outside the skill tree:

```text
~/person-intel/{person-company-slug}/
  .networker-config.json
  recon-state.json
  sources.jsonl
  claims.json
  agents/
  outreach/
  dossier.md
  connection-plan.md
```

## Extension Boundary

Add new capabilities as adapters that:

- declare input requirements
- emit versioned artifacts under the engagement root
- preserve `sources.jsonl` and `claims.json`
- do not add mandatory heavy dependencies
- include tests for parser, validator, or report contract changes

Do not bury operational rules inside one huge `SKILL.md`. Put reusable doctrine in companion docs and deterministic behavior in `networker_lib/`.
