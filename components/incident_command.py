import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import random
import time
from utils.data_simulator import get_stadium_details, initialize_simulation_state
from utils.theme import clean_html
from utils.security import is_valid_api_key, sanitize_html

def calculate_priority_score(crowd_size_val, severity_val, location_val, time_val):
    """
    Calculates a live incident risk score from 0 to 100 based on weighted attributes.
    Crowd Size: 45%, Severity: 30%, Location: 15%, Time: 10%
    """
    # Crowd Size weights
    crowd_weights = {"Small (< 50 fans)": 15, "Medium (50-200 fans)": 45, "Large (200-1000 fans)": 75, "Massive (> 1000 fans)": 100}
    crowd_score = crowd_weights.get(crowd_size_val, 15)
    
    # Severity weights
    severity_weights = {"Low (Routine)": 15, "Medium (Requires Attention)": 55, "High (Immediate Escalation Required)": 100}
    severity_score = severity_weights.get(severity_val, 15)
    
    # Location weights
    loc_weights = {
        "North Concourse": 60, "East Concourse": 65, "South Concourse": 70, "West Concourse": 60,
        "Seating Bowl": 90, "Gates / Entry Plaza": 95, "Parking Lot / Shuttle Hub": 40
    }
    loc_score = loc_weights.get(location_val, 50)
    
    # Time of match weights
    time_weights = {"Pre-Match (Arrivals)": 50, "Mid-Match (In-Play)": 30, "Halftime (Concourse Surge)": 80, "Post-Match (Egress)": 100}
    time_score = time_weights.get(time_val, 50)
    
    overall_score = int(0.45 * crowd_score + 0.3 * severity_score + 0.15 * loc_score + 0.1 * time_score)
    
    if overall_score < 40:
        return overall_score, "Low 🟢", "badge-success"
    elif overall_score < 75:
        return overall_score, "Medium 🟡", "badge-warning"
    else:
        return overall_score, "High 🔴", "badge-danger"

