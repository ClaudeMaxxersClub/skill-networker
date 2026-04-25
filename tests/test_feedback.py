from networker_lib.feedback import merge_sales_nav_mutuals


def test_sales_nav_feedback_appends_confirmed_mutuals_and_reranks():
    dossier = """# Jane Smith

## Network Bridges

### Recommended Warm Paths
- Alice Tan: weak alumni path

## Sources
"""
    mutuals = "Alice Tan - worked with Jane at Acme\nBob Lee - investor"
    network = {
        "top_50_relationships": [
            {"name": "Alice Tan", "strength": "strong"},
            {"name": "Bob Lee", "strength": "medium"},
        ]
    }

    updated = merge_sales_nav_mutuals(dossier, mutuals, network)

    assert "Confirmed Mutuals (from Sales Navigator)" in updated
    assert "Alice Tan" in updated
    assert "Re-ranked Warm Path" in updated
    assert updated.index("Alice Tan") < updated.index("Bob Lee")


def test_sales_nav_feedback_replaces_previous_confirmed_mutuals_section():
    dossier = """# Jane Smith

## Network Bridges

### Confirmed Mutuals (from Sales Navigator)

- Old Mutual (strong)

### Re-ranked Warm Path
- Ask Old Mutual for the first intro.

## Sources
"""

    updated = merge_sales_nav_mutuals(dossier, "Alice Tan - knows Jane", {"top_50_relationships": []})

    assert "Old Mutual" not in updated
    assert "Alice Tan" in updated
    assert updated.count("Confirmed Mutuals (from Sales Navigator)") == 1


def test_sales_nav_feedback_sanitizes_markdown_section_injection():
    dossier = "## Network Bridges\n\n## Sources\n"
    mutuals = "## Fake Section - <script>alert(1)</script>\nAlice [link](https://evil.example) - knows Jane"

    updated = merge_sales_nav_mutuals(dossier, mutuals, {"top_50_relationships": []})

    assert "## Fake Section" not in updated
    assert "<script>" not in updated
    assert "[link]" not in updated
