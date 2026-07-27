# KoalaBear next-slack source-plane closure

This packet pays the full-outside coefficient-rank-two branch at
`r=67,472` on the exact seven-owner residual, with zero additional owner
charge.

The source interpolation space has dimension exactly three. If its
base-rational span has dimension at most two, at most `p+1` finite map
images give the exact cap

```text
4,180,887,079,739,838
```

against the current reserve

```text
270,780,212,960,575,880.
```

If the base span has dimension three, reciprocal dimension two is already
owned by the active C5 cell. Reciprocal rank excess forces a `3 x 3`
polynomial rank-one normal form which contradicts the actual pair being
coprime and of exact reduced degree `67,473`.

```bash
python3 experimental/scripts/verify_kb_mca_v4_next_slack_source_plane_closure_v1.py --check
python3 experimental/scripts/verify_kb_mca_v4_next_slack_source_plane_closure_v1.py --tamper-selftest
```

```text
payload            9a48353924d95b2da22c062d91c3a86f89a92a608f09054240804d22043b8933
partition digest   7a57fa877417920862ed2fe2e5c569852555f78b73b046d320d5e7a65d98ebaa
additional charge  0
next open slack    67,473
```
