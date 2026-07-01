# Hankel Regular-Window Plan for the F17^32 Row

Status: AUDIT.

This note fixes the arithmetic target for the M3 regular-window audit in
`towards-prize.md`.

For the row

```text
C = RS[F_17^32,H,256],    |H| = 512,
```

we have `n=512` and `k=256`.  For exact agreement `A`, the v9 Hankel parameters
are

```text
j = n - A,
t = A - k.
```

The regular overdetermined condition is

```text
t >= j+1,
```

equivalently `2A >= n+k+1`.  Therefore the first regular agreement is

```text
A = ceil((512+256+1)/2) = 385.
```

The tangent-exact theorem starts at

```text
A = n - floor((n-k)/3) = 512 - 85 = 427.
```

Thus the first prize-facing non-tangent regular window is exactly

```text
385 <= A <= 426.
```

The concrete field/domain descriptor for this row is

```text
experimental/data/certificates/hankel-f17-32-row-descriptor/
  f17_32_n512_k256_hankel_row_descriptor.json
```

with domain hash

```text
35904a892e0319b3805e91438ec2733427a351a72ce9654428d6a33bd3575b92
```

For the prefix maximal minor with rows `0..j` and columns `0..j`, the largest
syndrome index used is `2j`.  Across the window this ranges from `254` down to
`172`, so every prefix minor is syntactically available from a syndrome vector
of length `n-k=256`.  The full Hankel window also uses no index beyond `255`.

The minor sizes run from `128` at `A=385` down to `87` at `A=426`.  Interpolating
one determinant polynomial per agreement would require `4557` determinant
evaluations in total.

The important negative audit is that degree bounds alone cannot close the
safe-side budget.  The finite-slope `2^-128` budget is

```text
floor(17^32 / 2^128) = 6,
```

while the regular degree-bound sum over this window is `4515`.  Therefore the
next useful M3 packet must compute actual root tables, or else identify the
first agreement where the regular bucket is singular and pass that residual to
pivot charts.  A degree-only certificate for this whole window would be far too
weak.

The follow-up note

```text
experimental/notes/m1/f17_32_m3_generic_regular_minor.md
```

proves that every maximal row-set minor is generically nonzero, with exact
degree `j+1`, for every agreement in this window.  Across the window this
covers
`155193154203428426778689566118132250614039201839551` formal row-set charts,
with `1806` contiguous charts singled out as the practical first-search
subatlas.  Thus vanished regular minors for an actual syndrome pencil are
special singular strata, not a forced failure of the regular Hankel chart.

The first concrete large-field stress packets for this window are the endpoint
rank-witness packets

```text
experimental/data/certificates/hankel-f17-32-m3-rank-witness-a385/
  f17_32_n512_k256_a385_rank_witness_packet.json

experimental/data/certificates/hankel-f17-32-m3-rank-witness-a426/
  f17_32_n512_k256_a426_rank_witness_packet.json
```

They use synthetic `F_17^32` syndrome pencils at `A=385` and `A=426` and prove
nonzero regular minors by rank witnesses.  This exercises the pinned
field/domain arithmetic at the largest and smallest minor sizes in the window,
but it is not a worst-case safe-side bound and does not provide a root table.
The compact family certificate

```text
experimental/data/certificates/hankel-f17-32-m3-rank-witness-family/
  f17_32_n512_k256_m3_rank_witness_family_certificate.json
```

records the same synthetic Vandermonde prefix witness for all 42 agreements in
the window without storing 42 full v9 packets.  The fixed top-window packet

```text
experimental/data/certificates/hankel-f17-32-m3-fixed-top-window/
  f17_32_n512_k256_a421_426_fixed_prefix92_packet.json
```

is a single v9 packet for one synthetic syndrome pencil covering
`421 <= A <= 426`.

The line-value lift

```text
experimental/data/certificates/hankel-f17-32-m3-line-value-lift/
  f17_32_n512_k256_a421_426_fixed_prefix92_line_values.json
```

uses the subgroup identity `lambda_x=x/512` to give explicit values
`f,g:H -> F_17^32` whose weighted syndromes are exactly the fixed top-window
input.  Thus that packet is not merely a free syndrome vector; it is the
syndrome image of an explicit received line on the pinned row.

