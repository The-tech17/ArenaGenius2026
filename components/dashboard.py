import random
import time
from datetime import datetime, timedelta, timezone

import streamlit as st

from utils.data_simulator import initialize_simulation_state, run_simulation_tick
from utils.theme import clean_html


STADIUM_NAME = "MetLife Stadium"
MATCH_NAME = "USA vs Germany"
CAPACITY = 82500
KICKOFF_TIME = datetime.now(timezone.utc) + timedelta(hours=2, minutes=14, seconds=18)


def _status_dot(color="var(--success)"):
    return f"<span class='status-dot' style='--dot-color:{color}'></span>"


def _sparkline(points, color="var(--primary)"):
    width = 126
    height = 38
    max_val = max(points)
    min_val = min(points)
    spread = max(max_val - min_val, 1)
    coords = []
    for idx, point in enumerate(points):
        x = idx * (width / (len(points) - 1))
        y = height - ((point - min_val) / spread * (height - 8)) - 4
        coords.append(f"{x:.1f},{y:.1f}")
    return f"""
    <svg class="sparkline" viewBox="0 0 {width} {height}" aria-hidden="true">
        <polyline points="{' '.join(coords)}" fill="none" stroke="{color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
        <linearGradient id="sparkFill" x1="0" x2="0" y1="0" y2="1">
            <stop offset="0%" stop-color="{color}" stop-opacity="0.22"/>
            <stop offset="100%" stop-color="{color}" stop-opacity="0"/>
        </linearGradient>
    </svg>
    """


def _metric_card(title, value, trend, comparison, updated, status, spark_points, color):
    return f"""
    <div class="kpi-card" style="--kpi-color:{color}" role="region" aria-label="{title} KPI Metric Dashboard Card">
        <div class="kpi-head">
            <span>{title}</span>
            <span class="kpi-status">{status}</span>
        </div>
        <div class="kpi-value count-up">{value}</div>
        <div class="kpi-mid">
            <span class="trend-positive">{trend}</span>
            <span>{comparison}</span>
        </div>
        {_sparkline(spark_points, color)}
        <div class="kpi-foot">Last updated {updated}</div>
    </div>
    """


def _widget(title, eyebrow, body_html, footer=""):
    footer_html = f"<div class='widget-footer'>{footer}</div>" if footer else ""
    return f"""
    <section class="ops-widget" aria-label="{title} Stadium Operations Widget">
        <div class="widget-title-row">
            <div>
                <div class="widget-eyebrow">{eyebrow}</div>
                <h3>{title}</h3>
            </div>
            <span class="widget-live">{_status_dot()} Live</span>
        </div>
        {body_html}
        {footer_html}
    </section>
    """


def _render_mission_hero(active_incidents, medical_count, capacity_pct, last_updated, countdown):
    weather_f = round(st.session_state.weather_temp * 9 / 5 + 32)
    html = f"""
    <section class="mission-hero" aria-label="FIFA World Cup Match Telemetry Summary">
        <div class="mission-main">
            <div class="mission-kicker">FIFA WORLD CUP 2026</div>
            <h2>{MATCH_NAME}</h2>
            <div class="mission-venue">{STADIUM_NAME}</div>
            <div class="mission-status">
                <span>{_status_dot()} MATCH STATUS</span>
                <strong>LIVE OPERATIONS</strong>
            </div>
        </div>
        <div class="mission-grid">
            <div>
                <span>Kickoff</span>
                <strong>{countdown}</strong>
            </div>
            <div>
                <span>Attendance</span>
                <strong>{st.session_state.attendance:,} / {CAPACITY:,}</strong>
            </div>
            <div>
                <span>Incidents</span>
                <strong>{active_incidents}</strong>
            </div>
            <div>
                <span>AI Risk Score</span>
                <strong class="risk-low">LOW 12%</strong>
            </div>
            <div>
                <span>Weather</span>
                <strong>{weather_f}F Clear</strong>
            </div>
            <div>
                <span>Capacity</span>
                <strong>{capacity_pct:.1f}%</strong>
            </div>
            <div>
                <span>Telemetry</span>
                <strong>{last_updated} UTC</strong>
            </div>
            <div>
                <span>Match Clock</span>
                <strong>68'</strong>
            </div>
        </div>
    </section>
    """
    st.markdown(clean_html(html), unsafe_allow_html=True)


