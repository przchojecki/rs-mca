# FM1 exact first-moment certificate

This directory contains the local verification artifact for FM1, the exact
aperiodic first-moment lemma for split locators.

- `fm1_exact_first_moment.json` records the F_13 rank/surjectivity check and
  the F_5 brute-force enumeration check.
- The generating script is
  `experimental/scripts/verify_fm1_exact_aperiodic_first_moment.py`.
- The companion proof note is
  `experimental/notes/m1/fm1_exact_aperiodic_first_moment.md`.

Replay:

```bash
python3 experimental/scripts/verify_fm1_exact_aperiodic_first_moment.py --emit
```
