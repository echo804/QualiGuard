# QualiGuard 🛡

> AI-powered code quality analysis CLI— scan, detect, fix.

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()

## 快速开始

```bash
pip install qualiguard

# 扫描当前目录
qg scan

# 扫描指定文件
qg scan ./src/main.py

# 自动修复
qg fix ./src

# 启动交互式 AI 对话
qg chat
```

## Chat Mode (AI 对话)

QualiGuard Chat 支持与 AI 模型对话，分析代码问题。

```bash
# 首次使用前配置 API Key
cp .env.example .env
# 编辑 .env 填入你的 DeepSeek / OpenAI API Key

# 启动对话
qg chat
```

### 命令说明

| 命令 | 说明 |
|------|------|
| `/scan <path>` | 执行代码质量分析 |
| `/fix <path>` | 自动修复可修复的问题 |
| `/read <file>` | 读取文件内容交给 AI 分析 |
| `/report <path>` | 生成 HTML 报告 |
| `/rules` | 列出所有规则 |
| `/help` | 显示帮助 |

## 检测能力

| 规则 | 级别 | 说明 |
|------|------|------|
| `STA000` | ❌ ERROR | Python 语法错误 |
| `SEC001` | ❌ ERROR | 硬编码密码 |
| `SEC002` | ❌ ERROR | 硬编码 API Key |
| `SEC004` | ❌ ERROR | 危险的 eval() 调用 |
| `STA001` | ⚠️ WARNING | 函数过长 |
| `CPX001` | ⚠️ WARNING | 圈复杂度过高 |

## Features

| Feature | Description |
|---------|-------------|
| 静态分析 | AST 语法树检查 |
| 代码风格 | 基于 ruff 的样式检查 |
| 安全检查 | 硬编码密钥eval()等危险模式 |
| 复杂度分析 | 圈复杂度测量 |
| 依赖审计 | 已知漏洞匹配 |
| 多格式报告 | Terminal/JSON/HTML/Markdown/SARIF |
| 自动修复 | 一键修复风格问题 |
| AI 对话 | 与 LLM 交互分析代码 |
| 中文注释 | 每类问题附有中文原因说明和修复建议 |

## License

MIT