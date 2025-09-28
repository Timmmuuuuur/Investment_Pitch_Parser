# Investment Pitch Parser

This app parses a startup pitch deck (PDF) and extracts valuable, investor-focused insights using OpenRouter + GPT-4.

## Setup

```bash
pip install -r requirements.txt
export OPENROUTER_API_KEY=your_key_here
```

## Run

```bash
python app/main.py
```

## Input

Put your pitch deck file as `data/sample_pitch.pdf`

## Output

The AI-generated markdown summary will be saved to `data/output.md`
