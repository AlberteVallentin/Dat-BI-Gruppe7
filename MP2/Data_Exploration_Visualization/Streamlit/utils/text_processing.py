import re

def summarize_text(text, max_sentences=5):
    """
    Simple text summarization - extracts the first few sentences
    """
    if not text:
        return "No text to summarize."
    
    # Clean the text
    clean_text = re.sub(r'\s+', ' ', text).strip()
    
    # Split into sentences - simple approach
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', clean_text)
    
    # Select first few sentences (simple extractive summarization)
    summary_sentences = sentences[:max_sentences]
    summary = ' '.join(summary_sentences)
    
    return summary