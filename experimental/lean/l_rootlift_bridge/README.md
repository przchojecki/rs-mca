# LRootliftBridge

Stdlib-only exact arithmetic for the M31 one-error root-lift census stop packet.

The package certifies:

- the deployed order-32 arithmetic and the two reported endpoint values;
- the exact conditional threshold `L <= 539583`;
- the crude no-overlap threshold `L <= 524287`;
- an exhaustive `F_37` Reed--Solomon counterexample with 32 selected roots,
  uniform partner-list size three, and target-list sizes 70 and 72; and
- the elementary cross-root collision `X(X-1)=(X-1)X`.

`native_decide` is used and disclosed. The source imports `Std` only and
contains no `sorry`, `admit`, custom axiom, or Mathlib import.

The mathematical source and proof boundary are in:

```text
experimental/notes/thresholds/m31_rootlift_bridge_stop.md
```

The exact replay is:

```text
python3 experimental/scripts/verify_m31_rootlift_bridge.py --check
python3 experimental/scripts/verify_m31_rootlift_bridge.py --tamper-selftest
```

## Axiom census

`Deployed.lean` ends with `#print axioms` for every theorem it states. All
fourteen declarations depend on exactly one axiom each, namely their own
`native_decide` evaluation:

```text
field_size, row_parameters, order32_decomposition, budget_decomposition,
reported_low, reported_high, reported_boundary, crude_rooted_boundary,
partner_sizes_A, partner_sizes_B, target_count_A, target_count_B,
partner_size_does_not_determine_target, cross_root_collision

  <name> depends on axioms: [<name>._native.native_decide.ax_1_1]
```

No `propext`, `Quot.sound`, `sorry`, `admit`, or custom axiom appears in the
census. The package builds under Lean 4.31.0 with an empty dependency set.
