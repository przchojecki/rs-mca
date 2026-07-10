# Lean: integer staircase / identity-profile scale

## Status
EXPERIMENTAL / AUDIT. lake build PASS.
**Named object:** MCA staircase / def:integer-staircase-detail
**Hard input:** (d) profile-envelope comparison

## Object
def:integer-staircase-detail L6667: at a=K+w=5, identity-profile scale
barN_1=C(8,5)/2^2=14 (exact division C(8,5)=14·4); second step w=1 gives
barN_1=C(8,4)/2=35.

## Dual routes
- generator: native_decide on binom/scale + exact-division identity
- checker: decide proofs of the same Nat goals

## Nonclaims
Toy scales only; does not prove the profile envelope e^{o(n)} barN_1.
