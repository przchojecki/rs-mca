# M1 A407/A408 residual-design threshold v1

Status: `PROVED_A407_A408_EXACT_AND_A407_PUBLIC_GATE`.

This packet proves the two exact rows reached by the A409 saturated-triple/high-neighbor/moment method and uses A407 as an exact-budget public threshold row. It deliberately stops at A406, where this exact method fails.

## Main theorem

```text
For every finite field F and every distinct 512-point RS domain D,
LD_sw(RS[F,D,256],408) = 105,
LD_sw(RS[F,D,256],407) = 106.
```

The matching lower bounds are the moving-root tangent witnesses recorded in the witness JSON. The upper bounds are certified by the residual-design sweep below.

## Imported proof dependencies

The proof note states proof sketches for these repo-standard RS/MDS reductions:

1. Exact-support reduction for support-wise noncontained finite-slope witnesses when `A >= k+1`, after contained/common-code-line branches are separated.
2. Per-support uniqueness for noncontained finite slopes.
3. Moving-root tangent lower witness `LD_sw >= n-A+1`.
4. RS uniqueness from `k` common coordinates in compact triples and common-code-line branches.

## Public threshold row

```text
p = 27168*2^120+1
  = 36112466189484594435050630213696401440769
p - 1 = 2^125 * 3 * 283
Lucas/primitive-root witness = 11
floor((p-1)/2^128) = 106
106*2^128 < p < 107*2^128
p == 1 mod 512
```

Therefore for `C = RS[F_p,H,256]`, with `H` the order-512 subgroup:

```text
A=407: LD_sw(C,407)=106, safe at delta=105/512.
A=406: LD_sw(C,406)>=107, unsafe at delta=53/256.
```

This pins the closed-grid finite-slope support-wise MCA gate between A=406 and A=407 for this prime row.

## Residual-design rows

| A | j | exact LD_sw | no-paid residual bound | first forbidden m |
|---:|---:|---:|---:|---:|
| 408 | 104 | 105 | 50 | 51 |
| 407 | 105 | 106 | 93 | 94 |

## First failure of this method

```text
A=406, j=106
pair_trigger=62
pair_cap=61
compact_T_paid_cap=150
status=FAIL_HIGH_NEIGHBOR_DEGREE_BOUND
reason=The inclusion-exclusion degree argument gives no finite high-neighbor bound.
```

So this is not an A406 exact theorem and not an M1 closure. The A406 unsafe side used for the public gate is only the tangent lower witness `LD_sw >= 107`.

## Third-moment minimizer certificate

For fixed family size `m`, the coordinate-degree kernel is

```text
phi_m(d) = binom(d,2)(m-d) + 2 binom(d,3).
```

The verifier records the identity

```text
phi_m(d+2) - 2 phi_m(d+1) + phi_m(d) = m-d-2 >= 0
```

for `0 <= d <= m-2`, so the standard exchange argument makes the balanced degree vector the minimum at fixed total degree.

## Validation

```bash
python3 -m py_compile experimental/scripts/certify_m1_a407_a408_residual_design_threshold_v1.py
python3 -m py_compile experimental/scripts/apply_m1_a407_a408_site_entries_v1.py
python3 experimental/scripts/certify_m1_a407_a408_residual_design_threshold_v1.py --check
python3 experimental/scripts/certify_m1_a407_a408_residual_design_threshold_v1.py --json
python3 -m json.tool experimental/data/certificates/m1-a407-a408-residual-design-threshold-v1/m1_a407_a408_residual_design_threshold_v1.json
python3 -m json.tool experimental/data/certificates/m1-a407-a408-residual-design-threshold-v1/tangent_witness_A408_A407_A406_v1.json
python3 -m json.tool site/data/frontier_prime_a406_a407_adjacent_gate.entry.json
python3 -m json.tool site/data/updates_m1_a407_a408_residual_design_threshold.entry.json
git diff --check
```

## Non-claims

- Finite-slope support-wise MCA / LD_sw only.
- Not ordinary list decoding.
- Not interleaved-list safety.
- Not protocol soundness or query accounting.
- Not an exact A406 upper bound.
- Not a full M1 closure.
- Does not use the false global RNC Fano-line classification.
