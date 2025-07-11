from langdetect import detect, LangDetectException
from collections import Counter
import sys
import os

def detect_word_languages(input_file):
    try:
        # Dictionary to store language counts
        language_counts = Counter()
        total_words = 0
        failed_detections = 0
        
        # Get total number of lines for progress calculation
        with open(input_file, 'r', encoding='utf-8') as f:
            total_lines = sum(1 for _ in f)
        
        print(f"Total lines to process: {total_lines}")
        print("Processing words...")
        
        # Read the input file
        with open(input_file, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                word = line.strip()
                if not word:  # Skip empty lines
                    continue
                
                total_words += 1
                try:
                    # Detect language for the word
                    lang = detect(word)
                    language_counts[lang] += 1
                except LangDetectException:
                    failed_detections += 1
                    continue
                
                # Show progress every 100 words
                if i % 100 == 0:
                    progress = (i / total_lines) * 100
                    print(f"Progress: {progress:.1f}% ({i}/{total_lines} lines processed)")
        
        # Print summary
        print(f"\nTotal words processed: {total_words}")
        print(f"Failed detections: {failed_detections} ({failed_detections/total_words*100:.2f}%)")
        print("\nLanguage Distribution:")
        print("-" * 60)
        print(f"{'Language':<10} {'Word Count':<15} {'Percentage':<15} {'Running Total':<15}")
        print("-" * 60)
        
        # Calculate total detected words and percentage
        total_detected = sum(language_counts.values())
        detected_percentage = (total_detected / total_words) * 100
        
        # Calculate and print percentages
        running_total = 0
        running_word_count = 0
        for lang, count in language_counts.most_common():
            percentage = (count / total_words) * 100
            running_total += percentage
            running_word_count += count
            print(f"{lang:<10} {count:<15} {percentage:>6.2f}%{'':<9} {running_word_count:<15}")
        
        print("-" * 60)
        print(f"Total detected: {total_detected} words ({detected_percentage:.2f}%)")
        print(f"Failed detections: {failed_detections} words ({failed_detections/total_words*100:.2f}%)")
        print(f"Running total: {running_total:.2f}%")
        
        # Save results to file
        output_file = "language_summary.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Total words processed: {total_words}\n")
            f.write(f"Failed detections: {failed_detections} ({failed_detections/total_words*100:.2f}%)\n\n")
            f.write("Language Distribution:\n")
            f.write("-" * 60 + "\n")
            f.write(f"{'Language':<10} {'Word Count':<15} {'Percentage':<15} {'Running Total':<15}\n")
            f.write("-" * 60 + "\n")
            running_word_count = 0
            for lang, count in language_counts.most_common():
                percentage = (count / total_words) * 100
                running_word_count += count
                f.write(f"{lang:<10} {count:<15} {percentage:>6.2f}%{'':<9} {running_word_count:<15}\n")
            f.write("-" * 60 + "\n")
            f.write(f"Total detected: {total_detected} words ({detected_percentage:.2f}%)\n")
            f.write(f"Failed detections: {failed_detections} words ({failed_detections/total_words*100:.2f}%)\n")
            f.write(f"Running total: {running_total:.2f}%\n")
        
        print(f"\nDetailed summary saved to {output_file}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python detect_languages.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    detect_word_languages(input_file) 