# Investment Pitch Parser

An AI-powered tool that analyzes startup pitch decks and generates comprehensive investment analysis reports. Built for Investment Managers focusing on early-stage startups.

## 🎯 Key Features

- **🔄 Batch Processing**: Automatically analyzes ALL pitch decks in the `data/` folder
- **📊 Multi-format Support**: PDF and PowerPoint (.pptx, .ppt) pitch decks
- **🤖 Automatic Company Detection**: Extracts company name and website directly from pitch content
- **💼 Investment-Focused Analysis**: Structured reports covering market opportunity, traction, financials, risks, and investment recommendations
- **🌐 Web Enrichment**: Gathers additional company information and competitive insights from the web
- **📝 Professional Output**: Well-structured markdown reports with company-specific filenames
- **⚡ Smart File Handling**: Auto-detects file formats and generates appropriate output names

## 🚀 Quick Start

### Setup
```bash
pip install -r requirements.txt
export OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### Usage Modes

#### 1. Batch Processing (Recommended)
Analyzes ALL pitch decks in the `data/` folder and generates individual reports:
```bash
python3 app/main.py
```
**Output**: `output/final_summary_[company_name].md` for each deck

#### 2. Single File Analysis
```bash
# Analyze specific file (auto-generates company-based output name)
python3 app/main.py path/to/your/pitch.pdf

# Specify both input and output
python3 app/main.py path/to/your/pitch.pptx path/to/custom_output.md
```

## 📁 File Structure & Examples

```
investment_pitch_parser/
├── app/
│   ├── main.py           # Main application entry point
│   ├── pitch_parser.py   # PDF/PPT parsing and AI analysis
│   └── web_search.py     # Web enrichment functionality
├── data/                 # 📂 Put your pitch decks here
│   ├── shopify_pitch.pptx
│   ├── instacart_pitch.pptx
│   └── poparide_pitch.pdf
├── output/               # 📊 Generated analysis reports
│   ├── final_summary_shopify.md
│   ├── final_summary_instacart.md
│   └── final_summary_poparide.md
├── requirements.txt      # Python dependencies
└── README.md
```

## 📋 Analysis Structure

Each generated report includes:

- **Company Overview & Mission**
- **Product/Service Description** 
- **Market Opportunity & Size**
- **Business Model & Revenue Streams**
- **Traction & Key Metrics**
- **Founding Team & Key Personnel**
- **Competitive Landscape**
- **Financial Projections**
- **Investment Ask & Use of Funds**
- **Key Risks & Concerns**
- **Investment Recommendation**
- **External Web Research & Insights**

## 🔧 Supported Formats

- **PDF**: `.pdf` files
- **PowerPoint**: `.pptx` and `.ppt` files
- **Auto-detection**: Automatically determines file type and uses appropriate parser

## 💡 How It Works

1. **📂 File Discovery**: Scans `data/` folder for supported pitch deck formats
2. **🔍 Content Extraction**: Extracts text from PDF or PowerPoint files
3. **🏢 Company Detection**: Uses AI to identify company name and website
4. **📊 Investment Analysis**: Generates comprehensive VC-focused analysis
5. **🌐 Web Enrichment**: Researches company online for additional insights
6. **📝 Report Generation**: Creates professional markdown reports with company-specific names

## 🎯 For Investment Managers

This tool is specifically designed for early-stage VC investors and provides:

- **Due Diligence Ready**: Structured analysis covering all key investment criteria
- **Risk Assessment**: Identifies potential red flags and areas requiring further investigation
- **Market Context**: External research to validate claims and understand competitive landscape
- **Batch Efficiency**: Process multiple decks simultaneously for portfolio reviews
- **Professional Output**: Clean, readable reports suitable for investment committee presentations

## 🔑 API Requirements

- **OpenRouter API Key**: Required for AI analysis (GPT-4)
- **No other paid services**: Complies with cost-conscious development requirements

## 📊 Example Output

Each company gets its own detailed analysis file:
- `final_summary_shopify.md` - Complete investment analysis for Shopify
- `final_summary_instacart.md` - Complete investment analysis for Instacart  
- `final_summary_poparide.md` - Complete investment analysis for Poparide

Perfect for investment committee reviews and due diligence processes!
