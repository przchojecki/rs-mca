# KoalaBear BCHKS25 JMCA safe edge v1

Status: `CONDITIONAL_ON_BCHKS25_THEOREM_4_6_AS_STATED`.

This directory contains the headline certificate for the deployed KoalaBear
sextic row using BCHKS25 Theorem 4.6 exactly as displayed.

Files:

- `certificate.json`: the per-result JSON certificate for the displayed
  Theorem 4.6 safe edge.

Regenerate and check from the repository root:

```text
python experimental/scripts/certify_koalabear_bchks25_jmca_bounds_v1.py --write
python experimental/scripts/certify_koalabear_bchks25_jmca_bounds_v1.py --check
```

Claimed safe edge:

```text
delta <= 604085 / 2097152
A >= 1493067
```

Non-claims: this directory does not certify the parameter-squeeze appendix,
does not close the deployed KoalaBear band, and does not make a protocol
soundness claim.
