from datetime import date
from typing import Dict

_WEEKDAY = ["Thứ hai", "Thứ ba", "Thứ tư", "Thứ năm", "Thứ sáu", "Thứ bảy", "Chủ nhật"]
TODAY = date.today().isoformat()
WEEKDAY = _WEEKDAY[date.today().weekday()]

VAT_TU = r"""\u2026{input_text}\u2026"""
CHUNG_TU = r"""\u2026{input_text}\u2026"""
CONG_VIEC = r"""\u2026{input_text}\u2026"""

PROMPTS: Dict[str, str] = {
    "vat_tu": VAT_TU,
    "chung_tu": CHUNG_TU,
    "cong_viec": CONG_VIEC,
}
