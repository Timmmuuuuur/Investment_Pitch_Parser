import os
from dotenv import load_dotenv
from pitch_parser import extract_text_from_pdf, summarize_with_ai
from web_search import enrich_company_data

load_dotenv()

def parse_pitch_deck(input_path: str, output_path: str, company_name: str, company_url: str):
    # 1. Extract text from PDF
    print("[1/4] Extracting text from pitch deck...")
    text = extract_text_from_pdf(input_path)

    # 2. Summarize with AI
    print("[2/4] Generating AI summary...")
    summary_md = summarize_with_ai(text)

    # 3. External enrichment via web + AI
    print("[3/4] Enriching with external web data...")
    enrichment_md = enrich_company_data(company_name, company_url)

    # 4. Combine + write to markdown
    print("[4/4] Writing output...")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# 📊 Investment Pitch Summary\n\n")
        f.write("## 🗂 From the Deck\n")
        f.write(summary_md)
        f.write("\n\n")
        f.write(enrichment_md)

    print(f"\n✅ Done! Output written to: {output_path}")


def main():
    input_file = "data/sample_pitch.pdf"        # Make sure this exists
    output_file = "output/final_summary.md"   # Will be created
    company_name = "OpenAI"                     # You can change this
    company_url = "https://openai.com"          # You can change this

    parse_pitch_deck(input_file, output_file, company_name, company_url)


if __name__ == "__main__":
    main()
