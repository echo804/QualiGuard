"""Test chat commands."""
from guardian.chat.commands import COMMANDS, cmd_read


def test_help_has_all_commands():
    help_text = COMMANDS["/help"]("")
    for cmd in ["/scan", "/fix", "/read", "/report", "/rules", "/clear", "/exit"]:
        assert cmd in help_text


def test_read_existing_file(tmp_path):
    f = tmp_path / "test.py"
    f.write_text("x = 1", encoding="utf-8")
    result = cmd_read(str(f))
    assert "x = 1" in result and "--- end ---" in result


def test_read_nonexistent():
    result = cmd_read("/nonexistent/file.py")
    assert "not found" in result


def test_read_empty():
    result = cmd_read("")
    assert "Usage" in result


def test_clear_sentinel():
    assert COMMANDS["/clear"]("") == "__CLEAR__"


def test_exit_sentinel():
    assert COMMANDS["/exit"]("") == "__EXIT__"
