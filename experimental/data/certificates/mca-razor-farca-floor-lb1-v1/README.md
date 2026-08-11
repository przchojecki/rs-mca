---
workboard_item: MCA
row: official maximal rate-half (n=2^41, k=2^40)
object: far-CA slope count B_ca^far of a column-far pair
direct_statement: LB1: for every admissible q with n < (a-k-1) log2 q — in particular every posed row q > 2^167 — and every a in the open bracket, there exist column-far pairs with B_ca^far(a) >= n-a+1; the banked upper bound T <= r+1 is TIGHT on its whole proved domain, and B_ca^far(3n/4) >= 2^39+1 makes residual budget 2^39 unattainable at the bracket top.
status: PROVED (counting construction; machine-checked arithmetic; exhaustive at the validation cell)
impact: first lower bound on B_ca^far at the safe index; two-sided window [2^39.9773, 2^128) at a = k+2^34
falsifier: a proof that every column-far pair at some posed row and bracket-interior a has fewer than n-a+1 CA-bad slopes
replay: python3 notes/pilots_20260810/rh_overlap_cap/d4_lb1.py and d2_maxcore.py at https://github.com/AllenGrahamHart/rs-mca-prize-dag @ 4e77e95b3acf
---

# LB1 — the far-CA floor at the razor rows

Construction (the maximal-core pencil): E an (a-1)-set, T = D \ E,
d_2 = 1_T, d_1 = -lam_j on T with distinct nonzero lam_j. For all but a
2^n q^{k-a}(1 + q^{1+k-a})-fraction of assignments the pair is column-far
at radius r = n-a, its finite CA-bad slopes are exactly {lam_j} (r+1 of
them, one witness each, agreement sets E u {j}), and every pairwise
overlap equals a-1. Admissibility (LB1-C): n < (a-k-1) log2 q — margin
670,014,898,009 at the bottom of the posed range q > 2^167; fails only
below ~2^129.

Consequences: (i) B_ca^far(k+2^34) >= n-a+1 = 1,082,331,758,593 =
2^39.9773 — the first lower bound at the safe index, 88.02 bits under the
2^128 budget; (ii) the banked tall-regime bound T <= r+1 is attained, i.e.
B_ca^far(n-r) = r+1 exactly on its whole proved domain; (iii)
B_ca^far(3n/4) >= 2^39+1, matching the campaign's precision-fixed budget
exactly: residual budget 2^39 is unattainable at a = 3n/4. Verified
exhaustively at the (n,k,q) = (8,4,17) cell over all 46,656 witness
assignments, and by sampling at six more cells over three scales; the
refutation of the pre-LB1 overlap-cap route STRENGTHENS with scale.
