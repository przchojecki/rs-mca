# W2: graded tangent ledger design

DAG nodes: `xr_partial_tangent_band`, `xr_heavy_triangle_charge`.

Status: DESIGN.  This packet consumes the proved 2b forcing map from
`xr_smallcore_rungs_2a_2b.md`; it does not prove the final graded tangent
ledger bound and does not promote either DAG node.

## 1. Cell Partition

Let `A=k+t`, and let two distinct-slope aligned supports have common core
size

```text
r = |S_1 cap S_2|.
```

The proved 2b map says that if

```text
k+1 <= r <= A-2,
```

then subtracting the two alignment identities forces a codeword pair `(U,V)`
with

```text
u = U,       v = V
```

on the core.  Write

```text
d = r-k,       s = A-r.
```

Then the partial band is exactly

```text
1 <= d <= t-2,
2 <= s <= t-1,
d+s=t.
```

The ledger cells are therefore:

| Cell | Core range | Charge |
| --- | --- | --- |
| residual boundary | `r=k`, `d=0`, `s=t` | no tangent forcing; stays in 2c rank/spread |
| partial tangent | `r=k+d`, `1<=d<=t-2` | charge a depth-`d` tangent cell |
| pencil cascade | `r>=A-1`, `d>=t-1`, `s<=1` | paid by `xr_pencil_cascade` |

This is the whole pairwise split.  There is no additional pairwise band.

## 2. Canonical Charge

For a partial-band pair:

1. Use the two slopes to recover `(U,V)`.
2. Let `R=S_1 cap S_2` and `d=|R|-k`.
3. Choose a canonical `k`-subset `R_0 subset R` for interpolation.
4. Charge the remaining `d` points `R \ R_0` as the tangent-depth witness.

The charge key is

```text
(d, R_0, R\R_0, U, V)
```

or any equivalent canonicalization used by the paid tangent ledger.  The key
point is that the proved forcing map supplies the cell; the remaining ledger
work is to bound how often depth-`d` cells can be occupied after quotient,
dihedral, extension, and cascade payments are removed.

## 3. Heavy-Triangle Boundary

For three supports, write pairwise overlaps `r_12,r_13,r_23` and triple
intersection `y`.  The heavy-triangle condition is

```text
r_12 + r_13 + r_23 - y > 2k.
```

The W2 split is:

- If some `r_ij >= k+1`, the triangle has a direct partial-tangent edge and is
  charged to the 2b depth cell `d=r_ij-k`.
- If no `r_ij >= k+1`, then heaviness forces at least two overlaps
  `> k/2`.  Otherwise the largest overlap is at most `k` and the other two are
  at most `k/2`, giving total budget at most `2k`, contradiction.

Thus the generic heavy boundary is not a fourth object: after direct 2b edges,
it is rationed by `deep_link_staircase`.

## 4. Non-Claims

This packet does not prove the quantitative tangent-depth ledger.  It fixes
the charge cells and the boundary routing:

```text
2b partial band        -> graded tangent depth d
2b cascade boundary   -> xr_pencil_cascade
2c residual boundary  -> rank/spread core
heavy triangles       -> direct 2b edge or deep_link_staircase
```

The next proof obligation is the actual occupancy bound for the depth-`d`
cells.

## Verifier

`experimental/scripts/verify_w2_graded_tangent_ledger.py` checks:

- the identities `d+s=t` and the partial-cell ranges for `t=1..8`;
- that there are exactly `max(0,t-2)` partial cells;
- the residual and cascade boundary formulas;
- by exhaustive integer profiles for `k<=18`, every heavy triangle without a
  direct 2b edge has at least two deep links.

The recomputed summary is pinned in
`experimental/data/certificates/w2-graded-tangent-ledger/w2_graded_tangent_ledger.json`.
