# Aligned-positive moving--moving closure certificate

The JSON certificate in this directory is emitted by
`experimental/scripts/compile_kb_mca_v4_m2_aligned_positive_moving_closure_v1.sage`.
It deletes exactly the twelve moving--moving cells of the checked-in
36-cell aligned-positive `(1,1,2)` atlas.

The Sage compiler is load-bearing.  The Python verifier binds the compiler,
its atlas and predecessor dependencies, the exact cell fence, the balanced
parity terminals, literal transport, imported-cell provenance, and all
nonclaims.  Its mutation suite recomputes payload hashes before checking so
that semantic mutations cannot fail merely because of a stale digest.

This packet moves no ledger value and does not close K3 or the KoalaBear
row.  Fresh independent proof review remains required before promotion to a
GREEN banked result.
