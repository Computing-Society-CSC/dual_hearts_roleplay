from langchain_groq import ChatGroq
import os

# Set up API key
os.environ["GROQ_API_KEY"] = "your groq key"
llm = ChatGroq(model="llama-3.1-8b-instant")