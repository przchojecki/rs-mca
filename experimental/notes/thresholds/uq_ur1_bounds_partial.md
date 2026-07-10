# Proved brackets on `U_Q` and `U_R1` for `cor:capfr1-Q-R1-closing`

## Claim

Exact finite summands `U_Q(a0+1)` and `U_R1(a0+1)` are missing because they need
open inputs.  This packet supplies the best **proved** upper/lower brackets at
the four deployed adjacent rows (plus an extension tier), and measures how far
those brackets are from the `B_*` budget.

## Status

`EXPERIMENTAL / PARTIAL-LEDGER`.

Not a proof of the one-step inequality.  Not a resolution of `prob:band`.
Replays and quantifies `prop:proper-q-gap`.

## Brackets (deployed a0+1)

### `U_Q`

| side | source | route |
|---|---|---|
| upper A | `thm:q-proper` Johnson one-term | `R_Q ≤ \|B\|^w / (C(m,t)C(n-m,t))`, `t=⌊w/2⌋` |
| upper B | `thm:q-proper` anticode | `R_Q ≤ \|B\|^w / C(n-m+w,w)` |
| lower | identity-prefix pigeonhole | `max fiber ≥ ⌈C(n,m)/\|B\|^w⌉` |

At all four deployed rows the Johnson upper exceeds `B_*` by **~1.66×10^6 bits**
of absolute fiber budget (normalized `log2 R_Q^pack ≈ 1.661e6`), matching
`prop:proper-q-gap` within 0.1.

### `U_R1`

| side | source | status |
|---|---|---|
| upper A | `cor:bc-one-pencil` `⌊n/ω⌋` | **conditional** on chart → one-parameter pencil |
| upper B | `thm:bc-proper` raw `C(n,ω)` | unconditional but MCA-wrong scale (`cor:raw-bc-fails`) |
| lower | — | `0` (no forced residual proved) |

For KoalaBear / Mersenne-31 MCA at `a+`, the conditional one-pencil upper is
**2**, which fits under `B_*`, but **cannot** be used in the closing sum without
the finite chart-decomposition audit (`rem:bc-status-after-moving-root`).

## Distance to closing

```text
unconditional_closing_possible_from_these_bounds = false
reason: U_Q packing upper >> B_*; U_R1 one-pencil is conditional
```

This is the constructive sequel to `prop:proper-q-gap`'s negative: the proved
Q packing bound is a real theorem and is explicitly too weak by a measured
bit-gap; the R1 side is strong only after structural reduction.

## Dual routes

| quantity | generator | checker |
|---|---|---|
| `log2 C(n,k)` | lgamma + forward product | reverse-order product sum |
| anticode | lgamma `C(n-m+w,w)` | reverse product |
| `U_Q` lower | ascending `comb_batch` | descending `C(n,m)` |
| one-pencil | `n//omega` | recompute `n//(n-m)` |
| oracle | brute ES-prefix fibers | independent re-census on a toy |

## Extension tier

Same brackets at `a0+2` for KoalaBear MCA and Mersenne-31 MCA (trend: packing
gap remains ~1.66e6 bits; one-pencil stays 2).

## Reproducibility

```text
py -3.13 experimental/scripts/verify_uq_ur1_bounds.py --emit --check
py -3.13 experimental/scripts/verify_uq_ur1_bounds_check.py --check
```

## Deviations (W24 R2)

The printed `log2` upper bounds used **lgamma / product-sum float routes**
rather than exact-bigint interval arithmetic.  An independent designer-side
exact-bigint recompute confirmed every printed value, so the numbers stand;
this packet does not claim interval-certified floats.
