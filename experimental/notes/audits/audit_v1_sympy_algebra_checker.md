# Verifier 1 (towards-prize.md A.3): independent algebra checker for the F_17^32 row

- **Status:** COMPLETE -- all 8 A.3 checklist items + both hardening checks implemented
  and passing (verifier exits 0: 11 PASS / 0 PENDING). Flagged for review.
- **Lane:** V (verification), independent of the M1/F1/L1 proof lanes.
- **Branch / PR:** `allen/v1-sympy-algebra-checker`.
- **Script:** `experimental/scripts/verify_v1_f17_32_algebra_checker.py`.
- **Row:** `C = RS[F_17^32, H, 256]`, `n = 512`, `k = 256`, `rho = 1/2`.

## What this is

`towards-prize.md` A.3 asks for **two independent** verifiers that must agree:
Verifier 1 (high-level algebra; Sage/Magma/PARI suggested) and Verifier 2
(low-level arithmetic; Rust/C++/minimal Python). The repo's 134 `verify_*.py`
scripts are the bespoke exact-integer stack those two are meant to be checked
*against*, not an independent re-implementation.

Sage / PARI-GP / Magma are **not installed** in the working environment, so this
Verifier 1 builds `F_17^32` on **sympy's `galoistools`** finite-field primitives
(`gf_irreducible`, `gf_mul`, `gf_rem`, `gf_pow_mod`, `gf_gcdex`, `gf_sqf_list`, ...).
sympy ships a native `GF(p)` but no turnkey `GF(p^32)`, so the extension field is
constructed here in ~one screen of code. That hand-rolled field is a **code path
entirely independent** of the repo's hand-rolled arithmetic, which is precisely
what "two verifiers must agree" requires. A `.sage` port of the same checklist is
a natural follow-on for anyone whose stack has Sage/Magma.

## A.3 checklist coverage

| # | item | status |
|---|------|--------|
| 0 | foundational gate / A.1 acceptance | **done** |
| 1 | field construction | **done** |
| 2 | domain construction | **done** |
| 3 | locator splitting | **done** |
| 4 | interpolation | **done** |
| 5 | degree bound | **done** |
| 6 | agreement count | **done** |
| 7 | slope distinctness | **done** |
| 8 | noncontainment rank | **done** |
| H1 | hardening: 2nd-irreducible representation-invariance | **done** |
| H2 | hardening: on-main record cross-checks (tangent506 / strict352 / strict264) | **done** |

**Full coverage reached (verifier exits 0: 11 PASS / 0 PENDING).** All 8 A.3 items plus
both hardening checks (2nd-irreducible invariance; on-`main` board-record arithmetic) pass.

### Already verified (independent recompute)

- **Gate / A.1 acceptance.** `q_line = 17^32`, `floor(q_line/2^128) = 6`,
  `6*2^128 < 17^32 < 7*2^128`, so the bridge gate `LD_sw(C,a) >= 7  <=>
  emca(C,delta) > 2^-128` holds and is agreement-independent.
- **Field construction.** The pinned degree-32 modulus is re-asserted irreducible
  over `F_17` at runtime; distributivity, multiplicative inverse, and the field
  order `a^q = a` (Frobenius/Fermat) all hold.
- **Domain construction.** `v2(17^32 - 1) = 9`, so `|H| = 512 = 2^9` is the **full
  2-Sylow** subgroup of `F_17^32*` (and `1024 \nmid 17^32-1`): the smooth domain is
  not merely assumed but constructible and unique in its 2-part. A deterministic
  order-512 generator is found; the 512 powers are distinct, close (`h^512 = 1`),
  contain `1`, exclude `0`, and the generator has order exactly 512 (`h^256 != 1`).
- **Locator splitting.** A monic locator `L_T(X) = prod_{x in T}(X - x)` is built over
  `GF(17^32)` on a runnable support `T` of 6 distinct `H`-points (the genuine
  "split squarefree locator" object of the F1/M1 program). Verified: degree `|T|`
  and monic; vanishes on all of `T` and on none of 6 disjoint `H`-points; all roots
  simple (derivative `L' != 0` on `T` ⇒ squarefree split, no gcd needed); Vieta ties
  the coefficient prefix to the elementary-symmetric / prefix map `Phi`
  (`[X^5] = -e_1`, `[X^0] = e_6`); negative control catches a doubled root
  (`L` and `L'` both vanish). Extension-field polynomial arithmetic is done locally
  (`pmul`/`pderiv`) since `galoistools` is prime-field only.
- **Interpolation.** On a runnable RS analog over `GF(17^32)` (a degree-`<k`
  message on `k` distinct `H`-nodes), a Vandermonde solve via field Gauss-Jordan
  (`field_solve`) recovers the message coefficients exactly; an **independent**
  Lagrange interpolant agrees with `P` at a fresh point; and interpolating from a
  **disjoint** `k`-node set recovers the same message (uniqueness of the deg-`<k`
  interpolant = RS decode-from-any-`k`-positions). `field_solve` is reused by the
  later noncontainment-rank check.
