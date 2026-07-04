# A-closure pilot: W_h torsion census + eliminant feasibility

- **Status:** EXPERIMENTAL computational pilot (feasibility scouting, not a proof).
- **Branch:** `allen/prize-dag-delta`.
- **Verifier / driver:** `experimental/scripts/verify_a_pilot_wh_torsion.py`
  (single Python process, memory ceiling ~2 GB; every result below is
  reproduced by two independent methods inside that one script).
- **Upstream context:**
  `experimental/notes/roadmaps/x83_uniform_square_shift_obstruction_gate.md`
  (square-shift obstruction gate); the census confirms the qualitative X24
  dichotomy at the torsion level.

## What this pilot decides

For the (A)-closure we need, per `h` and per row order `n`, the NON-toral
torsion structure of the obstruction variety `W_h` and the discriminant/eliminant
data at Row-C scale `n = 1024`. This note reports the **feasibility curve**: what
is cheap (the direct root-of-unity census), what is expensive (the variable
eliminant), and hence whether the campaign can lean on a direct eliminant at
`n = 1024` or must use the structural shortcut the proof agent is formalising.

Setup (from X83). A split `2h`-support `R = {x_1,...,x_{2h}}` has locator
`C(X) = prod (X - x_i) = X^{2h} + c_{2h-1}X^{2h-1} + ... + c_0`. The forced monic
degree-`h` square root `S_R` is fixed top-down by dividing by 2; `E_R = S_R^2 - C`
has `deg <= h-1`. The obstructions are `O_i = [X^i] E_R`, `1 <= i <= h-1`; the
constant is `lambda_R = [X^0] E_R`. `W_h = {O_1 = ... = O_{h-1} = 0}`, a cone
(scaling-equivariant), anchored with `x_1 = 1`. Toral (paid-fiber) points:
`R = alpha*mu_h ∪ beta*mu_h`, two full `mu_h`-cosets (only exist when `h | n`).

---

## Task 1 — h = 4 obstruction polynomials (DONE, PASS)

Built the 3 obstructions in the locator-coefficient variables `c_0..c_7`
(monic `c_8 = 1`) directly from the forced top-down recursion. Independent
recomputation (linear solve of `[X^7..X^4] (S^2 - C) = 0` for `s_3..s_0`) gives
byte-identical polynomials — cross-check PASS.

Forced root coefficients:

```
s_3 = c7/2
s_2 = c6/2 - c7^2/8
s_1 = c5/2 - c6*c7/4 + c7^3/16
s_0 = c4/2 - c5*c7/4 - c6^2/8 + 3*c6*c7^2/16 - 5*c7^4/128
```

Obstructions (`#mon` = monomials in `c`):

```
O_3 = [X^3]E = -c3 + c4*c7/2 + c5*c6/2 - 3*c5*c7^2/8 - 3*c6^2*c7/8
              + 5*c6*c7^3/16 - 7*c7^5/128                              (#mon 7)
O_2 = [X^2]E = -c2 + c4*c6/2 - c4*c7^2/8 + c5^2/4 - c5*c6*c7/2
              + c5*c7^3/8 - c6^3/8 + 9*c6^2*c7^2/32 - 15*c6*c7^4/128
              + 7*c7^6/512                                             (#mon 10)
O_1 = [X^1]E = -c1 + c4*c5/2 - c4*c6*c7/4 + c4*c7^3/16 - c5^2*c7/4
              - c5*c6^2/8 + 5*c5*c6*c7^2/16 - 9*c5*c7^4/128 + c6^3*c7/16
              - 7*c6^2*c7^3/64 + 11*c6*c7^5/256 - 5*c7^7/1024          (#mon 12)
lambda = -c0 + c4^2/4 - ... + 25*c7^8/16384                           (#mon 15)
```

**Quasi-homogeneity / degree cross-check (PASS).** With weight `w(c_k)=2h-k`
each `O_i` is isobaric of weight `2h-i`, i.e. in the x-coordinates
`O_i(gamma R) = gamma^{2h-i} O_i(R)`:

| obstruction | x-degree (= 2h-i) | isobaric check |
|---|---|---|
| O_3 (i=3) | 5 | PASS |
| O_2 (i=2) | 6 | PASS |
| O_1 (i=1) | 7 | PASS |
| lambda    | 8 | PASS |

Largest 2-power denominator is `2^{14} = 16384` in `lambda`, matching the X83
clearing exponent `4h-2 = 14`.

