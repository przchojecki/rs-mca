# M1 equal-line deck multiplicity ledger

**Status:** PROVED-LOCAL / AUDIT.

**Agent/model:** AllenGrahamHart / Codex.

**Date:** 2026-06-30.

This note isolates the multiplicity part of the equal-line model-entry target.
The packet-sift closure criterion in
`m1_equal_line_packet_sift_closure.md` needs a bound on the projective
`y`-multiplicity of leaves in an endpoint-independent high-overlap star.  The
equal-line geometry reduces that to a cleaner `z`-multiplicity target: outside
charged fibers, the projective map `z -> y` has degree two with an explicit
deck involution.

This is local algebra on `P^1`.  It does not prove global model entry, does
not prove M1, and does not bound the number of bad slopes.

## Projective map

Work over a field of characteristic `p>3`.  Write `z=[Z:T]` and define

```text
y(z) = [T^2 + 3Z^2 : (T-Z)^2].
```

In affine coordinates this is

```text
y = (1+3z^2)/(1-z)^2.
```

For fixed `y=[Y:W]`, the projective fiber equation is

```text
(Y-3W)Z^2 - 2Y ZT + (Y-W)T^2 = 0,                (F)
```

with discriminant

```text
Delta_y = 4W(4Y-3W).                              (D)
```

Thus the branch values are

```text
y = infinity,        y = 3/4.
```

## Deck involution

The map has deck involution

```text
sigma([Z:T]) = [Z+T : 3Z-T].
```

Equivalently, in affine coordinates,

```text
sigma(z) = (z+1)/(3z-1).
```

Then

```text
y(sigma(z)) = y(z),        sigma^2 = id.
```

The fixed points of `sigma` are exactly

```text
z = 1,          z = -1/3,
```

lying over

```text
y = infinity,  y = 3/4.
```

Consequently every nonbranch geometric fiber is a two-point orbit

```text
{z, sigma(z)}.
```

Over the base field, such a fiber either has two base-field points or none,
according as `Delta_y` is a square or nonsquare.  This is the splitting ledger
from `m1_equal_line_split_fiber_containment.md`.

## Multiplicity transfer

Let `B` be a finite set of leaf labels in the ordinary projective equal-line
split-fiber model.  Suppose each label has a projective `z` parameter, and all
labels with charged `y` values have already been removed.  Assume a
`z`-multiplicity cap

```text
#{ b in B : z(b)=z0 } <= nu        for every z0 in P^1(F).
```

Then the corresponding `y`-multiplicity satisfies

```text
#{ b in B : y(z(b))=y0 } <= 2nu    for every uncharged y0 in P^1(F).       (M)
```

This is sharp for local bookkeeping: a split ordinary fiber can contain two
base-field `z` points, and each can carry `nu` labels.

Combining `(M)` with the equal-line popularity gate gives

```text
U_eq,z(nu) = 8(2nu) = 16nu.                       (U-z)
```

In particular, injective `z` leaves are the case `nu=1`, recovering the
previous cap

```text
U_eq,z(1) = 16.
```

## Closure consequence

Substitute `U=16nu` in the support floor `(PC1)` of
`m1_high_overlap_graph_budget.md`.  Equivalently, in the notation of
`m1_equal_line_packet_sift_closure.md`, use

```text
F_eq,z(K,s,h,D,Lambda,nu)
  = F_pop(K,s,h,D,Lambda,16nu).
```

If

```text
F_eq,z(K,s,h,D,Lambda,nu) > R,
```

then every selected residual packet family satisfies at least one of:

```text
large support:
  B > R;

near-star:
  the endpoint-support family is one of the bounded near-star templates;

model-entry failure:
  a high-overlap star did not enter the ordinary projective equal-line
  split-fiber model;

z-multiplicity failure:
  some projective z value carries more than nu leaf labels;

charged exception:
  a quotient, tangent, fixed-root, endpoint-star, singular-y, denominator,
  or projective-boundary branch was not removed.
```

Thus the multiplicity part of the equal-line C3 target can be stated using
the `z` parameter rather than the coarser `y` parameter.

## Proof

The fiber equation `(F)` is obtained by clearing denominators in

```text
[Y:W] = [T^2+3Z^2 : (T-Z)^2].
```

Its discriminant is `(D)`, so the only branch values are `W=0` and
`4Y-3W=0`, namely `infinity` and `3/4`.

For the deck map, write `sigma([Z:T])=[Z+T:3Z-T]`.  Direct substitution gives

```text
(3Z-T)^2 + 3(Z+T)^2 = 4(T^2+3Z^2),
((3Z-T)-(Z+T))^2 = 4(T-Z)^2,
```

so `y(sigma(z))=y(z)`.  The matrix of `sigma` squares to `4I`, hence
`sigma^2=id` on `P^1`.

A fixed point satisfies `[Z:T]=[Z+T:3Z-T]`.  In affine form this is

```text
z = (z+1)/(3z-1),
```

or

```text
(z-1)(3z+1)=0.
```

The two fixed points are therefore `z=1` and `z=-1/3`, mapping to
`infinity` and `3/4`.  Away from these branch values, a geometric fiber has
two distinct points interchanged by `sigma`.

The multiplicity bound follows immediately: an uncharged `y` fiber contains
at most two base-field `z` points, and each has at most `nu` labels.  The
support-floor consequence is exactly the popularity-cap criterion from
`m1_high_overlap_graph_budget.md` after substituting `U=16nu`.

## Verification

The companion verifier checks the deck identity, involution, fixed-point
classification, branch/fiber ledger, sharpness of the `2nu` multiplicity
bound, and the substitution `U=16nu` into the packet-sift support floor:

```sh
python3 experimental/scripts/verify_m1_equal_line_deck_multiplicity_ledger.py
```
