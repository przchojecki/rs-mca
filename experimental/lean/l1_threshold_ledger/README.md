# L1 Threshold Ledger (stdlib-only Lean)

A small, self-contained Lean 4 package that machine-checks the **finite
arithmetic gates** of tonight's L1/M1 threshold results. Like the existing
`experimental/lean/rs_mca_formalization` package it is deliberately
**stdlib-only**: no `mathlib` dependency, and it builds offline in ~1.5 s
(`lake-manifest.json` has `packages: []`). Lean toolchain `v4.31.0`.

It certifies the elementary integer / counting cores that the informal notes
consume; the finite-field, polynomial, and Reed–Solomon content stays cited or
verifier-backed (recorded as typed targets, per the repo's `CERTIFICATION_MAP`
convention). `CORRESPONDENCE.md` is the reviewer-facing index mapping each Lean
theorem to the note and PR it formalizes.

## Modules

### `L1Threshold.PairCountClosing` — Theorem R closing (PRs #222, #223)

Notes: `experimental/notes/l1/l1_prime_ell_onset.md` (Theorem R / Lemma R),
`experimental/notes/l1/l1_coset_mixed_vacancy_threshold.md` (Theorem A),
`experimental/thresholds.tex`.

The prime-`ell` onset proof reduces "no mixed minimal kernel set" to the retained
count `R = sum_j rho_j < (m-t+1) ell = 2 ell`, and closes it by **Cauchy–Schwarz
over the `m = t+1` cosets** from the Lemma-R pair-count budget
`sum_j rho_j(rho_j-1) <= (ell-1)(ell-2)`. This module machine-checks that closing
as an **exact integer inequality**:

- `closing_four`  — `t = 3` (`m = 4` cosets): the budget and `ell >= 3` force
  `R <= 2 ell - 1`. (Theorem R.)
- `closing_three` — `t = 2` (`m = 3` cosets): same conclusion. (The `(2,3)` cell.)
- `closing_four_list` / `closing_three_list` — the same in the note's `sum_j`
  (`List`-fold) notation.
- `tightness_four` — kernel-`decide` certificate that `[3,2,2,2]` at `ell = 5`
  attains the pair-count budget **with equality** and hits `R = 2 ell - 1 = 9`:
  the bound is **razor-tight** (note §Tightness).
- `noclose_five`, `noclose_five_11` — kernel-`decide` certificates that at
  `t = 4` (`m = 5`) the profiles `[3,3,3,3,3]` (`ell=7`) and `[5,5,5,5,3]`
  (`ell=11`) meet the pair-count budget yet have `R >= 2 ell`: the pair-count
  argument closes **exactly** `t = 3` (note §Scope, the proved method boundary).

Discrete Cauchy–Schwarz (`cs3`, `cs4`) is built from the pairwise AM–GM
`2 x y <= x^2 + y^2` (`amgm`); the endgame is the integer `quad_closing`
(`R^2 <= 4R + 4(L-1)(L-2)`, `L >= 3` ⟹ `R <= 2L-1`, the discrete form of
"the positive root is `< 2L` because `ell > 2`"). Since Lean core lacks
`ring`/`nlinarith`, every quadratic identity is distributed by hand and closed by
`omega` over atomic products.

### `L1Threshold.FiberDoubleCount` — QF.10 fiber bound skeleton (PR #225)

Note: `experimental/notes/m1/conjecture_f_fiber_scoped.md` (Theorem A).

The fiber-side scoped Conjecture F bounds a prefix fiber by
`#E_p <= binom(n,d)/binom(j,d)`, via the shortened-RS MDS input "each `d`-subset
lies in at most one member". This module machine-checks that **double-count
skeleton** in a stdlib `List` model of finite types:

- `nodup_lt_length` — the counting primitive: a `Nodup` `Nat` list with entries
  `< T` has length `<= T` (a `Finset`-free pigeonhole, by `erase` induction).
- `double_count` — the injective-packing inequality `#members * b <= T` from
  "`#members` blocks of `b` distinct tokens, all tokens globally distinct
  (`Nodup`), universe of size `T`" (`b = binom(j,d)`, `T = binom(n,d)`).
- `fiber_card_bound` — the division step `E*b <= T` ∧ `0 < b` ⟹ `E <= T/b`.
- `fiber_bound` — the two combined: `#E_p <= binom(n,d)/binom(j,d)` verbatim.
- `choose_values`, `double_count_example` — kernel-`decide` sanity checks.

`binom` is a local Pascal recursion (`Nat.choose` is mathlib-only). The MDS /
dual-distance "`<= 1 owner`" fact (note §3) is the finite-field input; it enters
as the `Nodup` hypothesis and is recorded as the typed target
`SingletonOwnerBound`.

## Build

```sh
cd experimental/lean/l1_threshold_ledger
lake build
```

Green build = every theorem type-checks with **no `sorry`, no `native_decide`,
no mathlib**. Each module ends with `#print axioms`:

- all `PairCountClosing` theorems: `[propext, Quot.sound]` (or **no axioms** for
  the pure-`decide` certificates `tightness_four`, `noclose_five`);
- `FiberDoubleCount.double_count` / `fiber_bound`: `[propext, Classical.choice,
  Quot.sound]` — `Classical.choice` enters through a stdlib `List` lemma; this is
  the standard sanctioned set (cf. `rs_mca_formalization`'s `HighAgreementLedger`
  note); `choose_values` depends on no axioms.

## Scope (honest)

This is **not** a proof of the L1/M1 theorems. It certifies the finite arithmetic
gates the notes consume: the Cauchy–Schwarz closing of Theorem R, its razor-tight
and `t`-boundary certificates, and the QF.10 double-count/division skeleton. The
field-theoretic inputs — Lemma R's `(*)` twisted-root bound (prime `ell`), the
PR #219 reconstruction bijection, and QF.10's shortened-RS MDS / dual-distance
argument — remain cited proofs and verifier outputs (`verify_l1_prime_ell_onset.py`,
`verify_conjecture_f_fiber_scoped.py`), recorded here as the typed interfaces
`LemmaR_pairCount` and `SingletonOwnerBound`.

## Integration

Self-contained: it builds on its own. To fold into the existing stdlib track
instead, move the two modules to `rs_mca_formalization/RsMca/` (e.g.
`RsMca/PairCountClosing.lean`, `RsMca/FiberDoubleCount.lean`), change
`namespace L1Threshold` to `namespace RsMca`, add the imports to `RsMca.lean`, and
extend that package's `CERTIFICATION_MAP.md` with the rows in `CORRESPONDENCE.md`.
