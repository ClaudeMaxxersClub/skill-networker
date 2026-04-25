from __future__ import annotations

import argparse
import json
import shlex
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .paths import slugify


@dataclass
class Invocation:
    person_name: str
    company: str
    context: str = "intro"
    depth: str = "standard"
    linkedin: str = ""
    outreach: bool = False
    sales_nav_feedback: str = ""


@dataclass
class NetworkerConfig:
    skill_dir: Path
    person_name: str = ""
    company: str = ""
    context: str = "intro"
    depth: str = "standard"
    linkedin: str = ""
    outreach: bool = False
    agent_mode: str = "parallel"
    output_root: Path = field(default_factory=lambda: Path("~/person-intel").expanduser())
    local_search_paths: list[Path] = field(default_factory=list)
    network_file: Path = Path("library/network.yaml")
    user_profile_file: Path = Path("library/user-profile.md")
    icp_file: Path = Path("library/icp.md")
    tov_file: Path = Path("library/tov.md")
    case_studies_file: Path = Path("library/case-studies.md")
    competitors_file: Path = Path("library/competitors.md")
    rules_file: Path = Path("library/rules.md")
    verified_clients_file: Path = Path("library/verified-clients.md")

    @classmethod
    def default(cls, skill_dir: Path) -> "NetworkerConfig":
        skill_dir = Path(skill_dir)
        cfg = cls(skill_dir=skill_dir)
        local = _load_local_config(skill_dir / "config.yaml")
        if "output_root" in local:
            cfg.output_root = _resolve_runtime_path(local["output_root"])
            _ensure_outside_skill_dir(cfg.output_root, skill_dir)
        if "local_search_paths" in local:
            cfg.local_search_paths = [_resolve_runtime_path(path) for path in local["local_search_paths"]]
        return cfg

    @property
    def slug(self) -> str:
        return slugify(self.person_name, self.company)

    def to_json(self) -> str:
        payload = asdict(self)
        for key, value in list(payload.items()):
            if isinstance(value, Path):
                payload[key] = str(value)
            if isinstance(value, list):
                payload[key] = [str(item) if isinstance(item, Path) else item for item in value]
        payload["slug"] = self.slug
        return json.dumps(payload, indent=2, sort_keys=True)

    @classmethod
    def from_json(cls, data: dict, skill_dir: Path) -> "NetworkerConfig":
        data = dict(data)
        data.pop("slug", None)
        data["skill_dir"] = Path(skill_dir)
        path_fields = {
            "output_root",
            "network_file",
            "user_profile_file",
            "icp_file",
            "tov_file",
            "case_studies_file",
            "competitors_file",
            "rules_file",
            "verified_clients_file",
        }
        for field_name in path_fields:
            if field_name in data:
                data[field_name] = Path(data[field_name]).expanduser()
        if "local_search_paths" in data:
            data["local_search_paths"] = [Path(p).expanduser() for p in data["local_search_paths"]]
        return cls(**data)


def parse_invocation(text: str) -> Invocation:
    tokens = shlex.split(text)
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--company")
    parser.add_argument("--context", default="")
    parser.add_argument("--depth", choices=["fast", "standard", "deep"], default="standard")
    parser.add_argument("--linkedin", default="")
    parser.add_argument("--outreach", action="store_true")
    parser.add_argument("--sales-nav-feedback", default="")
    known, rest = parser.parse_known_args(tokens)
    unknown_flags = [token for token in rest if token.startswith("--")]
    if unknown_flags:
        raise ValueError(f"Unknown option: {unknown_flags[0]}")

    if known.company:
        person_name = " ".join(rest).strip()
        company = known.company
        context = known.context or "intro"
        if not person_name:
            raise ValueError("Expected a person name before --company.")
    else:
        if len(rest) < 3:
            raise ValueError("Expected '<Person Name> <Company>' or '--company'.")
        person_name = " ".join(rest[:2])
        company = rest[2]
        context = " ".join(rest[3:]) or known.context or "intro"

    return Invocation(
        person_name=person_name,
        company=company,
        context=context,
        depth=known.depth,
        linkedin=known.linkedin,
        outreach=known.outreach,
        sales_nav_feedback=known.sales_nav_feedback,
    )


def config_from_invocation(text: str, skill_dir: Path) -> NetworkerConfig:
    invocation = parse_invocation(text)
    cfg = NetworkerConfig.default(skill_dir)
    cfg.person_name = invocation.person_name
    cfg.company = invocation.company
    cfg.context = invocation.context
    cfg.depth = invocation.depth
    cfg.linkedin = invocation.linkedin
    cfg.outreach = invocation.outreach
    return cfg


def _load_local_config(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        import yaml  # type: ignore

        payload = yaml.safe_load(path.read_text()) or {}
        return payload if isinstance(payload, dict) else {}
    except Exception:
        return _parse_small_yaml(path.read_text())


def _parse_small_yaml(text: str) -> dict:
    """Parse the simple config.template.yaml shape without requiring PyYAML."""
    result: dict[str, object] = {}
    current_list: str | None = None
    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        stripped = line.strip()
        if stripped.startswith("- ") and current_list:
            result.setdefault(current_list, [])
            result[current_list].append(_strip_quotes(stripped[2:].strip()))  # type: ignore[index]
            continue
        current_list = None
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value:
            result[key] = _strip_quotes(value)
        else:
            result[key] = []
            current_list = key
    return result


def _strip_quotes(value: str) -> str:
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def _resolve_runtime_path(value: str | Path) -> Path:
    path = Path(value).expanduser()
    if path.is_absolute():
        return path
    return Path.home() / path


def _ensure_outside_skill_dir(path: Path, skill_dir: Path) -> None:
    resolved_path = path.resolve()
    resolved_skill_dir = skill_dir.resolve()
    if resolved_path == resolved_skill_dir or resolved_skill_dir in resolved_path.parents:
        raise ValueError(f"output_root must not be inside the skill bundle: {path}")
