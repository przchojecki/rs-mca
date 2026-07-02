# F17^32 M3 Rank-6 A385 Three-Core Residual Closure

Status: PROVED / AUDIT.

This packet closes the ratio-identically-consistent fixed three-core residual
line left by the A385 three-core quadratic-cut packet.

The proof uses three pieces.  First, the line-incidence count is
projective-budget safe through `e_G<=70`.  Second, a global forced external root
on the residual line forces the top coefficient of the common factor `H` to
vanish, so `L_{E R}=H R`; the product root count excludes `71<=e_G<=122`.
Third, the punctured projective tangent tail is budget-safe for `e_G>=122`.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_three_core_residual_closure.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-three-core-residual-closure/f17_32_n512_k256_m3_rank6_a385_three_core_residual_closure.json
```
