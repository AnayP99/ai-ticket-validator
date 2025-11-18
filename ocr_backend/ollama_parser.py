import os
import re
import time
import json
from datetime import datetime
from typing import Dict, Any, Optional
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = os.getenv("OLLAMA_MODEL", "mistral")
TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))
MAX_RETRIES = 2
BACKOFF = 2.0


def _extract_json_block(s: str) -> Optional[str]:
    m = re.search(r"\{.*\}", s, flags=re.DOTALL)
    return m.group(0) if m else None


def _prefilter_ocr(text: str) -> str:
    keywords = r"\b(from|to|date|time|valid|validity|class|pass|uts|season|journey|booking)\b"
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    kept = [ln for ln in lines if re.search(keywords, ln, flags=re.IGNORECASE)]
    if kept:
        return " ".join(kept)
    return text.strip()[:800]


def parse_ticket_llm(ocr_text: str) -> Dict[str, Any]:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    short_text = _prefilter_ocr(ocr_text)
    prompt = (
        "Extract the following fields from the OCR text of a Mumbai local train ticket. "
        "Return ONLY a single JSON object with these keys (use null when unknown): "
        "origin, destination, journey_date (YYYY-MM-DD), journey_time (HH:MM), "
        "travel_class, passenger_count (integer), ticket_type, is_valid_now (boolean), validity_reason (short string). "
        f"Use the current time {now} to decide validity. Keep validity_reason short.\n\n"
        f"OCR: {short_text}\nJSON:"
    )
    payload = {"model": MODEL, "prompt": prompt, "stream": False}
    last_err = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(OLLAMA_URL, json=payload, timeout=TIMEOUT)
            resp.raise_for_status()
            try:
                data = resp.json()
                raw = data.get("response") or data.get(
                    "generated") or json.dumps(data)
            except Exception:
                raw = resp.text if hasattr(resp, "text") else ""
            json_block = _extract_json_block(raw)
            if not json_block:
                return {"error": "model_no_json", "raw_reply": raw[:2000]}
            parsed = json.loads(json_block)
            if isinstance(parsed, dict):
                return parsed
            return {"result": parsed}
        except requests.Timeout as e:
            last_err = f"timeout: {e}"
            if attempt < MAX_RETRIES:
                time.sleep(BACKOFF ** attempt)
                continue
            return {"error": "timeout", "detail": last_err}
        except requests.RequestException as e:
            last_err = str(e)
            if attempt < MAX_RETRIES:
                time.sleep(BACKOFF ** attempt)
                continue
            return {"error": "request_failed", "detail": last_err}
        except json.JSONDecodeError:
            return {"error": "json_decode_failed", "raw_reply": raw[:2000]}
        except Exception as e:
            last_err = str(e)
            if attempt < MAX_RETRIES:
                time.sleep(BACKOFF ** attempt)
                continue
            return {"error": "unknown_error", "detail": last_err}
    return {"error": "failed_after_retries", "detail": last_err}
