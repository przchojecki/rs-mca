# X24: characteristic-zero dyadic descent

- **DAG node:** `x24_char0_dyadic_descent`.
- **Consumer:** `active_core_count_bound`.
- **Status:** proved over characteristic zero.
- **Verifier:** `experimental/scripts/verify_x24_char0_dyadic_descent.py`.
- **Certificate:**
  `experimental/data/certificates/x24-char0-dyadic-descent/x24_char0_dyadic_descent.json`.

## Statement

Let `n=2^s` and `H=mu_n(C)`.  Let `P,Q` be disjoint h-subsets of `H`
with equal first `h-1` elementary symmetric sums.

Then:

```text
if h is not a power of two:  no such trade exists;
if h is a power of two:      P and Q are full mu_h fibers.
```

Equivalently, characteristic-zero dyadic trades are exactly cyclic full-fiber
trades.

## Proof

Write `H=<zeta>`, and encode the difference of supports by the signed word

```text
f(X) = sum_{zeta^i in P} X^i - sum_{zeta^j in Q} X^j.
```

Equality of `e_1` gives `f(zeta)=0`.  Since `n` is a power of two,

```text
Phi_n(X) = X^(n/2) + 1.
```

With exponents represented in `[0,n)`, `deg f < n`, so `Phi_n | f` is
equivalent to

```text
coeff_i(f) = coeff_{i+n/2}(f)       for 0 <= i < n/2.
```

Because `P` and `Q` are disjoint, the coefficients are in `{ -1,0,1 }`.
Thus the positive and negative supports are both antipodal unions.  In
particular, `h` must be even.

If `h` is odd, this is impossible, so no trade exists.

If `h=2m`, write

```text
P = pi^{-1}(P'),       Q = pi^{-1}(Q'),       pi(x)=x^2,
```

with `P',Q'` disjoint m-subsets of `mu_{n/2}`.  Their locators satisfy

```text
L_P(X) = L_{P'}(X^2),       L_Q(X) = L_{Q'}(X^2).
```

Equality of the top `h-1=2m-1` coefficients of `L_P` and `L_Q` is therefore
equivalent to equality of the top `m-1` coefficients of `L_{P'}` and
`L_{Q'}`.  Hence `(P',Q')` is an m-trade in `mu_{n/2}`.

Iterating this descent proves:

- if any odd factor remains in `h`, the descent reaches an odd trade size and
  stops by contradiction;
- if `h=2^a`, the descent reaches size `1`, where the two singleton quotient
  supports are arbitrary and distinct.

Lifting back from the final singleton stage gives exactly the fibers of

```text
x -> x^h.
```

So `P` and `Q` are full `mu_h` fibers.

## Consequences for the terminal node

This explains both h=4 and h=5:

```text
h=4: characteristic-zero trades are exactly mu_4 full fibers;
h=5: characteristic-zero trades are impossible.
```

Finite-field terminal residues are therefore p-specific reductions of this
characteristic-zero picture.  The X20-X22 h=4 antipodal quotient lifts are an
example: they are finite-field reductions, but still cyclic-pullback paid.

The remaining proof obligation is not a characteristic-zero classification.
It is the finite-p certification/charging of p-specific reductions.

## Verification

Run:

```bash
python3 experimental/scripts/verify_x24_char0_dyadic_descent.py
```

To refresh the certificate:

```bash
python3 experimental/scripts/verify_x24_char0_dyadic_descent.py --write-certificate
```

Current replay: **15 PASS, 0 FAIL**.
