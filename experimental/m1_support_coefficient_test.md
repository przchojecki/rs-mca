# M1 Support Coefficient Test for Residue-Line Packing

## Claim

Let `C = RS[F,D,k]`, let `S subset D` have size `s > k`, and put
`t = s - k`. For a word `v:D -> F`, let `I_S(v)` be the unique polynomial of
degree `< s` agreeing with `v` on `S`. Define the top-coefficient obstruction

```text
Pi_S(v) = (coeff_X^k I_S(v), ..., coeff_X^(s-1) I_S(v)) in F^t.
```

Then `v|S` is explained by a codeword of `C` if and only if `Pi_S(v) = 0`.
For a line `u_z = f + z g`, a support `S` witnesses that `z` is
support-wise MCA-bad if and only if

```text
Pi_S(f) + z Pi_S(g) = 0
```

and not both `Pi_S(f)` and `Pi_S(g)` vanish. Equivalently:

- if `Pi_S(g) = 0`, then `S` contributes no bad slope;
- if `Pi_S(g) != 0`, then `S` contributes exactly one bad slope precisely when
  `Pi_S(f)` lies in the one-dimensional span of `Pi_S(g)`;
- in that case, if `Pi_S(f) = lambda Pi_S(g)`, the bad slope is `z = -lambda`.

Thus arbitrary-line MCA at fixed agreement size is exactly a collinearity
problem among the support top-coefficient vectors.

## Status

PROVED as a local finite-dimensional lemma. This does not prove the final M1
residue-line local limit; it isolates the exact support invariant that such a
proof or scanner has to control.

## Proof

The first assertion is just interpolation. Since `I_S(v)` is the unique
degree-`< s` interpolant on `S`, the restriction `v|S` agrees with a
degree-`< k` polynomial if and only if all coefficients in degrees
`k, ..., s-1` of `I_S(v)` vanish, i.e. if and only if `Pi_S(v) = 0`.

Linearity of interpolation gives

```text
I_S(f + z g) = I_S(f) + z I_S(g),
```

so

```text
Pi_S(f + z g) = Pi_S(f) + z Pi_S(g).
```

The line point `f + z g` is code-explained on `S` exactly when this vector is
zero. The support-wise MCA noncontainment condition says that there are not
two codewords explaining `f` and `g` separately on `S`, which is exactly the
condition that `Pi_S(f)` and `Pi_S(g)` are not both zero.

The three cases now follow from solving one vector equation in the scalar `z`.
If `Pi_S(g) = 0`, then either `Pi_S(f) = 0`, in which case the line is
explained on `S` for every `z` but the noncontainment condition fails, or
`Pi_S(f) != 0`, in which case no `z` solves the equation. If `Pi_S(g) != 0`,
there is a solution exactly when `Pi_S(f)` is a scalar multiple of `Pi_S(g)`,
and the scalar gives the unique bad slope.

This also recovers Paper B's one-bad-parameter-per-support theorem for
Reed-Solomon codes: a fixed support contributes at most one slope.

## Exact Minimal-Support Reduction

For a radius `delta < 1 - k/n`, put

```text
s_delta = ceil((1 - delta) n).
```

Then `s_delta > k`, and every support-wise MCA-bad slope has a witness of
exactly `s_delta` points.

Indeed, suppose `z` is witnessed by `S` with `|S| >= s_delta`. The line point
is code-explained on every subset of `S`. Since `f` and `g` are not both
code-explained on `S`, at least one of them, say `v`, is not degree-`< k` on
`S`. Hence some `(k+1)`-subset `T subset S` is not degree-`< k` for `v`;
otherwise every `(k+1)`-subset would lie on a degree-`< k` polynomial, forcing
all of `v|S` to do so: fix any `k` points, interpolate the unique degree-`< k`
polynomial through them, and add each remaining point one at a time. Extend `T`
inside `S` to a set `S0` of size `s_delta`. Then `f + z g` is still
code-explained on `S0`, while `f` and `g` are still not both code-explained
there. Thus `S0` is a witness of exact size `s_delta`.

Consequently the bad-slope set of a fixed line at radius `delta` is exactly

```text
Union over |S| = s_delta of
{ -lambda : Pi_S(g) != 0 and Pi_S(f) = lambda Pi_S(g) }.
```

This gives a finite scanner target with no larger-support ambiguity.

## Quotient-Occupancy Incidence Decomposition

Suppose now that the domain is partitioned into quotient fibers

```text
D = B_1 disjoint union ... disjoint union B_N,        |B_i|=m.
```

For exact support size `s`, let `A_h` be the supports with quotient-fiber
occupancy histogram `h=(h_0,...,h_m)`, as in
`experimental/m1_quotient_periodic_overlap_profile.md`.  For fixed line data
`f,g`, define

```text
Inc_h(f,g) = {
  (S,z) : S in A_h, Pi_S(f)+z Pi_S(g)=0,
          Pi_S(f),Pi_S(g) not both zero
}.
```

Then the exact-support incidence set decomposes as the disjoint union

```text
Inc_s(f,g) = disjoint union_h Inc_h(f,g),
```

where `h` ranges over all histograms with

```text
sum_a h_a=N,        sum_a a h_a=s.
```

Moreover each support contributes to at most one slope, namely
`z=-lambda` when `Pi_S(f)=lambda Pi_S(g)` and `Pi_S(g) != 0`. Thus a finite
scanner can label every exact-support incidence by quotient-fiber occupancy,
compare the observed support count in each class with the closed formula for
`|A_h|`, and pair the incidence data with the structured overlap ledger
`H_h(y)` from the quotient-profile note.

The proof is only bookkeeping. Every exact support has a unique occupancy
histogram, so the sets `A_h` partition the layer `|S|=s`. Applying the
support-coefficient criterion support by support gives the displayed incidence
partition and the one-slope-per-support assertion.

## Recovery of the Canonical Slack Formula

Take the canonical slack line from Paper B,

```text
u_z = X^(k+T) + z X^k,
```

and a support `S` of size `s = k + T`. Let

```text
L_S(X) = product_{x in S} (X - x)
       = X^s - e_1(S) X^(s-1) + ... + (-1)^T e_T(S) X^k + lower terms.
```

Modulo `L_S`, the top coefficients of `X^s + z X^k` are zero exactly when

```text
e_1(S) = ... = e_(T-1)(S) = 0,
z = (-1)^T e_T(S).
```

Thus the support coefficient test recovers the exact multi-symmetric image
`B_T(D,k)` in Paper B's slack characterization. The general arbitrary-line
case replaces this special elementary-symmetric vector by the pair
`Pi_S(f), Pi_S(g)`.

## Canonical Quotient-Core Factorization

The canonical elementary-symmetric test interacts cleanly with quotient
fibers. Suppose the domain is partitioned into fibers

```text
B_i = {x in D : x^m = y_i},
```

so each whole fiber has vanishing polynomial `X^m-y_i`.  For a support `S`,
let `W(S)` be the union of the whole fibers contained in `S`, and let

```text
R(S) = S \ W(S)
```

be the residual partial-fiber set. Then

```text
L_S(X) = L_{W(S)}(X) L_{R(S)}(X),
L_{W(S)}(X) = product_{B_i subset S} (X^m-y_i) in F[X^m].
```

Since `L_{W(S)}` has no terms whose degree deficit is strictly between `1`
and `m-1`, the low elementary-symmetric coefficients are invisible to the
whole quotient core:

```text
e_d(S) = e_d(R(S))        for 1 <= d < m.
```

Consequently, for the canonical slack line `X^(k+T)+zX^k` with `T <= m`, an
exact support `S` contributes a bad slope if and only if

```text
e_1(R(S)) = ... = e_(T-1)(R(S)) = 0.
```

The slope is still

```text
z = (-1)^T e_T(S).
```

If `T < m`, the whole quotient core also disappears from the slope:

```text
z = (-1)^T e_T(R(S)).
```

At the boundary `T=m`, write

```text
Y_W = { y_i : B_i subset S }.
```

Then the coefficient at degree deficit `m` in
`L_{W(S)}(X)L_{R(S)}(X)` gives the exact slope decomposition

```text
z = (-1)^m e_m(R(S)) - sum_{y in Y_W} y.
```

Thus the quotient core affects the canonical slope only at the boundary
`T=m`, and it does so by a linear quotient-level term.

This is a useful separation. Whole-fiber quotient structure automatically
satisfies the canonical zero-prefix equations, while dimension dither that
prevents exact whole-fiber supports leaves a residual partial-fiber
zero-prefix problem. For example, in the multiplicative-domain setting a
one-point residual set never satisfies `e_1(R)=0`, so maximal dither removes
the canonical quotient-locator incidence at every slack `T>=2` with `T<=m`;
the one-remainder overlap ledger remains relevant for arbitrary or random
line data, but it is not itself a canonical quotient-locator source in this
range.

This residual problem has an exact low-weight cutoff. Assume `D subset F^*`,
put `b=|R(S)|`, and keep `T<=m`. If

```text
0 < b < T,
```

then `S` cannot contribute to the canonical slack line. Indeed, the zero-prefix
condition on `R(S)` would include `e_b(R(S))=0`, but

```text
e_b(R(S)) = product_{x in R(S)} x != 0.
```

At the boundary `b=T`, the residual zero-prefix condition is also completely
rigid:

```text
e_1(R)=...=e_(T-1)(R)=0
```

