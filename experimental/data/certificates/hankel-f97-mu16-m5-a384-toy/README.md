# F_97/mu_16 M5 A=384 Toy U1-U5 Packet

Status: `PROVED-LOCAL / EXPERIMENTAL`.

This packet is the compact replay artifact for the `F_97`, `n=16`, `k=8`,
`A=12` deficiency-one toy row used by
`experimental/notes/m5/m5_underdetermined_a384_pivot_packet.md`.

It verifies the U1-U5 top-chart chain for one declared toy family:

```text
U1: deficiency-one kernel is the signed maximal-minor Cramer vector;
U2: the declared family is nondegenerate;
U3/U4: top-chart validity is divisibility by X^16-1, checked by
       pseudo-remainder equations;
U5: the pseudo-remainder coefficient gcd is the constant eliminant 1.
```

This closes only the declared toy top chart.  It does not claim a threshold,
a worst-case row bound, or any `F_17^32` result.

Replay:

```bash
python3 experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py \
  --check experimental/data/certificates/hankel-f97-mu16-m5-a384-toy/f97_mu16_n16_k8_a12_m5_deficiency_one_toy_u1_u5.json
```
