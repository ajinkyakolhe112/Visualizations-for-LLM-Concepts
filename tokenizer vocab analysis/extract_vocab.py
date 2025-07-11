import sys
import os

def extract_vocab_words(input_file):
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found")
        return
    
    try:
        # Create output filename based on input filename
        output_file = os.path.splitext(input_file)[0] + '_words.txt'
        
        # Read input file and write words to output file
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', encoding='utf-8') as outfile:
            
            word_count = 0
            for line in infile:
                # Skip empty lines and lines without quotes
                if not line.strip() or '"' not in line:
                    continue
                
                # Extract word between quotes
                try:
                    # Find the first and last quote in the line
                    start = line.find('"') + 1
                    end = line.rfind('"')
                    if start < end:  # Make sure we found valid quotes
                        word = line[start:end]
                        outfile.write(word + '\n')
                        word_count += 1
                except:
                    continue
        
        print(f"Successfully extracted {word_count} words to {output_file}")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_vocab.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    extract_vocab_words(input_file) 