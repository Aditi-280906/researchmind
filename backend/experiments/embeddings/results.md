# Embedding Model Comparison

Tested on 50 chunks from attention-is-all-you-need.pdf, on a MacBook Air M2.

| Model      | Dimension | Total Time (50 chunks) | Avg Time/Chunk |
|------------|-----------|-------------------------|-----------------|
| BGE-small  | 384       | 0.660s                  | 17.8ms          |
| E5-small   | 384       | 0.518s                  | 14.0ms          |

## Notes

- Both models happen to output 384-dimensional vectors — this is coincidental,
  not a general rule.
- E5-small was faster in this test, but this measurement includes some
  one-time model overhead and is based on a small sample (50 chunks).
- Speed alone does not indicate retrieval quality. Deciding which model is
  "better" requires an actual retrieval benchmark (real queries with known
  correct answers), which will be done in a later phase — not decided yet.

## Benchmark — Batch Size Scaling (BGE-small, M2)

| Chunks | Time   | Speed         |
|--------|--------|---------------|
| 10     | 0.28s  | 36.3 chunks/sec |
| 100    | 1.41s  | 71.0 chunks/sec |
| 500    | 5.59s  | 89.4 chunks/sec |
| 1000   | 10.76s | 93.0 chunks/sec |

### Observation

Throughput increases with batch size and levels off around ~90-93 chunks/sec.
This is expected: small batches are dominated by fixed model overhead, while
larger batches amortize that cost and benefit from more efficient parallel
processing. Practical takeaway: always embed in batches rather than one chunk
at a time, and expect a full paper (~30-50 chunks) to embed in under a second
on this hardware.