# Complete profile-envelope vs target (hard input d)

## Claim
Envelope E=1+(n-a+1)+sum(1+barN) dual-route exact; multi-profile toys exceed identity-only; deployed U(a0)>B*>=U(a1).

## Status
EXPERIMENTAL / AUDIT. Verdict: NO ISSUE. Complete lower at deployed = universal+identity L (no extra atlas terms committed).

## Pins
eq:profile-envelope, thm:intro-asymptotic-rs-mca, eq:intro-target-crossing, lem:safe-side

## Dual routes
- generator: exact int multi-profile E; bigint U vs B*
- checker: alternate expansion; pure integer redeploy

## Reproducibility
```
py -3.13 experimental/scripts/verify_profile_envelope_vs_target.py --emit-defaults --check
py -3.13 experimental/scripts/verify_profile_envelope_vs_target_check.py --check
```
