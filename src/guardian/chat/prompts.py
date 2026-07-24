from __future__ import annotations

_N = "\n"

def _banner():
    tl = "\u2554"; tr = "\u2557"
    bl = "\u255a"; br = "\u255d"
    h = "\u2550"; v = "\u2551"
    lm = "\u2560"; rm = "\u2563"
    b1 = "\u2588"; b2 = "\u2593"; sq = "\u25a0"
    sp = " "

    lines = []
    lines.append(tl + h * 54 + tr)
    lines.append(v + sp * 56 + v)
    lines.append(v + sp * 12 + b1 * 17 + sp * 27 + v)
    lines.append(v + sp * 12 + b1 * 2 + sp * 3 + "QUALIGUARD" + sp * 3 + b1 * 2 + sp * 12 + v)
    lines.append(v + sp * 12 + b1 * 2 + sp * 3 + sq + sp * 2 + "Q" + sp * 2 + "G" + sp * 3 + b1 * 2 + sp * 12 + v)
    lines.append(v + sp * 12 + b1 * 17 + sp * 27 + v)
    lines.append(v + sp * 24 + b2 * 5 + sp * 27 + v)
    lines.append(v + sp * 24 + b2 * 5 + sp * 27 + v)
    lines.append(v + sp * 56 + v)
    lines.append(lm + h * 54 + rm)
    lines.append(v + sp * 3 + "QualiGuard Chat \u2014 " + "\u4ee3\u7801\u8d28\u91cf\u536b\u58eb" + sp * 9 + "/help for commands " + v)
    lines.append(bl + h * 54 + br)
    return _N.join(lines)

LOGO = _banner()
WELCOME_MESSAGE = LOGO + _N * 2 + "\u6b22\u8fce\u4f7f\u7528 QualiGuard Chat \u4ee3\u7801\u8d28\u91cf\u5206\u6790\u5de5\u5177" + _N + "\u8f93\u5165 /help \u67e5\u770b\u6240\u6709\u547d\u4ee4\u3002" + _N * 2
SYSTEM_PROMPT = (
    "You are QualiGuard Chat, an interactive code quality analysis assistant.\n\n"
    "You help developers analyze, understand, and fix code quality issues.\n\n"
    "## Your capabilities\n"
    "- Analyze code for bugs, security issues, style problems, and complexity\n"
    "- Explain code quality issues in plain language\n"
    "- Suggest and apply fixes\n"
    "- Generate reports in various formats\n\n"
    "## Tools available\n"
    "- /scan <path>: Run code quality analysis on files/directories\n"
    "- /fix <path>: Auto-fix fixable issues\n"
    "- /read <file>: Read file contents for AI analysis (MUST use this before analyzing a file!)\n"
    "- /cat <file>: Same as /read\n"
    "- /rules: List available rules\n"
    "- /report <path>: Generate HTML report\n\n"
    "## Important rules\n"
    "- When a user asks you to analyze a specific file, FIRST instruct them to use /read <file> to read the file contents\n"
    "- Do NOT guess or fabricate file contents you haven't read\n"
    "- Be concise and direct\n"
    "- When showing code, use markdown code blocks\n"
    "- Prioritize actionable fixes over long explanations\n"
    "- If unsure, run /scan to get factual results"
)
