# M1 Remaining Two-Coordinate Wall Experiment

**Status:** EXPERIMENTAL / AUDIT.

## Purpose

This note records a targeted numerical stress test for the remaining
slack-two depth-two M1 two-coordinate Kummer wall. The tested target is

```text
|S_{a,b,c,d}| <= 4p
```

after removing the already proved infinity-unramified and projective
reciprocal line-pair slices.

The scan uses the canonical active coordinate pair `(a,b,c)=(a,b,0)`. The
other two active pairs are equivalent by the symmetry of
`A=uv+uw+vw-1` on the plane `u+v+w=-1`.

## Command

The report data below was generated with

```bash
python3 experimental/search_m1_remaining_two_coordinate_wall.py \
  --preset report --top 20
```

The script uses NumPy for vectorized full finite-field summation with
floating-point roots of unity.

## Result

The report preset ran two scans.

```text
grid:
  primes p <= 500
  character orders e <= 24 with e | p-1
  h = e gcd(2,(p-1)/e)
  all canonical ramified-nonreciprocal tuples
  cases = 453
  tuples = 840700
  violations of 4p = 0

diagonal n=20:
  primes p <= 1601 with 20 | p-1
  only tuples (a,a,0,d) in the remaining class
  cases = 29
  tuples = 105484
  violations of 4p = 0
```

The diagonal scan overlaps the bounded grid for small `p`, so the combined
count is `946184` tuple evaluations rather than a deduplicated tuple set.

The largest observed ratios were:

| ratio | `(p,n,e,h)` | tuple `(a,b,c,d)` | line monodromies |
| --- | --- | --- | --- |
| `3.9771715522` | `(421,20,21,42)` | `(5,5,0,6)` | `(10,10,10)` |
| `3.9643175123` | `(461,20,23,46)` | `(18,18,0,15)` | `(36,36,36)` |
| `3.9234263103` | `(641,20,32,64)` | `(25,25,0,21)` | `(50,50,50)` |
| `3.9002007257` | `(397,44,9,18)` | `(8,8,0,3)` | `(16,16,16)` |
| `3.9002007257` | `(397,22,18,36)` | `(16,16,0,6)` | `(32,32,32)` |
| `3.8966876387` | `(281,20,14,28)` | `(1,1,0,25)` | `(2,2,2)` |
| `3.8961513626` | `(181,20,9,18)` | `(5,5,0,12)` | `(10,10,10)` |
| `3.8961513626` | `(181,10,18,36)` | `(10,10,0,24)` | `(20,20,20)` |
| `3.8906714859` | `(1601,20,80,160)` | `(73,73,0,21)` | `(146,146,146)` |
| `3.8896540276` | `(89,8,11,22)` | `(1,1,0,8)` | `(2,2,2)` |

Every top-20 row in the report output had equal projective line monodromies.

## Interpretation

The scan did not find a counterexample to the proposed `4p` remaining-wall
bound. More importantly, the near-sharp examples are concentrated in the
equal-line-monodromy diagonal subfamily:

```text
a=b,        line_1 = line_2 = line_infinity.
```

When `h=2e`, this condition is equivalent to

```text
d == -3a mod e.
```

This suggests that the first analytic target should be the equal-monodromy
diagonal subfamily, not a generic off-diagonal estimate. If that subfamily
admits a clean `4p` trace bound, the remaining off-diagonal family may be
easier to handle by a less sharp conductor argument.

## Limitations

This is finite numerical evidence only. It neither proves the `4p` theorem
nor rules out a larger counterexample outside the scanned ranges. The
diagonal scan is deliberately biased toward the pattern seen in the bounded
exhaustive grid, so it should be read as a proof-guidance experiment rather
than a broad random search.

## Next Step

Try to prove the equal-line-monodromy diagonal case first. In the canonical
pair this is the family

```text
S_{a,a,0,d},        d == -3a mod e,
```

with all three projective line monodromies equal and nonprincipal. A useful
proof would likely explain why the finite ratios can approach `4p` from
below while still respecting the projective Euler-characteristic target.
The first reduction for this subfamily is recorded in
`experimental/m1_depth_two_equal_line_diagonal_reduction.md`.
