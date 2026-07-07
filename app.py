import streamlit as st
import os
import google.generativeai as genai
from utils.theme import get_theme_css, render_header
from utils.data_simulator import initialize_simulation_state, run_simulation_tick
from components.dashboard import render_dashboard
from components.fan_companion import render_fan_companion
from components.incident_command import render_incident_hub
from components.analytics import render_analytics

# 1. Page Config
st.set_page_config(
    page_title="ArenaGenius 2026 - Smart Stadium Platform",
    page_icon="⚽",
    layout="wide"
)

# 2. State & Telemetry Setup
initialize_simulation_state()

# 3. Sidebar Configuration & Preferences
with st.sidebar:
    st.markdown("### 🏟️ ArenaGenius 2026")
    st.markdown("FIFA World Cup Operations Portal")
    
    st.markdown("<div class='sidebar-section-header'>🏟️ VENUE VIEW</div>", unsafe_allow_html=True)
    
    # Hierarchical Navigation choices
    nav_choices = [
        "🏟 Dashboard",
        "👥 International Companion",
        "💬 Chat Assistant",
        "❓ FAQ Directory",
        "🚨 Incident Hub",
        "📊 Operational Analytics",
        "⚙ Portal Settings"
    ]
    
    # Maintain active page selection in session state
    if "current_page" not in st.session_state:
        st.session_state.current_page = "🏟 Dashboard"
        
    page = st.radio(
        "Navigation",
        nav_choices,
        label_visibility="collapsed",
        index=nav_choices.index(st.session_state.current_page)
    )
    st.session_state.current_page = page
    
    st.markdown("---")
    st.caption("Active Stadium: MetLife Stadium (NY/NJ)")

# 4. Preferences & Settings Data (Loaded from state or sidebar defaults)
if "theme_pref" not in st.session_state:
    st.session_state.theme_pref = "System Default"

if "api_key" not in st.session_state:
    st.session_state.api_key = os.environ.get("GEMINI_API_KEY", "")

# 5. Inject Dynamic Style
st.markdown(get_theme_css(st.session_state.theme_pref), unsafe_allow_html=True)

# 6. Configure Gemini GenAI SDK
if st.session_state.api_key:
    genai.configure(api_key=st.session_state.api_key)
else:
    st.sidebar.warning("🔑 Gemini API Key required for full decision support.")

# 7. Render Header Banner (Taller on Home Dashboard, 40% reduced height on other sections)
is_home = (page == "🏟 Dashboard")
render_header(is_compact=not is_home)

# 8. Main Router
if page == "🏟 Dashboard":
    render_dashboard()
    
elif page == "👥 International Companion":
    render_fan_companion(st.session_state.api_key)
    # Force default active tab inside components if needed, handled inside fan_companion
    
elif page == "💬 Chat Assistant":
    # Let fan companion show chat assistant tab
    # To bypass tab defaults, we can change component tabs manually, or standard tabs work nicely
    render_fan_companion(st.session_state.api_key)
    
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
elif page == "❓ FAQ Directory":
    render_fan_companion(st.session_state.api_key)
    
elif page == "🚨 Incident Hub":
    render_incident_hub(st.session_state.api_key)
>>>>>>> 5f9cb66 (Modified UI and polished the app)
    
elif page == "📊 Operational Analytics":
    render_analytics()
    
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

elif page == "⚙ Portal Settings":
    st.markdown("## ⚙ Settings & Sandbox Operations")
    st.markdown("Configure core interfaces, API bindings, and clear telemetry databases.")
    
    with st.container(border=True):
        st.markdown("### 🔑 API Authentication")
        api_val = st.text_input(
            "Gemini API Key", 
            value=st.session_state.api_key, 
            type="password",
            help="Allows calculations and automated incident checklists."
        )
        if api_val != st.session_state.api_key:
            st.session_state.api_key = api_val
            st.rerun()
            
    with st.container(border=True):
        st.markdown("### 🌓 UI Preferences")
        theme_val = st.selectbox(
            "Select Portal Theme",
            ["System Default", "Light Mode", "Dark Mode"],
            index=["System Default", "Light Mode", "Dark Mode"].index(st.session_state.theme_pref)
        )
        if theme_val != st.session_state.theme_pref:
            st.session_state.theme_pref = theme_val
            st.rerun()
            

            Generate:
            1. An optimization recommendation for stadium managers on how to divert foot traffic.
            2. A clear, friendly public PA audio announcement script matching a '{announcement_tone}' tone to seamlessly steer fans toward underutilized transit assets without causing panic.
            """
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(analytics_prompt)
            st.success("📈 Strategic Directives:")
            st.write(response.text)
    with st.container(border=True):
        st.markdown("### 🧹 Database Resets")
        st.caption("Clears logged incidents and telemetry streams.")
        if st.button("Reset Telemetry Database"):
            st.session_state.pop("sim_initialized", None)
            st.session_state.pop("incidents_db", None)
            st.session_state.pop("telemetry_feed", None)
            st.toast("Telemetry data reset to defaults!", icon="🧹")
            st.rerun()
