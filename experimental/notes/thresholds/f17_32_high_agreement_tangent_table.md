# F17^32 high-agreement tangent table

Status: **PROVED / AUDIT**.

This note records a compact item-5 ledger table for the already solved
high-agreement range of

```text
C = RS[F_17^32,H,256], |H|=512.
```

The proof input is the high-agreement tangent staircase packaged in

```text
experimental/data/certificates/high-agreement-threshold-package/
  f17_512_high_agreement_threshold_certificate.json
```

It proves

```text
LD_sw(C,A) = n-A+1
```

whenever

```text
n-A <= floor((n-k)/3).
```

For `n=512`, `k=256`, this is exactly the range `427 <= A <= 512`.

The checked table is

```text
experimental/data/certificates/hankel-f17-32-high-agreement-tangent-table/
  f17_32_n512_k256_a427_512_high_agreement_tangent_table.json
```

For every `A=427..512`, it records:

```text
B_tan = n-A+1
B_quot_support = B_quot_image = 0
B_ap_regular = B_ap_pivot = 0
B_ext = 0
deduped_total_upper_bound = known_lower_bound = n-A+1
```

The denominator is `q_line=17^32`, so the `2^-128` budget is `6`.  Therefore:

```text
A = 427..506: unsafe by proved lower bound
A = 507..512: safe by proved upper bound
```

Equivalently, the largest safe closed integer radius is `5`, the first unsafe
integer radius is `6`, and the real safe interval is `[0,6/512)`.

This table is deliberately not an M3 regular-window result.  It closes the
high-agreement ledger columns and gives a template for the lower-agreement M4
table, where the missing work is still actual v9 root counts, quotient/tangent
deduplication, and singular-pivot packets.

Reproduce:

```sh
python3 experimental/scripts/verify_f17_32_high_agreement_tangent_table.py \
  --check experimental/data/certificates/hankel-f17-32-high-agreement-tangent-table/f17_32_n512_k256_a427_512_high_agreement_tangent_table.json
```
