import json

from networker_lib.validators import (
    validate_agent_outputs,
    validate_artifact_contract,
    validate_claims,
    validate_sources,
)


def test_validate_sources_rejects_empty_or_malformed_jsonl(tmp_path):
    sources = tmp_path / "sources.jsonl"
    sources.write_text('{"url":"https://example.com"}\nnot-json\n')

    result = validate_sources(sources)

    assert result.ok is False
    assert "line 2" in result.errors[0]


def test_validate_claims_requires_source_and_confidence(tmp_path):
    claims = tmp_path / "claims.json"
    claims.write_text(json.dumps([{"claim": "CEO"}]))

    result = validate_claims(claims)

    assert result.ok is False
    assert "source" in " ".join(result.errors)
    assert "confidence" in " ".join(result.errors)


def test_validate_claims_accepts_minimum_contract(tmp_path):
    claims = tmp_path / "claims.json"
    claims.write_text(json.dumps([{"claim": "CEO", "source": "https://example.com", "confidence": "HIGH", "used_in": ["snapshot"]}]))

    result = validate_claims(claims)

    assert result.ok is True
    assert result.errors == []


def test_validate_agent_outputs_requires_json_objects(tmp_path):
    agents = tmp_path / "agents"
    agents.mkdir()
    (agents / "bad.json").write_text("not-json")
    (agents / "list.json").write_text("[]")

    result = validate_agent_outputs(agents)

    assert result.ok is False
    assert any("bad.json" in error for error in result.errors)
    assert any("list.json" in error for error in result.errors)


def test_validate_agent_outputs_accepts_minimum_contract(tmp_path):
    agents = tmp_path / "agents"
    agents.mkdir()
    (agents / "person-background.json").write_text(
        json.dumps({"agent": "person-background", "findings": [], "claims": [], "sources": [], "gaps": [], "next_actions": []})
    )

    result = validate_agent_outputs(agents)

    assert result.ok is True


def test_validate_agent_outputs_requires_known_agent_and_contract_keys(tmp_path):
    agents = tmp_path / "agents"
    agents.mkdir()
    (agents / "unknown.json").write_text(json.dumps({"agent": "unknown", "findings": []}))

    result = validate_agent_outputs(agents)

    assert result.ok is False
    assert any("unknown agent" in error for error in result.errors)
    assert any("missing claims" in error for error in result.errors)


def test_validate_artifact_contract_requires_claim_source_in_sources(tmp_path):
    sources = tmp_path / "sources.jsonl"
    claims = tmp_path / "claims.json"
    agents = tmp_path / "agents"
    agents.mkdir()
    sources.write_text('{"url":"https://example.com","status":"fetched"}\n')
    claims.write_text(
        json.dumps(
            [
                {
                    "claim": "CEO",
                    "source": "https://other.example.com",
                    "confidence": "HIGH",
                    "used_in": ["snapshot"],
                }
            ]
        )
    )
    (agents / "connection-plan.json").write_text(
        json.dumps(
            {
                "agent": "connection-plan",
                "findings": [],
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

    result = validate_artifact_contract(sources, claims, agents)

    assert result.ok is False
    assert any("not present in sources.jsonl" in error for error in result.errors)
