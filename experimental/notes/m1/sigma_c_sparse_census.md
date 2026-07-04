# sigma_C Sparse-Layer Census

## Claim

The sparse mutual layer `sigma_C` from `tex/towards-prize.tex` can be checked on
finite toy rows by two exact certificate rungs:

1. direct finite-slope brute force for tiny rows, using maximal witness sets;
2. sub-capacity Pade-Hankel closed-ball witnesses for larger q=11/13/17 rows.
3. a stdlib Pade-Hankel sparse-pair scan rung that solves the single finite
   slope unknown per closed-ball shape without materializing the RS codeword
   table.

The q=11/13/17 packet is exact where a row is marked as a trivial-regime theorem
guard or a finite-slope saturation witness.

## Status

AUDIT overall.

PROVED-by-enumeration for the v1 finite rows in
`experimental/data/certificates/sigma-c-sparse-census/sigma_c_sparse_census_toy_rows.json`
and
`experimental/data/certificates/sigma-c-sparse-census/sigma_c_sparse_census_extended_rows.json`.

PROVED for v2 rows whose `exact_path` is `trivial-regime-theorem` or
`pade-hankel-saturation-witness`.

PROVED-by-enumeration for the committed Hankel scan smoke packet
`experimental/data/certificates/sigma-c-sparse-census/sigma_c_sparse_census_hankel_scan_smoke.json`,
which scans all 34,849 sparse pairs for `(q,n,k,r)=(7,6,3,2)` without
materializing the `q^k` codeword table.

AUDIT / PROVED-by-enumeration in lab for
`experimental/data/certificates/sigma-c-sparse-census/sigma_c_sparse_census_q11_q13_r2_hankel_scan.json`,
which records local lab vectorized r=2 Pade-Hankel scans over all 649,201 sparse
pairs for `(q,n,k,r)=(11,10,7,2)` and all 1,864,801 sparse pairs for
`(13,12,9,2)`.  Both rows saturate the finite-slope upper bound.  The committed
checker replays the artifact invariants and the recorded max-pair witnesses.

AUDIT / PROVED-by-enumeration in lab for
`experimental/data/certificates/sigma-c-sparse-census/sigma_c_sparse_census_q17_r2_hankel_scan.json`,
which records local lab vectorized r=2 Pade-Hankel scans over all 9,957,889
sparse pairs for `(q,n,k,r)=(17,16,12,2)` and `(17,16,13,2)`.  The committed
checker replays the artifact invariants and the recorded max-pair witnesses.

EXPERIMENTAL applies only to lab-side search machinery and future rows not
included in this packet.

## Parameters

Endpoint conventions for every row:

```text
agreement radius: r = floor(delta*n)
slope denominator: q_line
slopes counted: finite gamma in F_q only, no projective infinity slope
field ledger: q_gen = q_line = q, q_chal not used
```

| q_gen | q_line | q_chal | n | k | r=floor(delta n) | result | status |
|---:|---:|---:|---:|---:|---:|---:|---|
| 5 | 5 | not used | 4 | 2 | 1 | sigma_C=1 | PROVED-by-enumeration |
| 7 | 7 | not used | 6 | 3 | 1 | sigma_C=1 | PROVED-by-enumeration |
| 5 | 5 | not used | 4 | 2 | 2 | sigma_C=4 | PROVED-by-enumeration |
| 7 | 7 | not used | 6 | 3 | 2 | sigma_C=7 | PROVED-by-enumeration / saturation |
| 7 | 7 | not used | 6 | 3 | 2 | sigma_C=7 | PROVED-by-Hankel-scan smoke row |
| 11 | 11 | not used | 10 | 4 | 3 | sigma_C=3 | PROVED by trivial-regime theorem |
| 11 | 11 | not used | 10 | 4 | 4 | sigma_C=11 | PROVED by saturation witness |
| 11 | 11 | not used | 10 | 4 | 5 | sigma_C=11 | PROVED by saturation witness |
| 11 | 11 | not used | 10 | 2 | 4 | sigma_C=4 | PROVED by trivial-regime theorem |
| 11 | 11 | not used | 10 | 2 | 5 | sigma_C=11 | PROVED by saturation witness |
| 11 | 11 | not used | 10 | 2 | 6 | sigma_C=11 | PROVED by saturation witness |
| 11 | 11 | not used | 10 | 2 | 7 | sigma_C=11 | PROVED by saturation witness |
| 11 | 11 | not used | 10 | 7 | 2 | sigma_C=11 | AUDIT / PROVED-by-lab-Hankel-scan / saturation |
| 13 | 13 | not used | 12 | 6 | 3 | sigma_C=3 | PROVED by trivial-regime theorem |
| 13 | 13 | not used | 12 | 6 | 4 | sigma_C=13 | PROVED by saturation witness |
| 13 | 13 | not used | 12 | 6 | 5 | sigma_C=13 | PROVED by saturation witness |
| 13 | 13 | not used | 12 | 4 | 4 | sigma_C=4 | PROVED by trivial-regime theorem |
| 13 | 13 | not used | 12 | 4 | 5 | sigma_C=13 | PROVED by saturation witness |
| 13 | 13 | not used | 12 | 4 | 6 | sigma_C=13 | PROVED by saturation witness |
| 13 | 13 | not used | 12 | 9 | 2 | sigma_C=13 | AUDIT / PROVED-by-lab-Hankel-scan / saturation |
| 17 | 17 | not used | 16 | 10 | 3 | sigma_C=3 | PROVED by trivial-regime theorem |
| 17 | 17 | not used | 16 | 10 | 4 | sigma_C=17 | PROVED by saturation witness |
| 17 | 17 | not used | 16 | 10 | 5 | sigma_C=17 | PROVED by saturation witness |
| 17 | 17 | not used | 16 | 12 | 2 | sigma_C=2 | PROVED by trivial-regime theorem |
| 17 | 17 | not used | 16 | 12 | 2 | sigma_C=2 | AUDIT / PROVED-by-lab-Hankel-scan |
| 17 | 17 | not used | 16 | 13 | 2 | sigma_C=17 | AUDIT / PROVED-by-lab-Hankel-scan / saturation |
| 17 | 17 | not used | 16 | 12 | 3 | sigma_C=17 | PROVED by saturation witness |
| 17 | 17 | not used | 16 | 8 | 4 | sigma_C=4 | PROVED by trivial-regime theorem |
| 17 | 17 | not used | 16 | 8 | 5 | sigma_C=17 | PROVED by saturation witness |

