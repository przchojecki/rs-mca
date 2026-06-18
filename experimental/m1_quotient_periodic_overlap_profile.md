# M1 Quotient-Periodic Support Overlap Profile

## Claim

Let `D` be a finite set partitioned into `N` disjoint fibers

```text
D = B_1 disjoint union ... disjoint union B_N,
|B_i| = m.
```

Fix `0 <= L <= N`, put `s = Lm`, and let `A_QP` be the quotient-periodic
support family

```text
A_QP = { union_{i in I} B_i : I subset {1,...,N}, |I| = L }.
```

Then

```text
|A_QP| = binom(N,L).
```

For ordered pairs of supports in `A_QP`, the whole overlap profile is the
Johnson overlap profile on the quotient, scaled by the fiber size. More
precisely, for any function `w:{0,...,s}->R`,

```text
sum_{S,T in A_QP} w(|S \ T|)
  = binom(N,L) * sum_{h=0}^{min(L,N-L)}
      binom(L,h) binom(N-L,h) w(hm).
```

Consequently the ordered exchange profile

```text
Delta_j(A_QP)
  = |{(S,T) in A_QP^2 : S != T and |S \ T| = |T \ S| = j}|
```

is

```text
Delta_j(A_QP) = 0       if m does not divide j,

Delta_{hm}(A_QP)
  = binom(N,L) binom(L,h) binom(N-L,h)
```

for `1 <= h <= min(L,N-L)`. The corresponding maximum exchange codegree is

```text
Gamma_j(A_QP) = 0       if m does not divide j,

Gamma_{hm}(A_QP)
  = binom(L,h) binom(N-L,h).
```

Now suppose this support family is used at agreement size `s = k+t`. The strict
M1 high-overlap range is `|S cap T| > k`, equivalently `|S \ T| < t`. Therefore
only quotient exchanges with

```text
1 <= hm <= t-1
```

can contribute to any strict-overlap support-family certificate. In particular,
if `t <= m`, then the quotient-periodic support family has no strict
high-overlap pairs.

More generally, for any line-field size `q`, the strict-overlap weighted
profile that appears in random-line M1 variance certificates evaluates to

```text
R_QP(t,q)
  = sum_{1 <= h <= min(L,N-L), hm <= t-1}
      binom(L,h) binom(N-L,h) q^(t-hm).
```

This is the exact quotient-periodic input to the max-codegree form of the
support-family certificate. The ordered-pair form is

```text
binom(N,L) * R_QP(t,q).
```

Equivalently, with

```text
r = floor((t - 1)/m),
```

this correction is the finite quotient prefix

```text
R_QP(t,q)
  = sum_{h=1}^{min(r,L,N-L)}
      binom(L,h) binom(N-L,h) q^(t-hm).
```

Thus the first nonzero strict-overlap quotient correction occurs only when
`t >= m+1`; in the first active band `m < t <= 2m`, it is exactly

```text
R_QP(t,q) = L(N-L) q^(t-m).
```

Equivalently, at a fixed exact agreement size `s = k+t`, the whole-fiber
quotient-periodic support family at this quotient scale is empty unless
`m | s`. If `m | s`, then `L = s/m` and the formulas above apply. Hence this
exact whole-fiber source has no strict high-overlap pairs whenever either

```text
m does not divide s,
```

or

```text
t <= m.
```

For dyadic dimensions this gives a useful dither rule. Suppose

```text
n = 2^nu,        rho = 2^(-b),        k0 = rho n,
k = k0 - r,      s = k + t = k0 + (t-r),
```

and consider a dyadic fiber size `m=2^u` with

```text
2 <= m <= k0.
```

Then `m | k0`, so this exact whole-fiber quotient-periodic family can occur at
agreement size `s` only if

```text
m | (t-r).
```

Its strict-overlap contribution further requires `m <= t-1`. Thus the
surviving dyadic whole-fiber strict-overlap scales are exactly the nontrivial
dyadic scales `m <= min(k0,t-1)` satisfying `m | (t-r)`. In particular, the
dither

```text
r = t-1
```

gives `t-r=1`, so every nontrivial dyadic whole-fiber quotient-periodic support
family at scales `2 <= m <= k0` is absent at exact agreement size `s`.

More generally, put `d=t-r` and

```text
Mmax = min(k0, t-1).
```

If `d != 0`, the surviving nontrivial dyadic strict-overlap scales are exactly

```text
m = 2^u,        1 <= u <= min(v2(|d|), floor(log2 Mmax)).
```

If `d=0`, all nontrivial dyadic scales `m <= Mmax` survive the exact-support
divisibility test. Thus any dither with `t-r` odd kills every nontrivial dyadic
whole-fiber strict-overlap scale, while `v2(|t-r|)`, capped by `Mmax`, gives
the exact number of dyadic scales that can remain when `t != r`.

## Adjacent-Slack Dither Obstruction

The dyadic dither rule above is intrinsically a one-slack rule. Keep the
dyadic setup and fix one integer dither `r`. For a slack value `u`, write

```text
s_u = k0 + (u-r).
```

Assume `k0 >= 2`, and assume that the support size stays away from the
scale-two quotient endpoints for the slacks being considered:

```text
2 <= s_u <= n-2.
```

Then, for every `u >= 3`, the nontrivial dyadic scale `m=2` has a strict
whole-fiber quotient-periodic contribution exactly when

```text
u-r is even.
```

At such a slack, `L=s_u/2`, `N=n/2`, and the first exchange codegree is

```text
Gamma_2 = L(N-L) = s_u(n-s_u)/4,
```

so the scale-two contribution to the weighted whole-fiber ledger is

```text
Gamma_2 q^(u-2).
```

Consequently, for any adjacent slacks `t,t+1` with `t >= 3`, exactly one of
`t-r` and `t+1-r` is even. Under the same interior assumption, one of those two
slacks therefore has a nonzero scale-two strict-overlap quotient term. Hence
no fixed dimension dither can eliminate all nontrivial dyadic whole-fiber
quotient-periodic strict-overlap scales at two adjacent slack radii.

More generally, on any integer slack interval `W subset {3,4,...}` where the
support sizes remain in the displayed interior range, scale `m=2` survives at
exactly the slacks

```text
u in W,        u == r mod 2.
```

Thus the number of slacks in the interval with a surviving scale-two
whole-fiber term is either `floor(|W|/2)` or `ceil(|W|/2)`. Reusing the
single-slack maximal dither `r=t-1` at the next slack is the smallest example:
at slack `t+1`, the difference is `(t+1)-r=2`, so the dyadic scale `m=2`
survives immediately.

## Fixed-Dither Slack-Window Ledger

The same residue-class obstruction holds at every dyadic scale. Keep the
dyadic setup, fix one dither `r`, and fix a nontrivial dyadic scale

```text
m = 2^a,        2 <= m <= k0.
```

For an integer slack interval

```text
W = {T0, T0+1, ..., T1},
```

define the scale-`m` eligible sub-window by

```text
s_u = k0 + (u-r),

W_m(r) = {u in W : u >= m+1 and m <= s_u <= n-m}.
```

Then the scale-`m` whole-fiber quotient family is active at slack `u in W`
exactly when

```text
u in W_m(r)        and        u == r mod m.
```

At every such active slack, with `N=n/m` and `L=s_u/m`, the first exchange
codegree and weighted first-exchange ledger term are

```text
Gamma_m(u) = L(N-L) = s_u(n-s_u)/m^2,

Gamma_m(u) q^(u-m).
```

The active-slack count in the window is therefore the exact residue count

```text
C_m(W,r) = |{u in W_m(r) : u == r mod m}|.
```

In particular, if the endpoint condition `m <= s_u <= n-m` holds on every
slack in an interval of eligible strict range, then every block of `m`
consecutive slacks in that interval activates scale `m` exactly once. On such
an eligible interval of length `ell`, the count is either `floor(ell/m)` or
`ceil(ell/m)`.

Equivalently, the whole first-exchange dyadic quotient ledger over a slack
window is the finite set

```text
L_win(r) = {
  (u,m) : u in W, m=2^a, 2 <= m <= k0,
          u >= m+1, m <= s_u <= n-m, u == r mod m
}.
```

For `(u,m) in L_win(r)`, the entry contributes

```text
(s_u/m)(n/m - s_u/m) q^(u-m)
```

