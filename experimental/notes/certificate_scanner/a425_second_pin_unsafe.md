# E23 A=425 Second-Pin Unsafe Fallback

Status: CERTIFIED_UNSAFE_FALLBACK / EXACT_A425_UPPER_OPEN.

This note records the E23 fallback packet for the row

```text
C = RS[F_p,D,256],  |D|=512,  p=22275*2^120+1.
```

The script

```sh
python3 experimental/scripts/verify_a425_second_pin_unsafe.py --check
```

checks that `p` is prime by the recorded Lucas witness, that the committed
domain generator has order `512`, and that

```text
floor((p-1)/2^128) = 87.
```

## Certified Unsafe Side

At agreement `A=425`, choose a core of `424` domain coordinates.  Define a
received line by coordinate values: `f=g=0` on the core; on the remaining
coordinates indexed by `i=0,...,87`, set `g=1` and `f=-i`.

For slope `z=i`, the line word `f+z g` vanishes on the core plus the `i`th
outside coordinate, so it is explained there by the zero codeword on a support
of size `425`.  On that same support, `g` has `424` zeros and one nonzero value.
No degree-`<256` polynomial can agree with `g` there, since it would have more
than `255` zeros and also a nonzero value.  Hence each of the `88` slopes is
support-wise noncontained.

Therefore

```text
LD_sw(RS[F_p,D,256],425) >= 88 > 87 = floor((p-1)/2^128).
```

This proves the E23 unsafe-side decision at the budget-prime row.

## Exact Attempt Audit

The same direct two-core arithmetic that closes the adjacent `A=426` row does
not close the `A=425` exact upper bound by itself.

For `A=425`, the complement size is `87`, and the large-pair threshold is

```text
n+k-A = 343.
```

If a pair of supports has intersection at least `343`, the residual budget
branch gives

```text
max_{343 <= c <= 512} floor((512-c)/max(1,425-c)) = 88,
```

attained at `c=424`.

If no pair has intersection `343`, then support intersections are at most
`342`.  The complements are `87`-sets with pairwise intersection at most `4`,
so the elementary packing count only gives

```text
M <= floor(binomial(512,5)/binomial(87,5)) = 7781.
```

That is why this packet is marked as the certified-witness fallback rather
than an exact computation of `LD_sw(C,425)`.

## Artifact

- Certificate:
  `experimental/data/certificates/a425-second-pin-unsafe/a425_second_pin_unsafe.json`
- Verifier:
  `experimental/scripts/verify_a425_second_pin_unsafe.py`
