# L2 Codegree Reduction Packet

- **Status:** PROVED / structural reduction.
- **DAG node:** `codegree`.
- **Certificate:** `experimental/data/certificates/codegree/codegree.json`.
- **Verifier:** `python3 experimental/scripts/verify_codegree_packet.py --check experimental/data/certificates/codegree/codegree.json`.

This packet names the proved L2 codegree reduction consumed by `list_safe`.
It packages the proved reduction boundary from
`experimental/notes/l2/l2_codegree_reduction_theorem.md` without promoting the
conditional exponent-saving corollary.

## Proved Content

The L2 interleaved-list object is reduced to base-code and higher-agreement
lists by codegree decomposition.

For `mu = 2`,

```text
Lambda_2^{(a)}(U_1,U_2)
  = sum_{c_1 in Fib_{U_1}} |{c_2 : |A_{U_1}(c_1) cap A_{U_2}(c_2)| >= a}|.
```

Equivalently, the inner count is a punctured-RS list for `U_2` on the agreement
set `A_{U_1}(c_1)`.

The two-regime reduction is

```text
Lambda_2^{(a)}(U_1,U_2)
  <= |Fib_{U_2}| + M_{U_2}(2a-k) |Fib_{U_1}|.
```

For general fixed arity `mu`, peeling one row gives

```text
Lambda_mu^{(a)}
  <= Lambda_{mu-1}^{(a)}
     + Lambda_{mu-1}^{(2a-k)} |Fib_{U_1}|.
```

These are L1-free structural reductions. They identify the exact L1-family
tail input needed for the saving, rather than hiding it.

## Evidence

The upstream note records the proofs and replay scripts:

```text
experimental/notes/l2/l2_codegree_reduction_theorem.md
experimental/scripts/verify_l2_codegree_decomposition.py
experimental/scripts/verify_l2_reduction_bound.py
experimental/scripts/verify_l2_mu_recursion.py
```

The packet verifier checks the certificate status boundary and the named
reduction formulas. The upstream scripts should be run when replaying the full
evidence bundle.

## Conditional Boundary

The exponent-saving corollary is not part of this PROVED packet. It requires a
named L1-family tail/profile input such as polynomial control of
`Lambda_j^{(2a-k)}` or `M(2a-k)` after quotient-periodic mass is budgeted.

## DAG Consequence

`codegree` is a proved input to `list_safe` alongside `imgfib`, `m_sweep`, and
`m_handling`. It does not close `list_safe` without the remaining `imgfib`
input.

## Non-Claims

- This packet does not prove the L1 image-fiber theorem.
- This packet does not prove the exponent-saving corollary unconditionally.
- This packet does not close `list_safe`.
- This packet does not edit Papers A-D.
