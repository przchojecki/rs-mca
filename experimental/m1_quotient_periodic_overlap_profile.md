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

## Large-Fiber Remainder Truncation

The preceding formula becomes especially useful in the large-fiber range
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

Thus maximal dither has a closed random-line certificate at every dyadic
quotient-remainder scale.  The only scale-dependent nonlinear accounting left
is the finite small-scale prefix `m<t`.

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
   obstruction even when whole-fiber scales are controlled.
9. In the maximal-dither case, the one-remainder profile is explicit at every
   scale, not only at `m>=t`: the full strict profile is the three-band formula
   at exchange sizes `hm-1`, `hm`, and `hm+1`. This gives a closed-form
   all-scale quotient ledger for the dithered dimension `s=k0+1`.

This makes the quotient-periodic exception quantitatively separable from the
aperiodic local-limit problem targeted by M1.

## Suggested Next Step

For a concrete M1 scanner, label each support by its quotient-fiber content and
emit three statistics for each support class:

```text
|A|,    Delta_j(A),    Gamma_j(A)    for 1 <= j < t.
```

The quotient-periodic class should match the closed formulas above. Any excess
strict-overlap profile in the remaining supports is then a direct witness for
the aperiodic obstruction that a future local-limit proof must control.  For
dimension dithering across more than one target slack, the scanner should also
emit `L_win(r)` for each allowed dither and rank the surviving dyadic
first-exchange ledger terms.  The command
`python3 experimental/quotient_profile_dither.py --slack-window 1:16` is the
current experimental hook for this finite-window report; it also evaluates the
one-remainder strict codegree mass from `H_REM` for each nonzero support
remainder in the window.
