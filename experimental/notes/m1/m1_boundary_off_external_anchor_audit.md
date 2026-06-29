# M1 Boundary-Off External-Anchor Audit

Date: 2026-06-29

Source PR: #131, AllenGrahamHart.

Updated by PR #138, AllenGrahamHart / Codex.

Status: PROVED-LOCAL / RULED-BRANCH CLASSIFIED / PROOF-PROGRAM / AUDIT.

## Claim Distilled

The PR isolates the one-outside `Boundary_off` residual in the M1 Hankel-pencil
program.  For a domain shadow `S subset D` of size `j-1` and an external anchor
`beta notin D`, the one-outside locator has the affine form

```text
ell_{S,beta} = ell_S^+ - beta ell_S^0.
```

Consequently the Hankel landing matrix

```text
M_S(beta) =
[ H(u) ell_{S,beta}   H(v) ell_{S,beta} ]
```

has columns affine-linear in `beta`, and the rank-one landing condition is
equivalent to quadratic minor equations in `beta`.

For fixed `S`, either one of these quadratic minors is nonzero, giving at most
two external anchors, or all minors vanish identically and the branch is a ruled
rank-one pencil.  In the `t=2` case this gives a three-scalar coefficient test
for the ruled branch.

The ruled `t=2` Hankel branch is now classified by
`m1_same_slope_root_slice_lemma.md`.  Writing

```text
c_i(w)=row_i(H_{3,j-1}(w)ell_S),        i=0,1,2,
```

one has

```text
H_{2,j}(w)ell_{S,beta}
 =
 (c_1(w)-beta c_0(w), c_2(w)-beta c_1(w)).
```

If the affine landing pencil is ruled, the Hankel shift collapse forces it to
be inactive or fixed finite slope:

```text
H_{2,j}(v)ell_{S,beta}=0        for every beta,
```

or

```text
(H_{2,j}(u)+z_0H_{2,j}(v))ell_{S,beta}=0
        for every beta.
```

The fixed finite-slope case is a boundary root slice and lifts to

```text
H_{3,j-1}(u+z_0v)ell_S=0.
```

Thus, after fixed-slope boundary root slices are charged, each shadow `S`
supports at most two active non-ruled external anchors.  The ruled
external-anchor branch no longer has to be mixed into quotient-periodic mass.

The same root-slice subtraction gives the shadow-image form now recorded in
`m1_same_slope_root_slice_lemma.md`.  If two external anchors over the same
shadow have the same finite slope `z`, then the lifted boundary core

```text
H_{3,j-1}(u+zv)ell_S=0
```

has already been charged.  Therefore, in the residual family, the projection

```text
S union {beta} |-> S
```

has fibers of size at most two and the finite-slope labels inside each fiber
are distinct.  Equivalently,

```text
|Boundary_off^res| <= 2 |Shadow_off^res|.
```

The remaining global task is to bound the shadow image, not to handle
uncontrolled external-anchor multiplicity over a fixed shadow.

There is also no hidden quantifier over external anchors in that shadow task.
For a fixed finite slope `z`, write

```text
c_i=row_i(H_{3,j-1}(u+zv)ell_S),        0<=i<=2.
```

Then `H_{2,j}(u+zv)ell_{S,beta}=0` for some `beta` iff either the lifted
boundary core is already zero,

```text
(c_0,c_1,c_2)=(0,0,0),
```

or

```text
c_0 != 0,        c_1^2=c_0c_2,        beta=c_1/c_0.
```

Thus the residual shadow-image problem is a scalar rank-one Hankel condition
on `S`, with the recovered anchor required to lie outside `D` and satisfy the
usual active filter.

## Integration Decision

The full PR was not merged wholesale.  It included a very large generated
draft, stale site/Paper D changes, and proof-program material that should not
be promoted as a solved M1 theorem.  The useful content is this local normal
form and the suggested exact primitive quotient-normal target.

The exact target proposed in the PR is:

```text
|Bad_nc(f,g,a)| <= M1QuotBudget(f,g,a) + n^B
```

after tangent, contained, quotient-periodic, presentation, reciprocal, and
finite-domain alias contributions have been charged.  This remains
CONJECTURAL / FALSIFICATION-FIRST.

## Use

This note is useful for the M1 residue-line local-limit program because it
turns the opaque one-outside boundary image into an explicit external-anchor
incidence problem.  It gives a route for future agents:

1. Prove polynomial bounds for the residual boundary shadow image.
2. Charge fixed-slope boundary root slices to the lifted Hankel ledger.
3. Keep the primitive quotient-normal target separate from exact quotient
   support budgets.

## Non-Claims

This note does not prove the all-line M1 polynomial packing theorem.  It gives
a per-shadow quadratic cap and the shadow-fiber reduction after the fixed-slope
boundary slices are charged, but it does not bound the total shadow image, does
not give a leaderboard row, and does not change any public MCA or
interleaved-list threshold.
