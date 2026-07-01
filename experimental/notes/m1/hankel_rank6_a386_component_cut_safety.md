# Hankel Rank-6 A386 Component-Cut Safety

Status: PROVED / AUDIT.

This note records a companion criterion for the separated rank-6 boundary at

```text
A = 386.
```

It refines the residual left by the conic-pair safety criterion.  It is still
not an unconditional closure of all `A=386` weights.

At `A=386`, the boundary low-degree transfer gives

```text
h = |X union Y|-t = 3,
```

so the auxiliary polynomial `Q` lives in a projective plane:

```text
deg Q < 3,        [Q] in P^2.
```

The previous conic-pair criterion says that if two direction-consistency
conics have no common component over the algebraic closure, Bezout bounds the
finite root count by `4`.  It leaves the case where two such conics have a
full common component `G`.

Let `G` have degree

```text
c in {1,2}.
```

Write the irreducible components of `G` as `G_i`, with degrees `c_i`.  If
each `G_i` is cut by some direction-consistency conic `F_i`, meaning `F_i`
does not contain `G_i`, then the zeros on the common component are contained
in the union of the cuts

```text
G_i = F_i = 0,
```

and have total length at most

```text
sum_i 2 c_i = 2c
```

by Bezout.  This component-wise formulation is needed when `G` is a reducible
degree-2 conic.  Away from `G`, the two original conics leave residual curves
of degree `2-c`, so the off-component intersection has length at most

```text
(2-c)^2.
```

Thus the finite ambient `Q`-classes are bounded by

```text
2c + (2-c)^2.
```

For `c=1` this is `3`; for `c=2` this is `4`.  The null-polynomial
split-locator gate can only remove finite ambient roots, not create new ones.
The endpoint-uniform theorem contributes one projective endpoint `[0:1]`.
Therefore under the component-cut criterion,

```text
finite split-locator roots <= 4,
endpoint contribution       = 1,
total projective contribution <= 5 <= 6.
```

After this refinement, the remaining `A=386` residual is not an arbitrary
common component.  It is an irreducible component contained in all
direction-consistency conics.

Replay:

```sh
python3 experimental/scripts/verify_f17_32_m3_rank6_a386_component_cut_safety.py \
  --check experimental/data/certificates/hankel-f17-32-m3-rank6-a386-component-cut-safety/f17_32_n512_k256_m3_rank6_a386_component_cut_safety.json
```

Nonclaims:

```text
no proof that every A=386 common-component case satisfies the cut criterion;
no classification of the global-component residual;
no A=385 closure;
no overlapping-support rank-6 classification;
no endpoint payment theorem.
```
