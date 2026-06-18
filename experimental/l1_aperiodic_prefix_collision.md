# L1 Aperiodic Prefix-Collision Certificate

Status: PROVED finite certificate; COUNTEREXAMPLE to a proof route.

This note isolates a small monomial-prefix locator-fiber computation for the L1
program in `agents.md`. It does not refute the prefix local-limit conjecture.
It refutes the stronger route that quotient-core removal should make
finite-field monomial-prefix collisions disappear.

## Finite Theorem

Work over `F_17` with

```text
H = F_17^*, n = 16, k = 6, sigma = 4, a = k + sigma = 10.
```

Let

```text
Phi_4(S) = (e_1(S), e_2(S), e_3(S), e_4(S)),
```

for `10`-subsets `S` of `H`, with elementary symmetric functions computed in
`F_17`. Then the complete fiber distribution of `Phi_4` is:

```text
total supports          = binom(16,10) = 8008
distinct prefix values  = 7968
singleton fibers        = 7928
two-point fibers        = 40
maximum fiber size      = 2
```

Every nonsingleton fiber is quotient-separated from the only subgroup orders
that could be charged as `M > sigma` quotient-periodic exceptions, namely
`M = 8` and `M = 16`: if `S != T` lie in the same fiber, then
`S symmetric-diff T` has size `12` and is not a union of cosets of either
subgroup.

These forty collisions have a small structural certificate. Passing to
complements `A = H \ S` and `B = H \ T`, the collisions form exactly three
dilation orbits of unordered complement pairs:

```text
orbit size 16:
  A={1,2,3,4,6,9}, B={5,8,10,11,12,13}, L_A-L_B = 3X+13
orbit size 16:
  A={1,2,4,11,14,15}, B={6,8,9,12,13,16}, L_A-L_B = 16X+5
orbit size 8:
  A={1,2,5,6,7,13}, B={4,10,11,12,15,16}, L_A-L_B = 13X
```

The last orbit has the antipodal stabilizer: multiplication by `-1` swaps the
two complements. Thus the full collision packet is `16 + 16 + 8 = 40`.

The generated-field entropy margin is already positive:

```text
4 log2(17) - log2 binom(16,10) = 3.382625... bits.
```

The Paper B list quotient-core profile is empty: `gcd(n,k)=2`, and the only
nontrivial divisor `M=2` fails the active condition `sigma < M`.

## General Complement-Prefix Lemma

Let `H <= F^*` be a multiplicative subgroup of order `n`, let
`1 <= sigma < n`, and define

```text
E_A(Z) = prod_{a in A} (1 + aZ)
       = sum_j e_j(A) Z^j.
```

For any support `S subset H` and complement `A = H \ S`,

```text
E_S(Z) E_A(Z) = prod_{h in H} (1 + hZ) = 1 - (-Z)^n.
```

Hence

```text
E_S(Z) E_A(Z) = 1 mod Z^(sigma+1).
```

Since both truncated series have constant term `1`, inversion modulo
`Z^(sigma+1)` is unique. Therefore, for equal-size supports `S,T subset H`
with complements `A=H\S` and `B=H\T`,

```text
(e_1(S),...,e_sigma(S)) = (e_1(T),...,e_sigma(T))
iff
(e_1(A),...,e_sigma(A)) = (e_1(B),...,e_sigma(B)).
```

If the complements have size `m`, then

```text
L_A(X) = X^m - e_1(A)X^(m-1) + e_2(A)X^(m-2) - ... + (-1)^m e_m(A).
```

Thus, for `sigma < m`, complement-prefix equality is equivalent to

```text
deg(L_A - L_B) <= m - sigma - 1.
```

For `sigma >= m`, it forces `A=B`.

## Exact Divisor-Gap Parametrization

The complement-locator compression gives an exact scanner target. Fix a support
`S0` in a prefix fiber, put `A0=H\S0`, and let `m=|A0|`. Then the fiber of
`S0` is in bijection with

```text
{ Q in F[X] : deg Q <= m-sigma-1 and L_A0 + Q divides X^n - 1 }.
```

