# Hankel smoke packet for the settled F_17^32 row

This directory contains a v9 `aperiodic-hankel-eliminant-v1` smoke packet for
the already-settled high-agreement row

```text
C = RS[F_17^32,H,256]
n = 512
k = 256
A = 506, 507
```

It is generated from the existing high-agreement threshold package:

```text
experimental/data/certificates/high-agreement-threshold-package/
  f17_512_high_agreement_threshold_certificate.json
```

Regenerate or check it with:

```sh
python3 experimental/scripts/verify_hankel_smoke_f17_506_507.py \
  --write experimental/data/certificates/hankel-smoke-f17-506-507/f17_32_hankel_smoke_506_507_packet.json

python3 experimental/scripts/verify_hankel_smoke_f17_506_507.py \
  --check experimental/data/certificates/hankel-smoke-f17-506-507/f17_32_hankel_smoke_506_507_packet.json

python3 scripts/check_aperiodic_eliminant_packet.py \
  experimental/data/certificates/hankel-smoke-f17-506-507/f17_32_hankel_smoke_506_507_packet.json
```

This is a format smoke test, not new mathematics.  It records the known
high-agreement tangent numerators

```text
A=506: numerator 7, unsafe
A=507: numerator 6, safe
```

as removed ledgers, then declares the residual aperiodic bucket empty for the
packet.
