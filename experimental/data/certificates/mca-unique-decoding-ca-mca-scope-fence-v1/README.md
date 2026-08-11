---
workboard_item: MCA
row: official maximal rate-half
object: MCA
direct_statement: The unique-decoding CA/MCA transfer (gate 2r <= n-k) is equivalent to a >= 3n/4 at rate 1/2; the whole live crossing interval [k+2^34, 3n/4) is outside its scope, failing by exactly 2 at a = 3n/4 - 1.
status: PROVED
impact: ROUTE FENCE (redirects the safe-side search to direct MCA theorems)
falsifier: a valid instance of the named transfer at some a < 3n/4
replay: python3 background/nodes/rate_half_unique_decoding_ca_mca_scope_fence/verify.py at https://github.com/AllenGrahamHart/rs-mca-prize-dag @ 4e77e95b3acf
---

# Unique-decoding CA/MCA scope fence at rate one-half

Why the staircase had to be a direct MCA import: the published
unique-decoding CA-to-MCA conversions (ACFY25 Lemma 4.10 / the BCIKS
unique-decoding input) carry the exact gate 2(n-a) <= n-k, which at rate
1/2 is a >= 3n/4 on the nose. Every agreement in the open crossing
interval fails it (by exactly 2 at the closest interior point), so a
beyond-half-distance conversion would be new mathematics.
