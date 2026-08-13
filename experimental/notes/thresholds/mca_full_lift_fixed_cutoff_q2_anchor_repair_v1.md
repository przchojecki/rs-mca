# MCA full-lift fixed-cutoff q2 anchor repair v1

## Status

PROVED / EXACT FINITE CALIBRATION / SUPPORT PAYMENT.

## Endpoint

At Mersenne-31 support `e=101156`,

```text
(s,q,H)=(33716,2,67439),
cutoff=65258,
F=16895280,
D1=284224,
D2=258385.
```

Here `F` is the fixed-cutoff prefix plus every coarse boundary-class charge,
and `D1,D2` are the charges of exact deficits `H,H-1`. The residue identity

```text
e-2s-(s+2)=K
```

allows two top anchors to synchronize both boundary layers.

## Five cases

If the top union has at least two members, remove `D1,D2` from `F`.
Unsafety would force `424545` members on the resulting line, hence common
core `67452=m-2`. Core absorption then gives

```text
101156*28+981129=3813497.
```

With exactly one top member, two first-boundary members synchronize that
layer; its outside agreement `15` gives line cap `94742`. With no top
member, an intersecting pair of first-boundary missed sets synchronizes the
layer, while the alternative pairwise-disjoint family has size at most
`floor(101156/33717)=3`.

The five exhaustive charges are

```text
3813497, 16705799, 16611058, 16705798, 16611059.
```

Their maximum is below budget by `71416`. Thus `e=101156` is safe.

## Scope

At adjacent `e=101157`, the residue resets to zero. This theorem neither
applies there nor supplies an unsafe certificate. The residual interval is
`101157<=e<=1044241`.

## Replay

```bash
python3 experimental/verify_mca_full_lift_fixed_cutoff_q2_anchor_repair_v1.py
python3 experimental/audit_mca_full_lift_fixed_cutoff_q2_anchor_repair_v1.py
```

The primary verifier reconstructs all `65,258` prefix caps, all `2,181`
boundary charges, the unsafe-core threshold, and all five cases. The audit
recomputes the endpoint constants without importing the primary verifier.
