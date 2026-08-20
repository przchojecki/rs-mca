# Independent certificate review

Status: **GREEN.**

The canonical verifier uses integer arithmetic only. It checks:

- the exact KoalaBear row constants and parent SHA;
- the common-core-aware affine-ray scan over all `1,048,576` legal core sizes, with maximum \(8,147,918\);
- every proper affine-space quotient for dimensions \(0,\ldots,10\), with
  maximum \(1,031\);
- an exhaustive \(\mathbb F_3\) classification of maximal cliques through
  zero in the \(2\times2\) rank-one matrix graph;
- an exhaustive \(\mathbb F_5\), degree-\(<3\) common-root boundary;
- a mixed left/right rank-two rejection;
- canonical JSON serialization and hostile mutations.

The independent verifier reimplements the finite checks and arithmetic
without importing the canonical verifier. The Wolfram Language replay
independently confirms the deployed integer formulas. The certificate
contains no floating-point gate and no claim of rank-eleven payment.
