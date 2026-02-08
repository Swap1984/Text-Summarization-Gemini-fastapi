# Text Summarisation with Gemini + FastAPI

## Overview
This project provides a REST API for text summarization using Gemini LLM, served via FastAPI.
It exposes a single `/summarize` endpoint that accepts text and returns a concise summary.

## Prerequisites
- Python 3.11.9 or later
- A Gemini API key

## Setup

### 1. Create and activate the virtual environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Ensure pip is upgraded in the venv
```powershell
python -m pip install --upgrade pip setuptools wheel
```

### 3. Install dependencies
```powershell
pip install -r requirements.txt
```

## Environment Variables
Set your API key as an environment variable before running the app:
```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

Optional: you can create a `.env` file and load it via `python-dotenv` in your runtime (not required by default).

## Running the API
```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Usage

### Endpoint
`POST /summarize`

### Request Body (JSON)
```json
{
  "text": "Long input text to summarize..."
}
```

### Request Body (text/plain)
Send raw text with `Content-Type: text/plain` (no JSON needed).
In Swagger UI, use the request body Content-Type dropdown to select `text/plain` before pasting text.

### Query Parameters
- `style` (dropdown in docs): one of `concise`, `executive`, `bullet points`, `numbered list`, `simple`, `technical`, `highlights`, `action items`, `key takeaways`, `tl;dr`
- `max_words`: integer between 20 and 400 (default 120)

### Response
```json
{
  "summary": "Short summary text here.",
  "meta": {
    "model": "gemini-2.5-flash-lite",
    "max_words": 120,
    "style": "concise",`r`n    "mock": false
  }
}
```

### Important: Content-Type Must Match
If you use JSON, set header `Content-Type: application/json` and send valid JSON.
If you use raw text, set `Content-Type: text/plain`.
If the content type and body don't match, you'll get a `422 Unprocessable Entity` error.

### Example cURL
```bash
curl -X POST "http://localhost:8000/summarize?style=executive&max_words=80" \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"FastAPI is a modern web framework for building APIs with Python...\"}"
```

### Example (text/plain)
```bash
curl -X POST "http://localhost:8000/summarize?style=numbered%20list&max_words=80" \
  -H "Content-Type: text/plain" \
  --data "FastAPI is a modern, fast web framework for building APIs with Python. It is based on standard Python type hints and provides automatic interactive documentation using OpenAPI."
```

## Error Handling
- `500 Internal Server Error` is returned if the model fails or the response is empty.
- Input validation errors return `422 Unprocessable Entity` (FastAPI default).

## Technical Architecture
See the architecture diagram in `architecture_diagram.mmd`.

## Deliverables
- `app/main.py` (FastAPI application)
- `requirements.txt` (dependencies)
- `DOCUMENTATION.md` (this file)
- `architecture_diagram.mmd` (technical architecture diagram)`r`n- `notebooks/Text_Summarisation_fastapi.ipynb` (notebook)

