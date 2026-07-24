"""Test Session and Scheduler integration."""
from guardian.core.session import Session
from guardian.core.scheduler import Scheduler
from guardian.checkers.static_analyzer import StaticAnalyzer
from guardian.checkers.security_scanner import SecurityScanner
from guardian.core.models import ScanResult


def test_session_create_result():
    session = Session("/tmp")
    result = session.create_result()
    assert isinstance(result, ScanResult)


def test_static_analyzer_syntax_error(tmp_path):
    f = tmp_path / "error.py"
    f.write_text("def foo(:\n    pass\n", encoding="utf-8")
    result = ScanResult(target=str(f))
    scheduler = Scheduler([StaticAnalyzer()])
    scheduler.run(str(f), result)
    assert any(i.rule_id == "STA000" for i in result.issues)


def test_security_scanner(tmp_path):
    f = tmp_path / "secret.py"
    f.write_text('password = "secret"\n', encoding="utf-8")
    result = ScanResult(target=str(f))
    scheduler = Scheduler([SecurityScanner()])
    scheduler.run(str(f), result)
    assert any(i.rule_id == "SEC001" for i in result.issues)


def test_scheduler_collects_files(tmp_path):
    f = tmp_path / "test.py"
    f.write_text("x = 1\n", encoding="utf-8")
    scheduler = Scheduler([])
    files = scheduler._collect_files(str(f))
    assert len(files) == 1
