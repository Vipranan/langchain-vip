import requests
from langchain.chat_models import ChatOllama

model = ChatOllama(
    model="llama3.1:8b",
    temperature=0.7,
)

response = model.invoke('hello, what is python ?')

print(response)