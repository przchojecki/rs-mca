# L1: the `m*(19) = 9` pin and the excess-`3` atlas (`m = 8` blocked, conditional)

**Type: PROVED (the spine + the equivalence) + PROVED-CONDITIONAL (the pin,
on `H_19`) + AUDIT/PROVED (the atlas localization + two `k3` caps) +
EXPERIMENTAL (extended null evidence) + OPEN (the one named missing input).**

**Result (one line).** `m = 8` is blocked at `ell = 19` — giving the listing
onset `m*(19) = 9` **exactly** — **conditional on, and only on, `H_19` :=
"no realizable `Gamma` at `ell = 19` has `E_3 >= ell+3 = 22`"** (the `ell = 19`
instance of the bounded-excess ceiling `C' <= 2`). The upper bound `m*(19) <= 9`
is the unconditional #364 witness; the lower bound `m*(19) >= 9` is the PROVED
spine (every `m = 8` crossing shape forces `E_3 >= 22`, `excess >= 3`, `T >= 7`,
airtight over all 17,012 crossers) **closed by `H_19`** — the spine itself is
unconditional; ruling out a *realizable* `m = 8` crossing (hence the lower bound
proper) is exactly the step that needs `H_19`. It is **NOT** blocked by the two PROVED
combinatorial caps alone (11,927 shapes survive; explicit falsifier family headed
by `[10,9,9,2^5]`). Lane T1's target *no-realizable-`T >= 7`* is strictly
stronger, implies `H_19`, and blocks every crosser directly.

Companion verifier (stdlib, zero-arg, `--tamper-selftest`, < 1s):
`experimental/scripts/verify_l1_m19_pin_excess3_atlas.py` — 6 gates: the spine
enumeration (17012/11927/59, 0 violations), the excess ladder, the two witness
spectra recomputed from raw `gamma`, the excess-`3` atlas partition for
`ell in {17,19,23,29}`, the two `k3` caps + a symbolic `deg R_zeta = 5`/`X|R_zeta`
check, and the #382 unique-`Gamma` nullspace-dim-`1` crack.

**Notation** (inherited verbatim from the integrated L1 notes). `ell` odd prime,
`ell | p-1`, `n = (p-1)/ell` cosets of `H = mu_ell`; `Gamma(X) =
sum_{r=1}^{ell-1} gamma_r X^r` constant-free mixed; per coset `mu_b` = max fiber
(level-set) size; **spectrum** = the `mu_b` sorted descending; `top-m` = sum of
the `m` largest `mu_b`; **listing threshold `top-m >= 2 ell`**; `E_3 :=
sum_b (mu_b-2)_+`; `T := sum_{k>=3}(mu_k-2)_+` (from the THIRD-largest fiber
onward, the sigma-calculus residual — NOT `#{mu>=3}`); `excess := E_3 - ell`;
`capslack := ell - (mu_1+mu_2) >= 0`. **`m*(ell)` = the listing ONSET: the
smallest `m` at which some realizable `Gamma` crosses `top-m >= 2 ell`.**

**Status legend.** PROVED (proof in an integrated note, cited) / PROVED-HERE
(elementary consequence of PROVED inputs, re-derived + enumerated) / WITNESS
(shipped explicit object) / CONDITIONAL (on the stated hypothesis) / CONJECTURAL
(the hypothesis itself, open) / EXPERIMENTAL (deep sweep, coverage stated) /
AUDIT.

---

## 0. Headline

**THE PIN (PROVED-CONDITIONAL).** `H_19 ⟹ m*(19) = 9` exactly. The `m = 10` and
`m = 11` attainment witnesses (`l1_ell19_attainment.md`, `p = 647`) are **not in
tension**: `m*` is the *onset* (smallest crossing `m`), and those are non-minimal
crossings on the attainment ladder `m = 9, 10, 11` — all listing, onset `= 9`
(the #364 `p = 571` witness crosses first at `m = 9 = (ell-1)/2`, one below the
old `(ell+1)/2 = 10` framing that `l1_ell19_band_refuted.md` #364 already
superseded). The block is **conditional** — 11,927 shapes survive the PROVED
caps — and its exact hypothesis is `H_19`, an instance of `C' <= 2`, which lane
T1 runs in parallel to decide.

---

## 1. Facts pinned from the integrated notes (not from memory)

All quoted/verified from the files named; re-grepped at base
(`upstream/main` @ `53bb5df`).

