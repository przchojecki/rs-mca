# XR Light-Profile Eliminant Nonvanishing

Status: PROVED.

Source DAG node: `xr_profile_eliminant_nonvanishing`.

## Statement

Let `F` be a field, let `x_u` be distinct evaluation points, and let
`T_0,T_1,T_2` be three support sets of common size `A = k + t`.  For each
support, define

```text
Lambda_T = {lambda supported on T :
            sum_{u in T} lambda_u x_u^d = 0 for d = 0,...,k-1}.
```

Thus `dim Lambda_T = t` by Vandermonde shortening.

Fix pairwise distinct slopes `z_0,z_1,z_2` and form the normal-form map

```text
Phi_z : Lambda_{T_0} + Lambda_{T_1} + Lambda_{T_2} -> F^U + F^U

(lambda_0,lambda_1,lambda_2)
  |-> (lambda_0 + lambda_1 + lambda_2,
       z_0 lambda_0 + z_1 lambda_1 + z_2 lambda_2),
```

where `U = T_0 union T_1 union T_2` and each `lambda_i` is extended by zero
outside `T_i`.

If the triple is light,

```text
|T_0 cap T_1| + |T_0 cap T_2| + |T_1 cap T_2| - |T_0 cap T_1 cap T_2| <= 2k,
```

then `Phi_z` is injective.  Equivalently, the normal-form matrix has rank
`3t`, so at least one `3t x 3t` maximal minor is a nonzero polynomial in the
support coordinates and slopes.  In particular no unpaid non-boundary
light-triangle profile has an identically vanishing eliminant.

## Proof

Write

```text
I = T_0 cap T_1 cap T_2,    r = |I|.
```

Since `I` lies in every pairwise intersection,

```text
|T_0 cap T_1| + |T_0 cap T_2| + |T_1 cap T_2| - |I| >= 2r.
```

The light inequality therefore implies `r <= k`.

Now take `(lambda_0,lambda_1,lambda_2) in ker Phi_z`.

At a point `u` that belongs to exactly one support, the two output rows force
the corresponding `lambda_i(u)` to be zero.

At a point `u` that belongs to exactly two supports, say `T_i` and `T_j`, the
two equations are

```text
lambda_i(u) + lambda_j(u) = 0,
z_i lambda_i(u) + z_j lambda_j(u) = 0.
```

The determinant is `z_j - z_i`, nonzero by the pairwise-distinct slope
assumption, so both values are zero.

Thus every `lambda_i` is supported only on the triple intersection `I`.
But `lambda_i in Lambda_{T_i}`, so for `d = 0,...,k-1`,

```text
sum_{u in I} lambda_i(u) x_u^d = 0.
```

The `k x r` Vandermonde matrix on the distinct points of `I` has full column
rank because `r <= k`.  Hence `lambda_i|_I = 0` for each `i`, so the kernel is
trivial and `Phi_z` is injective.

The entries of the normal-form matrix are polynomial/rational functions in the
profile coordinates on each Vandermonde chart.  Since `Phi_z` has full column
rank at every admissible specialization with distinct slopes, some maximal
minor is nonzero; after clearing the chart Vandermonde denominators, this is a
nonzero polynomial certificate for the profile.

## Program Use

This packet removes the "identically vanishing light profile" branch from the
XR route.  Remaining coordinate-special light-triangle failures, if any, live
on proper hypersurfaces inside the profile cell and should be charged by the
separate staircase/SPI/XR counting machinery.

In the current v13 final-resolution language, this is a proved local XR input
for the `paid_M1_aperiodic_or_SPI_layer(a)` branch.  It is not by itself an
adjacent deployed upper certificate: it must be combined with the row-packet
paid-cell compiler and residual counting bounds.

## Replay

The verifier enumerates small Venn-profile light triples and checks that the
normal-form matrix has rank `3t` over a prime field:

```bash
python3 experimental/scripts/verify_xr_light_profile_eliminant_nonvanishing.py
python3 experimental/scripts/verify_xr_light_profile_eliminant_nonvanishing.py --emit
```

The finite replay is only a schema guard; the proof above is the parametric
argument.
