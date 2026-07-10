# New-draft mining map

## Status
EXPERIMENTAL / AUDIT. Verdict: NO ISSUE. W35-R1: remark+hypothesis envs in ENVS.

## Spot-check
- rem:balanced-core-exhaustion env=remark status=DEFINITIONAL
- hyp:ray-compiler env=hypothesis status=CONDITIONAL

## Dual routes
- generator: lookback with \end{env} stop; ENVS include remark,hypothesis
- checker: forward begin→label exact end match; set equality

## Reproducibility
```
py -3.13 experimental/scripts/verify_newdraft_mining_map.py --emit-defaults --check
py -3.13 experimental/scripts/verify_newdraft_mining_map_check.py --check
```
