from networker_lib.config import NetworkerConfig
from networker_lib.dispatch import AGENTS, render_agent_prompt


def test_agent_registry_combines_networker_agents_with_atlas_coverage():
    names = [agent.name for agent in AGENTS]

    assert "Person Background" in names
    assert "Company Intelligence" in names
    assert "Network Bridges" in names
    assert "Location & Event Intelligence" in names
    assert "Connection Plan" in names


def test_render_agent_prompt_includes_evidence_and_ethics_contract(tmp_path):
    cfg = NetworkerConfig.default(skill_dir=tmp_path)
    cfg.person_name = "Jane Smith"
    cfg.company = "Acme Corp"
    cfg.context = "demo"

    prompt = render_agent_prompt(cfg, AGENTS[0])

    assert "TARGET: Jane Smith" in prompt
    assert "COMPANY: Acme Corp" in prompt
    assert "Every factual claim must include a fetched source URL" in prompt
    assert "Public professional sources only" in prompt
    assert "confidence: HIGH|MEDIUM|LOW" in prompt


def test_render_all_agent_prompts_handles_agent_specific_placeholders(tmp_path):
    cfg = NetworkerConfig.default(skill_dir=tmp_path)
    cfg.person_name = "Jane Smith"
    cfg.company = "Acme Corp"

    prompts = [render_agent_prompt(cfg, agent) for agent in AGENTS]

    assert len(prompts) == len(AGENTS)
    assert "{network_attribute}" not in "\n".join(prompts)
    assert "<network_attribute>" in "\n".join(prompts)
