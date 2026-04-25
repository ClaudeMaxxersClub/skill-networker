from pathlib import Path

from networker_lib.config import NetworkerConfig
from networker_lib.paths import engagement_paths, slugify


def test_slugify_is_stable_and_filesystem_safe():
    assert slugify("Jane A. Smith", "Acme / Robotics, Inc.") == "jane-a-smith-acme-robotics-inc"


def test_engagement_paths_use_slug_and_expected_artifacts(tmp_path):
    cfg = NetworkerConfig.default(skill_dir=tmp_path)
    cfg.person_name = "Jane Smith"
    cfg.company = "Acme Corp"
    cfg.output_root = tmp_path / "person-intel"

    paths = engagement_paths(cfg)

    assert paths.root == tmp_path / "person-intel" / "jane-smith-acme-corp"
    assert paths.config == paths.root / ".networker-config.json"
    assert paths.recon_state == paths.root / "recon-state.json"
    assert paths.sources == paths.root / "sources.jsonl"
    assert paths.claims == paths.root / "claims.json"
    assert paths.dossier == paths.root / "dossier.md"
    assert paths.connection_plan == paths.root / "connection-plan.md"
    assert paths.agents_dir == paths.root / "agents"
    assert paths.outreach_dir == paths.root / "outreach"
