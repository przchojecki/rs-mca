# Lean: unconditional support-envelope bracket

## Status
EXPERIMENTAL / AUDIT. lake build PASS.
**Hard input:** (e)/(d)

## Labels (rule 1b)
```
6212:\label{thm:unconditional-support-envelope-bracket}
```

## Object
n=5,k=1,|B|=2,q=|Γ|=11,B*=1: L(4)=2,P(4)=2>1,U(5)=1≤1;
adjacent a−=4,a+=5 ⇒ a*=5 (SB2/SB3).

## Dual routes
- generator: native_decide on ceilDiv nested L/P/U + SB2
- checker: decide proofs of the same Nat goals

## Nonclaims
Toy bracket arithmetic; does not prove B_MCA≥P or ≤U.
