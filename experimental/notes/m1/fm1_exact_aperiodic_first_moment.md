# FM1: exact aperiodic first moment for split locators

- **Status:** PROVED / local finite-field theorem, with toy verification.
- **DAG node:** `fm1`.
- **Roadmap role:** this proves the first-moment input stated as PROVABLE in
  `experimental/notes/roadmaps/proof_sketch/s2_paid_ledger.md`.  It supports
  the aperiodic safe-side model, but it is not a worst-case theorem.
- **Script:** `experimental/scripts/verify_fm1_exact_aperiodic_first_moment.py`.
- **Artifact:** `experimental/data/certificates/fm1-exact-first-moment/fm1_exact_first_moment.json`.

## Statement

Let `F = F_q`, let `D subset F^*` have size `n`, and let `k < A <= n`.
Put

```text
t = A-k,      j = n-A.
```

For a root set `R subset D` of size `j`, define the split locator

```text
ell_R(X) = prod_{r in R} (X-r).
```

For a word `w : D -> F`, define the locator-syndrome vector

```text
S_R(w) = ( sum_{x in D} w(x) ell_R(x) x^m )_{m=1..t} in F^t.
```

For independent uniform words `u,v : D -> F`, call `R` aligned if

```text
S_R(v) != 0
and
S_R(u) lies in the one-dimensional span F*S_R(v).
```

Then the expected number of aligned split locators is exactly

```text
E[# aligned R] = binom(n,j) * (1 - q^(-t)) * q^(1-t).
```

This is the finite-slope, nondegenerate alignment count.  It deliberately
excludes the `S_R(v)=0` degenerate direction, where the slope parameter is not
unique.

## Proof

Fix `R`, and let `E = D \ R`, so `|E| = A`.  The map

```text
w |-> S_R(w)
```

is linear from `F^D` to `F^t`.  The coordinates on `R` do not contribute,
because `ell_R` vanishes there.  On the remaining coordinates `E`, its matrix
has entries

```text
ell_R(x) x^m,       x in E,  1 <= m <= t.
```

For every `x in E`, both `ell_R(x)` and `x` are nonzero.  After scaling the
`x`-column by the nonzero factor `ell_R(x)x`, the matrix becomes the
Vandermonde row block

```text
x^(m-1),       x in E,  1 <= m <= t.
```

Since the elements of `E` are distinct and `|E|=A >= t`, this block has row
rank `t`.  Therefore `S_R` is surjective.

It follows that, for a uniform word `w`, the vector `S_R(w)` is uniform on
`F^t`.  Since `u` and `v` are independent, the pair

```text
(a,b) = (S_R(u), S_R(v))
```

is uniform on `F^t x F^t`.

The number of pairs `(a,b)` with `b != 0` and `a in F*b` is

```text
(q^t - 1) * q:
```

there are `q^t-1` nonzero choices for `b`, and each span `F*b` contains `q`
choices of `a`.  Thus, for this fixed locator,

```text
Pr[R aligned] = ((q^t - 1)q) / q^(2t)
              = (1 - q^(-t)) q^(1-t).
```

Finally there are `binom(n,j)` choices of `R`, and linearity of expectation
gives the formula.

## Consumer corollary

Let `N_A(u,v)` be the number of aligned split locators at agreement `A`.
For every `M >= 1`, Markov's inequality gives

```text
Pr_{u,v}[ N_A(u,v) >= M ]
    <= binom(n,j) * (1 - q^(-t)) * q^(1-t) / M.
```

In particular,

```text
Pr_{u,v}[ there exists an aligned split locator ]
    <= binom(n,j) * (1 - q^(-t)) * q^(1-t).
```

This is often the right diagnostic for whether a chart is generically empty.
It does **not** say that every pair has few aligned locators; all safe-side
work still needs a worst-case theorem or a paid-structure classification.

For the finite row

```text
C = RS[F_17^32, H, 256],     n=512,     k=256,
```

in the regular M3 window `385 <= A <= 426`, the verifier records the upper
bound

```text
log2 E[N_A] <= log2 binom(512,512-A) + (1-(A-256)) log2(17^32).
```

At the endpoints:

```text
A=385:  log2 E[N_A] < -16320
A=426:  log2 E[N_A] < -21760
```

and every `A` in the window has

```text
Pr[there exists an aligned split locator] < 2^-16000
```

for a random word-pair.  Thus any obstruction in this window is necessarily a
highly structured worst-case phenomenon, not random-pair mass.  This is a
sanity check for the M3/M5 chart program, not a replacement for root tables.

## Verification

The verifier records two checks.

1. **Surjectivity check, `F_13`.**  For `D=F_13^*`, `n=12`, `k=3`,
   `A=8`, `t=5`, `j=4`, every one of the `binom(12,4)=495`
   locator-syndrome maps has rank `5`.
2. **Exact brute-force check, `F_5`.**  For `D=F_5^*`, `n=4`, `k=1`,
   `A=3`, `t=2`, `j=1`, enumeration over all `5^8` word pairs gives

```text
total aligned locators = 300000
mean = 96/125
```

matching the formula

```text
binom(4,1) * (1 - 5^(-2)) * 5^(-1) = 96/125.
```

3. **F17 regular-window consumer scale.**  For `F_17^32`, `n=512`, `k=256`,
   the script computes the FM1/Markov one-locator upper bound across
   `385 <= A <= 426` and verifies the endpoint ranges above.

## Scope

FM1 is a mean statement over random word pairs and aligned locators.  It does
not by itself prove:

```text
worst-case safe-side bounds;
bad-slope bounds;
fiber-to-slope conversion;
or the aperiodic local limit.
```

Those require the separate concentration, fiber-rigidity, and paid-ledger
steps tracked elsewhere in the roadmap.  The contribution here is that the
first-moment input used by those steps is exact rather than heuristic.

## Reproduce

```bash
python3 experimental/scripts/verify_fm1_exact_aperiodic_first_moment.py
python3 experimental/scripts/verify_fm1_exact_aperiodic_first_moment.py --emit
```
