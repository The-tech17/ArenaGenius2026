import streamlit as st
import os
import google.generativeai as genai

# Configure page layouts and branding
st.set_page_config(
    page_title="ArenaGenius 2026 - Smart Stadium Assistant",
    page_icon="⚽",
    layout="wide"
)

# Initialize Gemini API safely
# For local testing, set your environment variable or use a sidebar text input
api_key = os.environ.get("GEMINI_API_KEY") or st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.warning("Please provide a Gemini API Key to activate the AI features.")

# Application Header
st.title("⚽ ArenaGenius 2026")
st.subheader("Smart Stadium & Tournament Operations Assistant — FIFA World Cup 2026")

# Sidebar navigation for User Personas
persona = st.sidebar.selectbox(
    "Select Your Portal",
    ["Global Fan Companion", "Operational Incident Command (Staff/Volunteers)", "Live Crowd Analytics & Decision Support"]
)

# -------------------------------------------------------------------------
# PERSONA 1: GLOBAL FAN COMPANION
# -------------------------------------------------------------------------
if persona == "Global Fan Companion":
    st.header("🌍 International Fan Companion")
    st.write("Get real-time, multilingual guidance inside the stadium.")
    
    # Context inputs to make the AI decision-making highly logical
    stadium = st.selectbox("Select Stadium", ["MetLife Stadium (New York/New Jersey)", "SoFi Stadium (Los Angeles)", "Azteca Stadium (Mexico City)"])
    gate = st.text_input("Your Current Location / Entry Gate (e.g., Gate C, Section 214)", placeholder="e.g., Gate B")
    language = Skinner = st.selectbox("Preferred Language", ["English", "Español", "Français", "Deutsch", "Português", "日本語"])
    
    user_query = st.text_area("How can we help you today?", placeholder="e.g., Where is the nearest vegetarian food option from my section, and how do I get to the nearest exit?")

    if st.button("Get Instant Guidance") and api_key:
        with st.spinner("Analyzing stadium blueprint and context..."):
            # System prompt to enforce specific behavior, security, and context logic
            system_instruction = f"""
            You are ArenaGenius, an elite AI Concierge for the FIFA World Cup 2026 at {stadium}. 
            The user is currently near {gate}. Respond strictly in {language}.
            Provide concise, highly actionable, polite, and practical stadium navigation or policy answers.
            If safety rules are violated or out-of-scope questions are asked, politely redirect back to tournament operations.
            """
            
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=system_instruction
            )
            
            response = model.generate_content(user_query)
            st.success("✨ AI Guide Recommendation:")
            st.write(response.text)

# -------------------------------------------------------------------------
# PERSONA 2: OPERATIONAL INCIDENT COMMAND (STAFF/VOLUNTEERS)
# -------------------------------------------------------------------------
elif persona == "Operational Incident Command (Staff/Volunteers)":
    st.header("📋 Volunteer & Staff Incident Protocol Hub")
    st.write("Report live issues to receive automated, compliant operational steps.")
    
    incident_type = st.selectbox("Incident Category", ["Crowd Bottleneck", "Medical Assistance Needed", "Facilities/Spill Issue", "Ticketing/Scanner Failure"])
    location = st.text_input("Exact Location (e.g., Concourse Level 2, Pod 4)")
    severity = st.radio("Severity Level", ["Low (Routine)", "Medium (Requires Attention)", "High (Immediate Escalation Required)"])
    details = st.text_area("Describe the situation details:")
    
    if st.button("Generate Protocol & Action Plan") and api_key:
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
    st.header("📊 Real-time Dispersal & Decision Support Matrix")
    st.write("Generates real-time announcements and traffic routing logic based on stadium outflow data post-match.")
    
    # Mock data to demonstrate decision-making inputs
    st.subheader("Current Match Outflow Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Main Metro Line Gate", "92% Capacity", "Heavy Bottleneck")
    col2.metric("North Parking Shuttle Zone", "45% Capacity", "Optimal Flow")
    col3.metric("Rideshare Zone B", "78% Capacity", "Moderate Delay")
    
    announcement_tone = st.selectbox("Announcement Strategy", ["Standard Directing", "Emergency Rerouting", "Sustainability Focus (Encouraging Walking/Buses)"])
    
    if st.button("Formulate Routing Strategy") and api_key:
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