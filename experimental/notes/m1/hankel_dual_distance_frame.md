# Hankel Dual-Distance Frame

Status: PROVED.

Source DAG node: `f_dual_distance_frame`.

## Statement

For a flat `P` of locators, a subset `S` of domain points has dependent
evaluation traces if and only if the dual of the evaluation code of `P`
contains a word supported on `S`. Weight-one dual words are common-root
branches, weight-two dual words are twin trace branches, and higher low-weight
dual words are the general sparse-dual obstruction.

If a supported dual word has minimal support, every coefficient on that support
is nonzero. Consequently, if a locator in `P` vanishes on all but one point of
a minimal sparse-dual support, the dual relation forces it to vanish on the
last point as well. This is the closure property used by the support-lattice
descent accounting.

## Proof

Let `ev_x : P -> F` be evaluation at a domain point `x`. The traces
`{ev_x : x in S}` are linearly dependent exactly when there are coefficients
`a_x`, not all zero, such that

```text
sum_{x in S} a_x ev_x = 0
```

as a functional on `P`. This is precisely a dual-code word of the evaluation
code of `P`, with support contained in `S`.

The low-weight interpretations are immediate. A word of weight one means that
one trace functional is zero on all of `P`, so that domain point is a common
root. A word of weight two means that two trace functionals are proportional,
which is the twin case. General low-weight words are the sparse-dual
obstructions.

For a minimal supported dependence, no coefficient can vanish, since deleting a
zero coefficient would give a smaller dependence on the same traces. If a
locator vanishes on every point of the minimal support except one, the dual
relation reduces to the remaining nonzero coefficient times the remaining
evaluation, so the remaining evaluation is also zero. Thus minimal sparse-dual
supports are closed under this vanishing rule.

Finally, if the dual distance is greater than `r`, then no dependent trace set
of size at most `r` exists. Therefore every `r`-subset of traces is in general
position.

## Non-Claims

This packet supplies the linear-algebra dictionary. It does not classify which
Hankel flats have many sparse-dual words, and it does not prove termination of
the descent by itself.

## Replay

```bash
python3 experimental/scripts/verify_hankel_dual_distance_frame.py --emit
python3 experimental/scripts/verify_hankel_dual_distance_frame.py \
  --check experimental/data/certificates/hankel-dual-distance-frame/hankel_dual_distance_frame.json
```
