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

## Non-Claims

This lemma does not bound the remaining different-slope one-exchange graph, the
two-exchange packet-edge ledger, or the one-outside boundary image.  It only
proves that same-slope one-exchange collisions belong to the fixed-slope
root-slice ledger.

## Verification

The dependency-free verifier

```bash
python3 experimental/scripts/verify_m1_same_slope_root_slice_lemma.py
```

checks the subtraction identity over sampled small prime fields and exhaustively
checks the row-wise linear-map implication in small dimensions.
