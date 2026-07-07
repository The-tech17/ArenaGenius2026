import streamlit as st
import random
import time

# Mock datasets that use st.cache_data for performance optimization

@st.cache_data
def get_stadium_details():
    """
    Returns static configuration data for the three supported World Cup stadiums.
    """
    return {
        "MetLife Stadium (New York/New Jersey)": {
            "capacity": 82500,
            "gates": ["Gate A (North)", "Gate B (East)", "Gate C (South)", "Gate D (West)", "VIP Entrance"],
            "medical_stations": ["Med Station 1 (Level 1)", "Med Station 2 (Level 2)", "Main Clinic (Gate C)"],
            "transit": ["Meadowlands Rail Station", "Bus Shuttle Hub A", "Rideshare Lot E"],
            "exits": ["North Exit 1 & 2", "East Exit 3", "South Exit 4 & 5", "West Exit 6"],
            "volunteer_hubs": ["Hub Blue (Gate B)", "Hub Green (Gate D)"]
        },
        "SoFi Stadium (Los Angeles)": {
            "capacity": 70240,
            "gates": ["Entry 1 (North)", "Entry 5 (South)", "Entry 8 (East)", "Entry 10 (West)", "VIP Club Entry"],
            "medical_stations": ["First Aid Suite 102", "First Aid Suite 240", "First Aid Clinic Gate 5A"],
            "transit": ["Metro Shuttle Line", "Rideshare Zone N", "South Parking Shuttle Hub"],
            "exits": ["North Egress Plaza", "Lake Plaza Exit", "South Canyon Exit", "East Gate Egress"],
            "volunteer_hubs": ["Hub Gold (Entry 1)", "Hub Purple (Entry 8)"]
        },
        "Azteca Stadium (Mexico City)": {
            "capacity": 87523,
            "gates": ["Torniquetes Norte", "Torniquetes Sur", "Acceso Especial", "Acceso Insurgentes"],
            "medical_stations": ["Servicio Médico Zona A", "Servicio Médico Zona B", "Clínica de Emergencias Tlalpan"],
            "transit": ["Tren Ligero Estadio Azteca", "Paradero Calzada de Tlalpan", "Taxi Seguro VIP"],
            "exits": ["Salida Principal Norte", "Salida Oriente", "Salida Sur Insurgentes"],
            "volunteer_hubs": ["Zona Voluntarios 1 (Norte)", "Zona Voluntarios 2 (Sur)"]
        }
    }

@st.cache_data
def get_cached_faqs():
    """
    Provides typical multilingual FAQs for international fans.
    """
    return [
        {
            "category": "🏟️ General",
            "q_en": "Can I bring my bag into the stadium?",
            "a_en": "Only clear bags smaller than 12x6x12 inches are allowed. One-gallon clear plastic freezer bags are permitted.",
            "a_es": "Solo se permiten bolsas transparentes de menos de 12x6x12 pulgadas. Se permite una bolsa de plástico transparente para congelar de un galón.",
            "a_fr": "Seuls les sacs transparents de moins de 12x6x12 pouces sont autorisés. Un sac de congélation en plastique transparent d'un gallon est permis."
        },
        {
            "category": "🚇 Transit",
            "q_en": "How do I get back to the metro post-match?",
            "a_en": "Follow the green directional signs for your stadium's metro terminal. Flow controllers are stationed at all exits.",
            "a_es": "Siga las señales direccionales verdes hacia la terminal de metro de su estadio. Hay controladores de flujo en todas las salidas.",
            "a_fr": "Suivez les panneaux directionnels verts pour le terminal de métro de votre stade. Des contrôleurs de flux sont postés à toutes les sorties."
        },
        {
            "category": "🚑 Health & Safety",
            "q_en": "Where do I go if I need medical help?",
            "a_en": "Contact any volunteer wearing an orange armband or head to the nearest Medical Station displayed on the stadium map.",
            "a_es": "Comuníquese con cualquier voluntario con brazalete naranja o diríjase a la estación médica más cercana que se muestra en el mapa del estadio.",
            "a_fr": "Contactez tout bénévole portant un brassard orange ou rendez-vous à la station médicale la plus proche indiquée sur le plan du stade."
        }
    ]

