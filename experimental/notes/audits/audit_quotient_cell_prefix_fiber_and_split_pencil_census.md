# Calibration for SS0.5 and the Quotient Payment: an Explicit Super-Polynomial QUOTIENT-CELL Prefix Fiber, and a Budget-3 Split-Pencil Chart Census (Scroll Branch Empty)

- **Status:** AUDIT / EXPERIMENTAL / calibration (enters no proof).
- **Agent/model:** Claude Fable 5 acting for AllenGrahamHart.
- **Artifact:** verifier `experimental/scripts/verify_quotient_cell_prefix_fiber_floor.py`
  (stdlib-only, fail-closed, exact big-integer decisions; ~3s) + this note.
- **Cross-repo source (SHA-pinned, read-only):**
  `github.com/AllenGrahamHart/rs-mca-prize-dag@8a7ec132` -- nodes
  `critical/nodes/rate_half_cyclic_rotated_prefix_floor` (PROVED; exhaustive
  toy-fixture enumeration + independent backward audit in its packet),
  `background/nodes/rate_half_list_budget_three_quadratic_scroll_full_rank`
  (PROVED), `critical/nodes/rate_half_list_adjacent_crossing` (TARGET;
  budget-3 chamber census, machine-enumerated and independently
  re-enumerated at audit).
- **Positioning:** companion calibration to
  `experimental/notes/rowsharp_q_external_calibration.md`, whose two
  pre-registered falsifier hunts (super-polynomial primitive prefix fiber;
  primitive shift-pair family) both came back NEGATIVE at primitive scales.
  This note supplies the complementary datum: an explicit super-polynomial
  prefix fiber DOES exist **one cell over, in the quotient cell** -- which is
  evidence FOR the ledger architecture, not against (Q).

## 1. What this note contributes

Two machine-checkable objects in the SS0.5 vocabulary, with their cell
assignments stated honestly:

1. an **explicit super-polynomial QUOTIENT-CELL prefix fiber** on rate-1/2
   prize-admissible rows (`n = 2^41`, prime `q ≡ 1 mod 2^41`,
   `q < 2^256`) -- NOT a primitive fiber, and therefore NOT a falsifier of
   (Q); its existence shows the exact quotient payment (hard-input #5,
   "exact extension and quotient payments") is load-bearing, and that
   "primitive" in the SS0.5 falsifier spec is the operative word;
2. a **budget-3 split-pencil chart census** at our row (the
   `prob:saturated-bc` chart-decomposition genre): any 4-codeword witness at
   the Johnson predecessor reduces to EXACTLY 13 chambers, and the
   rank-deficient quadratic-scroll branch is proved EMPTY. 0/13 chambers
   are closed.

## 2. The quotient-cell prefix fiber

For `C = RS[F, D, n/2]`, `c | n/2`, `N = n/c`, a fixed `s`-subset of one
`c`-point fiber of `x -> x^c` (`0 < s < c`), and `1 <= d <= N/2 - 1`,
`m = N/2 + d`, cyclic rotation modulo `Y^N - delta` plus the fixed tail
produces at least

```text
ceil( C(N-1, m) / (N * q^(d-1)) )                        (CR1)
```

distinct codewords agreeing on exactly `n/2 + d*c + s` points; the count is
`s`-independent, so the witness propagates through the residual band.

**Cell assignment (the honest part).** The construction lives on the
quotient of length `N = n/c` with `c > 1`: under the first-match ledger its
fibers are assigned to the **quotient cell**, not the primitive leaf. It is
consistent with, and in fact explains, the negative primitive-scale hunts of
the external-calibration packet: super-polynomial fibers exist and are
PAID -- by the exact quotient payment, not by the primitive envelope.

Two exact instances (both decided by big-integer comparison in the shipped
verifier):

- **Endpoint instance** (`c = 2^33`, `d = 1`, `N = 256`, `m = 129`,
  agreement `k + 2^34 - 1`): fiber floor `> 2^238` (measured 242.65 bits)
  even at `q = 2^256` -- far past the `2^-128` envelope.
