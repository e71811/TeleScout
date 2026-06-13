import os
import re
from telegram import Update
from telegram.ext import ContextTypes

from src.bot.state_manager import StateManager
from src.services.llm_service import LLMService
from src.services.image_service import ImageService

try:
    from src.services.search_service import SearchService
except ModuleNotFoundError:
    SearchService = None

try:
    from src.services.scraper_service import ScraperService
except ModuleNotFoundError:
    ScraperService = None

state_manager = StateManager()
llm_service = LLMService()
image_service = ImageService()
search_service = SearchService() if SearchService else None
scraper_service = ScraperService() if ScraperService else None

AGENT_SYSTEM_PROMPT = (
    "You are an autonomous AI Agent. "
    "If you need external data, emit ONLY: [CALL_TOOL: google_search | query: <text>]\n"
    "When you receive [System Search Output], analyze the data immediately "
    "and provide a final, comprehensive, and friendly answer in ENGLISH. "
    "Synthesize the answer—do not just list the search results."
)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await state_manager.clear_history(user_id)
    await update.message.reply_text("🤖 Hello! I am your autonomous AI Agent. I can search the web and generate images.")

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await state_manager.clear_history(user_id)
    await update.message.reply_text("🧹 Conversation history cleared.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text
    chat_id = update.effective_chat.id

    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    history = await state_manager.get_history(user_id)
    if not history or history[0].get("role") != "user":
        await state_manager.add_message(user_id=user_id, role="user", content=AGENT_SYSTEM_PROMPT)

    await state_manager.add_message(user_id=user_id, role="user", content=user_text)

    # Calling Gemini
    current_history = await state_manager.get_history(user_id)
    response_text = await llm_service.generate_response(current_history)
    
    print(f"DEBUG: LLM Raw Response: {response_text}")

    # Tool Call Analysis
    tool_match = re.search(
        r"\[CALL_TOOL:\s*(?P<tool>.*?)\s*\|\s*(?P<param>.*?):\s*(?P<value>.*?)\s*\]",
        response_text,
        re.IGNORECASE | re.DOTALL,
    )

    if tool_match:
        tool_name = tool_match.group("tool").strip().lower()
        tool_value = tool_match.group("value").strip()
        
        if "google_search" in tool_name:
            status_msg = await update.message.reply_text(f"🔍 Searching for: {tool_value}...")
            
            try:
                raw_results = await search_service.search_web(tool_value, max_results=3)
                tool_result = "\n".join([f"Title: {r['title']}\nSnippet: {r['snippet']}" for r in raw_results]) if raw_results else "No results found."
            except Exception as e:
                tool_result = f"Error: {str(e)}"
            
            await state_manager.add_message(user_id=user_id, role="model", content=f"[System Search Output]: {tool_result}")
            
            final_response = await llm_service.generate_response(await state_manager.get_history(user_id))
            await status_msg.delete()
            await state_manager.add_message(user_id=user_id, role="model", content=final_response)
            await update.message.reply_text(final_response)
            return

    await state_manager.add_message(user_id=user_id, role="model", content=response_text)
    await update.message.reply_text(response_text)