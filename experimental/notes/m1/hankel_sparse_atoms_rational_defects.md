# Hankel Sparse Atoms as Rational Defects

- **Status:** PROVED / structural packet.
- **DAG node:** `hankel_sparse_atoms_as_rational_defects`.
- **Certificate:** `experimental/data/certificates/hankel-sparse-atoms/hankel_sparse_atoms.json`.
- **Verifier:** `python3 experimental/scripts/verify_hankel_sparse_atoms_packet.py --check experimental/data/certificates/hankel-sparse-atoms/hankel_sparse_atoms.json`.

This packet records the rational-defect description of sparse annihilator atoms
for a Hankel state. It is the local separation input used by the
rank-profile entropy argument.

## Claim

For a Hankel state `P` on an evaluation set `E`, the sparse affine annihilator
has the RS-dual normal form

```text
Ann_E(P) = GRS_{n_E-j-1}(E, lambda) + omega RS_t(E).
```

Equivalently, every annihilator word has coordinates

```text
u_x = omega_x h(x) + lambda_x g(x),
deg h < t,
deg g <= n_E - j - 2.
```

A sparse atom is therefore a small defect set of a rational approximant
`-lambda g/h` to the spectral weight `omega`.

## Separation and Collapse

If two atoms come from distinct saturated rational-approximant classes, then
eliminating `omega` gives

```text
F = g_1 h_2 - g_2 h_1,
deg F <= n_E - j + t - 3.
```

The degree count forces the union of their defect supports to satisfy

```text
|T_1 union T_2| >= j - t + 2.
```

The working record verified this separation on `233130` atom pairs with zero
violations.

If atoms come from the same rational approximant, their restrictions to the
defect block are diagonal rescalings of a punctured GRS code. The MDS property
then makes all such atoms saturate to one closure.

## Heredity

The packet is stable under descent: passing to a child state multiplies the
spectral weight by the child locator factor, so the same rational-defect
description applies recursively.

## DAG Use

`hankel_rank_profile_entropy` consumes this separation/collapse packet to show
that row-full wide Hankel states have at most one low-weight atom closure.

## Non-Claims

- This packet does not prove the rank-profile entropy theorem by itself.
- This packet does not count row-deficient Hankel states.
- This packet does not provide the support-lattice accounting identity.
- This packet does not edit Papers A-D.
