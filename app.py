import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from io import BytesIO
from datetime import datetime

load_dotenv()

# Initialize OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(
    page_title="CVEdge - AI Resume Optimizer",
    page_icon="📄",
    layout="wide"
)

# Custom Blue SaaS Styling
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
        }
        .stDownloadButton>button {
            background-color: #10b981;
            color: white;
            border-radius: 8px;
        }
        footer {
            text-align: center;
            padding: 20px;
            font-size: 14px;
            color: gray;
        }
    </style>
""", unsafe_allow_html=True)

# Hero Section
st.title("Upgrade Your Resume With AI Precision")
st.write("Instant ATS optimization. Stronger impact. More interviews.")

st.divider()

resume_input = st.text_area(
    "Paste Your Resume Below",
    height=250,
    placeholder="Paste your resume here..."
)

if st.button("Optimize Resume"):
    if resume_input.strip() == "":
        st.warning("Please paste your resume first.")
    else:
        with st.spinner("Optimizing your resume..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a professional resume optimizer. Improve resumes for ATS, clarity, measurable impact and structure."},
                    {"role": "user", "content": resume_input}
                ]
            )

            optimized_text = response.choices[0].message.content

            st.success("Resume Optimized Successfully!")

            st.subheader("Optimized Resume")
            st.text_area("", optimized_text, height=300)

            # Generate PDF
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

st.divider()

# Footer
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
