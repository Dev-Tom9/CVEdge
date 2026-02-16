import os
from flask import Flask, render_template, request, send_file
from openai import OpenAI
from dotenv import load_dotenv
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from io import BytesIO

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route("/", methods=["GET", "POST"])
def home():
    optimized_text = ""

    if request.method == "POST":
        resume_text = request.form["resume"]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional resume optimizer. Improve resumes for ATS, clarity, impact, and measurable achievements."},
                {"role": "user", "content": resume_text}
            ]
        )

        optimized_text = response.choices[0].message.content

    return render_template("index.html", optimized_text=optimized_text)


@app.route("/download", methods=["POST"])
def download_pdf():
    content = request.form["optimized"]

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    style = styles["Normal"]
    style.fontSize = 11
    style.leading = 14

    for line in content.split("\n"):
        elements.append(Paragraph(line, style))
        elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="CVEdge_Optimized_Resume.pdf", mimetype="application/pdf")


if __name__ == "__main__":
    app.run(debug=True)
