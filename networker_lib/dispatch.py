from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ResearchAgent:
    slug: str
    name: str
    goal: str
    queries: tuple[str, ...]
    extract: tuple[str, ...]


AGENTS: tuple[ResearchAgent, ...] = (
    ResearchAgent(
        "person-background",
        "Person Background",
        "Build the target's professional spine: roles, education, achievements, public quotes.",
        ('"{name}" "{company}" LinkedIn', '"{name}" "{company}" biography', '"{name}" speaker podcast interview'),
        ("career timeline", "education", "awards", "quotes with dates"),
    ),
    ResearchAgent(
        "company-intelligence",
        "Company Intelligence",
        "Map the company context, funding, products, hiring, customers, competitors, and tech stack.",
        ('"{company}" funding raised', '"{company}" careers', '"{company}" customers partnerships'),
        ("company overview", "funding", "hiring velocity", "competitor matrix"),
    ),
    ResearchAgent(
        "public-voice",
        "Public Voice",
        "Extract the target's public writing, talks, themes, tone, and evidence style.",
        ('"{name}" blog OR medium OR substack', '"{name}" podcast OR keynote', '"{name}" site:x.com OR site:twitter.com'),
        ("themes", "verbatim quotes", "communication style", "topics they avoid"),
    ),
    ResearchAgent(
        "network-bridges",
        "Network Bridges",
        "Diff the target against user network files across schools, cohorts, employers, investors, boards, events, and hobbies.",
        ('"{name}" "{network_attribute}"', '"{company}" "{known_bridge}"', '"{name}" alumni cohort investor'),
        ("shared attributes", "temporal overlap", "intro paths", "unknown categories with queries tried"),
    ),
    ResearchAgent(
        "social-path",
        "Social Path & Proximity",
        "Rank legitimate warm paths and proximity plays from HOT to STRATEGIC.",
        ('"{name}" "{known_connection}"', '"{target_university}" alumni "{user_location}"', '"{industry}" conference "{target_city}"'),
        ("connection paths", "intro scripts", "event co-attendance", "content engagement plan"),
    ),
    ResearchAgent(
        "location-events",
        "Location & Event Intelligence",
        "Find current public location, upcoming events, travel signals, and timing windows.",
        ('"{name}" conference speaker', '"{company}" event tradeshow', '"{industry}" conference 2026'),
        ("current location", "upcoming events", "strike window", "confidence levels"),
    ),
    ResearchAgent(
        "commercial-needs",
        "Needs & Pain Points",
        "Infer company and role needs from public evidence and match only to verified user capabilities.",
        ('"{company}" hiring challenge bottleneck', '"{company}" launch expansion', '"{name}" looking for recommendations'),
        ("business needs", "professional needs", "urgency", "unique value match"),
    ),
    ResearchAgent(
        "friction-map",
        "Friction Map",
        "Identify public aversions, criticized practices, competitor landmines, and phrasing to avoid.",
        ('"{name}" criticism frustrated', '"{company}" lawsuit dispute complaint', '"{name}" "{competitor}" criticism'),
        ("landmines", "avoid list", "values hierarchy", "quote-backed concerns"),
    ),
    ResearchAgent(
        "connection-plan",
        "Connection Plan",
        "Synthesize ranked paths, channels, timing, exact messages, failure triggers, and regroup plan.",
        ('"{name}" "{company}" latest', '"{name}" event podcast', '"{company}" partnership news'),
        ("primary path", "backup paths", "cold fallback", "copy-paste-ready messages"),
    ),
)


def render_agent_prompt(config, agent: ResearchAgent) -> str:
    values = _PlaceholderMap({"name": config.person_name, "company": config.company})
    query_lines = "\n".join(f"- {query.format_map(_PlaceholderMap(values))}" for query in agent.queries)
    extract_lines = "\n".join(f"- {item}" for item in agent.extract)
    return f"""TARGET: {config.person_name}
COMPANY: {config.company}
CONTEXT: {config.context}
DEPTH: {config.depth}
LINKEDIN_HINT: {config.linkedin or "none"}

TASK: {agent.goal}

RULES:
- Public professional sources only.
- Every factual claim must include a fetched source URL.
- Mark confidence: HIGH|MEDIUM|LOW.
- If a category is unknown, list the queries tried instead of guessing.
- Do not collect private addresses, private family details, authenticated content, paywalled bypasses, or real-time location traces.
- Respect verified-client and suppression rules before drafting outreach.

SEARCH QUERIES TO TRY:
{query_lines}

EXTRACT:
{extract_lines}

RETURN JSON with keys: agent, findings, claims, sources, gaps, next_actions.
"""


class _PlaceholderMap(dict):
    def __missing__(self, key):
        return f"<{key}>"
