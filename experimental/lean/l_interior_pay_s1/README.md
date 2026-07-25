# `LInteriorPayS1`

Stdlib-only Lean replay for the Mersenne-31 fixed-`G` ordinary-boundary
interior-payment investigation.

The package checks:

- the sharp oversized-list selected-support formulation
  `RSHahn123SelectionGap` and its direct list-level falsifier;
- the exact open integer-target threshold
  `G₃ > 81858218311343544899896663534139630625 /
  389001796223311531724035804630343856388`;
- the stronger closed threshold
  `G₃ >= 40929119489723721648112549908683964625 /
  194500898111655765862017902315171928194`;
- exact positive and negative evidence instances, including the fractional
  zero-moment obstruction to a proof from ordinary Johnson positivity alone;
- the literal all-depth scalar route cut: repeated common-coordinate incidence
  shortening followed by ordinary Plotkin while applicable and the exact
  singleton terminal cap afterward;
- both adjacent-row print-block integers.

The Reed--Solomon-specific gap is a definition, not an asserted theorem.
`native_decide` is used for closed rational/big-integer calculations and the
finite oversized-list evidence instance. Ordinary `decide` is used only for
tiny closed positivity side conditions in power-monotonicity steps. The
quantified incidence and pullback lemmas are direct stdlib proofs. Every theorem
has a `#print axioms` census. There is no Mathlib, `sorry`, or custom axiom.

Replay:

```text
lake build LInteriorPayS1
lake build
```
