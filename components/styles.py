import streamlit as st


def inject_css():
    st.markdown(
        """
        <style>
        /*
        Streamlit theme-aware variables:
        Light mode এবং Dark mode অনুযায়ী এগুলো নিজে থেকেই পরিবর্তিত হয়।
        */

        :root {
            --mil-primary: #1677c8;
            --mil-primary-soft: rgba(22, 119, 200, 0.10);

            --mil-green: #16845b;
            --mil-green-soft: rgba(22, 132, 91, 0.10);

            --mil-purple: #805ad5;
            --mil-purple-soft: rgba(128, 90, 213, 0.10);

            --mil-orange: #d97706;
            --mil-orange-soft: rgba(217, 119, 6, 0.10);

            --mil-red: #c43d32;

            --mil-card-bg: var(--secondary-background-color);
            --mil-page-bg: var(--background-color);
            --mil-text: var(--text-color);

            --mil-border: rgba(128, 128, 128, 0.22);
            --mil-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
        }

        /* Main page spacing */
        .block-container {
            max-width: 1280px;
            padding-top: 1.5rem;
            padding-bottom: 4rem;
        }

        /* General headings */
        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {
            letter-spacing: -0.02em;
        }

        /* Hero */
        .hero {
            position: relative;
            overflow: hidden;
            padding: clamp(2rem, 5vw, 4.5rem);
            border-radius: 26px;
            background:
                radial-gradient(
                    circle at top right,
                    rgba(80, 180, 255, 0.30),
                    transparent 38%
                ),
                linear-gradient(
                    135deg,
                    #071d37 0%,
                    #0c3d68 48%,
                    #126f94 100%
                );
            border: 1px solid rgba(255, 255, 255, 0.16);
            box-shadow: 0 18px 45px rgba(0, 35, 70, 0.22);
            margin-bottom: 1.6rem;
        }

        .hero::after {
            content: "";
            position: absolute;
            width: 280px;
            height: 280px;
            right: -100px;
            bottom: -160px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.08);
        }

        .hero h1 {
            position: relative;
            z-index: 1;
            color: #ffffff !important;
            font-size: clamp(2.2rem, 5vw, 4.4rem);
            line-height: 1.05;
            margin-bottom: 1rem;
        }

        .hero p {
            position: relative;
            z-index: 1;
            color: rgba(255, 255, 255, 0.90) !important;
            font-size: clamp(1rem, 2vw, 1.2rem);
            max-width: 820px;
            line-height: 1.7;
        }

        /* Custom cards */
        .card {
            background: var(--mil-card-bg);
            color: var(--mil-text);
            border: 1px solid var(--mil-border);
            border-radius: 20px;
            padding: 1.5rem;
            min-height: 215px;
            height: 100%;
            box-shadow: var(--mil-shadow);
            transition:
                transform 0.22s ease,
                border-color 0.22s ease,
                box-shadow 0.22s ease;
        }

        .card:hover {
            transform: translateY(-4px);
            border-color: rgba(22, 119, 200, 0.45);
            box-shadow: 0 14px 34px rgba(0, 0, 0, 0.12);
        }

        .card h1,
        .card h2,
        .card h3,
        .card h4,
        .card h5,
        .card h6,
        .card p,
        .card span,
        .card div,
        .card li {
            color: var(--mil-text) !important;
        }

        .card h3 {
            font-size: 1.35rem;
            margin-top: 0.3rem;
            margin-bottom: 0.8rem;
        }

        .card p {
            opacity: 0.78;
            line-height: 1.65;
            margin-bottom: 0;
        }

        /*
        Vision cards:
        প্রথম, দ্বিতীয়, তৃতীয়, চতুর্থ card-এ আলাদা accent
        */
        div[data-testid="column"]:nth-of-type(1) .card {
            border-top: 4px solid var(--mil-primary);
            background:
                linear-gradient(
                    145deg,
                    var(--mil-primary-soft),
                    transparent 55%
                ),
                var(--mil-card-bg);
        }

        div[data-testid="column"]:nth-of-type(2) .card {
            border-top: 4px solid var(--mil-green);
            background:
                linear-gradient(
                    145deg,
                    var(--mil-green-soft),
                    transparent 55%
                ),
                var(--mil-card-bg);
        }

        div[data-testid="column"]:nth-of-type(3) .card {
            border-top: 4px solid var(--mil-purple);
            background:
                linear-gradient(
                    145deg,
                    var(--mil-purple-soft),
                    transparent 55%
                ),
                var(--mil-card-bg);
        }

        div[data-testid="column"]:nth-of-type(4) .card {
            border-top: 4px solid var(--mil-orange);
            background:
                linear-gradient(
                    145deg,
                    var(--mil-orange-soft),
                    transparent 55%
                ),
                var(--mil-card-bg);
        }

        /* Streamlit metrics */
        [data-testid="stMetric"] {
            position: relative;
            overflow: hidden;
            background:
                linear-gradient(
                    145deg,
                    rgba(22, 119, 200, 0.09),
                    transparent 60%
                ),
                var(--mil-card-bg);
            border: 1px solid var(--mil-border);
            border-radius: 18px;
            padding: 1.35rem 1.4rem;
            min-height: 145px;
            box-shadow: var(--mil-shadow);
            transition:
                transform 0.22s ease,
                border-color 0.22s ease;
        }

        [data-testid="stMetric"]:hover {
            transform: translateY(-3px);
            border-color: rgba(22, 119, 200, 0.45);
        }

        [data-testid="stMetric"]::before {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4px;
            background: linear-gradient(
                180deg,
                #2994e6,
                #13a579
            );
        }

        [data-testid="stMetricLabel"],
        [data-testid="stMetricLabel"] p {
            color: var(--mil-text) !important;
            opacity: 0.72;
            font-size: 0.95rem !important;
            font-weight: 650 !important;
        }

        [data-testid="stMetricValue"],
        [data-testid="stMetricValue"] div {
            color: var(--mil-text) !important;
            font-size: clamp(2rem, 4vw, 2.8rem) !important;
            font-weight: 800 !important;
        }

        [data-testid="stMetricDelta"] {
            color: var(--mil-green) !important;
        }

        /* Bordered Streamlit containers */
        [data-testid="stVerticalBlockBorderWrapper"] {
            background:
                linear-gradient(
                    145deg,
                    rgba(22, 119, 200, 0.035),
                    transparent
                ),
                var(--mil-card-bg);
            border-color: var(--mil-border) !important;
            border-radius: 18px;
            box-shadow: 0 5px 18px rgba(0, 0, 0, 0.05);
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.35rem;
            padding: 0.3rem;
            border-radius: 14px;
            background: var(--mil-card-bg);
            border: 1px solid var(--mil-border);
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 10px;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .stTabs [aria-selected="true"] {
            background: var(--mil-primary-soft);
        }

        /* Buttons */
        div.stButton > button,
        div.stFormSubmitButton > button {
            min-height: 2.8rem;
            border-radius: 12px;
            font-weight: 700;
            transition:
                transform 0.18s ease,
                box-shadow 0.18s ease;
        }

        div.stButton > button:hover,
        div.stFormSubmitButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 18px rgba(22, 119, 200, 0.18);
        }

        /* Badges */
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            padding: 0.35rem 0.75rem;
            border-radius: 999px;
            background: var(--mil-primary-soft);
            color: var(--mil-primary) !important;
            border: 1px solid rgba(22, 119, 200, 0.22);
            font-size: 0.8rem;
            font-weight: 750;
        }

        .badge-green {
            background: var(--mil-green-soft);
            color: var(--mil-green) !important;
            border-color: rgba(22, 132, 91, 0.22);
        }

        .badge-red {
            background: rgba(196, 61, 50, 0.10);
            color: var(--mil-red) !important;
            border-color: rgba(196, 61, 50, 0.22);
        }

        .badge-grey {
            background: rgba(128, 128, 128, 0.10);
            color: var(--mil-text) !important;
            border-color: var(--mil-border);
        }

        .muted {
            color: var(--mil-text) !important;
            opacity: 0.65;
        }

        /* Footer */
        .footer {
            margin-top: 3.5rem;
            padding: 2rem;
            border-radius: 22px;
            background:
                radial-gradient(
                    circle at top right,
                    rgba(48, 168, 255, 0.20),
                    transparent 40%
                ),
                linear-gradient(135deg, #071b32, #0d416b);
            border: 1px solid rgba(255, 255, 255, 0.15);
            box-shadow: 0 14px 35px rgba(0, 35, 70, 0.18);
        }

        .footer h1,
        .footer h2,
        .footer h3,
        .footer h4,
        .footer p,
        .footer span,
        .footer a {
            color: rgba(255, 255, 255, 0.92) !important;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            border-right: 1px solid var(--mil-border);
        }

        [data-testid="stSidebarNav"] a {
            border-radius: 10px;
            margin-bottom: 0.18rem;
        }

        [data-testid="stSidebarNav"] a:hover {
            background: var(--mil-primary-soft);
        }

        /* Dataframe */
        [data-testid="stDataFrame"] {
            border: 1px solid var(--mil-border);
            border-radius: 14px;
            overflow: hidden;
        }

        /* Mobile */
        @media (max-width: 768px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .hero {
                padding: 2.2rem 1.3rem;
                border-radius: 20px;
            }

            .card {
                min-height: auto;
            }

            [data-testid="stMetric"] {
                min-height: 120px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )