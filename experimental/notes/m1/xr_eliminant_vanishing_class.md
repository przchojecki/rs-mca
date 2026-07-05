# XR Eliminant Vanishing Class

Status: PROVED as a reduction.

Source DAG node: `xr_eliminant_vanishing_class`.

## Statement

In the XR light-triangle branch, there is no remaining unpaid class whose
normal-form eliminant vanishes identically on a light profile.  After the
light-profile nonvanishing input, coordinate-special stagnation inside a
profile is reduced to a proper bounded-degree hypersurface.

Equivalently, the old structured branch

```text
identically vanishing light-profile eliminant
```

is removed.  The remaining branch is

```text
nonzero eliminant hypersurface population/rationing.
```

## Proof

The normal-form packet `xr_triangle_eliminant_form` identifies light-triangle
stagnation with rank drop of the stacked twisted-sum matrix, i.e. with
vanishing of all maximal minors.

The packet `xr_light_profile_eliminant_nonvanishing.md` proves that, under the
light inequality, the normal-form map is injective.  Hence the normal-form
matrix has rank `3t`, so at least one maximal minor is nonzero on every light
profile.  Therefore no unpaid light profile has an identically vanishing
eliminant.

The packet `xr_coordinate_hypersurface_reduction.md` then applies to the
chosen nonzero maximal minor: any coordinate-special rank-stagnation point
inside the profile lies on the proper hypersurface cut out by that minor.

Thus the identically vanishing profile class is gone, and the only surviving
coordinate-special branch is a proper-hypersurface counting problem.

## Program Use

This closes the structural/nonvanishing side of the XR light-triangle branch.
It does not count points on the resulting hypersurface and does not by itself
prove a row-level adjacent upper ledger.  The remaining consumer is the
separate staircase/SPI/XR rationing input for hypersurface intersections.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_xr_eliminant_vanishing_class.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_xr_eliminant_vanishing_class.py \
  --check experimental/data/certificates/xr-eliminant-vanishing-class/xr_eliminant_vanishing_class.json
```

The verifier checks the dependency implication and non-claims.  It is not a
point-counting certificate.
