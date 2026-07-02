# F17^32 M3 Rank-6 A385 No-Fixed-Core Pressure

Status: PROVED / AUDIT.

This packet records the first obstruction profile after the A385 fixed-core
synthesis.  If a separated A385 rank-6 branch avoids every fixed forced
two-point base core and is still projectively over budget, then it must contain
six finite split-locator classes plus an unpaid endpoint.

Since `deg Q<5`, each finite class has at most four base roots.  The six
degree-`127` split locators therefore need at least `738` external-root
incidences in the `384` external subgroup points.  This forces total pairwise
external overlap at least `354`, so some pair of finite classes shares at least
`24` external roots.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_no_fixed_core_pressure.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-no-fixed-core-pressure/f17_32_n512_k256_m3_rank6_a385_no_fixed_core_pressure.json
```
