from crewai import Crew, Process
from agents import web_researcher, financial_analyst
from tasks import create_research_task, create_analysis_task
import os
from dotenv import load_dotenv

load_dotenv()

def test_agents():
    company = "INFY"
    print(f"Testing agents with company: {company}")

    try:
        # Create Tasks
        print("Creating tasks...")
        research = create_research_task(company)
        analysis = create_analysis_task(company)

        # Create Crew
        print("Creating crew...")
        crew = Crew(
            agents=[web_researcher, financial_analyst],
            tasks=[research, analysis],
            process=Process.sequential,
            verbose=True
        )

        # Run the crew
        print("Kicking off crew...")
        result = crew.kickoff()
        
        print("\n\n########################")
        print("## ANALYSIS RESULT ##")
        print("########################\n")
        print(result)
        print("\n########################")
        print("Test Completed Successfully")

    except Exception as e:
        print(f"Error running agents: {e}")

if __name__ == "__main__":
    test_agents()
