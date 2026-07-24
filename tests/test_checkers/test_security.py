from guardian.checkers.security_scanner import SecurityScanner
from tests.conftest import FIXTURES

def test_detect_hardcoded_password():
    checker = SecurityScanner()
    issues = checker.check(str(FIXTURES / "insecure_code.py"))
    assert any(i.rule_id == "SEC001" for i in issues)

def test_detect_eval():
    checker = SecurityScanner()
    issues = checker.check(str(FIXTURES / "insecure_code.py"))
    assert any(i.rule_id == "SEC004" for i in issues)