The bijection sends `Q` to the support `H\A`, where
`L_A = L_A0 + Q`. Indeed, every complement locator `L_A` is a monic
degree-`m` divisor of `X^n-1`, and the complement-prefix lemma says that
same-prefix supports are exactly those with `deg(L_A-L_A0) <= m-sigma-1`.
Conversely, any monic degree-`m` divisor of `X^n-1` has its roots in `H`, so
it is the locator of a unique complement `A`.

When `sigma >= m`, the set above contains only `Q=0`; this recovers injectivity
in the very co-large range. When `sigma < m`, it reduces finite-field
collisions to a concrete low-degree divisor perturbation problem.

## Divisor-Gap Graph Formulation

Equivalently, let `Div_m(H)` be the set of monic degree-`m` divisors of
`X^n-1`; these are exactly the complement locators. Put an edge between
`D,D' in Div_m(H)` when

```text
deg(D-D') <= m-sigma-1.
```

Then the monomial-prefix fibers at agreement size `s=n-m` are exactly the
connected components of this graph, transported by `S -> L_{H\S}`. Moreover
every component is a clique: the edge condition is just equality of the top
`sigma` locator coefficients, hence is already transitive.

Thus L1 co-large monomial-prefix scanning can be phrased without codewords or
supports: find large components in a low-degree perturbation graph on divisors
of `X^n-1`.

## Co-Large Prefix Bound

The divisor-gap formulation also gives a field-independent packing bound in the
co-large support range. Let `F = F_q`, let `s = k + sigma`, and set

```text
m = n - s = n - k - sigma.
d = m - sigma - 1.
```

If `d < 0`, every fiber is a singleton. If `d >= 0`, then for every prefix
target `c in F_q^sigma`,

```text
|Phi_sigma^{-1}(c)| <= binom(n,d+1) / binom(m,d+1).
```

Indeed, for two distinct complements `A,B` in one fiber, `L_A-L_B` has degree
at most `d`. Every point of `A cap B` is a root of `L_A-L_B`; hence
`|A cap B| <= d`, since otherwise `L_A=L_B` and `A=B`. Thus any fixed
`(d+1)`-subset of `H` lies in at most one complement in the fiber. Counting
`(d+1)`-subsets inside the complements gives the displayed packing bound.

The same `r`-packing structure also gives the recursive Johnson finite-length
bound. Let `J(n,m,r)` denote the maximum size of a family of `m`-subsets of an
`n`-point set in which every `r`-subset appears in at most one block. Set
`J(n,m,0)=1`; for `r>=1`,

```text
J(n,m,r) <= floor((n/m) J(n-1,m-1,r-1)).
```

Indeed, if `L_x` is the number of complements containing `x`, then after
removing `x` from those complements one obtains an `(r-1)`-packing of
`(m-1)`-subsets on `n-1` points. Thus `L_x <= J(n-1,m-1,r-1)` for every
`x`, while `sum_x L_x = mL`. Therefore every co-large monomial-prefix fiber
has size at most the nested Johnson bound

```text
floor(n/m floor((n-1)/(m-1) ... floor((n-r+1)/(m-r+1)) ...)).
```

This is usually a finite improvement over the raw ratio
`binom(n,r)/binom(m,r)`. In the `F_17` certificate the recursive bound is
still `8`, but on the deterministic dyadic grid used by the verifier, for
example `(n,k,sigma)=(64,28,15)`, it improves the packing bound from `1381`
to `1027`.

Counting perturbation polynomials gives the cruder field-size bound

```text
|Phi_sigma^{-1}(c)| <= q^max(m - sigma, 0)
                    = q^max(n - k - 2 sigma, 0),
```

because `A -> L_A-L_A0` is injective and there are only `q^(m-sigma)`
polynomials of degree at most `m-sigma-1`.

Consequently, monomial-prefix locator fibers are polynomially bounded
throughout the co-large strip `n-k-2sigma=O(1)`, without any quotient
hypothesis and without paying a generated-field factor. This strip is much
narrower than the desired final L1 reserve at fixed rate, but it is a proved
anchor and a useful model for low-degree complement-locator scanners.

