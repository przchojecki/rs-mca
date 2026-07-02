# F17^32 M3 Rank-6 A386 Slope-Free Containment

Status: PROVED / AUDIT.

This packet filters the slope-free part of the `A=386` separated rank-6
global-component residual.

In the low-degree transfer, for each direction node `y` write

```text
N_y(Q) = Omega_y Q(y),
D_y(Q) = b_y L_Q(y).
```

The slope-free condition is

```text
N_y(Q)=0 and D_y(Q)=0 for every direction node y.
```

Then the displayed transfer vector satisfies

```text
H(v)L_Q = 0,
H(u)L_Q = 0.
```

Thus at every finite slope it lies in the contained branch and fails the
finite-affine noncontainment gate `H(v)ell != 0`.  At projective infinity it
also fails the endpoint noncontainment gate `H(u)ell != 0`.

So slope-free transfer vectors contribute

```text
finite noncontained slopes:      0
projective endpoint witnesses:  0
```

If another independent vector with `H(v)ell != 0` occurs at the same finite
parameter, that parameter is charged once through the non-slope-free branch.
The slope-free vector is a contained shadow and adds no second count.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a386_slope_free_containment.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a386-slope-free-containment/f17_32_n512_k256_m3_rank6_a386_slope_free_containment.json
```

Nonclaims:

```text
does not close nonconstant moving-slope components;
does not prove existence or nonexistence of another independent noncontained vector at the same finite slope;
does not cover A=385;
does not classify overlapping-support rank-6 pencils;
does not prove endpoint payment.
```
