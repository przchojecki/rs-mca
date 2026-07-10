# Frontiers mining map (rs_mca_entropy_frontiers.tex)

## Claim
Complete labeled-statement inventory after W27-R1 parser+oracle fix: **213** statements / 5940 lines with triage classes for the entropy-frontiers SUBMISSION DRAFT campaign.

## Status
EXPERIMENTAL / AUDIT. Heuristic classifications for steering, not final referee judgments.

## Counts (post-fix cert; payload_sha256 `5a128b97193c6c577a21277963d2193f7a087099da0e2a3a0d6b990af1c250c8`)
- PROVED-IN-PAPER **88**
- CONDITIONAL **65**
- DEFINITIONAL **56**
- OPEN **3**
- CITED **1**
- Total **213** (section headers dropped; no soft-pass oracle)
- Fix-commit content identity: 4d8bdea (parser+oracle); this tip = W29 note/draft refresh rebased on 2b1a7e2

## Dual routes
generator: lookback label inventory with `\end{env}` stop + keyword classify; hard 10/10 oracle
checker: forward begin→label parse + set overlap + no sec: leak

## Weave with #494
holmbuar open PR #494 is a curated 33-instance five-class entropy-frontiers audit.
This packet is the **exhaustive** labeled-statement inventory complement.

## Reproducibility
```
py -3.13 experimental/scripts/verify_frontiers_mining_map.py --emit --check
py -3.13 experimental/scripts/verify_frontiers_mining_map_check.py --check
```