if and only if the residual vanishing polynomial has the form

```text
L_R(X) = X^T - c,
```

equivalently all residual points have the same `T`-th power. Thus a boundary
residual contribution is exactly a full root set of `X^T-c` inside the
multiplicative domain, and for `T<m` its slope is `z=-c`. If `T=m`, such a
residual set would be a whole quotient fiber and hence is absorbed into
`W(S)`, so no nonempty residual boundary case remains.

In a cyclic multiplicative domain `D` of order `n`, the boundary case has an
exact quotient-fiber count. The map

```text
x -> x^T
```

has fibers of size `gcd(T,n)`. Therefore a residual boundary set of size `T`
exists if and only if `T | n`, and then it is one of the `n/T` cosets of the
unique subgroup of `D` of size `T`. Relative to the quotient fibers of size
`m`, such a coset touches exactly

```text
T / gcd(T,m)
```

quotient fibers, with `gcd(T,m)` points in each touched fiber. Hence, for
`T<m` and exact support size

```text
s = Lm + T,
```

the number of exact supports whose residual partial-fiber set is a canonical
boundary coset is

```text
1_{T | n} * (n/T) * binom(N - T/gcd(T,m), L),
```

where `N=n/m`. If `s` is not congruent to `T` modulo `m`, or if `T=m`, this
boundary residual count is zero.

Thus the first residual canonical obstruction after low-residual dither is not
an arbitrary support family. It is a finite quotient-level menu of power-kernel
cosets together with ordinary whole-fiber choices disjoint from the touched
fibers.

There is also a useful residue-floor corollary. Let

```text
b = s mod m,        s=k+T,        0 <= b < m,
```

and keep `T<m`. Since `|R(S)| == b mod m`, the low-weight cutoff implies:

- if `0 < b < T`, then every canonical support has
  `|R(S)| >= m+b`;
- if `b=T`, then the only residual supports below `m+T` are exactly the
  boundary cosets counted above;
- if `b=1`, as in maximal one-step dimension dither at large dyadic scales,
  every canonical residual support has at least `m+1` residual points.

Thus a dithered support residue in the range `1,...,T-1` removes all
canonical small-residual packets. Any remaining canonical incidence at that
scale must involve a residual set larger than one full quotient fiber, so it
belongs to the genuinely residual/aperiodic part rather than to the
one-remainder quotient exception.

The slope image of this boundary family is exact as well. For `T<m`, the
boundary residual coset has vanishing polynomial `X^T-c`, hence slope `z=-c`.
As the residual coset varies through `D`, the values of `c` are exactly

```text
D^T = {x^T : x in D},
```

so the boundary residual slope set is `-D^T` and has size `n/T` when `T|n`.
Moreover, at support size `s=Lm+T`, each such boundary slope has exactly

```text
binom(N - T/gcd(T,m), L)
```

support witnesses: choose the `L` whole quotient fibers from those not touched
by the residual coset. Thus both the support count and the bad-slope count of
the boundary residual canonical source are closed quotient-level quantities.

Combining the preceding statements gives an exact small-residual ledger for
support residues `b <= T`. In the large-fiber range `T<m`, among supports with
`|R(S)|<m`:

```text
b=0:
  only whole-fiber supports occur; the canonical slope set is {0},
  with support multiplicity binom(N,L).

0<b<T:
  no canonical small-residual supports occur.

b=T:
  the only canonical small-residual supports are the boundary power cosets;
  the slope set is -D^T and each slope has multiplicity
  binom(N - T/gcd(T,m), L), when T|n.
```

The first unclassified small-residual residue is therefore `b>T`, where the
residual zero-prefix equations may still have genuinely partial-fiber
solutions. This is the point at which the canonical problem stops being a
quotient-core or boundary-coset ledger and becomes a residual local-limit
question.

The remaining canonical problem has an exact residual-packet lift
factorization. Keep `T<m` and fix support size `s`. Let `P` be any subset of
`D` which contains no whole quotient fiber. Write

```text
r=|P|,        tau(P)=#{quotient fibers touched by P}.
```

If `P` satisfies

```text
e_1(P)=...=e_(T-1)(P)=0
```

and `s-r` is divisible by `m`, then the exact supports whose residual
partial-fiber set is exactly `P` are obtained by adjoining

```text
a=(s-r)/m
```

whole quotient fibers disjoint from the `tau(P)` fibers already touched by
`P`. Hence this packet has exactly

```text
binom(N-tau(P), a)
```

canonical support lifts, with the convention that the binomial is zero if
`a<0` or `a>N-tau(P)`. Every one of these lifts has the same canonical slope

```text
z=(-1)^T e_T(P).
```

Thus, for `T<m`, the canonical bad-slope multiset at exact support size `s`
is the weighted image of the residual packet catalog

```text
{ P subset D : P has no whole quotient fiber,
               e_1(P)=...=e_(T-1)(P)=0,
               |P| congruent s mod m }
```

under the map `P -> (-1)^T e_T(P)`, with packet weight
`binom(N-tau(P), (s-|P|)/m)`.

The proof is the quotient-core factorization applied in reverse. Because
`T<m`, adjoining or deleting whole quotient fibers does not change
`e_1,...,e_T`; hence the zero-prefix test and slope are determined by `P`
alone. If a support has residual packet `P`, all remaining selected points
must be whole quotient fibers outside the fibers touched by `P`, and the
number of such fibers is forced to be `a=(s-|P|)/m`. Conversely, adjoining
any such `a` whole fibers gives an exact support of size `s` with residual
packet `P`. This proves both the binomial lift count and the common slope.

Consequently the small-residual superboundary depths have an exact dither
gate. Write a small residual size as

```text
|P| = T+d,        1 <= d < m-T.
```

Since `s=k+T`, this depth can lift at quotient scale `m` only if

```text
m | (s-|P|) = k-d.
```

Equivalently, when the quotient-scale hierarchy has `m | k0` and dimension
dither `k=k0-r`, depth `d` is active only if

```text
m | (r+d).
```

Thus all depths `1<=d<=D` are absent at every scale `m>r+D` dividing `k0`.
In particular, for any positive dither `1<=r<=T-1`, all small-residual
superboundary layers are absent at every scale `m>T` dividing `k0`; the
support residue is then `T-r`, which lies below the boundary size `T`. The
maximal dither `r=T-1` gives residue `1`, hence the residual-size floor is
`m+1` rather than any size below one full quotient fiber.

Equivalently, the local quotient-scale condition

```text
b=(k+T) mod m,        0<b<T,
```

is an immediate certificate that the canonical small-residual catalog is
empty below one quotient fiber. Every canonical zero-prefix support then has

```text
|R(S)| >= m+b.
```

This is the large-scale positive-dither clearance statement used by the M1
strategy: for such scales the boundary, first-superboundary, and every other
small-residual superboundary depth are already deleted by exact support
congruence, so no shape-count or sparse-trinomial estimate is needed there.

As a finite-prefix corollary, fix an exact dimension `k0` and a positive
dither

```text
k=k0-r,        1<=r<=T-1.
```

At every quotient scale `m>T` with `m | k0`, one has

```text
(k+T) mod m = T-r,
```

so the local clearance criterion applies. Therefore the entire canonical
small-residual catalog below one quotient fiber is absent at every such
large scale, and only quotient scales `m<=T` can require a small-residual
boundary or superboundary analysis. In a dyadic hierarchy of nontrivial fiber
sizes this leaves at most `floor(log2(T))` scales, namely
`2,4,...,2^floor(log2(T))`. All larger dyadic scales have residual-size floor
`m+T-r`.

This does not classify the first superboundary packets `T<|P|<m`. It proves
that they are the only new object left: once such a packet is known, the
quotient-core lift and slope multiplicity are completely deterministic.

The zero-slope part of the first superboundary is also exact. Assume
`T+1<m` and let `P` be a residual packet of size `T+1` satisfying
`e_1(P)=...=e_(T-1)(P)=0`. Its vanishing polynomial has the sparse form

```text
L_P(X)=X^(T+1)+zX-c,
```

where

```text
z=(-1)^T e_T(P),        c=(-1)^T e_(T+1)(P).
```

Therefore `z=0` if and only if

```text
L_P(X)=X^(T+1)-c,
```

equivalently all points of `P` have the same `(T+1)`-st power. In a cyclic
multiplicative domain `D` of order `n`, such zero-slope first-superboundary
packets exist if and only if `T+1 | n`; then they are exactly the `n/(T+1)`
cosets of the subgroup of `D` of size `T+1`. Each such packet touches

```text
(T+1)/gcd(T+1,m)
```

quotient fibers. Hence, at exact support size

```text
s=Lm+T+1,
```

the zero-slope first-superboundary support count is

```text
1_{T+1 | n} * (n/(T+1))
  * binom(N - (T+1)/gcd(T+1,m), L).
```

All other first-superboundary packets are precisely the nonzero-slope
`D`-split trinomials `X^(T+1)+zX-c` with `z != 0`. This gives a clean first
fork in the superboundary problem: the zero-slope component remains a counted
power-coset ledger, while the nonzero component is the genuinely new sparse
trinomial/additive residual source.

The whole first-superboundary layer has a uniform shape-coset reduction.
Assume `T+1<m` and define

```text
C_T(D) = { (u_1,...,u_T) in D^T :
           1,u_1,...,u_T are distinct,
           e_j(1,u_1,...,u_T)=0 for 1<=j<T }.
```

