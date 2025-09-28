import os
import fitz  # PyMuPDF
import pptx
import requests
import time

from openai import OpenAI
from serpapi import GoogleSearch

# Load API keys from environment
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

# Set up OpenRouter client
client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# Extract text from PDF
def extract_text_from_pdf(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Extract text from PPTX
def extract_text_from_pptx(path):
    prs = pptx.Presentation(path)
    text = ""
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text += shape.text + "\n"
    return text

# Optional: Use SerpAPI to enrich with company web info
def web_search_company_info(query, num_results=5):
    if not SERPAPI_API_KEY:
        return "No SERPAPI API key provided."

    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "num": num_results
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    snippets = []
    for res in results.get("organic_results", []):
        snippet = res.get("snippet", "")
        if snippet:
            snippets.append(snippet)

    return "\n".join(snippets)

# Use OpenRouter (ChatGPT or Claude) to generate a markdown summary
def summarize_with_ai(extracted_text, extra_context=""):
    print("[INFO] Sending data to OpenRouter for summarization...")

    SYSTEM_PROMPT = (
        "You are an analyst assistant for an early-stage VC investor. "
        "Given a pitch deck (text), generate a structured summary of the company "
        "as if preparing for an investment committee. Be concise but informative. "
        "Include: company name, website, founding team, product, traction, business model, market size, competitors, and risks. "
        "You can also include any helpful information from web search if available."
    )

    full_input = extracted_text + "\n\n" + extra_context

    response = client.chat.completions.create(
        model="openai/gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": full_input}
        ]
    )

    return response.choices[0].message.content
