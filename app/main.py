from __future__ import annotations

import os
import re
from enum import Enum
from typing import Any

from fastapi import FastAPI, HTTPException, Query, Request
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv


def _get_api_key() -> str:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")
    return api_key


def _build_model() -> genai.GenerativeModel:
    genai.configure(api_key=_get_api_key())
    generation_config = {
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 64,
        "max_output_tokens": 1024,
    }
    return genai.GenerativeModel(
        model_name="gemini-2.5-flash-lite",
        generation_config=generation_config,
    )


app = FastAPI(
    title="Gemini Text Summarizer",
    version="1.0.0",
    description=(
        "Summarize text using Gemini LLM via FastAPI. "
        "In Swagger UI, choose the request body Content-Type "
        "(application/json or text/plain) before pasting your text."
    ),
    openapi_version="3.0.2",
)

model = _build_model()


class SummarizeResponse(BaseModel):
    summary: str
    meta: dict[str, Any]


class SummaryStyle(str, Enum):
    concise = "concise"
    executive = "executive"
    bullet_points = "bullet points"
    numbered_list = "numbered list"
    simple = "simple"
    technical = "technical"
    highlights = "highlights"
    action_items = "action items"
    key_takeaways = "key takeaways"
    tldr = "tl;dr"


def _build_prompt(text: str, max_words: int | None, style: SummaryStyle) -> str:
    max_words_text = f"Max {max_words} words." if max_words else "Keep it brief."
    if style == SummaryStyle.bullet_points:
        style_text = "Return bullet points, each line starting with '- '."
    elif style == SummaryStyle.numbered_list:
        style_text = "Return a numbered list, one item per line like '1. ...'."
    else:
        style_text = f"Style: {style}."
    return (
        "You are a helpful assistant that summarizes text.\n"
        f"{max_words_text} {style_text}\n"
        "Return only the summary.\n\n"
        f"TEXT:\n{text}"
    )


def _clean_text(text: str) -> str:
    # Convert escaped newlines to real newlines if present.
    text = text.replace("\\n", "\n")
    # Replace URLs with a placeholder to reduce noise and tokens.
    text = re.sub(r"https?://\S+|www\.\S+", "[URL]", text)
    # Remove control characters except newlines/tabs.
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
    # Normalize whitespace and line breaks.
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _mock_summary(text: str, max_words: int | None) -> str:
    words = text.split()
    limit = max_words if max_words and max_words > 0 else 120
    snippet = " ".join(words[:limit])
    if len(words) > limit:
        snippet = f"{snippet}..."
    return snippet.strip()


@app.post(
    "/summarize",
    response_model=SummarizeResponse,
    summary="Summarize (JSON or text/plain)",
    description=(
        "Send JSON body with `text` using `Content-Type: application/json`, "
        "or send raw text using `Content-Type: text/plain`. "
        "In Swagger UI, use the request body Content-Type dropdown to pick the right format. "
        "If content type and body don't match, you'll get 422."
    ),
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string", "minLength": 1},
                        },
                        "required": ["text"],
                    }
                },
                "text/plain": {
                    "schema": {"type": "string"},
                },
            },
        }
    },
)
async def summarize(
    request: Request,
    style: SummaryStyle = Query(
        default=SummaryStyle.concise,
        description="Summary style (dropdown in docs).",
    ),
    max_words: int | None = Query(
        default=120,
        ge=20,
        le=400,
        description="Target maximum word count for the summary.",
    ),
) -> SummarizeResponse:
    try:
        content_type = (request.headers.get("content-type") or "").lower()
        if content_type.startswith("text/plain"):
            raw = await request.body()
            text = raw.decode("utf-8", errors="replace")
        elif content_type.startswith("application/json"):
            data = await request.json()
            if not isinstance(data, dict) or "text" not in data:
                raise HTTPException(status_code=422, detail="JSON body must include 'text'.")
            text = str(data.get("text", ""))
        else:
            raise HTTPException(
                status_code=415,
                detail="Unsupported Content-Type. Use application/json or text/plain.",
            )

        if not text.strip():
            raise HTTPException(status_code=422, detail="Text cannot be empty.")

        cleaned = _clean_text(text)
        if os.getenv("MOCK_SUMMARY", "").strip() == "1":
            summary = _mock_summary(cleaned, max_words)
        else:
            prompt = _build_prompt(cleaned, max_words, style)
            response = model.generate_content(prompt)
            summary = (response.text or "").strip()
        if not summary:
            raise HTTPException(status_code=500, detail="Empty summary from model.")
        return SummarizeResponse(
            summary=summary,
            meta={
                "model": "gemini-2.5-flash-lite",
                "max_words": max_words,
                "style": style,
                "mock": os.getenv("MOCK_SUMMARY", "").strip() == "1",
            },
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
