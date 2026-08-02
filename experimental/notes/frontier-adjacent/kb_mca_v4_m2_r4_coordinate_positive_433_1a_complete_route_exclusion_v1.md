# Positive `433-1a -> O0b` complete route exclusion (aggregation)

**Status:** proved — the complete deployed positive residual route
`433-1a -> O0b` is empty (60/60 raw rows, ten algebraic representatives,
both signed lanes).

**Row:** KoalaBear MCA at `2^-128`, deployed field `F_2130706433`.

**Direct target:** workboard item K3, positive coordinate part of the
residual order-two type with `(m,r)=(2,4)`.

**Quantifier:** every deployed-field positive complete packet in the unique
residual graph route `433-1a -> O0b`, over both signed target lanes and all
60 common matching/root-sign rows.

**Parent:** the exact positive loop cap and residual workboard at commit
`4569b506d7c86b3b7fbca5b22701ef83988e76e8`, and the complete-source outside
reduction at commit `1f5e715a1`.

**Provenance and audit:** the per-cell exclusion proofs were produced by the
Codex worker lineage and audited wave-by-wave into the canonical DAG at
<https://github.com/AllenGrahamHart/rs-mca-prize-dag> (audit notes
`notes/wave24_integration_20260727/WAVE38..41_AUDIT.md`; final integration
commit `2f7604fc`, 2026-08-02). The aggregation node's fail-closed verifier
— which checks all eleven cited PROVED nodes, their dependency edges, and
the census below — was replayed PASS in that canonical checkout on
2026-08-02. This note carries the census, the per-cell mechanism ledger,
and a self-contained arithmetic verifier; the full per-cell proof artifacts
live in the canonical DAG under
`background/nodes/rate_half_kb_m2_r4_coordinate_positive_433_1a_*`.

## 1. The census

Every packet on the route lies in one of **exactly two signed target
lanes** (the O0b signed-edge atlas) and carries one of the **60 common
matching/root-sign rows**. The exact source-projectivity quotient
partitions the 60 rows into ten algebraically distinct representatives:

```text
[0] | [1,2]_(epsilon_1 epsilon_2=+1) | [1,2]_(epsilon_1 epsilon_2=-1)
    | [3,6] | [4,7] | [5,8] | [9,10] | [11] | [12,13] | [14]   (KBPCR-1)
```

with disjoint raw-row coverage

```text
[0]      4 rows      [1,2]    8 rows      [3,6]    8 rows
[4,7]    8 rows      [5,8]    8 rows      [9,10]   8 rows
[11]     4 rows      [12,13]  8 rows      [14]     4 rows
                                          total   60.          (KBPCR-2)
```

Each exclusion is uniform in the signed cycle lane and outside assignment,
or excludes a necessary common/signed-pair subsystem that every such packet
must satisfy. Therefore no row in either signed lane lifts to a complete
packet, and the route is empty.

## 2. Per-cell mechanism ledger (waves 38-41)

| orbit | mechanism (one line) | wave |
|---|---|---|
| `[0]` | generic signed-pair orbit exclusion; all four raw rows empty by root-sign symmetry | 39 |
| `[1,2]` | common root-sign orbit exclusion (both `epsilon_1 epsilon_2` branches); all eight common rows empty | 39 |
| `[5,8]` | the full cell-five program (nine nodes): signed-pair weld/orbit machinery; proves all eight rows | 39 |
| `[3,6]` | genus-3 plane-kernel reduction (degree-8 square-free right side; exact denominator clearing + 16 pseudo-division steps), exceptional scale charts, signed-pair guard factorization | 40 |
| `[4,7]` | genus-1 plane-kernel reduction; signed-pair projection reconstruction; exceptional coefficient projection decomposition + colored exclusion + scale charts; main projection guard factorization | 40 |
| `[11]` | degree-2664 leading norm; the one proper non-scale fiber's twelve displayed roots are all original guards | 40 |
| `[12,13]` | plane-reduced signed-pair resultant factors with `(rd^2 w0 + rn^2)^2`; the one proper compact-scale root has exactly two deployed common points, replayed raw at both — only original guards | 40 |
| `[14]` | resultant factors as `N0 D0^5 (w0+1)^2 (rd^2 w0 - rn^2)(rd^2 w0 + rn^2)`; degree-2752 proportionality norm factored exactly; root-sign symmetry closes all four rows | 40 |
| `[9,10]` | compact cell 9 (lex basis size eleven): signed-pair guard factorization; closure transports to cell 10 | 41 |

Route count across the campaign: 13 routes at wave 38 -> six
representatives / 40 rows at wave 39 -> one representative at wave 40 ->
**zero at wave 41**.

## 3. Adjacent status (audited through the same pin): `433-1b`

Majority-closed at the wave-41 audit pin: the five-role Vieta minor
compiler (60 exact systems, 360 guard-stripped minors), the O0a
signed-edge atlas, the product-rankdrop branch closed end-to-end (common
exception classifier 60 rows; deployed rational classifier 40 finite rows,
32 rationally empty; complete exclusion — 6720 ledgers, all unit), cells
`0` and `1/2` closed, and cell `14`'s quadratic curve structure decomposed
(open exception: the unit chart). Work past that pin is not claimed here.

## 4. Explicitly not claimed

This closes **one coordinate route only**. It does not close the other
rate-half routes, K3, `rate_half_band_closure`, LIST, MCA, or either Prize
problem. Formal orbit representatives are not algebraic survivors, and
target elimination is not source-system elimination; bare resultants remain
only necessary. No alignment branch, positive orientation, order-two type,
owner, payment, or KoalaBear row value is closed by this note.

## 5. Falsifier

An admissible packet outside the two signed lanes or 60 common rows; an
incorrect source-symmetry orbit in `(KBPCR-1)`; a row not covered by
`(KBPCR-2)`; or a guard-valid survivor of any cited orbit theorem.

## 6. Verifier

`experimental/scripts/verify_kb_mca_v4_m2_r4_coordinate_positive_433_1a_complete_route_exclusion_v1.py`
(pure python, no third-party imports, fail-closed): replays the census
arithmetic of section 1 (partition, disjointness, row arity `4|orbit|`,
totals 60/10/2), cross-checks the canonical certificate JSON, and checks
this note's ledger and nonclaim sentences. The per-cell proofs are NOT
re-verified here; they are pinned by node id + closure marker to the
canonical DAG above, where their own verifiers were replayed at audit.
