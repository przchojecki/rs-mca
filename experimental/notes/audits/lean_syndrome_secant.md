# Lean: exact syndrome–secant compiler instance

## Status
EXPERIMENTAL / AUDIT. lake build PASS.
**Named object:** syndrome-line incidence / secant compiler
**Hard input:** (a)/(c)

## Labels (rule 1b)
```
1607:\label{thm:syndrome-secant-exact}
1615:\tag{3.3}\label{eq:transverse-secant-count}
1621:\tag{3.4}\label{eq:exact-secant-numerator}
```

## Object
t=1, F_5, columns h_x=(1,x), y0=(1,1), y1=(0,1):
per-E uniqueness ≤1; Θ=5 (all finite slopes transverse-secant).

## Dual routes
- generator: native_decide on per-E counts and Θ fold
- checker: decide proofs of the same Nat goals

## Nonclaims
Toy Θ for one (y0,y1); does not compute max over all pairs = B_MCA.
Finite/decidable only (no asymptotic parts).
