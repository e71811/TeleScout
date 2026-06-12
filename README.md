# Telegram AI Assistant Bot

An advanced, production-ready Telegram Bot serving as a personal AI assistant, built for the Applied Materials GenAI Infrastructure team take-home exercise.

## Core Architecture Overview
The project follows a strict **Separation of Concerns (Loose Coupling)** architecture:
- **Handler Layer:** Manages incoming Telegram events and routing.
- **State Manager Layer:** Handles asynchronous, multi-turn conversation memory per user.
- **Service Layer:** Independent modules for LLM reasoning, web search pipelines, and image generation.

---

## 🗺️ Project Roadmap

- [x] **Phase 0: Project Initialization & Infrastructure Setup**
- [x] **Phase 1: Async Conversation State Manager (Multi-turn Memory)**
- [ ] **Phase 2: Independent AI Services (LLM, DuckDuckGo Deep Search, Image API)**
- [ ] **Phase 3: Telegram Handlers & Core Integration**
- [ ] **Phase 4: Live Deployment & Final Documentation**