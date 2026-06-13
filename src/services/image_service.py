from typing import Optional
from src.services.gemini_provider import GeminiImageProvider
from src.services.huggingface_provider import HuggingFaceProvider

class ImageService:
    def __init__(self):
        self.gemini_provider = GeminiImageProvider()
        self.backup_provider = HuggingFaceProvider()

    async def generate_image(self, prompt: str) -> Optional[bytes]:
        if not prompt or not prompt.strip():
            return None

        print(" Attempting image generation via Google Gemini...")
        gemini_bytes = await self.gemini_provider.generate(prompt)
        if gemini_bytes:
            print("Image generated successfully via Gemini.")
            return gemini_bytes

        # Fallback to Hugging Face FLUX
        print(" Gemini unavailable. Activating Hugging Face FLUX AI fallback...")
        backup_bytes = await self.backup_provider.generate(prompt) 
        if backup_bytes:
            print("Image generated successfully via Hugging Face FLUX Fallback.")
            return backup_bytes

        print("Error: All image generation providers failed.")
        return None