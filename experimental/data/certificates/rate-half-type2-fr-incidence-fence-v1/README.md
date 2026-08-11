---
workboard_item: LIST/MCA shared (type-2 residual)
row: power-of-two scale family
object: type-2 stratum of the residual-budget program
direct_statement: The max-vs-mean upgrade (FR) for arbitrary joint supports W cannot follow from the banked incidence axioms: an explicit m=64 quartic cyclotomic set system satisfies all of them with max |S ^ W| = 189 > 2m = 128.
status: PROVED (route fence)
impact: LOCAL_ONLY (with a proved complement, see body)
falsifier: a derivation of |S ^ W| <= 2m + O(1) from block sizes, d_x <= e, the saturation deficit, pairwise unions, and the MDS spend floor alone
replay: python3 background/nodes/rate_half_type2_fr_incidence_only_route_fence/verify.py (+ verify_audit.py) at https://github.com/AllenGrahamHart/rs-mca-prize-dag @ 4e77e95b3acf
---

# Type-2 (FR) incidence-only route fence — with its proved complement

The fence: incidence axioms alone cannot bound |S_gamma ^ W| by ~2m for
arbitrary a-sets W (explicit m = 64 witness, hash-pinned, two independent
implementations).

The complement (campaign round 32, exhaustive over all 32,896 pair unions
of the fence's own blocks): at every CANONICAL W* = S_g u S_h the same
system satisfies max |S_gamma ^ W*| = 115 <= 2m — and at any minimising
pair union, |S_gamma ^ W*| <= 4rho - 2a* - 2o_gamma - o_g - o_h is a
two-line cardinality identity. The fenced statement is the arbitrary-W
form; the canonical form is a theorem. Together they price the type-2
residual at 7/4 over the band (9/8 at a = 7m-1), with the exactly-8/5
missing step named in the campaign record.
