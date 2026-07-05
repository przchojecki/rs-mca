# E22 Agreement Cofactor Equations

- **DAG node:** `e22_agreement_cofactor_equations`
- **Status:** PROVED
- **Source:** `prize/nodes/e22_agreement_cofactor_equations/`
- **Verifier:** `python3 experimental/scripts/verify_e22_agreement_cofactor_equations.py`

## Statement

For any listed E22 sunflower codeword `f` and its zero-agreement root set
`Z` inside `C union B0`, write

```text
f = U L_Z.
```

Then every petal agreement on petal `i` becomes the cofactor equation

```text
U(x) L_{Z\C}(x) = a_i L_{C\Z}(x)
```

after cancelling the common core factor.  Thus the mixed/full-petal
support-forcing problem may be studied through these cofactor equations on
petal agreement points.

## Proof

Let `C` be the core, `B0` the background, and `P_i` a petal with scalar
`a_i`.  The received word is zero on `C union B0` and equals `a_i L_C(x)` on
`P_i`.

Let `f` be a listed codeword, and let `Z subset C union B0` be the
coordinates where `f` agrees with the zero part of the received word.  Since
every point in `Z` is a root of `f`, write

```text
f = U L_Z.
```

Split the zero-agreement roots by their relation to the core:

```text
Z = (Z cap C) union (Z \ C),
C = (Z cap C) union (C \ Z).
```

At a petal agreement point `x in P_i`,

```text
U(x)L_Z(x) = f(x) = a_i L_C(x).
```

Petal points are disjoint from the core and background, so
`L_{Z cap C}(x)` is nonzero.  Cancelling this common locator factor gives

```text
U(x) L_{Z\C}(x) = a_i L_{C\Z}(x).
```

The argument applies to every petal agreement point, whether the petal is
full or partial.

## Role In The Program

This is the algebraic entry point for the E22 cofactor branch of the `(Q)`
quotient-ledger route.  It converts petal agreements into polynomial
cofactor constraints that downstream divisibility, tail, and quotient-fiber
packets can reason about.

