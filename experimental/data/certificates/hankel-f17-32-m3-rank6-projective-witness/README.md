# F17^32 M3 Rank-6 Projective Witness

Status: PROVED / AUDIT for this synthetic family.

This packet gives a Hankel-realizable rank-6 projective-infinity witness in the
regular M3 window for

```text
C = RS[F_17^32,H,256],    |H| = 512.
```

It applies on the subwindow

```text
388 <= A <= 426.
```

For each agreement, put `j=512-A` and use the prefix base support
`X_A={x_0,...,x_j}` with unit weights.  The direction syndrome uses the next
six domain nodes

```text
Y_A={x_{j+1},...,x_{j+6}}.
```

Then `rank H(v)=6`.  Every finite slope has full column rank, so the v10
canonical finite root table is empty.  At projective infinity, the locator
whose roots are all six direction nodes and the first `j-6` base nodes divides
`X^512-1`, satisfies `H(v)ell=0`, and has `H(u)ell!=0` by a 7x7 Vandermonde
argument on the surviving base nodes.

This proves that a genuine support-wise endpoint can occur in a
Hankel-realizable rank-6 direction family.  It does not prove simultaneous
rank-6 finite sharpness and endpoint sharpness, and it makes no claim for
`A=385..387`.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_projective_witness.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-projective-witness/f17_32_n512_k256_m3_rank6_projective_witness.json
```
