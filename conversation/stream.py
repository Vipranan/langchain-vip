import requests
from langchain_ollama import ChatOllama

model = ChatOllama(
    model="llama3.1:8b",
    temperature=0.7,
)
for chunk in model.stream('hello, what is python ?'):
    print(chunk.text, end='', flush=True)