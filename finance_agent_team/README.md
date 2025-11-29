# Finance Agent Team

A multi-agent system using `agno` and Google Gemini to research stocks and provide financial data.

## Features
- **Web Agent**: Searches the web for information using DuckDuckGo.
- **Finance Agent**: Fetches stock data using YFinance.
- **Team**: Coordinates between agents to answer complex queries.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Variables**:
    Create a `.env` file with your Google API Key:
    ```bash
    GOOGLE_API_KEY=your_google_api_key_here
    ```

3.  **Run Backend**:
    ```bash
    python finance_agent_team.py
    ```

4.  **Run Frontend**:
    ```bash
    python serve_frontend.py
    ```
    Then open `http://localhost:8000`.
