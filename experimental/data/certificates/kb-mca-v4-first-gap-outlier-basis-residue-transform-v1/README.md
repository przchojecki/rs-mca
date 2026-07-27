# KoalaBear first-gap outlier-basis/residue transform

This packet verifies that every independent outlier basis canonically
reconstructs one graph line and its complement locator through bordered
minors. It also checks the exact reindexing

```text
sum_L beta_L*(J_L-20)_+ = sum_B (J_B-20)_+.
```

Replay:

```bash
python3 experimental/scripts/verify_kb_mca_v4_first_gap_outlier_basis_residue_transform_v1.py --check
python3 experimental/scripts/verify_kb_mca_v4_first_gap_outlier_basis_residue_transform_v1.py --tamper-selftest
```

The finite model checks the algebra and normalization. It is not evidence for
the deployed weighted incidence bound.

The certificate also prints the exact active first-gap sufficient allowance:

```text
E20 <=
2930589315151076074409054963728781743707264369983654.
```

The packet makes no ledger movement. The selected-basis source-residue
packing theorem remains open.

The source-coupled `F_17` control uses an actual rank-four
`Lambda_Sigma * F[X]_(<=3)` subspace, exhausts all 495 carrier bases, and
checks 36 source pairs with canonical one-witness-per-slope selection. Its
largest admitted rich-basis count is `20`, its largest weighted excess is
`45`, and its largest basis multiplicity is `7`. These are finite controls,
not deployed asymptotic bounds.
