# Paid Ledger Functions

Status: PROVED-COMPILER-ARITHMETIC / CITED-LEDGER INTERFACE.

This note packages three required-path DAG nodes as a small compiler layer:

```text
paid_tan_fn
paid_quot_fn
paid_ext_fn
```

The point is not to prove the missing aperiodic theorem.  The point is to make
the already-paid terms in a v12 threshold packet into typed, computable
functions with explicit proof status:

```text
Paid_tan(A)   high-agreement tangent/common-line cell;
Paid_quot(A)  quotient support/image cell, with zone-b cells interval-valued;
Paid_ext(A)   extension-only cell, zero for generating rows and chart-counted otherwise.
```

The companion verifier is:

```text
python3 experimental/scripts/verify_paid_ledger_functions.py
```

It emits:

```text
experimental/data/certificates/paid-ledger-functions/paid_ledger_functions.json
```

## Convention Block

```text
object:              support-wise MCA / CA / finite-parameter curve ledgers
agreement:           integer A
closed radius:       r = n - A
line denominator:    q_line
generated field:     q_gen
target:              epsilon*
budget:              B_* = floor(epsilon* q_line)
status discipline:   exact values, safe upper bounds, or intervals; no silent point estimates
```

The functions below are ledger cells.  A consumer packet may add them only after
checking that the relevant branches are disjoint or after applying its own
deduplication rule.  This note does not itself prove global exhaustion of all
bad parameters.

## 1. Tangent Function

For a Reed--Solomon row `RS[F,D,k]` with `n=|D|`, define

```text
r(A) = n - A,
R_tan = floor((n-k)/3).
```

The theorem-backed high-agreement tangent cell is the partial function

```text
Paid_tan^hi(n,k,A) =
    r(A)+1,  if 0 <= r(A) <= R_tan;
    UNAVAILABLE, otherwise.
```

When available, this value is exact for the finite affine support-wise MCA
line numerator in the high-agreement tangent range, and the same integer
appears in the projective/no-loss high-agreement variants cited in the
existing threshold package.  Outside this range the function deliberately
returns `UNAVAILABLE`; a packet must use a different tangent/common-line
theorem or leave the cell open.

Proof.  The high-agreement tangent staircase promoted in Papers B/D gives

```text
LD_sw(C,A) = n - A + 1
```

whenever `n-A <= floor((n-k)/3)`.  The displayed function is just this theorem
with the range check included as part of the type.

For the pinned row `n=512`, `k=256`, `q_line=17^32`, the budget is `6` and

```text
Paid_tan^hi(512,256,506) = 7  > 6,
Paid_tan^hi(512,256,507) = 6 <= 6.
```

This recovers the known high-agreement threshold anchor; it is not a new row
threshold.

## 2. Quotient Function

Let `C` be a finite set of quotient fiber sizes `c | n`.  For an agreement
threshold `A`, Paper D's quotient-support safe sum is

```text
U_sum(n,A,C)
  = sum_{c in C} sum_{B=A}^n
      binom(n/c, floor(B/c))
      binom(n - c floor(B/c), B - c floor(B/c)).
```

This is always a safe support-level upper numerator for quotient-remainder
witnesses in the declared divisor family.  If an exact block-profile
coefficient extraction is available, the sharper exact support union
`U_supp(n,A,C)` may replace it.  If an lcm quotient-image certificate is
available, the exact distinct-parameter numerator

```text
deg R_T^{(1)}          affine finite-line cell,
deg R_T^{proj}         projective-line cell,
deg R_T^{(d)}          degree-d finite-parameter curve cell
```

may replace the support count.

Thus the safe quotient function is a status-valued cell:

```text
Paid_quot(n,A,C; cert) =
  EXACT_IMAGE(deg R)        if an image lcm certificate is supplied;
  EXACT_SUPPORT(U_supp)     if the block-profile union is supplied;
  SAFE_SUM(U_sum)           otherwise.
```

