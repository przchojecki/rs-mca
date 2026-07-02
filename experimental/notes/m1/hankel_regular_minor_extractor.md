# Regular Hankel-Minor Extractor

**Status:** EXPERIMENTAL / AUDIT, with a proved finite toy replay.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-30.

This note records the first reusable extractor for the regular overdetermined
bucket in the Paper D v12 Hankel atlas.  It addresses the next item in
`towards-prize.md`:

```text
Regular-minor extractor.
Given row data and exact agreement A, compute candidate nonzero minors
and root-count bounds.
```

## Extractor Scope

The script

```text
experimental/scripts/extract_regular_hankel_minors.py
```

reads a syndrome-pencil input over either a prime field `F_p` or an explicit
polynomial-basis extension field.  For each exact agreement `A`, it
sets

```text
j = n-A,
t = A-k.
```

If `t >= j+1`, it tries candidate `(j+1) x (j+1)` Hankel row minors of

```text
H_{t,j}(u) + Z H_{t,j}(v).
```

The current candidate schedule is data-driven: explicit row sets, prefix row
sets, a bounded scan of contiguous row windows, or the `rank_at_nodes` selector.
The rank selector evaluates the matrix pencil at `j+2` deterministic finite
slopes.  If the pencil has full column rank over `F(Z)`, some maximal minor has
degree at most `j+1`, so it cannot vanish at all `j+2` nodes; a full-rank
specialization supplies a row set whose determinant polynomial is nonzero.  If
no full-rank specialization appears at those nodes, all maximal minors vanish
identically and the regular bucket is genuinely singular.  Rank-at-nodes packet
audits now list the tested deterministic nodes, so the v9 checker can reject
underchecked or non-distinct singularity proofs.

The standalone proof/audit note

```text
experimental/notes/m1/rank_at_nodes_regular_bucket_lemma.md
```

isolates this rank-at-nodes dichotomy as a reusable theorem.  Its companion
certificate audits every current v9 packet item using the `rank_at_nodes`
selector.

The follow-up note

```text
experimental/notes/m1/rank_node_family_gcd_gate.md
```

combines this selector with the common-gcd gate.  A bounded deterministic scan
of rank nodes records every distinct full-rank row set it witnesses; the common
gcd of those determinant polynomials still contains every regular-bad finite
slope, while extra scanned nodes only sharpen the gcd and do not change the
`j+2` singularity proof obligation.

The determinant polynomial is recovered by interpolation from numeric
determinants, rather than by a factorial permutation determinant.  This is the
right algorithmic shape for the future `385 <= A <= 426` window once row data
for the `F_17^32` row are supplied.

A sharper regular-bucket gate is recorded in

```text
experimental/data/certificates/regular-minor-gcd-gate/
experimental/data/certificates/regular-minor-gcd-toy/
experimental/data/certificates/regular-minor-gcd-f17-2-toy/
experimental/data/certificates/regular-minor-gcd-f17-32-toy/
experimental/data/certificates/regular-minor-gcd-f17-32-zero-u-toy/
experimental/data/certificates/regular-minor-gcd-rank-node-family-toy/
experimental/data/certificates/regular-minor-gcd-projective-toy/
experimental/scripts/verify_m1_regular_minor_gcd_gate.py
```

If a slope is genuinely regular-bad, the full Hankel matrix has rank at most
`j`, so every maximal minor vanishes there.  Thus the bad slopes are contained
in the roots of the gcd of any audited family of maximal-minor determinant
polynomials.  On the `F_17`, `n=16`, `k=8` toy, the common gcd of all contiguous
maximal minors removes prefix-minor false roots at `A=14,15,16`.  The extractor
now emits this as a `regular_minor_gcd` v9 packet over prime fields and
polynomial-basis extension fields.  The checker verifies gcd divisibility,
exact roots in small fields, degree-bound root hashes in large fields, and
replays each recorded minor polynomial against the SHA-checked extractor input
at `j+2` finite slopes.  It also recomputes the monic common gcd of the
audited nonzero minors; divisibility by the advertised polynomial is not enough,
because a proper common divisor can miss simultaneous rank-defect roots.
The `F_17^2` replay checks exact extension roots; the first `F_17^32` toy uses
the pinned extension-field model and reports a degree bound without enumerating
the slope field.

