
# R=2 max-fiber control (W52-M1)

## Status
EXPERIMENTAL. **Rung: PROVED-SPECIAL** (fixed m); density regime **REDUCED** open.

## Phase 0
cube3 E=216, Delta=27/64.

## Lemma (R=2, any m>=2) — PROVED
By induction fixing one ground element: every fiber of Phi=(sum,sumsq) satisfies
f_s <= N^{m-2} (and f_s <= 1 for m=2). Line-checkable; no energy hypothesis needed.

## Corollary (fixed m)
If m is fixed and barN >= 1, log(max_f/barN)/N <= (m-2) log N / N -> 0.
Reduced C9 input holds for R=2 at fixed m.

## REDUCED open (density)
When m = Theta(N), N^{m-2} is useless. Prove low-energy fibers still have
f_s <= exp(o(N)) barN on deep R=2 charts.

## Dual routes
- generator: inductive combinatorial bound + toy enumeration
- checker: re-enum max_f vs N^{m-2}; four-tuple cube3

## Toys
All enumerated toys respect the bound (cert).

## Reproducibility
payload_sha256: f7a54058936e7f462c2f05536bf5656ebf0016c2d7c5a35658cfe39aec0fc5ba
