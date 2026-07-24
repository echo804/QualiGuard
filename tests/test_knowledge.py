"""Test knowledge base coverage."""
from guardian.knowledge import RULE_ADVICE


def test_critical_rules_have_advice():
    critical = ["STA000", "STA001", "SEC001", "SEC002", "SEC003", "SEC004", "CPX001"]
    for rid in critical:
        assert rid in RULE_ADVICE, f"{rid} missing"
        a = RULE_ADVICE[rid]
        assert "title" in a and "why" in a and "fix" in a


def test_style_rules_have_advice():
    for rid in ["STYF401", "STYF841", "STYE741"]:
        assert rid in RULE_ADVICE, f"{rid} missing"


def test_advice_non_empty():
    for rid, a in RULE_ADVICE.items():
        assert len(a["title"]) > 0 and len(a["why"]) > 0 and len(a["fix"]) > 0
