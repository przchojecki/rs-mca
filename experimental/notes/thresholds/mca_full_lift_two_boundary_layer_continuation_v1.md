# MCA full-lift two-boundary-layer continuation v1

## Status

PROVED / EXACT FINITE CALIBRATION.

## Statement

Retain the one-boundary notation

```text
s=floor((e-K)/3), q=e-K-3s, H=e-s-1.
```

Assume `q=2`, `H>=3`, `2(s+2)<e`, `m-H>K-1`, and the parent prefix
hypotheses through `H`. Put

```text
Q=floor((N-e-(K-1))/(m-H-(K-1))),
D=floor(e/(s+1)).
```

Then

```text
|Z| <= max{
  P_(H-2)+(N-m+1),
  P_(H-1)+Q+1,
  P_(H-1)+2,
  P_(H-1)+Q,
  P_(H-1)+D
}.
```

## Proof mechanism

If the top-third union has at least two members, two anchors synchronize
both boundary layers because the worst mixed triple intersection is
`e-s-s-(s+2)=K`. If it has one member, two first-boundary members synchronize
that layer; the top member is charged separately and the boundary line uses
the sharper outside-core cap `Q`.

If the top union is empty, choose exact size-`H` inside agreement sets for
the first boundary layer. If two missed sets intersect, that one repeated
miss raises every fixed-pair triple intersection from `K-1` to `K`, so the
whole layer is an outside-core line. Otherwise all missed sets are pairwise
disjoint and there are at most `D` of them.

## Official endpoint

At Mersenne-31 `e=98231`,

```text
P_(H-2) = 15505282,
P_(H-1) = 16433719,
N-m+1   =   981129,
Q       =      484,
D       =        3.
```

The five cases are

```text
16486411, 16434204, 16433721, 16434203, 16433722.
```

Their maximum has slack `290804` below budget `16777215`. At `e=98232`,
the residue is `q=0`, so this theorem stops without making an unsafe claim.
The Mersenne full-lift residual interval is `98232<=e<=1044241`.

## Replay

```bash
python3 experimental/verify_mca_full_lift_two_boundary_layer_continuation_v1.py
python3 -O experimental/verify_mca_full_lift_two_boundary_layer_continuation_v1.py
```
