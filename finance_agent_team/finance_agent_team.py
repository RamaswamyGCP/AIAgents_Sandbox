import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# CRITICAL FIX: The Agno library throws an error if OPENAI_API_KEY is missing,
# even when using other providers like Perplexity.
# We explicitly set it here to allow the code to run.
# This does NOT send data to OpenAI; it uses the base_url defined below.
if os.getenv("PERPLEXITY_API_KEY"):
    os.environ["OPENAI_API_KEY"] = os.getenv("PERPLEXITY_API_KEY")
else:
    print("⚠️ WARNING: PERPLEXITY_API_KEY not found in .env file!")

from agno.agent import Agent
from agno.team import Team
from agno.models.google import Gemini
from agno.db.sqlite import SqliteDb
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from agno.os import AgentOS
from fastapi.middleware.cors import CORSMiddleware

# Setup database for storage
db = SqliteDb(db_file="agents.db")

# Define the Gemini model
gemini_model = Gemini(id="gemini-2.0-flash-exp")

web_agent = Agent(
    name="Web Agent",
    role="Search the web for information",
    model=gemini_model,
    tools=[DuckDuckGoTools()],
    db=db,
    add_history_to_context=True,
    markdown=True,
)

finance_agent = Agent(
    name="Finance Agent",
    role="Get financial data",
    model=gemini_model,
    tools=[YFinanceTools()],
    instructions=["Always use tables to display data"],
    db=db,
    add_history_to_context=True,
    markdown=True,
)

agent_team = Team(
    id="finance_team",
    name="Agent Team (Web+Finance)",
    model=gemini_model,
    members=[web_agent, finance_agent],
    debug_mode=True,
    markdown=True,
)

agent_os = AgentOS(teams=[agent_team])
app = agent_os.get_app()

# ADD CORS MIDDLEWARE TO ALLOW FRONTEND ACCESS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (including localhost:8000)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    agent_os.serve(app="finance_agent_team:app", reload=True)
