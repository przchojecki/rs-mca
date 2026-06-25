# L2 Sharp Interleaved-List Target

- **Status:** CONJECTURAL TARGET / FALSIFICATION PROTOCOL.
- **Agent/model:** Codex acting autonomously.
- **Date:** 2026-06-24.
- **Scope:** L2 in `agents.md`: sharp interleaved-list constants near capacity.
  This note builds on `l2_interleaved_support_bridge.md`,
  `l2_exact_support_diagonalization.md`, and
  `l2_interleaved_dilation_constants.md`. It is related to the active X1/L2
  bridge PR #101, but is intended as a standalone exact target statement.

## Purpose

The previous L2 notes show that column-distance interleaving is governed by
common agreement supports, not by the Cartesian product of row lists. The
remaining target should therefore not be phrased as "prove polynomiality" in
isolation: for fixed interleaving arity `mu`, an L1 base-list bound already gives
the weaker polynomial estimate

```text
Lst(Int(C,mu),1-a/n) <= Lst(C,1-a/n)^mu.
```

The useful L2 target is sharper. It asks for the random simultaneous-support
term and the quotient-core packet to be charged once, diagonally, with only a
polynomial codegree/over-agreement error. In particular, it should avoid the
spurious Cartesian numerator

```text
binom(n,a)^mu q^(-mu(a-k)).
```

## 1. Setup

Let `H <= F_q^*` be a cyclic domain of order `n`, and let

```text
C = RS[F_q,H,k]
```

be the Reed-Solomon code of evaluations of polynomials of degree `< k`. Fix
an agreement threshold

```text
a = k + sigma,        a >= k,
```

and a fixed protocol arity `mu >= 2`. For a `mu`-row received word

```text
U = (U_1,...,U_mu) in (F_q^H)^mu,
```

write

```text
Lambda_mu(U,a)
  = { (c_1,...,c_mu) in C^mu :
      |{x in H : c_i(x)=U_i(x) for every i}| >= a }.
```

The worst-case interleaved list size is

```text
Lst_mu(H,k,a;q) = max_U |Lambda_mu(U,a)|.
```

For one row `V:H -> F_q`, define the full agreement support of a codeword

```text
A_V(c) = {x in H : c(x)=V(x)}
```

and the full-support family

```text
Supp_V^{>=a} = { A_V(c) : c in C, |A_V(c)| >= a }.
```

The support bridge proves the exact formula

```text
|Lambda_mu(U,a)|
 =
 |{(A_1,...,A_mu) :
      A_i in Supp_{U_i}^{>=a},
      |A_1 cap ... cap A_mu| >= a }|.
```

This is the object to bound.

The working generated-field reserve for this version is:

```text
q <= n^Cq,
mu sigma log_2(q) >= (1+epsilon) log_2 binom(n,a),
sigma >= C0 n/log n,
```

with fixed constants `epsilon>0`, `Cq`, and `C0`. The last inequality is the
same coarse high-slack guard used in the L1 proof program; later protocol
specialization may replace it with the exact corrected reserve.

## 2. Explicit all-remainder quotient budget

This version makes the quotient term concrete for every quotient scale, including
dimension-dithered cases where `M` need not divide `k`. Put `sigma=a-k`. For
every subgroup fiber size

```text
M | n,        M > sigma,        M >= 2,
```

put

```text
N = n/M,        Q = N-1,
ell_M = floor(a/M),        u_M = a - M ell_M        (0 <= u_M < M).
```

For a slack-overlap parameter `0 <= tau < M`, define

```text
h_M(a,tau) = max(0, ceil((a-tau)/M)).
```

For `R,b >= 0`, let

```text
E_empty(R,b,mu)
  = sum_{j=0}^b (-1)^j binom(R,j) binom(R-j,b-j)^mu.
```

This counts ordered `mu`-tuples of `b`-subsets of an `R`-set with empty common
intersection. The all-remainder aligned quotient-core packet at scale `M` is

```text
L_{M,mu}(a,tau)
  = sum_{c=h_M(a,tau)}^ell_M
      binom(Q,c) E_empty(Q-c,ell_M-c,mu),
```

with the value read as `0` if `h_M(a,tau)>ell_M`.

The reason this is the right dithered quotient packet is the following
degree-cancellation lemma. Choose one `M`-coset `C_0`, a set
`T subset C_0` with `|T|=u_M`, and an `ell_M`-subset `A` of the remaining
quotient cosets. Let `U_A` be the union of those full cosets and

```text
L_T(X) = prod_{t in T}(X-t),
L_A(X) = prod_{alpha in A}(X^M-alpha),
Y(X) = X^{M ell_M} L_T(X).
```

Then

```text
P_A(X) = Y(X) - L_T(X)L_A(X)
       = L_T(X)(X^{M ell_M}-L_A(X))
```

has degree `<k`: indeed `X^{M ell_M}-L_A(X)` has degree at most
`M(ell_M-1)`, so

```text
deg P_A <= u_M + M(ell_M-1) = a-M = k+sigma-M < k.
```

On `T union U_A`, either `L_T` or `L_A` vanishes, so `P_A` agrees with `Y` on
the advertised quotient-core support of size `a` (and possibly more points).
Thus the divisible case `M|k` is only the special case `ell_M=k/M` and
`u_M=sigma`; if `M` does not divide `k`, the partial omitted coset has size
`u_M=a mod M`.

In the residue-moment formulation below, this same packet is an explicit
zero-moment solution. For

```text
S = T union U_A,        L_S(X)=L_T(X)L_A(X),
```

the degree-`<a` interpolant of the word `Y` on `S` is exactly

```text
Y(X)-L_S(X) = P_A(X),
```

because the two polynomials agree with `Y` on the roots of `L_S` and both have
degree `<a`. Since `deg P_A<k`, all top syndromes vanish, equivalently

```text
R_j(Y,S)=0        for every 0 <= j < sigma.
```

Thus `Quot_rem_mu` is charging an explicit structured family inside the same
simultaneous zero-moment locus as the regular-core problem; the residual
aperiodic target is the zero-moment locus after these quotient packets are
removed or budgeted.

For interleaving, if row `i` has partial set `T_i` and quotient subset `A_i`,
then the common agreement size is

```text
|T_1 cap ... cap T_mu| + M |A_1 cap ... cap A_mu|.
```

So the same `E_empty` formula counts the packet. Since the partial sets have
size `u_M`, the actual overlap satisfies `0 <= tau <= u_M`. Define the
conservative all-remainder quotient budget

```text
Quot_rem_mu(n,k,a)
  = sum_{M | n, M>sigma, M>=2}
      max_{0 <= tau <= u_M} L_{M,mu}(a,tau),
```

omitting terms with `ell_M=0` or `ell_M>Q`. This is a budget, not a
disjointness claim: it may overcount overlapping quotient packets. Its value is
explicit and finite. At the aligned endpoint `tau=u_M`, one has
`h_M(a,u_M)=ell_M`, hence

```text
L_{M,mu}(a,u_M) = binom(Q,ell_M),
```

not `binom(Q,ell_M)^mu`. The previous divisible-only budget is the sub-sum over
scales with `M|k`; the all-remainder form is the budget used in the target
below.

There is also a closed active-scale criterion. In the nontrivial list-decoding
range `a<n`, the omissions `ell_M=0` and `ell_M>Q` mean exactly that an
all-remainder packet at scale `M` is nonempty iff

```text
M | n,        a-k < M <= a.
```

Indeed, `ell_M=floor(a/M)` is nonzero iff `M<=a`, while
`ell_M<=Q=n/M-1` follows automatically from `a<n` and `M|n`. Thus ordinary
dimension dithering by making `M` fail to divide `k` does not remove these
arbitrary-word quotient packets. The relevant clearance condition for this
all-remainder budget is instead interval-divisor clearance: no divisor of `n`
should lie in `(a-k,a]`, unless the resulting packet is explicitly charged to
`Quot_rem_mu`.

For dyadic domains this becomes especially transparent. If `n` is a power of
two and

```text
M_*(sigma) = min {2^j : 2^j > sigma},
```

then all all-remainder quotient packets are absent iff

```text
a < M_*(sigma).
```

Equivalently, with `a=k+sigma`, one needs `k < M_*(sigma)-sigma`. Small
dimension dithers usually do not meet this condition; they only move the upper
endpoint `a` of the active interval.

### Leading-term exactness

Two elementary facts explain why the two non-polynomial terms in V0 have the
displayed shape.

**Lemma (random simultaneous-fiber mean).** If the rows
`U_1,...,U_mu` are independent uniform functions `H -> F_q`, then

```text
E |Fib_U^cap(a)| = binom(n,a) q^{-mu(a-k)}.
```

Moreover, for the exact-row regular core,

```text
E Reg_mu(U,a)
 = binom(n,a) q^{-mu(a-k)} (1-1/q)^{mu(n-a)}.
```

In particular the first term in V0 is the exact random mean of the relaxed
simultaneous fiber and an upper envelope for the exact regular mean.

*Proof.* Fix an `a`-set `S subset H`. The restrictions to `S` of degree-`<k`
polynomials form a `k`-dimensional subspace of `F_q^S`, since `a>=k`.
Therefore a uniform row `U_i` is feasible on `S` with probability
`q^k/q^a=q^{-(a-k)}`. The rows are independent, so the probability that `S`
lies in `Fib_U^cap(a)` is `q^{-mu(a-k)}`. Summing over the `binom(n,a)`
possible sets `S` proves the first formula.

For exact regularity, after `U_i|_S` is feasible there is a unique row codeword
`c_{i,S}` agreeing with it on `S`. At each point of `H \ S`, the independent
uniform value `U_i(x)` must avoid the single value `c_{i,S}(x)`, which has
probability `1-1/q`. These outside conditions are independent over rows and
points. Summing again over `S` gives the displayed exact-regular mean.

The first nontrivial correlation in this random model is also exact.

**Lemma (support-pair rank and random second moment).** Fix two `a`-sets
`S,T subset H`, put `r=|S cap T|`, and let `U:H -> F_q` be a uniform random
row. Then

```text
Pr[S,T in Fib_U(a)]
 = q^{-2(a-k)}                  if r < k,
 = q^{-(2a-r-k)}                if r >= k.
```

For `mu` independent rows, the same probability is raised to the `mu`-th power.
Consequently

```text
E |Fib_U^cap(a)|^2
 = sum_{r=0}^a
     binom(n,a) binom(a,r) binom(n-a,a-r)
     q^{-mu(2a-r-2k+min(r,k))}.
```

Thus two candidate supports behave independently until their intersection has
size at least `k`; the only random-model pair surplus is the explicit factor
`q^{mu(r-k)}` from high-overlap pairs.

*Proof.* The condition `S in Fib_U(a)` says that `U|_S` lies in the
`k`-dimensional Reed-Solomon restriction space on `S`; similarly for `T`.
Equivalently, on `S union T` there must be two degree-`<k` polynomials
`P,Q` such that `U|_S=P|_S`, `U|_T=Q|_T`, and `P=Q` on `S cap T`.

The pair `(P,Q)` has `2k` coefficients. The equality on `S cap T` imposes
`min(r,k)` independent conditions, because a nonzero degree-`<k` polynomial
cannot vanish on `k` distinct points. Since `a>=k`, evaluation on `S` and `T`
separately determines `P` and `Q`; hence the resulting subspace of
`F_q^{S union T}` has dimension

```text
2k - min(r,k).
```

The ambient union has size `2a-r`, so the probability for one row is

```text
q^{(2k-min(r,k))-(2a-r)}
 = q^{-(2a-r-2k+min(r,k))},
```

which is the displayed two-case formula. Independence over rows gives the
`mu`-row probability. Finally, the number of ordered pairs `(S,T)` with
`|S|=|T|=a` and `|S cap T|=r` is
`binom(n,a) binom(a,r) binom(n-a,a-r)`, giving the second-moment identity.

For larger collections the exact rank depends on low-overlap consistency
relations, but the high-overlap part has a clean universal bound.

**Lemma (high-overlap cluster-rank bound).** Let `S_1,...,S_m` be `a`-subsets
of `H`. Form a graph `G_k` on `{1,...,m}` by joining `i` and `j` when

```text
|S_i cap S_j| >= k.
```

Let `c(G_k)` be the number of connected components and put
`V= S_1 union ... union S_m`. For one uniform random row,

```text
Pr[S_1,...,S_m in Fib_U(a)] <= q^{k c(G_k)-|V|}.
```

For `mu` independent rows, the right-hand side is raised to the `mu`-th power.

*Proof.* If a row is feasible on every `S_i`, choose degree-`<k` polynomials
`P_i` with `U|_{S_i}=P_i|_{S_i}`. Along an edge of `G_k`, the polynomials
`P_i` and `P_j` agree on at least `k` points, hence are identical. Therefore
all vertices in one connected component use the same polynomial. Thus the set
of feasible value assignments on `V` lies in the image of a linear map from at
most one degree-`<k` polynomial per component, a vector space of dimension
`k c(G_k)`. The ambient space has dimension `|V|`, which gives the probability
bound. Independence gives the `mu`-row version.

This lemma is deliberately an upper bound. It is tight for a single connected
high-overlap cluster, but low-overlap intersections between different
components can only add further linear consistency conditions. Its value is
that any super-random regular-core obstruction must organize many supports into
large high-overlap clusters, a much narrower structure than an arbitrary
Cartesian product of support fibers.

There is one immediate refinement that is useful for avoiding a false product
factorization across components. Start from the connected components of `G_k`.
If two current components have unions whose intersection has size at least `k`,
merge them, and iterate until no such pair remains. Call the resulting partition
the **`k`-closure** of the support tuple, and write `c_cl` for its number of
parts. Then

```text
Pr[S_1,...,S_m in Fib_U(a)] <= q^{k c_cl-|V|}
```

for one random row, and the `mu`-row version is obtained by raising the right
side to the `mu`-th power.

Indeed, each original high-overlap component already uses one polynomial. If
two component unions meet in at least `k` points, the two corresponding
degree-`<k` polynomials agree on at least `k` points and hence are identical.
Iterating gives at most one polynomial per `k`-closed part. This is strictly
stronger than using the raw connected components when low-overlap components
have large aggregate overlap across their unions.

For a full tuple this gives the following global exponent ledger. Let
`C_1,...,C_c` be the `k`-closed parts, let

```text
V_j = union_{i in C_j} S_i,        V = union_{j=1}^c V_j,
```

and define the global excess

```text
D = |V| - ac.
```

Then for one random row

```text
Pr[S_1,...,S_m in Fib_U(a)] <= q^{-(c(a-k)+D)}.
```

For `mu` independent rows, the exponent is multiplied by `mu`. Thus each
`k`-closed part contributes one diagonal-scale factor `q^{-(a-k)}`, and the
global excess `D` records the remaining correction. Positive `D` is genuine
union excess and pays extra entropy. Negative `D` is possible only because
different `k`-closed component unions may still overlap in fewer than `k`
points; it is a low-overlap cross-component correction, not a high-overlap
cluster. This is why the note does not claim a clean product factorization
across raw components.

The low-overlap correction can itself be recorded exactly as a linear rank.
For each closed part `C_alpha`, introduce one degree-`<k` polynomial
`P_alpha`. Whenever a domain point lies in two closed-part unions
`V_alpha` and `V_beta`, impose the linear equality

```text
P_alpha(x) = P_beta(x).
```

Let `r_cross` be the rank, over `F_q`, of all these cross-part equality
constraints on the `c k` polynomial coefficients.

**Lemma (rank-corrected closure ledger).** With notation as above, for one
random row

```text
Pr[S_1,...,S_m in Fib_U(a)]
  <= q^{-(c(a-k)+D+r_cross)}.
```

For `mu` independent rows, the exponent is multiplied by `mu`.

*Proof.* After `k`-closure, every closed part uses at most one degree-`<k`
polynomial. Thus the polynomial choices start in a vector space of dimension
`ck`. Since `U` is a single function on the union `V`, two closed-part
polynomials must give the same value at every point where their unions meet.
By definition these cross-part equalities have rank `r_cross`, so the feasible
value assignments on `V` lie in a space of dimension at most `ck-r_cross`.
Dividing by the ambient `q^{|V|}` assignments gives

```text
q^{ck-r_cross-|V|}
 = q^{-(c(a-k)+D+r_cross)}.
```

This rank correction explains exactly what the negative `D` entries measure:
they are not a new high-overlap component, but they must be paired with the
linear constraints forced by sharing actual domain points.

There is a clean case where this correction fully cancels the low-overlap
defect. Form the overlap graph on the `k`-closed parts by joining
`alpha,beta` when `V_alpha cap V_beta` is nonempty.

**Corollary (forest overlap factorization).** If this closed-part overlap graph
is a forest, then

```text
r_cross = sum_{alpha beta edge} |V_alpha cap V_beta|
```

and therefore

```text
D+r_cross = sum_{alpha=1}^c (|V_alpha|-a) >= 0.
```

In particular, two `k`-closed parts never create a residual negative correction
after the rank ledger; the first possible obstruction to closed-part
factorization is a low-overlap cycle among at least three closed parts.

*Proof.* Since the parts are `k`-closed, every edge intersection has size
`<k`. Root each tree and eliminate leaves. A leaf part meets the rest of its
tree only through its unique neighbor, so its cross constraints are evaluations
of one degree-`<k` polynomial at fewer than `k` distinct points; these
constraints are independent. Removing the leaf and iterating gives the stated
rank sum. A forest has no triple-overlap point across three distinct vertices
and no non-edge intersections, so the usual inclusion-exclusion for the union
has no cycle correction:

```text
|V| = sum_alpha |V_alpha|
      - sum_{alpha beta edge} |V_alpha cap V_beta|.
```

Substituting this identity into `D=|V|-ac` gives
`D+r_cross=sum_alpha(|V_alpha|-a)`.

The forest hypothesis is real: cyclic low-overlap overlaps can leave a
rank-corrected surplus over product-diagonal behavior.

**Counterexample to naive closed-part factorization.** Let `k>=4`, let
`A,B,C subset H` be pairwise disjoint sets of size `k-1`, and put

```text
S_1 = A union B,        S_2 = A union C,        S_3 = B union C.
```

Set `a=2(k-1)`. Then every pairwise intersection has size `k-1<k`, so the
`k`-closure has three singleton parts. Moreover

```text
|S_1 union S_2 union S_3| = 3(k-1),        D = -3(k-1).
```

Assume the locator ratio `L_A/L_B` is not constant on `C`. Then the
cross-component equality rank is

```text
r_cross = 2k,
```

and hence

```text
D+r_cross = 3-k < 0.
```

The rank-corrected exponent is therefore

```text
c(a-k)+D+r_cross = 2k-3,
```

whereas the product of three diagonal closed parts would have exponent
`3(a-k)=3k-6`. Thus the cyclic low-overlap triangle carries a surplus factor
`q^{k-3}` over product-diagonal factorization.

*Proof.* Write the three closed-part polynomials as `P_1,P_2,P_3`. The
condition on `A=S_1 cap S_2` says that

```text
P_2-P_1 = lambda L_A
```

for some scalar `lambda`, since `P_2-P_1` has degree `<k` and vanishes on the
`k-1` points of `A`. Similarly

```text
P_3-P_1 = mu L_B.
```

The remaining equality on `C=S_2 cap S_3` requires

```text
lambda L_A(x) - mu L_B(x) = 0        for every x in C.
```

Since `L_A/L_B` is not constant on `C`, this forces `lambda=mu=0`. Thus
`P_1=P_2=P_3`, and the solution space has dimension `k` inside the original
`3k` polynomial coefficients. Hence the cross-rank is `3k-k=2k`, giving the
displayed exponents.

This counterexample does not threaten L2-Sharp V0 by itself; it only rules out
one overly optimistic proof step. It says that after the forest ledger, the
remaining regular-core cluster route must count or rank-control cyclic
low-overlap closed-part diagrams rather than factor them independently.

For the generic triangle family above, this counting is favorable. Put
`r=k-1`, so `a=2r`, and consider labeled triples of the displayed form. Their
number is exactly

```text
binom(n,r) binom(n-r,r) binom(n-2r,r),
```

and the rank-corrected exponent exceeds the diagonal first-moment exponent
`a-k=r-1` by exactly `r`. Therefore their total random-model contribution to
the third moment, divided by the diagonal first-moment scale, is

```text
  binom(n,r) binom(n-r,r) binom(n-2r,r)
  -------------------------------------------------  q^{-mu r}.
                  binom(n,2r)
```

If `a>=rho_0 n`, then this is at most

```text
(27 rho_0^{-1} q^{-mu})^r.
```

Thus the generic cyclic triangle is not itself a random-model obstruction in
the polynomial-field window once `q^mu>27/rho_0`; the remaining cyclic problem
is to classify and count lower-rank, more structured cycles such as constant
locator-ratio configurations.

*Proof.* The labeled blocks `A,B,C` are recovered uniquely from the ordered
triple by pairwise intersections, so the displayed count is exact. The
exponent difference is

```text
(2k-3) - (a-k) = (2r-1) - (r-1) = r.
```

For the coarse bound, write the count as

```text
binom(n,3r) (3r)!/(r!)^3.
```

After division by `binom(n,2r)`, the first factor ratio is at most
`rho_0^{-r}` when `2r=a>=rho_0 n`, and the multinomial factor is at most
`3^{3r}=27^r`.

The first such lower-rank structured cycle also has a direct count.

**Lemma (constant-ratio triangle count).** Keep the notation
`r=k-1`, `a=2r`, and

```text
S_1=A union B,        S_2=A union C,        S_3=B union C
```

with `A,B,C` pairwise disjoint `r`-sets. Suppose the locator ratio
`L_A/L_B` is constant on `C`. Then this subfamily has at most

```text
(q-2) binom(n,r) binom(n-r,r)
```

ordered triples. Its rank-corrected exponent is `2r-2`, so its contribution
to the random-model third moment, divided by the diagonal first-moment scale,
is at most

```text
(q-2) binom(2r,r) q^{-mu(r-1)}.
```

In particular, for fixed `mu` this constant-ratio subfamily is exponentially
below diagonal once `r` grows linearly with `n` and the generated field is in
the polynomial window.

*Proof.* Let the constant value of `L_A/L_B` on `C` be `gamma`. Since
`A` and `B` are disjoint, `gamma` cannot be `1`: otherwise `L_A-L_B`, a
polynomial of degree at most `r-1`, would vanish on the `r` points of `C`, so
`L_A=L_B`. For fixed ordered disjoint `A,B` and fixed
`gamma in F_q^* \ {1}`, the set `C` is contained in the roots of

```text
L_A(X) - gamma L_B(X),
```

a degree-`r` polynomial. Hence there is at most one possible `r`-set `C`.
This gives the count bound.

In the rank calculation from the previous counterexample, constant ratio gives
one free scalar relation between `lambda` and `mu`, so the solution space has
dimension `k+1` and `r_cross=2k-1=2r+1`. Therefore

```text
c(a-k)+D+r_cross = 3(r-1)-3r+(2r+1) = 2r-2.
```

The diagonal exponent is `a-k=r-1`. Dividing the count bound by
`binom(n,2r)` and multiplying by `q^{-mu(r-1)}` gives the displayed relative
bound, using

```text
binom(n,r) binom(n-r,r) = binom(n,2r) binom(2r,r).
```

Combining the two cases clears the whole symmetric three-block cycle family.

**Corollary (symmetric cyclic triangle clearance).** With the same notation,
the total contribution of all ordered triples

```text
(A union B, A union C, B union C)
```

with pairwise disjoint `r`-sets `A,B,C` to the random-model third moment,
divided by the diagonal first-moment scale, is at most

```text
  binom(n,r) binom(n-r,r) binom(n-2r,r)
  -------------------------------------------------  q^{-mu r}
                  binom(n,2r)

  + (q-2) binom(2r,r) q^{-mu(r-1)}.
```

If `a=2r>=rho_0 n`, this is at most

```text
(27 rho_0^{-1} q^{-mu})^r
  + (q-2) 4^r q^{-mu(r-1)}.
```

In particular, for fixed arity `mu>=2`, generated field size `q=poly(n)`, and
linear `r`, the full symmetric low-overlap triangle family is below the
diagonal scale.

*Proof.* Split the family according to whether `L_A/L_B` is constant on `C`.
For the nonconstant part, use the generic triangle rank `2k` and bound the
number of triples by the full labeled count. For the constant part, use the
constant-ratio count and its exponent `2r-2`. The displayed estimates are
exactly the two relative bounds just proved. Finally,
`binom(2r,r)<=4^r`.

The same mechanism clears the full-rank part of every fixed cyclic necklace.

**Corollary (full-rank cyclic necklace clearance).** Fix `m>=3`, put
`r=k-1` and `a=2r`, and let `E_1,...,E_m` be pairwise disjoint `r`-subsets of
`H`, with indices taken modulo `m`. Define

```text
S_i = E_i union E_{i+1}.
```

Let `L_i` be the locator polynomial of `E_i`. Assume that
`L_1,...,L_m` are linearly independent in the degree-`<k` polynomial space
(in particular `m<=k`). Then the cyclic tuple has rank-corrected exponent

```text
(m-1)r - 1,
```

so its exponent gap over the diagonal first-moment exponent `a-k=r-1` is

```text
(m-2)r.
```

Consequently the total contribution of all ordered full-rank `m`-necklaces,
divided by the diagonal first-moment scale, is at most

```text
  prod_{j=0}^{m-1} binom(n-jr,r)
  -------------------------------- q^{-mu (m-2)r}.
             binom(n,2r)
```

If `2r=a>=rho_0 n` and `mr<=n`, this is bounded by

```text
(m^m rho_0^{-(m-2)} q^{-mu(m-2)})^r.
```

For fixed `m` and generated-field size polynomial in `n`, this is below the
diagonal scale when `r` is linear in `n`. Thus the low-overlap cyclic issue is
not all cycles: after the triangle, every fixed full-rank cyclic necklace is
also count-cleared. The remaining cyclic obstruction is the structured
rank-deficient case, where the edge-block locator span has dimension `<m`.

*Proof.* Since `|S_i cap S_{i-1}|=r=k-1`, the equality of the closed-part
polynomials on `E_i` gives

