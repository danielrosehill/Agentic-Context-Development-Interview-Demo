import streamlit as st
import openai
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Agent Interview Context Generation Demo",
    layout="wide"
)

# Custom CSS for chat bubbles and Font Awesome
st.markdown("""
<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');
.chat-bubble {
    padding: 15px;
    border-radius: 15px;
    margin: 5px 0;
    max-width: 80%;
    position: relative;
}

.bot-bubble {
    background-color: #F0F2F6;
    margin-right: auto;
    margin-left: 10px;
    border-bottom-left-radius: 5px;
}

.user-bubble {
    background-color: #4CAF50;
    color: white;
    margin-left: auto;
    margin-right: 10px;
    border-bottom-right-radius: 5px;
}

.chat-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 10px;
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.stTextArea textarea {
    border-radius: 20px;
    padding: 10px 15px;
    font-size: 16px;
}

.stButton button {
    border-radius: 20px;
    padding: 5px 20px;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'interview_complete' not in st.session_state:
    st.session_state.interview_complete = False
if 'context_data' not in st.session_state:
    st.session_state.context_data = ""
if 'interview_started' not in st.session_state:
    st.session_state.interview_started = False
if 'context_focus' not in st.session_state:
    st.session_state.context_focus = None

def get_random_question(api_key, focus_area=None):
    """Get a random question from OpenAI based on optional focus area."""
    try:
        client = openai.OpenAI(api_key=api_key)
        system_content = "You are an interviewer gathering context about the user. "
        if focus_area and focus_area != "general":
            system_content += f"Focus specifically on questions about their {focus_area}. "
        system_content += "Ask one random, open-ended question that reveals meaningful information about the user. Be creative and never repeat questions. Each response should be just one engaging question."
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": system_content
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
        st.session_state.context_focus = None
        st.rerun()

# Main content
st.title("Agent Interview Context Generation Demo")
st.markdown("""
This project demonstrates how AI agents can proactively gather and generate rich contextual data 
through intelligent interviewing. By focusing on specific areas of interest, the agent builds a comprehensive 
understanding that enhances AI-human interactions and enables more personalized experiences.
""")

# Create tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["Instructions", "Interview", "Gallery", "Generated Context"])

with tab1:
    st.header("How it Works")
    st.markdown("""
    This application helps gather and extract contextual information about you through an interactive interview process.
    
    Created by [Daniel Rosehill](https://danielrosehill.com) and Claude (Anthropic).
    
    View the source code on [GitHub](https://github.com/danielrosehill/Context-Extraction-Demo).
    
    ### Process:
    1. Enter your OpenAI API key in the sidebar
    2. Choose your preferred context focus area
    3. Click the "Start Interview" button in the Interview tab
    4. The AI interviewer will ask targeted questions based on your chosen focus
    5. Answer each question naturally - you can type or use voice input
    6. Click "Submit Answer" after each response
    7. Continue the conversation until you're ready to end
    8. Click "End Interview" to generate your context summary
    9. Review the extracted context and export it as needed
    
    ### Features:
    - **Focus Areas**: Choose to focus on specific aspects like professional background, technical skills, or keep it general
    - **Voice Input**: Use Chrome's built-in speech-to-text by clicking the microphone icon
    - **Targeted Questions**: The AI asks questions relevant to your chosen focus area
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
        # Display conversation history with chat bubbles
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            is_bot = msg.startswith('Q:')
            bubble_class = "bot-bubble" if is_bot else "user-bubble"
            message_content = msg[3:] if is_bot else msg
            bot_icon = '<i class="fas fa-robot" style="margin-right: 8px;"></i>' if is_bot else ''
            st.markdown(
                f'<div class="chat-bubble {bubble_class}">{bot_icon}{message_content}</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

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
                # Context focus selection
                if st.session_state.context_focus is None:
                    st.write("Before we begin, would you like to focus on a specific area or keep the questions general?")
                    focus_options = ["general", "professional background", "personal interests", "technical skills", "life experiences"]
                    selected_focus = st.selectbox("Choose focus area:", focus_options)
                    if st.button("Set Focus"):
                        st.session_state.context_focus = selected_focus
                        st.rerun()
                else:
                    if st.button("Start Interview", type="primary", use_container_width=True):
                        st.session_state.interview_started = True
                        question = get_random_question(api_key, st.session_state.context_focus)
                        st.session_state.messages.append(f"Q: {question}")
                        st.rerun()
            
            elif st.session_state.interview_started and not st.session_state.interview_complete:
                # Get last message
                last_message = st.session_state.messages[-1]
                
                # If last message was an answer, get next question
                if not last_message.startswith('Q:'):
                    question = get_random_question(api_key, st.session_state.context_focus)
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

with tab3:
    st.header("Feature Gallery")
    st.markdown("### Interactive Interview Process")
    st.image("screenshots/1.png", use_column_width=True)
    st.markdown("### Context Focus Selection")
    st.image("screenshots/2.png", use_column_width=True)
    st.markdown("### Generated Context Summary")
    st.image("screenshots/3.png", use_column_width=True)

with tab4:
    if st.session_state.interview_complete and st.session_state.context_data:
        st.header("Generated Context")
        st.markdown("""
        Below is the AI-generated context summary based on your interview responses. 
        This structured data can be used to enhance future AI interactions and create 
        more personalized experiences.
        """)
        st.markdown(st.session_state.context_data)
        
        # Export options in columns
        st.subheader("Export Options")
        col3, col4 = st.columns(2)
        with col3:
            if st.button("Copy to Clipboard", type="secondary", use_container_width=True):
                st.write("Context copied to clipboard!")
                st.code(st.session_state.context_data)
        
        with col4:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"context_data_{timestamp}.md"
            with open(filename, "w") as f:
                f.write(st.session_state.context_data)
            st.download_button(
                label="Download as Markdown",
                data=st.session_state.context_data,
                file_name=filename,
                mime="text/markdown",
                use_container_width=True
            )
    else:
        st.info("Complete the interview to generate your context summary.")
