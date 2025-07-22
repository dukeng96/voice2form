import json
import re
import time
import requests
import demjson3
from typing import Any, Dict

from .prompts import PROMPTS, TODAY, WEEKDAY
from ..settings import get_settings

# You would implement _strip_md_fence and safe_json_parse similar to previous work


def _strip_md_fence(text: str) -> str:
    pattern = r"^```(?:json)?|```$"
    return re.sub(pattern, "", text.strip(), flags=re.MULTILINE)


def safe_json_parse(raw: str, use_llm_fix: bool = True) -> Dict[str, Any]:
    raw = _strip_md_fence(raw)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        try:
            return demjson3.decode(raw)
        except demjson3.JSONDecodeError:
            if not use_llm_fix:
                raise
            fix_prompt = f"Fix JSON:\n{raw}"
            fixed = call_llm(fix_prompt)
            return safe_json_parse(fixed, use_llm_fix=False)


def call_llm(prompt: str, temperature: float = 0.0) -> str:
    cfg = get_settings()
    payload = {"system_prompt": "", "prompt": prompt, "temperature": temperature}
    for attempt in range(3):
        r = requests.post(cfg.llm_endpoint, json=payload, timeout=600)
        if r.ok:
            return r.json()["value"].strip()
        time.sleep(2 ** attempt)
    raise RuntimeError("LLM failed")


def parse_record(use_case: str, text: str, fix_json: bool = True) -> Dict[str, Any]:
    prompt = PROMPTS[use_case].format(input_text=text, current_date=TODAY, current_weekday=WEEKDAY)
    raw = call_llm(prompt)
    return safe_json_parse(raw, use_llm_fix=fix_json)
