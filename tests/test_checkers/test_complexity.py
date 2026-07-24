from guardian.checkers.complexity import ComplexityAnalyzer
from tests.conftest import FIXTURES

def test_high_complexity():
    checker = ComplexityAnalyzer()
    issues = checker.check(str(FIXTURES / "bad_python.py"))
    assert any(i.rule_id == "CPX001" for i in issues)
