# A=425 Second-Pin Unsafe Certificate

Status: CERTIFIED_UNSAFE_FALLBACK / EXACT_A425_UPPER_OPEN.

This directory contains the deterministic E23 certificate for the unsafe side
of the adjacent `A=426` budget-prime row.  It verifies the prime

```text
p = 22275*2^120 + 1
```

and records

```text
floor((p-1)/2^128) = 87.
```

For `RS[F_p,D,256]` with `|D|=512`, the certificate gives an explicit
support-wise line with `88` bad finite slopes at agreement `A=425`.  Therefore
`LD_sw(RS[F_p,D,256],425) > 87`, which is the E23 unsafe-side decision needed
at this row.

Generate and check it from the repository root:

```sh
python3 experimental/scripts/verify_a425_second_pin_unsafe.py --write
python3 experimental/scripts/verify_a425_second_pin_unsafe.py --check
```

The JSON also records the direct two-core exact-attempt arithmetic at `A=425`.
The large-core branch gives the matching bound `88`, but the low-pair packing
branch only gives

```text
floor(binomial(512,5)/binomial(87,5)) = 7781.
```

Thus this packet certifies the fallback unsafe verdict, but deliberately does
not claim `LD_sw(C,425)=88`.
