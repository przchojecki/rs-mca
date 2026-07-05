# Axis 4 Same-Support Predicate

- **Status:** PROVED / citation plus local predicate alignment.
- **DAG node:** `axis4_predicate`.
- **Certificate:** `experimental/data/certificates/axis4-predicate/axis4_predicate.json`.
- **Verifier:** `python3 experimental/scripts/verify_axis4_predicate.py --check experimental/data/certificates/axis4-predicate/axis4_predicate.json`.

This packet resolves S0 axis 4.  ABF's MCA bad event is the same-support
noncontainment condition for a line point: on a support `S`, the point
`f1 + gamma f2` agrees with the code, but the pair `(f1, f2)` does not agree
with a two-way interleaved codeword on that same support.

In repo terminology this is the same-support degenerate-pencil residue
predicate, using the local `noncontain_degeneracy` identification.

## Statement

ABF26 Definition 4.3 asks for a support `S` with:

```text
Delta_S(f1 + gamma f2, C) = 0
Delta_S((f1, f2), C^{==2}) > 0
```

The first condition says the slope has an aligned support.  The second says
the whole pair is not contained in the same support-wise two-codeword product.
The repo's `noncontain_degeneracy` node identifies that noncontainment with the
degenerate-pencil residue predicate.

## Citation Pin

The certificate pins ABF26 / IACR ePrint 2026/680, page 17, with PDF sha256:

```text
426a979c13cc61db0f2cdb909067ef4c9f24438859fe0a7a337d2b19b07fcaa5
```

The checked fragments are:

```text
Definition 4.3
exists S = S_gamma
Delta_S(f1 + gamma f2, C) = 0
Delta_S((f1, f2), C^{==2}) > 0
```

## Consequence

Packets using the repo residue dictionary may treat ABF's support-wise MCA bad
event and the same-support degenerate-pencil predicate as the same object,
provided they keep the support `S` fixed across the line point and the pair
test.

## Non-Claims

- This packet does not prove the full residue dictionary.
- This packet does not count bad slopes.
- This packet does not change CA or list-decoding predicates.
