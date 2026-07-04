# XR small-core rungs 2a/2b

- **Status:** PROVED structural reductions. This packet closes the same-slope
  list bridge and the distinct-slope partial-forcing bridge. It does not
  prove the list grand challenge or the graded tangent ledger.
- **DAG:** `xr_smallcore_spread_count`.
- **Verifier:** `experimental/scripts/verify_xr_smallcore_rungs_2a_2b.py`.
- **Parents:** `qx13_pair_rank_ledger.md`, `e27_exceptional_pair_census.md`,
  `proof_sketch/s7_list_side.md`, and the local `t=2` exchange packet
  `m1_t2_one_exchange_residual_degree.md`.

## Critical-path role

This is a proof-spine packet for the conditional prize route.  Together with
`xr_pencil_cascade.md`, it decomposes the face-4 small-core obligation before
the clean-rate compiler consumes the terminal polynomial residue:

- same-slope aligned supports are exactly the list-lane worst-word object;
- distinct-slope cores with `k+1 <= r <= A-2` are paid tangent-depth cells;
- distinct-slope cores with `r >= A-1` are handled by the pencil cascade;
- the remaining uncharged piece is the irreducible `r <= k` rank/spread shell.

Thus this packet does not assert the terminal polynomial bound itself.  It
identifies which bands are already proved/paid, so the downstream conditional
step can focus on the residual small-core shell and the
`active_core_count_bound` / PTE residue rather than recounting list or tangent
families.

## 0. Setup

Let `C = RS[D,k]`, `|D|=n`, and let the agreement threshold be

```text
A = k+t.
```

For a fixed pair `(u,v)` and finite slope `z`, write `w_z=u+zv`. An exact
aligned support is a tuple `(S,z,c)` with `|S|=A`, `c in C`, `w_z=c` on `S`,
and exact disagreement off `S`. Exactness is the convention used below;
ordinary `>=A` list bounds dominate exact-list counts.

## 1. Rung 2a: same slope = the list worst-word object

Fix `z`. If two exact aligned supports `(S,z,c_S)` and `(T,z,c_T)` have
`|S cap T| >= k`, then `c_S=c_T` by Reed-Solomon uniqueness. Exactness then
forces `S=T`, since a fixed word-codeword difference has one exact zero set.
Therefore distinct same-slope exact supports satisfy

```text
|S cap T| < k.
```

So same-slope families are automatically far-spread and need no new XR spread
analysis.

Moreover, for fixed `z`, the supports are exactly the exact-list codewords of
the received word `w_z` at radius `j=n-A`: each exact aligned support gives a
codeword at exact agreement `A`, and each such codeword gives its unique exact
agreement support. Hence

```text
same_slope_branch(u,v; z, A) = ExactList_C(w_z, A).
```

Consequently rung 2a is not an independent face-4 problem. It is the second
grand challenge's worst-word list object, with exact lists bounded by the
ordinary `>=A` list count.

## 2. Rung 2b: distinct slopes with `k < r <= A-2` are tangent-depth cells

Let two distinct slopes `z_1 != z_2` align on supports `S_1,S_2`, with
codewords `c_1,c_2`, and put

```text
R = S_1 cap S_2,      r = |R|.
```

On `R`,

```text
u+z_1 v = c_1,
u+z_2 v = c_2.
```

Since the slope matrix is invertible, define codewords

```text
V = (c_1-c_2)/(z_1-z_2),
U = (z_1 c_2 - z_2 c_1)/(z_1-z_2).
```

Then

```text
v = V and u = U on R.
```

If `r=k+d` with `d>=1`, this is a genuine tangent-depth `d` constraint: a
degree-`<k` codeword is determined by any `k` of the core points, and the
remaining `d` points are extra vanishing constraints for `v-V` (and similarly
for `u-U`). Thus every distinct-slope partial-core pair with

```text
k+1 <= r <= A-2
```

belongs to a graded tangent cell of depth

```text
d = r-k.
```

Equivalently, writing the support exchange distance as `s=A-r`, the partial
band has

```text
2 <= s <= t-1,       d = t-s,       d+s=t.
```

On this band qx13 gives `c(s,t)=s`; the tangent depth and the qx13 fresh
codimension are complementary.

## 3. Boundary and residual

The shell `r=k` has depth zero. A degree-`<k` polynomial interpolates any
values on `k` points, so the two-slope identities impose no tangent constraint
beyond interpolation. This boundary belongs with the irreducible rank/spread
core, not with rung 2b.

After charging:

- same-slope exact supports to the list lane;
- distinct-slope pairs with `r>=A-1` to the pencil cascade;
- distinct-slope pairs with `k+1<=r<=A-2` to the graded tangent ledger;

the residual small-core statement is the rank/spread shell with pairwise cores
`r<=k`, plus the known face-3 exception classes. This is the real rung 2c.

## 4. Non-claims

- This packet does not prove `list_grand`, `list_safe`, or
  `list_adjacency_closing`.
- This packet does not prove the general graded tangent ledger; it proves the
  exact two-slope forcing map that any such ledger must charge.
- This packet therefore does not flip `xr_smallcore_spread_count` to PROVED.
  It removes rungs 2a/2b from the irreducible residue.

## 5. Verifier

`experimental/scripts/verify_xr_smallcore_rungs_2a_2b.py` checks:

- exhaustive same-slope exact-list/k-spread behavior for a small RS row;
- Vandermonde rank/codimension `max(0,r-k)` for core sizes;
- a finite-field two-slope identity example where the extra core points are
  exactly tangent-depth constraints;
- the partial-band arithmetic `d+s=t` and `c(s,t)=s`.
