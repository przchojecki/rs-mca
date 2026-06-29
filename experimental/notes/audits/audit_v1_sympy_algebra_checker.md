# Verifier 1 (towards-prize.md A.3): independent algebra checker for the F_17^32 row

- **Status:** IN PROGRESS (coverage grows one A.3 checklist item per commit).
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
| 4 | interpolation | pending |
| 5 | degree bound | pending |
| 6 | agreement count | pending |
| 7 | slope distinctness | pending |
| 8 | noncontainment rank | pending |

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
