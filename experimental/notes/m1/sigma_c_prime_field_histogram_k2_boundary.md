# Sigma_C Prime-Field Histogram And k=2 Boundary Census

**Status:** AUDIT / EXPERIMENTAL.  The finite rows in the certificate are
PROVED finite enumerations; the family-level interpretation is experimental.

This note records full sparse-pair scans for two saturation rows and four
prime-field `k=2` boundary rows.  The endpoint convention is:

- `m = n-k`.
- `r = floor(delta*n)`.
- only finite slopes `gamma in F_q` are counted; there is no projective
  infinity slope.
- toy rows use `q_gen = q_line = q`; `q_chal` is unused.

The replay packet is:

```text
experimental/data/certificates/sigma-c-sparse-census/sigma_c_sparse_census_gpu_histograms_k2_rows.json
```

It is checked by:

```text
python experimental/scripts/verify_sigma_c_sparse_census.py --check experimental/data/certificates/sigma-c-sparse-census/sigma_c_sparse_census_gpu_histograms_k2_rows.json
python experimental/scripts/verify_sigma_c_histogram_packet.py --check experimental/data/certificates/sigma-c-sparse-census/sigma_c_sparse_census_gpu_histograms_k2_rows.json
```

The full scans were executed offline on a CUDA GPU accelerator; the device,
CuPy version, integer-arithmetic mode, per-row elapsed times, and kernel source
SHA-256 are recorded in the certificate's `gpu_run` block. The committed
verifiers are CPU/stdlib; no GPU is needed to check this contribution.
The shared sigma_C verifier recomputes `pairs_total` and replays recorded
extremal witnesses, but it does not re-derive the scan-wide histogram,
`bad_pair_count`, or `sigma_C` maximum for the large rows. The dedicated
histogram checker validates internal histogram arithmetic and replays the same
recorded extremal witnesses; the scan-wide maxima rest on the recorded offline
full scans plus the stated independent spot checks.

## Full-Scan Results

| q | n | k | m | r | pairs scanned | sigma_C | Interpretation |
|---:|---:|---:|---:|---:|---:|---:|---|
| 17 | 16 | 12 | 4 | 3 | 13,387,166,209 | 17 | saturated, with full histogram |
| 11 | 10 | 4 | 6 | 4 | 43,753,609,201 | 11 | saturated, with full histogram |
| 11 | 5 | 2 | 3 | 2 | 144,601 | 5 | intermediate: `r < sigma_C < q` |
| 7 | 6 | 2 | 4 | 3 | 2,246,689 | 7 | saturated |
| 13 | 6 | 2 | 4 | 3 | 95,257,009 | 13 | saturated |
| 17 | 8 | 2 | 6 | 4 | 482,919,545,089 | 9 | intermediate: `r < sigma_C < q` |

The `k=2` rows show that the empirical refinement proposed with the integrated
`k=1` counterexample family
(`experimental/notes/m1/sigma_c_subcapacity_dichotomy_counterexample.md`) -
"sub-capacity band and `k >= 2` implies immediate saturation" - is false as
stated. Two `k=2` rows saturate, but two have intermediate values:

```text
(q,n,k,r) = (11,5,2,2): sigma_C = 5
(q,n,k,r) = (17,8,2,4): sigma_C = 9
```

The row `(11,5,2,r=2)` resolves that note's stated open question - whether an
untested `k=2` row also fails to saturate - in the affirmative; the integrated
dichotomy certificates scanned only `k=1` rows.

The open boundary question is therefore not simply `k=1` versus `k>=2`.
The current finite evidence suggests that rate, `m`, and domain length still
matter inside the sub-capacity band.

For `(11,5,2,r=2)`, the value `sigma_C=5` is CPU-confirmed by exhaustive scan.
For `(17,8,2,r=4)`, exact CPU witness replay confirms `sigma_C >= 9`, and a
broad independent CPU search found no pair exceeding 9; the upper bound
`sigma_C <= 9` rests on the recorded full GPU scan.

## Histogram Signals

For `(17,16,12,r=3)`, almost every bad pair is fully saturated:

```text
0: 2,324,737
1: 39,520,512
17: 13,345,320,960
```

For `(11,10,4,r=4)`, saturation is present but the mass is spread across many
bad-slope counts:

```text
0: 2,224,601
1: 24,591,600
2: 1,133,000
3: 14,498,000
4: 136,928,000
5: 877,910,000
6: 3,601,400,000
7: 8,588,734,000
8: 11,975,469,000
9: 10,877,449,000
10: 6,103,933,000
11: 1,549,339,000
```

Thus the saturation witness is not isolated in either row.

## Scope And Open Rows

The row `(13,12,6,r=4)` is a natural next histogram row but is not included
here.  Its full scan has `395,359,140,961` sparse pairs.  In the Hankel-shape
engine used here, it has `C(12,4)*(6-4) = 990` closed-ball functional rows
per pair, about `5.79x` the measured `(17,8,2,r=4)` work units.

The row `(11,10,2,r=5)` is also not included even though its pair count is
below `10^13`: it has `6,314,320,009,201` sparse pairs and
`C(10,5)*(8-5) = 756` closed-ball functional rows per pair, about `70.6x`
the measured `(17,8,2,r=4)` work units, or roughly `17.5` hours at that
measured row's throughput.  It remains a visible open row, not a negative
result.

The row `(13,12,2,r=6)` is not included and is beyond the stated pair-count
envelope: it has `20,880,747,391,466,593` sparse pairs and
`C(12,6)*(10-6) = 3,696` closed-ball functional rows per pair.

## Non-Claims

This is not an asymptotic theorem, not a deployed-row claim, not a
`q_chal` soundness statement, and not extension-field evidence.  GF(9) and
other extension-field rows remain separate work because this verifier is a
prime-field packet checker.
