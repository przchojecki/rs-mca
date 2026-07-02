# FM1 exact first-moment certificate

This directory contains the local verification artifact for FM1, the exact
aperiodic first-moment lemma for split locators.

- `fm1_exact_first_moment.json` records the F_13 rank/surjectivity check, the
  F_13 all-pairs two-locator joint-rank formula, the F_5 standard
  fiber-product joint-probability check, the overlap-excess decomposition and
  slack-one variance check, exact relative-variance/Chebyshev consumers, the
  F_5 brute-force first- and second-moment enumeration check, the
  Paley-Zygmund averaged-existence consumer, and the F_17^32 regular-window
  Markov consumer scale.
- The generating script is
  `experimental/scripts/verify_fm1_exact_aperiodic_first_moment.py`.
- The companion proof note is
  `experimental/notes/m1/fm1_exact_aperiodic_first_moment.md`.

Replay:

```bash
python3 experimental/scripts/verify_fm1_exact_aperiodic_first_moment.py --emit
```
