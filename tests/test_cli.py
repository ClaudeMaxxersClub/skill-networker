import importlib.util
from pathlib import Path


def _load_cli_module():
    path = Path(__file__).resolve().parents[1] / "networker-cli.py"
    spec = importlib.util.spec_from_file_location("networker_cli", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_read_file_or_inline_returns_inline_when_value_is_not_safe_path():
    cli = _load_cli_module()
    value = "Alice Tan - knows Jane\n" * 1000

    assert cli._read_file_or_inline(value) == value


def test_read_file_or_inline_reads_existing_file(tmp_path):
    cli = _load_cli_module()
    mutuals = tmp_path / "mutuals.txt"
    mutuals.write_text("Alice Tan - knows Jane\n")

    assert cli._read_file_or_inline(str(mutuals)) == "Alice Tan - knows Jane\n"


def test_load_config_rejects_slug_path_traversal():
    cli = _load_cli_module()

    try:
        cli._load_config("../outside")
    except SystemExit as exc:
        assert "Unsafe slug" in str(exc)
    else:
        raise AssertionError("expected SystemExit")
