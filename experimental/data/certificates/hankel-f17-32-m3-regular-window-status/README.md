# F17^32 M3 Regular-Window Status

This directory contains a compact audit ledger for the Paper D v9 M3 regular
window

```text
RS[F_17^32,H,256], |H|=512, 385 <= A <= 426.
```

It hashes and cross-checks the regular-window plan, the generic all-row-set
minor certificate, three synthetic all-window families, the fixed top-window v9
packet, the explicit line-value lift of that fixed packet, and the reusable
subgroup syndrome-section theorem behind the lift.  The synthetic families are
the closed-form rank-witness family with root union `{0}` and the rank-2
low-rank family with exact split/nonsquare quadratic root table: 20 split
rows, 22 nonsquare rows, and 40 finite roots total under degree cap 84.  The
rank-2 family also records that `[0:1]` is not excluded by the original
regular-minor endpoint, so every agreement has at most 3 projective regular
roots against budget numerator 6.
Moreover, all 40 finite roots have a nonzero full-syndrome witness at moment
`m=0`, so none are common-code-line tangent roots.  Quotient-image overlap is
still not audited for this synthetic family.

The rank-3 low-rank family uses the same compressed Lagrange-kernel identity
with three update nodes.  It computes exact finite-root counts by
`gcd(Delta,Z^q-Z)`: 12 rows have no finite roots, 24 rows have one finite root,
and 6 rows have three finite roots, for 42 finite roots total under degree cap
126.  Its projective endpoint is likewise not excluded by the original
regular-minor endpoint, so every agreement has at most 4 projective regular
roots against budget numerator 6.  The Frobenius gcd is nonzero at the only
possible common-code-line slope, so none of these 42 finite roots are
tangent/common-code-line roots.  Quotient-image overlap is also not audited for
this synthetic family.

The rank-4 low-rank budget family uses four update nodes.  It verifies that
every compressed determinant has degree exactly `4`, but deliberately does not
enumerate finite roots: the v4 low-rank packet gate already makes the degree
bound budget-sufficient.  Each agreement has at most four finite regular roots,
and the corrected projective endpoint contributes at most one infinity point,
so every agreement has at most five projective regular roots against budget
numerator `6`.

The rank-5 low-rank budget family is the last automatic projective-safe rank in
the v4 packet gate.  It uses five update nodes and Newton identities for
`det(I+ZK)`, verifies degree exactly `5` in every row, and bounds each
agreement by at most five finite roots plus one corrected projective infinity
point.  Thus every agreement has at most six projective regular roots, exactly
the budget numerator `6`.

The rank-6 low-rank slack family tests the first rank where degree-only
projective accounting fails.  It verifies degree exactly `6`, then computes
`gcd(Delta,Z^q-Z)` for every agreement.  The exact finite-root histogram is
`{0:16, 1:17, 2:9}`, so every agreement has at most two finite roots and at
most three projective regular roots after the corrected infinity point.  Thus
this synthetic rank-6 family is projective-safe by finite-root slack, not by
degree alone.

The rank-7 low-rank slack family goes beyond the v4 degree envelope itself:
degree-only finite accounting gives `7 > 6` and projective accounting gives
`8 > 6`.  Exact Frobenius-gcd root counts still give histogram
`{0:16, 1:15, 2:6, 3:4, 4:1}`, so every agreement has at most four finite roots
and at most five projective regular roots after the corrected infinity point.
This is a synthetic example where exact root slack, not low-rank degree alone,
keeps the packet under budget.

The rank-8 low-rank slack family takes the same nested synthetic ladder another
step beyond the degree envelope: degree-only finite accounting gives `8 > 6`
and projective accounting gives `9 > 6`.  Exact Frobenius-gcd root counts give
histogram `{0:22, 1:10, 2:7, 3:2, 4:1}`, so every agreement again has at most
four finite roots and at most five projective regular roots after the corrected
infinity point.

The rank-9..11 low-rank slack sweep avoids adding three more bulky per-rank
sidecar certificates.  It recomputes exact Frobenius-gcd root counts for all
`126` rank/agreement pairs and records compact hashes.  The root histograms are
`rank 9: {0:17, 1:17, 2:6, 3:2}`, `rank 10: {0:8, 1:23, 2:9, 3:2}`, and
`rank 11: {0:15, 1:16, 2:5, 3:6}`.  Thus every checked pair has at most three
finite roots and at most four projective regular roots, despite degree-only
projective bounds `10`, `11`, and `12`.

The rank-2..11 projective-infinity audit proves that the corrected one-point
endpoint contribution in the low-rank ladder is exact for this synthetic
family.  For `u_m=sum_{x in X}x^m` and `v_m=sum_{y in Y}y^m`, the endpoint
`[0:1]` is witnessed on `D \ Y`, while simultaneous containment is ruled out by
Vandermonde independence on `X union Y`.  The largest checked union has
`139 <= n-k=256` columns, and `|D \ Y| >= 501 > 426`.

