# Lean: K2* rigidity census (W41-FIX)

## Status
EXPERIMENTAL / AUDIT. lake build PASS. Serves K2* enlarged rigidity kernel.

## Object
1. **prop:prefix-rigidity-full** (L2045): explicit m-sets M={0,1,4}, M'={0,2,3}
   share depth-w=1 prefix (e1=5=e1), d_J=2 ≥ w+1=2.
2. **lem:largest-fiber-log-detail**: ∑N²=38 ≤ maxN·M=50 on N=[5,3,2]; tight [4,4,4].

## Label fix
Cited prop:prefix-rigidity-full (not prop:prefix-rigidity).

## Dual routes
- generator: native_decide on set-diff Johnson distance + first-moment
- checker: decide proofs of the same Nat goals

## Nonclaims
Toy instance; not the general rigidity proof.
