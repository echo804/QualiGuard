<div align="center">

# 馃洡 QualiGuard

> **浠ｇ爜璐ㄩ噺鍗＋ 鈥?AI-driven Code Quality CLI**

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

## 馃殌 涓轰粈涔?QualiGuard

| 瀹氫綅 | 璇存槑 |
|--------|--------|
| 馃幆 **瀹氫綅** | 浠ｇ爜鎻愪氦鍓嶇殑瀹夊叏妫€鏌ラ棬锛屼笌 PyCharm 浜掕ˉ |
| 馃攧 **宸ヤ綔娴佺▼** | 寮€鍙戔啋鎻愪氦鈫扐I 鑷姩鎵弿鈫掓嫢鎶?|
| 鈭?**浜偣** | Tool-using Agent銆侀噺鍖栬瘎娴嬨€丄I 瀵硅瘽銆佷竴閿慨澶嶃€佸鏍煎紡鎶ュ憡 |

---

## 馃摝 瀹夎

```bash
pip install qualiguard

# 濡傞渶 Agent 鍜?Eval 鍔熻兘锛堥渶瑕丳PI Key锛?
pip install qualiguard[chat]

# 楠岃瘉瀹夎
qg --help
```

## 鈿狅笍 蹇€熶笂鎵?

### 馃摶 CLI 鎵弿

```bash
# 鎵弿褰撳墠鐩綍
qg scan

# 鎵弿鎸囧畾鐩爣
qg scan ./src

# 鐢熸垚 HTML 鎶ュ憡
qg scan ./src --format html --output report.html
```

### 馃敡 鑷姩淇

```bash
qg fix ./src
# 杈撳嚭: Fixed 60/61 fixable issues.
```

### 馃 AI Agent锛堟柊澶烇級

灏?QualiGuard 鐨?6 椤规牳蹇冭兘鍔涘皝瑁呬负 LLM 鍙皟鐢ㄧ殑宸ュ叿锛屾敮鎸佽嚜鐒辫瑷€椹卞姩銆佽嚜涓昏鍒掋€佸姝ユ墽琛岀殑鏅鸿兘浠ｇ爜瀹℃煡宸ヤ綔娴併€?

```bash
# 閰嶇疆 API Key锛堟敮鎸?DeepSeek / OpenAI 鍏煎鎺ュ彛锛?
cp .env.example .env

# 鍗曟锛氭壂鎻忓苟鍒嗘瀽
qg agent "鎵弿 tests/fixtures/ 鐩綍锛屾湁鍝簺瀹夊叏闂锛?"

# 澶氭锛氭壂鎻忊啋淇鈫掗獙璇?
qg agent "鎵弿 tests/fixtures/bad_python.py 骞朵慨澶?"

# 甯﹁缁?Trace 鏃ュ織
qg agent --verbose "璇诲彇 insecure_code.py 骞惰В閲奢EC001 瑙勫垯"

# 澶嶆潅浠诲姟锛氭壂鎻忊啋鍒嗘瀽鈫掔敓鎴愭姤鍛?
qg agent "鎵弿褰撳墠鐩綍锛岀敓鎴怬TML 鎶ュ憡"
```

### 馃摀 閲忓寲璇勬祴锛堟柊澶烇級

50 涓爣鍑嗗寲鍦烘櫙 脳 6 绉嶇被鍨?脳 3 绉嶉毦搴︼紝鑷姩璺戝垎鐢熸垚閲忓寲鎶ュ憡銆?

```bash
# 蹇€熻窇 5 涓畨鍏ㄥ満鏅?
qg eval --scenarios 5 --type security

# 鎸夐毦搴︾瓫閫?
qg eval --scenarios 10 --severity hard

# 鍏ㄩ儴璺戝畬骞朵繚瀛樻姤鍛?
qg eval --output eval_report.md
```

璇勬祴鎶ュ憡鍖呭惈锛氶€氳繃鐜囥€佸钩鍧囨鏁般€乀oken 娑堣€椼€佽€楁椂銆佸悇绫诲瀷/闅惧害缁嗗垎銆佸け璐ュ満鏅垎鏋愩€?

### 馃挰 AI 瀵硅瘽

```bash
# 鍚姩浜掍簰寮忓璇?
qg chat
```

## 馃幆 妫€娴嬭兘鍔?涓€瑙?

<table>
<thead>
<tr>
  <th>瑙勫垯</th>
  <th>绾у埆</th>
  <th>妫€娴嬪唴瀹?</th>
  <th>鍙慨澶?</th>
</tr>
</thead>
<tbody>
<tr>
  <td><code>SEC001</code></td>
  <td><span style="color:#e74c3c">馃敶 ERROR</span></td>
  <td>纭紪鐮佸瘑鐮?</td>
  <td></td>
</tr>
<tr>
  <td><code>SEC002</code></td>
  <td><span style="color:#e74c3c">馃敶 ERROR</span></td>
  <td>纭紪鐮?API Key</td>
  <td></td>
</tr>
<tr>
  <td><code>SEC004</code></td>
  <td><span style="color:#e74c3c">馃敶 ERROR</span></td>
  <td>鍗遍櫓鐨?eval()</td>
  <td></td>
</tr>
<tr>
  <td><code>STA000</code></td>
  <td><span style="color:#e74c3c">馃敶 ERROR</span></td>
  <td>Python 璇硶閿欒</td>
  <td></td>
</tr>
<tr>
  <td><code>STA001</code></td>
  <td><span style="color:#f39c12">鈿狅笍 WARN</span></td>
  <td>鍑芥暟杩囬暱</td>
  <td></td>
