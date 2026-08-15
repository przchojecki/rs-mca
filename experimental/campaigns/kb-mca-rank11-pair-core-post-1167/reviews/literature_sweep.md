# Targeted literature sweep

Date: 2026-08-13

Tool: Exa deep search, 55 returned sources across four queries plus targeted
primary-source fetches.

Frozen question: does the literature supply a worst-case theorem coupling
many distinct minimizing codeword pairs on one special Reed--Solomon received
line, strong enough to improve the cumulative pair/core count at explanation
dimension ten?

Primary sources inspected:

- Brakensiek, Gopi, and Makam, *Generic Reed--Solomon Codes Achieve
  List-Decoding Capacity* (arXiv:2206.05256v4).
- Yu and Loeliger, *Simultaneous Partial Inverses and Decoding Interleaved
  Reed--Solomon Codes* (arXiv:1612.07854).
- Shangguan and Tamo, *Combinatorial List-Decoding of Reed--Solomon Codes
  beyond the Johnson Radius* (arXiv:1911.01502).

The generic-RS result controls higher-order intersections for generic
evaluation sets; the deployed KoalaBear domain is special, so the genericity
hypothesis cannot be imported.  Simultaneous partial inverses concern
algorithmic locator reconstruction under structured error hypotheses, not a
worst-case upper bound for these actual minimizing-pair cores.  The
cycle-space method of Shangguan--Tamo is the closest conceptual neighbor, but
its list-ball dependency does not directly give the required same-line,
chronology-preserving cross-pair collision bound.

Verdict: no external theorem is load-bearing.  The search sharpens the missing
statement to an actual-record cross-pair compatibility/owner lemma; it does
not justify one.  The packet's theorems remain self-contained.
