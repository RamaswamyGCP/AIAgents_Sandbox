import sys
from crewai import Crew, Process
from agents import web_researcher, financial_analyst
from tasks import create_research_task, create_analysis_task

def run_crew(topic: str):
    # Create Tasks
    research_task = create_research_task(topic)
    analysis_task = create_analysis_task(topic)
    
    # Create Crew
    finance_crew = Crew(
        agents=[web_researcher, financial_analyst],
        tasks=[research_task, analysis_task],
        process=Process.sequential,
        verbose=True
    )
    
    # Run Crew
    result = finance_crew.kickoff()
    return result

if __name__ == "__main__":
    if len(sys.argv) > 1:
        topic = sys.argv[1]
    else:
        topic = input("Enter the stock or company to analyze (e.g., NVDA): ")
    
    print(f"\nStarting analysis for: {topic}\n")
    result = run_crew(topic)
    print("\n\n########################")
    print("## Analysis Result ##")
    print("########################\n")
    print(result)