In particular, if `r=n-k-2sigma` is fixed and `k/n -> rho`, then

```text
|Phi_sigma^{-1}(c)| <= (2/(1-rho) + o(1))^r.
```

Indeed, in this regime `m=sigma+r=((1-rho)n+r)/2`, and the packing ratio
`binom(n,r)/binom(m,r)` tends to `(n/m)^r`.

There is also a useful growing-width version. Fix `0 <= rho < 1` and assume
`k <= rho n`. Let

```text
r = n-k-2sigma >= 0,
```

and suppose

```text
r < (1-rho)n.
```

Then every monomial-prefix fiber satisfies the explicit envelope

```text
|Phi_sigma^{-1}(c)|
  <= (2/(1-rho-r/n))^r.
```

Indeed, with `m=n-k-sigma`, one has

```text
m = (n-k+r)/2,
m-r+1 = (n-k-r)/2 + 1 >= ((1-rho)n-r)/2.
```

The packing ratio factors as

```text
binom(n,r)/binom(m,r)
  = prod_{i=0}^{r-1} (n-i)/(m-i)
  <= (n/(m-r+1))^r
  <= (2/(1-rho-r/n))^r.
```

Consequently the packing bound alone gives polynomial prefix fibers whenever
`r=O(log n)`, and quasipolynomial fibers whenever `r=polylog(n)`, without any
quotient-periodic hypothesis.

There is a stronger second-moment bound in the same co-large strip. Let
`L` be the size of one monomial-prefix fiber, let its complements be
`A_1,...,A_L`, and put

```text
r = n-k-2sigma,     m = n-k-sigma.
```

When `r<=0`, the fiber is a singleton. When `r>0`, the intersection bound
above gives

```text
|A_i cap A_j| <= r-1       for i != j.
```

Write `d_x = #{i : x in A_i}`. Then

```text
sum_x d_x = Lm,
sum_x d_x(d_x-1) = sum_{i != j} |A_i cap A_j| <= L(L-1)(r-1).
```

Cauchy's inequality gives

```text
(Lm)^2 <= n sum_x d_x^2
       <= n(L(L-1)(r-1) + Lm).
```

Thus, whenever

```text
m^2 > n(r-1),
```

every monomial-prefix fiber satisfies the Plotkin-type bound

```text
|Phi_sigma^{-1}(c)| <= n(m-r+1) / (m^2 - n(r-1)).
```

Writing `a=k+sigma` for the original support agreement size, this becomes the
finite Johnson-threshold form

```text
m^2 - n(r-1) = a^2 - n(k-1),
m-r+1 = a-k+1,
```

so, whenever

```text
a^2 > n(k-1),
```

one has

```text
|Phi_sigma^{-1}(c)| <= n(a-k+1) / (a^2 - n(k-1)).
```

Thus the co-large Plotkin theorem is exactly a Johnson-region locator-fiber
anchor, expressed in monomial-prefix language. If `k/n -> rho` and
`a/n -> beta > sqrt(rho)`, then

```text
|Phi_sigma^{-1}(c)| <= (beta-rho)/(beta^2-rho) + o(1).
```

This improves the raw packing count from an exponential-in-`r` statement to a
constant bound throughout a linear-width high-slack region. In particular, if
`k/n -> rho` and `r/n -> theta` with

```text
0 <= theta < (1 - sqrt(rho))^2,
```

then the denominator is positive and

```text
|Phi_sigma^{-1}(c)|
  <= 2(1-rho-theta) / ((1-rho+theta)^2 - 4theta) + o(1).
```

For the finite `F_17` certificate this gives the explicit universal bound
`|Phi_4^{-1}(c)| <= 80/20 = 4`, while the actual maximum fiber size is `2`.
This is still a high-slack theorem, not the final `sigma=Theta(n/log n)`
local-limit range, but it sharply enlarges the theorem-backed L1 region where
large aperiodic monomial-prefix fibers cannot occur.

