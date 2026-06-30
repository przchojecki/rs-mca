# Quotient-Profile Scanner Certificate

- **Status:** AUDIT for the executable scan; PROVED for the divisor predicate
  and binomial entropy interval used by the scan.
- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Scope:** This note certifies `experimental/scripts/quotient_profile.py`, a
  deterministic scanner for the exact-divisibility quotient-core profile in
  Paper C, equation `qprofile`.

## Claim Audited

For integers `1 <= k <= a <= n`, write `sigma = a-k`.  The script enumerates
exactly the divisor scales

```text
M | gcd(n,k), M > 1, sigma < M, k/M <= n/M - 1
```

and reports the maximum of

```text
log2 binom(n/M - 1, k/M)
```

over those scales.  If no scale qualifies, it reports an empty profile.  This
is the literal exact-divisibility profile used by the certificate ledger; it is
not an all-line MCA theorem, a locator local-limit theorem, or a proof that
nearby remainder variants are harmless.

## Proof of the Enumeration

Every exact quotient-core scale in the Paper C profile must divide both `n` and
`k`, hence is a divisor of `gcd(n,k)`.  Conversely, every divisor of `gcd(n,k)`
divides both values, so the quotients `n/M` and `k/M` are integral.  Filtering
this finite divisor set by `M > 1`, `sigma < M`, and `k/M <= n/M - 1` leaves
exactly the admissible index set of the displayed maximum.  Taking the maximum
of the associated binomial logarithms over the filtered rows is therefore the
profile value, with the empty case corresponding to `-infinity`.

For large binomial coefficients the script reports an interval using the
standard entropy estimate

```text
2^(N H2(K/N))/(N+1) <= binom(N,K) <= 2^(N H2(K/N)).
```

The upper endpoint is conservative for the budget check in Paper C's condition
`Qprof_H(a,k) <= B_L log2(n) + Gamma_Q`.  If the upper endpoint clears the
budget, the scan clears the budget; if the lower endpoint exceeds the budget,
the scan fails it; otherwise the budget result is marked inconclusive.

## Reproducible Checks

Exact-rate dyadic dimensions have active quotient cores:

```bash
python3 experimental/scripts/quotient_profile.py --n 1048576 --k 524288 --sigma 1
```

One-step dyadic dithering empties the exact-divisibility profile:

```bash
python3 experimental/scripts/quotient_profile.py --n 1048576 --k 524287 --sigma 1
```

The sweep mode compares the exact-rate dimension and nearby dithered dimensions:

```bash
python3 experimental/scripts/quotient_profile.py \
  --dyadic-sweep --n 1048576 --rho-den 2 --sigma 1 --r-max 16
```

## Use in the Program

This supports the L3/P2 task of turning the quotient profile into a finite,
reproducible certificate item.  It gives witnesses for active exact quotient
scales at the actual pair `(n,k)`, making dimension dithering auditable before
the profile is consumed by list, MCA, or protocol ledgers.

## Next Checks

- Compare generated rows against any hand-written parameter tables before
  promotion into Paper C's certificate workflow.
- Add a separate scanner for the remainder variant described in the dimension
  hygiene section; this script deliberately covers only the exact-divisibility
  profile.
