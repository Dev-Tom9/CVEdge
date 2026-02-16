import streamlit as st
from openai import OpenAI
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from io import BytesIO
from datetime import datetime

# -----------------------------
# SAFE API KEY HANDLING
# -----------------------------
api_key = None

# First try Streamlit secrets (production)
if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]

# Fallback to local environment variable (for local testing)
elif os.getenv("OPENAI_API_KEY"):
    api_key = os.getenv("OPENAI_API_KEY")

# If no key found, show error
if not api_key:
    st.error("OpenAI API Key not found. Please add it to Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="CVEdge - AI Resume Optimizer",
    page_icon="📄",
    layout="wide"
)

# -----------------------------
# CUSTOM BLUE SAAS STYLING
# -----------------------------
st.markdown("""
    <style>
        .main {
            background-color: #f4f8ff;
        }
        h1 {
            color: #1e40af;
        }
        .stButton>button {
            background-color: #2563eb;
            color: white;
            border-radius: 8px;
            height: 3em;
            width: 100%;
            font-weight: 600;
        }
        .stDownloadButton>button {
            background-color: #10b981;
            color: white;
            border-radius: 8px;
            font-weight: 600;
        }
        footer {
            text-align: center;
            padding: 30px;
            font-size: 14px;
            color: gray;
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# HERO SECTION
# -----------------------------
st.title("Upgrade Your Resume With AI Precision")
st.write("Instant ATS optimization. Stronger impact. More interviews.")

st.divider()

# -----------------------------
# RESUME INPUT
# -----------------------------
resume_input = st.text_area(
    "Paste Your Resume Below",
    height=250,
    placeholder="Paste your resume here..."
)

# -----------------------------
# OPTIMIZATION LOGIC
# -----------------------------
if st.button("Optimize Resume"):

    if resume_input.strip() == "":
        st.warning("Please paste your resume first.")
    else:
        with st.spinner("Optimizing your resume..."):

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional resume optimizer. Improve resumes for ATS compatibility, clarity, structure, and measurable achievements."
                    },
                    {
                        "role": "user",
                        "content": resume_input
                    }
                ]
            )

            optimized_text = response.choices[0].message.content

        st.success("Resume Optimized Successfully!")

        st.subheader("Optimized Resume")
        st.text_area("", optimized_text, height=300)

        # -----------------------------
        # PDF GENERATION
        # -----------------------------
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
            label="Download Optimized Resume (PDF)",
            data=buffer,
            file_name="CVEdge_Optimized_Resume.pdf",
            mime="application/pdf"
        )

# -----------------------------
# FOOTER
# -----------------------------
st.divider()
current_year = datetime.now().year

st.markdown(
    f"""
    <footer>
        © {current_year} CVEdge. All rights reserved.<br>
        Built with ❤️ using Streamlit + OpenAI
    </footer>
    """,
    unsafe_allow_html=True
)