The rank-2..11 endpoint quotient-support audit classifies those same actual
endpoint supports.  For every nontrivial proper quotient fiber size
`c in {2,4,8,16,32,64,128,256}`, the consecutive update block `Y` meets more
than `ceil(|Y|/c)` quotient fibers, so `D \ Y` is not a quotient-remainder
support.  This is an endpoint-support audit only: the trivial fiber sizes
`c=1,512`, finite affine roots, and quotient-image supports remain outside its
scope.

The rank-2..11 endpoint quotient-image audit proves the complementary image
statement for the same projective parameter.  Although the minimal endpoint
support `D \ Y` is not quotient-remainder, every checked endpoint `[0:1]` has
an explicit agreement-size witness support built from `c=2` quotient fibers
that avoids `Y`.  The co-support therefore contains `Y`, while the base
syndrome is excluded from that co-support by Vandermonde independence with
maximum column count `255 <= n-k`.

The rank-6, `A=426` projective-infinity pivot packet packages one row of that
endpoint audit in the v9 `pivot_atlas` format.  Its projective-line
`projective_infinity` chart has coverage target `status=nonempty` and
`support_count=1`, and is accepted by `scripts/check_aperiodic_eliminant_packet.py`.
It is a chart packet only: finite affine roots are intentionally left to the
rank-6 finite-slack certificate.

The rank-6, `A=426` finite-affine companion packages the corresponding prefix
regular minor as a v9 packet.  The checker replays the rank-6 low-rank update
input, verifies degree `6`, and checks the exact one-root table by replaying
the `gcd(Delta,Z^q-Z)` certificate over `F_17^32`.  Together with the
projective-infinity packet, this gives one synthetic rank-6 row with both its
finite-affine regular-minor roots and projective endpoint represented in v9
packet form.

The rank-6, `A=426` projective-line packet combines those two audits in the
regular-minor packet format.  The finite root table is the same one-root
Frobenius-gcd table, while the `[0:1]` endpoint is checked inline by the
original top coefficient at degree `j+1=87`.  The resulting projective-line
numerator is `2`, still below the M3 budget numerator `6`, and the companion
pivot packet supplies the actual support witness for the endpoint.

The rank-7, `A=393` projective-line packet packages a harder beyond-envelope
row.  Its regular minor has degree `7`, so degree-only projective accounting
would give `8 > 6`; the verifier splits the degree-4 Frobenius gcd
deterministically and records four finite roots, while the top-degree audit
adds the `[0:1]` endpoint.  This gives projective-line numerator `5 <= 6` for
the unique rank-7 row where the finite-root count reaches four.

The rank-8, `A=393` projective-line packet repeats the same hard-row audit one
step farther beyond the degree envelope.  Degree-only projective accounting
would give `9 > 6`, but the degree-4 Frobenius gcd again splits into four
finite roots and the `[0:1]` endpoint contributes one point.  This supplies a
checked v9 packet for the unique rank-8 row where the finite-root count reaches
four, also with projective-line numerator `5 <= 6`.

The rank-9, `A=398` projective-line packet promotes one compact sweep row back
into a full v9 replay artifact.  Degree-only projective accounting would give
`10 > 6`, but the generator recomputes the degree-9 determinant and
Frobenius-gcd hashes, splits the degree-3 gcd into three finite roots, and adds
the `[0:1]` endpoint.  This gives projective-line numerator `4 <= 6` for a
representative rank-9 max-root row from the compact sweep.

The rank-10, `A=411` and rank-11, `A=391` projective-line packets finish the
same representative compact-sweep promotion for the remaining high-rank rows.
Degree-only projective accounting would give `11` and `12`, respectively, but
each packet replays the compact sweep hashes, splits a degree-3 Frobenius gcd,
and counts the `[0:1]` endpoint.  Both representative rows have projective-line
numerator `4 <= 6`.

The rank-6..11 tangent-exclusion audit is the first subtraction check for this
beyond-envelope low-rank block.  It consumes the exact finite-root certificates
above and checks the unique moment-zero common-code-line slope
`z=-|X|/s` for each rank `s`.  The result is zero tangent overlap for all `238`
finite roots counted in ranks `6..11`, so the low-rank slack roots are not
removed by the common-code-line tangent ledger.

The rank-6..11 subfield-exclusion audit checks the corresponding
subfield/confinement ledger for the same `238` finite roots.  It tests the
proper subfields `F_17^d` with `d in {1,2,4,8,16}` by Frobenius fixedness or
subfield gcds, and finds zero proper-subfield overlap.  Thus these counted
roots are genuinely outside all proper subfields of `F_17^32` for this
synthetic low-rank block.

The rank-6..11 known-ledger table combines the exact finite-root counts,
projective-infinity endpoint, endpoint quotient-support exclusion, endpoint
quotient-image witness, tangent exclusion, proper-subfield exclusion, and
shifted-minor exclusion into one compact M4-style residual ledger.  It rebuilds
`252` rank/agreement rows and records maximum residual projective regular-minor
upper count `5 <= 6`.  After the shifted-minor exclusion removes all finite
first-minor roots from the full-Hankel witness column, the maximum residual
projective full-Hankel witness upper count is `1 <= 6`.  After charging the
remaining endpoint to quotient-image, the aperiodic full-Hankel residual upper
count is `0` in every checked row.  Finite-root quotient-support and
quotient-image subtraction remain explicitly unaudited as separate quotient
ledgers.

