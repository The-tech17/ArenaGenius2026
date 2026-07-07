import streamlit as st
import textwrap

def get_theme_css(theme_mode):
    """
    Returns custom CSS for the FIFA-style smart stadium dashboard.
    Supports Light Mode, Dark Mode, and System Default.
    """
    if theme_mode == "Dark Mode":
        css_variables = """
        :root {
            --background: #020617;
            --text: #f8fafc;
            --sidebar-bg: #0b1329;
            --card-bg: #0f172a;
            --card-border: #1e293b;
            --primary: #10b981; /* World Cup green */
            --primary-rgb: 16, 185, 129;
            --accent: #f59e0b; /* Gold/yellow */
            --success: #10b981;
            --info: #06b6d4;
            --warning: #fbbf24;
            --danger: #f43f5e;
            --muted: #64748b;
            --radius: 16px;
            --shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.7);
        }
        """
    elif theme_mode == "Light Mode":
        css_variables = """
        :root {
            --background: #f8fafc;
            --text: #0f172a;
            --sidebar-bg: #ffffff;
            --card-bg: #ffffff;
            --card-border: #e2e8f0;
            --primary: #0f52ba; /* Premium Blue */
            --primary-rgb: 15, 82, 186;
            --accent: #10b981; /* World Cup green */
            --success: #10b981;
            --info: #06b6d4;
            --warning: #f59e0b;
            --danger: #ef4444;
            --muted: #64748b;
            --radius: 16px;
            --shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.08);
        }
        """
    else:  # System Default (FIFA Dark Navy Theme)
        css_variables = """
        :root {
            --background: #040815;
            --text: #f8fafc;
            --sidebar-bg: #0a0f24;
            --card-bg: #0f1535;
            --card-border: #1d2554;
            --primary: #10b981; /* Emerald Green */
            --primary-rgb: 16, 185, 129;
            --accent: #fbbf24; /* FIFA Gold */
            --success: #10b981;
            --info: #0ea5e9;
            --warning: #f59e0b;
            --danger: #f43f5e;
            --muted: #94a3b8;
            --radius: 16px;
            --shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.6);
        }
        @media (prefers-color-scheme: light) {
            :root {
                --background: #f4f6fc;
                --text: #0b1329;
                --sidebar-bg: #ffffff;
                --card-bg: #ffffff;
                --card-border: #e2e8f0;
                --primary: #0a0f24;
                --primary-rgb: 10, 15, 36;
                --accent: #10b981;
                --success: #10b981;
                --info: #06b6d4;
                --warning: #fbbf24;
                --danger: #ef4444;
                --muted: #64748b;
                --radius: 16px;
                --shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.08);
            }
        }
        """
    
    css_content = f"""
    <style>
    {css_variables}
    
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Rajdhani:wght@500;600;700&display=swap');
    
    .stApp {{
        background-color: var(--background) !important;
        color: var(--text) !important;
        font-family: 'Outfit', sans-serif !important;
    }}
    
    /* Global Typography Override */
    h1, h2, h3, h4, h5, h6, p, li, label, select, textarea, input {{
        font-family: 'Outfit', sans-serif !important;
    }}
    
    h1, h2, h3, h4 {{
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    [data-testid="stSidebar"] {{
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid var(--card-border) !important;
    }}
    
    /* Ensure all text-containing elements inside the sidebar are highly readable */
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] h5,
    [data-testid="stSidebar"] h6,
    [data-testid="stSidebar"] small,
    [data-testid="stSidebar"] caption,
    [data-testid="stSidebar"] div[data-testid="stRadio"] label,
    [data-testid="stSidebar"] .sidebar-section-header {{
        color: var(--text) !important;
    }}
    
    /* Input Elements */
    div[data-baseweb="input"], div[data-baseweb="select"] > div, textarea, input {{
        background-color: var(--card-bg) !important;
        color: var(--text) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: var(--radius) !important;
        transition: all 0.25s ease-in-out !important;
    }}
    
    div[data-baseweb="select"] > div * {{
        color: var(--text) !important;
    }}
    
    div[data-baseweb="input"]:focus-within, div[data-baseweb="select"]:focus-within > div, textarea:focus, input:focus {{
        border-color: var(--primary) !important;
        box-shadow: 0 0 12px rgba(var(--primary-rgb), 0.25) !important;
    }}
    
    /* Dropdown Hover styling */
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
    
    /* Buttons styling */
    div[data-testid="stButton"] button {{
        font-family: 'Outfit', sans-serif !important;
        background: linear-gradient(135deg, var(--primary), #059669) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius) !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        box-shadow: var(--shadow) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
    }}
    div[data-testid="stButton"] button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(var(--primary-rgb), 0.4) !important;
        filter: brightness(1.1);
    }}
    
    /* Card Container Wrapper */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: var(--radius) !important;
        padding: 1.5rem !important;
        box-shadow: var(--shadow) !important;
        margin-bottom: 1.5rem !important;
        transition: transform 0.25s ease !important;
    }}
    
    /* Operations Cards */
    .ops-card {{
        background-color: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: var(--radius);
        padding: 1.25rem;
        box-shadow: var(--shadow);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-align: center;
        position: relative;
        overflow: hidden;
    }}
    
    .ops-card:hover {{
        transform: translateY(-5px);
        border-color: var(--primary);
        box-shadow: 0 15px 30px -5px rgba(var(--primary-rgb), 0.15);
    }}
    
    /* Metric container override */
    div[data-testid="metric-container"] {{
        background-color: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: var(--radius) !important;
        padding: 1.25rem !important;
        box-shadow: var(--shadow) !important;
        text-align: center !important;
    }}
    div[data-testid="stMetricValue"] {{
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 700 !important;
        font-size: 2.2rem !important;
    }}
    
    /* Custom Badge/Tag styling */
    .badge {{
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    .badge-danger {{ background-color: rgba(244, 63, 94, 0.15); color: #f43f5e; border: 1px solid rgba(244, 63, 94, 0.3); }}
    .badge-warning {{ background-color: rgba(245, 158, 11, 0.15); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.3); }}
    .badge-success {{ background-color: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); }}
    
    /* Ticket confirmation styling */
    .ticket-container {{
        background: linear-gradient(145deg, var(--card-bg), #1e1b4b);
        border: 2px solid var(--primary);
        border-radius: var(--radius);
        padding: 2rem;
        color: white;
        margin-top: 1.5rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 40px -10px rgba(16, 185, 129, 0.2);
    }}
    
    .ticket-container::before {{
        content: '';
        position: absolute;
        top: -50px;
        right: -50px;
        width: 150px;
        height: 150px;
        background: radial-gradient(circle, rgba(16, 185, 129, 0.2) 0%, transparent 70%);
        border-radius: 50%;
    }}
    
    .ticket-header {{
        border-bottom: 1px dashed rgba(255, 255, 255, 0.2);
        padding-bottom: 1rem;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    
    .ticket-id {{
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--accent);
        letter-spacing: 1px;
    }}
    
    .ticket-field {{
        margin-bottom: 0.8rem;
    }}
    
    .ticket-label {{
        font-size: 0.8rem;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    .ticket-value {{
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text);
    }}
    
    /* Pulse Animation for Live telemetry indicator */
    .pulse-container {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.85rem;
        font-weight: 600;
        color: #f43f5e;
        margin-bottom: 1rem;
    }}
    .pulse-dot {{
        width: 8px;
        height: 8px;
        background-color: #f43f5e;
        border-radius: 50%;
        box-shadow: 0 0 0 0 rgba(244, 63, 94, 0.7);
        animation: pulse 1.6s infinite;
    }}
    @keyframes pulse {{
        0% {{
            transform: scale(0.95);
            box-shadow: 0 0 0 0 rgba(244, 63, 94, 0.7);
        }}
        70% {{
            transform: scale(1);
            box-shadow: 0 0 0 8px rgba(244, 63, 94, 0);
        }}
        100% {{
            transform: scale(0.95);
            box-shadow: 0 0 0 0 rgba(244, 63, 94, 0);
        }}
    }}
    
    /* Clean custom sidebar headers */
    .sidebar-section-header {{
        font-family: 'Rajdhani', sans-serif !important;
        color: var(--accent) !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.5rem !important;
        text-transform: uppercase !important;
    }}
    
    .stDeployButton {{
        display: none !important;
    }}
    [data-testid="stHeader"] {{
        background-color: transparent !important;
    }}
    </style>
    """
    return textwrap.dedent(css_content)

