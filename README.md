<div align="center">

# 🛡 QualiGuard

> **代码质量卫士 — AI-driven Code Quality CLI**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow?logo=opensourceinitiative)](LICENSE)
[![CI](https://img.shields.io/badge/CI-Passing-228B22?logo=githubactions)](.github/workflows/code-quality.yml)
[![Tests](https://img.shields.io/badge/Tests-26%2F26-228B22?logo=pytest)](tests/)
[![Ruff](https://img.shields.io/badge/Ruff-0.15+-D7FF64?logo=ruff)](https://astral.sh/ruff)
[![PyPI](https://img.shields.io/badge/PyPI-Coming%20Soon-orange?logo=pypi)](https://pypi.org/)

---

</div>

## 🚀 为什么 QualiGuard

| 定位 | 说明 |
|--------|--------|
| 🎯 **定位** | 代码提交前的安全检查门，与 PyCharm 互补 |
| 🔄 **工作流程** | 开发→提交→ CI 自动扫描→拥抱 |
| ✨ **亮点** | AI 对话、一键修复、多格式报告、中文注释 |

---

## 📦 安装

```bash
pip install qualiguard

# 验证安装
qg --help
```

## 🤔 快速上手

### 🔍 CLI 扫描

```bash
# 扫描当前目录
qg scan

# 扫描指定目标
qg scan ./src

# 生成 HTML 报告
qg scan ./src --format html --output report.html
```

### 🔧 自动修复

```bash
qg fix ./src
# 输出: Fixed 60/61 fixable issues.
```

### 💬 AI 对话

```bash
# 首次使用前配置 API Key
cp .env.example .env

# 启动对话
qg chat

qg > 分析一下 app.py
qg > /scan app.py
qg > /fix app.py
```

## 🧰 检测能力 一览

<table>
<thead>
<tr>
  <th>规则</th>
  <th>级别</th>
  <th>检测内容</th>
  <th>可修复</th>
</tr>
</thead>
<tbody>
<tr>
  <td><code>SEC001</code></td>
  <td><span style="color:#e74c3c">❌ ERROR</span></td>
  <td>硬编码密码</td>
  <td></td>
</tr>
<tr>
  <td><code>SEC002</code></td>
  <td><span style="color:#e74c3c">❌ ERROR</span></td>
  <td>硬编码 API Key</td>
  <td></td>
</tr>
<tr>
  <td><code>SEC004</code></td>
  <td><span style="color:#e74c3c">❌ ERROR</span></td>
  <td>危险的 eval()</td>
  <td></td>
</tr>
<tr>
  <td><code>STA000</code></td>
  <td><span style="color:#e74c3c">❌ ERROR</span></td>
  <td>Python 语法错误</td>
  <td></td>
</tr>
<tr>
  <td><code>STA001</code></td>
  <td><span style="color:#f39c12">⚠️ WARN</span></td>
  <td>函数过长</td>
  <td></td>
</tr>
<tr>
  <td><code>CPX001</code></td>
  <td><span style="color:#f39c12">⚠️ WARN</span></td>
  <td>圈复杂度过高</td>
  <td></td>
</tr>
<tr>
  <td><code>STY*</code></td>
  <td><span style="color:#3498db">ℹ️ INFO</span></td>
  <td>代码风格</td>
  <td><code>✅</code></td>
</tr>
</tbody>
</table>

## 💻 命令一览

| 命令 | 功能 |
|------|------|
| `qg scan <path>` | 执行完整的代码质量分析 |
| `qg fix <path>` | 一键自动修复可修复的问题 |
| `qg rules --list` | 列出所有规则 |
| `qg init` | 生成 .guardian.yaml 配置文件 |
| `qg chat` | 进入 AI 对话模式 |

### 🗨 Chat 内建命令

| 命令 | 说明 |
|------|------|
| `/scan <path>` | 执行分析 |
| `/fix <path>` | 自动修复 |
| `/read <file>` | 读取文件内容交给 AI |
| `/report <path>` | 生成 HTML 报告 |
| `/rules` | 列出规则 |
| `/help` | 显示帮助 |

## 📰 报告格式

QualiGuard 支持多种输出格式：

| 格式 | 说明 | 应用场景 |
|------|------|------|
| **Terminal** | 终端直接输出，含中文注释 | 日常开发 |
| **HTML** | 可浏览的 HTML 报告文件 | CI 板杂忘 |
| **JSON** | 机器可读的 JSON 格式 | 自动化工具 |
| **SARIF** | GitHub 专用格式 | GitHub 上查看问题 |
| **Markdown** | Markdown 格式 | 集成到文档 |

## 📚 项目结构

```
qualiguard/
├── src/guardian/
│   ├── cli/          CLI 命令 (扫描/修复/聊天)
│   ├── checkers/     分析器（static/style/security/complexity/dependency）
│   ├── chat/         AI 对话模式 (REPL + LLM)
│   ├── reporters/    报告生成 (terminal/HTML/JSON/SARIF)
│   ├── fixers/       自动修复 (ruff)
│   ├── rules/        规则引擎 + YAML 预设集
│   ├── core/         核心模型 (Session/Scheduler/Issue)
│   └── integrations/ CI 集成 (GitHub Actions/pre-commit)
├── tests/         26 个单元测试
├── .env.example   API Key 配置模板
└── pyproject.toml 项目配置
```

## 🔄 CI/CD 集成

QualiGuard 可以集成到 GitHub Actions 工作流程中，每次提交自动扫描：

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

## 🧱 技术栈

- **语言:** Python 3.10+
- **CLI:** Typer (click-based)
- **代码分析:** AST, ruff, custom checkers
- **AI:** OpenAI / Anthropic SDK (DeepSeek compatible)
- **测试:** pytest (26 tests)
- **格式检查:** ruff

---

<div align="center">

Made with ❤️ by echo804

[Report Bug](https://github.com/echo804/QualiGuard/issues) · [Request Feature](https://github.com/echo804/QualiGuard/issues)

</div>