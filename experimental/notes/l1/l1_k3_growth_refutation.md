# L1: fat-tail `k3` GROWS with `ell` — `C' <= 2`, "no realizable `T >= 7`", and the `O(1)` cap REFUTED

**Type: PROVED (the cubic-pencil reduction + the exact concurrency/gauge method) +
EXACT-COMPUTATION (exhaustive-up-to-rotation-gauge `max k3`, no sampling) +
COUNTEREXAMPLE (three of our own conjectured caps) + OPEN (the strict `p/ell -> infty`
limit; the new `k3` growth law). Non-superseding of proofs; supersedes-in-part the
integrated EXPERIMENTAL readings named in §7 (`#368` / `#379` / `#387`).**

**Result (one line).** Over `F_p` — the program's own setting — the uniform fat-tail cap
`k3 <= 7`, and with it `C' <= 2` (`E_3 <= ell+2`) and "no realizable `T >= 7`", are all
**FALSE**: explicit, verified, realizable mixed `Gamma` reach `k3 = 8` (`ell = 43`, excess `+3`,
`T = 7`), `k3 = 9` (`ell = 59`, excess `+4`, `T = 8`; also `ell in {61,71,73}`), and `k3 = 11`
(`ell = 53`, excess **`+6`**, `T = 10`), and the exhaustive-up-to-gauge `max k3` **grows with
`ell`** (`4,4,7,6,7,7,7,7,7,8,7,11,9` at `ell = 11..59`, then `9` at each of `ell = 61,71,73`;
per-prime coverage §3). The `k3 = 8` falsifier first appears at `ell = 43`; the program's `O(1)`
reading was a **small-`ell` mirage** (it searched `ell <= 31`, where the genuinely growing max is
still `<= 7`). The `ell = 19` pin `H_19` / `m*(19) = 9` is **UNTOUCHED — and now deep-null
verified**: exhaustive-up-to-gauge scan of **ALL 80 eligible primes `p = 19n+1` up to
`p = 13567`** (`n <= 714`; R2 scan, §3/§3A, artifact JSON in-repo) gives max `k3 = 6`, attained
**uniquely** at `p = 571`; zero primes reach `7`. It is the *uniform-in-`ell`* conjecture that
dies.

**Companion verifier** (stdlib, zero-arg, `< 60s`, self-contained; embeds its own `F_p`
machinery, imports no sibling; opt-in `--full` replays the entire §3 coverage table, ~20-25 min):
`experimental/scripts/verify_l1_k3_growth_refutation.py`.

**Notation** (inherited verbatim from `experimental/notes/l1/l1_sigma_calculus.md`). `ell` odd
prime, `ell | p-1`, `H = mu_ell subset F_p^*`, `n = (p-1)/ell` cosets partitioning `F_p^*`. A
**mixed `Gamma`** is any `Gamma(X) = sum_{r=1}^{ell-1} gamma_r X^r` (constant-free, `deg <= ell-1`)
— *exactly* the definition there, no hidden constraint. Per coset the **max fiber** size is `mu_b`
(per-coset-MAX; the `spectrum_A` label of `experimental/notes/l1/l1_e3_law_refuted.md`); sorted
spectrum `mu_1 >= mu_2 >= ...`; `E_3 :=
sum_k (mu_k-2)_+`; `T := sum_{k>=3}(mu_k-2)_+` (from the THIRD-largest fiber onward); `excess :=
E_3 - ell`; **realizable** = achieved by some mixed `Gamma`. The **fat tail** `[ell-3, 3^{k3}]` has
`excess = k3 - 5`, so the `C' <= 2` refuter is `k3 = 8` (excess `+3`), "one above" the old record
`k3 = 7` (`W3 = [14,3^7]` at `ell = 17`). All arithmetic exact over `F_p`, stdlib only.

**Status legend.** PROVED / EXACT-COMPUTATION (exhaustive, no sampling; coverage stated) /
COUNTEREXAMPLE (refuted, explicit object) / EXPERIMENTAL (deep, coverage stated) / OPEN / SURVIVES.

---

## 1. [PROVED] Reduction: the fat tail is a cubic pencil; `k3 = #` coset-aligned members

Plant the size-`(ell-3)` fiber in coset `0 = H` (WLOG by the scaling gauge). With drop set
`D = {d_1,d_2,d_3} subset mu_ell`, put `A_D = prod_i (X - d_i)` (a **cubic** dividing `X^ell - 1`).
`Gamma - c1` must vanish on `F_1 = H \ D` (the planted fiber) and have degree `<= ell-1`, so

> **`Gamma(X) = c1 + (X^ell - 1) q(X) / A_D(X)`,  `q` a QUADRATIC,  `c1 = q(0)/A_D(0)`** (forces
> `Gamma(0) = 0`); `deg Gamma = ell-1` **iff `q_2 != 0`** (`q_2 = 0` members have
> `deg in {ell-3, ell-2}`, still admissible mixed `Gamma`; every witness below has `q_2 = 1`).

