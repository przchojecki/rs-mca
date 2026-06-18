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
floating-point roots of unity. The current report also runs an
`asymmetric_wall` pass, which removes the projective equal-pair tuples now
isolated by the conditional `C_2^peq` ledger, and an
`asymmetric_nonresonant_wall` pass, which also removes the exact line-conic
resonant submass `C_2^lc`.  It now also reports the complementary
`asymmetric_line_conic_resonant_wall` pass, isolating `C_2^lc` itself.

## Result

The report preset ran five scans.

```text
grid:
  primes p <= 500
  character orders e <= 24 with e | p-1
  h = e gcd(2,(p-1)/e)
  all canonical ramified-nonreciprocal tuples
  cases = 453
  tuples = 840700
  violations of 4p = 0

asymmetric:
  same prime/character grid
  projective equal-pair tuples removed
  cases = 453
  tuples = 685152
  violations of 4p = 0

nonresonant:
  same prime/character grid
  projective equal-pair and line-conic resonant tuples removed
  cases = 453
  tuples = 596304
  violations of 4p = 0

line-conic resonant:
  same prime/character grid
  projective equal-pair tuples removed, line-conic resonant tuples retained
  cases = 453
  tuples = 88848
  violations of 4p = 0

diagonal n=20:
  primes p <= 1601 with 20 | p-1
  only tuples (a,a,0,d) in the remaining class
  cases = 29
  tuples = 105484
  violations of 4p = 0
```

The diagonal scan overlaps the bounded grid for small `p`, so the combined
old remaining-wall count is `946184` tuple evaluations rather than a
deduplicated tuple set. The asymmetric count is reported separately because
it is the post-`C_2^peq` residual wall. The nonresonant count is the
post-`C_2^lc` subwall inside that asymmetric residual. The line-conic
resonant count is the complementary `C_2^lc` stress test inside the same
asymmetric residual.

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

Every top-20 row in the combined remaining-wall report had equal projective
line monodromies, hence lies in the `C_2^peq` slice now separated from the
genuinely asymmetric residual wall.

The largest observed asymmetric-only ratios in the same grid were:

| ratio | `(p,n,e,h)` | tuple `(a,b,c,d)` | line monodromies | line-conic resonant |
| --- | --- | --- | --- | --- |
| `3.2173609608` | `(197,14,14,28)` | `(6,1,0,17)` | `(12,2,8)` | no |
| `3.0363644911` | `(241,15,16,16)` | `(7,4,0,4)` | `(7,4,13)` | no |
| `2.8791555174` | `(443,26,17,34)` | `(11,7,0,7)` | `(22,14,18)` | no |
| `2.8631382894` | `(199,9,22,22)` | `(15,14,0,16)` | `(15,14,5)` | no |
| `2.8302231739` | `(409,24,17,34)` | `(14,10,0,12)` | `(28,20,30)` | no |
| `2.8207562164` | `(241,12,20,40)` | `(19,2,0,23)` | `(38,4,32)` | no |
| `2.8141899827` | `(379,18,21,42)` | `(8,14,0,29)` | `(16,28,24)` | no |
| `2.8077205315` | `(461,46,10,20)` | `(5,9,0,9)` | `(10,18,14)` | no |
| `2.8077205315` | `(461,23,20,20)` | `(18,10,0,9)` | `(18,10,14)` | no |
| `2.7940447234` | `(463,22,21,42)` | `(1,11,0,25)` | `(2,22,10)` | no |

The top ten nonresonant asymmetric rows are the same ten rows.

The largest observed line-conic-resonant asymmetric ratios were:

| ratio | `(p,n,e,h)` | tuple `(a,b,c,d)` | line monodromies |
| --- | --- | --- | --- |
| `2.7649691518` | `(461,20,23,46)` | `(1,10,0,44)` | `(2,20,28)` |
| `2.7469261727` | `(211,21,10,10)` | `(9,4,0,7)` | `(9,4,3)` |
| `2.7070090633` | `(277,12,23,46)` | `(19,7,0,8)` | `(38,14,24)` |
| `2.5339082341` | `(463,33,14,14)` | `(4,11,0,10)` | `(4,11,7)` |
| `2.5335973491` | `(457,24,19,38)` | `(8,1,0,36)` | `(16,2,24)` |
| `2.4963697768` | `(241,20,12,24)` | `(7,8,0,10)` | `(14,16,22)` |
| `2.4963697768` | `(241,10,24,48)` | `(14,16,0,20)` | `(28,32,44)` |
| `2.4686120945` | `(211,10,21,42)` | `(12,14,0,18)` | `(24,28,38)` |
| `2.4437525698` | `(397,33,12,12)` | `(8,9,0,3)` | `(8,9,1)` |
| `2.3995060208` | `(137,8,17,34)` | `(5,3,0,28)` | `(10,6,30)` |

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

After the projective equal-pair ledger is carved out, the finite evidence
changes the next target. The actual post-reduction asymmetric wall has no
equal or reciprocal projective line pair, and the largest audited ratio drops
from near `4p` to `3.2173609608p`. This is not a proof of a smaller constant,
but it is useful counterexample-first evidence: a future conductor argument
for `C_2^asym` may not need to explain the near-`4p` equal-line phenomenon,
because that phenomenon has been isolated into `C_2^peq`.

After the line-conic-resonant ledger is also carved out, the current largest
audited nonresonant asymmetric ratio is still `3.2173609608p`. Thus the
largest observed asymmetric obstruction is already in the clean
normal-crossing nonresonant subwall `C_2^anr`; the line-conic resonant slice
is important for theorem hypotheses, but it does not currently explain the
largest asymmetric examples. In the same report grid, the largest audited
line-conic-resonant asymmetric ratio is only `2.7649691518p`.
The resonant slice is now algebraically reduced in
`experimental/m1_depth_two_line_conic_resonance_reduction.md`, so future
numerical searches can treat resonant and nonresonant families as distinct
one-dimensional and normal-crossing conductor targets.

## Limitations

This is finite numerical evidence only. It neither proves the `4p` theorem,
nor a sharper asymmetric-wall theorem, nor rules out a larger counterexample
outside the scanned ranges. The diagonal scan is deliberately biased toward
the pattern seen in the bounded exhaustive grid, so it should be read as a
proof-guidance experiment rather than a broad random search.

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
The focused pullback-main scanner is
`experimental/search_m1_equal_line_pullback.py`.

For the current PR after the conditional projective equal-pair reduction, the
next numerical stress test should focus on the nonresonant asymmetric wall
itself: extend the `asymmetric_nonresonant_wall` scan beyond the present grid
and look specifically for families that push the ratio above the current
`3.2173609608` maximum.
