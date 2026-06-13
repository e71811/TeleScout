import os
from typing import List, Dict
from google import genai
from google.genai import types

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(http_options={'api_version': 'v1'}) if self.api_key else None
        self.model_name = "gemini-2.5-flash"

    async def generate_response(self, conversation_history: List[Dict[str, str]]) -> str:
        if not self.client:
            return "Error: Gemini API key is missing."
        try:
            contents = []
            for message in conversation_history:
                role = "user" if message["role"] == "user" else "model"
                contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=message["content"])]
                    )
                )

            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=contents,
            )

            if response.text:
                return response.text
            return "I received an empty response from the AI model."

        except Exception as e:
            return f"Error communicating with Gemini AI Service: {str(e)}"