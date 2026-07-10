# Lean: Q-to-SP moment-to-max transfer

## Status
EXPERIMENTAL / AUDIT. lake build PASS.
**Named object:** moment-to-max / lem:q-to-sp-detail
**Hard input:** (b) image-scale MI+MA

## Object
lem:q-to-sp-detail L6659 on N=[6,3,3]: max=6 ≤ κ·N̄=8, ∑N²=54 ≤ κ·N̄·M=96.
Tight equality case N=[8], κ=1.

## Dual routes
- generator: native_decide on hyp + cleared conclusion
- checker: decide proofs of the same Nat goals

## Nonclaims
Distinct from #551 bare max·M and #548 sum-of-squares identity.
Toy fibers only.