There is also a closed-form `zero_u_monomial` common-gcd mode for zero-`u`
pencils.  In this case every audited nonzero maximal minor has the form
`c Z^(j+1)`, so the extractor computes only the leading determinant of each row
set, takes the common gcd, and emits the exact root table `{0}` with a
split-linear root certificate.  The packet checker independently verifies the
gcd divisibility, reconstructs the split-linear certificate, and uses the
visible monomial form to require the exact large-field root table `{0}` without
enumerating `F_17^32`.

The rank-node family gcd replay uses the same `F_17`, `n=16`, `k=8` toy as the
contiguous gcd packet, but obtains its row sets from deterministic full-rank
specializations.  With `node_limit=17`, it audits row-set counts
`1,2,3,2` for `A=13,14,15,16` and gets the same final root union `{11}` as the
all-contiguous replay.  The checker verifies that each gcd row set is backed by
a recorded full-rank witness node, and now evaluates the recorded determinant
polynomial at that node to confirm the witness is genuinely nonzero.

For projective-line common-gcd packets, the endpoint `[0:1]` is audited from
the whole minor family, not from the affine common gcd alone.  Infinity is empty
if at least one audited maximal-minor homogenization has nonzero top
coefficient; if every audited top coefficient vanishes, the packet must pay one
projective endpoint.  The projective gcd toy records all per-minor top
coefficients and the checker recomputes them from the minor-polynomial table.

When the field is small enough, the extractor enumerates roots in the full
finite slope field.  For extension fields, root-table elements are encoded as
base-`p` low-to-high integers so the existing v9 packet checker can audit root
hashes and declared numerators.  When the domain is supplied and the
split-locator subset count is small enough, it also enumerates split co-support
bad slopes and checks that they are contained in the extracted root set.

## Toy Replay

The replay input is

```text
experimental/data/hankel-regular-minor-inputs/f17_n16_k8_a13_toy.json
```

and the output packet is

```text
experimental/data/certificates/regular-minor-extractor-toy/
  f17_n16_k8_a13_regular_minor_extractor_packet.json
```

It uses the same toy row as the first regular-minor certificate:

```text
F = F_17,
D = F_17^*,
n = 16,
k = 8,
A = 13,14,15,16.
```

For inline ordinary `regular_minor` packets with row-set size at most `16`,
the generic checker now SHA-loads the extractor input and replays the recorded
determinant polynomial at `j+2` finite slopes.  This catches scaled or otherwise
fabricated determinant polynomials even when their root tables are still
internally consistent.  Larger closed-form `F_17^32` packets remain covered by
their compressed-root certificates and should get dedicated closed-form replay
gates rather than brute-force interpolation.

The closed-form scalar/zero-u packets now have a cheaper replay path.  The
checker verifies the visible input relation `u=c v`, verifies that the inline
polynomial is exactly `C(Z+c)^(j+1)`, and for row-set size at most `16`
recomputes the leading Hankel determinant `C` from the input.  For the deployed
`F_17^32` packets this avoids impractical repeated large determinant
interpolation while still tying the repeated-root location to the SHA-checked
syndrome pencil.

For the prefix synthetic `F_17^32` packets, the checker now also replays the
large leading coefficient from the checked-in row descriptor.  It verifies that
the input syndrome has

```text
v_m = sum_i x_i^m
```

for the advertised first descriptor-domain nodes.  If the witness-node count
equals the minor size, the leading coefficient is replayed as the
Vandermonde-square determinant.  For the fixed `A=421..426` top-window packet,
where the same `92` witness nodes feed smaller prefix minors, the checker
performs one cached prefix-Hankel elimination and reuses the leading principal
determinants.  Thus the deployed closed-form packets no longer trust an
arbitrary leading scalar.

