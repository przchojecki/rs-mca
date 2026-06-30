# Regular Hankel-Minor Extractor

**Status:** EXPERIMENTAL / AUDIT, with a proved finite toy replay.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-30.

This note records the first reusable extractor for the regular overdetermined
bucket in the Paper D v9 Hankel atlas.  It addresses the next item in
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

The determinant polynomial is recovered by interpolation from numeric
determinants, rather than by a factorial permutation determinant.  This is the
right algorithmic shape for the future `385 <= A <= 426` window once row data
for the `F_17^32` row are supplied.

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

The extractor finds nonzero prefix minors in all four exact agreements, with
degrees `4,3,2,1` and closed-range root union `{0,2,10,11}`.

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
rank-witness hash from the row set, pivot node, and degree bound, and requires
the audit fields `certificate_mode=rank_witness_bound` and
`root_count=not_enumerated`.  This is weaker than an enumerated root table, but
it is the intended cheap first pass for large `F_17^32` regular-window rows.

The negative packet

```text
experimental/data/certificates/regular-minor-extractor-rank-witness-toy/
  invalid_rank_witness_root_hash_packet.json
```

must fail because it keeps the same witness metadata but corrupts the
rank-witness root hash.

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
tested all `j+2` nodes.  The negative packet

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
integrated checker.

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

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_n10_k4_a8_rank_pivot_singular_toy.json \
  --check experimental/data/certificates/regular-minor-extractor-rank-pivot-singular-toy/f17_n10_k4_a8_rank_pivot_singular_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-rank-pivot-singular-toy/f17_n10_k4_a8_rank_pivot_singular_packet.json

! python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/regular-minor-extractor-rank-pivot-singular-toy/invalid_rank_pivot_underchecked_packet.json
```
