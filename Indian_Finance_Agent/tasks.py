from crewai import Task
from agents import web_researcher, financial_analyst

def create_research_task(topic: str):
    return Task(
        description=f"Research the latest financial news and market trends for {topic}. Focus on recent events that might affect the stock price.",
        expected_output="A summary of the latest news and trends.",
        agent=web_researcher
    )

def create_analysis_task(topic: str):
    return Task(
        description=f"Analyze the financial health and stock performance of {topic}. Use the stock price tool to get the current price. Combine this with the news research to provide an investment recommendation.",
        expected_output="A detailed financial analysis report with stock price, company info, and investment recommendation.",
        agent=financial_analyst,
        context=[] # Will be filled dynamically if needed, but CrewAI handles sequential context automatically
    )
