# F17^32 M3 Rank-6 A385 Two-Core Conic Product Collapse

Status: PROVED / AUDIT.

This packet verifies the product-collapse refinement for the separated
`A=385` rank-6 fixed two-core irreducible-conic high-core branch.

It depends on the row descriptor, the rank-6 low-degree transfer packet, the
A385 two-core high-core quotient normal form, and the null-polynomial
split-locator gate.  In the conic branch, a high forced external core is global
on the residual `Q`-plane.  Writing `G=q_0 P_X+H`, comparison of the remainders
of `G`, `T G`, and `T^2 G` at one global forced external point forces the top
two coefficients of `H` to vanish.  Therefore `L_{E R}=H R` with `deg H<=125`.

The product `H R` has the two fixed base roots, the global forced external
core, and at most two further subgroup roots from `R`.  Hence `e_G<=122` cannot
pass the degree-`127` split-locator gate, while `e_G>=124` is impossible for a
nonzero `H` of degree at most `125` with the two fixed base roots.  The packet
leaves exactly the irreducible-conic quotient tail `e_G=123`.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a385_two_core_conic_product_collapse.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a385-two-core-conic-product-collapse/f17_32_n512_k256_m3_rank6_a385_two_core_conic_product_collapse.json
```
