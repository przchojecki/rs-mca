# L2 codegree theorem: proving the interleaved-list saving

- **Status:** PROOF PROGRAM / IN PROGRESS. Step 1 (the codegree decomposition) is
  PROVED + verified (already in `main`); steps 2–3 are the work of this PR.
- **Agent/model:** Claude Opus 4.8 (L2 lane, branch `allen/l2-codegree-theorem`).
- **Date:** 2026-06-25.
- **Goal:** prove the *saving* in the L2 sharp interleaved-list target
  (`l2_sharp_target_conjecture.md`): the worst-case interleaved list near capacity
  is `≤ binom(n,a)q^{−μ(a−k)} + Quot_μ + n^B`, i.e. the interleaving exponent is
  **not** paid as a Cartesian product of row-lists. This is the "codegree theorem"
  named as the open target in `l2_sharp_target_conjecture.md` §5 and PR #107.

## The object

For a `μ`-row received word `U = (U_1,…,U_μ)` over `C = RS[F,H,k]`, the
column-distance interleaved list at radius `1−a/n` is
```
Λ_μ(U,a) = { (c_1,…,c_μ) ∈ C^μ : |{x : c_i(x)=U_i(x) ∀i}| ≥ a }.
```
Write `A_i(c) = {x : c(x)=U_i(x)}` and `Fib_i = {c : |A_i(c)| ≥ a}`. The naive
Cartesian bound is `|Λ_μ| ≤ ∏_i |Fib_i| ≤ (Lst)^μ` (polynomial given L1, but
Cartesian). The target removes the `binom(n,a)^{μ−1}` Cartesian factor.

## Step 1 — codegree decomposition (PROVED, in main)

`verify_l2_codegree_decomposition.py` proves and checks: a tuple `(c_1,c_2)` is
listed iff `c_2` agrees with `U_2` on `≥ a` points **of the set `A_1(c_1)`**.
Hence
```
|Λ_2(U,a)| = Σ_{c_1 ∈ Fib_1} | Λ( RS[F, A_1(c_1), k], 1 − a/|A_1(c_1)|, U_2 ) |,
```
the row-1 fiber summed against the **punctured-RS list** of `U_2` on the domain
`A_1(c_1)` (size `≤ n`). For general `μ` the inner object is the `(μ−1)`-fold
interleaved list on the puncture (recurse). This reduces the saving to a bound on
the inner punctured-RS list.

## Step 2 — bound the inner punctured-RS list (THE CORE WORK OF THIS PR)

Punctured RS is still MDS (puncturing an RS code gives an RS code on the
sub-evaluation-set). So the inner list `Λ(RS[F,A_1(c_1),k], 1−a/N')` with
`N' = |A_1(c_1)|` is RS list-decoding on `N'` points at agreement `a`:
- **unique decoding (`= 1`)** when `a > (N'+k)/2`;
- **Johnson regime** otherwise, list `≤ Johnson(N',k,a)`.

The deliverable: a clean worst-case bound `D(n,k,a) := max_{A_1(c_1)} (inner list)`,
giving
```
|Λ_2(U,a)|  ≤  |Fib_1| · D(n,k,a).
```
**Plan (qualitative-saving-first):**
1. Build a worst-case punctured-list scanner: over adversarial `A_1(c_1)` (sizes
   `a..n`) and `U_2`, measure the max inner punctured-RS list; check it tracks
   the Johnson/unique-decoding prediction (verify before claiming).
2. State and prove the qualitative bound `D ≤ Johnson(n,k,a)` (a known tool;
   the only subtlety is that `A_1(c_1)` is an arbitrary subset, so use the generic
   MDS Johnson bound, not the smooth-domain machinery).
3. Sum over `Fib_1`: `|Λ_2| ≤ min_i|Fib_i| · D` (use either row).

## Step 3 — plug in L1, and the μ>2 recursion

`|Fib_i| ≤ Lst(C,1−a/n) ≤ poly` is L1 (Codex's lane). Plugging in gives the
polynomial saving. **Note:** steps 1–2 are L1-INDEPENDENT — the codegree theorem
is a structural reduction `|Λ_2| ≤ |Fib_1|·D` that holds regardless of L1; L1 only
turns `|Fib_1|` into a polynomial at the end. For `μ>2`, recurse the decomposition
and control the product of `D`'s across rows.

## Honest scope and risks

- **Qualitative vs sharp.** This program targets the *qualitative* saving
  (`|Λ| ≤ |Fib_1|·D`, removing the Cartesian factor) first — plausibly
  prize-sufficient, since the List challenge only needs `|Λ| ≤ 2^{−128}|F|`. The
  **sharp constant** (matching `binom(n,a)q^{−μ(a−k)}` and `Quot_μ` exactly) needs
  list-decoding on the *non-smooth* puncture `A_1(c_1)` beyond generic Johnson —
  flagged as the hard stretch goal, not promised.
- **Composes with M2 bridge.** The new `emca = LD_sw(C,⌈(1−δ)n⌉)/|F|`
  normalization (M2, in main) feeds a list bound into the MCA quantity cleanly.
- **Coordination.** This proves the target Codex named on #107 (their conjecture +
  `Quot_align_μ` budget; my codegree theorem). Composition, not duplication.

## Milestones (this PR)
1. [ ] worst-case punctured-RS-list scanner + measured `D` vs Johnson.
2. [ ] qualitative bound `D ≤ Johnson(n,k,a)` (proved, verified).
3. [ ] assemble `|Λ_2| ≤ |Fib_1|·D` (codegree theorem, qualitative), L1-independent.
4. [ ] `μ>2` recursion constants.
5. [ ] (stretch) sharp constant via non-smooth-puncture analysis.
