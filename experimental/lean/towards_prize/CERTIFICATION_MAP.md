# TowardsPrize Finite Anchor Map

Status: PROVED finite arithmetic anchors / AUDIT bridge to verifier-backed
certificates.

The anchors in `TowardsPrize.FiniteAnchors` check printed finite numerators and
arithmetic identities. They do not replace the Python replay scripts that prove
the Reed-Solomon enumeration semantics.

| Certificate claim | Lean anchor | Source artifact | Status |
|---|---|---|---|
| The `(q,n,k,r)=(7,6,3,2)` sparse mutual layer has printed numerator `sigma_C=7`. | `TowardsPrize.FiniteAnchors.sigma_q763_r2_value` | `experimental/data/certificates/sigma-c-sparse-census/` | PROVED finite arithmetic anchor; verifier-backed census |
| The `(q,n,k,r)=(5,4,1,2)` sparse mutual layer counterexample row has printed numerator `sigma_C=3`. | `TowardsPrize.FiniteAnchors.sigma_q541_r2_value` | `experimental/data/certificates/sigma-c-sparse-census/` | PROVED finite arithmetic anchor; verifier-backed census |
| The `(7,6,3)` EMCA staircase rows satisfy `max(eca,sigma)=emca` at `r=0,1,2`. | `emca_q763_sparsify_r0`; `emca_q763_sparsify_r1`; `emca_q763_sparsify_r2` | `experimental/data/certificates/exact-worstcase-eca-emca-staircase/` | PROVED finite arithmetic anchor; verifier-backed census |
| The identity-prefix toy count `C(16,9)=11440` is kernel-checked. | `identity_prefix_floor_q17_n16_k8` | `TowardsPrize.lean` finite anchor | PROVED arithmetic |

## Non-Claims

These anchors do not prove full census exhaustiveness, support-wise MCA
semantics, or list-decoding semantics. Those remain attached to the relevant
certificate replay scripts.
