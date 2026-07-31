# Aligned-positive F02/F03 deletion certificate

This directory certifies one local lemma in the 36-cell aligned-positive
diagonal `(1,1,2)` atlas:

```text
F02-R02, F02-R11, F02-R20 are empty,
and literal full-source b -> b^-1 transport makes
F03-R02, F03-R11, F03-R20 empty.
```

The conclusion is local.  It moves no ledger, assigns no owner or charge, and
does not close K3.  In particular, `F00/F01`, `F04`--`F07`, and all
moving-moving assignments remain open.

Files:

- `kb_mca_v4_m2_aligned_positive_f02_f03_deletion_v1.json` — generated
  factor/branch, localized Groebner, lex-point, full-quotient, and literal
  source-transport certificate.
- `schema.json` — structural schema.  The Python verifier adds exact semantic
  checks and mutation tests.

Replay:

```bash
env HOME=/private/tmp/rs_mca_sage_home /usr/local/bin/sage \
  experimental/scripts/compile_kb_mca_v4_m2_aligned_positive_f02_f03_deletion_v1.sage \
  --check

python3 \
  experimental/scripts/verify_kb_mca_v4_m2_aligned_positive_f02_f03_deletion_v1.py \
  --check --tamper-selftest

python3 -O \
  experimental/scripts/verify_kb_mca_v4_m2_aligned_positive_f02_f03_deletion_v1.py \
  --check --tamper-selftest
```

The Sage replay performs exactly nine factor-first localized Groebner
computations over `GF(2130706433)`.  `R11` is a direct unit ideal.  `R02` and
`R20` have respectively four and eight exact quadratic-field q-slice points;
both full quotient identities have a certified nonzero coefficient-one
mismatch at every point.

No generic saturation, random sampling, floating-point arithmetic, or
Möbius covariance is used.