The reusable theorem behind this lift is recorded in

```text
experimental/notes/m1/subgroup_syndrome_section.md
experimental/data/certificates/subgroup-syndrome-section/
  subgroup_syndrome_section_certificate.json
```

It proves that for any multiplicative subgroup row, every syndrome vector of
length at most the subgroup order has the explicit inverse-Fourier section
`y_s(x)=sum_m s_m x^(-m-1)`.

For the whole M3 window this applies uniformly, not only to the fixed
top-window packet.  Since every exact bucket has

```text
t+j = (A-k)+(n-A) = n-k = 256 <= |H| = 512,
```

every length-256 syndrome pencil `(u,v)` is realized by explicit line values
`f,g:H -> F_17^32`.  The certificate

```text
experimental/data/certificates/hankel-f17-32-m3-syndrome-realizability/
  f17_32_n512_k256_m3_syndrome_realizability_certificate.json
```

records this reduction.  Thus the remaining M3 regular-window gap is not
construction of actual row data; it is universal classification of arbitrary
length-256 syndrome pencils after tangent, quotient, and extension-confined
branches are removed.

The first subtraction sidecar for this packet is

```text
experimental/notes/m1/f17_32_m3_zero_slope_subtraction.md
experimental/data/certificates/hankel-f17-32-m3-zero-slope-subtraction/
  f17_32_n512_k256_a421_426_zero_slope_subtraction.json
```

It verifies that the synthetic root `{0}` is the zero-codeword
tangent/common-code-line slope because the line-value lift has `f=0`.  Thus the
fixed top-window packet has residual synthetic aperiodic numerator `0` after
that paid tangent branch is removed.  This is a no-double-counting check for
one synthetic packet, not the full M4 row table.

The regular-window status ledger now records this as an explicit M4 mini-table
for every `A=421..426`:

```text
B_tan=1,
B_quot_support=B_quot_image=0,
B_ap_regular_before_removed=1,
B_ap_after_removed=0,
B_ext=0,
B_projective_infinity=0,
deduped total upper bound = 1 <= budget 6.
```

This closes only the subtraction/budget table for that synthetic packet; the
universal row table still requires arbitrary length-256 syndrome pencils to be
classified by root table or singular-bucket outcome.

The status ledger also consumes

```text
experimental/data/certificates/hankel-proportional-pencil-tangent-lemma/
  hankel_proportional_pencil_tangent_lemma_certificate.json
```

For this M3 window, `t+j=256` is exactly the stored syndrome length for every
agreement.  Therefore the lemma's tail caveat disappears here: if a length-256
syndrome pencil satisfies `u=c v`, then the branch is tangent/common-code-line
after the slope `Z=-c` and contributes no residual aperiodic roots.  This
classifies a universal proportional branch of arbitrary pencils, but it still
does not classify non-proportional pencils.

The corresponding F1 denominator audit is

```text
experimental/notes/f1/f17_32_m3_extension_denominator_audit.md
experimental/data/certificates/hankel-f17-32-m3-extension-denominator-audit/
  f17_32_n512_k256_a421_426_extension_denominator_audit.json
```

It verifies that `g` is non-base-valued at all 512 positions, so finite affine
slopes for this packet are sampled from `F_17^32` and the denominator is
`q_line=17^32`.

A reusable non-proportional exact-root template for future packets is recorded
in

```text
experimental/notes/m1/hankel_one_spike_linear_template.md
experimental/data/certificates/hankel-one-spike-linear-template/
  hankel_one_spike_linear_template_certificate.json
```

It proves that moments `u_m=sum_{x in X}x^m` with a one-spike direction
`v_m=y^m` give prefix determinants affine in the slope.  Thus such directions
have at most one regular-minor root per exact agreement, with explicit
Cauchy-Binet coefficients.  This is a template for non-proportional M3 root
packets.

The template is now instantiated at the M3 endpoint `A=426` by

```text
experimental/data/hankel-regular-minor-inputs/
  f17_32_n512_k256_a426_one_spike_input.json

experimental/data/certificates/hankel-f17-32-m3-one-spike-a426/
  f17_32_n512_k256_a426_one_spike_packet.json
```

