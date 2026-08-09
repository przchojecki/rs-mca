# K3 `[5,8]` closure: upstream provenance replay audit

## Statement audited

Whether the 23-node `[5,8]` closure packet added to rs-mca PR #1152 is
currently reproducible from its declared public source.

The packet claims 210/210 raw labels are empty and pins public-DAG commit
`3fa2987430242cb631ab76be4ebbee549ce95fb8`.  The audit concerns provenance
and replayability, not the truth or falsity of those mathematical claims.

## Files / sources read

- PR #1152 head `5443db878c488ac9cfa204d1d79e211caf9e8608`.
- `kb-mca-v4-433-1b-cells5-8-close-v1/README.md` and its JSON certificate.
- The advertised public repository
  `AllenGrahamHart/rs-mca-prize-dag` and its live refs.

## Exact checks at `2026-08-09T19:30:12Z`

1. `git fetch origin 3fa2987430242cb631ab76be4ebbee549ce95fb8`
   returned `remote error: upload-pack: not our ref`.
2. GitHub's commit API returned HTTP 422, `No commit found for SHA`.
3. `git ls-remote --heads origin` exposed neither the certificate's named
   branch `codex/full-prize-resolution-v12-20260807` nor the pinned SHA.
4. Current public `origin/master` was
   `fc7133243a42ffdb2fb7d1bcb15611d50bcc564d`; the three pairing-7/8/11
   cell-5 nodes, the cell-5 aggregate, the `[5,8]` aggregate, and the
   duplicate-role transport node were absent there.
5. By contrast, the independent replay packets in #1153 pin
   `28b3bc8ab13e94c25088e904251eb5cf49e68ad2`, which the GitHub commit API
   resolved successfully.

## Dependencies

- **Available:** PR #1152's rs-mca certificate and its list of 23 node paths
  and verifier SHA-256 values.
- **Unavailable:** the declared source commit and named source branch.
- **Not attempted:** the 46 primary/audit executions, because their pinned
  source files could not be obtained.
- **Independent partial control:** the #1153 local adapters replay all six
  residual `xi=3` cell-5 pairing representatives from an older public commit.
  They do not cover endpoint rootlessness or cell-5-to-cell-8 transport.

## Parameter dependence

The unavailable claim is field-specific at `p=2130706433`, agreement
`1116048`, role orbit `[5,8]`, and the positive 433-1b guarded route.  No
dependence on `T`, `Y`, `L`, `L_barI`, `lambda`, or `I` appears.

## Layer-cake / dyadic summability

Not applicable.

## Moment / Markov / Chebyshev

Not applicable.  The falsified FLOOR-v2 random-word first-moment route is
unrelated to this local provenance gate.

## Edge cases / notation

An unavailable commit is not a counterexample and does not refute the closure.
It does prevent the advertised independent replay and therefore prevents a
GREEN audit.  A later public push or durable re-pin can remove this blocker.

## Numerical evidence

None is promoted here.  The separate exact pairing replays are only partial
controls on the larger 23-node implication chain.

## Verdict

**RED for current reproducibility; NO VERDICT on mathematical truth.**

The source-bound 23-node chain cannot currently be reviewed from the public
provenance declared by #1152.  The `[5,8]` closure must not be treated as
independently GREEN on this evidence alone.

## Remaining risks

Even after the source commit is restored, a reviewer must check all verifier
hashes, run all primary and hostile audits, and inspect the load-bearing
endpoint-rootlessness, orbit-partition, and duplicate-role transport proofs.

## Minimal next action

Ask the source maintainer to push the exact commit or update #1152 to a
fetchable immutable commit.  Then replay all 23 verifier/audit pairs and audit
the endpoint and transport implication chain before changing the verdict.
