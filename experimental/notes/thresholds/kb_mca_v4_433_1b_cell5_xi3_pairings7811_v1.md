# K3 cell-5 xi=3 pairings 7/8/11: exact local route-cut audit

```yaml
workboard_item: K3
row: KoalaBear MCA at target epsilon 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: the guarded positive 433-1b source-role cell-5 xi=3 representatives 7, 8, and 11 are empty over F_2130706433
architecture: K3 coordinate-positive 433-1b source-role workboard
partition_digest: public-DAG-433-1b-router@28b3bc8a
atom_or_cell: source-role cell 5; xi=3; pairings 7,8,11
quantifier: all 24 exact source/colored sign rows printed in the certificate
projection_and_unit: local matching labels; not yet a v4 slope atom
claimed_bound: zero witnesses in the declared local cells
status: EXPERIMENTAL_REVIEW_REQUIRED
impact: ROUTE_CUT
falsifier: a covered witness, terminal pair solution, unresolved branch, unhandled degree drop, or source-hash mismatch
replay: certificate verifier plus source-bound local FLINT/SymPy run
```

## Statement audited

The implication from the public cell-5 four-basis tower and compact kernel to
emptiness of the `xi=3` pairing representatives `7`, `8`, and `11`.

The three cell-4 compilers have a common algebraic core.  For two quadratics,
the Sylvester resultant is

\[
(af-cd)^2-(ae-bd)(bf-ce).
\]

Writing the residual conjugate equation as `E(y)+z O(y)` with `z^2=y`
gives the sign-free cut `E(y)^2-y O(y)^2`.  The adapter changes only the
structure rows to the cell-5 `c_row_index=6` base, `b`, and `c` relations and
reclassifies a free `b` or `c` only when the corresponding cell-5 leading
coefficient vanishes.

## Files read

- The public-DAG theorem statements, proofs, audits, and executable templates
  for pairings `7`, `8`, and `11` at commit `28b3bc8a`.
- The public cell-5 four-basis tower and compact kernel pinned by SHA-256 in
  the certificate.
- The predecessor pairings-3/4/5 adapter, certificate, and audit note.

## Exact census

| Pairing | Signed rows | Target roots | Candidates | Source routes | `z` / `q` candidates | Terminal pairs | Witnesses |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 7 | 8 | 44 | 100 | 96 | 8 / 8 | 0 | 0 |
| 8 | 8 | 44 | 100 | 96 | 8 / 8 | 0 | 0 |
| 11 | 8 | 52 | 108 | 120 | 24 / 24 | 0 | 0 |
| **Total** | **24** | **140** | **308** | **312** | **40 / 40** | **0** | **0** |

The certificate separately records 216 guarded boundary rows, 48 target
product boundaries, and 124 no-lift rows.  Resultant vanishing is treated only
as a necessary lift condition; every surviving `q` candidate is replayed in
the original three pair equations, and every terminal third-pair cut is
nonzero.

## Independent tool check

Wolfram independently simplified the difference between the quadratic
Sylvester resultant and the displayed formula to `0`.  It also returned
`E^2-y O^2` for `(E+z O)(E-z O)` after substituting `z^2=y`.  This checks the
common symbolic compiler core, not the exhaustiveness of the 24-row replay.

## Dependencies

- **PROVED upstream:** the cell-5 four-basis tower and compact kernel; the
  three cell-4 compilers; and the universal outside-role transport theorem.
- **Exact computation here:** all 24 deployed-field rows have no witness,
  terminal pair solution, or unresolved branch.
- **UNPROVEN here:** correctness of the adapter substitution, completeness of
  boundary reclassification, and composition with source-role transport and
  exact labeled add-back.
- **Predecessor dependency:** the pairings-3/4/5 packet is separately YELLOW
  and requires the same fresh-review gate.

## Parameter dependence

This result is only over `F_2130706433`, at source-role cell `5`, `xi=3`, and
pairings `7,8,11`.  There is no asymptotic statement and no dependence on
`T`, `Y`, `L`, `L_barI`, `lambda`, or `I`.

## Layer-cake / dyadic summability

Not applicable.

## Moment / Markov / Chebyshev

Not applicable.  In particular, the falsified FLOOR-v2 random-word
first-moment route is not used.  This packet provides no estimate for the
global exact sparse-layer maximum `S_sparse`.

## Edge cases / notation

The replay enumerates both source signs, both colored signs, and both terminal
conjugate lanes.  It records vanishing guards, target-product boundaries,
no-lift rows, and free-polynomial degree drops separately.  A resultant zero
is never promoted to a solution without original-equation replay.

## Numerical evidence

This is an exact deployed-field census, not a toy random sweep.  It is still
computer-assisted evidence until a fresh reviewer independently validates the
adapter and transport/add-back implication.

## Verdict

**YELLOW — the local route cut is exact and exhaustive, but independent review
is required before closing the `[5,8]` role orbit.**

PR #1152 later asserted a full `[5,8]` closure using a newer 23-node public-DAG
packet.  At the 2026-08-09 audit, its pinned commit was not publicly fetchable,
so that larger implication could not be independently replayed.  The present
packet remains useful as a public, independent replay of the six `xi=3`
cell-5 representatives, but it does not validate #1152's endpoint or
cell-5-to-cell-8 transport nodes.  No v4 ledger movement, K3 closure, or
KoalaBear-row closure is claimed.

## Remaining risks

The load-bearing risks are the source-to-cell-5 adapter, degree-drop boundary
coverage, source-role-to-cell-8 transport, and exact labeled add-back.  The
same model generated this packet and performed this audit, so it cannot supply
the required independent approval.

## Minimal next action

Republish the exact source commit pinned by PR #1152 (or re-pin the certificate
to a durable public commit), then replay all 23 primary verifiers and hostile
audits.  The fresh reviewer must also audit the endpoint-rootlessness and
duplicate-role transport implications.  Until then, preserve the unavailable
provenance as an explicit route cut rather than treating `[5,8]` as GREEN.