This packet uses a non-proportional synthetic `F_17^32` syndrome pencil and
proves a degree-1 prefix regular minor with one explicit root.  The checker
replays both the declared moments and the Cauchy-Binet coefficients, and the
directory includes a tampered-coefficient fixture that must fail.  It is still
not a universal M3 row table or a safe-side MCA bound.

A broader low-rank update theorem is recorded in

```text
experimental/notes/m1/hankel_low_rank_update_template.md
experimental/data/certificates/hankel-low-rank-update-template/
  hankel_low_rank_update_template_certificate.json
```

It proves that if

```text
u_m = sum_{x in X} x^m,    v_m = sum_{y in Y} y^m,
```

then every prefix determinant has degree at most `|Y|` in the slope, with
Cauchy-Binet coefficients indexed by how many update nodes are selected.  Thus
small-rank non-proportional directions give regular-minor root bounds
independent of the minor size; identically zero determinants are explicitly
singular residual buckets for the pivot atlas, not aperiodic evidence.
The v4 certificate also records the corrected M3 budget envelope and packet
gate: because both
the finite and projective `F_17^32` budget numerators are `6`, every nonzero
regular low-rank update chart of rank `s <= 6` is finite-root budget safe.
Projective automatic safety without a separate infinity exclusion holds for
`s <= 5`; rank `6` needs infinity exclusion, finite-root slack, or an
equivalent deduplication/removal certificate before projective accounting.

The corresponding rank-2 `F_17^32` endpoint packet is

```text
experimental/data/hankel-regular-minor-inputs/
  f17_32_n512_k256_a426_low_rank2_input.json

experimental/data/certificates/hankel-f17-32-m3-low-rank2-a426/
  f17_32_n512_k256_a426_low_rank2_packet.json
```

It proves a degree-2 prefix regular-minor bound at `A=426`.  The compressed
quadratic now splits over `F_17^32`, so the packet records the exact two roots,
their split-linear factorization certificate, and a quadratic discriminant
certificate; the checker replays the determinant coefficients, the compressed
kernel sidecar, and the root certificate from the low-rank input.

The same rank-2 construction has an all-window synthetic family certificate:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank2-family/
  f17_32_n512_k256_m3_low_rank2_family_certificate.json
```

For every `385 <= A <= 426`, it uses the first `j+1` descriptor-domain nodes as
the square base and the next two descriptor-domain nodes as the low-rank
update.  The degree cap is `84`, versus the generic window sum `4515`.
Applying the rank-2 discriminant gate gives exact roots: 20 rows split, 22 rows
have nonsquare discriminant, and the exact finite-root total is `40`.  The
family also audits the projective endpoint `[0:1]`: every leading coefficient
of the compressed quadratic is nonzero, but the original regular-minor
projective endpoint is not excluded because the update direction has rank
`2 < j+1`.  Infinity therefore contributes one projective point in every row,
and every agreement has at most 3 projective regular roots against budget
numerator 6.  It also compares the 40 finite roots against the common-code-line
tangent ledger: at every finite root, the full syndrome has nonzero witness
`Syn_0(u+zv)=|X|+2z`, so no finite low-rank-family root is
tangent/common-code-line.  The family cross-checks the `A=426` endpoint against
the exact-root v9 packet.

The rank-3 companion certificate is:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank3-family/
  f17_32_n512_k256_m3_low_rank3_family_certificate.json
```

It uses the same nested prefixes and the next three descriptor-domain nodes as
the update set.  The degree cap is `3 * 42 = 126`, and the exact finite-root
count is computed by `gcd(Delta,Z^q-Z)`: 12 rows have no finite roots, 24 rows
have one finite root, and 6 rows have three finite roots, for total `42`.  The
original regular-minor projective endpoint is not excluded, so infinity
contributes one projective point in every row and every agreement has at most 4
projective regular roots against budget numerator 6.  The common-code-line
tangent overlap is also zero, because the Frobenius gcd is nonzero at the only
possible slope from `Syn_0(u+zv)=|X|+3z`.

The rank-4 budget companion is:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank4-budget-family/
  f17_32_n512_k256_m3_low_rank4_budget_family_certificate.json
