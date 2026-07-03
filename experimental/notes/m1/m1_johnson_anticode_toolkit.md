# Johnson Anticode Toolkit For XR

Status: PROVED / COMBINATORIAL / SCOPING.

This note packages the active-roadmap node:

```text
xr_anticode_toolkit
```

It is a small Johnson-scheme lemma kit for the XR lane.  The positive result is
the exact packing/anticode bound for locator families with large exchange
separation.  The negative result is equally important: this purely
combinatorial layer has only Johnson-scale strength, so it cannot by itself
produce the finite-field `q`-scale input needed in the prize corridor.

The companion verifier is:

```text
python3 experimental/scripts/verify_m1_johnson_anticode_toolkit.py
```

The emitted certificate is:

```text
experimental/data/certificates/m1-johnson-anticode-toolkit/m1_johnson_anticode_toolkit_certificate.json
```

## Convention Block

```text
object:              Johnson locator graph J(n,j)
vertices:            j-subsets of an n-point domain
exchange distance:   d(A,B)=|A\B|=j-|A cap B|
XR role:             combinatorial support separation only
sampler:             not an MCA/list slope sampler
denominator role:    none; consumers must print q_line/q_chal separately
```

## Theorem 1: Anticode Packing Bound

Let `F` be a family of `j`-subsets of `[n]`.  Suppose distinct members of
`F` satisfy

```text
d(A,B) > s.
```

Equivalently,

```text
|A cap B| < j-s.
```

Then

```text
|F| * binom(j,s) <= binom(n,j-s),
```

and hence

```text
|F| <= floor( binom(n,j-s) / binom(j,s) ).
```

Proof.  Each `A in F` contains exactly `binom(j,j-s)=binom(j,s)` subsets of
size `j-s`.  If two distinct members `A,B` contained the same `(j-s)`-subset,
then `|A cap B| >= j-s`, so `d(A,B) <= s`, contradicting the separation
hypothesis.  Thus the `(j-s)`-cores contributed by distinct members are
disjoint inside the set of all `binom(n,j-s)` possible cores.

This is the clique-coclique/Delsarte anticode bound in elementary form: the
family of all `j`-sets containing a fixed `(j-s)`-core is an anticode of
diameter at most `s`, and the separated family is a code with minimum distance
`s+1`.

## Corollary: Density Loss

Relative to all `j`-subsets,

```text
|F| / binom(n,j)
  <= 1 / binom(n-j+s,s).
```

Indeed the identity

```text
binom(n,j) / binom(n-j+s,s)
  = binom(n,j-s) / binom(j,s)
```

rewrites the packing bound.  For fixed `s` and `j=rho n`, this is only a
polynomial support-space saving, roughly `s! / ((1-rho)n)^s`.

## Theorem 2: One-Step Johnson Mixing Scope

For the simple one-exchange walk on `J(n,j)`, the nontrivial endpoint factor
appearing in `m1_johnson_exchange_mixing.md` is

```text
lambda_* = 1 - n/(j(n-j)).
```

Thus the one-step gap is

```text
gap = n/(j(n-j)).
```

At fixed rate `j=rho n`, this is `Theta(1/n)`.  Therefore a single-step
expander-mixing estimate is near-vacuous in the prize-scale regime: it can
separate dictator-like paid structure from average behavior, but it cannot
turn a support-counting statement into a finite-field `q`-power value-set
lower bound.

## Consequence For XR

The toolkit gives the right combinatorial accounting for separated support
families and prevents naive exchange-mixing overclaims.  It should be used as
one layer in XR arguments:

- anticode packing controls how many mutually exchange-separated locators can
  survive a strip;
- the averaged-XR theorem identifies dictator/common-root structure as the
  endpoint extremal model;
- any prize-scale value-set or MCA safe-side conclusion still needs algebraic
  input, such as displacement kernels, paid-ledger removal, or exact
  row-specific value-set certificates.

Non-claims:

- no XR inverse theorem is proved here;
- no spectral-disjointness or M1 safe-side threshold is proved here;
- no finite-field `q`-scale lower bound follows from this note alone.

