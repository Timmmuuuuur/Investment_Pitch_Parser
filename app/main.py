import os
from pitch_parser import parse_pitch_deck

def main():
    input_file = "../data/sample_pitch.pdf"

    output_file = "../data/output.md"
    parse_pitch_deck(input_file, output_file)

if __name__ == "__main__":
    main()
