# A=426 two-core exact threshold v26

**Status:** `PROVED_ADJACENT_THRESHOLD_ROW`.

This is a Hankel-free structural two-core support-wise line-decoding theorem. With the exact-budget prime, it gives an adjacent finite-slope support-wise MCA threshold row.

## Row

- `p = 29608553606109001068932302267744675430401 = 22275*2^120 + 1`, prime by Lucas witness `13` and `p-1=2^120*3^4*5^2*11`.
- `n=512`, `k=256`, `A_safe=426`, `A_unsafe=425`, `rho=1/2`.
- `q_gen=q_line=p`; `q_chal` is not protocol-bound; budget floor `floor((p-1)/2^128)=87`.
- Safe: `LD_sw(C,426) = 87` at closed radius `43/256`.
- First unsafe: direct tangent witness gives `LD_sw(C,425) >= 88` at closed radius `87/512`.

## Retained A=426 decomposition after v26 two-core coverage

| component | retained count | terminal status |
|---|---:|---|
| `B_tan(426)` | 87 | tangent moving-root witness complete |
| `B_quot_support(426)` | 0 | globally absorbed by two-core envelope |
| `B_quot_image(426)` | 0 | globally absorbed by two-core envelope |
| `B_ext(426)` | 0 | globally absorbed by two-core envelope |
| `B_ap_regular(426)` | 0 | globally absorbed by two-core envelope |
| `B_ap_pivot(426)` | 0 | globally absorbed by two-core envelope |
| `deduped_total(426)` | 87 | equals budget floor `87` |

## Proof sketch

Using the existing repo M2 exact-support bridge, restrict to exact supports of size `426`. If all support pairs intersect in at most `341`, complement pair-packing gives at most `35` slopes. Otherwise two supports have overlap at least `342`, determine a common code-line, and the existing common-code-line residual budget bounds the remaining slopes by `floor((512-c)/max(1,426-c)) <= 87`, with equality at `c=425`.

The matching lower witness takes a common zero core of size `425` and one moving outside coordinate for each of `87` slopes.

Monotonicity then makes every `A>=426` safe over this prime, while the direct `A=425` tangent witness gives the first unsafe grid point.

## Replay

```bash
python3 experimental/scripts/certify_a426_two_core_exact_threshold_v26.py --check
```