The extractor finds nonzero prefix minors in all four exact agreements, with
degrees `4,3,2,1` and closed-range root union `{0,2,10,11}`.

The projective-line replay is

```text
experimental/data/hankel-regular-minor-inputs/f17_n16_k8_a13_projective_toy.json
experimental/data/certificates/regular-minor-extractor-projective-toy/
```

It uses the same finite determinant polynomials but declares the sampler to be
`projective_line`.  For each exact agreement, the packet records the value of
the homogenized regular-minor determinant at `[0:1]`, which is the top
finite-patch coefficient of `Delta_A(Z)` in degree `j+1`.  The top
coefficients are `1,4,7,7`, so the point at infinity is empty for all four
agreements and the projective numerator remains the finite root union size
`4`.  The checker rejects projective regular-minor packets that omit this
audit.

The toy packet also carries a structured `claim_scope` saying that it is
`toy_mechanism` evidence and cannot be used for threshold pinning.  The checker
has a matching negative fixture,

```text
experimental/data/certificates/regular-minor-extractor-toy/
  invalid_synthetic_threshold_scope_packet.json
```

which must fail because it marks a synthetic packet as an actual safe-side
threshold bound.

The extension-field replay is

```text
experimental/data/hankel-regular-minor-inputs/f17_2_n16_k8_a13_toy.json
experimental/data/certificates/regular-minor-extractor-f17-2-toy/
```

It views the same scalar syndrome pencil inside
`F_17^2 = F_17[x]/(x^2-3)` and enumerates all `289` finite slopes.  The full
extension-field root union is again `{0,2,10,11}`, encoded as base-17 integers,
and the packet is accepted by the same v9 checker.

The non-base-root extension replay is

```text
experimental/data/hankel-regular-minor-inputs/f17_2_n5_k2_a4_nonbase_root_toy.json
experimental/data/certificates/regular-minor-extractor-f17-2-nonbase-root-toy/
```

Here the prefix minor is

```text
[[Z, x],
 [x, Z]]
```

over `F_17[x]/(x^2-3)`, so the determinant is `Z^2-3` and the two roots are the
non-base elements `x` and `-x`, encoded as `17` and `272`.  The integrated
checker now evaluates encoded polynomial-basis extension roots and, when the
field is small enough to enumerate, checks that the root table is complete.  So
this packet is a genuine small-extension root-table validation rather than only
a hash check.

The same packet now also carries a `split_linear_factorization` certificate:
the checker reconstructs `Z^2-3` from the encoded factors `(Z-x)(Z+x)` and
verifies that the factor roots are exactly the declared root table.  This is
the reusable compressed-root format intended for future large-field packets,
where brute-force enumeration of `F_17^32` is impossible.

The format is now also exercised at the actual M3 field size.  The synthetic
F17^32 rank-witness packets at `A=385` and `A=426`, the fixed top-window packet
for `421 <= A <= 426`, and the proportional scalar packet at `A=426` all carry
split-linear certificates.  The monomial packets certify `Z^d`, while the
scalar packet certifies `(Z+5)^87`; the checker reconstructs these determinant
polynomials from the factors and verifies the declared exact root tables without
enumerating `F_17^32`.

The checker also verifies that a polynomial-basis field model matches the row
field label and that its modulus is irreducible over `F_p`.  The negative packet

```text
experimental/data/certificates/regular-minor-extractor-f17-2-nonbase-root-toy/
  invalid_reducible_field_model_packet.json
```

must fail because it replaces `x^2-3` by the reducible modulus `x^2-1`.
The second negative packet

```text
experimental/data/certificates/regular-minor-extractor-f17-2-nonbase-root-toy/
  invalid_omitted_extension_root_packet.json
```

must fail because it lists only the encoded root `17` and omits the second root
`272`.
The third negative packet

```text
experimental/data/certificates/regular-minor-extractor-f17-2-nonbase-root-toy/
  invalid_bad_split_root_certificate_packet.json
```

