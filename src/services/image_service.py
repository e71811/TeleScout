import asyncio
from typing import Optional
from src.services.gemini_provider import GeminiImageProvider
from src.services.huggingface_provider import HuggingFaceProvider

class ImageService:
    def __init__(self):
        self.gemini_provider = GeminiImageProvider()
        self.huggingface_provider = HuggingFaceProvider()

    async def generate_image(self, prompt: str) -> Optional[bytes]:
        # 1. ניסיון ראשון: גוגל ג'מיני
        print("🎨 Attempting image generation via Google Gemini...")
        try:
            image_bytes = await self.gemini_provider.generate(prompt)
            if image_bytes:
                return image_bytes
        except Exception as e:
            print(f"⚠️ Gemini execution error: {str(e)}")

        # 2. ניסיון שני (Fallback): האגינג פייס FLUX
        print("🔄 Gemini unavailable. Activating Hugging Face FLUX AI fallback...")
        try:
            image_bytes = await self.huggingface_provider.generate(prompt)
            if image_bytes:
                return image_bytes
        except Exception as e:
            print(f"❌ Hugging Face execution error: {str(e)}")

        print("❌ Error: All image generation providers failed.")
        return None