# Paper D v12 Profile and Explicit-Pair Constants Audit

- **Status:** AUDIT / exact algebra and deployed integer check, with one
  narrow proof-writing correction found.
- **Source:** `tex/cs25_cap_v12.tex`, Corollary `explicit-deployed`,
  Theorem `explicit-pairs`, Proposition `profile`, Corollary
  `profile-deployed`; compact use in `tex/towards-prize.tex`.
- **Verifier:** `experimental/scripts/verify_cs25_v12_profile_explicit.py`.

This audit checks the remaining deployed constant surface around the optimized
failure profile and the explicit simple-pole pair construction.  The deployed
certificate table already checks the profile rows as table entries; this note
adds the surrounding algebra and the explicit-pair constants that explain what
the rows mean.

## Profile Algebra

Let

```text
T = (1/k)(1-n/q).
```

The verifier checks the exact rational identity behind Proposition `profile`:

```text
x = (kappa/(kappa+1))*T
    ==>  q*x/(1-x/T) = kappa*q*T.
```

Thus a list floor satisfying

```text
L >= 1 + kappa*q*T
```

forces `eca(C,delta) >= (kappa/(kappa+1))*T` by the conversion theorem's
contrapositive.  It also checks that this certified profile is always strictly
below the route ceiling `T` for finite `kappa`.

For the deployed rows, the verifier checks:

```text
KoalaBear:          floor((L-1)k/(q-n)) >= 2^54,
circle line-round:  floor((L-1)k/(q-n)) >= 2^116,
```

where `L=ceil(binom(256,130)/p)`.  The corresponding profile factors are at
least `1-2^-54` and `1-2^-116`.

## Explicit Head Floors

For the deployed explicit-head MCA floor at gap `2^-8`, the verifier checks:

```text
c = 2^12,       m = k/c + 2 = 258,
agreement = c*m = k + 2^13,
count = binom(256,129) >= 2^251.
```

This count exceeds `q/k+1` for both the KoalaBear sextic row and the
Mersenne-31 circle line-round row.

For the explicit list floor at gap `2^-7`, it checks:

```text
c = 2^14,       m = k/c + 1 = 65,
agreement = c*m = k + 2^14,
count = binom(63,32) = 916312070471295267 > 2^59.
```

This count exceeds `2^-128*q` on the KoalaBear row and `2^-100*q` on the circle
line-round row.

## Explicit Simple-Pole Pair Constants

Theorem `explicit-pairs` chooses an explicit subfamily of size

```text
L0 = ceil((q-n)/k)
```

from the `binom(256,129)` pure-power listed codewords.  The verifier checks
`L0 <= binom(256,129)` for both rows.

It then checks the exact majority-pole collision estimate from the proof.  With

```text
x* = ceil(2k*binom(L0,2)/(q-n)),
```

the Cauchy lower bound

```text
L0^2 / (L0 + 2(x*-1))
```

is not quite at least the printed integerized bound

```text
ceil((q-n)/(3k)).
```

In both deployed rows the exact rational bound is smaller than this ceiling by
less than one.  Since the actual number `M(alpha)` of distinct slopes is an
integer, the proof still gives the printed integer count:

```text
M(alpha) >= CauchyBound > ceil((q-n)/(3k)) - 1
    ==> M(alpha) >= ceil((q-n)/(3k)).
```

The exact rational bound itself also clears the printed density targets:

```text
KoalaBear:          > 2^-22,
circle line-round:  > 2^-23,
```

The verifier also checks the stronger `>2^-22` proxy and the exact
`>2^-21.6` comparison.  Thus the density statement and the theorem's integer
count survive; the displayed rational inequality should just mention the final
integrality step rather than assert the rational bound itself exceeds the
ceiling.

Finally, it records the field-of-definition scope: among all poles in
`Omega=F\\D`, at most `|B|` lie in the base field, so the majority construction
is compatible with the genuinely extension-valued conclusion of the
subfield-confinement lemma.

## Result

The current verifier reports:

```text
implemented PASS: 4   FAIL: 0
```

The profile algebra and explicit head floors pass as printed.  The
explicit-pair majority-pole check finds one small proof-writing discrepancy:
the displayed rational lower-bound chain is just below
`ceil((q-n)/(3k))` in the deployed rows, although the integer-valued slope count
still gives the printed lower bound.  The text should insert this integrality
rounding step.

This audit checks the arithmetic and algebraic counting constants; it does not
derandomize the choice of an individual pole, which remains the explicit-witness
residue stated in Paper D v12.
