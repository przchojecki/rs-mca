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
4. The multi-support high-overlap cluster bound is brute-checked on three
   `F_7`, `n=6`, `k=2`, `a=3` configurations. A connected high-overlap triple
   has one component, union size `4`, dimension bound `2`, and exactly `7^2`
   feasible assignments. A mixed high/low path has two components, union size
   `6`, and count below the `7^4` bound. A low-overlap cycle has three
   components, union size `6`, but only `7^3` feasible assignments below the
   loose `7^6` cluster bound, showing that low-overlap consistency can only
   reduce the feasible space further. This identifies high-overlap clustering
   as the only source of positive rank surplus left by the random model.
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
