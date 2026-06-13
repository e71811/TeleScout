import os
from google import genai

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY environment variable is not set.")
    raise SystemExit(1)

client = genai.Client(api_key=api_key)

try:
    result = client.models.list()
    print("Available Gemini models:")
    for model in result:
        name = getattr(model, 'name', None)
        if name:
            print(name)
        else:
            print(model)
except Exception as e:
    print(f"Error listing models: {e}")
    raise
