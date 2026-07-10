# First-match atlas (hard input a)

## Claim
Witness-exhaustive first-match atlas on `asymptotic_rs_mca_frontiers.tex`: every toy witness lands in exactly one first-match bucket; dual routes agree.

## Status
EXPERIMENTAL / AUDIT. Verdict: NO ISSUE.

## Pins
def:first-match, eq:first-match-projections, lem:first-match-bound, def:primitive-first-match-residual, prop:first-match-atlas-finite

## Dual routes
- generator: sequential set-difference first-match + witness residual filter
- checker: indicator-matrix least-index over sorted slopes

## Reproducibility
```
py -3.13 experimental/scripts/verify_first_match_atlas.py --emit-defaults --check
py -3.13 experimental/scripts/verify_first_match_atlas_check.py --check
```
