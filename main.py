from roleplay_bot import workflow

inputs = {
    "session_id": "session_12345",
    "user_id": "user_56789",
    "message": "Tell me about destiny."
}

result = workflow.invoke(inputs)
print(result["emotional_output"])
print(result["rational_output"])
print("_________________________________")
print(result["final_response"])
