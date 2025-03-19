# LLM Tokenizer Visualization

A web-based tool for visualizing and comparing different LLM tokenizers. This tool allows you to:
- Load tokenizers from HuggingFace repositories
- Compare how different models tokenize the same text
- See token counts and visual representations of tokens
- Add custom tokenizers from HuggingFace

## Live Demo
Visit the live demo at: [https://YOUR_USERNAME.github.io/visualizations/](https://YOUR_USERNAME.github.io/visualizations/)

## Features
- Real-time tokenization
- Visual token representation with color coding
- Support for multiple tokenizer models
- Ability to add custom tokenizers
- Local storage for saving preferred models

## Usage
1. Enter text in the input box
2. View how different tokenizers process the text
3. Add new tokenizers using the "Add tokenizer from HuggingFace" button
4. Compare token counts and tokenization patterns across models

## Technical Details
Built using:
- Pure JavaScript
- HuggingFace Transformers.js
- No backend required - runs entirely in the browser 