must fail because it corrupts the split-factor leading coefficient while
leaving the root table unchanged.

Extension-valued line packets now also carry a packet-level `sampler_audit`.
For `finite_affine_line` over `F_p^d`, the checker requires denominator
`p^d`; for `projective_line`, it requires `p^d+1`.  This is an F1-style
denominator audit only: it prevents accidentally dividing an extension-valued
slope count by the base field, but it does not assert any extension-line lift
theorem.  The negative packet

```text
experimental/data/certificates/regular-minor-extractor-f17-2-nonbase-root-toy/
  invalid_base_field_denominator_packet.json
```

must fail because it keeps the same non-base roots `x` and `-x` but changes the
finite-affine denominator from `|F_17^2|=289` to `17`.

The prime-field rank-pivot replay is

```text
experimental/data/hankel-regular-minor-inputs/f17_n10_k4_a8_rank_pivot_toy.json
experimental/data/certificates/regular-minor-extractor-rank-pivot-toy/
```

Here `n=10`, `k=4`, `A=8`, so `j=2` and `t=4`.  The prefix row set is singular
for the supplied pencil, but `rank_at_nodes` tests node `0`, then node `1`,
and finds row set `[0,1,3]`.  The extracted determinant is `13 Z^3`, with root
union `{0}`, and the packet checker verifies that the enumerated split bad
slopes are contained in that root set.

The extension-field rank-pivot replay is

```text
experimental/data/hankel-regular-minor-inputs/f17_2_n10_k4_a8_rank_pivot_toy.json
experimental/data/certificates/regular-minor-extractor-rank-pivot-f17-2-toy/
```

It embeds the same toy in `F_17^2 = F_17[x]/(x^2-3)`.  The same row set
`[0,1,3]` is selected at encoded node `1`, and the v9 checker verifies the
encoded extension-field root table.

The rank-witness replay is

```text
experimental/data/hankel-regular-minor-inputs/f17_n10_k4_a8_rank_witness_toy.json
experimental/data/certificates/regular-minor-extractor-rank-witness-toy/
```

It uses the same pencil but asks for `certificate_mode=rank_witness_bound`.
Here the full-rank specialization found by `rank_at_nodes` already proves that
the selected determinant is a nonzero polynomial.  The packet therefore records
the bound `deg Delta_A <= j+1` and leaves the root table unenumerated instead of
interpolating `Delta_A(Z)`.  The integrated checker recomputes the deterministic
rank-witness hash from the row set, pivot node, and degree bound, requires the
audit fields `certificate_mode=rank_witness_bound` and
`root_count=not_enumerated`, verifies the referenced extractor input SHA, and
replays the claimed full-rank specialization from the input syndrome.  This is
weaker than an enumerated root table, but it is the intended cheap first pass
for large `F_17^32` regular-window rows.

The negative packet

```text
experimental/data/certificates/regular-minor-extractor-rank-witness-toy/
  invalid_rank_witness_root_hash_packet.json
```

must fail because it keeps the same witness metadata but corrupts the
rank-witness root hash.

The second negative packet

```text
experimental/data/certificates/regular-minor-extractor-rank-witness-toy/
  invalid_singular_rank_witness_packet.json
```

recomputes the correct hash for row set `[0,1,2]`, but that row set is singular
at the claimed pivot node.  It must fail the replayed rank check.

The polynomial-basis extension companion is

```text
experimental/data/hankel-regular-minor-inputs/f17_2_n10_k4_a8_rank_witness_toy.json
experimental/data/certificates/regular-minor-extractor-rank-witness-f17-2-toy/
```

It exercises the same replay obligation over
`F_17^2 = F_17[x]/(x^2-3)`, including a singular-witness expected-fail packet.

The singular rank-pivot replay is

```text
experimental/data/hankel-regular-minor-inputs/f17_n10_k4_a8_rank_pivot_singular_toy.json
experimental/data/certificates/regular-minor-extractor-rank-pivot-singular-toy/
```

