import uuid
import os
from datetime import datetime, timezone
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, END, StateGraph
from langgraph.store.base import BaseStore

import chatbot.configuration as configuration
from chatbot.prompts import CHAT_INSTRUCTIONS
from chatbot.utils import get_all_tweets

import sys

def get_tweets2(state: MessagesState, config: RunnableConfig, store: BaseStore) -> dict:
    """Fetch and store recent tweets for a specified Twitter user."""
    # For now, just return empty to move to chat
    return {}

def chat(state: MessagesState, config: RunnableConfig, store: BaseStore) -> dict:
    """Generate a chat response in the style of a specific Twitter user."""
    # Get the configuration
    configurable = configuration.Configuration.from_runnable_config(config)
    username = configurable.username

    # For now, use a simple prompt without tweets
    prompt = f"You are {username}, a well-known figure in AI and machine learning. Respond to the user's questions in your characteristic style."
    
    # Generate a response
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.75)
    msg = llm.invoke([SystemMessage(content=prompt)] + state['messages'])
    return {"messages": [msg]}

def route_to_tweet_loader(state: MessagesState, config: RunnableConfig, store: BaseStore) -> str:
    """Route the workflow based on tweet availability and age."""
    # For now, always go to chat
    return "chat"

sys.path.append("/opt/workspace/playground/reply_gAI/src")
# Create the graph + all nodes
builder = StateGraph(MessagesState, config_schema=configuration.Configuration)
builder.add_node("chat",chat)
builder.add_node("get_tweets2",get_tweets2)
builder.set_conditional_entry_point(route_to_tweet_loader, ["chat", "get_tweets2"])
builder.add_edge("get_tweets2", "chat")
builder.add_edge("chat", END)

# Compile the graph
graph = builder.compile()