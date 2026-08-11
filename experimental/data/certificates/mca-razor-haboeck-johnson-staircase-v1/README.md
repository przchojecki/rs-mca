---
workboard_item: MCA
row: official maximal rate-half (n=2^41, k=2^40)
object: MCA
target_epsilon: 2^-128
direct_statement: For every admissible q >= Q_9*2^128 (log2 q >= 232.650530), a_RH(q) <= a_m(q) with m(q) = max{m: Q_m*2^128 <= q}; on every razor row q > 2^255.9, a_RH(q) <= a_94 = 1563215236073 < 3n/4, upgrading to a_95 = 1563128173124 above Q_95*2^128; m = 96 is unaffordable under q < 2^256.
status: PROVED
impact: MOVES the razor crossing safe bracket below 3n/4 for the first time
quantifier: safe side only; no adjacent-unsafe witness at a_m - 1; per-q, exact integers
claimed_bound: bracket-top gain 86,139,268,540 agreement steps on razor rows (3n/4 = 1,649,267,441,664 -> a_94)
falsifier: an admissible q and received pair with B_mca(a_m(q)) > floor(q/2^128)
replay: python3 background/nodes/rate_half_haboeck_quadratic_johnson_safe_bracket/verify.py (+ verify_audit.py) at https://github.com/AllenGrahamHart/rs-mca-prize-dag @ 4e77e95b3acf
---

# The razor Haboeck-Johnson staircase

Exact official-row specialization of the imported quadratic theorem, with
rho = (k-1)/n (the d = k-1 reindex verified independently and shown
load-bearing at the last unit). The full proved staircase, landmarks:

    m=9  from log2 q ~ 232.650530 : a_9  = 1,641,330,047,987 (first < 3n/4)
    m=20 @ ~240.42 : a_20 = 1,593,817,862,387
    m=40 @ ~247.54 : a_40 = 1,573,574,783,987
    m=60 @ ~251.46 : a_60 = 1,568,006,769,587
    m=80 @ ~254.14 : a_80 = 1,565,216,767,187
    m=94 on every razor row : a_94 = 1,563,215,236,073
    m=95 above Q_95*2^128   : a_95 = 1,563,128,173,124
    m=96 unaffordable (Q_96 > 2^128 - 1)

Q_94*2^128 < 2^255.9 < Q_95*2^128 < 2^256 (tenth-power integer check), so
every razor row affords m = 94. All integers re-derived from (HJ1) alone by
an independent implementation; the safe-bracket verifier characterizes both
roundings (floor on Q_m, ceil on a_m — both safe-side).
