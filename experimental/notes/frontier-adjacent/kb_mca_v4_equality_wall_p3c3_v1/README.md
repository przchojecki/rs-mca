# KoalaBear K3: \(P_3+C_3\) common-signature exclusion

```yaml
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
agreement: 1116048
B_star: 274980728111395087
architecture: source-bound normalized equality-wall split-scroll
partition_digest: N/A - local normalized residual, no global chart partition
atom_or_cell: reduced Q=6, u=2 conic common-signature branch
quantifier: all 60 labeled P3+C3 graphs in the declared reduced universe
projection_and_unit: distinct affine bad slopes per received line
status: PROVED_LOCAL_REDUCTION
impact: ROUTE_REDUCTION_ONLY
```

## Direct Result

All 60 labeled \(P_3\sqcup C_3\) common-signature graphs in the
source-derived, reduced \(Q=6,u=2\) conic branch are impossible. The
argument identifies the two endpoint free divisors as disjoint
degree-two fibers of the same separable map \(\chi\), then uses the
exact star coordinates to show that both fibers map to the same
normalization point.

The labeled common-signature census is:

| universe | count |
| --- | ---: |
| before the \(P_3+C_3\) exclusion | 465 |
| excluded \(P_3+C_3\) graphs | 60 |
| labeled survivors | 405 |

The values \(46,30,10,10\) reported by the classifier are four
separate orbit counts for four pole-cycle types. They are not a
partition of 405.

## Stack Position

This is stack layer 4 of 4. It consumes parent branch
`review/kb-equality-wall-geometry-v3` at commit
`44542e91e459364a521870ed2ebde7f6fe5055bf`, whose endpoint reduces
the normalized equality wall to the \(Q=6,u=2\)
plane/conic/quartic split.

The inherited facts used by the exclusion are itemized in
`proof/q6_u2_star_conic_geometry_reduction.md`, Section 5.1, with
parent theorem, transferred hypotheses, conclusion, and variable
translation.

## Artifacts

The committed orbit certificate is compact. The classifier
regenerates the complete representative lists and validates every
entry, while the certificate records:

* scalar case and orbit ledgers;
* orbit-size and signature histograms;
* ordered representative digests and digest chains;
* a complete hash for every full classification row;
* a hash of the complete full payload.

Runtime versions are informational metadata outside the
star-conic mathematical payload hash. SymPy is pinned in
`requirements.txt`. Every executable rejects `python -O`, and all
load-bearing checks use explicit exceptions rather than `assert`.

## Replay

From the repository root:

```bash
python3 experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_p3c3_v1/replay.py --quick
python3 experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_p3c3_v1/replay.py --full
```

`--quick` regenerates the exact mathematical payloads in memory and
checks the committed certificates. `--full` additionally runs every
tamper self-test. Hash checks establish artifact identity; the exact
replays establish the encoded finite and symbolic statements.

## Nonclaims

This packet:

* does not exclude every remaining conic or quartic branch;
* does not derive a global pencil-chart census;
* does not aggregate the fixed-union payment of other K3 packets;
* produces no `U_Q`, `U_BC`, `U_new`, or KoalaBear row certificate;
* does not move the active KoalaBear endpoint.

The surviving conic signatures are \(P_6\) and
\(P_2\sqcup C_4\), with the exact second-involution and same-record
owner obligations retained.