- **Bridge (PROVED, `l1_prime_ell_frontier_corrected.md` §2.1).**
  `max(mu_b,2) = 2 + (mu_b-2)_+`, so **`top-m <= 2m + E_3`** (and sharper
  `top-m <= m + min(m,a) + E_3`, `a := #{b : mu_b >= 2}`).
- **Pairwise cap (PROVED, `l1_sigma_calculus.md` Lemma 3).** *"For any two fibers
  of one `Gamma`, `mu_i + mu_j <= ell`."* Sorted ⟹ the binding instance is
  `mu_1 + mu_2 <= ell`, hence **`capslack >= 0`**.
- **Lemma R (PROVED, `l1_e3_charsum_paircap.md`).** `sum_b mu_b(mu_b-1) <=
  (ell-1)(ell-2)`; the max-fibers are a subset, so `sum_k mu_k(mu_k-1) <=
  (ell-1)(ell-2)` (`= 306` at `ell = 19`) is necessary.
- **Excess identity (PROVED, `l1_bounded_excess_structure.md` §1, given the cap).**
  `E_3 = (mu_1-2)+(mu_2-2)+T = (mu_1+mu_2)-4+T`, hence **`excess = T - 4 -
  capslack`** — verified there on all six integrated witnesses incl. the one
  non-cap-tight witness. Requires only `mu_1, mu_2 >= 2`.
- **Theorem 1 (PROVED, `l1_sigma_calculus.md` §2A.1).** `T <= 4 ⟹ E_3 <= mu_1+mu_2
  <= ell` (used only to certify the converse below is the live direction).
