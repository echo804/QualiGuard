from guardian.reporters.terminal import TerminalReporter
from guardian.reporters.json_reporter import JsonReporter
from guardian.reporters.html_reporter import HtmlReporter
from guardian.reporters.markdown import MarkdownReporter
from guardian.reporters.sarif import SarifReporter


REPORTER_MAP = {
    "terminal": TerminalReporter,
    "json": JsonReporter,
    "html": HtmlReporter,
    "markdown": MarkdownReporter,
    "sarif": SarifReporter,
}