def _render_live_strip(active_incidents, medical_count):
    security_active = max(3, active_incidents + 1)
    html = f"""
    <div class="live-strip" role="region" aria-label="Real-time Telemetry Service Status Strip">
        <div>{_status_dot()} <strong>Telemetry</strong><span>Active</span></div>
        <div>{_status_dot('#38bdf8')} <strong>Medical</strong><span>{medical_count} Active</span></div>
        <div>{_status_dot('#f59e0b')} <strong>Security</strong><span>{security_active} Active</span></div>
        <div>{_status_dot('#10b981')} <strong>Transport</strong><span>Normal</span></div>
        <div>{_status_dot('#10b981')} <strong>Systems</strong><span>100% Healthy</span></div>
        <div class="live-clock"><strong>Ops Clock</strong><span>{datetime.utcnow().strftime('%H:%M:%S')} UTC</span></div>
    </div>
    """
    st.markdown(clean_html(html), unsafe_allow_html=True)


def _render_kpis(active_incidents, medical_count):
    kpis = [
        _metric_card(
            "Attendance",
            f"{st.session_state.attendance:,}",
            "+2.8%",
            "vs previous hour",
            "12 sec ago",
            "Nominal",
            [40, 43, 44, 51, 57, 62, 68, 74],
            "#10b981",
        ),
        _metric_card(
            "Active Incidents",
            str(active_incidents),
            "-14.0%",
            "containment improving",
            "18 sec ago",
            "Watch",
            [8, 7, 7, 6, 5, 5, 4, active_incidents],
            "#f59e0b",
        ),
        _metric_card(
            "Gate Throughput",
            "18.4k/h",
            "+6.1%",
            "entry flow rate",
            "9 sec ago",
            "Healthy",
            [50, 52, 56, 59, 63, 65, 71, 75],
            "#06b6d4",
        ),
        _metric_card(
            "Medical Queue",
            str(medical_count),
            "Stable",
            "staffing adequate",
            "22 sec ago",
            "Controlled",
            [2, 3, 3, 2, 2, 1, 1, medical_count],
            "#38bdf8",
        ),
    ]
    st.markdown(clean_html(f"<div class='kpi-grid'>{''.join(kpis)}</div>"), unsafe_allow_html=True)


def _render_stadium_map():
    html = """
    <div class="stadium-map">
        <div class="route route-north"></div>
        <div class="route route-south"></div>
        <div class="bowl outer"></div>
        <div class="bowl middle"></div>
        <div class="pitch">FIELD</div>
        <span class="map-node gate gate-a">A</span>
        <span class="map-node gate gate-b alert">B</span>
        <span class="map-node gate gate-c warning">C</span>
        <span class="map-node gate gate-d">D</span>
        <span class="map-node med med-1">M1</span>
        <span class="map-node med med-2">M2</span>
        <span class="map-node security sec-1">S</span>
        <span class="map-node security sec-2">S</span>
        <span class="heat heat-1"></span>
        <span class="heat heat-2"></span>
        <span class="incident incident-1"></span>
        <span class="incident incident-2"></span>
    </div>
    <div class="map-legend">
        <span><i class="legend gate"></i>Gate status</span>
        <span><i class="legend med"></i>Medical</span>
        <span><i class="legend heat"></i>Crowd density</span>
        <span><i class="legend incident"></i>Incident</span>
        <span><i class="legend route"></i>Emergency route</span>
    </div>
    """
    return _widget("Interactive Stadium Map", "Venue Command", html, "Gate C congestion probability: 64% in next 12 minutes")