All rows use prime-field multiplicative subgroups and finite slopes only.

## Existing Paper Dependency

- `tex/towards-prize.tex`, `prob:mutual`
- `tex/towards-prize.tex`, sparse reduction `thm:sparsify`
- `tex/towards-prize.tex`, `lem:line`, `thm:sparse-threshold`, and the
  sub-capacity Pade-Hankel closed-ball formulation from the sparse-sigma audit.

This is adjacent to PR #198 ("Add CAP25 sparse sigma first-layer audit"), which
was closed without merge on 2026-07-03.  The 2026-07-04 refresh showed open PRs
#209--#260.  PR #210 uses related Hankel/coset vocabulary for a different
object; PRs #232--#260 are separate L1/WP/W/QX/X/XR/F/roadmap/DAG packets with
no exact file overlap except `experimental/agents-log.md`; #229 is the direct
predecessor of this sigma_C packet.

## Proof Idea Or Experiment

For v1 rows, the verifier enumerates every sparse pair `(eps1, eps2)` with
`|supp eps1 union supp eps2| <= r`, every finite slope `gamma in F_q`, and every
close RS codeword `z`.  It counts the slope exactly when `eps2|S_z` is not the
restriction of a degree-`<k` RS codeword on the maximal agreement set

```text
S_z = {i in D : eps1_i + gamma eps2_i = z_i}.
```

For v2 rows, the verifier uses the exact sub-capacity Pade-Hankel formulation.
For `m=n-k`, `r<=m-1`, and `|T|=r`, a slope is certified bad for a sparse pair
when

```text
(H_1 + gamma H_2) ell_T = 0
H_2 ell_T != 0
```

The first line gives a radius-`r` proximity witness on `S=D\T`; the second line
is the same-support noncontainment gate.  If a single sparse pair has all
`q_line` finite slopes certified this way, then `sigma_C=q_line` exactly because
no finite-slope count can exceed `q_line`.

The committed Hankel scan rung uses the same equations as the primary scan
kernel: for each sparse pair and closed-ball shape `T`, it computes
`h1_ell` and `h2_ell`, solves the single consistency equation
`h1_ell + gamma*h2_ell = 0` for a finite `gamma`, deduplicates by `gamma`,
then reconstructs the close codeword and maximal witness set before recording
the slope.  The smoke packet proves this no-codeword-materialization path on
the saturated `(7,6,3,r=2)` row.

For the q11/q13/q17 r=2 rows `(11,10,7,r=2)`, `(13,12,9,r=2)`,
`(17,16,12,r=2)`, and `(17,16,13,r=2)`, the lab vectorized scanner applies the
same shape equations over every sparse pair for each row.  The committed
packets are kept compact: they record the full pair count, bad-pair count,
exact `sigma_C` value, and enough extremal witnesses for the stdlib checker to
replay the maximal-witness records.

No symmetry quotient is used. Future GPU searches may use only
finite-slope-preserving upper-triangular reductions before returning candidate
witnesses to an exact verifier; full Mobius reductions are out of scope because
they can move finite slopes to the projective point at infinity.

## Ledger Impact

This extends the exact certificate ladder for the sparse mutual obstruction. It
does not change the Paper D v12 threshold claims and does not feed a
challenge-field soundness division.

## Constants

The trivial-regime rows recover `sigma_C = r` when `2r <= n-k`, matching the
expected tangent-floor check. The new exact saturation rows are:

```text
q=11: (n,k,r)=(10,4,4),(10,4,5),(10,2,5),(10,2,6),(10,2,7)
q=13: (n,k,r)=(12,6,4),(12,6,5),(12,4,5),(12,4,6)
q=17: (n,k,r)=(16,10,4),(16,10,5),(16,12,3),(16,8,5)
```

All q=11/13/17 v2 rows in this packet now have exact finite-row values by
either the trivial-regime theorem guard or a finite-slope saturation witness.

## Requested Row Coverage

The Wave-2 execution target asked for q=11/13/17 fast, mid, long, and
conditional rows.  This packet records exact finite-row values for every listed
row, but the evidence path is not uniform.  Rows marked `full_hankel_scan`
completed all sparse pairs.  Rows marked `saturation_witness` are exact because
one checked sparse pair has every finite slope bad, so the finite-slope upper
bound `sigma_C <= q_line` is met; they do not claim all-pair coverage.  Rows
marked `trivial_guard` use the tangent-floor equality in the `2r <= n-k`
regime.

```text
requested row              tier          sigma_C   evidence path
(11,10,4,r=4)              fast          11        saturation_witness
(11,10,4,r=5)              fast          11        saturation_witness
(13,12,4,r=5)              fast          13        saturation_witness
(17,16,10,r=4)             fast          17        saturation_witness
(17,16,12,r=3)             fast          17        saturation_witness
(11,10,2,r=5)              mid           11        saturation_witness
(13,12,6,r=4)              mid           13        saturation_witness
(11,10,2,r=6)              long          11        saturation_witness
(11,10,2,r=7)              long          11        saturation_witness
(13,12,6,r=5)              long          13        saturation_witness
(17,16,10,r=5)             long          17        saturation_witness
(17,16,8,r=5)              long          17        saturation_witness
(13,12,4,r=6)              conditional   13        saturation_witness

guard row                  role          sigma_C   evidence path
(11,10,4,r=3)              guard         3         trivial_guard
(11,10,2,r=4)              guard         4         trivial_guard
(13,12,6,r=3)              guard         3         trivial_guard
(13,12,4,r=4)              guard         4         trivial_guard
(17,16,10,r=3)             guard         3         trivial_guard
(17,16,12,r=2)             guard         2         trivial_guard + full_hankel_scan
(17,16,8,r=4)              guard         4         trivial_guard
```

Additional full r=2 scan rows, not part of the original fast/mid/long ladder:

```text
(7,6,3,r=2):      sigma_C=7,  pairs scanned 34,849 / 34,849
(11,10,7,r=2):    sigma_C=11, pairs scanned 649,201 / 649,201
(13,12,9,r=2):    sigma_C=13, pairs scanned 1,864,801 / 1,864,801
(17,16,12,r=2):   sigma_C=2,  pairs scanned 9,957,889 / 9,957,889
(17,16,13,r=2):   sigma_C=17, pairs scanned 9,957,889 / 9,957,889
```

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

```sh
python3 experimental/scripts/verify_sigma_c_sparse_census.py \
  --verify-mode extremal-only \
  --check experimental/data/certificates/sigma-c-sparse-census/sigma_c_sparse_census_q11_rows.json
```

```sh
python3 experimental/scripts/verify_sigma_c_sparse_census.py \
  --verify-mode extremal-only \
  --check experimental/data/certificates/sigma-c-sparse-census/sigma_c_sparse_census_q13_rows.json
```

```sh
python3 experimental/scripts/verify_sigma_c_sparse_census.py \
  --verify-mode extremal-only \
  --check experimental/data/certificates/sigma-c-sparse-census/sigma_c_sparse_census_q17_rows.json
```

```sh
python3 experimental/scripts/verify_sigma_c_sparse_census.py \
  --check experimental/data/certificates/sigma-c-sparse-census/sigma_c_sparse_census_hankel_scan_smoke.json
```

```sh
python3 experimental/scripts/verify_sigma_c_sparse_census.py \
  --check experimental/data/certificates/sigma-c-sparse-census/sigma_c_sparse_census_q11_q13_r2_hankel_scan.json
```

```sh
python3 experimental/scripts/verify_sigma_c_sparse_census.py \
  --check experimental/data/certificates/sigma-c-sparse-census/sigma_c_sparse_census_q17_r2_hankel_scan.json
```

The verifier uses only the Python standard library.

## Lab Scaffold

The non-committed GPU/CPU prototype scaffold lives in local-only lab evidence
at `C:\dev\research\rsmca-lab\sigma-census`.  The GPU smoke path is not a
certificate. It checks that GPU close-codeword candidates cover CPU-bad gammas
on sampled extremal pairs; CPU exact arithmetic remains the certificate
authority.

## Non-Claims

- No asymptotic bound is claimed.
- No deployed/prize-band row is claimed.
- The q-split saturation-witness rows are not all-pair enumerations unless they
  are also present in a committed Hankel scan packet.  All saturation rows are
  exact because a single sparse pair reaches the finite-slope upper bound
  `q_line`; only the committed scan-packet rows also claim all-pair coverage.
- Full witness-shape all-pair enumeration for larger non-saturated q=11/13/17
  rows remains future work.
