# E22 Quotient-Fiber Locator Saturation

- **DAG node:** `e22_fiber_locator_saturation`
- **Status:** PROVED
- **Source:** `prize/nodes/e22_fiber_locator_saturation/`
- **Verifier:** `python3 experimental/scripts/verify_e22_quotient_fiber_locator_saturation.py`

## Statement

Let `D` be a cyclic multiplicative subgroup domain, let `M` divide `|D|`,
and let `z` lie in the image of the quotient map

```text
pi_M(x) = x^M.
```

The fiber over `z`,

```text
F_z = {x in D : x^M = z},
```

has locator

```text
L_{F_z}(X) = X^M - z.
```

Consequently, for any squarefree support locator `L_R`, divisibility

```text
X^M - z | L_R
```

is equivalent to `F_z subset R`.  Products of distinct quotient-fiber factors
are therefore exactly local unions of full quotient fibers.

## Proof

Choose `y in D` with `y^M = z`.  Since `M | |D|`, the kernel of `pi_M` on
`D` is the subgroup `mu_M` of `M`-th roots of unity and has size `M`.
Thus

```text
F_z = y mu_M.
```

The roots of `X^M - z` are exactly the elements `y eta` with `eta in mu_M`,
because `(y eta)^M = y^M eta^M = z`.  There are `M` such roots and the
polynomial is monic of degree `M`, so

```text
X^M - z = prod_{x in F_z} (X - x) = L_{F_z}(X).
```

If `F_z subset R`, every linear factor of `L_{F_z}` occurs in the squarefree
locator `L_R`, hence `X^M - z` divides `L_R`.  Conversely, if `X^M - z`
divides `L_R`, every root in `F_z` is a root of `L_R`; since `L_R` is
squarefree with root set exactly `R`, the whole fiber is contained in `R`.

Distinct quotient values have disjoint fibers.  Multiplying distinct factors
`X^M - z` therefore records exactly the containment of the corresponding
union of full quotient fibers.

## Role In The Program

This is the local algebraic conversion needed by the `(Q)` quotient-fiber /
quotient-ledger route in `agents.md`: factor divisibility in a support locator
can be read as an exact full-fiber saturation statement, with no hidden
multiplicity at a fixed quotient value.

