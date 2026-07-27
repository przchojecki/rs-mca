# KoalaBear active C5/base, twist, and Frobenius-9208 certificate

This certificate inserts the pair-global common-twist source-subline owner
and the selector-free degree-9,208 source-Frobenius endpoint owner after the
active C5/base predecessor.

```text
incoming active subtotal        2134115797
common-twist cap                2130706432
Frobenius-9208 cap          19621675550706
active paid total           19625940372935
remaining budget          274961102171022152
```

Replay:

```sh
python3 experimental/scripts/verify_kb_mca_v4_c5_twist_frobenius9208_adapter_v1.py --check
python3 experimental/scripts/verify_kb_mca_v4_c5_twist_frobenius9208_adapter_v1.py --tamper-selftest
```

The endpoint owner does not import the legacy rank-nine one-cut gate. It
uses only the proved algebraic endpoint and direct determinant root cap.