On a tail coset (`X^ell = rho != 1`), `Gamma` is constant on a triple `<=> q/A_D` is, i.e. `<=>`
that triple is a 3-root of a member of the **cubic pencil** `{q - lambda A_D}` lying in one coset
("coset-aligned"). The cubic caps every tail fiber at `<= 3`, forcing the shape `[ell-3, 3^{k3}, ...]`
with **`k3 = #` coset-aligned pencil members**, hence `E_3 = (ell-5) + k3` and `excess = k3 - 5`
exactly. *(This is `l1_bounded_excess_structure.md` §1 / `l1_t7_atlas_concurrency.md` §0.3's
`excess = k3-5` identity — which SURVIVES and is the identity used throughout; only the
EXPERIMENTAL ceiling `k3 <= 7` on top of it dies.)*

**Exact `P^2`-concurrency form (no `q`-sweep).** A coset triple `{x_1,x_2,x_3}` is a 3-fiber of `q`
iff `q . (w_i - w_j) = 0` with `w_i = A_D(x_i)^{-1}(x_i^2, x_i, 1)`; so it pins `q` to the single
projective point `q = (w_1 - w_2) x (w_1 - w_3)` (cross product). Therefore, for a fixed `D`,
`max_q k3(q,D)` = the `q`-point hit by triples from the **most distinct tail cosets** — computed
exactly, without sweeping `q`.

