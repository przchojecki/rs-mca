# Positive `433-1b -> O0a` role cell 14: complete closure

**Status:** proved — role cell `14` of the deployed positive `433-1b -> O0a`
outside atlas is empty: all `1,680` raw outside cases excluded by four
disjoint exact families, retained frontier none. A companion structural
theorem makes the cell-14 kernel normalization global on the guarded curve.

**Row:** KoalaBear MCA at `2^-128`, deployed field `F_2130706433`.

**Direct target:** workboard item K3, positive coordinate part of the
residual order-two type with `(m,r)=(2,4)`, route `433-1b -> O0a`, role
cell `14` of the fifteen-cell atlas.

**Quantifier:** every guarded deployed-field outside packet of role cell
`14`: all `4` source-sign pairs, all `4` target lanes `(sigma_c,
sigma_o)`, all `7` missing outside records, all `15` canonical perfect
matchings of the six residual records.

**Parent:** the `433-1a` complete route exclusion and three-loop atlas at
commit `02d2788f`, and the cell-14 quadratic curve structure decomposition
audited at wave 41.

**Provenance and audit:** the exclusion proofs were produced by the Codex
worker lineage and audited wave-by-wave into the canonical DAG at
<https://github.com/AllenGrahamHart/rs-mca-prize-dag> (audit notes
`notes/wave24_integration_20260727/WAVE42_AUDIT.md` and `WAVE43_AUDIT.md`;
integration commits `7cbedd5d`, 2026-08-02, and `db970533`, 2026-08-03).
Every pinned node's `verify.py` (dag membership, dependency edges, ledger
custody hashes) and independent `verify_audit.py` (coverage census,
hostile count mutations, root-set recomputation) was replayed PASS in that
canonical checkout at audit, together with the manifest harness replay.
This note carries the census, the per-family mechanism ledger, and a
self-contained arithmetic verifier; the full proof artifacts live in the
canonical DAG under
`background/nodes/rate_half_kb_m2_r4_coordinate_positive_433_1b_cell14_*`.

## 1. The census

Write the seven signed outside product records of cell 14 as

```text
y = (de, de, -de, df, sigma_o ef, bf, sigma_c cf).       (KBP1B14C-0)
```

The raw outside ledger is the exact Cartesian product

```text
4 source signs x 4 target lanes x 7 missing records
                x 15 matchings  =  1,680 cases.          (KBP1B14C-1)
```

Matchings are indexed by the canonical first-element recursive
enumeration of the perfect matchings of the six residual records (the
verifier reproduces it); when the missing record is one of the three `de`
records, the two residual `de` records sit at residual positions `(0,1)`,
and indices `{0,1,2}` are **provably exactly** the matchings pairing them
(the verifier re-derives this, both directions). The ledger is tiled by
four **disjoint** proved-empty families:

```text
linear-pair        missing de,      matchings {0,1,2}          144
rank-one           missing df/ef/bf/cf, all 15 matchings       960
fixed-a chain      missing de,      matchings {3,4,5,9..14}    432
all-mixed          missing de,      matchings {6,7,8}          144
                                                     total   1,680.
                                                         (KBP1B14C-2)
```

`3x(3+9+3)x16 + 4x15x16 = 720 + 960 = 1,680`; the three missing-`de`
matching classes are pairwise disjoint with union all fifteen indices.
Retained frontier: **none** — deployed positive `433-1b` cell 14 is
closed.

## 2. Per-family mechanism ledger (waves 42-43)

| family | mechanism (one line) | wave |
|---|---|---|
| kernel normalization (structural) | the interpolation-normalized eight-coordinate kernel's common denominator meets the guarded principal curve in the EMPTY set for all four source signs (route-guard saturated boundary ideals all unit), so the `(-1,1)` normalization is global on the guarded curve, not merely generic | 42 |
| linear-pair (144) | quadratic-pair reduction to one target-free linear equation; 144 open + 1,632 parameter-boundary ideals all unit; timeout-replay custody on the one capped factor | 43 |
| rank-one (960) | rank-one substitution `a f^2 = u v` leaving two free target variables; three exact eliminant classes (32 direct, 448 two-stage, 480 target-free projections); 12,880-incidence deployed-field root census with independent complete root replay; 2,848 direct finite replays, all empty | 43 |
| fixed-a chain (432) | `a` fixed to `+/-B_xi/A_xi`; exact termwise torus substitution; FLINT two-stage eliminants; 9,456-root census with independent field-root replay; 8,736 direct-fiber replays, all empty; 480 target-zero points excluded by guards | 43 |
| all-mixed (144) | complete double resultants in both directions; exact common-factor fiber splitting (960 weighted branches, zero live `f` roots) and factor-removed residual elimination; 2,992-root census with independent replay | 43 |

Every family's census is fail-closed: an omitted, duplicate, non-unit, or
unresolved row fails its audit verifier.

## 3. Adjacent status (audited through the same pin): cell 3

At the wave-43 audit pin the cell-3 branch has the 24-chart compact
curve kernel and the global quadratic quotient (block-lex compression to
one base equation, one palindromic quadratic, one linear recovery), plus
the complete `DE` block: `xi in {0,1,2} x pairing in {0,1,2,3}` = 192 raw
cases proved empty (the `xi=1` cases by exact parallel-edge transport).
Cell 3 remains **open**; work past pin `6bc692e8` is not claimed here.

## 4. Explicitly not claimed

This closes **one role cell of one coordinate route**. It does not close
the other `433-1b` cells, `433-1b -> O0a` or `O0b`, any other rate-half
route, K3, `rate_half_band_closure`, LIST, MCA, or either Prize problem.
All exclusions are exact over the deployed prime `F_2130706433` and are
**not characteristic-uniform**; they do not transfer by themselves to
other role cells or prize rows. Bare resultants remain only necessary;
every degenerate specialization was reopened before exclusion.

## 5. Falsifier

A guarded deployed-field witness in any one of the 1,680 cases; an
omitted Cartesian case; a matching index in `{0,1,2}` that does not pair
the residual `de` records (or one outside `{0,1,2}` that does); a live
boundary discarded by coefficient or torus clearing; a common projection
factor with a live original-equation fiber; or a kernel-denominator zero
on the guarded principal curve.

## 6. Verifier

`experimental/scripts/verify_kb_mca_v4_m2_r4_coordinate_positive_433_1b_cell14_complete_closure_v1.py`
(pure python, no third-party imports, fail-closed): reproduces the
canonical matching enumeration and the `{0,1,2}` classification in both
directions, replays the census arithmetic of section 1 (tiling,
disjointness, family formulas, total 1,680), cross-checks the canonical
certificate JSON (family entries, pinned node ids, provenance commits),
and checks this note's ledger and nonclaim sentences. The per-family
proofs are NOT re-verified here; they are pinned by node id to the
canonical DAG above, where their own verifiers were replayed at audit.