For `u=(u_1,...,u_T)` put

```text
a_T(u)=(-1)^T e_T(1,u_1,...,u_T),
tau(u)=#{quotient fibers met by {1,u_1,...,u_T}}.
```

At exact support size `s=Lm+T+1`, the full lifted first-superboundary slope
multiset is

```text
M_T(z) = (1/(T+1)!) sum_{u in C_T(D)}
         binom(N-tau(u), L) * #{x in D : x^T a_T(u)=z}.
```

The proof is just normalization of residual packets. Every packet `P` of size
`T+1` has `T+1` choices of base point and `T!` orderings of the remaining
points; after scaling the base point to `1`, the zero-prefix equations are
exactly the defining equations of `C_T(D)`. Conversely, every pair
`(x,u) in D x C_T(D)` gives the packet
`x{1,u_1,...,u_T}`. Scaling by `x` multiplies the slope by `x^T`, while the
whole-fiber lift count is again determined only by the touched quotient
fibers. Hence the nonzero slope image is a union of cosets `a_T(u)D^T`, with
the zero-slope subcatalog equal to the power-coset family above.

This gives a direct bad-slope budget at every first-superboundary slack. Let
`C_T^act(D)` be the normalized shapes with nonzero exact-support lift count,
and let `Z_T^act` be the active shapes with `a_T(u)=0`. Then the exact
coset-compressed slope count is

```text
1_{Z_T^act nonempty}
  + #{nonzero cosets hit by a_T(C_T^act) in F^*/D^T} * |D^T|.
```

In particular,

```text
|Bad_{|P|=T+1}|
  <= min(|F|,
         1_{Z_T^act nonempty}
         + ((|C_T^act|-|Z_T^act|)/(T+1)!) * |D^T|).
```

The quotient by `(T+1)!` is legitimate because the active condition,
nonzero slope status, and the coset `a_T(u)D^T` are invariant under choosing
a different base point and ordering of the same residual packet. Moreover a
nonzero-slope normalized packet has trivial multiplicative stabilizer: if
`lambda P=P`, then its sparse polynomial
`X^(T+1)+zX-c` satisfies `lambda^(T+1)=1` from the constant term and
`z lambda=z` from the `X` term, so `z!=0` forces `lambda=1`. Zero-slope
shapes may have stabilizer, but they contribute only the single slope `0`.
For `T=2` this recovers the square-coset slope bound below.

The same normalization gives a uniform second-superboundary interface. Assume
`T+2<m` and define

```text
C_T^(2)(D) = { (u_1,...,u_(T+1)) in D^(T+1) :
               1,u_1,...,u_(T+1) are distinct,
               e_j(1,u_1,...,u_(T+1))=0 for 1<=j<T }.
```

For `u in C_T^(2)(D)` put

```text
b_T(u)=(-1)^T e_T(1,u_1,...,u_(T+1)),
tau(u)=#{quotient fibers met by {1,u_1,...,u_(T+1)}}.
```

At exact support size `s=Lm+T+2`, the depth-two residual-packet slope
multiset is

```text
M_T^(2)(z) = (1/(T+2)!) sum_{u in C_T^(2)(D)}
             binom(N-tau(u), L) * #{x in D : x^T b_T(u)=z}.
```

Indeed, every packet of size `T+2` has `T+2` choices of base point and
`(T+1)!` orderings after normalization. Scaling by `x` multiplies
`e_T` by `x^T`, while the quotient-core lift weight is again determined only
by the touched fibers. Hence the nonzero depth-two slope image is a union of
cosets `b_T(u)D^T`.

The zero-slope slice of this depth-two catalog is exactly the
first-superboundary shape catalog for the next slack:

```text
b_T(u)=0
  <=> e_1=...=e_T=0 on {1,u_1,...,u_(T+1)}
  <=> u in C_(T+1)(D).
```

Thus the low-slack residual-packet problem has a genuine hierarchy: the
transition locus from depth two at slack `T` is the depth-one shape problem
at slack `T+1`. Its exact-support lift gate is also uniform,

```text
m | (s-(T+2)) = k-2.
```

If the gate is closed, the whole second-superboundary catalog is absent at
that quotient scale before any shape-count estimate is needed.

There is a fixed-support way to read the same statement. Since

```text
k+T = (k-1)+(T+1),
```

the zero-slope second-superboundary residual packets for `(T,k)` at exact
support size `s=k+T` are exactly the first-superboundary residual packets for
`(T+1,k-1)` at the same exact support size. The lift congruence is the same
in both views:

```text
m | k-2.
```

Only the slope label changes: the family contributes slope `0` to the
slack-`T` depth-two catalog, while in the slack-`T+1` first-superboundary
catalog its slope is governed by `(-1)^(T+1)e_(T+1)`.

This is the first case of a general residual-depth shift. For any depth
`d>=1` with `T+d<m`, define

```text
C_T^(d)(D) = { (u_1,...,u_(T+d-1)) in D^(T+d-1) :
               1,u_1,...,u_(T+d-1) are distinct,
               e_j(1,u_1,...,u_(T+d-1))=0 for 1<=j<T }.
```

For `u in C_T^(d)(D)` put

```text
c_T,d(u)=(-1)^T e_T(1,u_1,...,u_(T+d-1)),
tau(u)=#{quotient fibers met by {1,u_1,...,u_(T+d-1)}}.
```

At exact support size `s=Lm+T+d`, the depth-`d` residual-packet slope
multiset is

```text
M_T^(d)(z) = (1/(T+d)!) sum_{u in C_T^(d)(D)}
             binom(N-tau(u), L) * #{x in D : x^T c_T,d(u)=z}.
```

For the canonical exact layer `s=k+T`, the lift gate is

```text
m | (s-(T+d)) = k-d.
```

Moreover, for `d>=2`, the zero-slope subcatalog satisfies

```text
c_T,d(u)=0
  <=> u in C_(T+1)^(d-1)(D).
```

At fixed exact support this is the dimension shift

```text
(T,k,d)  ->  (T+1,k-1,d-1).
```

Thus every zero-slope layer is not a new shape problem: it is the previous
residual-depth problem one slack higher. The genuinely new part at depth `d`
is the nonzero image of `c_T,d` modulo the power cosets `D^T`.

Iterating the shift gives a finite frontier description. A residual packet of
size `T+d` can have a chain of inherited zero slopes

```text
e_T=e_(T+1)=...=e_(T+j-1)=0
```

for `0<=j<d`. After `j` such zero steps, the same packet is viewed as a
depth-`d-j` packet at slack `T+j` and dimension `k-j`. If the zero chain
continues all the way to `j=d-1`, the packet lands in the first-superboundary
catalog at slack `T+d-1` and dimension `k-d+1`; its remaining zero-slope
subcatalog is the already counted `(T+d)`-power-coset family.

Therefore a residual-depth analysis can be organized by first nonzero
coefficient. The new frontier at depth `d` is not the whole catalog
`C_T^(d)(D)`, but the first nonzero image

```text
(-1)^(T+j) e_(T+j)
```

on the inherited zero stratum for some `0<=j<d`, modulo the corresponding
power cosets `D^(T+j)`. Pure zero chains contribute only the terminal
power-coset ledger. This is useful for M1 because it prevents lower-depth
zero strata from being counted again as new aperiodic residual structure.

Equivalently, there is an exact disjoint frontier partition. Put `h=T+d`.
For `0<=j<d`, define

```text
F_T,d^(j) = { P subset D : |P|=h,
              e_1(P)=...=e_(T+j-1)(P)=0,
              e_(T+j)(P) != 0 }.
```

Also define the terminal stratum

```text
F_T,d^(infty) = { P subset D : |P|=h,
                  e_1(P)=...=e_(h-1)(P)=0 }.
```

Then the residual-packet catalog `C_T^(d)(D)` is the disjoint union of the
`F_T,d^(j)` and `F_T,d^(infty)`. On `F_T,d^(j)`, after `j` residual-depth
shifts, the first nonzero slope is

```text
z_j(P)=(-1)^(T+j) e_(T+j)(P),
```

and scaling `P` by `x in D` sends `z_j` to `x^(T+j) z_j(P)`. Thus the
`j`-th frontier slope image is a union of `D^(T+j)`-cosets. At the original
slack `T`, only the `j=0` frontier contributes nonzero slopes; all
`j>0` frontiers and the terminal stratum are inherited zero-slope packets.
The lift gate is independent of `j`:

```text
m | s-h = k-d.
```

This partition is the useful bookkeeping for a depth-`d` attack: prove
coset-image bounds separately on the nonzero frontiers, then add the
terminal power-coset count below.

The terminal pure-zero ledger is explicit. Let `h=T+d<m`. A packet of size
`h` whose inherited zero chain reaches the terminal first-superboundary
zero-slope stratum satisfies

```text
e_1(P)=e_2(P)=...=e_(h-1)(P)=0.
```

Equivalently its vanishing polynomial is

```text
L_P(X)=X^h-c,
```

so all elements of `P` have the same `h`-th power. In a cyclic
multiplicative domain `D` of order `n`, such packets exist if and only if
`h|n`; then they are exactly the `n/h` cosets of the subgroup of size `h`.
At exact support size `s=k+T`, this terminal stratum is active only when

```text
m | s-h = k-d.
```

If active, each terminal packet touches

```text
h/gcd(h,m)
```

