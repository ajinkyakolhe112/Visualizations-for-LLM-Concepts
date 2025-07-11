from transformers import AutoTokenizer
from langdetect import detect, LangDetectException
from collections import Counter
import argparse
import os
from typing import Dict, List, Tuple
from dataclasses import dataclass
from pathlib import Path

@dataclass
class LanguageStats:
    """Data class to store language detection statistics."""
    total_words: int
    failed_detections: int
    language_counts: Counter
    output_file: str

class TokenizerAnalyzer:
    """A class to handle tokenizer vocabulary analysis and language detection."""
    
    def __init__(self, model_name: str):
        """Initialize the analyzer with a model name."""
        self.model_name = model_name
        self.tokenizer = None
        self.vocab = None
    
    def download_tokenizer(self) -> None:
        """Download and load the tokenizer from Hugging Face."""
        print(f"Downloading tokenizer for {self.model_name}...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.vocab = self.tokenizer.get_vocab()
    
    def save_vocab(self, output_file: str) -> None:
        """Save the vocabulary to a file."""
        if not self.vocab:
            raise ValueError("Tokenizer vocabulary not loaded. Call download_tokenizer() first.")
        
        print(f"Writing vocabulary to {output_file}...")
        sorted_vocab = sorted(self.vocab.items(), key=lambda x: x[1])
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for token, _ in sorted_vocab:
                f.write(f"{token}\n")
        
        print(f"Successfully extracted {len(self.vocab)} tokens to {output_file}")
    
    @staticmethod
    def analyze_languages(input_file: str, output_file: str = "language_summary.txt") -> LanguageStats:
        """Analyze the language distribution in the vocabulary file."""
        language_counts = Counter()
        total_words = 0
        failed_detections = 0
        
        # Count total lines for progress tracking
        total_lines = sum(1 for _ in open(input_file, 'r', encoding='utf-8'))
        print(f"Total lines to process: {total_lines}")
        
        # Process each word
        with open(input_file, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                word = line.strip()
                if not word:
                    continue
                
                total_words += 1
                try:
                    lang = detect(word)
                    language_counts[lang] += 1
                except LangDetectException:
                    failed_detections += 1
                
                if i % 100 == 0:
                    progress = (i / total_lines) * 100
                    print(f"Progress: {progress:.1f}% ({i}/{total_lines} lines processed)")
        
        # Create stats object
        stats = LanguageStats(
            total_words=total_words,
            failed_detections=failed_detections,
            language_counts=language_counts,
            output_file=output_file
        )
        
        # Save and print results
        TokenizerAnalyzer._save_language_stats(stats)
        TokenizerAnalyzer._print_language_stats(stats)
        
        return stats
    
    @staticmethod
    def _save_language_stats(stats: LanguageStats) -> None:
        """Save language statistics to a file."""
        total_detected = sum(stats.language_counts.values())
        detected_percentage = (total_detected / stats.total_words) * 100
        
        with open(stats.output_file, 'w', encoding='utf-8') as f:
            f.write(f"Total words processed: {stats.total_words}\n")
            f.write(f"Failed detections: {stats.failed_detections} "
                   f"({stats.failed_detections/stats.total_words*100:.2f}%)\n\n")
            f.write("Language Distribution:\n")
            f.write("-" * 60 + "\n")
            f.write(f"{'Language':<10} {'Word Count':<15} {'Percentage':<15} {'Running Total':<15}\n")
            f.write("-" * 60 + "\n")
            
            running_word_count = 0
            for lang, count in stats.language_counts.most_common():
                percentage = (count / stats.total_words) * 100
                running_word_count += count
                f.write(f"{lang:<10} {count:<15} {percentage:>6.2f}%{'':<9} {running_word_count:<15}\n")
            
            f.write("-" * 60 + "\n")
            f.write(f"Total detected: {total_detected} words ({detected_percentage:.2f}%)\n")
            f.write(f"Failed detections: {stats.failed_detections} words "
                   f"({stats.failed_detections/stats.total_words*100:.2f}%)\n")
    
    @staticmethod
    def _print_language_stats(stats: LanguageStats) -> None:
        """Print language statistics to console."""
        total_detected = sum(stats.language_counts.values())
        detected_percentage = (total_detected / stats.total_words) * 100
        
        print(f"\nTotal words processed: {stats.total_words}")
        print(f"Failed detections: {stats.failed_detections} "
              f"({stats.failed_detections/stats.total_words*100:.2f}%)")
        print("\nLanguage Distribution:")
        print("-" * 60)
        print(f"{'Language':<10} {'Word Count':<15} {'Percentage':<15} {'Running Total':<15}")
        print("-" * 60)
        
        running_word_count = 0
        for lang, count in stats.language_counts.most_common():
            percentage = (count / stats.total_words) * 100
            running_word_count += count
            print(f"{lang:<10} {count:<15} {percentage:>6.2f}%{'':<9} {running_word_count:<15}")
        
        print("-" * 60)
        print(f"Total detected: {total_detected} words ({detected_percentage:.2f}%)")
        print(f"Failed detections: {stats.failed_detections} words "
              f"({stats.failed_detections/stats.total_words*100:.2f}%)")
        print(f"\nDetailed summary saved to {stats.output_file}")

def main():
    parser = argparse.ArgumentParser(description='Analyze tokenizer vocabulary and detect languages')
    parser.add_argument('--model', type=str, required=True,
                      help='Name of the model/tokenizer on Hugging Face (e.g., bert-base-uncased)')
    parser.add_argument('--output', type=str, default=None,
                      help='Output file name for vocabulary (default: <model_name>_vocab.txt)')
    parser.add_argument('--analyze-only', action='store_true',
                      help='Skip tokenizer download and only analyze existing vocab file')
    parser.add_argument('--input', type=str,
                      help='Input vocabulary file for analysis (required if --analyze-only is set)')
    
    args = parser.parse_args()
    
    if args.analyze_only:
        if not args.input:
            parser.error("--input is required when --analyze-only is set")
        TokenizerAnalyzer.analyze_languages(args.input)
    else:
        if args.output is None:
            model_name = args.model.split('/')[-1]
            args.output = f"{model_name}_vocab.txt"
        
        analyzer = TokenizerAnalyzer(args.model)
        analyzer.download_tokenizer()
        analyzer.save_vocab(args.output)
        analyzer.analyze_languages(args.output)

if __name__ == "__main__":
    main() 