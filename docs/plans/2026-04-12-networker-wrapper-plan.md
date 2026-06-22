# Networker Deprecation Note

## Goal

Make it explicit that `skill-networker` is a temporary migration facade and that the canonical wrapper and retirement rules live in the Atlas docs.

## Repo Role

- `skill-atlas` is canonical.
- `skill-networker` is the lightweight surface.
- Networker should optimize for onboarding and quick use, not engine divergence.
- Networker is deprecated once the wrapper contract is stable.
- The source of truth for wrapper behavior and retirement rules is:
  - `skill-atlas/docs/plans/2026-04-12-atlas-networker-outer-join-design.md`
  - `skill-atlas/docs/plans/2026-04-12-atlas-networker-outer-join.md`

## What Networker Should Keep

- simple command examples
- lighter user-facing framing
- user-profile-first setup
- local-search and notification emphasis
- quick pre-call dossier posture

## What Networker Should Not Own Long Term

- independent bridge logic
- independent evidence rules
- independent output schema
- independent research pass evolution
- independent config model

## Local Responsibility

When touching this repo:

1. keep examples and onboarding language aligned with Atlas `fast` mode
2. do not add independent research logic, schema rules, or retirement criteria here
3. point users to Atlas as the canonical implementation
