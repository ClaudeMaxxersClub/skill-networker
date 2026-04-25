# Outputs

## Required Artifacts

```text
~/person-intel/{slug}/
  .networker-config.json
  recon-state.json
  sources.jsonl
  claims.json
  agents/*.json
  dossier.md
  connection-plan.md
```

## `sources.jsonl`

One JSON object per fetched source:

```json
{"url":"https://example.com/team","status":"fetched","title":"Team","fetched_at":"2026-04-25","notes":"target bio"}
```

## `claims.json`

List of sourced claims:

```json
[
  {
    "claim": "Jane Smith is VP Operations at Acme.",
    "source": "https://example.com/team",
    "confidence": "HIGH",
    "used_in": ["snapshot", "connection_plan"]
  }
]
```

Every claim source must match a URL in `sources.jsonl`.

## `agents/*.json`

Every agent artifact must be a JSON object with:

```json
{
  "agent": "connection-plan",
  "findings": [],
  "claims": [],
  "sources": [],
  "gaps": [],
  "next_actions": []
}
```

`agent` must match one of the known Networker agent slugs.

The `connection-plan` artifact is required before `report` can generate
external deliverables. It must include a complete `primary_path`:

```json
{
  "agent": "connection-plan",
  "findings": [],
  "claims": [],
  "sources": [],
  "gaps": [],
  "next_actions": [],
  "primary_path": {
    "actor": "Alice Tan",
    "channel": "email",
    "rationale": "confirmed mutual with direct professional context",
    "exact_message": "Could you intro us?",
    "timing": "this week",
    "success_signal": "positive reply or intro",
    "failure_trigger": "no response in five business days"
  }
}
```

## Dossier Structure

1. Connection Plan
2. Snapshot
3. Career Arc
4. Public Voice
5. What They Care About
6. What They Avoid
7. How They Argue
8. Network Bridges
9. Commercial Signals
10. Events Map
11. Meeting Playbook
12. Follow-Up Seed
13. Know But Don't Say
14. Gaps & Unknowns
15. Sources

## Connection Plan Requirements

Include:

- primary path
- backup paths
- cold fallback
- channels not to use
- probability estimate
- regroup trigger

Every path needs:

- actor
- channel
- rationale
- exact first message
- timing
- success signal
- failure trigger
