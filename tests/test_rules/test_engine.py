"""Test rule engine."""
from guardian.rules.engine import RuleEngine
from guardian.core.models import Issue, Severity


def _i(rid):
    return Issue(rule_id=rid, severity=Severity.INFO, message="t", file_path="/t.py", line=1, checker="t")


def test_filters_enabled():
    rules = [{"id": "STA001", "enabled": True}, {"id": "SEC001", "enabled": False}]
    result = RuleEngine(rules).evaluate([_i("STA001"), _i("SEC001")])
    assert len(result) == 1 and result[0].rule_id == "STA001"


def test_empty_rules_pass_through():
    result = RuleEngine([]).evaluate([_i("STA001")])
    assert len(result) == 1


def test_disabled_all():
    result = RuleEngine([{"id": "STA001", "enabled": False}]).evaluate([_i("STA001")])
    assert len(result) == 0
