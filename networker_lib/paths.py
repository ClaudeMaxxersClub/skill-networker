from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


def slugify(person_name: str, company: str) -> str:
    raw = f"{person_name} {company}".lower()
    slug = re.sub(r"[^a-z0-9]+", "-", raw).strip("-")
    return re.sub(r"-{2,}", "-", slug) or "unknown-target"


@dataclass(frozen=True)
class EngagementPaths:
    root: Path
    config: Path
    recon_state: Path
    sources: Path
    claims: Path
    dossier: Path
    connection_plan: Path
    agents_dir: Path
    outreach_dir: Path


def engagement_paths(config) -> EngagementPaths:
    root = Path(config.output_root).expanduser() / config.slug
    return EngagementPaths(
        root=root,
        config=root / ".networker-config.json",
        recon_state=root / "recon-state.json",
        sources=root / "sources.jsonl",
        claims=root / "claims.json",
        dossier=root / "dossier.md",
        connection_plan=root / "connection-plan.md",
        agents_dir=root / "agents",
        outreach_dir=root / "outreach",
    )
