import io
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse
from PIL import Image, UnidentifiedImageError
import pytesseract
import os
from datetime import datetime

app = FastAPI()

UPLOAD_DIR = "static"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def ocr_from_bytes(contents: bytes) -> str:
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    text = pytesseract.image_to_string(image, config="--psm 6")
    return text.strip()


@app.get("/")
def root():
    return {"message": "AI Ticket Validator backend is running"}


@app.post("/ocr")
async def perform_ocr(file: UploadFile = File(...)):
    if file.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(
            status_code=400, detail="Only JPEG or PNG images are supported")

    contents = await file.read()

    try:
        text = await run_in_threadpool(ocr_from_bytes, contents)
    except UnidentifiedImageError:
        raise HTTPException(
            status_code=400, detail="Uploaded file is not a valid image")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed: {str(e)}")

    return JSONResponse(content={"extracted_text": text})


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(
            status_code=400, detail="Only JPEG or PNG images are supported")

    contents = await file.read()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(contents)

    try:
        text = await run_in_threadpool(ocr_from_bytes, contents)
    except UnidentifiedImageError:
        raise HTTPException(
            status_code=400, detail="Saved file is not a valid image")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed: {str(e)}")

    return JSONResponse(content={"filename": filename, "extracted_text": text})
