import io
import os
import re
from datetime import datetime
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse
from PIL import Image, UnidentifiedImageError, ImageOps
import pytesseract

from ollama_parser import parse_ticket_llm

app = FastAPI()

UPLOAD_DIR = "static"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def ocr_from_bytes(contents: bytes) -> str:
    image = Image.open(io.BytesIO(contents))
    image = image.resize((image.width * 2, image.height * 2))
    gray = ImageOps.grayscale(image)
    gray = ImageOps.autocontrast(gray)
    config = "--oem 3 --psm 6 -l eng"
    text = pytesseract.image_to_string(gray, config=config)
    clean = re.sub(r"[^A-Za-z0-9:/\s-]", "", text)
    return " ".join(clean.split())


@app.get("/")
def root():
    return {"message": "AI Ticket Validator backend is running"}


@app.post("/upload")
async def upload_image(file: UploadFile = File(...), save: bool = Query(default=False)):
    if file.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(
            status_code=400, detail="Only JPEG or PNG images are supported")

    contents = await file.read()

    filename = None
    if save:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        with open(os.path.join(UPLOAD_DIR, filename), "wb") as f:
            f.write(contents)

    try:
        ocr_text = await run_in_threadpool(ocr_from_bytes, contents)
    except UnidentifiedImageError:
        raise HTTPException(
            status_code=400, detail="Uploaded file is not a valid image")

    parsed = parse_ticket_llm(ocr_text)

    response = {"extracted_text": ocr_text, "parsed_fields": parsed}
    if filename:
        response["filename"] = filename

    return JSONResponse(content=response)