- **Degree bound (MDS / Singleton).** On `RS[GF(17^32), H, k]` with the real
  `|H|=512` and small `k`: a nonzero degree-`(k-1)` polynomial has exactly `k-1`
  roots in `H`, so two distinct degree-`<k` codewords (built with difference a
  `(k-1)`-root locator) agree on exactly `k-1` of the 512 points -- the bound is
  tight (Singleton achieved). This is the agreement bound underpinning the staircase
  and the meaning of noncontainment. Row in miniature: `k=256` ⇒ distinct codewords
  agree on `<= 255` points, minimum distance `n-k+1 = 257`.
- **Agreement count.** For a received word `w` on the real 512-point domain and a
  planted codeword `P` (deg `<k`), `agreement(w,P) = #{x in H : w(x)=P(x)}` is exactly
  the planted `a` (here `a=300`); the disagreement set has size `n-a` (= error-locator
  degree); `a > (n+k)/2` puts it in the unique-decoding regime; and a distinct codeword
  agrees with `w` on `< a` points (MDS-consistent, observed 2). This is the agreement
  quantity LD_sw counts. **Scope:** agreement for GIVEN codewords -- NOT the
  agreement-`a` codeword *list* (the infeasible LD_sw enumeration).
- **Slope distinctness (dedup).** A bad slope is a deep-point image `z = P(alpha)`; a
  moving family `P_i = P0 + c_i*M` gives slopes `z_i = P0(alpha) + c_i*M(alpha)`. With
  `alpha` outside `H` (a genuine deep point: `alpha^512 != 1`, here `alpha = x`) and
  `M(alpha) != 0`, ten configs give ten **distinct** field slopes, with the injectivity
  reason `z_i - z_j = (c_i - c_j)*M(alpha) != 0` checked pairwise; the dedup negative
  control collapses all ten to one slope at a root of `M`. So a bad-slope *count* is a
  count of distinct field elements, not inflated by duplicates -- faithful to the
  deep-point bridge / moving-root tangent floor. Scope: dedup, not an LD_sw count.
- **Noncontainment rank.** The strict264 rank certificate: a retained slope is
  genuinely noncontained iff the `beta`-column of the Vandermonde at nodes `J u {beta}`
  is independent of the `j` support columns -- i.e. the `(j+1)x(j+1)` Vandermonde
  (rows = degrees `0..j`) is nonsingular, needing redundancy `r >= j+1`. Certified two
  independent ways -- the Vandermonde determinant `prod(node_b - node_a) != 0`, and a
  `field_solve` solve that reconstructs the RHS -- with `beta = x` a deep point outside
  `H`. Negative control: with only `r' = j` rows the `beta`-column IS a combination of
  the `J`-columns (containment), so `r >= j+1` is essential. Runnable miniature `j=4`;
  the row uses `r = n-k = 256`, `j = n-a`.
- **Hardening: 2nd-irreducible invariance.** All the representation-invariant facts
  -- the gate `floor(17^32/2^128)=6`, the field laws (distributivity, inverse,
  `a^q=a`), and `|H|=512` as the full 2-Sylow -- are re-verified under a SECOND,
  independent degree-32 irreducible `MODULUS2 != MODULUS` (re-asserted irreducible at
  runtime). Since `GF(17^32)` is unique up to isomorphism these must not depend on the
  chosen irreducible; confirming it guards against a representation-specific artifact
  in the pinned `MODULUS`.
- **Hardening: on-`main` board records.** Independently recomputes the integer arithmetic
  behind `site/data/frontier.json` for the row: the tangent staircase `LD_sw(C,a)=513-a`
  (so `LD_sw(C,506)=7` unsafe, `LD_sw(C,507)=6` safe), the agreement-independent `>=7`
  gate, and that each record's `badSlopes` is gate-consistent with its `safe/unsafe`
  status -- with the recorded count and the tangent floor agreeing on the gate. The
  tangent-floor records (`tangent257`=256, `reserve272/288/313`=241/225/200,
  `tangent506`=7) match `513-a` exactly; the mechanism records (`cycle116`/`cycle119`
  =52.7B, `strict264`=9, `strict352`=16) clear the same `>=7` gate. **Scope:** recomputes
  the recorded *arithmetic/gates*, not the slope counts by enumeration.

## Honest scope / limits

- Cross-checks the **algebra and the exact-integer gates** independently. Does
  **not** brute-force bad-slope counts over `binom(512, .)` (infeasible for every
  verifier on this row); asserts **no** safety/threshold/list-decoding status.
- The pinned irreducible is an **independent** choice, not yet the frozen A.1 field
  polynomial. Isomorphism-invariant facts (gate, `|H|=512`, field laws) are checked
  now; certificate-**hash** agreement (needs the frozen basis) is a hardening item,
  as is a cross-check under a second irreducible and wiring to the on-`main` records
  (`tangent506-exact-gate`, `strict352`, `strict264-min`).
- `galoistools` is pure-Python: fine for field laws, the gate, and the handful of
  certificate slopes; not for mass enumeration.

## Reproduce

```bash
python3 experimental/scripts/verify_v1_f17_32_algebra_checker.py   # exits non-zero iff an implemented check fails
```
