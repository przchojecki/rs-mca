# M1 Same-Slope One-Exchange Root-Slice Lemma

**Status:** PROVED-LOCAL / ROOT-SLICE REDUCTION / AUDIT.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-29.

This note proves the first local reduction requested in
`m1_all_line_hankel_aperiodic_packet_audit.md`: same-slope one-exchange
collisions in the Hankel-pencil model are not a residual aperiodic codegree
phenomenon.  They force a whole fixed-slope root slice.

## Setup

Work in the Hankel-pencil normal form.  Let

```text
L_z = H_{t,j}(u)+zH_{t,j}(v)
```

be the finite-slope linear landing map on monic split locator polynomials of
degree `j`, with values in the `t` syndrome coordinates.  For a `(j-1)`-set
`R subset D` and `y in D\R`, write

```text
T_y=R union {y},        ell_{T_y}=(X-y)ell_R.
```

A finite-slope support `T_y` satisfies the slope equation when

```text
L_z ell_{T_y}=0.
```

The noncontainment condition `H_{t,j}(v)ell_{T_y} != 0` is a separate active
filter and is not used in the slice-forcing step.

## Lemma

Suppose `y_1 != y_2` and

```text
L_z ell_{T_{y_1}}=L_z ell_{T_{y_2}}=0.
```

Then

```text
L_z ell_R=0,        L_z(X ell_R)=0,
```

and consequently

```text
L_z ell_{T_y}=0        for every y in F.
```

In particular, every same-slope one-exchange edge is contained in the
fixed-slope root slice with core `R`.

## Proof

Since

```text
ell_{T_y}=X ell_R-y ell_R,
```

subtracting the two equations gives

```text
0=L_z(ell_{T_{y_1}}-ell_{T_{y_2}})
 =(y_2-y_1)L_z ell_R.
```

Thus `L_z ell_R=0`.  Substituting back into either endpoint equation gives

```text
0=L_z(X ell_R-y_1 ell_R)=L_z(X ell_R).
```

Therefore, for every scalar `y`,

```text
L_z ell_{T_y}=L_z(X ell_R-y ell_R)=0.
```

This proves the lemma.

## Residual Consequence

Let `A_res` be any active locator family after fixed-slope root slices have
been charged or removed.  Then the one-exchange graph on `A_res` has no
same-slope edges.  Equivalently, every residual one-exchange edge is a
different-slope edge:

```text
{T,T'} subset A_res, |T cap T'|=j-1
    => z_T != z_T'.
```

Thus the one-exchange codegree residual in the all-line Hankel program is
exactly the different-slope one-exchange ledger after root-slice charging.
This is useful because it prevents same-slope multiplicity from being counted
again as an aperiodic residual obstruction.

## The `t=2` Determinant Gate

In the `t=2` Hankel window there is a second elementary one-exchange
separation.  For a fixed `(j-1)`-core `R`, put

```text
a_y=H(u)ell_{T_y},        b_y=H(v)ell_{T_y}        in F^2.
```

Since `ell_{T_y}=Xell_R-yell_R`, there are vectors
`a_X,a_0,b_X,b_0 in F^2` such that

```text
a_y=a_X-y a_0,        b_y=b_X-y b_0.
```

The finite-slope determinant gate is

```text
Delta_R(y)=det(a_y,b_y)=0,        b_y != 0.
```

The determinant is a polynomial of degree at most two:

```text
Delta_R(y)
 =
 det(a_X,b_X)
 - y(det(a_0,b_X)+det(a_X,b_0))
 + y^2 det(a_0,b_0).                              (DET2)
```

Consequently, if `Delta_R` is not the zero polynomial, at most two anchors
`y in F` can pass the determinant gate.  If three distinct anchors pass the
determinant gate, then `Delta_R` vanishes identically and the core `R` lies in
a ruled determinant branch:

```text
det(a_y,b_y)=0        for every y in F.
```

After fixed-slope root slices have been charged, this says that any fixed core
supporting three or more residual one-exchange anchors must be ruled but not
same-slope.  Non-ruled cores contribute at most one unordered one-exchange edge
through that core.

## Non-Ruled One-Exchange Degree Bound

Let `A_nr` be a residual `t=2` active locator family after fixed-slope root
slices and ruled determinant cores have been charged or removed.  Let
`G_1(A_nr)` be its one-exchange graph:

```text
T ~ T'        iff        |T cap T'|=j-1.
```

Then every vertex has one-exchange degree at most `j`:

```text
Gamma_1(A_nr) <= j.                              (DEG1)
```

Indeed, a locator `T` has exactly `j` possible `(j-1)` cores `R=T\{y}`.  For
each such core, the non-ruled determinant gate leaves at most two anchors in
total.  Since one of them is the anchor defining `T`, there is at most one
neighbor of `T` through that core.  Summing over the `j` cores gives (DEG1).

Equivalently, if `E_1(A_nr)` denotes unordered one-exchange edges, then

```text
E_1(A_nr) <= j |A_nr| / 2,
E_1(A_nr) <= binom(|D|,j-1).                     (EDGE1)
```

The second bound counts cores directly: after ruled cores are removed, each
core supports at most one unordered edge.  Thus high one-exchange codegree in
the `t=2` all-line Hankel branch can only come from fixed-slope root slices or
ruled determinant cores.

## Non-Claims

This lemma does not bound the remaining different-slope one-exchange graph, the
ruled determinant branch, the two-exchange packet-edge ledger, or the
one-outside boundary image.  It only proves that same-slope one-exchange
collisions belong to the fixed-slope root-slice ledger and that non-ruled
`t=2` one-exchange cores have at most two determinant anchors, giving the
local max-degree bound above.

## Verification

The dependency-free verifier

```bash
python3 experimental/scripts/verify_m1_same_slope_root_slice_lemma.py
```

checks the subtraction identity over sampled small prime fields and exhaustively
checks the row-wise linear-map implication in small dimensions.  It also checks
the quadratic determinant formula (DET2) and the "three roots imply ruled"
criterion in sampled small prime fields.