```text
P_i - P_{i-1} = lambda_i L_i
```

for some scalar `lambda_i`. Summing around the cycle gives

```text
sum_i lambda_i L_i = 0.
```

By the full-rank assumption all `lambda_i` vanish, so
`P_1=...=P_m`. Hence the feasible polynomial choices have dimension `k`
inside the original `mk` coefficients, and

```text
r_cross = mk-k = (m-1)k.
```

The `k`-closure has `m` singleton parts, the union size is `mr`, and the global
excess is `D=mr-ma=-mr`. Therefore

```text
c(a-k)+D+r_cross
  = m(r-1)-mr+(m-1)(r+1)
  = (m-1)r-1.
```

Subtracting the diagonal exponent `r-1` gives the gap `(m-2)r`.

The ordered block count is

```text
prod_{j=0}^{m-1} binom(n-jr,r).
```

Dividing by `binom(n,2r)` and multiplying by the entropy gain
`q^{-mu(m-2)r}` gives the displayed relative contribution. For the coarse
bound, rewrite the block count as

```text
binom(n,mr) (mr)!/(r!)^m.
```

The multinomial factor is at most `m^{mr}`. Also

```text
binom(n,mr)/binom(n,2r) <= (n/(2r))^{(m-2)r}
                         <= rho_0^{-(m-2)r},
```

because `2r>=rho_0 n`. This proves the stated bound.

The complementary rank-deficient necklaces can also be counted directly.

**Lemma (rank-deficient cyclic necklace count).** Keep the notation of the
previous corollary. Let `R=rank span(L_1,...,L_m)`. The rank-corrected exponent
gap over the diagonal first-moment exponent is

```text
(m-2)r + R - m.
```

If `R<m`, then the number of ordered rank-deficient `m`-necklaces is at most

```text
m q^{m-2} prod_{j=0}^{m-2} binom(n-jr,r).
```

Moreover `R>=2`, and hence their total contribution divided by the diagonal
first-moment scale is at most

```text
  m q^{m-2} prod_{j=0}^{m-2} binom(n-jr,r)
  ------------------------------------------------ q^{-mu (m-2)(r-1)}.
                    binom(n,2r)
```

If `2r=a>=rho_0 n` and `(m-1)r<=n`, this is bounded by

```text
m q^{(mu+1)(m-2)}
  ((m-1)^{m-1} rho_0^{-(m-3)} q^{-mu(m-2)})^r.
```

Thus, for fixed `m`, fixed arity `mu>=2`, generated field size polynomial in
`n`, and linear `r`, the rank-deficient fixed-length necklace contribution is
also below the diagonal scale.

*Proof.* The equations around the cycle have the form

```text
P_i - P_{i-1} = lambda_i L_i.
```

The cycle closes exactly when

```text
sum_i lambda_i L_i = 0.
```

If the locator span has rank `R`, the scalar choices
`(lambda_1,...,lambda_m)` have dimension `m-R`. After choosing `P_0`, all
other `P_i` are determined. Hence the feasible polynomial space has dimension
`k+m-R`, so

```text
r_cross = mk - (k+m-R) = (m-1)k - m + R.
```

As above `D=-mr` and `c=m`, so the rank-corrected exponent is

```text
m(r-1)-mr+(m-1)(r+1)-m+R = (m-1)r+R-m-1.
```

Subtracting the diagonal exponent `r-1` gives
`(m-2)r+R-m`.

Now suppose `R<m`. There is a nonzero relation
`sum_i lambda_i L_i=0`; choose one pivot index with `lambda_j != 0` and
normalize `lambda_j=1`. Since every `L_i` is monic, the leading coefficient
condition is

```text
sum_{i != j} lambda_i = -1.
```

For fixed pivot `j`, there are `q^{m-2}` choices of the remaining coefficients.
Choose the other `m-1` disjoint edge blocks in at most

```text
prod_{j=0}^{m-2} binom(n-jr,r)
```

ways. The pivot locator is then forced:

```text
L_j = - sum_{i != j} lambda_i L_i.
```

This polynomial has at most one possible `r`-element root set in `H`, and often
none. Multiplying by the `m` pivot choices gives the displayed count bound.

Finally, `R` cannot be `1`: all locator polynomials are monic, so a
one-dimensional span would make them all equal, contradicting disjoint
nonempty edge blocks. Thus `R>=2`, and the exponent gap is at least
`(m-2)(r-1)`. Combining this with the count bound gives the displayed
diagonal-relative contribution. For the coarse estimate, write the
`m-1`-block count as

```text
binom(n,(m-1)r) ((m-1)r)!/(r!)^{m-1}.
```

The multinomial factor is at most `(m-1)^{(m-1)r}`, and

```text
binom(n,(m-1)r)/binom(n,2r) <= (n/(2r))^{(m-3)r}
                             <= rho_0^{-(m-3)r}.
```

The remaining factor
`q^{m-2} q^{mu(m-2)}=q^{(mu+1)(m-2)}` comes from replacing
`q^{-mu(m-2)(r-1)}` by `q^{mu(m-2)}q^{-mu(m-2)r}`.

Combining the full-rank and rank-deficient estimates clears the fixed-length
edge-block necklace family:

**Corollary (fixed-length cyclic necklace clearance).** Fix `m>=3`. In the
model

```text
S_i=E_i union E_{i+1},       |E_i|=k-1,       a=2(k-1),
```

with pairwise disjoint edge blocks, the total contribution of all ordered
`m`-necklaces is below the diagonal first-moment scale for fixed arity
`mu>=2`, generated field size polynomial in `n`, and `k-1` linear in `n`.

This closes the cyclic necklace subfamily left by the forest-overlap ledger.
It does not yet classify arbitrary cyclic low-overlap diagrams: the remaining
regular-core cluster work is to reduce more general cyclic diagrams to
edge-block necklaces or count their own dependency loci.

The necklace computation is a special case of an exact rank formula for clean
simple cycles.

**Lemma (clean simple-cycle rank formula).** Let `S_0,...,S_{m-1}` be distinct
`a`-subsets forming a clean low-overlap cycle: indices are modulo `m`,

```text
E_i = S_i cap S_{i+1}
```

has size `e_i` with `0<e_i<k`, the edge sets `E_i` are pairwise disjoint, and
there are no other intersections among the `S_i`. Put

```text
W_i = { Q in F_q[X]_{<k} : Q|_{E_i}=0 }.
```

Let

```text
R_cyc = dim(W_0 + ... + W_{m-1}).
```

Then the cross-component equality rank is

```text
r_cross = sum_i e_i + R_cyc - k.
```

Consequently the rank-corrected random-row exponent is

```text
m(a-k) + R_cyc - k,
```

and its gap over the diagonal first-moment exponent `a-k` is

```text
(m-1)(a-k) + R_cyc - k.
```

Thus every clean simple cyclic low-overlap diagram is controlled exactly by the
single subspace-rank invariant `R_cyc`. The equal edge-block necklace is the
case `e_i=k-1` and `W_i=<L_i>`, so `R_cyc` is precisely the locator-span rank
used above.

*Proof.* Since all edge intersections have size `<k` and there are no other
intersections, the `k`-closure has `m` singleton parts. Also

```text
|S_0 union ... union S_{m-1}| = ma - sum_i e_i,
```

so `D=-sum_i e_i`. Write the closed-part polynomials as
`P_0,...,P_{m-1}`. The equality condition on `E_i` is exactly

```text
P_{i+1}-P_i in W_i.
```

Set `Delta_i=P_{i+1}-P_i`. After choosing `P_0`, the tuple is determined by
`(Delta_0,...,Delta_{m-1})`, and the only cycle-closing condition is

```text
Delta_0 + ... + Delta_{m-1} = 0.
```

The kernel of the sum map

```text
W_0 x ... x W_{m-1} -> F_q[X]_{<k}
```

has dimension

```text
sum_i dim W_i - R_cyc = sum_i (k-e_i) - R_cyc.
```

Therefore the feasible polynomial space has dimension

```text
k + sum_i(k-e_i) - R_cyc.
```

Subtracting this from the original `mk` polynomial coefficients gives

```text
r_cross
  = mk - (k + sum_i(k-e_i) - R_cyc)
  = sum_i e_i + R_cyc - k.
```

The rank-corrected closure ledger then gives exponent

```text
m(a-k) + D + r_cross
  = m(a-k) - sum_i e_i + sum_i e_i + R_cyc - k
  = m(a-k) + R_cyc - k.
```

Subtracting the diagonal exponent `a-k` gives the stated gap.

There is an equivalent dual form that makes the remaining dependency locus more
concrete.

**Lemma (dual form of the clean-cycle defect).** Let `V=F_q[X]_{<k}` and, for
each edge set `E_i`, let

```text
U_i = span{ ev_x : x in E_i } subset V^*
```

where `ev_x(Q)=Q(x)`. Then

```text
k - R_cyc = dim(U_0 cap ... cap U_{m-1}).
```

Equivalently, `R_cyc<k` exactly when there is a nonzero linear functional on
degree-`<k` polynomials that can be represented by weights supported on every
edge overlap `E_i`.

*Proof.* By definition `W_i` is the kernel of the evaluation map on `E_i`.
Since `e_i<k`, the evaluations at points of `E_i` are linearly independent on
`V`, so the annihilator of `W_i` in `V^*` is exactly `U_i`. Therefore

```text
(W_0+...+W_{m-1})^perp = U_0 cap ... cap U_{m-1}.
```

Taking dimensions in the `k`-dimensional space `V` gives the identity.

The dual form gives a projective incidence reduction for counting the
rank-deficient clean cycles. For `1<=e<k` and a projective nonzero functional
`[ell] in P(V^*)`, define

```text
N_e([ell]) =
  #{ E subset H : |E|=e and ell in span{ev_x : x in E} }.
```

**Corollary (functional-incidence count for clean-cycle defects).** Fix edge
sizes `e_0,...,e_{m-1}`. The number of ordered edge-block tuples
`(E_0,...,E_{m-1})` that can occur in a rank-deficient clean cycle is at most

```text
sum_{[ell] in P(V^*)} prod_{i=0}^{m-1} N_{e_i}([ell]).
```

The same bound remains valid after imposing the disjointness conditions on the
edge blocks, since it only overcounts. The private points in the clean cycle can
then be counted separately; the rank defect depends only on the edge blocks.

Moreover, if the same nonzero functional has two disjoint representations on
`E` and `F` with `|E|=e`, `|F|=f`, then

```text
e+f>k.
```

*Proof.* If a clean cycle is rank-deficient, the dual lemma gives a nonzero
functional `ell` lying in every edge span `U_i`. Passing to the projective
class `[ell]`, each edge block `E_i` is counted by `N_{e_i}([ell])`, giving the
displayed upper bound.

For the last claim, suppose `ell` has representations supported on disjoint
sets `E` and `F`. Subtracting these two representations gives a nontrivial
linear dependence among the evaluation functionals supported on
`E union F`. Reed-Solomon evaluation functionals on at most `k` distinct
points are independent, so this is impossible when `e+f<=k`.

The one-edge incidence mass is exact.

**Corollary (one-edge incidence mass).** For every `1<=e<k`,

```text
sum_{[ell] in P(V^*)} N_e([ell])
  = binom(n,e) (q^e-1)/(q-1).
```

Consequently, if clean rank-deficient edge-block tuples have fixed edge sizes
`e_0,...,e_{m-1}`, then for any distinguished index `t` their number is at most

```text
binom(n,e_t) (q^{e_t}-1)/(q-1)
  prod_{i != t} binom(n,e_i).
```

In particular, choosing an edge of minimum size `e_min` replaces the crude
projective-functional factor `(q^k-1)/(q-1)` by `(q^{e_min}-1)/(q-1)`. Thus a
clean cycle with a genuinely small edge gains a field-size saving of about
`q^{k-e_min}` before any further disjointness or minimal-support restrictions
are used.

*Proof.* Sum the incidence relation over edge sets instead of functionals. For
each fixed `e`-set `E`, the evaluation functionals `{ev_x:x in E}` are
independent because `e<k`; hence their span has dimension `e` and contains
exactly `(q^e-1)/(q-1)` projective nonzero functionals. Summing over the
`binom(n,e)` choices of `E` gives the identity. The edge-tuple bound follows
from the functional-incidence count by using this exact sum for the
distinguished edge and the trivial bound `N_{e_i}([ell])<=binom(n,e_i)` for
all remaining edges.

This immediately gives a clean-cycle support-tuple bound once the private
points are included. For a fixed clean cycle shape, write

```text
p_i = a-e_{i-1}-e_i
```

for the number of private points in `S_i`.

**Corollary (one-edge clean-cycle tuple bound).** Fix `m,a,k` and clean-cycle
edge sizes `e_0,...,e_{m-1}` with private sizes `p_i>=0`. The number of
ordered rank-deficient clean support tuples of this shape is at most

```text
  binom(n,e_t) (q^{e_t}-1)/(q-1)
  prod_{i != t} binom(n,e_i)
  prod_i binom(n,p_i)
```

for every distinguished edge `t`. In particular, choosing an edge of minimum
size `e_min` improves the crude projective-functional count

```text
  (q^k-1)/(q-1) prod_i binom(n,e_i) prod_i binom(n,p_i)
```

by the exact factor

```text
(q^{e_min}-1)/(q^k-1).
```

The estimate deliberately ignores disjointness among edge and private blocks,
so it is an upper bound for the clean tuples.

*Proof.* Apply the one-edge incidence mass to the distinguished edge, bound
each remaining edge block by `binom(n,e_i)`, and bound each private block by
`binom(n,p_i)`. The saving factor is the quotient of the distinguished-edge
projective factor `(q^{e_t}-1)/(q-1)` and the crude projective count
`(q^k-1)/(q-1)`.

Combining this support count with the two-edge rank lower bound gives a direct
diagonal comparison.

**Corollary (diagonal-relative one-edge clean-cycle bound).** Keep the notation
of the previous corollary, and put

```text
s_2 = min_{i<j} (e_i+e_j),       d_2=max(0,s_2-k).
```

For any distinguished edge `t`, the random-model contribution of
rank-deficient clean cycles of this fixed shape, divided by the diagonal
first-moment scale

```text
binom(n,a) q^{-mu(a-k)},
```

is at most

```text
  [ binom(n,e_t) (q^{e_t}-1)/(q-1)
    prod_{i != t} binom(n,e_i)
    prod_i binom(n,p_i)
    / binom(n,a) ]
  q^{-mu((m-1)(a-k)-d_2)}.
```

If a sharper lower bound `R_cyc>=k-d` is available for the same shape, the same
formula holds with `d` in place of `d_2`.

*Proof.* The clean-cycle rank formula gives exponent gap over the diagonal

```text
(m-1)(a-k) + R_cyc-k.
```

The two-edge lower bound gives `R_cyc>=k-d_2`, hence the gap is at least
`(m-1)(a-k)-d_2`. Multiplying the one-edge tuple bound by this probability
saving and dividing by `binom(n,a)` gives the displayed expression.

This criterion is intentionally coarse for symmetric triangles with all edge
sizes close to `k`; those are already cleared above by the generic and
constant-ratio triangle counts. Its role is to turn the one-edge incidence
saving into a quick clearance test for asymmetric or private-mass clean cycles,
and to isolate the remaining near-necklace regime that still needs sharper
incidence structure.

The first such sharpening is to use disjointness of two edge blocks.

**Corollary (two-edge disjoint incidence mass).** For disjoint edge sets
`E,F subset H` of sizes `e,f<k`, let

```text
U_E=span{ev_x:x in E},       U_F=span{ev_x:x in F}.
```

Then

```text
dim(U_E cap U_F)=max(0,e+f-k).
```

Consequently the number of ordered disjoint pairs `(E,F)` of sizes `(e,f)`,
together with a projective nonzero functional `[ell]` represented on both
edges, is exactly

```text
binom(n,e) binom(n-e,f) (q^{max(0,e+f-k)}-1)/(q-1).
```

In particular, this count is zero when `e+f<=k`.

*Proof.* Since Reed-Solomon evaluation functionals on at most `k` distinct
domain points are independent, the span of the evaluations on `E union F` has
dimension `min(k,e+f)`. Hence

```text
dim(U_E cap U_F)=dim U_E+dim U_F-dim(U_E+U_F)
               = e+f-min(k,e+f).
```

For each ordered disjoint pair, the common projective functionals are precisely
the nonzero projective points in this intersection, giving
`(q^d-1)/(q-1)` with `d=max(0,e+f-k)`. Summing over the
`binom(n,e)binom(n-e,f)` ordered disjoint pairs gives the formula.

For a fixed clean-cycle shape and two distinguished edge indices `s<t`, put

```text
d_{s,t}=max(0,e_s+e_t-k).
```

Then the number of ordered rank-deficient clean support tuples of this shape is
at most

```text
  binom(n,e_s) binom(n-e_s,e_t) (q^{d_{s,t}}-1)/(q-1)
  prod_{i notin {s,t}} binom(n,e_i)
  prod_i binom(n,p_i).
```

Combining with the clean-cycle exponent gap, their random-model contribution
relative to the diagonal first-moment scale is at most

```text
  [ binom(n,e_s) binom(n-e_s,e_t) (q^{d_{s,t}}-1)/(q-1)
    prod_{i notin {s,t}} binom(n,e_i)
    prod_i binom(n,p_i)
    / binom(n,a) ]
  q^{-mu((m-1)(a-k)-d_{s,t})}.
```

Choosing a pair minimizing `e_s+e_t` recovers the `d_2` loss in the two-edge
rank lower bound and gives the sharpest version of this coarse two-edge test.
It makes the small-pair obstruction exact: if two edge overlaps have total size
at most `k`, no rank-deficient clean cycle can use those two disjoint edge
blocks.

For three or more selected edges, the same idea must be rank-stratified: MDS
independence alone does not prevent locator dependencies among the selected
vanishing spaces.

**Corollary (rank-stratified multi-edge incidence sieve).** Let
`J subset {0,...,m-1}` be a set of selected clean-cycle edge indices. For
`j in J`, put

```text
W_j={Q in F_q[X]_{<k}: Q|_{E_j}=0},       U_j=span{ev_x:x in E_j}.
```

For a fixed selected edge tuple, set

```text
R_J = dim sum_{j in J} W_j.
```

Then the projective nonzero functionals represented on every selected edge are
exactly the projective points of `cap_{j in J} U_j`, and their number is

```text
(q^{k-R_J}-1)/(q-1).
```

Consequently, if `C_J(R)` denotes the number of ordered disjoint selected-edge
tuples of the prescribed sizes with `R_J=R`, then the number of
rank-deficient clean support tuples in that selected-rank stratum is at most

```text
  C_J(R) (q^{k-R}-1)/(q-1)
  prod_{i notin J} binom(n,e_i)
  prod_i binom(n,p_i).
```

Their random-model contribution relative to the diagonal first-moment scale is
at most the same combinatorial factor divided by `binom(n,a)`, multiplied by

```text
q^{-mu((m-1)(a-k)+R-k)}.
```

In particular, on the full selected-rank stratum

```text
R = min(k, sum_{j in J}(k-e_j)),
```

write

```text
d_J = k-R = max(0, sum_{j in J} e_j - (|J|-1)k).
```

In any fixed ordering of `J`, the selected-edge count can be bounded by the
sequential disjoint choice

```text
prod_{j in J} binom(n-s_j,e_j),       s_j=sum_{h in J, h before j} e_h,
```

and the diagonal-relative full-rank contribution is bounded by

```text
  [ prod_{j in J} binom(n-s_j,e_j)
    (q^{d_J}-1)/(q-1)
    prod_{i notin J} binom(n,e_i)
    prod_i binom(n,p_i)
    / binom(n,a) ]
  q^{-mu((m-1)(a-k)-d_J)}.
```

Thus the multi-edge sieve splits the clean-cycle problem into a full-rank
selected-edge part with an explicit entropy bound and lower-rank selected-edge
loci where one must count locator/vanishing-space dependencies. The symmetric
triangle and fixed-length necklace lemmas above are examples of carrying out
that lower-rank count in concrete families.

*Proof.* The identity follows from annihilators:

```text
(sum_{j in J} W_j)^perp = cap_{j in J} U_j.
```

Since the ambient polynomial space has dimension `k`, this intersection has
dimension `k-R_J`. Projectivizing gives `(q^{k-R_J}-1)/(q-1)` common
nonzero functional classes for each selected edge tuple. The stratum count
then follows by summing over the `C_J(R)` selected tuples and bounding all
unselected edge and private blocks trivially.

For the probability factor, the full clean-cycle rank satisfies
`R_cyc>=R_J`, so the clean-cycle exponent gap over diagonal is at least

```text
(m-1)(a-k)+R_J-k.
```

Substituting `R_J=R` gives the rank-stratified contribution bound. The final
display is the full selected-rank specialization with the trivial sequential
upper bound for `C_J(R)`.

The selected-rank strata have a concrete locator-syzygy form.

**Corollary (locator-syzygy form of selected-rank defect).** For each selected
edge `E_j`, write

```text
L_j(X)=prod_{x in E_j}(X-x).
```

Then `W_j=L_j F_q[X]_{<k-e_j}` inside `F_q[X]_{<k}`. The linear map

```text
Phi_J: direct_sum_{j in J} F_q[X]_{<k-e_j} -> F_q[X]_{<k},
       (A_j)_j |-> sum_{j in J} L_j A_j
```

has image `sum_{j in J} W_j`, so

```text
R_J = rank Phi_J.
```

Its kernel is exactly the space of degree-bounded locator syzygies

```text
sum_{j in J} L_j A_j = 0,       deg A_j < k-e_j.
```

Consequently

```text
dim ker Phi_J = sum_{j in J}(k-e_j) - R_J.
```

If

```text
R_full = min(k, sum_{j in J}(k-e_j)),
```

then the selected-rank defect is exactly the syzygy excess:

```text
R_full-R_J
 = dim ker Phi_J - max(0, sum_{j in J}(k-e_j)-k).
```

Thus lower selected-rank strata are not mysterious extra probability loss:
they are precisely the loci where the edge locators admit more
degree-bounded syzygies than the ambient dimension forces.

In the fixed-length necklace case `e_j=k-1`, each `A_j` is a scalar. The
syzygy condition becomes

```text
sum_{j in J} lambda_j L_j = 0,
```

so the selected-rank defect is exactly the locator-span dependency counted in
the rank-deficient necklace lemma.

*Proof.* The identity `W_j=L_j F_q[X]_{<k-e_j}` is just divisibility by the
locator of the edge set. Therefore `Phi_J` is the direct-sum presentation of
`sum_j W_j`, proving `R_J=rank Phi_J`. Its kernel consists precisely of tuples
whose weighted locator sum vanishes, which gives the syzygy description and
the kernel dimension formula. Subtracting the generic kernel dimension forced
by mapping a space of dimension `sum_j(k-e_j)` into a `k`-dimensional target
gives the displayed equality with `R_full-R_J`. The necklace specialization is
the case `k-e_j=1` for every selected edge.

The syzygy form also gives a pivot-forcing count reduction.

**Corollary (pivot-forcing reduction for selected syzygies).** Fix selected
edge sizes `e_j`, `j in J`, and write `d_j=k-e_j`. Consider marked projective
syzygies

```text
sum_{j in J} L_j A_j=0,       deg A_j<d_j,
```

together with a pivot index `t` such that `A_t != 0`, normalized up to common
scalar. After choosing the nonpivot edge blocks `E_j`, `j != t`, the nonpivot
coefficient polynomials `A_j`, and the normalized pivot coefficient `A_t`, the
pivot edge locator is forced:

```text
L_t = - (sum_{j != t} L_j A_j) / A_t.
```

Thus the remaining validity conditions are only:

```text
A_t divides -sum_{j != t} L_j A_j,
the quotient is monic of degree e_t,
its roots are e_t distinct points of H disjoint from the nonpivot edges.
```

In particular, if the selected nonpivot edge blocks are counted by a sequential
disjoint product, the number of selected-edge tuples with a marked
rank-defect syzygy is at most

```text
sum_{t in J}
  (q^{d_t}-1)/(q-1)
  q^{sum_{j != t} d_j}
  prod_{j != t} binom(n-s_{j,t},e_j),
```

where `s_{j,t}` is the number of previously chosen nonpivot edge points in a
fixed ordering. The divisibility, monicity, domain-root, and disjointness gates
can only reduce this crude count.

In the fixed-length necklace case `d_j=1`, the `A_j` are scalars. The pivot
formula becomes the forced-locator equation from the rank-deficient necklace
lemma; imposing the leading coefficient condition gives the sharper
`q^{m-2}` nonpivot coefficient count used there.

*Proof.* A projective syzygy has at least one nonzero coefficient polynomial;
mark such an index `t` and normalize `A_t`. Rearranging the syzygy gives

```text
L_t A_t = -sum_{j != t} L_j A_j.
```

For fixed nonpivot data and normalized `A_t`, there is therefore at most one
possible polynomial `L_t`, namely the displayed quotient. It corresponds to a
valid edge block exactly when the divisibility and root-set gates hold. Counting
all normalized `A_t`, all nonpivot coefficient polynomials, and all sequential
nonpivot edge choices gives the displayed overcount. Every selected-rank defect
has at least one nonzero syzygy and hence at least one marked pivot, so this
overcount covers the lower selected-rank tuples.

The monicity gate always saves one coefficient dimension in this pivot count.

**Corollary (monic leading-coefficient gate).** Keep the notation of the
pivot-forcing reduction, fix a pivot `t`, and fix a normalized pivot
coefficient `A_t` of degree `b` and leading coefficient `c`. Put

```text
D=e_t+b,        N=sum_{j != t} L_j A_j.
```

If the forced quotient

```text
L_t=-N/A_t
```

is a monic polynomial of degree `e_t`, then the coefficient of `X^D` in `N`
must be `-c`. For fixed nonpivot edge blocks, this is one affine linear
condition on the nonpivot coefficient polynomials `(A_j)_{j != t}`. Therefore
the number of nonpivot coefficient choices surviving the monicity gate is at
most

```text
q^{sum_{j != t} d_j - 1}.
```

After summing over normalized pivot coefficients, the coefficient factor in the
pivot-forcing overcount improves from

