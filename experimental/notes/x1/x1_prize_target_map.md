# X1: the prize-target map — what the two grand challenges still need

- **Status:** STRATEGIC MAP / AUDIT (no new theorem; orients the session's results
  against the exact prize spec). Spec read 2026-06-24 from
  [proximityprize.org](https://proximityprize.org/) (preliminary) + repo `readme.md`.
- **Agent/model:** Claude Opus 4.8 (L2/X1 lane, branch `allen/l2-x1-interleaved-mca`).
- **Date:** 2026-06-24.
- **Purpose:** pin the exact target so the deep-point/confinement/quotient results
  of this session and Codex's `Q_1 ≤ n^B` conjecture (#106) are measured against
  what actually wins the prize. Does not edit Papers A–D.

## The exact prize (both challenges)

For `C = RS[F, L, k]`, `L` smooth of power-of-two order `n`, `ρ = k/n ∈
{1/2, 1/4, 1/8, 1/16}`, **determine the largest threshold `δ*_C`** with:

```text
Grand MCA:            emca(C, δ*_C)            ≤  ε* = 2^-128
Grand List Decoding:  |Λ(C^{≡m}, δ*_C)|        ≤  ε* · |F| = 2^-128 · |F|
                      (C^{≡m} = m-fold INTERLEAVED code, m constant;
                       list divided by the CHALLENGE field |F|)
```
Regime: `ε* = 2^-128`, `k ≤ 2^40`, `|F| < 2^256`. Protocol soundness shape:
`MCA_error + |interleaved_list|/|challenge field| + query_error`. Prize: $1M total,
partial/split allowed, preliminary.

**Two things this corrects in earlier internal notes:**
1. The cap gap is **`2^-9`** (`2^-10` at `ρ=1/16`) — not `2^-7` (that was one
   `cor:deployed` instance). The positive theorem must reach `η ≳ 2^-9`.
2. The list challenge is **interleaved** (`Λ(C^{≡m})`) over the **challenge field**
   — the L2 ledger, not the base-code L1 list.

## Negative side — pinned (done)

Paper D universal cap: `δ*_C(2^-128) ≤ 1−ρ−2^-9` (`2^-10` at `ρ=1/16`) throughout
`|F| < 2^256`; error `> 2^-86` uniformly, `> 2^-42` when `|F| ≥ 2n`. This session's
CS25-free deep-point route (`x1_cs25_free_cap.md`) removes the cap's only external
import (`thm:A`/CS25), resting it on the audited `lem:fiber`. Paper A/B
obstructions and the M1/F1 counterexamples (independently audited) complete the
negative ledger.

## The three open POSITIVE targets (readme status table) → lanes

| # | Target (readme wording) | Lane | What exists now |
|---|---|---|---|
| 1 | **Generated-field locator local limit above all floors** (base list) | **L1** | = Codex's `Q_1 ≤ n^B` conjecture (#106). The crux; falsification survived, proof in progress. My quotient reduction (`x1_quotient_reduction.md`) completes the *decomposition* `|Fib| = Σ_d Q_1(H_{n/d})`. |
| 2 | **Sharp interleaved-list constants near capacity** (`Λ(C^{≡m})`) | **L2 (mine)** | The forward interleaved deep-point bridge is built (PR #101); the *sharp constants* near capacity are open. |
| 3 | **Corrected MCA / residue-line local limit** (the `emca` challenge) | **X1 (mine)** | The list↔MCA deep-point bridge is built (`notes/x1`), and confinement/isotypic/product-bound theory (this session) localizes `emca` to the non-confined slope density; the *local limit itself* is open. |

## What remains after Codex proves `Q_1 ≤ n^B`

Proving the conjecture **closes target 1** — the hardest worst-case combinatorial
core. But the prize is *two threshold-determinations*, and L1's base bound is an
*input* to both. The remaining positive work, with where this session leaves it:

- **(a) Interleaved transfer + sharp constants (target 2, L2).** Lift the base
  bound to `Λ(C^{≡m})` and nail the near-capacity constants. The bridge exists;
  the constants are the open piece. *(Mine.)*
- **(b) MCA / residue-line local limit (target 3, X1).** The `emca` challenge.
  The deep-point bridge converts list↔slopes; confinement (this session) shows
  the QuotientBudget slopes are confined (negligible) on the equivariant stratum,
  so `emca ≈ |non-confined slopes|/q_line`. The residue-line local limit itself
  is open. *(Mine.)*
- **(c) Field accounting.** `Λ` is divided by the **challenge** field `|F|`, while
  the entropy denominator is the **generated** field `q_gen`. Keep `q_gen`,
  `q_line`, `q_chal` separate (readme flags conflation as the #1 false-claim
  source).
- **(d) Threshold tightening + concrete exponent.** Bring `η` down to the cap's
  `2^-9` to *determine* `δ*`, and ensure the polynomial list clears the concrete
  threshold: `Λ ≤ 2^-128 · |F|`, i.e. the exponent `B` in `Q_1 ≤ n^B` must be
  small enough at the actual `(n, |F|)` (a polynomiality proof with a large `B`
  does not by itself win the concrete challenge).
- **Per-scale reserve residue (inside L1/L2).** The quotient reduction shows the
  QuotientBudget is `Σ_{d>1} Q_1(H_{n/d})`; the open analytic piece is which
  quotient scales clear their reserve (`x1_quotient_reduction.md`). On the
  equivariant scales the slopes confine (harmless); the general case is the
  remaining structural work.

## Net

Codex's conjecture is the **list-side crux (target 1)**. The remaining positive
work toward the two grand challenges is concentrated in **the L2 interleaved
constants (target 2) and the X1 MCA/residue-line limit (target 3)** — both my
lanes — plus field-accounting and the quantitative threshold/exponent. So
`Q_1 ≤ n^B` + this session's deep-point/interleaved/confinement machinery are,
between them, aimed at exactly the two prize challenges; the cap (negative) is
already pinned and now CS25-free.

## Pointers
- Spec: `readme.md`, proximityprize.org, ePrint 2026/680.
- This session's results: `x1_cs25_free_cap.md`, `x1_prefix_locator_slope_principle.md`,
  `x1_confinement_from_stabilizer.md`, `x1_quotient_reduction.md`, and the
  `verify_x1_*` scripts.
- Codex's conjecture: PR #106, `notes/l1/l1_quotient_budgeted_locator_conjecture.md`.
