# E22 Cofactor Petal Divisibility

- **DAG node:** `e22_cofactor_petal_divisibility`
- **Status:** PROVED
- **Source:** `prize/nodes/e22_cofactor_petal_divisibility/`
- **Depends on:** `e22_agreement_cofactor_equations`
- **Verifier:** `python3 experimental/scripts/verify_e22_cofactor_petal_divisibility.py`

## Statement

For each touched petal in an E22 mixed/full-petal challenger, the cofactor
equation

```text
U(x) L_{Z\C}(x) = a_i L_{C\Z}(x)
```

on the agreement subset `T_i` is equivalent to divisibility of

```text
H_i(X) = U(X)L_{Z\C}(X) - a_i L_{C\Z}(X)
```

by the locator `L_{T_i}(X)`.  In particular, a full touched petal contributes
the full petal locator as a divisor of `H_i`.

## Proof

The node `e22_agreement_cofactor_equations` gives, for every petal agreement
point `x in T_i`,

```text
U(x)L_{Z\C}(x) = a_i L_{C\Z}(x).
```

Define

```text
H_i(X) = U(X)L_{Z\C}(X) - a_i L_{C\Z}(X).
```

The pointwise cofactor equation says exactly that `H_i(x)=0` for each
`x in T_i`.  The petal points are distinct field points, so the agreement-set
locator

```text
L_{T_i}(X) = prod_{x in T_i} (X-x)
```

is squarefree and has precisely those roots.  Therefore `H_i` vanishes on
`T_i` if and only if every linear factor `(X-x)` for `x in T_i` divides
`H_i`, equivalently if and only if `L_{T_i}` divides `H_i`.

When the petal is full, `T_i=P_i`, so the full petal locator divides `H_i`.

## Role In The Program

This is the divisor form of the E22 cofactor constraints.  It is the bridge
from petal agreement equations to the quotient/tail support-forcing work in
the `(Q)` route.