**Toral sanity check (PASS).** A fiber pair `R = alpha*mu_4 ∪ beta*mu_4` has
`C = (X^4 - alpha^4)(X^4 - beta^4)`, i.e. `c_1=c_2=c_3=c_5=c_6=c_7=0`,
`c_4 = -(alpha^4+beta^4)`, `c_0 = alpha^4 beta^4`. Every monomial of
`O_1, O_2, O_3` contains at least one of `c_1,c_2,c_3,c_5,c_6,c_7`, so all three
vanish identically; and `lambda = -c_0 + c_4^2/4 = (alpha^4 - beta^4)^2/4`,
a nonzero square when `alpha^4 != beta^4`. Verified BOTH symbolically (in `c`)
and numerically by plugging the explicit `mu_16` cosets `alpha = 1`,
`beta = zeta_16` (so `alpha^4 = 1`, `beta^4 = i`) into the obstruction
expressions: `O_i = 0`, `lambda = (1 - i)^2/4 = -i/2`, a square. PASS.

---

## Tasks 2 & 4 — dyadic torsion census (DONE, PASS)

Method. A `W_h` point with `lambda != 0` is exactly a split `C = C_A * C_B`,
where the two monic degree-`h` halves `C_A, C_B` **share their top `h-1`
coefficients** (all but leading and constant) and differ in the constant. So
enumerate every `h`-subset `A` of `mu_n`, key it by the exact signature
`(e_1,...,e_{h-1})` of its locator, and read off collisions: any two subsets
`A != B` with the same signature, disjoint (a genuine `2h`-support), and
distinct constant give a `W_h` torsion point `R = A u B`. This is the
banked "same-top coefficients" trade test done directly.

Two INDEPENDENT signature engines (must agree):

- **MAIN** — faithful-prime fingerprint (campaign convention, cf.
  `probe_mixedradix_charzero_fiber.py`): pick `P == 1 (mod n)` with
  `P > (2 C(h, h//2))^{phi(n)}`, map `zeta_n -> g` of order `n`; then equal
  fingerprints <=> equal char-0 coefficients (norm bound < P).
- **VERIFIER** — exact cyclotomic-integer arithmetic in `Z[zeta_n]`
  (`n = 2^s`, `Phi_n = X^{n/2}+1`, `zeta^{n/2} = -1`), no modular reduction.

Classification: `R` is TORAL iff both halves `A, B` are single `mu_h`-cosets
(exponents in arithmetic progression, step `n/h`); else NON-toral.

| h | n | subsets C(n,h) | trade-pairs | toral | NON-toral | predicted toral C(n/h,2) |
|---|---|---|---|---|---|---|
| 4 | 16 | 1 820 | 6 | 6 | **0** | 6 |
| 4 | 32 | 35 960 | 28 | 28 | **0** | 28 |
| 4 | 64 | 635 376 | 120 | 120 | **0** | 120 |
| 5 | 16 | 4 368 | 0 | 0 | **0** | 0 |
| 5 | 32 | 201 376 | 0 | 0 | **0** | 0 |
| 6 | 16 | 8 008 | 0 | 0 | **0** | 0 |
| 6 | 32 | 906 192 | 0 | 0 | **0** | 0 |

Both engines agree on every row (fingerprint == exact cyclotomic).

**Findings.**
- **h = 4 (power of two).** Every char-0 dyadic trade is toral. The only
  collisions live in the zero-signature class (`e_1=e_2=e_3=0`), which is
  exactly the set of `mu_4`-cosets (`X^4 + const` has a full `mu_4`-coset of
  roots). Their number is `C(n/4, 2)` (all `n/4` cosets pairwise, all with
  distinct `alpha^4` hence `lambda != 0`): 6, 28, 120 for n=16,32,64 — matches
  the closed form exactly. **NON-toral char-0 torsion is EMPTY**, confirming
  the banked X24 theorem (2-power `h`: char-0 trades = fiber pairs). No
  exception found.
- **h = 5 and h = 6 (not powers of two).** In dyadic torsion `mu_{2^s}` there
  is no `mu_5` or `mu_6` (`h` has an odd factor), so no fiber pairs exist; and
  X24 forbids any other char-0 dyadic trade. The census is **entirely empty**
  at every tested `n`, as expected. (h=6 is the non-prime non-power-of-2 check.)

