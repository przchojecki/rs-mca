# Staircase Logic (stdlib-only Lean)

A small, self-contained Lean 4 package that machine-checks the **abstract
staircase / one-step layer** of the threshold compilers — the order-theoretic
skeleton that `agents.md` progress item 7 calls the "staircase, row-packet, and
paid-cell compilers". Like `experimental/lean/l1_threshold_ledger` and
`experimental/lean/rs_mca_formalization` it is deliberately **stdlib-only**: no
`mathlib` dependency (not even `Std`), `lake-manifest.json` has `packages: []`,
and it builds offline in ~1–2 s. Lean toolchain `v4.31.0`.

It proves the *abstract* layer only — an opaque nonincreasing numerator
`N : Nat → Nat` with an integer budget `B` — so there are **no huge integers**
and every proof is a pure `Nat`/order fact (`omega`, `Nat.not_le`) or a kernel
`decide` on tiny numerals. The finite-slope semantics of `N` (that it *is*
`LD_sw`) and the value of `B_* = ⌊ε* Q⌋` stay verifier-backed and enter only as
the instance data of a `Staircase` (see `ToyCert.lean`, the M1 `A406/A407` toy).

Green build = every theorem type-checks with **no `sorry`, no `native_decide`,
no mathlib**. `#print axioms` on **every** theorem reports exactly
`[propext, Quot.sound]` — nothing beyond the two propositional/quotient axioms
(no `Classical.choice`).

## Build

```sh
cd experimental/lean/staircase_logic
lake build
```

## Modules

### `StaircaseLogic.Staircase` — the abstract staircase / one-step layer

A `Staircase` bundles the numerator `N`, budget `B`, block length `n`, agreement
interval `I = [amin, amax]`, and the note's "nonincreasing on `I`" hypothesis
`antitone`. `safe a := N a ≤ B`; `Unsafe a := B < N a` (capital `U`: `unsafe` is
a reserved keyword).

- `safe_up` — **monotonicity of safety**: `a ≤ a'` and `safe a` ⟹ `safe a'`.
  Antitone-in-`a` means larger agreement ⇒ smaller numerator, so the safe set is
  the **up-set** `{a ≥ a_*}` (the direction fix the task flagged).
- `firstSafe_unique` — **uniqueness** of the first safe agreement `a_*`.
- `oneStep_isFirstSafe` — the **one-step certificate**: `N a0 > B` and
  `N (a0+1) ≤ B` ⟹ `IsFirstSafe (a0+1)`, i.e. `a_* = a0 + 1`.
- `safe_iff_ge_firstSafe` — the staircase set: safe `⟺ a ≥ a_*`.
- `endpoint_supremum` — the **endpoint / supremum** characterization in
  `Nat`/rational form: `r_safe = n - a_*` attained; supremum `(n-a_*+1)/n` not
  attained; every safe radius numerator `< n-a_*+1`.
- `firstSafe` / `firstSafeFrom` — a computable first-match scan for `a_*`.

### `StaircaseLogic.FirstMatch` — first-match paid-root removal

Each ledger cell is a `List Nat` of root ids; `paidStep paid c := paid ++ (c \ paid)`
pays only a cell's not-already-paid roots (the m5 leaf `L_i = T_i \ ⋃_{<i}`).

- `mem_paidFold` — the paid set telescopes to the union `paid ∪ ⋃ cells`.
- `nodup_paidFold` — **no double-count**: duplicate-free cells keep the paid set
  duplicate-free (disjointness-after-removal, via `nodup_append`).
- `firstMatch_partitions_union` — the shipped statement: the first-match paid set
  is duplicate-free and its members are **exactly** the union, so the running
  first-match count is the number of *distinct* roots (`agents.md` U(a)
  first-match rule / deduplication rule; m5 stratification-partition theorem).
- `firstMatch_example` — a concrete census: cells `[[1,2,3],[2,3,4],[3,5]]` with
  naive length-sum `8` pay only `5` distinct roots.

### `StaircaseLogic.ToyCert` — decide-certificates (M1 `A406/A407` toy)

Instantiates the abstract layer on the committed M1 residual-design threshold row
(`experimental/notes/m1/m1_a407_a408_residual_design_threshold_v1.md`): tangent
numerator `N(a) = n - a + 1 = 513 - a` at `n = 512`, giving `LD_sw` values
`107 / 106 / 105` at `a = 406 / 407 / 408`, versus the `2^-128`-scaled budget
`B_* = ⌊(p-1)/2^128⌋ = 106` for `p = 27168·2^120 + 1`. The huge-integer
primality/floor facts are the Python verifier's; Lean consumes only the small
integers. `decide`-certificates: `toy_unsafe_406`, `toy_safe_407/408`,
`toy_isFirstSafe` (`a_* = 407`), `toy_endpoint_arith` / `toy_endpoint_supremum`
(`r_safe = 105`, supremum `106/512 = 53/256` unattained), `toy_firstSafe_eval`
(`firstSafe = 407`), and `toy_consistency` (search value = abstract `a_*`, a
witness-vs-lemma consistency closure). `M1ThresholdBridge` records the packet
`LD_sw`/`B_*` interface as a typed target.

