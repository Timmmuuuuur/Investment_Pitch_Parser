import os
import sys
import glob
from pathlib import Path
from dotenv import load_dotenv
from pitch_parser import extract_text_from_file, extract_company_info, summarize_with_ai
from web_search import enrich_company_data

load_dotenv()

def parse_pitch_deck(input_path: str, output_path: str):
    try:
        filename = Path(input_path).name
        print(f"\n🔍 Processing: {filename}")
        print("=" * 50)
        
        # 1. Extract text from pitch deck (auto-detect format)
        print("[1/5] Extracting text from pitch deck...")
        text = extract_text_from_file(input_path)
        
        if not text.strip():
            print("❌ Warning: No text extracted from the pitch deck!")
            return None

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

        print(f"✅ Analysis written to: {output_path}")
        return company_name
        
    except FileNotFoundError as e:
        print(f"❌ Error processing {input_path}: {e}")
        return None
    except ValueError as e:
        print(f"❌ Error processing {input_path}: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error processing {input_path}: {e}")
        return None

def find_pitch_decks(data_dir: str):
    """Find all pitch deck files in the data directory"""
    supported_formats = ['*.pdf', '*.pptx', '*.ppt']
    pitch_decks = []
    
    for format_pattern in supported_formats:
        pattern = os.path.join(data_dir, format_pattern)
        pitch_decks.extend(glob.glob(pattern))
    
    return sorted(pitch_decks)

def generate_output_filename(company_name: str, original_filename: str):
    """Generate output filename based on company name"""
    if company_name and company_name != "Unknown Company":
        # Clean company name for filename
        clean_name = "".join(c for c in company_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        clean_name = clean_name.replace(' ', '_').lower()
        return f"final_summary_{clean_name}.md"
    else:
        # Fallback to original filename
        base_name = Path(original_filename).stem
        return f"final_summary_{base_name}.md"

def process_all_pitch_decks(data_dir: str = "data", output_dir: str = "output"):
    """Process all pitch decks in the data directory"""
    pitch_decks = find_pitch_decks(data_dir)
    
    if not pitch_decks:
        print(f"❌ No pitch deck files found in {data_dir}/")
        print("Supported formats: PDF (.pdf), PowerPoint (.pptx, .ppt)")
        return
    
    print(f"🚀 Found {len(pitch_decks)} pitch deck(s) to analyze:")
    for deck in pitch_decks:
        print(f"   📄 {Path(deck).name}")
    print()
    
    processed_count = 0
    failed_count = 0
    
    for pitch_deck in pitch_decks:
        # First pass: extract company name to determine output filename
        try:
            text = extract_text_from_file(pitch_deck)
            company_name, _ = extract_company_info(text)
        except:
            company_name = None
            
        output_filename = generate_output_filename(company_name, Path(pitch_deck).name)
        output_path = os.path.join(output_dir, output_filename)
        
        # Process the pitch deck
        result = parse_pitch_deck(pitch_deck, output_path)
        
        if result is not None:
            processed_count += 1
        else:
            failed_count += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Processing Summary:")
    print(f"   ✅ Successfully processed: {processed_count}")
    print(f"   ❌ Failed: {failed_count}")
    print(f"   📁 Output directory: {output_dir}/")
    
    if processed_count > 0:
        print(f"\n🎉 All analyses complete! Check the {output_dir}/ folder for results.")


def main():
    print("🚀 Investment Pitch Parser")
    print("=" * 50)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        # Single file mode
        input_file = sys.argv[1]
        
        if len(sys.argv) > 2:
            output_file = sys.argv[2]
        else:
            # Generate output filename based on company name
            try:
                text = extract_text_from_file(input_file)
                company_name, _ = extract_company_info(text)
                output_filename = generate_output_filename(company_name, Path(input_file).name)
                output_file = os.path.join("output", output_filename)
            except:
                # Fallback to generic filename
                base_name = Path(input_file).stem
                output_file = f"output/final_summary_{base_name}.md"

        print(f"📁 Single file mode")
        print(f"📄 Input: {input_file}")
        print(f"📄 Output: {output_file}")

        result = parse_pitch_deck(input_file, output_file)
        if result:
            print(f"\n🎉 Analysis complete! Check {output_file}")
        else:
            print(f"\n❌ Failed to process {input_file}")
    else:
        # Batch processing mode - analyze all files in data folder
        print("📁 Batch processing mode - analyzing all pitch decks in data/ folder")
        process_all_pitch_decks()


if __name__ == "__main__":
    main()
