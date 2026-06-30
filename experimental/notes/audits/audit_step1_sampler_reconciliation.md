# Step 1: reconcile the finite-slope support-wise MCA convention with the official sampler

- **Status:** COMPLETE -- all four items implemented and passing (verifier exits 0:
  4 PASS / 0 PENDING), with the residual judgment calls explicitly flagged (not asserted).
  Closes `towards-prize.md` S1 step 1 ("finish the definition audit against the official
  MCA sampler") on the audit/reconciliation side.
- **Lane:** V (verification / audit), independent of the M1/F1/L1 proof lanes.
- **Branch / PR:** `allen/step1-sampler-audit`.
- **Script:** `experimental/scripts/verify_step1_sampler_reconciliation.py`.

## What this is -- and is NOT

This is a **documented reconciliation**: it lines up our finite-slope support-wise MCA
convention against the survey's official MCA definition, point by point, and verifies
the exact-integer correspondences that hold **unambiguously**. It reuses the
`open-proximity.tex` anchors already recorded by the #147 high-agreement threshold
package (SHA-256 + line numbers there).

It is **NOT** a unilateral certification that our convention equals the official
sampler. Definitional matches that require sign-off against the authoritative
sampler (Def. 4.3) are flagged below as **residual judgment calls**, not asserted.

Row: `C = RS[F_17^32, H, 256]`, `n=512`, `k=256`, `q = q_line = 17^32`, target `2^-128`.

## Correspondence table

| survey MCA element (anchor) | our repo convention | status |
|---|---|---|
| target error `eps* = 2^-128` | gate `floor(|F|/2^128) = 6` | **unambiguous** (verified) |
| affine denominator `|F|` vs projective `|F|+1` | both give `B_Q = 6` ⇒ same `r<=5` safe / `r=6` unsafe cut | **unambiguous** (verified) |
| MCA event `∃ S=S_gamma, |S| >= (1-delta)n` | support `S` of agreement `a = ceil((1-delta)n)`; integer radius `r = floor(delta n)`, `a = n - r` | **unambiguous arithmetic**; the closed-vs-open **endpoint choice** is a convention to confirm |
| endpoint / closed Hamming ball | max safe `r=5` (`a>=507`), first unsafe `r=6` (`a=506`); safe real interval `[0, 6/512) = [0, 3/256)`, transition `3/256` endpoint UNSAFE; max safe closed grid radius `5/512` | **unambiguous arithmetic** (verified); endpoint convention flagged |
| line-decoding bridge `eps_mca(C,delta) <= a/|F|` | M2 bridge `emca = LD_sw / |F|`, reproducing `unsafe <=> LD_sw >= B_Q+1 = 7` | match **in form** (verified); see residual on the slope family |
| grand-challenge rates `{1/2,1/4,1/8,1/16}`, field range `|F| < 2^256` | envelope parameters; `B_Q` ranges up to `2^128 - 1` | **unambiguous** (recorded/verified) |
| support-wise noncontainment `Delta_S((f_1,f_2), C^{≡2}) > 0` | `LD_sw` counts support-wise noncontained finite slopes | **residual judgment call** — predicate-level match (next iteration) |
| line family `F_lines` (finite vs projective slopes) | finite-slope convention; projective variant recorded separately (denominator `|F|+1`) | **residual judgment call** — slope-family match (next iteration) |

## Coverage

| # | item | status |
|---|------|--------|
| 1 | gate: affine vs projective denominator | **done** |
| 2 | endpoint / closed-ball convention | **done** |
| 3 | survey anchors + bridge consistency | **done** |
| 4 | predicate / line-family correspondence | **done** |

**Full coverage (verifier exits 0: 4 PASS / 0 PENDING).** The unambiguous correspondences
are verified; the two residual judgment calls remain documented and explicitly not asserted.

### Verified so far

- **Gate denominators.** `floor(17^32/2^128) = floor((17^32+1)/2^128) = 6`, both bracketed
  by `6*2^128 < . < 7*2^128`, so the affine and projective denominators give the **same**
  `r<=5` safe / `r=6` unsafe cut. The projective variant changes the denominator, not the cut.
- **Endpoint / closed-ball.** With `r = floor(delta n)` and `B_Q=6`: max safe `r=5` (`a>=507`),
  first unsafe `r=6` (`a=506`); the closed real safe interval is `[0, 3/256)` with the
  transition radius `3/256` having an unsafe endpoint, and the largest safe closed grid
  radius is `5/512`.
- **Anchors + bridge.** Target `2^-128`, field range `|F| < 2^256` (so `B_Q` up to `2^128-1`),
  the four rates, and the bridge `emca = LD_sw/|F|` re-deriving the same `>= B_Q+1 = 7` gate.
- **Predicate / line-family.** The survey MCA event `exists S, |S| >= (1-delta)n` matches our
  co-support arithmetic exactly: with agreement `a=|S|` and co-support `r=n-a`,
  `|S| >= (1-delta)n  <=>  r <= floor(delta n)` (checked at the grid radii), and
  noncontainment is a per-support boolean, so the count is over size-`>=a` supports
  (one support pays for `<=1` slope, Paper D v8). The slope family: `|P^1(F)| = |F|+1`, and
  the point at infinity does not move the `5/6` cut (`floor(|F|/2^128)=floor((|F|+1)/2^128)=6`).
  The **definitional** equivalence of the predicate `Delta_S>0` and the finite-vs-projective
  slope family to the official sampler stays a documented residual judgment call, not asserted.

## Honest limit

Every row marked **unambiguous** is an exact-integer fact verified by the companion
script. The rows marked **residual judgment call** (the support-wise noncontainment
predicate, and the finite-vs-projective slope family) are *documented correspondences*
whose definitional equivalence to the official sampler is left to maintainer/author
sign-off — this note does not assert that equivalence.

## Reproduce

```bash
python3 experimental/scripts/verify_step1_sampler_reconciliation.py
```