to the scale-`m` first-exchange part of the quotient-periodic random-line
ledger. When `m < u <= 2m`, this first-exchange term is the entire strict
whole-fiber quotient contribution at that scale. For larger slack, higher
quotient exchanges may also appear, but only at scales already listed in
`L_win(r)`.

## One-Remainder-Fiber Profile

The exact-support divisibility guardrail above only treats supports that are
unions of whole fibers. If

```text
s = Lm + r,        1 <= r < m,
```

there is a natural one-remainder-fiber family

```text
A_REM = {
  union_{i in I} B_i  union  R :
  |I|=L, p notin I, R subset B_p, |R|=r
}.
```

Its size is

```text
|A_REM| = binom(N,L) (N-L) binom(m,r).
```

For a fixed support `S in A_REM`, let

```text
H_REM(y) = sum_{T in A_REM} y^|S \ T|.
```

With the convention `binom(a,b)=0` for infeasible `b`, the exact fixed-support
exchange enumerator is

```text
H_REM(y)
 =
  (sum_h binom(L,h) binom(N-L-1,h) y^(hm))
  (sum_l binom(r,l) binom(m-r,l) y^l)

  + L binom(m,r) sum_h binom(L-1,h) binom(N-L-1,h) y^(hm+m-r)
  + L binom(m,r) sum_h binom(L-1,h) binom(N-L-1,h+1) y^((h+1)m)

  + (N-L-1) binom(m,r) sum_{h>=1}
      binom(L,h) binom(N-L-2,h-1) y^(hm)
  + (N-L-1) binom(m,r) sum_h
      binom(L,h) binom(N-L-2,h) y^(hm+r).
```

Therefore

```text
Gamma_j(A_REM) = [y^j] H_REM(y),
Delta_j(A_REM) = |A_REM| [y^j] H_REM(y)       for j >= 1.
```

The strict-overlap weighted correction is consequently

```text
R_REM(t,q) = sum_{1 <= j <= t-1} Gamma_j(A_REM) q^(t-j).
```

This remainder family has a qualitatively different first strict-overlap term
from the whole-fiber family. Even when `t <= m`, same-remainder-fiber exchanges
contribute at point exchange sizes

```text
1 <= j <= min(r,m-r,t-1)
```

through the first product in `H_REM`. Thus dimension dither can remove exact
whole-fiber quotient-periodic supports while still leaving a smaller
one-remainder-fiber profile that must be budgeted separately.

## General Fiber-Occupancy Profile

The whole-fiber and one-remainder families are the first two cases of a more
general quotient-fiber content ledger.  For a support `S`, record the
occupancy histogram

```text
h_a(S) = |{ i : |S cap B_i| = a }|,        0 <= a <= m.
```

Fix a histogram

```text
h=(h_0,...,h_m),        sum_a h_a=N,        sum_a a h_a=s,
```

and let

```text
A_h = { S subset D : h_a(S)=h_a for every a }.
```

Then

```text
|A_h| =
  N!/(prod_a h_a!) prod_{a=0}^m binom(m,a)^{h_a}.
```

For `0 <= a,b <= m`, define the one-fiber transition polynomial

```text
P_{a,b}(y)
 =
  sum_x binom(a,x) binom(m-a,b-x) y^(a-x),
```

where the sum ranges over

```text
max(0,a+b-m) <= x <= min(a,b).
```

Here `x` is the within-fiber overlap between an old occupancy-`a` fiber and a
new occupancy-`b` fiber.  For any fixed `S in A_h`, the full exchange
enumerator

```text
H_h(y) = sum_{T in A_h} y^|S \ T|
```

is independent of `S` and is given by the coefficient extraction

```text
H_h(y)
 =
 [z_0^h_0 ... z_m^h_m]
 prod_{a=0}^m
   ( sum_{b=0}^m z_b P_{a,b}(y) )^h_a.
```

Consequently

```text
Gamma_j(A_h) = [y^j] H_h(y),
Delta_j(A_h) = |A_h| [y^j] H_h(y)        for j >= 1,
```

and the strict-overlap random-line ledger is

```text
R_h(t,q) = sum_{1 <= j <= t-1} [y^j] H_h(y) q^(t-j).
```

This gives an exact, finite coefficient formula for every quotient-fiber
content class.  The whole-fiber quotient-periodic profile is the specialization
`h_0=N-L`, `h_m=L`.  The one-remainder profile is the specialization
`h_0=N-L-1`, `h_b=1`, `h_m=L`; expanding the coefficient formula by the
location of the new remainder fiber gives the displayed `H_REM` formula above.

There is a complete histogram-enumeration corollary.  For fixed support size
`s`, the families `A_h` over all histograms satisfying

```text
sum_a h_a=N,        sum_a a h_a=s
```

partition the full support layer `{S subset D : |S|=s}`. Hence

```text
sum_h |A_h| = binom(Nm,s).
```

A finite M1 scanner can therefore enumerate histograms rather than supports:
for each content class it emits `|A_h|`, `[y^j]H_h(y)`, and `R_h(t,q)` for
`1 <= j < t`. This is complete for within-content quotient-fiber covariance.

The same coefficient extraction handles cross-histogram pairs. For two
histograms `h,g`, define

```text
H_{h->g}(y) = sum_{T in A_g} y^|S \ T|        for fixed S in A_h.
```

Then

```text
H_{h->g}(y)
 =
 [z_0^g_0 ... z_m^g_m]
 prod_{a=0}^m
   ( sum_{b=0}^m z_b P_{a,b}(y) )^h_a.
```

This gives the ordered cross-pair profile

```text
Delta_j(A_h,A_g) = |A_h| [y^j] H_{h->g}(y).
```

Consequently, for any union of content classes

```text
A_U = union_{h in U} A_h,
```

the exact ordered-pair profile and max-codegree profile are

```text
Delta_j(A_U) =
  sum_{h in U} |A_h| sum_{g in U} [y^j]H_{h->g}(y),

Gamma_j(A_U) =
  max_{h in U} sum_{g in U} [y^j]H_{h->g}(y).
```

Thus quotient-fiber content unions also have an exact finite ledger; no support
enumeration is needed for either within-content or cross-content covariance.
When `U` is the set of all histograms at support size `s`, this union ledger
recovers the ordinary Johnson layer:

```text
Gamma_j(A_U) = binom(s,j) binom(Nm-s,j),
Delta_j(A_U) = binom(Nm,s) binom(s,j) binom(Nm-s,j).
```

## Large-Fiber Remainder Truncation

The one-remainder formula becomes especially useful in the large-fiber range
`t <= m`. To avoid overloading notation, write the support remainder as `b`:

```text
s = Lm + b,        1 <= b < m.
```

If `t <= m`, then the whole strict range `1 <= j <= t-1` of the
one-remainder-fiber profile is

```text
H_REM^{<t}(y)
 =
  sum_{ell=1}^{min(b,m-b,t-1)}
    binom(b,ell) binom(m-b,ell) y^ell

  + 1_{b<t} (N-L-1) binom(m,b) y^b
  + 1_{m-b<t} L binom(m,b) y^(m-b).
```

Equivalently, in the same range

```text
R_REM^{<t}(t,q)
 =
  sum_{ell=1}^{min(b,m-b,t-1)}
    binom(b,ell) binom(m-b,ell) q^(t-ell)

  + 1_{b<t} (N-L-1) binom(m,b) q^(t-b)
  + 1_{m-b<t} L binom(m,b) q^(t-m+b),
```

with terms of the same exponent combined in the evident way.

This is the exact large-fiber remainder budget: below one full fiber exchange,
only three events survive.

1. The remainder fiber is the same and `ell` remainder points are swapped.
2. The remainder fiber moves to an unused nonwhole fiber, contributing `b`
   old points.
3. The remainder fiber moves onto an old whole fiber while the old remainder
   fiber is promoted to a whole fiber, contributing `m-b` old points.

All other cases in `H_REM` contain at least one whole-fiber exchange and have
exponent at least `m`, hence are outside the strict range when `t <= m`.

For dyadic dimension dithering this gives a concrete maximal-remainder
corollary. Suppose

```text
n = 2^nu,        rho = 2^(-alpha),    k0 = rho n,
k = k0 - r0,     s = k + t = k0 + d,
d = t - r0,      1 <= d < t.
```

