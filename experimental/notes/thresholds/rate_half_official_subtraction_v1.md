# Rate-1/2 official row: subtraction against thm:official, plus what survives

**Status:** CONCORDANCE (not novelty) ON THE DETERMINED RANGE /
PROVED BRACKET ABOVE THE COMPILER / PROVED MDS ROUTE CUT /
RATE-1/2 BAND OPEN.

This note leads with a **negative result about our own material**, then keeps
only the two pieces that survive it. It is written this way deliberately: we
had a rate-1/2 "determined family" packet drafted, and the subtraction below
is what stopped it going out as a novelty claim.

## Part 1 — the subtraction (the point of the note)

On the official rate-1/2 row `n = 2^41`, `k = 2^40`:

| bound | reach in `B` | as `2^x` |
|---|---|---|
| bare quadratic staircase — the `cor:target` hypothesis `(n-B+1)^2 >= n(k+B-1)` | `B_Q = 389,500,552,609` | `2^38.5028` |
| `thm:official`, `rho = 1/2` — `B <= r_rho^# + 1 = 2^39 - 2` | `549,755,813,886` | `2^39.0000` |

Two things follow, and both are checked exactly by the verifier.

**(a) `B_Q` is exactly your `tab:proth` rate-1/2 entry.** The quadratic reach on
this row is `389,500,552,609`, the same integer already tabulated for rate 1/2
in `tab:proth`. That is not a coincidence — it is the same condition — but it
does mean the quadratic staircase adds nothing to that row.

**(b) `thm:official` strictly dominates the quadratic staircase here**, by

```text
549,755,813,886 - 389,500,552,609 = 160,255,261,277 values of B,
```

i.e. it reaches **41.1% further**. Consequently *any* claim that the rate-1/2
threshold family is "determined" on

```text
2^128 < q < 2^166.503        (equivalently B* = floor(q/2^128) <= B_Q)
```

lies **strictly inside** the range `thm:official` already determines. We
therefore state our determined-family result as **concordance, not novelty**:
it agrees with `thm:official` on a subinterval of the latter's range, and is
self-contained (it does not use the BCIKS half-distance import), but it does
not extend the frontier.

**The residual seam is three values.** Taking the top of our drafted seam
claim, `B = 2^39 + 1`, the values not already covered by `thm:official` are
exactly

```text
B in { 2^39 - 1, 2^39, 2^39 + 1 }        (three values).
```

We are not claiming those three here.

## Part 2 — the bracket above the compiler

For `q >= 2^169` the compiler is **mute**, not merely weaker:

```text
B* = floor(q/2^128) >= 2^41 > n - k - 1 = 2^40 - 1,
```

so the `cor:target` hypothesis `B <= n-k-1` fails outright and `thm:official`
does not apply. In that regime the high-field bracket (HD2) gives

```text
k + 8,594,128,896  <=  a_RH(q)  <=  3n/4 = 1,649,267,441,664       (q >= 2^169).
```

This rests on the published unique-decoding proximity-gap bound together with
the exact MCA half-distance theorem. It is a bracket, not a determination.

## Part 3 — the MDS extension route cut

The exact quadratic staircase does **not** extend to the next radius by an
MDS-only argument. Explicitly, with

```text
C = RS[F_5, {0,1,2,3}, 2],    n = 4,   k = 2,   r = 1,
```

and parity-check column directions `h_x = (1,x)` for `x in {0,1,2,3}`, the
received pair with syndromes

```text
y_0 = (0,1),      y_1 = (1,4)
```

is column-far at radius one and still has **four** CA-bad finite slopes:

```text
y_0 + 1 y_1 = 1 h_0,     y_0 + 2 y_1 = 2 h_2,
y_0 + 3 y_1 = 3 h_1,     y_0 + 4 y_1 = 4 h_3.
```

The verifier replays all four incidences in `F_5`, checks the two syndromes are
independent, and includes a mutation control (perturbing `y_1`) that must break
at least one incidence. This is a route cut of the genre in `agents.md` item 5:
it does not bound anything, it removes an approach.

## What the verifier establishes

```text
RATE_HALF_OFFICIAL_SUBTRACTION_PASS B_Q=389500552609 (== tab:proth rate-1/2)
  thm_official_max=549755813886 domination_gap=160255261277 residual_seam=3
  compiler_applies_at_2^169=False bracket=[k+8594128896,1649267441664]
  mds_fence_bad_slopes=4
```

Exact integer arithmetic throughout; the quadratic reach is obtained by
bisection and checked sharp on both sides (`B_Q` satisfies the hypothesis,
`B_Q + 1` does not).

## Non-claims

- **No novelty is claimed on `2^128 < q < 2^166.503`.** That range is inside
  `thm:official`; Part 1 exists to say so.
- The three-value residual seam `{2^39-1, 2^39, 2^39+1}` is **not** claimed.
- Part 2 is a bracket, not a determination, and imports a published CA bound —
  it is not self-contained.
- Nothing here closes the rate-1/2 band, which remains open.
- No claim at rates 1/4, 1/8, 1/16.
- No list-decoding claim of any kind.
- The `n = 2^21` extension-field adjacent targets are a different lane and are
  untouched.

## Falsifier

An admissible `B <= B_Q` on this row where the quadratic hypothesis fails; a
`B` in `(B_Q, 2^39-2]` where `thm:official` does not in fact determine the safe
set; a `q >= 2^169` with `a_RH(q)` outside the HD2 bracket; or an `F_5` recount
giving other than four CA-bad slopes for the stated pair.

## Provenance

Source packets: `rate_half_quadratic_exact_range` (wave-10 audited, 7
verifiers, 25/25 independent checks), `rate_half_half_distance_safe_bracket`,
`rate_half_postquadratic_mds_extension_fence`. The subtraction in Part 1 was
performed against `proximity_prize_results_v4.tex` at `thm:quadratic`,
`cor:target`, `thm:official` and `tab:proth`.

- Verifier: `experimental/scripts/verify_rate_half_official_subtraction_v1.py`
- Certificate: `experimental/data/certificates/rate-half-official-subtraction-v1/rate_half_official_subtraction_v1.json`
