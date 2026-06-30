# F17^32 High-Agreement Tangent Table

This directory contains a checked ledger table for the theorem-backed
high-agreement range

```text
RS[F_17^32,H,256], |H|=512, 427 <= A <= 512.
```

The proof input is the existing high-agreement threshold package: in this range
`LD_sw(C,A)=n-A+1`.  The table rewrites that theorem into the `towards-prize.md`
ledger columns:

```text
B_tan
B_quot_support
B_quot_image
B_ap_regular
B_ap_pivot
B_ext
deduped_total_upper_bound
known_lower_bound
```

Since the tangent/common-code-line ledger pays the exact total numerator in the
high-agreement range, all quotient, aperiodic, and extension residual columns
are zero after tangent removal.

Run:

```sh
python3 experimental/scripts/verify_f17_32_high_agreement_tangent_table.py \
  --check experimental/data/certificates/hankel-f17-32-high-agreement-tangent-table/f17_32_n512_k256_a427_512_high_agreement_tangent_table.json
```

Non-claims: this does not cover `A < 427`, does not prove the M3
regular-window safe side, does not provide singular-pivot packets, and does not
replace the aperiodic local-limit problem.
