from roleplay_bot import workflow

# Example input
state_input = {
    "session_id": "session_12345",
    "user_id": "user_56789",
    "message": "Let's play a game.",
    "emotional_output": "",
    "rational_output": "",
    "final_response": "",
    "conversation_memory": {
        "history": [
            {"role": "user", "message": "What is fate?"},
            {"role": "bot", "message": "Fate is a river, ever flowing..."}
        ],
        "last_interaction": "2025-01-29T12:34:56"
    },
    "long_term_memory": "Player's name is Richard."
}

# Invoke workflow
result = workflow.invoke(state_input)

# Print final response
print(result["final_response"])