At any nontrivial dyadic fiber size `m | k0` with `m > d`, the exact support
remainder is `b=d`. If also `t <= m`, then the large-fiber formula above is
the complete strict one-remainder profile at that scale.

In the maximal-dither case `r0=t-1`, one has `d=1` and `s=k0+1`. Therefore,
for every dyadic scale `m | k0` with `m > t`,

```text
H_REM^{<t}(y) = (n-k0-1)y,
R_REM^{<t}(t,q) = (n-k0-1) q^(t-1).
```

Indeed `L=k0/m` and `N=n/m`, so

```text
(m-1) + (N-L-1)m = (N-L)m - 1 = n-k0-1.
```

If `m=t`, the same one-point term remains and there is one boundary term

```text
L m y^(t-1) = k0 y^(t-1),
```

coming from moving the one-point remainder onto an old whole fiber and
promoting the old remainder fiber. Thus maximal dither converts every large
dyadic one-remainder quotient packet into a linear strict codegree. The only
scales not covered by this corollary are the small scales `m < t`, where the
full `H_REM` formula or a finite scanner should be used.

There is also a stable large-scale hierarchy for nonmaximal dither. Keep the
same dyadic setup, and assume

```text
1 <= d < t,        m | k0,        m >= t+d.
```

Then `b=d`, the boundary promotion term is absent, and the complete strict
one-remainder profile is

```text
H_REM^{<t}(y)
 =
  sum_{ell=1}^d binom(d,ell) binom(m-d,ell) y^ell
  + ((n-k0)/m - 1) binom(m,d) y^d.
```

Consequently its unweighted strict codegree mass is

```text
H_REM^{<t}(1) = ((n-k0)/m) binom(m,d) - 1.
```

Thus the maximal dither `d=1` is not just sufficient to remove whole-fiber
quotient cores; it is the unique dither in this stable range that makes the
large-scale one-remainder strict codegree linear in the ambient codimension
`n-k0`, uniformly over all dyadic scales. For `d>=2`, large scales retain the
degree-`d` binomial factor `binom(m,d)` and therefore can still be a genuinely
larger quotient-profile term.

This gives a fixed-window obstruction. Suppose one fixed dither is maximal at
slack `t0`, so

```text
r0 = t0 - 1.
```

At the adjacent slack `t0+1`, the same dither has

```text
d = (t0+1)-r0 = 2.
```

Therefore, for every dyadic scale `m | k0` with

```text
m >= t0 + 3,
```

the stable large-scale one-remainder mass at slack `t0+1` is exactly

```text
H_REM^{<t0+1}(1)
  = ((n-k0)/m) binom(m,2) - 1
  = (n-k0)(m-1)/2 - 1.
```

By contrast, at the original slack `t0`, maximal dither has the linear
large-scale mass

```text
n-k0-1.
```

Thus a fixed dither that is optimal for one slack cannot keep the adjacent
large-scale one-remainder quotient packets uniformly tangent-sized. The next
slack already restores a scale-dependent mass of order `(n-k0)m`.

More generally, for any fixed dither `r0` and any slack `t` with
`d=t-r0 >= 2`, every dyadic scale `m | k0` satisfying `m >= t+d` has exact
stable mass

```text
((n-k0)/m) binom(m,d) - 1.
```

This is a degree-`d-1` polynomial in the scale `m` after the ambient codimension
factor is pulled out. Consequently, fixed-window dithering cannot be analyzed
only by asking which whole-fiber quotient scales survive; the one-remainder
ledger is a separate large-scale obstruction.

There is a complementary stable formula for near-full remainders. Taking
set-complements sends a one-remainder family with parameters `(N,m,L,b)` to
one with parameters

```text
(N,m,N-L-1,m-b),
```

and preserves the exchange size `|S\T|`. Therefore

```text
H_REM(N,m,L,b;y) = H_REM(N,m,N-L-1,m-b;y).
```

In particular, if `1 <= d < t` and

```text
b = m-d,        m >= t+d,
```

then the complete strict profile is

```text
H_REM^{<t}(y)
 =
  sum_{ell=1}^d binom(d,ell) binom(m-d,ell) y^ell
  + L binom(m,d) y^d.
```

The unweighted strict codegree mass is

```text
H_REM^{<t}(1) = (L+1) binom(m,d) - 1.
```

This is the over-dithered counterpart of the previous hierarchy. In a dyadic
window, if `t-r0=-d` and `m | k0` with `m>d`, the support size has remainder
`m-d`; for stable large scales the strict remainder packet is governed by the
displayed co-remainder mass. Thus fixed-window dithering has two large-scale
one-remainder tails: the under-dithered tail with coefficient `(N-L)` and the
over-dithered tail with coefficient `L+1`.

Equivalently, one can state the stable tail directly in fixed-dither
coordinates. Keep the dyadic setup, fix a dither `r0`, and let

```text
d_t = t-r0,        e_t = |d_t|.
```

Assume

```text
1 <= e_t < t,        m | k0,        m >= t+e_t.
```

Then the stable large-scale one-remainder strict mass at slack `t` is exactly

```text
M_stable(t,r0,m)
 =
  ((n-k0)/m) binom(m,d_t) - 1,        if d_t > 0,
  (k0/m) binom(m,e_t) - 1,            if d_t < 0.
```

Thus a fixed dither has two different large-scale tails across a slack window:
slacks above the dither are charged to the unused quotient side, while slacks
below the dither are charged to the occupied quotient side. This matters most
near high rate, where `k0/m` and `(n-k0)/m` can be very different.

The weighted random-line correction has the same two-sided closed form. Let
`e=|d_t|`. In the stable range above,

```text
R_stable(t,r0,m,q)
 =
  sum_{ell=1}^e binom(e,ell) binom(m-e,ell) q^(t-ell)
  + C_side binom(m,e) q^(t-e),
```

where

```text
C_side = (n-k0)/m - 1,        if d_t > 0,
C_side = k0/m - 1,            if d_t < 0.
```

This is the exact `R_A(t,q)` contribution of the stable large-scale
one-remainder packet in the M1 support-family variance ledger. The unweighted
formula above is recovered by setting `q=1` after combining the Vandermonde
sum with the side coefficient.

The same two-sided formula gives a minimax obstruction for fixed slack-window
dither.  Let

```text
W = {t_-, t_-+1, ..., t_+},        L_W = t_+ - t_- + 1,
E_W(r0) = max_{t in W} |t-r0|.
```

For unrestricted integer `r0`, the smallest possible endpoint gap is the
center radius

```text
min_{r0 in Z} E_W(r0) = floor(L_W/2).
```

This center choice is not a quotient cure: any integer minimizer lies inside
the slack interval, and at slack `t=r0` the support size is exactly `k0`, so
the exact whole-fiber support family reappears at every dyadic scale dividing
`k0`; its strict activity is then governed by the whole-fiber ledger above.
If one requires no exact-`k0` slack in the window, i.e. `r0 notin W`, then

```text
min_{r0 notin W} E_W(r0) = L_W,
```

with the two extremal choices `r0=t_- - 1` and `r0=t_+ + 1`.  Consequently, a
single fixed dither that avoids the exact-`k0` slack over a window of length
`L_W` must have an endpoint with one-remainder gap at least `L_W`.  Whenever
that endpoint is in the stable range `L_W < t` and `m >= t+L_W`, the
two-sided formula above gives an explicit stable tail of binomial degree
`L_W`:

```text
((n-k0)/m) binom(m,L_W) - 1
```

on the upper side, or

```text
(k0/m) binom(m,L_W) - 1
```

on the lower side.  Thus the adjacent-slack obstruction is the first case
`L_W=2` of a general fixed-window phenomenon: avoiding an exact support
slack by moving the dither outside the window makes the far endpoint carry a
large-scale one-remainder tail whose binomial degree is the full window
length.

There is also an exact finite-menu version. Let `R` be a set of allowed
integer dithers, and suppose that at each slack `t in W` the proof system may
choose some `r in R` with `r != t`, so exact support `k0` is not used at that
slack. For a target safe gap `D >= 1`, a single dither covers at most `D`
consecutive slacks, because the forbidden point `t=r` separates its two arms.
Two dithers cover at most

```text
3D+1
```

consecutive slacks: if their centers are farther than `D` apart they cannot
cover each other's forbidden points without a gap, while if their centers are
within distance `D` their union lies in an interval of length at most `3D+1`.
Pairing dithers from left to right gives the exact capacity

