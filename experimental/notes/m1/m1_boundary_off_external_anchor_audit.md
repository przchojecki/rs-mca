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

1. Prove polynomial bounds for the non-ruled external-anchor branch.
2. Charge fixed-slope boundary root slices to the lifted Hankel ledger.
3. Keep the primitive quotient-normal target separate from exact quotient
   support budgets.

## Non-Claims

This note does not prove the all-line M1 polynomial packing theorem.  It gives
a per-shadow quadratic cap after the fixed-slope boundary slices are charged,
but it does not bound the total `|Boundary_off|`, does not give a leaderboard
row, and does not change any public MCA or interleaved-list threshold.
