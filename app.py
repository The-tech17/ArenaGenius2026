import os

import google.generativeai as genai
import streamlit as st

from components.analytics import render_analytics
from components.dashboard import render_dashboard
from components.fan_companion import render_fan_companion
from components.incident_command import render_incident_hub
from utils.data_simulator import initialize_simulation_state
from utils.theme import get_theme_css, render_header


from utils.security import is_valid_api_key

st.set_page_config(
    page_title="ArenaGenius 2026 - Smart Stadium Platform",
    page_icon="AG",
    layout="wide",
)

initialize_simulation_state()

with st.sidebar:
    st.markdown("### ARENAGENIUS 2026")
    st.markdown("FIFA World Cup Operations Portal")
    st.markdown(
        """
        <div class="sidebar-badge-row">
            <strong>Operations Mode</strong>
            <span>LIVE</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='sidebar-section-header'>VENUE VIEW</div>", unsafe_allow_html=True)

    nav_choices = [
        "Dashboard",
        "International Companion",
        "Chat Assistant",
        "FAQ Directory",
        "Incident Hub",
        "Operational Analytics",
        "Portal Settings",
    ]

    if "current_page" not in st.session_state:
        st.session_state.current_page = "Dashboard"

    page = st.radio(
        "Navigation",
        nav_choices,
        label_visibility="collapsed",
        index=nav_choices.index(st.session_state.current_page),
    )
    st.session_state.current_page = page

    st.markdown("---")
    st.caption("Active Stadium: MetLife Stadium (NY/NJ)")
    st.caption("Alerts: Medical 1 | Security 3 | Systems 0")

if "theme_pref" not in st.session_state:
    st.session_state.theme_pref = "System Default"

if "api_key" not in st.session_state:
    st.session_state.api_key = os.environ.get("GEMINI_API_KEY", "")

st.markdown(get_theme_css(st.session_state.theme_pref), unsafe_allow_html=True)

if is_valid_api_key(st.session_state.api_key):
    genai.configure(api_key=st.session_state.api_key)
else:
    st.sidebar.warning("Valid Gemini API Key required for full decision support.")

is_home = page == "Dashboard"
render_header(is_compact=not is_home)

if page == "Dashboard":
    render_dashboard()
elif page == "International Companion":
    render_fan_companion(st.session_state.api_key)
elif page == "Chat Assistant":
    render_fan_companion(st.session_state.api_key)
elif page == "FAQ Directory":
    render_fan_companion(st.session_state.api_key)
elif page == "Incident Hub":
    render_incident_hub(st.session_state.api_key)
elif page == "Operational Analytics":
    render_analytics()
elif page == "Portal Settings":
    st.markdown("## Settings & Sandbox Operations")
    st.markdown("Configure core interfaces, API bindings, and clear telemetry databases.")

    with st.container(border=True):
        st.markdown("### API Authentication")
        api_val = st.text_input(
            "Gemini API Key",
            value=st.session_state.api_key,
            type="password",
            help="Allows calculations and automated incident checklists.",
        )
        if api_val != st.session_state.api_key:
            if not api_val:
                st.session_state.api_key = ""
                st.rerun()
            elif is_valid_api_key(api_val):
                st.session_state.api_key = api_val
                st.rerun()
            else:
                st.error("Invalid API key format. Key must start with 'AIzaSy' and be at least 30 characters.")

    with st.container(border=True):
        st.markdown("### UI Preferences")
        theme_val = st.selectbox(
            "Select Portal Theme",
            ["System Default", "Light Mode", "Dark Mode"],
            index=["System Default", "Light Mode", "Dark Mode"].index(st.session_state.theme_pref),
        )
        if theme_val != st.session_state.theme_pref:
            st.session_state.theme_pref = theme_val
            st.rerun()

    with st.container(border=True):
        st.markdown("### Database Resets")
        st.caption("Clears logged incidents and telemetry streams.")
        if st.button("Reset Telemetry Database"):
            st.session_state.pop("sim_initialized", None)
            st.session_state.pop("incidents_db", None)
            st.session_state.pop("telemetry_feed", None)
            st.toast("Telemetry data reset to defaults.")
            st.rerun()
