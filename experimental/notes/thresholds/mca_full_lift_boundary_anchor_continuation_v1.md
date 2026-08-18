# MCA full-lift boundary-anchor continuation v1

## Status

PROVED / EXACT FINITE CALIBRATION.

## Statement

Retain the full-lift mean-centered prefix caps and put

```text
s=floor((e-K)/3), q=e-K-3s, H=e-s-1.
```

Let `P_J` be the suffix-minimum Abel profile formed independently from the
cumulative caps through `J`. If `H>=2`, `q>=1`, `2(s+1)<e`, and the parent
prefix hypotheses hold through `H`, then

```text
|Z| <= max(P_H+1, P_(H-1)+(N-m+1)).
```

## Proof mechanism

Split on the size of the already-synchronized top-third union `A`. If it
has at most one explanation, charge the full prefix and one tail slope. If
it has at least two, use two members as anchors. Every exact boundary-layer
explanation has a mixed triple intersection of size

```text
e-s-s-(s+1)=K+q-1>=K,
```

so restriction injectivity places it on the same affine codeword line.
The total-core line theorem then charges the high union and boundary layer
together by `N-m+1`, leaving the prefix only through `H-1`.

## Official endpoint

At Mersenne-31 `e=98230`,

```text
P_H       = 16434744,
P_(H-1)   = 15506184,
N-m+1     =   981129,
bound     = 16487313,
budget    = 16777215,
slack     =   289902.
```

At `e=98231`, the same theorem gives `17492173`, over budget by `714958`.
That is a proof-method wall, not an unsafe certificate. The Mersenne
full-lift residual interval is now `98231<=e<=1044241`.

## Replay

```bash
python3 experimental/verify_mca_full_lift_boundary_anchor_continuation_v1.py
python3 -O experimental/verify_mca_full_lift_boundary_anchor_continuation_v1.py
```
