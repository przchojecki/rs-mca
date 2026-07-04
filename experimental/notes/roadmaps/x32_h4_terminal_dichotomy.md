# X32: h=4 terminal dichotomy

- **DAG node:** `x32_h4_terminal_dichotomy`.
- **Consumer:** `active_core_count_bound`.
- **Status:** proved reduction.  This does not bound the remaining top-level
  norm-gate branch.
- **Verifier:** `experimental/scripts/verify_x32_h4_terminal_dichotomy.py`.
- **Certificate:**
  `experimental/data/certificates/x32-h4-terminal-dichotomy/x32_h4_terminal_dichotomy.json`.

## Statement

Let `n = 2^s`, let `H = mu_n` in a field of odd characteristic `p`, and let
`P,Q` be disjoint 4-subsets of `H` with equal top-three elementary symmetric
sums:

```text
e_1(P) = e_1(Q),       e_2(P) = e_2(Q),       e_3(P) = e_3(Q).
```

Choose exponents in `[0,n)` and write the first-sum signed word

```text
f(X) = sum_{zeta^i in P} X^i - sum_{zeta^j in Q} X^j.
```

Then exactly one of the following branches contains the trade.

1. **Antipodal quotient branch.**  `Phi_n | f` over `Z`.  Then `P` and `Q`
   are antipodal unions and descend through `x -> x^2` to a quotient h=2
   sum collision.  By X29 and X31 this branch is exactly:

   ```text
   mu_4 full-fiber baseline
   +
   quotient h=2 sparse norm-gate extras.
   ```

   Both are cyclic-pullback paid by the existing ledger.

2. **Top-level sparse norm gate.**  `Phi_n` does not divide `f`.  Then

   ```text
   p | Res(Phi_n, f).
   ```

   Thus every h=4 trade outside the paid antipodal quotient branch is an
   explicit 8-sparse top-level cyclotomic norm-gate event.

Consequently the h=4 terminal problem has no hidden third branch:

```text
h=4 residue = paid antipodal quotient branch + top-level 8-sparse norm gates.
```

The second summand is now the precise remaining h=4 obstruction.

## Proof

The equality `e_1(P)=e_1(Q)` says exactly that the reduction of `f` has the
chosen primitive root `zeta` as a zero:

```text
f(zeta) = 0 in F_p.
```

Since `n` is a power of two,

```text
Phi_n(X) = X^(n/2) + 1.
```

With `deg f < n`, divisibility by `Phi_n` is equivalent to

```text
coeff_i(f) = coeff_{i+n/2}(f)       for 0 <= i < n/2.
```

The coefficients of `f` lie in `{ -1,0,1 }`, because `P` and `Q` are disjoint.
Therefore, if `Phi_n | f`, the positive support and the negative support are
both antipodal unions.  Writing `pi(x)=x^2`, there are quotient pairs
`A,B subset mu_{n/2}` with

```text
P = pi^{-1}(A),       Q = pi^{-1}(B).
```

X29 gives

```text
L_P(X) = L_A(X^2),       L_Q(X) = L_B(X^2),
```

so the h=4 top-three condition is equivalent to the quotient h=2 condition

```text
sum(A) = sum(B).
```

X31 classifies those quotient collisions: the descended zero-sum branch lifts
to full `mu_4` fibers, and every quotient extra is a sparse quotient norm gate.
This proves branch 1 and its payment.

If `Phi_n` does not divide `f`, then `f` and `Phi_n` are coprime over `Z`.
Their reductions modulo `p` have the common root `zeta`, so their resultant is
zero modulo `p`:

```text
p | Res(Phi_n, f).
```

This is exactly the X30 finite-p norm-gate alternative, specialized to a
4-vs-4 first-sum word.  The e2/e3 equalities are extra conditions inside this
branch; the norm gate is necessary, not sufficient.

## Checked Examples

The verifier records one example from each branch:

```text
mu4 baseline:
  n=64, p=4993
  P={0,16,32,48}, Q={1,17,33,49}

antipodal quotient extra:
  quotient m=32, p=4993
  1+zeta^2 = zeta^8+zeta^21
  lifts to P={0,2,32,34}, Q={8,21,40,53} in mu_64

top-level norm gate, first-sum only:
  n=32, p=4993
  P={0,1,2,17}, Q={3,8,19,21}
```

The last row is deliberately only a first-sum example.  It demonstrates the
named top-level obstruction:

```text
f(zeta)=0,       Phi_n does not divide f,       p | Res(Phi_n,f).
```

It is not asserted to be an h=4 top-three trade.

The verifier also re-reads the X20/X21/X22 certificates and checks that the
existing h=4 finite evidence has no non-fingerprinted residue:

```text
X20 selected rows:        other = 0
X21 prime sweep:          non-fingerprinted rows = 0
X22 n=64 full window:     non-fingerprinted rows = 0
```

## What Remains

This packet does not close `active_core_count_bound`.  It reduces the first
campaign trade size to a precise per-row certification problem:

```text
count or exclude non-antipodal top-level 8-sparse norm-gated h=4 trades.
```

If that branch is empty at the official rows, then h=4 is fully paid.  If not,
its count must be charged as a norm-gate column and checked against the W4
`n^3` compiler allowance.

## Verification

Run:

```bash
python3 experimental/scripts/verify_x32_h4_terminal_dichotomy.py
```

To refresh the certificate:

```bash
python3 experimental/scripts/verify_x32_h4_terminal_dichotomy.py --write-certificate
```
