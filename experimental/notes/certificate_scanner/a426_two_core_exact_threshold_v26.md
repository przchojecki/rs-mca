# A=426 two-core exact threshold v26

## Claim

For every finite field `F`, every distinct domain `D` with `|D|=512`, and

```text
C = RS[F,D,256],
```

the finite-slope support-wise line-decoding numerator satisfies

```text
LD_sw(C,426) = 87.
```

For the prime-field row

```text
p = 22275*2^120 + 1
  = 29608553606109001068932302267744675430401,
H <= F_p^*  with |H| = 512,
C = RS[F_p,H,256],
```

the existing moving-root tangent floor gives matching lower bounds:

```text
LD_sw(C,426) = 87,
LD_sw(C,425) >= 88.
```

Since

```text
87*2^128 < p < 88*2^128,
floor((p - 1) / 2^128) = 87,
```

this pins the adjacent finite-slope support-wise MCA threshold:

```text
safe:        A >= 426, closed radius <= 86/512 = 43/256,
first unsafe: A = 425, closed radius = 87/512.
```

## Status

`PROVED_ADJACENT_THRESHOLD_ROW` for the finite-slope support-wise MCA / `LD_sw`
object over the emitted prime field.

This is a Hankel-free structural packet. The new work is the two-core upper
bound at `A=426`; the exact-support reduction, `eps_mca = LD_sw/q_line` bridge,
and tangent lower floor are already repo results and are consumed as inputs.

## Parameters

```text
n = 512
k = 256
rho = 1/2
A_safe = 426
A_unsafe = 425
delta_safe = 43/256
delta_unsafe = 87/512
q_gen = q_line = p
q_chal = not protocol-bound
```

The prime certificate is Lucas:

```text
p - 1 = 2^120 * 3^4 * 5^2 * 11,
witness = 13.
```

Because `p == 1 mod 512`, the field contains an order-512 multiplicative
subgroup.

## What is new

The current repo already has:

- the M2 bridge `eps_mca(C,delta)=LD_sw(C,ceil((1-delta)n))/q_line`;
- exact-support reduction for Reed-Solomon when `A >= k+1`;
- the moving-root tangent floor `LD_sw(C,A) >= n-A+1`;
- high-agreement exact tangent rows beginning at `A >= 427`.

This packet adds the missing adjacent endpoint just below that tangent-exact
range:

```text
LD_sw(C,426) = 87 = n+1-426.
```

## Retained A=426 table after v26 two-core coverage

These are retained ledger contributions after the global two-core coverage
bound. The non-tangent rows are not separately proved empty; they are not
separately retained once the full support-wise bad-slope set is bounded by 87.

| component | retained count | terminal status |
|---|---:|---|
| `B_tan(426)` | 87 | tangent moving-root witness complete |
| `B_quot_support(426)` | 0 | globally absorbed by two-core envelope |
| `B_quot_image(426)` | 0 | globally absorbed by two-core envelope |
| `B_ext(426)` | 0 | globally absorbed by two-core envelope |
| `B_ap_regular(426)` | 0 | globally absorbed by two-core envelope |
| `B_ap_pivot(426)` | 0 | globally absorbed by two-core envelope |
| `deduped_total(426)` | 87 | exactly the budget floor |

## Proof sketch

By the repo's exact-support reduction, restrict to exact witness supports
`|S_z|=426`.

Let `Z` be the set of support-wise noncontained bad slopes for a fixed received
line. For each `z in Z`, choose one exact witness support `S_z`.

If every pair satisfies `|S_z cap S_w| <= 341`, then the complements
`T_z = D \ S_z` have size `86` and pairwise intersection at most `1`.
Their two-subsets are disjoint, so

```text
|Z| * binom(86,2) <= binom(512,2),
|Z| <= 35.
```

Otherwise, two supports overlap in at least `342` points. This overlap is
larger than `k=256`, so the two explaining codewords determine a common
degree-`<256` code-line `(c_f,c_g)`. Let `C0` be the full common support where
`f=c_f` and `g=c_g`, with `c=|C0| >= 342`.

For any other bad slope, subtracting the common code-line leaves a degree-`<256`
residual codeword with at least

```text
426 + c - 512 >= 256
```

zeros. Hence the residual codeword is zero. The existing common-code-line
residual budget gives

```text
|Z| <= floor((512-c)/max(1,426-c)) <= 87,
```

with equality only at `c=425`.

The direct tangent lower witness with a common zero core of size `425` and one
moving outside coordinate for each slope gives `87` slopes at `A=426`. The
matching direct `A=425` witness uses core size `424` and gives `88` slopes.
Since `LD_sw(C,a)` is nonincreasing in `a`, every `A>=426` is safe over the
emitted prime, and `A=425` is the first unsafe closed-grid point.

## Replay

```bash
python3 experimental/scripts/certify_a426_two_core_exact_threshold_v26.py --check
```

Expected output ends with:

```text
STATUS: PROVED_ADJACENT_THRESHOLD_ROW
LD_sw_upper_A426: 87
LD_sw_lower_A426: 87
budget_floor: 87
first_unsafe_A425_tangent_floor: 88
RESULT: PASS_ADJACENT_THRESHOLD_ROW_CANDIDATE
```

## Non-claims

This does not close the live `F_17^32` A=426 row: that denominator has budget
floor `6`, while the exact numerator here is `87`.

This does not claim ordinary list decoding, interleaved-list safety, protocol
query soundness, BETA_2, or full M1 local-limit closure.
