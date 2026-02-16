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

# ----------------------------
# API KEY HANDLING
# ----------------------------
api_key = None

if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]
elif os.getenv("OPENAI_API_KEY"):
    api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("OpenAI API Key not found. Add it in Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="CVEdge - AI Resume Optimizer",
    page_icon="🚀",
    layout="wide"
)

# ----------------------------
# PREMIUM SAAS CSS
# ----------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.hero {
    text-align: center;
    padding: 3rem 1rem;
}

.hero h1 {
    font-size: 48px;
    font-weight: 800;
    background: linear-gradient(90deg, #2563eb, #1e40af);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    font-size: 20px;
    color: #475569;
    margin-top: 1rem;
}

.feature-card {
    background-color: #f8fafc;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
}

.stButton>button {
    background: linear-gradient(90deg,#2563eb,#1e40af);
    color: white;
    border-radius: 10px;
    height: 3em;
    font-weight: 600;
}

.stDownloadButton>button {
    background-color: #10b981;
    color: white;
    border-radius: 10px;
    font-weight: 600;
}

footer {
    text-align: center;
    margin-top: 3rem;
    color: gray;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# HERO SECTION
# ----------------------------
st.markdown("""
<div class="hero">
    <h1>Optimize Your Resume. Get More Interviews.</h1>
    <p>AI-powered ATS optimization designed to increase your hiring success.</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ----------------------------
# FEATURE CARDS
# ----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="feature-card"><h3>⚡ Instant Optimization</h3><p>Rewrite your resume in seconds.</p></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="feature-card"><h3>🎯 ATS Ready</h3><p>Improve keyword matching & structure.</p></div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="feature-card"><h3>📄 PDF Export</h3><p>Download professionally formatted resumes.</p></div>', unsafe_allow_html=True)

st.divider()

# ----------------------------
# MAIN APP SECTION
# ----------------------------
left, right = st.columns([1, 1])

with left:
    st.subheader("Paste Your Resume")
    resume_input = st.text_area(
        "",
        height=300,
        placeholder="Paste your resume here..."
    )
    optimize_button = st.button("Optimize Resume")

with right:
    if optimize_button and resume_input.strip() != "":
        with st.spinner("AI is optimizing your resume..."):

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional resume optimizer. Improve resumes for ATS compatibility, clarity, measurable achievements, and strong action verbs."
                    },
                    {
                        "role": "user",
                        "content": resume_input
                    }
                ]
            )

            optimized_text = response.choices[0].message.content

        st.success("Optimization Complete!")

        # Simulated Resume Score
        score = random.randint(82, 96)
        st.metric("Resume Score", f"{score}%")

        st.subheader("Optimized Resume")
        st.text_area("", optimized_text, height=300)

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
            label="Download PDF",
            data=buffer,
            file_name="CVEdge_Optimized_Resume.pdf",
            mime="application/pdf"
        )

st.divider()

# ----------------------------
# FOOTER
# ----------------------------
current_year = datetime.now().year

st.markdown(
    f"""
    <footer>
        © {current_year} CVEdge. All rights reserved.<br>
        Built with Streamlit + OpenAI
    </footer>
    """,
    unsafe_allow_html=True
)
