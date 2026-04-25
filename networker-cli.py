#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from networker_lib.config import NetworkerConfig, config_from_invocation
from networker_lib.dispatch import AGENTS, render_agent_prompt
from networker_lib.feedback import merge_sales_nav_mutuals
from networker_lib.gates import check_report_ready, scaffold
from networker_lib.paths import engagement_paths
from networker_lib.report import load_agent_outputs, render_connection_plan, render_dossier


SKILL_DIR = Path(__file__).resolve().parent


def _load_config(target: str) -> NetworkerConfig:
    target_path = Path(target).expanduser()
    if target_path.is_dir():
        config_path = target_path / ".networker-config.json"
    else:
        if "/" in target or "\\" in target or target in {"", ".", ".."}:
            raise SystemExit(f"Unsafe slug: {target}")
        default_cfg = NetworkerConfig.default(SKILL_DIR)
        output_root = Path(default_cfg.output_root).expanduser().resolve()
        config_path = (output_root / target / ".networker-config.json").resolve()
        if not _is_relative_to(config_path, output_root):
            raise SystemExit(f"Unsafe slug: {target}")
    if not config_path.exists():
        raise SystemExit(f"No engagement config found at {config_path}")
    return NetworkerConfig.from_json(json.loads(config_path.read_text()), skill_dir=SKILL_DIR)


def cmd_init(args) -> int:
    try:
        cfg = config_from_invocation(args.invocation, SKILL_DIR)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    paths = scaffold(cfg)
    print(paths.root)
    return 0


def cmd_prompts(args) -> int:
    cfg = _load_config(args.slug)
    selected = AGENTS if args.agent == "all" else tuple(agent for agent in AGENTS if agent.slug == args.agent)
    if not selected:
        raise SystemExit(f"Unknown agent: {args.agent}")
    for agent in selected:
        print(f"--- {agent.slug} ---")
        print(render_agent_prompt(cfg, agent))
    return 0


def cmd_status(args) -> int:
    cfg = _load_config(args.slug)
    paths = engagement_paths(cfg)
    result = check_report_ready(paths)
    print(json.dumps({"ready": result.passed, "missing": result.missing, "reason": result.reason}, indent=2))
    return 0 if result.passed else 1


def cmd_validate(args) -> int:
    cfg = _load_config(args.slug)
    paths = engagement_paths(cfg)
    results = [check_report_ready(paths)]
    errors = []
    for result in results:
        errors.extend(getattr(result, "errors", []))
        errors.extend(getattr(result, "missing", []))
    print(json.dumps({"ok": not errors, "errors": errors}, indent=2))
    return 0 if not errors else 1


def cmd_report(args) -> int:
    cfg = _load_config(args.slug)
    paths = engagement_paths(cfg)
    gate = check_report_ready(paths)
    if not gate.passed:
        print(json.dumps({"ok": False, "missing": gate.missing, "reason": gate.reason}, indent=2))
        return 1
    claims = json.loads(paths.claims.read_text())
    agent_outputs = load_agent_outputs(paths)
    dossier = render_dossier(cfg, agent_outputs, claims)
    paths.dossier.write_text(dossier)
    paths.connection_plan.write_text(render_connection_plan(cfg, agent_outputs))
    print(paths.dossier)
    return 0


def cmd_feedback(args) -> int:
    cfg = _load_config(args.slug)
    paths = engagement_paths(cfg)
    if not paths.dossier.exists():
        raise SystemExit(f"No dossier found at {paths.dossier}. Run report first.")
    dossier = paths.dossier.read_text()
    mutuals = _read_file_or_inline(args.mutuals)
    network_path = SKILL_DIR / cfg.network_file
    network = {}
    if network_path.exists():
        try:
            import yaml  # optional, only used if available

            network = yaml.safe_load(network_path.read_text()) or {}
        except Exception:
            network = {}
    paths.dossier.write_text(merge_sales_nav_mutuals(dossier, mutuals, network))
    print(paths.dossier)
    return 0


def _read_file_or_inline(value: str) -> str:
    try:
        path = Path(value).expanduser()
        if path.exists() and path.is_file():
            return path.read_text()
    except OSError:
        pass
    return value


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="networker-cli.py")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init")
    init.add_argument("invocation")
    init.set_defaults(func=cmd_init)

    prompts = sub.add_parser("prompts")
    prompts.add_argument("slug")
    prompts.add_argument("--agent", default="all")
    prompts.set_defaults(func=cmd_prompts)

    status = sub.add_parser("status")
    status.add_argument("slug")
    status.set_defaults(func=cmd_status)

    validate = sub.add_parser("validate")
    validate.add_argument("slug")
    validate.set_defaults(func=cmd_validate)

    report = sub.add_parser("report")
    report.add_argument("slug")
    report.set_defaults(func=cmd_report)

    feedback = sub.add_parser("feedback")
    feedback.add_argument("slug")
    feedback.add_argument("--mutuals", required=True)
    feedback.set_defaults(func=cmd_feedback)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
