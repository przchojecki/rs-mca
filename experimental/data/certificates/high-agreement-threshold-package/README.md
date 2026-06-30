# High-Agreement Threshold Package Certificate

Status: PROVED-COMPILER-ARITHMETIC / AUDIT.

This directory contains the deterministic JSON certificate for the
`F_17^32`, `n=512`, `k=256` high-agreement threshold row and the
row-independent single-line compiler gate.

Generate and check it from the repository root:

```sh
python3 experimental/scripts/certify_high_agreement_threshold_package.py \
  --write experimental/data/certificates/high-agreement-threshold-package/f17_512_high_agreement_threshold_certificate.json

python3 experimental/scripts/certify_high_agreement_threshold_package.py \
  --check experimental/data/certificates/high-agreement-threshold-package/f17_512_high_agreement_threshold_certificate.json
```

Classify an arbitrary single-line high-agreement row:

```sh
python3 experimental/scripts/certify_high_agreement_threshold_package.py \
  --classify-row 512 256 17^32
```

Classify an official rate-`1/d` power-of-two field row using the inverse
boundary:

```sh
python3 experimental/scripts/certify_high_agreement_threshold_package.py \
  --classify-prize-power2 2 2^40 166
```

The certificate records:

- `open-proximity.tex` SHA-256 and line anchors for the official line family,
  MCA event, grand-challenge rates/field range, and line-decoding denominator;
- `floor(17^32 / 2^128) = 6`;
- hashes and decisive-row checks for the committed pure-MCA scanner replay
  `experimental/notes/certificate_scanner/outputs/f17_512_mca_only.report.json`;
- hashes and decisive-row checks for the committed line-plus-one-list scanner
  replay `experimental/notes/certificate_scanner/outputs/f17_512.report.json`,
  which shifts the coding threshold to `a=507/508`;
- affine and projective denominator checks;
- explicit finite support-wise MCA, finite no-loss CA, and projective
  denominator audit;
- exact tangent-range entry `a >= 427`;
- pure finite-slope support-wise MCA threshold `a=506/507`;
- same-denominator line-plus-one-list coding threshold `a=507/508`;
- exact M2 endpoint bridge checks
  `epsilon_mca(C,delta)=LD_sw(C,ceil((1-delta)n))/|F|`;
- closed endpoint language `[0,6/512)`;
- row-independent compiler examples for prize rates at `k=2^40`, including
  the `B_Q=0`, threshold-pinned, and exact-range-safe regimes;
- exact `k=2^40` prize-rate power-of-two denominator boundaries:
  `166,168,169,170` bits for rates `1/2,1/4,1/8,1/16`.
  The certificate also records the complementary official power-of-two
  ranges through bit `255` that require lower-agreement theory, and the exact
  minimum `k` this compiler would need to pin `Q=2^255`.
- the exact inverse criterion
  `k >= ceil(3*2^(lambda-128)/(d-1))` for rate `1/d`, `Q=2^lambda`.

It does not prove lower-agreement M1, quotient floors, extension transfer, L2,
or any protocol ledger that consumes extra list/curve/query/folding terms.