**Nondegeneracy (PROVED — closes the tally's degenerate case).** For distinct `x_1,x_2,x_3` in one
tail coset, `(w_1-w_2) x (w_1-w_3) != 0` — the pinned `q`-point always exists. *Proof.* First
`A_D(x_i) != 0` automatically (the roots of `A_D` are the drops, which lie in coset `0`). Each `w_i`
is a nonzero scalar multiple of `(x_i^2 : x_i : 1)` — three DISTINCT points on the smooth conic
`{(a:b:c) : b^2 = ac}` (irreducible, `p` odd). If the cross product vanished, `w_1-w_2` and
`w_1-w_3` would be parallel, so `w_1,w_2,w_3` would lie on one affine line of `F_p^3`, hence in a
2-dimensional linear subspace, hence on one projective LINE — but a line meets a smooth conic in at
most `2` points (Bezout, `deg 1*2`). Contradiction. ∎ (The verifier enforces this as an
**assertion**, not a silent skip.)

**Rotation gauge (PROVED).** `max_q k3(*, D)` is constant on drop orbits `D ~ zeta D`
(`zeta in mu_ell`). *Proof.* The substitution `X -> zeta^{-1}X` maps `Gamma_{D,q}` to
`Gamma_{zeta D, q'}` with **`q'(X) = zeta^3 q(zeta^{-1}X)`**: indeed `(zeta^{-1}X)^ell = X^ell` and
`A_D(zeta^{-1}X) = prod_i(zeta^{-1}X - d_i) = zeta^{-3} A_{zeta D}(X)`, so
`Gamma_{D,q}(zeta^{-1}X) = c1 + (X^ell - 1)[zeta^3 q(zeta^{-1}X)]/A_{zeta D}(X)`; the constant `c1`
is invariant since `A_{zeta D}(0) = zeta^3 A_D(0)` gives `c1' = q'(0)/A_{zeta D}(0) =
zeta^3 q(0)/(zeta^3 A_D(0)) = c1`. The map `q -> q'` (coefficientwise
`(q_0,q_1,q_2) -> (zeta^3 q_0, zeta^2 q_1, zeta q_2)`) is a bijection of the `q`-space `P^2`, and
multiplication by `zeta in mu_ell = H` fixes every coset SETWISE — so `Gamma_{zeta D, q'}` has the
identical per-coset fiber structure (hence spectrum, hence `k3`) as `Gamma_{D,q}`. Maximizing over
the bijection: `max_q k3(q, zeta D) = max_q k3(q, D)`. ∎ Scanning one representative per orbit
(`~C(ell,3)/ell`) is therefore **EXACT** for the maximum — this is what makes large `ell`
exhaustively decidable.

The verifier reproduces `k3` by independent routes: the via-`Gamma` spectrum on all six witnesses,
the via-pencil root count on the four primary witnesses, and the `P^2`-concurrency scans of gates
2-3 / `--full` on the table rows — agreeing everywhere they overlap.

## 2. [COUNTEREXAMPLE] The four primary falsifiers (full data; `q = X^2 + bX + c`)

**Coefficient convention: `q = X^2 + bX + c`** (leading coeff `1`). *(An originating-lane dossier
printed `q = 169X^2 + 294X + 1` for `ell = 43`; that was a reversed-tuple MISLABEL — the true
polynomial is `X^2 + 294X + 169`, printed correctly below and everywhere here.)* Each `Gamma` below
is a genuine mixed constant-free degree-`(ell-1)` polynomial, hence realizable by definition; all
quantities — including `c1` — are recomputed from `(p, ell, D, q)` by the verifier (gate 1).

| `ell` | `p` | `n` | drop `D subset mu_ell` | `q` | `c1` | spectrum | `E_3` | `= ell+` | `T` | `k3` |
|:-:|:-:|:-:|:--|:--|:-:|:--|:-:|:-:|:-:|:-:|
| **43** | 431 | 10 | `{1, 4, 16}` (`= {h^0,h^1,h^2}`, `h=4`) | `X^2 + 294X + 169` | 260 | `[40, 3^8]` | 46 | **+3** | **7** | **8** |
| **53** | 1061 | 20 | `{1, 37, 268}` (`= {h^0,h^{27},h^{30}}`, `h=308`; **NOT** of the `(0,1,k)` form) | `X^2 + 32X + 1060` | 451 | `[50, 3^{11}, 2^6]` | 59 | **+6** | **10** | **11** |
| 53 | 1061 | 20 | `{1, 308, 998}` (`= {1,h,h^{14}}`, `h=308`) | `X^2 + 672X + 806` | 176 | `[50, 3^9, 2^3]` | 57 | +4 | 8 | 9 |
| **59** | 709 | 12 | `{1, 551, 564}` (`= {1,h,h^3}`, `h=551`) | `X^2 + 341X + 336` | 650 | `[56, 3^9, 2]` | 63 | +4 | 8 | 9 |

`ell = 43` is **THE `C' <= 2` / `T1` falsifier**: `[40,3^8]` has `mu_1 = 40 = ell-3`,
`E_3 = 46 = ell+3` (excess `+3`), `T = 7`, `k3 = 8` — one above the old record. (`[40,3^8]` head
asserted by the verifier.) The `ell = 53` `k3 = 11` row is the **current record** — excess `+6`,
realizable `T = 10` — and equals the true exhaustive-gauge max at `(53,1061)` (§3); the `k3 = 9`
row below it was the originating lane's `(0,1,k)`-family record at the same prime, kept as a
second, independent witness.

**Band-persistence witnesses (honest-`Gamma`-verified; gate 1).** `excess >= +3` is not isolated —
it is realized at **every** `ell in {43,53,59,61,67,71,73}`:

| `ell` | `p` | `n` | drop `D` | `q` | `c1` | spectrum | excess | `T` | `k3` |
|:-:|:-:|:-:|:--|:--|:-:|:--|:-:|:-:|:-:|
| 61 | 733 | 12 | `{1, 10, 16}` (`= {h^0,h^1,h^{11}}`, `h=10`) | `X^2 + 258X + 515` | 432 | `[58, 3^9, 2^2]` | **+4** | 8 | 9 |
| 67 | 1609 | 24 | `{1, 1141, 320}` (`= {h^0,h^1,h^{24}}`) | `X^2 + 644X + 708` | 45 | `[64, 3^9, 2^{12}]` | **+4** | 8 | 9 |
| 71 | 853 | 12 | `{1, 81, 547}` (`= {h^0,h^2,h^{15}}`, `h=9`) | `X^2 + 761X + 164` | 543 | `[68, 3^9, 2^2]` | **+4** | 8 | 9 |
| 73 | 877 | 12 | `{1, 567, 766}` (`= {h^0,h^2,h^{12}}`, `h=38`) | `X^2 + 448X + 140` | 262 | `[70, 3^9, 2^2]` | **+4** | 8 | 9 |

*(The `ell = 61` row is the R2 EXHAUSTIVE-max witness — it upgrades this packet's originally
shipped `(0,1,k)`-family lower bound `k3 >= 8` (excess `+3`) at the same prime to the exhaustive
`k3 = 9` (excess `+4`); the `71`/`73` rows are new-`ell` exhaustive maxima at their `n = 12`
primes; `ell = 67` remains the shipped `(0,1,k)` lower-bound witness at `n = 24`.)* So the
counterexample **band** reaches **`C' >= 6`** (realized excesses: `+3` at `{43}`, `+4` at
`{59,61,67,71,73}`, `+6` at `53`) and spans seven consecutive eligible `ell`.

**R2 coverage-extension records (honest-`Gamma`-verified; gate 1).** Two further witnesses from
the R2 exhaustive grid (§3), re-verified through this packet's own checker:

| `ell` | `p` | `n` | drop `D` | `q` | `c1` | spectrum | `E_3` | excess | `T` | `k3` |
|:-:|:-:|:-:|:--|:--|:-:|:--|:-:|:-:|:-:|:-:|
| **23** | 1657 | 72 | `{1, 16, 913}` (`= {h^0,h^1,h^4}`, `h=16`) | `X^2 + 650` | 1306 | `[20, 3^7]` | 25 | **+2** | 6 | **7** |
| 43 | 1721 | 40 | `{1, 32, 1462}` (`= {h^0,h^1,h^{14}}`, `h=32`) | `X^2 + 75X + 925` | 730 | `[40, 3^8, 2^4]` | 46 | +3 | 7 | 8 |

The `ell = 23` row is a **new `ell = 23` record** (`5 -> 7`), set at the LARGEST prime R2 tested
for that `ell` — a *late* record (see §3A); it is not an excess-`>= 3` falsifier (excess `+2`),
but it moves the §3 table's `ell = 23` entry. The `ell = 43` row shows the max `8` *recurring* at
`n = 40` (`p = 1721`), far from the original `n = 10`.

## 3. [EXACT-COMPUTATION] `max k3` grows with `ell` — the exhaustive-up-to-gauge table

Exhaustive over all drop orbits (rotation-gauge-reduced, PROVED exact in §1) and exact over all `q`
(`P^2` concurrency) at each listed prime:

```
 ell :  11 13 17 19 23 29 31 37 41 43 47 53 59 | 61 67 71 73
 max :   4  4  7  6  7  7  7  7  7  8  7 11  9 |  9 >=9  9  9
```

*(The `ell = 23` entry moved `5 -> 7` in the R2 coverage extension — a LATE record at `p = 1657`,
`n = 72`; the prior `5` was the correct max over the primes then scanned, which is exactly why
this table carries its per-prime coverage column. `ell = 67` is a witness lower bound `>= 9`; its
only exhaustively scanned prime is tiny — see its row.)*

**Per-`ell` coverage** (every row below is EXACT at the primes listed; "gate 2/3/5" = re-verified
live by this packet's zero-arg verifier; "build-time" = exhaustively re-scanned at packaging time
by this packet's own transversal code, reproducible via the verifier's opt-in `--full` flag; "R2
grid" = the overnight R2 lane's exhaustive-gauge scans, shipped as the in-repo artifact
`experimental/data/certificates/l1-e3-law/l1_k3_growth_r2_scan.json` (per-prime rows + 4-route
witnesses), spot-replayed by this packet's own transversal where noted; "witness" = a §2 witness
gates the lower bound live in gate 1):

| `ell` | max `k3` | attained at `p` (`n`) | primes scanned exhaustively (max there) | established by |
|:-:|:-:|:--|:--|:--|
| 11 | 4 | 67 (6) | 23(1), 67(4), 89(3), 199(4), 331(4) | gate 3 @67; build-time rest |
| 13 | 4 | 313 (24) **only** | 53(3), 79(3), 131(3), 157(3), 313(4) | gate 3 @313; build-time rest |
| 17 | 7 | 137 (8) **only** | 103(4), 137(7), 239(5), 307(5), 409(**5** — the `#368` row fix); + R2: 44 primes to 5237, max elsewhere `<= 5` | gate 3 @137, @409; build-time; R2 grid |
| 19 | 6 | 571 (30) **UNIQUELY** | **ALL 80 eligible primes `n <= 714` (`p <= 13567`)**: `k3 = 3` at 42, `4` at 15, `5` at 22, `6` at exactly one (571); zero reach 7 | gate 2 live (5 window + 3 spot); R2 grid (80 rows, artifact + gate 5); my replays @1901, @13567; `--full` spot rows |
| **23** | **7** | 1657 (72) **only** (LATE record) | R2: 21 primes 47..3083 — 2(1), 13 consecutive at 5, 72(**7**), then 84(5), ..., 132(4), 134(5) | R2 grid + witness (`= 7` live, pencil); `--full` replay @1657; gate 3 @139 (5) |
| 29 | 7 | 233 (8), 1277 (44), 1973 (68) — recurs | 59(1), 233(7), 349(5), 523(5); + R2: 12 primes to 2089, 7 recurs 3x | gate 3 @233; build-time; R2 grid |
| 31 | 7 | 311 (10) | 311(7), 373(7), 683(7) | gate 3 @311; build-time rest |
| 37 | 7 | 593 (16) | 149(3), 223(5), 593(7) | build-time (`--full`) |
| 41 | 7 | 739 (18) | 739(7); (83 has `n = 2`: `k3 <= n-1 = 1`, trivial) | build-time (`--full`); lane row was SAMPLED-only |
| 43 | 8 | 431 (10), 1721 (40) — recurs | 431(8); + R2: 9 primes 173..2237 — 4(3), 10(**8**), 22(7), 24(7), 30(7), 36(6), 40(**8**), 46(7), 52(7) | gate 3 reaches `8` live + 2 witnesses; `--full` @431, @1721; R2 grid |
| 47 | 7 | 659 (14) | 283(**5**), 659(7) | build-time (`--full`); lane row was SAMPLED-only |
| **53** | **11** | 1061 (20) **only** (isolated spike) | 743(**7**), 1061(**11**); + R2: 107(1), 1697/n=32(**7**), 2333/n=44(**8**), 2969/n=56(**7**) | build-time (`--full`) + witness (`>= 11` live); R2 grid |
| 59 | 9 | 709 (12) | 709(9) | build-time (`--full`) + witness (`>= 9` live) |
| 61 | 9 | 733 (12) | R2: 367(5), 733(**9**) — upgrades this packet's shipped `(0,1,k)` bound `>= 8` to the exhaustive `9` | R2 grid + witness (`= 9` live) |
| 67 | `>= 9` | 1609 (24), witness | R2 exhaustive only @269 (`n = 4`): `3`; **no eligible prime `n = 5..23` exists** (`67n+1` composite throughout), so the thin `3` is a coverage artifact — the shipped witness realizes `9` at `n = 24` | witness (`>= 9` live); R2 grid @269 |
| 71 | 9 | 853 (12) | R2: 569(7), 853(**9**) | R2 grid + witness (`= 9` live) |
| 73 | 9 | 877 (12) | R2: 293(3), 439(5), 877(**9**) | R2 grid + witness (`= 9` live) |

- **`k3 = 8` first appears at `ell = 43`** (drop `{h^0,h^1,h^2}`); `ell <= 41` caps at `<= 7`.
- **CORRECTION (found by panel review of this packet — the FIFTH searched-too-shallow instance,
  caught inside the packet documenting the fourth).** The originating lane's table printed
  `ell = 53 -> 9`. That value was **truncated by its own scanner's early-exit design**: the lane's
  gauge scan returns at the FIRST drop orbit reaching `k3 >= 8` (a falsifier-*existence* hunt, not
  a max measurement — visible in its `scan_prime_gauge`), so at `(53,1061)` it stopped at a `9` and
  never measured the true max. The **true exhaustive-gauge max at `(53,1061)` is `11`**, attained at
  (at least) TWO distinct orbits, both beyond the truncation point: `{1, 37, 268} =
  {h^0, h^{27}, h^{30}}` (canonical exponent orbit `(0,3,26)`, not `(0,1,k)`-adjacent — the §2
  witness) and `{1, 308, 164} = {h^0, h^1, h^{19}}` (canonical `(0,1,19)` — so even the `(0,1,k)`
  family reaches `11` there, honest-`Gamma`-verified `[50,3^{11},2^6]`). The lane's `41`/`47` rows
  were likewise only sampled-consistent; both were **re-established exhaustively at build time**
  (values unchanged: `7`). The `59 -> 9` row was re-established exhaustively too (`9` confirmed).
- **Attaining `n` matters** (why the program missed it): `ell = 17, 29` reach `7` **only at
  `n = 8`** among small primes (this packet's scans: `17`: `239/307/409 -> 5`, `29`: `349/523 -> 5`;
  the R2 grid extends `ell = 17` exhaustively through 44 primes to `p = 5237` — never above `5`
  again — superseding the previously-cited `#379` SAMPLED data with exhaustive coverage, and shows
  `ell = 29`'s `7` recurring at `n = 44, 68`); `ell = 13` reaches `4` only at `n = 24`; `ell = 19`
  reaches `6` only at `p = 571` (`n = 30`) — now known unique among ALL 80 eligible primes to
  `p = 13567`. **`ell = 47`: the smallest eligible prime is `p = 283` (`n = 6`), where the
  exhaustive max is `5`; its `7` is attained at `p = 659` (`n = 14`).**
- **`p`-dependence at fixed `ell` FLUCTUATES — it neither grows monotonically nor freezes**
  (full reading in §3A). Sharpest: `ell = 53` runs `7 -> 11 -> 7 -> 8 -> 7` over
  `n = 14, 20, 32, 44, 56` — the record `11` is an isolated spike bracketed by `7`s. The old
  "`k3` does not grow with `n`" reading survives only inside the `ell <= 31` window where it was
  measured, and its naive replacement "`k3` grows with `n`" is *also* wrong.
- The `Theta(ell)` baselines `k3 <= 2(ell-1)/3` (deg-`5` `R_zeta`, `X | R_zeta`) and Lemma R
  `k3 <= (2ell-5)/3` (`l1_e3_charsum_paircap.md`) — previously read as *overshooting* an `O(1)`
  truth — are **no longer read as overshoots**: they bracket the realized growth from above
  (finitely many exact points do not establish the growth *order*; the growth law is OPEN, §4).

## 3A. [ANALYSIS] Non-monotonicity in `p`; the `n = 12` trio; what the deep `ell = 19` null means

*(ANALYSIS labels throughout: exact data, interpretive readings — no theorem claimed.)*

- **`k3(p)` at fixed `ell` is a sparse spike process, not a monotone law.** On the R2 exhaustive
  grid: `ell = 53` runs `7, 11, 7, 8, 7` (`n = 14..56`) — the `11` is isolated; `ell = 17` and
  `ell = 29` peak at their SMALLEST eligible prime (`n = 8`) and never regain it (17: not once in
  43 further primes to `p = 5237`; 29's `7` does recur, at `n = 44, 68`); `ell = 23`'s record
  arrives at its LARGEST tested prime (`p = 1657`, after 13 consecutive primes flat at `5`) and
  drops back to `5` at the very next prime; `ell = 43`'s `8` recurs at `n = 10` and `n = 40` with
  `6`-`7` between. Consequences, stated plainly: per-`(ell,p)` maxima do not reveal a monotone
  law; **the right object is `sup` over `p`, and it remains OPEN at every `ell`** (each table
  value is a certified lower bound for it, nothing more); and **late records are possible at any
  `ell`** — which is exactly why the `ell = 19` deep null below is *evidence*, not proof.
- **The `ell = 19` deep null.** All 80 eligible primes to `p = 13567` (16x more primes, 12x
  deeper in `p` than this packet previously shipped) cap at `k3 = 6`, attained uniquely at
  `p = 571`. Its neighbors `17, 23, 29` each reach `7` within far less search (44, 21, 12 primes
  respectively — 1.8x to 6.7x fewer than the 80 exhausted for `ell = 19`). Reading (ANALYSIS):
  the `6`-ceiling in this range looks like a **genuine `ell = 19` feature**, not a search-depth
  artifact. Status hygiene unchanged: `H_19` is **UNTOUCHED / strengthened-evidence** — never
  "supported by proof" (the late-record phenomenon above is the standing caution).
- **The `n = 12` trio.** `ell = 61, 71, 73` all hit exactly `k3 = 9` at their `n = 12` primes
  (`p = 733, 853, 877` — 4-route witnesses, re-verified here). `ell = 67`'s lone exhaustive value
  (`3`, at `n = 4`) is a coverage artifact — `67n+1` is composite for every `n = 5..23`, so `67`
  simply has no `n ~ 12` prime to test; the shipped `ell = 67` witness already realizes `9` at
  `n = 24`. Reading (ANALYSIS): primes near `n = 12` afford `9` across this `ell` range; the
  compact-`ell` values are search-depth-limited, not `ell`-limited.
- **Distance to the proved ceilings** (one line): on the R2 exhaustive grid the observed maxima
  sit at **7%–78%** of the Lemma-R ceiling `floor((2ell-5)/3)` (78% at `ell = 17`; the 7% is
  `ell = 67`'s single-thin-prime row — counting its witness `>= 9` it is `>= 21%`), the ratio
  broadly FALLING in `ell`: the proved `Theta(ell)` ceilings are nowhere near saturated, and the
  gap widens as `ell` grows.

## 4. Consequences (each labeled)

- **[COUNTEREXAMPLE] `C' <= 2` REFUTED.** Realizable `E_3 = ell+3` (`ell in {43,61}`), `ell+4`
  (`ell in {59,67}`), and **`ell+6`** (`ell = 53`); the excess band reaches **`>= +6`**. The
  bounded-excess ceiling must be restated: there is no uniform `E_3 <= ell + 2` (nor `<= ell + 5`).
- **[COUNTEREXAMPLE] "no realizable `T >= 7`" REFUTED** — the open core named in
  `l1_bounded_excess_structure.md` §6 and continued by `l1_t7_atlas_concurrency.md`. Realizable
  `T = 7` (`ell in {43,61}`), `T = 8` (`ell in {59,67}`), and **`T = 10`** (`ell = 53`).
- **[COUNTEREXAMPLE] the uniform `O(1)` cap `k3 <= 7` is FALSE**, and with it the "`max k3 = 7`
  everywhere, never `8`, does not grow" EXPERIMENTAL reading of `l1_t7_atlas_concurrency.md`
  §0.5/§4. That note's finding was correct *within its search window* (`ell <= 31`, where the max
  genuinely is `<= 7`), but neither extrapolation survives: the max grows **in `ell`** (`8` at
  `43`, `11` at `53`, `9` at `61/71/73`), and at fixed `ell` it **fluctuates** in `p` rather than
  freezing (`ell = 53`: `7, 11, 7, 8, 7`; `ell = 23`: a late record `5 -> 7` at `p = 1657` — §3A);
  the "no growth in `n`" observation holds only inside the `ell <= 31` window where it was
  measured — and even there `ell = 23` eventually breaks it.
- **[SURVIVES — deep-null verified] the `ell = 19` pin `H_19` / `m*(19) = 9`.**
  Exhaustive-up-to-gauge `max k3 = 6` at `ell = 19` across **ALL 80 eligible primes
  `p = 19n+1 <= 13567`** (`n <= 714`; R2 grid, artifact JSON, gate 5; distribution
  `3:42, 4:15, 5:22, 6:1`), attained **uniquely** at `p = 571` — 16x more primes and 12x deeper
  in `p` than this packet previously shipped (5 window primes + 3 spot checks, still verified
  live in gate 2; two R2 rows replayed by this packet's own transversal). So the fat-tail family
  cannot produce a realizable `E_3 >= 22` (excess `+3`) at `ell = 19` **at any tested prime**;
  `H_19` (and the conditional theorem `H_19 => m*(19) = 9` of the open `l1_m19_pin_excess3_atlas.md`,
  PR #399) is **untouched, with materially strengthened evidence**. Coverage is finite (as any
  per-prime scan is) and §3A's late-record phenomenon is the standing caution: `H_19` remains the
  named CONJECTURAL hypothesis, not a theorem. This falsifier family lives at `ell >= 43`, far
  from `19`. (Whether *other* families threaten `H_19` is a separate question, untouched here.)
- **[AUDIT] corrects one measured row of `l1_bounded_excess_structure.md` §5.** Its `(ell=17,p=409)`
  row reported `k3 = 3` from a 1-of-680-plant undercount; the **exhaustive-up-to-gauge `max k3` is `5`**
  (verified, gate 3) — no bearing on any claim there (still `<= 7`), corrected for the ledger.
- **[AUDIT] small-`ell` mirage diagnosis — now a DOUBLE diagnosis.** The prior program searched
  `ell <= 31`, where the exact max is `<= 7`; the `O(1)` reading was an artifact of that window —
  the FOURTH searched-too-shallow reversal in this program, and the first to catch **our own**
  conjecture. A FIFTH instance was then caught **inside this very packet** by panel review: the
  originating lane's `ell = 53` table value (`9`) was itself truncated by its scanner's
  early-exit-at-first-`k3 >= 8` design (§3) — the true max is `11`. Depth-limited search has now
  bitten five times; the mandated counter-measures (exhaustive-up-to-gauge scans with NO early
  exit, per-prime coverage columns, witness-vs-lemma closure) are exactly what §3 ships.
- **[OPEN] new object: the `k3` growth law.** The right question is now the growth RATE of `max k3`
  (the `Theta(ell)` caps `(2ell-5)/3` and `2(ell-1)/3` bracket it from above; realized values reach
  `11` at `ell = 53`, and the growth is visible in both `ell` and `n`), not an `O(1)` bound.

## 5. [OPEN] char-`0` vs char-`p`: refuted over `F_p`; the strict limit is MIXED

The refutation is **over `F_p`**, the program's own setting (`Gamma in F_p[X]`, cosets of
`mu_ell subset F_p^*`), so it stands independent of any characteristic-0 question. On whether any
cap survives in the strict `p/ell -> infty` limit, the evidence is **mixed**, and this is left
**OPEN**. *(Disclaimer, house style: the items below cite `derivation_g3.md` §4 and
`stability_sweep.py`, which are INTERNAL LANE ARTIFACTS, not repo files — EXPERIMENTAL provenance,
unlike the §3 table, whose every row is re-established by this packet's own repo-shipped code.
Given the §3 `ell = 53` truncation finding, the lane's `ell = 59` stability values should be
treated as indicative, not exact.)*
- *Against emptiness / for robustness:* the lane's `max`-over-drops at `ell = 59` stayed in `{8,9}`
  across `p = 709..1889` (`n = 12..32`), never dropping to `<= 7`; and the exhaustive grids show
  high values recurring at scattered large primes (`ell = 53`: `8` again at `n = 44`; `ell = 43`:
  `8` again at `n = 40`; `ell = 23`: a fresh record at `n = 72`) — though as spikes, not a trend
  (§3A).
- *For emptiness / char-`p` flavor:* every *fixed* drop pattern decays in the lane's sweeps (e.g.
  `(0,1,3)` at `ell = 59` gives `9,7,7,6` at `n = 12..20`); no single `Q(zeta_ell)`-lift was
  extracted (needs elimination beyond stdlib). Evidence both ways; no claim either direction. Moot
  for the conjecture, already refuted over `F_p`.

## 6. Appendix — why Lam–Leung (the `#400` mechanism) has no purchase here

In PR #400 (`bc-l4-veronese-top-stratum-empty`) the constrained objects are subsets of `mu_n`, so a
coincidence is a **vanishing sum of roots of unity** — Lam–Leung bites. Here the fiber base-points
are **free** elements of `F_p^*`; `mu_ell` enters only through the ratios `z, z'` and drops `d_i`.
The concurrency `psi_q(x) = psi_q(zeta x)` is `R_zeta(x) = 0` with generic roots — no vanishing sum,
no rigidity. A single 3-fiber already exists in a 2-parameter family; the count is bounded only by
projective transversality, which **permits** the `Theta(ell)` growth §3 realizes. So Lam–Leung was
always moot for this object, and `#400`'s own char-`p` residual (the curve-`M2` Veronese top stratum)
is a **different** object, unaffected.

## 7. Concurrent-work weave (relationship labels; no dependency taken)

- **`l1_bounded_excess_structure.md` (PR #368, integrated).** **Superseded-in-part:** its open core
  *"no realizable `T >= 7`"* is **ANSWERED** (a realizable `T = 7` exists at `ell = 43`; realizable
  `T` reaches `10` at `ell = 53`); its `excess = k3-5` identity and its N1 no-go SURVIVE. Its
  `(17,409)` row is corrected (§4).
- **`l1_t7_atlas_concurrency.md` (PR #379, integrated).** **Superseded-in-part:** its EXPERIMENTAL
  "`max k3 = 7` everywhere / `k3 = 8` never / does not grow with `n`" reading (§0.5/§4) dies for
  `ell >= 43` — the max grows in `ell` (`8` at `43`, `11` at `53`) and, at `ell = 53`, in `n` too
  (`7@n=14 -> 11@n=20`, §3); its `excess = k3-5` identity, the `j+5` over-determination theorem,
  and the ROUTE-CUT all SURVIVE (the no-growth-in-`n` observation holds inside its own `ell <= 31`
  window).
- **`l1_m19_pin_excess3_atlas.md` (PR #399, open).** **Affected:** §1/§3/§5/§6/§7/§8 are corrected
  by a companion amendment on branch `l1-m19-pin-excess3-atlas`; the CONDITIONAL THEOREM
  `H_19 => m*(19) = 9` is **UNAFFECTED** (§4, the `ell=19` pin survives). Its `(19,571)` `k3=6`
  cross-point (from PR #364 `l1_ell19_band_refuted.md`) is the same prime at which this note's
  `ell = 19` max is attained — consistent.
- **`l1_residual_excess_w3_collapse_edge_origin.md` (PR #387, integrated).** **Affected reading:**
  `W3 = [14,3^7]` (`ell=17`) is the *old* `k3 = 7` record; this note supersedes the "`k3 <= 7` is a
  hard ceiling" reading (`k3` reaches `8` at `ell=43` and `11` at `ell=53`). W3 itself as an
  `ell=17` object stands.
- **PR #402 (`x4b`, Hughes moment-column cap, open).** **Non-conflation:** its `k`-cap is an
  ELO / moment-column object over Mersenne reciprocal-gaps; this note's `k3` is a fat-tail 3-fiber
  count over `mu_ell` cosets — different objects, no conflict.

**Maintainer-vocabulary object touched.** This packet feeds the **excess-band** input to `m*(ell)`
via the L1-lane bridge `top-m <= 2m + E_3` (`l1_prime_ell_frontier_corrected.md`): a larger realizable
`E_3` band changes the `m*` accounting. It does **not** touch `prob:row-sharp-q` directly; no prize
contact is claimed.

## 8. Verifier contract

`experimental/scripts/verify_l1_k3_growth_refutation.py` — zero-arg, stdlib, deterministic, exit `0`
iff all pass, `< 60s`; self-contained (embeds all `F_p` machinery; imports no sibling; the §1
nondegeneracy lemma is enforced as an in-code **assertion**, not a silent skip). Gates:
**(1)** rebuild all FOUR primary witnesses (incl. the `ell = 53` `k3 = 11` record) + FOUR band
witnesses (`ell in {61,67,71,73}`) + TWO R2 records (`ell=23@1657`, `ell=43@1721`) from
`(p,ell,D,q)`: recompute spectrum / `E_3` / `T` / excess / `k3` / **`c1`** exactly, check
constant-free and `deg = ell-1` and `mu_1 = ell-3`, cross-check `k3` by the independent pencil
count (primary four + the `ell=23` record), assert the `[40,3^8]` head. **(2)** `ell = 19` pin:
exhaustive-up-to-gauge scan over ALL eligible primes `n in [2,30]` (self-verifies `191` is the
smallest), assert overall `max k3 = 6` (attained only at `p=571, n=30`; `p=191 -> 5`), hence
excess `<= +1`; plus the three beyond-window primes `{647,761,1103} -> 5`. **(3)** growth +
corrections: exhaustive-gauge `max k3` for `ell in {11,13,17,23,29,31}` (all `<= 7`, the mirage
window), `(17,409) -> 5`, `ell=43` gauge reaches `8`. **(4)** `>= 5` tamper self-tests (mutated
`q`-coefficient at `ell=43`, wrong spectrum head, false `k3 = 7` at `ell=43`, mutated `q` on the
`ell=53` `k3=11` record, mutated JSON stats for the `ell=19` deep sweep) — each must be REJECTED.
**(5)** R2 artifact consistency: load
`experimental/data/certificates/l1-e3-law/l1_k3_growth_r2_scan.json` and assert the `ell = 19`
deep-sweep invariants (80 rows; every `k3 <= 6`; `6` uniquely at `(571, n=30)`; distribution
`3:42, 4:15, 5:22, 6:1`; max `p = 13567`), the `ell=23` grid max `7` at `n=72` only, the `ell=53`
grid sequence `1,7,11,7,8,7`, and the 9 four-route witnesses' presence. **Opt-in `--full`**
(~25-35 min, documented): replays live, with NO early exit, every `(ell,p)` pair of the §3
coverage column that is within single-machine budget — the original 37 rows (incl.
`(53,1061) -> 11`, `(53,743) -> 7`, `(59,709) -> 9`) plus `(23,1657) -> 7`, `(43,1721) -> 8`, and
six deterministic `ell = 19` deep-sweep spot rows (`p in {1787,1901,2053,4409,8209,13567}`).
The R2-heavy rows NOT replayed by `--full` (the full 80-prime `ell = 19` sweep; the `ell = 17`
44-prime extension; the exhaustive `61/71/73` scans) are established by the R2 grid artifact +
gate-5 consistency + gate-1 witnesses + this packet's own two-row replay — per-row provenance in
§3's coverage column.

## Refs

- `experimental/notes/l1/l1_sigma_calculus.md` (definitions; the mixed-`Gamma` object; pairwise cap).
- `experimental/notes/l1/l1_bounded_excess_structure.md` (PR #368 — `excess = k3-5`; the "no
  realizable `T >= 7`" open core refuted here; the `(17,409)` row corrected).
- `experimental/notes/l1/l1_t7_atlas_concurrency.md` (PR #379 — the `k3 <= 7`/no-growth EXPERIMENTAL
  reading superseded-in-part; `excess = k3-5`, `j+5` theorem, ROUTE-CUT survive).
- `experimental/notes/l1/l1_m19_pin_excess3_atlas.md` (**open PR #399, not on main — branch
  `l1-m19-pin-excess3-atlas`**; §1/§3/§5/§6/§7/§8 corrected by companion amendment; conditional
  theorem unaffected).
- `experimental/notes/l1/l1_residual_excess_w3_collapse_edge_origin.md` (PR #387, integrated — W3 =
  old `k3=7` record; `k3 <= 7` reading superseded).
- `experimental/notes/l1/l1_e3_charsum_paircap.md` (Lemma R, `k3 <= (2ell-5)/3`);
  `experimental/notes/l1/l1_minj_pencil_freeze.md` (PR #382 — pencil reduction lineage);
  `experimental/notes/l1/l1_ell19_band_refuted.md` (PR #364 — the `(19,571)` cross-point);
  `experimental/notes/l1/l1_prime_ell_frontier_corrected.md` (the `top-m <= 2m + E_3` bridge).
- `experimental/data/certificates/l1-e3-law/l1_k3_growth_r2_scan.json` (the R2 exhaustive grid:
  180 per-prime rows incl. the 80-prime `ell = 19` deep sweep, `by_ell` sequences, 9 four-route
  witnesses; provenance block inside; consumed by gates 1/5 and `--full`).