It uses the zero syndrome pencil.  The selector tests `j+2=4` finite nodes and
finds no full-rank specialization.  Since every maximal minor has degree at
most `j+1=3`, this proves that all maximal regular minors vanish identically
and emits a singular residual declaration.

The checker treats this as an audited proof obligation, not just metadata:
`rank_pivot_nodes_required` must equal `j+2`, `rank_pivot_test_nodes` must list
the deterministic distinct nodes actually tested, a successful packet must name
the final node where full rank was found, and a singular declaration must have
tested all `j+2` nodes.  For singular declarations, the checker also loads the
referenced extractor input, checks its SHA, and replays the rank defect of the
full `t x (j+1)` Hankel matrix at each tested node.  The negative packet

```text
experimental/data/certificates/regular-minor-extractor-rank-pivot-singular-toy/
  invalid_rank_pivot_underchecked_packet.json
```

must fail because it claims the singular conclusion after only three of the
four required nodes.  The negative packet

```text
experimental/data/certificates/regular-minor-extractor-rank-pivot-singular-toy/
  invalid_rank_pivot_duplicate_nodes_packet.json
```

must fail because it records a duplicate tested node.

The replay-failure packet

```text
experimental/data/certificates/regular-minor-extractor-rank-pivot-singular-toy/
  invalid_rank_pivot_singular_replay_packet.json
```

keeps a structurally valid singular declaration but points to a SHA-checked
input where node `1` has a full-rank specialization.  It must fail the replayed
rank-defect test.

The first finite affine pivot-atlas replay is

```text
experimental/data/certificates/singular-pivot-toy/
experimental/notes/m1/singular_pivot_toy_packet.md
```

This is a nonzero singular bucket, not the zero-pencil singular toy.  The
chosen pencil has `H(u)+Z H(v)=(Z+5)H(v)` with `rank H(v)=2`, so all maximal
regular minors vanish.  Enumerating the split co-supports and applying the
exact support-image map closes the affine pivot cover: pivots `B_0` and `B_1`
both have eliminant `Z+5`, pivots `B_2` and `B_3` are empty, and the only
`B=0` residual is contained.  The exact finite root union is `{12}`.

## Non-Claims

This does not solve the `F_17^32` regular window.  In particular, it does not
yet provide:

```text
an F_17^32 row-data adapter;
quotient/tangent subtraction for 385 <= A <= 426;
actual-row singular pivot charts.
```

Those are the next M3/M4 steps.  The present contribution is the reusable
regular-minor extractor, with prime-field and explicit polynomial-basis
extension-field replays showing that it emits v9 packets accepted by the
integrated checker.  The `F_17^32` gcd toys are still toy-row data; they
exercise large-field packet shapes but are not prize-row evidence.

## Verification

Run:

