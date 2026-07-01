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

There is also a compressed form when the base block is nonsingular.  Put

```text
H_X = V_X V_X^T,
K = V_Y^T H_X^{-1} V_Y.
```

Then the matrix determinant lemma gives

```text
Delta_r(Z) = det(H_X) det(I + Z K).
```

This replaces the `r x r` determinant by a `|Y| x |Y|` determinant without
weakening the root bound.  This is the useful form for large M3 packets: the
minor size may be `87` or `128`, while the update kernel can still be rank
`1`, `2`, or another small constant.  If `H_X` is singular, this compressed
identity is not invoked; Cauchy-Binet, direct replay, or another regular chart
must be used.  The bucket becomes a singular residual only when `Delta_r`
itself vanishes.

For update rank `2` in odd characteristic, the compressed determinant is a
quadratic.  Thus exact root counting is controlled by the discriminant:

```text
Delta(Z)=aZ^2+bZ+c,
D=b^2-4ac.
```

If `D` is a square, the finite roots are `(-b +- sqrt(D))/(2a)`; if `D` is a
nonsquare, this regular-minor chart contributes no finite root.  The template
certificate records this gate over `F_17`, including split, repeated-root, and
nonsquare no-root rows.

The certificate

```text
experimental/data/certificates/hankel-low-rank-update-template/
  hankel_low_rank_update_template_certificate.json
```

checks rank-one, rank-two, rank-three, and rank-deficient cases over `F_17`.
For each nonsingular base block it verifies both the Cauchy-Binet coefficient
formula and the compressed determinant-lemma formula against direct determinant
evaluation at every finite slope.  For rank-two rows it also checks that the
discriminant formula gives the same roots as direct evaluation.

The extension-field packet

```text
experimental/data/certificates/hankel-f17-2-low-rank2-nonsquare-toy/
  f17_2_n10_k4_a8_low_rank2_nonsquare_packet.json
```

exercises the packet-level no-root branch: its compressed quadratic has
nonsquare discriminant over `F_17^2`, and the checker verifies the Euler
witness before accepting the empty root table.

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

The first `F_17^32` rank-2 instantiation is

```text
experimental/data/hankel-regular-minor-inputs/
  f17_32_n512_k256_a426_low_rank2_input.json

experimental/data/certificates/hankel-f17-32-m3-low-rank2-a426/
  f17_32_n512_k256_a426_low_rank2_packet.json
```

At `A=426`, where `j=86` and the prefix minor has size 87, this packet uses two
update nodes and proves a degree-2 regular-minor bound.  The compressed
quadratic splits over `F_17^32`, so the packet now records the exact two roots,
their split-linear factorization certificate, a quadratic discriminant
certificate, and `declared_aperiodic_numerator = 2`.  The packet checker
replays the low-rank moments, the compressed Lagrange-kernel determinant
coefficients, the sidecar itself, and the quadratic formula.  The companion
invalid fixtures mutate one coefficient, one kernel entry, one root table, and
one quadratic square root, respectively, and all are required to fail replay.

For extension-field low-rank packets, the extractor and checker now use the
compressed determinant-lemma coefficients as the primary replay path:

```text
Delta_r(Z)=det(H_X) det(I+ZK).
```

The Cauchy-Binet identity remains the theorem behind the template certificate,
but packet replay no longer has to recompute the large-minor coefficient sums
before checking the small kernel sidecar.  This is the scalable path for future
rank-3 or higher low-rank stress packets.  The Lagrange-kernel replay also uses
the barycentric formula

```text
L_i(y)=prod_j(y-x_j)/((y-x_i) prod_{j != i}(x_i-x_j))
```

with batch inversion for the denominators and update differences, so a
large-field endpoint packet needs only a few exponentiation-based inversions
instead of one inversion per basis value.

The all-window synthetic family certificate is

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank2-family/
  f17_32_n512_k256_m3_low_rank2_family_certificate.json
```

It applies the same rank-2 compressed kernel to every agreement in the M3
regular window `385 <= A <= 426`, using nested descriptor-domain prefixes for
`X` and the next two descriptor nodes for `Y`.  The verifier reuses prefix
Vandermonde denominators and base determinants, cross-checks the `A=426`
endpoint against the exact-root v9 packet, and applies the rank-2 discriminant
gate to every row.  The degree cap is `2 * 42 = 84`, but the exact synthetic
finite-root total is `40`: 20 split quadratics and 22 nonsquare quadratics.
The generic degree-bound sum for the same window would be `4515`.

Non-claims: this is not an actual `F_17^32` prize-row table, does not classify
arbitrary non-proportional pencils, and does not perform quotient/tangent
subtraction.
