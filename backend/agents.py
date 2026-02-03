import os
import datetime
from typing import Dict, List
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from .state import SupplyChainState, AgentThought
from .tools import search_supply_chain_risks, get_inventory_status, get_logistics_options
from dotenv import load_dotenv

load_dotenv()

# Initialize LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

def risk_sentinel(state: SupplyChainState):
    """Monitors global risks and disruptions."""
    print("--- RISK SENTINEL ---")
    
    query = "current global supply chain disruptions 2024"
    search_results = search_supply_chain_risks(query)
    
    prompt = f"""
    You are the Risk Sentinel. Analyze the following search results and identify key supply chain disruptions.
    Search Results: {search_results}
    
    Format your response as a JSON list of disruptions with: type, location, severity, description, source.
    Also include a 'thought' explaining your reasoning.
    """
    
    response = llm.invoke(prompt)
    # In a real app, we'd parse the JSON from response.content
    # For now, let's mock the extraction logic for simplicity in this demo
    
    thought = AgentThought(
        agent="Risk Sentinel",
        thought="Identified major port congestion and geopolitical tensions affecting trade routes.",
        timestamp=str(datetime.datetime.now())
    )
    
    # Example extracted data
    disruptions = [
        {
            "id": "1",
            "type": "Geopolitical",
            "location": "Red Sea",
            "severity": "High",
            "description": "Shipping delays due to maritime security alerts.",
            "source": "Tavily Search"
        }
    ]
    
    return {
        "thoughts": [thought],
        "disruptions": disruptions,
        "current_agent": "Risk Sentinel",
        "next_step": "inventory_analyst"
    }

def inventory_analyst(state: SupplyChainState):
    """Analyzes inventory health in context of identified risks."""
    print("--- INVENTORY ANALYST ---")
    
    inventory = get_inventory_status()
    
    thought = AgentThought(
        agent="Inventory Analyst",
        thought=f"Checking stock levels for products likely affected by {state['disruptions'][0]['location']} disruption.",
        timestamp=str(datetime.datetime.now())
    )
    
    return {
        "thoughts": [thought],
        "inventory": inventory,
        "current_agent": "Inventory Analyst",
        "next_step": "logistics_optimizer"
    }

def logistics_optimizer(state: SupplyChainState):
    """Generates mitigation strategies."""
    print("--- LOGISTICS OPTIMIZER ---")
    
    risk_location = state['disruptions'][0]['location']
    options = get_logistics_options(risk_location)
    
    thought = AgentThought(
        agent="Logistics Optimizer",
        thought=f"Developing mitigation plan for {risk_location} disruption using {options}.",
        timestamp=str(datetime.datetime.now())
    )
    
    mitigation_plan = [
        {"action": "Reroute shipments via Cape of Good Hope", "priority": "High", "impact": "Prevents stockouts but increases lead time by 12 days."},
        {"action": "Expedite semiconductor orders via air freight", "priority": "Medium", "impact": "Reduces lead time for critical parts."}
    ]
    
    return {
        "thoughts": [thought],
        "mitigation_plan": mitigation_plan,
        "current_agent": "Logistics Optimizer",
        "next_step": "complete"
    }

# Define the Graph
workflow = StateGraph(SupplyChainState)

workflow.add_node("risk_sentinel", risk_sentinel)
workflow.add_node("inventory_analyst", inventory_analyst)
workflow.add_node("logistics_optimizer", logistics_optimizer)

workflow.set_entry_point("risk_sentinel")
workflow.add_edge("risk_sentinel", "inventory_analyst")
workflow.add_edge("inventory_analyst", "logistics_optimizer")
workflow.add_edge("logistics_optimizer", END)

app_graph = workflow.compile()