```

It uses the next four descriptor nodes for `Y` and verifies that every
compressed determinant has degree exactly `4`.  Exact finite roots are not
enumerated, because the v4 low-rank packet gate makes degree-only accounting
strong enough at rank `4`: at most four finite roots plus the corrected
projective infinity contribution gives at most five projective regular roots
per agreement, below budget numerator `6`.

The rank-5 budget companion is:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank5-budget-family/
  f17_32_n512_k256_m3_low_rank5_budget_family_certificate.json
```

It uses the next five descriptor nodes for `Y` and verifies that every
compressed determinant has degree exactly `5`, using Newton identities from the
traces of powers of the compressed kernel.  This is the last automatically
projective-safe rank in the v4 gate: at most five finite roots plus the
corrected projective infinity contribution gives at most six projective regular
roots per agreement, exactly the budget numerator `6`.

The rank-6 finite-slack companion is:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank6-slack-family/
  f17_32_n512_k256_m3_low_rank6_slack_family_certificate.json
```

It uses the next six descriptor nodes for `Y`.  Degree-only accounting would
give `6+1=7`, so the certificate computes exact finite roots with
`gcd(Delta,Z^q-Z)`.  The root histogram is `{0:16, 1:17, 2:9}`, hence every
agreement has at most two finite roots and at most three projective regular
roots after the corrected infinity point.  This supplies the finite-root slack
that the v4 gate requires at rank `6`.

The rank-7 finite-slack companion is:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank7-slack-family/
  f17_32_n512_k256_m3_low_rank7_slack_family_certificate.json
```

It uses the next seven descriptor nodes for `Y`, beyond the v4 low-rank degree
envelope.  Degree-only accounting would give finite bound `7` and projective
bound `8`, both above budget numerator `6`.  Exact finite-root counts have
histogram `{0:16, 1:15, 2:6, 3:4, 4:1}`, so finite-root slack still gives at
most five projective regular roots per agreement.

The rank-8 finite-slack companion is:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank8-slack-family/
  f17_32_n512_k256_m3_low_rank8_slack_family_certificate.json
```

It uses the next eight descriptor nodes for `Y`, another step beyond the v4
low-rank degree envelope.  Degree-only accounting would give finite bound `8`
and projective bound `9`, both above budget numerator `6`.  Exact finite-root
counts have histogram `{0:22, 1:10, 2:7, 3:2, 4:1}`, so finite-root slack again
gives at most five projective regular roots per agreement.

The rank-9..11 finite-slack sweep is:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank9-11-slack-sweep/
  f17_32_n512_k256_m3_low_rank9_11_slack_sweep_certificate.json
```

It records a compact multi-rank replay rather than separate bulky kernel
sidecars.  Exact finite-root histograms are `{0:17, 1:17, 2:6, 3:2}` for rank
`9`, `{0:8, 1:23, 2:9, 3:2}` for rank `10`, and
`{0:15, 1:16, 2:5, 3:6}` for rank `11`.  Thus the checked sweep has at most
three finite roots, and at most four projective regular roots after the
corrected infinity point, despite degree-only projective bounds `10`, `11`,
and `12`.

The low-rank projective-infinity companion is:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank2-11-projective-infinity/
  f17_32_n512_k256_m3_low_rank2_11_projective_infinity_certificate.json
```

It proves that the corrected projective endpoint `[0:1]` is an actual
support-wise noncontained endpoint for the synthetic low-rank ladder at ranks
`2..11`, not merely a point left unexcluded by the top-degree regular minor.
The witness support is `D \ Y`, and simultaneous containment is ruled out by
Vandermonde independence on `X union Y`.

The endpoint quotient-support companion is:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank2-11-endpoint-quotient-support/
  f17_32_n512_k256_m3_low_rank2_11_endpoint_quotient_support.json
```

It checks the same actual supports `D \ Y` against all nontrivial proper
quotient fiber sizes `c in {2,4,8,16,32,64,128,256}`.  Since the consecutive
update block `Y` always meets more than `ceil(|Y|/c)` quotient fibers, these
endpoint supports are not quotient-remainder supports.  This is not an audit of
the trivial fiber sizes `c=1,512`, finite affine roots, or quotient-image
supports.