```text
Cap(C,D) = floor(C/2)(3D+1) + (C mod 2)D.
```

For the upper bound, look at a maximal consecutive block of slacks safely
covered by a menu. Any dither whose center lies strictly inside the block has
its own center as a puncture, so that puncture must be covered by another
dither within distance `D`. Thus interior dithers can be charged in pairs. A
paired pair contributes at most `3D+1` consecutive slacks as above. After all
such pairs are removed, at most one unpaired dither can contribute to one
endpoint of the block, and it contributes at most `D` consecutive slacks. This
gives the displayed upper bound for every consecutive slack block.

This bound is sharp. A pair of dithers at `a+D` and `a+2D` safely covers the
block `{a,...,a+3D}`, and a leftover single dither at `a+D` safely covers the
block `{a,...,a+D-1}`. Hence a `C`-value menu can safely cover `W` with gap at
most `D` if and only if

```text
L_W <= Cap(C,D).
```

This gives closed inverse formulas. For a target gap `D`, the exact minimum
menu size is

```text
C_D
 = min(
     2 ceil(L_W/(3D+1)),
     2 ceil(max(0,L_W-D)/(3D+1)) + 1
   ).
```

The first term uses only paired dithers, while the second uses one leftover
single dither plus paired dithers. Conversely, for a fixed menu size `C`, put

```text
p=floor(C/2),        eps=C mod 2.
```

The exact forced safe gap is

```text
D_C = max(1, ceil((L_W-p)/(3p+eps))).
```

Equivalently, every menu of `C` fixed dithers has some slack whose safe gap is
at least

```text
D_C.
```

The earlier counting lower bound `ceil(L_W/(2D))` is only a coarse corollary;
the puncture at `t=r` is what makes the exact capacity smaller than `2CD`.
Thus keeping stable one-remainder degree bounded across a growing slack window
requires a growing dither menu, unless one allows the exact-`k0` slack or
switches to genuinely per-slack dimension choices.

Combining this covering lemma with the two-sided stable-tail formula gives a
direct mass lower bound. Suppose a menu `R` of size `C` serves every slack in
`W` with a nonzero gap at most `D`, and set

```text
E = D_C = min { D' >= 1 : L_W <= Cap(C,D') }.
```

Assume

```text
D < t_-,        m | k0,        m >= t_+ + D.
```

Then there is some served slack `t in W` whose chosen dither has gap
`e=|t-r| >= E`.  Since `e <= D < t` and `m >= t+D >= t+e`, this slack is in
the stable range.  Moreover `e <= D < m/2`, so `binom(m,e) >= binom(m,E)`.
The stable one-remainder mass at that slack and scale is therefore at least

```text
min(k0/m, (n-k0)/m) binom(m,E) - 1.
```

Thus a bounded dither menu does not merely force a large gap somewhere; at
every sufficiently large dyadic quotient scale it forces a quantitative
one-remainder tail. This is the scale-level obstruction that a fixed menu must
pay before the remaining aperiodic M1 local-limit problem is reached.

The same argument gives the weighted random-line floor. In the stable profile
at the witness slack, all strict exchange sizes are at most the chosen gap
`e <= D`. Therefore every strict coefficient in `R_stable(t,r,m,q)` is
multiplied by at least `q^(t-D)`, and since `t >= t_-`,

```text
R_stable(t,r,m,q)
  >= (min(k0/m, (n-k0)/m) binom(m,E) - 1) q^(t_- - D).
```

This is the lower-bound form consumed directly by the M1 random-line variance
ledger. It is weaker than evaluating the exact two-sided weighted formula at
the witness slack, but it depends only on the menu size, window length, stable
gap budget, quotient scale, and line-field size.

The contrast with genuinely adaptive dither is sharp. If at each slack `t in W`
one may choose the maximal dither

```text
r(t)=t-1,
```

then every slack has exact support size `s=k0+1`. For every dyadic quotient
scale `m | k0` with

```text
m > t_+,
```

the maximal-dither large-scale formula gives, uniformly for all `t in W`,

```text
H_REM,max,t^{<t}(y) = (n-k0-1)y,
R_REM,max,t(t,q) = (n-k0-1)q^(t-1).
```

Thus the whole slack window has a large-scale adaptive baseline

```text
max_{t in W} R_REM,max,t(t,q) = (n-k0-1)q^(t_+-1)
```

at every dyadic scale `m>t_+`. All nonlinear maximal-dither quotient-remainder
terms over the window are confined to the finite prefix `m <= t_+`. This is
the precise sense in which a per-slack dimension choice avoids the finite-menu
tail floor above.

The finite-menu floor separates from this adaptive baseline whenever the
forced gap is at least two and the quotient scale is large enough.  At a stable
scale `m`, write

```text
A_ad = n-k0-1,
B_menu(m) = min(k0/m,(n-k0)/m) binom(m,E) - 1.
```

The adaptive maximal-dither mass at the same slack and scale is `A_ad`, while
the `C`-value menu forces mass at least `B_menu(m)` for some slack in the
window. Thus the finite menu already beats the adaptive linear tail whenever

```text
B_menu(m) > A_ad.
```

For fixed rate and fixed `E>=2`, the ratio `B_menu(m)/A_ad` grows like a
positive constant times `m^(E-1)`.  Hence any bounded menu whose exact capacity
forces `E>=2` eventually reintroduces a super-linear large-scale tail, while
adaptive maximal dither remains linear at all scales `m>t_+`.  With a line
field of size `q`, the same-slack weighted comparison has the conservative
criterion

```text
B_menu(m) > A_ad q^(D-1),
```

because the finite-menu weighted floor loses at most `q^(D-1)` relative to the
adaptive maximal-dither term at the same witness slack.

In the dyadic quotient-profile setting this comparison has an exact binomial
threshold. Suppose `m | k0` and `m | n`, and put

```text
K_side = min(k0,n-k0).
```

For a forced gap `E`, the finite-menu mass floor satisfies

```text
B_E(m)+1
  = (K_side/m) binom(m,E)
  = (K_side/E) binom(m-1,E-1).
```

Thus the finite-menu floor beats the adaptive linear mass exactly when

```text
K_side binom(m-1,E-1) > E(n-k0).
```

For the usual prize rates `k0 <= n/2`, this becomes the rate-only threshold

```text
binom(m-1,E-1) > E (n-k0)/k0.
```

In particular, for forced gap `E=2`, the first mass-separating dyadic scale is
the first dyadic `m` with

```text
m > 1 + 2(n-k0)/k0.
```

At rates `1/2, 1/4, 1/8, 1/16`, this gives first dyadic separating scales
`4, 8, 16, 32`, before imposing the stable-range condition
`m >= t_+ + D`. For `E=1`, the same criterion is false at all rates
`k0 <= n/2`, with equality only at rate `1/2`; hence gap one is exactly the
linear-mass-competitive regime in the standard rate range.

The same closed form converts the weighted same-slack comparison into an exact
integer inequality. With `Q=q^(D-1)`, the finite-menu floor beats the adaptive
same-slack weighted mass exactly when

```text
K_side binom(m-1,E-1) > E((n-k0-1)Q + 1).
```

For comparison against the whole adaptive slack window, the conservative
weighted floor above must be compared to

```text
(n-k0-1)q^(t_+-1).
```

Let

```text
G_win = t_+-1-(t_- - D) = |W| + D - 2.
```

Then the finite-menu lower bound beats the adaptive window maximum exactly
when

```text
K_side binom(m-1,E-1) > E((n-k0-1)q^G_win + 1).
```

Thus the whole-window comparison is stricter than the same-slack comparison by
the extra factor `q^(|W|-1)`. This isolates the field-size penalty as an
explicit scale threshold: increasing `q` or the allowed service gap `D` only
delays the first separating scale; it does not change the binomial degree
forced by a fixed menu.

Consequently, a finite menu is scale-unbounded adaptive-competitive exactly in
the gap-one case.  More precisely, fix a nontrivial asymptotic dyadic rate
`0 < k0/n < 1` and a finite same-slack field penalty. If the forced menu gap
`E` is at least two, then the binomial threshold above is crossed at all
sufficiently large dyadic stable scales in the family. If `E=1`, then

```text
B_1(m) = min(k0,n-k0)-1 <= n-k0-1 = A_ad,
```

