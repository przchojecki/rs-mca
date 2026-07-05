# Axis 9 Exact-Rate Dither Reading

- **Status:** PROVED / citation check.
- **DAG node:** `axis9_dither`.
- **Certificate:** `experimental/data/certificates/axis9-dither/axis9_dither.json`.
- **Verifier:** `python3 experimental/scripts/verify_axis9_dither.py --check experimental/data/certificates/axis9-dither/axis9_dither.json`.

This packet resolves the S0 axis-9 dither question.  The official rate set is
exact:

```text
rho in {1/2, 1/4, 1/8, 1/16}
```

Therefore dimension dither is not a built-in escape hatch from the maximal
dyadic quotient structure of the exact-rate rows.  Dithered dimensions can
still be useful experiments or protocol variants, but they are not the official
rows unless explicitly declared as such.

## Statement

For the official smooth multiplicative prize box, the rate is one of the four
listed constants.  The proof program must therefore price the quotient structure
at exact dyadic rates rather than assuming freedom to replace `k = rho n` by
`rho n - r` to suppress active quotient scales.

## Citation Pin

The certificate pins ABF26 / IACR ePrint 2026/680, page 5, with PDF sha256:

```text
426a979c13cc61db0f2cdb909067ef4c9f24438859fe0a7a337d2b19b07fcaa5
```

The checked fragments are:

```text
rho(C) := k/|L|
one of 1/2, 1/4, 1/8, 1/16
```

Those fragments make the official rate axis discrete.  A dithered row needs a
separate protocol or maintainer declaration; it is not silently available in
the printed challenge box.

## Consequence

Quotient-profile and exact-count packets should treat exact dyadic rates as
load-bearing:

```text
official row:        k = rho n with rho in the listed set
dithered variant:    experimental/protocol-specific unless separately declared
proof obligation:    price dyadic quotient cores rather than ignore them
```

## Non-Claims

- This packet does not prove dithered rows are useless.
- This packet does not forbid studying dither as a protocol-design option.
- This packet does not change any quotient-profile count; it fixes which rows
  the official proof must price.
