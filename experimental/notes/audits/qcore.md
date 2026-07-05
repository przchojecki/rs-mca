# Quotient-Core List Lower-Bound Packet

- **Status:** PROVED / q-independent counting.
- **DAG node:** `qcore`.
- **Certificate:** `experimental/data/certificates/qcore/qcore.json`.
- **Verifier:** `python3 experimental/scripts/verify_qcore_packet.py --check experimental/data/certificates/qcore/qcore.json`.

This packet names the quotient-core counting theorem used by the list-unsafe
side of the prize DAG.

## Claim

For a smooth subgroup row with a quotient scale `M` dividing `k`, the quotient
core construction gives a q-independent family of codewords. At agreement
`k + sigma`, whenever `0 <= sigma < M`, the count is at least

```text
binom(n/M - 1, k/M).
```

The lower bound is pure support/quotient counting. It does not rely on finite
field collision, norm-threshold, or value-set assumptions.

## Consequence

This is the counting input for `list_unsafe`: the list side has an unconditional
quotient-core lower family once the object/rules conventions are fixed by the
S0 layer. The packet does not itself assemble the endpoint or epsilon-star
crossing statement.

## Evidence Boundary

The theorem is recorded in the list-side proof sketch as `thm:qcore`. The
packet certificate stores the formula and sample arithmetic only; it is meant
to make the named DAG dependency explicit for downstream row packets.

## Non-Claims

- This packet does not close `list_unsafe`.
- This packet does not decide endpoint conventions.
- This packet does not provide the S0 object/rules audit.
- This packet does not prove the list-safe upper bound.
- This packet does not edit Papers A-D.
