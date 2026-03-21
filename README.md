# 🌙 AI Bedtime Story Generator

An AI-powered bedtime story generator for children aged 5–10, built with **LangGraph** and **OpenAI**. The app orchestrates multiple AI agents in a structured workflow to create safe, educational, and imaginative stories.

## ✨ Features

- **Content Guardrails** — Automatically screens user input for age-inappropriate topics before any story is generated
- **Smart Research** — Optionally enriches stories with real-world facts via [Tavily](https://tavily.com/) web search when the topic benefits from factual context
- **Iterative Quality Control** — A judge agent reviews each draft for safety, tone, and length, sending it back for rewrites if needed (up to 3 attempts)
- **Multi-Turn Storytelling** — Continue the story by adding new "story beats" across turns, building an evolving narrative with full conversational memory
- **Graceful Failure Handling** — Research failures are handled silently, and a max-retry safety valve prevents infinite loops

## 🏗️ Architecture

The app uses a **LangGraph StateGraph** to orchestrate four specialized nodes:

```
User Input → 🛡️ Guardrail → 📚 Research (optional) → ✍️ Writer ⇄ ⚖️ Judge → Story Output
```

| Node | Role |
|------|------|
| **Guardrail** | Screens input for safety; decides if research is needed |
| **Research** | Fetches real-world facts via Tavily search API |
| **Writer** | Generates a 5–6 paragraph bedtime story using GPT-3.5 |
| **Judge** | Reviews the draft for quality and safety; approves or requests rewrites |

## 📁 Project Structure

```
├── app.py                # Entry point — main CLI loop
├── requirements.txt      # Python dependencies
├── .env                  # API keys (not tracked in git)
└── src/
    ├── state.py          # State schema & Pydantic models
    ├── graph.py          # LangGraph workflow definition
    ├── nodes/
    │   ├── guardrail.py  # Safety & content moderation
    │   ├── research.py   # Web research via Tavily
    │   ├── writer.py     # Story generation
    │   └── judge.py      # Quality review
    └── utils/
        └── tools.py      # Shared LLM & tool instances
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- An [OpenAI API key](https://platform.openai.com/api-keys)
- A [Tavily API key](https://app.tavily.com/)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-bedtime-story-generator.git
   cd ai-bedtime-story-generator
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

### Usage

```bash
python app.py
```

You'll be prompted to enter a story theme. The AI will generate a bedtime story and you can keep adding story beats to continue the adventure, or type `end` to quit.

```
Welcome to the MODULAR AI Story Generator!

What kind of story do you want to hear? a brave kitten who explores the ocean

--- [GUARDRAIL] CHECKING SAFETY... ---
--- [WRITER] GENERATING STORY... ---
--- [JUDGE] REVIEWING STORY... ---

==================================================
--- STORY APPROVED ---
Time: 4.32s

Once upon a time, in a cozy little seaside village...
==================================================

Add a story beat or type 'end': now the kitten meets a friendly dolphin
```

## 🛠️ Tech Stack

- [LangGraph](https://github.com/langchain-ai/langgraph) — Agent orchestration & state management
- [LangChain](https://github.com/langchain-ai/langchain) — LLM framework & tool integrations
- [OpenAI GPT-3.5 Turbo](https://platform.openai.com/) — Language model for story generation & evaluation
- [Tavily](https://tavily.com/) — AI-optimized web search for fact-finding
- [Pydantic](https://docs.pydantic.dev/) — Structured output validation

## 📄 License

MIT