so the finite-menu mass floor never beats the adaptive linear mass. Thus
scale-unbounded mass competitiveness is equivalent to forcing `D_C=1`.

The exact menu size needed for this is the exact capacity at safe gap one.
For a slack window of length `L_W`,

```text
Cap(C,1) =
  2C       if C is even,
  2C-1     if C is odd.
```

Equivalently, writing `L_W=4a+r` with `0 <= r <= 3`, the minimum
asymptotically adaptive-competitive menu size is

```text
C_ad(L_W) =
  2a       if r=0,
  2a+1     if r=1,
  2a+2     if r=2 or r=3.
```

Any smaller menu has forced gap at least two and therefore eventually pays a
super-linear finite-menu tail at large dyadic scales. This is the precise
menu-size cost of replacing per-slack adaptive maximal dither by a finite menu
without allowing the exact-`k0` slack.

This threshold is also sufficient. A capacity-achieving gap-one menu covers
`W` by adjacent dithers: every served slack `t` has a permitted choice
`r=t-1` or `r=t+1`. At every stable dyadic scale `m | k0` with `m >= t+1`,
the two-sided stable formula gives the exact linear profile

```text
r=t-1:   H_REM^{<t}(y) = (n-k0-1)y,
         R_REM(t,q) = (n-k0-1)q^(t-1),

r=t+1:   H_REM^{<t}(y) = (k0-1)y,
         R_REM(t,q) = (k0-1)q^(t-1).
```

Thus, in the standard rate range `k0 <= n/2`, every gap-one menu choice has
same-slack mass and weighted correction at most the adaptive maximal-dither
baseline, with equality only on the under-dithered side. Combining this
sufficiency statement with the forced-gap lower bound above gives an exact
large-scale characterization: over an unbounded dyadic quotient hierarchy,
finite-menu stable tails are asymptotically adaptive-competitive if and only
if the menu size is at least `C_ad(L_W)`.

Finally, the maximal-dither remainder case has an exact all-scale formula, so
small scales need not be handled as a black-box enumeration. Suppose

```text
s = Lm + 1,        A = N-L-1.
```

Then the full strict profile of the one-remainder family in the range
`1 <= j <= t-1` is

```text
H_REM,1^{<t}(y)
 =
  sum_{h>=0, hm+1<t}
    binom(L,h) binom(A,h) (m(A-h+1)-1) y^(hm+1)

  + sum_{h>=1, hm<t}
      binom(L,h) binom(A,h) (1+2mh) y^(hm)

  + sum_{h>=1, hm-1<t}
      mh binom(L,h) binom(A,h-1) y^(hm-1),
```

again using `binom(a,b)=0` for infeasible `b`. Therefore the exact weighted
strict correction is obtained by multiplying each coefficient of `y^j` above
by `q^(t-j)`.

In the dyadic maximal-dither setting `s=k0+1`, every nontrivial scale
`m | k0` has remainder one, so this formula applies at every dyadic quotient
scale. The large-scale corollary above is exactly its `h=0` first-band term
when `m>t`, and the boundary case `m=t` is obtained by adding the final-band
term at `h=1`.

Thus maximal dither confines the nonlinear quotient-remainder work to a finite
small-scale prefix.  Let

```text
S_small(t,k0)
  = { m=2^u : 2 <= m < t and m | k0 }.
```

Then

```text
|S_small(t,k0)| <= 0                         if t <= 2,
|S_small(t,k0)| <= floor(log2(t-1))          if t >= 3.
```

For every dyadic quotient scale `m | k0` with `m>t`, the complete strict
profile is the same linear tail

```text
H_REM,1^{<t}(y) = (n-k0-1)y.
```

If `t` is itself a dyadic divisor of `k0`, there is exactly one boundary scale
`m=t`, where

```text
H_REM,1^{<t}(y) = (n-k0-1)y + k0 y^(t-1).
```

All other nonlinear terms in the all-scale formula occur only for
`m in S_small(t,k0)`.  Consequently, for fixed slack `t`, maximal dither turns
the entire growing dyadic quotient hierarchy into a uniform linear large-scale
tail plus an explicitly enumerable small-scale prefix of size at most the
displayed bound.

The over-dithered adjacent choice has the complementary all-scale formula.
For `s=k0-1` and a dyadic scale `m | k0`,

```text
s = (k0/m-1)m + (m-1).
```

Taking set-complements sends this co-remainder-one packet to the preceding
one-remainder formula with

```text
L^vee = (n-k0)/m,        A^vee = k0/m-1.
```

Thus its full strict profile is the same three-band expression as
`H_REM,1^{<t}`, with `L,A` replaced by `L^vee,A^vee`. In particular, for every
dyadic quotient scale `m | k0` with `m>t`,

```text
H_REM,m-1^{<t}(y) = (k0-1)y,
```

and if `m=t`, then

```text
H_REM,m-1^{<t}(y) = (k0-1)y + (n-k0)y^(t-1).
```

All other nonlinear terms again occur only for `m in S_small(t,k0)`. Therefore
both adjacent gap-one menu choices have complete all-scale quotient ledgers:
the under-dithered choice `r=t-1` uses the one-remainder formula above, while
the over-dithered choice `r=t+1` uses this complement-dual co-remainder
formula.

Consequently a gap-one menu has the same finite-prefix confinement as fully
adaptive maximal dither, but now uniformly over the whole window. For
`W=[t_-,t_+]`, every served slack has an adjacent choice. At any dyadic scale
`m | k0` with

```text
m > t_+,
```

both adjacent all-scale formulas are already in their linear large-scale
regime. The possible nonlinear quotient-remainder scales over the entire
window are therefore contained in the finite prefix

```text
S_win(W,k0) = { m=2^u : 2 <= m <= t_+ and m | k0 },
```

so

```text
|S_win(W,k0)| <= floor(log2 t_+).
```

Within this prefix, the boundary term can occur only at a slack with `m=t`,
and the remaining nonlinear terms are exactly the explicit three-band
one-remainder or co-remainder prefixes above. Thus a gap-one menu does not
remove all small quotient-remainder bookkeeping, but it prevents any nonlinear
large-scale tail from surviving beyond the window endpoint.

Putting the preceding pieces together gives an exact finite-menu dichotomy.
For a window of length `L_W` and a `C`-value dither menu that avoids the
exact-`k0` slack, let

```text
D_C = min { D >= 1 : L_W <= Cap(C,D) }.
```

If `D_C=1`, equivalently `C >= C_ad(L_W)`, then there is an explicit gap-one
menu and every dyadic quotient-remainder scale `m>t_+` has a linear all-scale
profile on both adjacent sides. If `D_C>=2`, then every such menu has some
served slack whose stable large-scale one-remainder mass has binomial degree
`D_C`; over an unbounded dyadic quotient hierarchy this eventually exceeds the
adaptive linear baseline, and with line field size `q` it crosses the same-slack
or whole-window weighted thresholds exactly when the displayed binomial
inequalities above hold. Thus finite menus have only two large-scale regimes:
gap-one finite-prefix linearity, or a forced super-linear stable tail.

## Random-Line Certificate Corollaries

The overlap profiles above plug directly into the support-family random-line
certificate. Let `A` be any deterministic support family of exact size
`s=k+t`, put

```text
M = |A|,
R_A(t,q) = sum_{1 <= j <= t-1} Gamma_j(A) q^(t-j),
```

and let `Bad_t(A;f,g)` denote the slopes witnessed by supports in `A` for
uniform random words `f,g in F^D`, where `|F|=q`. For each fixed slope, the
support-family certificate gives

```text
E[1 - |Bad_t(A;f,g)|/q]
  <= (1-p_z)/(M p_z) + 4 R_A(t,q)/M,

p_z = q^(-t)(1-q^(-t)).
```

Since `q >= 2`, this implies the simpler finite bound

```text
E[1 - |Bad_t(A;f,g)|/q]
  <= (2 q^t + 4 R_A(t,q)) / M.
```

For the whole-fiber quotient-periodic family, `M=binom(N,L)` and
`R_A=R_QP`. Hence

```text
E[1 - |Bad_t(A_QP;f,g)|/q]
  <= (2 q^t + 4 R_QP(t,q)) / binom(N,L).
```

In particular, if `m | s` and `t <= m`, then `R_QP=0`, so the whole-fiber
quotient family behaves like an independent support family in the fixed-slope
random-line certificate:

