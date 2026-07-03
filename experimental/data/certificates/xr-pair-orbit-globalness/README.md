# XR Pair-Orbit Globalness Certificate

Status: EXPERIMENTAL_EVIDENCE / EXACT_N16_CORPUS / SAMPLED_N32.

This directory contains the E18/E19 actual-pair scanner output.  It evaluates
genuine alignment sets

```text
A_{u,v} = {T in D_j : H_u l_T is parallel to H_v l_T and H_v l_T != 0}
```

instead of the E11 candidate-family dictionary.  The `n=16`, `j=8`, `F_97`,
`t=2` corpus is exact over the committed finite pair-orbit corpus.  The `n=32`,
`j=16` rows are Monte Carlo telemetry.

Replay from the repository root:

```sh
python3 experimental/scripts/verify_xr_pair_orbit_globalness.py --write
python3 experimental/scripts/verify_xr_pair_orbit_globalness.py --check
```

The E19 KLLM column is deliberately labelled as a proxy:

```text
max_r-link_density <= min(1, n^r * density(A)).
```

The certificate also reports a separate paid-tangent leak flag for post-strip
rows whose fixed-core link density is at least `9/10`.  In the exact `n=16`
corpus this flag fires on delta-character rows, so the packet is a taxonomy
warning rather than a clean globalness pass.

E20/QX.10 still needs to pin the imported KLLM constants before this proxy can
be promoted to a theorem-level threshold.