def initialize_simulation_state():
    """
    Ensures all simulation session state variables are initialized properly.
    """
    if "sim_initialized" not in st.session_state:
        st.session_state.sim_initialized = True
        st.session_state.attendance = 74215
        st.session_state.active_incidents_count = 3
        st.session_state.active_medical_count = 2
        st.session_state.weather_temp = 22
        st.session_state.weather_cond = "Clear"
        st.session_state.metro_delay = "None"
        st.session_state.gates_status = "12/14 Open"
        st.session_state.security_level = "Elevated 🚓"
        st.session_state.selected_location = "Concourse Level 2"
        
        # Incident Database
        st.session_state.incidents_db = [
            {
                "id": "INC-2026-04231",
                "type": "Crowd Bottleneck",
                "location": "Concourse Level 2, Gate C",
                "severity": "High (Immediate Escalation Required)",
                "details": "Massive crowding forming outside the restrooms blocking exit flow.",
                "risk_score": 82,
                "risk_label": "High 🔴",
                "assigned": "Security Team Alpha",
                "eta": "5 min",
                "timestamp": "08:42 AM",
                "status": "In Progress"
            },
            {
                "id": "INC-2026-04232",
                "type": "Medical Assistance Needed",
                "location": "Section 104, Row K",
                "severity": "Medium (Requires Attention)",
                "details": "Elderly spectator feeling dehydrated and light-headed.",
                "risk_score": 58,
                "risk_label": "Medium 🟡",
                "assigned": "Medical Team Bravo",
                "eta": "7 min",
                "timestamp": "08:45 AM",
                "status": "Dispatched"
            },
            {
                "id": "INC-2026-04233",
                "type": "Facilities/Spill Issue",
                "location": "Pod 4 Food Court",
                "severity": "Low (Routine)",
                "details": "Soda spill on steps creating slip hazard. Cleaning crew needed.",
                "risk_score": 25,
                "risk_label": "Low 🟢",
                "assigned": "Facilities Team Gamma",
                "eta": "12 min",
                "timestamp": "08:50 AM",
                "status": "Queued"
            }
        ]
        
        # System Log Feed
        st.session_state.telemetry_feed = [
            "08:50 AM - Cleaning crew dispatched to Pod 4 Food Court spill",
            "08:45 AM - Medical Team Bravo assigned to Section 104 hydration case",
            "08:42 AM - Crowd control volunteers redirected to Gate C exit corridor",
            "08:30 AM - Metro delay alert cleared. Metro line running normally"
        ]

def run_simulation_tick():
    """
    Simulates minor real-time variations in stadium telemetry data.
    """
    initialize_simulation_state()
    
    # 35% chance to update attendance and metrics
    if random.random() < 0.35:
        # Subtle attendance shifts
        st.session_state.attendance += random.randint(-15, 20)
        st.session_state.attendance = max(70000, min(80000, st.session_state.attendance))
        
        # Subtle temperature shifts
        if random.random() < 0.1:
            st.session_state.weather_temp += random.choice([-1, 1])
            st.session_state.weather_temp = max(18, min(30, st.session_state.weather_temp))
            
        # Randomly toggle metro status
        if random.random() < 0.05:
            st.session_state.metro_delay = random.choice(["None", "10m Delay (Line A)", "5m Delay (Line B)"])
            if st.session_state.metro_delay != "None":
                st.session_state.telemetry_feed.insert(0, f"{time.strftime('%I:%M %p')} - Operations Alert: {st.session_state.metro_delay} reported.")
            else:
                st.session_state.telemetry_feed.insert(0, f"{time.strftime('%I:%M %p')} - System Status: Metro lines returning to normal service.")
                
        # Truncate telemetry log
        st.session_state.telemetry_feed = st.session_state.telemetry_feed[:8]
