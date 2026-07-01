# Hankel Low-Rank Update Template

Status: **PROVED / AUDIT**.

This note records the finite-rank version of the one-spike regular-minor
template for the Paper D v9 Hankel atlas.

Let `F` be a field and let `X,Y` be disjoint finite node sets.  Define moments

```text
u_m = sum_{x in X} x^m,
v_m = sum_{y in Y} y^m.
```

For prefix size `r`,

```text
H_r(u) + Z H_r(v) = V_X V_X^T + Z V_Y V_Y^T.
```

Equivalently this is `V D(Z) V^T`, where `D(Z)` has diagonal entries `1` on
the `X` columns and `Z` on the `Y` columns.  Cauchy-Binet gives

```text
Delta_r(Z)
  =
  sum_{S subset X union Y, |S|=r}
    Vandermonde(S)^2 Z^{|S cap Y|}.
```

Thus

```text
deg Delta_r <= |Y|.
```

If `Delta_r` is nonzero, the finite bad-slope set captured by this regular
minor has size at most `|Y|`, independent of the Hankel minor size `r=j+1`.
If `Delta_r` vanishes identically, the bucket is a singular residual bucket and
must be passed to the v9 pivot/residual atlas rather than counted as aperiodic
evidence.

The certificate

```text
experimental/data/certificates/hankel-low-rank-update-template/
  hankel_low_rank_update_template_certificate.json
```

checks rank-one, rank-two, rank-three, and rank-deficient cases over `F_17` by
comparing the Cauchy-Binet coefficient formula with direct determinant
evaluation at every finite slope.

Run:

```sh
python3 experimental/scripts/verify_m1_hankel_low_rank_update_template.py \
  --check experimental/data/certificates/hankel-low-rank-update-template/hankel_low_rank_update_template_certificate.json
```

M3 relevance: this supplies a reusable branch theorem for non-proportional
syndrome pencils whose direction has small power-sum/Hankel rank.  It explains
why the one-spike packet has degree `1`, and it gives the next target shape:
find quotient/tangent/extension-removed M3 residuals whose regular direction
has bounded update rank, or prove that remaining high-rank directions must
enter the singular pivot atlas.

Non-claims: this is not an actual `F_17^32` prize-row table, does not classify
arbitrary non-proportional pencils, and does not perform quotient/tangent
subtraction.
