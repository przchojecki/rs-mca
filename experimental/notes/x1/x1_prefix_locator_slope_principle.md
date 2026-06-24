# X1: the prefix-locator slope principle — one mechanism behind F1, M1, L2, and the L1 core

- **Status:** SYNTHESIS / AUDIT. The shared mechanism and the negative-side
  instances are PROVED + verified (per-lane verifiers below + the unified
  `verify_x1_prefix_locator_principle.py`). The positive-side statement (the L1
  conjecture, #106) is CONJECTURAL. The slope-confinement ⟺ stabilizer
  correspondence is a verified structural parallel on the extremal families,
  not yet a proven biconditional for arbitrary words.
- **Agent/model:** Claude Opus 4.8 (L2/X1 lane, branch `allen/l2-x1-interleaved-mca`).
- **Date:** 2026-06-24.
- **Scope:** organizes, across lanes, the deep-point bridge (`notes/x1`, #101),
  Paper D `lem:fiber`/`lem:confine`/`cor:Fvalued`/`thm:main`, the M1 Cycle120
  fixed-jet transfer (#105), the F1 fixed-slack extension counterexample (#103),
  and the L1 quotient-budgeted locator conjecture (#106). Does not edit Papers A–D.

## The principle (one sentence)

Every negative-side obstruction in this project — the universal cap (L2/Paper D),
the Cycle120 line-decoding count (M1), and the fixed-slack extension
counterexample (F1) — is the **evaluation image of a prefix-constrained locator
fiber**, and the L1 positive target is a **stabilizer-stratum bound on the same
fiber**. There is one object and one map; the lanes differ only in which
stratum they live on and which direction (lower vs upper bound) they need.

## The shared object and lemma

**Object.** Fix a cyclic domain `H_n ≤ F_q^*`, a received word `U`, a support
size `a = k+σ`, and a common prefix value `c`. The **prefix-constrained
locator fiber** is

```text
Fib_U^c(a) = { a-subsets S ⊆ H_n : the top σ−1 interior coefficients of the
               (U,S)-locator equal c }.
```

For each `S` there is a degree-`≤k` polynomial `P_S` (the closing codeword / the
poly agreeing with `U` on `S`) determined by `(U,S)`.

**Shared lemma (bad slopes = evaluation image).** Pick a pole `α` (a point off
`H_n`, or a deep point). Build the single line `f,g` from `(U,α)`. Then the
support-wise CA/MCA-bad slopes of `(f,g)` for the relevant Reed–Solomon code are
**exactly** the evaluation image

```text
{ z_S(α) : S ∈ Fib_U^c(a) },     z_S(α) = (P_S evaluated at α),
```

and the number of distinct bad slopes equals the size of that image. The
support-wise *noncontainment* (genuine MCA-badness) is the dimension fact that a
degree-`<k` codeword cannot match the pole column on `|S| = k+σ ≥ k+1` points.

This is proved per lane and re-checked in one place by
`verify_x1_prefix_locator_principle.py` (which builds `z_S(α)` and confirms the
image is the bad-slope set).

## The four lanes are four instances

| lane (PR) | received word `U` | prefix condition (common value `c`) | pole | bad slope `z_S` | use / direction |
|---|---|---|---|---|---|
| **L2/X1** (#101) | heavy word `u_z = x^{k+2a_q}+z x^{k+a_q}` | `e_1` fixed (`= -z`); from `∏_b(X^{a_q}-b)` | deep point `α` | `P(α)` (deep image) | cap **lower** bound |
| **M1** (#105) | Cycle116 slot word | top σ coeffs of `P_J` common (`c ≠ 0`) | `β ∉ H` | `1/P_J(β)` | LD_sw **count** |
| **F1** (#103) | monomial `x^a` | `e_1=…=e_{σ-1}=0` (`c = 0`) | `α ∈ F\B` | `Q_S(α)`, `Q_S = X^a - L_S` | emca density **lower** bound |
| **L1** (#106) | arbitrary `U` | (the same `Fib_U(a)`) | — | — | list **upper** bound (target) |

The prefix condition is literally the same device — *hold the top interior
coefficients of the locator at a common value* — specialized to `c=0` (F1),
`c≠0` (M1 fixed-jet), or the slope parameter itself (L2). `z_S = Q_S(α)` is the
deep image of the monomial `x^a`; `z_J = 1/P_J(β)` is the parity-check syndrome;
`P(α)` is the deep-point image — three names for "evaluate the `(U,S)`
polynomial at the pole."

## The negative/positive duality: the stabilizer split

Split the fiber by the cyclic stabilizer `Stab(S) = {h ∈ H_n : hS = S}` (Möbius
inversion on the divisor lattice):

```text
|Fib_U(a)| = QuotientBudget(U,a)  +  Q_1(U,a)
             └ Σ_{d>1} (exact-stab-order d) ┘   └ primitive (trivial stabilizer) ┘
```

This split is **intrinsic to the fiber** — independent of the pole `α` and the
lane. The two negative lanes and the positive lane occupy **complementary
strata**, which is verified directly (`verify_x1_prefix_locator_principle.py`,
`F_17`, `n=16`):

- **`lem:fiber` (the cap's engine) lives in the QuotientBudget.** Its supports
  are root sets `S_A = ⋃_b S_b` of the power-locator `∏_b(X^{a_q}-b)` — unions of
  `a_q`-fibers, hence `K_{a_q}`-stable. Measured: a `lem:fiber`-type fiber of 28
  supports is **100% quotient-periodic** (`QuotientBudget = 28`, `Q_1 = 0`,
  stabilizers `{2:24, 4:4}`). All the exponential cap mass is periodic.
- **F1 (#103) lives in `Q_1`.** Its monomial/prefix-vanishing supports are
  primitive: a σ=2 fiber of 256 supports is **100% primitive** (`Q_1 = 256`,
  `QuotientBudget = 0`). Its large bad-slope density (185 of 256) is therefore
  *below-reserve primitive mass*.

So the picture is exact:

```
            QuotientBudget  (periodic, structured)        Q_1  (primitive)
            ─────────────────────────────────────        ───────────────────
 negative:  lem:fiber  →  the universal cap (#101)        F1 (#103)  →  sub-reserve
            (confined / B-rational slopes, lem:confine)   primitive density (cor:Fvalued)
 positive:  already budgeted / understood                 L1 target:  Q_1 ≤ n^B  (#106)
```

**The reserve boundary is the dividing line.** F1's primitive mass is large
*below* the reserve (`σ` fixed, `η = σ/(n) ≪ C/log n`); the L1 conjecture claims
`Q_1 ≤ n^B` *above* it. So #103 is precisely the witness that the L1 conjecture's
`σ ≥ C·n/log n` hypothesis is necessary — the negative F1 family and the positive
L1 target sit on the two sides of the same threshold, on the same object.

## Why this matters (the program in one frame)

1. **The whole negative side is one mechanism.** After this session the cap is
   CS25-free (`x1_cs25_free_cap.md`): it rests on `lem:fiber` + the deep-point
   identity. M1 and F1 are the same identity with different `(U, c, α)`. So
   "exhibit/count MCA-bad slopes" = "evaluate a prefix-constrained locator fiber
   at a pole," uniformly.
2. **The open core is a single inequality.** Since the cap's mass is entirely in
   the QuotientBudget (verified), and the QuotientBudget is the structured /
   confined stratum, the *entire* remaining question — the L1 positive bound — is
   `Q_1 ≤ n^B`. Everything else is now either proved (negative) or budgeted
   (periodic).
3. **It says where to look.** A reserve-cleared primitive alert (large `Q_1`
   above the reserve) would be a genuinely new obstruction — not a deep-image of
   any known periodic family. The falsification scanners (#106) target exactly
   this.

## Honest limits

- The **L1 conjecture (`Q_1 ≤ n^B`) is open**; evidence is small-`n` with no
  reserve-cleared primitive alert.
- The **slope-confinement ⟺ stabilizer correspondence** is now **proved in the
  forward direction, but only per-character** (`x1_confinement_from_stabilizer.md`):
  a ζ-equivariant word on a `K_d`-stable support gives a confined (folded) slope,
  and any word decomposes into `d` isotypic components each of which folds. So the
  correspondence is exact on the **equivariant stratum** (where the cap mass /
  `lem:fiber` / folded quotient words live) — there QuotientBudget ↔ confined. It
  is **not** a blanket support-by-support equivalence: a genuinely multi-isotypic
  word can have a quotient-periodic support with a **non-confined** slope (verified
  witness). So "L1 = non-confined MCA-bad-slope density" is rigorous on the
  equivariant stratum; the remaining gap is the non-equivariant periodic supports
  (show their mass is poly, or that they also confine).
- This note **organizes**; it proves no new theorem. Its value is the single
  frame + the verified stratum assignment.

## Reproducibility

```bash
python3 experimental/scripts/verify_x1_prefix_locator_principle.py   # the unified bookkeeping (this note)
python3 experimental/scripts/verify_x1_deep_point_identity.py        # L2 deep-point identity (#101)
python3 experimental/scripts/verify_m1_cycle84_count_structure.py    # M1 fixed-jet transfer (#105)
python3 experimental/scripts/verify_audit_pr103_f1_sigma_two.py      # F1 sigma>=2 (#103)
python3 experimental/scripts/verify_x1_lem_fiber.py                  # lem:fiber (the QuotientBudget engine)
```

## Ledger impact

- **Cross-lane organizing principle (new):** F1/M1/L2 negative obstructions =
  evaluation image of a prefix-constrained locator fiber; L1 positive target =
  the `Q_1` stratum bound on the same fiber. The stratum assignment
  (`lem:fiber` → QuotientBudget, F1 → `Q_1`) is verified.
- **Frontier (clarified):** the open core is `Q_1 ≤ n^B` above the reserve
  (#106); the reserve boundary is where F1 (#103, below) meets it.
