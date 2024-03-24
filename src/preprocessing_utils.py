import re


def clear_html(raw_text: str) -> str:
    # Remove HTML tags
    CLEANR = re.compile('<.*?>')
    cleared_text = re.sub(CLEANR, '', raw_text)
    return cleared_text

def clear_links(raw_text: str) -> str:
    # Remove http links
    cleared_text = re.sub(r'^https?:\/\/.*[\r\n]*', '', raw_text, flags=re.MULTILINE)
    return cleared_text

def preprocess_text(raw_text: str) -> str:
    """
    Standard preprocessing steps like lemmatization, stop-words and 
    punctuation removing do not improve the performance of
    transformers, unlike classic ML models.
    That's why we just remove links and html tags, that don't
    carry any information.
    """
    return clear_html(clear_links(raw_text))