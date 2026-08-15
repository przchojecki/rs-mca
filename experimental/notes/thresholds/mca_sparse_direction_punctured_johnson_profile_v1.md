# Sparse-direction punctured Johnson MCA profile

## Status

PROVED, field-general, exact finite arithmetic.

## Statement

After a codeword direction gauge with residual support `E`, `|E|=e<d`, a
transformed explanation of outside-agreement deficit `h` owns at most
`floor(e/h)` selected slopes.  Puncturing `E` turns all explanations of
deficit at most `h` into one ordinary RS list at agreement `m-h`.

Distinct explanations have agreement-set intersections at most `K-1`.
The ordinary Johnson incidence count therefore gives

```text
J_h=floor((N-e)(m-h-K+1)/((m-h)^2-(N-e)(K-1))).
```

If the denominator is positive at `h=e`, then

```text
|Z| <= sum_h (J_h-J_(h-1))*floor(e/h)
    <= (e-1)J_floor(e/2)+J_e.
```

## Exact deployed walls

```text
KoalaBear K=14:
  e<=63908, j=R-e>=984668, endpoint denominator 1218,
  endpoint bound 4607583 <= 274980728111395087.

Mersenne-31 K=6:
  e<=65236, j=R-e>=983340, endpoint denominator 2794,
  endpoint bound 2605443 <= 16777215.
```

The adjacent denominators are `-5924` and `-1636`.  They mark failure of
this Johnson proof, not unsafe rows.

Combined with the high-support proper-subspace walls, the full-lift
top-rank residual intervals are now

```text
KoalaBear: 63909<=e<=1044238;
Mersenne:  65237<=e<=1044241.
```

## Audit

`experimental/verify_mca_sparse_direction_punctured_johnson_profile_v1.py`
scans all 129,144 paid official supports exactly, reconstructs both adjacent
walls, independently checks the profile coarsening on two synthetic rows,
and rejects hostile constant mutations.  It uses standard-library integer
arithmetic and negligible memory.

## Nonclaims

This does not pay any support after the displayed walls, prove Johnson
sharpness, or close either official MCA row.
