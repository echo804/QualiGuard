from __future__ import annotations
import typer


def chat():
    """Start interactive chat mode."""
    from guardian.chat.repl import chat_loop
    chat_loop()
