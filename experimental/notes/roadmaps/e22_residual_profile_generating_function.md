# E22 Residual-Profile Generating Function

- **DAG node:** `e22_residual_profile_generating_function`
- **Status:** PROVED
- **Source:** `prize/nodes/e22_residual_profile_generating_function/`
- **Depends on:** `e22_overlap_nested_fiber_residual_identity`
- **Verifier:** `python3 experimental/scripts/verify_e22_residual_profile_generating_function.py`

## Statement

Fix dyadic scales `M_i < M_j` in a domain of size `n`.  Put

```text
P = n / M_j,          q = M_j / M_i,
```

so there are `P` coarse `M_j`-parents, each containing `q` fine `M_i`-fibers.
Before imposing lower-scale minimality conditions, canonical scale-`M_i` data
that are also raw-admissible at `M_j` are counted by a finite product formula.

Let

```text
G_q(u,z) = u + sum_{s=0}^{q-1} binom(q,s) z^s,
H_i(x)  = sum_{a=0}^{M_i-1} binom(M_i,a) x^a.
```

Here `u` marks a complete `M_j`-parent, and `z` marks a selected `M_i`-fiber
inside an incomplete `M_j`-parent.  For fixed `c,r,b`, the number of
canonical scale-`M_i` data with:

- `c` complete coarse parents;
- `r` selected fine fibers in incomplete coarse parents; and
- scale-`M_i` tail size `b`;

is

```text
[u^c z^r] G_q(u,z)^P * [x^b] H_i(x)^(Pq - cq - r).
```

The raw scale-`M_j` admissible part is obtained by summing this expression
over

```text
0 <= b < M_i,
b + M_i*r < M_j.
```

## Proof

Inside one coarse `M_j`-parent there are two cases.  If all `q` fine children
are selected, the parent is complete and contributes `u`.  If the parent is
incomplete, then exactly `s` of its `q` children may be selected for
`0 <= s < q`, giving `binom(q,s)` choices and contribution `z^s`.

Thus one parent contributes `G_q(u,z)`, and all `P` parents contribute
`G_q(u,z)^P`.  The coefficient `[u^c z^r]` counts selected fine-fiber sets
with `c` complete parents and `r` residual selected fine fibers in incomplete
parents.  Such a selected set contains `cq + r` fine fibers, leaving
`Pq - cq - r` unselected fine fibers.

A canonical scale-`M_i` tail may choose points only inside unselected fine
fibers and may not contain a whole unselected fine fiber.  For one unselected
fine fiber, the tail-size enumerator is

```text
H_i(x) = sum_{a=0}^{M_i-1} binom(M_i,a) x^a.
```

So `[x^b] H_i(x)^(Pq - cq - r)` counts tail choices of size `b`.

The fine-scale admissibility condition is `b < M_i`.  The nested-fiber
residual identity says raw scale-`M_j` admissibility is exactly

```text
b + M_i*r < M_j.
```

Summing the coefficient product over these inequalities counts exactly the
canonical scale-`M_i` data that are raw-admissible at `M_j`, before
lower-scale minimality and pricing-multiplicity filters.

## Role In The Program

This is a finite, exact profile enumerator for the `(Q)` quotient-ledger route.
It turns the nested-fiber residual identity into coefficients that later
minimality and intersection packets can filter without hiding residual
branches in point estimates.

