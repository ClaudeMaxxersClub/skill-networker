from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from .dispatch import AGENTS


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    errors: list[str]


KNOWN_AGENT_SLUGS = {agent.slug for agent in AGENTS}
REQUIRED_AGENT_KEYS = {"agent", "findings", "claims", "sources", "gaps", "next_actions"}
REQUIRED_CONNECTION_PATH_KEYS = {
    "actor",
    "channel",
    "rationale",
    "exact_message",
    "timing",
    "success_signal",
    "failure_trigger",
}
URL_RE = re.compile(r"^https?://[^\s]+$")


def validate_sources(path: Path) -> ValidationResult:
    errors = []
    if not path.exists() or path.stat().st_size == 0:
        return ValidationResult(False, [f"{path.name} is missing or empty"])

    for index, line in enumerate(path.read_text().splitlines(), start=1):
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            errors.append(f"{path.name} line {index} is not valid JSON")
            continue
        if not row.get("url"):
            errors.append(f"{path.name} line {index} missing url")
        elif not URL_RE.match(str(row["url"])):
            errors.append(f"{path.name} line {index} has invalid url")
    return ValidationResult(not errors, errors)


def validate_claims(path: Path) -> ValidationResult:
    errors = []
    if not path.exists() or path.stat().st_size == 0:
        return ValidationResult(False, [f"{path.name} is missing or empty"])
    try:
        claims = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        return ValidationResult(False, [f"{path.name} is not valid JSON: {exc}"])
    if not isinstance(claims, list):
        return ValidationResult(False, [f"{path.name} must contain a list"])
    for index, claim in enumerate(claims, start=1):
        if not claim.get("claim"):
            errors.append(f"{path.name} claim {index} missing claim")
        if not claim.get("source"):
            errors.append(f"{path.name} claim {index} missing source")
        elif not URL_RE.match(str(claim["source"])):
            errors.append(f"{path.name} claim {index} has invalid source URL")
        if claim.get("confidence") not in {"HIGH", "MEDIUM", "LOW"}:
            errors.append(f"{path.name} claim {index} missing confidence")
        if not isinstance(claim.get("used_in"), list) or not claim.get("used_in"):
            errors.append(f"{path.name} claim {index} missing used_in")
    return ValidationResult(not errors, errors)


def validate_agent_outputs(path: Path) -> ValidationResult:
    errors = []
    if not path.exists():
        return ValidationResult(False, [f"{path.name} is missing"])
    files = sorted(path.glob("*.json"))
    if not files:
        return ValidationResult(False, ["agents/*.json is missing"])
    for file_path in files:
        try:
            payload = json.loads(file_path.read_text())
        except json.JSONDecodeError as exc:
            errors.append(f"{file_path.name} is not valid JSON: {exc}")
            continue
        if not isinstance(payload, dict):
            errors.append(f"{file_path.name} must contain a JSON object")
            continue
        if not payload.get("agent"):
            errors.append(f"{file_path.name} missing agent")
        elif payload["agent"] not in KNOWN_AGENT_SLUGS:
            errors.append(f"{file_path.name} unknown agent: {payload['agent']}")
        for key in sorted(REQUIRED_AGENT_KEYS - set(payload)):
            errors.append(f"{file_path.name} missing {key}")
        if payload.get("agent") == "connection-plan":
            primary_path = payload.get("primary_path")
            if not isinstance(primary_path, dict):
                errors.append(f"{file_path.name} missing primary_path")
            else:
                for key in sorted(REQUIRED_CONNECTION_PATH_KEYS - set(primary_path)):
                    errors.append(f"{file_path.name} primary_path missing {key}")
    return ValidationResult(not errors, errors)


def validate_artifact_contract(sources_path: Path, claims_path: Path, agents_path: Path) -> ValidationResult:
    errors = []
    source_result = validate_sources(sources_path)
    claim_result = validate_claims(claims_path)
    agent_result = validate_agent_outputs(agents_path)
    for result in (source_result, claim_result, agent_result):
        errors.extend(result.errors)

    if source_result.ok and claim_result.ok:
        source_urls = set()
        for line in sources_path.read_text().splitlines():
            source_urls.add(json.loads(line)["url"])
        claims = json.loads(claims_path.read_text())
        for index, claim in enumerate(claims, start=1):
            if claim["source"] not in source_urls:
                errors.append(f"claims.json claim {index} source not present in sources.jsonl: {claim['source']}")

    if agents_path.exists():
        agent_slugs = set()
        for file_path in agents_path.glob("*.json"):
            try:
                payload = json.loads(file_path.read_text())
            except json.JSONDecodeError:
                continue
            if isinstance(payload, dict):
                agent_slugs.add(payload.get("agent"))
        if "connection-plan" not in agent_slugs:
            errors.append("agents/connection-plan.json is required before report generation")

    return ValidationResult(not errors, errors)
