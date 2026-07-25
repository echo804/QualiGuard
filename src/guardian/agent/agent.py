from __future__ import annotations
import os
import json
import time
from dataclasses import dataclass, field
from typing import Optional

from guardian.agent.tools import get_tool_schemas, dispatch_tool_call


# ---------------------------------------------------------------------------
# Agent configuration
# ---------------------------------------------------------------------------

@dataclass
class AgentConfig:
    model: str = "deepseek-chat"
    api_key: str = ""
    base_url: str = ""
    max_steps: int = 10
    temperature: float = 0.3
    max_tokens: int = 4096


@dataclass
class AgentTrace:
    """Complete trace of a single agent run."""
    steps: list[dict] = field(default_factory=list)
    total_tokens: int = 0
    total_duration_ms: int = 0
    success: bool = False
    final_answer: str = ""

    def to_dict(self) -> dict:
        return {
            "steps": self.steps,
            "total_tokens": self.total_tokens,
            "total_duration_ms": self.total_duration_ms,
            "success": self.success,
            "final_answer": self.final_answer,
        }


# ===================================================================
# LLM caller with tool support (OpenAI-compatible API)
# ===================================================================

def _load_config() -> AgentConfig:
    """Load agent config from environment (same .env pattern as chat/llm.py)."""
    from guardian.chat.llm import _find_config  # reuse existing env loader
    api_key, base_url, model = _find_config()
    return AgentConfig(
        model=model or "deepseek-chat",
        api_key=api_key or "",
        base_url=base_url or "",
    )


def _call_llm(
    messages: list[dict],
    tools: list[dict] | None = None,
) -> dict:
    """Call OpenAI-compatible LLM and return the full response dict.

    Returns {"role": ..., "content": ..., "tool_calls": [...]} or raises.
    """
    from openai import OpenAI

    cfg = _load_config()
    if not cfg.api_key:
        raise RuntimeError("LLM API key not configured. Set DEEPSEEK_API_KEY or OPENAI_API_KEY in .env")

    client = OpenAI(api_key=cfg.api_key, base_url=cfg.base_url or None)

    kwargs = dict(
        model=cfg.model,
        messages=messages,
        temperature=cfg.temperature,
        max_tokens=cfg.max_tokens,
    )
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"

    response = client.chat.completions.create(**kwargs)

    choice = response.choices[0]
    msg = choice.message

    result = {
        "role": msg.role,
        "content": msg.content or "",
        "tool_calls": [],
    }

    # Parse tool calls
    if msg.tool_calls:
        for tc in msg.tool_calls:
            result["tool_calls"].append({
                "id": tc.id,
                "type": tc.type,
                "function": {
                    "name": tc.function.name,
                    "arguments": tc.function.arguments,
                },
            })

    return result, response.usage.total_tokens if response.usage else 0


# ===================================================================
# Main agent loop
# ===================================================================

SYSTEM_PROMPT = (
    "You are an AI code quality assistant built into QualiGuard CLI. "
    "You can scan code, fix issues, read files, search code, generate reports, and explain rules.\n\n"
    "Rules:\n"
    "1. Always think step by step. First understand the task, then pick the right tool.\n"
    "2. After each tool result, decide if the task is complete or needs more steps.\n"
    "3. When done, summarize what you did and the results clearly.\n"
    "4. If you encounter errors, try alternative approaches (e.g., check if path exists).\n"
    "5. You have a maximum of 10 steps. Be efficient.\n"
    "6. Use scan_code with a rules filter (e.g. 'SEC') when only specific rule types are needed.\n"
    "7. Always prefer to verify results (e.g. re-scan after fixing)."
)


def run_agent(
    user_task: str,
    max_steps: int | None = None,
    trace: bool = True,
) -> str | dict:
    """Run the agent on a user task.

    Args:
        user_task: Natural language task description.
        max_steps: Override max steps (default from config, 10).
        trace: If True, return a dict with {"answer": ..., "trace": AgentTrace}.
               If False, return just the answer string.

    Returns:
        String or dict depending on trace parameter.
    """
    cfg = _load_config()
    if max_steps is not None:
        cfg.max_steps = max_steps

    messages: list[dict] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_task},
    ]
    tools = get_tool_schemas()

    agent_trace = AgentTrace()
    start_time = time.time()
    total_tokens = 0

    for step in range(1, cfg.max_steps + 1):
        step_start = time.time()

        try:
            response_msg, tokens = _call_llm(messages, tools=tools)
            total_tokens += tokens
        except Exception as exc:
            err = f"[AgentError] LLM call failed at step {step}: {exc}"
            return _finish(err, agent_trace, start_time, total_tokens, trace, success=False)

        tool_calls = response_msg.get("tool_calls", [])
        content = response_msg.get("content", "")

        step_record = {
            "step": step,
            "content": content[:200] if content else "",
            "tool_calls": [],
            "duration_ms": int((time.time() - step_start) * 1000),
        }

        # --- Case 1: No tool calls → final answer ---
        if not tool_calls:
            final = content or "Task complete."
            if trace:
                agent_trace.steps.append(step_record)
                return _finish(final, agent_trace, start_time, total_tokens, trace, success=True)
            return final

        # --- Case 2: Execute tool calls ---
        messages.append({"role": "assistant", "content": content, "tool_calls": [
            {"id": tc["id"], "type": tc["type"], "function": tc["function"]}
            for tc in tool_calls
        ]})

        for tc in tool_calls:
            fn_name = tc["function"]["name"]
            fn_args = tc["function"]["arguments"]

            tool_start = time.time()
            result = dispatch_tool_call(fn_name, fn_args)
            tool_duration = int((time.time() - tool_start) * 1000)

            step_record["tool_calls"].append({
                "name": fn_name,
                "arguments": fn_args,
                "result_preview": result[:200],
                "duration_ms": tool_duration,
            })

            messages.append({
                "role": "tool",
                "tool_call_id": tc["id"],
                "content": result,
            })

        agent_trace.steps.append(step_record)

    # --- Max steps reached ---
    msg = f"Reached maximum of {cfg.max_steps} steps without a final answer."
    return _finish(msg, agent_trace, start_time, total_tokens, trace, success=False)


def _finish(
    answer: str,
    trace_data: AgentTrace,
    start_time: float,
    tokens: int,
    return_trace: bool,
    success: bool,
) -> str | dict:
    """Wrap up and return result."""
    trace_data.success = success
    trace_data.total_tokens = tokens
    trace_data.total_duration_ms = int((time.time() - start_time) * 1000)
    trace_data.final_answer = answer

    if return_trace:
        return {"answer": answer, "trace": trace_data}
    return answer
