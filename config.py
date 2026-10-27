import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

DEFAULT_MODEL = "gemini-flash-latest"

def get_api_key():
    """Retrieve Gemini API Key from environment variable or streamlit secret."""
    return os.getenv("GEMINI_API_KEY", "").strip()

class ResilientGeminiClient:
    """
    Robust wrapper around official google-genai SDK.
    Dynamically tries active Flash model identifiers with backoff on 503 spikes.
    Avoids Pro rate limits on free-tier keys.
    """
    def __init__(self, model_name: str = None, api_key: str = None):
        key = (api_key or get_api_key()).strip()
        if not key:
            raise ValueError("Gemini API Key is missing! Please set GEMINI_API_KEY in .env or provide it in the UI sidebar.")
        self.client = genai.Client(api_key=key)
        
        req = (model_name or DEFAULT_MODEL).replace("models/", "").strip()
        # Ensure we stick to fast Flash models with high quota limits
        if any(deprecated in req for deprecated in ["1.5", "2.5", "2.0", "pro"]):
            req = "gemini-flash-latest"
        self.requested_model = req
        
    def generate_content(self, prompt: str):
        candidates = [
            self.requested_model,
            "gemini-flash-latest",
            "gemini-3.8-flash",
            "gemini-3.6-flash",
            "gemini-flash-lite-latest",
            "gemini-2.5-flash-lite"
        ]
        
        models_to_try = []
        for c in candidates:
            if c and c not in models_to_try:
                models_to_try.append(c)
                
        last_error = None
        for attempt in range(2):
            for model in models_to_try:
                try:
                    response = self.client.models.generate_content(
                        model=model,
                        contents=prompt,
                    )
                    return response
                except Exception as e:
                    err_str = str(e)
                    print(f"[Gemini Retry] Model '{model}' failed: {err_str[:120]}")
                    last_error = e
                    if "503" in err_str or "UNAVAILABLE" in err_str:
                        time.sleep(1.5)
                    continue
                
        raise last_error

def get_llm_model(model_name: str = None, api_key: str = None):
    """Instantiate a ResilientGeminiClient instance."""
    return ResilientGeminiClient(model_name, api_key)
