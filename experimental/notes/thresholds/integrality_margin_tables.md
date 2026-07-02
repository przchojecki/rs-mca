# Integrality Margin Tables

- **Status:** EXPERIMENTAL / entropy-upper margin table.
- **Agent:** Codex acting autonomously for Allen Graham Hart.
- **Evidence task:** E14, `QA.3 + QL.4`.
- **Verifier:** `experimental/scripts/verify_integrality_margin_tables.py`.
- **Artifact:** `experimental/data/certificates/integrality-margin-tables/integrality_margin_tables.json`.

This packet evaluates the computational half of the integrality endgame:
at the candidate crossing scales already used by the quotient-census and
planted-list arithmetic packets, an `n^3` polynomial slack factor is still
absorbed by an astronomical entropy/FM margin.

It does not prove the conjectural safe-side inputs.  In particular, it does
not prove R2 rigidity on the MCA side and does not prove the list-side
`ImgFib` theorem.  Its use is conditional: if a later theorem bounds the
unpaid aperiodic or extra-list contribution by `n^3` times the recorded proxy,
then the integer contribution at these candidates is exactly zero.

## Scope

The verifier uses the max official dimension rows

```text
k = 2^40,       n = R k,       R in {2,4,8,16},
```

and budget bits `64,96,128`, corresponding to `q_bits=192,224,256` after the
`2^-128` denominator shift.

Candidate scales are recomputed from the same exact formulas as the companion
packets:

```text
MCA relaxed A_2 crossing       from the exact 2-power count A_2(N,rho N+1)
MCA dyadic A_2 crossing        dyadic coarsening of the same count
LIST planted dyadic crossing   binom(N-1,N/R) > 2^budget_bits - 1
```

At a candidate quotient order `N`, the verifier sets

```text
sigma = ceil(n/N).
```

## Proxies Tested

For the MCA side it uses the FM1 upper proxy

```text
C(n,j) (1-q^-sigma) q^(1-sigma) <= C(n,j) q^(1-sigma),
j = n-k-sigma.
```

For the list side it uses the entropy extras proxy

```text
C(n,k+sigma) q^-sigma.
```

Both binomial coefficients are upper-bounded by

```text
log2 C(n,m) <= n H2(m/n).
```

The verifier records

```text
-log2( n^3 * proxy_upper )
```

and requires this margin to exceed `1000` bits for every row.

## Result

All recorded rows pass.  The worst row is the rate `1/2`, `q_bits=256`,
MCA dyadic `A_2` crossing at `N=256`; even there the margin is about
`9.68e7` bits after multiplying by `n^3`.

This supports the intended endgame interpretation: at the current candidate
scales, the hard work is structural classification, not numerical constant
sharpening.  Once the structural theorem supplies a polynomial `n^3` multiplier
against the relevant proxy, integrality forces the residual contribution to
vanish.

## Replay

```bash
python3 experimental/scripts/verify_integrality_margin_tables.py --emit
python3 experimental/scripts/verify_integrality_margin_tables.py \
  --check experimental/data/certificates/integrality-margin-tables/integrality_margin_tables.json
```
