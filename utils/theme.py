from datetime import datetime, timedelta, timezone

import streamlit as st

def clean_html(html_str):
    """
    Strips all leading whitespace from each line in the HTML/CSS string
    to prevent the Streamlit Markdown parser from treating indented lines
    as preformatted code blocks.
    """
    if not html_str:
        return ""
    return "\n".join([line.lstrip() for line in html_str.split("\n")])

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
            --radius: 10px;
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
            --radius: 10px;
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
            --radius: 10px;
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
                --radius: 10px;
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

    .mission-hero {{
        display: grid;
        grid-template-columns: minmax(260px, 0.9fr) minmax(420px, 1.6fr);
        gap: 1px;
        background: var(--card-border);
        border: 1px solid var(--card-border);
        border-radius: var(--radius);
        overflow: hidden;
        margin: 0 0 1rem 0;
        box-shadow: var(--shadow);
    }}

    .mission-main,
    .mission-grid > div {{
        background:
            linear-gradient(145deg, rgba(15, 21, 53, 0.96), rgba(4, 8, 21, 0.98)),
            var(--card-bg);
    }}

    .mission-main {{
        padding: 1.5rem;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 260px;
    }}

    .mission-kicker,
    .widget-eyebrow {{
        color: var(--accent);
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }}

    .mission-main h2 {{
        margin: 0.35rem 0 0.2rem 0 !important;
        color: var(--text) !important;
        font-size: 2.2rem !important;
        line-height: 1 !important;
        letter-spacing: 0 !important;
    }}

    .mission-venue {{
        color: var(--muted);
        font-size: 1rem;
        font-weight: 600;
    }}

    .mission-status {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        border-top: 1px solid rgba(148, 163, 184, 0.16);
        padding-top: 1rem;
        margin-top: 1rem;
        color: var(--muted);
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }}

    .mission-status span,
    .widget-live {{
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        white-space: nowrap;
    }}

    .mission-status strong,
    .risk-low {{
        color: var(--success) !important;
    }}

    .mission-grid {{
        display: grid;
        grid-template-columns: repeat(4, minmax(130px, 1fr));
        gap: 1px;
    }}

    .mission-grid > div {{
        padding: 1.25rem;
        min-height: 118px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}

    .mission-grid span,
    .kpi-head,
    .kpi-mid,
    .kpi-foot,
    .widget-footer,
    .widget-note,
    .recommendation-panel span,
    .weather-impact span,
    .ai-grid-mini span,
    .health-row span,
    .dispatch-row span,
    .queue-row span {{
        color: var(--muted);
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }}

    .mission-grid strong {{
        color: var(--text);
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1.45rem;
        line-height: 1.05;
        margin-top: 0.35rem;
    }}

    .live-strip {{
        display: grid;
        grid-template-columns: repeat(6, minmax(130px, 1fr));
        gap: 1px;
        background: var(--card-border);
        border: 1px solid var(--card-border);
        border-radius: var(--radius);
        overflow: hidden;
        margin-bottom: 1rem;
    }}

    .live-strip > div {{
        min-height: 48px;
        background: rgba(15, 23, 42, 0.78);
        display: flex;
        align-items: center;
        gap: 0.45rem;
        padding: 0.65rem 0.85rem;
        color: var(--text);
    }}

    .live-strip strong {{
        font-size: 0.82rem;
    }}

    .live-strip span:not(.status-dot) {{
        color: var(--muted);
        font-size: 0.78rem;
        margin-left: auto;
    }}

    .status-dot {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--dot-color, var(--success));
        box-shadow: 0 0 0 0 color-mix(in srgb, var(--dot-color, var(--success)) 55%, transparent);
        animation: opsPulse 1.8s ease-out infinite;
        flex: 0 0 auto;
    }}

    @keyframes opsPulse {{
        0% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.45); }}
        70% {{ box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }}
    }}

    .kpi-grid {{
        display: grid;
        grid-template-columns: repeat(4, minmax(180px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }}

    .kpi-card,
    .ops-widget,
    .ai-copilot,
    .activity-feed {{
        background: linear-gradient(180deg, rgba(15, 21, 53, 0.98), rgba(8, 13, 32, 0.98));
        border: 1px solid var(--card-border);
        border-radius: var(--radius);
        box-shadow: var(--shadow);
        transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
    }}

    .kpi-card:hover,
    .ops-widget:hover,
    .ai-copilot:hover,
    .activity-feed:hover {{
        transform: translateY(-2px);
        border-color: color-mix(in srgb, var(--primary) 55%, var(--card-border));
        box-shadow: 0 16px 34px -18px rgba(16, 185, 129, 0.42);
    }}

    .kpi-card {{
        padding: 1rem;
        border-top: 3px solid var(--kpi-color);
        min-height: 190px;
    }}

    .kpi-head,
    .kpi-mid {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.75rem;
    }}

    .kpi-status {{
        color: var(--kpi-color) !important;
    }}

    .kpi-value {{
        color: var(--text);
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 2.45rem;
        font-weight: 800;
        line-height: 1;
        margin: 0.8rem 0 0.4rem;
        font-variant-numeric: tabular-nums;
    }}

    .count-up {{
        animation: numberLift 0.55s ease both;
    }}

    @keyframes numberLift {{
        from {{ opacity: 0.35; transform: translateY(5px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    .trend-positive {{
        color: var(--success) !important;
    }}

    .sparkline {{
        display: block;
        width: 100%;
        height: 38px;
        margin: 0.8rem 0 0.45rem;
    }}

    .ops-widget-grid {{
        display: grid;
        grid-template-columns: repeat(3, minmax(240px, 1fr));
        gap: 1rem;
        margin: 1rem 0 0;
    }}

    .ops-widget,
    .ai-copilot,
    .activity-feed {{
        padding: 1rem;
        min-height: 240px;
    }}

    .widget-title-row,
    .ai-header {{
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: 0.9rem;
    }}

    .widget-title-row h3,
    .ai-header h3,
    .activity-feed h3 {{
        margin: 0.12rem 0 0 0 !important;
        color: var(--text) !important;
        font-size: 1.2rem !important;
        letter-spacing: 0 !important;
    }}

    .widget-live {{
        color: var(--muted);
        font-size: 0.72rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }}

    .density-grid {{
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 0.45rem;
    }}

    .density-cell {{
        aspect-ratio: 1;
        border-radius: 6px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }}

    .level-1 {{ background: rgba(16, 185, 129, 0.16); }}
    .level-2 {{ background: rgba(16, 185, 129, 0.3); }}
    .level-3 {{ background: rgba(6, 182, 212, 0.34); }}
    .level-4 {{ background: rgba(245, 158, 11, 0.48); }}
    .level-5 {{ background: rgba(244, 63, 94, 0.58); }}

    .stadium-map {{
        position: relative;
        min-height: 278px;
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 8px;
        background:
            linear-gradient(90deg, rgba(6, 182, 212, 0.07) 1px, transparent 1px),
            linear-gradient(rgba(6, 182, 212, 0.07) 1px, transparent 1px),
            #050a18;
        background-size: 28px 28px;
        overflow: hidden;
    }}

    .bowl {{
        position: absolute;
        inset: 32px 48px;
        border: 2px solid rgba(6, 182, 212, 0.46);
        border-radius: 50%;
    }}

    .bowl.middle {{
        inset: 62px 92px;
        border-color: rgba(16, 185, 129, 0.5);
    }}

    .pitch {{
        position: absolute;
        inset: 104px 145px;
        border: 1px solid rgba(16, 185, 129, 0.65);
        border-radius: 6px;
        display: grid;
        place-items: center;
        color: rgba(248, 250, 252, 0.62);
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.12em;
    }}

    .map-node {{
        position: absolute;
        z-index: 3;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: grid;
        place-items: center;
        color: #021016;
        font-size: 0.72rem;
        font-weight: 900;
        border: 2px solid rgba(255, 255, 255, 0.38);
    }}

    .gate {{ background: var(--success); }}
    .gate.warning {{ background: var(--warning); }}
    .gate.alert {{ background: var(--danger); color: white; }}
    .med {{ background: #38bdf8; }}
    .security {{ background: #f59e0b; }}
    .gate-a {{ top: 10px; left: 50%; }}
    .gate-b {{ right: 18px; top: 44%; }}
    .gate-c {{ bottom: 14px; left: 48%; }}
    .gate-d {{ left: 18px; top: 44%; }}
    .med-1 {{ left: 26%; top: 29%; }}
    .med-2 {{ right: 28%; bottom: 30%; }}
    .sec-1 {{ right: 28%; top: 28%; }}
    .sec-2 {{ left: 30%; bottom: 26%; }}

    .heat,
    .incident {{
        position: absolute;
        border-radius: 50%;
        z-index: 2;
    }}

    .heat {{
        width: 96px;
        height: 96px;
        background: radial-gradient(circle, rgba(245, 158, 11, 0.42), rgba(245, 158, 11, 0));
        animation: heatBreath 2.8s ease-in-out infinite;
    }}

    .heat-1 {{ right: 18%; top: 28%; }}
    .heat-2 {{ left: 18%; bottom: 22%; }}

    .incident {{
        width: 16px;
        height: 16px;
        background: var(--danger);
        border: 2px solid rgba(255, 255, 255, 0.7);
        box-shadow: 0 0 0 8px rgba(244, 63, 94, 0.14);
    }}

    .incident-1 {{ right: 23%; top: 40%; }}
    .incident-2 {{ left: 36%; bottom: 36%; }}

    .route {{
        position: absolute;
        height: 2px;
        background: repeating-linear-gradient(90deg, rgba(16, 185, 129, 0.8) 0 8px, transparent 8px 14px);
        z-index: 1;
    }}

    .route-north {{ top: 22px; left: 12%; width: 76%; }}
    .route-south {{ bottom: 22px; left: 12%; width: 76%; }}

    @keyframes heatBreath {{
        0%, 100% {{ opacity: 0.55; transform: scale(0.96); }}
        50% {{ opacity: 0.9; transform: scale(1.06); }}
    }}

    .map-legend {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem 0.8rem;
        margin-top: 0.8rem;
        color: var(--muted);
        font-size: 0.76rem;
        font-weight: 700;
    }}

    .map-legend span {{
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
    }}

    .legend {{
        width: 9px;
        height: 9px;
        border-radius: 50%;
        display: inline-block;
    }}
    .legend.gate {{ background: var(--success); }}
    .legend.med {{ background: #38bdf8; }}
    .legend.heat {{ background: var(--warning); }}
    .legend.incident {{ background: var(--danger); }}
    .legend.route {{ background: var(--primary); border-radius: 2px; width: 16px; }}

    .timeline-row,
    .activity-row,
    .queue-row,
    .dispatch-row,
    .health-row {{
        display: grid;
        grid-template-columns: 64px 1fr;
        gap: 0.75rem;
        align-items: center;
        padding: 0.7rem 0;
        border-bottom: 1px solid rgba(148, 163, 184, 0.12);
    }}

    .queue-row,
    .dispatch-row,
    .health-row {{
        grid-template-columns: 86px 1fr auto;
    }}

    .timeline-row strong,
    .activity-row strong {{
        color: var(--info);
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1rem;
    }}

    .timeline-row span,
    .activity-row span,
    .queue-row strong,
    .dispatch-row strong,
    .health-row strong {{
        color: var(--text);
        font-size: 0.9rem;
    }}

    .queue-row em,
    .dispatch-row em,
    .health-row em {{
        color: var(--success);
        font-size: 0.78rem;
        font-style: normal;
        font-weight: 800;
        white-space: nowrap;
    }}

    .weather-impact,
    .ai-grid-mini,
    .recommendation-panel {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.75rem;
    }}

    .weather-impact div,
    .ai-grid-mini div,
    .recommendation-panel div {{
        border: 1px solid rgba(148, 163, 184, 0.14);
        background: rgba(2, 6, 23, 0.32);
        border-radius: 8px;
        padding: 0.75rem;
    }}

    .weather-impact strong,
    .ai-grid-mini strong,
    .recommendation-panel strong {{
        display: block;
        color: var(--text);
        margin-top: 0.35rem;
        font-size: 0.95rem;
    }}

    .widget-footer,
    .widget-note {{
        margin-top: 0.85rem;
        padding-top: 0.8rem;
        border-top: 1px solid rgba(148, 163, 184, 0.12);
        line-height: 1.45;
    }}

    .ai-copilot {{
        min-height: 366px;
        border-color: rgba(16, 185, 129, 0.32);
    }}

    .risk-pill {{
        color: var(--muted);
        border: 1px solid rgba(16, 185, 129, 0.32);
        border-radius: 999px;
        padding: 0.45rem 0.7rem;
        font-size: 0.78rem;
        font-weight: 800;
        text-transform: uppercase;
    }}

    .risk-pill strong {{
        color: var(--success);
        margin-left: 0.35rem;
    }}

    .ai-content {{
        display: grid;
        grid-template-columns: 1.2fr 0.8fr;
        gap: 1rem;
    }}

    .ai-content h4 {{
        margin: 0 0 0.65rem 0 !important;
        color: var(--text) !important;
        font-size: 1rem !important;
        letter-spacing: 0 !important;
    }}

    .ai-content ul {{
        margin: 0;
        padding-left: 1.05rem;
        color: var(--text);
        line-height: 1.7;
        font-size: 0.92rem;
    }}

    .suggested-actions {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(148, 163, 184, 0.12);
    }}

    .suggested-actions button {{
        border: 1px solid rgba(16, 185, 129, 0.34);
        background: rgba(16, 185, 129, 0.12);
        color: var(--text);
        border-radius: 8px;
        padding: 0.55rem 0.75rem;
        font-weight: 800;
        font-family: 'Outfit', sans-serif !important;
    }}

    .activity-feed {{
        min-height: 366px;
    }}

    .skeleton-line {{
        height: 10px;
        border-radius: 999px;
        background: linear-gradient(90deg, rgba(148, 163, 184, 0.08), rgba(148, 163, 184, 0.2), rgba(148, 163, 184, 0.08));
        background-size: 200% 100%;
        animation: skeletonSweep 1.3s infinite;
    }}

    @keyframes skeletonSweep {{
        from {{ background-position: 200% 0; }}
        to {{ background-position: -200% 0; }}
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

    [data-testid="stSidebar"] [role="radiogroup"] label {{
        border-radius: 8px !important;
        padding: 0.45rem 0.55rem !important;
        margin-bottom: 0.2rem !important;
        border: 1px solid transparent !important;
        transition: all 0.18s ease !important;
    }}

    [data-testid="stSidebar"] [role="radiogroup"] label:hover {{
        background: rgba(16, 185, 129, 0.08) !important;
        border-color: rgba(16, 185, 129, 0.18) !important;
    }}

    [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {{
        background: rgba(16, 185, 129, 0.14) !important;
        border-color: rgba(16, 185, 129, 0.34) !important;
    }}

    .sidebar-badge-row {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.75rem;
        border: 1px solid var(--card-border);
        border-radius: 8px;
        padding: 0.6rem 0.7rem;
        margin: 0.75rem 0;
        background: rgba(16, 185, 129, 0.07);
    }}

    .sidebar-badge-row strong {{
        color: var(--text);
        font-size: 0.82rem;
    }}

    .sidebar-badge-row span {{
        color: var(--success) !important;
        font-size: 0.78rem;
        font-weight: 800;
    }}

    .header-ops-grid {{
        display: grid;
        grid-template-columns: repeat(6, minmax(110px, 1fr));
        gap: 1px;
        background: rgba(148, 163, 184, 0.2);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 8px;
        overflow: hidden;
        margin-top: 1.25rem;
        position: relative;
        z-index: 1;
        text-align: left;
    }}

    .header-ops-grid div {{
        background: rgba(2, 6, 23, 0.34);
        padding: 0.75rem;
    }}

    .header-ops-grid span {{
        display: block;
        color: rgba(226, 232, 240, 0.72);
        font-size: 0.68rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }}

    .header-ops-grid strong {{
        display: block;
        color: white;
        margin-top: 0.28rem;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1.12rem;
        line-height: 1.05;
    }}

    @media (max-width: 1100px) {{
        .mission-hero,
        .ai-content {{
            grid-template-columns: 1fr;
        }}
        .mission-grid,
        .kpi-grid,
        .ops-widget-grid {{
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }}
        .live-strip {{
            grid-template-columns: repeat(3, minmax(0, 1fr));
        }}
    }}

    @media (max-width: 720px) {{
        .mission-grid,
        .kpi-grid,
        .ops-widget-grid,
        .live-strip,
        .weather-impact,
        .ai-grid-mini,
        .recommendation-panel {{
            grid-template-columns: 1fr;
        }}
        .mission-main {{
            min-height: auto;
        }}
        .mission-grid > div {{
            min-height: 84px;
        }}
        .pitch {{
            inset: 112px 112px;
        }}
        .queue-row,
        .dispatch-row,
        .health-row {{
            grid-template-columns: 1fr;
            gap: 0.25rem;
        }}
        .header-ops-grid {{
            grid-template-columns: 1fr;
        }}
    }}
    
    .stDeployButton {{
        display: none !important;
    }}
    [data-testid="stHeader"] {{
        background-color: transparent !important;
    }}
    </style>
    """
    return clean_html(css_content)

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
    st.markdown(clean_html(header_html), unsafe_allow_html=True)


def render_header(is_compact=False):
    """
    Renders the ArenaGenius brand banner with home-page operations telemetry.
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

    attendance = st.session_state.get("attendance", 74259)
    capacity = 82500
    weather_temp = st.session_state.get("weather_temp", 22)
    weather_f = round(weather_temp * 9 / 5 + 32)
    weather_cond = st.session_state.get("weather_cond", "Clear")
    kickoff = datetime.now(timezone.utc) + timedelta(hours=2, minutes=14, seconds=18)
    remaining = max(kickoff - datetime.now(timezone.utc), timedelta())
    hours, remainder = divmod(int(remaining.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    countdown = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    header_ops = ""
    if not is_compact:
        header_ops = f"""
        <div class="header-ops-grid">
            <div><span>Stadium</span><strong>MetLife Stadium</strong></div>
            <div><span>Match</span><strong>USA vs Germany</strong></div>
            <div><span>Kickoff In</span><strong>{countdown}</strong></div>
            <div><span>Weather</span><strong>{weather_f}F {weather_cond}</strong></div>
            <div><span>Capacity</span><strong>{attendance:,} / {capacity:,}</strong></div>
            <div><span>Last Updated</span><strong>{datetime.utcnow().strftime("%H:%M:%S")} UTC</strong></div>
        </div>
        """

    header_html = f"""
    <div style="
        background: linear-gradient(135deg, #090f24 0%, #1e1b4b 50%, #064e3b 100%);
        padding: {padding};
        border-radius: var(--radius);
        border: 1px solid var(--card-border);
        color: white;
        text-align: center;
        margin-bottom: {margin};
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 30px -10px rgba(16, 185, 129, 0.25);
        height: {banner_height};
    ">
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
            <span style="font-size: {title_size}; font-family: 'Rajdhani', sans-serif !important; font-weight: 800;">AG</span>
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
            Tactical Stadium Operations & Real-Time Decision Support | FIFA World Cup 2026
        </p>
        {header_ops}
    </div>
    """
    st.markdown(clean_html(header_html), unsafe_allow_html=True)
