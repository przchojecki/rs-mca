# Frontiers mining map (rs_mca_entropy_frontiers.tex)

## Claim
Complete labeled-statement inventory (215 statements / 5940 lines) with triage classes for the entropy-frontiers SUBMISSION DRAFT campaign.

## Status
EXPERIMENTAL / AUDIT. Heuristic classifications for steering, not final referee judgments.

## Counts
PROVED-IN-PAPER 112, CONDITIONAL 32, DEFINITIONAL 62, OPEN 8, CITED 1.

## Dual routes
generator: lookback label inventory + keyword classify; checker: forward begin→label parse + set overlap.

## Reproducibility
```
py -3.13 experimental/scripts/verify_frontiers_mining_map.py --emit --check
py -3.13 experimental/scripts/verify_frontiers_mining_map_check.py --check
```
