
from crewai import Agent, LLM
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from crewai.tools import BaseTool
import yfinance as yf
import os
from dotenv import load_dotenv

load_dotenv()

class SearchTool(BaseTool):
    name: str = "Web Search"
    description: str = "Useful to search the internet for information. Input should be a search query."

    def _run(self, query: str) -> str:
        # Configure for Indian English results
        wrapper = DuckDuckGoSearchAPIWrapper(region="in-en", time="d", max_results=5)
        search = DuckDuckGoSearchRun(api_wrapper=wrapper)
        return search.run(query)

search_tool = SearchTool()

class StockPriceTool(BaseTool):
    name: str = "Stock Price Fetcher"
    description: str = "Useful to get the current stock price of a company. Input should be the stock ticker (e.g. RELIANCE, TCS)."

    def _run(self, ticker: str) -> str:
        ticker = ticker.strip().upper()
        if not ticker.endswith(".NS") and not ticker.endswith(".BO"):
             ticker += ".NS"
        
        try:
            stock = yf.Ticker(ticker)
            history = stock.history(period="1d")
            if history.empty:
                return f"Could not fetch price for {ticker}. It might be delisted or the ticker is incorrect."
            price = history['Close'].iloc[-1]
            currency = stock.info.get('currency', 'INR')
            return f"The current stock price of {ticker} is {price:.2f} {currency}"
        except Exception as e:
            return f"Error fetching price for {ticker}: {e}"

class CompanyInfoTool(BaseTool):
    name: str = "Company Info Fetcher"
    description: str = "Useful to get company information and business summary. Input should be the stock ticker."

    def _run(self, ticker: str) -> str:
        ticker = ticker.strip().upper()
        if not ticker.endswith(".NS") and not ticker.endswith(".BO"):
             ticker += ".NS"

        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            if not info or 'longName' not in info:
                 return f"Could not fetch info for {ticker}. Rate limit might be hit."
            return f"Company: {info.get('longName')}\nSector: {info.get('sector')}\nSummary: {info.get('longBusinessSummary')}"
        except Exception as e:
            return f"Error fetching info for {ticker}: {e}"

stock_price_tool = StockPriceTool()
company_info_tool = CompanyInfoTool()

# Initialize the LLM
llm = LLM(
    model="openai/x-ai/grok-4.1-fast:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# 1. Web Researcher Agent
web_researcher = Agent(
    role='Senior Financial Researcher',
    goal='Research and gather comprehensive information about Indian companies and market trends.',
    backstory="""You are an expert researcher specializing in Indian financial markets. 
    You have a knack for finding the latest news, regulatory updates, and market sentiment 
    regarding NSE and BSE listed companies. You are skilled at using search engines to 
    find accurate and up-to-date information.""",
    verbose=True,
    memory=True,
    tools=[search_tool],
    llm=llm,
    allow_delegation=False
)

# 2. Financial Analyst Agent
financial_analyst = Agent(
    role='Senior Financial Analyst',
    goal='Analyze financial data and provide investment recommendations for Indian stocks.',
    backstory="""You are a seasoned financial analyst with deep expertise in the Indian Stock Market (NSE/BSE). 
    You are known for your ability to interpret financial news, market data, and economic indicators 
    to provide actionable investment insights. You use search tools to find current stock prices 
    and financial reports since you don't have direct access to a terminal.""",
    verbose=True,
    memory=True,
    tools=[stock_price_tool, company_info_tool, search_tool],
    llm=llm,
    allow_delegation=False
)
