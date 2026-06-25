# The L2 codegree reduction theorem (interleaved list → base-code lists)

- **Status:** PROVED + script-verified (the reduction; L1-free). The *saving*
  corollary is CONDITIONAL on a named L1-family input (stated precisely below).
  Self-contained; intended for review / promotion. Does not edit Papers A–D.
- **Agent/model:** Claude Opus 4.8 (L2 lane, branch `allen/l2-codegree-theorem`, PR #108).
- **Date:** 2026-06-25.
- **Scope:** the L2 sharp interleaved-list target
  (`l2_sharp_target_conjecture.md`, Codex PR #107): bound the worst-case
  column-distance interleaved list near capacity without the Cartesian
  `binom(n,a)^{μ-1}` factor. Develops the "codegree theorem" that note names as
  the open proof target.

## 1. Setup and notation

Let `C = RS[F, H, k]` with `H ≤ F^×` a smooth domain of order `n`, rate `ρ=k/n`,
and fix an agreement threshold `a = k+σ` (so radius `1-a/n = 1-ρ-σ/n`). For a
word `V : H → F` and a codeword `c ∈ C` write the **agreement set**
`A_V(c) = {x ∈ H : c(x)=V(x)}`, and the **base fiber / list**
`Fib_V = {c ∈ C : |A_V(c)| ≥ a}`, with the **agreement-size profile**
`M_V(s) = #{c ∈ C : |A_V(c)| ≥ s}`  (so `M_V(a) = |Fib_V|`).

For a `μ`-row word `U=(U_1,…,U_μ)` and `1 ≤ j ≤ μ`, the **`j`-fold interleaved
list at agreement `s`** is
```
Λ_j^{(s)}(U_1,…,U_j) = #{ (c_1,…,c_j) ∈ C^j : |A_{U_1}(c_1) ∩ … ∩ A_{U_j}(c_j)| ≥ s }.
```
`Λ_1^{(s)}(U_1) = M_{U_1}(s)`. The worst-case interleaved list of the target is
`Lst(Int(C,μ),1-a/n) = max_U |Λ_μ^{(a)}(U)|`. The naive Cartesian bound is
`Λ_μ^{(a)} ≤ ∏_i |Fib_{U_i}| ≤ (Lst(C,1-a/n))^μ`.

## 2. Theorem A (codegree decomposition) — PROVED

> A tuple `(c_1,…,c_μ)` is interleaved-listed iff `c_μ` agrees with `U_μ` on `≥a`
> points of the common set `S = ∩_{i<μ} A_{U_i}(c_i)`. Equivalently (μ=2 form):
> ```
> Λ_2^{(a)}(U_1,U_2) = Σ_{c_1 ∈ Fib_{U_1}} | { c_2 ∈ C : |A_{U_1}(c_1) ∩ A_{U_2}(c_2)| ≥ a } |,
> ```
> the row-1 fiber summed against the **punctured-RS list** of `U_2` on `A_{U_1}(c_1)`.

*Proof.* Immediate from the definition of `∩`: the inner condition
`|A_{U_1}(c_1) ∩ A_{U_2}(c_2)| ≥ a` says `c_2` agrees with `U_2` on `≥a` points of
`A_{U_1}(c_1)`; any such `c_2` automatically has `|A_{U_2}(c_2)| ≥ a`. ∎
(Verified: `verify_l2_codegree_decomposition.py`, gluing and non-gluing words.)

## 3. Theorem B (two-regime bound, μ=2) — PROVED, L1-free

> ```
> Λ_2^{(a)}(U_1,U_2)  ≤  |Fib_{U_2}|  +  M_{U_2}(2a-k) · |Fib_{U_1}|,     2a-k = a+σ.
> ```

*Proof.* By Theorem A (symmetric form), `Λ_2^{(a)} = Σ_{c_2 ∈ Fib_{U_2}} L(c_2)`
with `L(c_2) = #{c_1 : |A_{U_1}(c_1) ∩ A_{U_2}(c_2)| ≥ a}` the punctured-RS list of
`U_1` on `A_{U_2}(c_2)` (size `N_2 := |A_{U_2}(c_2)|`).
*Unique-decoding regime:* if `N_2 < 2a-k` then `a > (N_2+k)/2`, so two degree-`<k`
polynomials agreeing with `U_1` on `≥a` of these `N_2` points agree with each other
on `≥ 2a-N_2 > k` points, forcing equality — `L(c_2) ≤ 1`.
*Tail regime:* if `N_2 ≥ 2a-k`, bound `L(c_2) ≤ |Fib_{U_1}|` trivially.
Summing: `Λ_2^{(a)} ≤ (#c_2 with N_2<2a-k)·1 + (#c_2 with N_2≥2a-k)·|Fib_{U_1}|
≤ |Fib_{U_2}| + M_{U_2}(2a-k)|Fib_{U_1}|`. ∎
(Verified: `verify_l2_reduction_bound.py`, holds in 100% of adversarial samples,
bound `< Cartesian`.)

## 4. Theorem C (μ-arity recursion) — PROVED, L1-free; verified μ=3

> ```
> Λ_μ^{(a)}(U_1,…,U_μ)  ≤  Λ_{μ-1}^{(a)}(U_2,…,U_μ)  +  Λ_{μ-1}^{(2a-k)}(U_2,…,U_μ) · |Fib_{U_1}|.
> ```

*Proof.* Peel row 1. For fixed `(c_2,…,c_μ)` put `S = ∩_{i≥2} A_{U_i}(c_i)`; the
listed `c_1` are those agreeing with `U_1` on `≥a` of `S`. If `|S| < 2a-k`, unique
decoding gives `≤1` such `c_1`, and the number of `(c_2,…,c_μ)` with `|S|≥a` is
`Λ_{μ-1}^{(a)}(U_2,…,U_μ)`. If `|S| ≥ 2a-k`, use `≤|Fib_{U_1}|`, and the number of
such tuples is `Λ_{μ-1}^{(2a-k)}(U_2,…,U_μ)`. ∎
For `μ=2`, `Λ_1^{(s)} = M(s)`, recovering Theorem B. (Verified: `verify_l2_mu_recursion.py`,
μ=3 holds in 100% of samples, bound `< Cartesian`, e.g. `|Fib|=(68,70,70)`,
Cartesian `333200`, bound `10`.)

**Unrolled bound.** Recursing Theorem C over the `μ-1` peels expands `Λ_μ^{(a)}`
into a sum over a binary "unique/tail" tree of depth `μ-1`. The all-unique branch
is `Λ_1^{(a)} = |Fib_{U_μ}|` (a *single* base list); every other branch is a
product of one or more `|Fib_{U_i}|` factors with higher-agreement lists
`Λ_j^{(2a-k)}` (`≤ Λ_j^{(a)}` by monotonicity). So `Λ_μ^{(a)}` is controlled by the
base lists `|Fib_{U_i}|` and the higher-agreement lists `Λ_j^{(2a-k)}` — never the
full Cartesian product.

## 5. The saving corollary, and its exact (L1-family) input

> **Corollary (qualitative saving).** Suppose, above the corrected reserve, the
> higher-agreement aperiodic interleaved lists satisfy `Λ_j^{(2a-k)} ≤ poly(n)`
> for `1 ≤ j ≤ μ-1` (the "tail" inputs). Then
> ```
> Λ_μ^{(a)}  ≤  poly(n) · max_i |Fib_{U_i}|  ≤  poly(n) · Lst(C,1-a/n),
> ```
> i.e. exponent `B` (one base-list factor), removing the Cartesian
> `binom(n,a)^{μ-1}`.

**What the input is, honestly.** For `μ=2` the input is `M_{U_2}(2a-k) ≤ poly`,
the base list at agreement `2a-k = a+σ` (twice the reserve below capacity). This
is **not** weaker than L1: `a+σ = k+2σ` is far below the full-code unique-decoding
radius `(n+k)/2`, so it is a list-decoding-regime count; L1 gives only the monotone
`M(a+σ) ≤ M(a) ≤ n^B`, which yields the Cartesian `n^{2B}`, *not* the saving. The
saving needs the list to *drop* to `poly`, which fails for quotient-periodic words
(`U=g(x^M)`): they keep `M(a+σ)=M(a)` (the surviving mass is exactly the
conjecture's `Quot` term). So `Λ_j^{(2a-k)} ≤ poly` is the **L1-family aperiodic
list bound at agreement `2a-k`** — the same kind of input the L1 program
(`prob:perfiber` / `Q_1 ≤ n^B`) and `conj:B` rest on, applied at higher agreement.
(Verified phenomenon: `verify_l2_profile_decay.py`.)

## 6. Status ledger

| Statement | Status |
|---|---|
| Theorem A (codegree decomposition) | **PROVED + verified**, L1-free |
| Theorem B (two-regime, μ=2) | **PROVED + verified**, L1-free |
| Theorem C (μ-recursion) | **PROVED**, L1-free; **verified μ=3** |
| Corollary (saving) | **CONDITIONAL** on `Λ_j^{(2a-k)} ≤ poly` (L1-family input) |
| Sharp constant `binom(n,a)q^{−μ(a−k)}` | OPEN (non-smooth puncture; stretch) |

**Net.** The interleaved list is *reduced*, unconditionally and for all `μ`, to
base-code lists at agreements `a` and `2a-k` — the codegree theorem PR #107 named.
The remaining saving is an L1-family input (aperiodic higher-agreement list `≤ poly`)
that composes with the L1 program; this note does not assume it for the reduction
itself.

## 7. Reproducibility
```bash
python3 experimental/scripts/verify_l2_codegree_decomposition.py   # Theorem A
python3 experimental/scripts/verify_l2_punctured_johnson.py        # per-N' D bound
python3 experimental/scripts/verify_l2_reduction_bound.py          # Theorem B
python3 experimental/scripts/verify_l2_mu_recursion.py             # Theorem C (μ=3)
python3 experimental/scripts/verify_l2_stratified_sum.py           # CS insufficiency
python3 experimental/scripts/verify_l2_profile_decay.py            # the L1-family input
```

## 8. Relation to the L2 conjecture and Codex's `Quot_align_μ`
The two-regime/`μ`-recursion split mirrors `l2_sharp_target_conjecture.md`'s
`binom(n,a)q^{−μ(a−k)} + Quot_align_μ + n^B`: the all-unique branch ↔ the random
baseline `|Fib|`-scale term; the quotient-periodic part of the tail lists `Λ_j^{(2a-k)}`
↔ `Quot_align_μ`; the aperiodic tail ↔ `n^B`. This note supplies the proof
skeleton that conjecture's §5 requested.
