import fitz  # PyMuPDF
import markdownify
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def extract_text_from_pdf(path):
    doc = fitz.open(path)
    return " ".join(page.get_text() for page in doc)

def parse_pitch_deck(pdf_path, output_md_path):
    content = extract_text_from_pdf(pdf_path)
    response = client.chat.completions.create(
        model="openai/gpt-4",
        messages=[{"role": "user", "content": f"Summarize this startup pitch deck for an investor: {content}"}]
    )
    result = response.choices[0].message.content
    with open(output_md_path, "w") as f:
        f.write(markdownify.markdownify(result, heading_style="ATX"))
