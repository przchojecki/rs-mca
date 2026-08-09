# KoalaBear K3: cell-5 xi=3 pairings 7, 8, and 11

This experimental packet ports the three pinned cell-4
quadratic-resultant/sign-free compilers to the cell-5 four-basis tower at
`c_row_index=6`.  Over `F_2130706433`, all 24 required signed rows for
pairings `7`, `8`, and `11` complete with zero witnesses, zero terminal pair
solutions, and zero unresolved branches.

The run was local-only with `python-flint==0.8.0` and `sympy==1.14.0`; no
source artifact was uploaded to hosted compute.  The certificate pins the
public source DAG commit, three template hashes, and the cell-5 tower and
kernel hashes.  Its normal verifier checks exact row coverage and aggregates;
`--mutations` rejects twelve hostile changes.

```bash
python3 experimental/scripts/verify_kb_mca_v4_433_1b_cell5_xi3_pairings7811_v1.py
python3 experimental/scripts/verify_kb_mca_v4_433_1b_cell5_xi3_pairings7811_v1.py --mutations
```

The mathematical replay requires `sympy==1.14.0`, `python-flint==0.8.0`, and
a checkout of the pinned public DAG commit.  The 24 cases are independently
chunkable through `--indices`; the committed compact row digests exclude only
local timing.

Status is `EXPERIMENTAL_REVIEW_REQUIRED`.  Together with the predecessor
pairings-3/4/5 packet, this independently replays the six cell-5
representatives left by the public pairings-1/2 result.  PR #1152 subsequently
claimed a full `[5,8]` closure through a newer 23-node packet, but its pinned
source commit was not publicly fetchable at the 2026-08-09 audit; the separate
provenance note records the exact failure.  This packet is a reproducible
cross-check, not a replacement for #1152's endpoint and cell-8 transport
nodes.  It is not a v4 ledger payment or a K3 closure.
