# M1 Slack-Two Depth-Two Lift-Window Theorem

**Status:** PROVED / CONDITIONAL / AUDIT.

This note extracts the theorem-level content of
`m1_support_occupancy_scan.py` and
`verify_m1_slack_two_depth_two_kummer_saturation.py`. It is meant to make the
slack-two depth-two M1 contribution reviewable without reading the scanner
field list.

## Setup

Let `p` be prime and let `D subset F_p^*` be a cyclic multiplicative subgroup
of order `n`. Fix a quotient decomposition of `D` into `N` equal fibers of
size `m`, and write `K` for the fiber containing `1`. Consider the canonical
slack-two line

```text
X^(k+2) + z X^k
```

at exact support size `s=k+2`. In the depth-two frontier, write

```text
s = Lm + 4,        R = N-L.
```

The four residual points may be normalized by one of their elements and
written

```text
x {1,u,v,w},       w = -1-u-v.
```

The normalized depth-two slope factor is

```text
A(u,v) = -(u^2 + v^2 + uv + u + v + 1).
```

Multiplying the packet by `x in D` expands the nonzero slope factor by `D^2`.
Thus every active normalized shape contributes the square coset
`A(u,v)D^2`, with a possible zero slope when `A(u,v)=0`.

## Exact Lift-Window Reduction

The exact-support lift condition is purely quotient-fiber combinatorics. A
normalized shape is active if and only if the four entries

```text
1, u, v, -1-u-v
```

are distinct, lie in `D`, and touch at most `R` quotient fibers. Equivalently,
for `R < min(4,N)`, the active normalized catalog is the union over all
quotient windows `W` satisfying

```text
K subset W,        |W|=R,
```

of

```text
C_2^(2)(W) = {(u,v): 1,u,v,-1-u-v in W and distinct}.
```

Consequently the exact active depth-two slope image is

```text
{0 : A=0 occurs in the active catalog}
  union A(C_2^(2)(D;R)) D^2,
```

where `C_2^(2)(D;R)` denotes the normalized shapes touching at most `R`
quotient fibers. This proves the `R=1` kernel reduction, the `R=2`
two-fiber-window union reduction, and the general `R`-window reduction used by
the scanner.

The verifier checks the reduction on the running sample `p=97,n=48,N=6,m=8`:

```text
R=1: 18 active parameters, 6 zero parameters, 1 nonzero D^2-coset, 25 slopes.
R=2: 210 active parameters, 6 zero parameters, 4 nonzero D^2-cosets, 97 slopes.
R=3: 690 active parameters, 6 zero parameters, 4 nonzero D^2-cosets, 97 slopes.
```

Thus, in this sample, the exact-support image is sparse at `R=1` but already
saturated at `R=2`, before the all-shapes lift gate `R>=min(4,N)` applies.

## Lift-Limited Ceiling

The same quotient-window description gives the unconditional active-slope
ceiling. If a normalized shape touches `r` quotient fibers, one of those fibers
is the kernel fiber containing `1`; the other `r-1` fibers are chosen from
`N-1` fibers, and the ordered pair `(u,v)` has at most `(rm)^2` possibilities.
Therefore

```text
B_R = sum_{r=1}^{min(R,4,N)} binom(N-1,r-1) (rm)^2
```

bounds the number of ordered normalized parameters. Since every nonzero
four-point packet has exactly `24` normalizations, the active bad-slope image
satisfies

```text
|Bad_{t=2,d=2}^{active}|
  <= min(p, 1 + floor(B_R/24) |D^2|).
```

This bound is independent of the Kummer estimate. It is useful precisely when
too few quotient fibers remain for the raw saturated catalog to lift.

## Kummer Saturation Certificates

The saturation certificates are conditional on the standard two-variable
Kummer-Weil estimate with squarefree radical divisor

```text
u v (-1-u-v) A(u,v)
```

of component degrees `1,1,1,2`. The imported error constant is therefore
recorded as `(1+1+1+2-1)^2 = 16`.

For the raw normalized catalog on `D`, the verifier audits the character
expansion, the divisor nontriviality, the exact principal open-set count

```text
p^2 - 4p + 6 + 4 chi(-3),
```

and the exact six-line distinctness loss `6p-11`.

For a fixed quotient window `W` of size `R`, let

```text
h = [F_p^*:K],        q = [F_p^*:D^2].
```

The indicator of `W` has principal coefficient `R`; after the three conditions
`u,v,-1-u-v in W`, both the principal weight and the nonprincipal coefficient
bound are `R^3`. Hence the conservative lower numerator for a fixed
`D^2`-coset is

```text
R^3 (p^2 - 4p + 6 + 4 chi(-3))
  - (R^3*16p + 6p - 11) h^3 q.
```

When this numerator is positive, that fixed `R`-window already hits every
nonzero `D^2`-coset. If the exact-support complement has at least those `R`
remaining quotient fibers, this is an exact-support saturation certificate.

The verifier audits:

```text
R=2, p=7351, n=3675, N=3: positive fixed-window certificate.
R=3, p=2213, n=2212, N=4: positive fixed-window certificate.
```

In the second case, exact fixed-window enumeration gives `2,055,708`
parameters, `996` zero parameters, and both nonzero `D^2`-cosets, agreeing
with the certificate.

## Contribution to M1

This theorem closes a coherent low-slack subproblem: the slack-two depth-two
canonical frontier is now split into exact quotient-window lift regimes, a
lift-limited sparse regime, and Kummer-certified saturation regimes. It does
not prove the full M1 corrected-reserve local limit. What remains is to remove
or prove the imported Kummer-Weil estimate in a standalone algebraic-geometry
argument, sharpen the fixed-window threshold, and extend beyond this canonical
depth-two frontier toward the genuinely aperiodic residue-line packing
problem.
