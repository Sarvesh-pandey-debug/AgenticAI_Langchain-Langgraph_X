import streamlit as st 
from chatbot_backend import chatbot
from langchain_core.messages import BaseMessage, HumanMessage


CONFIG = {'configurable': {'thread_id': 'session_1'}}

# st. session_state -> dict - is used for storing the messages



if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


# loading the conversation history 
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input("type here")

if user_input: 
   
   # first add the user message in message history
   # second display the user message
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)
    
    responce = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)
    ai_message =    responce['messages'][-1].content
    # first add the user message in message history
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})    
    with st.chat_message('assistant'):
        st.text(ai_message)    