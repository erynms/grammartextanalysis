#!/usr/bin/env python3
"""
Citation Extraction Script
Extracts author citations and references from grammar texts
"""

import json
import re
from pathlib import Path
from collections import Counter

# Common authors cited in educational texts
NOTABLE_AUTHORS = {
    'shakespeare': 'William Shakespeare',
    'milton': 'John Milton',
    'dickens': 'Charles Dickens',
    'washington': 'George Washington',
    'lincoln': 'Abraham Lincoln',
    'franklin': 'Benjamin Franklin',
    'jefferson': 'Thomas Jefferson',
    'emerson': 'Ralph Waldo Emerson',
    'hawthorne': 'Nathaniel Hawthorne',
    'longfellow': 'Henry Wadsworth Longfellow',
    'whittier': 'John Greenleaf Whittier',
    'lowell': 'James Russell Lowell',
    'holmes': 'Oliver Wendell Holmes',
    'irving': 'Washington Irving',
    'cooper': 'James Fenimore Cooper',
    'poe': 'Edgar Allan Poe',
    'whitman': 'Walt Whitman',
    'tennyson': 'Alfred Tennyson',
    'browning': 'Robert Browning',
    'wordsworth': 'William Wordsworth',
    'byron': 'Lord Byron',
    'shelley': 'Percy Bysshe Shelley',
    'keats': 'John Keats',
    'coleridge': 'Samuel Taylor Coleridge',
    'scott': 'Sir Walter Scott',
    'burns': 'Robert Burns',
    'gray': 'Thomas Gray',
    'pope': 'Alexander Pope',
    'dryden': 'John Dryden',
    'addison': 'Joseph Addison',
    'swift': 'Jonathan Swift',
    'defoe': 'Daniel Defoe',
    'goldsmith': 'Oliver Goldsmith',
    'johnson': 'Samuel Johnson',
    'macaulay': 'Thomas Babington Macaulay',
    'carlyle': 'Thomas Carlyle',
    'ruskin': 'John Ruskin',
    'arnold': 'Matthew Arnold',
    'thackeray': 'William Makepeace Thackeray',
    'eliot': 'George Eliot',
    'austen': 'Jane Austen',
    'bronte': 'Charlotte Bronte',
    'kingsley': 'Charles Kingsley',
    'lamb': 'Charles Lamb',
    'hazlitt': 'William Hazlitt',
    'de quincy': 'Thomas De Quincy',
    'stevenson': 'Robert Louis Stevenson',
    'kipling': 'Rudyard Kipling',
    'webster': 'Daniel Webster',
    'clay': 'Henry Clay',
    'calhoun': 'John C. Calhoun',
    'everett': 'Edward Everett',
    'sumner': 'Charles Sumner',
    'phillips': 'Wendell Phillips',
    'beecher': 'Henry Ward Beecher',
    'cicero': 'Marcus Tullius Cicero',
    'virgil': 'Virgil',
    'homer': 'Homer',
    'horace': 'Horace',
    'plato': 'Plato',
    'aristotle': 'Aristotle',
    'demosthenes': 'Demosthenes',
    'caesar': 'Julius Caesar',
    'thucydides': 'Thucydides',
}

# Our textbook authors to check for cross-citations
TEXTBOOK_AUTHORS = {
    'abbott': 'Edwin Abbott Abbott',
    'armstrong': 'Edward Armstrong',
    'fischer': 'Dorothea Fischer Canfield',
    'canfield': 'Dorothea Fischer Canfield',
    'carpenter': 'George Rice Carpenter',
    'miller': 'Edwin L. Miller',
    'northrop': 'Henry Davenport Northrop',
    'wood': 'T. Wood',
}


def extract_citations(text, author_dict):
    """Extract citations from text"""
    citations = Counter()
    text_lower = text.lower()

    for key, full_name in author_dict.items():
        # Count occurrences (case-insensitive)
        count = len(re.findall(r'\b' + re.escape(key) + r'\b', text_lower))
        if count > 0:
            citations[full_name] = count

    return citations


def analyze_citations(filepath):
    """Analyze citations in a single text file"""
    print(f"Analyzing citations in: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract main text (remove Gutenberg headers)
    start_pattern = r'\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*'
    end_pattern = r'\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*'

    start_match = re.search(start_pattern, content, re.IGNORECASE)
    end_match = re.search(end_pattern, content, re.IGNORECASE)

    if start_match and end_match:
        text = content[start_match.end():end_match.start()]
    else:
        text = content

    # Extract citations
    notable_citations = extract_citations(text, NOTABLE_AUTHORS)
    cross_citations = extract_citations(text, TEXTBOOK_AUTHORS)

    # Get filename
    filename = Path(filepath).stem

    return {
        'filename': filename,
        'notable_authors': dict(notable_citations.most_common(30)),
        'cross_citations': dict(cross_citations),
        'total_notable_citations': sum(notable_citations.values()),
        'total_cross_citations': sum(cross_citations.values())
    }


def main():
    """Main execution function"""
    txt_files = list(Path('.').glob('*.txt'))

    all_citations = []
    all_notable = Counter()
    all_cross = Counter()

    for txt_file in txt_files:
        result = analyze_citations(str(txt_file))
        all_citations.append(result)

        # Aggregate data
        for author, count in result['notable_authors'].items():
            all_notable[author] += count
        for author, count in result['cross_citations'].items():
            all_cross[author] += count

    # Create summary
    summary = {
        'individual_texts': all_citations,
        'corpus_wide': {
            'top_cited_authors': dict(all_notable.most_common(20)),
            'cross_citations': dict(all_cross),
            'total_notable_citations': sum(all_notable.values()),
            'total_cross_citations': sum(all_cross.values()),
            'texts_analyzed': len(txt_files)
        }
    }

    # Save to JSON
    output_file = 'citations_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"\nCitation analysis complete! Results saved to {output_file}")
    print(f"\nTop 10 Cited Authors Across All Texts:")
    for i, (author, count) in enumerate(all_notable.most_common(10), 1):
        print(f"{i}. {author}: {count} mentions")

    print(f"\nCross-citations between textbook authors: {sum(all_cross.values())}")
    if all_cross:
        for author, count in all_cross.items():
            print(f"  - {author}: {count} mentions")
    else:
        print("  None found - texts do not cite each other")


if __name__ == '__main__':
    main()
