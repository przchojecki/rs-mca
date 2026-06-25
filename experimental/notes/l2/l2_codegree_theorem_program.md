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

## Step 2 progress (2026-06-25)

**Step 2a — per-`N'` Johnson bound (DONE, verified).**
`verify_l2_punctured_johnson.py` measures the worst-case inner list `L` over
adversarial `(A, U2)` (`A` of size `N'`, random / glued / core-overlap words) and
confirms across **90 `(N',k,a)` checks, 0 violations**:
```
   D(N',k,a) := max_{A,U2} L  ≤  N'(N'-k+1) / (a^2 - N'(k-1))   (when a^2 > N'(k-1)),
   = 1 when a > (N'+k)/2 ;  = 1 at N'=a.
```
Derivation: distinct deg-`<k` codewords agree on `≤ k-1` pts, so the list's
agreement sets are `≥ a`, pairwise `≤ k-1`; the Fisher/Johnson second-moment
inequality gives the bound. (Loose but valid: measured `L` is often `≪` Johnson.)

**Step 2b — the assembly is NOT `|Fib_1|·max D` (the real subtlety).** The Johnson
bound is **vacuous at large `N'`** (the near-capacity prize regime: `a≈k`, `N'≈n`,
so `a^2 < N'(k-1)`). There `D` can be as large as the full base list `|Fib_2|`.
BUT large `N' = |A_1(c_1)|` forces **few such `c_1`**: at `N'=n` (`A_1(c_1)=H`,
`c_1=U_1` a codeword) the row-1 fiber collapses to `|Fib_1|=1`. So the crude
`|Λ_2| ≤ |Fib_1|·max_c D` loses the saving; the correct object is the
**agreement-size-stratified sum**
```
   |Λ_2|  =  Σ_{c_1 ∈ Fib_1} D(|A_1(c_1)|),
```
exploiting the tradeoff "large agreement set ⟹ rare codeword." Bounding this sum
(the agreement-size profile of `Fib_1` against the `N'`-dependent `D`) is the next
increment. The `N'=a` end (`D=1`, many `c_1`) and the `N'=n` end (`D=|Fib_2|`, one
`c_1`) both give small contributions; the interior is the work.

## Milestones (this PR)
1. [x] worst-case punctured-RS-list scanner + measured `D` vs Johnson (step 2a).
2. [ ] the agreement-size-stratified sum `Σ_{c1} D(|A_1(c1)|)` (step 2b) — bound it.
3. [ ] assemble the codegree theorem (qualitative saving), L1-independent, verify.
4. [ ] `μ>2` recursion constants.
5. [ ] (stretch) sharp constant via non-smooth-puncture analysis.
