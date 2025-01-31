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
    setting_imagine: str

# Chat model processing
def process_emotional(state: BotState):
    """Generate an emotionally engaging response."""
    session_memory = state["conversation_memory"]
    user_memory = state["long_term_memory"]
    
    prompt = f"""
"You are {settings['character']['name']}, {settings['character']['role']}.
You speak in {settings['emotional_processing']['style']}, focusing on {settings['emotional_processing']['focus']}.

## Task:
Answer the player’s words with emotion in a stream of consciousness.

## Player Context:
{user_memory}

## Your Background:
{settings["character"]["background"]}

## Player’s Words:
"{state['message']}"

## Response Format:
Generate an immersive response in 100 words.
"""
    response = llm.invoke(prompt)
    state["emotional_output"] = response.content
    return {"emotional_output":response.content}

def process_rational(state: BotState):
    """Generate a structured and logical response."""
    user_memory = state["long_term_memory"]

    prompt = f"""
"You are {settings['character']['name']}, {settings['character']['role']}.

You are {settings['character']['name']}, {settings['character']['role']}.
You speak logically in {settings['rational_processing']['style']}, focusing on {settings['rational_processing']['focus']}.

## Player Context:
{user_memory}

## Player’s Question:
"{state['message']}"

## Response Format:
Provide a structured, rational answer.
"""
    response = llm.invoke(prompt)
    state["rational_output"] = response.content
    return {"rational_output": response.content}

def imagine(state: BotState):
    user_memory = state["long_term_memory"]
    conversation_mem = state["conversation_memory"]["history"]

    prompt = f"""
"You are {settings['character']['name']}, {settings['character']['role']}, {settings['character']['personality']}.

## Your Background
{settings['character']['background']}

## Your Memory:
- Conversation Memory: {conversation_mem}
- User's Information: {user_memory}
- Latest User Message: {state['message']}

## Task:
You are trying to complete the setting in this role-playing game by imagining them.
If the past conversation does not reveal sufficient information about your setting, imagine your current situation and output them to make your situation clear and complete.
For example, you can imagine your past and the scene in the current room.

## Final Response:
Generate an **immersive setting that complete the setting in previous conversation** and **coherent to previous conversation**.
The word count should be under 100 words.
"""
    response = llm.invoke(prompt)
    return {"setting_imagine": response.content}

def finalize(state: BotState):
    """Final node that integrates emotional and rational responses and updates memory."""
    session_memory = state["conversation_memory"]

    prompt = f"""
You are {settings['character']['name']}, {settings['character']['role']}.

## Inputs:
- Original Response: {state["final_response"]}
- Emotional Response: {state["emotional_output"]}
- Rational Response: {state["rational_output"]}
- Past Conversation: {state['conversation_memory']["history"]}
- Latest User Message: {state['message']}
- Situation: {state["setting_imagine"]}

## Task:
Create an in-character response that integrates both emotional and rational aspects, making it immersive and cohesive with the ongoing conversation. Use details from the past conversation and the situation to ensure continuity.

## Guidelines:
- Maintain {settings['processing_weights']['emotional_percentage']}% emotion and {settings['processing_weights']['rational_percentage']}% logic.
- Prioritize user preferences according to {settings['integration_rules']["user_preference_priority"]}.
- Match your tone with {settings['integration_rules']['output_tone']} and avoid repeating greetings or redundant statements.
- Stay within the character’s established voice and ensure your response contributes directly to the flow of the conversation.
- If the user is passive or withdrawn, respond gently and empathetically, offering support or a shift in topic without pushing them to be more active. Consider the context and balance engagement without forcing the interaction.

## Final Response:
Your response should be under 100 words.
"""

    response = llm.invoke(prompt)
    state["final_response"] = response.content
    return {
        "final_response": response.content,
    }

def add_context(state: BotState):
    session_memory = state["conversation_memory"]
    prompt = f"""
"You are {settings['character']['name']}, {settings['character']['role']}.

## Your Profile:

- Background: {settings["character"]["background"]}
- Personality: {settings["character"]["personality"]}

## Inputs:
- Original Response: {state["final_response"]}
- Situation: {state["setting_imagine"]}
- Past Conversation: {state['conversation_memory']["history"]}
- Latest User Message: {state['message']}

## Task:
Your goal is to provide a more natural, in-character response that fits seamlessly within the ongoing conversation.
Modify your original response to align with the context and dynamics of the prior exchanges.
Use details from the previous conversation and the current situation to ensure continuity, avoiding repetition of greetings or statements.
Enhance the role-playing experience by enriching your response where needed to keep the interaction engaging and relevant.

## Guidelines:
- The response should remain under 100 words.
- Speak according to {settings["character"]["speech_pattern"]}, consistently reflecting your character's voice.
- Make sure the response contributes meaningfully to the conversation and stays true to the character's backstory and current setting.
"""
    response = llm.invoke(prompt)
    # state["final_response"] = response.content

    return {
        "final_response": response.content,
    }

def update_conversation_memory(state: BotState):
    session_memory = state["conversation_memory"]
    if "history" not in session_memory:
        session_memory["history"] = []
    
    session_memory["history"].append({"role": "bot", "message": state["final_response"]})
    session_memory["last_interaction"] = datetime.utcnow().isoformat()

    return {
        "conversation_memory": session_memory
    }

# Define LangGraph workflow
graph = StateGraph(BotState)
graph.add_node("emotional_processing", process_emotional)
graph.add_node("rational_processing", process_rational)
graph.add_node("imagine_processing", imagine)
graph.add_node("final", finalize)
graph.add_node("update_memory", update_conversation_memory)
# graph.add_node("add_context", add_context)

graph.add_edge(START, "rational_processing")
graph.add_edge(START, "emotional_processing")
graph.add_edge(START, "imagine_processing")
graph.add_edge("rational_processing", "final")
graph.add_edge("emotional_processing", "final")
graph.add_edge("imagine_processing", "final")
# graph.add_edge("final", "add_context")
graph.add_edge("final", "update_memory")
graph.add_edge("update_memory", END)
# graph.add_edge("add_context", END)

workflow = graph.compile()