So the "non-toral torsion structure" the (A)-closure asks for is, at these `h`,
the empty set — the discriminant `D(n, h)` question collapses to certifying
that emptiness persists, which is Task 3.

## Task 3 — eliminant-route feasibility at h = 4 (DONE, PASS + honest blow-up)

Formulation. A split half is `C_A = X^4 + p X^3 + q X^2 + r X + u`; the two
halves of a trade share `(p, q, r)` and differ in the constant. Being a `mu_n`
trade means each half **divides `X^n - 1`**, i.e. the remainder
`rem(X^n - 1, C_A)` (four polynomials `R_0..R_3 in Z[p,q,r,u]`) vanishes. The
toral locus is `p = q = r = 0` (fiber halves `X^4 + const`).

Divisibility-remainder sizes (cheap):

| n | time | remainder deg (= n-3) | #monomials | max coef bits |
|---|---|---|---|---|
| 16 | 0.05 s | 13 | ~46 | 9 |
| 32 | 0.36 s | 29 | ~305 | 22 |
| 64 | 4.5 s | 61 | ~2 146 | 51 |

First variable elimination (remove `u`) at n=16 — **completes**:
`Res_u(R_0, R_1)` is a polynomial in `(p, q, r)` of total degree **58**, 569
monomials, **42-bit** integer coefficients, **content 1** (primitive), and
**irreducible**. It vanishes at the toral origin `(0,0,0)`: the toral locus is
an EMBEDDED component, not a clean polynomial factor. Splitting it off
therefore needs an ideal **saturation** (add `1 - t(p^2+q^2+r^2)`, eliminate
`t`), which is precisely the step that blows up.

Blow-up boundary (measured; reproduce with `--heavy`):
- **second** elimination (remove `r`) at n=16: no termination in > 120 s.
- **first** elimination (remove `u`) at n=32: no termination in > 150 s.

So the direct eliminant does not even close at n=16 (needs the saturation), and
its first step already fails at n=32. This is the feasibility datum: the
eliminant coefficient/degree data at Row-C scale is unreachable by naive
resultants.

## Task 5 — feasibility curve toward Row-C n = 1024 = 2^10

| route | n=16 | n=32 | n=64 | n=1024 (Row-C) |
|---|---|---|---|---|
| **census** (C(n,4) subsets) | 0.01 s / 1.8k | 0.11 s / 36k | 3.4 s / 635k | ~4.6e10 subsets: tens of hours + many-GB signature dict — INFEASIBLE |
| **eliminant** (resultant cascade) | 1st elim ok (deg 58, 42-bit); 2nd elim > 120 s | 1st elim > 150 s | — | hopeless |

Scaling. Census cost grows like `C(n,4) ~ n^4/24`; exact and cheap only to
`n ~ 64-128` (h=4), worse for larger `h`. The eliminant grows worse still
(remainder degree `n-3`, coef bits `~ n`, then a resultant cascade that already
diverges at the second variable for n=16). **Neither brute route reaches
n=1024.**

**VERDICT.** The direct eliminant route is NOT realistic at Row-C scale; even
the exhaustive census tops out two orders of magnitude in `n` below 1024. The
campaign therefore **requires the structural `D(n, h)` shortcut** the proof
agent is formalising. This pilot pins down exactly what that shortcut must
prove, as a checked target:

1. For `h` a power of two, the char-0 dyadic locus of `W_h` is *exactly* the
   `C(n/h, 2)` toral (fiber-pair) points — no non-toral component (verified
   exactly through n=64).
2. For `h` not a power of two, the char-0 dyadic locus of `W_h` is *empty*
   (verified exactly for h=5,6 through n=32).
3. Hence `D(n, h)` reduces to a discriminant/norm certificate that the toral
   locus is reduced and the remaining ideal is trivial (empty), which must be
   produced *structurally* (via the coset/norm description of the
   zero-signature class), not by enumeration or elimination.

## Reproduce

```bash
python3 experimental/scripts/verify_a_pilot_wh_torsion.py           # bounded (~40 s)
python3 experimental/scripts/verify_a_pilot_wh_torsion.py --heavy   # also runs the blow-up steps
```

Every quantitative claim above is emitted with PASS/FAIL by the script, each
via two independent methods (recursion vs linear solve for the obstructions;
faithful-prime fingerprint vs exact cyclotomic arithmetic for the census;
symbolic vs numeric for the fiber sanity check).
