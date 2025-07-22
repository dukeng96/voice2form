import aiohttp
from ..config import load_config


async def speech_to_text(filepath: str) -> str:
    cfg = load_config()
    async with aiohttp.ClientSession() as sess:
        with open(filepath, "rb") as f:
            data = f.read()
        async with sess.post(cfg["stt_endpoint"], data=data, headers={"Content-Type": "audio/wav"}) as resp:
            js = await resp.json()
    return js.get("text", "")