def _render_widgets(active_incidents, medical_count):
    density_cells = "".join(
        f"<span class='density-cell level-{level}'></span>"
        for level in [1, 2, 2, 3, 4, 3, 1, 2, 4, 5, 5, 4, 2, 3, 4, 5, 4, 3, 1, 2, 3, 3, 2, 1]
    )
    timeline = "".join(
        f"<div class='timeline-row'><strong>{item[0]}</strong><span>{item[1]}</span></div>"
        for item in [
            ("14:31", "Medical team dispatched to Section 124"),
            ("14:29", "Crowd density normalized at North Concourse"),
            ("14:27", "Gate B queue reduced by 18%"),
            ("14:25", "Security patrol completed on Level 2"),
        ]
    )
    medical_rows = "".join(
        f"<div class='queue-row'><span>{item[0]}</span><strong>{item[1]}</strong><em>{item[2]}</em></div>"
        for item in [
            ("MED-07", "Section 124", "2 min ETA"),
            ("MED-02", "Gate C Clinic", "Available"),
            ("MED-11", "Level 2", "Standby"),
        ]
    )
    security_rows = "".join(
        f"<div class='dispatch-row'><span>{item[0]}</span><strong>{item[1]}</strong><em>{item[2]}</em></div>"
        for item in [
            ("Alpha", "Gate C", "On scene"),
            ("Bravo", "North Plaza", "Patrol"),
            ("Delta", "VIP Entry", "Holding"),
        ]
    )
    transport_rows = "".join(
        f"<div class='health-row'><span>{item[0]}</span><strong>{item[1]}</strong><em>{item[2]}</em></div>"
        for item in [
            ("Rail", "Normal", "4 min headway"),
            ("Shuttle", "Normal", "28 buses"),
            ("Rideshare", "Moderate", "Lot E open"),
        ]
    )
    systems_rows = "".join(
        f"<div class='health-row'><span>{item[0]}</span><strong>{item[1]}</strong><em>{item[2]}</em></div>"
        for item in [
            ("Power", "100%", "Redundant feeds active"),
            ("Network", "99.98%", "Edge nodes healthy"),
            ("Access Control", "100%", "Scanner mesh online"),
        ]
    )
    weather_body = """
    <div class="weather-impact">
        <div><span>Temperature</span><strong>72F</strong></div>
        <div><span>Wind</span><strong>NE 8 mph</strong></div>
        <div><span>Impact</span><strong>Low</strong></div>
    </div>
    <p class="widget-note">No weather-driven ingress or evacuation constraints detected.</p>
    """
    prediction_body = """
    <div class="ai-grid-mini">
        <div><span>Crowd Surge</span><strong>Gate C +12 min</strong></div>
        <div><span>Incident Risk</span><strong>Low 12%</strong></div>
        <div><span>Staff Allocation</span><strong>92/100</strong></div>
        <div><span>Queue Forecast</span><strong>-18% Gate B</strong></div>
    </div>
    """
    widgets = [
        _widget("Crowd Density Heatmap", "Predictive Flow", f"<div class='density-grid'>{density_cells}</div>", "Hot zones: Gate C, Pod 4, South upper concourse"),
        _render_stadium_map(),
        _widget("Incident Timeline", "Newest First", f"<div class='timeline'>{timeline}</div>"),
        _widget("Medical Response Queue", "EMS Dispatch", f"<div class='queue-list'>{medical_rows}</div>", f"{medical_count} active medical case under watch"),
        _widget("Security Dispatch Status", "Field Teams", f"<div class='dispatch-list'>{security_rows}</div>", f"{max(3, active_incidents + 1)} active security assignments"),
        _widget("Transportation Status", "Regional Mobility", f"<div class='health-list'>{transport_rows}</div>", "Post-match egress plan remains green"),
        _widget("Weather Impact", "Venue Conditions", weather_body),
        _widget("Power & Network Health", "Critical Systems", f"<div class='health-list'>{systems_rows}</div>", "No degraded services detected"),
        _widget("AI Operational Intelligence", "Hackathon Showcase", prediction_body, "Emergency route optimization: Route North-2 remains fastest"),
    ]
    st.markdown(clean_html(f"<div class='ops-widget-grid'>{''.join(widgets)}</div>"), unsafe_allow_html=True)


def _render_ai_copilot():
    insights = "".join(
        f"<li>{item}</li>"
        for item in [
            "Predicted congestion at Gate C in 12 minutes.",
            "Recommend opening Gate 8 and shifting two volunteers.",
            "Medical staffing adequate for current demand.",
            "Transportation operating normally across rail and shuttle.",
            "No elevated security risks detected.",
        ]
    )
    actions = "".join(
        f"<button>{action}</button>"
        for action in ["Open Gate 8", "Dispatch Volunteers", "Notify Transport Lead"]
    )
    html = f"""
    <section class="ai-copilot" aria-label="AI Operations Copilot Recommendation Command Center">
        <div class="ai-header">
            <div>
                <div class="widget-eyebrow">AI Command Center</div>
                <h3>AI Operations Copilot</h3>
            </div>
            <div class="risk-pill">Risk Score <strong>12%</strong></div>
        </div>
        <div class="ai-content">
            <div>
                <h4>Situation Summary</h4>
                <ul>{insights}</ul>
            </div>
            <div class="recommendation-panel">
                <div><span>Priority</span><strong>Gate C Flow Control</strong></div>
                <div><span>Confidence</span><strong>94%</strong></div>
                <div><span>Resource Utilization</span><strong>88 / 100</strong></div>
                <div><span>Emergency Route</span><strong>North-2 Optimal</strong></div>
            </div>
        </div>
        <div class="suggested-actions">{actions}</div>
    </section>
    """
    st.markdown(clean_html(html), unsafe_allow_html=True)


