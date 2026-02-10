import requests
# from langchain_community.llms import Ollama
from langchain_ollama import ChatOllama

# Initialize Ollama LLM
llm = ChatOllama(model="llama3.1:8b", base_url="http://localhost:11434")

# Ask a question
# message = "What is the weather like in mumbai? Make it funny!"
# response = llm.invoke(message)
# print(response)

response = llm.invoke("What is the weather like in mumbai? Make it funny!")

print(response.content)