def render_header(is_compact=False):
    """
    Renders a stunning FIFA-branded header banner.
    Reduces height by ~40% and switches layout when is_compact is True.
    """
    if is_compact:
        padding = "1rem 2rem"
        title_size = "1.8rem"
        subtitle_display = "none"
        margin = "1rem"
        banner_height = "auto"
    else:
        padding = "2rem"
        title_size = "2.6rem"
        subtitle_display = "block"
        margin = "2rem"
        banner_height = "auto"
        
    header_html = f"""
    <div style="
        background: linear-gradient(135deg, #090f24 0%, #1e1b4b 50%, #064e3b 100%);
        padding: {padding};
        border-radius: 16px;
        border: 1px solid var(--card-border);
        color: white;
        text-align: center;
        margin-bottom: {margin};
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 30px -10px rgba(16, 185, 129, 0.25);
        height: {banner_height};
    ">
        <!-- Decorative diagonal highlights -->
        <div style="
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: repeating-linear-gradient(
                45deg,
                transparent,
                transparent 10px,
                rgba(16, 185, 129, 0.03) 10px,
                rgba(16, 185, 129, 0.03) 20px
            );
            pointer-events: none;
        "></div>
        
        <div style="display: flex; align-items: center; justify-content: center; gap: 1rem; position: relative; z-index: 1;">
            <span style="font-size: {title_size};">⚽</span>
            <h1 style="
                color: white !important; 
                font-size: {title_size}; 
                font-weight: 800; 
                margin: 0; 
                text-shadow: 0 2px 8px rgba(16, 185, 129, 0.5);
                font-family: 'Rajdhani', sans-serif !important;
                letter-spacing: 1px;
            ">
                ARENAGENIUS 2026
            </h1>
            <span style="
                background: linear-gradient(90deg, var(--accent), #fbbf24);
                padding: 0.2rem 0.6rem;
                border-radius: 6px;
                font-size: 0.75rem;
                font-weight: 800;
                color: #040815;
                font-family: 'Rajdhani', sans-serif !important;
            ">
                FIFA OPS
            </span>
        </div>
        
        <p style="
            display: {subtitle_display};
            color: var(--muted) !important; 
            font-size: 1.1rem; 
            margin-top: 0.75rem; 
            margin-bottom: 0; 
            font-weight: 500;
            letter-spacing: 0.5px;
        ">
            Tactical Stadium Operations & Real-Time Decision Support • FIFA World Cup 2026
        </p>
    </div>
    """
    st.markdown(textwrap.dedent(header_html), unsafe_allow_html=True)
