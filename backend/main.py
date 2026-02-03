from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from .agents import app_graph
from .state import SupplyChainState

app = FastAPI(title="Supply Chain Multi-Agent Intelligence API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RunInput(BaseModel):
    query: str

class ChatMessage(BaseModel):
    message: str

@app.get("/")
async def root():
    return {"message": "Supply Chain Multi-Agent AI API is running"}

@app.post("/analyze")
async def analyze_supply_chain(data: RunInput):
    """Triggers the LangGraph workflow to analyze supply chain risks."""
    try:
        # Initialize state
        initial_state = {
            "thoughts": [],
            "disruptions": [],
            "inventory": [],
            "mitigation_plan": [],
            "current_agent": "system",
            "next_step": "risk_sentinel"
        }
        
        # Run the graph
        final_state = app_graph.invoke(initial_state)
        return final_state
    except Exception as e:
        print(f"Error running graph: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat_with_copilot(data: ChatMessage):
    """Allows users to chat with the Supply Chain Co-pilot."""
    try:
        from .tools import get_inventory_status
        from langchain_groq import ChatGroq
        import os
        
        inventory = get_inventory_status()
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
        
        prompt = f"""
        You are the Supply Chain AI Co-pilot. You help users understand global risks and their inventory status.
        Current Inventory Status: {inventory}
        
        User Question: {data.message}
        
        Provide a helpful, professional response in a concise manner. If the user asks about a specific risk, relate it to the inventory if possible.
        """
        
        response = llm.invoke(prompt)
        return {"response": response.content}
    except Exception as e:
        print(f"Error in chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
