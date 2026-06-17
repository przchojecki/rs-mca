# Tiny Interleaved-List Enumeration Certificate

- **Status:** EXPERIMENTAL / AUDIT.
- **Agent/model:** Codex acting autonomously through AllenGrahamHart.
- **Scope:** This note certifies `experimental/interleaved_list_enum.py`, a tiny
  finite-field enumerator for comparing direct interleaved list counts with the
  trivial product bound.

## Claim Audited

For a prime field `F_p`, a finite domain `D`, dimension `k`, received rows
`U_1,...,U_mu`, and agreement threshold `a`, the script enumerates every
degree-`<k` polynomial over `F_p`.  For each row it records the agreement
support mask

```text
{x in D : P(x) = U_i(x)}.
```

The base list count for row `i` is the number of masks of size at least `a`.
The direct interleaved count is the number of polynomial tuples
`(P_1,...,P_mu)` whose support-mask intersection has size at least `a`.
This exactly matches the column-wise interleaved agreement condition for the
tiny instances enumerated by the script.

The trivial product bound is the product of the base list counts.  Comparing
the direct count with that product gives a finite sanity check for the
interleaved-list overcharge discussed in the L2/Paper C ledger.

## Reproducible Check

The following enumerates two high-degree received rows on the order-8 subgroup
`<2> <= F_17^*`, with dimension `k=3` and common agreement threshold `4`:

```bash
python3 experimental/interleaved_list_enum.py \
  --p 17 \
  --subgroup-generator 2 \
  --subgroup-order 8 \
  --k 3 \
  --agreement 4 \
  --row-polys '0,0,0,0,1;0,0,0,0,0,1'
```

The JSON output mode is intended for later aggregation into certificate
experiments:

```bash
python3 experimental/interleaved_list_enum.py \
  --p 17 \
  --subgroup-generator 2 \
  --subgroup-order 8 \
  --k 3 \
  --agreement 4 \
  --row-polys '0,0,0,0,1;0,0,0,0,0,1' \
  --format json
```

## Limits

The script is deliberately exhaustive and therefore only for tiny parameters.
It does not prove an asymptotic interleaved-list theorem, and it does not
replace the product or GGR-style bounds in Paper C.  Its purpose is to produce
small exact data for guessing sharper finite-length interleaving behavior.
