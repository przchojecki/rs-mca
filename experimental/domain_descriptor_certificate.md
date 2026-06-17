# Field and Domain Descriptor Certificate

- **Status:** AUDIT / PROVED for the arithmetic checks implemented by the
  script.
- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Scope:** This note certifies `experimental/domain_descriptor.py`, a small
  descriptor generator for the field and domain ledger requested by P2 in the
  blueprint.

## Claim Audited

The script records the certificate-facing fields

```text
q_arith, q_gen, q_line, q_chal, n, k, domain type,
extension degree, mu, nu, and optional a/sigma reserve data.
```

It performs only arithmetic checks:

- whether the supplied field sizes are prime powers;
- whether `q_gen` is a subfield of `q_line`, and with what extension degree;
- whether `q_chal` is a subfield extension of `q_line`, when supplied;
- whether a multiplicative subgroup or coset domain satisfies
  `n | (q_gen - 1)`;
- whether `k <= n`;
- the factorization of `n` and `gcd(n,k)`;
- optional `rho`, `eta`, and `delta` values as exact rational strings.

These checks are necessary bookkeeping for Paper C certificates.  They do not
prove any locator local limit, MCA bound, extension-line transfer theorem, or
protocol reduction.

## Reproducible Checks

Base-field example:

```bash
python3 experimental/domain_descriptor.py \
  --name fermat-17-half-rate \
  --q-arith 17 \
  --q-gen 17 \
  --q-line 17 \
  --n 16 \
  --k 8 \
  --domain-type multiplicative_subgroup \
  --sigma 1 \
  --mu 2 \
  --nu 1
```

KoalaBear-sextic style descriptor, using `q_line = q_gen^6`:

```bash
Q_LINE=$(python3 -c 'print(2130706433**6)')
python3 experimental/domain_descriptor.py \
  --name koalabear-sextic-ledger \
  --q-arith 2130706433 \
  --q-gen 2130706433 \
  --q-line "$Q_LINE" \
  --n 262144 \
  --k 131071 \
  --domain-type multiplicative_subgroup \
  --sigma 16384 \
  --mu 2 \
  --nu 8 \
  --expected-extension-degree 6 \
  --format json
```

## Use in the Program

This supports the P2 certificate-scanner lane by making field separation
machine-readable before entropy, quotient-profile, list, MCA, and lower-bound
audits are combined.

## Limits

The script is intentionally a descriptor and arithmetic sanity checker.  It
does not assert that a protocol is sound, nor that `q_line` may be used for
MCA/list denominators without the matching extension-code or extension-line
theorem required by Paper C.
