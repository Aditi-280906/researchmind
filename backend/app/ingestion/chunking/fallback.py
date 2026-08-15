import re
import tiktoken

_encoder = tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    return len(_encoder.encode(text))


def split_oversized_text(text: str, max_tokens: int, overlap_tokens: int) -> list[str]:
    """
    Fallback splitter for a single paragraph/unit that exceeds max_tokens.
    Strategy:
      1. Split into sentences.
      2. Group sentences until reaching max_tokens.
      3. If a single sentence is still too large, hard-split it by tokens.
    Returns a list of text pieces, each within (or as close as possible to) max_tokens.
    """
    if count_tokens(text) <= max_tokens:
        return [text]

    sentences = _split_into_sentences(text)

    pieces: list[str] = []
    current_sentences: list[str] = []
    current_tokens = 0

    for sentence in sentences:
        sentence_tokens = count_tokens(sentence)

        if sentence_tokens > max_tokens:
            if current_sentences:
                pieces.append(" ".join(current_sentences))
                current_sentences = []
                current_tokens = 0
            pieces.extend(_hard_token_split(sentence, max_tokens, overlap_tokens))
            continue

        if current_sentences and current_tokens + sentence_tokens > max_tokens:
            pieces.append(" ".join(current_sentences))
            overlap_text = _get_overlap(" ".join(current_sentences), overlap_tokens)
            current_sentences = [overlap_text] if overlap_text else []
            current_tokens = count_tokens(overlap_text) if overlap_text else 0

        current_sentences.append(sentence)
        current_tokens += sentence_tokens

    if current_sentences:
        pieces.append(" ".join(current_sentences))

    return pieces


def _split_into_sentences(text: str) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s for s in sentences if s.strip()]


def _hard_token_split(text: str, max_tokens: int, overlap_tokens: int) -> list[str]:
    tokens = _encoder.encode(text)
    pieces = []
    start = 0
    while start < len(tokens):
        end = min(start + max_tokens, len(tokens))
        piece_tokens = tokens[start:end]
        pieces.append(_encoder.decode(piece_tokens))
        if end == len(tokens):
            break
        start = end - overlap_tokens  
    return pieces


def _get_overlap(text: str, overlap_tokens: int) -> str:
    if overlap_tokens <= 0:
        return ""
    tokens = _encoder.encode(text)
    if len(tokens) <= overlap_tokens:
        return text
    return _encoder.decode(tokens[-overlap_tokens:])