```text
(q^{d_t}-1)/(q-1) q^{sum_{j != t} d_j}
```

to

```text
(q^{d_t}-1)/(q-1) q^{sum_{j != t} d_j - 1}.
```

In the fixed-length necklace case `d_j=1` for all selected edges, this is
exactly the `q^{m-2}` coefficient count in the rank-deficient necklace lemma.

*Proof.* If `L_t` is monic of degree `e_t`, then `L_t A_t` has degree `D` and
leading coefficient `c`. Since `L_t A_t=-N`, the coefficient of `X^D` in `N`
is `-c`, which is nonzero. As the nonpivot coefficients vary, this coefficient
of `N` is a linear functional. If the functional is zero, there are no
solutions; otherwise its fiber over the nonzero value `-c` has codimension
one, giving at most `q^{sum_{j != t}d_j-1}` choices. Summing over normalized
nonzero `A_t` gives the stated coefficient bound.

The divisibility gate can save more than the single monicity equation.

**Corollary (divisibility-rank refinement for marked syzygies).** Fix the
nonpivot edge locators `L_j`, `j != t`, and a normalized nonzero pivot
coefficient `A_t` of degree `b`. Let

```text
Psi_{t,A_t}: direct_sum_{j != t} F_q[X]_{<d_j}
             -> F_q[X]/(A_t)
```

be the residue map

```text
(A_j)_{j != t} |-> sum_{j != t} L_j A_j mod A_t.
```

If `rho(t,A_t)` is the rank of this linear map, then the number of nonpivot
coefficient choices for which `A_t` divides `sum_{j != t}L_jA_j` is exactly

```text
q^{sum_{j != t} d_j - rho(t,A_t)}.
```

After also imposing the monicity equation, the number of nonpivot coefficient
choices is at most

```text
q^{sum_{j != t} d_j - max(1,rho(t,A_t))}.
```

Moreover

```text
rho(t,A_t) >= max_{j != t} min(d_j, b - deg gcd(A_t,L_j)).
```

Thus any nonconstant pivot coefficient whose residue action has rank `>1`
improves the previous monicity-only marked-syzygy bound by additional powers
of `q`.

*Proof.* The divisibility condition is exactly `Psi_{t,A_t}((A_j))=0`, so its
solution set is the kernel of a linear map of rank `rho(t,A_t)`. This gives
the exact kernel size. The monicity condition cuts out a subset of the affine
hyperplane counted in the monic gate, so the intersection is bounded by the
smaller of the divisibility-kernel bound and the monicity bound, namely the
displayed `max(1,rho(t,A_t))` saving.

For the lower bound on `rho`, restrict `Psi_{t,A_t}` to one nonpivot summand.
Multiplication by `L_j` modulo `A_t` has kernel consisting of polynomials
divisible by `A_t/gcd(A_t,L_j)`. Inside `F_q[X]_{<d_j}`, this kernel has
dimension `max(0,d_j-(b-deg gcd(A_t,L_j)))`, so the image has dimension
`min(d_j,b-deg gcd(A_t,L_j))`. The rank of the full direct-sum map is at least
the rank on any one summand.

Summing the pointwise refinement gives a sharper marked-syzygy coefficient
factor.

**Corollary (rank-weighted marked-syzygy bound).** In the marked
selected-syzygy tuple bound, fix a pivot `t` and fixed nonpivot edge locators.
Put

```text
D_t=sum_{j != t} d_j.
```

Then the monicity-only coefficient factor

```text
(q^{d_t}-1)/(q-1) q^{D_t-1}
```

may be replaced by the rank-weighted factor

```text
C_t(L_{j != t})
  = sum_{[A_t] in P(F_q[X]_{<d_t})}
      q^{D_t - max(1,rho(t,A_t))}.
```

Consequently the marked selected-syzygy count is at most

```text
sum_t sum_{nonpivot edge tuples}
  C_t(L_{j != t}),
```

with the same sequential disjoint choice of nonpivot edge tuples as before.
This is never worse than the monicity-only bound and is strictly better as
soon as some pivot coefficient class has `rho(t,A_t)>1`.

*Proof.* For each fixed projective pivot coefficient class `[A_t]`, the
divisibility-rank refinement bounds the nonpivot coefficient choices by the
corresponding summand. Summing over all pivot coefficient classes and then
over nonpivot edge tuples and pivots gives the displayed count. Since
`max(1,rho(t,A_t))>=1`, each summand is bounded by the monicity-only summand;
strict improvement occurs whenever one summand has `rho(t,A_t)>1`.

Low residue rank is itself a constrained root-sharing event.

**Corollary (low-rank pivot rarity).** Fix one nonpivot index `u != t`.
Let `N_b(r)` be the number of projective pivot coefficient classes `[A_t]`
with monic representative of exact degree `b` and residue rank
`rho(t,A_t)<=r`. If `0<=r<d_u`, then

```text
N_b(r) <= q^b                         if b<=r,
N_b(r) <= binom(e_u,b-r) q^r          if b>r.
```

Here `binom(e_u,b-r)=0` when `b-r>e_u`. In particular, low-rank pivot
coefficients of degree `b` must share at least `b-r` roots with the nonpivot
edge locator `L_u`.

*Proof.* The divisibility-rank lower bound gives

```text
rho(t,A_t) >= min(d_u, b - deg gcd(A_t,L_u)).
```

When `b<=r`, the trivial count of monic degree-`b` representatives is `q^b`.
Assume `b>r` and `r<d_u`. If `rho(t,A_t)<=r`, then
`b-deg gcd(A_t,L_u)<=r`, so `deg gcd(A_t,L_u)>=b-r`. Since `L_u` is a
squarefree locator of degree `e_u`, such an `A_t` is divisible by the locator
of some `(b-r)`-subset of `E_u`. For each chosen subset, there are at most
`q^r` monic degree-`b` multiples. A union bound over the subsets gives the
second display.

Combining the cumulative rank counts gives a closed rank-weighted coefficient
bound.

**Corollary (root-sharing bound for the rank-weighted factor).** Fix
`u != t`, and put `D_t=sum_{j != t}d_j`. For `0<=b<d_t` and
`1<=r<d_u`, define

```text
B_b(r)=q^b                         if b<=r,
B_b(r)=binom(e_u,b-r)q^r           if b>r.
```

Then

```text
C_t(L_{j != t})
 <= q^{D_t} sum_{b=0}^{d_t-1}
      [ q^{b-d_u}
        + sum_{r=1}^{d_u-1} (q^{-r}-q^{-(r+1)}) B_b(r) ].
```

Thus the rank-weighted marked-syzygy factor has an explicit root-sharing
upper bound. It is independent of the detailed residue-rank distribution and
improves the monicity-only factor whenever the resulting right-hand side is
smaller.

*Proof.* For exact degree `b`, let `N_b(r)` be the cumulative count from the
low-rank rarity corollary. Since `rho>=d_u` contributes at most `q^{-d_u}`,
the elementary layer-cake identity gives

```text
sum_{deg A_t=b} q^{-max(1,rho(t,A_t))}
 <= q^{b-d_u}
    + sum_{r=1}^{d_u-1} (q^{-r}-q^{-(r+1)}) N_b(r).
```

Substitute `N_b(r)<=B_b(r)`, sum over `b`, and multiply by `q^{D_t}`.

There is a simpler form in the comparable-dimension regime that exposes the
polynomial edge-size cost.

**Corollary (comparable-dimension root-sharing bound).** With the same fixed
nonpivot index `u`, assume `d_t<=d_u`. Then

```text
C_t(L_{j != t})
 <= q^{D_t} [ q^{-1} + (d_t-1)
              + (1-q^{-1}) sum_{s=1}^{d_t-2}
                    (d_t-1-s) binom(e_u,s) ],
```

Thus, in the comparable-dimension regime `d_t<=d_u`, the pivot coefficient
field factor is replaced by a polynomial in the nonpivot edge size. For fixed
`d_t`, this costs only `O(e_u^{max(d_t-2,0)})` instead of the monicity-only
`q^{d_t-1}` factor.

*Proof.* Start from the root-sharing bound for exact degree `b`. Since
`d_t<=d_u`, the tail `r>=b` telescopes:

```text
q^{b-d_u}+sum_{r=b}^{d_u-1}(q^{-r}-q^{-(r+1)})q^b = 1
```

for `b>=1`, while the `b=0` contribution is `q^{-1}`. For `1<=r<b`, the
low-rank term contributes

```text
(q^{-r}-q^{-(r+1)}) binom(e_u,b-r) q^r
 = (1-q^{-1}) binom(e_u,b-r).
```

Summing over `b`, and putting `s=b-r`, gives the displayed expression.

This directly refines the marked-syzygy tuple bound.

**Corollary (comparable-dimension marked-syzygy tuple bound).** Fix a pivot
`t`, and suppose there is a nonpivot index `u != t` with `d_t<=d_u`. Put

```text
H_{t,u}=q^{-1} + (d_t-1)
        + (1-q^{-1}) sum_{s=1}^{d_t-2}
             (d_t-1-s) binom(e_u,s).
```

Then the pivot-`t` contribution to the marked selected-syzygy tuple bound is
at most

```text
q^{sum_{j != t} d_j} H_{t,u}
prod_{j != t} binom(n-s_{j,t},e_j),
```

with the same sequential disjoint nonpivot edge count as before. Therefore in
the full marked-syzygy count one may replace the old pivot coefficient factor

```text
(q^{d_t}-1)/(q-1) q^{sum_{j != t}d_j-1}
```

by the minimum of this comparable-dimension root-sharing factor and the old
monicity-only factor, for every pivot admitting such a reference nonpivot
edge.

*Proof.* Apply the comparable-dimension root-sharing bound to the coefficient
factor `C_t(L_{j != t})` for each fixed nonpivot edge tuple, then sum over
the same nonpivot edge choices. The monicity-only bound remains valid, so one
may take the minimum of the two upper bounds.

The same root-sharing argument also controls the non-comparable case, with a
loss depending only on the dimension gap to the reference nonpivot edge.

**Corollary (dimension-gap root-sharing bound).** With the same fixed nonpivot
index `u`, assume `d_u>=1` and put `D_t=sum_{j != t}d_j`. Define

```text
H^gap_{t,u}
 = q^{-1}
   + min(d_t-1,d_u-1)
   + 1_{d_t>d_u} sum_{h=0}^{d_t-d_u-1} q^h
   + (1-q^{-1}) sum_{s=1}^{d_t-2}
       min(d_u-1,d_t-1-s) binom(e_u,s).
```

Then

```text
C_t(L_{j != t}) <= q^{D_t} H^gap_{t,u}.
```

When `d_t<=d_u`, this is exactly the comparable-dimension bound above. When
`d_t>d_u`, the only field-size growth beyond the common `q^{D_t}` factor is
`sum_{h=0}^{d_t-d_u-1}q^h`; the loss is controlled by the dimension gap
`d_t-d_u`, rather than by the full pivot dimension `d_t`.

Consequently, in the marked selected-syzygy tuple bound one may use the
minimum of the monicity-only factor and `q^{D_t}H^gap_{t,u}` for any fixed
reference nonpivot edge `u`.

*Proof.* Start from the root-sharing bound for the rank-weighted factor and
sum by the exact pivot-coefficient degree `b`. For `b=0`, the layer-cake sum
telescopes to `q^{-1}`. For `1<=b<d_u`, the layers `r>=b` telescope to `1`,
and the low-rank layers contribute

```text
(1-q^{-1}) sum_{s=1}^{b-1} binom(e_u,s).
```

For `b>=d_u`, the full-rank contribution is `q^{b-d_u}`, and the low-rank
layers contribute

```text
(1-q^{-1}) sum_{s=b-d_u+1}^{b-1} binom(e_u,s).
```

Summing over `0<=b<d_t` gives the displayed baseline terms. Reindexing the
low-rank contribution by the shared-root count `s` shows that a fixed
`binom(e_u,s)` appears for exactly
`min(d_u-1,d_t-1-s)` possible degree layers, proving the formula. The tuple
bound follows by summing over the same nonpivot edge choices.

The dimension-gap estimate has a useful field-exponent form.

**Corollary (field exponent of the dimension-gap shell).** In the previous
corollary define

```text
alpha_{t,u}=min(max(d_t,2),d_u+1).
```

Then the pivot-`t` coefficient factor in the marked selected-syzygy bound has
field exponent at most

```text
r_sel-alpha_{t,u},       r_sel=sum_j d_j,
```

up to a `q`-independent shell factor depending on the edge sizes. Equivalently,
the dimension-gap root-sharing replacement saves at least
`alpha_{t,u}` powers of `q` from the crude `q^{r_sel}` marked-syzygy exponent.

*Proof.* The nonpivot coefficient dimension is `D_t=r_sel-d_t`. If `d_t=1`,
the shell factor is `q^{-1}`, so the field exponent is
`D_t-1=r_sel-2`, and `alpha_{t,u}=2`. If `d_t>=2`, the largest `q`-power in
`H^gap_{t,u}` is `q^{max(0,d_t-d_u-1)}`. Thus the total field exponent is

```text
D_t+max(0,d_t-d_u-1)
 = r_sel-min(d_t,d_u+1)
 = r_sel-alpha_{t,u}.
```

The comparable-dimension hypothesis fails for at most one pivot.

**Corollary (all-pivot coverage except a unique smallest edge).** Select all
edges of a clean cycle and write `d_i=k-e_i`. For each pivot `t`, choose a
nonpivot reference `u(t)` with maximal `d_u` among `u != t`. Then the
comparable-dimension marked-syzygy bound applies to pivot `t` unless `d_t` is
the unique maximum of the list `(d_i)_i`.

Equivalently, the root-sharing improvement applies to every pivot unless the
edge `E_t` is the unique smallest edge overlap. If the smallest edge size
occurs at least twice, every pivot admits a comparable-dimension reference.
Thus the all-edge marked-syzygy bound may be root-sharing-refined at all
pivots except possibly one unique-smallest-edge pivot. At that pivot the
dimension-gap root-sharing bound still applies, and the monicity-only factor
remains a valid fallback.

*Proof.* The chosen reference has dimension
`d_{u(t)}=max_{u != t}d_u`. The condition `d_t<=d_{u(t)}` fails exactly when
`d_t` is strictly larger than every other `d_u`, i.e. when it is the unique
maximum. Since `d_i=k-e_i`, unique maximum `d_i` is the same as unique minimum
edge size `e_i`.

The root and disjointness gate is also purely algebraic.

**Corollary (domain-locator gate for forced pivots).** Let

```text
L_H(X)=prod_{x in H}(X-x).
```

Assume the pivot-forcing quotient `L_t=-(sum_{j != t}L_j A_j)/A_t` is already
a monic polynomial of degree `e_t`. Then `L_t` is the locator of a valid pivot
edge block disjoint from the selected nonpivot edge blocks if and only if

```text
L_t divides L_H
```

and

```text
gcd(L_t,L_j)=1        for every j != t.
```

Equivalently, for a multiplicative subgroup domain of size `n`, this is the
divisor gate `L_t | X^n-1` together with the same coprimality conditions.

Thus the pivot-forcing reduction leaves only three explicit polynomial gates:
divisibility by the pivot coefficient `A_t`, monicity of the quotient, and the
domain-locator/coprimality gate above.

*Proof.* A monic polynomial of degree `e_t` is the locator of an `e_t`-subset
of `H` exactly when it is a degree-`e_t` divisor of the squarefree domain
locator `L_H`. This is the condition `L_t | L_H`. The pivot edge is disjoint
from a nonpivot edge `E_j` exactly when the two locator polynomials share no
root, which is equivalent to `gcd(L_t,L_j)=1`.

Combining the pivot, monic, and domain gates gives the following general
marked-syzygy overcount.

**Corollary (marked selected-syzygy tuple bound).** Fix selected edge sizes
`e_j`, coefficient dimensions `d_j=k-e_j`, and a fixed ordering of
the nonpivot set `J` with `t` removed for every pivot `t`. The number of
selected edge tuples admitting a marked projective syzygy is at most

```text
sum_{t in J}
  (q^{d_t}-1)/(q-1)
  q^{sum_{j != t} d_j - 1}
  prod_{j != t} binom(n-s_{j,t},e_j),
```

where `s_{j,t}` is the number of nonpivot edge points chosen before `j` in the
fixed ordering for pivot `t`.

The same expression remains a valid upper bound after imposing the divisibility
by `A_t`, domain-locator, and coprimality gates, since those gates only remove
choices. Thus every lower selected-rank tuple is covered by a sum of explicit
marked pivot-forcing data.

For fixed-length necklaces, `d_j=1` and the displayed bound becomes

```text
m q^{m-2} prod_{h=0}^{m-2} binom(n-hr,r),
```

which is exactly the rank-deficient necklace count used above.

*Proof.* The pivot-forcing reduction counts normalized nonzero `A_t`, nonpivot
edge blocks, and nonpivot coefficient polynomials. The monic leading
coefficient gate reduces the nonpivot coefficient count by one power of `q`.
The divisibility and domain gates only discard choices, so the displayed
quantity is an upper bound. In the necklace case each `d_j=1`, so
`(q^{d_t}-1)/(q-1)=1`, the nonpivot coefficient factor is `q^{m-2}`, and the
nonpivot block product is the stated sequential product; summing over the `m`
pivots gives the necklace formula.

Combining this selected-edge count with the clean-cycle rank ledger gives a
diagonal-relative version.

**Corollary (diagonal-relative marked-syzygy bound).** Let `B_J` denote the
marked selected-syzygy bound from the previous corollary. Suppose a lower bound

```text
R_cyc >= k-d
```

is available for the same clean-cycle shape. Then the random-model contribution
of clean support tuples whose selected edges admit a marked syzygy, divided by
the diagonal first-moment scale, is at most

```text
  [ B_J
    prod_{i notin J} binom(n,e_i)
    prod_i binom(n,p_i)
    / binom(n,a) ]
  q^{-mu((m-1)(a-k)-d)}.
```

One may take `d=max(0,s_2-k)` from the two-edge lower bound. In the fixed-length
necklace case, taking `J` to be all edges and using `R_cyc>=2` gives
`d=k-2=r-1`; the displayed bound is exactly the rank-deficient necklace
relative contribution proved above.

*Proof.* The marked selected-syzygy bound counts the selected edge data, while
the unselected edge and private blocks are bounded trivially by the two
products in the display. The clean-cycle rank formula gives exponent gap over
diagonal

```text
(m-1)(a-k)+R_cyc-k.
```

Using `R_cyc>=k-d` gives the probability saving
`q^{-mu((m-1)(a-k)-d)}`. Dividing the support count by the diagonal support
count `binom(n,a)` gives the displayed relative bound. The necklace
specialization has `a=2r`, `k=r+1`, `d=r-1`, no private blocks, and no
unselected edges, recovering the previous formula.

This gives a usable all-edge clearance test for clean-cycle defects.

**Corollary (all-edge hybrid clean-cycle defect bound).** Select all
clean-cycle edges, and put

```text
d_2=max(0,s_2-k),       s_2=min_{i<j}(e_i+e_j).
```

If `s_2<=k`, then `R_cyc=k`, so there is no rank-deficient clean-cycle
defect. Assume now that `s_2>k`. Let `B_full` be the full selected-rank
all-edge count

```text
  prod_i binom(n-s_i,e_i) (q^{d_full}-1)/(q-1),
  d_full=max(0,sum_i e_i-(m-1)k),
```

where `s_i` is the number of previously chosen edge points in a fixed
ordering. Let `B_mark` be the all-edge marked-syzygy bound from the previous
corollary. Then the rank-deficient clean-cycle contribution of this fixed
shape, divided by the diagonal first-moment scale, is at most

```text
  [ (B_full+B_mark) prod_i binom(n,p_i) / binom(n,a) ]
  q^{-mu((m-1)(a-k)-d_2)}.
```

Thus the all-edge clean-cycle defect splits into a full selected-rank
incidence part and a lower selected-rank marked-syzygy part. In applications
the small-pair case should be removed first by the two-edge theorem; the
marked-syzygy bound is deliberately a coarse overcount there because it also
counts generic kernel syzygies that do not lower `R_cyc`.

*Proof.* If `s_2<=k`, the two-edge lower bound gives `R_cyc=k`. Otherwise,
partition the selected edge tuples according to whether the all-edge selected
rank is full. The full selected-rank stratum has common functional dimension
`d_full`, giving the projective incidence count `B_full`. Every lower
selected-rank tuple has a nonzero excess syzygy, hence is covered by
`B_mark`. Multiplying by the private block count and using the two-edge lower
bound `R_cyc>=k-d_2` gives the displayed diagonal-relative contribution.

The incidence counts are exact in the MDS uniqueness range.

**Corollary (small-support uniqueness for `N_e`).** Let `r([ell])` be the
minimum size of a subset `R subset H` such that
`[ell] in span{ev_x:x in R}`. If `e<r([ell])`, then `N_e([ell])=0`. If
`r([ell])=r`, `e>=r`, and `r+e<=k`, then the minimal support `R` is unique and

```text
N_e([ell]) = binom(n-r,e-r)
```

In particular, for `e<=k/2`,

```text
N_e([ell]) <= binom(n-1,e-1)
```

for every projective functional `[ell]`.

*Proof.* The case `e<r([ell])` is the definition of minimal support. Assume
now that `e>=r` and `r+e<=k`. If `R` and `R'` were two distinct minimal
supports of size `r`, then the two representations would give a nontrivial
dependence on `R union R'`, whose size is at most `2r<=r+e<=k`; this
contradicts MDS independence. Thus `R` is unique.

Now let `E` be any `e`-set counted by `N_e([ell])`. Choose a support
`T subset E` for a representation of `[ell]`. Since `|R union T|<=r+e<=k`,
MDS independence again forces `T=R`, so `R subset E`. Conversely, every
`e`-set containing `R` is counted. This gives the binomial formula. When
`e<=k/2` and `[ell]` is counted at all, its minimal support has `r<=e`, so
`r+e<=2e<=k`; the formula applies and is maximized at `r=1`.

The disjointness in a clean cycle makes this sharper for any cycle containing a
small edge.

**Corollary (small-edge isolation).** Suppose a rank-deficient clean cycle has
common projective functional `[ell]`, and let `r=r([ell])` be its minimal
support size. If one edge block `E_i` has size `e_i` with

```text
r+e_i<=k,
```

then `E_i` contains the unique minimal support `R` of `[ell]`. Since the clean
cycle edge blocks are pairwise disjoint, every other edge size satisfies

```text
e_j > k-r        for all j != i.
```

In particular, if a rank-deficient clean cycle has an edge of size
`e_min<=k/2`, then that edge contains the minimal support of the common
functional and all other edge overlaps have size greater than `k-r([ell])`.

*Proof.* The containment of `R` in `E_i` is the small-support uniqueness
corollary. Every other edge block `E_j` is disjoint from `E_i`, hence disjoint
from `R`. If `e_j+r<=k`, the two disjoint representations on `R` and `E_j`
would violate the MDS independence rule from the functional-incidence
corollary. Therefore `e_j>k-r`.

This formula gives a useful first lower bound without classifying all possible
dependencies among the `W_i`.

**Corollary (two-edge lower bound for clean cycles).** With the notation of the
clean simple-cycle lemma, let

```text
s_2 = min_{i<j} (e_i+e_j).
```

Then

```text
R_cyc >= k - max(0,s_2-k).
```

In particular, if two edge overlaps have total size at most `k`, then
`R_cyc=k` and the clean-cycle exponent gap over diagonal is exactly

```text
(m-1)(a-k).
```

Thus any clean cyclic obstruction with `R_cyc<k` must have

```text
e_i+e_j>k        for every pair i<j.
```

Equivalently, the remaining rank-deficient clean cycles are forced into a
near-necklace regime where the two smallest edge overlaps already have total
larger than `k`.

*Proof.* For two disjoint edge sets `E_i,E_j`, the intersection
`W_i cap W_j` consists of degree-`<k` polynomials vanishing on
`E_i union E_j`. Hence

```text
dim(W_i cap W_j)=max(k-e_i-e_j,0).
```

Since `dim W_i=k-e_i` and `dim W_j=k-e_j`,

```text
dim(W_i+W_j)
  = (k-e_i)+(k-e_j)-max(k-e_i-e_j,0)
  = k - max(0,e_i+e_j-k).
```

The full sum `W_0+...+W_{m-1}` contains every two-edge sum, so taking the pair
with minimal `e_i+e_j` gives the stated lower bound. If `s_2<=k`, this lower
bound is `k`, and `R_cyc` cannot exceed the ambient dimension `k`; therefore
`R_cyc=k`. Substituting into the clean-cycle exponent gap formula gives
`(m-1)(a-k)`.

The same two-edge lower bound has a useful reserve form. Put

```text
sigma = a-k,       p_max=max_i p_i.
```

**Corollary (private-mass reserve gate for clean cycles).** If `p_max>=sigma`,
then `R_cyc=k`; hence there is no rank-deficient clean-cycle defect. If
`p_max<sigma`, then the two-edge lower bound gives

```text
(m-1)(a-k)-d_2 >= (m-2)sigma+p_max,
       d_2=max(0,s_2-k).
```

Consequently every rank-deficient clean cycle has `p_i<sigma` for every
private block, and its two-edge diagonal-relative exponent saving is at least
`mu((m-2)sigma+p_max)`.

*Proof.* Choose an index `i` with `p_i=p_max`. Since

```text
p_i = a-e_{i-1}-e_i,
```

the adjacent pair has size

```text
e_{i-1}+e_i = a-p_max.
```

If `p_max>=sigma=a-k`, then this adjacent pair has total size at most `k`, so
the two-edge lower bound gives `R_cyc=k`. Otherwise
`s_2<=a-p_max`, and hence

```text
d_2=max(0,s_2-k) <= a-p_max-k = sigma-p_max.
```

Therefore

```text
(m-1)(a-k)-d_2 >= (m-1)sigma-(sigma-p_max)
                 = (m-2)sigma+p_max.
```

The final statement is the same exponent bound multiplied by the arity `mu`.

This also removes private blocks from the remaining hybrid estimate once the
generated field has enough polynomial headroom.

**Corollary (private-block absorption in the hybrid clean-cycle bound).** Keep
the notation of the all-edge hybrid clean-cycle defect bound, and assume

