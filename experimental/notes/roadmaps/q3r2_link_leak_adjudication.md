# Q3R.2 Link-Leak Adjudication

- **Campaign task:** C-1.
- **DAG node:** `xr_globalness_from_ledger` / Q3R.2.
- **Status:** PROVED for the exact #209 finite corpus.
- **Verifier:** `experimental/scripts/verify_q3r2_link_leak_adjudication.py`.
- **Artifact:** `experimental/data/certificates/q3r2-link-leak-adjudication/q3r2_link_leak_adjudication.json`.
- **Source corpus:** `experimental/data/certificates/xr-pair-orbit-globalness/xr_pair_orbit_globalness.json`.

The #209 exact corpus reports ten post-quotient-strip link-leak candidates for
`F_97`, `n=16`, `j=8`, `t=2`.  This packet adjudicates only those ten rows.  It
does not rerun the sampled `n=32` telemetry and does not claim an exhaustive
classification of all projective word pairs.

## Strip Criterion

For each aligned support `T in A_{u,v}`, compute its finite slope `z(T)` from

```text
H_u l_T + z(T) H_v l_T = 0.
```

Fix a `(j-1)`-core `R`.  If two distinct completions

```text
T_1 = R union {y_1},     T_2 = R union {y_2}
```

have the same slope `z`, then `u + z v` has agreement on
`R union {y_1,y_2}`, of size `j+1`.  This is the T2 tangent-overlap leaf in
the first-match stratification tree: it is charged as `paid:tangent`, not as
unpaid residual link mass.

After removing every support lying in such a same-slope `(j-1)`-core bucket,
the residual per-core completion count is the relevant `L_tan` test:

```text
max_R #{residual T : R subset T} <= L_tan.
```

The stricter first-unpaid convention uses `L_tan = 1`.  The residual-edge
convention uses `L_tan = 2`, matching the local `t=2` one-exchange residual
degree bound.

## Verdict Table

| candidate | source paid-tangent radii | aligned | T2-paid supports | residual supports | residual max `(j-1)` core | verdict |
|---|---:|---:|---:|---:|---:|---|
| `delta_character_13` | 1,2,3,4 | 6537 | 6456 | 81 | 1 | strippable, `L_tan=1` |
| `delta_character_10` | 1,2,3,4 | 6537 | 6456 | 81 | 1 | strippable, `L_tan=1` |
| `delta_character_9` | 1,2,3,4 | 6510 | 6456 | 54 | 1 | strippable, `L_tan=1` |
| `delta_character_14` | 1,2,3,4 | 6510 | 6456 | 54 | 1 | strippable, `L_tan=1` |
| `delta_character_8` | 1,2,3,4 | 6471 | 6435 | 36 | 1 | strippable, `L_tan=1` |
| `delta_character_15` | 1,2,3,4 | 6471 | 6435 | 36 | 1 | strippable, `L_tan=1` |
| `delta_character_12` | 1,2,3,4 | 6524 | 6470 | 54 | 1 | strippable, `L_tan=1` |
| `delta_character_11` | 1,2,3,4 | 6524 | 6470 | 54 | 1 | strippable, `L_tan=1` |
| `character_pair_9_13` | 4 | 2048 | 1968 | 80 | 2 | strippable, residual-edge `L_tan=2` |
| `character_pair_10_14` | 4 | 2048 | 1968 | 80 | 2 | strippable, residual-edge `L_tan=2` |

Thus the eight `delta_character_*` rows are fully accounted for even under the
`L_tan=1` first-unpaid convention.  The two `character_pair_*` rows are the
only convention-sensitive cases: the T2 same-slope strip leaves exactly two
residual completions above some `(j-1)` cores, so they need the residual-edge
`L_tan=2` convention.  They are not genuine unpaid tangent leaks for Q3R.2.

## Consequence for `xr_globalness_from_ledger`

Under the residual-edge convention, all ten #209 candidates are strippable or
allowed by the `L_tan=2` residual cap:

```text
genuine unpaid tangent leaks among the ten candidates = 0.
```

The #209 warning is therefore a taxonomy/convention warning, not a new
unpaid tangent obstruction.  It still remains important as a regression test:
if later packets insist on `L_tan=1` without a separate residual-edge
deduplication rule, then the two character-pair rows are the rows that expose
the mismatch.

## Replay

```bash
python3 experimental/scripts/verify_q3r2_link_leak_adjudication.py --write
python3 experimental/scripts/verify_q3r2_link_leak_adjudication.py --check
python3 -m py_compile experimental/scripts/verify_q3r2_link_leak_adjudication.py
```

## Nonclaims

This packet does not prove `c_xr_content`, does not import KLLM constants, and
does not adjudicate any row outside the exact #209 `n=16` corpus.  It only
classifies the ten already-discovered post-strip link-leak candidates under
the pinned `L_tan` bookkeeping convention.
