import requests
from langchain_community.llms import Ollama

# Initialize Ollama LLM
llm = Ollama(model="qwen2.5:7b", base_url="http://localhost:11434")

# Ask a question
message = "What is the weather like in madurai? Make it funny!"
response = llm.invoke(message)
print(response)