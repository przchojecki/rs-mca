# Lean: exact first adjacent row AD1

## Status
EXPERIMENTAL / AUDIT. lake build PASS.
**Hard input:** (d)/(e)

## Labels (rule 1b)
```
1870:\label{thm:exact-first-adjacent-row}
1878:B_C^{MCA}(k+1)=M.      \tag{AD1}
```

## Object
n=4,k=1: M=6, Qsep=15, |F|=16>15, B_MCA(k+1)=M=6.

## Dual routes
- generator: native_decide on binom/Qsep/gate
- checker: decide proofs of the same Nat goals

## Nonclaims
Anchors gate + AD1 value M; does not rebuild MCA maximizer.