```text
E[1 - |Bad_t(A_QP;f,g)|/q]
  <= 2 q^t / binom(N,L).
```

In the first active band `m < t <= 2m`,

```text
E[1 - |Bad_t(A_QP;f,g)|/q]
  <= (2 q^t + 4 L(N-L) q^(t-m)) / binom(N,L).
```

For the one-remainder family, with `s=Lm+b` and `1 <= b < m`,

```text
M_REM = binom(N,L)(N-L)binom(m,b),
```

and the corresponding certificate is

```text
E[1 - |Bad_t(A_REM;f,g)|/q]
  <= (2 q^t + 4 R_REM(t,q)) / M_REM.
```

Under dyadic maximal dither, `s=k0+1`, and at every dyadic scale `m | k0`
with `m>t`, the one-remainder packet has `b=1`,

```text
M_REM = binom(n/m,k0/m)(n-k0),
R_REM(t,q) = (n-k0-1) q^(t-1).
```

Therefore

```text
E[1 - |Bad_t(A_REM;f,g)|/q]
  <= (2 q^t + 4(n-k0-1)q^(t-1))
      / (binom(n/m,k0/m)(n-k0)).
```

At the boundary scale `m=t`, the one-point term remains and the boundary
promotion contributes `k0 q`, giving

```text
R_REM(t,q) = (n-k0-1)q^(t-1) + k0 q.
```

The maximal-dither all-scale formula gives the exact certificate at every
dyadic scale, not only in the large-scale tail.  For `m | k0`, let

```text
N=n/m,        L=k0/m,
R_MAX(m,t,q) = sum_{1 <= j <= t-1}
  [y^j] H_REM,1^{<t}(y) q^(t-j),
```

where `H_REM,1^{<t}` is the three-band formula above with these `N,L,m`.
Then

```text
E[1 - |Bad_t(A_REM;f,g)|/q]
  <= (2 q^t + 4 R_MAX(m,t,q))
      / (binom(n/m,k0/m)(n-k0)).
```

The scale-confinement corollary makes this a finite-prefix ledger:

```text
m>t:   R_MAX(m,t,q) = (n-k0-1)q^(t-1),

m=t:   R_MAX(m,t,q) = (n-k0-1)q^(t-1) + k0 q,

m<t:   use the explicit three-band prefix, for at most
       floor(log2(t-1)) dyadic scales when t>=3.
```

For the over-dithered adjacent choice `s=k0-1`, the complement-dual ledger
has the same form with the two sides exchanged:

```text
m>t:   R_CO_MAX(m,t,q) = (k0-1)q^(t-1),

m=t:   R_CO_MAX(m,t,q) = (k0-1)q^(t-1) + (n-k0)q,

m<t:   use the complement-dual three-band prefix, for the same finite set
       of dyadic scales.
```

Thus maximal dither has a closed random-line certificate at every dyadic
quotient-remainder scale.  The only scale-dependent nonlinear accounting left
is the finite small-scale prefix `m<t`, and the same is true for the adjacent
over-dithered side of a gap-one menu.

These are random-line baselines, not worst-case M1 bounds. Their purpose is to
turn the quotient/remainder support-profile formulas into certificate-sized
quantities: once quotient-periodic and one-remainder packets are isolated, a
future M1 proof or scanner can charge their missing-slope contribution through
`M` and `R_A(t,q)` instead of the full Johnson-sphere high-overlap term.

## Status

PROVED.

This is a finite combinatorial support-profile theorem. It does not prove the
M1 residue-line local limit; it supplies the exact overlap ledger for the
quotient-periodic support family that the local-limit problem must separate.

## Proof

Every support in `A_QP` is determined uniquely by a quotient index set
`I subset {1,...,N}` of size `L`. Thus `|A_QP| = binom(N,L)`.

Fix one support

```text
S_I = union_{i in I} B_i.
```

A second support `S_J` differs from `S_I` by exactly `h` quotient fibers if and
only if

```text
|I \ J| = |J \ I| = h.
```

For fixed `I`, the number of such `J` is

```text
binom(L,h) binom(N-L,h),
```

because one chooses the `h` fibers to remove from `I` and the `h` fibers to add
from the complement of `I`. Since every fiber has size `m`,

```text
|S_I \ S_J| = |S_J \ S_I| = hm,

|S_I cap S_J| = (L-h)m = s - hm.
```

Summing over all `binom(N,L)` choices of `I` gives the weighted identity

```text
sum_{S,T in A_QP} w(|S \ T|)
  = binom(N,L) * sum_h binom(L,h) binom(N-L,h) w(hm).
```

Taking `w` to be the indicator of one exchange size `j` gives the displayed
formula for `Delta_j(A_QP)` after deleting the `h=0` diagonal. Maximizing over
the starting support `S_I` gives the same count without the leading
`binom(N,L)`, which is the formula for `Gamma_j(A_QP)`.

For the M1 strict-overlap range, write `s = k+t`. A pair contributes to strict
high-overlap exactly when

```text
|S cap T| > k
  <=> s - |S \ T| > s - t
  <=> |S \ T| < t.
```

For quotient-periodic supports, `|S \ T| = hm`, so the only possible strict
high-overlap exchange sizes satisfy `1 <= hm <= t-1`. Substituting the formula
for `Gamma_{hm}(A_QP)` into a weighted sum with weights `q^(t-hm)` gives
`R_QP(t,q)`, and multiplying by `|A_QP| = binom(N,L)` gives the ordered-pair
version. The prefix form follows by writing the condition `hm <= t-1` as
`h <= floor((t-1)/m)`. If `m < t <= 2m`, this prefix contains only `h = 1`,
which gives `R_QP(t,q) = L(N-L)q^(t-m)`.

Finally, at exact support size `s`, a support that is a union of whole fibers
has size `Lm` for some integer `L`. Thus no such exact-support family exists
unless `m | s`; when it exists, `L = s/m`. The strict-overlap assertion is then
the preceding `hm < t` condition. If `t <= m`, no positive multiple of `m` is
less than `t`, so the strict-overlap profile is empty.

For the dyadic dither rule, `m=2^u <= k0=2^(nu-b)` implies `m | k0`. Since
`s=k0+(t-r)`, the condition `m | s` is therefore equivalent to `m | (t-r)`.
The strict-overlap condition is still `m <= t-1` for the first possible
one-fiber exchange. If `r=t-1`, then `t-r=1`, which has no nontrivial dyadic
divisor. Hence no nontrivial dyadic whole-fiber family at scale `m <= k0`
exists at the exact support size.

The valuation refinement is the same divisibility condition written explicitly:
for nonzero `d=t-r`, a dyadic scale `m=2^u` divides `d` exactly when
`u <= v2(|d|)`. The strict-overlap and size restrictions add the cap
`u <= floor(log2 Mmax)`. If `d=0`, every dyadic scale divides `d`, so only the
cap remains.

For the adjacent-slack obstruction, specialize this divisibility test to
`m=2`. Since `k0 >= 2`, the scale is present in the dyadic divisor ladder, and
since `u >= 3`, the first exchange size `2` lies in the strict range
`2 <= u-1`. The only remaining exact-support condition is parity:

```text
2 | s_u    <=>    2 | (u-r).
```

The interior hypothesis `2 <= s_u <= n-2` makes this a nondegenerate quotient
family, with `1 <= L=s_u/2 <= N-1`; hence the `h=1` codegree is
`L(N-L)=s_u(n-s_u)/4`. Consecutive integers have opposite parity, so exactly
one of `t-r` and `t+1-r` is even. The interval count follows by counting one
parity class in an integer interval.

The fixed-dither slack-window ledger is the same argument without specializing
to `m=2`. Since `m | k0`, exact support at slack `u` is equivalent to

```text
m | s_u    <=>    m | (u-r)    <=>    u == r mod m.
```

The assumption `u >= m+1` puts the one-fiber exchange `h=1` inside the strict
range, because `m <= u-1`. The endpoint condition `m <= s_u <= n-m` is exactly
`1 <= L=s_u/m <= N-1`, so the quotient family has both selected and unselected
fibers. Thus the `h=1` codegree is

```text
binom(L,1) binom(N-L,1) = L(N-L) = s_u(n-s_u)/m^2.
```

