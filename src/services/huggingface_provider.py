import os
from typing import Optional
from huggingface_hub import InferenceClient

class HuggingFaceProvider:
    def __init__(self):
        self.api_key = os.getenv("HF_API_KEY")
        # שימוש בקליינט הרשמי של Hugging Face
        self.client = InferenceClient(token=self.api_key) if self.api_key else None

    async def generate(self, prompt: str) -> Optional[bytes]:
        if not prompt or not prompt.strip():
            return None

        if not self.client:
            print("HuggingFaceProvider Status: No HF_API_KEY provided.")
            return None

        try:
            # שליחה ישירה למודל FLUX דרך הצינור הרשמי והמאובטח שלהם
            image = self.client.image_generation(
                model="black-forest-labs/FLUX.1-schnell",
                prompt=prompt.strip()
            )
            
            # המרה של התמונה ל-Bytes (קובץ JPEG)
            import io
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG')
            return img_byte_arr.getvalue()

        except Exception as e:
            print(f"HuggingFaceProvider Status: Failed ({str(e)})")
            return None