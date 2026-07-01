# F17^32 M3/M4 Regular-Bucket Synthesis

Status: AUDIT.

This directory composes the current M3/M4 regular-window lemmas for the pinned
row

```text
C = RS[F_17^32,H,256],    |H| = 512,
385 <= A <= 426.
```

It composes proved local certificates into a decision table for a regular pencil

```text
M_A(Z)=H_{t,j}(u)+Z H_{t,j}(v).
```

Closed by current lemmas:

```text
v=0 and rank H(u)=j+1:
  no finite affine roots;
  projective infinity is tangent/common-code-line paid.

v!=0, u=c v, and rank H(v)=j+1:
  the unique finite root z=-c is tangent/common-code-line paid;
  projective infinity is excluded.

u=0 and rank H(v)=j+1:
  the c=0 proportional subcase.
```

Finite/projective-safe with projective kernel accounting:

```text
v!=0, u not proportional to v, rank H(v)<=5, and the finite regular bucket is
nonsingular:
  finite affine root count <=5 and has zero tangent overlap;
  projective infinity contributes at most one endpoint;
  finite + projective contribution <=6.

v!=0, u not proportional to v, rank H(v)=6, and the finite regular bucket is
nonsingular:
  finite affine root count <=6, so the finite sampler is safe;
  the projective sampler is endpoint-sensitive and needs endpoint empty/paid
  or an exact finite root table with at most 5 surviving roots.
```

Still residual:

```text
rank-deficient finite regular buckets not covered by a paid family;
non-proportional finite buckets with direction rank >6 unless exact root
tables improve the bound;
rank-6 projective endpoint-sensitive buckets when the endpoint is not paid and
six finite roots survive;
quotient, extension, and subfield overlap for future non-proportional root
tables.
```

For projective samplers, a nonempty infinity kernel chart contributes the single
endpoint `[0:1]`.  Thus a finite-affine rank-`<=5` bucket is projective-budget
safe without an endpoint payment, while rank `6` is exactly the endpoint-sensitive
boundary.

The ambient sharpness packet

```text
experimental/data/certificates/hankel-f17-32-m3-m4-rank6-ambient-sharpness/
  f17_32_n512_k256_m3_m4_rank6_ambient_sharpness.json
```

shows that this boundary is real for arbitrary regular pencils: rank `6`, six
finite roots, and one projective endpoint can occur simultaneously.  The M3
rank-6 boundary must be attacked with Hankel-specific structure, exact root
tables, or a paid/empty endpoint ledger.

The rank-6 projective witness packet

```text
experimental/data/certificates/hankel-f17-32-m3-rank6-projective-witness/
  f17_32_n512_k256_m3_rank6_projective_witness.json
```

proves that the endpoint part of the boundary is Hankel-realizable.  On
`385 <= A <= 426`, a prefix-plus-six-spikes Hankel family has direction rank
`6`, empty finite canonical root table, and a genuine split-locator endpoint
at `[0:1]`; the first three finite-root closures come from the boundary
dual-gcd packet.  Thus endpoint emptiness cannot be used as a universal rank-6
closure argument.

The rank-node dichotomy packet

```text
experimental/data/certificates/hankel-f17-32-m3-rank-node-dichotomy/
  f17_32_n512_k256_m3_rank_node_dichotomy.json
```

gives the finite regular/singular gate.  If one tested finite slope has full
column rank, row elimination supplies a nonzero maximal minor.  If all `j+2`
deterministic finite test nodes have rank at most `j`, then every maximal minor
vanishes identically and the bucket is genuinely singular.

The null-polynomial split-locator gate

```text
experimental/data/certificates/hankel-f17-32-m3-nullpolynomial-split-locator-gate/
  f17_32_n512_k256_m3_nullpolynomial_split_locator_gate.json
```

separates ambient regular roots from actual support-wise split locators.  In a
nonsingular bucket, finite canonical roots are exactly ambient null-polynomials
`H(u+zv)ell=0`; a root becomes a split-locator witness only after `ell`
normalizes to a monic degree-`j` divisor of `X^512-1` and satisfies
`H(v)ell != 0`.

The projective split-locator gate

```text
experimental/data/certificates/hankel-f17-32-m3-projective-split-locator-gate/
  f17_32_n512_k256_m3_projective_split_locator_gate.json
```

is the endpoint companion.  The ambient infinity chart is
`H(v)ell=0, H(u)ell!=0`, but an actual support-wise endpoint witness still
requires `ell` to normalize to a monic degree-`j` divisor of `X^512-1`.  Thus
the rank-6 endpoint-sensitive branch must test the split-locator divisor gate
before counting or paying the projective endpoint.

The affine-pivot compression packet