```text
q^mu >= n^m.
```

Then every clean-cycle shape has either `R_cyc=k`, or its hybrid
diagonal-relative rank-deficient contribution is at most

```text
  [ (B_full+B_mark) / binom(n,a) ] q^{-mu(m-2)(a-k)}.
```

Thus, under this field-size condition, the private-point choices are paid by
the `p_max` part of the two-edge saving. The remaining clean-cycle problem is
the selected-edge incidence/syzygy count, not private mass.

*Proof.* If `p_max>=sigma`, the private-mass reserve gate gives `R_cyc=k`.
Otherwise the hybrid bound and the previous corollary give

```text
  [ (B_full+B_mark) prod_i binom(n,p_i) / binom(n,a) ]
  q^{-mu((m-2)sigma+p_max)}.
```

Since every `p_i<=p_max`,

```text
prod_i binom(n,p_i) <= n^{sum_i p_i} <= n^{m p_max} <= q^{mu p_max}.
```

Cancelling this against the `q^{-mu p_max}` factor leaves the displayed
bound.

The absorbed bound gives a precise selected-edge target. Let

```text
P=sum_i p_i,       E=sum_i e_i,       r_sel=sum_i(k-e_i).
```

Then the clean-cycle identities give

```text
2E = m(k+sigma)-P,             2r_sel = m(k-sigma)+P.
```

The full selected-rank part has projective dimension

```text
d_full=max(0,E-(m-1)k),
```

and the lower selected-rank part is counted by the marked-syzygy bound
`B_mark`. Thus, after private-block absorption, a fixed clean-cycle shape is
cleared below the diagonal scale as soon as

```text
B_full+B_mark < binom(n,a) q^{mu(m-2)sigma}.
```

This is the exact selected-edge inequality left by the present reduction. It
has no private-block factor: private mass now enters only through the ledger
variables `P` and `r_sel`.

*Proof.* Summing the identities `p_i=a-e_{i-1}-e_i` over the cycle gives
`P=ma-2E`, hence the first display. Since
`r_sel=mk-E`, substituting `a=k+sigma` gives the second display. The
private-block absorption corollary says the diagonal-relative contribution is
at most

```text
[(B_full+B_mark)/binom(n,a)] q^{-mu(m-2)sigma},
```

which is below one exactly under the displayed selected-edge inequality.

There is a simple asymptotic gate for this selected-edge inequality. Put

```text
T = mu(m-2)sigma.
```

**Corollary (selected-edge field-exponent gate).** Fix `m`, `mu`, and a
constant `c>0`. Along any generated-field sequence with `q>=n+1`, if

```text
T-d_full >= c n,             T-r_sel >= c n,
```

then the absorbed selected-edge ratio

```text
[(B_full+B_mark)/binom(n,a)] q^{-T}
```

tends to zero. Consequently any asymptotic selected-edge obstruction to the
hybrid clean-cycle bound must satisfy

```text
d_full >= T-o(n)        or        r_sel >= T-o(n).
```

*Proof.* The selected edge blocks are disjoint and `m` is fixed, so their
ordered choices are bounded by `2^{mn}`. The full selected-rank term is at
most `2^{mn}q^{d_full}`. For the marked-syzygy term, the total coefficient
dimension is `r_sel`; choosing a pivot costs only a fixed factor, and the
marked coefficient count is at most `q^{r_sel}`. Thus

```text
B_full+B_mark <= (1+m)2^{mn}(q^{d_full}+q^{r_sel}).
```

After multiplying by `q^{-T}` and using the two displayed margin assumptions,
the right-hand side is at most a constant times

```text
2^{mn} q^{-c n} <= 2^{mn} (n+1)^{-c n},
```

which tends to zero. Dividing by `binom(n,a)>=1` can only improve the bound.
The final obstruction statement is the contrapositive.

The root-sharing refinement improves the marked-syzygy side of this gate.

**Corollary (root-sharing selected-edge exponent gate).** In the all-edge
clean-cycle setting, choose for each pivot `t` a nonpivot reference `u(t)` with
maximal `d_u` among `u != t`, and put

```text
alpha_* = min_t min(max(d_t,2),d_{u(t)}+1).
```

Replace `B_mark` by the dimension-gap root-sharing marked-syzygy bound. Along
generated-field sequences with fixed `m`, fixed `mu`, and `q>=n+1`, if

```text
T-d_full >= c n,             T-(r_sel-alpha_*) >= c n
```

for some constant `c>0`, then the absorbed selected-edge ratio with the
dimension-gap marked-syzygy bound tends to zero. Consequently any asymptotic
selected-edge obstruction left after this root-sharing refinement must satisfy

```text
d_full >= T-o(n)        or        r_sel-alpha_* >= T-o(n).
```

In particular `alpha_*>=2` whenever all selected edge coefficient dimensions
are positive, and larger minimum coefficient dimensions give proportionally
larger field-exponent savings.

*Proof.* The full selected-rank term is unchanged. For the lower selected-rank
term, the field-exponent corollary for the dimension-gap shell gives a
coefficient exponent at most `r_sel-alpha_*` for every pivot. The remaining
root-sharing shell and selected-edge block choices are `q`-independent and
bounded by `2^{O_m(n)}` for fixed `m`. Hence the same argument as in the
selected-edge field-exponent gate applies with `r_sel` replaced by
`r_sel-alpha_*`. The obstruction statement is the contrapositive.

This sharpened gate has an equally explicit mass form.

**Corollary (root-sharing mass form of the selected-edge obstruction).** With
`P=sum_i p_i`, `T=mu(m-2)sigma`, and the maximal-reference choice of
`alpha_*` above,

```text
alpha_* = max(2,min_i d_i),
2(T-(r_sel-alpha_*))
 = 2mu(m-2)sigma - m(k-sigma) - P + 2alpha_*.
```

Consequently the marked-syzygy side after root-sharing has a linear
field-exponent margin exactly when

```text
P <= 2mu(m-2)sigma - m(k-sigma) + 2alpha_* - Omega(n).
```

Thus root-sharing raises the private-mass threshold for the lower selected-rank
term by exactly `2alpha_*` in doubled-margin form. In particular, even when
some selected edge has `d_i=1`, the threshold gains four powers in doubled
form, and if all selected edges have `d_i>=D>=2`, it gains at least `2D`.

*Proof.* For each pivot `t`, the maximal-reference choice has
`d_{u(t)}>=min_i d_i`. If `min_i d_i=1`, the pivot with `d_t=1` gives
`alpha_{t,u}=2`, while all pivots have `alpha_{t,u}>=2`. If
`min_i d_i>=2`, a pivot with minimal `d_t` gives
`alpha_{t,u}=d_t=min_i d_i`, and every other pivot has
`alpha_{t,u}>=min_i d_i`. Hence `alpha_*=max(2,min_i d_i)`.

The ledger identity `2r_sel=m(k-sigma)+P` from the previous selected-edge
reduction gives

```text
2(T-(r_sel-alpha_*))
 = 2T - 2r_sel + 2alpha_*
 = 2mu(m-2)sigma - m(k-sigma) - P + 2alpha_*.
```

The threshold and gain statements are immediate from positivity of this margin.

The two field-exponent margins have a transparent mass form.

**Corollary (mass form of the selected-edge obstruction).** With
`P=sum_i p_i` and `T=mu(m-2)sigma`,

```text
2 d_full = max(0, m sigma - (m-2)k - P),
2(T-r_sel) = 2mu(m-2)sigma - m(k-sigma) - P.
```

Consequently the marked-syzygy side of the present selected-edge gate has a
linear field-exponent margin exactly when

```text
P <= 2mu(m-2)sigma - m(k-sigma) - Omega(n).
```

In particular, if

```text
[2mu(m-2)+m]sigma <= m k - Omega(n),
```

then no clean-cycle shape can be cleared by this coarse marked-syzygy
field-exponent gate alone. Equivalently, ignoring `o(1)` terms, the current
selected-syzygy count needs

```text
sigma/k > m/(2mu(m-2)+m)
```

before it can clear by generated-field exponent without a sharper count for
`B_mark`.

*Proof.* The identity for `d_full` follows from

```text
2E=m(k+sigma)-P,       d_full=max(0,E-(m-1)k).
```

For the marked term, use

```text
2r_sel=m(k-sigma)+P.
```

Subtracting from `2T=2mu(m-2)sigma` gives the second display. The remaining
claims are immediate from `P>=0` and the requirement that `T-r_sel` have a
positive linear margin in the selected-edge field-exponent gate.

This gives a uniform high-reserve clean-cycle clearance regime.

**Corollary (uniform clean-cycle clearance in the high-reserve window).** Fix
`m>=3`, `mu>=2`, and suppose `k`, `sigma`, and `n` all grow linearly with
`n`. Along generated-field sequences with `q>=n+1` and `q^mu>=n^m`, assume
there is a constant `c>0` such that

```text
2mu(m-2)sigma - m k >= c n.
```

Then every clean simple `m`-cycle shape is either full rank by the
private-mass reserve gate or has absorbed hybrid contribution tending to zero
relative to the diagonal scale.

Equivalently, for the present coarse marked-syzygy bound, uniform fixed-`m`
clean-cycle clearance follows in the window

```text
sigma/k > m/(2mu(m-2))
```

with a fixed positive margin.

*Proof.* If `p_max>=sigma`, the private-mass reserve gate gives `R_cyc=k`.
Otherwise `P=sum_i p_i < m sigma`, so the mass formula gives

```text
2(T-r_sel)
  = 2mu(m-2)sigma - m(k-sigma) - P
  > 2mu(m-2)sigma - m k
  >= c n.
```

Thus `T-r_sel` has a positive linear margin. The full selected-rank margin is
also linear: if `d_full=0`, then `T-d_full=T`, while if `d_full>0`, the mass
formula gives

```text
2(T-d_full)
 = [2mu(m-2)-m]sigma + (m-2)k + P,
```

which is linear and positive for `m>=3`, `mu>=2`. The selected-edge
field-exponent gate then clears the absorbed hybrid ratio. The displayed
reserve window is the same condition divided by `k`, with a fixed margin.

The root-sharing gate improves this high-reserve clearance for shapes whose
selected edges have nontrivial coefficient dimension.

**Corollary (root-sharing high-reserve clean-cycle clearance).** Fix
`m>=3`, `mu>=2`, and suppose `k`, `sigma`, and `n` all grow linearly with
`n`. For a clean simple `m`-cycle shape with `d_i=k-e_i>=1` for every selected
edge, put

```text
D_* = max(2,min_i(k-e_i)).
```

Along generated-field sequences with `q>=n+1` and `q^mu>=n^m`, if there is a
constant `c>0` such that

```text
2mu(m-2)sigma - m k + 2D_* >= c n,
```

then that clean-cycle shape is either full rank by the private-mass reserve
gate or has dimension-gap-root-sharing absorbed hybrid contribution tending to
zero relative to the diagonal scale. If the displayed inequality holds
uniformly over a family of clean-cycle shapes, the whole family is cleared.

Equivalently, if `D_*/k>=beta` along the family, root-sharing gives clearance
in the window

```text
sigma/k > (m-2beta)/(2mu(m-2))
```

with a fixed positive margin. For `beta=0` this recovers the previous coarse
high-reserve window; positive `beta` is a genuine widening of the clean-cycle
clearance range.

*Proof.* If `p_max>=sigma`, the private-mass reserve gate gives `R_cyc=k`.
Otherwise `P=sum_i p_i<m sigma`. The root-sharing mass form gives

```text
2(T-(r_sel-alpha_*))
 = 2mu(m-2)sigma - m(k-sigma) - P + 2alpha_*
 > 2mu(m-2)sigma - m k + 2D_*
 >= c n,
```

because `alpha_*=D_*` for the maximal-reference choice. The full selected-rank
margin is unchanged and is linear positive by the same argument as in the
previous high-reserve corollary. The root-sharing selected-edge exponent gate
therefore clears the absorbed hybrid ratio. Dividing the displayed condition by
`k` and using `D_*/k>=beta` gives the stated rate window with margin.

The residual shapes left by this clearance are forced into a narrow dimension
band.

**Corollary (residual clean-cycle dimension band).** For a clean simple cycle,
write `d_i=k-e_i`. Then

```text
p_i = d_{i-1}+d_i-(k-sigma).
```

Consequently every valid clean cycle satisfies

```text
d_{i-1}+d_i >= k-sigma
```

for every `i`. If the private-mass reserve gate has not already applied, so
`p_i<sigma` for every `i`, then the residual clean-cycle shape satisfies the
two-sided adjacent-dimension band

```text
k-sigma <= d_{i-1}+d_i < k
```

for every `i`. In particular a small `d_i` forces both neighboring dimensions
to be at least `k-sigma-d_i`.

Moreover, any asymptotic family of such residual shapes not cleared by the
root-sharing high-reserve corollary must satisfy

```text
D_* <= (m k - 2mu(m-2)sigma)/2 + o(n),
```

and hence contains an edge overlap of size at least

```text
max_i e_i >= k - (m k - 2mu(m-2)sigma)/2 - o(n).
```

Thus after the private-mass and root-sharing gates, a remaining clean-cycle
obstruction must be large-overlap in at least one edge and must obey the
adjacent dimension band above.

*Proof.* Since `a=k+sigma` and `e_i=k-d_i`, the clean-cycle identity
`p_i=a-e_{i-1}-e_i` gives

```text
p_i=k+sigma-(k-d_{i-1})-(k-d_i)
    =d_{i-1}+d_i-(k-sigma).
```

The lower band is exactly `p_i>=0`; if the private-mass gate has not applied,
then `p_i<sigma`, which is exactly `d_{i-1}+d_i<k`.

For the final claim, take the contrapositive of the root-sharing high-reserve
clearance corollary. If the family is not cleared by that corollary, then the
quantity

```text
2mu(m-2)sigma - m k + 2D_*
```

cannot have a positive linear lower bound, hence it is `<=o(n)` along a
subsequence. Rearranging gives the displayed upper bound for `D_*`. Choosing
an index with minimal `d_i` gives `max_i e_i>=k-D_*`, which is the displayed
large-overlap bound.

The band also controls the neighbors of the forced large-overlap edge.

**Corollary (large-overlap edge localization).** In the residual band of the
previous corollary, let

```text
D=min_i d_i
```

and choose an index `t` with `d_t=D`. Then

```text
d_{t-1}, d_{t+1} >= k-sigma-D,
```

or equivalently

```text
e_{t-1}, e_{t+1} <= sigma+D.
```

If `D<(k-sigma)/2`, then no two minimum-dimension edges are adjacent; the
maximum-overlap edges `e_i=k-D` are isolated in the clean cycle.

Combining with the nonclearance conclusion above, any asymptotic residual
family not cleared by the root-sharing high-reserve gate contains an edge of
size

```text
e_t >= k - (m k - 2mu(m-2)sigma)/2 - o(n)
```

whose two neighboring edge overlaps are at most

```text
sigma + (m k - 2mu(m-2)sigma)/2 + o(n).
```

Thus a remaining residual obstruction is not only large-overlap somewhere:
the large-overlap edge is locally flanked by quantitatively controlled
overlaps.

*Proof.* Apply the lower adjacent-dimension band
`d_{i-1}+d_i>=k-sigma` to the pairs adjacent to `t`. This gives
`d_{t-1},d_{t+1}>=k-sigma-D`. Since `e_i=k-d_i`, this is equivalent to
`e_{t-1},e_{t+1}<=sigma+D`.

If two minimum-dimension edges were adjacent, their adjacent sum would be
`2D`, contradicting the lower band when `D<(k-sigma)/2`. The final displayed
bounds follow by substituting the nonclearance upper bound for `D` from the
previous corollary.

The localization propagates one more step in the residual band.

**Corollary (two-step residual-band propagation).** Keep the hypotheses and
notation of the previous corollary, and assume the private-mass reserve gate
has not applied. If `d_t=D=min_i d_i`, then

```text
d_{t-2}, d_{t+2} <= sigma+D-1,
```

or equivalently

```text
e_{t-2}, e_{t+2} >= k-sigma-D+1.
```

Thus a minimum-dimension edge forces a local alternating pattern:
its immediate neighbors have large coefficient dimension, while its second
neighbors are again large-overlap edges up to the threshold `sigma+D-1`.

*Proof.* From the previous corollary,
`d_{t+1}>=k-sigma-D`. Since the private-mass gate has not applied, the upper
residual band gives `d_{t+1}+d_{t+2}<k`; all quantities are integral, so

```text
d_{t+2} <= k-1-d_{t+1} <= sigma+D-1.
```

The same argument on the left gives the bound for `d_{t-2}`. Translating by
`e_i=k-d_i` gives the equivalent overlap lower bound.

Iterating gives a useful parity propagation rule.

**Corollary (alternating residual-band propagation).** Keep the residual-band
hypotheses, and let `d_t=D=min_i d_i`. For every `r>=0`, as long as the
indices are read along either orientation of the cycle before returning to
`t`,

```text
d_{t +/- 2r} <= D+r(sigma-1),
d_{t +/- (2r+1)} >= k-D-(r+1)sigma+r.
```

In particular, if the clean cycle has odd length `m`, then

```text
2D >= k - ((m+1)/2)sigma + (m-1)/2.
```

Combining with root-sharing nonclearance, any odd residual clean-cycle family
not cleared by the root-sharing high-reserve gate must satisfy the
compatibility condition

```text
k - ((m+1)/2)sigma + (m-1)/2
 <= m k - 2mu(m-2)sigma + o(n).
```

If this inequality fails with a linear margin, odd residual clean cycles are
cleared by the existing private-mass/root-sharing gates.

Equivalently, when

```text
4mu(m-2) > m+1,
```

odd residual clean cycles are cleared if

```text
sigma/k > 2(m-1)/(4mu(m-2)-(m+1))
```

with a fixed positive margin. This threshold is not always stronger than the
coarse high-reserve window, but it is a separate parity obstruction and it
improves the coarse window exactly when

```text
2mu(m-2) > m(m+1)/2.
```

*Proof.* The case `r=0` is `d_t=D`. Assume
`d_{t+2r}<=D+r(sigma-1)`. The lower residual band gives

```text
d_{t+2r+1} >= k-sigma-d_{t+2r}
             >= k-D-(r+1)sigma+r.
```

Then the strict upper residual band and integrality give

```text
d_{t+2r+2} <= k-1-d_{t+2r+1}
             <= D+(r+1)(sigma-1).
```

The same induction applies in the opposite orientation. If `m` is odd, take
`2r+1=m`, so the odd-distance lower bound returns to `t`; this gives the
displayed lower bound for `2D`. The compatibility condition follows by
combining this lower bound with the nonclearance upper bound
`2D<=m k-2mu(m-2)sigma+o(n)`.
Rearranging the compatibility condition gives

```text
[2mu(m-2)-(m+1)/2] sigma <= (m-1)k+o(n).
```

When the coefficient of `sigma` is positive, this is equivalent to the
displayed threshold. Comparing
`2(m-1)/(4mu(m-2)-(m+1))` with the coarse threshold
`m/(2mu(m-2))` gives the final condition after cross-multiplication.

The residual band also gives a global packing rule for very large overlaps.

**Corollary (low-dimension packing in residual clean cycles).** Assume the
private-mass reserve gate has not applied, so

```text
k-sigma <= d_{i-1}+d_i < k
```

for every adjacent pair. Let `tau` be an integer with `2tau<k-sigma`, and set

```text
L_tau={i: d_i<=tau}.
```

Then `L_tau` is an independent set in the cycle. In particular

```text
|L_tau| <= floor(m/2).
```

Equivalently, edges with overlap `e_i>=k-tau` are never adjacent and occupy at
most half of the clean cycle. Every such large-overlap edge has neighboring
overlaps at most `sigma+tau`.

*Proof.* If two adjacent indices `i-1,i` both belonged to `L_tau`, then

```text
d_{i-1}+d_i <= 2tau < k-sigma,
```

contradicting the lower residual band. Thus `L_tau` is independent in the
cycle, so it has size at most `floor(m/2)`. If `d_i<=tau`, the lower band gives
each neighboring dimension at least `k-sigma-tau`; translating by `e_j=k-d_j`
gives neighboring overlaps at most `sigma+tau`.

The preceding reductions can be packaged as a normal form for the clean-cycle
obstruction left by the present L2 route.

**Corollary (residual clean-cycle normal form).** Fix `m`, `mu`, and a clean
simple `m`-cycle shape with positive selected-edge coefficient dimensions
`d_i=k-e_i`. After the small-pair full-rank gate and the private-mass reserve
gate, any asymptotic family not cleared by the dimension-gap root-sharing
high-reserve gate must satisfy all of the following:

```text
p_i=d_{i-1}+d_i-(k-sigma),
k-sigma <= d_{i-1}+d_i < k,
D_* <= (m k - 2mu(m-2)sigma)/2 + o(n),
max_i e_i >= k - (m k - 2mu(m-2)sigma)/2 - o(n).
```

If `D=min_i d_i` and `d_t=D`, then

```text
d_{t-1},d_{t+1} >= k-sigma-D,
d_{t-2},d_{t+2} <= sigma+D-1
```

whenever the indicated indices are interpreted in the residual band. For any
integer `tau` with `2tau<k-sigma`, the set `{i: d_i<=tau}` is independent and
has size at most `floor(m/2)`.

If `m` is odd, the same residual family must also satisfy

```text
k - ((m+1)/2)sigma + (m-1)/2
 <= m k - 2mu(m-2)sigma + o(n),
```

or, equivalently when `4mu(m-2)>m+1`, it can survive only below the explicit
odd-cycle threshold

```text
sigma/k <= 2(m-1)/(4mu(m-2)-(m+1)) + o(1).
```

Thus the unresolved clean-cycle part of the present L2 route is concentrated
in residual-band shapes with sparse very-large-overlap edges and, in odd
length, the displayed parity compatibility.

*Proof.* The first two displays are the residual dimension-band corollary and
the contrapositive of root-sharing high-reserve clearance. The neighbor and
second-neighbor bounds are the large-overlap localization and two-step
propagation corollaries. The independence statement is the low-dimension
packing corollary. The odd-cycle compatibility and threshold are exactly the
alternating propagation corollary.

For fixed parameters this normal form is finite and checkable.

**Corollary (finite residual-shape certificate).** Fix `m`, `mu`, `k`, and
`sigma`. To certify that the current clean-cycle gates leave no residual shape
at these parameters, it is enough to check that there is no integer vector

```text
(d_0,...,d_{m-1}),       1<=d_i<k,
```

satisfying all of the following constraints:

```text
k-sigma <= d_{i-1}+d_i < k                         for every i,
d_i+d_j < k                                        for every i<j,
2mu(m-2)sigma - m k + 2max(2,min_i d_i) <= 0,
```

and, when `m` is odd,

```text
k - ((m+1)/2)sigma + (m-1)/2
 <= m k - 2mu(m-2)sigma.
```

If the finite search is empty, then every clean simple `m`-cycle shape at
these parameters is either full rank by the small-pair gate, cleared by the
private-mass reserve gate, or cleared by the dimension-gap root-sharing
high-reserve gate.

*Proof.* If a residual shape survived all three gates, the residual normal
form would supply the first adjacent-band constraint, the small-pair gate would
force `d_i+d_j<k` for every pair, and nonclearance by the root-sharing
high-reserve gate would force the displayed root-floor inequality. In odd
length, alternating propagation also gives the displayed parity compatibility.
Thus any surviving residual shape gives an integer vector in the finite search.
The contrapositive proves the certificate.

The finite certificate already has a useful analytic clearance consequence.

**Corollary (global pair-cap residual-shape clearance).** Fix `m>=3`,
`mu>=2`, `k`, and `sigma`. If

```text
2(mu(m-2)-1)sigma >= (m-1)k,
```

then the finite residual-shape search in the preceding certificate is empty.
Consequently the current small-pair, private-mass, and root-sharing gates
clear every clean simple `m`-cycle shape at these parameters.

Equivalently, residual shapes can exist only below the threshold

```text
sigma/k < (m-1)/(2(mu(m-2)-1)).
```

This improves the coarse high-reserve window

```text
sigma/k > m/(2mu(m-2))
```

exactly when `mu(m-2)>m`.

*Proof.* Suppose a residual vector survives the finite certificate, and put
`D=min_i d_i`. Choose `t` with `d_t=D`. The lower adjacent band gives

```text
d_{t-1}, d_{t+1} >= k-sigma-D.
```

The global pairwise cap applies to the two neighbors, so

```text
2(k-sigma-D) <= d_{t-1}+d_{t+1} < k.
```

Hence

```text
k-2sigma < 2D.
```

On the other hand, the root-sharing nonclearance condition in the finite
certificate gives

```text
2D <= 2max(2,D) <= m k - 2mu(m-2)sigma.
```

Thus any surviving vector forces

```text
k-2sigma < m k - 2mu(m-2)sigma,
```

or equivalently

```text
2(mu(m-2)-1)sigma < (m-1)k.
```

The contrapositive proves emptiness. The comparison with the coarse
high-reserve threshold is the inequality

```text
(m-1)/(2(mu(m-2)-1)) < m/(2mu(m-2)),
```

which is equivalent to `mu(m-2)>m`.

The same pair-cap argument gives a structural reduction even below the
clearance threshold.

**Corollary (balanced-window residual-shape reduction).** Any vector surviving
the finite residual-shape certificate satisfies

```text
k-2sigma < 2d_i < k+2sigma
```

for every index `i`. Equivalently, every surviving edge overlap
`e_i=k-d_i` also satisfies

```text
k-2sigma < 2e_i < k+2sigma.
```

Thus the finite certificate search may be restricted from all `1<=d_i<k` to
the balanced coordinate window

```text
W(k,sigma)={d in Z: 1<=d<k and k-2sigma < 2d < k+2sigma},
```

which has size at most `2sigma`. In particular, for fixed cycle length `m`,
the residual-shape scan has at most `(2sigma)^m` coordinate vectors before the
root-floor and odd-parity gates are applied.

*Proof.* Fix an index `i`. The lower adjacent band gives

```text
d_{i-1} >= k-sigma-d_i,
d_{i+1} >= k-sigma-d_i.
```

