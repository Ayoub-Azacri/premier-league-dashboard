def get_custom_css(theme: str = "light") -> str:
    """Returns custom CSS for an executive sports analytics dashboard."""
    is_dark = (theme == "dark")
    bg_card = "#1E293B" if is_dark else "#FFFFFF"
    text_color = "#F8FAFC" if is_dark else "#0F172A"
    sub_color = "#94A3B8" if is_dark else "#64748B"
    border_color = "#334155" if is_dark else "#E2E8F0"
    minto_bg = "#172554" if is_dark else "#EFF6FF"
    minto_border = "#1E3A8A" if is_dark else "#BFDBFE"
    minto_text = "#93C5FD" if is_dark else "#1E3A8A"

    return f"""
    <style>
    .hero-banner {{
        background: {bg_card};
        border: 1px solid {border_color};
        border-radius: 12px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    .hero-badge {{
        display: inline-block;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #2563EB;
        background: {minto_bg};
        border: 1px solid {minto_border};
        border-radius: 9999px;
        padding: 4px 12px;
        margin-bottom: 8px;
    }}
    .hero-title {{
        font-size: 1.75rem;
        font-weight: 800;
        color: {text_color};
        margin: 6px 0 8px 0;
        line-height: 1.25;
    }}
    .hero-subtitle {{
        font-size: 0.95rem;
        color: {sub_color};
        margin-bottom: 12px;
        line-height: 1.5;
    }}
    .minto-card {{
        background: {minto_bg};
        border-left: 4px solid #2563EB;
        border-top: 1px solid {minto_border};
        border-right: 1px solid {minto_border};
        border-bottom: 1px solid {minto_border};
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 20px;
        font-size: 0.92rem;
        color: {text_color};
        line-height: 1.45;
    }}
    .minto-highlight {{
        font-weight: 700;
        color: {minto_text};
    }}
    div[data-testid="stMetricValue"] {{
        font-size: 1.85rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
    }}
    div[data-testid="stMetricDelta"] {{
        font-size: 0.82rem !important;
        font-weight: 600 !important;
    }}
    </style>
    """
