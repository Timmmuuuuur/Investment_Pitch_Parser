# Investment Pitch Parser

An AI-powered tool that analyzes startup pitch decks and generates comprehensive investment analysis reports. Built for Investment Managers focusing on early-stage startups.

## Features

- **Multi-format support**: PDF and PowerPoint (.pptx) pitch decks
- **Automatic company detection**: Extracts company name and website from the deck
- **Comprehensive analysis**: Investment-focused analysis including market size, traction, risks, and recommendations
- **Web enrichment**: Gathers additional company information from the web
- **Professional output**: Well-structured markdown reports

## Setup

```bash
pip install -r requirements.txt
export OPENROUTER_API_KEY=your_openrouter_api_key_here
```

## Usage

### Basic usage (uses default sample file):
```bash
python app/main.py
```

### Custom input file:
```bash
python app/main.py path/to/your/pitch.pdf
```

### Custom input and output:
```bash
python app/main.py path/to/your/pitch.pdf path/to/output.md
```

## Supported Formats

- **PDF**: `.pdf` files
- **PowerPoint**: `.pptx` files

## Input

Place your pitch deck file in the `data/` directory or specify the path as a command line argument.

## Output

The AI-generated investment analysis will be saved to `output/final_summary.md` (or your specified output path).

## Project Structure

```
investment_pitch_parser/
├── app/
│   ├── main.py           # Main application entry point
│   ├── pitch_parser.py   # PDF/PPT parsing and AI analysis
│   └── web_search.py     # Web enrichment functionality
├── data/
│   └── sample_pitch.pdf  # Sample pitch deck
├── output/
│   └── final_summary.md  # Generated analysis output
└── requirements.txt      # Python dependencies
```
