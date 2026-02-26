from llm import get_llm
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate


def main():
    print("=" * 50)
    print("Welcome to the CLI chatbot!")
    print("=" * 50)


    while True:
        mode = input("choose answer mode (1: normal, 2: One-line): ").strip()
        if mode in ["1", "2"]:
            one_line_mode = (mode == "2")
            break
        print("Invalid input. Please enter 1 or 2.")

    print("\n Type \"quit to exit the chatbot.\n")

    llm = get_llm()
    memory = ConversationBufferMemory()

    if one_line_mode:
        template = """The following is a conversation between a human and an AI assistant. The assistant provides concise, one-line answers to the human's questions.

current conversation:
{history}
human: {input}
AI:"""
    else:
        template = """The following is a conversation between a human and an AI assistant. The assistant provides detailed answers to the human's questions.

current conversation:
{history}
human: {input}
AI:"""

    prompt = PromptTemplate(
        input_variables=["history", "input"],
        template=template,
    )
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=prompt,
    )


    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "quit":
            print("Goodbye!")
            break
        if not user_input:
            continue

        try:
            response = conversation.predict(input=user_input)
            print(f"AI: {response}")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

