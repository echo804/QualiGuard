<div align="center">

# QualiGuard

> **AI-driven Code Quality CLI**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow?logo=opensourceinitiative)](LICENSE)
[![CI](https://img.shields.io/badge/CI-Passing-228B22?logo=githubactions)](.github/workflows/code-quality.yml)
[![Tests](https://img.shields.io/badge/Tests-26%2F26-228B22?logo=pytest)](tests/)
[![Ruff](https://img.shields.io/badge/Ruff-0.15+-D7FF64?logo=ruff)](https://astral.sh/ruff)
[![Agent](https://img.shields.io/badge/Agent-ReAct-blue?logo=openai&logoColor=white)](src/guardian/agent/)
[![Eval](https://img.shields.io/badge/Eval-50%20scenarios-green?logo=githubactions)](src/guardian/eval/)
[![PyPI](https://img.shields.io/badge/PyPI-Coming%20Soon-orange?logo=pypi)](https://pypi.org/)

---

</div>

## Why QualiGuard

QualiGuard is an AI-powered code quality CLI that scans, analyzes, and fixes code issues before commit. It supports static analysis, security scanning, complexity detection, auto-fixing, and multi-format reporting. The project now extends to a full **Tool-using Agent** system with a **50-scenario quantitative evaluation** framework.

---

## Installation

```bash
pip install qualiguard

# For Agent and Eval features (requires API Key)
pip install qualiguard[chat]

# Verify
qg --help
```

## Quick Start

### CLI Scan

```bash
# Scan current directory
qg scan

# Scan specific target
qg scan ./src

# Generate HTML report
qg scan ./src --format html --output report.html
```

### Auto Fix

```bash
qg fix ./src
# Output: Fixed 60/61 fixable issues.
```

### AI Agent (New)

Wraps 6 core QualiGuard capabilities as LLM-callable tools. Supports natural language driven, multi-step, autonomous code review workflows via ReAct loop.

```bash
# Configure API Key (DeepSeek / OpenAI compatible)
cp .env.example .env

# Single step: scan and analyze
qg agent "Scan tests/fixtures/ for security issues"

# Multi-step: scan -> fix -> verify
qg agent "Scan and fix tests/fixtures/bad_python.py"

# With detailed trace logging
qg agent --verbose "Read insecure_code.py and explain SEC001 rule"

# Complex: scan -> analyze -> generate report
qg agent "Scan current directory and generate an HTML report"
```

### Evaluation Benchmark (New)

50 standardized scenarios x 6 types x 3 difficulty levels. Auto-run and generate quantitative reports.

```bash
# Quick run 5 security scenarios
qg eval --scenarios 5 --type security

# Filter by difficulty
qg eval --scenarios 10 --severity hard

# Run all and save report
qg eval --output eval_report.md
```

Report includes: pass rate, avg steps, token usage, duration, breakdown by type/difficulty, failure analysis.

### AI Chat

```bash
qg chat
```

## Detection Rules

| Rule | Severity | Description | Auto-fix |
|------|----------|-------------|----------|
| `SEC001` | ERROR | Hardcoded password | |
| `SEC002` | ERROR | Hardcoded API Key | |
| `SEC004` | ERROR | Dangerous eval() | |
| `STA000` | ERROR | Python syntax error | |
| `STA001` | WARN | Function too long | |
| `CPX001` | WARN | High cyclomatic complexity | |
| `STY*` | INFO | Code style issues | `YES` |

## Commands

| Command | Description |
|---------|-------------|
| `qg scan <path>` | Run full code quality analysis |
| `qg fix <path>` | Auto-fix fixable issues |
| `qg rules --list` | List all rules |
| `qg init` | Generate .guardian.yaml config |
| `qg agent <task>` | Run AI agent for autonomous code review |
| `qg eval` | Run 50-scenario evaluation benchmark |
| `qg chat` | Start interactive AI chat mode |

### Chat Commands

| Command | Description |
|---------|-------------|
| `/scan <path>` | Run analysis |
| `/fix <path>` | Auto-fix |
| `/read <file>` | Read file content for AI |
| `/report <path>` | Generate HTML report |
| `/rules` | List rules |
| `/help` | Show help |

## Report Formats

| Format | Description | Use Case |
|--------|-------------|----------|
| **Terminal** | Direct terminal output | Daily dev |
| **HTML** | Browseable HTML report | CI dashboard |
| **JSON** | Machine-readable JSON | Automation tools |
| **SARIF** | GitHub SARIF format | GitHub integration |
| **Markdown** | Markdown report | Documentation |

## Project Structure

```
qualiguard/
├── src/guardian/
│   ├── cli/          CLI commands
│   ├── checkers/     Analyzers (static/style/security/complexity/dependency)
│   ├── chat/         AI chat mode (REPL + LLM)
│   ├── agent/        Autonomous Agent (Tool-using ReAct loop)
│   ├── eval/         Quantitative eval (50 scenarios + report)
│   ├── reporters/    Report generation (terminal/HTML/JSON/SARIF/Markdown)
│   ├── fixers/       Auto-fix (ruff)
│   ├── rules/        Rule engine + YAML presets
│   ├── core/         Core models (Session/Scheduler/Issue)
│   └── integrations/ CI integrations (GitHub Actions/pre-commit)
├── tests/            26 unit tests + 5 fixture files
├── .env.example      API Key config template
└── pyproject.toml    Project config
```

## CI/CD Integration

```yaml
name: Code Quality Check
on: [push, pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install qualiguard
      - run: qg scan ./src
      - run: qg fix ./src
```

## Tech Stack

- **Language:** Python 3.10+
- **CLI:** Typer (click-based)
- **Code Analysis:** AST, ruff, custom checkers
- **AI Agent:** OpenAI SDK (Function Calling) + ReAct loop
- **Eval System:** 50 standardized scenarios + multi-metric analysis
- **LLM Support:** DeepSeek / Qwen / GLM (domestic models compatible)
- **Testing:** pytest (26 tests)
- **Formatting:** ruff

---

<div align="center">

Made with by echo804

[Report Bug](https://github.com/echo804/QualiGuard/issues)  [Request Feature](https://github.com/echo804/QualiGuard/issues)

</div>
