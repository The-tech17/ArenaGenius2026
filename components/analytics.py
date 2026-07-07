import streamlit as st
import pandas as pd
import random
import time

def render_analytics():
    """
    Renders visual analytics, incident trend charts, and volunteer workload.
    """
    st.markdown("## 📊 Venue Analytics & Predictive Logistics")
    st.markdown("Post-match egress statistics, incident categories breakdown, and volunteer workload indicators.")
    
    # Custom dashboard KPIs for Admins
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Avg. Response Time", "5.4 Min", "-1.2 Min Egress Target", delta_color="normal")
    with c2:
        st.metric("Total Solved Issues", "148 Cases", "+24 Cases Halftime", delta_color="normal")
    with c3:
        st.metric("Avg. Queue Wait Time", "18.5 Min", "+4.2 Min Metro Gate", delta_color="inverse")
    with c4:
        st.metric("Logistics Flow Rate", "1,240 fans/min", "+150 fans/min East Gate", delta_color="normal")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("### 🚨 Incidents by Category (24-Hour Window)")
        # Construct Pandas dataframe for bar chart
        categories_data = {
            "Category": ["Crowd Bottleneck", "Medical Assistance Needed", "Facilities/Spill Issue", "Ticketing/Scanner Failure"],
            "Count": [42, 18, 55, 33]
        }
        df_categories = pd.DataFrame(categories_data).set_index("Category")
        st.bar_chart(df_categories, color="#10b981") # World Cup Green
        
        st.markdown("### 🚇 Queue Lengths Over Match Timeline (Minutes)")
        # Construct timeline data
        timeline_data = {
            "Match Segment": ["Gates Open", "Pre-Match", "Kickoff", "Halftime", "Fulltime", "Egress Peak", "Clearance"],
            "Metro Gate A Queue": [15, 45, 10, 25, 60, 92, 20],
            "North Parking Shuttle": [5, 15, 5, 10, 25, 45, 10],
            "Rideshare Zone B": [10, 30, 8, 15, 50, 78, 15]
        }
        df_timeline = pd.DataFrame(timeline_data).set_index("Match Segment")
        st.line_chart(df_timeline)
        
    with col_right:
        st.markdown("### 🗣️ Fan Preferred Language Distribution")
        lang_data = {
            "Language": ["English", "Español", "Français", "Deutsch", "Português", "日本語"],
            "Share (%)": [35, 40, 10, 5, 6, 4]
        }
        df_lang = pd.DataFrame(lang_data).set_index("Language")
        st.bar_chart(df_lang, color="#fbbf24") # Gold Accent
        
        st.markdown("### 📍 Live Concourse Security Heatmap")
        st.caption("Coordinates showing active sensor warning levels across stadium sectors (X, Y plane).")
        # Scatter coordinate mock dataset
        heatmap_data = {
            "X Coord": [120, 420, 280, 180, 360, 250, 450, 150, 300, 220],
            "Y Coord": [150, 180, 250, 220, 120, 80, 240, 110, 310, 190],
            "Density Index": [80, 50, 95, 30, 40, 60, 75, 20, 88, 65]
        }
        df_heatmap = pd.DataFrame(heatmap_data)
        st.scatter_chart(df_heatmap, x="X Coord", y="Y Coord", size="Density Index", color="#f43f5e")
        
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("### 👥 Operational Resource Distribution")
        st.caption("Active volunteer workloads and team assignments.")
        
        res1, res2, res3 = st.columns(3)
        with res1:
            st.markdown("**🛡️ Security Command Alpha**")
            st.markdown("- Active deployment: `Gate C / South Concourse`\n- Handled cases: `14 cases today`\n- Workload: `High (94%)`")
        with res2:
            st.markdown("**🚑 Medical Response Team Bravo**")
            st.markdown("- Active deployment: `Main Clinic & Level 1`\n- Handled cases: `8 cases today`\n- Workload: `Optimal (45%)`")
        with res3:
            st.markdown("**🧹 Facilities Group Gamma**")
            st.markdown("- Active deployment: `Concourse Food Courts`\n- Handled cases: `22 cases today`\n- Workload: `Moderate (60%)`")
