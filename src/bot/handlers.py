import re
import os
from telegram import Update
from telegram.ext import ContextTypes
from src.bot.state_manager import StateManager
from src.services.llm_service import LLMService
from src.services.scraper_service import ScraperService
from src.services.image_service import ImageService
state_manager = StateManager()
llm_service = LLMService()
scraper_service = ScraperService()
image_service = ImageService()

def extract_url(text: str) -> str:
    """Search for a URL in the user's text message."""
    if not text:
        return None
    url_pattern = r'(https?://[^\s]+)'
    match = re.search(url_pattern, text)
    return match.group(0) if match else None

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command - initialize conversation and greet the user."""
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    
    
    await state_manager.clear_history(user_id)
    
    welcome_text = (
        f"🤖 Hello {first_name}! Welcome to TeleScout Bot.\n\n"
        "I am an advanced AI assistant capable of:\n"
        "💬 Maintaining context in continuous conversations.\n"
        "🔍 Reading and analyzing specific links you send me.\n"
        "🎨 Generating images directly on demand.\n\n"
        "How can I help you today?"
    )
    await update.message.reply_text(welcome_text)

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /clear command - delete the specific user's conversation history."""
    user_id = update.effective_user.id
    await state_manager.clear_history(user_id)
    await update.message.reply_text("🧹 Your conversation history has been cleared successfully!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming text messages, including URL detection and context injection."""
    user_id = update.effective_user.id
    user_text = update.message.text
    
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # Check whether the user explicitly requested image generation
    # (detect words like image, generate, draw, picture, תמונה, צייר)
    trigger_words = ["image", "generate", "draw", "picture", "תמונה", "צייר", "תג'נרט"]
    if any(word in user_text.lower() for word in trigger_words):
        await update.message.reply_text("🎨 Processing your image request via AI generation pipeline, please wait...")
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_photo")

        translation_prompt = [
            {"role": "user", "content": f"Extract ONLY the visual subject from this request and translate it to a clean English image prompt. If the text contains unrelated conversation, ignore it and isolate only the core image description: '{user_text}'"}
        ]
        refined_prompt = await llm_service.generate_response(translation_prompt)
        print(f"✨ [System Refined Prompt for FLUX]: {refined_prompt}")
        image_bytes = await image_service.generate_image(refined_prompt)
        if image_bytes:
            await update.message.reply_photo(photo=image_bytes, caption="✅ Generated via FLUX.1 Engine")
            return
        else:
            await update.message.reply_text("❌ Failed to generate image. Please try a different prompt later.")
            return

    detected_url = extract_url(user_text)
    
    if detected_url:
        await update.message.reply_text(f"🔍 Link detected! Scraping content from: {detected_url}...")
        scraped_content = await scraper_service.scrape_url(detected_url)
        
        enriched_prompt = (
            f"[System Context from scraped URL: {detected_url}]\n"
            f"The user wants you to analyze or answer based on this content:\n\n"
            f"{scraped_content}\n\n"
            f"User request: {user_text}"
        )
    
        await state_manager.add_message(user_id=user_id, role="user", content=enriched_prompt)
    else:
       
        await state_manager.add_message(user_id=user_id, role="user", content=user_text)

    history = await state_manager.get_history(user_id)
    ai_response = await llm_service.generate_response(history)
    await state_manager.add_message(user_id=user_id, role="assistant", content=ai_response)
    await update.message.reply_text(ai_response)