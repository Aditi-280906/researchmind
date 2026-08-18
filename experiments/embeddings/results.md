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