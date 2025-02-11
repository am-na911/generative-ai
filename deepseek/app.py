# develop end-to-end generativeAI Application with the help of deepseekr1 model
import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate 
)

#custom css styling
st.markdown("""
<style>
    /* Existing Styles */
    .main {
        background-color: #1a1a1a;
        color: #ffffff;
    }
            
    .sidebar .sidebar-content {
            background-color: #2d2d2d;
    }
            
    .stTextInput textarea {
            color: #ffffff !important;
    }
            
    /* Add these new styles for select box*/
    .stSelectbox div[data-baseweb='select'] {
            color: white !important;
            background-color: #3d3d3d !important;
    }
            
    .stSelectbox svg {
            fill: white !important;
    }
    .stSelectbox option {
            background-color: #2d2d2d !important;
            color: white !important;
    }
    
    /* For dropdown menu items */
    div[role='listbox'] div {
            background-color: #2d2d2d !important;
            color: white !important;
    }
</style>    
""", unsafe_allow_html=True)

st.title('🧠 DeepSeek Code Companion')
st.caption('🚀 Your AI Pair Programmer with Debugging Superpower')

# sidebar configuration
with st.sidebar:
    st.header('Configuration')
    selected_model = st.selectbox(
        'Choose Model', 
        ['deepseek-r1:1.5b', 'deepseek-r1:3b'], index=0
    )
    st.divider()
    st.markdown('### Model Capabilities')
    st.markdown("""
    -🐍 Python Expert
    -🐞 Debugging Assistant
    -👨‍💻 Code Documentation
    -💡 Solution Design
""")
    st.divider()
    st.markdown('Built with [Ollama](https://ollama.ai) | [LangChain](https://python.langchain.com/)')

# initiate the chat engine
llm_engine = ChatOllama(
    model=selected_model,
    base_url = 'http://localhost:11434',

    temperature=0.3
)  

# System Prompt Configuration [how this llm model should react]
system_prompt= SystemMessagePromptTemplate.from_template(
    'You are an expert AI coding assistant. Provide concise, correct solutions'
    'with strategic print statements for debugging, Always respond in English'
)

# session state management
# it will basically help us to manage the chat history
if 'message_log' not in st.session_state:
    st.session_state.message_log = [{'role': 'ai', 'content': 'Hi! I am DeepSeek🐬. How can I help you code today?'}]

# chat container: a section in the app where chat messages are displayed
chat_container = st.container()
# Display chat message
with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

# chat input and processing
user_query = st.chat_input('Type your coding question here...')

# creating preprocessing and post-processing pipeline
def generate_ai_response(prompt_chain):
    processing_pipeline = prompt_chain | llm_engine | StrOutputParser()
    return processing_pipeline.invoke({})

def build_prompt_chain():
    prompt_sequence = [system_prompt]
    for msg in st.session_state.message_log:
        if msg['role'] == 'user':
            prompt_sequence.append(HumanMessagePromptTemplate.from_template(msg['content']))
        elif msg['role'] == 'ai':
            prompt_sequence.append(AIMessagePromptTemplate.from_template(msg['content']))
    return ChatPromptTemplate.from_messages(prompt_sequence)

if user_query:
    # add user message to log
    st.session_state.message_log.append({'role':'user', 'content': user_query})

# Generate AI response
    with st.spinner('⚙ Processing...'):
        prompt_chain = build_prompt_chain()
        ai_response = generate_ai_response(prompt_chain)

        # Add AI response to log
        st.session_state.message_log.append({'role':'ai', 'content':ai_response})

        # rerun to update chat display
        st.rerun()