quotient fibers and has lift multiplicity

```text
binom(N - h/gcd(h,m), (k-d)/m).
```

Therefore the active terminal pure-zero support count at depth `d` is

```text
1_{h|n} * (n/h)
  * binom(N - h/gcd(h,m), (k-d)/m),
```

with the convention that the binomial term is zero when the lift gate is
closed or the requested number of whole fibers is outside
`[0, N-h/gcd(h,m)]`. This formula closes the inherited-zero side of the
residual-depth hierarchy: all remaining unclassified M1 content at depth
`d` lies on a first nonzero coefficient frontier, not in another zero-slope
subcatalog.

This formula has an immediate dither gate. Since the residual packet has size
`T+1` but the exact support size is `s=k+T`, a first-superboundary packet can
lift only if

```text
m | (s-(T+1)) = k-1.
```

If this divisibility fails, the whole first-superboundary shape catalog is
inactive at quotient scale `m`, regardless of how large `C_T(D)` is. If it
holds, then `L=(k-1)/m` in the displayed formula. Thus for a quotient-scale
hierarchy with base dimension `k0` divisible by `m` and dither
`k=k0-r`, the first-superboundary layer is active only at scales

```text
m | (r+1).
```

In particular, the maximal slack-`T` dither `k=k0-(T-1)` removes the
first-superboundary layer at every quotient scale `m>T` dividing `k0`. This
is the first low-superboundary analogue of the quotient-periodic dither
ledger: a dimension choice can delete the entire `|P|=T+1` residual catalog
from all growing quotient scales before any shape-count estimate is needed.

For slack `T=2`, this first-superboundary catalog has an exact unit-equation
normal form. Assume `3<m`. Put

```text
C_2(D) = { u in D : v=-1-u in D, 1,u,v are distinct }.
```

Every residual packet `P` of size three with `e_1(P)=0` can be written as

```text
P = x {1,u,-1-u},        x in D, u in C_2(D),
```

and the map `(x,u) -> P` is six-to-one: the six choices are exactly the
choice of a base point of `P` and an ordering of the two remaining points.
Consequently the packet count is

```text
|D| |C_2(D)| / 6.
```

For exact support size `s=Lm+3`, define

```text
alpha(u)=-(1+u+u^2),
tau(u)=#{quotient fibers met by {1,u,-1-u}}.
```

Then the full lifted slope multiset in the slack-two first superboundary has
multiplicity

```text
M(z) = (1/6) sum_{u in C_2(D)}
       binom(N-tau(u), L) * #{x in D : x^2 alpha(u)=z}.
```

This formula includes the zero-slope power-coset case: `alpha(u)=0` exactly
when `u` is a nontrivial cube root of unity. Thus the entire `T=2`, `|P|=3`
canonical residual source is reduced to the multiplicative unit equation
`u in D` and `-1-u in D`, plus the square-image map `x -> x^2` on `D`.

It also gives a direct slope-count bound. Let `C_2^act(D)` be the shapes in
`C_2(D)` with enough disjoint quotient fibers to lift to the target exact
support size, and let `Z_2^act` be the active shapes with `alpha(u)=0`. Since
the nonzero shapes occur in sixfold orbits and `D^2` has size
`|D|/gcd(2,|D|)`, the number of first-superboundary slack-two slopes is at
most

```text
1_{Z_2^act nonempty}
  + ((|C_2^act(D)|-|Z_2^act|)/6) * |D|/gcd(2,|D|),
```

capped by `|F|`. This is not an aperiodic local-limit theorem by itself, but
it converts the first nonzero canonical superboundary slope problem into two
explicit inputs: a unit-equation shape count and the square-coset overlap of
the values `alpha(u)`.

The square-coset overlap is itself exact, not merely a union bound. Put

```text
Q = D^2 = {x^2 : x in D},
A_2^act = { alpha(u)Q : u in C_2^act(D), alpha(u) != 0 }.
```

Because `Q` is a multiplicative subgroup, two nonzero sets
`alpha(u)Q` and `alpha(u')Q` are either equal or disjoint. Hence the
first-superboundary slack-two slope image has exact size

```text
1_{Z_2^act nonempty} + |A_2^act| |Q|.
```

Thus the only remaining loss in the square-coset step is the number of
distinct cosets hit by `alpha(C_2^act(D))`, not any uncontrolled overlap
inside those cosets.

For proper subgroups this coset image has its own character expansion. Let
`D <= F_p^*` have order `n`, index `e`, put `g=gcd(2,n)`,
`H=D^2`, and `h=[F_p^*:H]=eg`. Let `chi` have kernel `D`, let `psi` have
kernel `H`, and fix a nonzero coset `gamma H`. Define the raw coset count

```text
U_gamma^raw =
  #{ u in F_p : u in D, -1-u in D, alpha(u) in gamma H }.
```

With all multiplicative characters extended by zero at zero,

```text
U_gamma^raw =
  (1/(e^2 h)) sum_{a,b,c}
    psi^(-c)(gamma) S_{a,b,c},

S_{a,b,c} =
  sum_{u in F_p} chi^a(u) chi^b(-1-u) psi^c(alpha(u)),
```

where `0<=a,b<e` and `0<=c<h`. The principal term is

```text
S_{0,0,0} = p - 3 - chi_2(-3),
```

for `p>5`, where `chi_2` is the quadratic character. All nonprincipal terms
are mixed multiplicative character sums supported on the four-root divisor
`u(-1-u)alpha(u)`.

Consequently, using the standard Weil bound

```text
|S_{a,b,c}| <= 3 sqrt(p)        for nonprincipal (a,b,c),
```

gives the uniform lower estimate

```text
U_gamma^raw >= (p - 3 - chi_2(-3))/(e^2 h) - 3 sqrt(p).
```

The admissible shape set removes at most the three degenerate parameters
`u=1`, `u=-2`, and `u=-1/2`. Hence, if the right-hand side is greater than
`3`, every nonzero coset of `H=D^2` is hit by an admissible slack-two shape.
In the exact support layer `s=3`, where there is no quotient-core lift
filter, the slack-two first-superboundary image then contains every nonzero
field slope. This is the complementary small-index saturation regime to the
large-index non-field-filling threshold below.

This exact compression also explains why the full multiplicative domain is a
saturated obstruction rather than a promising non-field-filling case. Take
`D=F_p^*`, `p>5`, and write `chi` for the quadratic character. On the
admissible shape set `C_2(F_p^*)`, let

```text
A_+ = #{u in C_2 : chi(alpha(u))= 1},
A_- = #{u in C_2 : chi(alpha(u))=-1},
A_0 = #{u in C_2 : alpha(u)=0}.
```

Then

```text
A_0 = 1 + chi(-3),
A_+ + A_- = p - 6 - chi(-3),
A_+ - A_- = -3(chi(-1)+chi(-3)).
```

Indeed, the excluded parameters are

```text
u in {0, -1, 1, -2, -1/2},
```

and for `alpha(u)=-(u^2+u+1)` the standard quadratic character sum gives

```text
sum_{u in F_p} chi(alpha(u)) = -chi(-1).
```

The excluded contribution is `2chi(-1)+3chi(-3)`, and the zeros of
`alpha` are exactly the nontrivial cube roots, counted by `1+chi(-3)`.
This gives the displayed formulas.

Consequently, for every prime `p>=17`, the full-domain slack-two residual
slope image is

```text
F_p        if p == 1 mod 3,
F_p^*      if p == 2 mod 3.
```

The small exceptional primes are visible from the same formulas: `p=7` gives
only the zero slope, `p=11` gives one nonzero square class, and `p=13` gives
zero plus one nonzero square class. Thus full-domain low-index examples are
guaranteed to saturate all nonzero slopes, and sometimes the zero slope too;
non-field-filling slack-two progress must come from proper subgroup index,
inactive quotient lifts, or a sharper reserve argument.

For prime fields this unit-equation shape count is a cyclotomic number. Let
`D <= F_p^*` have order `n`, index `e=(p-1)/n`, and let `chi` be a
multiplicative character of order `e`, extended by `chi(0)=0`. The raw shape
equation count

```text
U_2(D) = #{ u in D : -1-u in D }
```

has the exact character expansion

```text
U_2(D) =
  (1/e^2) sum_{a,b=0}^{e-1}
    chi^(a+b)(-1) J(chi^a, chi^b),
```

where `J(A,B)=sum_x A(x)B(1-x)` is the Jacobi sum. The shape set `C_2(D)` is
obtained from `U_2(D)` by deleting the degenerate cases
`u=1`, `-1-u=1`, and `u=-1-u`.

Using the standard Jacobi-sum bound for nontrivial pairs gives the immediate
conditional estimate

```text
|U_2(D) - (p-2)/e^2| <= ((e^2-1)/e^2) sqrt(p).
```

Consequently

```text
|C_2(D)| <= ceil((p-2 + (e^2-1)sqrt(p))/e^2),
```

and the first-superboundary slack-two slope count is bounded by

```text
min(|F_p|,
    1 + ceil(|C_2(D)|/6) * n/gcd(2,n)).
```

The exact scanner keeps the sharper active-shape and square-coset count; this
character estimate is the asymptotic bridge from the unit-equation ledger to a
field-size bad-slope budget.

Writing

```text
B_e = ceil((p-2 + (e^2-1)sqrt(p))/e^2),
g = gcd(2,n),
```

the cyclotomic estimate gives the concrete certificate

