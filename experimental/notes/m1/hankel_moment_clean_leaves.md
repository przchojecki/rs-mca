# Hankel Moment-Clean Leaves

Status: PROVED.

Source DAG node: `hankel_moment_clean_leaves`.

## Statement

Terminal unpaid primitive Hankel leaves satisfy the moment-count input needed by
the descent accounting through the pinned-value variant. Literal direction-dual
cleanliness is false in general: monic or affine slices can have sparse affine
annihilator words with nonzero affine constant. The corrected statement is that
these pinned words can remove the all-zero assignment, but they do not add new
members beyond the clean moment bound.

## Proof

Let `A` be the affine family at a terminal leaf, and let `T` be a set of
coordinates with `|T| = s <= r`. If the affine annihilator has no nonzero
word of weight at most `r`, then the projection

```text
ev_T(A)
```

is either missing the zero vector or is all of `F^T`. Otherwise, a nonzero
linear functional vanishing on the image would lift to a sparse affine-
annihilator word, contradicting terminality.

When the projection is onto, every fiber has size `q^{dim A - s}`. When the
zero vector is missing, the all-zero fiber has size zero. Thus the zero-fiber
count is always at most the clean value `q^{dim A - s}`. Summing over all
`s`-subsets gives

```text
sum_f binom(rho(f), s) <= binom(|E|, s) q^{dim A - s}.
```

This is the same member/moment upper bound as in the clean case. Pinned
affine constraints can delete zero assignments; they never create extra
zero assignments.

## Non-Claims

This packet proves the terminal leaf moment-count input. It does not prove the
rank-profile entropy bound or the full Hankel termination theorem by itself.

## Replay

```bash
python3 experimental/scripts/verify_hankel_moment_clean_leaves.py --emit
python3 experimental/scripts/verify_hankel_moment_clean_leaves.py \
  --check experimental/data/certificates/hankel-moment-clean-leaves/hankel_moment_clean_leaves.json
```
