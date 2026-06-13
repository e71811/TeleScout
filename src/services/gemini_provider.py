import os
from typing import Optional
import httpx

class GeminiImageProvider:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={self.api_key}"

    async def generate(self, prompt: str) -> Optional[bytes]:
        if not prompt or not prompt.strip():
            return None

        if not self.api_key:
            print("GeminiProvider Status: No GEMINI_API_KEY provided.")
            return None

        headers = {"Content-Type": "application/json"}
        payload = {
            "instances": [
                {"prompt": prompt.strip()}
            ],
            "parameters": {
                "sampleCount": 1,
                "aspectRatio": "1:1",
                "outputMimeType": "image/jpeg"
            }
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(self.url, headers=headers, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    base64_image = data["predictions"][0]["bytesBase64Encoded"]
                    import base64
                    return base64.b64decode(base64_image)
                print(f"GeminiProvider Status: Restricted or failed ({response.status_code})")
                return None
        except Exception as e:
            print(f"GeminiProvider Status: Failed ({str(e)})")
            return None