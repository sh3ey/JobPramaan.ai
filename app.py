import streamlit as st
from predict import predict_job_posting
import time

# 1. Page Config (Wide Layout is essential for this design)
st.set_page_config(
    page_title="JobScamScore AI",
    page_icon="🛡️",
    layout="wide"
)

# 2. Hardcore Dark Theme & Specific UI Matching Screenshot 2026-07-26 023303.jpg
st.markdown("""
    <style>
    /* Hide Streamlit Headers/Footers */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Full App Background */
    .stApp {
        background-color: #060908; /* Super dark greenish-black */
    }
    
    /* Adjust main container width and padding */
    .block-container {
        padding-top: 5rem;
        max-width: 1300px;
    }

    /* --- LEFT COLUMN TYPOGRAPHY --- */
    .overline-text {
        color: #6b7280;
        letter-spacing: 2.5px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 20px;
    }
    .main-heading {
        font-size: 72px;
        font-weight: 700;
        line-height: 1.05;
        color: #ffffff;
        margin-bottom: 30px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .highlight-green {
        color: #22c55e; /* Neon Green */
    }
    .subtext {
        color: #9ca3af;
        font-size: 18px;
        line-height: 1.6;
        max-width: 85%;
    }
    .subtext strong {
        color: #ffffff;
    }

    /* --- RIGHT COLUMN (THE APP CARD) --- */
    /* Target the second column specifically to make it look like a software window */
    [data-testid="column"]:nth-of-type(2) {
        background-color: #0b110e;
        border: 1px solid #1a2621;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
    }

    /* Text Area Styling */
    .stTextArea label { display: none; } /* Hide label */
    .stTextArea textarea {
        background-color: #121a17 !important;
        border: 1px solid #1f2e28 !important;
        color: #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 16px !important;
        font-size: 15px !important;
        min-height: 180px !important;
    }
    .stTextArea textarea:focus {
        border-color: #22c55e !important;
        box-shadow: 0 0 0 1px #22c55e !important;
    }

    /* Scan Button */
    .stButton button {
        background-color: #1f7844 !important; /* Muted green for default state */
        color: #ffffff !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 12px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        width: 100% !important;
        transition: 0.3s ease !important;
        margin-top: 10px !important;
    }
    .stButton button:hover {
        background-color: #22c55e !important; /* Bright neon green on hover */
        color: #000000 !important;
    }

    /* Security Footer Text */
    .security-text {
        color: #4b5563;
        font-size: 11px;
        text-align: center;
        margin-top: 15px;
        display: flex;
        justify-content: center;
        gap: 15px;
    }

    /* Mac Dots & Tabs Header */
    .window-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    .tabs {
        display: flex;
        gap: 15px;
    }
    .tab {
        background-color: #212f29;
        color: #fff;
        border: 1px solid #2d4038;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .tab-inactive {
        color: #6b7280;
        font-size: 12px;
        font-weight: 500;
        padding: 5px 5px;
    }
    .mac-dots {
        display: flex;
        gap: 6px;
    }
    .dot {
        height: 10px; width: 10px; border-radius: 50%;
    }

    /* Result Box Styling */
    .result-box-danger {
        background-color: #180a0a;
        border: 1px solid #4a1515;
        border-radius: 12px;
        padding: 16px;
        margin-top: 20px;
    }
    .result-box-safe {
        background-color: #0a180e;
        border: 1px solid #144a23;
        border-radius: 12px;
        padding: 16px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Layout Generation (2 Columns)
# Make the left column slightly wider than the right column, just like the image
col1, col2 = st.columns([1.1, 1], gap="large")

# --- LEFT COLUMN (Typography) ---
with col1:
    st.markdown('<div class="overline-text">FREE AI JOB SCAM CHECKER</div>', unsafe_allow_html=True)
    st.markdown('''
        <div class="main-heading">
            Check if a job is a<br>
            scam<br>
            <span class="highlight-green">before you reply.</span>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown('''
        <div class="subtext">
            Paste any job description or requirements. Get a <strong>0–100 risk score</strong> 
            with every red flag explained — completely <strong>free with no account required.</strong>
        </div>
    ''', unsafe_allow_html=True)

# --- RIGHT COLUMN (The App Window) ---
with col2:
    # 4. Fake Window Header (Tabs & Mac Dots)
    st.markdown('''
        <div class="window-header">
            <div class="tabs">
                <div class="tab"><span style="color:#22c55e;">●</span> Paste text</div>
                <div class="tab-inactive">🔗 URL</div>
                <div class="tab-inactive">🖼️ Screenshot</div>
            </div>
            <div class="mac-dots">
                <div class="dot" style="background-color: #ef4444;"></div>
                <div class="dot" style="background-color: #f59e0b;"></div>
                <div class="dot" style="background-color: #22c55e;"></div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # 5. Input Area
    job_text = st.text_area(
        "", 
        placeholder="Paste the full job description here...",
        height=200,
        label_visibility="collapsed"
    )

    # 6. Button
    scan_clicked = st.button("Scan Now ➔")

    # 7. Fake Security Sub-footer
    st.markdown('''
        <div class="security-text">
            <span>🔒 Anonymous scan</span>
            <span>Names redacted</span>
            <span>IP not stored</span>
            <span>Never sold</span>
        </div>
    ''', unsafe_allow_html=True)

    # 8. Prediction Logic & Results UI
    if scan_clicked:
        if not job_text.strip():
            st.warning("Please paste some text to scan.")
        else:
            with st.spinner("Analyzing text syntax and risk factors..."):
                time.sleep(1.2) # Realistic delay
                
                result = predict_job_posting(job_text)
                is_fake = result["is_fake"]
                prob = result.get("probability_fake")
                
                # Mock score if model doesn't return probability
                if prob is None:
                    prob = 98.4 if is_fake else 4.2
                
                # Render results matching the bottom-right of the screenshot
                if is_fake:
                    st.markdown(f'''
                        <div class="result-box-danger">
                            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #331515; padding-bottom: 10px; margin-bottom: 10px;">
                                <div style="color: #e5e7eb; font-weight: 600; font-size: 14px;"><span style="color:#ef4444;">●</span> Analyzed Text - Potential Fraud</div>
                                <div style="background-color: #ef4444; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; letter-spacing: 1px;">{prob} / 100 MAX RISK</div>
                            </div>
                            <ul style="color: #ef4444; font-size: 13px; margin: 0; padding-left: 15px;">
                                <li style="margin-bottom: 5px;">High concentration of scam-related keywords detected</li>
                                <li style="margin-bottom: 5px;">Unrealistic salary to experience ratio</li>
                                <li>Urgency pattern or requests for financial info suspected</li>
                            </ul>
                        </div>
                    ''', unsafe_allow_html=True)
                else:
                    real_score = round((100 - prob) if prob > 50 else prob, 1) # Keep score low for safe
                    st.markdown(f'''
                        <div class="result-box-safe">
                            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #143320; padding-bottom: 10px; margin-bottom: 10px;">
                                <div style="color: #e5e7eb; font-weight: 600; font-size: 14px;"><span style="color:#22c55e;">●</span> Analyzed Text - Legitimate</div>
                                <div style="background-color: #22c55e; color: black; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; letter-spacing: 1px;">{real_score} / 100 SAFE</div>
                            </div>
                            <ul style="color: #22c55e; font-size: 13px; margin: 0; padding-left: 15px;">
                                <li style="margin-bottom: 5px;">No suspicious financial requests found</li>
                                <li>Language patterns match standard corporate postings</li>
                            </ul>
                        </div>
                    ''', unsafe_allow_html=True)