# Chunking — ResearchMind

## Why chunking?

An LLM can't take an entire research paper as input for every question — it has a
limited context window, and even when a full paper would fit, giving it too much
text at once makes retrieval worse, not better.

So before we can search or answer questions over a paper, we split it into smaller,
self-contained pieces called chunks. Each chunk should represent one coherent idea,
small enough to match a specific question precisely, but large enough to still make
sense on its own without the rest of the paper around it.

Chunking sits right after cleaning and right before embeddings in our pipeline:
PDF → Reader → Cleaner → Chunker → Embeddings → Vector DB → Retrieval → LLM

If chunking is done badly, nothing downstream can fix it — a bad chunk boundary
means the retrieval step will either miss the right answer, or return an answer
without the context needed to understand it.

## Chunking strategies 

There are four common approaches, in increasing order of sophistication:

**1. Fixed-size chunking** — cut every N tokens, no matter what's there.
Simple and fast, but can slice a sentence or even a word in half, destroying
meaning at the cut point.

**2. Paragraph-based chunking** — group whole paragraphs together until reaching
a target size. Respects natural writing boundaries instead of cutting blindly.
This is what we built for our baseline.

**3. Recursive chunking** — tries to split at the largest structural unit first
(section), then paragraph, then sentence, then word — only going smaller when
necessary. A stronger, more structure-aware version of paragraph chunking.

**4. Semantic / structure-aware chunking** — instead of asking "where are N
tokens?", asks "where does the meaning or structure of the document actually
change?" (headings, equations, tables, figures, references). This is where our
future adaptive chunking research will live — not implemented yet.

## Our baseline: ParagraphChunker

For Version 1, we implemented **paragraph-based chunking**:

- Split cleaned text into paragraphs
- Combine consecutive paragraphs until reaching a target token count
- Carry a small overlap of text into the next chunk, so consecutive chunks
  share some context and don't lose meaning at the boundary

### Chosen parameters

- Target chunk size: **400 tokens**
- Overlap: **50 tokens** (~12%)

These are starting values, not final ones — we're deliberately not trying to find
the "best" size yet. We're establishing a reproducible baseline first, so that
later, when we build a more advanced (adaptive) chunker, we can measure whether it
actually performs better than this simple version — and know that any improvement
came from the new strategy, not from accidentally-better parameters.

### Why tokens, not characters

Characters and tokens aren't the same thing — a token is roughly a word or
word-fragment, and LLM context windows and API costs are measured in tokens, not
characters. Counting characters would give a misleading sense of how much content
actually fits in a model's context window. We used a tokenizer (`tiktoken`) to get
real token counts.

## Experiment results (before fallback fix)

| Chunk Size | # Chunks | Avg Tokens | Min | Max |
|---|---|---|---|---|
| 200 | 216 | 679 | 22 | 6901 |
| 400 | 184 | 813 | 42 | 6921 |
| 600 | 165 | 922 | 68 | 6941 |
| 800 | 149 | 1034 | 98 | 6961 |

## Experiment results (after fallback fix)

| Chunk Size | # Chunks | Avg Tokens | Min | Max |
|---|---|---|---|---|
| 200 | 914 | 180 | 37 | 219 |
| 400 | 455 | 353 | 57 | 424 |
| 600 | 313 | 514 | 120 | 606 |
| 800 | 240 | 672 | 109 | 810 |

## Problems observed (manual inspection + experiment data)

- The largest chunk in every experiment run (~6900+ tokens regardless of
  target size) was traced to the References section of
  "attention-is-all-you-need" (chunk_id: attention-is-all-you-need_0018).
  The PDF's reference list has no real paragraph breaks between individual
  citations, so our paragraph-based chunker treats the entire References
  section as a single paragraph and cannot split it further — producing one
  oversized chunk regardless of the configured target size.
- This reveals a limitation of relying purely on `\n\n` as the paragraph
  boundary signal: it works well for prose but fails for densely-packed
  sections like references, which have no blank-line separation.

## What we deliberately did NOT build yet

To keep this baseline clean and reproducible, we're holding off on:

- Semantic chunking with an LLM
- RAPTOR / parent-child retrieval / contextual retrieval
- Adaptive chunking (our eventual research contribution)
- Table-aware or equation-aware chunking
- Using LangChain or LlamaIndex directly

Current implementation is a baseline. Adaptive / structure-aware chunking will
be evaluated later against this baseline** — we're not pretending Version 1 is
our research contribution; it's the yardstick everything else gets measured
against.

## Observed Failure Case

Paragraph-based chunking failed on the References section of
Attention Is All You Need because the extracted PDF text contained
the references as one extremely large paragraph.

## Baseline Mitigation

An oversized-unit fallback splitter was introduced to guarantee
that no chunk exceeds the configured token limit.

## Remaining Limitation

The system still does not understand scientific document structure.
References, equations, tables, captions, and section boundaries are
not yet treated differently.

This motivates future structure-aware/adaptive chunking.