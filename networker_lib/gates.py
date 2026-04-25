from __future__ import annotations

import json
from dataclasses import dataclass

from .paths import EngagementPaths, engagement_paths
from .validators import validate_artifact_contract


@dataclass(frozen=True)
class GateResult:
    passed: bool
    missing: list[str]
    reason: str


def scaffold(config) -> EngagementPaths:
    paths = engagement_paths(config)
    paths.root.mkdir(parents=True, exist_ok=True)
    paths.agents_dir.mkdir(parents=True, exist_ok=True)
    paths.outreach_dir.mkdir(parents=True, exist_ok=True)
    paths.config.write_text(config.to_json() + "\n")
    if not paths.recon_state.exists():
        paths.recon_state.write_text(json.dumps({"coverage": {}, "signals": [], "fetches": []}, indent=2) + "\n")
    return paths


def check_report_ready(paths: EngagementPaths) -> GateResult:
    missing = []
    missing.extend(validate_artifact_contract(paths.sources, paths.claims, paths.agents_dir).errors)

    if missing:
        return GateResult(False, missing, "Required research artifacts are missing or invalid.")
    return GateResult(True, [], "Minimum research artifact contract is present.")
