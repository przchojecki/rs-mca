STATE: COMPLETE

# M31 flatness conjecture C1 — Lean correspondence

## Validation boundary

This stdlib-only package states one conjecture as a `def : Prop` and proves only
its logical falsifier implication, integrated finite-zoo consistency instances,
the complete-`T_32` scope guard, and exact coefficient-four arithmetic. It does
not prove the conjecture, a row-sharp `U_Q`, an ordinary-list upper bound, a
received-word realization, first-match survival, or row closure.

The package builds on Lean `v4.31.0`.
The package contains no `sorry`, `admit`, custom `axiom`, or Mathlib dependency.
Every theorem has a `#print axioms` census in
`M31FlatnessConjectureC1/Champion.lean`.

## Source statement

The source dossier is

```text
experimental/notes/thresholds/m31_flatness_conjecture_c1.md
```

Its single champion is

```text
for every target eta, anchor A in F_eta, and 33 <= e <= 213,
  d_e(A) <= 1233.
```

The Lean definition `m31Depth32BandFlatnessConjecture` carries the same
quantifiers through duplicate-free canonical support lists. Universality over
every finite certified neighbor list is equivalent to the rooted shell-degree
cap on the finite pinned support universe.

## Object correspondence

- `Support` is a list of odd quotient representatives.
- `canonicalSupportValid` checks a valid 479-subset of the punctured 1022-point
  quotient domain and canonical list order.
- `PrefixTarget` is a list of the first 32 nonleading monic locator
  coefficients; `prefixTargetValid` checks length 32 and entries below `p`.
- `bandNeighborValid target anchor e support` checks canonical support validity,
  the exact target, rooted deficiency `e`, and inequality from the anchor.
- `bandPacketValid` additionally checks `33 <= e <= 213`, a valid anchor with
  the same target, and a duplicate-free neighbor list; `IsBandPacket` is its
  proposition wrapper.
- `IsMinimalChampionFalsifier` is exactly one valid packet of length 1234.

## Proved declarations and source meaning

- `minimal_falsifier_refutes_champion` proves that a valid 1234-neighbor packet
  negates the champion. It does not require shell completeness.
- `integrated_zoo_consistency_shard` checks the full-`T_64` packet lengths
  `49`, `441`, and `1225`; their exact band admissibility; the off-lattice
  deficiency-96 pair and its 47/48 coefficient boundary; and the mixed
  deficiency-192 packet of exactly 1233 distinct certified neighbors. The last
  packet proves only a lower degree of 1233, not completeness of that shell.
- `t32_skeleton_scope_shard` transports the integrated selector-atlas theorem
  to the fixed-remainder total `3432` and nontrivial collision submaximum `482`,
  and records their relation to the shell cap.
- `ambient_average_shard` transports the exact floor/ceiling average and
  `floor(4M/Q)=14456476` from the integrated quotient arithmetic theorem.
- `coefficient_four_compiler_shard` checks the live-window arithmetic: champion
  total `15007628`, reserve `1769587`, and the `5191/5192` edge.

## Imported kernel-checked evidence

The package imports and uses these existing declarations:

```text
M31QuotientBandMixing.Witnesses.rooted_shell_census
M31QuotientBandMixing.Witnesses.mixing_prefix_exact
M31QuotientBandMixing.Witnesses.quotient_average_arithmetic
M31QuotientT16MixingFloor.Witness.one_thousand_two_hundred_thirty_three_distinct_neighbors
M31QuotientT16MixingFloor.Witness.coefficient_four_window_arithmetic
M31FlatnessKeystone.SelectorAtlas.selector_relation_atlas_exact
M31FlatnessKeystone.packet_selector_atlas
```

The source-level degree transfers and scope boundaries are in:

```text
experimental/notes/thresholds/m31_quotient_band_swap_census_t16_mixing.md
experimental/notes/thresholds/m31_quotient_t16_mixing_floor.md
experimental/notes/thresholds/m31_t32_skeleton_flatness_keystone.md
experimental/notes/thresholds/m31_q_rooted_shell_envelope.md
```

## Green axiom census

The green build log prints:

```text
minimal_falsifier_refutes_champion:
  [propext]
integrated_zoo_consistency_shard:
  [propext, integrated_zoo_consistency_shard._native.native_decide.ax_1_1]
t32_skeleton_scope_shard:
  [propext, Quot.sound,
   M31FlatnessKeystone.SelectorAtlas.selector_relation_atlas_exact._native.native_decide.ax_1_1]
ambient_average_shard:
  [M31QuotientBandMixing.Witnesses.quotient_average_arithmetic._native.native_decide.ax_1_1]
coefficient_four_compiler_shard:
  []
```

No new declaration depends on `sorryAx`. The only warnings are inherited
unused-variable lints in the imported selector-atlas source.

## `decide` / `native_decide` disclosure

`integrated_zoo_consistency_shard` uses `native_decide` on closed finite data.
It reconstructs the listed supports, quotient-locator prefixes, rooted
deficiencies, duplicate checks, and packet predicates from imported definitions.
The coefficient-four arithmetic theorem uses ordinary `decide`. The T32 and
ambient-average shards reuse imported kernel-checked theorems; those imported
sources disclose their own `native_decide` use.

Green CI establishes compilation and the displayed declaration census. The
mathematical statement-to-source comparison above is a separate audit and is
not inferred from compilation alone.
