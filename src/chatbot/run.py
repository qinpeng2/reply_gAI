import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.store.memory import InMemoryStore
from chatbot.graph import builder

# Load environment variables
load_dotenv()

def main():
    # Initialize store
    store = InMemoryStore()
    
    # Compile graph with store
    graph = builder.compile(store=store)
    
    # Configure the chatbot to mimic Andrej Karpathy
    config = {"configurable": {"username": "karpathy"}}
    
    # Ask a question
    response = graph.invoke(
        {
            "messages": [
                HumanMessage(content="What are some of your favorite applications of LLMs?")
            ]
        },
        config=config,
    )
    
    # Print the response
    print("\nResponse:", response["messages"][0].content)

if __name__ == "__main__":
    main()
