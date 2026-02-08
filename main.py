from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

genai.configure(api_key=("API KEY HERE"))

# Set up the model configuration
generation_config = {
    "temperature": 0.2,
    "top_p": 0.8,
    "top_k": 64,
    "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Function to translate text using the Gemini model
def translate_text(text: str, source_language: str, target_language: str) -> str:
    prompt = f"Translate the following text from {source_language} to {target_language}: \"{text}\""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating translation: {str(e)}")

# Initialize FastAPI app
app = FastAPI()

# Request model for input validation
class TranslationRequest(BaseModel):
    text: str
    source_language: str
    target_language: str

# Translation endpoint
@app.post("/translate/")
async def translate(request: TranslationRequest):
    try:
        translated_text = translate_text(request.text, request.source_language, request.target_language)
        return {"original_text": request.text, "translated_text": translated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