The first v9 projective-infinity pivot packet extracted from this audit is:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank-rank6-a426-projective-pivot/
  f17_32_n512_k256_a426_rank6_projective_infinity_pivot_packet.json
```

It packages the rank-6, `A=426` endpoint as a projective-line `pivot_atlas`
record.  The `projective_infinity` chart is nonempty with contribution one,
verified by the v9 packet checker through a coverage reference to the same
Vandermonde endpoint witness.  Finite affine roots are deliberately not
enumerated in this chart packet.

The finite-affine v9 companion for the same synthetic row is:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank-rank6-a426-finite-affine/
  f17_32_n512_k256_a426_rank6_finite_affine_packet.json
```

It records the rank-6, `A=426` prefix regular minor with degree `6` and one
exact finite root.  The packet checker replays both the low-rank update input
and the `gcd(Delta,Z^q-Z)` certificate, giving one concrete v9 finite/projective
chart pair inside the synthetic low-rank ladder.

The tangent/common-code-line exclusion companion is:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-tangent-exclusion/
  f17_32_n512_k256_m3_low_rank6_11_tangent_exclusion_certificate.json
```

For rank `s`, moment zero gives `Syn_0(u+zv)=|X|+s z`, so the only possible
common-code-line slope is `z=-|X|/s`.  Since `6 <= s <= 11` is nonzero in
characteristic `17`, the verifier checks `Delta_s(-|X|/s) != 0` for every
rank/agreement pair.  This proves that the `238` finite roots counted by the
rank `6..11` slack certificates have zero common-code-line tangent overlap.

The proper-subfield/confinement companion is:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-subfield-exclusion/
  f17_32_n512_k256_m3_low_rank6_11_subfield_exclusion_certificate.json
```

It checks the proper subfields `F_17^d` for `d in {1,2,4,8,16}` by Frobenius
fixedness on listed roots and by subfield gcds on count-only rows.  The result
is zero proper-subfield overlap for the same `238` counted finite roots.

The rank-6..11 known-ledger table is:

```text
experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-known-ledger-table/
  f17_32_n512_k256_m3_low_rank6_11_known_ledger_table.json
```

It combines the exact finite-root counts, projective-infinity endpoint,
tangent exclusion, and proper-subfield exclusion into one M4-style residual
table.  Across all `252` rank/agreement rows, the maximum residual projective
regular-root upper count after these known ledgers is `5 <= 6`.  Quotient
support/image subtraction for finite affine roots is deliberately recorded as
`not_audited`.

The current status ledger

```text
experimental/data/certificates/hankel-f17-32-m3-regular-window-status/
  f17_32_n512_k256_m3_regular_window_status.json
```

hashes the plan, generic certificate, synthetic family certificates, and fixed
top-window packet.  It records, per agreement, that the generic/synthetic facts
are proved but actual `F_17^32` row-data root tables and singular-bucket
outcomes remain unsupplied.

Reproduce the audit packet:

