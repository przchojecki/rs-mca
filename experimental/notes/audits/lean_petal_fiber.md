# Lean: K4* map-smooth fiber + cap (W41-FIX path B)

## Status
EXPERIMENTAL / AUDIT. lake build PASS. Serves K4* petal kernel.

## Fix path
**(B)** Dropped fabricated thm:fiber-to-slope. Rebuilt on real
lem:map-smooth-fiber (L2741) + prop:map-smooth-cap (L2764).

## Object
- a=2,k=2,N=4,n=8,ℓ=3,A=6 with k+a+1≤A≤k+2a and A=k+2a (a|k)
- L=⌈C(4,3)/2⌉=2
- Cap ⌈L(q−n)/(q−n+k(L−1))⌉ = 4/4 = 1 exact (q−n=2)

## Dual routes
- generator: native_decide on ℓ,A bounds, L, cap formula
- checker: decide proofs of the same Nat goals

## Nonclaims
Toy instance; not the general map-smooth proof.
