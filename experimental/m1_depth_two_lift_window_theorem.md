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
The exact external dependency and its audited hypotheses are separated in
`m1_kummer_weil_import_contract.md`; the present note remains conditional on
that import.
The same contract also proves two elementary `p`-bound subcases: the `d=0`
Jacobi part and the `d!=0` conic-only part with coordinate characters
principal. The imported `16p` Kummer estimate is paid only for mixed terms
with nonzero conic exponent and at least one nonprincipal coordinate
character.

For the raw normalized catalog on `D`, the verifier audits the character
expansion, the divisor nontriviality, the exact principal open-set count

```text
p^2 - 4p + 6 + 4 chi(-3),
```

and the exact six-line distinctness loss `6p-11`. With
`e=[F_p^*:D]` and `q=[F_p^*:D^2]`, the nonprincipal expansion splits into
the proved Jacobi part `e^3-1`, the proved conic-only part `q-1`, and the
remaining mixed Kummer part `(e^3-1)(q-1)`.

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
  - p R^3((h^3-1) + (q-1) + 16(h^3-1)(q-1))
  - (6p - 11) h^3 q.
```

The uniform sufficient threshold for this fixed-window numerator is

```text
p >= ceil((R^3((h^3-1)+(q-1)+16(h^3-1)(q-1)) + 6h^3q)/R^3) + 4.
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

There is also a stronger certificate for the full quotient-window union. Let
`Q=D/K` have order `N`, and let

```text
T_R(N) = #{(a,b,c) in Q^3 : |{1,a,b,c}| <= R}.
```

Equivalently,

```text
T_R(N) = sum_{j=0}^{min(R-1,3,N-1)}
           binom(N-1,j)
           sum_{i=0}^j (-1)^i binom(j,i) (j+1-i)^3.
```

In particular,

```text
T_1(N)=1,        T_2(N)=7N-6,
T_3(N)=1+7(N-1)+12 binom(N-1,2),        T_4(N)=N^3.
```

Expanding the indicator of the union of all `R`-windows by quotient-kernel
characters gives principal weight `T_R(N)`. The nonprincipal coefficients are
smaller. A quotient-Fourier calculation gives the coefficient bounds

```text
C_1(N)=1,
C_2(N)=3N-6,
C_3(N)=max(6,(N-2)(N-3)).
```

The `R=2` formula follows by writing each coefficient as `zN-6`, where `z`
counts zero subset sums among the three quotient frequencies. For `R=3`, the
complement is the ordered catalog of three distinct nonidentity quotient
labels; inclusion-exclusion gives

```text
U(r)U(s)U(t) - U(r+s)U(t) - U(r+t)U(s) - U(s+t)U(r)
  + 2U(r+s+t),
```

where `U(a)=N-1` if `a=0` and `U(a)=-1` otherwise. The displayed bound is the
maximum absolute nonprincipal value of that expression.

The Kummer expansion is over ambient characters modulo `K`, not only over
characters of `D/K`. Put

```text
e = [F_p^*:D],        h = [F_p^*:K] = eN,
q = [F_p^*:D^2].
```

The `e^3` ambient character triples that restrict trivially to `D/K` still
have coefficient `T_R(N)`. All other ambient triples have coefficient bounded
by `C_R(N)`. Hence the quotient-label L1 bound is

```text
S_R <= e^3 T_R(N) + (h^3-e^3) C_R(N),
```

For `R=2`, the quotient L1 term is exact. If `z(r,s,t)` is the number of
nonempty subset sums among `r,s,t` that vanish in `D/K`, the coefficient is
`zN-6`. The distribution is:

```text
N odd:
  z=0: (N-1)(N-3)^2,    z=1: (N-1)(7N-17),
  z=2: 3N-3,            z=3: 6N-6,      z=7: 1.

N even:
  z=0: N^3-7N^2+15N-10, z=1: (N-2)(7N-10),
  z=2: 3N-6,            z=3: 6N-5,      z=7: 1.
```

Thus

```text
S_2 = e^3 sum_z count_z |zN-6|.
```

For `R=3`, the quotient L1 term is also exact. The principal coefficient is
`T_3(N)`. For odd `N`, the remaining coefficient/count pairs are

```text
-(2N-6): (N-1)(4N-5),       -(N-6): 3(N-1)(N-3),
6: N^3-7N^2+15N-9,          (N-2)(N-3): 6N-6.
```

For even `N`, they are

```text
-(3N-6): 1,                 -(2N-6): (N-2)(4N-1),
-(N-6): 3(N-2)^2,           6: N^3-7N^2+15N-10,
(N-2)(N-3): 6N-6.
```

Thus `S_3=e^3` times the resulting absolute coefficient sum. After the
`D^2`-coset expansion, the total nonprincipal coefficient L1 bound is

```text
E_R <= q S_R - T_R(N).
```

The Jacobi/conic/Kummer split is sharper than applying the `16p` bound to all
of `E_R`: the `d=0` part has L1 at most `S_R-T_R(N)`, the conic-only
`d!=0` part has L1 at most `(q-1)T_R(N)`, and the mixed `d!=0` part has L1
at most `(q-1)(S_R-T_R(N))`. Put

```text
W_R = (S_R-T_R(N)) + (q-1)T_R(N)
      + 16(q-1)(S_R-T_R(N)).
```

Thus the conservative lower numerator for the whole active union is

```text
T_R(N) (p^2 - 4p + 6 + 4 chi(-3))
  - p W_R - (6p - 11) h^3 q.
```

The corresponding uniform sufficient threshold is

```text
p >= ceil((W_R + 6h^3q)/T_R(N)) + 4.
```

When this is positive and `R<min(4,N)`, the exact-support active
quotient-window catalog itself hits every nonzero `D^2`-coset. This can prove
saturation in cases where no single fixed window is Kummer-certified. The
verifier audits two such strict improvements:

```text
R=2, p=181, n=180, N=3: exact L1 positive, bounded L1 negative.
R=3, p=113, n=112, N=4: exact L1 positive, bounded L1 negative.
```

## Contribution to M1

This theorem closes a coherent low-slack subproblem: the slack-two depth-two
canonical frontier is now split into exact quotient-window lift regimes, a
lift-limited sparse regime, and Kummer-certified saturation regimes. The
quotient-window union certificate narrows the remaining lift-limited window by
using all active quotient labels at once, not only one fixed window. It does
not prove the full M1 corrected-reserve local limit. What remains is to remove
or prove the imported Kummer-Weil estimate in a standalone algebraic-geometry
argument and extend beyond this canonical depth-two frontier toward the
genuinely aperiodic residue-line packing problem.
