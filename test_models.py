import os
from dotenv import load_dotenv
from google import genai

# טעינת מפתח ה-API מה-.env
load_dotenv()

def list_my_models():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in .env file!")
        return

    print("📡 Connecting to Google AI Studio...")
    try:
        # אתחול ה-Client בדיוק כמו שהוא מאותחל אצלך בפרויקט
        client = genai.Client()
        
        print("\n🤖 Available Models for your SDK and API Key:")
        print("--------------------------------------------------")
        
        # תשאול השרת לגבי כל המודלים הזמינים לחשבון שלך
        for model in client.models.list():
            print(f"🔗 Model Name: {model.name}")
            print(f"   Supported Actions: {model.supported_actions}\n")
            
        print("--------------------------------------------------")
    except Exception as e:
        print(f"❌ Failed to list models: {str(e)}")

if __name__ == "__main__":
    list_my_models()