# Lean: deep-regime upper bound

## Status
EXPERIMENTAL / AUDIT. lake build PASS.
**Hard input:** (a)/(d)

## Labels (rule 1b)
```
1790:\label{thm:deep-regime-upper}
1795:\tag{3.5}\label{eq:deep-upper}
```

## Object
3 instances: tight 3r=d−1 (bound 3), strict r=1 (bound 2), n=10 k=3 (bound 3).

## Dual routes
- generator: native_decide on hyp 3r≤d−1 and bound r+1
- checker: decide proofs of the same Nat goals

## Nonclaims
Value+gate only; MCA maximizer not rebuilt.
