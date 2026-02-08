# Notes (Summary of Current Setup)

## API Endpoints
- Single endpoint: `POST /summarize`
- Accepts two content types:
  - `application/json` with body `{"text": "..."}`
  - `text/plain` with raw text
- Query params: `style` (dropdown) and `max_words`

## Swagger UI
- Open: `http://127.0.0.1:8080/docs`
- Use the request body Content-Type dropdown to choose JSON vs text/plain.
- Only one POST endpoint should appear.

## Styles (Enum)
- `concise`
- `executive`
- `bullet points`
- `numbered list`
- `simple`
- `technical`
- `highlights`
- `action items`
- `key takeaways`
- `tl;dr`

## Model
- Current model in `app/main.py`: `gemini-2.5-flash-lite`

## Common Errors
- `422 Unprocessable Entity` usually means invalid JSON or mismatched Content-Type.
- For messy/multi-line text, use `text/plain` instead of JSON.

## Run Command (CMD)
```bat
uvicorn app.main:app --host 127.0.0.1 --port 8080
```

## Mock Mode (Local Only)
- Set `MOCK_SUMMARY=1` to bypass Gemini calls and return a placeholder summary.
- Example (CMD):
```bat
set MOCK_SUMMARY=1
uvicorn app.main:app --host 127.0.0.1 --port 8080
```
- Disable: `set MOCK_SUMMARY=`
- Do not commit this change if you don't want mock mode in GitHub.

## Problems Faced + Fixes Applied
- Swagger UI not opening at `0.0.0.0`: use `http://127.0.0.1:PORT/docs`.
- Port conflicts on 8000: kill old process or switch to 8080.
- Swagger dropdown not showing for body enums: moved `style` to query params.
- 422 errors in Swagger: JSON invalid or Content-Type mismatch.
- Multi-line messy text broke JSON: added `text/plain` support in `/summarize`.
- Docs confusion: added explicit Content-Type notes in Swagger, README, DOCUMENTATION.