```text
|Bad_{T=2, |P|=3}| <= min(p, 1 + ceil(B_e/6) * n/g).
```

Thus the slack-two first-superboundary slice is provably non-field-filling
whenever

```text
1 + ceil(B_e/6) * n/g < p.
```

This is the first explicit index threshold for the superboundary catalog:
using `n=(p-1)/e`, the leading term is on the order of
`p^2/(6g e^3)` plus the square-root-error contribution. Hence the character
method starts to give a nontrivial slope budget around the regime
`e^3 >> p`, while small-index domains can still saturate the whole slope
field in the toy slack-two catalog.

The next low-slack case has a similarly finite shape ledger. For slack
`T=3`, assume `4<m` and put

```text
C_3(D) = { (u,v) in D^2 :
           w=-1-u-v in D,
           1,u,v,w distinct,
           u^2+v^2+uv+u+v+1=0 }.
```

Every residual packet `P` of size four with `e_1(P)=e_2(P)=0` can be written
as

```text
P = x {1,u,v,w},        x in D,        (u,v) in C_3(D),
```

and the map `(x,u,v) -> P` is twenty-four-to-one: choose the base point of
`P`, then choose an ordered pair among the three remaining points. Indeed,
after scaling one point to `1`, the equation `e_1=0` gives
`w=-1-u-v`, while `e_2=0` becomes the displayed conic equation.

For exact support size `s=Lm+4`, define

```text
beta(u,v)=-(1+uvw),
tau(u,v)=#{quotient fibers met by {1,u,v,w}}.
```

The full lifted slope multiset in the slack-three first superboundary is

```text
M_3(z) = (1/24) sum_{(u,v) in C_3(D)}
         binom(N-tau(u,v), L) * #{x in D : x^3 beta(u,v)=z}.
```

The conic ledger can be compressed one step further. For a fixed
`beta in F`, the corresponding normalized shape points are exactly the three
roots in `D\{1}` of

```text
G_beta(Y)=Y^3+Y^2+Y+beta+1.
```

Indeed, once `1` is one point of the packet, the other three roots have
elementary sums

```text
u+v+w=-1,        uv+uw+vw=1,        uvw=-(beta+1).
```

Thus admissible nonordered shapes are indexed by the values `beta` for which
`G_beta` has three distinct roots in `D\{1}`. Each such `beta` contributes
exactly six ordered pairs `(u,v)` to `C_3(D)`. In particular the
two-dimensional conic ledger reduces to a one-parameter split-cubic ledger,
and the slope cosets are the cube cosets `beta D^3`.

Equivalently, define the split-cubic root count

```text
r_D(beta)=#{ y in D\{1} : y^3+y^2+y+beta+1=0 }.
```

Then

```text
beta is admissible  <=>  r_D(beta)=3,
|C_3(D)| = 6 * #{ beta : r_D(beta)=3 },
#{admissible beta in gamma D^3}
  = #{ beta in gamma D^3 : r_D(beta)=3 }.
```

This is an exact finite-audit route: all abstract slack-three beta counts and
all nonzero `D^3` coset counts can be computed by one pass through
`D\{1}`, grouping the values

```text
beta(y)=-(y^3+y^2+y+1).
```

The conic enumeration is still needed for quotient-lift weights depending on
`tau(u,v)`, but the coset-coverage questions used by the character
certificates reduce to this one-dimensional split-cubic ledger.

Thus the `T=3`, `|P|=4` residual catalog is reduced to a conic over the
multiplicative domain plus the cube-image map `x -> x^3` on `D`. Its nonzero
slope image is exactly a union of cosets `beta(u,v)D^3`; since `D^3` is a
subgroup, the same disjoint-or-equal coset compression applies. The zero
slope slice is the already classified four-power-coset family.

The same conic is also the exact zero-slope slice of the next residual layer
for slack two. Keep `T=2`, assume `4<m`, and consider second-superboundary
residual packets of size four. The only zero-prefix equation is `e_1(P)=0`.
After scaling one packet point to `1`, every such residual packet has the
form

```text
P = x {1,u,v,w},        w=-1-u-v,
```

with `u,v,w in D` and `1,u,v,w` distinct. Conversely every such pair
`(u,v)` gives a packet with `e_1(P)=0`. The next canonical coefficient is

```text
e_2(x{1,u,v,w})
  = -x^2 (u^2+v^2+uv+u+v+1).
```

Thus, putting

```text
A(u,v)=-(u^2+v^2+uv+u+v+1),
tau(u,v)=#{quotient fibers met by {1,u,v,w}},
```

the full lifted slope multiset at exact support size `s=Lm+4` is

```text
M_2^(2)(z) = (1/24) sum_{u,v}
             binom(N-tau(u,v), L) * #{x in D : x^2 A(u,v)=z},
```

where the sum is over the displayed admissible ordered pairs. The factor
`24` is the number of choices of base point and ordered pair among the three
remaining points of the same four-point packet.

In particular the nonzero depth-two slack-two slope image is a union of
square cosets `A(u,v)D^2`, while the zero-slope subcatalog is exactly

```text
u^2+v^2+uv+u+v+1=0.
```

This is precisely the slack-three first-superboundary conic shape equation.
So the conic found above is not an isolated slack-three accident: it is the
interface between slack-two depth two and slack-three depth one. The
exact-support lift gate is the depth-two congruence

```text
m | (s-4) = k-2.
```

If this fails, the whole depth-two slack-two small-residual layer is inactive
at that quotient scale before any conic or square-coset counting is needed.

For the full multiplicative domain, the nonzero depth-two frontier saturates
all nonzero slopes except in the two tiny cases `p=5,7`. Let `D=F_p^*`,
`p>=11`, and keep the admissibility conditions above. Then the values

```text
A(u,v)=-(u^2+v^2+uv+u+v+1)
```

hit both quadratic classes among admissible pairs. Hence the nonzero
depth-two slack-two slope image is all of `F_p^*`, because multiplying by
`x^2` runs through the square class of `A(u,v)`.

For `p>=23` this follows from a character-sum margin. Write `chi` for the
quadratic character and `Q=-A`. For fixed `u`, the polynomial in `v`

```text
Q(u,v)=v^2+(u+1)v+u^2+u+1
```

has discriminant `-3u^2-2u-3`. Therefore

```text
sum_(u,v in F_p) chi(A(u,v)) = p chi(2),
```

because the discriminant has `1+chi(-2)` roots. Also the zero locus is a
nondegenerate conic, so it has at most `p+1` points. Thus each nonzero
quadratic class occurs at least

```text
(p^2-(p+1)-p)/2
```

times before the admissibility cuts. The forbidden conditions

```text
u=0, v=0, w=0, u=1, v=1, w=1, u=v, u=w, v=w
```

with `w=-1-u-v` lie in the union of nine affine lines, containing at most
`9p` pairs. Since `(p^2-2p-1)/2 > 9p` for `p>=23`, both quadratic classes
remain after the cuts. The remaining primes `p=11,13,17,19` are checked by

```bash
python3 experimental/verify_m1_slack_two_depth_two_full_domain.py
```

The same finite check records the sharp tiny failures: at `p=5` the
admissible depth-two frontier is purely zero, and at `p=7` it hits only the
square class.

The complementary high-index ceiling is unconditional and works for every
multiplicative subgroup `D`. Put `n=|D|` and `g=gcd(2,n)`. In the slack-two
depth-two frontier, normalized ordered shapes are a subset of `D^2`, and each
nonzero shape contributes at most one square coset `A(u,v)D^2`. Since
`|D^2|=n/g`, the nonzero slope image has size at most

```text
n^2 * n/g.
```

Adding the possible zero slope gives the field-capped certificate

```text
|Bad_{T=2,d=2}| <= min(p, 1 + n^3/g).
```

This is crude compared with the exact square-coset scanner, but it is useful
as a scale marker: whenever `1+n^3/g<p`, the depth-two slack-two frontier is
provably non-field-filling before any character-sum estimate is invoked.
Thus the full-domain saturation theorem above and this high-index ceiling
bracket the first nonzero frontier: low-index/full-domain cases saturate,
while sufficiently high-index subgroup cases are automatically sparse.

There is also a low-index saturation certificate for proper subgroups. Let
`D <= F_p^*` have order `n`, index `e`, put `g=gcd(2,n)`, and put
`H=D^2`, so `[F_p^*:H]=h=eg`. Fix a multiplicative character `chi` with
kernel `D`, a character `psi` with kernel `H`, and a nonzero coset `gamma H`.
For the depth-two shape map

```text
A(u,v)=-(u^2+v^2+uv+u+v+1),     w=-1-u-v,
```

define the raw coset count

```text
V_gamma^raw =
  #{(u,v) in F_p^2 :
      u,v,w in D, A(u,v) in gamma H }.
```

With all characters extended by zero at zero, this has the exact expansion

```text
V_gamma^raw =
  (1/(e^3 h)) sum_{a,b,c,d}
    psi^(-d)(gamma) S_{a,b,c,d},

S_{a,b,c,d} =
  sum_{u,v in F_p}
    chi^a(u) chi^b(v) chi^c(-1-u-v) psi^d(A(u,v)).
```

The nonprincipal terms in this expansion are genuinely Kummer-nontrivial.
Indeed `H=D^2` has index `h=eg`, and after choosing `psi` of order `h` one
has `chi=psi^g`. Thus each summand is

