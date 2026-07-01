# F17^32 M3 One-Spike Canonical Empty Root Table

Status: PROVED.

This directory records an all-window canonical finite-root closure for the
non-proportional one-spike family in the M3 regular window

```text
385 <= A <= 426.
```

For each exact agreement, write `s=j+1`.  Let `X_A` be the first `s`
descriptor-domain elements and let `y_A` be the next descriptor-domain element.
The synthetic syndrome pencil is

```text
u_m = sum_{x in X_A} x^m,
v_m = y_A^m.
```

The selected prefix minor can vanish at one finite slope; the A=426 packet in
`hankel-f17-32-m3-one-spike-a426/` records that selected-minor root.  This
certificate proves the stronger v10 canonical statement: the full
overdetermined Hankel matrix has rank `j+1` for every finite slope, even after
scalar extension.  Therefore the canonical regular gcd is constant and has no
finite roots.

For `z=0`, the base support `X_A` has size `j+1` and gives invertible
Vandermonde factors.  For `z!=0`, the support `X_A union {y_A}` has size
`j+2`; since `t>=j+2` throughout the M3 window, the row Vandermonde is
injective and the column Vandermonde has rank `j+1`.

At projective infinity, `H(v)` has rank one while `H(u)` has full column rank.
Thus the M5 kernel chart gives the one-point `dimension_degree` fallback for
`[0:1]`.  The packet does not claim split-locator nonemptiness at infinity.
That nonemptiness is proved separately in:

```text
experimental/data/certificates/hankel-f17-32-m3-one-spike-projective-witness/
```

Regenerate and check:

```sh
python3 experimental/scripts/verify_f17_32_m3_one_spike_canonical_empty.py \
  --write experimental/data/certificates/hankel-f17-32-m3-one-spike-canonical-empty/f17_32_n512_k256_m3_one_spike_canonical_empty.json

python3 experimental/scripts/verify_f17_32_m3_one_spike_canonical_empty.py \
  --check experimental/data/certificates/hankel-f17-32-m3-one-spike-canonical-empty/f17_32_n512_k256_m3_one_spike_canonical_empty.json
```
