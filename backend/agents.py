import os
import datetime
import json
from typing import Dict, List
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from .state import ResearchState, AgentThought
from .tools import perform_deep_search, get_knowledge_context
from dotenv import load_dotenv

load_dotenv()

# Initialize LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)

def research_scout(state: ResearchState):
    """Performs deep research on the query and extracts findings."""
    print("--- RESEARCH SCOUT ---")
    
    query = state.get("query") or "global research trends"
    print(f"Searching for: {query}")
    search_results = perform_deep_search(query)
    
    prompt = f"""
    You are a Research Scout. Analyze the following search results for the query: "{query}"
    
    Search Results: {search_results}
    
    Extract the top 3 most significant findings. 
    Return ONLY a JSON list of objects with keys: "id", "category", "title", "description", "source".
    Example: [{{"id": "1", "category": "Tech", "title": "Example", "description": "Desc", "source": "Source"}}]
    """
    
    try:
        response = llm.invoke(prompt)
        # Clean response for JSON parsing
        content = response.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        findings = json.loads(content)
    except Exception as e:
        print(f"Error parsing findings: {e}")
        findings = [{"id": "1", "category": "Error", "title": "Search Failed", "description": "Could not parse research results.", "source": "System"}]

    thought = AgentThought(
        agent="Research Scout",
        thought=f"Synthesized research for: {query}. Identified {len(findings)} key trends from web sources.",
        timestamp=str(datetime.datetime.now())
    )
    
    return {
        "thoughts": [thought],
        "findings": findings,
        "current_agent": "Research Scout",
        "next_step": "critical_analyst"
    }

def critical_analyst(state: ResearchState):
    """Analyzes findings against existing knowledge."""
    print("--- CRITICAL ANALYST ---")
    
    findings_str = json.dumps(state.get("findings", []))
    context = get_knowledge_context()
    
    thought = AgentThought(
        agent="Critical Analyst",
        thought="Cross-referencing web findings with internal baseline knowledge to validate importance.",
        timestamp=str(datetime.datetime.now())
    )
    
    return {
        "thoughts": [thought],
        "knowledge_hub": context,
        "current_agent": "Critical Analyst",
        "next_step": "strategy_advisor"
    }

def strategy_advisor(state: ResearchState):
    """Generates strategic insights based on findings."""
    print("--- STRATEGY ADVISOR ---")
    
    findings = state.get("findings", [])
    findings_str = json.dumps(findings)
    
    prompt = f"""
    You are a Strategy Advisor. Based on these research findings:
    {findings_str}
    
    Develop 2 strategic recommendations.
    Return ONLY a JSON list of objects with keys: "recommendation", "impact", "confidence".
    Ensure the recommendations are directly related to the findings.
    """
    
    try:
        response = llm.invoke(prompt)
        content = response.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
            
        strategies = json.loads(content)
    except Exception as e:
        print(f"Error parsing strategies: {e}")
        strategies = [{"recommendation": "Manual Review Required", "impact": "Inconclusive data synthesis.", "confidence": "Low"}]

    thought = AgentThought(
        agent="Strategy Advisor",
        thought="Generated strategic roadmap based on synthesized insights. Ready for deployment.",
        timestamp=str(datetime.datetime.now())
    )
    
    return {
        "thoughts": [thought],
        "strategies": strategies,
        "current_agent": "Strategy Advisor",
        "next_step": "complete"
    }

# Define the Graph
workflow = StateGraph(ResearchState)

workflow.add_node("research_scout", research_scout)
workflow.add_node("critical_analyst", critical_analyst)
workflow.add_node("strategy_advisor", strategy_advisor)

workflow.set_entry_point("research_scout")
workflow.add_edge("research_scout", "critical_analyst")
workflow.add_edge("critical_analyst", "strategy_advisor")
workflow.add_edge("strategy_advisor", END)

app_graph = workflow.compile()
