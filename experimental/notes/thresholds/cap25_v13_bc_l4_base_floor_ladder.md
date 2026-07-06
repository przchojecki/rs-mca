# CAP25 v13 BC L4 base-field floor ladder

Status: `AUDIT` / `EXACT_ARITHMETIC` / `TARGET_NORMALIZATION`.

**Data:** `experimental/data/certificates/frontier-adjacent/kb_mca_bc_l4_base_floor_ladder_v1.json`.
**Verifier:** `experimental/scripts/verify_bc_l4_base_floor_ladder.py`
(`--emit-defaults`, `--check`, and `--tamper-selftest`).

## What this is

This packet pins the finite conventions for the KoalaBear-MCA `L_4` quotient
row already present in the integrated `conj:Q` rung audit, read through
`agents.md`'s finite `conj:BC` split-pencil certificate target:

```text
(n, m, w_Q) = (131072, 69753, 4216).
```

It then evaluates the exact base-field floor from `prop:capg-census-floor` /
the BC work-plan at the boundary profile and the first eight interior profiles.
This is a normalization packet for the BC target, not a proof of the BC upper
census.

## Convention check

For the moved KoalaBear-MCA row, the line uses the MCA dimension
`K0 = 2^20 + 1`.  At scale `16`,

```text
K = ceil(K0/16) = 65537,
m = floor(1116048/16) = 69753,
w_BC = m - K = 4216.
```

Thus the boundary split-pencil profile is

```text
d1 = w_BC + 1 = 4217,
```

and the first BC interior profile is

```text
d1 = w_BC + 2 = 4218.
```

This matters because the boundary profile is delegated to `conj:Q`; counting it
inside BC double-counts the prefix fiber.  The `L_4` row is also clean for this
audit because `m=69753` is odd, so there is no further 2-adic ladder correction
inside this row.

## Exact floor values

For an interior profile `d1`, put

```text
m' = K - 1 + d1.
```

The base-field floor is

```text
binom(m', m) * ceil( binom(n, m') / p^(d1-1) ),
```

with `p = 2^31 - 2^24 + 1`.  The verifier recomputes every integer exactly.

| offset from boundary | role | `d1` | `m'` | log2 prefix average | ceil fiber floor | log2 base-field floor |
|---:|---|---:|---:|---:|---:|---:|
| 0 | Q boundary, not BC | 4217 | 69753 | 23.139009 | 9237104 | 23.139009 |
| 1 | BC interior | 4218 | 69754 | -8.035617 | 1 | 16.089988 |
| 2 | BC interior | 4219 | 69755 | -39.210288 | 1 | 31.179997 |
| 3 | BC interior | 4220 | 69756 | -70.385003 | 1 | 45.685065 |
| 4 | BC interior | 4221 | 69757 | -101.559762 | 1 | 59.775115 |
| 5 | BC interior | 4222 | 69758 | -132.734551 | 1 | 73.543258 |
| 6 | BC interior | 4223 | 69759 | -163.909361 | 1 | 87.048387 |
| 7 | BC interior | 4224 | 69760 | -195.084186 | 1 | 100.331145 |
| 8 | BC interior | 4225 | 69761 | -226.259041 | 1 | 113.421278 |

The important finite feature is the integer-ceiling regime: already at the
first BC interior profile, the expected prefix fiber is below one.  The exact
floor is therefore forced by the statement that some prefix value is realized,
and the binomial sub-support multiplier then grows quickly with `m'-m`.

## Interpretation

This packet supports the statement that the next BC computation should be an
upper census after the base-field floor and paid strata are separated.  It also
prevents two common convention errors:

1. using the Q boundary profile `d1=w+1` as a BC interior row; and
2. replacing the exact integer floor by the density model when the density is
   below one.

The orientation columns in the JSON compare the floor numbers to `K_raw` and
`B*`, but those comparisons are deliberately labelled `orientation_only`.
Support-census floors are not themselves bad-slope counts, and they are not
ledger payments.

## Non-claims

This packet does **not** prove any of the following:

```text
conj:BC,
U(1116048) <= B*,
a bound on primitive split-pencil cells,
a new unsafe floor,
or a bad-slope lower bound.
```

The live mathematical target remains the primitive interior split-pencil upper
census at `L_4`, with the base-field floor above included in the model and
with Q-boundary and quotient/tangent/extension/common-GCD cells paid by their
own ledgers.

## Replay

```sh
python experimental/scripts/verify_bc_l4_base_floor_ladder.py --check \
  experimental/data/certificates/frontier-adjacent/kb_mca_bc_l4_base_floor_ladder_v1.json

python experimental/scripts/verify_bc_l4_base_floor_ladder.py --check \
  experimental/data/certificates/frontier-adjacent/kb_mca_bc_l4_base_floor_ladder_v1.json \
  --tamper-selftest
```

The verifier is stdlib-only and recomputes the large binomial/power integers
exactly.
