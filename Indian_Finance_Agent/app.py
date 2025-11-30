import streamlit as st
import os
from dotenv import load_dotenv
import phoenix as px
from openinference.instrumentation.crewai import CrewAIInstrumentor
import nest_asyncio
import socket
import time
import sys

# Apply nest_asyncio
nest_asyncio.apply()

# Load environment variables
load_dotenv()

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

@st.cache_resource
def instrument_crewai():
    CrewAIInstrumentor().instrument()

instrument_crewai()

# Import agents and tasks AFTER instrumentation
from agents import web_researcher, financial_analyst
from tasks import create_research_task, create_analysis_task
from crewai import Crew, Process

phoenix_url = "http://localhost:6006"

st.set_page_config(page_title="Indian Stock Analyst", page_icon="📈", layout="wide")

st.title("📈 Indian Stock Analyst Agent")
st.markdown("Deep market insights for NSE/BSE stocks powered by AI Agents.")

with st.sidebar:
    st.header("About")
    st.markdown("""
    This application uses **CrewAI** to orchestrate two AI agents:
    1.  **Web Researcher**: Finds the latest financial news and trends.
    2.  **Financial Analyst**: Analyzes stock data and provides investment recommendations.
    
    **Model**: Xai (Grok) via OpenRouter
    """)
    
    st.divider()
    st.header("🔍 Observability")
    st.markdown(f"[Open Phoenix UI]({phoenix_url})")
    if not is_port_in_use(6006):
        st.warning("Phoenix server not detected.")
        st.code("python -m phoenix.server.main serve", language="bash")
        st.info("Run the above command in a terminal to enable observability.")
    else:
        st.success("Phoenix connected!")
        st.info("Click above to view agent traces and evaluations locally.")

company = st.text_input("Enter Company Ticker (e.g., RELIANCE, TCS, HDFCBANK):")

if st.button("Analyze"):
    if not company:
        st.error("Please enter a company ticker.")
    else:
        with st.spinner(f"Analyzing {company}... This may take a minute."):
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
                
                st.success("Analysis Complete!")
                st.markdown("### 📊 Analysis Report")
                st.markdown(result)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
