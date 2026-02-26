import requests
from langchain_ollama import ChatOllama
from langchain.messages import (AIMessage, HumanMessage, SystemMessage)

llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0.9
    )

conversation = [
    SystemMessage(content="You are a helpful assistant for question regarding programming."),
    HumanMessage(content="What is python ?"),
    AIMessage(content="Python is a high-level, interpreted programming language known for its simplicity and readability. It supports multiple programming paradigms, including procedural, object-oriented, and functional programming. Python is widely used for web development, data analysis, artificial intelligence, scientific computing, and more."),
    HumanMessage(content="What is the latest version of python ?")
]

response = llm.invoke(conversation)
#print(response)
print(response.content)




