import os
import time
from typing import Any, Dict, List
from google import genai
from google.genai import errors as genai_errors
from google.genai import types

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key) if self.api_key else None
        self.preferred_models = [
            "models/gemini-2.5-flash",
            "models/gemini-2.0-flash",
            "models/gemini-3.5-flash",
        ]
        self.model_name = os.getenv("GEMINI_MODEL_NAME", self.preferred_models[0])

    async def generate_response(self, conversation_history: List[Dict[str, str]]) -> str:
        if not self.client:
            return "Error: Gemini API key is missing."

        contents: List[types.Content] = []
        for message in conversation_history:
            role = message.get("role", "user")
            if role != "user":
                role = "model"

            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=message["content"])],
                )
            )

        config = types.GenerateContentConfig(
            temperature=0.35,
            max_output_tokens=700,
        )

        try:
            return await self._generate_with_fallback(contents, config)
        except genai_errors.ClientError as e:
            print(f"❌ Gemini ClientError: {e}")
            return f"Error: Gemini service issue."
        except Exception as e:
            print(f"❌ Error in LLMService: {e}")
            return "Error: Failed to generate response."

    async def _generate_with_fallback(self, contents, config) -> str:
        models_to_try = [self.model_name] + [m for m in self.preferred_models if m != self.model_name]
        last_error = None

        for model in models_to_try:
            try:
                time.sleep(2)
                response = await self.client.aio.models.generate_content(
                    model=model,
                    contents=contents,
                    config=config,
                )
                self.model_name = model
                if hasattr(response, "text") and response.text:
                    return response.text
            except genai_errors.ClientError as e:
                last_error = e
                if "429" in str(e):
                    continue
                raise

        raise last_error or Exception("Unable to generate response")