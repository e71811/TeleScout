import asyncio
import os
import sys
import re
from dotenv import load_dotenv

# Add project root to Python path to allow imports from the tests directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our modular services
from src.services.llm_service import LLMService
from src.services.scraper_service import ScraperService
from src.services.image_service import ImageService

# Load environment variables (.env)
load_dotenv()

def extract_url(text: str) -> str:
    """
    Helper function that searches for a URL inside text using a regex
    """
    url_pattern = r'(https?://[^\s]+)'
    match = re.search(url_pattern, text)
    return match.group(0) if match else None

async def run_comprehensive_phase2_test():
    print("============================================================")
    print("🚀 Starting Comprehensive Phase 2 Integration Test 🚀")
    print("============================================================\n")
    
    # Initialize all Phase 2 services
    llm = LLMService()
    scraper = ScraperService()
    image_service = ImageService()

    # ------------------------------------------------------------
    # Part A: Standard Conversation Test (Standard Multi-turn LLM Conversation)
    # ------------------------------------------------------------
    print("🔹 [Part 1/3] Testing Standard Conversation Capability...")
    standard_history = [
        {"role": "user", "content": "Hello! Explain briefly what a Python decorator is."}
    ]
    print(f"👤 User: {standard_history[0]['content']}")
    
    chat_response = await llm.generate_response(standard_history)
    print(f"🤖 Gemini: {chat_response}\n")
    print("-" * 60)

    # ------------------------------------------------------------
    # Part B: URL Scraping & Context-Based Response Test (URL Scraping & Context Response)
    # ------------------------------------------------------------
    print("🔹 [Part 2/3] Testing URL Scraping & Context-Based Response...")
    url_message = (
        "Please read this article and summarize the key points for me: "
        "https://example.com"
    )
    print(f"👤 User Message: '{url_message}'")
    
    detected_url = extract_url(url_message)
    conversation_history = [{"role": "user", "content": url_message}]
    
    if detected_url:
        print(f"🔍 [System] Detected URL: {detected_url}")
        print("⏳ Fetching and scraping content from the specified URL...")
        
        # Actual scraping of data from the provided URL
        scraped_data = await scraper.scrape_url(detected_url)
        print(f"📄 [System] Scraped Context Preview ({len(scraped_data)} characters fetched).")
        
        # Inject the scraped information into the conversation history for the LLM
        context_prompt = (
            f"[System Context from scraped URL: {detected_url}]\n"
            f"The user wants you to answer based on this web content:\n\n"
            f"{scraped_data}\n\n"
            f"Now, answer the user's request: Summary of the key points."
        )
        conversation_history[-1]["content"] = context_prompt
        
        print("⏳ Sending combined prompt to Gemini...")
        agent_url_response = await llm.generate_response(conversation_history)
        print(f"🤖 Gemini (Context Answer):\n{agent_url_response}\n")
    else:
        print("❌ Error: No URL was detected for Part 2.")
    
    print("-" * 60)

    # ------------------------------------------------------------
    # Part C: Image Generation & Fallback Test (Image Generation & Fallback)
    # ------------------------------------------------------------
    print("🔹 [Part 3/3] Testing Image Generation & Fallback System...")
    image_prompt = "A high-tech digital AI agent scanning a website holographic projection, cyberpunk style"
    print(f"🎨 Target Prompt: '{image_prompt}'")
    
    image_bytes = await image_service.generate_image(image_prompt)
    
    if image_bytes:
        # Save the file to the project root for visualizing the success
        output_path = os.path.join(os.getcwd(), "test_phase2_output.jpg")
        with open(output_path, "wb") as f:
            f.write(image_bytes)
        print(f"✅ Success! Saved generated image to: {output_path}")
    else:
        print("❌ Error: Image generation failed across all providers.")

    print("\n============================================================")
    print("🏁 Phase 2 Verification Completed Successfully! All Services Operational.")
    print("============================================================")

if __name__ == "__main__":
    asyncio.run(run_comprehensive_phase2_test())