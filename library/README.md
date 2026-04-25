# library/

This folder holds local context templates for Networker. Copy templates to their
non-template filenames and fill them with private data on your machine.

Committed:

- `user-profile.template.md`
- `network.template.yaml`
- `icp.template.md`
- `tov.template.md`
- `case-studies.template.md`
- `competitors.template.md`
- `rules.template.md`
- `verified-clients.template.md`

Gitignored local files:

- `user-profile.md`
- `network.yaml`
- `icp.md`
- `tov.md`
- `case-studies.md`
- `competitors.md`
- `rules.md`
- `verified-clients.md`

Minimum first-time setup:

```bash
cp library/user-profile.template.md library/user-profile.md
cp library/network.template.yaml library/network.yaml
cp library/rules.template.md library/rules.md
```

Networker is a framework. The methodology, templates, CLI, and tests are shared;
your personal network, client list, private notes, and outreach rules stay local.
