import os
from typing import Optional
import httpx

class HuggingFaceProvider:
    def __init__(self):
        self.api_key = os.getenv("HF_API_KEY")
        # הכתובת המדויקת והרשמית ישירות מול ה-Endpoint של המודל
        self.url = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"

    async def generate(self, prompt: str) -> Optional[bytes]:
        if not prompt or not prompt.strip():
            return None

        if not self.api_key:
            print("HuggingFaceProvider Status: No HF_API_KEY provided.")
            return None

        # הגדרת ה-Headers בצורה קפדנית כפי שה-API דורש
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {"inputs": prompt.strip()}

        try:
            # שימוש ב-AsyncClient עם טיפול מוגדר בשגיאות
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(self.url, headers=headers, json=payload)

                if response.status_code == 200:
                    return response.content
                
                print(f"HuggingFaceProvider Status: Restricted or failed (Status {response.status_code})")
                if response.text:
                    print(f"Details: {response.text[:100]}")
                return None
        except Exception as e:
            print(f"HuggingFaceProvider Status: Failed ({str(e)})")
            return None