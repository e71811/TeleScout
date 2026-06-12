# Telegram AI Assistant Bot

[cite_start]An advanced, production-ready Telegram Bot serving as a personal AI assistant, built for the Applied Materials GenAI Infrastructure team take-home exercise[cite: 4, 5].

## Core Architecture Overview
[cite_start]The project follows a strict **Separation of Concerns (Loose Coupling)** architecture[cite: 60]:
- **Handler Layer:** Manages incoming Telegram events and routing.
- [cite_start]**State Manager Layer:** Handles asynchronous, multi-turn conversation memory per user[cite: 57].
- [cite_start]**Service Layer:** Independent modules for LLM reasoning, web search pipelines, and image generation[cite: 49, 54, 55].

---

## 🗺️ Project Roadmap

- [x] **Phase 0: Project Initialization & Infrastructure Setup**
- [ ] **Phase 1: Async Conversation State Manager (Multi-turn Memory)**
- [ ] **Phase 2: Independent AI Services (LLM, DuckDuckGo Deep Search, Image API)**
- [ ] **Phase 3: Telegram Handlers & Core Integration**
- [ ] **Phase 4: Live Deployment & Final Documentation**