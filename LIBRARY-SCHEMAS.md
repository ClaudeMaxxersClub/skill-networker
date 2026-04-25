# Library Schemas

Local library files live under `library/`. Copy templates to non-template names
and fill them with real context. Keep real files out of git.

## `config.yaml`

```yaml
output_root: "~/person-intel"
local_search_paths:
  - "~/Documents/person-intel"
notification:
  type: "none"
```

## `library/user-profile.md`

Required fields:

- `USER_NAME`
- `USER_COMPANY`
- `USER_LOCATION`
- `USER_ROLE`
- `USER_VALUE_PROP`
- network notes
- reference customers that are safe to name
- anti-patterns to avoid

## `library/network.yaml`

Recommended keys:

- `education`
- `employers`
- `accelerators`
- `investors`
- `top_50_relationships`
- `known_bridges`
- `research_query_templates`

## `library/rules.md`

Must include:

- externally nameable clients
- internal-only clients
- not-clients list
- fabrication rules
- suppression rules

## Date Consistency

Before citing local network facts, check:

- exchange years fall inside undergrad years
- postgrad starts after undergrad
- full-time roles do not overlap implausibly
- awards are plausible for the target's age and timeline
- same institution bridges are ranked by actual overlap, not name match alone
