# XR light-triangle eliminant normal form (2c-beta-3a)

DAG node: `xr_triangle_eliminant_form`.

Status: PROVED as a construction.

## Statement

Let `C` be a length-`n`, dimension-`k` Reed-Solomon evaluation code on
distinct field points `H`, and write `A = k + t`.

For agreement supports `T_0,T_1,T_2`, each of size `A`, define

```text
Lambda_i = { lambda in C^perp : supp(lambda) subset T_i }.
```

For distinct finite slopes `z_0,z_1,z_2`, a triangle syzygy is a nonzero
triple `lambda_i in Lambda_i` satisfying

```text
lambda_0 + lambda_1 + lambda_2 = 0,
z_0 lambda_0 + z_1 lambda_1 + z_2 lambda_2 = 0.
```

Choose a chart basis `B_i` for each `Lambda_i`.  In MDS coordinates, take
`k` pivot points of `T_i`, take the remaining `t` coordinates as free, and
solve the `k x k` Vandermonde system.  This gives an `n x t` matrix `B_i`.

Let `U = T_0 union T_1 union T_2`.  The normal-form matrix is

```text
E(T,z) : F^{3t} -> F^U x F^U

(a_0,a_1,a_2) |-> (
    B_0 a_0 + B_1 a_1 + B_2 a_2,
    z_0 B_0 a_0 + z_1 B_1 a_1 + z_2 B_2 a_2
).
```

Then a triangle syzygy exists if and only if

```text
rank E(T,z) < 3t.
```

Equivalently, the light-triangle eliminant locus is the determinantal locus
where all `3t x 3t` minors of `E(T,z)` vanish.  On a fixed chart, clearing the
Vandermonde pivot denominators turns these minors into explicit polynomials
in the support coordinates and slopes.

## Twisted Form

Subtracting `z_2` times the first component from the second component is an
invertible row operation on `F^U x F^U`.  Thus the same determinantal locus is
given by

```text
(a_0,a_1,a_2) |-> (
    B_0 a_0 + B_1 a_1 + B_2 a_2,
    (z_0-z_2) B_0 a_0 + (z_1-z_2) B_1 a_1
).
```

The twists are nonzero because the slopes are distinct.  This is the explicit
normal form used by the 2c-alpha support-budget bookkeeping and by the
light-triangle residue.

## Light Regime

For pairwise overlaps `r_ij = |T_i cap T_j|` and triple overlap
`r_012 = |T_0 cap T_1 cap T_2|`, the DAG's light side is

```text
r_01 + r_02 + r_12 - r_012 <= 2k.
```

This packet does not classify the vanishing locus.  It supplies the exact
matrix whose rank drop is the locus to classify.  The structured/paid branch
remains `xr_eliminant_vanishing_class`; the population bound remains under
`xr_light_triangle_eliminant`.

## Verifier

`experimental/scripts/verify_xr_triangle_eliminant_form.py` builds chart
bases by solving the Vandermonde pivot systems and compares:

- the normal-form rank;
- the twisted-form rank;
- the brute stacked alignment-row rank in `F^H x F^H`;
- the rank-drop criterion `kernel_dim > 0 iff rank < 3t`.

It exhausts all ordered triples for `F_7, n=6, k=2, A=4`, which includes
rank-defect examples outside the light regime, and exhausts all light triples
for `F_11, n=8, k=2, A=4`.

The recomputed summary is pinned in
`experimental/data/certificates/xr-triangle-eliminant-form/toy_triangle_eliminant.json`.
