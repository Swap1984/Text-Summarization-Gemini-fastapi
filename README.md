# Text Summarisation with Gemini + FastAPI

## Overview
This project provides a REST API for abstractive text summarization using Gemini LLM, served via FastAPI.
It exposes a single `/summarize` endpoint that accepts text and returns a concise summary.

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

## Running the API
```powershell
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
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
    "model": "gemini-1.5-flash",
    "max_words": 120,
    "style": "concise"
  }
}
```

### Important: Content-Type Must Match
If you use JSON, set header `Content-Type: application/json` and send valid JSON.
If you use raw text, set `Content-Type: text/plain`.
If the content type and body don’t match, you’ll get a `422 Unprocessable Entity` error.

### Example (text/plain)
```bash
curl -X POST "http://localhost:8000/summarize?style=numbered%20list&max_words=80" \
  -H "Content-Type: text/plain" \
  --data "FastAPI is a modern, fast web framework for building APIs with Python. It is based on standard Python type hints and provides automatic interactive documentation using OpenAPI."
```

## Preprocessing (Why and What We Do)
Preprocessing helps reduce noise and improves summary quality, especially for scraped or messy text.
Current preprocessing in `app.py`:
- Replace URLs with `[URL]` to reduce distraction and token usage.
- Normalize whitespace (collapse multiple spaces/newlines).

You can extend this with domain-specific cleanup (e.g., removing repeated boilerplate).

## Parameter Tuning (Key Generation Settings)
These parameters control how deterministic or diverse the summary is:
- `temperature`: lower values make outputs more stable and conservative.
- `top_p`: nucleus sampling; lower = more deterministic.
- `top_k`: limits candidate tokens; lower = more deterministic.

Recommended starting points for summarization:
- `temperature`: 0.2–0.4
- `top_p`: 0.7–0.9
- `top_k`: 20–64

## Styles (Dropdown in API Docs)
The API exposes a fixed set of styles via an enum, shown as a dropdown in the FastAPI docs UI:
- `concise`
- `executive`
- `bullet points` (forced `- ` bullets)
- `numbered list` (forced `1.`, `2.`, `3.`)
- `simple`
- `technical`
- `highlights`
- `action items`
- `key takeaways`
- `tl;dr`

## Deliverables
- `app.py` (FastAPI application)
- `requirements.txt` (dependencies)
- `README.md` (this file)
- `DOCUMENTATION.md` (detailed documentation)
- `architecture_diagram.mmd` (technical architecture diagram)
