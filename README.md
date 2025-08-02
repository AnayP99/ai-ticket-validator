# 🧾 AI Ticket Validator

An AI-powered mobile app to help Mumbai local train ticket checkers validate UTS mobile tickets using OCR, GPS, and real-time logic.

---

## 📌 Use Case
Ticket Checkers (TCs) manually check UTS tickets by eye. This project aims to automate the validation of a ticket shown on a mobile screen, in real time, using the TC's camera, current location, and time.

---

## 🛠️ Tech Stack

### 👁️ OCR & Parsing (Backend)
- Python
- Tesseract OCR
- OpenCV (image preprocessing)
- FastAPI (API layer)
- LangChain / OpenAI API (LLM ticket parsing and validation)

### 📱 Mobile App
- Flutter (camera + UI)
- geolocator (location data)
- HTTP client for API calls

---

## 📁 Folder Structure

ai-ticket-validator/ ├── ocr_backend/         ← Python backend for OCR + GPT ├── mobile_scanner/      ← Flutter frontend for ticket scanner ├── shared/              ← Shared config, prompts, ticket examples └── README.md            ← You are here

---

## 🚶 Phase 1 Roadmap – OCR Ticket Validator

### Week 1
- [x] Create GitHub repo and folder structure
- [x] Set up Python FastAPI backend
- [ ] Integrate Tesseract OCR
- [ ] Build preprocessing pipeline (OpenCV)

### Week 2
- [ ] Prepare sample UTS tickets (screenshots/mockups)
- [ ] Send OCR output to OpenAI LLM to extract fields
- [ ] Build basic ticket validity logic (origin, dest, time)

### Week 3
- [ ] Build mobile UI (Flutter camera + capture button)
- [ ] Send image and location to backend
- [ ] Display result to TC instantly

---

## 🔮 Future Scope
- Add QR-based ticket validation pipeline
- Offline fallback using on-device ML
- Use fine-tuned models for specific ticket formats
- Multi-language support (Marathi, Hindi)

---

## 🙌 Credits
Created by Anay Padhye to explore real-world applications of AI in public infrastructure.