For finite scanners the same second-moment proof has an integral sharpening.
If a fiber has size `L`, then `sum_x d_x=Lm` is an integer composition over
`n` points, so

```text
sum_x d_x^2 >= (n-b)a^2 + b(a+1)^2,
```

where

```text
a = floor(Lm/n),       b = Lm - an.
```

Therefore `L` is impossible whenever

```text
(n-b)a^2 + b(a+1)^2 > Lm + L(L-1)(r-1).
```

This is the finite Plotkin-design obstruction: a fiber close to the rational
Plotkin bound must have nearly balanced incidence degrees and nearly maximal
pairwise complement intersections. In the `F_17` certificate the rational
bound allows `L=4`, but then `Lm=24` cannot be evenly distributed over `16`
points; the integer inequality gives `|Phi_4^{-1}(c)| <= 3`.

The exact slack in the Plotkin proof splits into two nonnegative defects.
For a fiber of size `L`, let

```text
D_2 = n sum_x d_x^2 - (Lm)^2,
P_2 = L(L-1)(r-1) - sum_x d_x(d_x-1).
```

Then

```text
n(Lm + L(L-1)(r-1)) - (Lm)^2 = D_2 + n P_2.
```

Thus equality in the rational Plotkin bound forces both defects to vanish:
the incidence degrees must be perfectly regular, and every ordered pair of
distinct complements must meet in exactly `r-1` points. Near-extremal fibers
must therefore be near-designs in this precise sense. In the `F_17` certificate
each two-point fiber is far from extremal: its complements are disjoint, and
the verifier records defect tuple `(D_2,P_2,total)=(48,2,80)` for all forty
colliding fibers.

The same parametrization can be read as a standard Reed-Solomon list problem.
Fix a prefix fiber, choose one complement locator `L_0`, and put

```text
V_r = {Q in F[X] : deg Q < r},       r = m - sigma.
```

For `r>0`, the fiber is exactly

```text
{ Q in V_r : L_0 + Q has exactly m roots in H }.
```

Equivalently, evaluating on `H`, it is the list of codewords
`Q|_H` in the dimension-`r` Reed-Solomon code `RS[H,<r]` that agree with
the received word `-L_0|_H` on exactly `m` positions. Since this code has
minimum distance `n-r+1`, two listed codewords can agree on at most `r-1`
positions; the second-moment bound above is precisely the resulting Johnson
bound for this affine list.

Thus the co-large L1 problem is not only a divisor scan: it is an affine
low-rate RS list-size problem where the agreement threshold is the complement
size `m`. The full final L1 conjecture lies outside this Johnson region, but
the reduction identifies the missing input cleanly: one needs non-Johnson
local limits for these affine locator cosets after quotient-periodic pieces
have been budgeted.

The same proof gives a stronger overlap statement. If `r<=0`, every fiber is a
singleton. If `r>0` and `S,T` are distinct supports in the same
monomial-prefix fiber, with complements `A=H\S` and `B=H\T`, then

```text
|A cap B| <= r-1.
```

Therefore

```text
|S \ T| = |T \ S| = |B \ A|
        = m - |A cap B|
        >= m-r+1 = sigma+1.
```

Equivalently,

```text
|S cap T| <= (k+sigma) - (sigma+1) = k-1.
```

Thus every co-large monomial-prefix fiber has zero strict M1 high-overlap
pairs at slack `sigma`: its internal support-family correction

```text
sum_{1 <= j <= sigma-1} Gamma_j q^(sigma-j)
```

vanishes. Co-large prefix fibers can have multiplicity, as the `F_17` example
shows, but any multiplicity is automatically separated below the M1 overlap
threshold.

Equivalently, when `r>0`, the complements in one prefix fiber form an
`r`-packing: every `r`-subset of `H` lies in at most one complement in the
fiber. Dually, the supports in one fiber form a constant-weight code of length
`n`, weight `k+sigma`, and minimum Hamming distance at least `2(sigma+1)`.
In exchange-profile notation this says

