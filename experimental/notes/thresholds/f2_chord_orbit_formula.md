# F2 chord-orbit formula

- **Status:** PROVED using standard multiplicative-character and Jacobi-sum
  identities; replay verifier included.
- **Track:** `(Q)` / F2 quotient-prefix flatness lane.
- **Verifier:** `python3 experimental/scripts/verify_f2_chord_orbit_formula.py`

## Statement

Let `q` be an odd prime, let `n | q-1`, and put

```text
H = mu_n subset F_q^x,
m = (q-1)/n.
```

For `c != 0`, define the ordered chord count

```text
N(c) = #{(x,y) in H^2 : x+y=c}.
```

Let `C_m` be the `m` multiplicative characters of `F_q^x` that are trivial on
`H`. Let `delta = 1_{-1 in H}`. Then

```text
N(c) = (q + 1 - 2m 1_H(c) - m delta + E(c)) / m^2,
```

where

```text
E(c) = sum chi1(c) chi2(c) J(chi1,chi2)
```

over pairs `chi1,chi2 in C_m` such that `chi1`, `chi2`, and `chi1 chi2` are all
nontrivial. Here `J(chi1,chi2)` is the usual Jacobi sum. For every generic pair,

```text
|J(chi1,chi2)| = sqrt(q),
```

so

```text
|E(c)| <= (m-1)(m-2) sqrt(q).
```

The unordered distinct-pair collision count is

```text
kappa(c) = (N(c) - 1_{c/2 in H}) / 2.
```

Both `N(c)` and `kappa(c)` are constant on `H`-orbits of `c`.

## Proof

For `x != 0`,

```text
1_H(x) = (1/m) sum_{chi in C_m} chi(x).
```

Therefore, for `c != 0`,

```text
N(c) = (1/m^2) sum_{chi1,chi2 in C_m}
       sum_{x+y=c, xy != 0} chi1(x) chi2(y).
```

With `x=cs` and `y=c(1-s)`, the inner sum is

```text
chi1(c) chi2(c) J(chi1,chi2),
```

where the Jacobi sum runs over `s != 0,1`. The special values are:

```text
J(eps,eps) = q-2,
J(chi,eps) = J(eps,chi) = -1       for chi != eps,
J(chi,chi^{-1}) = -chi(-1)         for chi != eps,
|J(chi1,chi2)| = sqrt(q)           when chi1, chi2, chi1 chi2 are nontrivial.
```

Collecting the non-generic terms gives

```text
(eps,eps):              q - 2,
(chi,eps)+(eps,chi):   -2(m 1_H(c) - 1),
(chi,chi^{-1}):        -(m delta - 1).
```

Thus the non-generic contribution is `q + 1 - 2m 1_H(c) - m delta`, and the
remaining terms are exactly `E(c)`.

Orbit constancy follows because every `chi in C_m` is trivial on `H`, so
`chi(uc)=chi(c)` for `u in H`. The formula for `kappa(c)` removes the diagonal
ordered solution `x=y=c/2`, if present, and halves the remaining ordered pairs.

## Why This Helps F2

The generic chord geometry is not a large unstructured object: after quotient
by `H`, it is an exact `m`-orbit computation with a printed Jacobi error term.
At small co-index `m`, this explains the narrow observed `kappa` strata in the
F2 calibration rows.

This packet does not close the F2 mid-band. It supplies the exact per-orbit
chord census used by later arc bounds and generic-class accounting. For official
rows, `q` should be read as the generated field containing the root domain, so
the co-index `m=(q-1)/n` is the generated-field co-index.
