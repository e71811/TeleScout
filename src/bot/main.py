import os
import sys
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters
load_dotenv()

from src.bot.handlers import start_command, clear_command, handle_message

def validate_environment():
    """
    Handle the edge case: verify that all API keys exist and are valid before the bot starts.
    If something is missing, stop execution cleanly and explain what is missing to the developer.
    """
    critical_keys = ["TELEGRAM_BOT_TOKEN", "GEMINI_API_KEY", "HF_API_KEY"]
    missing_keys = [key for key in critical_keys if not os.getenv(key)]
    
    if missing_keys:
        print("\n❌ CRITICAL CONFIGURATION ERROR:")
        print("--------------------------------------------------")
        print(f"The following required environment keys are missing: {missing_keys}")
        print("Please check your .env file and ensure they are populated properly.")
        print("--------------------------------------------------\n")
        sys.exit(1) 

def main():
    validate_environment()
    
    print("🚀 Initializing TeleScout Bot Application...")
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("clear", clear_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("⚡ Bot configuration completed successfully. Listening for events via Polling...")
    application.run_polling()

if __name__ == "__main__":
    main()