```text
Delta_j = Gamma_j = 0        for 1 <= j <= sigma
```

inside each co-large prefix fiber. The finite `F_17` certificate is even more
separated: all forty unordered colliding support pairs have exchange size `6`,
so the internal ordered profile has `Delta_6=80` and maximum codegree
`Gamma_6=1`, with no support-pair mass at exchange sizes `1,2,3,4,5`.

## Complement-Locator Compression

The orbit certificate is an instance of this lemma. Here `H=F_17^*`,
`n=16`, `m=6`, `sigma=4`, and the co-large bound is `17^(6-4)=289`.
The sharper packing bound is

```text
binom(16,2) / binom(6,2) = 8.
```

This is the fixed-width `r=2` case of the constant-fiber corollary.

Since

```text
prod_{h in F_17^*} (1 + hZ) = 1 - Z^16,
```

the support elementary series and complement elementary series are inverse to
each other modulo `Z^5`. Therefore two `10`-supports have the same
`Phi_4` value if and only if their `6`-point complements have the same first
four elementary symmetric coefficients.

For complements of size `6`,

```text
L_A(X) = X^6 - e_1(A)X^5 + e_2(A)X^4 - ... + e_6(A).
```

Equal first four elementary coefficients are equivalent to

```text
L_A(X) - L_B(X) = alpha X + beta.
```

In this toy case, every aperiodic prefix collision is exactly one of the three
linear locator-gap orbits listed above. This turns the finite counterexample to
aperiodic injectivity into a small divisor-pair problem inside `X^16 - 1`.

## Example Collision

One of the forty two-point fibers is

```text
c = (8, 12, 13, 7),
S = {1,2,3,4,5,6,7,9,10,12},
T = {1,2,3,8,10,11,13,14,15,16}.
```

Both sets have

```text
Phi_4(S) = Phi_4(T) = (8,12,13,7).
```

For the monomial-prefix word

```text
U_c(X) = X^10 - 8 X^9 + 12 X^8 - 13 X^7 + 7 X^6
        = X^10 + 9 X^9 + 12 X^8 + 4 X^7 + 7 X^6 in F_17[X],
```

the polynomials

```text
P_S = U_c - L_S,  P_T = U_c - L_T,
L_A = product_{x in A} (X - x),
```

have degree `< k = 6`. Thus both are Reed-Solomon codewords agreeing with
`U_c` on their respective `10`-point supports, exactly as in
`tex/slackMCA_v3.tex` `prop:monomial-fiber`.

## Route Cut

This is a useful obstruction, not a large-list counterexample. At this toy
point the maximum prefix fiber has size only `2`, so the polynomial local-limit
shape survives. What fails is a no-collision proof strategy:

```text
entropy clears + quotient cores absent => aperiodic prefix map is injective.
```

The surviving L1 target must allow isolated finite-field aperiodic collisions
and prove a multiplicity bound for them.

## Reproduction

```bash
python3 experimental/verify_l1_aperiodic_prefix_collision.py
python3 experimental/verify_l1_aperiodic_prefix_collision.py --format json
```

The verifier enumerates all `8008` supports, recomputes the fiber histogram,
checks the example codewords, verifies the entropy and quotient-core ledgers,
checks that all forty nonsingleton fibers are not `M=8` or `M=16`
coset-union collisions, verifies that support-prefix and complement-prefix
partitions agree for all supports, checks the exact divisor-gap
parametrization, certifies the divisor-gap graph component profile, checks the
co-large packing, recursive Johnson packing, and field-size upper bounds,
checks the growing-width co-large envelope, rational Plotkin bounds, and
their exact support-side Johnson-threshold form on deterministic parameter
grids, records the Plotkin defect decomposition for nonsingleton fibers,
checks the affine Reed-Solomon list reduction by enumerating all `17^2`
low-degree perturbations for every prefix fiber, verifies the co-large fiber
separation, records the internal ordered exchange and maximum codegree
profiles, verifies zero internal M1 high-overlap correction, and certifies the
three complement-locator dilation orbits.
