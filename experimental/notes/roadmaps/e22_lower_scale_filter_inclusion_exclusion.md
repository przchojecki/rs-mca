# E22 Lower-Scale Filter Inclusion-Exclusion

- **DAG node:** `e22_lower_scale_filter_inclusion_exclusion`
- **Status:** PROVED
- **Source:** `prize/nodes/e22_lower_scale_filter_inclusion_exclusion/`
- **Depends on:** `e22_residual_profile_generating_function`
- **Verifier:** `python3 experimental/scripts/verify_e22_lower_scale_filter_inclusion_exclusion.py`

## Statement

Fix a dyadic pair `M_i < M_j` and a residual-profile universe `U_{i,j}`
counted by `e22_residual_profile_generating_function`.  For each smaller
dyadic scale `M' < M_i`, let `A_{M'}` be the event that the same support is
admissible at scale `M'`.

Then the minimality condition

```text
|B_{M'}(R)| >= M'        for every M' < M_i
```

is exactly the complement of the union of the events `A_{M'}`.  Therefore the
weighted count of minimal-scale-`M_i` residual profiles is

```text
sum_{S subset Smaller(M_i)} (-1)^|S| W(intersection_{M' in S} A_{M'}),
```

where the empty intersection is all of `U_{i,j}` and `W` is the declared
multiplicity weight.

## Proof

Let `U = U_{i,j}` be the finite residual-profile universe.  For each smaller
dyadic scale `M' < M_i`, define

```text
A_{M'} = {R in U : |B_{M'}(R)| < M'}.
```

The tail-minimality condition for selecting `M_i` says precisely that none of
these smaller-scale admissibility events occurs:

```text
R is minimal at M_i
    iff R in U \ union_{M'<M_i} A_{M'}.
```

Finite inclusion-exclusion gives the indicator identity

```text
1_{U \ union A_{M'}}
  = sum_{S subset Smaller(M_i)}
      (-1)^|S| 1_{intersection_{M' in S} A_{M'}}.
```

The empty intersection is `U`.  Multiplying the pointwise identity by any
declared nonnegative integer multiplicity weight `w(R)` and summing over `U`
gives the displayed weighted count.

## Role In The Program

This isolates the lower-scale minimality filter as a formal finite
inclusion-exclusion layer.  It lets later exact intersection-profile packets
focus only on computing the weighted intersections needed by the `(Q)`
quotient-ledger route.