```text
psi(u^(ga) v^(gb) w^(gc) A(u,v)^d),     w=-1-u-v.
```

For `p>3`, the four divisors `u=0`, `v=0`, `w=0`, and `A=0` are distinct
reduced components, with `A=0` a nonsingular conic. The divisor exponents
are

```text
ga, gb, gc, d      modulo h.
```

If all four exponents are `0 mod h`, then `a=b=c=0 mod e` and `d=0 mod h`,
which is exactly the principal tuple. Hence no nonprincipal term is an
`h`-th power times a constant on the Kummer open set. The imported
two-variable Weil bound is therefore being applied only to nontrivial
Kummer sheaves; the scanner reports this as
`canonical_slack_two_second_kummer_divisor_nontriviality_check`.

The principal term counts the complement of the divisor
`u v (-1-u-v) A(u,v)=0`, and this count is exact. The three lines
`u=0`, `v=0`, and `w=0` have union size `3p-3`. The affine conic `A=0`
has `p-chi(-3)` points. On each of the three lines it cuts
`1+chi(-3)` points, and these intersection sets are disjoint because the
line-line intersections are not on the conic. Hence the principal count is

```text
p^2 - (3p-3) - (p-chi(-3)) + 3(1+chi(-3))
  = p^2 - 4p + 6 + 4 chi(-3).
```

The imported constant is attached to the radical divisor, not to the possibly
large character orders. The squarefree support divisor has component degrees

```text
deg(u=0), deg(v=0), deg(w=0), deg(A=0) = 1,1,1,2,
```

so its total degree is `5`. The standard two-variable Kummer-Weil estimate
for a nontrivial rank-one Kummer sheaf with squarefree divisor of total
degree `r` gives constant `(r-1)^2`. The coarse full-radical constant is

```text
|S_{a,b,c,d}| <= 16 p
```

when all three coordinate divisors and the conic divisor are active. The
current scanner uses the sharper radical-degree ledger. The `d=0` Jacobi
part and the `d!=0` coordinate-principal conic part each pay a linear `p`
term plus the open-set correction `6 ceil(sqrt(p))`; the quadratic
one-coordinate subcase pays the elementary `4p`; and the remaining mixed
Kummer terms pay `4p`, `9p`, or `16p` according as exactly one, two, or
three coordinate divisors are active. With `h=[F_p^*:D^2]`, put

```text
J = (e^3-1) + (h-1),
C_1 = 3(e-1)(h-2),
C_2 = 3(e-1)^2(h-1),
C_3 = (e-1)^3(h-1),
E = (e^3-1) + (h-1) + 12(e-1) + 4C_1 + 9C_2 + 16C_3.
```

The remaining admissibility cuts `u=1`, `v=1`, `w=1`, `u=v`, `u=w`, and
`v=w` form six affine lines. For `p>3`, these lines have exact union size
`6p-11`, so they remove at most `6p-11` points from any fixed coset count.
Therefore every nonzero `H`-coset is hit by a raw admissible depth-two shape
whenever

```text
p^2 - 4p + 6 + 4 chi(-3)
  > p E + 6 ceil(sqrt(p)) J + (6p-11)e^3 h.
```

Equivalently, the scanner's integer certificate with this weighted error
forces the raw nonzero depth-two slack-two shape catalog to saturate every
nonzero `D^2`-coset.

There is one further exact-support transfer gate. At support size
`s=k+2=Lm+4`, a normalized four-point residual packet touching `tau` quotient
fibers has lift multiplicity

```text
binom(N-tau,L),        N=n/m.
```

Since always `tau <= min(4,N)`, every raw depth-two shape is lift-active if

```text
N-L >= min(4,N).
```

Under this complement-fiber gate, the raw Kummer saturation certificate
therefore promotes to exact-support saturation: every nonzero `D^2`-coset
occurs among actual slack-two depth-two supports. Without this gate, the
Kummer estimate is still a raw shape theorem, but the exact-support image must
be read from the active shape catalog or proved by an additional argument.

The same lift filter also gives an unconditional sparse bound in the
lift-limited case. Let

```text
R=N-L
```

be the number of quotient fibers not consumed by the whole-fiber part of the
support. An active normalized four-point shape must have

```text
tau(u,v) <= R,
```

so its quotient support is a subset of at most `R` quotient fibers containing
the normalized fiber of `1`. Hence the number of active ordered normalized
pairs `(u,v)` is at most

```text
B_R = sum_(r=1)^min(R,4,N) binom(N-1,r-1) (r m)^2.
```

The nonzero depth-two packets still have exactly `24` normalizations, while
zero-slope packets contribute only the single slope `0`. Therefore the active
exact-support slope image obeys the field-capped bound

```text
|Bad_{T=2,d=2}^{active}|
  <= min(p, 1 + floor(B_R/24) |D^2|).
```

This bound is independent of the Kummer estimate. It explains part of the
new `raw_saturated_lift_limited` regime: even if the raw shape map is
surjective onto `F_p^*/D^2`, exact supports are non-field-filling whenever
the displayed lift-limited bound is below `p`.

At the extreme `R=1`, this quotient-limited bound becomes an exact reduction.
Let

```text
K = {x in D : x is in the quotient fiber of 1};
```

equivalently `K` is the subgroup of `D` of order `m`. A normalized active
shape touches only one quotient fiber if and only if

```text
u,v,-1-u-v in K.
```

It then has lift multiplicity `1`, because the remaining `N-1` quotient
fibers are forced to be the whole-fiber part of the support. Hence the
`R=1` exact-support slope image is

```text
{0 : A(u,v)=0 for some kernel shape}
  union
{ A(u,v) D^2 :
    u,v,-1-u-v in K, 1,u,v,-1-u-v distinct, A(u,v) != 0 }.
```

Thus the most lift-limited depth-two layer is not an ambient support problem
at all: it is the depth-two shape map on the quotient kernel, expanded by the
ambient square image `D^2`.

This does not give a positive M1 bound; it is the complementary wall to the
high-index ceiling above. Low-index proper subgroups are saturated only when
the lift gate and complement-fiber gate transfer raw shapes to exact supports,
high-index subgroups are sparse by the elementary `n^3/g` bound, lift-limited
supports are sparse when the `B_R` bound is nontrivial, and the genuinely
M1-relevant regime is the intermediate window where none of these
certificates fires.

The same inequality gives an exact integer threshold for fixed subgroup
index data:

```text
p >= 22 e^3 h + 4 = 22 e^4 g + 4.
```

At and above this threshold, the Kummer certificate forces raw low-index
saturation, and it forces exact-support saturation when
`N-L >= min(4,N)` also holds. The high-index ceiling above gives sparse
non-field-filling whenever

```text
1 + n^3/g < p,        n=(p-1)/e.
```

Thus, after the lift gate `m | k-2` and complement-fiber gate
`N-L >= min(4,N)` are checked, the slack-two depth-two frontier has only one
unresolved proper-subgroup index window in this catalog:

```text
p < 22 e^4 g + 4
and
1 + (p-1)^3/(e^3 g) >= p.
```

Heuristically this is the interval
`(p/(22g))^(1/4) lesssim e lesssim p^(2/3)/g^(1/3)`. The point is not that
this window is small enough for the final M1 theorem, but that everything
outside it is now explained by a precise reason: inactive lift gate,
low-index saturation, or high-index sparsity.

For the full multiplicative domain this conic ledger has an exact elementary
count. Take `D=F_p^*`, `p>3`, and write `chi` for the quadratic character.
The affine conic `Q(u,v)=0` has `p-chi(-3)` points. The three sections
`u=0`, `v=0`, and `w=0` are disjoint on the conic and each has
`1+chi(-3)` points. The six degeneracy sections

```text
u=1, v=1, w=1, u=v, u=w, v=w
```

are disjoint from those zero sections, and for `p>3` are pairwise disjoint
on the conic. Each has `1+chi(-2)` points. Hence the ordered full-domain
shape count is

```text
|C_3(F_p^*)| = p - 9 - 4 chi(-3) - 6 chi(-2).
```

The split-cubic compression then gives exactly

```text
#{admissible beta values}
  = (p - 9 - 4 chi(-3) - 6 chi(-2))/6.
```

The zero value `beta=0` occurs exactly when

```text
G_0(Y)=Y^3+Y^2+Y+1=(Y+1)(Y^2+1)
```

splits over `F_p`, equivalently when `chi(-1)=1`; in that case it contributes
one beta value and six ordered shapes.

Consequently, when `p==2 mod 3` the cube map on `F_p^*` is surjective, so
any nonzero admissible beta value already gives every nonzero slope. The
count above shows that such a nonzero beta exists for every `p>=23` with
`p==2 mod 3`. Therefore the full-domain slack-three first-superboundary slope
image is

```text
F_p        if p==5 mod 12 and p>=29,
F_p^*      if p==11 mod 12 and p>=23.
```

The small exceptional primes are also explicit: `p=5` and `p=17` contribute
only the zero slope, while `p=11` has no admissible full-domain slack-three
shape. Thus, as in the slack-two full-domain case, the full-domain
cube-surjective slack-three catalog is a saturated obstruction, not a
non-field-filling source.

The index-three cube-image case has a parallel character certificate. Assume
`p==1 mod 3`, let `psi` be a cubic character with kernel `(F_p^*)^3`, and
fix a nonzero cube coset `gamma(F_p^*)^3`. Let `A_3` be the ordered
full-domain shape set above and put

