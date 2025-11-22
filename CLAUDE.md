# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A distant reading analysis system for historical grammar and composition texts. The project analyzes six Project Gutenberg texts, performing sentiment analysis, statistical analysis, and providing an interactive web-based visualization interface.

## Commands

### Run Analysis

```bash
python3 analyze_texts.py
```

Processes all `.txt` files in the directory, performs sentiment analysis and text statistics, and generates `analysis_results.json`.

### View Results

```bash
python3 -m http.server 8000
# Then open http://localhost:8000 in browser
```

Or simply open `index.html` directly in a web browser.

### Install Dependencies (Optional)

```bash
pip3 install nltk  # For enhanced VADER sentiment analysis
```

The script works with basic sentiment analysis if NLTK is not available.

## Architecture

### Analysis Pipeline (`analyze_texts.py`)

1. **Text Extraction**: `extract_gutenberg_text()` removes Project Gutenberg headers/footers
2. **Text Cleaning**: `clean_text()` normalizes whitespace, quotes, and removes artifacts
3. **Chunking**: `split_into_chunks()` divides text into 2000-word segments for progression analysis
4. **Sentiment Analysis**:
   - Uses VADER if available (`analyze_sentiment_vader()`)
   - Falls back to basic word-list analysis (`analyze_sentiment_basic()`)
5. **Statistics**: `analyze_text_statistics()` calculates word counts, lexical diversity, etc.
6. **JSON Output**: All results saved to `analysis_results.json`

### Web Interface (`index.html`)

Single-page application with four main sections:
- **Overview**: Summary cards for all texts with basic stats and sentiment bars
- **Individual Texts**: Detailed analysis including sentiment progression charts and word clouds
- **Compare Texts**: Side-by-side comparison of selected texts
- **Statistics**: Corpus-wide statistics and complete data table

Data flows from JSON → JavaScript → Dynamic DOM rendering.

## Key Files

- `analyze_texts.py`: Main analysis script (TextAnalyzer class)
- `analysis_results.json`: Generated analysis data
- `index.html`: Web visualization (HTML/CSS/JavaScript in one file)
- `*.txt`: Six Project Gutenberg source texts
- `README.md`: User documentation

## Data Structure

The JSON output contains:
```
{
  "analysis_info": {...},
  "texts": [
    {
      "filename": "...",
      "author": "...",
      "title": "...",
      "statistics": {word_count, unique_words, sentence_count, avg_sentence_length, lexical_diversity, top_words},
      "overall_sentiment": {positive, negative, neutral, compound},
      "sentiment_progression": [{chunk_index, sentiment}, ...],
      "sentiment_stats": {mean_compound, std_compound, min_compound, max_compound}
    }
  ]
}
```

## Sentiment Analysis

Basic analyzer uses positive/negative word lists. Scores:
- **positive/negative/neutral**: Percentage (0-1)
- **compound**: Overall score (-1 to +1). >0.05 = positive, <-0.05 = negative

If NLTK is installed, uses VADER (Valence Aware Dictionary and sEntiment Reasoner) for more sophisticated analysis.

## Extending the Analysis

To add new analysis features:
1. Add method to `TextAnalyzer` class in `analyze_texts.py`
2. Update JSON output structure in `analyze_file()`
3. Update web interface in `index.html` to display new data
4. Re-run `python3 analyze_texts.py` to regenerate JSON
