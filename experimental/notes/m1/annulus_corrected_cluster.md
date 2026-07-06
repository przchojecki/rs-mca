# Annulus Bounded-Cluster Insufficiency Search

## Claim

No Johnson-bounded cluster correction among the four tested notions restores
the annulus MCA-from-CA shape on the recorded rows. The only Johnson-bounded
notion is `C0`, the parent pair-explanation cluster, and it fails on two
rows. The notions that make the inequality hold, `C1`, `C2`, and `C3`, all
fail the Johnson size check.

Thus the parent slope-count gap converts into a size-control gap. This
strengthens the parent #349 finite finding: a bounded cluster-count fix does
not suffice on this toy annulus range.

## Status

EXPERIMENTAL. This is a finite insufficiency search for A.3, not a proof of a
corrected annulus MCA-from-CA theorem and not a `prob:band` resolution.

## Parameters

The recorded annulus rows are:

| q | n | k | r | a=n-r |
|---:|---:|---:|---:|---:|
| 11 | 10 | 3 | 4 | 6 |
| 13 | 12 | 5 | 4 | 8 |
| 17 | 16 | 7 | 5 | 11 |
| 31 | 10 | 3 | 4 | 6 |
| 7 | 6 | 1 | 3 | 3 |
| 17 | 8 | 3 | 3 | 5 |
| 19 | 9 | 2 | 4 | 5 |

Every row is in the strict annulus `2r > n-k`, uses the natural agreement
threshold `a=n-r`, and satisfies the Johnson check `a^2 > (k-1)n`.

## Existing Paper Dependency

- `def:ca` and `def:mca` define the CA/MCA bad-slope predicates and the
  `eca`/`emca` normalizations.
- `thm:deep-mca` supplies the `r+1` deep-regime oracle gate.
- `thm:johnson-list` supplies the list bound checked at agreement `a=n-r`.
- `thm:mca-from-ca`, `rem:half-scope`, and `cor:band-reduction` identify the
  below-half-distance explanation issue.
- The parent finite check is #349; this packet keeps its MCA/CA definitions
  and its shared-row C0 counts fixed.

## Proof Idea Or Experiment

The enumerator builds exact prime-field Reed-Solomon analyzers and records:

- `C0`: parent pair-explanation cluster.
- `C1`: distinct MCA witness codewords. This is the principled unbounded
  correction, because it counts the actual MCA witnesses.
- `C2`: degenerate diagnostic counting size-at-least-`a` sub-supports of the
  witness agreement sets. Its large size is a combinatorial artifact, not a
  serious cluster candidate.
- `C3`: distinct single-codeword half-explanations for either received word.

The verifier independently replays the MCA/CA counts and the candidate counts
from direct agreement-set interpolation. For `C1`, `C2`, and `C3`, the JSON
certificate stores counts plus two deterministic example records per pair
instead of complete provenance; the checker recomputes the full objects before
checking the slim projection.

## Ledger Impact

The finite ledger is negative. No tested notion is both:

```text
1. strong enough to restore epsilon_mca*q <= epsilon_ca*q + |C|*r, and
2. bounded by the Johnson list size at a=n-r.
```

`C1`, `C2`, and `C3` restore the recorded inequalities only because their
cluster sizes are not Johnson-bounded on the full range. `C3` has the smallest
maximum per-pair count among the unbounded successful notions, but that is only
a diagnostic tie-break. `C1` is the more principled unbounded notion because it
counts the actual distinct witness codewords.

## Constants

Overall candidate summary:

| candidate | universal shape | Johnson on all rows | max count | total count |
|---|:---:|:---:|---:|---:|
| C0 | no | yes | 2 | 21 |
| C1 | yes | no | 5 | 41 |
| C2 | yes | no | 6883 | 9151 |
| C3 | yes | no | 3 | 44 |

The parent C0 cross-check passes on all shared rows. In particular, the parent
gap row `(13,12,5,4)` still has the seeded sample

```text
MCA slopes = 5, CA slopes = 0, C0 = 1, C1 = 5, C2 = 37, C3 = 2.
```

The oracle gate passes:

| row | result |
|---|---|
| `F_5, n=4, k=1, r=1` | exhaustive replay gives max MCA = 2 and max CA = 2, matching `r+1` |
| `F_13, n=12, k=6, r=2` | tangent witness gives MCA = 3 and CA = 3, matching `r+1` |

The compact certificate is `112623` bytes. The payload hash is:

```text
175ad0b12bf0be6f5990058ff981ab45a6defc9a0f1b7e168beaf60122bb9e6b
```

## Reproducibility

```powershell
py -3.13 experimental/scripts/verify_annulus_corrected_cluster.py --emit-defaults
py -3.13 experimental/scripts/verify_annulus_corrected_cluster.py --check experimental/data/certificates/annulus-corrected-cluster/annulus_corrected_cluster.json
py -3.13 experimental/scripts/verify_annulus_corrected_cluster_check.py --check experimental/data/certificates/annulus-corrected-cluster/annulus_corrected_cluster.json
```

## Deviations

- The recorded annulus pairs are constructed and deterministic seeded samples;
  the packet is exhaustive only for the small deep-regime oracle row.
- `C2` is explicitly diagnostic and degenerate: it counts all size-at-least-`a`
  sub-supports of witness agreement sets, so its size reflects combinatorial
  inflation.
- The JSON certificate stores complete counts but only two deterministic
  example records per pair for `C1`, `C2`, and `C3`; rerun the generator command
  above to recompute the full objects.
- The packet is exact CPU-only; no GPU path is used or required.
