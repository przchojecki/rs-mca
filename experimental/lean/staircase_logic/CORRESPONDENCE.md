# Correspondence Map — Staircase Logic

Status: stdlib-only abstract-layer certificates for the threshold staircase /
one-step / paid-cell compilers (`agents.md` progress item 7). The package proves
only `Nat`/order facts and `Nat`-list counting facts; the finite-slope,
Reed–Solomon, and huge-integer content stays verifier-backed, recorded as
`Staircase` instance data and the `M1ThresholdBridge` typed target.

Build:

```sh
cd experimental/lean/staircase_logic
lake build
```

## Abstract staircase / one-step — `StaircaseLogic.Staircase`

Source: `experimental/thresholds.tex` (`def:integer numerator staircase`,
`thm:staircase`, `cor:endpoint`, `thm:corridor`);
`experimental/cap25_v13_experimental.tex` (`thm:v13-staircase`,
`cor:v13-endpoint`, `thm:v13-corridor`, `rem:v13-staircase-v12`);
`experimental/experiments.tex` (`thm:one-step-staircase`).

| Claim consumed by the notes | Lean certificate | Source claim | Status |
| --- | --- | --- | --- |
| Safe predicate `N a ≤ B_*` is monotone in `a` (proof of `thm:staircase`). | `safe_up` | `thm:v13-staircase` proof. | Lean-certified |
| The first safe agreement `a_*` is unique. | `firstSafe_unique` | `thm:v13-staircase` (iii), "unique". | Lean-certified |
| One-step pinning: `N a0 > B_* ≥ N (a0+1)` ⟹ `a_* = a0+1`. | `oneStep_isFirstSafe` | `prop:onestep` = `thm:one-step-staircase`; `rem:v13-staircase-v12`. | Lean-certified |
| Safe set is the up-set `{a ≥ a_*}`. | `safe_iff_ge_firstSafe` | `thm:v13-staircase` (iii). | Lean-certified |
| Endpoint: `r_safe = n-a_*`; real supremum `(n-a_*+1)/n` not attained. | `endpoint_supremum` | `cor:v13-endpoint` / `cor:endpoint`. | Lean-certified |

## First-match paid-root removal — `StaircaseLogic.FirstMatch`

Source: `agents.md` §"The complete upper ledger to build at `a0 + 1`" and the
row-packet schema "deduplication rule"; `def:paid-root-removal` ordering;
`experimental/notes/m5/m5_stratification_partition_theorem.md`.

| Claim consumed by the notes | Lean certificate | Source claim | Status |
| --- | --- | --- | --- |
| Paid set telescopes to the union of cells (leaves cover `Ω`). | `mem_paidFold` | m5 partition theorem, "union is `Ω`". | Lean-certified |
| No double-count: paid set stays duplicate-free (leaves pairwise disjoint). | `nodup_paidFold` | m5 partition theorem, "pairwise disjoint". | Lean-certified |
| First-match sum = distinct-root count (U(a) first-match / dedup rule). | `firstMatch_partitions_union` | `agents.md` U(a) rule; m5 partition theorem. | Lean-certified (given `Nodup` cells) |
| Naive overlap over-counts; first-match partitions. | `firstMatch_example` | m5 §Replay mixed example. | Lean-certified (`decide`) |

## M1 `A406/A407` toy — `StaircaseLogic.ToyCert`

Source: `experimental/notes/m1/m1_a407_a408_residual_design_threshold_v1.md`.

| Claim consumed by the note | Lean certificate | Source claim | Status |
| --- | --- | --- | --- |
| `LD_sw` values `107/106/105` = `N(a)=n-a+1`; `B_* = 106`. | `toyN_values`, `toy_matches_bridge`, `M1ThresholdBridge` | note "Third-moment inequality" table / "Public exact-budget row". | Lean-certified (`decide`) / typed target |
| Deployed adjacent pair `L(406) > B_*`, `U(407) ≤ B_*`. | `toy_unsafe_406`, `toy_safe_407` | note "Public exact-budget row". | Lean-certified (`decide`) |
| First safe agreement `a_* = 407`. | `toy_isFirstSafe`, `toy_firstSafe_eval`, `toy_consistency` | note "Public exact-budget row". | Lean-certified |
| `A=407` safe at `105/512`; `A=406` unsafe at `53/256`. | `toy_endpoint_arith`, `toy_endpoint_supremum` | note "Public exact-budget row". | Lean-certified (`decide` + `cor:v13-endpoint`) |

## Typed Targets And Non-Claims

| Claim boundary | Lean artifact | Classification |
| --- | --- | --- |
| `N = LD_sw` (finite-slope support-wise MCA numerator). | `Staircase.N` field / instance data. | Verifier-backed input; not stdlib-certifiable. |
| `B_* = ⌊(p-1)/2^128⌋ = 106`, `p = 27168·2^120+1` prime (Lucas witness 11). | `M1ThresholdBridge` (`Bstar = 106`). | Typed target; huge-integer facts owned by `certify_m1_a407_a408_residual_design_threshold_v1.py`. |
| Every lower/upper staircase input `L(a) ≤ N(a) ≤ U(a)`. | `Staircase.antitone` + instance points. | Verifier-backed / cited. |

## Audit Rule

A row is "Lean-certified" only if it is one of the order/counting rows above or a
direct instantiation of them. `Staircase` instance data (`N`, `B`, antitone) and
`M1ThresholdBridge` flag the field-theoretic / huge-integer inputs supplied
externally; the Lean theorem certifies the abstract step that consumes them. This
map is not a proof of MCA / list-decoding semantics, RS duality, primality, or
protocol soundness. Every theorem's `#print axioms` is within `{propext,
Quot.sound}` (no `sorry`, `native_decide`, `Classical.choice`, or mathlib).
