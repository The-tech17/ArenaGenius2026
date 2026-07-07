import streamlit as st
import os
import google.generativeai as genai

# Configure page layouts and branding
st.set_page_config(
    page_title="ArenaGenius 2026 - Smart Stadium Assistant",
    page_icon="⚽",
    layout="wide"
)

# Sidebar navigation & settings
with st.sidebar:
    st.markdown("### 🏟️ Portal Settings")
    persona = st.selectbox(
        "Select Your Portal",
        ["Global Fan Companion", "Operational Incident Command (Staff/Volunteers)", "Live Crowd Analytics & Decision Support"]
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ Preferences & API")
    theme = st.selectbox(
        "🌓 Select Theme",
        ["System Default", "Light Mode", "Dark Mode"],
        index=0
    )
    
    api_key_input = ""
    if not os.environ.get("GEMINI_API_KEY"):
        api_key_input = st.text_input("Enter Gemini API Key", type="password")
    
    api_key = os.environ.get("GEMINI_API_KEY") or api_key_input

if api_key:
    genai.configure(api_key=api_key)
else:
    st.warning("Please provide a Gemini API Key to activate the AI features.")

# Inject CSS Themes & Global Styles
# Theme styles mapping
if theme == "Dark Mode":
    css_theme = """
    :root {
        --background: #0b0f19;
        --text: #f8fafc;
        --sidebar-bg: #111827;
        --card-bg: #1f2937;
        --card-border: #374151;
        --primary: #3b82f6;
        --accent: #60a5fa;
        --success: #34d399;
        --info: #22d3ee;
        --warning: #fbbf24;
        --danger: #f87171;
        --muted: #9ca3af;
        --radius: 12px;
        --shadow: 0 10px 15px -3px rgb(0 0 0 / 0.3), 0 4px 6px -4px rgb(0 0 0 / 0.3);
    }
    """
elif theme == "Light Mode":
    css_theme = """
    :root {
        --background: #f8fafc;
        --text: #0f172a;
        --sidebar-bg: #ffffff;
        --card-bg: #ffffff;
        --card-border: #e2e8f0;
        --primary: #2563eb;
        --accent: #3b82f6;
        --success: #10b981;
        --info: #06b6d4;
        --warning: #f59e0b;
        --danger: #ef4444;
        --muted: #64748b;
        --radius: 12px;
        --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05), 0 2px 4px -2px rgb(0 0 0 / 0.05);
    }
    """
else:  # System Default
    css_theme = """
    :root {
        --background: #0b0f19;
        --text: #f8fafc;
        --sidebar-bg: #111827;
        --card-bg: #1f2937;
        --card-border: #374151;
        --primary: #3b82f6;
        --accent: #60a5fa;
        --success: #34d399;
        --info: #22d3ee;
        --warning: #fbbf24;
        --danger: #f87171;
        --muted: #9ca3af;
        --radius: 12px;
        --shadow: 0 10px 15px -3px rgb(0 0 0 / 0.3), 0 4px 6px -4px rgb(0 0 0 / 0.3);
    }
    @media (prefers-color-scheme: light) {
        :root {
            --background: #f8fafc;
            --text: #0f172a;
            --sidebar-bg: #ffffff;
            --card-bg: #ffffff;
            --card-border: #e2e8f0;
            --primary: #2563eb;
            --accent: #3b82f6;
            --success: #10b981;
            --info: #06b6d4;
            --warning: #f59e0b;
            --danger: #ef4444;
            --muted: #64748b;
            --radius: 12px;
            --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05), 0 2px 4px -2px rgb(0 0 0 / 0.05);
        }
    }
    """

st.markdown(
    f"""
    <style>
    {css_theme}
    
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    .stApp {{
        background-color: var(--background) !important;
        color: var(--text) !important;
        font-family: 'Outfit', sans-serif !important;
    }}
    
    /* Revert Material Symbols/Icons font-family to Streamlit defaults to avoid text ligatures showing */
    [data-testid="stIconMaterial"], 
    .material-symbols-outlined, 
    .material-icons,
    .stIcon,
    [class*="material-symbols"], 
    [class*="material-icons"] {{
        font-family: 'Material Symbols Outlined', 'Material Symbols Rounded', 'Material Symbols Sharp', 'Material Icons', sans-serif !important;
    }}
    
    [data-testid="stSidebar"] {{
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid var(--card-border) !important;
    }}
    
    h1, h2, h3, h4, h5, h6, p, li, label, select, textarea, input {{
        font-family: 'Outfit', sans-serif !important;
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        color: var(--text) !important;
        font-weight: 600 !important;
    }}
    
    p, span, label, [data-testid="stMarkdownContainer"] p {{
        color: var(--text) !important;
    }}
    
    div[data-baseweb="input"], div[data-baseweb="select"] > div, textarea, input {{
        background-color: var(--card-bg) !important;
        color: var(--text) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: var(--radius) !important;
        transition: all 0.2s ease-in-out !important;
    }}
    div[data-baseweb="select"] > div * {{
        color: var(--text) !important;
    }}
    div[data-baseweb="input"]:focus-within, div[data-baseweb="select"]:focus-within > div, textarea:focus, input:focus {{
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }}
    
    div[role="listbox"] ul li,
    ul[data-testid="stSelectboxVirtualDropdown"] li[role="option"] {{
        font-family: 'Outfit', sans-serif !important;
        background-color: var(--card-bg) !important;
        color: var(--text) !important;
        transition: background-color 0.2s ease-in-out !important;
    }}
    div[role="listbox"] ul li:hover,
    ul[data-testid="stSelectboxVirtualDropdown"] li[role="option"]:hover {{
        background-color: var(--primary) !important;
        color: white !important;
    }}
    
    div[data-testid="stButton"] button {{
        font-family: 'Outfit', sans-serif !important;
        background-color: var(--primary) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius) !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        box-shadow: var(--shadow) !important;
        transition: all 0.2s ease-in-out !important;
        width: 100% !important;
    }}
    div[data-testid="stButton"] button:hover {{
        background-color: var(--accent) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    }}
    div[data-testid="stButton"] button:active {{
        transform: translateY(0) !important;
    }}
    
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: var(--radius) !important;
        padding: 1.5rem !important;
        box-shadow: var(--shadow) !important;
        margin-bottom: 1.5rem !important;
    }}
    
    div[data-testid="metric-container"] {{
        background-color: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: var(--radius) !important;
        padding: 1rem !important;
        box-shadow: var(--shadow) !important;
    }}
    div[data-testid="stMetricLabel"] {{
        font-family: 'Outfit', sans-serif !important;
        color: var(--muted) !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }}
    div[data-testid="stMetricValue"] {{
        font-family: 'Outfit', sans-serif !important;
        color: var(--text) !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }}
    
    div[data-testid="stAlert"] {{
        font-family: 'Outfit', sans-serif !important;
        border-radius: var(--radius) !important;
        background-color: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        box-shadow: var(--shadow) !important;
    }}
    
    .stDeployButton {{
        display: none !important;
    }}
    [data-testid="stHeader"] {{
        background-color: transparent !important;
    }}
    
    div[data-testid="stRadio"] > label {{
        color: var(--text) !important;
    }}
    div[data-testid="stRadio"] div[role="radiogroup"] {{
        gap: 1.5rem !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Application Header (Vibrant premium banner)
st.markdown(
    """
    <div style="
        background: linear-gradient(135deg, #1e40af, #3b82f6, #06b6d4);
        padding: 2.5rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 2.5rem;
        box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.4);
    ">
        <h1 style="color: white !important; font-size: 2.5rem; font-weight: 800; margin: 0; text-shadow: 0 2px 4px rgba(0,0,0,0.15);">⚽ ArenaGenius 2026</h1>
        <p style="color: rgba(255, 255, 255, 0.9) !important; font-size: 1.1rem; margin-top: 0.5rem; margin-bottom: 0; font-weight: 500;">
            Smart Stadium & Tournament Operations Assistant — FIFA World Cup 2026
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------------------------------
# PERSONA 1: GLOBAL FAN COMPANION
# -------------------------------------------------------------------------
if persona == "Global Fan Companion":
    st.markdown("## 🌍 International Fan Companion")
    st.markdown("Get real-time, multilingual guidance inside the stadium.")
    
    with st.container(border=True):
        st.markdown("### 🎫 Location & Language")
        col1, col2 = st.columns(2)
        with col1:
            stadium = st.selectbox("Select Stadium", ["MetLife Stadium (New York/New Jersey)", "SoFi Stadium (Los Angeles)", "Azteca Stadium (Mexico City)"])
        with col2:
            language = st.selectbox("Preferred Language", ["English", "Español", "Français", "Deutsch", "Português", "日本語"])
            
        gate = st.text_input("Your Current Location / Entry Gate (e.g., Gate C, Section 214)", placeholder="e.g., Gate B")
        
    with st.container(border=True):
        st.markdown("### ❓ Ask ArenaGenius")
        user_query = st.text_area("How can we help you today?", placeholder="e.g., Where is the nearest vegetarian food option from my section, and how do I get to the nearest exit?")
        
        get_guidance = st.button("Get Instant Guidance")

    if get_guidance and api_key:
        with st.spinner("Analyzing stadium blueprint and context..."):
            # System prompt to enforce specific behavior, security, and context logic
            system_instruction = f"""
            You are ArenaGenius, an elite AI Concierge for the FIFA World Cup 2026 at {stadium}. 
            The user is currently near {gate}. Respond strictly in {language}.
            Provide concise, highly actionable, polite, and practical stadium navigation or policy answers.
            If safety rules are violated or out-of-scope questions are asked, politely redirect back to tournament operations.
            """
            
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash",
                system_instruction=system_instruction
            )
            
            response = model.generate_content(user_query)
            st.success("✨ AI Guide Recommendation:")
            st.write(response.text)

# -------------------------------------------------------------------------
# PERSONA 2: OPERATIONAL INCIDENT COMMAND (STAFF/VOLUNTEERS)
# -------------------------------------------------------------------------
elif persona == "Operational Incident Command (Staff/Volunteers)":
    st.markdown("## 📋 Volunteer & Staff Incident Protocol Hub")
    st.markdown("Report live issues to receive automated, compliant operational steps.")
    
    with st.container(border=True):
        st.markdown("### ⚠️ Incident Information")
        col1, col2 = st.columns(2)
        with col1:
            incident_type = st.selectbox("Incident Category", ["Crowd Bottleneck", "Medical Assistance Needed", "Facilities/Spill Issue", "Ticketing/Scanner Failure"])
        with col2:
            location = st.text_input("Exact Location (e.g., Concourse Level 2, Pod 4)")
            
        severity = st.radio("Severity Level", ["Low (Routine)", "Medium (Requires Attention)", "High (Immediate Escalation Required)"], horizontal=True)
        
    with st.container(border=True):
        st.markdown("### 📝 Incident Details")
        details = st.text_area("Describe the situation details:")
        
        generate_plan = st.button("Generate Protocol & Action Plan")
    
    if generate_plan and api_key:
        with st.spinner("Synthesizing standard operating procedures..."):
            staff_prompt = f"""
            Context: A FIFA World Cup 2026 stadium staff member has reported an issue.
            Incident Type: {incident_type}
            Location: {location}
            Severity: {severity}
            Details: {details}
            
            Task: Provide a clear, step-by-step checklist of immediate physical actions the staff member should take. Include communication protocols (who to radio) and safety measures. Keep it highly professional and direct.
            """
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(staff_prompt)
            
            st.info("⚡ Immediate Action Plan Generated:")
            st.write(response.text)

# -------------------------------------------------------------------------
# PERSONA 3: LIVE CROWD ANALYTICS & DECISION SUPPORT
# -------------------------------------------------------------------------
elif persona == "Live Crowd Analytics & Decision Support":
    st.markdown("## 📊 Real-time Dispersal & Decision Support Matrix")
    st.markdown("Generates real-time announcements and traffic routing logic based on stadium outflow data post-match.")
    
    with st.container(border=True):
        st.markdown("### 🏟️ Current Match Outflow Metrics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Main Metro Line Gate", "92% Capacity", "Heavy Bottleneck", delta_color="inverse")
        with col2:
            st.metric("North Parking Shuttle Zone", "45% Capacity", "Optimal Flow", delta_color="normal")
        with col3:
            st.metric("Rideshare Zone B", "78% Capacity", "Moderate Delay", delta_color="inverse")
            
    with st.container(border=True):
        st.markdown("### 📢 Announcement Strategy")
        announcement_tone = st.selectbox("Announcement Strategy", ["Standard Directing", "Emergency Rerouting", "Sustainability Focus (Encouraging Walking/Buses)"])
        
        formulate_strategy = st.button("Formulate Routing Strategy")
        
    if formulate_strategy and api_key:
        with st.spinner("Calculating optimal dispersal parameters..."):
            analytics_prompt = f"""
            Analyze this post-match logistics state:
            - Metro Gate: 92% capacity (Bottlenecked)
            - North Shuttle: 45% capacity (Clear)
            - Rideshare Zone B: 78% capacity (Delayed)
            
            Generate:
            1. An optimization recommendation for stadium managers on how to divert foot traffic.
            2. A clear, friendly public PA audio announcement script matching a '{announcement_tone}' tone to seamlessly steer fans toward underutilized transit assets without causing panic.
            """
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(analytics_prompt)
            st.success("📈 Strategic Directives:")
            st.write(response.text)
