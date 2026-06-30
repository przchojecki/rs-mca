# M1 equal-line generic popularity budget

**Status:** PROVED-LOCAL / CONDITIONAL / AUDIT.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-30.

This note combines three local ingredients:

1. the equal-line diagonal singular-value ledger from
   `m1_depth_two_equal_line_diagonal_reduction.md`;
2. the equal-line resultant popularity gate from
   `m1_equal_line_resultant_popularity_gate.md`;
3. the finite split-fiber containment lemma from
   `m1_equal_line_split_fiber_containment.md`.

It gives an explicit popularity constant for the ordinary finite equal-line
split-fiber branch.  It remains conditional only on the nonlocal model-entry
step: the global endpoint-disjoint high-overlap leaves must actually reduce to
this equal-line split-fiber model after quotient, tangent, fixed-root, and
denominator exceptions are charged.

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

## Local cap theorem

In the ordinary finite split-fiber equal-line model, the containment hypothesis
needed by the divisor gate is no longer open.  If a leaf parameter `z` is
regular and a center residue `x` satisfies the leaf-containment equation

```text
K_x(z)=0,
```

then `m1_equal_line_split_fiber_containment.md` proves that, with

```text
y = (1+3z^2)/(1-z)^2,
```

one has

```text
R(x,y)=0,
```

unless `y` lies in the six charged projective singular fibers.  Therefore a
fixed center residue is contained in at most

```text
mu(6+2) = 8mu
```

endpoint-disjoint ordinary finite split-fiber leaves.

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
or model-entry failure:
  the endpoint-independent high-overlap leaves do not reduce to the ordinary
  finite equal-line split-fiber model after the charged branches are removed.
```

This turns the equal-line branch into a concrete falsifiable target.  The
ordinary finite split-fiber containment, packet combinatorics, and divisor root
count are closed locally; the remaining algebraic work is the global reduction
from the full M1 high-overlap model into this equal-line split-fiber chart.

## Verification

The companion verifier reconstructs the projective singular support, checks
the `E_eq <= 6` budget including the `p=11` collision row, checks the resultant
quadratic gate, and verifies the support-floor composition with `U=8mu`:

```sh
python3 experimental/scripts/verify_m1_equal_line_generic_popularity_budget.py
```
