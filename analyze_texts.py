#!/usr/bin/env python3
"""
Text Analysis Script for Grammar and Composition Books
Performs preprocessing, sentiment analysis, and generates JSON output
"""

import json
import re
import os
from pathlib import Path
from collections import Counter
import statistics

# Try to import nltk, if not available, use basic sentiment analysis
try:
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    from nltk import download
    VADER_AVAILABLE = True
except ImportError:
    VADER_AVAILABLE = False
    print("Warning: NLTK not available. Using basic sentiment analysis.")


class TextAnalyzer:
    def __init__(self):
        if VADER_AVAILABLE:
            try:
                self.sia = SentimentIntensityAnalyzer()
            except:
                # Download VADER lexicon if not available
                download('vader_lexicon', quiet=True)
                self.sia = SentimentIntensityAnalyzer()
        else:
            self.sia = None

    def extract_gutenberg_text(self, content):
        """Extract main text from Project Gutenberg file"""
        # Find start marker
        start_pattern = r'\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*'
        end_pattern = r'\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*'

        start_match = re.search(start_pattern, content, re.IGNORECASE)
        end_match = re.search(end_pattern, content, re.IGNORECASE)

        if start_match and end_match:
            text = content[start_match.end():end_match.start()]
        else:
            # If markers not found, use full content
            text = content

        return text.strip()

    def clean_text(self, text):
        """Clean and normalize text"""
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        # Remove page markers and other artifacts
        text = re.sub(r'\[.*?\]', '', text)
        # Normalize quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        return text.strip()

    def split_into_chunks(self, text, chunk_size=1000):
        """Split text into chunks for analysis"""
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i+chunk_size])
            chunks.append(chunk)
        return chunks

    def analyze_sentiment_vader(self, text):
        """Analyze sentiment using VADER"""
        if self.sia is None:
            return self.analyze_sentiment_basic(text)

        scores = self.sia.polarity_scores(text)
        return {
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu'],
            'compound': scores['compound']
        }

    def analyze_sentiment_basic(self, text):
        """Basic sentiment analysis using word lists"""
        positive_words = set(['good', 'great', 'excellent', 'best', 'better', 'beautiful',
                             'clear', 'correct', 'proper', 'elegant', 'fine', 'perfect',
                             'superior', 'right', 'well', 'pleasing', 'effective'])
        negative_words = set(['bad', 'poor', 'wrong', 'incorrect', 'error', 'fault',
                             'defect', 'awkward', 'confused', 'unclear', 'improper',
                             'inferior', 'weak', 'clumsy', 'harsh'])

        words = re.findall(r'\b\w+\b', text.lower())
        pos_count = sum(1 for w in words if w in positive_words)
        neg_count = sum(1 for w in words if w in negative_words)
        total = len(words)

        if total == 0:
            return {'positive': 0, 'negative': 0, 'neutral': 1, 'compound': 0}

        pos_score = pos_count / total
        neg_score = neg_count / total
        neu_score = 1 - (pos_score + neg_score)
        compound = (pos_count - neg_count) / total if total > 0 else 0

        return {
            'positive': round(pos_score, 3),
            'negative': round(neg_score, 3),
            'neutral': round(neu_score, 3),
            'compound': round(compound, 3)
        }

    def extract_metadata(self, filename):
        """Extract author and title from filename"""
        name = Path(filename).stem
        # Common patterns: "Author Title" or "Author - Title"
        parts = name.split(' - ') if ' - ' in name else [name]

        if len(parts) == 2:
            author, title = parts
        else:
            # Try to split on common keywords
            words = name.split()
            if len(words) > 0:
                author = words[0]
                title = ' '.join(words[1:]) if len(words) > 1 else name
            else:
                author = "Unknown"
                title = name

        return author.strip(), title.strip()

    def analyze_text_statistics(self, text):
        """Calculate various text statistics"""
        # Word count
        words = re.findall(r'\b\w+\b', text.lower())
        word_count = len(words)

        # Unique words
        unique_words = len(set(words))

        # Sentence count (approximate)
        sentences = re.split(r'[.!?]+', text)
        sentence_count = len([s for s in sentences if s.strip()])

        # Average sentence length
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0

        # Most common words (excluding very short words)
        meaningful_words = [w for w in words if len(w) > 3]
        word_freq = Counter(meaningful_words)
        top_words = word_freq.most_common(20)

        # Lexical diversity
        lexical_diversity = unique_words / word_count if word_count > 0 else 0

        return {
            'word_count': word_count,
            'unique_words': unique_words,
            'sentence_count': sentence_count,
            'avg_sentence_length': round(avg_sentence_length, 2),
            'lexical_diversity': round(lexical_diversity, 4),
            'top_words': [{'word': w, 'count': c} for w, c in top_words[:10]]
        }

    def analyze_file(self, filepath):
        """Analyze a single text file"""
        print(f"Analyzing: {filepath}")

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract and clean text
        text = self.extract_gutenberg_text(content)
        text = self.clean_text(text)

        # Extract metadata
        author, title = self.extract_metadata(filepath)

        # Calculate statistics
        stats = self.analyze_text_statistics(text)

        # Analyze sentiment for the whole text
        overall_sentiment = self.analyze_sentiment_vader(text)

        # Split into chunks and analyze sentiment progression
        chunks = self.split_into_chunks(text, chunk_size=2000)
        chunk_sentiments = []

        for i, chunk in enumerate(chunks):
            sentiment = self.analyze_sentiment_vader(chunk)
            chunk_sentiments.append({
                'chunk_index': i,
                'sentiment': sentiment
            })

        # Calculate sentiment statistics
        compound_scores = [cs['sentiment']['compound'] for cs in chunk_sentiments]
        sentiment_stats = {
            'mean_compound': round(statistics.mean(compound_scores), 4) if compound_scores else 0,
            'std_compound': round(statistics.stdev(compound_scores), 4) if len(compound_scores) > 1 else 0,
            'min_compound': round(min(compound_scores), 4) if compound_scores else 0,
            'max_compound': round(max(compound_scores), 4) if compound_scores else 0
        }

        return {
            'filename': os.path.basename(filepath),
            'author': author,
            'title': title,
            'statistics': stats,
            'overall_sentiment': overall_sentiment,
            'sentiment_progression': chunk_sentiments[:50],  # Limit to first 50 chunks
            'sentiment_stats': sentiment_stats
        }

    def analyze_all_files(self, directory='.'):
        """Analyze all text files in directory"""
        txt_files = list(Path(directory).glob('*.txt'))

        results = {
            'analysis_info': {
                'total_files': len(txt_files),
                'analyzer': 'VADER' if VADER_AVAILABLE else 'Basic',
                'description': 'Distant reading analysis of grammar and composition texts'
            },
            'texts': []
        }

        for txt_file in txt_files:
            try:
                analysis = self.analyze_file(str(txt_file))
                results['texts'].append(analysis)
            except Exception as e:
                print(f"Error analyzing {txt_file}: {e}")

        return results


def main():
    """Main execution function"""
    analyzer = TextAnalyzer()

    # Analyze all text files
    results = analyzer.analyze_all_files()

    # Save to JSON
    output_file = 'analysis_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nAnalysis complete! Results saved to {output_file}")
    print(f"Analyzed {len(results['texts'])} texts")

    # Print summary
    for text in results['texts']:
        print(f"\n{text['author']} - {text['title']}")
        print(f"  Words: {text['statistics']['word_count']:,}")
        print(f"  Sentiment (compound): {text['overall_sentiment']['compound']:.3f}")


if __name__ == '__main__':
    main()