```text
experimental/data/certificates/hankel-f17-32-m3-m4-affine-pivot-compression/
  f17_32_n512_k256_m3_m4_affine_pivot_compression.json
```

gives the finite-root table route a smaller target.  On a row-set chart with
finite pivot `z0` and `rank H_R(v)<=6`, the original `87..128` dimensional
maximal-minor determinant compresses to a `6 x 6` determinant with the same
finite roots in that affine pivot chart.

The gcd-equivalence companion

```text
experimental/data/certificates/hankel-f17-32-m3-m4-affine-pivot-gcd-equivalence/
  f17_32_n512_k256_m3_m4_affine_pivot_gcd_equivalence.json
```

shows that good pivots are plentiful for nonzero rank-6 minors and that the
v10 canonical gcd root set is preserved after replacing each chart by its
compressed determinant translated back to the global slope variable.

For finite affine roots, the M5 kernel chart gives a per-root filter:

```text
z survives the ambient affine noncontainment test
  iff ker(H(u)+zH(v)) is not contained in ker H(v).
```

If the containment holds, that root contributes nothing to the support-wise
noncontainment numerator.  If containment fails, it contributes at most the
single finite parameter `z` before split-locator, quotient, and extension
audits.

The regular-root rank-drop bridge explains why this filter applies directly to
v10 root tables:

```text
z root of canonical regular gcd
  => rank(H(u)+zH(v)) <= j.
```

In a nonsingular regular bucket the converse also holds for finite field
slopes.  Thus a regular root table is a rank-drop table.  Combining this with
the kernel filter shows that full-direction-rank regular roots always survive
same-support containment and must be handled by root counts plus the remaining
quotient, extension, subfield, or split-locator audits.

The filter also has a rank-stratification corollary: if
`rank H(v) > rank(H(u)+zH(v))`, then containment is impossible and `z` survives
the ambient noncontainment test.  Thus full-direction-rank finite regular roots
cannot be removed by this same-support kernel filter; they need actual root
tables and then quotient/extension/subfield audits.

This is not a worst-case row bound.  It is the current M4 decision table for
regular buckets after composing the proved local certificates.

Regenerate and check:

```sh
python3 experimental/scripts/verify_m1_hankel_m4_regular_bucket_synthesis.py \
  --write experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/f17_32_n512_k256_m3_m4_regular_bucket_synthesis.json

python3 experimental/scripts/verify_m1_hankel_m4_projective_budget_split.py \
  --check experimental/data/certificates/hankel-f17-32-m3-m4-projective-budget-split/f17_32_n512_k256_m3_m4_projective_budget_split.json

python3 experimental/scripts/verify_m1_hankel_m4_rank6_ambient_sharpness.py \
  --check experimental/data/certificates/hankel-f17-32-m3-m4-rank6-ambient-sharpness/f17_32_n512_k256_m3_m4_rank6_ambient_sharpness.json

python3 experimental/scripts/verify_f17_32_m3_rank6_projective_witness.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-projective-witness/f17_32_n512_k256_m3_rank6_projective_witness.json

python3 experimental/scripts/verify_f17_32_m3_rank6_boundary_dual_gcd.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-boundary-dual-gcd/f17_32_n512_k256_m3_rank6_boundary_dual_gcd.json

python3 experimental/scripts/verify_m1_hankel_m3_rank_node_dichotomy.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank-node-dichotomy/f17_32_n512_k256_m3_rank_node_dichotomy.json

python3 experimental/scripts/verify_m1_hankel_m3_nullpolynomial_split_locator_gate.py \
  --check experimental/data/certificates/hankel-f17-32-m3-nullpolynomial-split-locator-gate/f17_32_n512_k256_m3_nullpolynomial_split_locator_gate.json

python3 experimental/scripts/verify_m1_hankel_m3_projective_split_locator_gate.py \
  --check experimental/data/certificates/hankel-f17-32-m3-projective-split-locator-gate/f17_32_n512_k256_m3_projective_split_locator_gate.json

python3 experimental/scripts/verify_m1_hankel_m4_affine_pivot_compression.py \
  --check experimental/data/certificates/hankel-f17-32-m3-m4-affine-pivot-compression/f17_32_n512_k256_m3_m4_affine_pivot_compression.json

python3 experimental/scripts/verify_m1_hankel_m4_affine_pivot_gcd_equivalence.py \
  --check experimental/data/certificates/hankel-f17-32-m3-m4-affine-pivot-gcd-equivalence/f17_32_n512_k256_m3_m4_affine_pivot_gcd_equivalence.json

python3 experimental/scripts/verify_m1_hankel_m4_regular_bucket_synthesis.py \
  --check experimental/data/certificates/hankel-f17-32-m3-m4-regular-bucket-synthesis/f17_32_n512_k256_m3_m4_regular_bucket_synthesis.json
```