## Theorem → tex / agents.md map

| Lean theorem (`StaircaseLogic`) | Source statement | Where | Status |
| --- | --- | --- | --- |
| `Staircase` (structure), `safe`, `Unsafe` | `def:integer numerator staircase` — `N` nonincreasing on `I`, `B_* = ⌊ε*Q⌋`, safe `N a ≤ B_*` | `thresholds.tex` §def; `cap25_v13_experimental.tex` `def` before `thm:v13-staircase` | modeled |
| `safe_up` | safe predicate monotone in `a` (proof of `thm:staircase`: "if it holds at `a`, then for `a' ≥ a`, `N a' ≤ N a ≤ B_*`") | `thm:v13-staircase` / `thm:staircase` proof | Lean-certified |
| `firstSafe_unique` | unique first safe agreement `a_*` (case (iii) "there is a **unique** first safe agreement") | `thm:v13-staircase` (iii) / `thm:staircase` | Lean-certified |
| `oneStep_isFirstSafe` | **`prop:onestep`** = one-step staircase pinning: `N a0 > B_* ≥ N (a0+1)` ⟹ `a_* = a0+1` | `experiments.tex` `thm:one-step-staircase`; `cap25_v13_experimental.tex` `rem:v13-staircase-v12`; `agents.md` finite MCA node | Lean-certified |
| `safe_iff_ge_firstSafe` | staircase set = up-set `{a ≥ a_*}` (safe set `{a : a ≥ a_*}` in (iii)) | `thm:v13-staircase` (iii) | Lean-certified |
| `endpoint_supremum` | **`cor:v13-endpoint`**: `r_safe = n - a_*`; real supremum `(n-a_*+1)/n` not attained when `N(a_*-1) > B_*` | `cap25_v13_experimental.tex` `cor:v13-endpoint`; `thresholds.tex` `cor:endpoint` | Lean-certified |
| `firstSafe`, `firstSafeFrom`, `firstSafeFrom_eq`, `firstSafe_eq_of_isFirstSafe`, `oneStep_firstSafe` | computable localization of `a_*`: the scan returns the first safe agreement, and one-step gives `firstSafe = a0+1` literally | `thm:v13-staircase` (constructive reading); `prop:onestep` | Lean-certified (computable) |
| `paidStep`, `paidFold` | paid-root subtraction ordering; m5 leaf `L_i = T_i \ (T_0 ∪ … ∪ T_{i-1})` | `def:paid-root-removal` ordering; `m5_stratification_partition_theorem.md` | modeled |
| `mem_paidFold` | leaves cover `Ω` (union telescopes) | m5 partition theorem "their union is `Ω`" | Lean-certified |
| `nodup_paidFold` | leaves pairwise disjoint (no double-count) | m5 partition theorem "pairwise disjoint" | Lean-certified |
| `firstMatch_partitions_union` | **`agents.md` U(a) first-match rule** / "deduplication rule: support/image/root coalescing theorem": first-match sums = distinct-root count | `agents.md` §"complete upper ledger", row-packet schema; m5 partition theorem | Lean-certified |
| `firstMatch_example` | naive overlap over-counts, first-match partitions (m5 replay's "mixed example where naive overlap counting overcounts") | m5 partition theorem §Replay | Lean-certified (`decide`) |
| `toy_unsafe_406`, `toy_safe_407` | the deployed pair `L(a0) > B_*`, `U(a0+1) ≤ B_*` at the M1 row | `m1_a407_a408_residual_design_threshold_v1.md` (`LD_sw` 107/106; `B_* = 106`) | Lean-certified (`decide`) |
| `toy_isFirstSafe` | `a_* = 407` for the M1 `A406/A407` row | same note, "Public exact-budget row" | Lean-certified |
| `toy_endpoint_arith`, `toy_endpoint_supremum` | `A=407` safe at `105/512`; `A=406` unsafe at `53/256` | same note, "Public exact-budget row" | Lean-certified (`decide` + `cor:v13-endpoint`) |
| `toy_consistency` | witness-vs-lemma closure (computable `firstSafe` = abstract `a_*`) | process mandate (memory) | Lean-certified |
| `M1ThresholdBridge` | typed target for the packet `LD_sw` / `B_*` interface | `m1_a407_a408_residual_design_threshold_v1.md` | Typed target (verifier-backed) |

## Scope (honest)

This is **not** a proof of any MCA / list-decoding / threshold theorem. It
certifies the abstract order layer that the compilers consume: the staircase
localization, one-step pinning, endpoint convention, and first-match
deduplication, plus a `decide` instantiation on the M1 `A406/A407` integers. The
identity that `N = LD_sw` (finite-slope support-wise MCA), the value
`B_* = ⌊(p-1)/2^128⌋ = 106` (huge-integer primality/floor), and every lower/upper
staircase input remain verifier-backed / cited, recorded here as the `Staircase`
instance data and the `M1ThresholdBridge` typed target. See `CORRESPONDENCE.md`
for the audit rule.
