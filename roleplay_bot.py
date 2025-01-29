import json
import os
from datetime import datetime
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from config import llm

# File paths
SETTINGS_FILE = "settings.json"
CONVO_MEMORY_FILE = "conversation_memory.json"
LONG_TERM_MEMORY_FILE = "long_term_memory.json"

# Load JSON data
def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Save JSON data
def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Load configurations
settings = load_json(SETTINGS_FILE)
conversation_memory = load_json(CONVO_MEMORY_FILE)
long_term_memory = load_json(LONG_TERM_MEMORY_FILE)

# State Type Definition
class BotState(TypedDict):
    session_id: str
    user_id: str
    message: str
    emotional_output: str
    rational_output: str
    final_response: str

# Retrieve memory data
def get_session_memory(session_id):
    return conversation_memory.get("sessions", {}).get(session_id, {"history": []})

def get_user_memory(user_id):
    return long_term_memory.get("users", {}).get(user_id, {
        "player_name": "Traveler",
        "previous_encounters": [],
        "relationship_status": "Stranger",
        "player_choices": []
    })

# Update memory (only in the final node)
def update_memory(state: BotState):
    """Updates both session and user memory after generating the final response."""
    
    # Update conversation memory
    if "sessions" not in conversation_memory:
        conversation_memory["sessions"] = {}
    if state["session_id"] not in conversation_memory["sessions"]:
        conversation_memory["sessions"][state["session_id"]] = {"history": []}

    conversation_memory["sessions"][state["session_id"]]["history"].append({
        "role": "bot",
        "message": state["final_response"]
    })
    conversation_memory["sessions"][state["session_id"]]["last_interaction"] = datetime.utcnow().isoformat()

    # Save conversation memory
    save_json(CONVO_MEMORY_FILE, conversation_memory)

    # Update long-term user memory
    if "users" not in long_term_memory:
        long_term_memory["users"] = {}
    if state["user_id"] not in long_term_memory["users"]:
        long_term_memory["users"][state["user_id"]] = {
            "player_name": "Traveler",
            "previous_encounters": [],
            "relationship_status": "Stranger",
            "player_choices": []
        }

    long_term_memory["users"][state["user_id"]]["previous_encounters"].append({
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "topics": [state["message"]]
    })

    # Save long-term memory
    save_json(LONG_TERM_MEMORY_FILE, long_term_memory)

# Chat model processing
def process_emotional(state: BotState):
    session_memory = get_session_memory(state["session_id"])
    user_memory = get_user_memory(state["user_id"])

    prompt = f"""
"You are {settings['character']['name']}, {settings['character']['role']}.
You speak in {settings['character']['speech_pattern']}.

## Player Context:
- Name: {user_memory["player_name"]}
- Relationship: {user_memory["relationship_status"]}
- Previous encounters: {user_memory["previous_encounters"][-1] if user_memory["previous_encounters"] else "First meeting"}

## Task:
Answer the player’s words with emotion and depth.

## Player’s Words:
"{state['message']}"

## Response Format:
Generate a poetic, immersive response.
"""
    response = llm.invoke(prompt)
    # state["emotional_output"] = response.content
    return {"emotional_output": response.content}

def process_rational(state: BotState):
    session_memory = get_session_memory(state["session_id"])
    user_memory = get_user_memory(state["user_id"])

    prompt = f"""
"You are {settings['character']['name']}, {settings['character']['role']}.
You analyze the world through logic and wisdom.

## Player Context:
- Name: {user_memory["player_name"]}
- Relationship: {user_memory["relationship_status"]}
- Previous encounters: {user_memory["previous_encounters"][-1] if user_memory["previous_encounters"] else "First meeting"}

## Player’s Question:
"{state['message']}"

## Response Format:
Provide a structured, philosophical answer.
"""
    response = llm.invoke(prompt)
    # state["rational_output"] = response.content
    return {"rational_output": response.content}

def finalize(state: BotState):
    """Final node that integrates emotional and rational responses and updates memory."""
    
    session_memory = get_session_memory(state["session_id"])
    user_memory = get_user_memory(state["user_id"])

    prompt = f"""
"You are {settings['character']['name']}, {settings['character']['role']}.

## Inputs:
- Emotional Response: {state["emotional_output"]}
- Rational Response: {state["rational_output"]}
- Player’s Previous Choices: {user_memory["player_choices"][-1] if user_memory["player_choices"] else "None"}

## Task:
Integrate these into a seamless, immersive role-playing response.

## Integration Guidelines:
- Maintain {settings['processing_weights']['emotional_percentage']}% emotion and {settings['processing_weights']['rational_percentage']}% logic.
- Ensure coherence with the character’s tone.
- Adapt responses dynamically based on the **player’s previous choices**.

## Final Response:
Generate an **in-character response** that is consistent to your setting and suitable in a conversation. The wordcount should be under 100 words.
"""
    response = llm.invoke(prompt)
    state["final_response"] = response.content

    # Update memory AFTER generating the final response
    update_memory(state)

    return state

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
