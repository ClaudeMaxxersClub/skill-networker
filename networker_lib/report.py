from __future__ import annotations

import json
from datetime import date


def render_dossier(config, agent_outputs: list[dict], claims: list[dict]) -> str:
    sections = [
        f"# {config.person_name} - Networker Dossier",
        "",
        f"**Prepared:** {date.today().isoformat()}",
        f"**Company:** {config.company}",
        f"**Context:** {config.context}",
        "",
        "## Connection Plan",
        "Use the Connection Plan agent output as source of truth. Rank paths by legitimacy, warmth, timing, and response probability.",
        "",
        "## Snapshot",
        "",
        "## Career Arc",
        "",
        "## Public Voice",
        "",
        "## What They Care About",
        "",
        "## What They Avoid",
        "",
        "## How They Argue",
        "",
        "## Network Bridges",
        "",
        "## Commercial Signals",
        "",
        "## Events Map",
        "",
        "## Meeting Playbook",
        "",
        "## Follow-Up Seed",
        "",
        "## Know But Don't Say",
        "",
        "## Gaps & Unknowns",
        "",
        "## Sources",
    ]
    for claim in claims:
        sections.append(f"- {claim.get('source')}: {claim.get('claim')} ({claim.get('confidence')})")
    sections.append("")
    sections.append("<!-- Agent outputs are stored as JSON artifacts; do not replace them with unsupported prose. -->")
    sections.append(f"<!-- agent_output_count={len(agent_outputs)} -->")
    return "\n".join(sections) + "\n"


def render_connection_plan(config, agent_outputs: list[dict]) -> str:
    connection_output = next(
        (output for output in agent_outputs if output.get("agent") == "connection-plan"),
        {},
    )
    primary_path = connection_output.get("primary_path") or {}
    lines = [
        f"# {config.person_name} - Connection Plan",
        "",
        f"**Company:** {config.company}",
        f"**Context:** {config.context}",
        "",
        "## Primary Path",
    ]
    lines.extend(
        [
            f"- **Actor:** {primary_path.get('actor', '')}",
            f"- **Channel:** {primary_path.get('channel', '')}",
            f"- **Rationale:** {primary_path.get('rationale', '')}",
            f"- **Exact Message:** {primary_path.get('exact_message', '')}",
            f"- **Timing:** {primary_path.get('timing', '')}",
            f"- **Success Signal:** {primary_path.get('success_signal', '')}",
            f"- **Failure Trigger:** {primary_path.get('failure_trigger', '')}",
        ]
    )
    lines.extend(
        [
            "",
            "## Required Fields Before External Use",
            "",
            "- actor",
            "- channel",
            "- rationale",
            "- exact first message",
            "- timing",
            "- success signal",
            "- failure trigger",
            "",
        ]
    )
    return "\n".join(lines)


def load_agent_outputs(paths) -> list[dict]:
    outputs = []
    for file_path in sorted(paths.agents_dir.glob("*.json")):
        outputs.append(json.loads(file_path.read_text()))
    return outputs
