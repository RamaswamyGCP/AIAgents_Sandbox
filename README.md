# Indian Stock Analyst Agent 📈

An intelligent multi-agent system designed to analyze Indian stocks (NSE/BSE) using AI. It combines web research with financial analysis to provide deep market insights.

## 🚀 Tech Stack

- **Framework**: [CrewAI](https://crewai.com) (Agent Orchestration)
- **LLM**: Xai (Grok-beta) via [OpenRouter](https://openrouter.ai)
- **Frontend**: [Streamlit](https://streamlit.io) & HTML/JS (FastAPI)
- **Observability**: [Arize Phoenix](https://arize.com/phoenix) (Open Source Tracing)
- **Data Source**: `yfinance`, `duckduckgo-search`

## 🛠️ Setup

1.  **Clone the repository**:
    ```bash
    git clone <repo-url>
    cd Indian_Finance_Agent
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**:
    - Copy `.env.example` to `.env`:
      ```bash
      cp .env.example .env
      ```
    - Add your API keys (OpenRouter, etc.).

## 🏃‍♂️ How to Run

### Option 1: Streamlit App (Recommended)
The easiest way to use the agent with a friendly UI.

```bash
streamlit run app.py
```
*Access at `http://localhost:8501`*

### Option 2: FastAPI Backend
Run the backend API directly.

```bash
python api.py
```
*Access at `http://localhost:8000`*

## 🔍 Observability
This project uses **Arize Phoenix** for local tracing.
1.  Start the Phoenix server:
    ```bash
    python -m phoenix.server.main serve
    ```
2.  View traces at `http://localhost:6006`.
