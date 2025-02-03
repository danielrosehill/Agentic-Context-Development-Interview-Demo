import streamlit as st
import openai
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Context Extraction Demo",
    layout="wide"
)

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'interview_complete' not in st.session_state:
    st.session_state.interview_complete = False
if 'context_data' not in st.session_state:
    st.session_state.context_data = ""
if 'interview_started' not in st.session_state:
    st.session_state.interview_started = False

def get_random_question(api_key):
    """Get a random question from OpenAI."""
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an interviewer gathering context about the user. Ask one random, open-ended question that reveals meaningful information about the user's life, experiences, preferences, beliefs, or background. Be creative and vary your questions across different topics like: career/education, hobbies/interests, life experiences, values/beliefs, goals/aspirations, daily habits, relationships, travel experiences, cultural background, skills/talents, etc. Each response should be just one engaging question. Never repeat topics or questions that have been asked before. Focus on questions that will yield rich contextual information about who the user is as a person."
                },
                {
                    "role": "user",
                    "content": "Please ask me a random question."
                }
            ]
        )
        return response.choices[0].message.content if hasattr(response.choices[0].message, 'content') else str(response.choices[0].message)
    except Exception as e:
        return f"Error: {str(e)}"

def extract_context(api_key, conversation):
    """Extract context from the conversation using OpenAI."""
    try:
        client = openai.OpenAI(api_key=api_key)
        conversation_text = "\n".join([f"{'Bot' if i%2==0 else 'User'}: {msg}" for i, msg in enumerate(conversation)])
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Analyze the following conversation and extract key information about the user. Create a well-organized summary in markdown format, grouping similar information under appropriate headings. Write in third person perspective."
                },
                {
                    "role": "user",
                    "content": f"Please analyze this conversation and create a context summary:\n\n{conversation_text}"
                }
            ]
        )
        return response.choices[0].message.content if hasattr(response.choices[0].message, 'content') else str(response.choices[0].message)
    except Exception as e:
        return f"Error: {str(e)}"

# Sidebar for API key and controls
with st.sidebar:
    st.title("Settings")
    api_key = st.text_input("Enter OpenAI API Key", type="password")
    
    if st.button("Clear/Reset"):
        st.session_state.messages = []
        st.session_state.interview_complete = False
        st.session_state.context_data = ""
        st.session_state.interview_started = False
        st.rerun()

# Main content
st.title("Context Extraction Demo")

# Create tabs for instructions and interview
tab1, tab2 = st.tabs(["Instructions", "Interview"])

with tab1:
    st.header("How it Works")
    st.markdown("""
    This application helps gather and extract contextual information about you through an interactive interview process.
    
    ### Process:
    1. Enter your OpenAI API key in the sidebar
    2. Click the "Start Interview" button in the Interview tab
    3. The AI interviewer will ask you random questions about various aspects of your life
    4. Answer each question naturally - you can type or use voice input
    5. Click "Submit Answer" after each response
    6. Continue the conversation until you're ready to end
    7. Click "End Interview" to generate your context summary
    8. Review the extracted context and export it as needed
    
    ### Features:
    - **Voice Input**: Use Chrome's built-in speech-to-text by clicking the microphone icon
    - **Random Questions**: The AI asks diverse questions about your experiences, preferences, and background
    - **Context Extraction**: Automatically organizes your information into a structured summary
    - **Export Options**: Copy or download your context data in markdown format
    
    ### Tips:
    - Provide detailed, honest answers for better context extraction
    - Use voice input to make the process faster and more natural
    - Take your time with each response
    - You can reset and start over at any time using the Clear/Reset button
    """)

with tab2:
    # Create two columns for the main interface
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Conversation")
        # Display conversation history
        for msg in st.session_state.messages:
            st.text(f"{'Bot' if msg.startswith('Q:') else 'You'}: {msg}")

    with col2:
        st.subheader("Your Response")
        # Add microphone icon and voice input instructions
        st.markdown("""
        💡 **Voice Input Tip**: 
        - Click the microphone icon in Chrome
        - Or use built-in speech-to-text
        """)
        
        # Show interview interface
        if api_key:
            if not st.session_state.interview_started and not st.session_state.interview_complete:
                if st.button("Start Interview"):
                    st.session_state.interview_started = True
                    question = get_random_question(api_key)
                    st.session_state.messages.append(f"Q: {question}")
                    st.rerun()
            
            elif st.session_state.interview_started and not st.session_state.interview_complete:
                # Get last message
                last_message = st.session_state.messages[-1]
                
                # If last message was an answer, get next question
                if not last_message.startswith('Q:'):
                    question = get_random_question(api_key)
                    st.session_state.messages.append(f"Q: {question}")
                    st.rerun()
                
                # User input
                user_answer = st.text_area("Your answer:", height=100)
                
                # Submit answer button
                if st.button("Submit Answer"):
                    if user_answer:
                        st.session_state.messages.append(user_answer)
                        st.rerun()
                
                # End interview button
                if st.button("End Interview"):
                    if len(st.session_state.messages) > 1:  # Ensure there's at least one Q&A pair
                        st.session_state.interview_complete = True
                        # Extract context
                        st.session_state.context_data = extract_context(api_key, st.session_state.messages)
                        st.rerun()
        else:
            st.warning("Please enter your OpenAI API key in the sidebar to begin.")

# Show context data and export options after interview is complete
if st.session_state.interview_complete and st.session_state.context_data:
    st.markdown("---")
    st.subheader("Extracted Context")
    st.markdown(st.session_state.context_data)
    
    # Export options
    col3, col4 = st.columns(2)
    with col3:
        if st.button("Copy to Clipboard"):
            st.write("Context copied to clipboard!")
            st.code(st.session_state.context_data)
    
    with col4:
        if st.button("Download as Markdown"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"context_data_{timestamp}.md"
            with open(filename, "w") as f:
                f.write(st.session_state.context_data)
            st.download_button(
                label="Download",
                data=st.session_state.context_data,
                file_name=filename,
                mime="text/markdown"
            )