Counting active slacks is now just counting one residue class modulo `m` in an
integer interval. Each complete block of `m` consecutive eligible slacks
contains exactly one representative of that class, and an incomplete block
contains either zero or one, giving the displayed `floor/ceil` count. The set
`L_win(r)` is obtained by applying this criterion simultaneously over all
dyadic divisors `m` of `k0`.

For the general fiber-occupancy profile, first note that the group permuting
fibers and permuting points inside each fiber is transitive on `A_h`.  Thus the
fixed-support enumerator is independent of the chosen `S in A_h`.  For one
fiber with old occupancy `a` and new occupancy `b`, if the two within-fiber
subsets overlap in `x` points, then the contribution to `|S\T|` is `a-x`, and
the number of choices is

```text
binom(a,x) binom(m-a,b-x).
```

Summing over feasible `x` gives `P_{a,b}(y)`.  The auxiliary variable `z_b`
records that the target support `T` uses occupancy `b` on that fiber.  For the
`h_a` old fibers of occupancy `a`, the independent contribution is therefore

```text
(sum_b z_b P_{a,b}(y))^h_a.
```

Multiplying over all `a` and extracting the coefficient of
`z_0^h_0 ... z_m^h_m` enforces that `T` has the same occupancy histogram as
`S`.  This proves the displayed formula for `H_h(y)`.  The formula for
`|A_h|` is obtained independently by first assigning the occupancy values to
the `N` fibers and then choosing an `a`-subset inside each occupancy-`a` fiber.
The `Gamma_j`, `Delta_j`, and `R_h(t,q)` formulas then follow exactly as in
the whole-fiber case.

The histogram-enumeration corollary follows because every support has exactly
one occupancy histogram relative to the fixed quotient partition. Thus the
families `A_h` are disjoint and their union is the full support layer
`|S|=s`; summing the already proved formula for `|A_h|` over all feasible
histograms gives `binom(Nm,s)`.

The cross-histogram formula is the same argument with a different target
histogram.  Starting from a fixed `S in A_h`, the old fibers still contribute

```text
(sum_b z_b P_{a,b}(y))^h_a
```

for old occupancy `a`, but now extracting
`z_0^g_0 ... z_m^g_m` enforces that the target support lies in `A_g`. This
proves `H_{h->g}` and the ordered cross-pair formula. For a union `A_U`, every
target support lies in exactly one `A_g`, so fixed-source codegrees add over
`g in U`; maximizing over the source histogram gives `Gamma_j(A_U)`, and
summing source counts gives `Delta_j(A_U)`.
If `U` contains all support-size-`s` histograms, then `A_U` is simply the full
Johnson layer of `s`-subsets of `D`; the displayed Johnson formulas follow by
choosing `j` points to delete from a fixed support and `j` points to insert
from its complement.

For the one-remainder-fiber profile, fix

```text
S = (I,p,R),
```

where `I` is the set of whole fibers, `p` is the remainder fiber, and
`R subset B_p` has size `r`. Count a second support `T=(J,q,R')` by the
location of its remainder fiber `q`.

If `q=p`, then `J` is obtained from `I` by exchanging `h` whole fibers inside
the `N-1` fibers other than `p`, and `R'` differs from `R` by `l` points inside
`B_p`. This gives the product term

```text
binom(L,h) binom(N-L-1,h) binom(r,l) binom(m-r,l) y^(hm+l).
```

If `q in I`, choose the old whole fiber `q` in `L` ways. Either `p in J`, in
which case `q` contributes `m-r` points to `S\T` and the other whole-fiber
exchange contributes `hm`; or `p notin J`, in which case the old remainder
fiber `p` contributes `r` more points and the exponent becomes `(h+1)m`. These
are the two middle sums. In both cases the `r` points of `T` inside `B_q` may
be chosen arbitrarily, giving the factor `binom(m,r)`.

If `q` is outside `I union {p}`, choose it in `N-L-1` ways. If `p in J`, then
one added whole fiber has been spent on `p`, so at least one original whole
fiber is removed and the exponent is `hm`. If `p notin J`, the old remainder
fiber contributes `r` points, giving exponent `hm+r`. These are the final two
sums. Again the subset `R' subset B_q` is arbitrary and contributes
`binom(m,r)`. The six disjoint cases exhaust all possible remainder-fiber
positions, so the displayed `H_REM` is exact. Transitivity of the fiber and
within-fiber permutation action makes the fixed-support enumerator independent
of `S`; hence `Gamma_j` is the coefficient of `H_REM`, and multiplying by
`|A_REM|` gives the ordered-pair count `Delta_j`.

For the large-fiber truncation, write the remainder size as `b` and assume
`t <= m`. In the strict range `j<t`, every term of `H_REM` with a positive
whole-fiber exchange is absent, because its exponent is at least `m`.

In the same-remainder-fiber product, this leaves only `h=0` and
`1 <= ell <= min(b,m-b,t-1)`, giving

```text
binom(b,ell) binom(m-b,ell) y^ell.
```

In the two cases where the new remainder fiber lies in an old whole fiber,
only the subcase that promotes the old remainder fiber can contribute below
`m`; its exponent is `m-b` and its multiplicity is `L binom(m,b)`. This term
is strict exactly when `m-b<t`. The other subcase has exponent at least `m`.

In the two cases where the new remainder fiber lies outside `I union {p}`, only
the subcase with no whole-fiber exchange contributes below `m`; its exponent is
`b` and its multiplicity is `(N-L-1)binom(m,b)`. This term is strict exactly
when `b<t`. The remaining subcase has exponent at least `m`.

These are precisely the three displayed terms in `H_REM^{<t}`. Multiplying
each coefficient at exchange size `j` by `q^(t-j)` gives the displayed
weighted profile.

For the dyadic corollary, every dyadic `m | k0` also divides `s-d=k0`. Thus
`s=k0+d` has remainder `b=d` modulo `m` whenever `m>d`. The large-fiber formula
then applies for `t <= m`. If `d=1` and `m>t`, the only strict terms are

```text
(m-1)y      and      (N-L-1)m y.
```

Since `L=k0/m` and `N=n/m`, their coefficient sum is
`(N-L)m-1=n-k0-1`. If `m=t`, the boundary term
`L m y^(t-1)=k0 y^(t-1)` also enters.

For the stable large-scale hierarchy, the assumptions `m | k0` and `m>d` again
give remainder `b=d`. The stronger bound `m >= t+d` implies `m-d >= t`, so the
boundary promotion term with exponent `m-d` is not strict. It also implies
`m-d >= d`, so all same-remainder swaps with `1 <= ell <= d` appear. Substituting
`L=k0/m` and `N=n/m` into the large-fiber truncation gives the displayed
polynomial. Finally,

```text
sum_{ell=0}^d binom(d,ell) binom(m-d,ell) = binom(m,d)
```

by Vandermonde, because `m-d >= d`. Hence the same-remainder contribution at
`ell>=1` has total `binom(m,d)-1`, and adding the move-to-unused contribution
`((n-k0)/m-1)binom(m,d)` gives

```text
H_REM^{<t}(1) = ((n-k0)/m) binom(m,d) - 1.
```

The fixed-window obstruction is the specialization of the same formula. If
`r0=t0-1`, then at slack `t0+1` one has `d=2`. The stability condition becomes
`m >= (t0+1)+2 = t0+3`, and the stable mass is

```text
((n-k0)/m) binom(m,2) - 1 = (n-k0)(m-1)/2 - 1.
```

For any fixed dither and any slack with `d=t-r0 >= 2`, the displayed stable
hierarchy formula applies verbatim at scales `m >= t+d`; its leading behavior
in `m` is `(n-k0)m^(d-1)/d!`, which is no longer uniformly linear in
`n-k0`.

For the maximal-dither all-scale formula, specialize the one-remainder
enumerator to `b=1` and put `A=N-L-1`. The same-remainder-fiber factor is
`1+(m-1)y`. The terms with new remainder fiber outside `I union {p}` simplify
using

```text
A binom(A-1,h-1) = h binom(A,h),
A binom(A-1,h)   = (A-h) binom(A,h).
```

The terms with new remainder fiber in an old whole fiber simplify using

```text
L binom(L-1,h-1) = h binom(L,h).
```

After collecting equal exponents, the coefficients are:

```text
y^(hm+1):  binom(L,h) binom(A,h) (m(A-h+1)-1),
y^(hm):    binom(L,h) binom(A,h) (1+2mh)          for h>=1,
y^(hm-1):  mh binom(L,h) binom(A,h-1)             for h>=1.
```

