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

## 4. Already proved or checked

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

checks three stress points.

1. The explicit aligned quotient budget is computable. For example, at
   `(n,k,a,mu)=(64,16,18,2)` the conservative budget has three active packet
   scales and total `1389`.
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
   Thus the target cannot forbid local Cartesian blocks. The correct target is
   the global sharp bound above, with these blocks charged to the polynomial
   over-agreement/codegree error.

## 5. Falsification boundary

The conjecture would fail, or need refinement, if one finds any of the
following above the reserve.

- A non-aligned quotient family whose interleaved contribution is not covered
  by `Quot_align_mu(n,k,a)` and is larger than `n^B`.
- A non-grid over-agreement/codegree construction whose common-intersection
  count grows like a Cartesian support product rather than a polynomial error.
- A dithered-dimension quotient packet (`M` not dividing `k`) that changes the
  diagonal packet count by more than a polynomial factor.
- A protocol-relevant growing-`mu` regime. This version treats `mu` as fixed.

The next useful proof target is therefore a codegree theorem: after quotient
packets are budgeted, the full-support families arising from Reed-Solomon words
should have bounded `>=a` common-intersection completion number. Proving that
would turn this L2 target into a direct protocol ledger bound.