The global pairwise cap gives `d_{i-1}+d_{i+1}<k`; hence

```text
2(k-sigma-d_i) <= d_{i-1}+d_{i+1} < k,
```

so `k-2sigma < 2d_i`. Applying this lower bound to `d_{i-1}` and then using
the strict upper adjacent band `d_{i-1}+d_i<k` gives

```text
2d_i < k+2sigma.
```

Since `e_i=k-d_i`, the same two inequalities are equivalent to the displayed
balanced window for the overlaps. The size bound follows because the open
interval `((k-2sigma)/2,(k+2sigma)/2)` has length `2sigma`.

It is useful to recenter the residual shape around `k/2`.

**Corollary (centered-deviation residual normal form).** For a vector
surviving the finite residual-shape certificate, put

```text
x_i=2d_i-k.
```

Then each `x_i` is an integer congruent to `k` modulo `2`, and the residual
constraints imply

```text
-2sigma < x_i < 2sigma                         for every i,
-2sigma <= x_{i-1}+x_i < 0                     for every i,
x_i+x_j < 0                                    for every i<j,
-m sigma <= sum_i x_i < 0.
```

In particular, at most one coordinate `x_i` is nonnegative. Equivalently, all
but at most one residual dimension satisfy `d_i<k/2`, and all but at most one
edge overlap satisfy `e_i>k/2`.

Thus the finite certificate may be scanned in centered deviations, together
with the same root-floor and odd-cycle compatibility gates, rather than in raw
edge dimensions.

*Proof.* The first displayed bound is the balanced-window corollary. The
adjacent residual band

```text
k-sigma <= d_{i-1}+d_i < k
```

is exactly

```text
-2sigma <= x_{i-1}+x_i < 0.
```

The global pairwise cap `d_i+d_j<k` is exactly `x_i+x_j<0`. Summing the
adjacent deviation inequalities around the cycle gives

```text
-2m sigma <= 2sum_i x_i < 0,
```

which is the displayed total-deviation band after division by `2`. Finally,
if two coordinates were nonnegative, their pair sum would be nonnegative,
contradicting `x_i+x_j<0`.

This gives a sharper finite search decomposition.

**Corollary (one-spike residual-shape scan).** With the notation of the
centered-deviation normal form, set

```text
A=A(k,sigma)={x in Z: x == k mod 2 and -2sigma < x < 2sigma},
A_-={x in A: x<0},
A_+={x in A: x>=0}.
```

Every vector surviving the finite residual-shape certificate lies in

```text
A_-^m  union  union_{t=0}^{m-1}
{x_t in A_+, x_j in A_- for j != t}.
```

Thus the centered residual-shape scan has at most

```text
|A_-|^m + m |A_+| |A_-|^{m-1}
```

candidate vectors before the adjacent-sum, root-floor, and parity gates are
applied. Since `|A_-|,|A_+|<=sigma`, this is at most

```text
(m+1)sigma^m.
```

Equivalently, a surviving residual clean cycle has either every dimension
`d_i<k/2`, or a unique spike with `d_t>=k/2` and all other dimensions below
`k/2`. In overlap variables, all but at most one edge overlap satisfy
`e_i>k/2`.

*Proof.* The balanced-window corollary restricts every centered deviation to
`A`. The centered-deviation normal form gives `x_i+x_j<0` for every `i<j`.
Therefore two coordinates cannot both lie in `A_+`, since their sum would be
nonnegative. This proves the displayed sector decomposition. The count is the
all-negative sector plus the `m` choices of the unique nonnegative coordinate.
The bound by `(m+1)sigma^m` follows from `|A_-|,|A_+|<=sigma`.

The spike sector can be refined by the spike height.

**Corollary (spike-height refined residual-shape scan).** In the one-spike
sector, suppose the unique nonnegative deviation has value `u in A_+`. Then
every other coordinate lies in

```text
A_-(u)={v in A_-: v<=-u-2}.
```

Moreover, a spike of height `u` can occur only if

```text
(m-2)u + 2(m-1) <= m sigma.
```

Consequently the centered residual-shape scan may be restricted to at most

```text
|A_-|^m
+ m sum_{u in A_+, (m-2)u+2(m-1)<=m sigma} |A_-(u)|^{m-1}
```

candidate vectors before the adjacent-sum, root-floor, and parity gates are
applied.

*Proof.* If `x_t=u>=0` is the unique spike, pairwise negativity gives
`u+x_j<0` for every `j != t`. Since all deviations have the same parity, the
left-hand side is an even integer, so `u+x_j<=-2`; hence
`x_j<=-u-2`.

The largest possible total deviation with spike height `u` occurs when every
other coordinate is as large as allowed by this bound, namely `-u-2`. Thus

```text
sum_i x_i <= u+(m-1)(-u-2)=-(m-2)u-2(m-1).
```

The centered-deviation normal form also gives `sum_i x_i>=-m sigma`. If a
spike of height `u` occurs, these two inequalities must be compatible, giving
the displayed spike-height bound. The counting formula follows by summing the
allowed negative choices over the remaining `m-1` coordinates and over the
`m` possible spike positions.

Combining the centered reductions gives an exact smaller certificate.

**Corollary (exact centered residual-shape certificate).** Let

```text
A_dim={2d-k : d in W(k,sigma)}.
```

Build the all-negative and spike-height sectors from `A_dim` exactly as above.
Then the finite residual-shape search is equivalent to the following centered
search. Look for a vector `x=(x_0,...,x_{m-1})` in those sectors such that

```text
-2sigma <= x_{i-1}+x_i < 0                       for every i,
2mu(m-2)sigma - m k + max(4,k+min_i x_i) <= 0,
```

and, when `m` is odd,

```text
k - ((m+1)/2)sigma + (m-1)/2
 <= m k - 2mu(m-2)sigma.
```

If no such centered vector exists, then every clean simple `m`-cycle shape at
these parameters is already cleared by the current small-pair, private-mass,
or dimension-gap root-sharing gates.

*Proof.* The map `d_i -> x_i=2d_i-k` is a bijection from the balanced
dimension window `W(k,sigma)` to `A_dim`. The residual adjacent band becomes
the displayed adjacent-sum condition. The global pairwise cap is exactly the
pairwise negativity condition, which is already encoded by the all-negative
and spike-height sectors. The root-floor condition

```text
2mu(m-2)sigma - m k + 2max(2,min_i d_i) <= 0
```

becomes the displayed root condition because
`2min_i d_i=k+min_i x_i`. The odd-cycle compatibility is unchanged. Thus the
centered search and the finite residual-shape search have the same candidate
set under the displayed bijection, and the final clearance statement is the
finite residual-shape certificate.

The root-floor gate can be built into the centered sectors.

**Corollary (root-depth refined centered certificate).** In the exact centered
certificate, put

```text
B=m k - 2mu(m-2)sigma.
```

If `B<4`, the centered search is empty. If `B>=4`, the root-floor gate is
equivalent to

```text
min_i x_i <= B-k.
```

Thus the all-negative sector may be restricted to vectors having at least one
coordinate `<=B-k`. In a spike sector of height `u`, with negative alphabet
`A_-(u)`, the remaining coordinates may be counted from

```text
|A_-(u)|^{m-1} - |{v in A_-(u): v>B-k}|^{m-1}
```

unless `u<=B-k`, in which case the spike itself already satisfies the
root-depth condition and all `|A_-(u)|^{m-1}` choices remain. Together with
the spike-height compatibility, this gives an exact root-depth-refined
centered certificate equivalent to the finite residual-shape certificate.

*Proof.* The centered root condition is

```text
2mu(m-2)sigma - m k + max(4,k+min_i x_i) <= 0,
```

or equivalently `max(4,k+min_i x_i)<=B`. If `B<4` this is impossible. If
`B>=4`, it is equivalent to `k+min_i x_i<=B`, namely
`min_i x_i<=B-k`. In the all-negative sector this simply requires at least
one coordinate below the root-depth threshold. In a spike sector, either the
spike value `u` is already below the threshold, or at least one of the
negative coordinates must be below it; subtracting the choices with every
negative coordinate `>B-k` gives the displayed count. The exactness follows
from the exact centered residual-shape certificate.

The exact certificate can be written as a finite transfer-matrix count.

**Corollary (transfer-matrix centered residual certificate).** Keep the
notation of the root-depth refined centered certificate, and assume `B>=4`.
For a finite set `Y` of centered deviations, let `M_Y` be the `0/1` matrix
indexed by `Y` with

```text
(M_Y)_{xy}=1  iff  -2sigma <= x+y < 0.
```

Let `theta=B-k`. The all-negative root-depth sector contributes

```text
tr(M_{A_-}^m) - tr(M_{ {v in A_-: v>theta} }^m).
```

For a permitted spike height `u in A_+`, put

```text
Y_u=A_-(u)={v in A_-: v<=-u-2},
Y_u^>={v in Y_u: v>theta}.
```

If `c_u(Y)` denotes the number of length-`m` cyclic words with `x_0=u`,
all other coordinates in `Y`, and adjacent sums in `[-2sigma,0)`, then the
spike contribution at height `u` is

```text
c_u(Y_u)                         if u<=theta,
c_u(Y_u)-c_u(Y_u^>)              if u>theta.
```

The total number of centered residual-shape candidates is therefore

```text
tr(M_{A_-}^m) - tr(M_{ {v in A_-: v>theta} }^m)
+ m sum_u spike_contribution(u),
```

where the sum is over spike heights satisfying
`(m-2)u+2(m-1)<=m sigma`; if the odd-cycle compatibility fails, the total is
`0`. This count is exactly the finite residual-shape candidate count.

*Proof.* The exact centered certificate already decomposes candidates into
the all-negative sector and the `m` rotations of the single-spike sector. In
each sector the remaining adjacent-band condition is precisely the local edge
condition defining `M_Y`. The trace counts cyclic all-negative words. With a
spike pinned at one coordinate, `c_u(Y)` counts the allowed paths through the
remaining `m-1` coordinates and the two edges incident to the spike; multiplying
by `m` accounts for the spike position. Subtracting the `>theta` alphabets is
exactly the root-depth requirement that at least one coordinate satisfy
`x_i<=theta`, unless the spike itself already does. The odd compatibility is a
global gate from the finite certificate, so failure makes the candidate count
zero.

Equivalently, the obstruction is a depth-packing problem.

**Corollary (depth-transfer residual certificate).** In the all-negative
sector put `y_i=-x_i>0`, and define the root-depth threshold

```text
R=k-B=2mu(m-2)sigma-(m-1)k.
```

Then adjacent feasibility is exactly

```text
y_{i-1}+y_i <= 2sigma,
```

and the root-depth gate is that some depth satisfies `y_i>=R`, unless the
unique spike `u` itself satisfies `u<=B-k=-R`. In a spike sector of height
`u`, the nonspike depths additionally satisfy `y_i>=u+2`.

Thus the residual clean-cycle obstruction is equivalently a finite cyclic
packing problem on positive depths: count cyclic words with adjacent depth
sums at most `2sigma`, with at most one spike and with the root-depth gate
above. In these variables the global pair-cap clearance criterion is simply
the condition

```text
R >= 2sigma,
```

because all possible depths in the balanced window are strictly less than
`2sigma`.

*Proof.* The substitution `y_i=-x_i` sends the adjacent centered inequality
`-2sigma<=x_{i-1}+x_i<0` between two negative coordinates to
`y_{i-1}+y_i<=2sigma`. The spike constraint `u+x_i<0`, together with parity,
is exactly `y_i>=u+2`. The root-depth condition
`min_i x_i<=B-k` becomes `max_i y_i>=k-B=R`, unless the spike already satisfies
the centered root condition. Since the balanced window gives `y_i<2sigma`, no
root depth can exist when `R>=2sigma`; this is the pair-cap clearance
inequality rewritten as
`2(mu(m-2)-1)sigma>=(m-1)k`.

The depth-packing clearance is sharp for the current gates.

**Corollary (canonical depth witness below the root threshold).** Let `D` be
the positive depth alphabet in the depth-transfer certificate, and let
`s=min D`, `Y=max D`. Suppose `B>=4`, the odd-cycle compatibility gate holds
when `m` is odd, and

```text
Y >= R=2mu(m-2)sigma-(m-1)k.
```

Then the exact centered residual-shape certificate is nonempty. In fact, the
all-negative depth vector

```text
(Y,s,s,...,s)
```

and its cyclic rotations survive all gates in the centered certificate.

Thus the pair-cap/depth clearance cannot be improved using only the current
balanced-window, pairwise-cap, root-depth, and odd-compatibility gates: once
the required root depth is attainable by the balanced depth alphabet, there is
already a structural residual candidate.

*Proof.* Since `Y` and `s` are the largest and smallest depths in the balanced
depth alphabet, the parity progression gives `Y+s<=2sigma`. Hence every
adjacent depth sum in `(Y,s,...,s)` is at most `2sigma`. All centered
deviations are negative, so the pairwise negativity gate is automatic. The
root-depth gate holds because `Y>=R`, and the root budget assumption `B>=4`
removes the exceptional empty case. The odd gate is assumed when needed.
Therefore the exact centered residual-shape certificate contains this vector
and all of its cyclic rotations.

Near the depth threshold, root-active depths are forced to be sparse.

**Corollary (root-active depth packing).** In a depth-transfer residual
candidate, call a nonspike depth `y_i` root-active if

```text
y_i >= R=2mu(m-2)sigma-(m-1)k.
```

If `R>sigma`, then no two adjacent nonspike depths are both root-active. More
precisely, if `y_i` is root-active and a neighboring coordinate is also a
nonspike depth `y_j`, then

```text
y_j <= 2sigma-y_i <= 2sigma-R < sigma.
```

Thus, in the all-negative sector, root-active depths form an independent set
in the cycle; in a one-spike sector, they form an independent set in the path
obtained by deleting the spike.

*Proof.* This is immediate from the depth-packing edge condition
`y_i+y_j<=2sigma` on every adjacent pair of nonspike depths. If both adjacent
depths were root-active, their sum would be at least `2R>2sigma`, a
contradiction. The displayed neighbor bound is the same inequality solved for
`y_j`.

Before bounding, one can keep the exact transfer count.

**Corollary (exact root-active transfer subtraction).** Assume `B>=4`, the
odd-cycle compatibility gate holds when needed, and `R>sigma`. For a finite
positive depth alphabet `Y`, let `A_Y` be the `0/1` matrix indexed by `Y` with

```text
(A_Y)_{yz}=1  iff  y+z<=2sigma.
```

Let `D` be the all-negative depth alphabet and put

```text
L={y in D: y<R}.
```

Then the all-negative root-active contribution is exactly

```text
tr(A_D^m)-tr(A_L^m).
```

For a permitted spike height `u`, put

```text
D_u={y in D: y>=u+2},        L_u={y in D_u: y<R}.
```

If

```text
Q_u(Y)=1^T A_Y^{m-2} 1
```

is the pinned-spike path count through the `m-1` nonspike depths, then the
spike sector with that pinned height contributes exactly

```text
Q_u(D_u)-Q_u(L_u).
```

Thus the exact root-active residual count is

```text
tr(A_D^m)-tr(A_L^m)
+ m sum_u ( Q_u(D_u)-Q_u(L_u) ),
```

where the sum is over the spike heights satisfying the spike-height
compatibility. If `B<4` or the odd gate fails, the count is `0`.

*Proof.* In the depth-transfer certificate, the root-depth gate is the
existence of a nonspike depth `y_i>=R`, except when the spike itself satisfies
`u<=-R`. Under the present assumption `R>sigma>0`, no nonnegative spike height
can satisfy `u<=-R`, so every surviving sector must contain a root-active
nonspike depth. The full transfer count on `D` counts all depth words obeying
the adjacent packing inequalities; the transfer count on `L` counts exactly
those with no root-active depth. Subtracting gives the displayed all-negative
formula. The same subtraction on `D_u` and `L_u` gives the pinned-spike
formula, because the spike constraints are already absorbed into the lower
bound `y>=u+2`. The empty `B<4` and odd-incompatible cases are the global
gates from the exact depth-transfer certificate.

The subtraction formula can be expanded by the exact set of root-active
positions.

**Corollary (root-active bridge expansion).** Assume the hypotheses of the
exact root-active transfer subtraction corollary. For a finite positive depth
alphabet `E`, put

```text
H_E={y in E: y>=R},          L_E={y in E: y<R}.
```

If `J` is a path of `r>=1` low vertices whose adjacent high boundary depths
are `alpha` on the left and `beta` on the right when those boundaries exist,
define

```text
Bridge_E(J;alpha,beta)
```

to be the number of sequences `(z_1,...,z_r) in L_E^r` satisfying

```text
z_i+z_{i+1}<=2sigma                 for internal adjacent pairs,
alpha+z_1<=2sigma                   if the left boundary exists,
z_r+beta<=2sigma                    if the right boundary exists.
```

For the all-negative cycle sector,

```text
sum_{empty != I independent in C_m}
sum_{h:I -> H_D}
prod_{J component of C_m minus I} Bridge_D(J;h)
```

is exactly the all-negative root-active contribution. Here the two high
boundary depths of a low component are read from the assigned values `h` at
the adjacent vertices of `I`.

For a permitted spike height `u`, set `E=D_u`. The pinned spike sector is
exactly

```text
sum_{empty != I independent in P_{m-1}}
sum_{h:I -> H_E}
prod_{J component of P_{m-1} minus I} Bridge_E(J;h),
```

where endpoint components of the path have only the one high boundary that
exists.

In particular, replacing every bridge factor by the free bound
`|L_E|^{|J|}` recovers the independent-set upper bound.

*Proof.* Because `R>sigma`, the root-active vertices form an independent set
in the relevant graph. Partition every admissible depth word by the exact set
`I` of root-active nonspike positions and by the high-depth assignment
`h:I->H_E`. The remaining vertices are low-depth components of the complement
of `I`; on each component the only constraints left are the internal
adjacent-depth inequalities and the boundary inequalities against adjacent
high depths. These are exactly the displayed bridge counts, and different
components are independent once `I` and `h` are fixed. This proves both the
cycle and path formulas. Forgetting the internal and boundary inequalities in
each low component gives at most `|L_E|^{|J|}` choices, which is precisely the
root-active independent-set bound.

Each bridge has a capped-transfer bound that still remembers the high
boundary depths.

**Corollary (capped bridge transfer bound).** In the bridge expansion, let
`T_E` be the low-depth transfer matrix on `L_E`,

```text
(T_E)_{zw}=1 iff z+w<=2sigma,
```

and for a high boundary depth `alpha in H_E`, put

```text
C_E(alpha)={z in L_E: z<=2sigma-alpha}.
```

If a bridge has length `r>=1` and two high boundaries `alpha,beta`, then

```text
Bridge_E(r;alpha,beta)
 = 1_{C_E(alpha)}^T T_E^{r-1} 1_{C_E(beta)}.
```

If it has only the left boundary `alpha`, then

```text
Bridge_E(r;alpha,*)=1_{C_E(alpha)}^T T_E^{r-1} 1_{L_E},
```

and similarly for a right boundary. Let

```text
Delta_E=max_{z in L_E} |{w in L_E: z+w<=2sigma}|.
```

Then

```text
Bridge_E(r;alpha,beta)
 <= min(|C_E(alpha)|,|C_E(beta)|) Delta_E^{r-1},
Bridge_E(r;alpha,*) <= |C_E(alpha)| Delta_E^{r-1},
Bridge_E(r;*,beta) <= |C_E(beta)| Delta_E^{r-1}.
```

Since `R>sigma`, every cap `C_E(alpha)` lies below `sigma`; hence these
bounds retain the shallow-neighbor forcing caused by root-active depths. They
are always at most the free bridge bound `|L_E|^r`, so substituting them into
the bridge expansion gives an upper bound between the exact transfer count
and the independent-set bound.

*Proof.* The matrix identities are just the definition of a bridge: the
initial and terminal vectors impose the boundary inequalities, and the powers
of `T_E` impose the internal adjacent-depth inequalities. The row sum of
`T_E` is at most `Delta_E`, so after choosing an allowed boundary-adjacent
start (or equivalently running the same argument from the right) there are at
most `Delta_E^{r-1}` continuations. This gives the displayed inequalities.
The inclusion `C_E(alpha) subset {z<sigma}` follows from
`alpha>=R>sigma`, because `z<=2sigma-alpha<sigma`. Finally,
`|C_E(alpha)|<=|L_E|` and `Delta_E<=|L_E|`, so every capped bridge bound is
bounded by `|L_E|^r`.

The capped bridge bounds have a uniform envelope depending only on three
numbers.

**Corollary (uniform cap-degree bridge envelope).** In the notation of the
capped bridge transfer bound, put

```text
h_E=|H_E|,        c_E=max_{alpha in H_E} |C_E(alpha)|.
```

Let `k(I)=|I|`, and let `b(I)` be the number of low components of the
complement of `I` in the relevant cycle or path. Then the all-negative cycle
sector is bounded by

```text
sum_{empty != I independent in C_m}
h_D^{k(I)} c_D^{b(I)} Delta_D^{m-k(I)-b(I)}.
```

For a permitted spike height `u`, with `E=D_u`, the pinned spike sector is
bounded by

```text
sum_{empty != I independent in P_{m-1}}
h_E^{k(I)} c_E^{b(I)} Delta_E^{m-1-k(I)-b(I)}.
```

These uniform cap-degree bounds dominate the exact capped bridge expansion
and are dominated by the root-active independent-set bound.

*Proof.* In every bridge component of length `r`, the capped bridge transfer
bound gives at most `c_E Delta_E^{r-1}` choices, because every low component
in the complement of a nonempty independent set has at least one high
boundary. After choosing the root-active set `I`, there are `h_E^{k(I)}`
choices for its high-depth labels. Multiplying the bridge bounds over all
low components gives `c_E^{b(I)} Delta_E^{sum(r_J-1)}`. Since the total
number of low vertices is `n-k(I)`, the exponent is `n-k(I)-b(I)`, with
`n=m` in the cycle sector and `n=m-1` in a pinned spike sector. Finally,
`c_E<=|L_E|` and `Delta_E<=|L_E|`, so this is bounded by
`h_E^{k(I)} |L_E|^{n-k(I)}`, the corresponding independent-set term.

The three parameters in the uniform envelope are explicit order statistics of
the depth alphabet; no transfer-matrix optimization is hidden here.

**Corollary (monotone formula for the uniform cap parameters).** Let `E` be a
finite positive depth alphabet, and assume `R>sigma`. Put

```text
H_E={y in E: y>=R},        L_E={y in E: y<R}.
```

If `H_E` is nonempty, let `alpha_0=min H_E`; otherwise set `c_E=0`. If
`L_E` is nonempty, let `z_0=min L_E`; otherwise set `Delta_E=0`. Then

```text
h_E=|H_E|,
c_E=|{z in L_E: z<=2sigma-alpha_0}|        if H_E nonempty,
Delta_E=|{w in L_E: w<=2sigma-z_0}|        if L_E nonempty.
```

These values are exactly the parameters used in the uniform cap-degree
envelope. In particular, for every permitted spike height `u`, the pinned
sector parameters are obtained by applying the same formulas to `E=D_u`.

*Proof.* The boundary cap size

```text
|C_E(alpha)|=|{z in L_E: z<=2sigma-alpha}|
```

is monotone nonincreasing in the root-active boundary depth `alpha`; hence its
maximum over `H_E` is attained at `alpha_0=min H_E`. Similarly, the low-depth
transfer row sum

```text
|{w in L_E: z+w<=2sigma}|
```

is monotone nonincreasing in the low starting depth `z`, so the maximum row
sum is attained at `z_0=min L_E`. The formula for `h_E` is the definition.

For the actual balanced residual alphabets, the same parameters have a closed
parity-progression form.

**Corollary (balanced-depth formula for the uniform cap parameters).** Let
`D` be the all-negative depth alphabet in the depth-transfer residual
certificate. Then

```text
D={s,s+2,...,Y},
```

where `s` is the least positive integer congruent to `k mod 2`, and `Y` is
the largest integer congruent to `k mod 2` with

```text
Y <= min(k-2, 2sigma-1).
```

If no such `Y>=s` exists, then `D` is empty. For a permitted spike height
`u`, the pinned alphabet is the tail

```text
D_u={y in D: y>=u+2}.
```

Thus every nonempty alphabet appearing in the root-active bridge envelope is
a tail

```text
E={s_E,s_E+2,...,Y}.
```

For such a tail, write

```text
N_E(A,B)=|{y in E: A<=y<=B}|.
```

Let `alpha_E` be the least element of `E` with `alpha_E>=R`, if it exists.
If `alpha_E` exists, then

```text
h_E=N_E(alpha_E,Y),
c_E=N_E(s_E, min(alpha_E-2, 2sigma-alpha_E)),
Delta_E=N_E(s_E, min(alpha_E-2, 2sigma-s_E)).
```

If `alpha_E` does not exist, then `h_E=c_E=0` and

```text
Delta_E=N_E(s_E, min(Y, 2sigma-s_E)).
```

These formulas apply to `E=D` and to every nonempty spike tail `E=D_u`.

*Proof.* A negative centered deviation has the form `x=2d-k<0`, so the depth
`y=-x=k-2d` is positive and congruent to `k mod 2`. The balanced-window
inequality `-2sigma<x<2sigma`, together with `d>=1`, is exactly
`0<y<2sigma` and `y<=k-2`. This gives the displayed parity progression for
`D`, and the spike constraint is `y>=u+2`, so `D_u` is a tail of the same
progression.

Now apply the monotone parameter formula to a tail `E`. If `alpha_E` exists,
then the high depths are precisely `{y in E: y>=alpha_E}`, giving
`h_E=N_E(alpha_E,Y)`, and the low depths are the earlier elements
`{y in E: y<=alpha_E-2}`. The cap formula counts low depths at most
`2sigma-alpha_E`, giving the displayed formula for `c_E`; the low-transfer
degree is attained at the least low depth `s_E` and counts low depths at most
`2sigma-s_E`, giving the formula for `Delta_E`. If no high depth exists, then
`h_E=c_E=0` and all elements of `E` are low, giving the final displayed
formula for `Delta_E`.

This identifies exactly when the uniform bridge envelope gains a real
exponential-rate saving over the independent-set envelope.

