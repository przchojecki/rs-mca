# L2 sharp-constant conjecture — falsification log

- **Status:** FALSIFICATION-IN-PROGRESS / EXPERIMENTAL. Running the
  conjecture→falsify→iterate methodology on the L2 sharp-constant interleaved
  conjecture (`l2_interleaved_dilation_constants.md` §2) before any proof attempt.
- **Agent/model:** Claude Opus 4.8 (L2/X1 lane, branch `allen/l2-x1-interleaved-mca`).
- **Date:** 2026-06-24.
- **Conjecture under test:** above the reserve,
  `Lst(Int(C,μ), 1−a/n) ≤ binom(n,a)·q^{−μ(a−k)} + Quot_μ + n^B`, the open piece
  being the aperiodic μ-fold intersection remainder `n^B`.
- **Scanner:** `experimental/scripts/verify_l2_falsify_interleaved.py`.

## Iteration 1–2 (F_17, n=16, k=3, a=5, σ=2)

**Setup fact (used throughout).** The interleaved list at radius `1−a/n` is
`#{(c_1,…,c_μ) : |∩_i A_i(c_i)| ≥ a}`. Since distinct degree-`<k` codewords agree
on `≤ k−1 < a` points, a common agreement support `S` (`|S|≥a`) **pins one
codeword per row**, so each listed tuple is `(interp(U_1,S),…,interp(U_μ,S))` for a
common support `S`. Tuples ↔ common supports.

**Correction to a naive guess.** "interleaved ≤ min base fiber" is **FALSE**: when
one row is an exact codeword (`A_1 = H`), the interleaved list equals the *other*
row's fiber, which exceeds `min_base`. The right quantity to watch is
`max_i |Fib(U_i)|`.

**Decisive question tested:** can interleaving **create mass**, i.e.
`interleaved > max_i |Fib(U_i)|`? (Yes ⟹ L2 has content beyond L1; a super-poly
such remainder would threaten the conjecture. No ⟹ interleaved ≤ a single-row
fiber ≤ L1's poly above the reserve.)

**Adversarial sweep:** exact codeword row; near-codewords; aligned 2-codeword
gluings; **misaligned** gluings (block vs even/odd vs mod-3 partitions — the
construction meant to realize cross pairs); monomial; quotient-periodic; `μ=2,3`.

**Result: NO mass creation.** `interleaved ≤ max_base` in every family. Notable:
- exact-codeword × glued(8-fiber): interleaved `= 8 = max_base` (bounded by the
  larger fiber, as predicted for a codeword row).
- aligned gluings: interleaved `= 2 = max_base` (only the diagonal cross pairs).
- **misaligned gluings: interleaved `= 0`** — distinct-region overlaps fall below
  `a`, so the rows share *no* common support. Misalignment *destroys* the list
  rather than creating cross-mass (the opposite of the naive worry).
- The random-baseline term `binom(n,a)q^{−μ(a−k)} ≈ 0.05` here, so the observed
  mass is entirely the structured/base-fiber part — consistent with `Quot_μ + n^B`.

## Reading (honest)

This is **supporting evidence**, not proof. Across this sweep the interleaved
list is bounded by a single-row base fiber, so above the reserve (base fibers
poly by L1) it would be poly — i.e. **L2's aperiodic remainder looks subsumed by
L1** (`interleaved ≤ max base fiber`). That would both harden the conjecture and
simplify it (reduce L2's open piece to L1). But the sweep is small and
hand-picked; the "create mass" construction tried here self-destructs (overlaps
< a), so it does not yet *rule out* a cleverer cross-mass word.

## Next iterations (planned)

1. **Engineer genuine cross-mass:** partitions whose pairwise cross-regions are
   each `≥ a` (needs `n` larger, or `a` smaller relative to `n`), to actually test
   whether `interleaved > max_base` is achievable at all.
2. **Randomized adversarial search** over many words (not hand-picked), larger
   fields `F_p`, `F_{p^2}`, and rates `ρ ∈ {1/2,1/4,1/8}`; record the worst
   observed `interleaved / max_base`.
3. **Directly test the bound** `interleaved ≤ binom(n,a)q^{−μ(a−k)} + Quot_μ + n^B`
   with the exact `Quot_μ = L_μ(a,τ)` count, hunting a reserve-cleared excess.
4. If `interleaved ≤ max_base` keeps holding, attempt to *prove* it (it would be
   the clean structural statement reducing L2's aperiodic part to L1).

## Reproducibility
```bash
python3 experimental/scripts/verify_l2_falsify_interleaved.py
python3 experimental/scripts/verify_l2_falsify_interleaved.py --json
```
