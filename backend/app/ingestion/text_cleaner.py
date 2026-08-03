import re
import unicodedata


def clean_text(text: str) -> str:
    """
    Clean raw extracted PDF text.
    Only responsible for cleaning — does not read PDFs, does not chunk.
    """
    text = _normalize_unicode(text)
    text = _join_broken_words(text)
    text = _remove_page_numbers(text)
    text = _collapse_spaces(text)
    text = _collapse_blank_lines(text)
    return text.strip()


def _normalize_unicode(text: str) -> str:
    return unicodedata.normalize("NFKC", text)


def _join_broken_words(text: str) -> str:
    return re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)


def _remove_page_numbers(text: str) -> str:
    text = re.sub(r"(?m)^\s*Page\s+\d+\s*$", "", text)
    text = re.sub(r"(?m)^\s*\d+\s*$", "", text)
    return text


def _collapse_spaces(text: str) -> str:
    return re.sub(r"[ \t]+", " ", text)


def _collapse_blank_lines(text: str) -> str:
    return re.sub(r"\n{3,}", "\n\n", text)