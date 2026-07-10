# Deployed template finite-fragment replay

## Claim
prop:verification-template has no printed deployed numbers. Finite identity-prefix + collision-aware chain on KB MCA and M31 MCA matches q-r1 floors; U(a0)>B_*, U(a1) quiet. (A2)--(A7) remain OPEN.

## Status
EXPERIMENTAL / AUDIT.

## Dual routes
ceil_div vs integer loop / binary search for U; comb_batch vs math.comb for L.

## Reproducibility
```
py -3.13 experimental/scripts/verify_deployed_template_replay.py --emit --check
py -3.13 experimental/scripts/verify_deployed_template_replay_check.py --check
```
