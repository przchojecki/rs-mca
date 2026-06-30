# F17^32 M3 Extension-Denominator Audit

This directory contains an F1-style denominator audit for the synthetic
top-window line-value packet

```text
RS[F_17^32,H,256], |H|=512, 421 <= A <= 426.
```

The audit checks that the packet is genuinely `F_17^32`-valued: `f` is the
zero vector, but every value of `g` lies outside the base field `F_17` under the
repository's polynomial-basis encoding.  Therefore finite affine slopes are
sampled from `F_17^32`, and the denominator for the MCA numerator is
`q_line=17^32`, not `17`.

Run:

```sh
python3 experimental/scripts/verify_f17_32_m3_extension_denominator_audit.py \
  --check experimental/data/certificates/hankel-f17-32-m3-extension-denominator-audit/f17_32_n512_k256_a421_426_extension_denominator_audit.json
```

Non-claims: this is not an extension-line lift theorem, not a base-field MCA
packet, not actual M3 row data, not a Prime192 denominator audit, and not a
safe-side MCA bound.
