from transformers import AutoTokenizer
import argparse
import os

def extract_tokenizer_vocab(model_name, output_file):
    try:
        print(f"Downloading tokenizer for {model_name}...")
        # Download and load the tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Get the vocabulary
        vocab = tokenizer.get_vocab()
        
        # Sort vocabulary by token ID
        sorted_vocab = sorted(vocab.items(), key=lambda x: x[1])
        
        # Write vocabulary to file
        print(f"Writing vocabulary to {output_file}...")
        with open(output_file, 'w', encoding='utf-8') as f:
            for token, token_id in sorted_vocab:
                f.write(f"{token}\n")
        
        print(f"Successfully extracted {len(vocab)} tokens to {output_file}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract vocabulary from a Hugging Face tokenizer')
    parser.add_argument('--model', type=str, required=True,
                      help='Name of the model/tokenizer on Hugging Face (e.g., bert-base-uncased)')
    parser.add_argument('--output', type=str, default=None,
                      help='Output file name (default: <model_name>_vocab.txt)')
    
    args = parser.parse_args()
    
    # If output file is not specified, create one based on model name
    if args.output is None:
        model_name = args.model.split('/')[-1]  # Get the last part of the model name
        args.output = f"{model_name}_vocab.txt"
    
    extract_tokenizer_vocab(args.model, args.output) 