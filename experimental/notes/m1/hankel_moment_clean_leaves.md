# Hankel Moment Clean Leaves Packet

- **Status:** PROVED / pinned-value leaf bound.
- **DAG node:** `hankel_moment_clean_leaves`.
- **Certificate:** `experimental/data/certificates/hankel-moment-clean-leaves/hankel_moment_clean_leaves.json`.
- **Verifier:** `python3 experimental/scripts/verify_hankel_moment_clean_leaves_packet.py --check experimental/data/certificates/hankel-moment-clean-leaves/hankel_moment_clean_leaves.json`.

This packet records the terminal-leaf member-count input for the Hankel
termination route. The important point is the corrected pinned-value boundary:
plain direction-dual cleanliness is false in general, but the pinned affine
variant gives the same moment upper bound needed by the consumer.

## Claim

Let `A` be the affine solution space at a terminal unpaid primitive Hankel
leaf, and let `E` be the residual domain. Suppose the affine annihilator has no
nonzero word of weight at most `r`. Then for every `T subset E` with
`|T| = s <= r`, the evaluation map on `T` has one of two outcomes:

```text
ev_T(A) misses 0, so the zero-count is 0;
ev_T(A) is onto, so the zero-count is q^(dim A - s).
```

If a nonzero functional killed the image while also hitting the pinned zero
assignment, it would extend to a sparse affine-annihilator word of weight at
most `s`, contradicting the terminal-leaf hypothesis.

Therefore the same moment bound as in the clean case holds:

```text
sum_f binom(rho(f), s) <= binom(|E|, s) q^(dim A - s).
```

## Evidence Boundary

The working record checked `279` clean terminal flats and observed counts only
of the permitted forms `0` and `q^(dim A - s)`. The proof is affine linear
algebra and is not Hankel-specific; Hankel enters through the terminal-leaf
hypothesis that removes sparse affine annihilators.

## Correction

The unpinned cleanliness statement is false for monic/affine slices: MDS
examples have direction-dual low-weight words with nonzero affine constant.
This packet intentionally packages the pinned-value lemma instead.

## DAG Use

`f_termination_hankel` consumes this packet after
`hankel_rank_profile_entropy` has bounded the number of terminal states. The
present packet supplies the member-count and moment/residue bound at those
leaves.

## Non-Claims

- This packet does not assert unpinned direction-dual cleanliness.
- This packet does not count reachable terminal states.
- This packet does not prove the rank-profile entropy theorem.
- This packet does not edit Papers A-D.
