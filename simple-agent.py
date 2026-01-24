import requests
from dotenv import load_dotenv
import os
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()


@tool('get_weather', description="Get the current weather for a given city.", return_direct=False)
def get_weather(city:str):
    response = requests.get(f"https://wttr.in/{city}?format=j1")
    return response.json()

agent = create_agent(
    model="gemini-1.5-flash",
    tools=[get_weather],
    system_prompt="You are a helpful assistant that provides weather information, who always cracks jokes and is humorous while remaining helpful."

)

response = agent.invoke({
    'messages' : [
        {"role": "user", "content": "What is the weather like in New York City?"}
    ]
    
})
print(response['messages'] [-1]['content'])
print(response)