# M1 Equal-Line Pullback Spectrum Experiment

**Status:** EXPERIMENTAL / COUNTEREXAMPLE / AUDIT.

## Purpose

This note records a targeted numerical audit of the normalized equal-line
pullback main term

```text
M_alpha =
  chi_2(-1) sum_{s!=-1, B(s)!=0} sum_x
    alpha(B(s)) alpha^(-2)(x) alpha^3(x-1)
    chi_2(4B(s)x-s^2),
```

where `B(s)=s^2+s+1`.  The earlier tuple scanner only tested the
M1-admissible equal-line characters.  This scan tests the full character
spectrum and then filters the same data back to the M1-admissible tuples.

## Method

For a primitive root `g`, write

```text
alpha(g)=exp(2 pi i k/(p-1)).
```

For every nonzero Kummer factor, the summand depends on `k` only through

```text
log B(s) - 2 log x + 3 log(x-1) mod p-1.
```

The script builds this additive-log histogram once for each prime and applies
one FFT to recover `M_alpha` for every multiplicative character `alpha` of
`F_p^*`.  It then reports:

- the full nonquadratic spectrum,
- the maximum equal-line domain size `n_max` for each character,
- the M1 equal-line grid with `e <= 24`,
- the diagonal M1 family with `n=20`.

The FFT calculation is checked against direct summation on small primes by
passing `--validate`.  The same validation also checks the domain-size
criterion below against direct equal-line tuple enumeration.

## Equal-Line Character Filter

Let `m=p-1`, let `alpha` have order `r`, and fix a domain size `n | m`.
Put

```text
e=m/n,        h=e gcd(2,n).
```

Then `alpha` occurs as `alpha=mu eta` in an equal-line tuple for this `n` if
and only if

```text
r | h        and        r notin {1,2,3}.
```

Indeed, if `A` is the exponent of `alpha` modulo `h`, the equal-line
condition gives

```text
line exponent = -2A,        d = 3A        mod h.
```

For odd `n`, all line exponents occur.  For even `n`, line exponents are the
even residues modulo `h`, and `-2A` is automatically even.  The active
coordinate and conic characters are nonprincipal exactly when
`alpha^2 != 1` and `alpha^3 != 1`, which excludes precisely
`r in {1,2,3}`.

Consequently the largest domain size in which a character of order `r` can
occur is

```text
n_max(alpha) =
  2m/r,        r even and r>3,
   m/r,        r odd and r>3,
   0,          r in {1,2,3}.
```

This is the filter used by the spectrum scanner.  It is useful because the
largest full-spectrum counterexamples have high character order and therefore
can only arise in very small equal-line domains.

## Command

The report data below was generated with

```bash
python3 experimental/search_m1_equal_line_pullback_spectrum.py \
  --preset report --top 12
```

The compatibility check against the old tuple-scan range was generated with

```bash
python3 experimental/search_m1_equal_line_pullback_spectrum.py \
  --preset report --prime-limit 500 --m1-max-character-order 24 --top 8
```

## Result

The report preset scans all primes `p <= 1601`.  On the full nonquadratic
character spectrum it tests `184552` character values and finds `28`
violations of the unrestricted target

```text
|M_alpha| <= 3p.
```

Those exact violations are small-domain phenomena in this range:

```text
violation counts by n_max threshold:
  n_max >= 4:  14
  n_max >= 6:  10
  n_max >= 8:   2
  n_max >= 12:  2
  n_max >= 16:  0
  n_max >= 20:  0
  n_max >= 32:  0
  maximum n_max among violations: 12
```

The largest full-spectrum rows are:

| ratio | `p` | exponent `k` | order | `n_max` |
| --- | ---: | ---: | ---: | ---: |
| `3.0600680546` | `1153` | `181` | `1152` | `2` |
| `3.0527498268` | `1013` | `450` | `506` | `4` |
| `3.0277388242` | `1447` | `1122` | `241` | `6` |
| `3.0235039776` | `607` | `192` | `101` | `6` |
| `3.0167068703` | `599` | `470` | `299` | `2` |

The same FFT data gives the following M1-filtered results.

```text
M1 equal-line grid:
  primes p <= 1601
  character orders e <= 24 with e | p-1
  tuples = 13662
  violations of 3p = 0
  rows above 2.95p = 2
  best ratio = 2.9877564255 at p=1429, exponent k=966, order=34

M1 diagonal n=20:
  primes p <= 1601 with 20 | p-1
  tuples = 2134
  violations of 3p = 0
  rows above 2.95p = 0
  best ratio = 2.9412840316 at p=461, exponent k=410, order=46
```

An extended run to `p <= 3000` keeps the same qualitative picture but shows
that a literal exact `3p` bound is still too rigid:

```bash
python3 experimental/search_m1_equal_line_pullback_spectrum.py \
  --preset report --prime-limit 3000 --top 12
```

It finds `46` full-spectrum exact `3p` violations.  Only two have
`n_max >= 20`, namely the conjugate pair

```text
p=1753,        order=73,        n_max=24,
exponents k=48 and k=1704,
|M_alpha|/p = 3.0015628082.
```

The excess over `3p` in this pair is only `2.7396027319`, or
`0.0654329699 sqrt(p)`.  In the same extended scan the bounded
`e <= 24` equal-line grid has `23650` tuple evaluations and no exact `3p`
violation, while the diagonal `n=20` family has `6300` tuple evaluations and
no exact `3p` violation.

On the old tuple-scan range `p <= 500`, `e <= 24`, the spectrum scanner
reproduces the earlier M1 count:

```text
M1 equal-line grid:
  tuples = 4804
  violations of 3p = 0
  best ratios = 2.9412840316, 2.9391353527, 2.9357869704
```

## Interpretation

The naive all-character version of the literal `3p` pullback conjecture is
false.  Thus a future proof of the equal-line M1 target cannot be just a
generic rank-one Kummer surface estimate for the divisor

```text
B(s), x, x-1, 4B(s)x-s^2.
```

It must use the M1-admissible character arithmetic, the hypergeometric
pullback structure, or a slightly weaker ambient estimate plus an
equal-line-domain refinement.

More precisely, the finite evidence now points to a top-dimensional target
rather than a literal inequality:

```text
|M_alpha| <= 3p + O(sqrt(p))
```

under the M1 domain-size and reserve hypotheses.  The `p=1753`, `n_max=24`
row shows that the exact `3p` inequality already fails in a moderate
equal-line domain, but only by a square-root-sized amount.  The bounded
`e <= 24` and diagonal `n=20` filters still support this corrected target in
the tested ranges.

## Limitations

This is finite numerical evidence only.  It disproves the unrestricted
finite-range statement over all nonquadratic characters in the scanned range,
but it does not prove the M1-admissible `3p+O(sqrt(p))` target and does not
rule out a larger M1-admissible counterexample outside the scanned
parameters.
