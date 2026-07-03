# E13 spread-exception finite-geometry census

- **Status:** EXPERIMENTAL / AUDIT.
- **DAG nodes:** `spread_exception_classification`, `spread_regime_bound`.
- **Fable evidence item:** E13, "spread exception census / QS.1".
- **Verifier:** `experimental/scripts/verify_e13_spread_exception_finite_geometry_census.py`.
- **Artifact:**
  `experimental/data/certificates/spread-regime-design-evidence/e13_spread_exception_finite_geometry_census.json`.

This packet stress-tests the revised E3 interpretation:

```text
below-cap spread rank loss is finite-geometry/net shaped, or v-syndrome
degenerate
```

The result is mixed and useful.  The `AG(2,4)` cell supports the finite-geometry
interpretation, but the bounded `n=32` controls find unclassified
non-geometry examples.  Therefore the literal "AG/net only" classification is
too narrow unless those control examples are later shown to belong to a larger
finite-geometry class, a paid ledger, or a degenerate branch not captured by
the current classifier.

## Exact AG(2,4) cell

The verifier enumerates every subfamily of all `20` affine lines in `AG(2,4)`
for sizes `2..7`, under both deterministic distinct-slope schedules used by
the E3 packet.

Outcome:

```text
AG(2,4) nondegenerate below-cap exceptions: 373
unclassified AG(2,4) nondegenerate exceptions: 0
```

The first rank loss occurs at six lines.  Sizes `2..5` have no below-cap
losses.  The nondegenerate AG exceptions split into the finite line-net
incidence signatures recorded in the JSON artifact:

```text
distinct_linear, size 6:     435 losses, 195 nondegenerate, 240 degenerate
distinct_linear, size 7:       2 losses,   2 nondegenerate,   0 degenerate
distinct_geometric, size 6:  416 losses, 176 nondegenerate, 240 degenerate
distinct_geometric, size 7:    0 losses,   0 nondegenerate,   0 degenerate
```

This strengthens #185: the bounded AG exceptions are not just examples; in
this finite-geometry cell the whole exception set is classified by affine
line-net incidence data.

## n=32 controls

The verifier also enumerates all subfamilies of the first `16` deterministic
E3 greedy blocks in the two `n=32` control families, for sizes `2..6`.  These
are bounded falsification cells, not full `n=32` support censuses.

Outcome:

```text
greedy_32_j5_lambda1_first16_control: 1 unclassified nondegenerate exception
greedy_32_j6_lambda2_first16_control: 70 unclassified nondegenerate exceptions
```

These examples are nondegenerate by the same union-bound certificate used in
E3.  They are not classified by the present `AG(2,4)` line-net signature, so
they should be treated as a red-team hit against the overly narrow
finite-geometry-only statement.

The conservative next target is not to discard the spread-regime route.  It is
to refine the exception taxonomy:

```text
below-cap spread rank loss is either
  finite-geometry/net shaped,
  v-syndrome degenerate,
  or belongs to the new n=32 sparse-greedy exception class.
```

The new class is small in the tested controls, but it is real enough that a
proof should either classify it structurally or show it is paid.

## Non-claims

This packet does not prove `spread_regime_bound`.

This packet does not enumerate every support family for every `16 <= n <= 32`.
The exact exhaustive part is the `AG(2,4)` line-net cell.  The `n=32` cells are
bounded controls chosen from the deterministic E3 greedy families.

This packet does not show growing many-slope mass.  All recorded losses have
degree deficiency `1` in the reported examples.  The point is classification,
not asymptotic growth.

## Reproduce

```bash
python3 experimental/scripts/verify_e13_spread_exception_finite_geometry_census.py
python3 experimental/scripts/verify_e13_spread_exception_finite_geometry_census.py --emit
python3 experimental/scripts/verify_e13_spread_exception_finite_geometry_census.py --check experimental/data/certificates/spread-regime-design-evidence/e13_spread_exception_finite_geometry_census.json
```