```text
B_gamma =
  #{(u,v) in A_3 : beta(u,v) in gamma(F_p^*)^3}.
```

With characters extended by zero at zero,

```text
B_gamma =
  (1/3) sum_{r=0}^2 psi^(-r)(gamma)
    sum_{(u,v) in A_3} psi^r(beta(u,v)).
```

For `r=1,2`, the inner sum is the projective-conic character sum attached to
the rational function `beta=-(1+uvw)`, with the zero sections and degeneracy
sections removed. The divisor of `beta` has at most eight geometric
zero/pole points on the smooth conic: the cubic numerator contributes at most
six zero points and the line at infinity contributes two pole points. These
zeros are simple in characteristic `p>3`, so neither `beta` nor `beta^2` is a
cube as a rational function on the conic. Hence the same genus-zero
multiplicative Weil bound gives `6 sqrt(p)` for the full conic sum, and
removing the finite excluded sections costs at most `18` points. If
`A_nonzero` denotes the ordered shapes with `beta != 0`, then
every nonzero cube coset contains at least

```text
ceil((A_nonzero - 12 sqrt(p) - 36)/18)
```

admissible beta values whenever the numerator is positive. Since

```text
A_nonzero = |C_3(F_p^*)| - 6 * 1_{chi(-1)=1},
```

the crude bound `A_nonzero >= p-25` shows that all three cube cosets occur
for every prime `p>=271` with `p==1 mod 3`. Thus for all such primes the
full-domain slack-three first-superboundary slope image contains every
nonzero field slope, and it contains zero exactly when `chi(-1)=1`.

The remaining finite range is small enough to audit exactly from the
split-cubic beta ledger. For primes `p==1 mod 3` below `271`, exact
enumeration of admissible beta values by cube coset gives the unsaturated
list

```text
7, 13, 19, 31, 37, 43, 61, 67, 73, 79, 97.
```

Every prime `p==1 mod 3` with `103<=p<271` hits all three nonzero cube
cosets. Combining this finite audit with the character-sum certificate proves
that the full-domain slack-three first-superboundary image contains every
nonzero field slope for every prime `p==1 mod 3` with `p>=103`.
This finite audit is reproduced by

```bash
python3 experimental/verify_m1_slack_three_full_domain_audit.py
```

There is also a prime-field character-sum route for the slack-three conic
count. Let `D <= F_p^*` have order `n`, index `e=(p-1)/n`, and let `chi` be
a multiplicative character of order `e`, extended by zero at zero. Put

```text
w=-1-u-v,        Q(u,v)=u^2+v^2+uv+u+v+1.
```

The raw ordered conic count

```text
U_3^raw(D)=#{(u,v) in F_p^2 : Q(u,v)=0, u,v,w in D}
```

has the exact expansion

```text
U_3^raw(D) =
  (1/e^3) sum_{a,b,c=0}^{e-1} S_{a,b,c},

S_{a,b,c} =
  sum_{Q(u,v)=0} chi^a(u) chi^b(v) chi^c(w).
```

For `p>3`, the projective conic attached to `Q=0` is nonsingular. Its affine
point count is `p-chi_2(-3)`, where `chi_2` is the quadratic character. The
principal term in the displayed expansion counts affine conic points with
`uvw != 0`; the three zero-line intersections are disjoint and each has
`1+chi_2(-3)` points, so

```text
S_{0,0,0}=p-3-4 chi_2(-3).
```

The admissible shape count `|C_3(D)|` is at most this raw conic count, after
removing the finite degeneracies where one of `u,v,w` equals `1` or two of
`1,u,v,w` coincide.

The character-sum conductor is small in this case. On the smooth projective
conic, the rational functions

```text
u=U/Z,        v=V/Z,        w=(-U-V-Z)/Z
```

have zeros on the three lines `U=0`, `V=0`, and `U+V+Z=0`, and common poles
on the line `Z=0`. Each line meets the conic in two geometric points, and
for `p>3` these four intersection divisors are pairwise disjoint. Thus every
nonprincipal product `u^a v^b w^c` has geometric zero/pole support of size at
most `8`; it is not an `e`-th power unless `a=b=c=0`, since the three zero
divisors have coefficients `a`, `b`, and `c`. The standard genus-zero
multiplicative Weil bound therefore gives

```text
|S_{a,b,c}| <= 6 sqrt(p)        for nonprincipal (a,b,c).
```

This gives the ordered-shape estimate

```text
|C_3(D)| <= ceil((p+1 + 6(e^3-1)sqrt(p))/e^3).
```

Therefore the slack-three first-superboundary slope set satisfies

```text
|Bad_{T=3, |P|=4}|
  <= min(p,
         1 + ceil(|C_3(D)|/24) * n/gcd(3,n)).
```

Combining the previous two displays gives an explicit conditional
non-field-filling certificate. Its leading term is on the order of
`p^2/(24 gcd(3,n) e^4)`, so the conic-count route starts to help in the
large-index regime `e^4 >> p`, complementing the slack-two unit-equation
threshold `e^3 >> p`.

There is also a complementary low-index saturation certificate for proper
subgroups. Keep the same notation, put `g=gcd(3,n)`, `H=D^3`, and
`h=[F_p^*:H]=eg`. For a nonzero coset `gamma H`, define

```text
V_gamma^raw =
  #{(u,v) in F_p^2 : Q(u,v)=0,
                       u,v,w in D,
                       beta(u,v) in gamma H}.
```

Let `psi` have kernel `H`. With characters extended by zero,

```text
V_gamma^raw =
  (1/(e^3 h)) sum_{a,b,c=0}^{e-1} sum_{d=0}^{h-1}
    psi^{-d}(gamma) S_{a,b,c,d},

S_{a,b,c,d} =
  sum_{Q(u,v)=0}
    chi^a(u) chi^b(v) chi^c(w) psi^d(beta(u,v)).
```

The principal term counts affine conic points with `uvw beta != 0`, and is
at least `p-9-4 chi_2(-3)`. For a nonprincipal tuple, the rational function
`u^a v^b w^c beta^d` on the smooth projective conic has geometric zero/pole
support contained in the six points from `u,v,w`, at most six zeros of
`beta`, and the two points at infinity. The standard genus-zero
multiplicative character-sum estimate therefore gives

```text
|S_{a,b,c,d}| <= 12 sqrt(p)       for nonprincipal (a,b,c,d).
```

Removing the six degeneracy sections where one of `1,u,v,w` coincides with
another point costs at most `12` additional ordered parameters. Hence every
nonzero `H=D^3` coset contains at least

```text
ceil((p - 9 - 4 chi_2(-3) - (12 sqrt(p)+12)e^3 h)/(e^3 h))
```

admissible ordered slack-three shape parameters, whenever the displayed
quantity is positive. In that case the abstract first-superboundary
slack-three catalog hits every nonzero `D^3` slope coset; in the exact
support layer `s=4`, where there is no quotient-lift filter, it contains
all nonzero field slopes. This is the low-index counterpart to the
high-index non-field-filling bound above. Its leading condition is
`e^4 g << sqrt(p)`, while the upper-bound route begins to help around
`e^4 >> p`; the broad middle range is where sharper beta-coset Jacobi sums
or exact finite audits are most valuable.

This criterion has an exact fixed-denominator threshold. Put

```text
M=e^3 h=e^3 [F_p^*:D^3].
```

Let `s_M` be the least positive integer such that

```text
(s_M-1)^2 + 1 - 13 > (12 s_M + 12) M,
```

and define

```text
P_M=(s_M-1)^2+1.
```

Then for every prime `p>=P_M`, independently of the value of `chi_2(-3)`,

```text
p - 9 - 4 chi_2(-3) > (12 ceil(sqrt(p)) + 12) M.
```

Indeed, on the bucket where `ceil(sqrt(p))=s`, the left side minus the right
side is minimized at `p=(s-1)^2+1`; the displayed defining inequality for
`s_M` is increasing for all larger buckets. Hence the proper-subgroup
cube-coset certificate fires for every prime with this denominator once
`p>=P_M`. For example,

```text
M=3      gives P_M=1522,
M=16     gives P_M=38026,
M=48     gives P_M=335242.
```

Thus quadratic-residue domains with `p==5 mod 6` have `M=16`, so this
conditional certificate already proves full nonzero `D^3`-coset coverage for
all such primes `p>=38026`.

The remaining finite range for this index-two case is small enough to audit
exactly with the split-cubic beta ledger. Let `D=(F_p^*)^2` and assume
`p==5 mod 6`. Then `D^3=D`, so the nonzero beta image has exactly two
`D^3` cosets to hit. Exact enumeration for every prime `p==5 mod 6` below
`38026` shows that the only unsaturated primes are

```text
5,11,17,23,29,41,47,53,59,71,83,89,101,107,113,131,137,149,
167,173,179,191,197,227,233,239,251,257,269,281,317,347,359,
383,401,431,467,491,503,587,617,647,653,701,1031.
```

Every prime `p==5 mod 6` with `1049<=p<38026` hits both nonzero `D^3`
cosets. Combining this finite audit with the uniform conditional threshold
above gives full nonzero `D^3`-coset coverage for every quadratic-residue
domain with `p==5 mod 6` and `p>=1049`, subject only to the imported
large-prime character-sum estimate for the range `p>=38026`.
The finite audit is reproduced by

