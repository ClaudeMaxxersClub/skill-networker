import json
from pathlib import Path

import pytest

from networker_lib.config import NetworkerConfig, config_from_invocation, parse_invocation


def test_parse_invocation_supports_networker_flags():
    invocation = parse_invocation(
        '"Jane Smith" --company "Acme Corp" --context demo --depth deep '
        "--linkedin https://linkedin.com/in/jane --outreach"
    )

    assert invocation.person_name == "Jane Smith"
    assert invocation.company == "Acme Corp"
    assert invocation.context == "demo"
    assert invocation.depth == "deep"
    assert invocation.linkedin == "https://linkedin.com/in/jane"
    assert invocation.outreach is True


def test_parse_invocation_supports_legacy_networker_positional_form():
    invocation = parse_invocation(
        "Marie Dupont BioTech meeting at JPM next week --outreach"
    )

    assert invocation.person_name == "Marie Dupont"
    assert invocation.company == "BioTech"
    assert invocation.context == "meeting at JPM next week"
    assert invocation.outreach is True


def test_config_defaults_keep_runtime_artifacts_outside_skill_tree(tmp_path):
    cfg = NetworkerConfig.default(skill_dir=tmp_path)

    assert cfg.output_root == Path("~/person-intel").expanduser()
    assert not str(cfg.output_root).startswith(str(tmp_path))
    assert cfg.depth == "standard"
    assert cfg.agent_mode == "parallel"


def test_config_from_invocation_loads_local_config_yaml(tmp_path):
    (tmp_path / "config.yaml").write_text(
        """
output_root: "./intel-output"
local_search_paths:
  - "./crm"
  - "~/notes"
""".strip()
        + "\n"
    )

    cfg = config_from_invocation('"Jane Smith" --company "Acme Corp"', tmp_path)

    assert cfg.output_root == Path.home() / "intel-output"
    assert cfg.local_search_paths[0] == Path.home() / "crm"
    assert cfg.local_search_paths[1] == Path("~/notes").expanduser()


def test_config_rejects_output_root_inside_skill_bundle(tmp_path):
    (tmp_path / "config.yaml").write_text(f'output_root: "{tmp_path / "output"}"\n')

    with pytest.raises(ValueError, match="skill bundle"):
        NetworkerConfig.default(skill_dir=tmp_path)


def test_parse_invocation_rejects_missing_person_with_company_flag():
    with pytest.raises(ValueError, match="person name"):
        parse_invocation('--company "Acme Corp"')


def test_parse_invocation_rejects_unknown_flags():
    with pytest.raises(ValueError, match="Unknown option"):
        parse_invocation('"Jane Smith" --compnay "Acme Corp"')


def test_config_json_round_trip(tmp_path):
    cfg = NetworkerConfig.default(skill_dir=tmp_path)
    cfg.person_name = "Jane Smith"
    cfg.company = "Acme Corp"
    cfg.context = "intro"

    payload = cfg.to_json()
    loaded = NetworkerConfig.from_json(json.loads(payload), skill_dir=tmp_path)

    assert loaded.person_name == "Jane Smith"
    assert loaded.company == "Acme Corp"
    assert loaded.slug == "jane-smith-acme-corp"
