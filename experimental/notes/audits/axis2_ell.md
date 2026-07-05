# Axis 2 Pair-Versus-Tuple Reading

- **Status:** PROVED / citation check.
- **DAG node:** `axis2_ell`.
- **Certificate:** `experimental/data/certificates/axis2-ell/axis2_ell.json`.
- **Verifier:** `python3 experimental/scripts/verify_axis2_ell.py --check experimental/data/certificates/axis2-ell/axis2_ell.json`.

This packet resolves S0 axis 2.  The official MCA challenge is formulated for
pairs of received words on an affine line, not for arbitrary `ell`-tuples as
the primitive MCA object.

## Statement

ABF26 defines CA and MCA from two words `f1, f2` and the line
`{f1 + gamma f2}`.  The MCA bad event compares the same pair `(f1, f2)` with
the two-way interleaved code `C^{==2}` on a support.

The paper separately records interleaving stability for `C^{==t}`.  That
theorem does not change the official MCA sampler into arbitrary `ell`-tuples;
it says the interleaved-code MCA error equals the base-code MCA error.

## Citation Pin

The certificate pins ABF26 / IACR ePrint 2026/680, page 17, with PDF sha256:

```text
426a979c13cc61db0f2cdb909067ef4c9f24438859fe0a7a337d2b19b07fcaa5
```

The checked fragments are:

```text
Let f1, f2
line L := {f1 + gamma f2}
Delta_S((f1, f2), C^{==2})
epsilon_mca(C^{==t}, delta) = epsilon_mca(C, delta)
```

## Consequence

The MCA object used by row packets is the pair/line object:

```text
sampler:      f1 + gamma f2
support test: same-support pair condition against C^{==2}
```

If a packet studies higher-arity interleaving, it should state whether it is
using the ABF interleaving-stability theorem, a list-side `m` object, or a
separate protocol generator.

## Non-Claims

- This packet does not prove the interleaving-stability theorem.
- This packet does not resolve list-side constant-`m` thresholds.
- This packet does not forbid protocol-specific higher-arity generators.
