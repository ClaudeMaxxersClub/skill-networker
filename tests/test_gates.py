import json

from networker_lib.config import NetworkerConfig
from networker_lib.gates import check_report_ready, scaffold
from networker_lib.paths import engagement_paths


def test_report_gate_fails_before_research_artifacts_exist(tmp_path):
    cfg = NetworkerConfig.default(skill_dir=tmp_path)
    cfg.person_name = "Jane Smith"
    cfg.company = "Acme Corp"
    cfg.output_root = tmp_path / "person-intel"
    scaffold(cfg)

    result = check_report_ready(engagement_paths(cfg))

    assert result.passed is False
    assert any("sources.jsonl" in item for item in result.missing)
    assert any("claims.json" in item for item in result.missing)


def test_report_gate_passes_with_minimum_artifact_contract(tmp_path):
    cfg = NetworkerConfig.default(skill_dir=tmp_path)
    cfg.person_name = "Jane Smith"
    cfg.company = "Acme Corp"
    cfg.output_root = tmp_path / "person-intel"
    paths = scaffold(cfg)
    paths.sources.write_text('{"url":"https://example.com","status":"fetched"}\n')
    paths.claims.write_text(json.dumps([{"claim": "CEO", "source": "https://example.com", "confidence": "HIGH", "used_in": ["snapshot"]}]))
    (paths.agents_dir / "person-background.json").write_text(
        json.dumps({"agent": "person-background", "findings": [], "claims": [], "sources": [], "gaps": [], "next_actions": []})
    )
    (paths.agents_dir / "connection-plan.json").write_text(
        json.dumps(
                {
                    "agent": "connection-plan",
                    "findings": ["Primary path: ask Alice"],
                    "claims": [],
                    "sources": [],
                    "gaps": [],
                    "next_actions": [],
                    "primary_path": {
                        "actor": "Alice",
                        "channel": "email",
                        "rationale": "confirmed mutual",
                        "exact_message": "Could you intro us?",
                        "timing": "this week",
                        "success_signal": "reply",
                        "failure_trigger": "no response in 5 business days",
                    },
                }
            )
        )

    result = check_report_ready(paths)

    assert result.passed is True
    assert result.missing == []


def test_report_gate_requires_connection_plan_agent(tmp_path):
    cfg = NetworkerConfig.default(skill_dir=tmp_path)
    cfg.person_name = "Jane Smith"
    cfg.company = "Acme Corp"
    cfg.output_root = tmp_path / "person-intel"
    paths = scaffold(cfg)
    paths.sources.write_text('{"url":"https://example.com","status":"fetched"}\n')
    paths.claims.write_text(json.dumps([{"claim": "CEO", "source": "https://example.com", "confidence": "HIGH", "used_in": ["snapshot"]}]))
    (paths.agents_dir / "person-background.json").write_text(
        json.dumps({"agent": "person-background", "findings": [], "claims": [], "sources": [], "gaps": [], "next_actions": []})
    )

    result = check_report_ready(paths)

    assert result.passed is False
    assert any("connection-plan" in item for item in result.missing)


def test_report_gate_rejects_invalid_artifact_contents(tmp_path):
    cfg = NetworkerConfig.default(skill_dir=tmp_path)
    cfg.person_name = "Jane Smith"
    cfg.company = "Acme Corp"
    cfg.output_root = tmp_path / "person-intel"
    paths = scaffold(cfg)
    paths.sources.write_text("not-json\n")
    paths.claims.write_text(json.dumps([{"claim": "CEO"}]))
    (paths.agents_dir / "person-background.json").write_text("not-json")

    result = check_report_ready(paths)

    assert result.passed is False
    assert any("sources.jsonl" in item for item in result.missing)
    assert any("claims.json" in item for item in result.missing)
    assert any("person-background.json" in item for item in result.missing)
