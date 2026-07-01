# Subgroup Syndrome Section

Status: PROVED / AUDIT.

This packet proves the reusable line-value section for the pinned
`F_17^32` M3 row.  Let `H` be the order-512 subgroup from the row descriptor
and define the weighted syndrome map

```text
Syn(y)_m = (1/|H|) sum_{x in H} x*y(x)*x^m,    0 <= m < 256.
```

For any syndrome vector `s=(s_0,...,s_255)`, set

```text
y_s(x) = sum_{a=0}^{255} s_a x^(-a-1).
```

Then `Syn(y_s)_m=s_m` for every `m`.  The proof is the character-orthogonality
identity

```text
sum_{x in H} x^e = 0    for 0 < |e| < 256,
sum_{x in H} 1   = 512.
```

The verifier checks the pinned generator, the character sums over the required
exponent range, and all `256*256` coordinate-basis section identities.

Regenerate and check:

```sh
python3 experimental/scripts/verify_m1_subgroup_syndrome_section.py \
  --write experimental/data/certificates/subgroup-syndrome-section/subgroup_syndrome_section_certificate.json

python3 experimental/scripts/verify_m1_subgroup_syndrome_section.py \
  --check experimental/data/certificates/subgroup-syndrome-section/subgroup_syndrome_section_certificate.json
```