- **Cap-row instance** (`c = 2^22`, `d = 2048`, `N = 524288`,
  `m = 264192`): the unsafe criterion `N q^d < 2^128 C(N-1, m)` holds at
  `q = 2^256` with a **75.079624-bit margin**, hence at every admissible
  field under the official cap.

## 3. The budget-3 split-pencil chart census (worked example)

At our rate-1/2 row, any hypothetical 4-codeword list witness at the Johnson
predecessor reduces, via the split-pencil normal form
`A_k b_ij + A_i b_jk = A_j b_ik` (entries degree <= 2) and the Pluecker gate
`b01 b23 - b02 b13 + b03 b12 = 0` (edge polynomials degree <= 4), to
EXACTLY 13 chambers. The rank-deficient quadratic-scroll branch is proved
EMPTY in the source repo:

```text
det C = b01^2 (L12 L03 - L02 L13) != 0
```

in all four quadratic chambers (pendant chambers by exact linear factors;
the quadratic K4-e chamber by the leading Pluecker coefficient,
`det C = -b01^3 [X^2]b23 != 0`). So no super-polynomial primitive
split-pencil family arises in the rank-deficient scroll branch at this row.
**The other chambers are open: 0/13 closed.** The census algebra is
SHA-pinned above and was machine-enumerated and independently re-enumerated
at audit in the source repo; it is cited here, not re-verified by the
shipped script.

## 4. Verification (what the shipped script decides)

`experimental/scripts/verify_quotient_cell_prefix_fiber_floor.py`,
stdlib-only, exact integers in every decision branch (floats only in margin
displays):

- generic pigeonhole-floor exactness self-test;
- the endpoint instance: floor `> 2^238` and `> 2^128` at `q = 2^256`, plus
  the unsafe criterion;
- the cap-row instance: `(CR3)` at `q = 2^256`, margin reported;
- mutation controls (all three must be caught): wrong denominator exponent
  `d-1 -> d`, tightened envelope `2^-128 -> 2^-256`, over-strict field
  exponent `2^256 -> 2^257` at the cap row.

Passes identically under `python3` and `python3 -O`.

## 5. Non-claims (fence)

This note does **not**:

- exhibit a falsifier for (Q) or the SS0.5 envelope -- the fiber is
  QUOTIENT-CELL, not primitive, and is realized on the unsafe side (it
  confirms the envelope architecture),
- claim any primitive-cell statement whatsoever; the primitive leaf is
  untouched,
- prove that no super-polynomial primitive split-pencil family exists --
  only the rank-deficient scroll branch is empty; 13 chambers remain open
  and are not closed here,
- move any threshold (the proved budget-3 bracket at our row is unchanged);
  official score unchanged,
- claim any Grand List / Grand MCA / Proximity Prize result,
- transport to the `n = 2^21` SS0.4 deployed rows (different row family;
  the parametrization mismatch is recorded on the auditing side in
  `REGIME_MAP.md`).

## 6. What this gives the six-input list

- **#5 "exact extension and quotient payments":** a concrete
  super-polynomial quotient-cell fiber on prize-admissible rows = the
  sharpest available demonstration that the quotient payment is
  load-bearing (if the quotient cell were left unpaid, this family alone
  would break the envelope's arithmetic).
- **#1 "row-sharp finite Q / prefix max-fiber certificates":** calibration
  of the falsifier boundary -- (Q)'s primitivity restriction is exactly
  what excludes this family, so falsifier hunts can safely skip
  quotient-reachable scales (as the external-calibration packet's negative
  results already suggest).
- **SS0.5:** a sharpened, honest map of where a counterexample could still
  hide at a determined row (the 13 open budget-3 chambers) and where it
  cannot (the rank-deficient scroll branch; every quotient-reachable
  prefix scale).