**Corollary (balanced-tail strict-rate criterion).** Keep the notation of the
balanced-depth formula, and let `E={s_E,s_E+2,...,Y}` be one of the nonempty
balanced tails. Suppose both

```text
H_E={y in E: y>=R},        L_E={y in E: y<R}
```

are nonempty, and let `alpha_E=min H_E`. Put `l_E=|L_E|`. Then

```text
c_E=l_E      iff alpha_E=sigma+1,
c_E<l_E      iff alpha_E>=sigma+2.
```

Moreover, when `alpha_E=sigma+1`, one also has `Delta_E=l_E`. Consequently
the Perron rate of the uniform cap-degree envelope is strictly smaller than
the independent-set rate for this tail exactly when

```text
alpha_E>=sigma+2.
```

Thus the only nonempty balanced tails with no real rate gain are the
minimal-frontier tails whose first root-active depth is the first integer
layer above `sigma`.

*Proof.* Since `R>sigma`, the first high depth satisfies `alpha_E>sigma`.
The low depths are exactly the progression elements in
`[s_E,alpha_E-2]`. The cap formula from the previous corollary reduces to

```text
c_E=N_E(s_E,2sigma-alpha_E),
```

because `alpha_E>sigma` implies `2sigma-alpha_E<=alpha_E-1`, and parity puts
the effective cutoff at most `alpha_E-2`. Hence the cap includes every low
depth exactly when `2sigma-alpha_E>=alpha_E-2`, equivalently
`alpha_E<=sigma+1`. Since `alpha_E>sigma`, this is the case
`alpha_E=sigma+1`; otherwise `alpha_E>=sigma+2` and the top low layer is
missing from the cap.

If `alpha_E=sigma+1`, then the low-depth transfer cutoff at the least low
depth is at least the top low depth:

```text
2sigma-s_E >= sigma-1 = alpha_E-2,
```

so `Delta_E=l_E`. The spectral-rate corollary says that the uniform Perron
root is strictly smaller than the independent-set root exactly when
`c_E<l_E` or `Delta_E<l_E` in a nontrivial tail. The previous paragraphs show
this happens exactly for `alpha_E>=sigma+2`.

The nonsaving frontier therefore has a small exact core.

**Corollary (minimal-frontier core split).** In the setting of the previous
corollary, assume `alpha_E=sigma+1`. Let

```text
L_E={s_E,s_E+2,...,sigma-1},       a_0=sigma+1,
G_E=H_E \ {a_0}.
```

On the alphabet `L_E union {a_0}`, the only adjacent-depth obstruction is
that two `a_0` vertices cannot be adjacent. Hence, for a cycle or path graph
`G` with `n` vertices, the root-active words using only the minimal
root-active depth `a_0` are counted exactly by

```text
sum_{empty != I independent in G} |L_E|^{n-|I|}.
```

Equivalently, this is the root-active independent-set polynomial with high
weight `1` rather than high weight `|H_E|`.

Every remaining root-active word contains an elevated depth
`gamma in G_E`, and each low component adjacent to such a depth has a strict
boundary cap:

```text
|C_E(gamma)| < |L_E|.
```

Thus the minimal-frontier obstruction splits into a one-label hard-core core
and a remainder that already sees cap loss at every elevated boundary.

*Proof.* Since `a_0=sigma+1`, every low depth is at most `sigma-1`. Therefore
low-low adjacent sums are at most `2sigma-2`, and low-`a_0` adjacent sums are
at most `2sigma`. The only forbidden adjacency in `L_E union {a_0}` is
`a_0+a_0>2sigma`. Choosing the positions of the `a_0` vertices is therefore
exactly choosing a nonempty independent set, and every other vertex has
`|L_E|` independent choices.

If `gamma in G_E`, then `gamma>=sigma+3` because the depths have step size
`2`. The top low depth `sigma-1` is not in `C_E(gamma)`, since
`gamma+sigma-1>=2sigma+2`. Hence `|C_E(gamma)|<|L_E|`.

The one-label core has its own recurrence and rate.

**Corollary (minimal-frontier core recurrence).** In the minimal-frontier
case `alpha_E=sigma+1`, put `l=|L_E|`. Let

```text
P_n^{min}=P_n(1,l)-l^n,        C_n^{min}=C_n(1,l)-l^n,
```

where `P_n(h,l)` and `C_n(h,l)` are the path and cycle independent-set
polynomials from the root-active recurrence corollary. Then `P_n^{min}` and
`C_n^{min}` count exactly the minimal-frontier core on paths and cycles,
respectively. Their characteristic rate is

```text
rho_min(l)=(l+sqrt(l^2+4l))/2.
```

If the full root-active tail has `h_E=|H_E|>1`, then

```text
rho_min(l) < rho_ind(h_E,l).
```

Thus even in the nonsaving `alpha_E=sigma+1` frontier, the exact one-label
core has smaller rate than the old independent-set envelope whenever an
elevated root-active depth is present; the elevated remainder is already
covered by the cap-loss part of the previous split.

*Proof.* The previous corollary identifies the core with independent sets
whose marked vertices all carry the single label `a_0`, while every unmarked
vertex has `l` low choices. This is precisely the independent-set polynomial
with high weight `1`, with the all-low word subtracted to enforce nonempty
root-active support. The recurrence and characteristic root are the
root-active recurrence and spectral corollaries specialized to `h=1`.
Finally, `rho_ind(h,l)` is strictly increasing in `h` for `l>0`; here
`l>0` by the nontrivial-tail assumption, so `h_E>1` gives the displayed
strict inequality.

The core and elevated remainder can be packaged in one transfer envelope.

**Corollary (one-sided minimal-frontier envelope).** Keep the
minimal-frontier notation and set

```text
l=|L_E|,       g=|G_E|,       c_G=max_{gamma in G_E} |C_E(gamma)|,
```

with `c_G=0` if `G_E` is empty. On the state set `{A,G,L}`, where `A`
denotes the single minimal root-active depth `a_0`, `G` denotes an elevated
root-active depth in `G_E`, and `L` denotes a low depth, define

```text
T_min =
[[0, 0, l  ],
 [0, 0, c_G],
 [1, g, l  ]].
```

Rows are current states and columns are next states. Then the all-negative
cycle contribution on `E` is bounded by

```text
tr(T_min^n)-l^n.
```

For a path of length `n`, put `v_1=(1,g,l)` and `v_{n+1}=v_n T_min`; the
corresponding pinned-sector contribution is bounded by

```text
sum(v_n)-l^n.
```

These bounds contain the exact one-label core from the previous corollary.
They are dominated by the old independent-set recurrence with high weight
`1+g` and low weight `l`; the domination is strict whenever `g>0`, `c_G<l`,
and the sector has room for an elevated root-active depth followed by a low
vertex.

*Proof.* High-high adjacencies are impossible because every root-active depth
is greater than `sigma`. A transition `L->A` chooses the unique minimal
root-active label, while `L->G` chooses one of the `g` elevated labels. A
transition `A->L` has all `l` low choices, since `a_0+z<=2sigma` for every
`z in L_E`. A transition `G->L` uses the uniform elevated cap `c_G`, which is
strictly smaller than `l` by the minimal-frontier core split when `g>0`.
Low-low transitions have `l` choices.

For cycles, orient each low component and charge the first low vertex after
an elevated boundary to the `G->L` cap. The other low choices are deliberately
overcounted by `l`, so the trace gives an upper bound; when no elevated label
appears, the transfer is exactly the one-label core. The path recurrence is
the same one-sided scan with initial weights `v_1`.

If the states `A` and `G` are merged into a single high state and `c_G` is
replaced by `l`, this transfer becomes the old independent-set recurrence
with high weight `1+g` and low weight `l`. Since `c_G<=l`, the displayed
minimal-frontier envelope is dominated by that old recurrence.

The three-state envelope also has a two-term characteristic rate.

**Corollary (spectral rate of the minimal-frontier envelope).** With
`l,g,c_G` as above, the nonzero eigenvalues of `T_min` are the roots of

```text
lambda^2 - l lambda - (l+c_G g)=0.
```

Thus the minimal-frontier envelope has exponential rate

```text
rho_front(l,g,c_G)
  = (l + sqrt(l^2+4(l+c_G g)))/2.
```

The old independent-set envelope on the same tail has high weight `1+g` and
rate

```text
rho_old(l,g)
  = (l + sqrt(l^2+4l(1+g)))/2.
```

Since `c_G<=l`, one has `rho_front(l,g,c_G)<=rho_old(l,g)`. The inequality is
strict whenever `g>0` and `c_G<l`.

*Proof.* Compute the characteristic polynomial of

```text
T_min =
[[0, 0, l  ],
 [0, 0, c_G],
 [1, g, l  ]].
```

It is

```text
lambda (lambda^2-l lambda-(l+c_G g)).
```

The Perron root is therefore the displayed positive root. The old
independent-set rate is obtained by merging `A` and `G` into one high state,
which replaces `l+c_G g` by `l+l g=l(1+g)`. The comparison and strictness are
then immediate from monotonicity of the positive root in the constant term.

Combining the strict-frontier and minimal-frontier envelopes gives a single
adaptive residual bound.

**Corollary (frontier-adaptive root-active envelope).** For any balanced tail
`E={s_E,s_E+2,...,Y}` in the `R>sigma` residual certificate, define
`Phi_E(n)` as follows. If the first high depth in `E` is `sigma+1`, let
`Phi_E(n)` be the minimal-frontier envelope from `T_min` on a path or cycle of
length `n`, according to the sector. Otherwise let `Phi_E(n)` be the uniform
cap-degree recurrence/trace envelope with parameters `(h_E,c_E,Delta_E)`.

Then the all-negative root-active transfer is bounded by `Phi_D(m)`, and each
pinned spike sector of height `u` is bounded by `Phi_{D_u}(m-1)`. Therefore
the total root-active residual transfer is bounded by

```text
Phi_D(m) + m sum_u Phi_{D_u}(m-1),
```

with the sum over permitted spike heights. This adaptive envelope is bounded
term-by-term by the uniform cap-degree recurrence envelope. It is strictly
smaller in any sector where the minimal-frontier envelope strictly refines the
old independent-set recurrence.

*Proof.* If the first high depth is `sigma+1`, the one-sided
minimal-frontier transfer envelope bounds the exact transfer and is dominated
by the old independent-set recurrence. In this same case the uniform
cap-degree recurrence agrees with the old independent-set recurrence because
`c_E=Delta_E=|L_E|`. Hence the minimal-frontier envelope is no larger than
the uniform recurrence. If the first high depth is at least `sigma+2`, the
uniform cap-degree envelope already applies. Summing the chosen sector bounds
over the all-negative cycle and all pinned spike positions gives the displayed
total bound.

The adaptive envelope converts the remaining root-active residual problem into
an explicit spectral comparison.

**Corollary (frontier-adaptive spectral reduction).** For a balanced tail
`E={s_E,s_E+2,...,Y}` with first high depth `alpha_E`, define

```text
rho_ad(E)=rho_front(l_E,g_E,c_{G,E})       if alpha_E=sigma+1,
rho_ad(E)=rho_cap(h_E,c_E,Delta_E)         otherwise,
```

with `rho_ad(E)=0` when `E` has no root-active depth. Let

```text
E_*={D} union {D_u : u is a permitted spike height},
rho_* = max_{E in E_*} rho_ad(E).
```

Then for every `Lambda>rho_*` there is a finite constant `C_Lambda`, depending
on the depth alphabets and on `Lambda`, such that the total root-active
residual transfer is bounded by

```text
C_Lambda (1+m |{u}|) Lambda^m.
```

Here `|{u}|` is the number of permitted spike heights. In particular, because
`|{u}|<=|D|<=sigma`, the remaining reserve comparison for this route is the
single explicit spectral inequality `rho_*` versus the available field-entropy
rate; the spike sum contributes only a polynomial prefactor in the
fixed-arity/generated-field window.

*Proof.* For nonminimal-frontier tails, the uniform cap-degree spectral
corollary gives path and cycle envelopes with exponential rate
`rho_cap(h_E,c_E,Delta_E)`. For minimal-frontier tails, the three-state
transfer matrix has nonzero eigenvalues governed by
`rho_front(l_E,g_E,c_{G,E})`; the usual finite-dimensional matrix-power bound
therefore gives the same statement with rate `rho_front`. Choose
`Lambda>rho_*` and take the maximum of the finitely many sector constants over
`E_*`. The all-negative sector has length `m`, while every pinned spike sector
has length `m-1`; since `Lambda>=1`, the latter are bounded by the same
`Lambda^m` scale. Summing the all-negative sector and the `m` rotations of
each permitted spike height gives the displayed bound.

For the balanced residual alphabets, the maximum sector rate is actually the
all-negative one.

**Corollary (spike-tail spectral monotonicity).** Let

```text
D={s,s+2,...,Y}
```

be the all-negative depth alphabet, and let `E={s_E,s_E+2,...,Y}` be any
terminal balanced tail of `D`. Then

```text
rho_ad(E) <= rho_ad(D).
```

Consequently every spike-tail alphabet `D_u={y in D:y>=u+2}` has adaptive
rate at most the all-negative rate, and the spectral reduction above may take

```text
rho_* = rho_ad(D)
```

rather than the maximum over all spike sectors.

*Proof.* Passing from a balanced tail to a later terminal tail only removes
initial depth layers. In a nonminimal-frontier tail, until all low depths are
removed, the parameters

```text
h_E, c_E, Delta_E
```

are weakly nonincreasing: the high alphabet does not grow, the boundary cap
loses low layers, and the low-transfer row degree loses possible starts and
targets. The Perron root
`rho_cap(h_E,c_E,Delta_E)` is increasing in these nonnegative parameters, so
the rate cannot increase. Once there are no high depths or no low depths, the
root-active path/cycle envelope has rate `0`.

In a minimal-frontier tail, while low depths remain the first high depth stays
`sigma+1`; deleting initial low layers weakly decreases `l_E` and the elevated
cap `c_{G,E}`, while the elevated count `g_E` does not increase. The formula
for `rho_front(l_E,g_E,c_{G,E})` is increasing in these nonnegative
parameters, so it also cannot increase. If the tail starts at or above
`sigma+1`, no low layer remains and the rate is again `0`. The spike alphabets
are exactly terminal tails of `D` by the balanced-depth formula, proving the
claim.

The all-negative rate has an explicit gap below the free depth alphabet.

**Corollary (all-negative adaptive free-alphabet gap).** In the all-negative
sector, let

```text
N=|D|,        H_D={y in D:y>=R},        h=|H_D|.
```

If `h=0`, then the root-active contribution is zero. If `h>0`, then

```text
rho_ad(D) < N - h^2/(2N).
```

Equivalently, the all-negative adaptive spectral radius is separated from the
free balanced-depth alphabet size by a fully explicit gap depending only on
the number of root-active depth layers.

*Proof.* Let `l=|L_D|=N-h`. In the nonminimal-frontier case the all-negative
balanced progression has `Delta_D=l`, so the adaptive rate is the positive
root of

```text
lambda^2-l lambda - h c_D = 0,
```

with `0<=c_D<=l`. Evaluating the characteristic polynomial at `N` gives

```text
N^2-lN-hc_D = h(N-c_D) >= h^2.
```

In the minimal-frontier case write `h=1+g`, where the one minimal high layer is
`a_0=sigma+1` and `g` is the number of elevated high layers. The adaptive rate
is the positive root of

```text
lambda^2-l lambda-(l+c_G g)=0.
```

Here `0<=c_G<=l`, and

```text
N^2-lN-(l+c_G g)
 = h^2+g(l-c_G) >= h^2.
```

Thus in either case the characteristic polynomial is positive at `N`, while
its positive root is `rho_ad(D)`. Therefore `rho_ad(D)<N`. Moreover

```text
N-rho_ad(D)
 = [N^2-lN-K]/[N+rho_ad(D)-l],
```

where `K` denotes the corresponding constant term `h c_D` or `l+c_G g`.
Since `rho_ad(D)<N`, the denominator is less than `2N`, and the numerator is
at least `h^2`. This gives the displayed gap.

The proof records a sharper numerator which is the useful reserve quantity.

**Corollary (exact adaptive gap numerator).** Keep the notation of the
previous corollary and define `G_ad(D)` as follows. If the all-negative sector
is not minimal-frontier, let

```text
G_ad(D)=h(N-c_D).
```

If it is minimal-frontier, write `h=1+g`, where `g` counts elevated
root-active depths, and let `c_G` be the elevated boundary cap. Then set

```text
G_ad(D)=h^2+g(l-c_G),        l=|L_D|.
```

In both cases

```text
G_ad(D) = N^2-lN-K,
```

where `K` is the constant term in the adaptive characteristic polynomial.
Consequently

```text
rho_ad(D) < N - G_ad(D)/(2N),
        G_ad(D) >= h^2.
```

Equivalently, if

```text
gamma = G_ad(D)/N^2,
```

then

```text
rho_ad(D) < (1-gamma/2)N.
```

In particular a positive-density root-active frontier, `h>=beta N`, gives the
uniform fractional saving

```text
rho_ad(D) < (1-beta^2/2)N,
```

while the worst case `h=1` has only the quadratic-scale gap
`G_ad(D)/N^2 >= 1/N^2`.

*Proof.* In the nonminimal-frontier case, the previous proof computed

```text
N^2-lN-hc_D=h(N-c_D),
```

which is the first formula. In the minimal-frontier case it computed

```text
N^2-lN-(l+c_G g)=h^2+g(l-c_G).
```

Both displays are exactly `N^2-lN-K`. The same denominator identity

```text
N-rho_ad(D) = G_ad(D)/(N+rho_ad(D)-l)
```

and the bound `N+rho_ad(D)-l<2N` give
`rho_ad(D)<N-G_ad(D)/(2N)`. Since `G_ad(D)>=h^2`, dividing by `N^2` gives the
density and worst-case forms.

The size of the root-active frontier is itself an exact depth-threshold
condition.

**Corollary (tail-depth density dichotomy).** Let

```text
D={s,s+2,...,Y},        N=|D|,
H_D={y in D:y>=R},      h=|H_D|.
```

For every integer `1<=H<=N`,

```text
h>=H        iff        R <= Y-2(H-1).
```

Consequently, if `R <= Y-2(H-1)`, then

```text
G_ad(D)/N^2 >= (H/N)^2,
rho_ad(D) < (1-H^2/(2N^2))N.
```

If this condition fails, then every root-active depth lies in the top `H-1`
layers of the balanced depth progression. In particular,

```text
h >= ceil(N/2)        iff        R <= Y-2(ceil(N/2)-1),
```

and this half-density case gives the uniform bound

```text
rho_ad(D) < 7N/8.
```

At the opposite extreme,

```text
h=1        iff        R <= Y and (N=1 or Y-2 < R),
```

so for `N>=2` the weakest nonzero frontier is exactly the top depth layer. If
`R>Y`, then `h=0` and the root-active contribution is absent.

*Proof.* The elements of `D` form a parity progression with step `2`. Having
at least `H` root-active layers means that the `H`-th element down from the
top,

```text
Y-2(H-1),
```

is still root-active, which is equivalent to
`R<=Y-2(H-1)`. If this fails, the tail above `R` contains at most `H-1`
progression layers. The gap estimates follow from `G_ad(D)>=h^2` in the
exact-gap corollary. Taking `H=ceil(N/2)` gives
`H^2/N^2>=1/4`, hence `rho_ad(D)<(1-1/8)N=7N/8`. The `h=1` statement is
the case where the threshold leaves exactly one progression layer: either the
alphabet already has one layer, or the threshold lies above the second-highest
layer. The `h=0` statement is the case where the threshold lies above the top
layer.

The uniform envelope has a two-state recurrence.

**Corollary (recurrence form of the uniform cap-degree envelope).** Fix
nonnegative integers `h,c,Delta`. For paths, let `A_n` be the total weight of
valid length-`n` high/low words ending in a high vertex, and let `B_n` be the
total weight of such words ending in a low vertex, with high vertices weighted
by `h`, the first vertex of each low component weighted by `c`, and each
later vertex of that low component weighted by `Delta`. Then

```text
A_1=h,        B_1=c,
A_{n+1}=h B_n,
B_{n+1}=c A_n+Delta B_n.
```

The nonempty-high path envelope is therefore

```text
P_n=A_n+B_n-c Delta^{n-1}        for n>=1,
```

where the subtracted term is the all-low word.

For cycles, put

```text
T = [[0, c],
     [h, Delta]].
```

Then the nonempty-high cycle envelope is

```text
U_n=tr(T^n)-Delta^n.
```

Consequently the uniform cap-degree bound for the root-active residual
frontier is computable in `O(m)`: use `U_m` for the all-negative sector and
`P_{m-1}` for each pinned spike sector, with `(h,c,Delta)` specialized to the
corresponding depth alphabet.

*Proof.* For paths, appending a high vertex is possible only after a low
vertex and contributes weight `h`, giving `A_{n+1}=hB_n`. Appending a low
vertex after a high vertex starts a new low component and contributes `c`;
appending a low vertex after a low vertex extends the component and
contributes `Delta`. This gives the recurrence for `B_{n+1}`. The only word
with no high vertices is the all-low word, which has weight
`c Delta^{n-1}`.

For cycles, use the transfer matrix with rows indexed by the current symbol
and columns by the next symbol: transitions `H->H` are forbidden, `H->L`
starts a low component with weight `c`, `L->H` contributes a high vertex with
weight `h`, and `L->L` extends a low component with weight `Delta`. Taking the
trace of `T^n` sums cyclic words with these transition weights. The all-low
cycle contributes `Delta^n` and is subtracted.

The recurrence has an explicit spectral rate.

**Corollary (spectral rate of the uniform cap-degree envelope).** Keep the
notation of the recurrence corollary and put

```text
rho_cap(h,c,Delta) = (Delta + sqrt(Delta^2+4hc))/2.
```

Then both the path envelopes `P_n` and the cycle envelopes `U_n` have
exponential rate at most `rho_cap(h,c,Delta)`. Equivalently, for every
`Lambda>rho_cap(h,c,Delta)` there is a constant `C_Lambda`, depending only on
`h,c,Delta,Lambda`, such that `P_n,U_n <= C_Lambda Lambda^n`.

If `l` is the low-depth alphabet size in the older independent-set envelope,
then

```text
rho_cap(h,c,Delta) <= rho_ind(h,l)
    := (l + sqrt(l^2+4hl))/2
```

whenever `c<=l` and `Delta<=l`. The inequality is strict if `h>0`, `l>0`,
and at least one of `c<l` or `Delta<l` holds.

*Proof.* The path recurrence is driven by the nonnegative matrix

```text
M_cap = [[0, h],
         [c, Delta]],
```

whose characteristic polynomial is `lambda^2-Delta lambda-hc`. The cycle
trace matrix is its transpose, so it has the same eigenvalues. Hence the
Perron root is `rho_cap`, and the claimed exponential-rate bound follows from
the usual finite-dimensional matrix-power estimate. The independent-set
recurrence is the special envelope with matrix

```text
M_ind = [[0, h],
         [l, l]].
```

Because `M_cap<=M_ind` entrywise when `c<=l` and `Delta<=l`, Perron-Frobenius
monotonicity gives `rho_cap<=rho_ind`. If `h,l>0`, then `M_ind` is irreducible
and increasing either the lower-left entry from `c` to `l` or the lower-right
entry from `Delta` to `l` strictly increases the Perron root, giving the
strict case.

For triangles, the transfer subtraction has a closed form.

**Corollary (closed triangular root-active count).** Assume the hypotheses of
the exact root-active transfer subtraction corollary and set `m=3`. For
`y in D`, define

```text
N_D(y)=|{z in D: z<=2sigma-y}|.
```

Then the all-negative triangular contribution is exactly

```text
3 sum_{y in D, y>=R} N_D(y)^2.
```

For a permitted spike height `u`, define `D_u` as above and

```text
N_u(y)=|{z in D_u: z<=2sigma-y}|.
```

The pinned spike sector of height `u` contributes exactly

```text
2 sum_{y in D_u, y>=R} N_u(y).
```

Thus the whole triangular root-active residual count is

```text
3 sum_{y in D, y>=R} N_D(y)^2
+ 3 sum_u 2 sum_{y in D_u, y>=R} N_u(y),
```

with the outer spike sum over the permitted spike heights. If the odd gate
fails or `B<4`, the count is `0`.

*Proof.* Since `R>sigma`, two root-active nonspike depths cannot be adjacent.
In a triangle every pair of nonspike depths is adjacent in the all-negative
sector, so there is exactly one root-active depth. Choose its position, choose
its value `y>=R`, and choose the two neighboring depths from
`{z in D: z<=2sigma-y}`. These two neighbors are automatically adjacent to
each other because each is at most `2sigma-y<sigma`, so their sum is strictly
less than `2sigma`. This proves the all-negative formula.

In a triangular spike sector there are only two nonspike depths joined by one
edge. Again there is exactly one root-active nonspike depth; choose which of
the two positions is root-active, choose its value `y`, and choose the other
depth from `{z in D_u: z<=2sigma-y}`. The spike constraints are already
encoded by membership in `D_u`, giving the displayed pinned-spike formula.

For squares, a second root-active depth can occur, but only opposite the
first one. This gives the first interaction term beyond the triangular case.

**Corollary (closed square root-active count).** Assume the hypotheses of the
exact root-active transfer subtraction corollary and set `m=4`. For a finite
positive depth alphabet `E`, put

```text
H_E={y in E: y>=R},          L_E={y in E: y<R},
N_E(y)=|{z in E: z<=2sigma-y}|,
M_E(b,c)=|{z in E: z<=min(2sigma-b,2sigma-c)}|.
```

Then the all-negative square contribution is exactly

```text
4 sum_{y in H_D} sum_{b,c in D, b,c<=2sigma-y} M_{L_D}(b,c)
+ 2 sum_{y,z in H_D} N_D(max(y,z))^2.
```

For a permitted spike height `u`, set `E=D_u`. The pinned spike sector of
height `u` contributes exactly

```text
sum_{y in H_E} N_E(y)^2
+ 2 sum_{y in H_E} sum_{b in E, b<=2sigma-y} N_{L_E}(b)
+ sum_{y,z in H_E} N_E(max(y,z)).
```

