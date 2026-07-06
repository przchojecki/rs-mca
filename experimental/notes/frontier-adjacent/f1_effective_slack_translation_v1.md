# F1 effective-slack translation for frontier-adjacent rows

Status: EXPERIMENTAL / AUDIT.

This packet translates the current deployed frontier-adjacent rows into the
same slack variable used by the F1 full-orbit toy scanner:

```text
t = a - k.
```

It answers a narrow scoping question.  The toy scanner
`experimental/data/certificates/frontier-adjacent/f1_full_orbit_scan_v1.json`
finds a sharp split for the simple-pole pencil:

- toy `t=1`: full-orbit `K=F` slopes grow with the base prime;
- toy `t>=2`: the same pencil has zero full-orbit bad slopes on the tested
  menu.

The deployed adjacent rows are not `t=1` rows under the direct variable
translation.

## Replay

```bash
python3 experimental/scripts/verify_f1_effective_slack_translation.py --check \
  experimental/data/certificates/frontier-adjacent/f1_effective_slack_translation_v1.json
```

The verifier reads the four row packets in `frontier-adjacent/`, uses the
current v14 moved pair when present, and checks the F1 toy split from
`f1_full_orbit_scan_v1.json`.

## Result

| row | adjacent open `a` | `t=a-k` | `j=n-a` | direct toy bucket |
|---|---:|---:|---:|---|
| KoalaBear MCA | 1116048 | 67472 | 981104 | `t>=2` |
| KoalaBear list | 1116047 | 67471 | 981105 | `t>=2` |
| M31 MCA | 1116024 | 67448 | 981128 | `t>=2` |
| M31 list | 1116023 | 67447 | 981129 | `t>=2` |

So the `t=1` growth branch of the toy scanner is **not deployed-shape evidence**
for these adjacent rows under the direct slack translation.  It remains a
corrected-reserve warning: a real growth branch exists when a support supplies
only one linear constraint on the slope.

The direct analogy for the deployed adjacent rows is the toy `t>=2` branch,
where the same simple-pole pencil vanishes in the current scan.

## Non-claims

- This does **not** prove `paid_extension(a)` is safe.
- This does **not** classify all genuinely `F`-valued received pairs.
- This does **not** rule out other extension-cell counterexamples.
- This does **not** promote the toy scanner to a deployed theorem.
- This does **not** resolve the open M1/L1/sparse residual cells.

## Next step

The next useful F1 task is to turn the observed simple-pole split into a
theorem or a falsifier:

1. prove the divided-difference obstruction for the simple-pole pencil at
   `t>=2`; or
2. find a genuinely `F`-valued pair whose `t>=2` constraints still leave a
   growing full-orbit `K=F` slope set.

Either outcome is cleaner than extending the `t=1` growth branch, because the
frontier-adjacent deployed rows sit deep in `t>=2`.
