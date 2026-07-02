# F17^32 M3 Rank-6 A385 Two-Core High-Core Quotient

Status: PROVED / AUDIT.

This packet records the high-core quotient normal form for the fixed two-core
moving-slope residual at `A=385`.

Conclusion:

```text
line high-core branch:              quotient pencil degree <= 56;
irreducible-conic high-core branch: quotient family degree <= 59.
```

The packet is a quotient normal form, not a product-collapse or paid-ledger
closure.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_two_core_high_core_quotient.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-two-core-high-core-quotient/f17_32_n512_k256_m3_rank6_a385_two_core_high_core_quotient.json
```

Nonclaims:

```text
does not prove product collapse for A=385 high-core line or conic components;
does not claim the high-core quotient pencils or families are empty or paid;
does not close moving-core or no-common-core A=385 branches;
does not classify overlapping-support rank-6 pencils;
does not prove endpoint payment;
does not produce a row-level M3 safe-side bound.
```