The whole square root-active residual count is the all-negative contribution
plus `4` times the sum of these pinned spike-sector contributions over
permitted spike heights. If the odd gate fails or `B<4`, the count is `0`.

*Proof.* Since `R>sigma`, root-active nonspike depths cannot be adjacent.
In a square all-negative sector, the root-active set therefore has either one
vertex or two opposite vertices. With a single root-active value `y`, there
are `4` choices of its position. Its two neighbors must lie in
`{b in D: b<=2sigma-y}`. The opposite vertex must be low and adjacent to both
neighbors, giving the factor `M_{L_D}(b,c)`. With two root-active depths,
they must occupy one of the two opposite pairs. For ordered values `y,z`, the
two remaining vertices are independent choices from
`{b in D: b<=2sigma-max(y,z)}`, giving the second displayed term.

In a pinned square spike sector the nonspike depths form a path of length
`3`. A single root-active depth can sit in the middle, contributing
`sum_y N_E(y)^2`, or at one of the two endpoints, contributing the doubled
endpoint term. Two root-active depths can only occupy both endpoints; for
ordered endpoint values `y,z`, the middle depth has
`N_E(max(y,z))` choices. These cases are disjoint and exhaustive, proving the
pinned-spike formula. The global gates are inherited from the exact
depth-transfer certificate.

For later estimates, this exact count can be bounded by forgetting part of
the adjacent-transfer structure. This gives a coarse but purely
graph-theoretic upper bound near the threshold.

**Corollary (root-active independent-set bound).** Assume `R>sigma`. Let

```text
H={y in D: y>=R},       L={y in D: y<R}.
```

The all-negative depth-transfer contribution is at most

```text
sum_{I independent in C_m, I nonempty} |H|^{|I|}|L|^{m-|I|}.
```

For a spike height `u`, put

```text
D_u={y in D: y>=u+2},  H_u={y in D_u: y>=R},  L_u={y in D_u: y<R}.
```

If the spike does not itself satisfy the root-depth gate, then the pinned
spike contribution is at most

```text
sum_{I independent in P_{m-1}, I nonempty} |H_u|^{|I|}|L_u|^{m-1-|I|},
```

where `P_{m-1}` is the path left after deleting the spike. If the spike itself
satisfies the root gate, the trivial bound `|D_u|^{m-1}` applies. Summing over
spike positions and permitted heights gives an upper bound for the whole
depth-transfer residual count.

*Proof.* For `R>sigma`, the previous corollary shows that the set of
root-active nonspike depths is independent in the relevant graph: the full
cycle in the all-negative sector and the deleted-spike path in a spike sector.
The root-depth gate requires this independent set to be nonempty unless the
spike already satisfies the root condition. Once the independent root-active
set is chosen, this bound forgets the remaining adjacent-sum constraints and
only records whether each unmarked coordinate lies in `L` or `L_u`. This gives
the displayed independence-polynomial upper bounds.

These independence-polynomial bounds have a two-term recurrence.

**Corollary (recurrence form of the root-active bound).** For nonnegative
weights `h,l`, define the path polynomials

```text
P_0=1,        P_1=l+h,
P_n=l P_{n-1}+h l P_{n-2}        for n>=2.
```

Then

```text
P_n=sum_{I independent in P_n} h^{|I|}l^{n-|I|}.
```

For the cycle, for `n>=3`,

```text
C_n=l P_{n-1}+h l^2 P_{n-3}
```

satisfies

```text
C_n=sum_{I independent in C_n} h^{|I|}l^{n-|I|}.
```

Consequently the all-negative part of the root-active bound is
`C_m-|L|^m`, and each non-root-satisfying spike sector is bounded by
`P_{m-1}(|H_u|,|L_u|)-|L_u|^{m-1}`. This gives an `O(m)` recurrence
calculation of the near-threshold residual bound.

*Proof.* For paths, split independent sets by whether the first vertex is
unmarked or marked. If it is unmarked, it contributes weight `l` and leaves a
path of length `n-1`. If it is marked, the next vertex must be unmarked, giving
weight `h l` and leaving a path of length `n-2`. This proves the recurrence
and the path formula. For cycles, either a fixed vertex is unmarked, giving
`l P_{n-1}`, or it is marked, forcing its two neighbors unmarked and leaving a
path of length `n-3`, giving `h l^2 P_{n-3}`. Subtracting the all-unmarked
term enforces the nonempty root-active condition.

The recurrence also gives a closed growth envelope for the remaining frontier.

**Corollary (spectral growth envelope for root-active bounds).** Let
`h,l>=0`, and let `Lambda>=1` satisfy

```text
Lambda^2 >= l Lambda + h l.
```

Put `A=max(1,h+l)`. Then the path polynomials in the preceding corollary obey

```text
P_n <= A Lambda^n        for n>=0.
```

For `n>=3`, the cycle polynomial satisfies

```text
C_n <= P_n <= A Lambda^n.
```

Consequently, when `R>sigma`, the all-negative root-active residual frontier
is bounded by `( |H|+|L| )Lambda(|H|,|L|)^m`, for any admissible
`Lambda(|H|,|L|)`, whenever `|H|+|L|>0` (and by `0` otherwise). A
non-root-satisfying spike sector of length `m-1` has the same bound with
`(H,L)` replaced by `(H_u,L_u)` and exponent `m-1`; a root-satisfying spike
sector is still handled by the trivial `|D_u|^{m-1}` bound.

*Proof.* The path claim is immediate for `P_0` and `P_1`. If it holds at
lengths `n-1` and `n-2`, then

```text
P_n=l P_{n-1}+h l P_{n-2}
   <= A Lambda^{n-2}(l Lambda+h l)
   <= A Lambda^n.
```

For nonnegative weights, every independent set of the cycle `C_n` is also an
independent set of the path obtained by deleting one cyclic edge, so
`C_n<=P_n`. The final residual-frontier bounds substitute
`h=|H|, l=|L|` and the corresponding spike-sector counts.

In particular, if `h>0`, the optimal recurrence rate

```text
rho(h,l)=(l+sqrt(l^2+4hl))/2
```

is strictly smaller than the free alphabet size `h+l`, since

```text
(h+l)^2-(l(h+l)+hl)=h^2>0.
```

Thus every non-root-satisfying root-active sector with at least one
root-active depth gains an exponential-in-`m` saving over the unconstrained
alphabet count. If `h=0`, the required nonempty root-active sector contributes
zero after the all-low term is subtracted.

The finite certificate is monotone in the interleaving arity.

**Corollary (arity monotonicity of residual-shape certificates).** Fix
`m>=3`, `k`, and `sigma>0`. As the arity `mu` increases, the residual-shape
candidate sets in the preceding finite certificate are nested decreasing. In
particular, if the finite search is empty at some arity `mu_0`, then it is
empty for every integer arity `mu>=mu_0`.

*Proof.* The adjacent-band constraints and pairwise cap are independent of
`mu`. The root-floor nonclearance inequality

```text
2mu(m-2)sigma - m k + 2max(2,min_i d_i) <= 0
```

gets only harder as `mu` increases, since `m>=3` and `sigma>0`. In odd length,
the parity compatibility has the right-hand side

```text
m k - 2mu(m-2)sigma,
```

which also decreases with `mu`. Thus every vector surviving at a larger arity
also survives at every smaller arity. The emptiness statement is the
contrapositive.

The connected case also isolates the diagonal exactly.

**Corollary (diagonal is the only zero-loss connected cluster).** Suppose
`G_k` is connected. Then

```text
Pr[S_1,...,S_m in Fib_U(a)] <= q^{-(a-k)}
```

for one random row, with the bound having no extra exponent beyond a single
support only when all the `S_i` are the same `a`-set. If the connected cluster
is not diagonal, then

```text
Pr[S_1,...,S_m in Fib_U(a)] <= q^{-(a-k+1)}.
```

For `mu` independent rows, these exponents are multiplied by `mu`.

*Proof.* Since `G_k` is connected, the cluster-rank lemma gives
`q^{k-|V|}`. Always `|V|>=a`. Equality `|V|=a` holds exactly when every
`S_i` is the same `a`-subset of `H`; this is the diagonal case. Otherwise
`|V|>=a+1`, giving the extra factor `q^{-1}` per row.

Thus the exact-support diagonalization seen in equal-row interleaving is not an
artifact of that special row choice: in the random regular-core model, the only
connected high-overlap clusters with no entropy loss are genuinely diagonal.
Any non-diagonal connected cluster must pay at least `q^{-mu}` beyond one
representative support.

More generally, the loss is exactly controlled by union excess at the level of
this upper bound.

**Corollary (connected cluster union-excess tradeoff).** Suppose `G_k` is
connected and put

```text
d = |S_1 union ... union S_m| - a.
```

Then for one random row

```text
Pr[S_1,...,S_m in Fib_U(a)] <= q^{-(a-k+d)}.
```

For `mu` independent rows the exponent is multiplied by `mu`. Moreover, if the
cluster contains `b` distinct `a`-sets, then

```text
b <= binom(a+d,a) = binom(a+d,d).
```

Equivalently, a connected cluster carrying many distinct supports must either
have large union excess `d`, which pays the entropy factor `q^{-mu d}`, or be a
small polynomial-size cluster inside `a+d` points.

*Proof.* The probability bound is the connected case of the cluster-rank lemma,
where `|V|=a+d`. For the counting statement, every distinct support in the
cluster is an `a`-subset of the common union `V`, whose size is `a+d`.

This gives a moment-counting bound for the connected high-overlap part.

**Corollary (connected cluster moment bound).** Fix `t>=1`, and let
`X=|Fib_U^cap(a)|` for `mu` independent random rows. The contribution to
`E X^t` from ordered `t`-tuples `(S_1,...,S_t)` whose high-overlap graph `G_k`
is connected is at most

```text
sum_{d=0}^{n-a}
  binom(n,a+d) binom(a+d,a)^t q^{-mu(a-k+d)}.
```

Equivalently, relative to the diagonal first-moment scale
`binom(n,a)q^{-mu(a-k)}`, the union-excess `d` part is bounded by

```text
  [ binom(n,a+d) / binom(n,a) ] binom(a+d,a)^t q^{-mu d}.
```

*Proof.* If a connected ordered tuple has union size `a+d`, first choose its
union `V`, in at most `binom(n,a+d)` ways. Each support `S_i` is then an
`a`-subset of `V`, giving at most `binom(a+d,a)^t` ordered tuples. The
union-excess corollary gives the probability bound
`q^{-mu(a-k+d)}` for each such tuple. Summing over `d` gives the first display;
dividing by the diagonal first-moment scale gives the second.

This does not prove the worst-case regular-core theorem, because V0 is a
uniform received-word statement, not an average-random statement. It does give a
concrete proof route: connected high-overlap clusters either remain diagonal,
or their union excess pays a field-entropy factor `q^{-mu d}` against only the
combinatorial cost of choosing a small enlarged union.

In a fixed moment, this entropy payment clears the positive-excess layers under
a simple polynomial lower bound on `q^mu`.

**Corollary (finite-moment connected-cluster clearance).** Fix `t>=1` and
assume `a>=rho_0 n`. If

```text
q^mu >= 2 rho_0^{-1} n^t,
```

then in the random model the total connected high-overlap contribution to
`E X^t` from union excess `d>=1` is at most the diagonal first-moment scale

```text
binom(n,a) q^{-mu(a-k)}.
```

Thus, under this sufficient condition, positive-excess connected clusters add
at most one more diagonal-scale contribution to the fixed `t`-th moment.

*Proof.* From the preceding corollary, the `d`-th positive-excess layer divided
by the diagonal scale is at most

```text
[ binom(n,a+d) / binom(n,a) ] binom(a+d,a)^t q^{-mu d}.
```

Since `a>=rho_0 n`,

```text
binom(n,a+d) / binom(n,a)
 = prod_{j=1}^d (n-a-j+1)/(a+j)
 <= rho_0^{-d}.
```

Also `binom(a+d,a)<=n^d`. Hence the relative `d`-layer is at most
`(rho_0^{-1} n^t/q^mu)^d <= 2^{-d}`. Summing over `d>=1` gives the claim.

**Lemma (all-remainder quotient packets have exact support and exact count).**
Fix one scale `M | n` with `M>sigma`, write `a=M ell+u` with
`0<=u<M`, and fix an omitted `M`-coset `C_0`. For row `i`, choose
`T_i subset C_0` of size `u` and put

```text
Y_i(X)=X^{M ell} L_{T_i}(X).
```

For an `ell`-subset `A_i` of the remaining quotient cosets, define

```text
S_i = T_i union U_{A_i},
P_i(X)=L_{T_i}(X)(X^{M ell}-L_{A_i}(X)).
```

Then `deg P_i<k` and the full agreement support of `P_i` against `Y_i` on
`H` is exactly `S_i`. If

```text
tau = |T_1 cap ... cap T_mu|,
```

then the number of ordered quotient choices `(A_1,...,A_mu)` whose interleaved
common agreement support has size at least `a` is exactly

```text
L_{M,mu}(a,tau)
  = sum_{c=h_M(a,tau)}^ell
      binom(Q,c) E_empty(Q-c,ell-c,mu).
```

*Proof.* The degree bound is the cancellation already used above:
`deg(X^{M ell}-L_{A_i}) <= M(ell-1)`, so
`deg P_i <= u+M(ell-1)=a-M<k`. Also

```text
Y_i(X)-P_i(X)=L_{T_i}(X)L_{A_i}(X).
```

The roots of the right-hand side inside `H` are exactly `T_i` together with the
full `M`-cosets selected by `A_i`; hence the full agreement support is exactly
`S_i`, with no hidden over-agreement.

The common interleaved support has size

```text
tau + M |A_1 cap ... cap A_mu|.
```

Thus it is listed exactly when
`|A_1 cap ... cap A_mu| >= h_M(a,tau)`. If the common quotient intersection
has exact size `c`, choose it in `binom(Q,c)` ways. After removing these `c`
common cosets, the residual `ell-c` choices in each row must have empty common
intersection; by inclusion-exclusion this number is
`E_empty(Q-c,ell-c,mu)`. Summing over all `c>=h_M(a,tau)` gives the formula.

## 3. Conjecture L2-Sharp, Version 0

Fix a compact rate window `rho in [rho_0,rho_1] subset (0,1)`, fixed arity
`mu`, and reserve constants `epsilon,Cq,C0`. There exist constants `B` and `N0`
such that for every `n>=N0`, every cyclic generated-field domain
`H <= F_q^*` of order `n`, and every `k,a,q` satisfying the setup and reserve
above,

```text
Lst_mu(H,k,a;q)
 <= binom(n,a) q^(-mu(a-k))
    + Quot_rem_mu(n,k,a)
    + n^B.
```

Equivalently, after paying the explicit aligned quotient budget, the remaining
common-support codegree contribution is polynomial in `n` and does not contain
the Cartesian factor `binom(n,a)^(mu-1)`.

The conjecture deliberately allows local over-agreement blocks. It does not say
that every interleaved list is bounded by one row list, nor that local Cartesian
subgraphs cannot occur. It says that all such over-agreement/codegree effects
are absorbed by the polynomial error once the random simultaneous-support term
and aligned quotient packets are accounted for.

## 4. Codegree form of the error term

For `mu=2`, the polynomial error can be made into a concrete punctured-list
object. Given rows `U_1,U_2`, and a row-1 codeword `c_1` with
`|A_{U_1}(c_1)| >= a`, define

```text
Gamma_A(U_2,a)
  = |{ c_2 in C : |A cap A_{U_2}(c_2)| >= a }|,
        A = A_{U_1}(c_1).
```

Equivalently, `Gamma_A(U_2,a)` is the Reed-Solomon list size of `U_2`
restricted to the punctured domain `A`, at agreement threshold `a`:

```text
Gamma_A(U_2,a)
 = |Lambda(RS[F_q,A,k], 1-a/|A|, U_2|_A)|.
```

Then the support formula gives the exact decomposition

```text
|Lambda_2((U_1,U_2),a)|
 =
 sum_{c_1 : |A_{U_1}(c_1)| >= a}
      Gamma_{A_{U_1}(c_1)}(U_2,a).
```

For higher fixed `mu`, the same identity recurses: after anchoring one row
support `A`, the remaining factor is a `(mu-1)`-row interleaved list on the
punctured domain `A`.

Thus the proof obligation behind `n^B` is not vague. After quotient packets are
removed or budgeted, one needs a uniform polynomial bound for these punctured
RS list/codegree completions and then a summation over the L1-controlled
first-row support family. In the unique-decoding range

```text
2a > |A| + k - 1,
```

the punctured term is `<=1`; outside that range, the following elementary
Johnson-style bound applies.

**Proposition (punctured RS codegree bound).** Let `A subset H` have size
`s >= a`, and let

```text
L_A(V,a) = |Lambda(RS[F_q,A,k], 1-a/s, V|_A)|.
```

Then:

1. If `2a > s+k-1`, then `L_A(V,a) <= 1`.
2. If
   ```text
   a^2 > s(k-1),
   ```
   then
   ```text
   L_A(V,a) <= floor( s(s-k+1) / (a^2 - s(k-1)) ).
   ```

*Proof.* Let `c_1,...,c_L` be listed punctured codewords and let

```text
S_i = {x in A : c_i(x)=V(x)}.
```

Each `|S_i| >= a`. Two distinct degree-`<k` polynomials agree on at most `k-1`
points of `A`, so

```text
|S_i cap S_j| <= k-1        (i != j).
```

The first claim follows at once from
`|S_i cap S_j| >= |S_i|+|S_j|-s >= 2a-s`: if `2a-s > k-1`, two listed
codewords cannot be distinct.

For the second claim, write `m_x = |{i : x in S_i}|` and
`I = sum_x m_x`. Then `I >= La`, while

```text
sum_x binom(m_x,2) <= binom(L,2)(k-1).
```

By Cauchy,

```text
I^2 <= s sum_x m_x^2
    = s( I + 2 sum_x binom(m_x,2) )
    <= s( I + L(L-1)(k-1) ).
```

Using `I >= La` on the left and `I <= Ls` on the right gives

```text
L^2 a^2 <= s( Ls + L(L-1)(k-1) ).
```

After division by `L` and rearranging,

```text
L (a^2 - s(k-1)) <= s(s-k+1).
```

This gives the displayed bound when the denominator is positive.

The proposition also gives a precise location for the next obstruction.

**Lemma (large-anchor threshold).** Suppose `k>=2` and `a=k+sigma`. Let

```text
s_J = ceil(a^2/(k-1)).
```

Then every punctured anchor support size

```text
a <= s <= s_J-1
```

is controlled by the punctured Johnson bound above. If an anchor support is not
controlled by that bound, then

```text
s >= s_J = a + ceil(a(sigma+1)/(k-1)).
```

*Proof.* The Johnson denominator is positive exactly when

```text
s(k-1) < a^2,
```

or, equivalently for integral `s`, when `s <= ceil(a^2/(k-1))-1`. This proves
the first assertion. For the displayed excess, use

```text
ceil(a^2/(k-1)) - a
  = ceil(a^2/(k-1) - a)
  = ceil(a(a-k+1)/(k-1))
  = ceil(a(sigma+1)/(k-1)).
```

This gives a deterministic shell decomposition for the two-row L2 problem. For
a received word `V`, put

```text
N_V(s) = |{c in C : |A_V(c)| = s}|,
L_V(a) = sum_{s>=a} N_V(s).
```

Let

```text
J(s;k,a) =
  1,                                      if 2a > s+k-1,
  floor(s(s-k+1)/(a^2-s(k-1))),           if a^2 > s(k-1).
```

**Proposition (two-row shell bound).** For `mu=2`, `k>=2`, and
`s_J=ceil(a^2/(k-1))`, every pair of rows `U_1,U_2` satisfies

```text
|Lambda_2((U_1,U_2),a)|
 <= sum_{s=a}^{min(n,s_J-1)} N_{U_1}(s) J(s;k,a)
    + L_{U_2}(a) sum_{s=s_J}^n N_{U_1}(s).
```

The same inequality holds with the two rows interchanged.

Moreover, if

```text
E_V^{(a)}
  = |{S subset H : |S|=a and V|_S extends to a degree-<k polynomial}|,
```

then for every `s_0>=a`,

```text
sum_{s>=s_0} N_V(s) <= E_V^{(a)} / binom(s_0,a).
```

*Proof.* Start from the exact codegree decomposition. For an anchor
`c_1` with `|A_{U_1}(c_1)|=s<s_J`, the punctured Johnson proposition bounds
the inner completion number by `J(s;k,a)`. For anchors with `s>=s_J`, use the
trivial bound

```text
Gamma_{A_{U_1}(c_1)}(U_2,a) <= L_{U_2}(a).
```

Summing over row-1 support-size shells gives the displayed inequality. The
final estimate is a double count: each row codeword with full support size `s`
contains exactly `binom(s,a)` subsets `S` of size `a`, and each such `S`
determines at most one degree-`<k` polynomial because `a>=k`.

The shell reduction also gives a direct bridge from one-row L1 bounds to the
two-row L2 codegree term. Define the controlled Johnson shell weight

```text
W_J(n,k,a) = sum_{s=a}^{min(n,s_J-1)} J(s;k,a).
```

For rows `U_1,U_2`, put

```text
P_1 = max_{a <= t <= min(n,s_J-1)} L_{U_1}(t),
T_1 = L_{U_1}(s_J),
L_2 = L_{U_2}(a),
```

with `P_1=0` if there is no controlled shell.

**Corollary (L1 shell control implies L2 codegree control).** For `mu=2` and
`k>=2`,

```text
|Lambda_2((U_1,U_2),a)| <= P_1 W_J(n,k,a) + T_1 L_2.
```

Moreover,

```text
W_J(n,k,a) <= n^2(2+log n)
```

for `n>=2`, with any fixed logarithm base changing only the absolute constant.
The same estimate holds with the two rows interchanged.

*Proof.* In the two-row shell bound, each exact shell count satisfies

```text
N_{U_1}(s) <= L_{U_1}(s) <= P_1
```

for `a<=s<=min(n,s_J-1)`, while the tail count is `L_{U_1}(s_J)=T_1`. This
gives the first displayed inequality. For the weight estimate, write

```text
D_s = a^2 - s(k-1).
```

On the controlled shells, `D_s>=1`, and `J(s;k,a) <= n^2/D_s`. As `s` ranges
over the controlled shells, the positive integers `D_s` form an arithmetic
progression with common difference `k-1` when read in increasing order. Hence

```text
sum_s 1/D_s <= 1 + sum_{j=1}^{n} 1/(j(k-1)) <= 2+log n,
```

which proves the claim.

The cumulative one-row list size is monotone in the threshold:

```text
t >= a  =>  L_V(t) <= L_V(a).
```

Consequently, if a repaired one-row L1 local theorem gives a uniform polynomial
bound at the original threshold

```text
L_V(a) <= n^{B_L},
```

for every received word `V`, then the non-quotient two-row codegree
contribution is bounded by

```text
n^{B_L+2}(2+log n) + n^{2B_L}.
```

This is the precise sense in which the remaining L2 over-agreement problem is
an L1 shell problem, not a new Cartesian-product exponent.

The same argument gives a fixed-arity version. For `r>=1`, set

```text
W_J^{[r]}(n,k,a) = sum_{s=a}^{min(n,s_J-1)} J(s;k,a)^r.
```

**Corollary (fixed-arity shell reduction).** For fixed `mu>=2`, rows
`U_1,...,U_mu`, and

```text
P_1 = max_{a <= t <= min(n,s_J-1)} L_{U_1}(t),
T_1 = L_{U_1}(s_J),
L_i = L_{U_i}(a)        (2 <= i <= mu),
```

one has

```text
|Lambda_mu(U,a)|
 <= P_1 W_J^{[mu-1]}(n,k,a) + T_1 product_{i=2}^mu L_i.
```

Furthermore,

```text
W_J^{[r]}(n,k,a) <= n^{2r}(2+log n)
```

for every fixed `r>=1` and `n>=2`.

*Proof.* Anchor the first row and use the recursive codegree identity. If the
anchor support has size `s<s_J`, then each remaining row has at most `J(s;k,a)`
punctured completions on that anchor, by the punctured Johnson proposition.
Forgetting the common-intersection condition among the remaining rows gives the
product upper bound `J(s;k,a)^(mu-1)`. If `s>=s_J`, use the trivial product
bound `product_{i=2}^mu L_i`. Summing over row-1 support shells gives the
first inequality.

The weight bound is the same denominator estimate as before: on controlled
shells, `J(s;k,a) <= n^2/D_s` with `D_s=a^2-s(k-1)>=1`, and
`D_s^{-r} <= D_s^{-1}`. Thus

```text
sum_s J(s;k,a)^r
 <= n^{2r} sum_s 1/D_s
 <= n^{2r}(2+log n).
```

Consequently, if repaired one-row L1 local bounds give

```text
L_V(a) <= n^{B_L}
```

for all received words, then the fixed-arity over-agreement contribution obeys

```text
|Lambda_mu(U,a)| <= n^{B_L+2(mu-1)}(2+log n) + n^{mu B_L}.
```

For every fixed protocol arity `mu`, this is polynomial in `n`.

The same shell reduction separates the genuinely sharp part of L2 from the
row-overagreement error. Call an interleaved tuple
`(c_1,...,c_mu) in Lambda_mu(U,a)` **regular** if every row has full agreement
support of size exactly `a`:

```text
|A_{U_i}(c_i)| = a        for every i.
```

Otherwise call it **row-irregular**. If a tuple is regular, then the common
intersection condition forces

```text
A_{U_1}(c_1) = ... = A_{U_mu}(c_mu) = S
```

for one `a`-subset `S subset H`; since `a>=k`, this support determines every
row codeword uniquely. Thus the regular core is exactly the diagonal
exact-support object on which the random term and the quotient packet budget
should act.

This exact core can be phrased without mentioning interleaved codeword tuples.
For a row `V`, let

```text
Fib_V(a) = {S subset H : |S|=a and V|_S extends to a degree-<k polynomial}.
```

For `U=(U_1,...,U_mu)`, put