def render_interactive_map(selected_loc):
    """
    Generates a premium interactive SVG stadium map inside an HTML iframe.
    Hovering changes colors, clicking redirects parent URL search parameters to sync selection.
    """
    # Sanitize inputs
    selected_loc_s = sanitize_html(selected_loc)
    # Determine the theme preference
    theme_pref = st.session_state.get("theme_pref", "System Default")
    
    # Define CSS variables based on theme preference for iframe styling
    if theme_pref == "Dark Mode":
        css_variables = """
        :root {
            --rim-fill: #0b1329;
            --rim-stroke: #1d2554;
            --concourse-fill: #1e293b;
            --bowl-fill: #0f172a;
            --pitch-fill: #065f46;
            --text-color: #94a3b8;
            --selected-text-color: #ffffff;
            --highlight-fill: #10b981;
        }
        """
    elif theme_pref == "Light Mode":
        css_variables = """
        :root {
            --rim-fill: #cbd5e1;
            --rim-stroke: #94a3b8;
            --concourse-fill: #f1f5f9;
            --bowl-fill: #e2e8f0;
            --pitch-fill: #10b981;
            --text-color: #475569;
            --selected-text-color: #0f172a;
            --highlight-fill: #0f52ba;
        }
        """
    else:  # System Default
        css_variables = """
        :root {
            --rim-fill: #0b1329;
            --rim-stroke: #1d2554;
            --concourse-fill: #1e293b;
            --bowl-fill: #0f172a;
            --pitch-fill: #065f46;
            --text-color: #94a3b8;
            --selected-text-color: #ffffff;
            --highlight-fill: #10b981;
        }
        @media (prefers-color-scheme: light) {
            :root {
                --rim-fill: #cbd5e1;
                --rim-stroke: #94a3b8;
                --concourse-fill: #f1f5f9;
                --bowl-fill: #e2e8f0;
                --pitch-fill: #10b981;
                --text-color: #475569;
                --selected-text-color: #0f172a;
                --highlight-fill: #0a0f24;
            }
        }
        """

    # Define fill colors for the SVG sectors using variables
    colors = {
        "North Concourse": "var(--concourse-fill)",
        "East Concourse": "var(--concourse-fill)",
        "South Concourse": "var(--concourse-fill)",
        "West Concourse": "var(--concourse-fill)",
        "Seating Bowl": "var(--bowl-fill)"
    }
    
    # Highlight the selected location if matching one of the sectors
    if selected_loc in colors:
        colors[selected_loc] = "var(--highlight-fill)"
        
    svg_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            {css_variables}
            body {{
                margin: 0;
                padding: 0;
                background-color: transparent;
                display: flex;
                justify-content: center;
                align-items: center;
                overflow: hidden;
            }}
            .clickable {{
                cursor: pointer;
                transition: fill 0.3s, opacity 0.3s;
            }}
            .clickable:hover {{
                fill: #fbbf24 !important; /* Gold on hover */
                opacity: 0.9;
            }}
            .field {{
                stroke: #ffffff;
                stroke-width: 2px;
            }}
            .label {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 10px;
                font-weight: bold;
                fill: var(--text-color);
                pointer-events: none;
                text-anchor: middle;
            }}
            .selected-label {{
                fill: var(--selected-text-color);
                font-size: 11px;
                text-shadow: 0 1px 3px rgba(0,0,0,0.8);
            }}
            .marker-text {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 9px;
                font-weight: bold;
                fill: white;
                text-anchor: middle;
                pointer-events: none;
            }}
        </style>
    </head>
    <body>
        <svg viewBox="0 0 500 350" width="100%" height="100%" style="border-radius: 12px; max-width: 500px;" role="img" aria-label="FIFA World Cup Stadium Layout Map">
            <!-- Outer Stadium Rim -->
            <ellipse cx="250" cy="175" rx="230" ry="155" fill="var(--rim-fill)" stroke="var(--rim-stroke)" stroke-width="4" />
            
            <!-- Concourse Quadrants -->
            <!-- North Concourse -->
            <path id="North Concourse" class="clickable" d="M 90 90 A 230 155 0 0 1 410 90 L 360 120 A 150 100 0 0 0 140 120 Z" 
                  fill="{colors['North Concourse']}" stroke="var(--rim-stroke)" stroke-width="2" onclick="selectSection('North Concourse')" />
                  
            <!-- East Concourse -->
            <path id="East Concourse" class="clickable" d="M 410 90 A 230 155 0 0 1 410 260 L 360 230 A 150 100 0 0 0 360 120 Z" 
                  fill="{colors['East Concourse']}" stroke="var(--rim-stroke)" stroke-width="2" onclick="selectSection('East Concourse')" />
                  
            <!-- South Concourse -->
            <path id="South Concourse" class="clickable" d="M 410 260 A 230 155 0 0 1 90 260 L 140 230 A 150 100 0 0 0 360 230 Z" 
                  fill="{colors['South Concourse']}" stroke="var(--rim-stroke)" stroke-width="2" onclick="selectSection('South Concourse')" />
                  
            <!-- West Concourse -->
            <path id="West Concourse" class="clickable" d="M 90 260 A 230 155 0 0 1 90 90 L 140 120 A 150 100 0 0 0 140 230 Z" 
                  fill="{colors['West Concourse']}" stroke="var(--rim-stroke)" stroke-width="2" onclick="selectSection('West Concourse')" />
            
            <!-- Seating Bowl -->
            <ellipse id="Seating Bowl" class="clickable" cx="250" cy="175" rx="120" ry="75" 
                     fill="{colors['Seating Bowl']}" stroke="#fbbf24" stroke-width="3" onclick="selectSection('Seating Bowl')" />
            
            <!-- Central Pitch -->
            <rect x="200" y="145" width="100" height="60" rx="3" fill="var(--pitch-fill)" class="field" />
            <circle cx="250" cy="175" r="15" fill="none" stroke="#ffffff" stroke-width="1.5" />
            <line x1="250" y1="145" x2="250" y2="205" stroke="#ffffff" stroke-width="1.5" />
            
            <!-- Labels -->
            <text x="250" y="70" class="label {'selected-label' if selected_loc_s == 'North Concourse' else ''}">NORTH CONCOURSE</text>
            <text x="250" y="295" class="label {'selected-label' if selected_loc_s == 'South Concourse' else ''}">SOUTH CONCOURSE</text>
            <text x="430" y="180" class="label {'selected-label' if selected_loc_s == 'East Concourse' else ''}" transform="rotate(90 430 180)">EAST CONCOURSE</text>
            <text x="70" y="180" class="label {'selected-label' if selected_loc_s == 'West Concourse' else ''}" transform="rotate(-90 70 180)">WEST CONCOURSE</text>
            <text x="250" y="178" fill="#ffffff" font-size="9px" style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-weight: bold; text-anchor: middle; opacity: 0.6;">PITCH</text>
            
            <!-- Dynamic Exit Gates Indicators -->
            <circle cx="250" cy="20" r="8" fill="#f43f5e" /> <text x="250" y="23" class="marker-text">A</text>
            <circle cx="480" cy="175" r="8" fill="#f43f5e" /> <text x="480" y="178" class="marker-text">B</text>
            <circle cx="250" cy="330" r="8" fill="#f43f5e" /> <text x="250" y="333" class="marker-text">C</text>
            <circle cx="20" cy="175" r="8" fill="#f43f5e" /> <text x="20" y="178" class="marker-text">D</text>
            
            <!-- Medical Alerts Indicators -->
            <circle cx="360" cy="160" r="7" fill="#0ea5e9" /> <text x="360" y="163" class="marker-text">+</text>
            <circle cx="140" cy="190" r="7" fill="#0ea5e9" /> <text x="140" y="193" class="marker-text">+</text>
        </svg>

        <script>
            function selectSection(name) {{
                // Attempt to update streamlit query params via window parent redirect
                try {{
                    const parentUrl = new URL(window.parent.location.href);
                    parentUrl.searchParams.set('selected_loc', name);
                    window.parent.location.href = parentUrl.toString();
                }} catch (e) {{
                    console.error("Query parameter navigation blocked or not supported: ", e);
                }}
            }}
        </script>
    </body>
    </html>
    """
    components.html(svg_html, height=360)

def render_incident_hub(api_key):
    """
    Main incident command page. Handles smarter forms, calculations, maps, and AI feedback.
    """
    st.markdown("## 🚨 Operational Incident Command Hub")
    st.markdown("Log venue issues, check risk prioritization, and dispatch AI-generated response protocol checklists.")
    
    # Process potential clicked section from query parameters
    query_params = st.query_params
    if "selected_loc" in query_params:
        clicked_loc = query_params["selected_loc"]
        if clicked_loc in ["North Concourse", "East Concourse", "South Concourse", "West Concourse", "Seating Bowl"]:
            st.session_state.selected_location = clicked_loc
            
    col_map, col_form = st.columns([1.1, 1.3])
    
    stadiums = get_stadium_details()
    
    with col_map:
        st.markdown("### 🏟️ Interactive Stadium Map")
        st.caption("Click on any stadium concourse or bowl segment below to instantly select the location field.")
        
        render_interactive_map(st.session_state.selected_location)
        
        # Interactive information card depending on selected sector
        loc = st.session_state.selected_location
        st.markdown(f"#### 🔍 Segment Insights: **{loc}**")
        
        # Mock nearest locations depending on selected region
        exits = {
            "North Concourse": "Gate A (North) • Exit 1 & 2",
            "East Concourse": "Gate B (East) • Exit 3",
            "South Concourse": "Gate C (South) • Exit 4 & 5",
            "West Concourse": "Gate D (West) • Exit 6",
            "Seating Bowl": "Upper Portal 12 • Lower Tunnel A"
        }
        meds = {
            "North Concourse": "Med Station 1 (Level 1) - 45m away",
            "East Concourse": "Main Clinic (Gate C) - 80m away",
            "South Concourse": "Main Clinic (Gate C) - 30m away",
            "West Concourse": "Med Station 2 (Level 2) - 60m away",
            "Seating Bowl": "First Aid Suite 102 - Adjacent Corridor"
        }
        volunteers = {
            "North Concourse": "4 Volunteers (Sectors 108-112)",
            "East Concourse": "8 Volunteers (Gate B Area)",
            "South Concourse": "12 Volunteers (Main Gate C Entry)",
            "West Concourse": "6 Volunteers (Hub Green Zone)",
            "Seating Bowl": "15 Volunteers (Upper Seating Bowls)"
        }
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"🚪 **Nearest Exits:**\n\n{exits.get(loc, 'Gate A')}")
            st.markdown(f"👥 **Responders Nearby:**\n\n{volunteers.get(loc, '4 Volunteers')}")
        with c2:
            st.markdown(f"🚑 **Medical Post:**\n\n{meds.get(loc, 'Med Station 1')}")
            st.markdown(f"📶 **Segment Load:**\n\n`Optimal (34%)`")

    with col_form:
        st.markdown("### ⚠️ Log Live Incident")
        
        with st.form("incident_report_form"):
            selected_stadium = st.selectbox("Active Stadium", list(stadiums.keys()))
            
            # Category selection
            incident_type = st.selectbox("Incident Category", [
                "Crowd Bottleneck", 
                "Medical Assistance Needed", 
                "Facilities/Spill Issue", 
                "Ticketing/Scanner Failure"
            ])
            
            # Sync text input with the map clicking parameter or drop-down fallback
            locations_list = ["North Concourse", "East Concourse", "South Concourse", "West Concourse", "Seating Bowl", "Gates / Entry Plaza", "Parking Lot / Shuttle Hub"]
            try:
                def_index = locations_list.index(st.session_state.selected_location)
            except ValueError:
                def_index = 0
                
            location_val = st.selectbox("Incident Sector", locations_list, index=def_index)
            
            # Sync selections back to session state
            st.session_state.selected_location = location_val
            
            # Smarter Conditional Form Inputs
            cond_data = {}
            if incident_type == "Medical Assistance Needed":
                st.markdown("<div style='border-left: 3px solid #0ea5e9; padding-left: 10px; margin-bottom:15px;'>", unsafe_allow_html=True)
                c_injured = st.number_input("Number of Injured / Distressed Spectators", min_value=1, value=1, step=1)
                c_conscious = st.radio("Are they conscious?", ["Yes", "No", "Unconfirmed"], horizontal=True)
                c_ambulance = st.radio("Is ambulance transportation required?", ["No", "Yes", "To be assessed"], horizontal=True)
                cond_data = {"injured_count": c_injured, "conscious": c_conscious, "ambulance_needed": c_ambulance}
                st.markdown("</div>", unsafe_allow_html=True)
                
            elif incident_type == "Crowd Bottleneck":
                st.markdown("<div style='border-left: 3px solid #f43f5e; padding-left: 10px; margin-bottom:15px;'>", unsafe_allow_html=True)
                c_size_est = st.selectbox("Estimated crowd density in blocked corridor", ["Under 50 fans", "50-200 fans", "200-500 fans", "Over 500 fans"])
                c_blocked = st.radio("Are emergency exit paths physically blocked?", ["No", "Yes - Partially", "Yes - Fully"], horizontal=True)
                c_police = st.radio("Are tactical security reinforcements required?", ["No", "Yes (Escalate to Command Center)"], horizontal=True)
                cond_data = {"est_density": c_size_est, "exits_blocked": c_blocked, "police_required": c_police}
                st.markdown("</div>", unsafe_allow_html=True)
                
            elif incident_type == "Facilities/Spill Issue":
                st.markdown("<div style='border-left: 3px solid #fbbf24; padding-left: 10px; margin-bottom:15px;'>", unsafe_allow_html=True)
                c_spill_type = st.selectbox("Issue Type", ["Liquid Spill (Slip Hazard)", "Structural Damage / Broken Seat", "Restroom Flooding", "Electrical / Lighting Outage"])
                c_hazards = st.radio("Are active electrical or chemical hazards present?", ["No", "Yes", "Unsure"], horizontal=True)
                c_sign = st.radio("Has 'Caution: Wet Floor' sign been deployed?", ["No", "Yes", "N/A"], horizontal=True)
                cond_data = {"spill_category": c_spill_type, "hazardous": c_hazards, "caution_sign_placed": c_sign}
                st.markdown("</div>", unsafe_allow_html=True)
                
            elif incident_type == "Ticketing/Scanner Failure":
                st.markdown("<div style='border-left: 3px solid #94a3b8; padding-left: 10px; margin-bottom:15px;'>", unsafe_allow_html=True)
                c_gate_details = st.selectbox("Gate affected", stadiums[selected_stadium]["gates"])
                c_scanner_id = st.text_input("Scanner Device Serial / ID", placeholder="e.g. SCN-514B")
                c_duration = st.selectbox("Offline Duration", ["Just failed", "< 5 minutes", "5 - 15 minutes", "Over 15 minutes"])
                cond_data = {"gate": c_gate_details, "device_id": c_scanner_id, "downtime": c_duration}
                st.markdown("</div>", unsafe_allow_html=True)
                
            # Rest of the form parameters
            crowd_size = st.selectbox("Overall Area Crowd Size Status", ["Small (< 50 fans)", "Medium (50-200 fans)", "Large (200-1000 fans)", "Massive (> 1000 fans)"])
            severity = st.radio("Severity Level", ["Low (Routine)", "Medium (Requires Attention)", "High (Immediate Escalation Required)"], horizontal=True)
            time_phase = st.selectbox("Match Time Window", ["Pre-Match (Arrivals)", "Mid-Match (In-Play)", "Halftime (Concourse Surge)", "Post-Match (Egress)"])
            details = st.text_area("Describe the situation details (e.g. age, symptoms, blockage factors):", placeholder="Enter specific observations...")
            
            # Dynamic Decision-Support Priority Calculation (shown in form)
            p_score, p_label, p_badge = calculate_priority_score(crowd_size, severity, location_val, time_phase)
            
            st.markdown(
                clean_html(f"""
                <div style="background-color: var(--card-bg); padding: 0.75rem 1rem; border-radius: 8px; margin: 15px 0; border: 1px solid var(--card-border);">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-weight:600; font-size:0.95rem; color: var(--text) !important;">📊 Calculated Risk Score:</span>
                        <div>
                            <span class="badge {p_badge}" style="font-size:0.85rem;">{p_label} ({p_score}%)</span>
                        </div>
                    </div>
                </div>
                """),
                unsafe_allow_html=True
            )
            
            submit_incident = st.form_submit_button("Generate AI Dispatch & SOP Checklist")

        # Process Submission
        if submit_incident:
            if not is_valid_api_key(api_key):
                st.warning("Please configure a valid Gemini API Key in Settings to generate AI responses.")
            else:
                incident_id = f"INC-2026-{random.randint(10000, 99999)}"
                
                # Mock assigned details
                assignments = {
                    "Low (Routine)": ("Facilities Team Gamma", "12 min"),
                    "Medium (Requires Attention)": ("Medical Team Bravo" if incident_type == "Medical Assistance Needed" else "Crowd Unit Epsilon", "7 min"),
                    "High (Immediate Escalation Required)": ("Security Team Alpha" if incident_type == "Crowd Bottleneck" else "Tactical Response Unit Delta", "4 min")
                }
                assigned_team, response_eta = assignments.get(severity, ("Operations Team", "8 min"))
                
                # Progress Indicator Simulation
                status_block = st.status("Analyzing Live Incident Telemetry...")
                with status_block:
                    st.write("Initializing risk verification matrix...")
                    time.sleep(0.7)
                    st.progress(25)
                    
                    st.write("Verifying nearest active responders...")
                    time.sleep(0.6)
                    st.progress(60)
                    
                    st.write("Retrieving FIFA World Cup 2026 Standard Operating Procedures (SOPs)...")
                    time.sleep(0.5)
                    st.progress(85)
                    
                    st.write("Generating optimal crowd dispersal routes and volunteer tasks...")
                    time.sleep(0.5)
                    st.progress(100)
                    status_block.update(label="SOP Checklist Formulated!", state="complete")
                
                # Generate actual protocol using Gemini
                prompt = f"""
                Context: A FIFA World Cup 2026 stadium incident has been reported.
                Incident ID: {incident_id}
                Stadium: {selected_stadium}
                Location Segment: {location_val}
                Incident Type: {incident_type}
                Severity: {severity}
                Priority Risk Score: {p_score}% ({p_label})
                Time Phase: {time_phase}
                Details: {details}
                Additional Inputs: {cond_data}
                
                Task: Generate a step-by-step checklist of immediate physical actions the reporting volunteer/staff member should take. Include specific dispatch actions for '{assigned_team}'. Outline a public service announcement (PSA) suggestion if a crowd redirect is necessary. Keep it direct, tactical, and clean.
                """
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(prompt)
                
                # Render beautifully formatted operations ticket
                # Escape user and model inputs for safety
                incident_id_s = sanitize_html(incident_id)
                assigned_team_s = sanitize_html(assigned_team)
                response_eta_s = sanitize_html(response_eta)
                incident_type_s = sanitize_html(incident_type)
                location_val_s = sanitize_html(location_val)
                selected_stadium_s = sanitize_html(selected_stadium)
                p_badge_s = sanitize_html(p_badge)
                p_label_s = sanitize_html(p_label)
                p_score_s = sanitize_html(p_score)

                st.markdown(
                    f"""
                    <div class="ticket-container" role="region" aria-label="Incident Dispatch Operations Ticket Log">
                        <div class="ticket-header">
                            <div>
                                <div style="font-size:0.8rem; color:var(--muted); text-transform:uppercase;">Operations Center Log</div>
                                <div class="ticket-id">✓ {incident_id_s}</div>
                            </div>
                            <span class="badge {p_badge_s}" style="font-size:0.9rem; padding:0.4rem 1rem;">{p_label_s} ({p_score_s}%)</span>
                        </div>
                        <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom:1.5rem;">
                            <div class="ticket-field">
                                <div class="ticket-label">Assigned Tactical Team</div>
                                <div class="ticket-value" style="color:#fbbf24;">{assigned_team_s}</div>
                            </div>
                            <div class="ticket-field">
                                <div class="ticket-label">Target Response ETA</div>
                                <div class="ticket-value">{response_eta_s}</div>
                            </div>
                            <div class="ticket-field">
                                <div class="ticket-label">Category</div>
                                <div class="ticket-value">{incident_type_s}</div>
                            </div>
                            <div class="ticket-field">
                                <div class="ticket-label">Reported Location</div>
                                <div class="ticket-value">{location_val_s} ({selected_stadium_s})</div>
                            </div>
                        </div>
                        <div style="border-top: 1px dashed rgba(255,255,255,0.15); padding-top:1rem;">
                            <div class="ticket-label" style="margin-bottom:0.5rem;">Immediate Action Checklist (AI Recommendations)</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                st.write(response.text)
                
                # Add to simulated live database
                new_incident = {
                    "id": incident_id,
                    "type": incident_type,
                    "location": f"{location_val}, {selected_stadium}",
                    "severity": severity,
                    "details": details,
                    "risk_score": p_score,
                    "risk_label": p_label,
                    "assigned": assigned_team,
                    "eta": response_eta,
                    "timestamp": time.strftime("%I:%M %p"),
                    "status": "Dispatched"
                }
                st.session_state.incidents_db.insert(0, new_incident)
                
                # Add log
                st.session_state.telemetry_feed.insert(0, f"{new_incident['timestamp']} - New Incident: {incident_id} ({incident_type}) reported in {location_val}.")
                st.toast(f"Incident {incident_id} successfully logged and dispatched!", icon="🚨")
