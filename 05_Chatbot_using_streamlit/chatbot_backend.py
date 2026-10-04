from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv(override=True)
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
print('Key loaded:', bool(GROQ_API_KEY))



llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    api_key=GROQ_API_KEY
)


# define state
from langgraph.graph.message import add_messages
class ChatState(TypedDict):
    
    """ add_message it is reducer (when we define any state then state has a charector which is
     it delete the previous messg and only hold new message but we want to keep every message so
     for that we use reduceer)"""
    messages: Annotated[list[BaseMessage], add_messages]


# creating fun 
def chat_node(state: ChatState):

    # take user query from state
    messages = state['messages']

    # send to llm
    responce = llm.invoke(messages)

    # responce store in state
    return {'messages': [responce]}    




# define graph
graph = StateGraph(ChatState)

# add node
graph.add_node('chat_node', chat_node)

# add edges
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

# SQLite checkpointer - conversation history .db file mein save hogi
conn = sqlite3.connect('chatbot_memory.db', check_same_thread=False)
memory = SqliteSaver(conn)

# compile graph WITH checkpointer
chatbot = graph.compile(checkpointer=memory)
print('Chatbot compiled with SQLite memory!')



# Only export 'chatbot' — Streamlit frontend handles the conversation loop