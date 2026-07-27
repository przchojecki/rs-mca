# Lean/source correspondence: KoalaBear v4 tangent-plus-deep adapter

## Package boundary

`KbMcaV4TangentDeepOwnerAdapter.lean` imports only `Std`. It formalizes the
finite first-match order, the deep/tangent frontloading identity, and deployed
integer arithmetic. It does not replace the source theorems below.

## Tangent source theorem

The active tangent owner is supplied by:

```text
experimental/rs_mca_thresholds.tex
experimental/lean/rs_mca_thresholds/RsMcaThresholds/ExactSparsification.lean
experimental/notes/frontier-adjacent/kb_mca_v4_tangent_source_adapter_v1.md
```

One public first SP3 translation is fixed for the complete received line. The
translation preserves the bad-slope set, and its coordinate-ratio image has at
most `n-a=981104` distinct slopes.

## Deep source theorem

For a bad slope with an exact noncontained agreement witness, let `E_z` be the
actual nonzero error support. Set

```text
r* = floor((n-k)/3) = 349525
A* = n-r* = 1747627.
```

If `|E_z| <= r*`, the same codeword explains the line point on
`D \ E_z`, and noncontainment persists when the witness support is enlarged.
The slope is therefore MCA-bad at agreement `A*`. The exact deep numerator
gives at most

```text
r*+1 = 349526
```

such finite slopes on every received line.

The source proof is recorded in:

```text
tex/cs25_cap_v12.tex
experimental/rs_mca_thresholds.tex
experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md
experimental/notes/m1/m1_kb_branch3_deep_ccl_tdd_v1.md
```

The owner predicate is intrinsic existence of one valid witness with
`|E_z| <= r*`. Its global envelope bound is monotone under every earlier
first-match deletion.

## Frontloading

Write `D` for the intrinsic deep predicate and `T` for the canonical tangent
image. The old local order and new active order have paid unions

```text
(Z intersect D) union ((Z \ D) intersect T)
(Z intersect T) union ((Z \ T) intersect D).
```

Both equal `Z intersect (D union T)`. The Lean theorem
`frontload_tangent_paid_union` checks the pointwise Boolean identity. The
source caps are global envelope caps, so restricting either second cell cannot
increase its charge.

## Declaration map

| Lean declaration | Source claim |
|---|---|
| `firstOwner` | active tangent, deep, Q, BC, complement chronology |
| `activeOwner_cases_of_bad` | exact exhaustion of bad slopes |
| `firstOwner_unique` | constructor-valued first-match uniqueness |
| `frontload_tangent_paid_union` | legacy and active two-owner unions agree |
| `activeDeep_characterization` | active deep is the non-tangent part of the intrinsic deep owner |
| `deployedConstantsExact` | exact deep gate, charges, and remaining budget |

## Proof-status boundary

The package proves no source cardinality theorem by itself. It also does not
transport the rest of the M1 ledger, prove the active Q hypothesis, pay
balanced core, or pay the final complement.

Expected `#print axioms` output:

```text
activeOwner_cases_of_bad       [propext]
firstOwner_unique              []
frontload_tangent_paid_union   [propext]
activeDeep_characterization    [propext]
deployedConstantsExact         []
```

`propext` is Lean's standard proposition-extensionality axiom used by the
`simp` proofs. There are no packet-defined axioms, `sorry`, or `admit`.
