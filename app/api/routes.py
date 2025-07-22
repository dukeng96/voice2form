import uuid
import os
import logging
from fastapi import APIRouter, UploadFile, File, Form, Depends
from ..core.stt import speech_to_text
from ..core.llm import parse_record
from ..settings import Settings

router = APIRouter()
logger = logging.getLogger(__name__)
RECORD_DIR = "recordings"
os.makedirs(RECORD_DIR, exist_ok=True)


@router.post("/stt")
async def stt_api(file: UploadFile = File(...)):
    tmp = os.path.join(RECORD_DIR, f"{uuid.uuid4()}.wav")
    with open(tmp, "wb") as f:
        f.write(await file.read())
    text = await speech_to_text(tmp)
    return {"text": text}


@router.post("/parse")
async def parse_api(use_case: str = Form(...), text: str = Form(...)):
    data = parse_record(use_case, text)
    return {"data": data}


@router.post("/speech2json")
async def speech2json(file: UploadFile = File(...), use_case: str = Form(...)):
    tmp = os.path.join(RECORD_DIR, f"{uuid.uuid4()}.wav")
    with open(tmp, "wb") as f:
        f.write(await file.read())
    text = await speech_to_text(tmp)
    data = parse_record(use_case, text)
    return {"text": text, "data": data}
