import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from openai import OpenAIError

# Load environment variables
load_dotenv()

# Get API key
OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")

# Check if API key is set
if not OPEN_ROUTER_API_KEY:
    st.error("OPEN_ROUTER_API_KEY environment variable is not set. Please configure it in your deployment platform's settings or in a .env file for local testing.")
    st.stop()

# Initialize OpenAI client
try:
    client = OpenAI(
        api_key=OPEN_ROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )
except Exception as e:
    st.error(f"Failed to initialize OpenAI client: {str(e)}")
    st.stop()

# Streamlit UI configuration
st.set_page_config(
    page_title="Writer AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar for settings and info
with st.sidebar:
    st.header("AI Writer About")
    st.markdown("**Model**: DeepSeek Chat (Free)")
    st.markdown("**API**: OpenRouter")
    st.markdown("---")
    st.info("Enter your prompt below to generate essays, stories, poems, emails, or letters. For support, contact the developer.")
    # Footer
    st.markdown('<div style="text-align: center; color: white; margin-top: 2em;">Made with ❤️ by Abdul Uzair</div>', unsafe_allow_html=True)    

# Main UI
st.title("Writer AI Chatbot 🤖")
st.subheader("Your Specialist for Essays, Stories, Poems, Emails, and Letters")
st.markdown(
    """
    Welcome to **Writer AI Chatbot**! I'm here to craft high-quality written content based on your prompts.
    Type your request below, and I'll generate a response tailored to your needs.
    """
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else None):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Enter your message here...")

if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.spinner("Generating your content..."):
        try:
            response = client.chat.completions.create(
                model="deepseek/deepseek-chat",  # Valid OpenRouter model
                messages=[
                    {
                        "role": "system",
                        "content": "You are a writer agent specializing in creating high-quality essays, stories, poems, emails, and letters. Provide creative, well-structured, and engaging responses tailored to the user's prompt."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,  # Balanced creativity
                max_tokens=1000   # Reasonable length for poems, essays, etc.
            )
            output = response.choices[0].message.content.strip()
            
        except OpenAIError as e:
            st.error(f"Error generating response: {str(e)}")
            st.session_state.messages.append({"role": "assistant", "content": f"Error: {str(e)}"})
            output = None

        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
            st.session_state.messages.append({"role": "assistant", "content": f"Unexpected error: {str(e)}"})
            output = None

    # Add assistant response to chat history
    if output:
        st.session_state.messages.append({"role": "assistant", "content": output})
        with st.chat_message("assistant", avatar="🤖"):
            # Display the generated content
            st.markdown(output)