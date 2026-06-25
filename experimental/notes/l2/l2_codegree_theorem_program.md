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

## Step 2b findings (2026-06-25) — the reduction, and an honest correction

`verify_l2_stratified_sum.py` measured the saving over adversarial `(U1,U2)`:
- The saving is **real and strong**: e.g. `|Fib1|=72, |Fib2|=67` (Cartesian 4824)
  gives interleaved `= 4` — far below even a single fiber.
- **Second moment is insufficient.** Markov/Cauchy–Schwarz hold but are loose; the
  quadratic term of `Σ_x cov_i(x)^2` dominates up to 94% of samples, where CS gives
  only `Cartesian·(k-1)/a` (exponent `2B`, no real saving). So CS cannot prove the
  exponent-`B` saving.

**The right bound (the reduction).** By the codegree decomposition + step 2a,
```
|Λ_2| = Σ_{c2 ∈ Fib_2} (punctured list of U1 on A_2(c2))
      ≤ Σ_{c2} D(|A_2(c2)|)  =  Σ_{N2} M_2(N2) · D(N2),
```
where `M_2(N2) = #{c2 : |A_2(c2)| ≥ N2}` is the **L1 agreement-size profile** and
`D(N2) ≤ N2(N2-k+1)/(a^2-N2(k-1))` is the per-`N'` punctured list (step 2a).

**Honest correction: the saving is NOT L1-independent.** I earlier claimed steps
1–2 were L1-independent; that holds for the *structure* (the decomposition and the
per-`N'` `D` bound), but **not for the saving assembly**. At near-capacity (`a≈k`)
the Johnson bound `D(N2)` is non-vacuous only for `N2 ≲ a²/(k-1) ≈ a`; for all
larger `N2` it is vacuous (`D` up to `|Fib1|`). So controlling `Σ_{N2} M_2(N2)D(N2)`
requires the **profile decay `M_2(N2)`** — i.e. the L1 / `prob:perfiber` input.
The L2 saving therefore **reduces to** (i) the punctured-RS Johnson bound
(L1-independent, done) + (ii) the L1 agreement-size profile. This is a clean,
named reduction — `L2 saving ⟸ L1 profile + punctured-RS Johnson` — even though
it is not the L1-free result I first hoped for.

## The two-regime reduction theorem (2026-06-25) — the landable result

> **Theorem (L2 codegree, two-regime; PROVED, verified).** For `C=RS[F,H,k]`,
> `a=k+σ`, and any 2-row word `U=(U_1,U_2)`,
> ```
> |Λ_2(U,a)|  ≤  |Fib_2|  +  M_2(2a-k) · |Fib_1|,
> ```
> and symmetrically with `1↔2`, where `Fib_i = {c : |A_i(c)| ≥ a}` and
> `M_i(s) = #{c ∈ Fib_i : |A_i(c)| ≥ s}`. Here `2a-k = a+σ`.

*Proof.* Codegree decomposition: `|Λ_2| = Σ_{c2∈Fib_2} (#{c1 : |A_1(c1)∩A_2(c2)| ≥ a})`.
The inner count is the punctured-RS list of `U_1` on `A_2(c2)` (`N2:=|A_2(c2)|`
points). **Unique-decoding regime:** if `N2 < 2a-k` then `a > (N2+k)/2`, so a
degree-`<k` poly agreeing with `U_1` on `≥a > (N2+k)/2` of the `N2` points is
unique — inner count `≤ 1`. **Tail regime:** if `N2 ≥ 2a-k`, bound the inner count
trivially by `|Fib_1|`. Summing: `|Λ_2| ≤ (#c2 with N2<2a-k)·1 + (#c2 with
N2≥2a-k)·|Fib_1| ≤ |Fib_2| + M_2(2a-k)|Fib_1|`. ∎

**The theorem is L1-INDEPENDENT** (pure unique-decoding + counting). Verified in
`verify_l2_reduction_bound.py`: the bound holds in 100% of adversarial samples and
is `< Cartesian` (a real saving); e.g. `|Fib1|=22,|Fib2|=25` (Cartesian 550) gives
two-regime `= 25 = |Fib2|` (`M_2`-tail `= 0`).

> **Corollary (saving).** If `M_2(2a-k) ≤ poly(n)` then
> `|Λ_2| ≤ |Fib_2| + poly·|Fib_1| ≤ poly·max(|Fib_1|,|Fib_2|)` — exponent `B`, the
> Cartesian `binom(n,a)^{μ-1}` factor removed.

**The exact remaining input (sharper than `conj:B`).** The saving needs only that
the base list at agreement `2a-k = a+σ` — i.e. **twice the reserve below capacity**
— is polynomial. This is a *higher-agreement* (smaller-radius) list bound than
`conj:B`/L1's list at agreement `a`, so it is **weaker/easier** input: above the
reserve, going `σ` further into the unique-decoding side should make the list drop
from `n^B` toward `poly`. So L2's saving rests on a sharper hypothesis than the
full L1 — a genuine advantage, recovered after the earlier honest correction.

## Milestones (this PR)
1. [x] per-`N'` punctured-RS `D ≤ Johnson` (step 2a).
2. [x] stratified-sum reduction; CS shown insufficient (step 2b).
3. [x] two-regime reduction THEOREM `|Λ_2| ≤ |Fib_2| + M_2(2a-k)|Fib_1|` (proved, verified).
4. [ ] the sharper L1-input: is `M_2(a+σ) ≤ poly` (list at 2×reserve) provable / from L1?
5. [ ] `μ>2` recursion (recurse the decomposition); (stretch) sharp constant.
