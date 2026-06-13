import os
import sys
import pathlib
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.request import HTTPXRequest 

workspace_root = pathlib.Path(__file__).resolve().parents[2]
venv_site_packages = workspace_root / ".venv" / "Lib" / "site-packages"
venv_site_packages_unix = workspace_root / ".venv" / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"
for path in (venv_site_packages, venv_site_packages_unix):
    if path.exists() and str(path) not in sys.path:
        sys.path.insert(0, str(path))

load_dotenv()

from src.bot.handlers import start_command, clear_command, handle_message

def validate_environment():
    critical_keys = ["TELEGRAM_BOT_TOKEN", "GEMINI_API_KEY", "HF_API_KEY"]
    missing_keys = [key for key in critical_keys if not os.getenv(key)]
    
    if missing_keys:
        print("\n❌ CRITICAL CONFIGURATION ERROR:")
        print("--------------------------------------------------")
        print(f"Missing required keys: {missing_keys}")
        print("Check your .env file.")
        print("--------------------------------------------------\n")
        sys.exit(1) 

def main():
    validate_environment()
    
    print("🚀 Initializing Bot Application...")
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    request_config = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0)
    
    application = (
        Application.builder()
        .token(token)
        .request(request_config)
        .build()
    )
    
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("clear", clear_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("⚡ Bot configured. Polling started...")
    application.run_polling()

if __name__ == "__main__":
    main()