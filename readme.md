# 🎭 Role-Playing AI Bot

A conversational AI designed for immersive **role-playing experiences**. The bot **remembers past interactions**, **adapts to user choices**, and **responds in character** based on predefined settings.

---

## 📌 Features
✔ **In-Character Responses** – The bot speaks as a defined character with a backstory and personality.  
✔ **Memory System** – Keeps track of **short-term (session-based) and long-term (user-specific) memory**.  
✔ **Balanced Emotional & Logical Processing** – Integrates **storytelling** and **philosophical reasoning**.  
✔ **Dynamic Role-Play Adaptation** – Changes responses based on **past encounters and user choices**.  
✔ **Powered by `LangGraph` & `ChatGroq`** – For structured AI reasoning and chat interaction.  

---

## 🚀 Quick Start

### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/your-username/roleplay-bot.git
cd roleplay-bot
```

### 2️⃣ **Install Dependencies**
Make sure you have Python installed (`>=3.8`), then run:
```bash
pip install -r requirements.txt
```
**Dependencies:**
- `langgraph`
- `langchain_groq`

### 3️⃣ **Set Your API Key**

Create `config.py` according to `config copy.py`. Get a free API key from Groq.

---

## 🛠️ Setting Up Memory System

### **🔹 Initialize Memory Files**
Before running the bot, initialize the **memory system**:
```bash
python initialize_memory.py
```
This creates:
- `settings.json` → Defines character behavior and processing rules.
- `conversation_memory.json` → Stores **session-based chat history**.
- `long_term_memory.json` → Tracks **user-specific details** (past encounters, choices).

---

## 🎮 Running the Bot

### **🔹 Start a Conversation**
Run:
```bash
python main.py
```

Example usage inside `main.py`:
```python
inputs = {
    "session_id": "session_12345",
    "user_id": "user_56789",
    "message": "Tell me about destiny."
}

result = workflow.invoke(inputs)
print(result["final_response"])
```

### **🔹 Expected Output**
```
Ah, Aeron, the seeker returns to the Sage of Veltharion. 
Do you remember the ruins where time whispered its secrets to us? 
Writing, like fate, is a river—flowing where the winds of intent guide it...
```
---

## 📝 Configuring the Character (`settings.json`)

Modify `settings.json` to **change the bot's role, personality, and response style**.

Example:
```json
{
    "character": {
        "name": "Eldrin the Sage",
        "role": "A wandering scholar who offers wisdom to seekers.",
        "speech_pattern": "Uses poetic metaphors, historical references, and rhetorical questions."
    },
    "processing_weights": {
        "emotional_percentage": 60,
        "rational_percentage": 40
    }
}
```
✔ **Change the `"name"` and `"role"`** to define a new character.  
✔ **Modify `"speech_pattern"`** to adjust speaking style.  
✔ **Tweak `"emotional_percentage"` vs `"rational_percentage"`** for different response styles.

---

## 🛠️ Memory System Overview

| File | Purpose |
|------|---------|
| `settings.json` | Defines the bot's character, role, and response balance. |
| `conversation_memory.json` | Stores **session-based chat history** for continuity. |
| `long_term_memory.json` | Remembers **user preferences & past encounters**. |

**🔹 Example Long-Term Memory (`long_term_memory.json`)**
```json
{
    "users": {
        "user_56789": {
            "player_name": "Aeron",
            "previous_encounters": [
                {"date": "2025-01-25", "location": "Ruins of Eldoria", "topic": "Ancient artifacts"}
            ],
            "relationship_status": "Curious Seeker"
        }
    }
}
```
✔ **Remembers the user's character name (`"Aeron"`)**  
✔ **Keeps track of past locations and topics discussed**  

---

## 🔧 Customization

Want a **new role-playing character**? Edit `settings.json` to:
- Create a **sci-fi AI companion**, **medieval knight**, or **steampunk scientist**.
- Change `"speech_pattern"` for **Shakespearean, robotic, or cryptic** tones.
- Adjust `"balance_method"` for a **more emotional or rational character**.

---

## 🎭 Future Enhancements
🔹 **NPC Relationship Tracking** – Change dialogue based on **player-NPC trust levels**.  
🔹 **Multi-Character Mode** – Allow switching **between different personalities** dynamically.  
🔹 **Quest System Integration** – Create an **interactive storytelling adventure**.  

---

## 📜 License
MIT License. Feel free to modify and expand the project!

---

## 🤝 Contributions
Got ideas to improve the bot? Open an **issue** or submit a **pull request**! 🚀

