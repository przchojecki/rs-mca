# Dyadic Profile Evaluation

Status: PROVED.

Source DAG node: `dyadic_profile_evaluation`.

## Statement

For dyadic domains `n = 2^m`, the quotient profile is the finite divisor sum

```text
Q_H = sum_{M | n, M > t} binom(n/M - 1, floor(A/M)).
```

At the relevant clean-rate rows, the admissible dyadic divisors form a chain, the
first admissible scale dominates the sum, and the deciding quotient length is
uniform between Row-C scale `n = 2^10` and prize scale `n = 2^41`.

The exact deciding-scale values are:

| row class | rate | `N*` | `h` | `log2 Q_M*` | `log2 D_M*` |
| --- | --- | ---: | ---: | ---: | ---: |
| Row-C and prize | 1/4 | 128 | 32 | 99.8063 | 48.3804 |
| Row-C and prize | 1/8 | 128 | 16 | 66.1465 | 31.8508 |
| Row-C and prize | 1/16 | 256 | 16 | 82.9664 | 40.2857 |

The rate-`1/2` pinned calibration profile is trivial: the dyadic quotient mass
is parity-killed at the candidate row.

## Proof

The replay script computes every admissible dyadic scale using exact integer
binomial coefficients.  It checks:

- the QA.22 target values for `Q_M*` and the dihedral/Chebyshev companion
  `D_M*`;
- first-scale dominance, i.e. `log2 Q_H = log2 Q_M*` to six decimal places;
- n-uniformity, i.e. Row-C and prize rows have identical `(N*, h, log2 Q, log2 D)`
  at rates `1/4`, `1/8`, and `1/16`;
- rate-`1/2` triviality.

No search, random sampling, or large-memory computation is used.

## Consequence

The dyadic quotient-profile mass is an exact replayable input for row-packet
pricing, E22 minimal-scale accounting, and list/counterexample profile ledgers.

## Non-Claims

This packet evaluates the dyadic quotient profile.  It does not close a deployed
adjacent row theorem by itself, does not prove non-dyadic profile statements,
and does not alter Papers A-D.

## Replay

```bash
python3 experimental/scripts/verify_dyadic_profile_evaluation.py --emit
python3 experimental/scripts/verify_dyadic_profile_evaluation.py \
  --check experimental/data/certificates/dyadic-profile-evaluation/dyadic_profile_evaluation.json
```
