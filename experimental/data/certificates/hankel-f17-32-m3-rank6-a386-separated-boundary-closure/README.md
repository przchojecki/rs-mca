# F17^32 M3 Rank-6 A386 Separated Boundary Closure

Status: PROVED / AUDIT.

This packet composes the existing `A=386` separated rank-6 boundary packets
into one closure statement.  For arbitrary nonzero weights on separated
supports `|X|=127`, `|Y|=6`, the low-degree transfer gives a projective
`Q`-plane.  The conic-pair and component-cut packets close the Bezout branches;
the global-component slope dichotomy reduces the remaining branch to
constant-slope, slope-free, or moving-slope cases; the slope-free containment
packet removes contained shadows; and the moving-slope split-incidence packet
closes all line and irreducible-conic moving components.

The resulting branch has no live separated-support `A=386` rank-6 residual and
is projective-budget safe:

```text
support-wise projective contribution <= 6.
```

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a386_separated_boundary_closure.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a386-separated-boundary-closure/f17_32_n512_k256_m3_rank6_a386_separated_boundary_closure.json
```

Nonclaims:

```text
does not cover A=385;
does not classify overlapping-support rank-6 pencils;
does not prove endpoint payment;
does not produce a row-level M3 safe-side bound.
```
