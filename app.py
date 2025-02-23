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

# Custom CSS to adjust avatar size and message alignment
st.markdown("""
<style>
/* Increase avatar size */
.stChatMessage img {
    width: 120px !important;
    height: 120px !important;
}

/* Align user messages to the right */
[data-testid="chat-message-container"]:has([data-testid="chat-message-avatar"][src*="User"]) {
    flex-direction: row-reverse;
    margin-left: auto;
    margin-right: 0;
}

/* Add some spacing between messages */
[data-testid="chat-message-container"] {
    margin: 1rem 0;
    max-width: 85%;
}

/* Assistant messages to the left */
[data-testid="chat-message-container"]:has([data-testid="chat-message-avatar"]:not([src*="User"])) {
    margin-right: auto;
    margin-left: 0;
}
</style>
""", unsafe_allow_html=True)

# Custom CSS for chat UI and avatars
st.markdown("""
<style>
/* Increase avatar size */
.stChatMessage img {
    width: 120px !important;
    height: 120px !important;
}

/* Align user messages to the right */
[data-testid="chat-message-container"]:has([data-testid="chat-message-avatar"][src*="User"]) {
    flex-direction: row-reverse;
    margin-left: auto;
    margin-right: 0;
}

/* Add some spacing between messages */
[data-testid="chat-message-container"] {
    margin: 1rem 0;
    max-width: 85%;
}

/* Assistant messages to the left with bubble styling */
[data-testid="chat-message-container"]:has([data-testid="chat-message-avatar"]:not([src*="User"])) {
    margin-right: auto;
    margin-left: 0;
}

/* Chat bubble styling */
[data-testid="chat-message-container"] > div:nth-child(2) {
    border-radius: 15px;
    padding: 10px 15px;
}

/* Assistant message bubble */
[data-testid="chat-message-container"]:has([data-testid="chat-message-avatar"]:not([src*="User"])) > div:nth-child(2) {
    background-color: #f0f2f6;
    border-top-left-radius: 5px;
}

/* User message bubble */
[data-testid="chat-message-container"]:has([data-testid="chat-message-avatar"][src*="User"]) > div:nth-child(2) {
    background-color: #e3f2fd;
    border-top-right-radius: 5px;
}

/* Remove default message background */
.stChatMessage {
    background-color: transparent !important;
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

def get_random_topic(api_key):
    """Generate a completely random, potentially quirky topic for discussion."""
    client = openai.OpenAI(api_key=api_key)
    
    system_prompt = """You are Corn, a quirky sloth interviewer with an inexplicable fascination with anteaters.
    Generate ONE completely random, unexpected, and interesting topic or question to ask about.
    It can be about ANYTHING - the more surprising and unique, the better.
    Be creative and don't limit yourself to conventional categories.
    The topic should be engaging and thought-provoking, even if unconventional.
    Return ONLY the topic/question, nothing else."""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Generate a random, unexpected topic or question."}
            ],
            temperature=1.0,  # High temperature for more randomness
            max_tokens=50
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error generating random topic: {str(e)}")
        return None

def get_random_question(api_key, focus_area=None):
    """Get a random question from OpenAI based on optional focus area."""
    client = openai.OpenAI(api_key=api_key)
    
    system_prompt = """You are Corn, a friendly and quirky sloth who conducts interviews to help build context data. 
    While you take your mission seriously to gather meaningful information, you have a delightful personality and an inexplicable fascination with anteaters 
    (though you try not to let it show too much). Your goal is to ask engaging questions that help build a rich context profile for the user.
    
    If a specific focus area is provided, ensure your questions are relevant to that area while maintaining a natural conversational flow.
    Keep questions open-ended to encourage detailed responses. Avoid yes/no questions.
    Each response should be a single question that builds on previous responses when available."""

    messages = [
        {"role": "system", "content": system_prompt}
    ]

    if focus_area:
        messages.append({
            "role": "user", 
            "content": f"Ask me an engaging question about {focus_area}. Make it conversational and natural."
        })
    else:
        messages.append({
            "role": "user", 
            "content": "Ask me an engaging question to learn more about me. Make it conversational and natural."
        })

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error generating question: {str(e)}")
        return None

def extract_context(api_key, conversation):
    """Extract context from the conversation using OpenAI."""
    client = openai.OpenAI(api_key=api_key)
    
    system_prompt = """You are Corn, a diligent sloth assistant who excels at extracting and organizing meaningful context from conversations.
    While you occasionally daydream about anteaters, you stay focused on your primary mission: creating clear, well-structured context summaries.
    
    Analyze the conversation and create a detailed but concise summary that:
    1. Captures key information, insights, and patterns
    2. Organizes the information in a clear, logical structure
    3. Maintains the user's voice and perspective
    4. Focuses on substantive content rather than casual conversation
    5. Uses markdown formatting for better readability"""

    conversation_text = "\n".join(conversation)
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Please extract and organize the context from this conversation:\n\n{conversation_text}"}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.5,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error extracting context: {str(e)}")
        return None

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
        with st.chat_message("assistant", avatar="https://res.cloudinary.com/drrvnflqy/image/upload/v1740345962/corn-stickers_1_cqpgji.png"):
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

# Create two columns for the layout
left_col, right_col = st.columns([1, 1])

with left_col:
    # Interview Mode Selection
    st.markdown("### 📋 Interview Configuration")
    mode_col, random_col = st.columns([2, 1])
    
    with mode_col:
        st.session_state.interview_mode = st.radio(
            "Interview Mode",
            ["AMA (Ask Me Anything)", "Subject Restricted"],
            index=0 if st.session_state.interview_mode == "AMA (Ask Me Anything)" else 1,
            help="Choose between an open-ended interview or focus on specific subjects"
        )
    
    with random_col:
        if st.button("🎲 Random!", help="Let Corn surprise you with a completely random topic!", type="primary"):
            random_topic = get_random_topic(api_key)
            if random_topic:
                st.session_state.messages = []
                st.session_state.context_data = ""
                st.session_state.interview_started = True
                st.session_state.interview_complete = False
                st.session_state.context_focus = None
                st.session_state.messages.append(f"Q: {random_topic}")
                st.rerun()

with right_col:
    if st.session_state.interview_mode == "Subject Restricted":
        st.markdown("### Select Your Interview Focus")
        
        col1, col2 = st.columns(2)
        with col1:
            subject_categories = {
                "Biography & Background": [
                    "General Biography",
                    "Personal History",
                    "Family Background",
                    "Childhood & Upbringing",
                    "Life Milestones",
                    "Cultural Heritage",
                    "Geographic History",
                    "Family Traditions",
                    "Formative Experiences",
                    "Personal Timeline",
                    "Family Structure",
                    "Life Stories"
                ],
                "Health & Wellness": [
                    "General Health",
                    "Physical Health",
                    "Exercise Routine",
                    "Medical History",
                    "Diet & Nutrition",
                    "Sleep Habits",
                    "Health Goals",
                    "Wellness Practices",
                    "Preventive Care",
                    "Energy Levels",
                    "Recovery & Rest",
                    "Health Challenges"
                ],
                "Mental Health & Wellbeing": [
                    "General Mental Health",
                    "Emotional Awareness",
                    "Stress Management",
                    "Anxiety & Concerns",
                    "Coping Strategies",
                    "Mental Resilience",
                    "Therapy Experience",
                    "Self-Care Practices",
                    "Emotional Growth",
                    "Support Systems",
                    "Mental Health Goals",
                    "Personal Boundaries"
                ],
                "Children & Family Life": [
                    "General Parenting",
                    "Parenting Style",
                    "Child Development",
                    "Family Activities",
                    "Education Choices",
                    "Family Values",
                    "Work-Family Balance",
                    "Family Goals",
                    "Childcare Approach",
                    "Family Challenges",
                    "Family Traditions",
                    "Future Planning"
                ],
                "Inspirations & Influences": [
                    "General Influences",
                    "Role Models",
                    "Mentors & Teachers",
                    "Inspiring Books",
                    "Life-Changing Events",
                    "Creative Influences",
                    "Cultural Inspirations",
                    "Career Influences",
                    "Personal Heroes",
                    "Motivational Sources",
                    "Artistic Influences",
                    "Philosophical Influences"
                ],
                "Humor & Entertainment": [
                    "General Entertainment",
                    "Sense of Humor",
                    "Comedy Preferences",
                    "Entertainment Choices",
                    "Movie Tastes",
                    "TV Shows",
                    "Music Preferences",
                    "Gaming Interests",
                    "Reading Preferences",
                    "Social Media",
                    "Live Entertainment",
                    "Content Creation"
                ],
                "Personality & Character": [
                    "General Personality",
                    "Core Traits",
                    "Communication Style",
                    "Decision Making",
                    "Social Tendencies",
                    "Emotional Style",
                    "Leadership Style",
                    "Conflict Approach",
                    "Risk Tolerance",
                    "Adaptability",
                    "Personal Strengths",
                    "Growth Areas"
                ],
                "Food & Drink": [
                    "General Preferences",
                    "Favorite Cuisines",
                    "Cooking Skills",
                    "Dietary Choices",
                    "Restaurant Preferences",
                    "Beverage Choices",
                    "Food Adventures",
                    "Recipe Collection",
                    "Food Traditions",
                    "Dining Habits",
                    "Food Philosophy",
                    "Culinary Goals"
                ],
                "Career & Professional": [
                    "General Career",
                    "Professional Background",
                    "Technical Skills",
                    "Leadership Experience",
                    "Project Management",
                    "Industry Knowledge",
                    "Career Goals",
                    "Work Experience",
                    "Remote Work",
                    "Workplace Culture",
                    "Professional Development",
                    "Career Challenges"
                ],
                "Education & Skills": [
                    "General Education",
                    "Education History",
                    "Research Experience",
                    "Communication Skills",
                    "Problem-Solving",
                    "Languages",
                    "Certifications",
                    "Technical Training",
                    "Self-Learning",
                    "Academic Achievements",
                    "Study Methods",
                    "Learning Goals"
                ],
                "Personal Development": [
                    "General Growth",
                    "Work-Life Balance",
                    "Personal Growth",
                    "Life Goals",
                    "Values & Beliefs",
                    "Motivation & Drive",
                    "Time Management",
                    "Stress Management",
                    "Decision Making",
                    "Self-Awareness",
                    "Personal Challenges",
                    "Future Aspirations"
                ],
                "Interests & Lifestyle": [
                    "General Interests",
                    "Hobbies",
                    "Travel Experiences",
                    "Cultural Interests",
                    "Sports & Fitness",
                    "Creative Pursuits",
                    "Reading Habits",
                    "Entertainment",
                    "Food & Cuisine",
                    "Music & Arts",
                    "Technology Usage",
                    "Lifestyle Choices"
                ],
                "Social & Relationships": [
                    "General Social",
                    "Team Collaboration",
                    "Cultural Background",
                    "Community Involvement",
                    "Mentorship",
                    "Social Activities",
                    "Networking",
                    "Family Dynamics",
                    "Friendship",
                    "Social Impact",
                    "Communication Style",
                    "Cultural Exchange"
                ],
                "Innovation & Creativity": [
                    "General Innovation",
                    "Creative Process",
                    "Problem Innovation",
                    "Design Thinking",
                    "Ideation Methods",
                    "Creative Projects",
                    "Innovation Mindset",
                    "Creative Challenges",
                    "Artistic Expression",
                    "Technical Innovation",
                    "Creative Collaboration",
                    "Future Vision"
                ],
                "Beliefs & Values": [
                    "General Beliefs",
                    "Religious Views",
                    "Political Views",
                    "Moral Framework",
                    "Ethical Principles",
                    "Spiritual Practices",
                    "Cultural Values",
                    "Social Justice",
                    "Human Rights",
                    "Economic Views",
                    "Tradition & Heritage",
                    "Personal Philosophy"
                ],
                "Entertainment": [
                    "General Entertainment",
                    "Favorite Movies",
                    "Favorite TV Shows",
                    "Favorite Music",
                    "Favorite Books",
                    "Favorite Games",
                    "Favorite Sports",
                    "Favorite Hobbies",
                    "Favorite Travel Destinations",
                    "Favorite Food",
                    "Favorite Drink",
                    "Favorite Activities"
                ],
                "Worldview & Society": [
                    "General Perspective",
                    "Global Issues",
                    "Social Change",
                    "Environmental Views",
                    "Technology Impact",
                    "Future of Society",
                    "Cultural Perspectives",
                    "Education Systems",
                    "Healthcare Views",
                    "Economic Systems",
                    "Social Structures",
                    "World Challenges"
                ]
            }
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
    tab1.write("")  # Add some spacing
    for message in st.session_state.messages:
        if message.startswith("Q: "):
            with tab1.chat_message("assistant", avatar="https://res.cloudinary.com/drrvnflqy/image/upload/v1740345962/corn-stickers_1_cqpgji.png"):
                st.write(message[3:])
        else:
            with tab1.chat_message("user"):
                st.write(message)

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
