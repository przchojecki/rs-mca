# KoalaBear K3: cell-5 xi=3 pairings 3-5

This experimental packet ports the pinned cell-4 reciprocal-square and
nested sign-free compilers to the cell-5 four-basis tower at
`c_row_index=6`.  Over `F_2130706433`, all 20 required signed rows for
pairings `3`, `4`, and `5` complete with zero witnesses, zero final pair
solutions, and zero unresolved branches.

The run was local-only with `python-flint==0.8.0` and `sympy==1.14.0`; no
source artifact was uploaded to hosted compute.  The certificate pins the
public source DAG commit, three template hashes, and the cell-5 tower and
kernel hashes.  Its normal verifier checks exact row coverage and aggregates;
`--mutations` rejects ten hostile changes.

```bash
python3 experimental/scripts/verify_kb_mca_v4_433_1b_cell5_xi3_pairings345_v1.py
python3 experimental/scripts/verify_kb_mca_v4_433_1b_cell5_xi3_pairings345_v1.py --mutations
```

The local mathematical replay requires `sympy==1.14.0`,
`python-flint==0.8.0`, and a checkout of the pinned public DAG commit:

```bash
python experimental/scripts/replay_kb_mca_v4_433_1b_cell5_xi3_pairings345_v1.py \
  --dag-root /path/to/rs-mca-prize-dag \
  --indices all \
  --output /tmp/cell5_xi3_part_0.json
```

The 20 rows are independent and may be replayed in disjoint `--indices`
chunks.  The committed compact row digests are unchanged by local timing.

Status is `EXPERIMENTAL_REVIEW_REQUIRED`.  This is a local K3 route cut, not
a Grande Finale v4 payment.  A fresh reviewer must audit the adapter, all
degree-drop/boundary classifications, the source-role transport, and the
labeled add-back before promotion.
