# DLI Erdos-Turan Peak-Mass Reduction

Status: PROVED.

Source DAG node: `dli_et_peak_mass_reduction`.

## Statement

If the normalized odd-evaluation sequence satisfies the required
finite-frequency Weyl-sum bounds up to the reciprocal scales used by the DLI
peak neighborhoods, then Erdos-Turan plus dyadic annuli around the Dirichlet
peaks gives the truncated-log discrepancy and peak-mass tail bounds required
by `dli_truncated_log_transfer`.

## Proof

Let `theta_y in R/Z` be the normalized odd-evaluation sequence, and write

```text
S_m = sum_y exp(2 pi i m theta_y).
```

The Erdos-Turan inequality gives, for every interval `I` and cutoff `H >= 1`,

```text
|#{y : theta_y in I}/Y - |I||
  <= C/(H+1) + C sum_{1 <= m <= H} |S_m|/(mY).
```

Thus finite-frequency Weyl-sum bounds imply interval discrepancy at every
scale `|I| >= 1/H`, with error controlled by the harmonic sum of the normalized
Weyl sums.

The Dirichlet kernel has finitely many peak centers in each DLI factor. For a
truncation height `T`, decompose each peak neighborhood into dyadic annuli

```text
2^{-r-1} < dist(theta, peak) <= 2^{-r}
```

down to the reciprocal scale used by the truncation. Each annulus is a union
of at most two intervals, so Erdos-Turan controls its empirical mass by its
circle mass plus the same discrepancy error.

The truncated logarithmic loss is a bounded linear combination of superlevel
set indicators by the layer-cake identity

```text
min(F,T) = int_0^T 1_{F >= u} du.
```

Therefore the annular interval bounds control the empirical average of the
truncated logarithmic loss. The residual below the smallest annulus is the
peak-mass tail term, also controlled at the reciprocal truncation scale.
Summing over DLI factors gives the advertised total error.

## Non-Claims

This packet proves only the deterministic Erdos-Turan and annulus transfer. It
does not prove the finite-frequency Weyl-sum bounds themselves.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_dli_et_peak_mass_reduction.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_dli_et_peak_mass_reduction.py \
  --check experimental/data/certificates/dli-et-peak-mass-reduction/dli_et_peak_mass_reduction.json
```

The verifier checks note anchors and a toy annular-discrepancy budget schema.
