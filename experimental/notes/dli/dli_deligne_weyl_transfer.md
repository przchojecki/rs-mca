# DLI Deligne-Weil Transfer

Status: PROVED.

Source DAG node: `dli_deligne_weyl_transfer`.

## Statement

If, for every central profile, nonzero frequency, and harmonic `m` in the DLI
ranges, the odd-evaluation phase on each square-root component defines a
geometrically nontrivial bounded-conductor trace sheaf whose conductor budget
has harmonic total `o(t)`, then Deligne/Weil square-root cancellation gives
the finite-frequency Weyl-sum bounds required by
`dli_odd_eval_exponential_sum_bound`.

## Proof

Fix a central profile, a nonzero frequency, and a harmonic `m` in the range
used by the DLI peak-mass reduction. The noncollapse/conductor input supplies
the geometric datum: on each square-root component, the relevant phase is a
geometrically nontrivial trace sheaf of bounded conductor, and the conductor
bounds have harmonic total `o(t)`.

For a geometrically nontrivial trace sheaf on a curve over `F_q`, the
Weil/Deligne Riemann-hypothesis estimate gives square-root cancellation:

```text
|sum_y trace(Frob_y)| <= C(conductor) q^{1/2},
```

up to the bounded contribution from omitted singular points. After dividing by
the component size, this gives a normalized Weyl-sum bound of size
`O(C(conductor) q^{-1/2})`, plus lower-order endpoint terms.

Summing over components and harmonic ranges gives exactly the harmonic error
budget assumed in the predicate. Since that total is `o(t)`, the finite
frequency Weyl bounds needed downstream follow.

## Non-Claims

This packet proves only the standard transfer from geometric nontriviality and
conductor control to Weyl cancellation. It does not prove that the actual DLI
odd-evaluation phases satisfy the noncollapse/conductor input.

## Replay

Regenerate:

```bash
python3 experimental/scripts/verify_dli_deligne_weyl_transfer.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_dli_deligne_weyl_transfer.py \
  --check experimental/data/certificates/dli-deligne-weyl-transfer/dli_deligne_weyl_transfer.json
```

The verifier checks note anchors and a toy conductor-budget schema for the
transfer implication.