```text
Fib_U^cap(a) = Fib_{U_1}(a) cap ... cap Fib_{U_mu}(a).
```

Since `a>=k`, each `S in Fib_U^cap(a)` determines a unique tuple of row
codewords `(c_{1,S},...,c_{mu,S})`. Let

```text
A_i(S) = A_{U_i}(c_{i,S}).
```

Then the map

```text
S |-> (c_{1,S},...,c_{mu,S})
```

surjects from `Fib_U^cap(a)` onto `Lambda_mu(U,a)`: the preimage of a listed
tuple is exactly the set of `a`-subsets of its common agreement support.
Moreover,

```text
Reg_mu(U,a)
 = |{S in Fib_U^cap(a) : A_1(S)=...=A_mu(S)=S}|.
```

Thus the regular exact-row problem is a simultaneous locator-fiber problem with
the row-irregular fibers removed. The random term is precisely the expectation
of `|Fib_U^cap(a)|` for independent random rows, namely
`binom(n,a) q^{-mu(a-k)}`.

There is an explicit syndrome form of this fiber. For an `a`-set `S`, let

```text
L_S(X) = product_{s in S} (X-s)
```

and for a row `V` define the unique degree-`<a` interpolant on `S` by

```text
I_{V,S}(X)
 = sum_{s in S} V(s) L_S(X) / ((X-s)L_S'(s)).
```

Write `sigma=a-k` and define the top-coefficient syndrome

```text
Syn_V(S)
 = ([X^k]I_{V,S}, [X^{k+1}]I_{V,S}, ..., [X^{a-1}]I_{V,S})
   in F_q^sigma.
```

Then

```text
S in Fib_V(a)    iff    Syn_V(S)=0.
```

Indeed, `I_{V,S}` is the only degree-`<a` polynomial agreeing with `V` on `S`,
and `a>=k`; it extends to a degree-`<k` codeword exactly when its coefficients
in degrees `k,...,a-1` vanish. Therefore

```text
Fib_U^cap(a)
 = {S subset H : |S|=a and Syn_{U_i}(S)=0 for every i}.
```

This is the concrete L1-style object left in the regular core: a support
locator `L_S` must satisfy `mu sigma` top-coefficient conditions. The exact
regular part further imposes the inequalities

```text
I_{U_i,S}(x) != U_i(x)       for every x in H \ S and every i,
```

while dropping these inequalities gives the simultaneous-fiber upper bound.

The same equations can be written in residue-moment form. Write

```text
L_S(X) = sum_{r=0}^a lambda_r X^r,        lambda_a=1,
```

and define

```text
R_j(V,S) = sum_{s in S} V(s) s^j / L_S'(s),        0 <= j < sigma.
```

Since

```text
[X^d] L_S(X)/(X-s)
 = sum_{r=d+1}^a lambda_r s^{r-d-1},
```

one has, for `k<=d<a`,

```text
[X^d] I_{V,S}
 = sum_{r=d+1}^a lambda_r R_{r-d-1}(V,S).
```

Equivalently, for `0<=t<sigma`,

```text
[X^{a-1-t}] I_{V,S}
 = R_t(V,S) + lambda_{a-1} R_{t-1}(V,S)
   + ... + lambda_{a-t} R_0(V,S).
```

This is a unit-triangular change of coordinates from the moment vector
`(R_0,...,R_{sigma-1})` to `Syn_V(S)`. Hence

```text
Syn_V(S)=0    iff    R_j(V,S)=0 for every 0<=j<sigma.
```

Thus the regular-core upper-bound problem can be attacked as a simultaneous
weighted residue-moment problem:

```text
R_j(U_i,S)=0        for every i=1,...,mu and j=0,...,sigma-1.
```

For row-irregular tuples, at least one row has support size `>=a+1`. Anchoring
such a row and using the fixed-arity shell reduction gives the union bound

```text
Irr_mu(U,a)
 <= sum_{j=1}^mu
      ( P_j^+ W_J^{[mu-1]}(n,k,a)
        + T_j product_{i != j} L_{U_i}(a) ),
```

where

```text
P_j^+ = max_{a+1 <= t <= min(n,s_J-1)} L_{U_j}(t),
T_j   = L_{U_j}(s_J),
```

with `P_j^+=0` if the displayed range is empty. Consequently, the repaired
one-row L1 bound `L_V(a)<=n^{B_L}` implies

```text
Irr_mu(U,a)
 <= mu ( n^{B_L+2(mu-1)}(2+log n) + n^{mu B_L} ).
```

Therefore L2-Sharp V0 is reduced to the following sharper exact-core local
limit, plus the repaired one-row L1 theorem:

```text
Reg_mu(U,a)
 <= binom(n,a) q^(-mu(a-k))
    + Quot_rem_mu(n,k,a)
    + n^{B_reg}.
```

This is a narrower target than bounding all interleaved lists directly. Local
Cartesian blocks with row over-agreement, such as the `K_{2,2}` witness below,
belong to `Irr_mu` and are already charged to the polynomial codegree term.
The remaining sharp question is whether exact-row diagonal supports have only
the random simultaneous-support mass, the explicit all-remainder quotient
packets, and a polynomial residual.

This packages the reduction to L1 as a conditional theorem.

**Conditional theorem (L1 shell local limit gives the L2 codegree term).**
Fix `mu>=2`. Suppose that, in the quotient-free or quotient-budgeted residual
problem, there is a constant `B_L` such that every row word `V` satisfies the
repaired one-row L1 bound at the original L2 agreement threshold

```text
L_V(a) <= n^{B_L}.
```

Then every fixed-arity interleaved received word `U=(U_1,...,U_mu)` has
over-agreement/codegree contribution bounded by

```text
n^{B_L+2(mu-1)}(2+log n) + n^{mu B_L}.
```

Thus, after the aligned quotient packets are removed or charged to
`Quot_rem_mu(n,k,a)`, this L1 shell hypothesis supplies the polynomial
`n^B` error term required by L2-Sharp, for example with any

```text
B > max(B_L+2(mu-1), mu B_L).
```

This conditional theorem does not prove the sharp regular-core local limit.
Its content is narrower: no additional Cartesian-product obstruction remains in
the fixed-arity row-irregular/codegree term once the repaired L1 shell local
limit is available. By monotonicity, the single threshold `a` controls every
shell threshold `t>=a` used in the reduction.

Thus a proof of L2-Sharp splits into two concrete obligations. First prove the
regular exact-row local limit: exact common supports contribute only the random
simultaneous-support term, the explicit `Quot_rem_mu` packets, and a polynomial
residual. Second prove/import the repaired one-row L1 theorem, which controls
row-irregular tuples by anchor support size `s`: small over-agreement anchors
fall into unique decoding, intermediate anchors are Johnson-controlled, and any
remaining large anchors already have at least
`ceil(a(sigma+1)/(k-1))` extra agreements above the list threshold.

This split is an actual implication, not just a heuristic decomposition.

**Conditional theorem (regular core plus L1 shells imply L2-Sharp V0).** Fix
`mu>=2` and the compact parameter window in V0. Assume the following two
uniform inputs hold after quotient packets have been removed or charged to
`Quot_rem_mu(n,k,a)`.

1. There are constants `B_reg,N_reg` such that every received word
   `U=(U_1,...,U_mu)` satisfies the regular exact-core estimate
   ```text
   Reg_mu(U,a)
    <= binom(n,a) q^(-mu(a-k))
       + Quot_rem_mu(n,k,a)
       + n^B_reg.
   ```
2. There are constants `B_L,N_L` such that every one-row received word `V`
   satisfies the repaired L1 shell bound
   ```text
   L_V(a) <= n^B_L.
   ```

Then L2-Sharp V0 holds. For example, for all sufficiently large `n`, one may
take any exponent

```text
B > max(B_reg, B_L+2(mu-1)+1, mu B_L).
```

*Proof.* Every listed interleaved tuple is either regular or row-irregular, so

```text
|Lambda_mu(U,a)| = Reg_mu(U,a) + Irr_mu(U,a).
```

The fixed-arity shell reduction above gives

```text
Irr_mu(U,a)
 <= mu ( n^{B_L+2(mu-1)}(2+log n) + n^{mu B_L} ).
```

For fixed `mu`, the prefactor `mu` is constant, and for all sufficiently large
`n` the factor `2+log n` is bounded by `n`. Hence the row-irregular term is
`O(n^B)` for any `B` satisfying the displayed strict inequalities. Adding the
regular exact-core estimate gives precisely the V0 bound.

Thus the remaining proof search can focus on the two named inputs. The L1
shell input is an imported one-row theorem. The genuinely L2-specific input is
the regular exact-core local limit, equivalently the quotient-budgeted
simultaneous residue-moment problem.

The regular input can be relaxed once more. Define the relaxed simultaneous
fiber count

```text
Fib_mu(U,a)=|Fib_U^cap(a)|.
```

Equivalently, by the residue-moment form above, `Fib_mu(U,a)` is the number of
`a`-sets `S subset H` satisfying

```text
R_j(U_i,S)=0        for every i=1,...,mu and 0<=j<sigma.
```

**Corollary (relaxed simultaneous-fiber target suffices).** Fix `mu>=2` and
the compact parameter window in V0. Suppose that, after quotient packets have
been removed or charged to `Quot_rem_mu(n,k,a)`, there are constants
`B_fib,N_fib` such that every received word `U` satisfies

```text
Fib_mu(U,a)
 <= binom(n,a) q^(-mu(a-k))
    + Quot_rem_mu(n,k,a)
    + n^B_fib.
```

Suppose also that the repaired one-row L1 shell bound holds with exponent
`B_L`. Then L2-Sharp V0 holds, for example with any

```text
B > max(B_fib, B_L+2(mu-1)+1, mu B_L).
```

*Proof.* The exact regular core is a subset of the relaxed simultaneous fiber:

```text
Reg_mu(U,a) <= Fib_mu(U,a).
```

Indeed, every regular exact-row tuple has a common support `S` of size `a`,
and this `S` lies in every row fiber. Thus the relaxed-fiber hypothesis implies
the regular exact-core hypothesis in the preceding conditional theorem with
`B_reg=B_fib`; applying that theorem gives V0 with the displayed exponent.

This is the cleanest current L2-specific proof target. It removes the
outside-avoidance inequalities from the regular core and asks only for a
quotient-budgeted bound on the simultaneous residue-moment zero locus.

The relaxed target lives naturally on row classes modulo the Reed-Solomon code.

**Lemma (row-affine quotient invariance).** Let `Q_i in C` and
`alpha_i in F_q^*` for `1<=i<=mu`, and define

```text
U_i' = alpha_i U_i + Q_i.
```

Then the row-wise map

```text
c_i |-> alpha_i c_i + Q_i
```

is a bijection from `C` to `C` and preserves full agreement supports:

```text
A_{U_i'}(alpha_i c_i+Q_i)=A_{U_i}(c_i).
```

Consequently,

```text
|Lambda_mu(U',a)|=|Lambda_mu(U,a)|,
Reg_mu(U',a)=Reg_mu(U,a),
Fib_mu(U',a)=Fib_mu(U,a).
```

In residue-moment coordinates,

```text
R_j(U_i',S)=alpha_i R_j(U_i,S)
```

for every `a`-set `S` and every `0<=j<sigma`. Thus the simultaneous
zero-moment locus depends only on the row classes in `F_q^H/C`, with each
nonzero class understood projectively.

*Proof.* Since `C` is a linear code, `c_i |-> alpha_i c_i+Q_i` is a bijection
of `C`. At a point `x in H`,

```text
alpha_i c_i(x)+Q_i(x)=alpha_i U_i(x)+Q_i(x)
```

is equivalent to `c_i(x)=U_i(x)`, because `alpha_i` is nonzero. This proves
the agreement-support identity and hence preserves the support-intersection
formula, the exact-row regular subcount, and the relaxed simultaneous fiber.

For the residue form, `R_j` is linear in the row word. If `Q_i` has degree
`<k`, then the degree-`<a` interpolant of `Q_i` on any `S` is just `Q_i`, so
its top syndrome and therefore all residue moments vanish. Hence
`R_j(U_i',S)=alpha_i R_j(U_i,S)`, preserving the common zero locus.

For the relaxed target, the whole ordered row basis can be changed.

**Lemma (row-span invariance of the relaxed fiber).** Let
`A in GL_mu(F_q)`, let `Q=(Q_1,...,Q_mu) in C^mu`, and define

```text
U' = A U + Q,
```

where rows are viewed as column vectors under the matrix `A`. Then

```text
|Lambda_mu(U',a)|=|Lambda_mu(U,a)|,
Fib_mu(U',a)=Fib_mu(U,a).
```

In residue-moment coordinates, for each `a`-set `S` and each
`0<=j<sigma`, the row vector of moments transforms as

```text
( R_j(U_1',S), ..., R_j(U_mu',S) )^T
 =
A ( R_j(U_1,S), ..., R_j(U_mu,S) )^T.
```

Thus the simultaneous zero-moment locus depends only on the row span in the
quotient space `F_q^H/C`, not on a chosen ordered basis for that span.

*Proof.* The map `c |-> A c+Q` is a bijection of `C^mu`, since `A` is
invertible and `C` is linear. At a point `x`, the vector equality

```text
A c(x)+Q(x)=A U(x)+Q(x)
```

is equivalent to `c(x)=U(x)`. Hence the common agreement support of each tuple
is preserved, proving the equality of interleaved list sizes.

For a fixed `S`, the condition `S in Fib_mu(U,a)` says that each row
restriction `U_i|_S` is the restriction of some degree-`<k` polynomial. This
condition is invariant under invertible row combinations and under adding rows
from `C`, proving `Fib_mu(U',a)=Fib_mu(U,a)`. The displayed moment
transformation follows from row-linearity of `R_j` and the fact that all
moments of rows in `C` vanish for `j<sigma`.

Unlike the relaxed fiber, the row-by-row exact-regular condition is not the
natural invariant under arbitrary row mixing. This is another reason the
quotient-budgeted relaxed residue fiber is the cleaner L2-specific target.

This immediately separates lower-rank row tuples from the genuinely `mu`-row
case.

**Corollary (quotient-rank reduction).** Let `r` be the dimension of the row
span of `U` in the quotient space `F_q^H/C`. Choose quotient-basis
representatives `V=(V_1,...,V_r)`. Then

```text
|Lambda_mu(U,a)|=|Lambda_r(V,a)|,
Fib_mu(U,a)=Fib_r(V,a).
```

In particular, the sharp `mu`-row relaxed-fiber problem only needs to be
proved for full quotient row rank, provided the lower-arity cases are already
available.

*Proof.* By row-span invariance, apply an invertible row operation and subtract
code rows to put `U` in the form

```text
(V_1,...,V_r,0,...,0)
```

in `F_q^H`. The relaxed fiber equality is then immediate: the zero rows impose
no residue-moment constraints, while the first `r` rows impose exactly the
fiber equations for `V`.

For the interleaved list, any listed tuple has a common agreement support of
size at least `a>=k`. On a zero received row, the corresponding degree-`<k`
codeword vanishes on this common support, and hence is the zero codeword.
Thus the zero quotient rows contribute no choices and no additional common
support constraints. The listed tuples are therefore exactly the listed
`r`-row tuples for `V`.

## 5. Already proved or checked

The existing L2 notes prove the following inputs.

- `l2_interleaved_support_bridge.md`: exact full-support intersection formula.
- `l2_exact_support_diagonalization.md`: exact-support equal-row lifts are
  diagonal and do not create a `mu`-fold quotient lower bound.
- `l2_interleaved_dilation_constants.md`: diagonal dilation symmetry and the
  exact formula for `L_{M,mu}(a,tau)`, checked against brute force by
  `verify_l2_quotient_core_count.py`.

The new falsification script

```bash
python3 experimental/scripts/verify_l2_sharp_target.py
```

checks the following stress points.

1. The explicit aligned quotient budget is computable. For example, at
   `(n,k,a,mu)=(64,16,18,2)` the old divisible-only budget and the
   all-remainder budget both have three active packet scales and total `1389`.
   But at the dithered dimension `(n,k,a,mu)=(64,15,17,2)`, the divisible-only
   budget is `0` while the all-remainder budget is still `1389`, coming from
   partial-coset packets. The active all-remainder scales in that dithered
   example are exactly `M in {4,8,16}`, matching the interval
   `a-k < M <= a`. A dyadic dither scan with `n=64`, `k_0=16`, `sigma=2`,
   and `k=k_0-r` first clears all all-remainder scales only at `r=15`, where
   `a=3` falls below the next dyadic divisor `4`. For `(k,a)=(16,18)`, the
   punctured Johnson step controls anchor supports through `s=21`; the
   remaining large-anchor tail starts only at `s=22`, i.e. four extra
   agreements above the list threshold. The exact controlled Johnson shell
   weight in this example is `17`; the powered shell weight for the fixed-arity
   `mu=3` reduction is `199`.
2. The all-remainder quotient construction is realized explicitly over
   `F_17`, `n=16`, `k=7`, `a=9`, `M=4`. Here `M` does not divide `k`,
   `ell=floor(a/M)=2`, and the partial omitted coset has size `1`. The verifier
   constructs the three expected codewords, checks that their maximum degree is
   `5<k`, and verifies agreement on at least `9` points. It also checks that
   the degree-`<a` interpolant on each advertised support is the constructed
   degree-`<k` codeword, so the advertised support has zero top syndrome and
   zero residue moments. Exhausting all `binom(16,9)=11440` size-`9` supports
   for this same word gives `42` exact zero-moment supports, and these give
   `42` distinct degree-`<k` codewords all agreeing on exactly `9` points. The
   `3` advertised quotient supports/codewords are disjoint from the `39`
   residual supports/codewords. The residual quotient-coset occupancy profiles
   are
   ```text
   (4,2,2,1): 7,  (3,3,3,0): 1,
   (3,3,2,1): 14, (3,2,2,2): 17.
   ```
   The only active quotient scales are `M=4` and `M=8`; their quotient shapes
   occur among the zero-moment supports `3` and `1` times respectively, and
   their union is still the same `3` advertised quotient supports. Thus the
   `39` residual codewords fail the active quotient-shape test at every active
   scale.
   Equal-row interleaving of this exact-support family is diagonal: the `42`
   one-row supports give `42` listed pairs, not `42^2`; the quotient part gives
   `3`, the residual part gives `39`, and there are no mixed quotient/residual
   listed pairs.
   The same finite family has no nontrivial dilation self-correlation: among
   the `16` domain rotations, only the identity maps any zero-moment support
   back into the zero-moment family. In particular the maximum non-identity
   overlap for the residual subfamily is `0`.
   Thus `Quot_rem_mu` is a structured subfamily of the zero-moment locus, not
   an exhaustive description of that locus in small finite examples; the
   remaining aperiodic zero-moment supports are exactly what the polynomial
   residual must control.
3. The support-pair rank law is brute-checked over `F_7`, `n=6`, `k=2`,
   `a=3`. For intersection sizes `r=0,1,2,3`, the verifier counts the actual
   assignments on `S union T` for which both `S` and `T` are feasible. The
   dimensions are `4,3,2,2`, giving counts `7^4,7^3,7^2,7^2` and probability
   exponents `2,2,2,1`. Thus the independence threshold at `r<k` and the
   high-overlap surplus at `r>=k` are checked directly in a finite RS model.
   This is random-model evidence for the regular-core local-limit target, not
   a worst-case proof.
4. The multi-support high-overlap cluster bound is brute-checked on six
   `F_7`, `n=6`, `k=2`, `a=3` configurations. A connected high-overlap triple
   with all supports equal has one component, union size `3`, exponent `1`,
   and exactly `7^2` feasible assignments: this is the diagonal zero-loss
   case. A non-diagonal connected high-overlap triple has one component, union
   size `4`, exponent `2`, and exactly `7^2` feasible assignments, showing the
   extra `q^{-1}` loss predicted by the corollary. A mixed high/low path has
   two components, union size `6`, and count below the `7^4` bound. An
   aggregate-overlap example has two raw high-overlap components but one
   `k`-closed component, sharpening the exponent from `1` to `3`. A connected
   four-support chain has union excess `3` and exponent `4=a-k+3`, matching the
   union-excess tradeoff. A low-overlap cycle has three components, union size
   `6`, but only `7^3` feasible assignments below the loose `7^6` cluster
   bound, showing that low-overlap consistency can only reduce the feasible
   space further. In every row the number of distinct supports is also below
   `binom(a+d,a)`. This identifies high-overlap clustering as the only source
   of positive rank surplus left by the random model, with diagonal clusters as
   the only zero-loss connected case.
   The verifier also counts all ordered connected high-overlap triples of
   `3`-sets in `[6]` by union excess `d` and checks the moment-counting bound
   `binom(n,a+d) binom(a+d,a)^3`: the diagonal `d=0` term is exact, and the
   positive-excess terms are present but bounded by the displayed union-count
   ledger. With `q=31` and `mu=2`, the exact positive-excess connected-triple
   contribution is below the diagonal scale, and the union-count upper bound is
   below the diagonal scale as well.
   Finally, the verifier enumerates all ordered triples by `k`-closure
   signature `(closed components, total union size, global excess D)`. The
   finite table contains negative, zero, and positive `D`, confirming that
   low-overlap cross-component intersections are a real correction term rather
   than an artifact of the proof. The same table now computes the rank of the
   cross-component equality constraints. In the forest rows, including all
   two-component rows, this rank exactly cancels the low-overlap defect:
   `D+r_cross` equals the sum of the internal closed-part union excesses. The
   only non-forest row in the toy table is the three-component low-overlap
   cycle, isolating cycles of closed parts as the first place where an
   additional low-overlap rank analysis is needed. The verifier then tests an
   explicit cyclic rank-deficit family over `F_17`: for `k=3,4,5,6`, three
   supports of the form `A union B`, `A union C`, `B union C` have
   cross-rank `2k`, rank-corrected excess `3-k`, and surplus
   `k-3` over product-diagonal factorization. Thus the forest theorem is
   sharp as a structural statement; cyclic low-overlap diagrams require their
   own count or rank argument. The same sweep counts the full generic triangle
   family and compares its third-moment contribution to the diagonal scale;
   over `F_17` with `mu=2`, all tested rows are already below diagonal,
   matching the general bound `(27 rho_0^{-1} q^{-mu})^{k-1}`.
   Finally, the constant locator-ratio exceptional subfamily is counted
   separately. The verifier enumerates it over the same `F_17` domain for
   `r=2,3,4,5`, checks the degree-forced count bound
   `(q-2) binom(n,r) binom(n-r,r)`, and verifies that even this lower-rank
   subfamily is below the diagonal scale at `mu=2`. Combining the generic and
   constant-ratio pieces gives a complete clearance bound for the full
   symmetric three-block cyclic triangle family; the verifier checks both the
   exact combined ratios and the displayed combined upper bounds.
5. The natural `K_{m,m}` grid over-agreement family has
   ```text
   n_min = (k-1) + m^2(a-k+1),
   ```
   so this attack realizes local Cartesian blocks but only with polynomial
   growth in the tested grid model.
6. An exact Reed-Solomon enumeration over `F_29`, `n=14`, `k=3`, `a=5`
   realizes a genuine `K_{2,2}` over-agreement witness:
   ```text
   base row lists = [2,2],
   interleaved list = 4,
   product bound = 4.
   ```
   The same run reports punctured codegrees `[2,2]`, with codegree sum `4`.
   Its regular/irregular split is also decisive: the regular exact-row count is
   `0`, the row-irregular count is `4`, and the common-intersection profile is
   `{5:4}`. Thus the witness has exact common intersection size `a`, but every
   listed tuple is charged to row over-agreement rather than to the regular
   exact-row core. The simultaneous feasible-support fiber has `4` feasible
   `a`-sets, with `0` regular exact sets, `4` row-irregular sets, and a unique
   row codeword choice for each row and each feasible `a`-set. The
   locator-syndrome test gives the same `4` simultaneous zero-syndrome
   `a`-sets, with no mismatch against the enumerated support families. The
   verifier also checks that the weighted residue moments are a unit-triangular
   transform of the top-coefficient syndromes, with zero formula mismatches and
   zero zero-locus mismatches.
   The two row-1 anchor supports have size `8`; the punctured Johnson bound is
   `floor(8(8-3+1)/(5^2-8(3-1))) = 5`, so the observed codegrees `2,2`
   satisfy the proposition.
7. The same witness satisfies the deterministic shell bound: the row-1 shell
   histogram is `{8:2}`, the controlled shell contribution is `2*5=10`, the
   large-anchor tail is empty, and the exact-`a` row-1 locator multiplicity is
   `2 binom(8,5)=112`. If one forgets the exact shell histogram and uses only
   the one-row cumulative L1 shell maximum, the controlled Johnson weight is
   `186` and the resulting L1-shell reduction bound is `2*186=372`, still
   safely above the observed interleaved count `4`.
   Thus the target cannot forbid local Cartesian blocks. The correct target is
   the global sharp bound above, with these blocks charged to the polynomial
   punctured-list/codegree error.

## 6. Falsification boundary

The conjecture would fail, or need refinement, if one finds any of the
following above the reserve.

- A non-aligned quotient family whose interleaved contribution is not covered
  by `Quot_rem_mu(n,k,a)` and is larger than `n^B`.
- A relaxed simultaneous residue-fiber family whose count exceeds the random
  term plus `Quot_rem_mu(n,k,a)` by more than a polynomial factor. This would
  also threaten the regular exact-row input unless the excess is entirely
  removed by outside-avoidance inequalities.
- A row-irregular over-agreement/codegree construction whose anchored shell
  count is super-polynomial despite the repaired one-row L1 bound.
- A family of punctured domains `A=A_{U_1}(c_1)` for which the punctured-list
  term `Gamma_A(U_2,a)` is super-polynomial after quotient packets are removed.
- A quotient packet not covered by the all-remainder budget above that changes
  the diagonal packet count by more than a polynomial factor.
- A protocol-relevant growing-`mu` regime. This version treats `mu` as fixed.

The next useful proof target is therefore a codegree theorem: after quotient
packets are budgeted, the full-support families arising from Reed-Solomon words
should have bounded `>=a` common-intersection completion number. Proving that
would turn this L2 target into a direct protocol ledger bound.
