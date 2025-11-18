# 🧾 AI Ticket Validator Backend

AI-powered backend for validating **Mumbai Local Train UTS & Season Tickets** using **OCR + Local LLM (Ollama)**.  
Fast, private, and fully offline.

---

## 🚀 Features

### ✅ OCR (Tesseract)
- Extracts ticket text from uploaded photos or screenshots.
- Preprocessing improves recognition accuracy.
- Cleans and normalizes noisy OCR output.

### ✅ Local LLM Parsing (Ollama)
Extracts structured ticket information using a fast local model (default: **Mistral**):

- origin  
- destination  
- journey_date  
- journey_time  
- travel_class  
- passenger_count  
- ticket_type  
- is_valid_now  
- validity_reason  

All done **locally** — no cloud, no external APIs.

### ✅ FastAPI Backend
- Upload images via HTTP  
- Performs OCR  
- Sends cleaned text to local LLM  
- Returns structured JSON  
- Optional image saving  

---

## 🛠️ Tech Stack

| Component        | Technology                   |
| ---------------- | ---------------------------- |
| Backend          | FastAPI                      |
| OCR              | Tesseract                    |
| Image Processing | Pillow                       |
| LLM              | Ollama (Mistral recommended) |
| Language         | Python                       |
| Server           | Uvicorn                      |

---

## 📁 Project Structure

```text
ai-ticket-validator/
│
├── ocr_backend/
│   ├── main.py               # FastAPI backend (OCR + LLM API)
│   ├── ollama_parser.py      # Local LLM ticket parser
│   ├── requirements.txt
│   └── static/               # Optional saved images
│
└── README.md
```

---

## ⚙️ Installation

### 1. Create Virtual Environment
```bash
cd ai-ticket-validator/ocr_backend
python -m venv venv
```

Activate:

**Windows**
```bash
venv\Scripts\activate
```

**macOS / Linux**
```bash
source venv/bin/activate
```

---

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 3. Install Tesseract

**Windows:**  
Download from: https://github.com/tesseract-ocr/tesseract  

**macOS**
```bash
brew install tesseract
```

**Linux**
```bash
sudo apt install tesseract-ocr
```

---

### 4. Install & Start Ollama

Install from:  
https://ollama.com

Pull recommended model:
```bash
ollama pull mistral
```

Start Ollama server:
```bash
ollama serve
```

(Optional) Preload model for faster first response:
```bash
ollama run mistral
```

---

## ▶️ Run the Backend

```bash
uvicorn main:app --reload
```

API Docs available at:  
👉 http://127.0.0.1:8000/docs

---

## 📤 API Usage

### **POST /upload**

Uploads an image → runs OCR → parses fields via LLM → returns JSON.

#### Example (PowerShell)
```powershell
curl.exe -F "file=@D:\path\to\ticket.jpg" http://127.0.0.1:8000/upload
```

#### Example JSON Response
```json
{
  "extracted_text": "FROM THANE TO CSMT DATE 21-10-2025 TIME 09:15 CLASS 2ND",
  "parsed_fields": {
    "origin": "THANE",
    "destination": "CSMT",
    "journey_date": "2025-10-21",
    "journey_time": "09:15",
    "travel_class": "2nd",
    "passenger_count": 1,
    "ticket_type": "UTS",
    "is_valid_now": true,
    "validity_reason": "Within validity period."
  }
}
```

---

## 🔒 Privacy

- All processing happens on your machine  
- No external API calls  
- No cloud storage  
- Suitable for official or secure environments  

---

## 🔮 Future Enhancements

- QR code scanning
- Flutter mobile app frontend  
- Lightweight on-device model for validation  
- More accurate season-ticket validation  
- Marathi/Hindi OCR
