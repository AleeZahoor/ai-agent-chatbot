from dotenv import load_dotenv
load_dotenv()

import streamlit as st

st.set_page_config(page_title="AI Chatbot Agents", layout="centered")

# Dark mode CSS
st.markdown("""
<style>
    .stApp {
        background: #1a1a2e;
    }
    .block-container {
        background: #16213e;
        color: white;
    }
    h1, h2, h3 {
        color: #e94560;
    }
    .stTextArea textarea {
        background: #0f3460;
        color: white;
    }
    .stButton button {
        background: #e94560;
        color: white;
    }
    .stSelectbox select {
        background: #0f3460;
        color: white;
    }
    .stCheckbox label {
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 AI Chatbot Agents")
st.write("Create and Interact with the AI Agents!")

system_prompt = st.text_area("Define your AI Agent: ", height=70, placeholder="Type your system prompt here...")

# ✅ SIRF GROQ - OpenAI HATAYA
provider = "Groq"
selected_model = st.selectbox(
    "Select Groq Model:", 
    ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
)

allow_web_search = st.checkbox("Allow Web Search")
user_query = st.text_area("Enter your query: ", height=150, placeholder="Ask Anything!")

API_URL = "https://ai-agent-backend-mnxb.onrender.com/chat"

if st.button("Ask Agent!"):
    if user_query.strip():
        import requests

        payload = {
            "model_name": selected_model,
            "model_provider": provider,  # Always "Groq"
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": allow_web_search
        }

        try:
            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                response_data = response.json()
                
                if isinstance(response_data, dict):
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