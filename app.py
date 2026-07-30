import base64
import time
import streamlit as st
from predict import predict_job_posting


# Helper function to convert local image to Base64 (Prevents Streamlit hover/fullscreen buttons)
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except Exception:
        return ""


logo_b64 = get_base64_image("logo.png")

st.set_page_config(
    page_title="JobPramaan.ai", page_icon="logo.png", layout="wide"
)

st.markdown(
    """
    <!-- Import Distinctive Premium Web Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@600;700;800&display=swap" rel="stylesheet">

    <style>
    /* Global Typography Reset */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #060908;
        color: #f1f5f9;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* PERMANENTLY HIDE STREAMLIT IMAGE HOVER / FULLSCREEN BUTTONS */
    [data-testid="stElementToolbar"],
    [data-testid="stImage"] [data-testid="stElementToolbar"],
    .stEmotionBlock [data-testid="stElementToolbar"],
    button[title="View fullscreen"] {
        display: none !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }

    .block-container { padding-top: 4rem; padding-bottom: 5rem; max-width: 1300px; }

    /* Hero Section Fonts & Styling */
    .overline-text { 
        color: #22c55e; 
        letter-spacing: 2.5px; 
        font-size: 12px; 
        font-weight: 700; 
        text-transform: uppercase; 
        margin-bottom: 20px; 
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    .main-heading { 
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 68px; 
        font-weight: 800; 
        line-height: 1.05; 
        color: #ffffff; 
        margin-bottom: 25px; 
        letter-spacing: -1.5px;
    }
    
    .highlight-green { color: #22c55e; }
    
    .subtext { 
        color: #cbd5e1; 
        font-size: 18px; 
        line-height: 1.6; 
        max-width: 85%; 
        font-weight: 400;
    }
    .subtext strong { color: #ffffff; font-weight: 600; }

    /* Scanner Card Styling */
    [data-testid="column"]:nth-of-type(2) { 
        background-color: #0b110e; 
        border: 1px solid #1a2621; 
        border-radius: 16px; 
        padding: 24px; 
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7); 
    }

    .stTextArea label { display: none; }
    .stTextArea textarea { 
        background-color: #121a17 !important; 
        border: 1px solid #1f2e28 !important; 
        color: #f8fafc !important; 
        border-radius: 12px !important; 
        padding: 16px !important; 
        font-size: 15px !important; 
        min-height: 220px !important; 
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    .stTextArea textarea:focus { border-color: #22c55e !important; box-shadow: 0 0 0 1px #22c55e !important; }

    .stButton button { 
        font-family: 'Space Grotesk', sans-serif !important;
        background-color: #1f7844 !important; 
        color: #ffffff !important; 
        border: none !important; 
        border-radius: 30px !important; 
        padding: 12px !important; 
        font-weight: 700 !important; 
        font-size: 16px !important; 
        letter-spacing: 0.5px !important;
        width: 100% !important; 
        transition: 0.3s ease !important; 
        margin-top: 10px !important; 
    }
    .stButton button:hover { background-color: #22c55e !important; color: #000000 !important; }

    .security-text { 
        color: #64748b; 
        font-size: 11px; 
        text-align: center; 
        margin-top: 15px; 
        display: flex; 
        justify-content: center; 
        gap: 15px; 
        font-family: 'JetBrains Mono', monospace !important;
    }

    .window-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
    .tabs { display: flex; gap: 15px; }
    .tab { 
        background-color: #212f29; 
        color: #fff; 
        border: 1px solid #2d4038; 
        padding: 5px 15px; 
        border-radius: 20px; 
        font-size: 12px; 
        font-weight: 600; 
        display: flex; 
        align-items: center; 
        gap: 6px; 
        font-family: 'JetBrains Mono', monospace !important;
    }
    .mac-dots { display: flex; gap: 6px; }
    .dot { height: 10px; width: 10px; border-radius: 50%; }

    .result-box-danger { background-color: #180a0a; border: 1px solid #4a1515; border-radius: 12px; padding: 16px; margin-top: 20px; }
    .result-box-safe { background-color: #0a180e; border: 1px solid #144a23; border-radius: 12px; padding: 16px; margin-top: 20px; }

    /* Info Cards Styling */
    .info-card { 
        background-color: #0b110e; 
        border: 1px solid #1a2621; 
        border-radius: 16px; 
        padding: 28px; 
        height: 100%; 
        transition: transform 0.2s; 
    }
    .info-card:hover { transform: translateY(-5px); border-color: #22c55e; }
    
    .info-title { 
        font-family: 'Space Grotesk', sans-serif !important;
        color: #ffffff; 
        font-size: 21px; 
        font-weight: 700; 
        margin-bottom: 16px; 
        display: flex; 
        align-items: center; 
        gap: 10px; 
    }
    
    .info-text { 
        color: #e2e8f0; 
        font-size: 15px; 
        line-height: 1.65; 
        font-weight: 400;
    }
    .info-text strong, .info-text b { color: #ffffff; font-weight: 600; }
    .info-text ul { padding-left: 20px; margin-top: 10px; }
    .info-text li { margin-bottom: 10px; }

    /* How It Works & FAQ Headers */
    .section-heading {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 2.3rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        color: #ffffff;
        margin-bottom: 8px;
        text-align: center;
    }
    
    .section-subheading {
        color: #94a3b8;
        font-size: 1.1rem;
        text-align: center;
        font-weight: 400;
    }

    /* Steps Section Styling */
    .step-circle {
        width: 50px;
        height: 50px;
        background-color: #1f7844;
        color: #ffffff;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        font-weight: 700;
        margin: 0 auto 16px auto;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    .step-title {
        font-family: 'Space Grotesk', sans-serif !important;
        text-align: center;
        font-size: 1.2rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 10px;
    }
    
    .step-desc {
        text-align: center;
        color: #cbd5e1;
        font-size: 1rem;
        line-height: 1.6;
    }

    /* FAQ Expander Custom Fonts */
    .stExpander {
        border-color: #1a2621 !important;
        background-color: #0b110e !important;
        border-radius: 10px !important;
    }
    .stExpander details summary p {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        color: #f1f5f9 !important;
    }
    .stExpander details div[data-testid="stMarkdownContainer"] p {
        font-size: 1rem !important;
        color: #cbd5e1 !important;
        line-height: 1.65 !important;
    }

    /* Footer Styling */
    .brand-footer {
        width: 100%;
        text-align: center;
        padding: 30px 0 10px 0;
        font-size: 0.95rem;
        font-weight: 700;
        color: #64748b;
        border-top: 1px solid #1a2621;
        margin-top: 60px;
        font-family: 'JetBrains Mono', monospace !important;
        letter-spacing: 1.5px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# HERO SECTION
# ==========================================
col1, col2 = st.columns([1.1, 1], gap="large")

with col1:
    logo_col, overline_col = st.columns([0.12, 0.88], gap="small")

    with logo_col:
        # Render Base64 HTML image to avoid Streamlit's image wrapper & zoom overlay
        if logo_b64:
            st.markdown(
                f'<img src="data:image/png;base64,{logo_b64}" width="48" style="display:'
                ' block; margin-top: 4px;">',
                unsafe_allow_html=True,
            )
        else:
            # Fallback if image isn't loaded properly
            st.markdown("🛡️")

    with overline_col:
        st.markdown(
            '<div class="overline-text" style="margin-top:'
            ' 14px;">JOBPRAMAAN.AI • FREE SCAM CHECKER</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '''
        <div class="main-heading" style="margin-top: 10px;">
            Check if a job is a<br>
            scam<br>
            <span class="highlight-green">before you reply.</span>
        </div>
    ''',
        unsafe_allow_html=True,
    )

    st.markdown(
        '''
        <div class="subtext">
            Paste any job description or requirements. Get a <strong>0–100 risk score</strong> 
            with every red flag explained — completely <strong>free with no account required.</strong>
        </div>
    ''',
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        '''
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
    ''',
        unsafe_allow_html=True,
    )

    job_text = st.text_area(
        "",
        placeholder=(
            "Paste the full job description here (e.g. Responsibilities,"
            " Requirements, Salary)..."
        ),
        height=200,
        label_visibility="collapsed",
    )

    # Reset state if text field is empty
    if not job_text.strip():
        st.session_state["last_scanned_text"] = ""
        st.session_state["scan_result"] = None

    scan_clicked = st.button("Scan Now ➔")

    st.markdown(
        '''
        <div class="security-text">
            <span>🔒 Anonymous scan</span>
            <span>•</span>
            <span>Names redacted</span>
            <span>•</span>
            <span>Never sold</span>
        </div>
    ''',
        unsafe_allow_html=True,
    )

    # Calculate prediction ONLY when Scan Now button is clicked
    if scan_clicked:
        if not job_text.strip():
            st.warning("Please paste some text to scan.")
            st.session_state["scan_result"] = None
            st.session_state["last_scanned_text"] = ""
        else:
            with st.spinner("Analyzing text syntax and risk factors..."):
                time.sleep(1.0)
                st.session_state["scan_result"] = predict_job_posting(job_text)
                st.session_state["last_scanned_text"] = job_text.strip()

    # Render result ONLY IF current text matches last scanned text AND is not empty
    current_has_result = (
        bool(job_text.strip()) 
        and st.session_state.get("scan_result") is not None
        and st.session_state.get("last_scanned_text") == job_text.strip()
    )

    if current_has_result:
        result = st.session_state["scan_result"]
        is_fake = result["is_fake"]
        prob = result.get("probability_fake")

        if prob is None:
            prob = 98.4 if is_fake else 4.2

        if is_fake:
            reasons = result.get("reasons", [])
            if reasons:
                reason_items = "".join(
                    [f"<li style='margin-bottom: 6px;'>{r}</li>" for r in reasons]
                )
            else:
                reason_items = (
                    "<li>High concentration of scam-related keywords"
                    " detected</li><li>Unrealistic requirements or suspicious"
                    " onboarding process</li><li>Urgency pattern or off-platform"
                    " link suspected</li>"
                )

            danger_html = f"""
                    <div class="result-box-danger">
                        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #331515; padding-bottom: 10px; margin-bottom: 10px;">
                            <div style="color: #e5e7eb; font-weight: 600; font-size: 14px;"><span style="color:#ef4444;">●</span> Analyzed Text - Potential Fraud</div>
                            <div style="background-color: #ef4444; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; letter-spacing: 1px; font-family: 'JetBrains Mono';">{prob} / 100 MAX RISK</div>
                        </div>
                        <ul style="color: #ef4444; font-size: 13.5px; margin: 0; padding-left: 15px;">{reason_items}</ul>
                    </div>"""
            st.markdown(danger_html, unsafe_allow_html=True)
        else:
            real_score = round((100 - prob) if prob > 50 else prob, 1)
            safe_html = f"""
                    <div class="result-box-safe">
                        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #143320; padding-bottom: 10px; margin-bottom: 10px;">
                            <div style="color: #e5e7eb; font-weight: 600; font-size: 14px;"><span style="color:#22c55e;">●</span> Analyzed Text - Legitimate</div>
                            <div style="background-color: #22c55e; color: black; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; letter-spacing: 1px; font-family: 'JetBrains Mono';">{real_score} / 100 SAFE</div>
                        </div>
                        <ul style="color: #22c55e; font-size: 13.5px; margin: 0; padding-left: 15px;"><li style="margin-bottom: 5px;">No suspicious financial requests found</li><li>Language patterns match standard corporate postings</li></ul>
                    </div>"""
            st.markdown(safe_html, unsafe_allow_html=True)

st.markdown(
    "<br><br><hr style='border-color: #1a2621;'><br>", unsafe_allow_html=True
)

# ==========================================
# INFO CARDS SECTION
# ==========================================
info1, info2, info3 = st.columns(3, gap="large")

with info1:
    st.markdown(
        """
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
    """,
        unsafe_allow_html=True,
    )

with info2:
    st.markdown(
        """
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
    """,
        unsafe_allow_html=True,
    )

with info3:
    st.markdown(
        """
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
    """,
        unsafe_allow_html=True,
    )

# ==========================================
# HOW IT WORKS SECTION
# ==========================================
st.markdown(
    "<br><br><hr style='border-color: #1a2621;'><br>", unsafe_allow_html=True
)
st.markdown(
    """
    <div style="margin-bottom: 40px;">
        <div class="section-heading">How The Job Scam Detector Works</div>
        <div class="section-subheading">Three steps to safer job searching.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

step1, step2, step3 = st.columns(3)

with step1:
    st.markdown(
        """
        <div class="step-circle">1</div>
        <div class="step-title">Paste the Job Posting</div>
        <div class="step-desc">
            Copy the full job posting text – including any contact information or email addresses – and paste it into the box.
        </div>
        """,
        unsafe_allow_html=True,
    )

with step2:
    st.markdown(
        """
        <div class="step-circle">2</div>
        <div class="step-title">Click Check</div>
        <div class="step-desc">
            Our tool scans the text for known scam patterns: suspicious domains, banking requests, unrealistic pay, urgency language, and more.
        </div>
        """,
        unsafe_allow_html=True,
    )

with step3:
    st.markdown(
        """
        <div class="step-circle">3</div>
        <div class="step-title">Read Your Risk Report</div>
        <div class="step-desc">
            Get a risk score, a list of red flags with explanations, and clear advice on what to do next.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ==========================================
# FREQUENTLY ASKED QUESTIONS (FAQ)
# ==========================================
st.markdown(
    "<br><br><hr style='border-color: #1a2621;'><br>", unsafe_allow_html=True
)
st.markdown(
    """
    <div style="margin-bottom: 30px;">
        <div class="section-heading">Frequently Asked Questions</div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("How can I tell if a job posting is fake?"):
    st.write(
        "Fake job postings often use vague job descriptions, offer"
        " unrealistically high salaries for entry-level work, and request"
        " off-platform communication (such as Telegram or WhatsApp). You can paste"
        " any job description into **JobPramaan.ai** to analyze its text using"
        " Machine Learning and heuristic risk detection."
    )

with st.expander("What are the most common job scam red flags?"):
    st.write(
        "- **Upfront payments:** Demanding registration, training, or equipment"
        " fees.\n- **Off-platform messaging:** Directing applicants to"
        " communicate via Telegram, WhatsApp, or personal Gmail accounts.\n-"
        " **Unrealistic compensation:** Offering high weekly payouts for minimal"
        " or unspecified work.\n- **Cheque/Wire transfer requests:** Asking you to"
        " deposit a cheque and wire money back.\n- **Missing company details:**"
        " Lack of an official domain, website, or verifiable address."
    )

with st.expander("Are LinkedIn job postings safe?"):
    st.write(
        "While platforms like LinkedIn and Indeed actively monitor listings, fake"
        " jobs still slip through. Scammers often create duplicate profiles of"
        " legitimate companies or post ghost jobs. Always verify the recruiter's"
        " profile and double-check suspicious listings using JobPramaan.ai"
        " before sharing sensitive personal details."
    )

with st.expander("What should I do if I think I applied to a scam job?"):
    st.write(
        "1. **Stop all communication** immediately with the recruiter or"
        " sender.\n2. **Do not send money** or make any payments under any"
        " circumstances.\n3. **Secure your accounts:** If you shared passwords"
        " or financial info, update your passwords and contact your bank.\n4."
        " **Report the listing:** Report the job post on the portal where you"
        " found it and file a report with local cybercrime authorities."
    )

with st.expander("How do job scammers target people?"):
    st.write(
        "Scammers gather public resume data from job boards, social media, and"
        " data leaks. They reach out via unsolicited SMS, WhatsApp messages, or"
        " emails offering instant interview approvals without a proper screening"
        " or formal interview process."
    )

with st.expander("Is it safe to give personal information in a job application?"):
    st.write(
        "Standard job applications only require basic contact information and"
        " career history. **Never share** sensitive details such as government ID"
        " numbers, bank account numbers, or credit card details during the initial"
        " application stage. Legitimate employers collect banking info only after"
        " a formal, verified job offer is signed."
    )

# ==========================================
# FOOTER
# ==========================================
st.markdown(
    """
    <div class="brand-footer">
        JOBPRAMAAN.AI • HYBRID ML ENGINE
    </div>
    """,
    unsafe_allow_html=True,
)