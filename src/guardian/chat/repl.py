from __future__ import annotations
import sys, os, re, glob

from guardian.chat.commands import COMMANDS
from guardian.chat.prompts import WELCOME_MESSAGE, SYSTEM_PROMPT
from guardian.chat.llm import get_llm_response, check_llm_available, get_setup_guide


def _auto_read_file(user_input: str) -> str | None:
    keywords = [chr(0x5206)+chr(0x6790), chr(0x68c0)+chr(0x67e5),
                chr(0x770b)+chr(0x770b), chr(0x8bfb)+chr(0x53d6),
                chr(0x6253)+chr(0x5f00), chr(0x6ce8)+chr(0x5165),
                "analyze", "check", "read", "inspect", "review"]
    if not any(kw in user_input.lower() for kw in keywords):
        return None

    cwd = os.getcwd()
    parts = user_input.replace(chr(0xff0c), " ").replace(chr(0x3002), " ").split()
    for word in parts:
        w = word.strip(".,;:\"'\u300c\u300d\u300a\u300b")
        if not w or "." not in w:
            continue
        for candidate in [w, os.path.join(cwd, w), os.path.join(cwd, os.path.basename(w))]:
            ap = os.path.abspath(candidate)
            if os.path.isfile(ap):
                try:
                    with open(ap, encoding="utf-8", errors="replace") as fh:
                        content = fh.read()
                    return "--- " + ap + " (" + str(content.count(chr(10)) + 1) + " lines) ---\n" + content + "\n--- end ---"
                except Exception:
                    continue
        ext = w.split(".")[-1]
        for f in glob.glob(os.path.join(cwd, "*." + ext)):
            fname = os.path.basename(f)
            if w in fname or fname in w:
                try:
                    with open(f, encoding="utf-8", errors="replace") as fh:
                        content = fh.read()
                    return "--- " + f + " (" + str(content.count(chr(10)) + 1) + " lines) ---\n" + content + "\n--- end ---"
                except Exception:
                    continue
    return None

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def chat_loop():
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    llm_available = check_llm_available()

    sys.stdout.write(WELCOME_MESSAGE)
    if llm_available:
        sys.stdout.write("  [LLM " + chr(0x6a21) + chr(0x5f0f) + "] AI " + chr(0x9a71) + chr(0x52a8) + chr(0x7684) + chr(0x4ee3) + chr(0x7801) + chr(0x8d28) + chr(0x91cf) + chr(0x5206) + chr(0x6790) + chr(0x5bf9) + chr(0x8bdd) + chr(0x3002) + chr(0x8f93) + chr(0x5165) + chr(0x95ee) + chr(0x9898) + chr(0x6216) + chr(0x4f7f) + chr(0x7528) + " /" + chr(0x547d) + chr(0x4ee4) + chr(0x3002) + "\n\n")
    else:
        sys.stdout.write("  [" + chr(0x5de5) + chr(0x5177) + chr(0x6a21) + chr(0x5f0f) + "] " + chr(0x672a) + chr(0x914d) + chr(0x7f6e) + " API " + chr(0x5bc6) + chr(0x94a5) + chr(0x3002) + "\n\n")
        sys.stdout.write(get_setup_guide() + "\n\n")
    sys.stdout.flush()

    while True:
        try:
            sys.stdout.write(chr(0x1b) + "[36mqg > " + chr(0x1b) + "[0m")
            sys.stdout.flush()
            user_input = sys.stdin.readline()
        except (EOFError, KeyboardInterrupt):
            sys.stdout.write(chr(10))
            break

        if not user_input:
            break

        user_input = user_input.strip()
        if not user_input:
            continue

        if user_input.startswith("/"):
            cmd_parts = user_input.split(None, 1)
            cmd_name = cmd_parts[0].lower()
            cmd_args = cmd_parts[1] if len(cmd_parts) > 1 else ""

            if cmd_name in COMMANDS:
                result = COMMANDS[cmd_name](cmd_args)
                if result == "__CLEAR__":
                    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                    sys.stdout.write(chr(10) + "  " + chr(0x804a) + chr(0x5929) + chr(0x5386) + chr(0x53f2) + chr(0x5df2) + chr(0x6e05) + chr(0x9664) + chr(0x3002) + chr(10) + chr(10))
                elif result == "__EXIT__":
                    sys.stdout.write(chr(10) + "  " + chr(0x518d) + chr(0x89c1) + chr(0xff01) + chr(10))
                    break
                else:
                    sys.stdout.write(chr(10) + result + chr(10) + chr(10))
                    messages.append({"role": "user", "content": user_input})
                    messages.append({"role": "assistant", "content": result})
            else:
                sys.stdout.write("  " + chr(0x672a) + chr(0x77e5) + chr(0x547d) + chr(0x4ee4) + ": " + cmd_name + chr(10))
                sys.stdout.write("  " + chr(0x8f93) + chr(0x5165) + " /help " + chr(0x67e5) + chr(0x770b) + chr(0x53ef) + chr(0x7528) + chr(0x547d) + chr(0x4ee4) + chr(0x3002) + chr(10) + chr(10))
            sys.stdout.flush()
            continue

        file_content = _auto_read_file(user_input)
        messages.append({"role": "user", "content": user_input})

        if file_content:
            messages.append({"role": "user", "content": "(Auto-read file contents for analysis)\n" + file_content})

        if llm_available:
            sys.stdout.write(chr(10) + "  " + chr(0x6b63) + chr(0x5728) + chr(0x601d) + chr(0x8003) + "..." + chr(10) + chr(10))
            sys.stdout.flush()
            response = get_llm_response(messages)
            if response:
                sys.stdout.write(response + chr(10) + chr(10))
                messages.append({"role": "assistant", "content": response})
            else:
                sys.stdout.write("  LLM " + chr(0x8c03) + chr(0x7528) + chr(0x5931) + chr(0x8d25) + chr(0x3002) + chr(0x8bf7) + chr(0x68c0) + chr(0x67e5) + chr(0x914d) + chr(0x7f6e) + chr(0xff1a) + chr(10) + chr(10))
                sys.stdout.write(get_setup_guide() + chr(10) + chr(10))
                sys.stdout.write("  " + chr(0x6216) + chr(0x76f4) + chr(0x63a5) + chr(0x4f7f) + chr(0x7528) + " /" + chr(0x547d) + chr(0x4ee4) + chr(0x3002) + chr(10) + chr(10))
        else:
            sys.stdout.write(chr(10) + "  " + chr(0x672a) + chr(0x914d) + chr(0x7f6e) + " LLM" + chr(0x3002) + chr(0x8bf7) + chr(0x4f7f) + chr(0x7528) + " /" + chr(0x547d) + chr(0x4ee4) + chr(0x6216) + chr(0x8bbe) + chr(0x7f6e) + " API " + chr(0x5bc6) + chr(0x94a5) + chr(0xff1a) + chr(10) + chr(10))
            sys.stdout.write(get_setup_guide() + chr(10) + chr(10))
        sys.stdout.flush()
