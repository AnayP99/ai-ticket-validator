from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os
from datetime import datetime

app = FastAPI()

UPLOAD_DIR = "static"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def read_root():
    return {"message": "AI Ticket Validator backend is running"}


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        return JSONResponse(status_code=400, content={"error": "Only JPEG or PNG images allowed"})
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"filename": filename, "message": "Upload successful"}
