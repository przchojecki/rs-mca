# M1 equal-line generic popularity budget

**Status:** PROVED-LOCAL / CONDITIONAL / AUDIT.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-30.

This note combines two existing local ingredients:

1. the equal-line diagonal singular-value ledger from
   `m1_depth_two_equal_line_diagonal_reduction.md`;
2. the equal-line resultant popularity gate from
   `m1_equal_line_resultant_popularity_gate.md`.

It gives an explicit popularity constant for the equal-line diagonal branch.
It remains conditional on the nonlocal containment step: the endpoint-disjoint
high-overlap leaves containing a fixed center residue must actually reduce to
the equal-line resultant outside the charged singular/denominator fibers.

## Singular support

The equal-line pullback ledger isolates the projective `y`-line singular
support in the set

```text
y = 0,
y = 1,
9y^2 + 2y + 1 = 0,
y = 3/4,
y = infinity.
```

This has at most six projective points over any field of characteristic
`p>3`.  In the exceptional characteristic `p=11`, some listed fibers collide;
the support does not grow.

Thus the projective exceptional budget is

```text
E_eq <= 6.
```

## Resultant gate

For every fixed projective center residue, the equal-line kernel resultant

```text
16x^2y^2 - 8xy^2 + 4xy + y^2 - 2y + 1
```

gives a nonzero quadratic projective gate in the leaf parameter `y`.  Therefore
the projective divisor-gate lemma gives

```text
U_eq <= mu(E_eq+2) <= 8mu.                         (EQ-U)
```

Here `mu` is the multiplicity of the projective leaf parameter: at most `mu`
endpoint-disjoint leaves may share the same `y`.

## Packet-sift consequence

Insert

```text
U = 8mu
```

in the popularity-cap support criterion `(PC1)` of
`m1_high_overlap_graph_budget.md`.  If

```text
F_pop(K,s,h,D,Lambda,8mu) > R_budget,
```

then the equal-line diagonal residual satisfies at least one of:

```text
large support,
near-star,
or containment/gate failure:
  a fixed center residue has endpoint-independent high-overlap leaves
  not covered by the six singular fibers and the quadratic resultant gate.
```

This turns the equal-line branch into a concrete falsifiable target.  The only
remaining algebraic work is the containment statement, not the packet
combinatorics or the divisor root count.

## Verification

The companion verifier reconstructs the projective singular support, checks
the `E_eq <= 6` budget including the `p=11` collision row, checks the resultant
quadratic gate, and verifies the support-floor composition with `U=8mu`:

```sh
python3 experimental/scripts/verify_m1_equal_line_generic_popularity_budget.py
```
