import streamlit as st


def page_header(titulo, subtitulo=None):
    subtitulo_html = f"<p>{subtitulo}</p>" if subtitulo else ""
    st.markdown(
        f"""
        <div class="pa-page-header">
            <h1>{titulo}</h1>
            {subtitulo_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_note(texto):
    st.markdown(f'<div class="pa-section-note">{texto}</div>', unsafe_allow_html=True)


def aplicar_estilos():
    st.markdown(
        """
        <style>
            :root {
                --pa-bg: #f6f3ea;
                --pa-panel: #ffffff;
                --pa-panel-soft: #fbfaf5;
                --pa-text: #171717;
                --pa-muted: #6f6a60;
                --pa-line: #ded8ca;
                --pa-dark: #0f1012;
                --pa-dark-soft: #1b1c20;
                --pa-yellow: #ffc400;
                --pa-yellow-hover: #f2b600;
                --pa-red: #d93636;
                --pa-red-hover: #bd2c2c;
                --pa-green: #1f9d55;
            }

            .stApp {
                background: var(--pa-bg) !important;
                color: var(--pa-text) !important;
            }

            [data-testid="stMain"] {
                background: var(--pa-bg) !important;
            }

            [data-testid="stMain"] .block-container {
                max-width: 1220px;
                padding-top: 3.25rem;
                padding-bottom: 4rem;
            }

            h1, h2, h3, h4 {
                color: var(--pa-text) !important;
                letter-spacing: 0 !important;
            }

            [data-testid="stMain"] p,
            [data-testid="stMain"] li,
            [data-testid="stMain"] label {
                color: var(--pa-text) !important;
            }

            [data-testid="stMain"] small,
            [data-testid="stCaptionContainer"],
            [data-testid="stCaptionContainer"] p {
                color: var(--pa-muted) !important;
            }

            header[data-testid="stHeader"] {
                background: rgba(246, 243, 234, 0.92) !important;
                backdrop-filter: blur(10px);
                border-bottom: 1px solid rgba(222, 216, 202, 0.7);
            }

            header[data-testid="stHeader"] svg,
            header[data-testid="stHeader"] a,
            header[data-testid="stHeader"] button,
            header[data-testid="stHeader"] span {
                color: var(--pa-text) !important;
                fill: var(--pa-text) !important;
            }

            [data-testid="stSidebar"] {
                background: var(--pa-dark) !important;
                border-right: 1px solid #2a2b31;
            }

            [data-testid="stSidebar"] * {
                color: #f7f3e7 !important;
            }

            [data-testid="stSidebarNav"] li a {
                border-radius: 8px;
                margin: 2px 8px;
            }

            [data-testid="stSidebarNav"] li a:hover {
                background: #25262b !important;
            }

            [data-testid="stSidebarNav"] li a[aria-current="page"],
            [data-testid="stSidebarNav"] li a[aria-current="page"]:hover {
                background: var(--pa-yellow) !important;
            }

            [data-testid="stSidebarNav"] li a[aria-current="page"] span {
                color: #111111 !important;
                font-weight: 800 !important;
            }

            .pa-page-header {
                margin: 0 0 1.4rem;
                padding: 1.35rem 1.45rem;
                border: 1px solid var(--pa-line);
                border-radius: 16px;
                background:
                    linear-gradient(135deg, rgba(255, 196, 0, 0.16), transparent 42%),
                    var(--pa-panel);
                box-shadow: 0 14px 34px rgba(15, 16, 18, 0.06);
            }

            .pa-page-header h1 {
                margin: 0 !important;
                font-size: clamp(1.75rem, 3vw, 2.35rem) !important;
                font-weight: 950 !important;
                line-height: 1.05 !important;
            }

            .pa-page-header p {
                max-width: 780px;
                margin: 0.55rem 0 0 !important;
                color: var(--pa-muted) !important;
                font-size: 1rem;
            }

            .pa-section-note {
                margin: 0.4rem 0 1rem;
                padding: 0.9rem 1rem;
                border: 1px solid rgba(255, 196, 0, 0.32);
                border-radius: 12px;
                background: rgba(255, 196, 0, 0.1);
                color: var(--pa-text);
                font-weight: 650;
            }

            .stButton > button,
            .stFormSubmitButton > button {
                border-radius: 9px !important;
                min-height: 42px !important;
                font-weight: 800 !important;
                border: 1px solid transparent !important;
                transition: background 0.15s ease, border-color 0.15s ease, transform 0.15s ease !important;
            }

            .stButton > button:focus,
            .stFormSubmitButton > button:focus {
                box-shadow: 0 0 0 3px rgba(255, 196, 0, 0.28) !important;
                outline: none !important;
            }

            .stButton > button:hover,
            .stFormSubmitButton > button:hover {
                transform: translateY(-1px);
            }

            div.stButton > button[kind="primary"],
            div.stFormSubmitButton > button[kind="primary"] {
                background: var(--pa-yellow) !important;
                border-color: var(--pa-yellow) !important;
            }

            div.stButton > button[kind="primary"] *,
            div.stFormSubmitButton > button[kind="primary"] * {
                color: #111111 !important;
            }

            div.stButton > button[kind="primary"]:hover,
            div.stFormSubmitButton > button[kind="primary"]:hover {
                background: var(--pa-yellow-hover) !important;
                border-color: var(--pa-yellow-hover) !important;
            }

            div.stButton > button[kind="secondary"] {
                background: var(--pa-red) !important;
                border-color: var(--pa-red) !important;
            }

            div.stButton > button[kind="secondary"] *,
            div.stFormSubmitButton > button[kind="secondary"] * {
                color: #ffffff !important;
            }

            div.stButton > button[kind="secondary"]:hover {
                background: var(--pa-red-hover) !important;
                border-color: var(--pa-red-hover) !important;
            }

            .stTextInput input,
            .stNumberInput input,
            .stTextArea textarea,
            div[data-baseweb="select"] > div {
                background: var(--pa-panel) !important;
                color: var(--pa-text) !important;
                border: 1px solid var(--pa-line) !important;
                border-radius: 8px !important;
                box-shadow: none !important;
            }

            div[data-baseweb="select"] * {
                color: var(--pa-text) !important;
            }

            div[data-baseweb="popover"] {
                z-index: 999999 !important;
            }

            div[data-baseweb="popover"] ul,
            div[data-baseweb="popover"] li {
                background: var(--pa-panel) !important;
                color: var(--pa-text) !important;
            }

            .stTextInput input:focus,
            .stNumberInput input:focus,
            .stTextArea textarea:focus {
                border-color: var(--pa-yellow) !important;
                box-shadow: 0 0 0 2px rgba(255, 196, 0, 0.24) !important;
            }

            input::placeholder,
            textarea::placeholder {
                color: #9a9489 !important;
            }

            [data-testid="stFileUploader"] section {
                background: var(--pa-panel) !important;
                border: 1px dashed #bfb6a2 !important;
                border-radius: 10px !important;
                min-height: 86px;
            }

            [data-testid="stFileUploader"] section * {
                color: var(--pa-text) !important;
            }

            [data-testid="stFileUploader"] button {
                background: var(--pa-dark) !important;
                color: #ffffff !important;
                border-radius: 8px !important;
            }

            [data-testid="stExpander"] {
                background: var(--pa-panel) !important;
                border: 1px solid var(--pa-line) !important;
                border-radius: 10px !important;
                overflow: hidden;
                margin-bottom: 0.9rem;
            }

            [data-testid="stExpander"] details summary {
                background: var(--pa-dark) !important;
                color: #ffffff !important;
                min-height: 46px;
            }

            [data-testid="stExpander"] details summary * {
                color: #ffffff !important;
            }

            [data-testid="stExpander"] details[open] summary {
                border-bottom: 1px solid var(--pa-line);
            }

            [data-testid="stDataFrame"],
            [data-testid="stTable"],
            [data-testid="stMetric"],
            [data-testid="stAlert"] {
                border-radius: 10px !important;
            }

            [data-testid="stDataFrame"] {
                border: 1px solid var(--pa-line) !important;
                box-shadow: 0 10px 24px rgba(15, 16, 18, 0.05);
            }

            [data-testid="stMetric"] {
                background: var(--pa-panel) !important;
                border: 1px solid var(--pa-line) !important;
                padding: 16px !important;
                box-shadow: 0 8px 24px rgba(15, 16, 18, 0.06) !important;
            }

            [data-testid="stMetricValue"] div {
                color: var(--pa-red) !important;
            }

            [data-testid="stAlert"] {
                background: #fff7d6 !important;
                border: 1px solid #f2d46b !important;
            }

            [data-testid="stAlert"] * {
                color: var(--pa-text) !important;
            }

            hr {
                border-color: var(--pa-line) !important;
            }

            @media (max-width: 760px) {
                [data-testid="stMain"] .block-container {
                    padding-left: 1rem;
                    padding-right: 1rem;
                    padding-top: 2rem;
                }

                .pa-page-header {
                    padding: 1.1rem;
                    border-radius: 14px;
                }
            }
            
            .pa-home-card {
                background: var(--pa-panel);
                border: 1px solid var(--pa-line);
                border-radius: 14px;
                padding: 18px;
                min-height: 154px;
                box-shadow: 0 10px 24px rgba(15,16,18,.05);
            }

            .pa-home-card h3 {
                margin: 0 0 8px !important;
                font-size: 1.08rem !important;
                line-height: 1.15 !important;
            }

            .pa-home-card p {
                color: var(--pa-muted) !important;
                font-size: .9rem;
                line-height: 1.4;
                margin: 0 0 14px !important;
            }

            .pa-home-hero {
                margin: 0 0 1.3rem;
                padding: 1.5rem;
                display: grid;
                grid-template-columns: 108px 1fr;
                gap: 1.2rem;
                align-items: center;
                border: 1px solid var(--pa-line);
                border-radius: 18px;
                background:
                    linear-gradient(135deg, rgba(255, 196, 0, 0.2), transparent 46%),
                    var(--pa-panel);
                box-shadow: 0 16px 36px rgba(15,16,18,.06);
            }

            .pa-home-logo {
                width: 108px;
                height: 108px;
                border-radius: 18px;
                object-fit: cover;
                border: 1px solid rgba(255, 196, 0, .36);
                box-shadow: 0 12px 24px rgba(15,16,18,.09);
            }

            .pa-home-kicker {
                margin: 0 0 .35rem !important;
                color: var(--pa-muted) !important;
                text-transform: uppercase;
                font-size: .78rem;
                font-weight: 850;
            }

            .pa-home-hero h1 {
                margin: 0 !important;
                color: var(--pa-text) !important;
                font-size: clamp(2rem, 4vw, 3rem) !important;
                line-height: .98 !important;
                font-weight: 950 !important;
            }

            .pa-home-hero h1 span {
                color: var(--pa-yellow);
            }

            .pa-home-hero p:last-child {
                max-width: 720px;
                margin: .65rem 0 0 !important;
                color: var(--pa-muted) !important;
                line-height: 1.45;
            }

            .pa-home-section-title {
                margin: 1.1rem 0 .7rem !important;
                font-size: 1rem !important;
                text-transform: uppercase;
                letter-spacing: 0 !important;
                font-weight: 950 !important;
            }

            .pa-home-card .stButton > button {
                width: 100%;
            }

            @media (max-width: 760px) {
                .pa-home-hero {
                    grid-template-columns: 1fr;
                    padding: 1.15rem;
                }

                .pa-home-logo {
                    width: 88px;
                    height: 88px;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