The representative shifted-minor exclusion checks the finite roots in the six
rank-6..11 projective-line packets.  For all `18` listed roots, the row-shift-1
square Hankel minor is nonzero, so those first-minor roots are not actual
full-Hankel exact-support witnesses.  This is a representative-packet audit
only, not an all-row quotient or support-image theorem.

The rank-2..5 shifted-minor exclusion applies the same criterion to every
checked row in the lower-rank synthetic ladder.  It proves that the first
regular minor is coprime to the row-shift-1 minor in all `168` rank/agreement
rows, clearing the `82` exact finite roots from ranks 2..3 and the degree-bound
finite root-locus upper total `378` from ranks 4..5 as full-Hankel witnesses.
Thus the surviving finite full-Hankel witness upper bound is `0` in these
ranks, even where finite roots were not enumerated.

The rank-6..11 shifted-minor exclusion extends this test from the six
representative packets to every root-bearing row in the synthetic low-rank
slack ladder.  Across the source slack ledgers, all `238` finite first-minor
roots are excluded by the row-shift-1 square minor.  This is still a synthetic
ladder statement and does not audit quotient image or quotient support.

The rank-2..11 full-Hankel ledger packages the lower-rank and higher-rank
shifted-minor exclusions with the endpoint quotient-image audit.  It rebuilds
all `420` synthetic rank/agreement rows and records finite regular
first-minor upper mass `698`, all cleared from the full-Hankel witness column.
The only remaining projective full-Hankel contribution is the endpoint
`[0:1]`, which has a quotient-image witness in every row, so the aperiodic
full-Hankel residual upper bound is `0` throughout the synthetic low-rank
ladder.  This is not an arbitrary M3-row theorem.

The one-spike window full-Hankel ledger closes a separate non-proportional
rank-one branch across all `42` agreements.  In each row
`u_m=sum_{x in X}x^m` for `|X|=j+1` and `v_m=y^m` for the next domain point.
The Cauchy-Binet one-spike formula gives one finite first-minor root; the
row-shift-1 minor is nonzero at that root in every row, so it is not a
full-Hankel witness.  The remaining `[0:1]` endpoint has a `c=2`
quotient-image witness, leaving aperiodic full-Hankel residual upper bound
`0` for this whole one-spike branch.

The companion one-spike v9 projective-line packet records the same branch in
the Paper D packet schema.  Before full-Hankel and quotient-image charging, its
projective numerator is `43`: one finite affine root in each of the `42`
agreement rows, plus the shared projective endpoint `[0:1]`.  The full-Hankel
ledger above explains why this projective regular-minor packet has zero
aperiodic full-Hankel residual after the paid ledgers are applied.

The ledger also imports the v4 low-rank update template budget envelope.  Since
both the finite and projective `F_17^32` budget numerators are 6, every nonzero
regular low-rank update chart of rank at most 6 is within the finite regular
root budget.  Without a separate infinity exclusion, projective automatic
safety holds through rank 5; rank 6 needs an infinity exclusion, finite-root
slack, or a deduplication/removal certificate.  Zero determinants remain
singular buckets, not aperiodic evidence.
The v4 packet gate records this as a checked decision rule: projective use of
rank `1..5` low-rank packets is accepted after the nonzero determinant check,
while rank `6` projective use needs an additional endpoint, finite-root slack,
or deduplication/removal certificate.

The ledger also references the M3 syndrome-realizability certificate, which
proves that every length-256 syndrome pencil in this window is realized by
explicit line values on the pinned subgroup row.  The zero-slope subtraction
sidecar shows that the fixed top-window packet's synthetic root `{0}` is paid
by the zero-codeword tangent branch, the extension-denominator audit shows that
the line-value lift is genuinely `F_17^32`-valued, and the projective endpoint
sidecar proves that `[0:1]` is empty for the fixed top-window regular minors.
Its purpose is to make the frontier explicit: generic and synthetic
regular-minor facts are proved and row-realizability is discharged, while
universal tangent/quotient-deduped root tables and singular-bucket outcomes are
still not supplied.

For `A=421..426`, the ledger also records the fixed synthetic packet's M4
mini-table:

```text
B_tan=1, B_quot_support=B_quot_image=B_ext=0,
B_ap_regular_before_removed=1, B_ap_after_removed=0,
B_projective_infinity=0, deduped total upper bound=1 <= budget 6.
```

This is a no-double-counting check for the fixed synthetic packet only.

The ledger also imports the proportional-pencil tangent lemma.  Since
`t+j=256` is the full stored syndrome length for every agreement in this
window, any proportional syndrome pencil `u=c v` has no hidden tail check:
after the tangent/common-code-line ledger is removed, that branch leaves
aperiodic residual `0`.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_regular_window_status.py \
  --check experimental/data/certificates/hankel-f17-32-m3-regular-window-status/f17_32_n512_k256_m3_regular_window_status.json
```

Non-claims: this is not a worst-case MCA bound, not a universal M3 row outcome,
not a full quotient/tangent subtraction table, and not a singular-pivot packet.
