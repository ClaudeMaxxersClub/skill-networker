# networker

Canonical person-intelligence and connection-planning skill.

This bundle merges the upstream Atlas and Networker approaches, then upgrades
them with the same structural pattern used by `web-recon`: companion docs,
runtime artifacts, a tested CLI, and explicit gates.

## Install

The canonical local copy lives at:

```text
~/.claude/skills/networker
```

## Quick Start

```bash
python3 ~/.claude/skills/networker/networker-cli.py init '"Jane Smith" --company "Acme Corp" --context intro --depth standard --outreach'
python3 ~/.claude/skills/networker/networker-cli.py prompts jane-smith-acme-corp
python3 ~/.claude/skills/networker/networker-cli.py validate jane-smith-acme-corp
```

Runtime artifacts are written to `~/person-intel/{slug}/`.

## Tests

```bash
cd ~/.claude/skills/networker
python3 -m pytest tests -q
```
