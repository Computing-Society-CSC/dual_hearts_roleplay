# from langchain_groq import ChatGroq
# import os

# # Set up API key
# os.environ["GROQ_API_KEY"] = "your groq key"
# llm = ChatGroq(model="llama-3.1-8b-instant")

from langchain_openai import ChatOpenAI
import os

llm = ChatOpenAI(
    api_key="your aliyun key",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-turbo",
    # other params...
)