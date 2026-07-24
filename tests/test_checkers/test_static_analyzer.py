from guardian.checkers.static_analyzer import StaticAnalyzer
from tests.conftest import FIXTURES

def test_detect_long_function():
    checker = StaticAnalyzer()
    issues = checker.check(str(FIXTURES / "bad_python.py"))
    assert any(i.rule_id == "STA001" for i in issues)

def test_detect_syntax_error(tmp_path):
    bad = tmp_path / "bad_syntax.py"
    bad.write_text("def foo(:\n    pass\n")
    checker = StaticAnalyzer()
    issues = checker.check(str(bad))
    assert any(i.rule_id == "STA000" for i in issues)
