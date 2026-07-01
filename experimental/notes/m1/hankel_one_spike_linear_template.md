# Hankel One-Spike Linear Template

Status: **PROVED / AUDIT**.

This note records a reusable non-proportional regular-minor template for the
Paper D v9 Hankel atlas.

Let `F` be a field, let `X` be a finite set of base nodes, and let `y` be a
single spike node.  Define syndrome moments

```text
u_m = sum_{x in X} x^m,
v_m = y^m.
```

For prefix size `r`, the regular Hankel matrix is

```text
H_r(u) + Z H_r(v) = V_X V_X^T + Z w_y w_y^T.
```

Thus the determinant is affine in the slope:

```text
Delta_r(Z) = C_0 + Z C_1,
```

with Cauchy-Binet coefficients

```text
C_0 = sum_{S subset X, |S|=r} Vandermonde(S)^2,
C_1 = sum_{T subset X, |T|=r-1} Vandermonde(T union {y})^2.
```

Consequently, if `C_1 != 0`, this non-proportional direction has the exact
regular-minor root table

```text
{-C_0/C_1}.
```

If `C_1=0` and `C_0 != 0`, the prefix regular minor has no finite root.  If both
vanish, this template identifies a singular residual bucket rather than
aperiodic evidence.

The certificate

```text
experimental/data/certificates/hankel-one-spike-linear-template/
  hankel_one_spike_linear_template_certificate.json
```

checks the identity over `F_17` for several non-proportional and singular-base
toy windows by comparing the Cauchy-Binet coefficients with direct determinant
evaluation at every finite slope.

Run:

```sh
python3 experimental/scripts/verify_m1_hankel_one_spike_linear_template.py \
  --check experimental/data/certificates/hankel-one-spike-linear-template/hankel_one_spike_linear_template_certificate.json
```

M3 relevance: this is the first reusable exact-root template in this PR for
non-proportional regular Hankel pencils.  It suggests a route to compact
`F_17^32` top-window packets whose determinants are linear in the slope, but it
does not itself provide an actual prize-row root table or quotient/tangent
subtraction ledger.
