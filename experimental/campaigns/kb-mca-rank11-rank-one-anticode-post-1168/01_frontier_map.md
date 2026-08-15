# Frontier map

## Exact parent

PR #1168 head `6a5dcdae1591fc7f044eda6a942bfe178521a48c`.

## Imported frontier

PR #1168 proves that any over-budget post-near affine-error-rank-eleven line
forces:

- one actual minimizing pair of core deficiency at most `8` and weighted load
  at least `743449148`; and
- independently, a possibly different pair of core deficiency at most `4`
  owning at least `200632` slopes.

The fixed-pair multiplier is sharp. Its declared pair/core certificate class
still has minimum `811958533186703629 > B_*`, so the missing input must couple
different pair types or route them to an owner.

## New cut

Write a minimizing pair in a basis of the ten-dimensional direction code as
a `2 x s` coefficient matrix `M_e`, `s<=10`.

This packet removes the complete rank-one anticode branch:

- if `rank(M_e-M_f)<=1` for every two pair types, the family is a translate
  of one of the two maximal-clique geometries of the bilinear-forms graph;
- a fixed right factor is one affine correction ray, paid uniformly over
  its possible universal core by `8147918`;
- a fixed left factor is one affine correction space of dimension at most
  ten;
- pairwise core overlap `K-1` implies the rank-one hypothesis.

Thus the genuine successor residual contains rank-two pair differences, or
else enters the already named positive-dimensional linear correction
component.

## What remains

The packet does **not** prove that an unsafe rank-eleven family contains one
large rank-one pair anticode. The next aggregate theorem must do at least one
of the following:

1. force substantial mass into one rank-one anticode and preserve first-match
   ownership;
2. control collections containing rank-two pair differences by a new
   intersection/cycle theorem; or
3. pay the emitted degree-one positive-dimensional correction component.

## Non-overlap

This is not another fixed-pair multiplicity improvement, threshold scan,
ordinary distinct-neighbor claim, or per-clique summation. No sum over
different anticodes is banked.
