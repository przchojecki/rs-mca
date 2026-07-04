# Paper D v12 BCIKS Half-Distance Import Audit

- **Status:** AUDIT / external-source normalization and exact integer check.
- **Sources:** `tex/cs25_cap_v12.tex`, Corollary
  `conditional-half`; `tex/towards-prize.tex`, Corollary `import`; BCIKS
  Theorem 4.1 in the public JACM/NSF copy
  <https://par.nsf.gov/servlets/purl/10467091>.
- **Verifier:** `experimental/scripts/verify_cs25_v12_bciks_import.py`.

This audit checks the second current `agents.md` priority for Paper D v12: the
optional BCIKS half-distance import in the exact normalization of `eca`.

## Imported Statement

The accessible JACM/NSF copy of BCIKS Theorem 4.1 states the unique-decoding
line result with this threshold shape: for `RS[F_q,D,d]` at rate `(d+1)/n`,
if `delta <= (1-rho)/2` and a line `u0 + gamma u1` is `delta`-close to the
code for more than `n` slopes `gamma`, then the whole line is explained by a
single pair of codewords, with a common error set of size at most `delta*n`.

The repo writes `RS[F,D,k]` for degree `< k`, so the BCIKS degree parameter is
`d=k-1` and the rate is `(d+1)/n=k/n`.  Therefore the BCIKS conclusion gives,
for every column-far pair in the repo CA definition, at most `n` CA-bad slopes.
In the repo density normalization this is exactly

```text
eca(C,delta) <= n/q.
```

This is the exact constant used in both `tex/cs25_cap_v12.tex` and
`tex/towards-prize.tex`.

## Radius Gate

For `C=RS[F,D,k]`, the minimum Hamming weight is `w_min=n-k+1`, so the
mutual-from-correlated theorem's half-distance hypothesis

```text
2*r <= w_min - 1,        r=floor(delta*n)
```

is exactly

```text
2*floor(delta*n) <= n-k.
```

The phrasing in `towards-prize.tex`,

```text
delta <= (n-k)/(2n),
```

is sufficient for this floor condition, including the endpoint.  At the
challenge rate `rho=1/2`, `n=2^21`, `k=2^20`, the endpoint is
`r=2^19` and `delta=1/4`.

## MCA Transfer

Paper D v12 proves locally that, under the same floor condition,

```text
emca(C,delta) <= max(eca(C,delta), r/q).
```

Combining this with the imported `eca(C,delta)<=n/q` gives

```text
emca(C,delta) <= max(n/q, r/q) = n/q,
```

since `r<=n`.  Thus no extra factor is introduced by the MCA layer in this
range.

The exact `n/q` constant is load-bearing for the printed `q>=2^128 n` clause:
it gives `n/q <= 2^-128` by cross multiplication.  If a later source audit
replaced the import by a weaker `C(n)/q` statement, the CH certificate grammar
would need to print that numerator and the `q>=2^128 n` safe clause would have
to be updated accordingly.  The current audit found no such mismatch in the
BCIKS Theorem 4.1 statement checked above.

## Deployed Rows

The verifier checks the two imported CH rows printed in Paper D v12:

```text
KoalaBear sextic: p=2^31-2^24+1, q=p^6, n=2^21
    n/q < 2^-164 < 2^-128.

Circle line-round: p=2^31-1, q=p^4, n=2^21
    n/q < 2^-102 < 2^-100.
```

The endpoint condition is also exact in both rows:

```text
r = 2^19,     2r = n-k = 2^20.
```

## Result

The current verifier reports:

```text
implemented PASS: 5   FAIL: 0
```

No normalization, endpoint, or deployed-integer discrepancy was found in the
BCIKS half-distance import as used by Paper D v12 and `towards-prize.tex`.

## Adversarial Follow-Up

A 2026-07-03 adversarial pass rechecked `cor:conditional-half`,
`thm:mca-from-ca`, and `thm:sandwich2`.  The import still matches the local
`eca` normalization and denominator convention, but two presentation follow-ups
should be carried forward before editing Paper D:

1. `tex/cs25_cap_v12.tex:5055` imports BCIKS for
   `delta <= (1-rho)/2`, while the corollary states the equivalent integer-ball
   range `2*floor(delta*n) <= n-k`.  The proof at
   `tex/cs25_cap_v12.tex:5063` should explicitly insert
   `delta' = floor(delta*n)/n <= (1-rho)/2` and note that the close-ball event
   for `delta` is the same as the close-ball event for `delta'`.  This is a
   proof-clarity correction, not a normalization failure.
2. In `tex/cs25_cap_v12.tex:5191`, the circle widened unsafe edge is printed
   as `0.46788`, while the exact edge in the caption is
   `30663/65536 = 0.467880249...`.  Since the caption says the unsafe edges are
   rounded outward to five digits, the conservative five-decimal lower edge for
   the unsafe interval is `0.46789`, or the table should use the exact fraction.
   The KoalaBear edge `15331/32768 = 0.467864990...` is consistent with the
   printed outward value `0.46787`.

These follow-ups do not change the verifier result above and do not promote the
BCIKS import beyond CONDITIONAL/AUDIT status.
