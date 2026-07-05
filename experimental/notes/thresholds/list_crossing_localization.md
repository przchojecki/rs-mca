# List Crossing Localization

Status: PROVED.

Source DAG node: `list_crossing_localization`.

## Statement

Use the agreement-index convention of `list_adjacency_closing`: larger index
means a stronger agreement requirement and therefore a smaller list. For every
received word `U`, the list sets are nested:

```text
Lambda(U, delta + 1) subset Lambda(U, delta).
```

Therefore

```text
L(delta) := sup_U |Lambda(U, delta)|
```

is integer-valued and nonincreasing in this agreement-index convention. If
list-window arithmetic supplies a bracket

```text
L(delta_lo) > eps |F|
L(delta_hi) <= eps |F|,
```

then there is a unique first safe integer `delta*` in the bracket with

```text
L(delta* - 1) > eps |F| >= L(delta*).
```

Thus the list-side adjacency problem reduces to finitely many pointwise grid
decisions printed by the list-window arithmetic.

## Proof

For fixed `U`, increasing the agreement index only removes codewords from the
list, so `Lambda(U, delta + 1) subset Lambda(U, delta)`. Taking cardinalities
preserves the inclusion inequality. Taking the supremum over `U` preserves
monotonicity, hence `L(delta)` is nonincreasing and integer-valued.

Given a bracket with `L(delta_lo) > eps |F|` and
`L(delta_hi) <= eps |F|`, define `delta*` to be the first integer in the
bracket satisfying `L(delta*) <= eps |F|`. Existence follows from the upper end
of the bracket. Minimality gives `L(delta* - 1) > eps |F|`, and the definition
gives `L(delta*) <= eps |F|`. This proves the adjacent crossing inequality.

The reduction is purely order-theoretic: it uses nesting, integrality, and the
already-printed list-window bracket, not an asymptotic estimate.

## Non-Claims

This packet proves only the list-side monotone crossing localization. It does
not prove the pointwise list upper certificate, the unsafe lower certificate,
or a deployed row theorem.

## Replay

```bash
python3 experimental/scripts/verify_list_crossing_localization.py --emit
python3 experimental/scripts/verify_list_crossing_localization.py \
  --check experimental/data/certificates/list-crossing-localization/list_crossing_localization.json
```
