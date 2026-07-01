# F17^32 M3/M4 Affine-Pivot GCD Equivalence

Status: PROVED / AUDIT.

This packet connects the affine-pivot compression theorem to the v10 canonical
gcd/root-table object for the M3 regular window.

Let

```text
p_R(z) = det(H_R(u)+z H_R(v))
```

be a nonzero maximal row-set minor.  If `rank H_R(v)<=r`, then the
direction-rank degree cap gives `deg p_R <= r`.  Therefore `p_R` has at most
`r` bad finite pivots.

For the rank-6 boundary over `F_17^32`, every nonzero minor has at least

```text
17^32 - 6
```

good finite pivots.

Choose a good pivot `z_R` for each nonzero row-set minor and let `c_R(w)` be
the local compressed determinant from the affine-pivot compression theorem.
Translate it back to the global slope variable by

```text
ctilde_R(Z) = c_R(Z-z_R).
```

Then

```text
p_R(Z) = p_R(z_R) ctilde_R(Z),    p_R(z_R) != 0.
```

Multiplying each gcd input by a nonzero scalar does not change the monic gcd,
so

```text
gcd_R p_R(Z) = gcd_R ctilde_R(Z)
```

after monic normalization.  Thus the rank-6 finite root table can be computed
from `6 x 6` compressed determinants translated to the global slope variable,
without changing the v10 canonical root set, as long as each nonzero row-set
chart uses a good finite pivot.

Regenerate and check:

```sh
python3 experimental/scripts/verify_m1_hankel_m4_affine_pivot_gcd_equivalence.py \
  --write experimental/data/certificates/hankel-f17-32-m3-m4-affine-pivot-gcd-equivalence/f17_32_n512_k256_m3_m4_affine_pivot_gcd_equivalence.json

python3 experimental/scripts/verify_m1_hankel_m4_affine_pivot_gcd_equivalence.py \
  --check experimental/data/certificates/hankel-f17-32-m3-m4-affine-pivot-gcd-equivalence/f17_32_n512_k256_m3_m4_affine_pivot_gcd_equivalence.json
```
