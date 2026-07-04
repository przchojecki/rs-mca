# KoalaBear BCHKS25 JMCA bounds v1

This shared directory contains the full verifier output for the KoalaBear
BCHKS25 packet.

Files:

- `run_output.json`: complete JSON emitted by
  `experimental/scripts/certify_koalabear_bchks25_jmca_bounds_v1.py`, including
  both the headline displayed-Theorem-4.6 certificate and the conditional
  parameter-squeeze appendix.

Regenerate and check from the repository root:

```text
python experimental/scripts/certify_koalabear_bchks25_jmca_bounds_v1.py --write
python experimental/scripts/certify_koalabear_bchks25_jmca_bounds_v1.py --check
```

The headline status is
`CONDITIONAL_ON_BCHKS25_THEOREM_4_6_AS_STATED`. The appendix status is
`CONDITIONAL_ON_PARAMETRIC_LIST_MCA_LEMMA_V1`.
