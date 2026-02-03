from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from .agents import app_graph
from .state import ResearchState

app = FastAPI(title="Nexus AI: Global Research & Strategy Engine")

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
    return {"message": "Nexus AI Research Hub is running"}

@app.post("/analyze")
async def analyze_topic(data: RunInput):
    """Triggers the LangGraph workflow to perform deep research."""
    try:
        # Initialize state
        initial_state = {
            "query": data.query,
            "thoughts": [],
            "findings": [],
            "knowledge_hub": [],
            "strategies": [],
            "current_agent": "system",
            "next_step": "research_scout"
        }
        
        # Run the graph
        final_state = app_graph.invoke(initial_state)
        return final_state
    except Exception as e:
        print(f"Error running graph: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat_with_copilot(data: ChatMessage):
    """Allows users to chat with the Research Co-pilot."""
    try:
        from .tools import get_knowledge_context
        from langchain_groq import ChatGroq
        
        context = get_knowledge_context()
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
        
        prompt = f"""
        You are the Nexus AI Research Co-pilot. You help users understand global trends.
        Current Knowledge Context: {context}
        
        User Question: {data.message}
        
        Provide a helpful, professional response in a concise manner.
        """
        
        response = llm.invoke(prompt)
        return {"response": response.content}
    except Exception as e:
        print(f"Error in chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
