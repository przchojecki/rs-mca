# High-Agreement Threshold Package

Status: PROVED-COMPILER-ARITHMETIC / AUDIT.

This note records the certificate object used to package the current
high-agreement finite-row threshold and the row-independent compiler requested
in `towards-prize.md`. It does not reprove the tangent staircase. Its proof
input is the promoted theorem

```text
LD_sw(C,a)=r+1=n-a+1 when r=n-a <= floor((n-k)/3).
```

The script

```text
python3 experimental/scripts/certify_high_agreement_threshold_package.py
```

checks the exact integer arithmetic that turns this theorem into a prize-facing
threshold certificate.

## Definition Freeze

The certificate uses the following conventions.

```text
object:                 finite-slope support-wise MCA / LD_sw
agreement:              a = n - r
closed integer radius:  r = n - a
closed real radius:     r(delta) = floor(delta n)
affine denominator:     q_line = |F|
projective denominator: |P^1(F)| = |F| + 1
target:                 2^-128
```

The endpoint convention is closed-ball: if the first unsafe integer radius is
`r0`, then the real safe interval is `[0,r0/n)`. The supremum `r0/n` is not
attained.

The local M2 bridge used here is the exact finite-length identity from
`experimental/notes/m2/m2_line_decoding_mca_bridge.md`:

```text
epsilon_mca(C,delta) = LD_sw(C,ceil((1-delta)n)) / |F|.
```

For closed grid radii this agrees with the convention above, since

```text
ceil((1-delta)n) = n - floor(delta n).
```

The certificate checks this equality at the safe endpoint `delta=5/512` and
the first unsafe endpoint `delta=6/512`.

## Finite Row

For

```text
C = RS[F_17^32,H,256],   n = 512,
```

the certificate verifies

```text
floor(17^32 / 2^128) = 6,
6 * 2^128 < 17^32 < 7 * 2^128,
floor((512-256)/3) = 85,
ceil((2*512+256)/3) = 427.
```

The exact tangent range therefore contains the threshold row, and the pure
finite-slope support-wise MCA verdict is

```text
a = 506, r = 6: LD_sw = 7, unsafe;
a = 507, r = 5: LD_sw = 6, safe.
```

Equivalently, by the exact M2 bridge,

```text
epsilon_mca(C,5/512) = 6 / 17^32 <= 2^-128,
epsilon_mca(C,6/512) = 7 / 17^32 >  2^-128.
```

Thus the largest safe integer radius is `5/512`, the first unsafe integer
radius is `6/512`, and the closed real safe interval is

```text
[0, 6/512) = [0, 3/256).
```

The projective-slope denominator has the same integer budget because

```text
floor((17^32 + 1) / 2^128) = 6.
```

So the projective-line version has the same `5/6` integer-radius transition,
with denominator `|F|+1`.

## Row-Independent Compiler

For a single theorem-backed line/MCA/CA numerator, define

```text
B_Q = floor(Q / 2^128).
```

There are three integer-budget regimes.

```text
B_Q = 0:
  no integer radius is safe; even r=0 has numerator 1.

1 <= B_Q <= floor((n-k)/3):
  the threshold is pinned:
  r <= B_Q - 1  is safe,
  r =  B_Q      is unsafe.

B_Q > floor((n-k)/3):
  the exact tangent theorem proves safety throughout the high-agreement
  range r <= floor((n-k)/3), but it does not locate the later threshold.
```

The threshold-pinning regime is therefore exactly

```text
1 <= B_Q <= floor((n-k)/3)
```

Equivalently, for a rate `rho=1/d` prize row with `n=dk`, the exact
single-line threshold is pinned precisely when

```text
2^128 <= Q <= 2^128 * (floor((d-1)k/3) + 1) - 1.
```

When `floor((d-1)k/3)>0`, for power-of-two denominators `Q=2^lambda` the
largest pinned bit-size is

```text
lambda_max = 128 + floor(log2(floor((d-1)k/3))).
```

At the maximal prize dimension `k=2^40`, this gives:

```text
rho=1/2:  lambda_max = 166
rho=1/4:  lambda_max = 168
rho=1/8:  lambda_max = 169
rho=1/16: lambda_max = 170
```

Above those power-of-two sizes, the tangent theorem still proves safety through
its exact high-agreement range, but the later threshold belongs to the
lower-agreement quotient/local-limit program.

This is only the single-line/MCA/CA compiler. If a protocol consumes an extra
same-denominator list term, curve term, query term, folding term, or crypto
term, that term must be added in its own ledger.

## Reproduction

Generate and check the committed certificate with:

```text
python3 experimental/scripts/certify_high_agreement_threshold_package.py \
  --write experimental/data/certificates/high-agreement-threshold-package/f17_512_high_agreement_threshold_certificate.json

python3 experimental/scripts/certify_high_agreement_threshold_package.py \
  --check experimental/data/certificates/high-agreement-threshold-package/f17_512_high_agreement_threshold_certificate.json
```

The committed JSON is intentionally small and exact-integer based. It is a
certificate for the finite-row/compiler arithmetic, not for lower-agreement M1,
quotient floors, extension-line transfer, or L2.