```sh
python3 experimental/scripts/plan_f17_regular_hankel_window.py \
  --check experimental/data/certificates/hankel-regular-window-f17-385-426/f17_32_n512_k256_regular_window_plan.json

python3 experimental/scripts/verify_f17_32_m3_regular_window_status.py \
  --check experimental/data/certificates/hankel-f17-32-m3-regular-window-status/f17_32_n512_k256_m3_regular_window_status.json

python3 experimental/scripts/verify_f17_32_m3_line_value_lift.py \
  --check experimental/data/certificates/hankel-f17-32-m3-line-value-lift/f17_32_n512_k256_a421_426_fixed_prefix92_line_values.json

python3 experimental/scripts/verify_m1_subgroup_syndrome_section.py \
  --check experimental/data/certificates/subgroup-syndrome-section/subgroup_syndrome_section_certificate.json

python3 experimental/scripts/verify_f17_32_m3_zero_slope_subtraction.py \
  --check experimental/data/certificates/hankel-f17-32-m3-zero-slope-subtraction/f17_32_n512_k256_a421_426_zero_slope_subtraction.json

python3 experimental/scripts/verify_f17_32_m3_extension_denominator_audit.py \
  --check experimental/data/certificates/hankel-f17-32-m3-extension-denominator-audit/f17_32_n512_k256_a421_426_extension_denominator_audit.json

python3 experimental/scripts/emit_f17_32_m3_rank_witness_input.py \
  --agreement 426 \
  --one-spike-linear \
  --check experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_one_spike_input.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_one_spike_input.json \
  --check experimental/data/certificates/hankel-f17-32-m3-one-spike-a426/f17_32_n512_k256_a426_one_spike_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-f17-32-m3-one-spike-a426/f17_32_n512_k256_a426_one_spike_packet.json

python3 experimental/scripts/verify_m1_hankel_low_rank_update_template.py \
  --check experimental/data/certificates/hankel-low-rank-update-template/hankel_low_rank_update_template_certificate.json

python3 experimental/scripts/emit_f17_32_m3_rank_witness_input.py \
  --agreement 426 \
  --low-rank-update-count 2 \
  --check experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_low_rank2_input.json

python3 experimental/scripts/extract_regular_hankel_minors.py \
  experimental/data/hankel-regular-minor-inputs/f17_32_n512_k256_a426_low_rank2_input.json \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank2-a426/f17_32_n512_k256_a426_low_rank2_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-f17-32-m3-low-rank2-a426/f17_32_n512_k256_a426_low_rank2_packet.json

python3 experimental/scripts/verify_f17_32_m3_low_rank2_family.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank2-family/f17_32_n512_k256_m3_low_rank2_family_certificate.json

python3 experimental/scripts/verify_f17_32_m3_low_rank3_family.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank3-family/f17_32_n512_k256_m3_low_rank3_family_certificate.json

python3 experimental/scripts/verify_f17_32_m3_low_rank4_budget_family.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank4-budget-family/f17_32_n512_k256_m3_low_rank4_budget_family_certificate.json

python3 experimental/scripts/verify_f17_32_m3_low_rank5_budget_family.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank5-budget-family/f17_32_n512_k256_m3_low_rank5_budget_family_certificate.json

python3 experimental/scripts/verify_f17_32_m3_low_rank6_slack_family.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank6-slack-family/f17_32_n512_k256_m3_low_rank6_slack_family_certificate.json

python3 experimental/scripts/verify_f17_32_m3_low_rank7_slack_family.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank7-slack-family/f17_32_n512_k256_m3_low_rank7_slack_family_certificate.json

python3 experimental/scripts/verify_f17_32_m3_low_rank8_slack_family.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank8-slack-family/f17_32_n512_k256_m3_low_rank8_slack_family_certificate.json

python3 experimental/scripts/verify_f17_32_m3_low_rank9_11_slack_sweep.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank9-11-slack-sweep/f17_32_n512_k256_m3_low_rank9_11_slack_sweep_certificate.json

python3 experimental/scripts/verify_f17_32_m3_low_rank2_11_projective_infinity.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank2-11-projective-infinity/f17_32_n512_k256_m3_low_rank2_11_projective_infinity_certificate.json

python3 experimental/scripts/verify_f17_32_m3_low_rank_rank6_a426_projective_pivot.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank-rank6-a426-projective-pivot/f17_32_n512_k256_a426_rank6_projective_infinity_pivot_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-f17-32-m3-low-rank-rank6-a426-projective-pivot/f17_32_n512_k256_a426_rank6_projective_infinity_pivot_packet.json

python3 experimental/scripts/verify_f17_32_m3_low_rank6_11_tangent_exclusion.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-tangent-exclusion/f17_32_n512_k256_m3_low_rank6_11_tangent_exclusion_certificate.json

python3 experimental/scripts/verify_f17_32_m3_low_rank6_11_subfield_exclusion.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-subfield-exclusion/f17_32_n512_k256_m3_low_rank6_11_subfield_exclusion_certificate.json

python3 experimental/scripts/verify_f17_32_m3_low_rank6_11_known_ledger_table.py \
  --check experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-known-ledger-table/f17_32_n512_k256_m3_low_rank6_11_known_ledger_table.json
```

Non-claims: this note does not enumerate universal root sets for arbitrary
syndrome pencils, classify singular buckets, or prove a safe-side MCA bound.
