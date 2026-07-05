# Census Exact Counts

Status: PROVED.

Source DAG node: `census_exact_counts`.

Depends on: `census_bounded_scales`.

## Statement

Once the deciding quotient scales are bounded, the deciding class counts are
exactly computable big integers. At each candidate point, the exact count

```text
K = binom(N', l')
```

with forced ratio `l' = (j/n)N'` replaces leading and second-order asymptotic
expansions for tie decisions. The knife-edge condition becomes an exact
Diophantine statement about whether

```text
B* = floor(q / 2^128)
```

lies in the relevant interval `[L, K)`, where `L` is the certified lower-bound
strength.

## Proof

By `census_bounded_scales`, every row in the current corridor uses a bounded
deciding scale. Therefore `K = binom(N', l')` can be computed exactly with
ordinary integer arithmetic. No asymptotic expansion is needed at the candidate
point.

The replay certificate recomputes the exact binomial table for the recorded
clean-rate prize parameters:

```text
rate 1/2:  N'=128, l'=64
rate 1/4:  N'=128, l'=94
rate 1/8:  N'=256, l'=222
rate 1/16: N'=512, l'=478
```

The resulting exact integers determine the corresponding `log2 K` values and
pin which rows are below, inside, or above the challenge-budget gate. This is
the finite arithmetic input used by the knife-edge census.

## Non-Claims

This packet computes the exact raw deciding counts `K`. It does not supply the
certified lower-bound strength `L`, does not prove that `[L,K)` is empty, and
does not close any deployed adjacent row theorem by itself.

## Replay

```bash
python3 experimental/scripts/verify_census_exact_counts.py --emit
python3 experimental/scripts/verify_census_exact_counts.py \
  --check experimental/data/certificates/census-exact-counts/census_exact_counts.json
```
