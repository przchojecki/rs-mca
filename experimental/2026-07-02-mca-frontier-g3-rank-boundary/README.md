# External G3 Rank-Boundary Toy Evidence + Tangent-Convention Reconciliation

- **Status:** EXPERIMENTAL / AUDIT (external toy evidence; one convention
  question for maintainers).
- **Agent/model:** Claude Fable 5 acting for latifkasuli.
- **Scope:** toy-scale rank-boundary evidence for the residual (non-tangent,
  non-quotient) accounting question behind middle-band floor exactness, plus a
  worked stable aperiodic family, from the external `mca-frontier` repository
  (`github.com/latifkasuli/mca`). Not a deployed-row certificate and not a
  prize-resolution claim.

## Use Rule header (per `m0_prize_mca_definition_freeze.md`, PR #171)

```text
object:            toy rank-boundary ledger + aperiodic family census
sampler:           finite_affine
q_line:            97 (toy rows; deployed-row conventions not consumed)
agreement/radius:  a = 11, r = 5 (rank boundary);  a = 3n/4, r = n/4 (mu4 rows)
statement type:    closed-grid toy observations only; no supremum claim
paid ledgers:      quotient-periodic and tangent packets subtracted via the
                   support-family criterion below; criterion match to the M4
                   filter is the conditional dependency this note asks about
```

## Two tangent senses (the convention question)

The PR #171 certificate `hankel-f17-32-m3-finite-tangent-overlap` defines the
M4 finite tangent filter at the **slope** level: a finite slope `z` is
tangent/common-code-line iff `Syn(f+zg) = u + z v = 0` in all stored
coordinates (unique slope `z=-c` when `u=cv`; the `u=v=0` codeword-line branch
is removed before aperiodic accounting).

The external ledgers below use a **support-family** classifier for the same
exclusion purpose: an assigned exact-size-`a` witness support family is
tangent (i.e. belongs to the moving-root tangent-packet stratum) iff any pair
of its supports overlaps in `>= a-1` coordinates; the non-tangent guardrail is
`max_pairwise_overlap <= a-2`. This criterion was regression-tested the hard
way: an earlier common-core-of-all version nearly certified a fake
counterexample, and the corrected pairwise version is what all ledgers cited
here use.

**Question for maintainers:** for residual/aperiodic accounting in the middle
band, is the support-family classifier above an acceptable packet-level
stand-in for "not the tangent-packet stratum," alongside (not instead of) the
per-slope syndrome filter? If the intended boundary object is different,
which convention should external ledgers target?

## Toy rank boundary (corrected ledgers)

Row `F_97, n=16, k=8, a=11`; residual model `Lp1 = 7`, local cap heuristic
`<= 6`. A fully-unlocked non-tangent non-quotient `Lp1=7` family would be a
`>= 7` residual construction; none is found:

| fact | value | artifact (external repo) |
|---|---|---|
| counterexample found | `false` | `runs/g3_lp7_counterexample_corrected.json` |
| non-tangent non-quotient min `rank(Gamma)` | `6` (full) | same |
| random baselines `deg(E)=1..4` | all `min_rank 6`, `21/21` locked (~2985 samples each) | same |
| boundary census rank distribution | `{6: 74102}` | `runs/g3_lp7_boundary_corrected.json` |
| min locked among rank-5 candidates across prongs | `21` | same |
| determinantal wall | deficiency `0`, `21/21` locked | `runs/g3_rankdrop_locus_corrected.json` |

A narrower verified-witness layer records `rank 5` with `6` locked pairs
(`runs/g3_partial_theorem_ledger.json`); its witnesses re-verify but its
search breadth is smaller, so the lock-floor statement
(`genuine non-tangent + deficient => at least one locked pair`) is motivation
for the next proof obligation, not a headline claim.

## Worked aperiodic family: mu4 monomial lines

Monomial pairs `f=x^u, g=x^v` with `u,v >= k` (both sides above the
codeword-line branch). Exhaustively over the two-sided space at both tested
rows, the nonzero content is exactly `u-v = +-n/4`:

| row | result |
|---|---|
| `F_97,n=16,k=8,a=12` | all 28 aperiodic pairs exact: nonzero iff `u-v=+-4`, count `4`, slopes `mu_4(F_97)={1,22,75,96}` |
| `F_97,n=32,k=16,a=24` | full 240-pair two-sided grid exact: nonzero iff `u-v=+-8`, always count `4`, same slopes |
| `F_97,n=32,k=16,a=28` | `mu_8`-shaped pairs: exact count `0` (no `mu_{2^r}` tower) |

The `n=32` sweeps are complete because `r = n-a` is within the unique-decoding
radius. Count is pinned at `|mu_4| = 4` while the tangent floor grows
(`5 -> 9`): a stable, bounded, non-floor-beating family.

Tangency status in **both** senses: every counted slope has
`Syn(f+zg) != 0` (checked directly: `h_z` interpolates to degree `>= k` on
the full domain for all 16 pair/slope combinations at `n=16`), and every
witness family is support-family non-tangent (`max_pairwise_overlap 8 <= 10`
at `n=16`, `16 <= 22` at `n=32`). Any middle-band exactness argument must
budget this family; at deployed thresholds its count `4` is harmless.

## Machine-readable evidence

`g3_rank_boundary_toy_evidence.json` in this directory carries the values
above with artifact pointers into the external repository (frozen at the
commit named in the JSON). The external repository also has a stdlib-only
second-stack replayer (`py/certcheck.py bank`) for its candidate-bank sweeps.

## What to do next

1. Maintainer answer to the convention question above (M4 tangent filter vs
   support-family classifier for packet-level residual accounting).
2. If the classifier is acceptable: the toy rank-6/all-locked wall and the
   mu4 census become citable external evidence for the middle-band residual
   program; the natural next external experiment is the same boundary at a
   deployed-shape row.
3. If a different convention is intended: the external ledgers re-run under
   the intended criterion (the classifier is one shared module).
