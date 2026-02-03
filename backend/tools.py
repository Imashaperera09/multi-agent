import os
from typing import List, Dict
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv

load_dotenv()

# Mock Inventory Database
MOCK_INVENTORY = [
    {"product": "Semiconductors", "stock_level": 500, "reorder_point": 1000, "status": "At Risk"},
    {"product": "Lithium Batteries", "stock_level": 2000, "reorder_point": 500, "status": "OK"},
    {"product": "Steel Coils", "stock_level": 50, "reorder_point": 200, "status": "Out of Stock"},
    {"product": "Plastic Pellets", "stock_level": 5000, "reorder_point": 1000, "status": "OK"},
]

def get_inventory_status(query: str = "") -> List[Dict]:
    """Returns the current inventory status from the internal database."""
    if query:
        return [item for item in MOCK_INVENTORY if query.lower() in item["product"].lower()]
    return MOCK_INVENTORY

def search_supply_chain_risks(query: str) -> str:
    """Searches for real-time global supply chain disruptions and risks."""
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not tavily_api_key:
        return "MOCK SEARCH RESULT: Major port strike in Long Beach causing 10-day delays. Geopolitical tensions in the Red Sea affecting shipping routes."
    
    search = TavilySearchResults(k=3)
    results = search.run(query)
    return str(results)

def get_logistics_options(route: str) -> str:
    """Returns available logistics mitigation strategies for a specific route."""
    options = {
        "Red Sea": "Reroute via Cape of Good Hope (+12 days, +$2000/container)",
        "Long Beach": "Divert to Port of Oakland or use rail from Vancouver",
        "Suez Canal": "Air freight for critical components, reroute others via South Africa"
    }
    return options.get(route, "Standard shipping routes available; consider air freight for urgent needs.")
