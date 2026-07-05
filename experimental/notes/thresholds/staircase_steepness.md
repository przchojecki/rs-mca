# Staircase Steepness

Status: PROVED.

Source DAG node: `staircase_steepness`.

## Statement

For the aligned leading stratum

```text
M(j,t) = binom(n,j) (1 - q^(-t)) q^(1-t),
```

with adjacent grid motion `j -> j + 1` and `t -> t - 1`, one grid step changes
the non-binomial factor by a field-size factor.  More precisely, for `t > 1`,

```text
M(j + 1,t - 1) / M(j,t)
  = ((n - j) / (j + 1)) q ((1 - q^(1-t)) / (1 - q^(-t))).
```

The final parenthesized factor is bounded between `q/(q+1)` and `1` for every
`q >= 2`, so the normalized adjacent jump is between `q^2/(q+1)` and `q`.

## Proof

The binomial recurrence gives

```text
binom(n,j + 1) / binom(n,j) = (n - j) / (j + 1).
```

Substituting the two adjacent grid points into `M` gives

```text
M(j + 1,t - 1) / M(j,t)
  = ((n - j) / (j + 1))
    q
    ((1 - q^(1-t)) / (1 - q^(-t))).
```

Write

```text
F(q,t) = (1 - q^(1-t)) / (1 - q^(-t)).
```

For `q >= 2` and `t > 1`,

```text
F(q,t) - q/(q+1)
  = (1 - q^(2-t)) / ((q+1)(1 - q^(-t))) >= 0,
```

and

```text
1 - F(q,t)
  = ((q - 1) q^(-t)) / (1 - q^(-t)) > 0.
```

Thus `q F(q,t)` is a constant-factor `q` jump, uniformly in the row.  The same
calculation applies to the ACL terms used in the adjacent corridor comparison:
each term is a row-scale coefficient times a `q`-power whose exponent changes
by one across an adjacent step.

Consequently the adjacent comparison `B_C(A)` versus `B*` only needs relative
precision much coarser than a full adjacent-step factor, except for the stated
knife-edge cells where the exact count lies inside the error band of `B*`.

## Role

This is a threshold-compiler packet.  It supports finite adjacent-row
certificates by explaining why all non-knife-edge rows can be decided by coarse
validated estimates, while the residual cells are routed to exact census or
printed row certificates.

## Non-Claims

This packet does not decide any particular deployed `v13` frontier row, does
not supply the knife-edge census itself, and does not alter Papers A-D.

## Replay

```bash
python3 experimental/scripts/verify_staircase_steepness.py --emit
python3 experimental/scripts/verify_staircase_steepness.py \
  --check experimental/data/certificates/staircase-steepness/staircase_steepness.json
```
