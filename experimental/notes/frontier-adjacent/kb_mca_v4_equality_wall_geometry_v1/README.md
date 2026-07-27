# KoalaBear K3 normalized equality-wall geometry

```yaml
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
agreement: 1116048
B_star: 274980728111395087
architecture: normalized Q=6,u=2 equality-wall geometry
partition_digest: N/A - local reduction inside the inherited declared residual
atom_or_cell: normalized fixed-domain rank-16 equality-wall branch
quantifier: every packet admitted by the parent normalization theorem
projection_and_unit: distinct affine bad slopes per received line
direct_statement: reduce the normalized fixed-domain branch to the Q=6,u=2 plane/conic/quartic image-degree split
status: PROVED_LOCAL_REDUCTION
impact: ROUTE_REDUCTION_ONLY
falsifier: a replay-valid admitted packet outside the exhaustive image-degree split
```

## Status

This packet is stack layer 3 of 4. It consumes:

```text
branch: review/kb-equality-wall-normalization-v4
commit: 065f347a96c91ade7d80df8bf324f646329c623e
```

It proves the geometric reduction from the five surviving low-excess
split-scroll degrees to the normalized `Q=6,u=2` coefficient-map and
line/conic/quartic image-degree split. The conic `P3+C3` common-signature
family remains the sole target of the child packet.

## Proof spine

The exact reductions are:

1. regular GRS/MDS deficit and complement-locator interpolation;
2. homogeneous resultant and minimum-window coefficient-curve reduction;
3. source-partition Cremona descent and its star/hypercohomology form;
4. reciprocal-Cauchy, periodicity, grouped-component, and
   Cayley-Bacharach reductions;
5. pole-disjoint conic support and facet-collinearity reductions; and
6. the exact `Q=6,u=2` coefficient-map/star-configuration reduction.

The generated orbit certificate is compact. It stores the complete input
digest, orbit and stabilizer histograms, ordered representative digests, and
the complete sorted-output digest. The classifier regenerates the full
11,130-case universe for each of the four declared pole-cycle partitions.

## Evidence boundary

**Proved exact reductions:** the proof chain and exact finite classifiers
whose admitted universes are derived in the notes.

**Finite certified evidence:** the synthetic normalized-model C++ search and
its frozen output. This search is explicitly not a deployed-field theorem.

**Open residue:** the child `P3+C3` exclusion and all downstream global
owner/partition accounting.

## Layout

```text
proof/         load-bearing mathematical notes
target/        exact open subtargets and guardrails
verification/  deterministic verifiers and compact certificates
experiments/   normalized-model search and orbit classifier
replay.py      portable quick, full, and full-search replay
REPLAY.ps1     Windows wrapper for replay.py --full
```

## Portable replay

From the repository root:

```bash
python3 experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/replay.py --quick
python3 experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/replay.py --full
python3 experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/replay.py --full-search
```

`--quick` validates committed certificates, regenerates the compact orbit
classification, and verifies the frozen C++ artifact. `--full` adds every
semantic tamper suite. `--full-search` also compiles and executes the C++20
search and compares its output with the committed report. Child Python
processes use `sys.executable`; every verifier and the driver refuse optimized
execution.

## Nonclaims

This packet produces no cap `68`, `U_Q`, `U_BC`, `U_new`, global chart
census, complete K3 slope payment, KoalaBear row certificate, or active
endpoint movement. It does not derive a global pencil-chart census or
aggregate a fixed-union transverse-secant payment.
