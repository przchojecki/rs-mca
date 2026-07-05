# L1 Petal Residue-Kernel Reduction

## Status

CONDITIONAL-ON-LEDGER, with the local implication steps proved.

This packet packages the full-petal growing-defect reduction behind
`petal_residue_kernel_linear_bound`,
`petal_realizable_kernel_injection`,
`petal_squarefree_classification_counting_soundness`, and
`petal_squarefree_classification_ledger_soundness`.

It does not construct the missing squarefree classification ledger and does
not close the primitive L1 image-fiber theorem.

## Setting

Use the full-petal coset-chart notation of
`experimental/notes/l1/l1_coset_chart_residue_bridge_v1.md` and
`experimental/notes/l1/l1_full_list_quotient_proof_program.md`.
For a touched petal set `I`, defect `d`, petal size `ell`, and excess

```text
c = d - ell,
```

write

```text
K_{I,d} = ker(pi_{>d} R_{I,d})
```

for the residue-line kernel controlling full-petal growing-defect extras.

## Proved Local Inputs

1. **Linear kernel ceiling.**  Lemma 13 of the L1 full-list quotient proof
   program gives

   ```text
   dim K_{I,d} <= c + 1.
   ```

   This is the valid ambient-kernel control.  It is deliberately weaker than
   the refuted hope that the kernel dimension is uniformly bounded or trivial.

2. **Realizable-extra injection.**  Lemma 8 and the coset-chart residue bridge
   send every exact realizable full-petal extra injectively to a squarefree
   locator point lying in `K_{I,d}`.

3. **Finite-classification counting.**  If the squarefree realizable locator
   points in a corridor cell are partitioned into charged classes already paid
   elsewhere and finitely many uncharged classes

   ```text
   |C_i| <= A_i n^{B_i},
   ```

   where the number of uncharged classes and the exponents `B_i` are
   independent of `c`, then the total uncharged part is polynomial with
   exponent independent of `c`.

4. **Ledger soundness.**  A complete classification ledger with disjoint
   charged/uncharged records, paid citations for charged records, and
   `c`-independent polynomial bounds for uncharged records implies the
   squarefree classification payload.

These are proof reductions, not searches.

## Conditional Theorem

Assume the remaining payload:

```text
petal_squarefree_classification_ledger_payload
```

namely an actual ledger covering every squarefree realizable locator point in
the residue-line kernels by charged records or uniformly polynomial uncharged
records, with the number of uncharged records bounded independently of `c`.

Then the following chain holds.

```text
petal_squarefree_classification_ledger_payload
  + petal_squarefree_classification_ledger_soundness
    -> petal_squarefree_kernel_classification_payload

petal_squarefree_kernel_classification_payload
  + petal_squarefree_classification_counting_soundness
    -> petal_kernel_realizable_sparsity

petal_kernel_realizable_sparsity
  + petal_realizable_kernel_injection
    -> petal_realizable_extra_uniformity

petal_realizable_extra_uniformity
  + petal_residue_kernel_linear_bound
    -> petal_residue_line_uniformity

petal_residue_line_uniformity
    -> petal_mixed_amplification_step
```

Thus an actual squarefree classification ledger is sufficient to turn the
full-petal growing-defect residue into a uniformly polynomial contribution at
the mixed-amplification step.  The packet isolates the live mathematical
obligation to the ledger itself; the surrounding bookkeeping is proved.

## Proof

The first implication is exactly the ledger-soundness statement: a complete
valid ledger is a charged/uncharged squarefree classification.

For the second implication, apply the finite-classification counting rule in
each corridor cell.  Charged classes are excluded from the uncharged residual
budget because their citations point to already paid ledgers.  The uncharged
part is a finite sum of polynomial bounds with exponents independent of `c`,
so the maximum exponent remains independent of `c`.

For the third implication, the realizable-extra injection maps exact
full-petal extras into the squarefree realizable locator points counted by the
sparsity bound.  An injection cannot increase cardinality.

For the fourth implication, the coset-chart bridge identifies the new
full-petal residue-line contribution with realizable extras inside
`K_{I,d}`.  The linear ceiling `dim K_{I,d} <= c+1` is the ambient accounting
input, while the previous step supplies the required uniform bound on the
actual realized points.  No flatness of the full ambient kernel is used.

Finally, the mixed-amplification transition adds the old excess-`c` layer and
the new residue-line extras at excess `c+1`.  A sum of the old uniform
polynomial bound and the residue-line uniform polynomial bound is still
polynomial with exponent independent of `c`.

## Non-Claims

- This packet does not provide the actual squarefree classification ledger.
- It does not prove polynomial growth for all mixed-petal or growing-defect
  branches without that ledger.
- It does not alter the status of the primitive image-fiber theorem.
- It records a safe route after the fixed-excess and distinct-label full-petal
  paid layers in `cap25_v13_experimental.tex`.

## Reproducibility

Regenerate the dependency certificate:

```bash
python3 experimental/scripts/verify_l1_petal_residue_kernel_reduction.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_l1_petal_residue_kernel_reduction.py \
  --check experimental/data/certificates/l1-petal-residue-kernel-reduction/l1_petal_residue_kernel_reduction.json
```

The verifier is stdlib-only and checks the implication DAG, status labels, and
the unique live payload assumption.