```bash
python3 experimental/verify_m1_slack_three_qr_index_two_audit.py
```

The split-cubic exact audit

```bash
python3 experimental/verify_m1_slack_three_cube_coset_coverage.py
```

checks this certificate on an index-two proper subgroup at `p=38039`,
where the lower bound is positive and both nonzero `D^3` cosets are hit.

## M1 Impact

This turns the positive M1 problem into a precise incidence question:

```text
How many distinct slopes can arise from support collinearities
Pi_S(f) in span(Pi_S(g))
after tangent and quotient-periodic families are separated?
```

For `t = 1`, every nonzero `Pi_S(g)` is automatically collinear with
`Pi_S(f)`, which is the linear-algebra shadow of the tangent floor. For
`t >= 2`, collinearity has codimension `t - 1` in the random-support model,
which is the heuristic reason the aperiodic packing number should collapse
once the corrected reserve clears the quotient floors.

The note is therefore a bridge between the coordinate definition of
support-wise MCA and the residue-line normal form: denominator closure
parameterizes structured ways in which these top-coefficient vectors can align,
while this test is the exact finite support criterion that a proof or
experiment can check directly.
The quotient-occupancy decomposition adds a second label to the same incidence
problem: after supports are grouped by fiber content, the quotient-structured
part can be compared against the exact `H_h` ledger before any remaining
support-collinearity is called aperiodic.
The canonical quotient-core factorization sharpens this in the monomial
slack line: for `T<=m`, whole quotient fibers can be stripped away before
checking the zero-prefix equations, leaving a concrete residual
partial-fiber symmetric-zero problem.
The low-residual cutoff then proves that residual packets of total size
`1,...,T-1` are harmless for the canonical quotient-locator line over a
multiplicative domain; the first possible residual canonical obstruction is
the rigid boundary case `|R|=T`, where the residual set must itself be a
`T`-power fiber.
The slope decomposition adds that, below the boundary `T<m`, even the slope
value is residual-only. At `T=m`, all whole-fiber dependence is compressed to
the additive quotient-core sum `sum y_i`, which is a much smaller
quotient-level object than the original support.
In cyclic domains the boundary residual obstruction is also exactly counted:
it exists only when `T|n`, then there are `n/T` residual cosets, each touching
`T/gcd(T,m)` quotient fibers. This turns the remaining canonical boundary
case into a finite quotient-level object rather than an aperiodic family.
Its slope image is the equally explicit set `-D^T`, and every boundary slope
has the same whole-fiber multiplicity. Hence the canonical boundary source can
be charged by exact slope count and multiplicity, not just by support count.
Finally, if the support residue satisfies `0<s mod m<T`, then even the
boundary source is absent and canonical residual incidences must have at least
`m+(s mod m)` residual points. This is the precise small-residual payoff of
dimension dither.
For residues `b<=T`, the small-residual canonical ledger is now exact: slope
`0` in the whole-fiber case, no slopes in the subboundary case, and the
`-D^T` boundary image at `b=T`.
Beyond this range, the residual-packet lift factorization prevents the
superboundary problem from spreading back into full support enumeration: each
residual packet carries only the explicit quotient multiplier
`binom(N-tau(P),(s-|P|)/m)`. The unresolved M1 content is therefore the size,
structure, and slope image of the residual zero-prefix packet catalog itself.
In the first superboundary layer `|P|=T+1`, the whole catalog has a uniform
shape-coset reduction: normalized shapes form `C_T(D)`, the quotient by
normalization has size `(T+1)!`, and the slope image is a union of cosets
`a_T(C_T(D))D^T`. The zero-slope subcatalog is the counted
`(T+1)`-power-coset family, while the remaining nonzero slopes are exactly
the nonzero coefficients of `D`-split sparse trinomials `X^(T+1)+zX-c`.
The resulting slope budget is the generic power-coset bound
`1_zero + (active nonzero shape orbits)|D^T|`, capped by the field size.
The exact-support dither gate adds that this whole layer is inactive unless
`m | k-1`; for dyadic quotient scales dividing an exact dimension `k0`, a
dither `k=k0-r` leaves only scales dividing `r+1`.
The small-residual depth gate extends this to every depth below one quotient
fiber: depth `d` can survive only when `m | k-d`. Hence positive dithers
`1<=r<=T-1` remove all small-residual superboundary layers at all quotient
scales `m>T` dividing the exact dimension `k0`.
Equivalently, the local residue certificate `0<(k+T mod m)<T` clears the
entire canonical catalog below one quotient fiber at that scale.
Thus, in a dyadic quotient hierarchy, positive dither turns the canonical
small-residual M1 problem into a finite-prefix problem with at most
`floor(log2(T))` nontrivial scales; beyond that prefix only large-residual or
aperiodic packing can contribute.
For `T=2`, even that nonzero catalog is no longer a support-enumeration
problem: it is exactly the unit-equation shape set `C_2(D)`, with slope image
given by the square cosets `alpha(u)D^2` and quotient-lift weight
`binom(N-tau(u),L)`.
The resulting square-coset slope bound is the first direct bad-slope-count
payoff inside the superboundary range: improving M1 here reduces to bounding
`C_2(D)` and overlaps among the square cosets `alpha(u)D^2`.
The exact square-coset compression removes one ambiguity: those overlaps are
only equality of cosets, so the M1-relevant object is the image of
`alpha(C_2(D))` in `F_p^*/D^2`.
The proper-subgroup character expansion gives a second analytic route: it
counts this image coset-by-coset and proves all nonzero cosets are hit in a
small-index regime, subject to the standard four-root Weil bound.
The exact-support lift-limited bound gives the complementary finite-support
route: when only `R=N-L` quotient fibers remain, the active depth-two image is
bounded by `1+floor(B_R/24)|D^2|` even if the raw character-sum image
saturates all square cosets.
At `R=1`, this finite-support route is exact: the active catalog is just the
kernel-fiber depth-two catalog, followed by multiplication by `D^2`.
For the full multiplicative domain this image is already both quadratic
classes for every `p>=17`, with zero added exactly when `p==1 mod 3`; this
proves that full-domain slack-two examples saturate all nonzero slopes rather
than giving a route to non-field-filling.
The cyclotomic expansion gives the first analytic route to such a bound: once
standard Jacobi-sum estimates apply, the shape count is roughly `p/e^2` with
square-root error, where `e=(p-1)/|D|`.
The resulting non-field-filling test is explicit in `p,n,e`: it identifies
which subgroup indices are already controlled by the cyclotomic method and
which low-index cases require a sharper argument or different reserve.
For `T=3`, the first-superboundary catalog is also no longer a raw support
enumeration: it is a split-cubic beta ledger, equivalently a conic shape set
`C_3(D)`, and a cube-coset image. This extends the low-slack template
classification one step beyond the unit equation case.
In the full-domain cube-surjective case `p==2 mod 3`, the exact conic count
proves saturation for every `p>=23`: all nonzero slopes occur, and zero
occurs exactly when `p==1 mod 4`.
For `p==1 mod 3`, the full-domain cubic-character refinement gives a
large-prime saturation certificate as well: every cube coset is hit once
`p>=271`, so the full-domain slack-three obstruction again fills all nonzero
slopes.
The exact finite audit improves the final threshold to `p>=103` in this
index-three case.
The prime-field conic character expansion gives the matching analytic route:
under a standard genus-zero character-sum estimate, the slack-three ordered
shape count is roughly `p/e^3`, and the resulting cube-coset slope budget has
leading size `p^2/(24 gcd(3,n) e^4)`.

## Suggested Next Step

The script `experimental/m1_support_occupancy_scan.py` is the current small M1
scanner around `Pi_S` and quotient-fiber occupancy. It can be run, for example,
as

```bash
python3 experimental/m1_support_occupancy_scan.py \
  --prime 17 --n 8 --k 4 --slack 2 --quotient-order 4
```

The next step is to run this on more tiny fields and line families, then compare
the observed histogram incidence counts with the occupancy-profile random-line
ledger before attacking the genuinely aperiodic packing number. For the default
canonical line, the scanner also verifies the elementary-symmetric slope
formula and the quotient-core invisibility identity `e_d(S)=e_d(R(S))` for
`d<m`. It also checks the low-residual exclusion and the boundary coset
classification on every scanned support, and verifies the residual-only and
boundary quotient-core slope decompositions. In cyclic-domain scans it also
checks the exact boundary-coset count above and the associated boundary slope
image/multiplicity, and reports the subboundary residual-size floor in the
dithered residue range. It also reports the closed small-residual regime for
support residues `b<=T`. In the first superboundary range it now also checks
the residual-packet lift formula, so scans can distinguish the new residual
packet catalog from the already solved quotient-core lifting multiplicity.
For residual packets of size `T+1`, it additionally checks the zero-slope
power-coset classification and the corresponding lifted support count.
For small scanned slack, it also checks the full normalized shape-coset
formula, its `D^T` coset-compressed slope count, and the exact-support
dither gate `m | k-1` for first-superboundary activity.
It also reports the active small-residual superboundary depth, if any, using
the general gate `m | k-d`.
When `T=2`, it also checks the complete unit-equation shape ledger and its
weighted slope histogram.
The same scanner reports the associated square-coset slope-count bound.
For prime fields it also reports the cyclotomic/Jacobi shape-count bound and
the induced slope-count bound.
It flags whether this induced bound is genuinely below the ambient field size.
