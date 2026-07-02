# Towards-Prize v3 Cap-Paper Package Constant Audit

- **Status:** AUDIT / exact integer and constant check.
- **Source:** `tex/towards-prize.tex`, Theorem `cap-paper-package`;
  `tex/cs25_cap_v12.tex`, Corollary `self-contained-safe` and certificate
  table `certs`.
- **Verifier:** `experimental/scripts/verify_towards_prize_v3_cap_package.py`.

This audit checks the constants newly exposed by the `towards-prize v3`
cap-paper package.  It is deliberately narrower than a transport audit: it
checks interval endpoints, half-Johnson arithmetic, and rate-comparison
constants, but it does not check the circle/stereographic or genus-one
transport hypotheses.

## Deployed Intervals

For the deployed KoalaBear and circle line-round rows, `n=2^21` and
`k=2^20`.  The self-contained safe edge printed in the compact note is the
deep-regime edge

```text
floor((n-k)/3) = 349525.
```

The imported half-distance edge is

```text
floor((n-k)/2)/n = 2^19/2^21 = 1/4.
```

The widened unsafe edges are recovered from the printed prefix-floor handles:

```text
KoalaBear: 1 - 16*69748 / 2^21 = 15331/32768.
Circle:    1 - 32*34873 / 2^21 = 30663/65536.
```

Thus the interval endpoints in Theorem `cap-paper-package` match the exact
certificate arithmetic.

## Safe Error Gates

The verifier also checks that the deployed safe numerators clear their targets:

```text
KoalaBear deep:    (349525+1)/p^6 <= 2^-128,
KoalaBear import:  n/p^6 <= 2^-128,
Circle deep:       (349525+1)/(2^31-1)^4 <= 2^-100,
Circle import:     n/(2^31-1)^4 <= 2^-100.
```

The corresponding radius gates are exact:

```text
3*349525 <= n-k,       2*2^19 <= n-k.
```

## Half-Johnson Handle

The Paper D v12 half-Johnson row for the KoalaBear sextic deployment is

```text
r=307121,     L2=1001282.
```

The verifier checks the printed denominator

```text
(n-2r)^2 - (k-1)n = 909700,
```

checks that the integer `L2` upper-bounds the rational Johnson list term, and
checks

```text
(1 + (r+1)L2) / p^6 < 2^-147.
```

At rate `rho=1/2`, this half-Johnson endpoint is dominated by the deep safe
edge (`307121 < 349525`), which matches the v3 package's use of the deep edge
in the deployed self-contained interval.

## Rate Comparison

For `0<rho<1`,

```text
(1-sqrt(rho))/2 > (1-rho)/3    iff    rho < 1/4.
```

The verifier checks this comparison on the four challenge rates.  Consequently
the half-Johnson certificate improves the self-contained edge only at rates
`1/8` and `1/16`; at rate `1/4` it is asymptotically tied, and at rate `1/2`
the deep edge is better.

## Result

The current verifier reports:

```text
implemented PASS: 4   FAIL: 0
```

No constant or endpoint discrepancy was found in the `towards-prize v3`
cap-paper package constants checked here.  The remaining high-priority audit
item in the same package is the circle/genus-one transport scope against the
actual deployed code models.
