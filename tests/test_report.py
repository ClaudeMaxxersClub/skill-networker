import json

from networker_lib.config import NetworkerConfig
from networker_lib.gates import scaffold
from networker_lib.report import load_agent_outputs, render_connection_plan, render_dossier


def test_render_connection_plan_extracts_connection_agent_output(tmp_path):
    cfg = NetworkerConfig.default(skill_dir=tmp_path)
    cfg.person_name = "Jane Smith"
    cfg.company = "Acme Corp"
    outputs = [
        {"agent": "person-background", "findings": ["VP Operations"]},
        {
            "agent": "connection-plan",
            "findings": ["Ask Alice Tan for intro"],
            "claims": [],
            "primary_path": {
                "actor": "Alice Tan",
                "channel": "email",
                "rationale": "confirmed mutual",
                "exact_message": "Could you intro us?",
                "timing": "this week",
                "success_signal": "reply",
                "failure_trigger": "no response in 5 business days",
            },
        },
    ]

    rendered = render_connection_plan(cfg, outputs)

    assert "# Jane Smith - Connection Plan" in rendered
    assert "Alice Tan" in rendered
    assert "Could you intro us?" in rendered


def test_load_agent_outputs_reads_json_artifacts(tmp_path):
    cfg = NetworkerConfig.default(skill_dir=tmp_path)
    cfg.person_name = "Jane Smith"
    cfg.company = "Acme Corp"
    cfg.output_root = tmp_path / "person-intel"
    paths = scaffold(cfg)
    (paths.agents_dir / "connection-plan.json").write_text(json.dumps({"agent": "connection-plan", "findings": []}))

    assert load_agent_outputs(paths) == [{"agent": "connection-plan", "findings": []}]


def test_render_dossier_mentions_agent_output_count(tmp_path):
    cfg = NetworkerConfig.default(skill_dir=tmp_path)
    cfg.person_name = "Jane Smith"
    cfg.company = "Acme Corp"

    rendered = render_dossier(cfg, [{"agent": "connection-plan"}], [])

    assert "agent_output_count=1" in rendered


def test_render_dossier_includes_all_documented_sections(tmp_path):
    cfg = NetworkerConfig.default(skill_dir=tmp_path)
    cfg.person_name = "Jane Smith"
    cfg.company = "Acme Corp"

    rendered = render_dossier(cfg, [], [])

    expected_sections = [
        "## Connection Plan",
        "## Snapshot",
        "## Career Arc",
        "## Public Voice",
        "## What They Care About",
        "## What They Avoid",
        "## How They Argue",
        "## Network Bridges",
        "## Commercial Signals",
        "## Events Map",
        "## Meeting Playbook",
        "## Follow-Up Seed",
        "## Know But Don't Say",
        "## Gaps & Unknowns",
        "## Sources",
    ]
    positions = [rendered.index(section) for section in expected_sections]

    assert positions == sorted(positions)
