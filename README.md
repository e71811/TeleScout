# 🤖 TeleScout - Applied AI Telegram Bot

An advanced, asynchronous multi-turn Telegram assistant built with Python. Powered by Google Gemini Pro, duckduckgo_search (DDGS), and Hugging Face FLUX.1 image generation fallback mechanics.

## Core Architecture Overview
The project follows a strict **Separation of Concerns (Loose Coupling)** architecture:
- **Handler Layer:** Manages incoming Telegram events, user commands, and text/image routing.
- **State Manager Layer:** Handles asynchronous, multi-turn conversation memory strictly isolated per user.
- **Service Layer:** Independent modules for LLM reasoning, web search pipelines, link scraping, and image generation.

## 🗺️ Project Roadmap

- [x] **Phase 0: Project Initialization & Infrastructure Setup**
- [x] **Phase 1: Async Conversation State Manager (Multi-turn Memory)**
- [x] **Phase 2: Independent AI Services (LLM, DuckDuckGo Search, Scraper, Image API)** 
- [x] **Phase 3: Telegram Bot API Integration & Command Handlers**
- [ ] **Phase 4: Advanced Tool Integration & Deployment Execution**

## ⚙️ How to Run the Bot Locally
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_google_gemini_token
HF_API_KEY=your_huggingface_token