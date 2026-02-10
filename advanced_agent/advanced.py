from dataclasses import dataclass
from pyexpat.errors import messages
import requests
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.tools import tool

@tool("get_weather", description="Get the current weather for a given location.",   return_direct=False)
def get_weather(city: str):
    response = requests.get(f"https://wttr.in/{city}?format=j1")
    return response.json()

agent = create_agent(
    model=ChatOllama(model="llama3.1:8b"),
    tools=[get_weather],
    system_prompt=("you are a helpful assistant that provides weather information in a humorous way. Always use the get_weather tool for city questions. Return only one short humorous sentence. ")
        
)

# response = agent.invoke({
#     "messages": [
#         {
#             "role": "user",
#             "content": "Weather tomorrow in Madurai. Make it funny and short.",
#         }
#     ]   
# })


# print(response["messages"][-1].content)

for chunk in agent.stream({
    "messages": [
        {
            "role": "user",
            "content": "Weather tomorrow in Madurai. Make it funny and short.",
        }
    ]
}):
    if "messages" in chunk:
        print(chunk["messages"][-1].content, end="", flush=True)
