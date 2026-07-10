# Partial U_paid ledger for `cor:capfr1-Q-R1-closing`

## Claim

At the four deployed adjacent rows, the one-step closing corollary

```text
U_paid(a0+1) + U_Q(a0+1) + U_R1(a0+1) <= B_* < L(a0)
```

names a paid summand `U_paid(a0+1)` that is **not** supplied as a single
integrated integer.  This packet constructs a **per-cell** ledger of every paid
cell the corollary's compilers cite, and for each cell either:

1. an exact integer from a proved formula, or
2. a named open input that blocks a finite integer.

## Status

`EXPERIMENTAL / PARTIAL-LEDGER`.

This is **not** a proof of the one-step inequality, **not** a complete
`U_paid` certificate, and **not** a resolution of `prob:band` /
`prob:capfr1-normalized-band`.

## Parameters

| row | a0 | a0+1 | n | k | B_* model |
|---|---:|---:|---:|---:|---|
| KoalaBear MCA | 1116047 | 1116048 | 2^21 | 2^20 | floor(p^6 / 2^128) |
| KoalaBear list | 1116046 | 1116047 | 2^21 | 2^20 | floor(p^6 / 2^128) |
| Mersenne-31 MCA | 1116023 | 1116024 | 2^21 | 2^20 | floor(p^4 / 2^100) |
| Mersenne-31 list | 1116022 | 1116023 | 2^21 | 2^20 | floor(p^4 / 2^100) |

## Cell catalog (value-or-blocker)

| cell | paying theorem | deployed a0+1 status |
|---|---|---|
| C1 tangent/deep | `prop:capf-tangent` | **UNAVAILABLE** — `r = n-(a0+1) >> R_tan = floor((n-k)/3)` |
| C2 common-support | `def:paid-cells` (ii) | **EXACT 0** on MCA; list CA form **BLOCKED** |
| C3 quotient-pullback | `def:capf-quotient-status` | **BLOCKED** — missing declared scale set `C` and coverage hypothesis |
| C4 prefix-boundary | `def:paid-cells` (iv) | **CHARGED TO U_Q** (not U_paid) |
| C5 planted/GCD | `def:paid-cells` (v) | **BLOCKED** |
| C6 shift-pair SP | `thm:q-implies-sp` | **BLOCKED** (needs sharp Q) |
| C7 extension-pole | `prop:capf-extension` | **BLOCKED** — no chart list; ExtPole is a lower floor, not an upper |
| C8 SPI / Conjecture-F | `prob:capfpr-A` | **BLOCKED** |
| C9 sunflower/planted layers | `prob:capfpr-A` | **BLOCKED** |

## Partial sum

```text
U_paid^computable(a0+1)  =  sum of EXACT cells only
                         =  0   on each MCA deployed row
                         =  0   on list rows as well (no EXACT list paid cell lands)
```

Gap `B_* - U_paid^computable` equals `B_*` itself.  This does **not** close the
inequality: blocked cells may still contribute positive mass, and `U_Q`, `U_R1`
are separate residual summands (see the companion `w23-uq-ur1-bounds` packet).

## Oracle gates

- Tangent closed form `r+1` under `3r <= n-k` on small rows; range-fail when
  outside.
- Quotient `U_sum` binomial product **≥** exact support-union enumeration on
  `n <= 16` (union bound is falsifiable if sum under-counted).

## Dual routes

| quantity | generator route | checker route |
|---|---|---|
| tangent | `r+1` under `r <= floor((n-k)/3)` | equivalent `3r <= n-k` + value `n-A+1` |
| L(a0) | ascending `comb_batch` | descending product `n(n-1).../k!` |
| quotient toy | `math.comb` double sum | residual-class DP recompute |
| B_* | `q_line // 2^lambda` | same floor, independent recompute |

## Ledger impact

Narrows the missing-input map for `cor:capfr1-Q-R1-closing`: the paid side is
not a single missing integer — it is a cell-wise map whose only currently exact
MCA entry is common-support 0, with tangent out of range at the frontier
agreements and every structural paid cell still open.

## Reproducibility

```text
py -3.13 experimental/scripts/verify_upaid_ledger.py --emit --check
py -3.13 experimental/scripts/verify_upaid_ledger_check.py --check
```

## Weave with first-match ledger (in-base)

Under the *different* first-match decomposition of the integrated certificate
`kb-mca-1116048-first-match-ledger-v1` (integrated at 0955594), the same
deployed MCA row raw-pays terminal dyadic quotient rungs (471,447,040) and a
generated-field image-cell cover (143,763,024,447,376) with lower rungs open.
Therefore the claim that the only exact paid MCA entry in *this* packet's
paid-cell map is common-support 0 is **route-scoped** to the
`cor:capfr1-Q-R1-closing` cell catalog — not a claim that no proved paid mass
exists under any first-match decomposition.
