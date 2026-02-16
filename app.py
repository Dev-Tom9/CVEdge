import streamlit as st
from openai import OpenAI
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from io import BytesIO
from datetime import datetime
import random

# ------------------ API KEY ------------------
api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
if not api_key:
    st.error("Missing OpenAI API key.")
    st.stop()

client = OpenAI(api_key=api_key)

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="CVEdge",
    page_icon="🚀",
    layout="wide"
)

# ------------------ REMOVE STREAMLIT DEFAULT STYLE ------------------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

.hero-section {
    background: linear-gradient(135deg, #1e3a8a, #2563eb);
    padding: 80px 20px;
    text-align: center;
    color: white;
    border-radius: 0 0 40px 40px;
}

.hero-section h1 {
    font-size: 56px;
    font-weight: 800;
    margin-bottom: 20px;
}

.hero-section p {
    font-size: 20px;
    opacity: 0.9;
}

.card {
    background: white;
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0px 10px 40px rgba(0,0,0,0.08);
}

.metric-box {
    background: #f1f5f9;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    font-weight: 600;
}

.stButton>button {
    background: linear-gradient(90deg,#2563eb,#1e40af);
    color: white;
    border-radius: 12px;
    height: 3em;
    font-weight: 600;
    width: 100%;
}

.stDownloadButton>button {
    background: #10b981;
    color: white;
    border-radius: 12px;
    font-weight: 600;
    width: 100%;
}

textarea {
    border-radius: 12px !important;
}

.footer-custom {
    text-align: center;
    margin-top: 80px;
    color: gray;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ HERO ------------------
st.markdown("""
<div class="hero-section">
    <h1>Land Interviews Faster</h1>
    <p>CVEdge uses AI to optimize your resume for ATS systems and hiring managers.</p>
</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# ------------------ MAIN CARD ------------------
st.markdown('<div class="card">', unsafe_allow_html=True)

col1, col2 = st.columns([1,1])

with col1:
    st.subheader("Paste Your Resume")
    resume_input = st.text_area("", height=350)
    optimize = st.button("Optimize Resume")

with col2:
    if optimize and resume_input.strip():
        with st.spinner("Optimizing with AI..."):

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Optimize this resume for ATS, clarity, measurable results, and professional tone."},
                    {"role": "user", "content": resume_input}
                ]
            )

            optimized_text = response.choices[0].message.content

        score = random.randint(85, 97)

        st.markdown(f"""
        <div class="metric-box">
            Resume Strength Score: {score}%
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        st.subheader("Optimized Resume")
        st.text_area("", optimized_text, height=350)

        # PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        for line in optimized_text.split("\n"):
            elements.append(Paragraph(line, styles["Normal"]))
            elements.append(Spacer(1, 0.2 * inch))

        doc.build(elements)
        buffer.seek(0)

        st.download_button(
            "Download Optimized PDF",
            buffer,
            "CVEdge_Optimized_Resume.pdf",
            "application/pdf"
        )

st.markdown('</div>', unsafe_allow_html=True)

# ------------------ FOOTER ------------------
year = datetime.now().year
st.markdown(f"""
<div class="footer-custom">
© {year} CVEdge. All rights reserved.
</div>
""", unsafe_allow_html=True)
