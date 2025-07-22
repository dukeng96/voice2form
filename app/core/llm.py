import json
import re
import time
import requests
import demjson3
from typing import Any, Dict

from .prompts import PROMPTS, TODAY, TODAY_WEEKDAY, FIX_JSON_PROMPT
from ..config import load_config

# You would implement _strip_md_fence and safe_json_parse similar to previous work


_MD_FENCE_RE = re.compile(r"^\s*```[a-zA-Z0-9]*\s*|\s*```\s*$")

def _strip_md_fence(text: str) -> str:
    """Remove leading/trailing ```... fences (with optional language tag)."""
    # find first line fence
    text = _MD_FENCE_RE.sub("", text, count=1)
    # remove trailing fence (greedy from the end)
    text = _MD_FENCE_RE.sub("", text[::-1], count=1)[::-1]
    return text

def escape_newlines_in_string_literals(text: str) -> str:
    def _esc(m):
        inner = m.group(0)[1:-1].replace("\n", "\\n")
        return f'"{inner}"'
    return re.sub(r'"(.*?)"', _esc, text, flags=re.DOTALL)

def safe_json_parse(text: str, use_llm_fix: bool = True):
    """Parse JSON that may be wrapped in markdown fences / bad quotes / newlines."""
    # 1) strip ```json ... ``` block
    text = _strip_md_fence(text)

    # 2) try strict json
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # 3) quick-fix common issues: ' -> ", raw newlines in strings
        text_fixed = re.sub(r"(?<!\\)'", '"', text)           # unescaped single quotes
        text_fixed = escape_newlines_in_string_literals(text_fixed)
        try:
            return demjson3.decode(text_fixed)
        except Exception as e2:
            print("JSON parse failed: %s\nRaw:\n%s", e2, text)
            # 3) use llm fix
            if use_llm_fix:
                print("Attempting to repair json with LLM")
                try:
                    patched = call_llm(FIX_JSON_PROMPT.format(bad_json=text_fixed, json_bug=e2))
                    cleaned = _strip_md_fence(patched).strip()
                    return json.loads(cleaned)
                except Exception as e:
                    print("JSON repaired via LLM failed: %s\nRaw JSON:\n%s", e, text)

        return {}


def call_llm(
    prompt: str,
    temperature: float = 0.6,
    retry: int = 3,
    top_k: int = 20,
    top_p: float = 0.95,
    min_p: float = 0.0,
    max_new_tokens: int = 2048,
    think: bool = False,
) -> str:
    """
    • Automatic retry with exponential back-off (1 s, 2 s, 4 s …).
    • Returns raw text from `response["value"]`.
    """

    payload = {
        "system_prompt": "",
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_new_tokens,
        "top_k": top_k,
        "top_p": top_p,
        "min_p": min_p,
        "extra_body": {
            "chat_template_kwargs": {
                "enable_thinking": bool(think)
            }
        },
    }

    cfg = load_config()
    headers = {"Content-Type": "application/json"}

    for attempt in range(retry):
        try:
            resp = requests.post(cfg["llm_endpoint"], headers=headers,
                                 json=payload, timeout=600)

            if resp.status_code != 200:
                print("LLM HTTP %s (try %d)", resp.status_code, attempt + 1)
                raise RuntimeError

            raw_text = resp.json().get("value", "")
            if not raw_text:
                print("Empty LLM response (try %d)", attempt + 1)
                raise RuntimeError

            return raw_text.strip()

        except Exception as e:
            print("LLM error %s (try %d)", e, attempt + 1)
            time.sleep(2 ** attempt)          # 1s, 2s, 4s …

    raise RuntimeError("LLM failed after retries")


def parse_record(use_case: str, text: str, fix_json: bool = True) -> Dict[str, Any]:
    prompt = PROMPTS[use_case].format(input_text=text, current_date=TODAY, current_weekday=TODAY_WEEKDAY)
    raw = call_llm(prompt)
    return safe_json_parse(raw, use_llm_fix=fix_json)
