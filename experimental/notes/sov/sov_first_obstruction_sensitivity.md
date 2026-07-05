# SOV First-Obstruction Sensitivity

Status: PROVED.

Source DAG node: `sov_first_obstruction_sensitivity`.

## Statement

For the forced-root obstruction construction, changing only the coefficient of
`X^{h-1}` in the locator `L` leaves the forced root unchanged and changes the
first obstruction `O_{h-1}` by exactly the negative of that coefficient change.
Hence `O_{h-1}` is the coordinate-sensitive obstruction used by the SOV
value-set problem.

## Proof

By `sov_forced_root_recursion_algebra`, the forced root `S` is computed from
the coefficients of the monic degree-`2h` locator `L` in degrees

```text
2h-1, 2h-2, ..., h.
```

The coefficient of `X^{h-1}` in `L` is not used anywhere in that triangular
recursion. Therefore changing only `[X^{h-1}]L` leaves the forced root `S`
unchanged.

The first obstruction is

```text
O_{h-1} = [X^{h-1}](S^2 - L).
```

If `[X^{h-1}]L` changes by `delta` and `S` is unchanged, then
`[X^{h-1}]S^2` is unchanged and

```text
O_{h-1} -> O_{h-1} - delta.
```

Thus a unit bump changes `O_{h-1}` by `-1`, and the coordinate is exactly the
one isolated by the SOV value-set scan.

## Non-Claims

This packet proves the coefficient sensitivity gate only. It does not prove
that actual conditioned anchored-core families have small value sets or
character sums.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_sov_first_obstruction_sensitivity.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_sov_first_obstruction_sensitivity.py \
  --check experimental/data/certificates/sov-first-obstruction-sensitivity/sov_first_obstruction_sensitivity.json
```

The verifier reuses the forced-root recursion helper and checks multiple
coefficient perturbations in a deterministic sample.
