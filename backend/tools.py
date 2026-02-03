import os
from typing import List, Dict
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv

load_dotenv()

# Mock Knowledge Base
KNOWLEDGE_BASE = [
    {"topic": "Artificial Intelligence", "depth_score": 85, "status": "Comprehensive"},
    {"topic": "Quantum Computing", "depth_score": 30, "status": "Needs Update"},
    {"topic": "Green Energy", "depth_score": 60, "status": "Under-analyzed"},
    {"topic": "Space Exploration", "depth_score": 45, "status": "Under-analyzed"},
]

def get_knowledge_context(query: str = "") -> List[Dict]:
    """Returns the current knowledge context from the internal database."""
    if query:
        return [item for item in KNOWLEDGE_BASE if query.lower() in item["topic"].lower()]
    return KNOWLEDGE_BASE

def perform_deep_search(query: str) -> str:
    """Performs a deep web search via Tavily for the given query."""
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not tavily_api_key:
        print(f"DEBUG: Tavily API key missing. Simulating research for: {query}")
        # Use Groq to simulate research results if Tavily is missing
        from langchain_groq import ChatGroq
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
        sim_prompt = f"Provide 3-5 realistic, detailed search results for the research query: '{query}'. Include titles, descriptions, and mock URLs."
        res = llm.invoke(sim_prompt)
        return res.content
    
    search = TavilySearchResults(k=5)
    results = search.run(query)
    return str(results)
