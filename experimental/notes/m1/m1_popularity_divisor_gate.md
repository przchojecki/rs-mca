# M1 popularity divisor gate

**Status:** PROVED-LOCAL / CONDITIONAL / AUDIT.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-30.

This note is the algebraic handoff for
`m1_high_overlap_graph_budget.md`.  The packet-sift package reduces the
far-from-star small-support branch to a popularity cap for one center-packet
residue against endpoint-disjoint high-overlap leaves.  This note records a
simple but useful way to obtain that cap from bounded-degree divisor gates,
which is the form produced by many of the Kummer/resultant reductions already
used in the M1 notes.

It does not prove the missing Hankel/Kummer gate for the actual residue-line
families.  It proves that once such gates are supplied, the popularity cap and
the corresponding support floor follow with explicit constants.

## Setup

Fix a center packet `P_a` and a center residue point `x in P_a`.  Let `B` be a
set of endpoint-disjoint high-overlap leaves attached to `a`.  Assume the
leaves have an affine parameter

```text
theta : B -> F
```

with multiplicity at most `mu`:

```text
#{ b in B : theta(b)=t } <= mu        for every t in F.
```

Let `B_x` be the leaves containing the residue point:

```text
B_x = { b in B : x in P_b }.
```

Suppose the algebraic high-overlap condition has been reduced to:

```text
theta(B_x) subset Z_exc union V(g_1) union ... union V(g_r),
```

where:

```text
|Z_exc| <= E,
g_i in F[T] is nonzero,
deg(g_i) <= d_i.
```

The exceptional set includes any points outside the chosen affine chart, such
as the point at infinity in a projective parameter line.

## Lemma: divisor gate to popularity cap

Under the setup above,

```text
pop_a(x) = |B_x| <= mu ( E + d_1 + ... + d_r ).       (DG)
```

Thus a uniform divisor-gate package gives the popularity cap

```text
U_gate = mu ( E + sum_i d_i ).
```

## Proof

Each nonzero polynomial `g_i` has at most `deg(g_i)` roots in the affine line
over `F`.  Hence

```text
|Z_exc union V(g_1) union ... union V(g_r)|
  <= E + d_1 + ... + d_r.
```

The parameter multiplicity bound multiplies this by at most `mu`, proving
`(DG)`.

## Support-floor consequence

Insert

```text
U = U_gate
```

into the popularity-cap support criterion `(PC1)` of
`m1_high_overlap_graph_budget.md`.  If

```text
F_pop(K,s,h,D,Lambda,U_gate) > R,
```

then every selected packet family satisfies at least one of:

```text
large support:       B > R,
near-star:           #{endpoint supports E_a} < L D,
divisor-gate break:  for some center residue x, the leaf parameters containing
                     x are not covered by the stated exceptional set and
                     nonzero divisor gates.
```

So the remaining M1/C3 algebraic task can be stated as a falsifiable local
claim:

```text
for every endpoint-disjoint high-overlap star and every center residue x,
the leaf parameters containing x are covered by boundedly many nonzero
bounded-degree gates, up to a bounded exceptional set and bounded
parameter multiplicity.
```

If this claim is proved for the actual Hankel residue-line packet families,
then the far-from-star small-support residual branch is closed whenever the
displayed `F_pop` inequality beats the target support budget.

## Projective/rational form

In many residue-line reductions the leaf parameter is projective, or the gate
is first obtained as a rational function and then cleared of denominators.  The
same lemma has the following projective form.

Let

```text
theta : B -> P^1(F)
```

have fiber multiplicity at most `mu`.  Suppose

```text
theta(B_x) subset Z_exc union V(G_1) union ... union V(G_r),
```

where:

```text
|Z_exc| <= E,
G_i in F[Y_0,Y_1] is a nonzero homogeneous binary form,
deg(G_i) <= d_i.
```

Then again

```text
pop_a(x) <= mu ( E + d_1 + ... + d_r ).            (PDG)
```

This includes rational affine gates: after writing a gate as
`N(T)/Q(T)=0`, the roots of `Q`, the point at infinity, and any chart-exception
fibers are charged to `Z_exc`, while the homogenized numerator supplies the
nonzero binary form.  The nonzero condition is essential; if a cleared
numerator vanishes identically, the leaf family has entered a structured
exception branch rather than a bounded divisor gate.

The proof is the same: a nonzero homogeneous binary form of degree `d` has at
most `d` roots on `P^1(F)`, counted without multiplicity over the rational
points.

## Verification

The companion verifier checks finite-field root bounds, randomized divisor-gate
instances, projective binary-form gates, multiplicity sharpness, and the
composition with the popularity-cap support floor:

```sh
python3 experimental/scripts/verify_m1_popularity_divisor_gate.py
```
