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

# Clean, simplified CSS
st.markdown("""
<style>
/* Base styles */
* {
    font-family: 'Inter', sans-serif;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Main container spacing */
.main {
    padding: 2rem;
}

/* Clean header styles */
header {
    border-bottom: none !important;
    background: none !important;
    margin-bottom: 2rem;
}

.stApp header {
    background-color: transparent !important;
    border-bottom: none !important;
}

/* Remove default Streamlit styling */
.block-container {
    padding-top: 2rem !important;
    max-width: 1200px;
}

.stMarkdown {
    background: transparent;
    padding: 0;
    box-shadow: none;
}

/* Button styling */
.stButton > button {
    border-radius: 8px;
    padding: 0.5rem 1rem;
    background-color: #2196f3;
    color: white;
    border: none;
    font-weight: 500;
}

.stButton > button:hover {
    background-color: #1976d2;
}

/* Chat message styling */
.chat-message {
    padding: 1rem;
    border-radius: 8px;
    margin: 0.5rem 0;
    background: #f8f9fa;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 1rem;
    border-bottom: 2px solid #f0f0f0;
}

.stTabs [data-baseweb="tab"] {
    height: 40px;
    padding: 0 16px;
    color: #666;
}

.stTabs [data-baseweb="tab-highlight"] {
    background-color: #2196f3;
}

/* Sidebar styling */
.css-1d391kg {
    padding: 2rem 1rem;
}

/* Input fields */
.stTextInput > div > div {
    border-radius: 8px;
    border: 1px solid #e0e0e0;
}

/* Text size */
.stTextInput, .stTextArea, .stMarkdown, .stText {
    font-size: 16px !important;
}

div[data-testid="stChatMessage"] {
    font-size: 16px !important;
}
</style>
""", unsafe_allow_html=True)

# Custom CSS to adjust avatar size
st.markdown("""
<style>
/* Increase avatar size */
.stChatMessage img {
    width: 60px !important;
    height: 60px !important;
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

def display_chat_message(message, is_user=False):
    """Display a chat message using Streamlit's chat components."""
    if is_user:
        with st.chat_message("user", avatar="https://ui-avatars.com/api/?name=User&background=random"):
            st.write(message)
    else:
        with st.chat_message("assistant", avatar="https://res.cloudinary.com/drrvnflqy/image/upload/v1740344521/CB_1_jfptsm.png"):
            st.write(message)

# Sidebar for API settings
with st.sidebar:
    st.write("## API Settings")
    
    use_stored_key = st.checkbox("Use stored API key", value=st.session_state.use_stored_key)
    st.session_state.use_stored_key = use_stored_key

    if use_stored_key:
        api_key = load_api_key()
        if not api_key:
            st.warning("No stored API key found. Please enter one below.")
    
    api_key_input = st.text_input("OpenAI API Key:", type="password", value=api_key if use_stored_key and api_key else "")
    
    if api_key_input:
        if use_stored_key:
            save_api_key(api_key_input)
        api_key = api_key_input
    else:
        st.error("Please enter an API key to continue")
        st.stop()

# Main content
st.write("# Agentic Context Development Interview")

# Interview Configuration
st.markdown('<div class="subject-settings">', unsafe_allow_html=True)
st.markdown("### 📋 Interview Configuration")

# Interview Mode Selection
st.session_state.interview_mode = st.radio(
    "Interview Mode",
    ["AMA (Ask Me Anything)", "Subject Restricted"],
    index=0 if st.session_state.interview_mode == "AMA (Ask Me Anything)" else 1,
    help="Choose between an open-ended interview or focus on specific subjects"
)

subject_categories = {
    "Career & Professional": [
        "Professional Background",
        "Technical Skills",
        "Leadership Experience",
        "Project Management",
        "Industry Knowledge",
        "Career Goals",
        "Work Experience"
    ],
    "Education & Skills": [
        "Education History",
        "Research Experience",
        "Communication Skills",
        "Problem-Solving",
        "Languages",
        "Certifications"
    ],
    "Personal Development": [
        "Work-Life Balance",
        "Personal Growth",
        "Life Goals",
        "Values & Beliefs",
        "Motivation & Drive"
    ],
    "Interests & Lifestyle": [
        "Hobbies",
        "Travel Experiences",
        "Cultural Interests",
        "Sports & Fitness",
        "Creative Pursuits"
    ],
    "Social & Relationships": [
        "Team Collaboration",
        "Cultural Background",
        "Community Involvement",
        "Mentorship",
        "Social Activities"
    ]
}

if st.session_state.interview_mode == "Subject Restricted":
    st.markdown("""
    <div style="margin-top: 15px;">
        <h4>Select Your Interview Focus</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        categories = sorted(list(subject_categories.keys()))
        selected_category = st.selectbox(
            "1️⃣ Select Category",
            ["General"] + categories,
            help="Choose a broad category to narrow down your focus area"
        )

    with col2:
        if selected_category == "General":
            selected_subject = "General"
        else:
            sorted_subjects = sorted(subject_categories[selected_category])
            selected_subject = st.selectbox(
                "2️⃣ Select Specific Focus",
                sorted_subjects,
                help="Choose a specific area within the selected category"
            )
    
    # Custom subject option
    use_custom = st.checkbox("🎯 Use Custom Subject", help="Define your own subject area")
    if use_custom:
        custom_subject = st.text_input("Enter Custom Subject", placeholder="e.g., Artificial Intelligence Ethics")
        new_subject = custom_subject if custom_subject else None
    else:
        new_subject = selected_subject.lower() if selected_subject != "General" else None

    # Update Subject button
    if st.button("📝 Update Interview Focus", type="primary", use_container_width=True):
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

st.markdown('</div>', unsafe_allow_html=True)

# Initialize tabs
tab1, tab2, tab3 = st.tabs(["Interview", "Context Review", "How it Works"])

with tab1:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Start New Interview", use_container_width=True):
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
        if st.button("End Interview", use_container_width=True):
            if st.session_state.messages:
                st.session_state.interview_complete = True
                st.session_state.context_data = extract_context(api_key, st.session_state.messages)
                st.rerun()

    with col3:
        if st.button("Export Conversation", use_container_width=True):
            if st.session_state.messages:
                filename = generate_markdown_filename(st.session_state.context_focus)
                st.download_button(
                    label="Download Chat",
                    data=st.session_state.context_data,
                    file_name=filename,
                    mime="text/markdown",
                    use_container_width=True
                )

    # Display chat messages
    for i, message in enumerate(st.session_state.messages):
        if message.startswith("Q: "):
            display_chat_message(message[3:], is_user=False)
        else:
            display_chat_message(message, is_user=True)

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