```sh
python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_n16_k8_a13_toy.json \
  --check experimental/data/certificates/regular-minor-extractor-toy/f17_n16_k8_a13_regular_minor_extractor_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-toy/f17_n16_k8_a13_regular_minor_extractor_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/regular-minor-extractor-toy/invalid_synthetic_threshold_scope_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/regular-minor-extractor-toy/invalid_bad_regular_minor_replay_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/regular-minor-extractor-toy/invalid_scalar_closed_form_leading_packet.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_2_n16_k8_a13_toy.json \
  --check experimental/data/certificates/regular-minor-extractor-f17-2-toy/f17_2_n16_k8_a13_regular_minor_extractor_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-f17-2-toy/f17_2_n16_k8_a13_regular_minor_extractor_packet.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_2_n5_k2_a4_nonbase_root_toy.json \
  --check experimental/data/certificates/regular-minor-extractor-f17-2-nonbase-root-toy/f17_2_n5_k2_a4_nonbase_root_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-f17-2-nonbase-root-toy/f17_2_n5_k2_a4_nonbase_root_packet.json

! python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-f17-2-nonbase-root-toy/invalid_reducible_field_model_packet.json

! python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-f17-2-nonbase-root-toy/invalid_omitted_extension_root_packet.json

! python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-f17-2-nonbase-root-toy/invalid_base_field_denominator_packet.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_n16_k8_a13_gcd_toy.json \
  --check experimental/data/certificates/regular-minor-gcd-toy/f17_n16_k8_a13_regular_minor_gcd_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-gcd-toy/f17_n16_k8_a13_regular_minor_gcd_packet.json

! python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-gcd-toy/invalid_bad_minor_replay_packet.json

! python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-gcd-toy/invalid_proper_gcd_divisor_packet.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_2_n16_k8_a13_gcd_toy.json \
  --check experimental/data/certificates/regular-minor-gcd-f17-2-toy/f17_2_n16_k8_a13_regular_minor_gcd_packet.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_32_n16_k8_a13_gcd_toy.json \
  --check experimental/data/certificates/regular-minor-gcd-f17-32-toy/f17_32_n16_k8_a13_regular_minor_gcd_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-gcd-f17-32-toy/f17_32_n16_k8_a13_regular_minor_gcd_packet.json

! python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-gcd-f17-32-toy/invalid_extension_gcd_nondivisor_packet.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_32_n16_k8_a13_zero_u_gcd_toy.json \
  --check experimental/data/certificates/regular-minor-gcd-f17-32-zero-u-toy/f17_32_n16_k8_a13_zero_u_regular_minor_gcd_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-gcd-f17-32-zero-u-toy/f17_32_n16_k8_a13_zero_u_regular_minor_gcd_packet.json

! python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-gcd-f17-32-zero-u-toy/invalid_zero_u_gcd_root_certificate_packet.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_n16_k8_a13_rank_node_gcd_toy.json \
  --check experimental/data/certificates/regular-minor-gcd-rank-node-family-toy/f17_n16_k8_a13_rank_node_family_gcd_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-gcd-rank-node-family-toy/f17_n16_k8_a13_rank_node_family_gcd_packet.json

! python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-gcd-rank-node-family-toy/invalid_bad_rank_node_witness_packet.json

! python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-gcd-rank-node-family-toy/invalid_zero_rank_node_witness_packet.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_n16_k8_a13_projective_gcd_toy.json \
  --check experimental/data/certificates/regular-minor-gcd-projective-toy/f17_n16_k8_a13_projective_regular_minor_gcd_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-gcd-projective-toy/f17_n16_k8_a13_projective_regular_minor_gcd_packet.json

! python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-gcd-projective-toy/invalid_bad_projective_gcd_top_packet.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_n10_k4_a8_rank_pivot_toy.json \
  --check experimental/data/certificates/regular-minor-extractor-rank-pivot-toy/f17_n10_k4_a8_rank_pivot_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-rank-pivot-toy/f17_n10_k4_a8_rank_pivot_packet.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_2_n10_k4_a8_rank_pivot_toy.json \
  --check experimental/data/certificates/regular-minor-extractor-rank-pivot-f17-2-toy/f17_2_n10_k4_a8_rank_pivot_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-rank-pivot-f17-2-toy/f17_2_n10_k4_a8_rank_pivot_packet.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_n10_k4_a8_rank_witness_toy.json \
  --check experimental/data/certificates/regular-minor-extractor-rank-witness-toy/f17_n10_k4_a8_rank_witness_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-rank-witness-toy/f17_n10_k4_a8_rank_witness_packet.json

! python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-rank-witness-toy/invalid_rank_witness_root_hash_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py --expect-fail \
  experimental/data/certificates/hankel-f17-32-m3-rank-witness-a426/invalid_large_closed_form_leading_packet.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_n10_k4_a8_rank_pivot_singular_toy.json \
  --check experimental/data/certificates/regular-minor-extractor-rank-pivot-singular-toy/f17_n10_k4_a8_rank_pivot_singular_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-rank-pivot-singular-toy/f17_n10_k4_a8_rank_pivot_singular_packet.json

! python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-rank-pivot-singular-toy/invalid_rank_pivot_underchecked_packet.json

! python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-rank-pivot-singular-toy/invalid_rank_pivot_singular_replay_packet.json
```
