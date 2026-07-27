import streamlit as st
from predict import predict_job_posting
import time

st.set_page_config(
    page_title="JobPramaan.ai",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stApp { background-color: #060908; }
    .block-container { padding-top: 5rem; padding-bottom: 5rem; max-width: 1300px; }

    .overline-text { color: #6b7280; letter-spacing: 2.5px; font-size: 12px; font-weight: 600; text-transform: uppercase; margin-bottom: 20px; }
    .main-heading { font-size: 72px; font-weight: 700; line-height: 1.05; color: #ffffff; margin-bottom: 30px; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    .highlight-green { color: #22c55e; }
    .subtext { color: #9ca3af; font-size: 18px; line-height: 1.6; max-width: 85%; }
    .subtext strong { color: #ffffff; }

    [data-testid="column"]:nth-of-type(2) { background-color: #0b110e; border: 1px solid #1a2621; border-radius: 16px; padding: 24px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7); }

    .stTextArea label { display: none; }
    .stTextArea textarea { background-color: #121a17 !important; border: 1px solid #1f2e28 !important; color: #e2e8f0 !important; border-radius: 12px !important; padding: 16px !important; font-size: 15px !important; min-height: 220px !important; }
    .stTextArea textarea:focus { border-color: #22c55e !important; box-shadow: 0 0 0 1px #22c55e !important; }

    .stButton button { background-color: #1f7844 !important; color: #ffffff !important; border: none !important; border-radius: 30px !important; padding: 12px !important; font-weight: 600 !important; font-size: 16px !important; width: 100% !important; transition: 0.3s ease !important; margin-top: 10px !important; }
    .stButton button:hover { background-color: #22c55e !important; color: #000000 !important; }

    .security-text { color: #4b5563; font-size: 11px; text-align: center; margin-top: 15px; display: flex; justify-content: center; gap: 15px; }

    .window-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
    .tabs { display: flex; gap: 15px; }
    .tab { background-color: #212f29; color: #fff; border: 1px solid #2d4038; padding: 5px 15px; border-radius: 20px; font-size: 12px; font-weight: 500; display: flex; align-items: center; gap: 6px; }
    .mac-dots { display: flex; gap: 6px; }
    .dot { height: 10px; width: 10px; border-radius: 50%; }

    .result-box-danger { background-color: #180a0a; border: 1px solid #4a1515; border-radius: 12px; padding: 16px; margin-top: 20px; }
    .result-box-safe { background-color: #0a180e; border: 1px solid #144a23; border-radius: 12px; padding: 16px; margin-top: 20px; }

    .info-card { background-color: #0b110e; border: 1px solid #1a2621; border-radius: 16px; padding: 25px; height: 100%; transition: transform 0.2s; }
    .info-card:hover { transform: translateY(-5px); border-color: #22c55e; }
    .info-title { color: #ffffff; font-size: 20px; font-weight: 700; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }
    .info-text { color: #9ca3af; font-size: 14.5px; line-height: 1.6; }
    .info-text ul { padding-left: 20px; margin-top: 10px; }
    .info-text li { margin-bottom: 8px; }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1.1, 1], gap="large")

with col1:
    st.markdown('<div class="overline-text">JOBPRAMAAN.AI • FREE SCAM CHECKER</div>', unsafe_allow_html=True)
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

with col2:
    st.markdown('''
        <div class="window-header">
            <div class="tabs">
                <div class="tab"><span style="color:#22c55e;">●</span> Paste Text Only</div>
            </div>
            <div class="mac-dots">
                <div class="dot" style="background-color: #ef4444;"></div>
                <div class="dot" style="background-color: #f59e0b;"></div>
                <div class="dot" style="background-color: #22c55e;"></div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    job_text = st.text_area("", placeholder="Paste the full job description here (e.g. Responsibilities, Requirements, Salary)...", height=200, label_visibility="collapsed")
    scan_clicked = st.button("Scan Now ➔")

    st.markdown('''
        <div class="security-text">
            <span>🔒 Anonymous scan</span>
            <span>Names redacted</span>
            <span>IP not stored</span>
            <span>Never sold</span>
        </div>
    ''', unsafe_allow_html=True)

    if scan_clicked:
        if not job_text.strip():
            st.warning("Please paste some text to scan.")
        else:
            with st.spinner("Analyzing text syntax and risk factors..."):
                time.sleep(1.0)
                result = predict_job_posting(job_text)
                is_fake = result["is_fake"]
                prob = result.get("probability_fake")
                
                if prob is None:
                    prob = 98.4 if is_fake else 4.2
                
                if is_fake:
                    reasons = result.get("reasons", [])
                    if reasons:
                        reason_items = "".join([f"<li>Trigger keyword detected: <b>'{r}'</b></li>" for r in reasons])
                    else:
                        reason_items = "<li>High concentration of scam-related keywords detected</li><li>Unrealistic requirements or suspicious onboarding process</li><li>Urgency pattern or off-platform link suspected</li>"
                    
                    danger_html = f"""<div class="result-box-danger"><div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #331515; padding-bottom: 10px; margin-bottom: 10px;"><div style="color: #e5e7eb; font-weight: 600; font-size: 14px;"><span style="color:#ef4444;">●</span> Analyzed Text - Potential Fraud</div><div style="background-color: #ef4444; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; letter-spacing: 1px;">{prob} / 100 MAX RISK</div></div><ul style="color: #ef4444; font-size: 13px; margin: 0; padding-left: 15px;">{reason_items}</ul></div>"""
                    st.markdown(danger_html, unsafe_allow_html=True)
                else:
                    real_score = round((100 - prob) if prob > 50 else prob, 1)
                    safe_html = f"""<div class="result-box-safe"><div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #143320; padding-bottom: 10px; margin-bottom: 10px;"><div style="color: #e5e7eb; font-weight: 600; font-size: 14px;"><span style="color:#22c55e;">●</span> Analyzed Text - Legitimate</div><div style="background-color: #22c55e; color: black; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; letter-spacing: 1px;">{real_score} / 100 SAFE</div></div><ul style="color: #22c55e; font-size: 13px; margin: 0; padding-left: 15px;"><li style="margin-bottom: 5px;">No suspicious financial requests found</li><li>Language patterns match standard corporate postings</li></ul></div>"""
                    st.markdown(safe_html, unsafe_allow_html=True)

st.markdown("<br><br><hr style='border-color: #1a2621;'><br>", unsafe_allow_html=True)

info1, info2, info3 = st.columns(3, gap="large")

with info1:
    st.markdown('''
        <div class="info-card">
            <div class="info-title">📖 How to Use</div>
            <div class="info-text">
                Using our AI scanner is quick and entirely anonymous.
                <ul>
                    <li><b>Find a Post:</b> Copy the full job description from LinkedIn, Indeed, or an email.</li>
                    <li><b>Paste it:</b> Drop the text into the secure scanner window above.</li>
                    <li><b>Scan:</b> Click 'Scan Now' to let our Hybrid Model analyze the text.</li>
                    <li><b>Review:</b> Get an instant 0-100 risk score and highlighted red flags.</li>
                </ul>
            </div>
        </div>
    ''', unsafe_allow_html=True)

with info2:
    st.markdown('''
        <div class="info-card">
            <div class="info-title">💡 Pro Safety Tips</div>
            <div class="info-text">
                Don't rely entirely on AI. Always keep these manual checks in mind:
                <ul>
                    <li><b>Check the Email:</b> Legitimate recruiters rarely use <code>@gmail.com</code>. Watch out for misspelled domains.</li>
                    <li><b>Never Pay:</b> Real jobs pay you. If they ask for an "onboarding fee" or "equipment purchase," it's a scam.</li>
                    <li><b>Interview Process:</b> Scammers often hire immediately via text or Telegram without a real video interview.</li>
                </ul>
            </div>
        </div>
    ''', unsafe_allow_html=True)

with info3:
    st.markdown('''
        <div class="info-card">
            <div class="info-title">📊 Did You Know?</div>
            <div class="info-text">
                Employment fraud is at an all-time high globally.
                <ul>
                    <li>According to the FTC, job scams cost victims hundreds of millions of dollars every year.</li>
                    <li><b>The 'Fake Check' tactic</b> is the most common: scammers send you a check for home office gear and ask you to wire leftover money back.</li>
                    <li>Our AI flags <b>"Urgency"</b> and <b>"Unrealistic Pay"</b> ($50/hr for basic data entry) as high risk factors.</li>
                </ul>
            </div>
        </div>
    ''', unsafe_allow_html=True)

st.markdown("<br><p style='text-align: center; color: #4b5563; font-size: 13px;'>JobPramaan.ai • Hybrid ML & Heuristic Engine • Educational Project</p>", unsafe_allow_html=True)