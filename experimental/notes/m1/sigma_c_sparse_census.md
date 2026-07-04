# sigma_C Sparse-Layer Census

## Claim

The sparse mutual layer `sigma_C` from `tex/towards-prize.tex` can be verified
exactly on tiny rows by a direct finite-slope brute force that checks every bad
slope against the maximal witness set `S_z`.

## Status

EXPERIMENTAL / PROVED-by-enumeration for the finite rows in
`experimental/data/certificates/sigma-c-sparse-census/sigma_c_sparse_census_toy_rows.json`
and
`experimental/data/certificates/sigma-c-sparse-census/sigma_c_sparse_census_extended_rows.json`.

## Parameters

Rows currently certified:

| q_gen | q_line | q_chal | n | k | r=floor(delta n) | sigma_C |
|---:|---:|---:|---:|---:|---:|---:|
| 5 | 5 | not used | 4 | 2 | 1 | 1 |
| 7 | 7 | not used | 6 | 3 | 1 | 1 |
| 5 | 5 | not used | 4 | 2 | 2 | 4 |
| 7 | 7 | not used | 6 | 3 | 2 | 7 |

All rows use prime-field multiplicative subgroups and finite slopes only.

## Existing Paper Dependency

- `tex/towards-prize.tex`, `prob:mutual`
- `tex/towards-prize.tex`, sparse reduction `thm:sparsify`

This is adjacent to PR #198 ("Add CAP25 sparse sigma first-layer audit"), which
was closed without merge on 2026-07-03. This is not a theory-note duplicate:
this contribution supplies a CPU exact verifier and JSON certificate for tiny
rows. The 2026-07-03 refresh showed open PRs #209--#222; none is a sigma_C
sparse-census verifier packet.

## Proof Idea Or Experiment

For each sparse pair `(eps1, eps2)` with
`|supp eps1 union supp eps2| <= r`, enumerate every finite slope `gamma in F_q`
and every close RS codeword `z`.

For each close codeword, use the maximal witness set

```text
S_z = {i in D : eps1_i + gamma eps2_i = z_i}.
```

The slope is counted as sparse-MCA-bad exactly when `eps2|S_z` is not the
restriction of any degree-`<k` RS codeword. This avoids the subtle bug of
checking only a smaller witness set when the maximal agreement set fails.

No symmetry quotient is used. Future GPU searches may use only
finite-slope-preserving upper-triangular reductions before returning candidate
witnesses to this exact verifier; full Mobius reductions are out of scope
because they can move finite slopes to the projective point at infinity.

## Ledger Impact

This starts the exact certificate ladder for the sparse mutual obstruction. It
does not change the Paper D v12 threshold claims and does not feed a
challenge-field soundness division.

## Constants

The two trivial-regime rows recover `sigma_C = r` when `2r <= n-k`, matching the
expected tangent-floor check. The tiny row `(q,n,k,r)=(5,4,2,2)` is beyond that
trivial regime and has `sigma_C=4`.  The extended row
`(q,n,k,r)=(7,6,3,2)` is also beyond the trivial regime and has `sigma_C=7`.

## Reproducibility

```sh
python3 experimental/scripts/verify_sigma_c_sparse_census.py \
  --check experimental/data/certificates/sigma-c-sparse-census/sigma_c_sparse_census_toy_rows.json
```

```sh
python3 experimental/scripts/verify_sigma_c_sparse_census.py \
  --row 7,6,3,2,7 \
  --check experimental/data/certificates/sigma-c-sparse-census/sigma_c_sparse_census_extended_rows.json
```

The verifier uses only the Python standard library.

## Lab Scaffold

The migrated non-committed GPU/CPU prototype scaffold lives in local-only lab
evidence at `C:\dev\research\RSMCA\_migration\lab\sigma-census`.  Future
scratch work should use `C:\dev\research\rsmca-lab\sigma-census`.  The migrated
scaffold currently contains:

- `theory.md`, recording the maximal-witness and finite-slope invariants;
- `cpu_reference.py`, an exact direct-definition CPU reference;
- `verify_witness.py`, a witness/certificate rechecker;
- `params.py`, direct-search cost estimates;
- `gpu_kernels.py` and `run_census.py`, a CuPy close-codeword candidate smoke
  path whose outputs are still returned to the CPU maximal-witness checker.

Smoke commands already run locally:

```sh
python C:/dev/research/RSMCA/_migration/lab/sigma-census/run_census.py \
  --backend cpu --row 5,4,2,1,1 --row 5,4,2,2,4 \
  --out C:/dev/research/RSMCA/_migration/lab/sigma-census/runs/tiny_cpu.json

python C:/dev/research/RSMCA/_migration/lab/sigma-census/verify_witness.py \
  --certificate C:/dev/research/RSMCA/_migration/lab/sigma-census/runs/tiny_cpu.json --full

python C:/dev/research/RSMCA/_migration/lab/sigma-census/run_census.py \
  --backend gpu-smoke --row 5,4,2,2,4 \
  --out C:/dev/research/RSMCA/_migration/lab/sigma-census/runs/tiny_gpu_smoke.json

python C:/dev/research/RSMCA/_migration/lab/sigma-census/run_census.py \
  --backend gpu-full-small --row 5,4,2,2,4 \
  --out C:/dev/research/RSMCA/_migration/lab/sigma-census/runs/q5_n4_k2_r2_gpu_full.json

python C:/dev/research/RSMCA/_migration/lab/sigma-census/run_census.py \
  --backend gpu-full-small --row 7,6,3,2,7 \
  --out C:/dev/research/RSMCA/_migration/lab/sigma-census/runs/q7_n6_k3_r2_gpu_full.json
```

The GPU smoke path is not a certificate. It checks that GPU close-codeword
candidates cover CPU-bad gammas on sampled extremal pairs; CPU exact arithmetic
remains the certificate authority. The `gpu-full-small` path is likewise only a
candidate-enumeration accelerator: its q=5 and q=7 outputs were rechecked by
the CPU maximal-witness verifier before the q=7 row was exported to the repo
certificate.

## Non-Claims

- No asymptotic bound is claimed.
- No deployed/prize-band row is claimed.
- No GPU search result is included here.
- This does not close `prob:mutual`; it only supplies the first exact
  replayable census rung.
