# Correspondence Map — L1 Threshold Ledger

Status: stdlib-only arithmetic / counting certificates for tonight's L1/M1
threshold results (PRs #222–#225).

Scope: this map records exactly which Lean theorem certifies each finite gate the
notes consume. The package proves only `Nat` arithmetic and `Nat`-list counting
facts. Finite-field, polynomial, Reed–Solomon, and reconstruction-bijection
statements remain cited proofs / verifier outputs, recorded as typed targets.

Build:

```sh
cd experimental/lean/l1_threshold_ledger
lake build
```

## Theorem R closing — `L1Threshold.PairCountClosing`

Source: `experimental/notes/l1/l1_prime_ell_onset.md` (PR #223, Theorem R,
Lemma R, §Tightness, §Scope); companion
`experimental/notes/l1/l1_coset_mixed_vacancy_threshold.md` (PR #222, Theorem A);
`experimental/thresholds.tex`.

| Claim consumed by the note | Lean certificate | Source claim | Status |
| --- | --- | --- | --- |
| Discrete Cauchy–Schwarz over the `m = t+1` cosets: `(sum rho_j)^2 <= m sum rho_j^2`. | `cs4` (`m=4`), `cs3` (`m=3`); built from `amgm` (`2xy <= x^2+y^2`). | Note "Closing", the C–S step. | Lean-certified |
| Integer closing: `R^2 <= 4R + 4(ell-1)(ell-2)` and `ell >= 3` ⟹ `R <= 2ell-1` (positive root `< 2ell` because `ell > 2`). | `quad_closing` | Note "Closing", the strict `(ell-1)(ell-2) < ell(ell-2)` step. | Lean-certified |
| **Theorem R** (`t=3`, `m=4`): pair-count budget ⟹ `R = sum_j rho_j <= 2ell-1 < 2ell`, so no mixed minimal kernel set. | `closing_four`; `closing_four_capped` (note's full hypotheses incl. `rho_j <= ell-1`); `closing_four_list` (`sum_j` form). | Note "Theorem R". | Lean-certified (given Lemma R) |
| The `(2,3)` cell (`t=2`, `m=3`) by the same proof over 3 cosets. | `closing_three`; `closing_three_list`. | Note Corollary, `(2,3)`. | Lean-certified (given Lemma R) |
| Razor-tightness: `[3,2,2,2]` at `ell=5` attains the budget with equality (`sum rho(rho-1)=12=(ell-1)(ell-2)`) and hits `R=2ell-1=9`. | `tightness_four`; `tightness_four_inrange`. | Note §Tightness (`p in {41,61}`). | Lean-certified (`decide`, axiom-free) |
| Method boundary is sharp in `t`: at `t=4` (`m=5`) profiles `[3,3,3,3,3]` (`ell=7`) and `[5,5,5,5,3]` (`ell=11`) meet the budget but have `R >= 2ell` — pair-counting closes exactly `t=3`. | `noclose_five`; `noclose_five_11`. | Note §Scope (IP-max `>= 2ell` for `t>=4`). | Lean-certified (`decide`, axiom-free) |

## QF.10 fiber double-count — `L1Threshold.FiberDoubleCount`

Source: `experimental/notes/m1/conjecture_f_fiber_scoped.md` (PR #225, Theorem A,
§3 MDS input).

| Claim consumed by the note | Lean certificate | Source claim | Status |
| --- | --- | --- | --- |
| Finite-set pigeonhole (no `Finset` in core): a `Nodup` list of naturals `< T` has length `<= T`. | `nodup_lt_length` | Counting primitive behind the double-count. | Lean-certified |
| Injective packing / double-count: `#members * binom(j,d) <= binom(n,d)` from "each `d`-subset in `<= 1` member". | `double_count` | Note Theorem A proof (double-counting `d`-subsets). | Lean-certified (given `<= 1 owner`) |
| Division step: `E * b <= T` ∧ `0 < b` ⟹ `E <= T / b`. | `fiber_card_bound` | Note Theorem A, the quotient bound. | Lean-certified |
| **QF.10 Theorem A** (fiber bound): `#E_p <= binom(n,d)/binom(j,d)`. | `fiber_bound` (`b=binom(j,d)`, `T=binom(n,d)`, `d<=j`). | Note Theorem A. | Lean-certified (given §3 MDS input) |
| Local `binom` reproduces standard values / ratios, e.g. `binom(6,2)/binom(4,2)=2`. | `choose_values`; `double_count_example`. | Note reserve-`d` ratio. | Lean-certified (`decide`, axiom-free) |

## Typed Targets And Non-Claims

| Claim boundary | Lean artifact | Classification |
| --- | --- | --- |
| Lemma R pair-count `sum_j rho_j(rho_j-1) <= (ell-1)(ell-2)`, whose proof is the `(*)` twisted-root bound over `F_p` (needs PRIME `ell` and polynomial root counting). | `LemmaR_pairCount` (interface `Prop`; the hypothesis of `closing_*`). | Typed target; verifier-backed (`verify_l1_prime_ell_onset.py`), not stdlib-certifiable. |
| The PR #219 reconstruction bijection (listed full-petal codewords ↔ minimal kernel sets) turning `R < 2ell` into "no mixed kernel set". | (cited in module docstring) | Cited proof (`l1_general_reconstruction_collapse.md`). |
| QF.10 "`<= 1 owner`" = shortened-RS MDS / dual-distance `d+1` (no `d` points carry a `V`-dependence). | `SingletonOwnerBound` (interface `Prop`; the `Nodup` hypothesis of `double_count`). | Typed target; verifier-backed (`verify_conjecture_f_fiber_scoped.py`), not stdlib-certifiable. |

## Audit Rule

A row is "Lean-certified" only if it is one of the arithmetic/counting rows above
or a direct conjunction of them. "Given Lemma R" / "given the §3 MDS input" /
"given `<= 1 owner`" flags that the field-theoretic hypothesis is supplied
externally (typed target); the Lean theorem certifies the elementary step that
consumes it. This map is not a proof of MCA/list-decoding, finite-field
semantics, RS duality, or protocol soundness.
