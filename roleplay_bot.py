import os
from datetime import datetime
from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, START, END
from config import llm  # Ensure you have llm configured in a separate config.py file
import json

# Load settings from JSON
SETTINGS_FILE = "settings.json"
def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

settings = load_json(SETTINGS_FILE)

# Define Bot State
class BotState(TypedDict):
    session_id: str
    user_id: str
    message: str
    emotional_output: str
    rational_output: str
    final_response: str
    conversation_memory: Dict[str, Any]  # Holds session-based memory
    long_term_memory: List[str]  # Holds user-specific long-term memory

# Chat model processing
def process_emotional(state: BotState):
    """Generate an emotionally engaging response."""
    session_memory = state["conversation_memory"]
    
    prompt = f"""
"You are {settings['character']['name']}, {settings['character']['role']}.
You speak in {settings['character']['speech_pattern']}.

## Task:
Answer the player’s words with emotion and depth.

## Player’s Words:
"{state['message']}"

## Response Format:
Generate a poetic, immersive response.
"""
    response = llm.invoke(prompt)
    state["emotional_output"] = response.content
    return {"emotional_output":response.content}

def process_rational(state: BotState):
    """Generate a structured and logical response."""
    user_memory = state["long_term_memory"]

    prompt = f"""
"You are {settings['character']['name']}, {settings['character']['role']}.
You analyze the world through logic and wisdom.

## Player Context:
{user_memory}

## Player’s Question:
"{state['message']}"

## Response Format:
Provide a structured, philosophical answer.
"""
    response = llm.invoke(prompt)
    state["rational_output"] = response.content
    return {"rational_output": response.content}

def finalize(state: BotState):
    """Final node that integrates emotional and rational responses and updates memory."""
    session_memory = state["conversation_memory"]

    prompt = f"""
"You are {settings['character']['name']}, {settings['character']['role']}.

## Inputs:
- Emotional Response: {state["emotional_output"]}
- Rational Response: {state["rational_output"]}
- Past Conversation: {state['conversation_memory']}

## Task:
Integrate these into a seamless, immersive role-playing response.

## Integration Guidelines:
- Maintain {settings['processing_weights']['emotional_percentage']}% emotion and {settings['processing_weights']['rational_percentage']}% logic.
- Ensure coherence with the character’s tone.
- Adapt responses dynamically based on the **player’s previous choices**.

## Final Response:
Generate an **in-character response** that is consistent to your setting and suitable in a conversation. The word count should be under 100 words.
"""
    response = llm.invoke(prompt)
    state["final_response"] = response.content

    # ✅ Update memory AFTER generating the final response
    # Update conversation history
    if "history" not in session_memory:
        session_memory["history"] = []
    
    session_memory["history"].append({"role": "bot", "message": state["final_response"]})
    session_memory["last_interaction"] = datetime.utcnow().isoformat()

    return {
        "final_response": response.content,
        "conversation_memory": session_memory
    }

# Define LangGraph workflow
graph = StateGraph(BotState)
graph.add_node("emotional_processing", process_emotional)
graph.add_node("rational_processing", process_rational)
graph.add_node("final", finalize)

graph.add_edge(START, "rational_processing")
graph.add_edge(START, "emotional_processing")
graph.add_edge("rational_processing", "final")
graph.add_edge("emotional_processing", "final")
graph.add_edge("final", END)

workflow = graph.compile()
