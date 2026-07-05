# L1 Petal Realizable-Kernel Injection

Status: PROVED.

Source DAG node: `petal_realizable_kernel_injection`.

## Statement

In the full-petal coset-chart residue bridge, every exact realizable
full-petal extra determines a squarefree missed-core locator point lying in

```text
K_{I,d} = ker(pi_{>d} R_{I,d}),
```

and the assignment is injective for fixed touched set `I` and defect `d`.

## Proof

The coset-chart residue bridge supplies coordinates for full-petal extras.
For a realizable full-petal extra with touched set `I` and defect `d`, there
is an actual missed-core subset `D` and therefore a squarefree locator

```text
L_D(X) = product_{x in D} (X - x).
```

Lemma 8 of `l1_full_list_quotient_proof_program.md`, the full-petal rank
certificate, states that non-planted full-petal extras with the same `(I,d)`
inject into

```text
{ L_D : D subset C, |D| = d } cap K_{I,d}.
```

The residue bridge identifies the high-coefficient constraints for a
full-petal extra with membership in `K_{I,d}`.  Since realizability supplies
an actual subset `D`, every exact realizable extra maps to a squarefree
locator point in that kernel.

If two realizable extras have the same locator `L_D`, then they have the same
missed-core subset `D`.  The fixed `(I,d)` coset chart recovers the same
full-petal extra data from that locator, exactly as in the Lemma 8 injection.
Thus the map is injective.

## Non-Claims

This packet does not bound how many squarefree locator points lie in the
kernel.  It only reduces exact realizable full-petal extras to that
squarefree-kernel counting problem.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_l1_petal_realizable_kernel_injection.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_l1_petal_realizable_kernel_injection.py \
  --check experimental/data/certificates/l1-petal-realizable-kernel-injection/l1_petal_realizable_kernel_injection.json
```

The verifier checks that the Lemma 8 rank-certificate and residue-bridge
anchors are present, then emits the dependency certificate.
