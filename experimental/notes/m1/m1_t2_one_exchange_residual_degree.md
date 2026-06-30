# M1 t=2 one-exchange residual degree

**Status:** PROVED-LOCAL / AUDIT.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-30.

This note extracts a compact `t=2` one-exchange package from the broad
same-slope packet in PR #138.  It is intended as a small modular lemma after
the root-slice split: once fixed-slope root slices have been charged, the
actual Hankel shift structure prevents ruled determinant cores from creating a
separate residual one-exchange multiplicity.

## Scope and non-claims

This is local algebra in the `t=2` Hankel-pencil normal form.  It does not
prove the all-line M1 aperiodic local limit, does not bound the global
residual slope image, and does not add a leaderboard or threshold row.

Field ledger: the statement is over an arbitrary field `F`.  In an MCA
application the slope is a finite line slope in `q_line`.  No generated-field,
challenge-field, denominator, or radius endpoint convention enters this local
step.  Domain-root, split-root, quotient-periodic, tangent/contained, and
noncontainment filters are external filters; they can only shrink the residual
families considered below.

## Setup

Fix a `t=2` Hankel-pencil instance.  For a `(j-1)` core `R`, write

```text
T_y = R union {y},        ell_{T_y} = (X-y)ell_R.
```

Put

```text
a_y = H_{2,j}(u) ell_{T_y},
b_y = H_{2,j}(v) ell_{T_y}        in F^2.
```

Because `ell_{T_y}=Xell_R-yell_R`, there are vectors
`a_X,a_0,b_X,b_0 in F^2` such that

```text
a_y = a_X - y a_0,
b_y = b_X - y b_0.
```

The finite noncontained slope condition at this core is

```text
b_y != 0,        det(a_y,b_y)=0.
```

When this holds, the finite slope is the unique `z` such that

```text
a_y + z b_y = 0.
```

## Lemma 1: quadratic determinant gate

The one-exchange determinant is a polynomial of degree at most two:

```text
Delta_R(y) = det(a_y,b_y)
 =
 det(a_X,b_X)
 - y(det(a_0,b_X)+det(a_X,b_0))
 + y^2 det(a_0,b_0).                              (DET2)
```

Consequently, if `Delta_R` is not the zero polynomial, at most two anchors
`y in F` pass the determinant gate.  If three distinct anchors pass, then
`Delta_R` is identically zero and the core is ruled:

```text
det(a_y,b_y)=0        for every y in F.
```

## Lemma 2: Hankel ruled-core collapse

The ruled branch has no moving-slope residual in the actual Hankel
one-exchange setting.  For any syndrome vector `w`, write

```text
c_i(w) = row_i(H_{3,j-1}(w) ell_R),        i=0,1,2.
```

Then

```text
H_{2,j}(w) ell_{T_y}
 =
 (c_1(w)-y c_0(w),  c_2(w)-y c_1(w)).             (SHIFT)
```

Assume

```text
det(a_y,b_y)=0        for every y.
```

Then either

```text
b_y = 0        for every y,
```

or there is a fixed finite slope `z_0 in F` such that

```text
a_y + z_0 b_y = 0        for every y.              (HC)
```

### Proof

Write

```text
a_y=(a_1-y a_0, a_2-y a_1),
b_y=(b_1-y b_0, b_2-y b_1),
```

where `a_i=c_i(u)` and `b_i=c_i(v)`.  Expanding the determinant gives

```text
det(a_y,b_y)
 =
 (a_1 b_2-a_2 b_1)
 + y(a_2 b_0-a_0 b_2)
 + y^2(a_0 b_1-a_1 b_0).
```

If this polynomial is identically zero, all three adjacent minors vanish:

```text
a_0 b_1=a_1 b_0,
a_0 b_2=a_2 b_0,
a_1 b_2=a_2 b_1.
```

Thus the triples `(a_0,a_1,a_2)` and `(b_0,b_1,b_2)` are proportional.  If the
`b` triple is zero, then `b_y=0` for every `y`, so the active finite-slope
filter removes the core.  Otherwise choose `z_0` with

```text
a_i + z_0 b_i = 0        for i=0,1,2.
```

Then `(SHIFT)` gives `a_y+z_0 b_y=0` for every `y`.

So every active ruled Hankel core is already a fixed-slope core.  After
fixed-slope root slices have been charged, ruled determinant cores contribute
no residual one-exchange edges.

## Theorem: residual one-exchange degree bound

Let `A_res` be any residual active `t=2` locator family after fixed-slope root
slices have been charged or removed.  Let `G_1(A_res)` be its one-exchange
graph:

```text
T ~ T'        iff        |T cap T'|=j-1.
```

Then

```text
Delta(G_1(A_res)) <= j.                            (DEG1)
```

Indeed, a locator `T` has exactly `j` possible `(j-1)` cores `R=T\{y}`.  For
each such core, Lemma 1 leaves at most two anchors unless the core is ruled.
In the non-ruled case, a fixed core can therefore supply at most one residual
neighbor of `T`.  In the ruled case, Lemma 2 says the core is inactive or
fixed-slope; an active fixed-slope core with two anchors is exactly a
fixed-slope root-slice event and has already been charged.  Hence each of the
`j` cores supplies at most one residual neighbor.

Equivalently, if `E_1(A_res)` is the set of unordered one-exchange edges, then

```text
|E_1(A_res)| <= j |A_res| / 2,
|E_1(A_res)| <= binom(|D|,j-1).                   (EDGE1)
```

The second bound counts cores directly: after fixed-slope root-slice charging,
each `(j-1)` core supports at most one residual one-exchange edge.

Thus high one-exchange multiplicity in the `t=2` all-line Hankel branch can
only come from the fixed-slope root-slice ledger, not from a separate
ruled-core residual.

## Average-collinearity corollary

The degree bound plugs into the average support-collinearity ledger in
`experimental/notes/m1/m1_average_support_collinearity.md`.  To avoid a
notation clash with locator degree `j`, write the line-field size as `Q`.
For `t=2`, that ledger has the max-codegree form

```text
B_2^max(A) = (1-p_z)/(M p_z) + (4/M) Delta(G_1(A)) Q,
p_z = Q^(-2)(1-Q^(-2)),        M=|A|.
```

Therefore the residual family after fixed-slope root-slice charging satisfies

```text
B_2^max(A_res) <= (1-p_z)/(M p_z) + 4jQ/M.        (AVG1)
```

This is not a worst-case M1 packing theorem.  It identifies the remaining
average-ledger obstruction after this local reduction: small residual family
size, fixed-slope root slices, or higher two-exchange/top-packet structure.

## Verification

The companion verifier checks the determinant expansion, root-count gate,
Hankel ruled-core collapse, residual Johnson-graph degree bound, and the
average-collinearity substitution over small exact finite fields:

```sh
python3 experimental/scripts/verify_m1_t2_one_exchange_residual_degree.py
```
