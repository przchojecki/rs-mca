# Q3R.2 link-leak adjudication certificate

This directory contains the deterministic certificate emitted by:

```bash
python3 experimental/scripts/verify_q3r2_link_leak_adjudication.py --write
```

The packet reads the exact #209 XR pair-orbit corpus and classifies the ten
post-strip link-leak candidates under the `L_tan` convention.  It rebuilds only
the exact `F_97`, `n=16`, `j=8`, `t=2` rows and does not rerun the sampled
`n=32` telemetry.

Replay:

```bash
python3 experimental/scripts/verify_q3r2_link_leak_adjudication.py --check
python3 -m py_compile experimental/scripts/verify_q3r2_link_leak_adjudication.py
```

The conclusion is that all ten candidates are strippable or allowed under the
residual-edge `L_tan = 2` cap.  The two character-pair rows are the only rows
that remain convention-sensitive if a later packet insists on `L_tan = 1`
without a residual-edge deduplication rule.
