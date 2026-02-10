import requests
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama   # NEW import

load_dotenv()


@tool("get_weather")
def get_weather(city: str):
    """Get the current weather for a given location."""
    response = requests.get(f"https://wttr.in/{city}?format=j1")
    return response.json()


# Create LLM object (NOT string)
llm = ChatOllama(model="llama3.1:8b")


agent = create_agent(
    model=llm,   # <-- IMPORTANT change
    tools=[get_weather],
    system_prompt=(
    "You are a funny weather assistant.\n"
    "ALWAYS use the weather tool for city questions.\n"
    "Return ONLY one short humorous sentence.\n"
    "Never explain JSON, data, or structure."
)

)

response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Weather tomorrow in Madurai. Make it funny and short.",
            }
        ]
    }
)
print(response) # This will print the full response object, which includes metadata and the message content.
print(response["messages"][-1].content) # This will print just the content of the last message, which is the agent's response.
