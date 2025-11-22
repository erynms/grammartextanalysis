# Grammar Text Analysis - Distant Reading

A comprehensive distant reading analysis system for historical grammar and composition texts. This project preprocesses, analyzes, and visualizes six classic texts on English grammar and composition.

## 📚 Texts Analyzed

1. **Abbott** - How to Write Clearly
2. **Armstrong** - English Grammar
3. **Fischer and Carpenter** - Elementary Composition
4. **Miller** - Practical English
5. **Northrop** - New Century Speaker and Writer
6. **Wood** - Practical Grammar and Composition

## 🎯 Features

- **Text Preprocessing**: Automatic extraction and cleaning of Project Gutenberg texts
- **Sentiment Analysis**: Comprehensive sentiment analysis using positive/negative word matching
- **Statistical Analysis**: Word counts, lexical diversity, sentence analysis, and more
- **Interactive Visualization**: Web-based interface for exploring and comparing texts
- **Sentiment Progression**: Visual representation of how sentiment changes throughout each text
- **Comparative Analysis**: Side-by-side comparison of any two texts

## 🚀 Quick Start

### 1. Run the Analysis

```bash
python3 analyze_texts.py
```

This will:
- Process all `.txt` files in the directory
- Extract and clean the text content
- Perform sentiment analysis
- Generate `analysis_results.json`

### 2. View the Results

Open `index.html` in a web browser:

```bash
# Using Python's built-in server
python3 -m http.server 8000

# Then open http://localhost:8000 in your browser
```

Or simply open `index.html` directly in your browser.

## 📊 Analysis Output

The `analysis_results.json` file contains:

- **Basic Statistics**
  - Word count
  - Unique words
  - Sentence count
  - Average sentence length
  - Lexical diversity

- **Sentiment Analysis**
  - Overall sentiment (positive, neutral, negative, compound)
  - Sentiment progression throughout the text (by chunks)
  - Sentiment statistics (mean, standard deviation, min, max)

- **Word Frequency**
  - Most common words in each text

## 🎨 Web Interface

The interactive web interface provides four main sections:

### Overview
- Quick summary of all texts
- Visual sentiment distribution for each text
- Basic statistics at a glance

### Individual Texts
- Detailed analysis of each text
- Sentiment progression visualization
- Word cloud of most common terms
- Complete statistical breakdown

### Compare Texts
- Side-by-side comparison of any two texts
- Comparative metrics and differences
- Easy-to-read comparison tables

### Statistics
- Corpus-wide statistics
- Comprehensive table of all texts
- Aggregated metrics

## 🛠️ Technical Details

### Python Script (`analyze_texts.py`)

The analysis script includes:

- **TextAnalyzer Class**: Main class for text analysis
- **Gutenberg Text Extraction**: Removes headers and footers from Project Gutenberg texts
- **Text Cleaning**: Normalizes whitespace, quotes, and removes artifacts
- **Sentiment Analysis**: Uses word-based sentiment scoring
- **Statistical Analysis**: Calculates various text metrics
- **Chunking**: Splits texts into manageable chunks for progression analysis

### Web Interface (`index.html`)

Features:
- Responsive design that works on desktop and mobile
- Interactive charts and visualizations
- Dynamic content loading from JSON
- Smooth navigation between sections
- Hover tooltips for detailed information

## 📈 Understanding the Results

### Sentiment Scores

- **Positive**: Percentage of positive words (0-1)
- **Neutral**: Percentage of neutral words (0-1)
- **Negative**: Percentage of negative words (0-1)
- **Compound**: Overall sentiment score (-1 to +1)
  - Positive: > 0.05
  - Neutral: -0.05 to 0.05
  - Negative: < -0.05

### Lexical Diversity

Ratio of unique words to total words. Higher values indicate more varied vocabulary.

## 🔧 Requirements

- Python 3.6+
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Optional: NLTK library for enhanced sentiment analysis

## 📝 Files

- `analyze_texts.py` - Python script for text analysis
- `analysis_results.json` - Generated analysis data
- `index.html` - Web visualization interface
- `*.txt` - Source text files (Project Gutenberg format)
- `README.md` - This file
- `CLAUDE.md` - Development guidance for Claude Code

## 🎓 Use Cases

This project is useful for:

- Digital humanities research
- Comparative literature studies
- Historical linguistics analysis
- Text mining and distant reading
- Educational demonstrations of NLP techniques

## 🤝 Contributing

The analysis can be extended with:
- Additional sentiment analysis methods
- Topic modeling
- Named entity recognition
- Stylometric analysis
- Network analysis of word relationships

## 📄 License

The texts are from Project Gutenberg and are in the public domain. The analysis code is provided as-is for educational and research purposes.

## 🙏 Acknowledgments

- Texts sourced from [Project Gutenberg](https://www.gutenberg.org)
- Analysis inspired by distant reading methodologies
- Visualization designed for accessibility and clarity
