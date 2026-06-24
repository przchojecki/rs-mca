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

## 2. Explicit aligned quotient budget

This version makes the quotient term concrete in the divisible quotient window.
For every subgroup fiber size

```text
M | n,        M | k,        M >= 2,
```

put

```text
N = n/M,        ell = k/M,        Q = N-1.
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
intersection. The aligned quotient-core packet at scale `M` is

```text
L_{M,mu}(a,tau)
  = sum_{c=h_M(a,tau)}^ell
      binom(Q,c) E_empty(Q-c,ell-c,mu),
```

with the value read as `0` if `h_M(a,tau)>ell`.

Define the conservative aligned quotient budget

```text
Quot_align_mu(n,k,a)
  = sum_{M | gcd(n,k), M>=2}
      max_{0 <= tau < M} L_{M,mu}(a,tau),
```

omitting terms with `ell=0` or `ell>Q`. This is a budget, not a disjointness
claim: it may overcount overlapping quotient packets. Its value is explicit and
finite. At the aligned threshold `a=k+sigma`, `tau=sigma<M`, the endpoint is
diagonal:

```text
L_{M,mu}(k+sigma,sigma) = binom(Q,ell),
```

not `binom(Q,ell)^mu`.

The non-divisible and dimension-dithered quotient cases are not included in
this version. They should either be reduced to this divisible window or added
as a separate exact budget.

## 3. Conjecture L2-Sharp, Version 0

Fix a compact rate window `rho in [rho_0,rho_1] subset (0,1)`, fixed arity
`mu`, and reserve constants `epsilon,Cq,C0`. There exist constants `B` and `N0`
such that for every `n>=N0`, every cyclic generated-field domain
`H <= F_q^*` of order `n`, and every `k,a,q` satisfying the setup and reserve
above,

```text
Lst_mu(H,k,a;q)
 <= binom(n,a) q^(-mu(a-k))
    + Quot_align_mu(n,k,a)
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

Thus a proof of L2-Sharp can be organized by anchor support size `s`: small
over-agreement anchors fall into unique decoding; intermediate anchors are
Johnson-controlled by the proposition; any remaining large anchors must already
have at least `ceil(a(sigma+1)/(k-1))` extra agreements above the list threshold
`a`, and their number is reducible to an exact-`a` one-row locator budget with
a `binom(s_J,a)` multiplicity saving. The remaining proof obligation is
therefore not arbitrary punctured list-decoding, but a high-overagreement tail
after quotient packets are removed or budgeted.

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

checks four stress points.

1. The explicit aligned quotient budget is computable. For example, at
   `(n,k,a,mu)=(64,16,18,2)` the conservative budget has three active packet
   scales and total `1389`. For the same `(k,a)=(16,18)`, the punctured
   Johnson step controls anchor supports through `s=21`; the remaining
   large-anchor tail starts only at `s=22`, i.e. four extra agreements above
   the list threshold.
2. The natural `K_{m,m}` grid over-agreement family has
   ```text
   n_min = (k-1) + m^2(a-k+1),
   ```
   so this attack realizes local Cartesian blocks but only with polynomial
   growth in the tested grid model.
3. An exact Reed-Solomon enumeration over `F_29`, `n=14`, `k=3`, `a=5`
   realizes a genuine `K_{2,2}` over-agreement witness:
   ```text
   base row lists = [2,2],
   interleaved list = 4,
   product bound = 4.
   ```
   The same run reports punctured codegrees `[2,2]`, with codegree sum `4`.
   The two row-1 anchor supports have size `8`; the punctured Johnson bound is
   `floor(8(8-3+1)/(5^2-8(3-1))) = 5`, so the observed codegrees `2,2`
   satisfy the proposition.
4. The same witness satisfies the deterministic shell bound: the row-1 shell
   histogram is `{8:2}`, the controlled shell contribution is `2*5=10`, the
   large-anchor tail is empty, and the exact-`a` row-1 locator multiplicity is
   `2 binom(8,5)=112`.
   Thus the target cannot forbid local Cartesian blocks. The correct target is
   the global sharp bound above, with these blocks charged to the polynomial
   punctured-list/codegree error.

## 6. Falsification boundary

The conjecture would fail, or need refinement, if one finds any of the
following above the reserve.

- A non-aligned quotient family whose interleaved contribution is not covered
  by `Quot_align_mu(n,k,a)` and is larger than `n^B`.
- A non-grid over-agreement/codegree construction whose common-intersection
  count grows like a Cartesian support product rather than a polynomial error.
- A family of punctured domains `A=A_{U_1}(c_1)` for which the punctured-list
  term `Gamma_A(U_2,a)` is super-polynomial after quotient packets are removed.
- A dithered-dimension quotient packet (`M` not dividing `k`) that changes the
  diagonal packet count by more than a polynomial factor.
- A protocol-relevant growing-`mu` regime. This version treats `mu` as fixed.

The next useful proof target is therefore a codegree theorem: after quotient
packets are budgeted, the full-support families arising from Reed-Solomon words
should have bounded `>=a` common-intersection completion number. Proving that
would turn this L2 target into a direct protocol ledger bound.
