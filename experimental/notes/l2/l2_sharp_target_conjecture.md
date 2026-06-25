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
- A regular exact-row support family whose count exceeds the random term plus
  `Quot_rem_mu(n,k,a)` by more than a polynomial factor.
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
