# SOV Nonconstant Affine Character Cancellation

Status: PROVED.

Source DAG node: `sov_nonconstant_affine_character_cancellation`.

## Statement

Let `V` be a finite-dimensional affine space over the row field `F`, let `psi`
be a nontrivial additive character of `F`, and let

```text
c(v) = ell(v) + b
```

be an affine-linear map `V -> F` whose linear part `ell` is nonzero. Then, for
every `xi != 0`,

```text
sum_{v in V} psi(xi c(v)) = 0.
```

Consequently, if a forced-root conditioning cell is partitioned into disjoint
affine pieces on which `c(L)=[X^{h-1}]L` is nonconstant affine-linear, plus an
exceptional set `E`, then every nontrivial character sum over the whole cell
has absolute value at most `|E|`.

## Proof

Translate the affine space so that `V` is a vector space plus a base point
`v_0`. Write

```text
c(v_0+u) = c(v_0) + ell(u),
```

where `ell` is a nonzero linear functional on the underlying vector space. For
`xi != 0`, the functional `xi ell` is also nonzero. Hence its kernel has
codimension one, and every value in `F` has exactly `|ker ell|` preimages.

The character sum is

```text
sum_{u in V} psi(xi c(v_0+u))
  = psi(xi c(v_0)) sum_{u in V} psi(xi ell(u)).
```

Since `xi ell` is surjective onto `F`, the second factor is

```text
|ker ell| sum_{a in F} psi(a).
```

A nontrivial additive character sums to zero over the field, so every
nonconstant affine piece contributes zero.

For a disjoint union of such affine pieces plus an exceptional set `E`, the
affine pieces cancel and only `E` remains. Each remaining summand has absolute
value one, so the whole character sum has absolute value at most `|E|`.

## Non-Claims

This packet proves only the finite-field cancellation lemma. It does not prove
that the actual anchored-core conditioning cells admit affine-piece partitions
with budget-small exceptional sets.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_sov_nonconstant_affine_character_cancellation.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_sov_nonconstant_affine_character_cancellation.py \
  --check experimental/data/certificates/sov-nonconstant-affine-character-cancellation/sov_nonconstant_affine_character_cancellation.json
```

The verifier checks note anchors and enumerates nonconstant affine maps over
small prime fields.
