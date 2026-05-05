from dotenv import load_dotenv
load_dotenv()

import streamlit as st

# Page config
st.set_page_config(
    page_title="AI Chatbot Agents", 
    layout="centered"
)

# DARK MODE CSS - Yahan add kiya gaya hai
st.markdown("""
<style>
    /* Main app background */
    .stApp {
        background: #1a1a2e;
    }
    
    /* Main container */
    .block-container {
        background: #16213e;
        color: white;
        border-radius: 15px;
        padding: 20px;
    }
    
    /* Headers color */
    h1, h2, h3, .stTitle {
        color: #e94560 !important;
    }
    
    /* Text area styling */
    .stTextArea textarea {
        background: #0f3460 !important;
        color: white !important;
        border: 1px solid #e94560 !important;
        border-radius: 10px !important;
    }
    
    /* Text input styling */
    .stTextInput input {
        background: #0f3460 !important;
        color: white !important;
    }
    
    /* Selectbox styling */
    .stSelectbox select {
        background: #0f3460 !important;
        color: white !important;
    }
    
    /* Button styling */
    .stButton button {
        background: #e94560 !important;
        color: white !important;
        border-radius: 20px !important;
        padding: 10px 30px !important;
        font-weight: bold !important;
        border: none !important;
    }
    
    .stButton button:hover {
        background: #ff6b8a !important;
        transform: scale(1.02);
    }
    
    /* Checkbox styling */
    .stCheckbox label {
        color: white !important;
    }
    
    /* Radio button styling */
    .stRadio label {
        color: white !important;
    }
    
    /* Info/Warning/Error messages */
    .stAlert {
        background: #0f3460 !important;
        color: white !important;
    }
    
    /* Sidebar (if you have it) */
    .css-1d391kg {
        background: #0f3460 !important;
    }
    
    /* Write text */
    .stMarkdown {
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Your existing code continues here
st.title("AI Chatbot Agents")
st.write("Create and Interact with the AI Agents!")

system_prompt = st.text_area("Define your AI Agent: ", height=70, placeholder="Type your system prompt here...")

MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
MODEL_NAMES_OPENAI = ["gpt-4o-mini"]

provider = st.radio("Select Provider:", ("Groq", "OpenAI"))

if provider == "Groq":
    selected_model = st.selectbox("Select Groq Model:", MODEL_NAMES_GROQ)
elif provider == "OpenAI":
    selected_model = st.selectbox("Select OpenAI Model:", MODEL_NAMES_OPENAI)

allow_web_search = st.checkbox("Allow Web Search")
user_query = st.text_area("Enter your query: ", height=150, placeholder="Ask Anything!")

API_URL = "http://127.0.0.1:9999/chat"

if st.button("Ask Agent!"):
    if user_query.strip():
        import requests

        payload = {
            "model_name": selected_model,
            "model_provider": provider,
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": allow_web_search
        }

        try:
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                response_data = response.json()
                
                if isinstance(response_data, str):
                    st.subheader("Agent Response")
                    st.markdown(f"**Final Response:** {response_data}")
                elif isinstance(response_data, dict):
                    if "error" in response_data:
                        st.error(response_data["error"])
                    else:
                        st.subheader("Agent Response")
                        st.markdown(f"**Final Response:** {response_data.get('response', response_data)}")
                else:
                    st.subheader("Agent Response")
                    st.markdown(f"**Final Response:** {response_data}")
            else:
                st.error(f"Backend error: {response.status_code}")
                
        except Exception as e:
            st.error(f"Connection error: {str(e)}")