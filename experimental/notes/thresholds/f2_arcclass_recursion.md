# F2 arc-class recursion and Parseval guardrail

- **Status:** PROVED self-contained orthogonality lemma, plus a proved
  nonclosure guardrail for raw Parseval.
- **Track:** `(Q)` / F2 quotient-prefix flatness lane.
- **Verifier:** `python3 experimental/scripts/verify_f2_arcclass_recursion.py`

## Setting

Let `D = mu_n subset F_q^x`, and for a weight-`b` subset `S subset D` write

```text
p_1(S) = sum_{x in S} x,
p_2(S) = sum_{x in S} x^2.
```

For `lambda=(lambda_1,lambda_2) in F_q^2`, define the Fourier arc

```text
E_b(lambda) = sum_{|S|=b} psi(lambda_1 p_1(S) + lambda_2 p_2(S)).
```

Let

```text
N_b^{(1)}(0)  = #{|S|=b : p_1(S)=0},
N_b^{(2x)}(0) = #{|S|=b : p_2(S)=0},
N_b^{(12)}(0)= #{|S|=b : p_1(S)=p_2(S)=0}.
```

## Arc-Class Recursion

The structured arc masses collapse exactly to lower-order censuses:

```text
(1/q^2) sum_{lambda_1 in F_q} E_b(lambda_1,0)
  = (1/q) N_b^{(1)}(0),

(1/q^2) sum_{lambda_2 in F_q} E_b(0,lambda_2)
  = (1/q) N_b^{(2x)}(0),

(1/q^2) sum_{lambda in F_q^2} E_b(lambda)
  = N_b^{(12)}(0).
```

Proof. Exchange the finite sums over subsets and over `lambda`; then use

```text
sum_{lambda in F_q} psi(lambda v) = q 1_{v=0}.
```

This gives the exact regrouping

```text
N_b^{(12)}(0)
  = binom(n,b)/q^2
    + (N_b^{(1)}(0)/q  - binom(n,b)/q^2)
    + (N_b^{(2x)}(0)/q - binom(n,b)/q^2)
    + (1/q^2) sum_{lambda_1 != 0, lambda_2 != 0} E_b(lambda).
```

Every term is exact. Thus the structured arc classes in the `t=2` F2
inversion are not per-arc estimates: they recurse to `t=1` censuses. Only the
generic class `lambda_1 lambda_2 != 0` remains as the new estimate target.

The same one-line proof works for general `t`: each coordinate subset of the
moment map contributes the corresponding lower-order census by orthogonality.

## Consequence For The F2 Program

This corrects the tempting but infeasible plan of computing individual
structured arcs at official scale. A single mid-band value of `E_b(lambda)` has
size about `binom(n,b)` and cannot be computed directly when `n ~= 2^41`.
The assembly only needs arc-class masses, and those masses are exactly
lower-order censuses.

For `p_2`, the order-one census is the exact two-cover version of the linear
zero-sum census on the squared root domain: at even `n`, the squaring map
`mu_n -> mu_{n/2}` is two-to-one, so each image point carries multiplicity
`0,1,2` according to how many preimages are selected. For `p_1`, the remaining
primitive problem is the mildest linear zero-sum fiber. This makes the natural
proof order: solve/prioritize the `t=1` zero-fiber flatness input, then lift
through the recursion and pay the generic class.

## Parseval Guardrail

Let

```text
SP_b = sum_s N_b(s)^2
     = #{(S,S') : |S|=|S'|=b and (p_1,p_2)(S)=(p_1,p_2)(S')}.
```

Parseval gives

```text
sum_lambda |E_b(lambda)|^2 = q^2 SP_b.
```

But raw Parseval cannot close the mid-band on its own. Even in the most
optimistic collision-free case `SP_b = binom(n,b)`, Cauchy's pointwise bound
would only give

```text
N_b^{(12)}(0) <= sqrt(SP_b) = sqrt(binom(n,b)),
```

which is exponentially larger than the finite-prize polynomial budget at the
mid-band peak. Therefore a successful F2 mid-band proof must use the special
structure of the zero value and the paid lower-order/generic split; an `L^2`
fiber statistic alone is not enough.

## Nonclaims

This packet does not bound the generic class, does not prove the `t=1`
zero-fiber flatness input, and does not close `(Q)`. It records the exact
recursion interface that any F2 mid-band argument can consume.
