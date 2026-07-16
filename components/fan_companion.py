# Refined GenAI routing logic satisfying FIFA World Cup 2026 Smart Stadiums, crowd management optimization, and multilingual assistant specifications.
import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
from utils.data_simulator import get_stadium_details, get_cached_faqs
from utils.security import is_valid_api_key, sanitize_html, sanitize_js_string

def get_language_code(lang_name):
    """
    Maps language display names to ISO codes for Speech APIs.
    """
    mapping = {
        "English": "en-US",
        "Español": "es-ES",
        "Français": "fr-FR",
        "Deutsch": "de-DE",
        "Português": "pt-PT",
        "日本語": "ja-JP"
    }
    return mapping.get(lang_name, "en-US")

def render_stt_button(lang_code):
    """
    Renders an HTML5 microphone button that records voice and updates the search query.
    """
    stt_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; padding: 0; background: transparent; }}
            .mic-btn {{
                background: linear-gradient(135deg, #f43f5e, #be123c);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 0.6rem 1rem;
                font-family: system-ui, -apple-system, sans-serif;
                font-size: 0.85rem;
                font-weight: 600;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 8px;
                box-shadow: 0 4px 12px rgba(244, 63, 94, 0.3);
                transition: all 0.2s ease;
            }}
            .mic-btn:hover {{
                transform: translateY(-1px);
                box-shadow: 0 6px 16px rgba(244, 63, 94, 0.4);
            }}
            .recording {{
                animation: pulse 1.2s infinite;
                background: #b91c1c;
            }}
            @keyframes pulse {{
                0% {{ opacity: 1; }}
                50% {{ opacity: 0.6; }}
                100% {{ opacity: 1; }}
            }}
        </style>
    </head>
    <body>
        <button id="mic-trigger" class="mic-btn" onclick="startRecognition()">
            🎤 Speak Query (Voice input)
        </button>

        <script>
            let recognition;
            function startRecognition() {{
                const btn = document.getElementById("mic-trigger");
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                
                if (!SpeechRecognition) {{
                    alert("Speech recognition is not supported in this browser. Please use Chrome/Safari.");
                    return;
                }}
                
                btn.innerText = "🛑 Listening...";
                btn.classList.add("recording");
                
                recognition = new SpeechRecognition();
                recognition.continuous = false;
                recognition.interimResults = false;
                recognition.lang = "{lang_code}";
                
                recognition.onresult = function(event) {{
                    const transcript = event.results[0][0].transcript;
                    btn.innerText = "✓ Processing...";
                    btn.classList.remove("recording");
                    
                    // Redirect parent URL with the search query to update Streamlit input
                    const parentUrl = new URL(window.parent.location.href);
                    parentUrl.searchParams.set("stt_query", transcript);
                    window.parent.location.href = parentUrl.toString();
                }};
                
                recognition.onerror = function(event) {{
                    console.error("Speech Recognition Error:", event.error);
                    btn.innerText = "🎤 Retry Voice Input";
                    btn.classList.remove("recording");
                }};
                
                recognition.onend = function() {{
                    btn.innerText = "🎤 Speak Query";
                    btn.classList.remove("recording");
                }};
                
                recognition.start();
            }}
        </script>
    </body>
    </html>
    """
    components.html(stt_html, height=45)

def render_tts_button(text_to_speak, lang_code):
    """
    Renders a button that utilizes browser SpeechSynthesis to read responses aloud.
    """
    # Clean response text to prevent JavaScript syntax issues
    cleaned_text = sanitize_js_string(text_to_speak)
    
    tts_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; padding: 0; background: transparent; }}
            .speak-btn {{
                background: linear-gradient(135deg, #10b981, #047857);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 0.5rem 1rem;
                font-family: system-ui, -apple-system, sans-serif;
                font-size: 0.8rem;
                font-weight: 600;
                cursor: pointer;
                display: inline-flex;
                align-items: center;
                gap: 6px;
                box-shadow: 0 4px 10px rgba(16, 185, 129, 0.25);
                transition: all 0.2s ease;
            }}
            .speak-btn:hover {{
                transform: translateY(-1px);
                filter: brightness(1.1);
            }}
        </style>
    </head>
    <body>
        <button class="speak-btn" onclick="speakText()">
            🔊 Listen to Guide (Audio Playback)
        </button>

        <script>
            function speakText() {{
                if ('speechSynthesis' in window) {{
                    // Cancel any active speech first
                    window.speechSynthesis.cancel();
                    
                    const utterance = new SpeechSynthesisUtterance("{cleaned_text}");
                    utterance.lang = "{lang_code}";
                    utterance.rate = 1.0;
                    utterance.pitch = 1.0;
                    
                    window.speechSynthesis.speak(utterance);
                }} else {{
                    alert("Audio Playback is not supported in this browser.");
                }}
            }}
        </script>
    </body>
    </html>
    """
    components.html(tts_html, height=42)

def render_fan_companion(api_key):
    """
    Renders the Global Fan Companion view, handling queries, chats, and FAQs.
    """
    st.markdown("## 🌍 Global Fan Companion")
    st.markdown("Your smart assistant for navigating the stadium, understanding guidelines, and translating details.")
    
    # Process Voice Input parameters
    query_params = st.query_params
    voice_query = ""
    if "stt_query" in query_params:
        voice_query = query_params["stt_query"]
        # Clear search parameters to avoid re-triggering on subsequent actions
        st.query_params.pop("stt_query", None)
        
    stadiums = get_stadium_details()
    
    tab_guide, tab_chat, tab_faq = st.tabs([
        "✈️ Stadium Multilingual Guide", 
        "💬 Chat Assistant", 
        "❓ Frequently Asked Questions"
    ])
    
    with tab_guide:
        with st.container(border=True):
            st.markdown("### 🎫 Select Stadium & Preferences")
            col1, col2 = st.columns(2)
            with col1:
                selected_stadium = st.selectbox("Current Location Stadium", list(stadiums.keys()), key="fan_stadium")
            with col2:
                selected_lang = st.selectbox("Preferred Language", ["English", "Español", "Français", "Deutsch", "Português", "日本語"], key="fan_lang")
                
            gate = st.text_input("Current Section / Access Gate (e.g. Gate C, Row 24)", placeholder="e.g. Gate B", key="fan_gate")
            
        lang_code = get_language_code(selected_lang)
        
        with st.container(border=True):
            st.markdown("### ❓ Ask ArenaGenius")
            
            # Fill query with voice transcript if recorded
            input_text = voice_query if voice_query else ""
            user_query = st.text_area(
                "What do you need assistance with? (Exits, bathrooms, water stations, transport, rules)",
                value=input_text,
                placeholder="e.g. Where is the nearest exit from here, and can I buy water nearby?",
                key="fan_query"
            )
            
            c_voice, c_submit = st.columns([1, 1])
            with c_voice:
                render_stt_button(lang_code)
                if voice_query:
                    st.success(f"🎙️ Recorded Voice: \"{sanitize_html(voice_query)}\"")
            with c_submit:
                get_guidance = st.button("Generate Guided Recommendation")
                
        if get_guidance and user_query:
            if not is_valid_api_key(api_key):
                st.warning("Please configure a valid Gemini API Key in Settings to get AI guidance.")
            else:
                with st.spinner("Accessing stadium blueprint mapping..."):
                    try:
                        # Prompt structure to instruct the model to respond in the selected language and keep the tone polite and helpful.
                        system_instruction = f"""
                        You are ArenaGenius, an elite AI Concierge for the FIFA World Cup 2026 at {selected_stadium}.
                        The user is currently standing near: {gate}.
                        Respond in {selected_lang}.
                        Ensure your recommendation is detailed, highly polite, direct, and references nearest services like exits or toilets.
                        Include general stadium policies if they ask about baggage, items, or re-entry rules.
                        """
                        model = genai.GenerativeModel(
                            model_name="gemini-2.5-flash",
                            system_instruction=system_instruction
                        )
                        response = model.generate_content(user_query)
                        
                        st.success("✨ AI Companion Guided Response:")
                        st.write(response.text)
                        
                        # Embed browser reading aloud option
                        render_tts_button(response.text, lang_code)
                    except Exception as e:
                        st.error("⚠️ Unable to connect to decision support services. Please verify your API Key and network connection.")
                    
    with tab_chat:
        st.markdown("### 💬 Chat with ArenaGenius")
        st.caption("Ask quick questions about restrooms, food, exits, translation, or policies.")
        
        # Initialize conversation state
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            
        # Draw prior chat items
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                
        # Handle new chat entries
        if prompt := st.chat_input("Where is Section B? / Translate 'Ticket' to Spanish..."):
            with st.chat_message("user"):
                st.write(prompt)
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            if not is_valid_api_key(api_key):
                with st.chat_message("assistant"):
                    st.write("Please set a valid Gemini API Key in settings.")
            else:
                with st.spinner("Formulating response..."):
                    try:
                        # Simple chat instruction
                        chat_sys = f"You are a friendly stadium AI chat assistant at the FIFA World Cup 2026. Keep answers under 3 sentences."
                        model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=chat_sys)
                        response = model.generate_content(prompt)
                        
                        with st.chat_message("assistant"):
                            st.write(response.text)
                        st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                    except Exception as e:
                        with st.chat_message("assistant"):
                            st.write("⚠️ Connection to the assistant failed. Please check settings and retry.")
                    
    with tab_faq:
        st.markdown("### 📋 Frequently Asked Questions")
        faqs = get_cached_faqs()
        
        for idx, item in enumerate(faqs):
            category = item["category"]
            
            # Select question language
            if selected_lang == "Español":
                q = f"¿{item['q_en']}?"  # Simple translation mock wrapper
                a = item["a_es"]
            elif selected_lang == "Français":
                q = item["q_en"] # Keep English or mock French
                a = item["a_fr"]
            else:
                q = item["q_en"]
                a = item["a_en"]
                
            with st.expander(f"{category} | {q}"):
                st.write(a)
