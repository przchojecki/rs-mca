# Hankel Rank-Profile Entropy

Status: PROVED.

Source DAG node: `hankel_rank_profile_entropy`.

Depends on:

- `hankel_sparse_atoms_as_rational_defects`;
- `f_support_lattice`.

## Statement

For fixed cutoff `W`, unpaid primitive saturated states in the Hankel
rank-profile descent are bounded by `n^{O(W^2)}`. The proof uses a three-way
rank-profile dichotomy:

1. row-deficient Hankel kernels are principal GRS segments after the corrected
   torus/root-at-infinity adjustment;
2. row-full wide states have at most one atom-closure, using rational-defect
   separation and same-approximant collapse;
3. row-full narrow states have dimension `O(W)`, so the support-lattice
   accounting gives only `O(W)` branching levels of width at most `n^W`.

## Proof

The row-deficient case uses binary apolarity. If `rank M < t`, then the kernel
flat has the form

```text
P = q K[X]_{<=D-1},
deg q = (j + 1 - D) - alpha,
```

where `alpha` is the root-at-infinity multiplicity. Multiplication by
`X^alpha` is invertible on the multiplicative domain `mu_n`, so

```text
X^alpha P = qtilde K[X]_{<=D-1},
deg qtilde = j + 1 - D.
```

After this root strip, the zero-support matroid is a principal GRS segment, so
there is no unpaid entropy in the row-deficient branch.

In the row-full wide case, the inequality

```text
j - t + 3 > 2W
```

forces sparse atoms of size at most `W` into one rational-approximant closure:
distinct closures would violate the rational-defect separation bound from
`hankel_sparse_atoms_as_rational_defects`. Hence the wide branch contributes at
most one atom-closure.

In the row-full narrow case, `j - t + 3 <= 2W`, so the residual kernel
dimension is `O(W)`. Applying `f_support_lattice`, every strict descent chain
is memoized by closed-set states and has only bounded dimension/degree drops.
The resulting number of unpaid primitive saturated states is therefore
`n^{O(W^2)}` for fixed `W`.

## Non-Claims

This packet proves the rank-profile entropy bound used by the Hankel
termination chain. It does not produce per-agreement M3 root tables, close a
row-level `F_17^32` safe-side certificate, or prove the terminal moment-count
leaf condition.

## Replay

```bash
python3 experimental/scripts/verify_hankel_rank_profile_entropy.py --emit
python3 experimental/scripts/verify_hankel_rank_profile_entropy.py \
  --check experimental/data/certificates/hankel-rank-profile-entropy/hankel_rank_profile_entropy.json
```
