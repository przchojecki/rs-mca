# L1 Petal Squarefree Classification Counting Soundness

Status: PROVED.

Source DAG node: `petal_squarefree_classification_counting_soundness`.

## Statement

Fix a coset-chart corridor cell.  Suppose the uncharged squarefree realizable
locator points in the residue-line kernel are partitioned into finitely many
classes

```text
C_1, ..., C_r,
```

where `r` is bounded independently of the excess `c`.  Suppose each class has
a bound

```text
|C_i| <= B_i n^{A_i},
```

where the exponent `A_i` is independent of `c`.

Then the total uncharged squarefree realizable kernel points in that cell are
bounded by a polynomial in `n` whose exponent is independent of `c`.

## Proof

Let

```text
A = max_i A_i
B = sum_i B_i.
```

Since there are only `r` uncharged classes and `r` is bounded independently of
`c`, the maximum exponent `A` is independent of `c`.  The finite sum of the
class bounds gives

```text
sum_i |C_i| <= sum_i B_i n^{A_i} <= (sum_i B_i) n^A = B n^A.
```

Thus the union of the uncharged classes has a polynomial bound with exponent
independent of `c`.

Charged classes are excluded from this uncharged budget because their mass is
paid by their cited external ledgers.  Therefore a finite classification with
uniform class exponents gives the required uniformly polynomial uncharged
count.

## Non-Claims

This packet does not construct the squarefree classification ledger.  It only
proves that, once such a finite ledger exists with the stated uniformity
properties, the uncharged part has a uniformly polynomial count.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_l1_petal_squarefree_classification_counting_soundness.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_l1_petal_squarefree_classification_counting_soundness.py \
  --check experimental/data/certificates/l1-petal-squarefree-classification-counting-soundness/l1_petal_squarefree_classification_counting_soundness.json
```

The verifier checks the proof anchors and runs finite-union inequality samples.
