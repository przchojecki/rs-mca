# The star-PTE support micro-lemma: h <= A (not 2h <= A)

- **DAG node:** `h_window_derivation` (the micro-step flagged by
  `h_window_derivation_audit.md` sec 2.3, "HONEST FLAG": the exact
  trade-support bound `h <= A` vs `2h <= A` was unpinned in-repo and
  changes the mid/large-h gap).
- **Status:** PROVED (four-line lemma once the definitions are pinned) +
  arithmetic corrections banked. Roadmap-lane; toy-verified.
- **Verifier:** `experimental/scripts/verify_star_pte_support_bound.py`
  (6/6 PASS: the arithmetic identities, the corrected gap, explicit
  finite-field constructions realising both range endpoints, and the pinned
  certificate).
- **Consumers:** `a_closure_assembly.md` (`H_max`), `w4_direct_column_rewiring.md`
  (the `R_PTE` split-pair column), `w3_chargeable_dictionary_grammar.md`
  (the grammar window), `b_writeup_band_trade_reduction.md`.

## Critical-path role

This packet fixes the size convention for the split-pair/PTE residue that
remains after the paid strip. The conditional prize path needs a polynomial
bound for the remaining split-pair families; this lemma determines the exact
window that bound must cover (`t < h <= A`), and prevents the downstream
compiler from using the false smaller envelope `2h <= A`.

## 0. TL;DR

The star-PTE trade between two list members has half-size `h = A - r`
(`r` = agreement-set overlap), so **`t < h <= A`** and the correct
consumer envelope is **`H_max = A`** (the `h <= A` reading). The `2h <= A`
reading is **wrong**: the trade's `2h`-point support splits across two
different agreement sets, so `2h` ranges up to `2A`, not `A`. Pinning this
**widens** the declared mid/large-h gap to `(100, A]` — matching the
window audit's post-dichotomy `H_max := A` decision.

## 1. Definitions (pinned)

A **list member** is a codeword `c_f` = evaluation of a degree-`< k`
polynomial `f`, and its **exact-agreement set** `S_f` is the set of
positions where the received word `y` equals `c_f`. On the safe side of a
clean-rate row the list members sit at the agreement number
`|S_f| = A = k + t` (`A` banked; `qa22_staircase_budget_column.md` line 10).

For two distinct members `c_f, c_g` the **canonical star-PTE trade** is the
symmetric difference of their agreement sets:

```text
P := S_f \ S_g,     Q := S_g \ S_f,     r := |S_f cap S_g|,
h := |P| = |Q| = A - r    (half-size),
support := |P u Q| = 2h = 2(A - r).
```

`P, Q` are the varying parts after the common core `S_f cap S_g` is
removed; they are exactly the two sides of the moment/PTE trade routed to
`R_PTE` (`w4_direct_column_rewiring.md`, `b_writeup_band_trade_reduction.md`
exit 3). This is the "split-pair" object of the split-pair census
(`sp_census_split_pair_census.md`) and the anchored-core reduction: the
anchored core is `S_f cap S_g`, the trade is `(P, Q)`.

## 2. The micro-lemma (four lines)

**Lemma (star-PTE support size).** With the definitions above,

```text
t  <  h  <=  A ,      and      2t  <  support = 2h  <=  2A .
```

*Proof.*
1. On `S_f cap S_g` both codewords equal `y`, hence equal each other; two
   distinct degree-`< k` polynomials agree in at most `k-1` points
   (`f - g != 0` has degree `< k`, so `< k` roots). Thus `r <= k-1`.
2. Therefore `h = A - r >= A - (k-1) = (k+t) - k + 1 = t+1`, i.e. `h > t`.
3. `r >= 0` gives `h = A - r <= A`, with equality **iff** `S_f cap S_g` is
   empty (`r = 0`); `h = A` is realisable (Verifier, r=0 construction).
4. The support is `P u Q` with `P subset S_f`, `Q subset S_g` in **two
   different** size-`A` agreement sets, so `support = 2h = 2(A - r)` runs
   over `(2t, 2A]`; it is **not** bounded by `A`. ∎

**Corollary (which reading the consumers use).** The rigorous a-priori
envelope on the trade half-size fed to `R_PTE` is `h <= A` — the
`h <= A` reading. The `2h <= A` reading is incorrect: it presumes the
whole `2h`-point support lies inside a single size-`A` agreement set,
which is false because `P` and `Q` lie in `S_f` and `S_g` respectively.
Hence **`H_max = A`**, not `floor(A/2)`.

Both boundary cases are realised over a finite field in the verifier:
`r = 0` gives `h = A` with support `2A > A` (killing the `2h <= A`
reading), and `r = k-1` gives the minimal trade `h = t+1`.

## 3. Corrected H_max per rate (n = 1024)

```text
rate    k     t    A = k+t    H_max = A    h-range [t+1, A]    support [2t+2, 2A]
1/4     256   5    261        261          [6, 261]            [12, 522]
1/8     128   5    133        133          [6, 133]            [12, 266]
1/16    64    3    67         67           [4, 67]             [8, 134]
```

This is exactly the `a_closure_assembly.md` repoint `H_max := A`
(Row-C: 261/133/67) mandated by `h_window_derivation_audit.md` sec 4.
The prize rows have `t >> (log2 n)^2 = 1681`, so their small-block window
is empty and the whole small-window lane is vacuous there (giant blocks
are U2-C's job).

## 4. The corrected mid/large-h gap

The frozen W3 v1 grammar charges only `t < h <= (log2 n)^2 = 100`
(`w3_chargeable_dictionary_grammar.md`). The uncovered accounting hole
between the grammar cap and the true envelope `A` is:

```text
reading          rate 1/4        rate 1/8        rate 1/16
h <= A (CORRECT)  (100, 261]      (100, 133]      empty (A = 67 < 100)
2h <= A (WRONG)   (100, 130]      empty           empty
```

So pinning the lemma **widens** the declared gap: the honest hole is
`(100, 261]` at rate 1/4 (161 sizes) and `(100, 133]` at rate 1/8
(33 sizes); rate 1/16 has no gap (`A = 67 < 100`). Under the mistaken
`2h <= A` reading the hole would have looked like only `(100, 130]` at
rate 1/4 (31 sizes) with rate 1/8 clean — a false comfort. The wider,
correct gap is what blocker 3 of the critical path
(`critical_path_status_2026_07_04.md`) must cover, via resolution (i):
extend the (C1) certificates to `h <= A` (A3 + X24 apply verbatim at every
`h`; `h_window_derivation_audit.md` sec 3.2, 4).

## 5. Verification

```bash
python3 experimental/scripts/verify_star_pte_support_bound.py
```

Checks: (1) the `A = k+t` identities and the `[t+1, A]` / `[2t+2, 2A]`
ranges at all three rates; (2) the corrected gap `(100, A]` vs the wrong
`(100, floor(A/2)]`; (3) distinct degree-`< k` codewords agree in `<= k-1`
points (randomised); (4) an explicit `F_101` construction with `r = 0`
giving `h = A`, `support = 2A > A`; (5) an `F_101` construction with
`r = k-1` giving the minimal trade `h = t+1`; (6) the pinned JSON
certificate in `experimental/data/certificates/star-pte-support-bound/`.
Current run **6/6 PASS**.
