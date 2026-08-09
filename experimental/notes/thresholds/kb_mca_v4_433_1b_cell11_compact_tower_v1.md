# K3 433-1b cell-11 compact-tower audit

```yaml
workboard_item: K3/K4
row: KoalaBear MCA at target epsilon 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: three exact guarded towers, empty deployed leading boundaries, and a ten-row coefficient kernel for cell 11 at epsilon=(-1,-1), pivot 1
architecture: K3 coordinate-positive 433-1b source-role workboard
partition_digest: public-DAG-433-1b-router@28b3bc8a
atom_or_cell: source-role cell 11
quantifier: the exact guarded common locus in the declared source-sign chart
projection_and_unit: local common-locus parameters; not affine slopes or a v4 atom
claimed_bound: structural reduction only; no witness count
status: EXPERIMENTAL_REVIEW_REQUIRED
impact: LOCAL_ONLY
falsifier: a nonzero tower or kernel remainder, a deployed boundary point, or a surviving untransported signed-pair component
replay: local SymPy/Singular replay, canonical certificate, 16 hostile mutations, and Wolfram boundary cross-checks
```

## Statement audited:

For the public 433-1b source-role cell-11 pilot over
`F_2130706433`, at `epsilon=(-1,-1)` and pivot `1`:

1. each of the `c_row=5,6,7` three-equation presentations generates the
   guarded eight-equation common locus;
2. on the selected `c_row=5` chart, both the quadratic-`b` and linear-`c`
   leading-coefficient boundary ideals have no deployed-field point; and
3. a primitive eight-coordinate kernel annihilates all ten Vieta rows modulo
   the guarded common locus.

This is a local structural lemma.  It is not the complete cell-11 signed-pair
resultant dichotomy and does not close role orbit `[11]`.

## Files/sections read:

- `agents.md`, including K3/K4, bankability, computational-packet, and stop
  rules.  The ancestor-chain guide's printed snapshot is older than current
  `origin/main@b99b2c461`; its direct K-lane contract remains controlling.
- The public common Vieta compiler, product-rank compiler result, and
  cells-5/11 pivot-pilot result pinned in the certificate.
- The public cell-5 compact-kernel and four-basis-tower compiler methods used
  only as executable construction templates.
- The predecessor cell-5 pairings-3/4/5 and pairings-7/8/11 packets.

## Dependencies:

- **IMPORTED / source-bound:** the public pilot's eight-polynomial lex basis,
  common Vieta equations, and product cofactors at commit `28b3bc8a`.
- **PROVEN by exact local computation:** all eight pilot equations reduce to
  zero under each of three reduced towers.  Their tower basis sizes are
  `43`, `39`, and `41`; each ideal has dimension one.
- **PROVEN by exact local computation:** the selected chart's two boundary
  ideals are zero-dimensional.  Each has one deployed `r` lift; the induced
  monic quadratic in `b` has nonsquare discriminant, so neither boundary has
  an `F_2130706433` point.
- **PROVEN by exact local computation:** the eight primitive kernel
  coordinates satisfy all ten Vieta rows modulo the guarded common locus.
- **INDEPENDENT TOOL CONTROL:** Wolfram reproduced both quartic
  linear-times-cubic factorizations and both Euler-criterion values.
- **UNPROVEN:** the complete necessary signed-pair resultant and its factor
  classification, all source signs, outside-role transport, labeled add-back,
  and projection to distinct affine slopes.
- **UNVERIFIED:** fresh reviewer approval.  The generator performed this
  audit and therefore cannot bless it.

## Parameter dependence:

The result is finite and specific to `F_2130706433`, cell `11`, source sign
`(-1,-1)`, and pivot `1`.  It contains no asymptotic constants and no
dependence on `T`, `Y`, `L`, `L_barI`, `lambda`, `I`, or a dyadic index.

## Layer-cake / dyadic summability:

Not applicable.  No level-set integration or additive dyadic error occurs.

## Moment / Markov / Chebyshev:

Not applicable.  In particular, this packet does not reuse the falsified
FLOOR-v2 random-word first-moment route.  The global analytic obligation is
an upper bound for the exact sparse-layer maximum `S_sparse`, which is not
addressed here.

## Edge cases / notation:

The guard explicitly removes zero, collision, and sign-degenerate factors.
The two leading coefficients are not silently inverted: their boundary
ideals are computed separately and shown deployed-field empty.  The public
pilot's `quotient_exact=false` flag is preserved as an input fact rather than
promoted.  A kernel identity on a common curve is not identified with an
affine-slope count.

## Numerical evidence:

The evidence is exact arithmetic over the deployed prime field, not floating
point and not a random or toy scan.  It proves the printed finite polynomial
identities conditional on the source-bound construction.  It does not prove
exhaustive signed-pair emptiness or any asymptotic sparse-layer inequality.

## Verdict:

**YELLOW - the exact local structural reduction is complete, but the orbit
closure implication and independent review remain unresolved; do not
authorize a global proof.**

## Remaining risks:

The main mathematical risk is a primitive component of the complete
signed-pair resultant that is invisible to the common-kernel calculation.
Degree drops beyond the two tower-leading boundaries, sign transport, and
outside-role/labeled add-back must be handled explicitly.  No v4 ledger atom
or KoalaBear numerator changes.

## Minimal next action:

Compute the complete necessary signed-pair resultant over the selected exact
tower, reduce and factor it with explicit leading/scale boundary branches,
then classify every factor as empty, transported/paid, or
`UNPAID_PRIMITIVE`.  Replay the factorization independently before extending
from `epsilon=(-1,-1)` to the remaining sign and role charts.

OPEN GAP

