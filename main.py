#Importing modules/packages
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Setup/Page config
st.set_page_config(
    page_title="AI Chatbot (By Jay Tailor)",
    page_icon="🔥",
    layout="wide"
)

# Ask for OpenAI key at the beginning
if "openai_key" not in st.session_state:
    st.title("🔑 OpenAI API Key Required")
    st.write("Please enter your OpenAI API key to continue:")
    
    api_key = st.text_input("OpenAI API Key:", type="password", placeholder="sk-...")
    
    if st.button("Submit API Key"):
        if api_key.startswith("sk-"):
            st.session_state.openai_key = api_key
            st.success("API key saved! Refreshing...")
            st.rerun()
        else:
            st.error("Please enter a valid OpenAI API key (should start with 'sk-')")
    
    st.stop()  # Stop execution until key is provided

# Initialize OpenAI client with the saved key
client = OpenAI(api_key=st.session_state.openai_key)

# Setup message history
if "messages" not in st.session_state:
    st.session_state.messages = []

#Main page
st.markdown('<h1 style="text-align: center;">An AI Chatbot.</h1>', unsafe_allow_html=True)
st.markdown("---")
st.markdown(
    "<div style='text-align: center;'>"
    "Powered by <span style='color: #48cae4;'>OpenAI API</span>, "
    "<span style='color: #48cae4;'>Streamlit</span>, and "
    "<span style='color: #48cae4;'>lots of late nights</span> 😅"
    "</div>",
    unsafe_allow_html=True
)

# Display previous chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input field (always pinned at bottom)
prompt = st.chat_input("Ask me anything...")

if prompt:

    # Save and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)  # Show original user input
    
    # Send to OpenAI with the enhanced prompt
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )

    bot_reply = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    with st.chat_message("assistant"):
        st.markdown(bot_reply)

#Sidebar
with st.sidebar:
        st.title("An AI Chatbot.")
        if st.button("🗑️ Clear chat history"):
         st.session_state.messages = []
         st.rerun()

        st.markdown("---")
#------------------TIPS SECTION------------------
        st.header("💡 Tips") #HEADER OF THE TIPS SECTION
        st.markdown("- Talk to the bot naturally! The bot will understand your context.") #TIP 1
        st.markdown("---")
        st.header("🛠️ Technical info") #TECHNICAL INFO (Make it the 2nd topic)
        st.markdown("- **Model:** OpenAI GPT 3.5 Turbo") #RESOURCE 1
        st.markdown("- **Framework:** Streamlit + OpenAI") #RESOURCE 2
        st.markdown("- Made by Jay Tailor")
#------------------PROJECT PAGE BUTTON------------------
        if st.button("See the project page!"):
            st.markdown("Coming soon. Still working on it!")
        
#TEXT SIZE ELEMENTS
#with st.sidebar:
#st.title("Settings")  # Big title
#st.header("Options")  # Medium title
#st.subheader("More Options")  # Small title
#st.write("Some text here")  # Regular text
