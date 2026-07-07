# M1 nonconsecutive coefficient-window normal form v1 report

Status: `PROVED`.

This packet proves the normal-form identity for coefficient windows `W={1,r}`
and routes every survivor to generated collision, half-turn, recursive lower-core
affine slice, or the named pair-deficient residual branch.

## Formula checks

| r | formula | branch rule |
| -: | --- | --- |
| 3 | `b_0 theta_3 + b_1 theta_1 = 0` | odd window: nonzero active residual vector descends; all odd theta defects zero routes to half-turn |
| 4 | `b_0 theta_4 + b_1 theta_2 + b_2 theta_0 = 0` | even window: deep paired core solves for the next lower-domain coefficient |
| 5 | `b_0 theta_5 + b_1 theta_3 + b_2 theta_1 = 0` | odd window: nonzero active residual vector descends; all odd theta defects zero routes to half-turn |
| 6 | `b_0 theta_6 + b_1 theta_4 + b_2 theta_2 + b_3 theta_0 = 0` | even window: deep paired core solves for the next lower-domain coefficient |
| 7 | `b_0 theta_7 + b_1 theta_5 + b_2 theta_3 + b_3 theta_1 = 0` | odd window: nonzero active residual vector descends; all odd theta defects zero routes to half-turn |
| 8 | `b_0 theta_8 + b_1 theta_6 + b_2 theta_4 + b_3 theta_2 + b_4 theta_0 = 0` | even window: deep paired core solves for the next lower-domain coefficient |
| 9 | `b_0 theta_9 + b_1 theta_7 + b_2 theta_5 + b_3 theta_3 + b_4 theta_1 = 0` | odd window: nonzero active residual vector descends; all odd theta defects zero routes to half-turn |
| 10 | `b_0 theta_10 + b_1 theta_8 + b_2 theta_6 + b_3 theta_4 + b_4 theta_2 + b_5 theta_0 = 0` | even window: deep paired core solves for the next lower-domain coefficient |

## Exact cyclotomic scan checks

| model | j | window | supports | buckets |
| --- | -: | --- | -: | --- |
| Q(zeta_16) | 5 | `[1, 3]` | 336 | `{'honest_half_turn_pair_core': 336}` |
| Q(zeta_16) | 5 | `[1, 5]` | 336 | `{'honest_half_turn_pair_core': 336}` |
| Q(zeta_16) | 8 | `[1, 5]` | 70 | `{'honest_half_turn_pair_core': 70}` |
| Q(zeta_16) | 8 | `[1, 6]` | 70 | `{'recursive_lower_core_affine_slice': 70}` |
| Q(zeta_16) | 8 | `[1, 7]` | 70 | `{'honest_half_turn_pair_core': 70}` |

## Finite generated-collision guardrails

| model | j | window | finite survivors | honest lift | generated-only |
| --- | -: | --- | -: | -: | -: |
| F_17 | 5 | `[1, 3]` | 464 | 336 | 128 |
| F_17 | 5 | `[1, 5]` | 448 | 336 | 112 |

## Nonclaims

- payment of pair-deficient residual windows.
- lower-rung Q/BC/SP constants.
- primitive Q-fin max-fiber flatness.
- arbitrary sparse Hankel row-slices without printed coefficient rows.
- extension-valued split-pencil branches.
