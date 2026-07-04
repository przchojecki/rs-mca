# KoalaBear BCHKS25 JMCA parameter squeeze v2

Status: `CONDITIONAL_ON_PARAMETRIC_LIST_MCA_LEMMA_V1`.

This directory contains the appendix certificate for the stronger KoalaBear
parameter squeeze. It is not a consequence of BCHKS25 Theorem 4.6 as displayed;
it depends on the parametric bridge lemma in
`experimental/notes/audits/koalabear_bchks25_parametric_list_mca_lemma_v1.md`.

Files:

- `certificate.json`: the per-result JSON certificate for the conditional
  parameter-squeeze endpoint.

Regenerate and check from the repository root:

```text
python experimental/scripts/certify_koalabear_bchks25_jmca_bounds_v1.py --write
python experimental/scripts/certify_koalabear_bchks25_jmca_bounds_v1.py --check
```

Conditional endpoint, if the bridge lemma is accepted:

```text
delta <= 611983 / 2097152
A >= 1485169
```

Non-claims: this directory does not promote the squeeze to a displayed
Theorem 4.6 corollary and does not close the deployed KoalaBear band.
