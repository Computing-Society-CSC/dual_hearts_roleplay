import gradio as gr
import langgraph.graph as lg
from langchain.schema import AIMessage, HumanMessage
from datetime import datetime
from typing import Dict, Any
from roleplay_bot import workflow  # Import the LangGraph workflow

# Define the chatbot response function
def chatbot_response(message: str, history: list):
    """
    Handles user messages, updates conversation history, and generates bot responses.
    
    Args:
        message (str): The latest user message.
        history (list): The chat history in OpenAI format.

    Returns:
        str: The chatbot's response.
    """
    
    # Convert history from OpenAI format to LangChain format
    formatted_history = []
    for msg in history:
        if msg["role"] == "user":
            formatted_history.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            formatted_history.append(AIMessage(content=msg["content"]))
    
    # Prepare state for LangGraph workflow
    session_id = "session_12345"  # Simulated session ID
    user_id = "user_56789"  # Simulated user ID

    # Prepare conversation memory state
    conversation_memory = {
        "history": formatted_history,
        "last_interaction": datetime.utcnow().isoformat(),
    }

    # Prepare long-term user memory state
    long_term_memory = {
        "player_name": "Aeron",
        "previous_encounters": [
            {"date": "2025-01-25", "location": "Ruins of Eldoria", "topic": "Ancient artifacts"},
            {"date": "2025-01-27", "location": "Mystic Library", "topic": "The lost art of soul-binding"}
        ],
        "relationship_status": "Curious Seeker",
        "player_choices": [
            {"choice": "Accepted Eldrin’s wisdom on fate"},
            {"choice": "Questioned the existence of destiny"}
        ]
    }

    # Define initial bot state
    state = {
        "session_id": session_id,
        "user_id": user_id,
        "message": message,
        "emotional_output": "",
        "rational_output": "",
        "final_response": "",
        "conversation_memory": conversation_memory,
        "long_term_memory": [],
    }

    # Invoke LangGraph workflow
    result = workflow.invoke(state)

    # Extract bot's final response
    bot_response = result["final_response"]

    # Update conversation history
    conversation_memory["history"].append(AIMessage(content=bot_response))

    return bot_response

# Create a Gradio chat interface
chatbot_ui = gr.ChatInterface(
    fn=chatbot_response,
    type="messages",
    title="Role-Playing AI Chatbot",
    description="Engage in immersive storytelling with an AI-driven role-playing character.",
)

# Launch the Gradio UI
if __name__ == "__main__":
    chatbot_ui.launch()
