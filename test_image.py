import asyncio
import os
from dotenv import load_dotenv
from src.services.image_service import ImageService

# טעינת משתני הסביבה (יקרא מה-.env במחשב, או מה-env של GitHub Actions)
load_dotenv()

async def main():
    print("🎨 Initializing Image Service...")
    image_service = ImageService()

    # הפרומפט המקורי והמלא שאתה רוצה שה-AI יג'נרט
    test_prompt = (
        "A futuristic cyberpunk hacker workspace with multiple neon screens, "
        "high-tech computer equipment, low lighting, 4k resolution"
    )

    print(f"\n🚀 Sending prompt to Imagen 3 / Flux: '{test_prompt}'")
    print("⏳ Generating image (this usually takes 4-7 seconds)...")
    
    # הפעלת הצינור הראשי (מנסה ג'מיני, ואז עובר כגיבוי ל-Hugging Face)
    image_bytes = await image_service.generate_image(test_prompt)

    if image_bytes:
        # שמירת קובץ ה-JPEG האמיתי בתיקיית הפרויקט
        output_path = os.path.join(os.getcwd(), "test_generated_output.jpg")
        with open(output_path, "wb") as f:
            f.write(image_bytes)
        print(f"\n✅ Success! Received image bytes.")
        print(f"📊 Total size: {len(image_bytes)} bytes")
        print(f"💾 Saved test image to: {output_path}")
    else:
        print("\n❌ Failed to generate image. Check logs above for errors.")

if __name__ == "__main__":
    # הרצת הלולאה האסינכרונית של פייתון
    asyncio.run(main())