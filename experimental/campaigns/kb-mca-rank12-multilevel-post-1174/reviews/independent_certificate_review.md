# Independent certificate, custody, and publication review

Date: 2026-08-20

Reviewer: fresh isolated `rank12_packet_custody` subagent

## Statement audited

This review covers the publication packet for two deliberately scoped
claims on one actual KoalaBear received line at the initial affine-error
rank-twelve row:

1. the complete scalar truncated-margin resource and selected-support first
   moment cannot force the existing rank-ten child; and
2. the actual-line gluing quotient has received-pair image rank zero, one,
   or two, with the complete guarded rank-zero family bounded by
   `49106899082787469` slopes.

The packet claims no payment for quotient ranks one or two, no payment of
affine error rank twelve, no active-v4 ledger movement, and no KoalaBear
closure.

## Files and sections read

- the four new labelled source statements and their proofs in
  `experimental/grande_finale.tex`;
- both proof notes, both Sage controls, the threshold note, campaign
  contract, frontier map, dependency and claim ledgers, review tables, and
  proposed PR description;
- the primary Python verifier, canonical result, manifest verifier,
  certificate README, and sealed manifest;
- the independent mathematics review;
- live GitHub metadata for PRs #1160 and #1174 and the current open-PR
  search for overlapping rank-twelve supported-dual/gluing work.

## Exact custody

The reviewed Git base is exact PR #1174 head
`1b613fc669158a690a52b64f0eeb440f10672f1e`.  The separately imported
near-rational dependency is exact PR #1160 head
`c5f4ea7a0c78828c901ae5f3428894a8b2e2806b`.  Both are live, ready,
mergeable PRs based on `93fba1be3f3299b0ba4708d88715377bbb656e45`,
and neither is an ancestor of the other.  The successor therefore must not
be integrated or advertised as unconditional until an integration tree
containing both artifacts is replayed.

Before final sealing, this review found that the primary verifier and
manifest used bare `assert` statements and that the advertised hostile
mutations were not genuine validator replays.  The coordinator replaced
those checks with explicit fail-closed rejection, added a canonical
`validate_result`, converted all eight cases to deep-copy mutations followed
by validation, and resealed the unchanged mathematical result.  The current
bytes, not the rejected preliminary verifier, are the subject of this GREEN
review.

The final registry-inclusive sealed payload contains 23 files and reports:

```text
canonical result SHA-256  79b056f8e5cf87269c31e52b52c981a0887c0412fe38395ad71e4c058039e684
result-file SHA-256       0d2c2e7fa55afe5bf8cda8b029a9f0ac90c9e42d0e9da4e0068cdbabc9de1ea4
active-source SHA-256     7fe84b53e038c962cd3ab663d2300c848e57c204a1e231dfeae160bca0178946
internal result payload   d98050cea1db01c7a80452b6fabcbeb3197d932103f9a119846c58eda5593417
manifest-file SHA-256     0dd3ceb32f8800c9aed66cdd2531ea508dd5bd5577aca21edc4956814f44c7b0
```

The four declared source labels each occur exactly once.  Reviews remain
outside the hashed packet to avoid self-reference.  The review-registry and
public-wording rows are included in the final manifest above; the final
normal and optimized replays both pass.

## Independent replay

All checks below passed on the repaired, currently reviewed theorem,
generator, result, and source bytes:

```text
primary Python, normal                         PASS, 8/8 rejected
primary Python, optimized (-O)                 PASS, 8/8 rejected
external optimized C_11 tamper                 REJECTED
manifest, normal                               PASS, 23 files
manifest, optimized (-O)                       PASS, 23 files
external optimized manifest rejection gate    REJECTED
independent result payload recomputation       PASS
independent big-integer rederivation           PASS
SYZ25 negative and incremental-overlap Sage    PASS
GF(11) post-near rank-zero Sage regression     PASS
campaign audit --require-actionable            PASS, 8 claims/9 dependencies
provisionally verified campaign claims         C-006 and C-008
source-label uniqueness                        PASS, 4/4
pdflatex after reference stabilization         PASS, 127 pages
git diff --check                               PASS
generated Sage/Python byproducts                NONE
```

