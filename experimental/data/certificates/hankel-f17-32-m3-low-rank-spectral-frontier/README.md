# M3 Low-Rank Spectral Frontier Probe

Status: EXPERIMENTAL / AUDIT.

This directory records a bounded counterexample-first probe for the PR #170
synthetic low-rank spectral target

```text
gcd(Phi_{m,r,0}, Phi_{m,r,1}) = 1.
```

The probe covers the first top-window frontier beyond the certified
low-rank2..12 packet:

```text
A = 426,    m = 87,    ranks 13..20.
```

It crosses the characteristic-17 boundary: ranks `13..16` use Newton
identities, while ranks `17..20` use determinant interpolation.
The JSON includes the row descriptor, target, probe parameters, and source
artifact hashes.

The same script also has an opt-in contiguous all-shift mode.  For example, at
`A=426`, rank `13`, there are `84` available contiguous shifts, and the running
gcd is already constant after checking the first two:

```bash
python3 experimental/scripts/search_f17_32_m3_low_rank_spectral_target.py \
  --agreement-min 426 --agreement-max 426 \
  --rank-min 13 --rank-max 13 \
  --shift-mode all-contiguous
```

Reproduce or check the recorded JSON:

```bash
python3 experimental/scripts/search_f17_32_m3_low_rank_spectral_target.py \
  --agreement-min 426 --agreement-max 426 \
  --rank-min 13 --rank-max 20 \
  --stop-on-collision --write \
  experimental/data/certificates/hankel-f17-32-m3-low-rank-spectral-frontier/f17_32_m3_low_rank_spectral_frontier_a426_r13_20.json

python3 experimental/scripts/search_f17_32_m3_low_rank_spectral_target.py \
  --agreement-min 426 --agreement-max 426 \
  --rank-min 13 --rank-max 20 \
  --stop-on-collision --check \
  experimental/data/certificates/hankel-f17-32-m3-low-rank-spectral-frontier/f17_32_m3_low_rank_spectral_frontier_a426_r13_20.json
```

Observed summary:

```text
records: 8
degree failures: 0
coefficient methods: {'interpolation': 4, 'newton': 4}
common gcd degree histogram: {'0': 8}
first collision: none
```

Nonclaims: this is not a certificate for the endpoint-capacity range, not an
arbitrary-row M3 result, and not a replacement for the low-rank2..12 proved
packet. It is a reproducible frontier probe showing that the first eight
uncertified ranks at `A=426` do not produce a spectral collision.