Keeping exactly those exponents below `t` gives the displayed strict profile.
The dyadic maximal-dither reading follows because `m | k0` implies
`k0+1 = Lm+1` at every nontrivial dyadic scale.

## M1 Impact

This note turns one of the main structured exceptions in the M1 program into an
exact overlap ledger. The quotient-periodic support family is not random, but
its exchange profile, and hence its strict high-overlap profile after
restricting to `j < t`, is completely explicit:

```text
support size               Lm
family size                binom(N,L)
strict exchange sizes      hm < t
max codegree at hm         binom(L,h) binom(N-L,h).
```

Thus after a residue-line argument separates quotient-periodic supports from an
aperiodic family `A`, the quotient-periodic part can be accounted for exactly,
and the remaining M1 task is to prove that the aperiodic part has small
`Delta_j(A)` or `Gamma_j(A)` in the strict range `j < t`.

Two immediate readings are useful.

1. If `m` does not divide the exact support size `s = k+t`, this whole-fiber
   quotient-periodic support family is absent at that exact agreement size.
   This is the exact-support version of dimension/slack dithering.
2. If `t <= m`, quotient-periodic supports have no strict high-overlap pairs.
   In that regime they may still be an algebraic bad-slope source, but they do
   not create strict-overlap covariance in the random-line support-family
   ledger.
3. If `t > m`, all strict-overlap mass comes from whole-fiber exchanges. The
   correction term is the finite quotient prefix `R_QP(t,q)`, not a full
   Johnson-sphere sum over point exchanges. The first active band
   `m < t <= 2m` has only the one-fiber exchange contribution
   `L(N-L)q^(t-m)`.
4. At dyadic rates, dimension dither can eliminate all exact whole-fiber
   quotient-periodic scales in one step: for `k=k0-(t-1)`, every dyadic
   nontrivial fiber scale `m <= k0` fails the divisibility test `m | s`.
   More generally, the surviving dyadic scales are counted by the 2-adic
   valuation of `t-r`, capped at `min(k0,t-1)`.
5. This dither is necessarily a one-slack tool. For any fixed `r` and any
   adjacent slacks `t,t+1 >= 3`, scale `m=2` survives at exactly one of the
   two slacks, provided the scale-two support sizes are interior. Thus no
   single fixed dimension dither can globally remove dyadic whole-fiber
   quotient terms across a slack window. More generally, at dyadic scale `m`,
   active slacks are exactly one residue class modulo `m`; every eligible
   block of `m` consecutive slacks reactivates that quotient scale once. The
   resulting finite set `L_win(r)` is the exact first-exchange quotient ledger
   a parameter scanner must report for a fixed dither over a slack window.
6. If exact support has a nonzero remainder modulo a quotient fiber size, the
   one-remainder-fiber family has its own exchange profile `H_REM`. This
   smaller profile can create strict point exchanges below one full fiber and
   therefore must be budgeted separately from the whole-fiber quotient term.
   More generally, every fixed quotient-fiber occupancy histogram has an exact
   coefficient-extraction ledger `H_h`, so a scanner can account for all
   fiber-content classes before treating the residual obstruction as genuinely
   aperiodic.
7. In the large-fiber range `t <= m`, that remainder budget is itself explicit:
   only same-remainder swaps, moves to unused nonwhole fibers, and one boundary
   promotion term survive. Under maximal dyadic dither `k=k0-(t-1)`, every
   scale `m>t` has the same linear strict codegree `n-k0-1`, so the large
   quotient remainder packet becomes a tangent-sized term rather than a
   quotient-profile-sized term.
8. The stable large-scale hierarchy explains why maximal dither is the
   distinguished choice: if `d=t-r0` and `m >= t+d`, then the unweighted
   strict remainder mass is exactly `((n-k0)/m)binom(m,d)-1`. Thus `d=1` is the
   only stable dither class with a uniformly linear large-scale remainder
   budget. If a fixed dither is maximal at slack `t0`, the adjacent slack
   `t0+1` has `d=2` and large-scale mass `(n-k0)(m-1)/2-1`; fixed-window
   dithering therefore reintroduces a scale-dependent one-remainder
   obstruction even when whole-fiber scales are controlled. More generally,
   a fixed dither avoiding exact support `k0` over a slack window of length
   `L_W` has an endpoint stable tail of binomial degree at least `L_W` whenever
   the endpoint lies in the stable range. If one instead allows a finite menu
   of `C` dithers and chooses among them per slack without using exact support,
   some slack still has safe gap at least
   `D_C=min{D: L_W<=Cap(C,D)}`; bounded stable degree over long windows
   therefore requires a growing dither menu.
   Quantitatively, if a `C`-value menu keeps every slack within gap `D`, then
   at large dyadic scales it forces a stable one-remainder mass at least
   `min(k0/m,(n-k0)/m)binom(m,D_C)-1`, and a random-line weighted correction
   at least this mass times `q^(t_- - D)`. This floor has the exact binomial
   threshold
   `K_side binom(m-1,D_C-1) > D_C(n-k0)` for beating adaptive linear mass.
   At the standard rates, forced gap two first separates at dyadic scales
   `4, 8, 16, 32` for rates `1/2, 1/4, 1/8, 1/16`, respectively. Over an
   unbounded dyadic hierarchy, asymptotic adaptive competitiveness is
   equivalent to `D_C=1`, so the exact required menu size for a length-`L_W`
   window is the gap-one capacity inverse `C_ad(L_W)`. For weighted random-line
   budgets, the comparison against the whole adaptive window maximum pays the
   explicit extra factor `q^(L_W-1)` beyond the same-slack comparison. The
   gap-one construction realizes the converse: every stable tail is linear and,
   for `k0 <= n/2`, no larger than the adaptive same-slack baseline.
9. In the maximal-dither case, the one-remainder profile is explicit at every
   scale, not only at `m>=t`: the full strict profile is the three-band formula
   at exchange sizes `hm-1`, `hm`, and `hm+1`. This gives a closed-form
   all-scale quotient ledger for the dithered dimension `s=k0+1`. The adjacent
   over-dithered dimension `s=k0-1` has the complement-dual all-scale ledger,
   so a gap-one menu has exact quotient-remainder certificates on both sides
   of each served slack. Over an entire slack window, all nonlinear terms for
   such a menu are confined to the dyadic prefix `m <= t_+`. Equivalently, a
   finite menu is either in the gap-one finite-prefix regime or it forces a
   super-linear stable tail of degree `D_C>=2`.

This makes the quotient-periodic exception quantitatively separable from the
aperiodic local-limit problem targeted by M1.

## Suggested Next Step

For a concrete M1 scanner, label each support by its quotient-fiber content and
emit three statistics for each support class:

```text
|A|,    Delta_j(A),    Gamma_j(A)    for 1 <= j < t.
```

The general fiber-occupancy formula gives these statistics exactly for every
fixed quotient-fiber content histogram. Any excess strict-overlap profile after
these structured classes are isolated is then a direct witness for the
aperiodic obstruction that a future local-limit proof must control. The
cross-histogram formula also gives the exact union ledger for any chosen set of
content classes. The command

```bash
python3 experimental/m1_occupancy_profile_scan.py \
  --quotient-order 4 --fiber-size 3 --support-size 4 --slack 3 \
  --line-field-size 17
```

is the current experimental hook for this complete histogram-level report. For
dimension dithering across more than one target slack, the scanner should also
emit `L_win(r)` for each allowed dither and rank the surviving dyadic
first-exchange ledger terms.  The command
`python3 experimental/quotient_profile_dither.py --slack-window 1:16` is the
current experimental hook for this finite-window report; it also evaluates the
one-remainder strict codegree mass from `H_REM` for each nonzero support
remainder in the window. Supplying `--line-field-size q` additionally reports
the two-sided stable weighted correction `R_stable(t,r0,m,q)` for stable
large-scale one-remainder entries. The scanner also emits the fixed-window
minimax gap certificate, distinguishing the unconstrained center radius from
the larger no-exact-`k0` radius. Supplying `--target-stable-gap D` additionally
reports the exact finite-menu capacity threshold `Cap(C,D)`. Supplying
`--dither-menu-size C` turns this into a per-scale stable-tail mass lower bound
for a `C`-value menu; with `--line-field-size q`, it also reports the
corresponding weighted lower bound.
