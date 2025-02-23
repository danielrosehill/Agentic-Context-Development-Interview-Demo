import streamlit as st
import openai
import json
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Agentic Context Development Interview",
    layout="wide"
)

# Custom CSS for chat bubbles, badges, and Font Awesome
st.markdown("""
<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

/* Global styles */
.stApp {
    font-family: 'Inter', sans-serif;
}

/* Control buttons */
.control-buttons {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}

.stButton > button {
    border-radius: 20px;
    padding: 10px 24px;
    font-weight: 500;
    transition: all 0.3s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

/* Sidebar styling */
.sidebar .stRadio > label {
    font-weight: 600;
    margin-bottom: 12px;
    color: #1E293B;
}

/* Chat message styling */
.chat-message {
    padding: 1rem;
    border-radius: 12px;
    margin: 8px 0;
    max-width: 85%;
}

.user-message {
    background: #F1F5F9;
    margin-left: auto;
}

.assistant-message {
    background: #E0F2FE;
    margin-right: auto;
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    margin-bottom: 16px;
}

.stTabs [data-baseweb="tab"] {
    padding: 8px 16px;
    border-radius: 8px;
}

/* Headers */
h1, h2, h3 {
    color: #0F172A;
    margin-bottom: 1rem;
}

/* Cards and containers */
.stMarkdown {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

/* Input fields */
.stTextInput > div > div {
    border-radius: 8px;
}

/* Progress indicators */
.stProgress > div > div {
    border-radius: 8px;
    height: 8px;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'interview_started' not in st.session_state:
    st.session_state.interview_started = False
if 'interview_complete' not in st.session_state:
    st.session_state.interview_complete = False
if 'context_data' not in st.session_state:
    st.session_state.context_data = ""
if 'context_focus' not in st.session_state:
    st.session_state.context_focus = None
if 'use_stored_key' not in st.session_state:
    st.session_state.use_stored_key = True
if 'interview_mode' not in st.session_state:
    st.session_state.interview_mode = "AMA (Ask Me Anything)"

def get_config_dir():
    """Get the configuration directory for storing API key."""
    if os.name == 'nt':  # Windows
        config_dir = os.path.join(os.environ['APPDATA'], 'AgenticContext')
    else:  # Unix/Linux/Mac
        config_dir = os.path.join(os.path.expanduser('~'), '.config', 'agentic_context')
    os.makedirs(config_dir, exist_ok=True)
    return config_dir

def save_api_key(api_key):
    """Save API key to configuration file."""
    config_path = os.path.join(get_config_dir(), 'config.json')
    with open(config_path, 'w') as f:
        json.dump({'api_key': api_key}, f)

def load_api_key():
    """Load API key from configuration file."""
    config_path = os.path.join(get_config_dir(), 'config.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f).get('api_key')
    except (FileNotFoundError, json.JSONDecodeError):
        return None

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

def generate_markdown_filename(context_focus):
    """Generate a filename for the markdown export."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    subject = context_focus if context_focus else "general"
    return f"context_{subject}_{timestamp}.md"

# Sidebar for settings
with st.sidebar:
    st.title("Settings")
    
    # API Key Management
    st.subheader("API Key")
    stored_key = load_api_key()
    
    if stored_key:
        st.session_state.use_stored_key = st.checkbox("Use stored API key", value=st.session_state.use_stored_key)
    
    if stored_key and st.session_state.use_stored_key:
        api_key = stored_key
        st.success("Using stored API key")
    else:
        api_key = st.text_input("Enter OpenAI API Key", type="password")
        if api_key:
            if st.button("Save API Key"):
                save_api_key(api_key)
                st.success("API key saved successfully!")
                st.rerun()
    
    st.divider()
    
    # Interview Settings
    st.subheader("Interview Settings")
    st.session_state.interview_mode = st.radio(
        "Interview Mode",
        ["AMA (Ask Me Anything)", "Subject Restricted"],
        index=0 if st.session_state.interview_mode == "AMA (Ask Me Anything)" else 1
    )
    
    if st.session_state.interview_mode == "Subject Restricted":
        predefined_subjects = ["General", "Professional Background", "Technical Skills", "Education", "Interests"]
        selected_subject = st.selectbox("Select Subject Focus", predefined_subjects)
        
        use_custom = st.checkbox("Use Custom Subject")
        if use_custom:
            custom_subject = st.text_input("Enter Custom Subject")
            new_subject = custom_subject if custom_subject else None
        else:
            new_subject = selected_subject.lower() if selected_subject != "General" else None
            
        # Add Update Subject button
        if st.button("Update Subject", type="primary"):
            st.session_state.context_focus = new_subject
            st.session_state.messages = []
            st.session_state.context_data = ""
            st.session_state.interview_started = True
            st.session_state.interview_complete = False
            question = get_random_question(api_key, new_subject)
            if question:
                st.session_state.messages.append(f"Q: {question}")
                st.rerun()
    else:
        st.session_state.context_focus = None

    # Add a clear button to reset everything
    if st.button("Clear All", type="secondary"):
        st.session_state.messages = []
        st.session_state.interview_started = False
        st.session_state.interview_complete = False
        st.session_state.context_data = ""
        st.session_state.context_focus = None
        st.rerun()

# Main content
st.title("Agentic Context Development Interview")

# GitHub badges
st.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <a href="https://github.com/danielrosehill" class="github-badge" target="_blank">
        <i class="fab fa-github"></i> Author's GitHub
    </a>
    <a href="https://github.com/danielrosehill/Agentic-Context-Development-Interview-Demo" class="github-badge" target="_blank">
        <i class="fab fa-github"></i> Project Repository
    </a>
</div>
""", unsafe_allow_html=True)

st.markdown("""
This application provides a simple interface for using a large language model to conduct context-generating interviews. 
It creates context snippets that can be fed into vector storage for personalized LLM inference. You can use a data pipeline 
to provide your data into the vector database of your choice.
""")

# Create tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["Interview", "Generated Context", "Instructions", "Gallery"])

with tab1:
    # Control buttons at the top
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Start New Interview", key="start_new", use_container_width=True):
            st.session_state.messages = []
            st.session_state.context_data = ""
            st.session_state.interview_started = True
            st.session_state.interview_complete = False
            question = get_random_question(api_key, st.session_state.context_focus)
            if question:
                st.session_state.messages.append(f"Q: {question}")
                st.rerun()
            else:
                st.error("Failed to generate question. Please check your API key.")

    with col2:
        if st.button("End Interview", key="end", use_container_width=True):
            if st.session_state.messages:
                st.session_state.interview_complete = True
                st.session_state.context_data = extract_context(api_key, st.session_state.messages)
                st.rerun()

    with col3:
        if st.button("Export Conversation", key="export", use_container_width=True):
            if st.session_state.messages:
                filename = generate_markdown_filename(st.session_state.context_focus)
                st.download_button(
                    label="Download Chat",
                    data=st.session_state.context_data,
                    file_name=filename,
                    mime="text/markdown",
                    use_container_width=True
                )

    # Chat messages
    for msg in st.session_state.messages:
        is_bot = msg.startswith('Q:')
        if is_bot:
            with st.chat_message("assistant", avatar="🤖"):
                st.write(msg[2:])  # Remove the 'Q: ' prefix
        else:
            with st.chat_message("user", avatar="👤"):
                st.write(msg)

    # Input area
    if api_key and st.session_state.interview_started and not st.session_state.interview_complete:
        prompt = st.chat_input("Type your response here...")
        
        if prompt:
            st.session_state.messages.append(prompt)
            question = get_random_question(api_key, st.session_state.context_focus)
            if question:
                st.session_state.messages.append(f"Q: {question}")
                st.rerun()
            else:
                st.error("Failed to generate question. Please check your API key.")

with tab4:
    st.header("Feature Gallery")
    st.markdown("### Interactive Interview Process")
    st.image("screenshots/1.png", use_container_width=True)
    st.write("")
    st.markdown("### Context Focus Selection")
    st.image("screenshots/2.png", use_container_width=True)
    st.write("")
    st.markdown("### Generated Context Summary")
    st.image("screenshots/3.png", use_container_width=True)

with tab2:
    if st.session_state.interview_complete and st.session_state.context_data:
        st.header("Generated Context")
        st.markdown(st.session_state.context_data)
        
        # Download button for markdown
        if st.button("Download as Markdown"):
            filename = generate_markdown_filename(st.session_state.context_focus)
            st.download_button(
                label="Click to Download",
                data=st.session_state.context_data,
                file_name=filename,
                mime="text/markdown"
            )
    else:
        st.info("Complete the interview to generate your context summary.")

with tab3:
    st.header("How it Works")
    st.markdown("""
    This application helps gather and extract contextual information about you through an interactive interview process.
    
    Created by [Daniel Rosehill](https://danielrosehill.com) and Claude (Anthropic).
    
    View the source code on [GitHub](https://github.com/danielrosehill/Context-Extraction-Demo).
    
    ### Process:
    1. Enter your OpenAI API key in the sidebar
    2. Choose your preferred interview subject
    3. Click the "Start Interview" button
    4. The AI interviewer will ask targeted questions based on your chosen subject
    5. Answer each question naturally - you can type or use voice input
    6. Click "Submit Answer" after each response
    7. You can change the interview subject at any time
    8. Click "End Interview" when you're ready to finish
    9. Review the extracted context and export it as needed
    
    ### Features:
    - **Interview Subjects**: Choose to focus on specific aspects like professional background, technical skills, or keep it general
    - **Dynamic Subject Changes**: Change the interview focus at any time during the conversation
    - **Voice Input**: Use Chrome's built-in speech-to-text by clicking the microphone icon
    - **Targeted Questions**: The AI asks questions relevant to your chosen subject
    - **Context Extraction**: Automatically organizes your information into a structured summary
    - **Export Options**: Copy or download your context data in markdown format
    
    ### Tips:
    - Provide detailed, honest answers for better context extraction
    - Use voice input to make the process faster and more natural
    - Take your time with each response
    - Feel free to change subjects to cover different aspects of your background
    - You can reset and start over at any time using the Clear/Reset button
    """)
