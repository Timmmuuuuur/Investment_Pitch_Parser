import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def get_company_description_from_website(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.content, 'html.parser')
        paragraphs = soup.find_all('p')
        text = "\n".join([p.get_text(strip=True) for p in paragraphs[:10]])
        return text if text.strip() else "No meaningful text found."
    except Exception as e:
        return f"Error fetching site content: {e}"


def get_external_insights(company_name):
    query = f"{company_name} overview site:news.ycombinator.com OR site:techcrunch.com OR site:businessinsider.com"
    search_url = f"https://www.google.com/search?q={quote_plus(query)}"
    return f"[🔍 External news search for {company_name}]({search_url})"


def summarize_with_ai(company_name, website_text):
    if not website_text or "Error" in website_text:
        website_text = f"{company_name} is a company I want you to research based on your training data."

    prompt = f"""
    You are an expert startup analyst. Given the company info below, summarize what the company does, what market it's in, and what makes it interesting to investors.

    Company name: {company_name}

    Website info:
    {website_text}

    Return 3 paragraphs: 1) Overview of what the company does, 2) Key differentiators and competitors, 3) What questions a VC should ask.
    """

    response = client.chat.completions.create(
        model="openai/gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()


def enrich_company_data(company_name, company_url):
    website_text = get_company_description_from_website(company_url)
    ai_summary = summarize_with_ai(company_name, website_text)
    external_links = get_external_insights(company_name)

    return f"""
## 🔍 External Enrichment Summary

### 🧠 AI Analysis of Brand
{ai_summary}

### 🌐 Website
{company_url}

### 📰 External Insights
{external_links}
"""