def _render_activity_feed():
    events = [
        ("14:31", "Medical team dispatched to Section 124"),
        ("14:29", "Crowd density normalized"),
        ("14:27", "Gate B queue reduced"),
        ("14:25", "Security patrol completed"),
        ("14:22", "Network edge node health verified"),
    ]
    rows = "".join(f"<div class='activity-row'><strong>{time_}</strong><span>{text}</span></div>" for time_, text in events)
    st.markdown(
        clean_html(
            f"""
            <section class="activity-feed" aria-label="Live Operations Activity Feed Log">
                <div class="widget-title-row">
                    <div>
                        <div class="widget-eyebrow">Live Stream</div>
                        <h3>Activity Feed</h3>
                    </div>
                    <span class="widget-live">{_status_dot()} Newest First</span>
                </div>
                {rows}
            </section>
            """
        ),
        unsafe_allow_html=True,
    )


def render_dashboard():
    """
    Renders the live tactical operations dashboard showing stadium state.
    """
    initialize_simulation_state()
    run_simulation_tick()

    active_incidents = len([i for i in st.session_state.incidents_db if i["status"] != "Resolved"])
    medical_count = len(
        [
            i
            for i in st.session_state.incidents_db
            if i["type"] == "Medical Assistance Needed" and i["status"] != "Resolved"
        ]
    )
    last_updated = datetime.utcnow().strftime("%H:%M:%S")
    remaining = max(KICKOFF_TIME - datetime.now(timezone.utc), timedelta())
    hours, remainder = divmod(int(remaining.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    countdown = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    capacity_pct = st.session_state.attendance / CAPACITY * 100

    _render_mission_hero(active_incidents, medical_count, capacity_pct, last_updated, countdown)
    _render_live_strip(active_incidents, medical_count)
    _render_kpis(active_incidents, medical_count)

    left, right = st.columns([1.45, 0.95])
    with left:
        _render_ai_copilot()
    with right:
        _render_activity_feed()

    _render_widgets(active_incidents, medical_count)

    with st.expander("Simulation Controller", expanded=False):
        st.caption("Use these controls to generate operational changes for demos and judging walkthroughs.")
        c_btn1, c_btn2 = st.columns(2)
        with c_btn1:
            if st.button("Trigger Random Incident"):
                mock_inc_types = [
                    "Crowd Bottleneck",
                    "Medical Assistance Needed",
                    "Facilities/Spill Issue",
                    "Ticketing/Scanner Failure",
                ]
                mock_locs = ["North Concourse", "East Concourse", "South Concourse", "West Concourse", "Seating Bowl"]
                mock_sevs = [
                    "Low (Routine)",
                    "Medium (Requires Attention)",
                    "High (Immediate Escalation Required)",
                ]
                m_type = random.choice(mock_inc_types)
                m_loc = random.choice(mock_locs)
                m_sev = random.choice(mock_sevs)
                m_id = f"INC-2026-{random.randint(10000, 99999)}"
                m_score = random.randint(20, 95)
                m_label = "High" if m_score > 70 else ("Medium" if m_score > 40 else "Low")
                teams = {
                    "Low (Routine)": "Facilities Team Gamma",
                    "Medium (Requires Attention)": "Crowd Unit Epsilon",
                    "High (Immediate Escalation Required)": "Security Team Alpha",
                }
                etas = {
                    "Low (Routine)": "15 min",
                    "Medium (Requires Attention)": "8 min",
                    "High (Immediate Escalation Required)": "4 min",
                }
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
                    "status": "Queued",
                }
                st.session_state.incidents_db.insert(0, new_m_inc)
                st.session_state.telemetry_feed.insert(0, f"{new_m_inc['timestamp']} - Simulator Alert: {m_id} created.")
                st.toast(f"Simulator logged new incident: {m_id}")
                st.rerun()
        with c_btn2:
            if st.button("Simulate Telemetry Update"):
                st.session_state.attendance += random.randint(-50, 60)
                st.session_state.weather_temp = max(
                    18, min(32, st.session_state.weather_temp + random.choice([-1, 0, 1]))
                )
                st.session_state.telemetry_feed.insert(
                    0,
                    f"{time.strftime('%I:%M %p')} - Telemetry checked. Attendance: {st.session_state.attendance}",
                )
                st.toast("Telemetry data recalculated.")
                st.rerun()
