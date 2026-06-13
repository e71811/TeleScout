import os
from typing import Optional
from google import genai
from google.genai import types

class GeminiImageProvider:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key, http_options={'api_version': 'v1'}) if self.api_key else None
        self.model_name = "imagen-3.0-generate-002"

    async def generate(self, prompt: str) -> Optional[bytes]:
        if not self.client:
            print("GeminiProvider Status: No GEMINI_API_KEY provided.")
            return None
        try:
            response = await self.client.aio.models.generate_images(
                model=self.model_name,
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    output_mime_type="image/jpeg",
                    aspect_ratio="1:1"
                )
            )
            if response and response.generated_images:
                return response.generated_images[0].image.image_bytes
            return None
        except Exception as e:
            print("GeminiImageProvider: Model is restricted or unavailable. Switching to fallback...")
            return None