</tr>
<tr>
  <td><code>CPX001</code></td>
  <td><span style="color:#f39c12">鈿狅笍 WARN</span></td>
  <td>鍦堝鏉傚害杩囬珮</td>
  <td></td>
</tr>
<tr>
  <td><code>STY*</code></td>
  <td><span style="color:#3498db">鈩癸笍 INFO</span></td>
  <td>浠ｇ爜椋庢牸</td>
  <td><code>鈭?</code></td>
</tr>
</tbody>
</table>

## 馃捇 鍛戒护涓€瑙?

| 鍛戒护 | 鍔熻兘 |
|------|-------|
| `qg scan <path>` | 鎵ц瀹屾暣鐨勪唬鐮佽川閲忓垎鏋?|
| `qg fix <path>` | 涓€閿嚜鍔ㄤ慨澶嶅彲淇鐨勯棶棰?|
| `qg rules --list` | 鍒楀嚭鎵€鏈夎鍒?|
| `qg init` | 鐢熸垚 .guardian.yaml 閰嶇疆鏂囦欢 |
| `qg agent <task>` | 鑷劧璇█椹卞姩 Agent 鑷富鎵ц瀹℃煡浠诲姟 |
| `qg eval` | 杩愯 50 涓満鏅殑閲忓寲璇勬祴骞剁敓鎴愭姤鍛?|
| `qg chat` | 杩涘叆 AI 瀵硅瘽妯″紡 |

### 馃棬 Chat 鍐呭缓鍛戒护

| 鍛戒护 | 璇存槑 |
|------|------|
| `/scan <path>` | 鎵ц鍒嗘瀽 |
| `/fix <path>` | 鑷姩淇 |
| `/read <file>` | 璇诲彇鏂囦欢鍐呭浜ょ粰 AI |
| `/report <path>` | 鐢熸垚 HTML 鎶ュ憡 |
| `/rules` | 鍒楀嚭瑙勫垯 |
| `/help` | 鏄剧ず甯姪 |

## 馃摪 鎶ュ憡鏍煎紡

QualiGuard 鏀寔澶氱杈撳嚭鏍煎紡锛?

| 鏍煎紡 | 璇存槑 | 搴旂敤鍦烘櫙 |
|------|------|---------|
| **Terminal** | 缁堢鐩存帴杈撳嚭锛屽惈涓枃娉ㄩ噴 | 鏃ュ父寮€鍙?|
| **HTML** | 鍙祻瑙堢殑 HTML 鎶ュ憡鏂囦欢 | CI 闈㈡澘 |
| **JSON** | 鏈哄櫒鍙鐨?JSON 鏍煎紡 | 鑷姩鍖栧伐鍏?|
| **SARIF** | GitHub 涓撶敤鏍煎紡 | GitHub 涓婃煡鐪嬮棶棰?|
| **Markdown** | Markdown 鏍煎紡 | 闆嗘垚鍒版枃妗?|

## 馃摎 椤圭洰缁撴瀯

```
qualiguard/
鈹溾攢鈹€ src/guardian/
鈹?  鈹溾攢鈹€ cli/          CLI 鍛戒护
鈹?  鈹溾攢鈹€ checkers/     鍒嗘瀽鍣紙static/style/security/complexity/dependency锛?
鈹?  鈹溾攢鈹€ chat/         AI 瀵硅瘽妯″紡 (REPL + LLM)
鈹?  鈹溾攢鈹€ agent/        馃 鑷富 Agent锛圱ool-using ReAct 寰幆锛?
鈹?  鈹溾攢鈹€ eval/         馃摀 閲忓寲璇勬祴锛?0 涓満鏅?+ 鎶ュ憡鐢熸垚锛?
鈹?  鈹溾攢鈹€ reporters/    鎶ュ憡鐢熸垚 (terminal/HTML/JSON/SARIF/Markdown)
鈹?  鈹溾攢鈹€ fixers/       鑷姩淇 (ruff)
鈹?  鈹溾攢鈹€ rules/        瑙勫垯寮曟搸 + YAML 棰勮闆?
鈹?  鈹溾攢鈹€ core/         鏍稿績妯″瀷 (Session/Scheduler/Issue)
鈹?  鈹斺攢鈹€ integrations/ CI 闆嗘垚 (GitHub Actions/pre-commit)
鈹溾攢鈹€ tests/            26 涓崟鍏冩祴璇?+ 5 涓す鍏锋枃浠?
鈹溾攢鈹€ .env.example       API Key 閰嶇疆妯℃澘
鈹斺攢鈹€ pyproject.toml     椤圭洰閰嶇疆
```

## 馃攧 CI/CD 闆嗘垚

QualiGuard 鍙互闆嗘垚鍒?GitHub Actions 宸ヤ綔娴佷腑锛屾瘡娆℃彁浜よ嚜鍔ㄦ壂鎻忥細

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

## 馃Ф 鎶€鏈爤

- **璇█:** Python 3.10+
- **CLI:** Typer (click-based)
- **浠ｇ爜鍒嗘瀽:** AST, ruff, custom checkers
- **AI Agent:** OpenAI SDK (Function Calling) + ReAct 寰幆
- **璇勬祴绯荤粺:** 50 涓爣鍑嗗寲鍦烘櫙 + 澶氱淮鎸囨爣璁＄畻 + Markdown 鎶ュ憡
- **AI:** DeepSeek / Qwen / GLM 绛夊浗浜фā鍨嬪吋瀹?
- **娴嬭瘯:** pytest (26 tests)
- **鏍煎紡妫€鏌?** ruff

---

<div align="center">

Made with 鈾ワ笍 by echo804

[Report Bug](https://github.com/echo804/QualiGuard/issues) 路 [Request Feature](https://github.com/echo804/QualiGuard/issues)

</div>
