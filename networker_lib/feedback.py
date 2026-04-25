from __future__ import annotations

import re

MAX_MUTUALS = 50
MAX_FIELD_LENGTH = 180


def _parse_mutuals(text: str) -> list[tuple[str, str]]:
    mutuals = []
    for line in text.splitlines():
        clean = line.strip(" -\t")
        if not clean:
            continue
        if " - " in clean:
            name, context = clean.split(" - ", 1)
        elif ":" in clean:
            name, context = clean.split(":", 1)
        else:
            name, context = clean, ""
        name = _sanitize_field(name)
        context = _sanitize_field(context)
        if name:
            mutuals.append((name, context))
        if len(mutuals) >= MAX_MUTUALS:
            break
    return mutuals


def merge_sales_nav_mutuals(dossier_markdown: str, mutuals_text: str, network: dict) -> str:
    dossier_markdown = _remove_existing_sales_nav_section(dossier_markdown)
    mutuals = _parse_mutuals(mutuals_text)
    strengths = {
        item.get("name", "").lower(): item.get("strength", "weak")
        for item in network.get("top_50_relationships", [])
        if isinstance(item, dict)
    }
    score = {"strong": 3, "medium": 2, "weak": 1}
    ranked = sorted(
        mutuals,
        key=lambda item: score.get(strengths.get(item[0].lower(), "weak"), 1),
        reverse=True,
    )
    lines = ["### Confirmed Mutuals (from Sales Navigator)", ""]
    for name, context in ranked:
        strength = strengths.get(name.lower(), "unclassified")
        suffix = f" - {context}" if context else ""
        lines.append(f"- {name} ({strength}){suffix}")
    if ranked:
        lines.extend(["", "### Re-ranked Warm Path", f"- Ask {ranked[0][0]} for the first intro."])
    insertion = "\n".join(lines) + "\n\n"

    marker = "## Network Bridges"
    if marker not in dossier_markdown:
        return dossier_markdown.rstrip() + "\n\n" + marker + "\n\n" + insertion

    next_section = re.search(r"\n## (?!Network Bridges)", dossier_markdown[dossier_markdown.index(marker) + len(marker):])
    if not next_section:
        return dossier_markdown.rstrip() + "\n\n" + insertion
    offset = dossier_markdown.index(marker) + len(marker) + next_section.start()
    return dossier_markdown[:offset].rstrip() + "\n\n" + insertion + dossier_markdown[offset:].lstrip()


def _remove_existing_sales_nav_section(markdown: str) -> str:
    pattern = re.compile(
        r"\n### Confirmed Mutuals \(from Sales Navigator\)\n.*?(?=\n### |\n## |\Z)",
        re.DOTALL,
    )
    markdown = pattern.sub("\n", markdown)
    pattern = re.compile(r"\n### Re-ranked Warm Path\n.*?(?=\n### |\n## |\Z)", re.DOTALL)
    return pattern.sub("\n", markdown)


def _sanitize_field(value: str) -> str:
    value = re.sub(r"[\x00-\x1f\x7f]", " ", value)
    value = re.sub(r"<[^>]*>", "", value)
    value = re.sub(r"^\s*#+\s*", "", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"\s+", " ", value).strip(" -\t")
    return value[:MAX_FIELD_LENGTH]
