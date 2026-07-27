# KoalaBear K3 equality-wall normalization

```yaml
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
agreement: 1116048
B_star: 274980728111395087
architecture: normalized source-bound equality-wall split-scroll packet
partition_digest: N/A - local reduction inside the inherited declared residual
atom_or_cell: source-bound equality-wall residual
quantifier: every 69-record packet satisfying the inherited source-bound hypotheses
projection_and_unit: distinct affine bad slopes per received line
direct_statement: exclude the q=1 lower branch and splitting degrees 2 through 11 in the surviving exact-q=2 low-excess branch
status: PROVED_LOCAL_REDUCTION
impact: ROUTE_REDUCTION_ONLY
falsifier: a replay-valid packet in an excluded delta interval or splitting degree
```

## Direct result

The lower range

```text
3912 <= delta < c
```

has pushforward quotient `q=1` and is excluded first. Only after that
exclusion, the surviving low-excess range

```text
c <= delta < e
```

has exact quotient `q=2`. The source-fiber and carrier-incidence bounds then
exclude splitting degrees `2,...,11`. The only surviving low-excess splitting
degrees are `12,...,16`, with the exact intervals printed by the source-fiber
certificate.

The local equality-wall slack is denoted `sigma_wall`; `r` remains reserved
for the deployed Hamming radius.

## Dependency

This is stack layer 2 of 4. Its exact parent is:

```text
branch: review/kb-equality-wall-prerequisites-v3
commit: 702cd8e16673f2971ac1e7898603de2d7d087dfa
```

The imported source-bound prerequisites are consumed from the parent packet.
No mutable GitHub PR status is proof authority.

## Portable replay

From the repository root:

```bash
python3 experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_normalization_v2/replay.py --quick
python3 experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_normalization_v2/replay.py --full
```

`--quick` regenerates and compares the five exact endpoint certificates.
`--full` additionally runs every endpoint tamper suite. The driver uses
`sys.executable` for child processes and refuses optimized execution.

## Nonclaims

This local reduction produces no `U_Q`, `U_BC`, `U_new`, global pencil-chart
census, complete K3 slope payment, KoalaBear row certificate, or active
endpoint movement. It does not aggregate the fixed-union payment of the
transverse-secant packet and does not derive the global chart census missing
from the local pencil route cut.