In every case the printed upper bound is theorem-backed.  A support count is
not the same as a distinct-slope count; it is conservative until the image lcm
certificate is present.

### Zone Tags

For the unsafe/lower quotient side, the same cell must carry a zone tag.  At
quotient order `N'` and rate `rho`, set

```text
ell' = rho N' + 1.
```

The norm-exact gate used in the proof sketch is

```text
(2 ell')^(N') <= q_line^2,
```

equivalent to `(N'/2) log(2 ell') <= log(q_line)` when `N'` is even.  The
quotient lower cell is therefore:

```text
ZONE_A_NORM_EXACT       if the norm-exact gate holds;
ZONE_B_COLLISION_OPEN   if the gate fails and no cap/floor theorem decides the cell;
ZONE_C_CAP_FLOOR        if a Paper-D cap/floor theorem supplies the unsafe mass.
```

The key compiler rule is that `ZONE_B_COLLISION_OPEN` is interval-valued.  It
must be printed as a lower/upper interval or as a named conditional cell, never
as a point estimate.  This is the proof-status content of `paid_quot_fn` that
prevents M4 tables from silently treating the quotient collision wall as
settled.

## 3. Extension Function

Let `B` be the generated field of size `q_gen`, and let the affine line
parameters be sampled from a field `F` of size `q_line`.

### Generating Rows

If

```text
q_gen = q_line,
```

there is no proper extension-only line-parameter cell:

```text
Paid_ext^only = 0.
```

This is the `paid_ext_fn` import rule in its simplest form.  Extension-valued
lines may still be present in other objects, but there is no extra field layer
to charge beyond the base row's existing ledgers.

### Proper Extension Rows

If `q_gen < q_line`, the lower-side extension-pole mechanism imported from
Paper D maps a base list lower bound `L` to the exact integer numerator

```text
ExtPole(q_line,q_gen,k,L)
  = ceil( L (q_line-q_gen) / (q_line-q_gen + k L) ).
```

This is an unsafe/floor cell, not a safe upper classification.

For safe-side extension charts, choose a `B`-basis of `F`, write
`m=[F:B]`, and suppose a Weil-restricted chart projects into a closed
parameter set of degree at most `Delta` and dimension at most `e` over `B`.
The chart contributes at most

```text
Delta q_gen^e
```

affine extension parameters, normalized by denominator `q_line=q_gen^m`.
For a family of charts, the conservative safe upper cell is the sum of these
integers, again subject to the consumer packet's deduplication rule.

Proof.  The generating-row statement is the equality of the generated and line
fields.  The pole formula is the extension-pole floor already printed in Paper
D.  The chart upper bound is the affine degree point-count bound over the base
field applied to the Weil-restricted parameter projection.

## Consumer Schema

A packet consuming these functions should print a row like:

```text
agreement A
budget floor(epsilon* q_line)
Paid_tan:   EXACT(value) or UNAVAILABLE
Paid_quot:  EXACT_IMAGE / EXACT_SUPPORT / SAFE_SUM, with zone tags
Paid_ext:   ZERO_GENERATING / EXT_POLE_FLOOR / CHART_UPPER
dedup rule: packet-specific root/support/image coalescing
residual:   named aperiodic or extension chart status
```

The sum of the upper cells is a valid safe-side bound only after the packet
has proved that the cells cover disjoint branches or has applied an explicit
deduplication rule.  The verifier below checks the arithmetic of the functions,
not branch exhaustion.

## DAG Discharge

This note discharges the computable part of:

```text
paid_tan_fn   -> exact high-agreement partial function;
paid_quot_fn  -> safe quotient support/image function plus zone-b interval rule;
paid_ext_fn   -> generating-zero rule, extension-pole floor, chart upper function.
```

The following are not discharged here:

```text
global quotient-periodic exhaustion;
zone-b quotient collision resolution;
aperiodic local limit;
safe-side classification of every extension-valued residual chart.
```

