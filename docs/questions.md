## Observations : attention-is-all-you-need.pdf (body text)

1. Hyphenated words broken across line wraps are preserved literally
   e.g. "transduc-\ntion" instead of "transduction" — will need cleanup
   before chunking/embedding.

2. Line breaks inside paragraphs are just visual line-wrap breaks, not
   real paragraph boundaries. Naive splitting on "\n" would fragment
   sentences incorrectly.

3. Inline citation markers like [35, 2, 5] are embedded directly in
   sentence text — may need to strip/handle separately for clean NLP input.

4. Math notation (subscripts like h_t-1) loses all formatting and
   flattens to plain characters (ht−1) — could cause ambiguity in
   technical term extraction.

## Questions to investigate
- Does PyMuPDF have an option to detect hyphenation and rejoin
  split words automatically?
- Is there a reliable way to distinguish real paragraph breaks from
  line-wrap breaks?
- Should citation markers be stripped before chunking, or kept for
  citation-aware retrieval later?
