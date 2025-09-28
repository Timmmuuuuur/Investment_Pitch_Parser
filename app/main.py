import os
import sys
from dotenv import load_dotenv
from pitch_parser import extract_text_from_file, extract_company_info, summarize_with_ai
from web_search import enrich_company_data

load_dotenv()

def parse_pitch_deck(input_path: str, output_path: str):
    try:
        # 1. Extract text from pitch deck (auto-detect format)
        print("[1/5] Extracting text from pitch deck...")
        text = extract_text_from_file(input_path)
        
        if not text.strip():
            print("❌ Warning: No text extracted from the pitch deck!")
            return

        # 2. Extract company information from the deck
        print("[2/5] Extracting company information...")
        company_name, company_url = extract_company_info(text)
        
        if not company_name:
            print("❌ Warning: Could not extract company name from pitch deck!")
            company_name = "Unknown Company"
        else:
            print(f"✅ Found company: {company_name}")
            
        if company_url:
            print(f"✅ Found website: {company_url}")
        else:
            print("⚠️  No website found in pitch deck")

        # 3. Summarize with AI
        print("[3/5] Generating AI investment analysis...")
        summary_md = summarize_with_ai(text)

        # 4. External enrichment via web + AI (only if we have company info)
        enrichment_md = ""
        if company_name and company_name != "Unknown Company":
            print("[4/5] Enriching with external web data...")
            enrichment_md = enrich_company_data(company_name, company_url)

        # 5. Combine + write to markdown
        print("[5/5] Writing output...")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("# 📊 Investment Pitch Analysis\n\n")
            f.write(f"**Company:** {company_name}\n")
            if company_url:
                f.write(f"**Website:** {company_url}\n")
            f.write(f"**Source:** {input_path}\n\n")
            f.write("---\n\n")
            f.write("## 📋 Investment Analysis\n\n")
            f.write(summary_md)
            if enrichment_md:
                f.write("\n\n")
                f.write(enrichment_md)

        print(f"\n✅ Done! Investment analysis written to: {output_path}")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


def main():
    # Check if custom input file is provided as command line argument
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = "data/sample_pitch.pdf"
    
    # Check if custom output file is provided as command line argument  
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        output_file = "output/final_summary.md"

    print(f"🚀 Starting pitch deck analysis...")
    print(f"📁 Input: {input_file}")
    print(f"📄 Output: {output_file}")
    print()

    parse_pitch_deck(input_file, output_file)


if __name__ == "__main__":
    main()
