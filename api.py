from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crewai import Crew, Process
from agents import web_researcher, financial_analyst
from tasks import create_research_task, create_analysis_task
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Finance Agent API", description="API for AI-powered financial analysis")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CompanyRequest(BaseModel):
    company: str

@app.post("/analyze")
async def analyze_company(request: CompanyRequest):
    company = request.company
    if not company:
        raise HTTPException(status_code=400, detail="Company name is required")

    try:
        # Create Tasks
        research = create_research_task(company)
        analysis = create_analysis_task(company)

        # Create Crew
        crew = Crew(
            agents=[web_researcher, financial_analyst],
            tasks=[research, analysis],
            process=Process.sequential,
            verbose=True
        )

        # Run the crew
        result = crew.kickoff()
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
