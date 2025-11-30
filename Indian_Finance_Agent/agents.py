import os
from crewai import Agent, LLM
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools import YahooFinanceNewsTool
from crewai.tools import tool
import yfinance as yf

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize the Xai model via OpenRouter
llm = LLM(
    model="openai/x-ai/grok-4.1-fast:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Define Tools
# search_tool = DuckDuckGoSearchRun()
# Wrapping search tool to ensure compatibility
@tool("Web Search")
def search_tool(query: str):
    """Useful to search the internet for information. Input should be a search query."""
    # Configure for Indian English results to avoid random language results (e.g. Chinese)
    wrapper = DuckDuckGoSearchAPIWrapper(region="in-en", time="d", max_results=5)
    search = DuckDuckGoSearchRun(api_wrapper=wrapper)
    return search.run(query)


class FinanceTools:
    @tool("Stock Price Fetcher")
    def get_stock_price(ticker: str):
        """Useful to get the current stock price of a company. Input should be the stock ticker (e.g. RELIANCE, TCS)."""
        ticker = ticker.strip().upper()
        # Append .NS for NSE if not present and not a US ticker (heuristic)
        if not ticker.endswith(".NS") and not ticker.endswith(".BO"):
             ticker += ".NS"
        
        try:
            stock = yf.Ticker(ticker)
            price = stock.history(period="1d")['Close'].iloc[-1]
            currency = stock.info.get('currency', 'INR')
            return f"The current stock price of {ticker} is {price:.2f} {currency}"
        except Exception as e:
            return f"Error fetching price for {ticker}: {e}"

    @tool("Company Info Fetcher")
    def get_company_info(ticker: str):
        """Useful to get company information and business summary. Input should be the stock ticker."""
        ticker = ticker.strip().upper()
        # Append .NS for NSE if not present
        if not ticker.endswith(".NS") and not ticker.endswith(".BO"):
             ticker += ".NS"

        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            return f"Company: {info.get('longName')}\nSector: {info.get('sector')}\nSummary: {info.get('longBusinessSummary')}"
        except Exception as e:
            return f"Error fetching info for {ticker}: {e}"

# Define Agents
web_researcher = Agent(
    role='Web Researcher',
    goal='Find accurate and up-to-date information on the internet',
    backstory="""You are a skilled web researcher who can find any information online. 
    You are focused on gathering financial news and market trends, specifically for the Indian market.""",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
    llm=llm
)

financial_analyst = Agent(
    role='Financial Analyst',
    goal='Analyze financial data and provide investment insights',
    backstory="""You are an experienced financial analyst specializing in the Indian Stock Market (NSE/BSE). 
    You use stock data and market news to provide detailed financial analysis.""",
    verbose=True,
    allow_delegation=False,
    tools=[FinanceTools.get_stock_price, FinanceTools.get_company_info],
    llm=llm
)
