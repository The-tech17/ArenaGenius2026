import streamlit as st
import time
from utils.data_simulator import initialize_simulation_state, run_simulation_tick

def render_dashboard():
    """
    Renders the live tactical operations dashboard showing stadium state.
    """
    initialize_simulation_state()
    run_simulation_tick()
    
    st.markdown("## 🏟️ Venue Operations Control Center")
    st.markdown("Real-time telemetry, incident dispatch status, and dispersal tracking for the match organizers.")
    
    # Live Telemetry indicator
    st.markdown(
        """
        <div class="pulse-container">
            <div class="pulse-dot"></div>
            <span>LIVE TELEMETRY STREAM ACTIVE</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 6-Card Dashboard Grid using custom columns and styles
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    
    with col1:
        st.markdown(
            f"""
            <div class="ops-card">
                <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">👥</div>
                <div style="font-size: 0.85rem; color: var(--muted); text-transform: uppercase; font-weight: 600;">Live Attendance</div>
                <div style="font-size: 1.8rem; font-weight: 700; font-family: 'Rajdhani', sans-serif; color: var(--text);">
                    {st.session_state.attendance:,} Fans
                </div>
                <div style="font-size: 0.75rem; color: var(--primary); margin-top: 0.25rem;">● 92.7% Venue Capacity</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
    with col2:
        # Highlight if incidents are present
        inc_count = len([i for i in st.session_state.incidents_db if i["status"] != "Resolved"])
        color = "var(--danger)" if inc_count > 0 else "var(--success)"
        st.markdown(
            f"""
            <div class="ops-card">
                <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">🚨</div>
                <div style="font-size: 0.85rem; color: var(--muted); text-transform: uppercase; font-weight: 600;">Active Incidents</div>
                <div style="font-size: 1.8rem; font-weight: 700; font-family: 'Rajdhani', sans-serif; color: {color};">
                    {inc_count} Cases
                </div>
                <div style="font-size: 0.75rem; color: var(--muted); margin-top: 0.25rem;">● Tactical teams dispatched</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
    with col3:
        med_count = len([i for i in st.session_state.incidents_db if i["type"] == "Medical Assistance Needed" and i["status"] != "Resolved"])
        color = "#0ea5e9" if med_count > 0 else "var(--muted)"
        st.markdown(
            f"""
            <div class="ops-card">
                <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">🚑</div>
                <div style="font-size: 0.85rem; color: var(--muted); text-transform: uppercase; font-weight: 600;">Medical Alerts</div>
                <div style="font-size: 1.8rem; font-weight: 700; font-family: 'Rajdhani', sans-serif; color: {color};">
                    {med_count} Cases
                </div>
                <div style="font-size: 0.75rem; color: var(--muted); margin-top: 0.25rem;">● Medics on high alert</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
    with col4:
        st.markdown(
            f"""
            <div class="ops-card" style="margin-top: 1rem;">
                <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">🚪</div>
                <div style="font-size: 0.85rem; color: var(--muted); text-transform: uppercase; font-weight: 600;">Gates Status</div>
                <div style="font-size: 1.8rem; font-weight: 700; font-family: 'Rajdhani', sans-serif; color: var(--success);">
                    {st.session_state.gates_status}
                </div>
                <div style="font-size: 0.75rem; color: var(--muted); margin-top: 0.25rem;">● Egress routes configured</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
    with col5:
        st.markdown(
            f"""
            <div class="ops-card" style="margin-top: 1rem;">
                <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">🌦</div>
                <div style="font-size: 0.85rem; color: var(--muted); text-transform: uppercase; font-weight: 600;">Weather Status</div>
                <div style="font-size: 1.8rem; font-weight: 700; font-family: 'Rajdhani', sans-serif; color: var(--text);">
                    {st.session_state.weather_temp}°C • {st.session_state.weather_cond}
                </div>
                <div style="font-size: 0.75rem; color: var(--muted); margin-top: 0.25rem;">● Winds NE 8 km/h</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
    with col6:
        color = "var(--text)" if st.session_state.metro_delay == "None" else "var(--accent)"
        st.markdown(
            f"""
            <div class="ops-card" style="margin-top: 1rem;">
                <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">🚇</div>
                <div style="font-size: 0.85rem; color: var(--muted); text-transform: uppercase; font-weight: 600;">Metro Delay</div>
                <div style="font-size: 1.8rem; font-weight: 700; font-family: 'Rajdhani', sans-serif; color: {color};">
                    {st.session_state.metro_delay}
                </div>
                <div style="font-size: 0.75rem; color: var(--muted); margin-top: 0.25rem;">● Integrated transit link</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
    # Bottom Layout: Left: Active Log Feed, Right: Telemetry Feeds
    st.markdown("<br>", unsafe_allow_html=True)
    c_left, c_right = st.columns([1.3, 1])
    
    with c_left:
        st.markdown("### 📋 Active Tactical Incident List")
        if not st.session_state.incidents_db:
            st.info("No active incidents currently logged.")
        else:
            for inc in st.session_state.incidents_db:
                # Severity badge selection
                if "Low" in inc["severity"]:
                    s_badge = "badge-success"
                elif "Medium" in inc["severity"]:
                    s_badge = "badge-warning"
                else:
                    s_badge = "badge-danger"
                    
                st.markdown(
                    f"""
                    <div style="
                        background-color: var(--card-bg); 
                        border: 1px solid var(--card-border); 
                        padding: 1rem; 
                        border-radius: 12px; 
                        margin-bottom: 0.75rem;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    ">
                        <div>
                            <span style="font-family: 'Rajdhani', sans-serif; font-weight:700; color: var(--accent); font-size:1.1rem; margin-right: 10px;">{inc['id']}</span>
                            <strong style="color: var(--text); font-size: 0.95rem;">{inc['type']}</strong>
                            <div style="font-size:0.8rem; color:var(--muted); margin-top: 2px;">
                                📍 {inc['location']} • ⏱ Reported {inc['timestamp']}
                            </div>
                        </div>
                        <div style="text-align: right; display:flex; flex-direction:column; align-items:flex-end; gap:5px;">
                            <span class="badge {s_badge}">{inc['risk_label']} ({inc['risk_score']}%)</span>
                            <span style="font-size:0.75rem; color:#fbbf24; font-weight:600;">📟 {inc['assigned']} (ETA {inc['eta']})</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
    with c_right:
        st.markdown("### 📡 Live Operations Log")
        
        # Display simulated telemetry log feed
        logs_html = "".join([
            f"<div style='font-size:0.85rem; padding: 0.4rem 0; border-bottom: 1px solid rgba(255,255,255,0.05); color: var(--text); font-family: monospace;'>{log}</div>"
            for log in st.session_state.telemetry_feed
        ])
        st.markdown(
            f"""
            <div style="
                background-color: #020617; 
                border: 1px solid var(--card-border); 
                border-radius: 12px; 
                padding: 1rem;
                height: 270px;
                overflow-y: auto;
            ">
                {logs_html}
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Simulation Controls Panel
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("#### ⚡ Simulation Controller")
            st.caption("Auto-refresh simulates changing crowd density, logs, and transit details live.")
            
            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                if st.button("Trigger Random Incident"):
                    mock_inc_types = ["Crowd Bottleneck", "Medical Assistance Needed", "Facilities/Spill Issue", "Ticketing/Scanner Failure"]
                    mock_locs = ["North Concourse", "East Concourse", "South Concourse", "West Concourse", "Seating Bowl"]
                    mock_sevs = ["Low (Routine)", "Medium (Requires Attention)", "High (Immediate Escalation Required)"]
                    
                    m_type = random.choice(mock_inc_types)
                    m_loc = random.choice(mock_locs)
                    m_sev = random.choice(mock_sevs)
                    
                    # Create mock record
                    m_id = f"INC-2026-{random.randint(10000, 99999)}"
                    m_score = random.randint(20, 95)
                    m_label = "High 🔴" if m_score > 70 else ("Medium 🟡" if m_score > 40 else "Low 🟢")
                    
                    teams = {"Low (Routine)": "Facilities Team Gamma", "Medium (Requires Attention)": "Crowd Unit Epsilon", "High (Immediate Escalation Required)": "Security Team Alpha"}
                    etas = {"Low (Routine)": "15 min", "Medium (Requires Attention)": "8 min", "High (Immediate Escalation Required)": "4 min"}
                    
                    new_m_inc = {
                        "id": m_id,
                        "type": m_type,
                        "location": m_loc,
                        "severity": m_sev,
                        "details": f"Simulated auto-generated report for {m_type}.",
                        "risk_score": m_score,
                        "risk_label": m_label,
                        "assigned": teams[m_sev],
                        "eta": etas[m_sev],
                        "timestamp": time.strftime("%I:%M %p"),
                        "status": "Queued"
                    }
                    st.session_state.incidents_db.insert(0, new_m_inc)
                    st.session_state.telemetry_feed.insert(0, f"{new_m_inc['timestamp']} - Simulator Alert: Mock incident {m_id} created.")
                    st.toast(f"Simulator logged new incident: {m_id}", icon="🚨")
                    st.rerun()
            with c_btn2:
                if st.button("Simulate Telemetry Update"):
                    # Manually force telemetry update
                    st.session_state.attendance += random.randint(-50, 60)
                    st.session_state.weather_temp = max(18, min(32, st.session_state.weather_temp + random.choice([-1, 0, 1])))
                    st.session_state.telemetry_feed.insert(0, f"{time.strftime('%I:%M %p')} - Telemetry: Checked gate sensors. Attendance: {st.session_state.attendance}")
                    st.toast("Telemetry data recalculated!", icon="📈")
                    st.rerun()
