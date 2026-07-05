# L1 Petal Squarefree Classification Ledger Soundness

Status: PROVED.

Source DAG node: `petal_squarefree_classification_ledger_soundness`.

## Statement

Fix a coset-chart corridor cell and let `X` be the set of squarefree
realizable locator points in the residue-line kernel.  Suppose a ledger gives
a disjoint cover of `X` by records of two kinds:

- charged records, each citing an already paid family; and
- uncharged records, each carrying a bound `K_i n^{A_i}` whose exponent
  `A_i` is independent of the excess `c`.

Suppose also that the number of uncharged records is bounded independently of
`c`.  Then the ledger proves the squarefree-kernel classification payload for
that corridor cell.

## Proof

The ledger cover says every point of `X` belongs to exactly one record.
Charged records cite already paid families, so those points are assigned to
the paid side of the squarefree-kernel classification.

Every uncharged record has a polynomial bound with exponent independent of
`c`, and the number of uncharged records is also independent of `c`.  Thus the
uncharged records satisfy the finite classification requirements.  The
separate finite-union counting lemma can then convert those records into a
single `c`-independent polynomial bound whenever a consumer needs the aggregate
uncharged count.

Therefore a complete ledger with the stated charged/uncharged record semantics
is exactly the data required by the squarefree-kernel classification payload.

## Non-Claims

This packet does not construct the squarefree classification ledger, and it
does not certify any proposed list of records.  It only proves that a ledger
with the stated coverage, disjointness, citation, and uncharged-bound
properties is sound for the payload.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_l1_petal_squarefree_classification_ledger_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_l1_petal_squarefree_classification_ledger_soundness.py \
  --check experimental/data/certificates/l1-petal-squarefree-classification-ledger-soundness/l1_petal_squarefree_classification_ledger_soundness.json
```

The verifier checks the proof anchors and a small ledger-semantics sample.
