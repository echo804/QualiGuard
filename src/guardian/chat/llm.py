from __future__ import annotations
import os
from pathlib import Path


def _load_env():
    env_path = Path(__file__).resolve().parent.parent.parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key = key.strip()
            val = val.strip().strip(chr(34)).strip(chr(39))
            os.environ[key] = val


def _find_config():
    _load_env()
    base_url = os.environ.get("ANTHROPIC_BASE_URL") or os.environ.get("OPENAI_BASE_URL") or ""
    api_key = os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("OPENAI_API_KEY")
    api_key = api_key or os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("LLM_API_KEY")
    model = os.environ.get("MODEL_ID") or os.environ.get("LLM_MODEL") or "gpt-4o-mini"
    return api_key, base_url, model


def check_llm_available() -> bool:
    api_key, base_url, model = _find_config()
    return bool(api_key) and bool(model)


def get_setup_guide() -> str:
    api_key, base_url, model = _find_config()
    parts = ["LLM Configuration:", ""]
    parts.append("  API Key: " + ("set" if api_key else "not set"))
    parts.append("  Base URL: " + (base_url if base_url else "default"))
    parts.append("  Model: " + model)
    parts.append("")
    if api_key and model:
        parts.append("  Ready. Type your question to chat.")
    else:
        parts.append("  Set API key in .env file.")
    return chr(10).join(parts)


def get_llm_response(messages: list[dict]) -> str | None:
    api_key, base_url, model = _find_config()
    if not api_key:
        return None
    # Try OpenAI-compatible API (works for DeepSeek, OpenAI, Moonshot v1)
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url=base_url or None)
        response = client.chat.completions.create(model=model, messages=messages, max_tokens=4096, temperature=0.3)
        return response.choices[0].message.content
    except Exception:
        pass
    # Fallback: Anthropic SDK (for Anthropic-compatible proxies)
    try:
        from anthropic import Anthropic
        anth_key = os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("OPENAI_API_KEY")
        if anth_key and base_url:
            client = Anthropic(api_key=anth_key, base_url=base_url)
            sys_msg = ""
            for m in messages:
                if m["role"] == "system":
                    sys_msg = m["content"]
            conv = [m for m in messages if m["role"] != "system"]
            r = client.messages.create(model=model, max_tokens=4096, messages=conv, system=sys_msg)
            if r.content:
                return r.content[0].text
    except ImportError:
        pass
    except Exception:
        pass
    return None