- **Eligibility (`l1_prime_ell_key_lemma_refuted.md`).** A full `m`-listing needs
  `n >= t+m = 2m-1` cosets to assemble the codeword; for **`m = 8`, `n >= 15`**
  (the note's own `p = 191`, `n = 10`, is "too small to list").
- **`m*(19) <= 9` (WITNESS, unconditional, #364 `l1_ell19_band_refuted.md`).** A
  16-gate `m = 9` listing at `ell = 19, p = 571`, `n = 30 >= 2*9-1 = 17`,
  spectrum `[16,3^6,2^6,1^17]`, `top-8 = 36`, `top-9 = 38 = 2 ell`, `E_3 = 20`,
  `T = 5`. Recomputed here from raw `gamma` over `F_p` — exact match (gate iii).
- **`m*(19)` regularity (WITNESS, #attainment `l1_ell19_attainment.md`).** A full
  `m = 10 = (ell+1)/2` listing at `p = 647`, spectrum `[12,7,4,3,2^10,1^20]`,
  `E_3 = 18`, `top-10 = 38`; a companion `m = 11` listing at the same prime.
  Recomputed here — exact match (gate iii). These are the non-minimal rungs.
- **`T1` = the open core (`l1_bounded_excess_structure.md` §6; #379
  `l1_t7_atlas_concurrency.md`; #365 `l1_e3_dim_syz_crux_refuted.md`).**
  *"no realizable config has `T >= 7`"* — equivalently the uniform ceiling
  `C' <= 2` (`E_3 <= ell+2`). ~~CONJECTURAL~~ **REFUTED globally over `F_p` (2026-07-07)** —
  realizable `T = 7` at `ell = 43`, reaching `T = 10` at `ell = 53` (§6/§7;
  `l1_k3_growth_refutation.md`). The pin needs only `H_19` (the `ell = 19` instance), which is
  **UNTOUCHED** (fat-tail excess `<= +1` there — exhaustive over the five eligible primes
  `n <= 30`, attained only at the `n = 30` boundary; beyond-window `647/761/1103` give `5`).

---

## 2. [PROVED] The Spine Theorem — what a crossing at `m = 8` forces

`m*(19) >= 9` ⟺ **no `Gamma` at `ell = 19` has `top-8 >= 2 ell = 38`.** (Blocking
`m = 8` blocks all `m <= 8`: `top-m <= top-8` for `m <= 8`, so any lower crossing
would already show `top-8 >= 38`; eligibility `n >= 2m-1` is only easier for
smaller `m`, never rescuing one.) The reduction chain, each step PROVED from §1:

```
 top-8 >= 38
   =>[bridge]   38 <= top-8 <= 2*8 + E_3 = 16 + E_3   =>   E_3 >= 22 = ell+3
   =>           excess = E_3 - ell >= 3
   =>[cap: a crossing has mu_2 >= 4 >= 2, so the identity applies]
                T = excess + 4 + capslack >= 3 + 4 + 0 = 7      [capslack >= 0]
```

**Why `mu_2 >= 4` (no crossing is a fat tail).** The six fibers `mu_3..mu_8` are
each `<= mu_2` and supply `top-8 - (mu_1+mu_2) >= 38 - 19 = 19`, so `6 mu_2 >= 19`
⟹ `mu_2 >= 4`. The fat-tail family `[ell-3,3^{k3}]` has `mu_2 = 3`, so it is
excluded — the crossing lives in the multi-big-fiber regime.

> **Spine Theorem (PROVED-HERE).** Every `m = 8` crossing shape at `ell = 19` has
> `E_3 >= ell+3 = 22`, `excess >= 3`, and (realizable) `T >= 7`.

**Full enumeration (gate i).** All descending top-8 profiles `mu_1>=...>=mu_8>=1`
with the pairwise cap and `top-8 >= 38` (cheapest size-1 tail): **17,012
crossers, 0 violations** of the bridge, the identity, `capslack >= 0`,
`excess >= 3`, or `T >= 7`; and `min E_3 = 22`, `min excess = 3`, `min T = 7`,
`min mu_2 = 4` are all **attained**. So the spine is airtight, not a slack bound.
Therefore **`T1 ⟹ no m=8 crossing ⟹ m*(19) >= 9`** directly (a crosser has
`T >= 7`), and the weaker `E_3 >= 22 ⟹ excess >= 3` already suffices.

---

## 3. [PROVED-CONDITIONAL] The pin, and the exact hypothesis hierarchy

> **CONDITIONAL THEOREM.** `H_19 ⟹ m*(19) = 9` exactly; and `T1 ⟹ H_19`.
> *Proof.* `m*(19) <= 9` is the shipped #364 WITNESS (unconditional). For
> `m*(19) >= 9`: any crossing at `m <= 8` has `top-8 >= 38` (monotonicity), hence
> `E_3 >= 22` (Spine Theorem); `H_19` forbids that at `ell = 19` for all `n`, a
> fortiori at eligible `n >= 15`. ∎

**Hierarchy (minimal ⟶ named), stated exactly — not overstated.**
- **`H_19`** := "no realizable `Gamma` at `ell = 19` has `E_3 >= 22`" — the
  `ell = 19`, excess-`3` instance of `C' <= 2`. **Minimal sufficient**: `H_19`
  alone gives `m*(19) >= 9`.
- **`T1`** := "no realizable config has `T >= 7`". Via `excess = T-4-capslack`,
  `T <= 6 ⟹ excess <= 2 ⟹ C' <= 2 ⟹ H_19`. **`T1` is strictly stronger than
  `H_19`**: a realizable `excess = 2, capslack = 1, T = 7` config satisfies
  `H_19`/`C' <= 2` yet violates `T1`. Both suffice; the block needs only `H_19`.
- **Do NOT assume `T1`.** ~~It is CONJECTURAL~~ **it is now REFUTED globally (2026-07-07)**
  (realizable `T = 7` at `ell = 43`, `T = 10` at `ell = 53`; §6/§7). This does **not** affect
  the pin: the pin needs only `H_19` (the `ell = 19` instance, **UNTOUCHED** — exhaustive
  fat-tail excess `<= +1` over the five eligible primes `n <= 30`, boundary-attained at
  `n = 30`), and `T1` was only ever an *optional stronger* route to `H_19`. The pin remains
  stated *conditional on `H_19`*.

**The excess ladder — why `m = 9` is the onset (gate ii).** The bridge gives, at
`top-m >= 2 ell`, `E_3 >= 2 ell - 2m = 2(ell-m)`:

| `m` | needs `E_3 >=` | `= ell +` | needs excess | status at `ell = 19` |
|:-:|:-:|:-:|:-:|---|
| 11 | 16 | `-3` | `-3` | trivial (attainment ladder) |
| 10 | 18 | `-1` | `-1` | **WITNESS** `E_3 = 18` (#attainment) |
| **9** | **20** | **`+1`** | **`+1`** | **WITNESS** `E_3 = 20, T = 5` (#364) — `T < 7` |
| **8** | **22** | **`+3`** | **`+3`** | **needs `T >= 7`** — forbidden by `T1` |
| 7 | 24 | `+5` | `+5` | needs `T >= 9` — a fortiori forbidden |

The onset lands at `m = 9` because the required excess jumps **`+1 -> +3`** across
`m = 9 -> 8` (each `m`-step moves required `E_3` by 2), **stepping over the
observed realizable ceiling `+2`** — which is itself one short (`excess +2 ⟹
top-8 <= 37`). `m*(19) = 9` is exactly the statement that realizable excess tops
out in `[+1,+2]`, i.e. `C' <= 2` at `ell = 19`.

---

## 4. [PROVED] The equivalence and its tightness — same wall as `C' <= 2`

**Not an unconditional block.** Of the 17,012 crossers, **11,927 survive Lemma R**
(`sum mu(mu-1) <= 306`; 5,085 killed), with `min excess = 3`, `min T = 7`,
`mu_2 in [4,9]`, all `mu_3 >= 4`. The two PROVED caps do **not** block `m = 8`.
The **cheapest** falsifier targets are the **59** cap-tight (`T = 7`,
`capslack = 0`, `top-8 = 38`, over-det `= 13`) frontier shapes (gate i); the
**unique `j = 3`** one is **`[10,9,9,2^5]`** — the excess-`3` atlas min-`j` core
`[10,9,9]` (#379/#382) padded with five size-`2` fibers that lift `top-8` from
`33` to `38` while preserving `E_3 = 22`, `T = 7`, `excess = 3`.

**The pin sits exactly at the `C' <= 2` wall — bracketed both sides.**
- *Upper (sufficiency):* `H_19` (no realizable excess-`3` at `ell = 19`) ⟹
  `m*(19) = 9`. `H_19` is an instance of `C' <= 2`.
- *Lower (tightness):* refuting `m*(19) = 9` needs a realizable `Gamma` with
  `top-8 >= 38`, which (Spine Theorem) has `T >= 7`, refuting `T1`/`C' <= 2`. So
  **`m*(19) = 9` cannot be refuted without refuting `T1`**, and a config
  realizing any frontier shape (e.g. `[10,9,9,2^5]` at some `p ≡ 1 (mod 19)`,
  `n >= 15`) does both at once.

**Precise caveat (refines T2's "same question" gloss).** The `m = 8` crossers are
exactly the excess-`3` configs that *also* satisfy `top-8 >= 38` — a **subset** of
"realizable excess-`3`". The fat tail `[16,3^8]` is the excess-`3` object that
would refute `C' <= 2` yet **not** cross `m = 8` (`top-8 = 16 + 7*3 = 37 < 38`).
So `m = 8` and `C' <= 2` share the **same missing input** (§7) and the pin is
sandwiched at that wall — but "refuting `C' <= 2` ⟹ refuting `m*(19) = 9`" is
**false in general** (the fat tail witnesses the gap). The operative claims
(`H_19` suffices; refuting the pin refutes `T1`) both stand.

---

## 5. [AUDIT/PROVED] Atlas localization (lane T1)

The excess-`3` **atlas** = shapes with `E_3 = ell+3` obeying the two PROVED caps.
By the WLOG fiber-deletion reduction (#358, `l1_e3_law_refuted.md` §2: removing a
size-`2` fiber preserves realizability and changes `E_3, T` by `0`),
**`C' <= 2 ⟺ no realizable excess-`3` shape**. Partition (gate iv, regenerated;
matches #379):

| `ell` | atlas | cap-tight (`T=7`) | FAT-TAIL | MIN-J (`j=3`) | BIG3TAIL | MIDDLE |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| 17 | 447 | 51 | 1 | 0 | 11 | 435 |
| 19 | 792 | 66 | 1 | 1 | 13 | 777 |
| 23 | 2166 | 96 | 1 | 5 | 17 | 2143 |
| 29 | 7989 | 141 | 1 | 16 | 23 | 7949 |

(FAT-TAIL + MIN-J + BIG3TAIL + MIDDLE = atlas exactly; cap-tight is an orthogonal
count.) Families, by the largest tail fiber `mu_3`:

- **FAT-TAIL `[ell-3, 3^8]`** (unique, cap-tight): a **cubic**-pencil concurrency;
  refutes iff `k3 = 8`.
- **MIN-J `[a, ell-a, 9]`** (`j = 3`, least over-determined; exists `ell >= 19`):
  refutes iff `mu_3 = 9` — exactly #382's open `mu_3 <= 8` conjecture. At
  `ell = 19` the **unique** member is `[10,9,9]`, the core of `[10,9,9,2^5]`.
- **BIG3TAIL / MIDDLE**: the same degree-`(ell-mu_1)` pencil `P - lambda A_drop`
  with the shape's split pattern.

**The cap-tight slice is the minimal-tail target, and it is finite (PROVED, #382
Thm 1).** For a cap-tight top pair `(F1,F2)`, `|F1|+|F2| = ell` forces a **unique**
`Gamma` — the coincidence rows have nullspace dimension **exactly `1`** (gate vi:
plant `(10,9)` at `ell = 19, p = 191` ⟹ dim `= 1`). So a cap-tight shape's
realizability is a **deterministic per-plant** check, and each tail fiber is a
root-count of the explicit degree-`(ell-mu_1)` pencil in one coset.

**Two independently PROVED `k3` caps for the fat tail (gate v).** With
`R_zeta(X) := q(X) A_drop(zeta X) - q(zeta X) A_drop(X)`:
- **Cyclotomic pair count.** `deg R_zeta = 5` and `X | R_zeta` (verified
  symbolically over `F_p`), so `<= 4` nonzero roots per `zeta`; each tail
  `3`-fiber makes `6` ordered pairs `(u, zeta u)`, so `6 k3 <= 4(ell-1)`, i.e.
  **`k3 <= 2(ell-1)/3`**.
- **Lemma R.** `(ell-3)(ell-4) + 6 k3 <= (ell-1)(ell-2)` ⟹ **`k3 <= (2ell-5)/3`**.

| `ell` | Lemma R `(2ell-5)/3` | `R_zeta` `2(ell-1)/3` | empirical max `k3` |
|:-:|:-:|:-:|:-:|
| 17 | 9 | 10 | 7 (only at `n=8`) |
| 19 | 11 | 12 | 6 (only at `n=30`) |
| 23 | 13 | 14 | 5 |
| 29 | 17 | 18 | 7 (only at `n=8`) |
| 31 | 19 | 20 | 7 |
| **43** | **27** | **28** | **8**  ← falsifier |
| **53** | **33** | **34** | **11** |

**CORRECTED 2026-07-07 (was: uniform empirical `7`).** The two `Theta(ell)` caps are **no
longer read as overshoots** of an `O(1)` truth: the exhaustive-up-to-gauge `max k3` **GROWS
with `ell`** (`4,4,7,6,5,7,7,7,7,8,7,11,9` at `ell = 11..59`), crossing the fat-tail falsifier
`k3 = 8` at **`ell = 43`** (realizable `[40,3^8]`, excess `+3`) and reaching **`11`** at
`ell = 53` (`[50,3^11,2^6]`, excess `+6`, `T = 10`) — and `k3` can grow with `n` at fixed
`ell` as well (`ell = 53`: `7` at `n = 14` vs `11` at `n = 20`, both exhaustive). The
`ell <= 31` reading (`max <= 7`) was a small-`ell` mirage; see §6/§7 and the companion note
`experimental/notes/l1/l1_k3_growth_refutation.md` (finitely many exact points do not establish
the growth *order*; the caps bracket it from above). (The `ell = 19` entry `6` is the
pin-relevant one — excess `+1`, `H_19` safe; exhaustive over the five eligible primes
`n <= 30`, attained only at the `n = 30` boundary; beyond-window `647/761/1103` give `5`.)

---

## 6. [EXPERIMENTAL] Extended null evidence (lane T1)

Across all searched families, **zero realizable excess `>= 3`**; realized frontier
`excess <= +2` / `T <= 6`. Coverage is **deep, not exhaustive** — stated honestly.

- **Fat-tail concurrency, exhaustive-in-`q`** (drops → rotation orbits; one
  representative covers all drops per prime), `ell in {17,19,23,29}`, ~12 primes
  incl. the **large-`n` regimes #368 left unrun**: max `k3 = 7` (`ell in {17,29}`,
  only at `n = 8`), `<= 6` for `ell in {19,23}`; `k3 = 8` **never**. The
  `(17,137)` case is **airtight** (full `P^2` × drops, max excess exactly `+2`,
  `E_3 = 19`), cross-validating #368's own full sweep.
- **Balanced / cap-tight / min-`j`-complement plants** (B2 under-plant + full
  projective nullspace sweep; the min-`j` plant seats `F1(a)` and the *target*
  size-`9` third fiber directly): max emergent excess `0..+1`; even planting the
  size-`9` fiber, no second big fiber co-emerges (`[10,9,9]` un-realized).
- **#382 min-`j` freeze**: 2.78M cap-tight pair-plant evals, `mu_3` frozen `<= 5`
  on the true frontier (`ell-a >= 9`), never `9`.

**~~Striking plateau~~ — PLATEAU REFUTED (2026-07-07).** The reading that empirical max
`k3 = 7` is constant across `ell` (`O(1)`) was a **small-`ell` mirage**: the sweep above
stops at `ell <= 31`. Extending the exhaustive-up-to-gauge scan shows `max k3` **GROWS with
`ell`** — `4,4,7,6,5,7,7,7,7,8,7,11,9` at `ell = 11..59` — crossing `k3 = 8` first at
`ell = 43` (realizable `[40,3^8]`, excess `+3`, `T = 7`) and reaching `k3 = 11` at `ell = 53`
(`[50,3^11,2^6]`, excess `+6`, `T = 10`; `9` at `ell = 59`, excess `+4`). The growth is not
only in `ell`: at fixed `ell = 53` the exhaustive max jumps `7` (`n = 14`) `-> 11`
(`n = 20`). So over `F_p` the uniform cap `k3 <= 7`, and with it `C' <= 2` and "no realizable
`T >= 7`", are **REFUTED**; the two `Theta(ell)` caps are **no longer read as overshoots**
(they bracket the realized growth from above). Companion note + verifier:
`experimental/notes/l1/l1_k3_growth_refutation.md`,
`experimental/scripts/verify_l1_k3_growth_refutation.py`.

**The pin is UNTOUCHED.** At `ell = 19` the exhaustive-up-to-gauge max is `k3 = 6` (excess
`+1`; exhaustive over the five eligible primes `n <= 30` — maxima `5,5,5,5,6`, attained only
at the `n = 30` boundary — with `5` at the beyond-window primes `647/761/1103`), so the
fat-tail family cannot make a realizable `E_3 >= 22` at `ell = 19` in the scanned range:
`H_19` and the CONDITIONAL THEOREM `H_19 => m*(19) = 9` (§3) stand, and so does the min-`j`
falsifier frontier `[10,9,9,2^5]` (§4) — which this fat-tail family never realizes anyway (it
has `mu_2 = 3`, so it is not an `m = 8` crosser: a crosser needs `mu_2 >= 4`, §2). The
refutation is of the *uniform-in-`ell`* cap; the `ell = 19` instance is a separate,
still-standing pin.

---

## 7. [OPEN] The one named missing input

Every survivor reduces to a single statement:

> **(★) A uniform `O(1)` bound on the number of roots an explicit low-degree
> pencil member `P - lambda A_drop` (deg `= ell-mu_1`, `A_drop` a product of
> cyclotomic factors) can concentrate inside one coset of `mu_ell`** — for the
> fat tail the cubic case (`k3 <= 7`), for the min-`j` #382's `mu_3 <= 8`.

**[(★) FAT-TAIL CUBIC HORN — REFUTED over `F_p`, 2026-07-07.]** The uniform `O(1)` for the
**cubic** (fat-tail) case is **FALSE**: `k3` GROWS with `ell`, realizing `k3 = 8` at
`ell = 43`, `k3 = 11` at `ell = 53` (excess `+6`, `T = 10`), and `k3 = 9` at `ell = 59` —
explicit realizable mixed `Gamma`, verified in
`experimental/notes/l1/l1_k3_growth_refutation.md`. The three `Theta(ell)` routes below are
**no longer read as overshoots** of an `O(1)` truth (they bracket the realized growth from
above). **The `ell = 19` instance is untouched** (exhaustive max `k3 = 6` over the five
eligible primes `n <= 30`, attained only at the `n = 30` boundary; beyond-window
`647/761/1103` give `5` — excess `+1`), so `H_19` and the pin (§3) stand; refuting
`m*(19) = 9` still needs a realizable `ell = 19` crosser (`mu_2 >= 4`), which this
`mu_2 = 3` fat-tail family does not provide. The min-`j` `mu_3 <= 8` horn (#382, a *different*,
higher-degree, non-cubic shape) is **not** refuted by this fat-tail family and remains OPEN —
it, not the cubic cap, is now the live missing input.

**Re-derived barrier (PROVED negative, independent of the integrated N1 no-go).**
The three elementary routes — the `R_zeta` cyclotomic-pair count, Lemma R, and a
Bézout count of the coincidence locus (a bidegree-`(2,2)` curve against
`{x^ell = y^ell}`, `= 4 ell` points) — **all give `Theta(ell)`, never `O(1)`**.
So (★) is invisible to degree / moment / Bézout tools; it is irreducibly the
`(W,lambda)`-Veronese / cyclotomic-transversality core that
`l1_bounded_excess_structure.md` §4 and `l1_e3_dim_syz_crux_refuted.md` name as
the program's open crux (their diagnostic N1). This lane confirms that no-go from
a fresh angle rather than inheriting it.

---

## 8. Non-claims

Does **not** prove `m*(19) = 9` unconditionally — it is conditional on `H_19`
(implied by `T1` — though `T1` itself is now REFUTED globally, §1/§6, so `H_19`, the
`ell = 19` instance, is the operative and still-open hypothesis), CONJECTURAL. Does **not** prove any surviving shape
unrealizable (§6 is EXPERIMENTAL corroboration, deep not exhaustive). Does **not**
claim a new `E_3`/`T` ceiling beyond the notes. Does **not** claim `k3 <= 7`
concurrency blocks `m = 8` (it does not apply — no crosser is a fat tail; even
`k3 = 8` gives `top-8 = 37`). Does **not** claim `m = 8` and `C' <= 2` are a
literal config-equivalence (§4 caveat: the fat tail refutes `C' <= 2` without
crossing `m = 8`). Depends on lane T1's target only as a *stated hypothesis*.
Ships nothing; `experimental/` reasoning only. **Falsifier explicitly invited:**
any realization of the `[10,9,9,2^5]` family (or a fat-tail `[16,3^8]`, or any
excess-`3` atlas shape) at `p ≡ 1 (mod 19)`, `n >= 15`, refutes `H_19`/`C' <= 2`;
if it is a frontier shape it also refutes `m*(19) = 9`.

---

## 9. Reproduction, siblings, references

`experimental/scripts/verify_l1_m19_pin_excess3_atlas.py` (zero-arg,
`--tamper-selftest`, stdlib, deterministic, < 1s): all 6 gates pass; all 6 tampers
caught. Enumerations re-derive 17012/11927/59, the ladder integers, the two
witness spectra, the four-`ell` atlas partition, the two `k3` caps + symbolic
`R_zeta`, and the unique-`Gamma` dim-`1` crack.

**Integrated notes cited** (`experimental/notes/l1/`): `l1_ell19_band_refuted.md`
(#364, `m*(19) <= 9`), `l1_ell19_attainment.md` (#attainment, `m = 10/11` rungs),
`l1_bounded_excess_structure.md` (#368, excess identity + N1 no-go),
`l1_t7_atlas_concurrency.md` (#379, atlas + concurrency law),
`l1_minj_pencil_freeze.md` (#382, unique-`Gamma` crack + freeze),
`l1_e3_law_refuted.md` (#358, WLOG deletion + B2 method),
`l1_sigma_calculus.md` (pairwise cap Lemma 3, Theorem 1),
`l1_e3_charsum_paircap.md` (Lemma R), `l1_prime_ell_frontier_corrected.md`
(bridge), `l1_prime_ell_key_lemma_refuted.md` (eligibility),
`l1_e3_dim_syz_crux_refuted.md` (#365, the transversality crux).

**Open siblings (no overlap with this lane).** The older L1-core siblings #363
(M31 rung, NOT-GREEN), #365 (dim-Syz), #366 (Q-routes) sit on the M31 / `Q`-wall /
dim-Syz questions. Among the newer open siblings, the only other **L1-lane**
packets are #390/#391 — the **W3 collapse-edge at `ell = 17`** (the residual-excess
edge, a different `ell` and a different question than the `ell = 19`, `m = 8`
onset), so they are disjoint by target even though same-lane; the rest (#389
CAP25 LQ-seam, #392/#396 thresholds, #393/#395 BC L4, #394 Lean) are other program
lanes, and the newest Q-frontier packets #397 (row-sharp Q atom reductions at the
deployed row) and #398 (b2 conj:Q barrier map) share no object with the `ell = 19`
onset. None touches the `m = 8` / `ell = 19` onset pin. Concurrent lanes T3/T4
carry no dependency on this packet.
