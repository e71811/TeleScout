import os
from typing import Optional
import httpx

class HuggingFaceProvider:
    def __init__(self):
        self.api_key = os.getenv("HF_API_KEY")
        self.url = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"

    async def generate(self, prompt: str) -> Optional[bytes]:
        if not prompt or not prompt.strip():
            return None

        if not self.api_key:
            print("HuggingFaceProvider Status: No HF_API_KEY provided.")
            return None

        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"inputs": prompt}

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(self.url, headers=headers, json=payload)
                if response.status_code == 200:
                    return response.content
                print(f"HuggingFaceProvider Warning: Status {response.status_code}")
                return None
        except Exception as e:
            print(f"HuggingFaceProvider Status: Failed ({str(e)})")
            return None