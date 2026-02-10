from langchain_ollama import OllamaLLM

llm = OllamaLLM(
    model="llama3.1:8b",
    base_url="http://localhost:11434",
    temperature=0.7,
)

response = llm.invoke("give me the weather forecast for tomorrow in madurai, make it funny!, make it short and concise")
print(response)
