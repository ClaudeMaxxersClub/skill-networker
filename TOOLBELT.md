# Toolbelt

## CLI

Create engagement:

```bash
python3 ~/.claude/skills/networker/networker-cli.py init '"Jane Smith" --company "Acme Corp" --context demo --depth deep --outreach'
```

Generate prompts:

```bash
python3 ~/.claude/skills/networker/networker-cli.py prompts jane-smith-acme-corp
```

Generate one prompt:

```bash
python3 ~/.claude/skills/networker/networker-cli.py prompts jane-smith-acme-corp --agent network-bridges
```

Check readiness:

```bash
python3 ~/.claude/skills/networker/networker-cli.py status jane-smith-acme-corp
```

Validate artifacts:

```bash
python3 ~/.claude/skills/networker/networker-cli.py validate jane-smith-acme-corp
```

Build dossier:

```bash
python3 ~/.claude/skills/networker/networker-cli.py report jane-smith-acme-corp
```

`report` is intentionally strict. It fails unless `sources.jsonl`,
`claims.json`, and `agents/connection-plan.json` satisfy the contract in
`OUTPUTS.md`, including a complete warm `primary_path`.

Merge Sales Navigator mutuals:

```bash
python3 ~/.claude/skills/networker/networker-cli.py feedback jane-smith-acme-corp --mutuals mutuals.txt
```

## Deterministic vs Agentic Work

Script these:

- slug generation
- directory scaffold
- prompt rendering
- artifact validation
- report skeleton
- Sales Nav feedback merge

Keep these agentic:

- evaluating credibility
- choosing which weak signals matter
- deciding what is outreach-safe
- writing final messages
- ranking relationship paths when evidence is ambiguous