The independent integer replay reproduced

```text
C_11                                      3313389801746721900417
capped records                            49103551414195675
resource remainder                        56673
minimum abstract core incidence           252089545421228709377370
first-moment forced coordinate            120205662451376300
first-moment child shortfall               128500736889912070
rank-zero cap                              49106899082787469
rank-zero child slack                      199599500258500901
pair types needed                          230227321946
proved pair-type cap                       12761830235484
```

## Dependencies

- **PROVEN in the packet:** exact scalar optimizer, canonical arithmetic,
  result identities, fail-closed mutations, source-label binding, and the
  declared zero-ledger nonclaims.
- **PROVEN and independently reviewed:** actual-line orthogonal-complement
  identities, the guarded rank-zero injection/payment, and the
  incremental-overlap route.
- **IMPORTED / CONDITIONAL:** #1160's `2d` near-rational deletion.
- **IMPORTED:** #1174's rank-eleven resource and rank-ten child target.
- **OPEN:** actual-record payments for gluing ranks one and two, affine-error
  rank twelve, and active-v4 chronology reconstruction.

## Parameter dependence

All published integers are tied to the printed initial KoalaBear values
`R=1048576`, `d=67472`, `n=2097152`, `m=1116048`, and the exact #1174
rank-ten child.  The rank-zero payment also requires the printed
exact-support, `dim(C')=11`, and `|U|>=m` guards.  It is not transported to
shortened rows.  No hidden asymptotic parameter is used.

## Layer-cake / dyadic summability

Not applicable.  The packet contains no layer-cake or dyadic summation.

## Moment / Markov / Chebyshev

Not applicable.  The packet uses exact finite combinatorics and integer
optimization, not a moment tail argument.

## Edge cases and notation

The source distinguishes the post-near unsafe load from an actual RS
counterexample, selected-support incidence from complete pair-core geometry,
and the local gluing quotient from active-v4 owners.  The GF(11) control
guards the critical boundary where a rank-zero common pair core coexists
with support-wise bad slopes.  The names `rank zero`, `rank one`, and `rank
two` refer only to the two-dimensional received-pair image in the gluing
quotient.

## Numerical evidence

The large constants are exact integer identities, not sampled numerical
evidence.  The two finite-field controls are boundary regressions only; they
do not prove the KoalaBear theorem by extrapolation.  The abstract incidence
extremizer is explicitly not claimed Reed--Solomon realizable.

## Publication and overlap

The proposed PR wording is conservative: it says partial rank-twelve
payment/method barrier, zero active-v4 movement, and no row closure.  A live
open-PR search found no other PR claiming this scalar-resource barrier or
actual-line supported-dual rank-zero payment.  PR #1170 is adjacent
conditional rank-eleven component geometry, not a duplicate of this
initial-row theorem.

PR #1174 was a draft for procedural dependency reasons rather than a known
mathematical defect; it is now ready and mergeable.  This successor remains
publication-worthy only as a separate conditional packet, with its exact
#1160/#1174 integration requirement prominent.

## Verdict

**GREEN - the repaired certificate, custody boundary, source labels, exact
arithmetic, controls, and conservative public wording are publication-ready.
The required registry-inclusive administrative reseal is complete and its
normal and optimized replays pass.**

This verdict does not upgrade the mathematical scope: quotient ranks one
and two and affine error rank twelve remain open, and active-v4 ledger
movement remains zero.

## Remaining risks

- The eventual integration commit containing both #1160 and #1174 must be
  replayed; present mergeability does not prove combined-source custody.
- The Wolfram replay mentioned in the log is not a separately hashed packet
  artifact; it is corroborative only and is not needed by this verdict.
- The next theorem must work on actual received-line records and preserve
  slope and chronology; abstract supported-dual generation alone is
  insufficient.

## Minimal next action

Stage exactly the reviewed packet, verify the staged diff and manifest once,
and publish it with the #1160/#1174 integration condition prominent.  Do not
include generated `.sage.py` or cache files.
