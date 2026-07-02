# Paper D v12 Deployed Certificate Arithmetic Audit

- **Status:** AUDIT / exact integer replay.
- **Source:** `tex/cs25_cap_v12.tex`, the deployed certificate table
  `tab:certs`, plus the adjacent deployed-profile corollary.
- **Packet:** `experimental/data/certificates/cs25-v12-deployed-certificates/cs25_v12_deployed_certificates.json`.
- **Verifier:** `experimental/scripts/verify_cs25_v12_deployed_certificates.py`.

This audit turns the printed deployed-row certificate tuples into a
machine-readable packet and replays their integer inequalities with exact
Python arithmetic.  It is intentionally narrow: it verifies the arithmetic
behind the printed certificates, not the surrounding theorem dependencies.

## Checked Claims

The verifier checks:

1. the four optimized prefix-floor inequalities for the KoalaBear sextic and
   Mersenne-31 circle line-round rows;
2. the four explicit-head inequalities;
3. the mutual-from-correlated half-distance radius condition;
4. the KoalaBear half-Johnson handle, including the list-size inequality and
   the denominator bound;
5. both optional CH import denominator bounds;
6. the KoalaBear deployed profile certificate and the adjacent circle-profile
   corollary certificate;
7. the `i`-free circle rational-floor inequality, including the printed
   `2^63000` margin.

All comparisons involving `q/k+1` are checked by integer cross-multiplication,
for example

```text
binom(N,m) > p^w (q/k+1)
```

is replayed as

```text
binom(N,m) * k > p^w * (q+k).
```

## Result

The current packet reports:

```text
implemented PASS: 15   FAIL: 0
```

No arithmetic discrepancy was found.  This supports the current `agents.md`
priority item asking agents to verify that Paper D v12's "verified exactly"
deployed-row inequalities are backed by reproducible scripts or printed integer
certificates.
