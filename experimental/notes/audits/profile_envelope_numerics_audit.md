
# Audit: profile-envelope quantitative spine

## Claim
Collision-aware lower (eq:collision-aware-lower) recomputes exactly at four deployed rows and matches identity-prefix floors; dual routes agree; a0 unsafe / a1 quiet; g*/g_T dual routes agree; a_cross within a few units of a0.

## Status
EXPERIMENTAL / AUDIT. Does not claim full Eprof upper or closed-ledger at deployed scale.

## Dual routes
L: comb_batch vs math.comb; U: ceil_div vs integer loop; g*: forward grid vs reverse/bisection.

## Reproducibility
```
py -3.13 experimental/scripts/verify_profile_envelope_numerics.py --emit --check
py -3.13 experimental/scripts/verify_profile_envelope_numerics_check.py --check
```
