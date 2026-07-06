# L1: the min-`j` frontier `[a, ell-a, 9]` frozen (unique-`Gamma` pencil reduction)

**Type: PROVED-LOCAL (two theorems) + AUDIT (the sweep + the pseudorandom-ceiling
mechanism) + EXPERIMENTAL (the freeze law) + OPEN (the root-non-concentration core).**
This note attacks the open core named by `l1_t7_atlas_concurrency.md`
(**PR #379**) Sec 0.2 / Sec 4: the minimal-`j` excess=3 candidate family
`[a, ell-a, 9]` (`ceil(ell/2) <= a <= ell-9`), the *least over-determined*
excess=3 shape on that note's own atlas (over-determination `j+5 = 8`,
against `12`-`14` for the fat-tail shapes it could reach), which it declared
"analytically un-obstructed AND computationally out of exhaustive reach" and
"NOT reached by any tractable plant." Two proved theorems below convert that
frontier from an un-huntable search into a **deterministic per-plant check**:
plant a cap-tight top pair, read the *unique* resulting `Gamma`'s spectrum.
A 2.78M-evaluation sweep of that check then finds a decisive **freeze law** —
the emergent third fiber never approaches the target, anywhere — and
**no refutation of `C' <= 2`.**

**Weave (concurrent, cited by path and number, not depended on).**
`l1_t7_atlas_concurrency.md` (**PR #379**) is the note whose Sec 0.2/Sec 4
this one directly answers: this note *supplies the method* PR #379's own
Sec 4 says does not exist for the `[a,ell-a,9]` family (it calls the
balanced-pair coverage there "thin," reaching only `d<=3` gaps and never a
size-9 third fiber). `l1_bounded_excess_structure.md` (**PR #368**) supplies
the excess identity `excess = T-4-capslack` this note's own sweep is
consistent with (every observed excess stays `<=+2`, matching PR #368's own
`ell in {17,19}` coverage) and the `q`-plane concurrency frame PR #379
extends; not depended on. `l1_ell19_band_refuted.md` (**PR #364**) ships an
`m*(19)<=9` witness at `ell=19, p=571` — the *identical prime* this note's
own sweep independently covers at `ell=19` (Sec 3's `ell=19,p=571` row,
`a=10`); the two notes test different objects at that shared prime (PR
#364's fat-tail-plant listing witness vs. this note's cap-tight pair-plant
frontier check) and do not depend on one another; no conflict. Integrated:
`l1_sigma_calculus.md` proves the pairwise cap `mu_1+mu_2<=ell` via a
pencil-through-two-points argument (its Lemma 3); this note's Theorem 2
independently re-derives the same cap via a lower-degree, fully explicit
route (Sec 2). `l1_e3_law_refuted.md`'s W3 witness (`ell=17,p=137`,
spectrum `[14,3^7]`, excess `+2`) is reproduced here (Sec 3) via a
*different* construction (a cap-tight pair-plant, not W3's own
fat-tail-plant) — a different `Gamma` landing on the identical spectrum.

Notation inherited from `l1_t7_atlas_concurrency.md` / `l1_sigma_calculus.md`:
`ell` odd prime, `ell | p-1`, `H = mu_ell`, cosets `bH` partition `F_p^*`,
`n = (p-1)/ell`. `Gamma(X) = sum_{r=1}^{ell-1} gamma_r X^r` (constant-free,
degree `<= ell-1`); per coset, the max fiber (level set) size `mu_b`; the
sorted spectrum `mu_1 >= mu_2 >= ...`; `E_3 := sum_k (mu_k-2)_+`;
`excess := E_3 - ell`. A **cap-tight pair-plant**: fix `a` with
`1<=a<=ell-1`, plant a size-`a` fiber `F1` in one coset (`b1`) and a
size-`(ell-a)` fiber `F2` in a *distinct* coset (`b2`), i.e. `|F1|+|F2|=ell`
exactly. All arithmetic exact over `F_p`, stdlib only.

**Status legend:** PROVED-LOCAL (proof included, scope stated) / AUDIT
(root-cause / mechanism, independently recomputed) / EXPERIMENTAL
(well-supported, coverage stated honestly) / OPEN (no claim, the named core).

---

## 0. Headline

1. **THEOREM 1 (PROVED) — the unique-`Gamma` crack.** For a cap-tight
   pair-plant, the `(a-1)+(ell-a-1) = ell-2` fiber-coincidence rows on the
   `(ell-1)`-dim constant-free `Gamma`-space ALWAYS have full rank `ell-2`:
   the nullspace is **exactly dimension 1** — never 0, never 2 — for
   *arbitrary* dropsets, no genericity assumed. Hence every cap-tight
   pair-plant determines a **UNIQUE** `Gamma*` (up to scalar), given in two
   independent closed forms (Sec 1), cross-checked against the direct
   nullspace solve on every plant below.
2. **THEOREM 2 (PROVED) — the degree-`(ell-a)` pencil reduction.** Because
   `F1` sits inside a *full* coset of `mu_ell`, the third-fiber question
   reduces exactly to root-concentration of the explicit, low-degree
   polynomial pencil `{P - lambda*A_drop : lambda in F_p}` (degree `ell-a`,
   a genuine drop from `Gamma*`'s own degree `ell-1`) inside *one* coset —
   turning "does `[a,ell-a,9]` occur" into a deterministic per-plant
   read-off rather than a search over an `~C(ell,a)^2*(n-1)`-size dropset
   space. This self-contains the pairwise cap (`mu_3 <= ell-a`, an
   independent, lower-degree re-derivation of `l1_sigma_calculus.md`'s
   Lemma 3) and its twin form gives `mu_3 <= min(a, ell-a)`.
3. **EXPERIMENTAL — the freeze law (Sec 3).** Sweeping the check across
   **2,775,275 evaluations** (1,469,279 random/structured cap-tight
   pair-plants + 1,305,996 hill-climb steps; `ell in {17,19,23,29,31}`, 8
   primes): on the **true frontier** (`ell-a>=9`), the emergent third fiber
   **never exceeds `mu_3=5`** and the excess **never exceeds `+1`** — nowhere
   close to the `mu_3=9` / excess `+3` needed to occupy `[a,ell-a,9]`.
   (A ninth, off-frontier row at `ell=17`, whose `a`-range cannot reach the
   true frontier at all since `ell-9<ceil(ell/2)` there, separately
   saturates the pairwise cap at `mu_3=6` and reproduces the known W3 excess
   `+2` spectrum `[14,3^7]` via a *different* construction — Sec 3.) **Zero
   witnesses; `[a,ell-a,9]` realized by NOTHING tested.**
4. **AUDIT — the mechanism (Sec 4).** A pseudorandom-ceiling model for
   `Gamma*` restricted to a third coset predicts the observed tail
   quantitatively (three spot-checked configs, all within a few percent) and
   pins `P(mu_3>=9)` at `~10^-8` per plant — explaining *why* the freeze
   holds, not merely that it does.
5. **THE RELOCATED CORE (Sec 5, OPEN).** The residual content is exactly:
   does the explicit degree-`(ell-a)` pencil `{P-lambda*A_drop}` ever
   concentrate `>=9` of its roots in one coset? I.e., **`mu_3 <= 8`** for
   this pencil family — a Weil-type root-non-concentration statement, the
   cleanest tractable form yet of the cyclotomic transversality the whole
   program has been circling.
6. **Non-claim.** `C' <= 2` is NOT proved. `[a,ell-a,9]` is not proved empty.
   The freeze law is EXPERIMENTAL (deep, not exhaustive — the dropset space
   is combinatorially enormous, Sec 6). Ships nothing to the prize DAG.

---

## 1. Theorem 1: the unique-`Gamma` crack

**Theorem.** Let `F1 subset` coset `b1`, `F2 subset` coset `b2` (`b2 != b1`),
`|F1|=a`, `|F2|=ell-a`, `1<=a<=ell-1`. Then
`{Gamma : deg<=ell-1, Gamma(0)=0, Gamma const on F1, Gamma const on F2}`
has dimension **exactly 1**.

**Proof.** `F1, F2` are disjoint (distinct cosets) and `0 notin F1 cup F2`
(cosets of `mu_ell` miss `0`), so `|F1 cup F2| = a+(ell-a) = ell` exactly.
The space `W = {p : deg p<ell, p const c1 on F1, p const c2 on F2}` is
parameterized *bijectively* by `(c1,c2) in F_p^2`: for each `(c1,c2)` there
is a unique degree-`<ell` interpolant through the `ell` points of
`F1 cup F2` with those values (Lagrange interpolation on `ell` points fixes
a unique degree-`<ell` polynomial), and distinct `(c1,c2)` give distinct
polynomials. So `dim W = 2` exactly and unconditionally — no genericity, no
dependence on which points are dropped. The constant-free cut `p(0)=0` is a
single linear functional on `W`, nonzero (the `(c1,c2)=(1,1)` member is the
constant `1`, with value `1 != 0` at `X=0`), so it drops `dim` by exactly 1:
`dim(W cap {p(0)=0}) = 1`. The candidate `Gamma* := L - L(0)`, `L` the
degree-`<ell` interpolant `=1` on `F1`, `=0` on `F2`, lies in this space and
is nonzero (else `L` would be constant, impossible since `L` takes both
values `0` and `1`). `QED`

Consequently the `ell-2` coincidence rows always have full rank `ell-2` — no
degenerate dropset exists, for any `a`, any pair of distinct cosets, any
choice of which `a` (resp. `ell-a`) points are kept. **The same argument
generalizes cleanly to non-cap-tight pairs:** for arbitrary fiber sizes with
`|F1|+|F2| = ell-d` (`d>=1`, a strict sub-cover, not necessarily related to
the frontier's own `a`), `dim W = ell-|F1|-|F2|+2 = d+2` by the identical
bijection count (the pair no longer spans a full coset, so the
interpolation freedom grows by `d`), and the same nonzero constant-free
functional drops it to `dim = d+1` — the crack (`d=0`) is the `d+1=1`
special case of one uniform statement, not an isolated coincidence.
Verified exactly (0 exceptions) below.

**Closed form (A): the Lagrange indicator.** `Gamma* = L - L(0)`, as above.

**Closed form (B): Bezout / extended-gcd (independently re-derived here).**
Write `A = prod_{x in F1}(X-x)` (degree `a`), `B = prod_{x in F2}(X-x)`
(degree `ell-a`) — coprime (disjoint root sets), both prime to `X` (since
`0 notin F1 cup F2`). The extended Euclidean algorithm on the pair `(A,B)`
gives the **unique** `P` (`deg P = ell-1-a`), `Q` (`deg Q = a-1`) with
`A*P - B*Q = 1`. Then `A*P` is *itself* a degree-`<=ell-1` polynomial,
constant `0` on `F1` (`A` vanishes there) and constant `1` on `F2` (`B`
vanishes there, so `A*P - B*Q = 1` reads `A*P = 1` on `F2`) — i.e. `A*P` IS
the interpolant `1-L` of closed form (A) (both sides are the unique
degree-`<ell` polynomial through the same `ell` values of `F1 cup F2`, hence
identical). This gives
> **`Gamma* = (1-L(0)) - A*P`**,
a construction from the extended-gcd of the coprime pair `(A,B)` alone, with
no interpolation anywhere — genuinely independent of closed form (A).
*(Found-vs-claimed: an earlier internal draft of this identity stated
`A*P-B*Q=c1-c2` with `P:=(Gamma*-c1)/A`, `Q:=(Gamma*-c2)/B` — substituting
those definitions gives `A*P-B*Q = c2-c1`, sign-reversed from what was
written; a labeling slip with no effect on any downstream number, since the
extended-gcd construction re-derived from scratch here — verified against
the nullspace solve on every plant below — supersedes it. See Sec 6.)*

**Verification.** `experimental/scripts/l1_minj_pencil_kit.py` and
`experimental/scripts/verify_l1_minj_pencil_freeze.py` (independently) solve
the nullspace directly AND construct both closed forms, asserting all three
agree. Live gate counts (this note's own verifier, Sec 8): **>=200
deterministic plants across `ell in {17,19,23}`**, including explicit
adversarial dropsets (contiguous arcs, arithmetic progressions, first-`k`/
last-`k`), nullity exactly 1 and both closed forms matching on every one, 0
exceptions. This reproduces, independently, the original Lane L toolkit's
own verification: `laneL_verify_crack.py` (re-run for this packaging pass)
gives **1500/1500** cap-tight plants (`ell in {11,17,19,23}`, 5 `(ell,p)`
configs x 300 trials) with nullity `=1` and the Lagrange closed form matching
on all 1500, plus **412** non-cap-tight control trials (`d in {1,2,3}`, `ell
in {11,17,19,23}`) with `dim = d+1` exactly on all 412, 0 exceptions in
either set.

---

## 2. Theorem 2: the degree-`(ell-a)` pencil reduction

**Setup.** `F1` is a subset of the *full* coset `H_0` of `mu_ell`
(`|H_0|=ell`), so `A = prod_{x in F1}(X-x) = (X^ell-1)/A_drop`, where
`A_drop := prod_{y in H_0 setminus F1}(X-y)` has degree `ell-a` (the
*dropped* points of `F1`'s own coset). On any third coset `C_k`
(`k != b1, b2`), every point satisfies `X^ell = rho_k` for the coset's own
constant `rho_k`, so `X^ell - 1 = rho_k - 1` is **constant** on `C_k`,
giving `A(x) = (rho_k-1)/A_drop(x)` there. Writing `Gamma* = c1 + A*P` (`P :=
(Gamma*-c1)/A`, exact since `A | Gamma*-c1`, `deg P = ell-1-a`):

> **Theorem 2.** A size-`t` third fiber of `Gamma*` at coset `C_k`, value
> `w`, exists **iff** the explicit polynomial `P(X) - lambda*A_drop(X)`
> (`lambda := (w-c1)/(rho_k-1)`) has `t` roots in `C_k`. Its degree is
> `deg A_drop = ell-a` (since `deg P = ell-1-a < ell-a`) — a genuine
> reduction from `Gamma*`'s own degree `ell-1` to a fixed, explicit,
> degree-`(ell-a)` object.

**Proof.** `Gamma*(x) = w` at `x in C_k` `<=>` `c1 + A(x)P(x) = w` `<=>`
`P(x) = (w-c1)/A(x) = (w-c1)*A_drop(x)/(rho_k-1) = lambda*A_drop(x)` `<=>`
`(P-lambda*A_drop)(x) = 0`. `QED` Consequently `t <= ell-a` — **a
self-contained, independent re-derivation of the pairwise cap** `mu_3 <=
ell-a` (`l1_sigma_calculus.md`'s Lemma 3 proves `mu_1+mu_2<=ell` via a
pencil `alpha*X^ell+beta*Gamma+gamma` through two points; this is a
different, lower-degree route to the same fact in this setting). The
**twin identity**, via `B_drop := prod_{H_0' setminus F2}(X-y)` (`H_0'` =
`F2`'s own coset, `deg B_drop = a`) and `Q := (Gamma*-c2)/B`, gives by the
identical argument `t <= a`; combined,
> **`mu_3 <= min(a, ell-a)`.**

**What this is.** The third-fiber question — a priori a search over the
`(ell-1)`-dim space of possible `Gamma` — reduces to root-concentration of
ONE fixed degree-`(ell-a)` pencil member inside ONE coset of size `ell`: a
strictly lower-degree, fully explicit object, checkable by direct
polynomial evaluation once `(F1, F2)` (equivalently `(A_drop, P)`) are
fixed. This is the mechanism that converts the frontier from "un-huntable"
to "read the spectrum."

**Verification.** Independently re-run for this packaging pass:
`verify_reduction.py` (Lane L's original) gives **1159/1159** tested
max-fibers (`ell in {17,19,23,29}`) with every fiber point confirmed a root
of `P-lambda*A_drop`; the polynomial's degree matches `ell-a` exactly on
**1154/1159** (the remaining 5 land at a strictly *lower* degree — an even
more constrained pencil member, not a violation). This note's own verifier
(Sec 8, gate ii) reproduces the equivalence live on **>=100** freshly
generated plants across `ell in {17,19,23,29}`, checking every eligible
third coset per plant (not just the modal one): **686** coset-level checks,
0 failures.

---

## 3. The sweep and the freeze law

By Theorems 1-2, each plant `(a; b2; F1, F2)` yields one `Gamma*`; reading
its TRUE spectrum (brute force over all `n` cosets) gives `mu_1>=a`,
`mu_2>=ell-a` (planted) and an EMERGENT `mu_3, mu_4, ...` tail.
`[a,ell-a,9]` realized `<=> mu_3=9` co-occurs with `mu_1=a, mu_2=ell-a` (or
any spectrum with `E_3 >= ell+3`). The sweep (`laneL_sweep.py` /
`laneL_climb.py`, both re-run and cross-checked against `laneL_results.json`
for this packaging pass) covers dropsets uniform (85%) + structured
arcs/APs (15%), plus random-restart single-index hill-climbing (both
`mu_3`- and `E_3`-scored); `b1` gauge-fixed to coset `0` (WLOG, the
rotation-by-`zeta` scaling symmetry), `b2` cycled over all others.

**Coverage table** (`a`-range = the true frontier `[ceil(ell/2), ell-9]`;
`ell=17` has NO true-frontier `a` at all — `ell-9=8 < ceil(17/2)=9` — so its
row instead sweeps `[9,ell-3]`, a cap-tight-but-off-frontier substitute kept
for the pairwise-cap-saturation and W3-reproduction data below, and
excluded from every "on the frontier" claim in this note):

| `ell` | `p` | `n` | `a`-range | on frontier? | plants | max `mu_3` | max excess | witnesses |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| 17 | 137 | 8 | 9..14 | **no** (`ell-a<=8`) | 466,224 | 6 (`@ell-a=6`) | +2 (W3-equiv., `[14,3^7]`) | 0 |
| 19 | 229 | 12 | 10 | yes | 294,386 | 5 | +1 | 0 |
| 19 | 419 | 22 | 10 | yes | 153,722 | 5 | +0 | 0 |
| 19 | 571 | 30 | 10 | yes | 150,054 | 4 | +0 | 0 |
| 23 | 277 | 12 | 12..14 | yes | 173,489 | 5 | +1 | 0 |
| 23 | 461 | 20 | 12..14 | yes | 99,586 | 5 | +0 | 0 |
| 29 | 349 | 12 | 15..20 | yes | 72,684 | 5 | +1 | 0 |
| 31 | 373 | 12 | 16..22 | yes | 59,134 | 5 | +1 | 0 |

Total random/structured plants: **1,469,279**. Hill-climb (220s per run,
random-restart + single-index mutation, sideways moves allowed across
plateaus; 1,305,996 total steps): `ell=19,p=229,a=10` — the `mu_3`-scored
climb reaches best `mu_3=5` (`E_3=19`, excess `0`), the *separate*
`E_3`-scored climb reaches best `E_3=20` (`mu_3=4`, excess `+1`) — two
different runs, reported separately to avoid implying a single spectrum
attained both; `ell=23,p=277,a=13` (`E_3`-scored) reaches `E_3=24` (excess
`+1`); `ell=17,p=137,a=9` (`E_3`-scored, off-frontier) reaches `E_3=18`
(excess `+1`). **Local search never beat the random ceiling anywhere on the
frontier** (`mu_3<=5`, excess `<=+1`).

**`mu_3` vs. the tail width `ell-a` (max observed over every source):**

| `ell-a` | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| max `mu_3` | 3 | 4 | 5 | **6** | 5 | 5 | 5 | 5 | 5 | 4 | 5 | 5 | 4 |
| vs. cap `ell-a` | `=` | `=` | `=` | `=` | `-2` | `-3` | **`-4`** | **`-5`** | **`-6`** | **`-8`** | **`-8`** | **`-9`** | **`-11`** |

The pairwise cap `mu_3<=ell-a` **saturates for `ell-a<=6`** (all off the
true frontier, `ell-a<9`), then is **abandoned**: for `ell-a>=7` the third
fiber **freezes at `4`-`5`**, a gap from the cap that widens without bound
as `ell-a` grows. The true frontier (`ell-a>=9`) lives entirely in the
frozen regime, `4`+ below its own target of `9`.

**Global vs. frontier-only summary.** `GLOBAL max mu_3 = 6` (at
`ell=17,ell-a=6` — off the true frontier); **on the true frontier,
`max mu_3 = 5`**. `GLOBAL max excess = +2` (at `ell=17,a=14`, off the true
frontier — see the W3 reproduction below); **on the true frontier,
`max excess = +1`.** Excess `+3` reached **nowhere**, on or off the frontier.
`mu_3=9` reached **nowhere**. **0 witnesses.**

**`mu_3` histograms (three representative rows; full histograms in the
companion JSON, Sec 8):**

| `mu_3` | 1 | 2 | 3 | 4 | 5 |
|:-:|:-:|:-:|:-:|:-:|:-:|
| `ell=19,a=10` (`N=294,386`) | 154 | 246,536 | 46,781 | 907 | 8 |
| `ell=23,a=12` (`N=58,000`) | 12 | 46,449 | 11,312 | 224 | 3 |
| `ell=17,a=9` (`N=78,000`, off-frontier) | 174 | 63,396 | 14,021 | 395 | 14 |

Every row: `mu_3=2` is overwhelmingly modal (`80`-`84%` of plants), the mass
collapses geometrically by `mu_3=4`-`5`, and `mu_3>=6` is never observed in
any of these three rows at all — consistent with the pseudorandom-ceiling
model of Sec 4, which these exact rows feed.

**The W3-equivalent reproduction (off-frontier, `ell=17,a=14`).** The
sweep's `ell=17` excess `+2` maximum reproduces `l1_e3_law_refuted.md`'s W3
spectrum `[14,3,3,3,3,3,3,3]` (`E_3=19=ell+2`) — via a **cap-tight
pair-plant**, a different construction from W3's own fat-tail-plant
(`Gamma = g_0*q + lambda_0` with a size-`(ell-3)` planted fiber alone). The
underlying `Gamma` differs (confirmed: not a scalar multiple of the
original W3 `gamma`). Found by an independent re-search for this packaging
pass (the original sweep recorded only the scalar `max_E3`, not the
exemplar plant) and verified four ways: solved from the raw dropset via
Theorem 1's nullspace, matched against BOTH closed forms of Sec 1, and
checked live against Theorem 2's pencil reduction on three distinct third
cosets — all agree:

```text
ell=17, p=137, a=14  (off the true frontier; ell-a=3)
F1 (14 pts, coset 0)   = [1,16,38,50,56,60,72,73,74,88,115,122,123,133]
F2 (3 pts, coset b2)   = [6,21,33]
gamma (X^1..X^16)      = [69,53,99,58,125,34,26,124,24,65,76,36,103,33,75,1]
spectrum = [14,3,3,3,3,3,3,3]   E_3 = 19 = ell+2   excess = +2
Gamma* on F1 = 42, on F2 = 127 (c1 != c2, as Theorem 1 requires)
```

This is a **reproduction, not a refutation**: excess `+2` is not new (it is
`l1_e3_law_refuted.md`'s own recorded ceiling), and this witness sits off
the `[a,ell-a,9]` frontier entirely (`ell-a=3 < 9`).

---

## 4. Mechanism: the pseudorandom ceiling (AUDIT, quantitatively matched)

Model `Gamma*` restricted to a third coset as a uniform random map
`C_k -> F_p` (`|C_k|=ell`, `p ~ ell*n >> ell`). The expected count, over `N`
plants, of some third coset carrying a `>=t`-fiber is
`~ N*(n-2)*C(ell,t)/p^{t-1}`. Spot-checked against the observed cumulative
histograms (recomputed from the shipped per-config JSONs for this
packaging pass):

| config | `N` | `mu_3>=4` model/obs | `mu_3>=5` model/obs | `mu_3>=9` model |
|:--|:-:|:-:|:-:|:-:|
| `ell=19,p=229,a=10` | 294,386 | 950.2 / 915 | 12.4 / 8 | `~3.6e-8` |
| `ell=23,p=277,a=12` | 58,000 | 241.6 / 227 | 3.3 / 3 | `~1.4e-8` |
| `ell=17,p=137,a=9` | 78,000 | 433.2 / 409 | 8.2 / 14 | `~9.2e-8` |

The model tracks the observed tail within a few percent everywhere except a
mild over-shoot at the small prime `ell=17` (model 8.2 vs. observed 14 at
`t=5` — still the same order of magnitude), and pins `P(mu_3>=9)` at
`~10^-8` **per entire sweep of that size** — i.e., unreachable by chance,
and (via Theorem 2) exactly the statement that the degree-`(ell-a)` pencil
`P-lambda*A_drop` scatters its roots across cosets rather than
concentrating `>=9` of them in one. **This is a heuristic model, not a
proof** — it explains the freeze, it does not establish it.

---

## 5. The relocated core (OPEN)

By Theorem 2, `[a,ell-a,9]` is realizable **iff**, for some cap-tight
pair-plant, some third coset's copy of the pencil `{P-lambda*A_drop :
lambda in F_p}` has a member with `>=9` roots in that one coset (`ell`
points). The precise open statement, stated to be exactly sufficient to
kill the frontier (not the stronger empirical freeze of Sec 3-4):

> **Conjecture (root-non-concentration of the min-`j` pencil).** For every
> cap-tight pair-plant and every third coset `C_k`, no member of the
> degree-`(ell-a)` pencil `P(X) - lambda*A_drop(X)` (`lambda in F_p`) has
> `>=9` roots in `C_k`. Equivalently: **`mu_3 <= 8`** for this family.

This is a genuine root-concentration / Weil-type statement about an
explicit low-degree polynomial family restricted to one coset of `mu_ell`
— the cleanest tractable form yet of the cyclotomic transversality that
`l1_sigma_calculus.md`'s N1 no-go, `l1_bounded_excess_structure.md`'s
route-cut, and `l1_t7_atlas_concurrency.md`'s sharpened Bezout/dimension
route-cut all independently identify as the program's irreducible content.
Sec 3-4's evidence suggests the TRUE ceiling is far tighter (`~5`-`6`, not
merely `8`), but `mu_3<=8` is the minimal statement that empties
`[a,ell-a,9]` outright. No proof is offered here.

---

## 6. Honest ledger

- **Deep-sampled, NOT exhaustive.** The dropset space per row is
  `C(ell,a)^2*(n-1)` (choices of `a`-subset of coset `b1`, `(ell-a)`-subset
  of coset `b2`, and `b2` itself). Restricted to the true frontier rows
  (`ell-a>=9`) this ranges from `~9.4x10^10` (`ell=19,p=229`, the smallest
  true-frontier case) to `~9.9x10^17` (`ell=31,p=373`, the largest swept
  case); the swept plant counts (`5.9x10^4` to `2.9x10^5` per row) sample a
  fraction between `~3.1x10^-6` (best coverage, `ell=19,p=229`) and
  `~6.0x10^-14` (thinnest, `ell=31,p=373`) of the respective space. Coverage
  is real and directed (structured dropsets + hill-climbing target the most
  plausible concentrations) but nowhere near exhaustive for `ell>=19`.
- **WLOG gauges.** `b1` (the coset carrying `F1`) is fixed to coset index
  `0` throughout, using the rotation-by-`zeta` scaling symmetry
  (`Gamma(X) -> Gamma(zeta*X)` permutes cosets transitively and preserves
  every fiber-size spectrum exactly); `b2` is swept over all `n-1` others.
  `a in [ceil(ell/2), ell-9]` is the frontier's own definition (`a<=ell-a`
  WLOG by swapping `F1 <-> F2`, which the frontier's `[a,ell-a,9]` labeling
  already treats symmetrically).
- **Found-vs-claimed corrections (this packaging pass).**
  1. The Bezout-identity sign slip of Sec 1 (an internal draft's
     `A*P-B*Q=c1-c2` should read `c2-c1` under its own `P,Q` definitions) —
     corrected by re-deriving closed form (B) from scratch via the extended
     Euclidean algorithm on `(A,B)` alone (verified against the nullspace
     solve on every plant, Sec 1/Sec 8).
  2. All three of the `_e3`-mode hill-climb scratch JSONs
     (`climb_17_137_e3.json`, `climb_19_229_e3.json`,
     `climb_23_277_e3.json`) carry mode-mislabeled TOP-LEVEL `best_mu3` /
     `best_E3` / `best_excess` fields — an artifact of `laneL_climb.py`'s
     score-tuple ordering swapping under `MODE="e3"` (the printed/top-level
     fields report `(E_3, mu_3, mu_4)` mislabeled as `(mu_3, E_3, excess)`).
     The nested `"best"` sub-record in every climb file carries the correct
     fields regardless of mode (named keys, not tuple-order-dependent), and
     `consolidate.py`'s own `climb_best()` already reads exclusively from
     that sub-record (its docstring: *"mode-independent true (mu3, E3,
     excess) from the correct sub-record"*) — so every number in
     `laneL_analysis.md`, `laneL_results.json`, and this note is unaffected.
     Flagged here only so a future reader of the raw scratch JSON is not
     misled by the top-level fields.
  3. The packaging brief for this note cited "1500+2196" as the crack /
     reduction verification counts. Re-running the shipped scripts gives
     **1500** (crack, cap-tight, `laneL_verify_crack.py`) and **1159**
     (pencil reduction, `verify_reduction.py`) — both exactly matching
     `laneL_analysis.md`'s own citations and both independently reconfirmed
     above (Sec 1, Sec 2); "2196" does not correspond to any reproducible
     total in the shipped Lane L artifacts (a plausible, unconfirmed source:
     `l1_t7_atlas_concurrency.md`'s unrelated `ell=23` atlas-shape count of
     2166). This note uses the reconfirmed figures throughout.
- **Toolchain note.** `laneL_sweep.py` / `laneL_climb.py` / `consolidate.py`
  (the sweep harness) are not shipped as repo files (matching the pattern of
  `l1_t7_atlas_concurrency.md`'s own "Lane I" and
  `l1_bounded_excess_structure.md`'s "Lane G" — internal hunt scaffolding,
  not carried into `experimental/`); every number they produced is
  independently reconfirmed above by re-running the scripts and, for the
  coverage/model tables, by direct recomputation from the shipped histogram
  data. `laneL_core.py` / `laneL_verify_crack.py` / `verify_reduction.py`
  (Theorem 1/2's own toolkit) were run fresh for this packaging pass (Sec 1,
  Sec 2); their logic is repackaged, independently, into
  `l1_minj_pencil_kit.py` (Sec 8).

---

## 7. Non-claims

`C' <= 2` is **NOT proved.** `[a,ell-a,9]` is **NOT proved empty** — this
note converts it into a deterministic check and reports a deep, directed,
non-exhaustive sweep finding no occupant, nothing more. The freeze law
(`mu_3<=5` on the true frontier) is **EXPERIMENTAL**: a heuristic mechanism
(Sec 4) explains it quantitatively but does not prove it, and the dropset
space is combinatorially far larger than what was swept (Sec 6). The
`mu_3<=8` statement of Sec 5 is **OPEN** — stated precisely, not attempted.
No claim is made about `ell>=37`, nor about any non-cap-tight or
non-balanced-pair plant family. This note ships nothing to the prize DAG
(`experimental/data/prize-dag/prize_dag.json` is untouched) and supersedes
nothing already integrated.

---

## 8. Verifier contract

`experimental/scripts/verify_l1_minj_pencil_freeze.py`: zero-arg, stdlib,
offline, deterministic; exit 0 iff all five gates pass; self-contained (a
FRESH reimplementation — different coset construction, i.e. grouping by
`x^ell` directly rather than a generator/primitive-root search, and a
differently-ordered two-phase Gaussian elimination — that does **not**
import `l1_minj_pencil_kit.py` or any sibling script). Measured runtime
**~2s** zero-arg (target `<90s`).

- **Gate i (crack theorem).** `>=200` deterministic plants (seeded-random +
  explicit adversarial dropsets: contiguous arcs, arithmetic progressions,
  first-`k`/last-`k`) across `ell in {17,19,23}`: nullity `==1` and both
  closed forms (Lagrange indicator, Bezout/extended-gcd) match the direct
  nullspace solve, on every one.
- **Gate ii (pencil reduction).** `>=100` plants across
  `ell in {17,19,23,29}`, every eligible third coset checked per plant
  (`>=100` coset-level checks): fiber size `t` equals the root count of
  `P-lambda*A_drop` there, with degree `<=ell-a`.
- **Gate iii (freeze-table consistency).** A deterministic live subsample
  (120 plants) per row of the 8-row Sec 3 coverage table: the subsample's
  `max_mu3` must never exceed the recorded value, on every row; and an
  embedded exact frontier witness (`ell=19,p=229,a=10`, spectrum
  `[10,9,5,...]`) must reproduce `mu_3=5` exactly at a true frontier row
  (`ell-a>=9`) — guaranteeing the ceiling reproduction rather than trusting
  subsample luck.
- **Gate iv (W3-equivalent reproduction).** The Sec 3 witness
  (`ell=17,p=137`, `F1`/`F2` embedded) reconstructs to the exact spectrum
  `[14,3,3,3,3,3,3,3]`, `E_3=19`, excess `+2`, with both closed forms
  agreeing with the nullspace solve.
- **Gate v (model-vs-observed spot check).** The three Sec 4 ratios
  recomputed from the embedded per-row histograms, both the model formula
  and the observed cumulative counts, against the quoted table values.
- `--tamper-selftest`: corrupts one datum per gate (a reference `Gamma`
  solve, a pencil-check result, the recorded freeze ceiling, a plant point,
  a histogram tail count) and asserts each targeted gate then FAILS. All
  five caught.

`experimental/scripts/l1_minj_pencil_kit.py`: the companion constructor
toolkit (both closed forms, the pencil-reduction check, deterministic demo
mode — no args, no randomness — reconstructing the `ell=17` W3-equivalent
pair-plant and the `ell=19,a=10` true-frontier example). Not imported by the
verifier (independence, per the ground rule above); a citable, reusable
library for any future `[a,ell-a,X]` hunt.

Companion data:
`experimental/data/certificates/l1-e3-law/l1_minj_freeze_ledger.json`
(coverage table, `mu_3`-vs-tail table, global and frontier-only maxima, the
W3-equivalent witness, the model-vs-observed table, dropset-space/coverage-
fraction figures). Zero witnesses => no
listing-chain (`run_chain.py`) invocation needed.

---

## Refs

- `experimental/notes/l1/l1_t7_atlas_concurrency.md` (**PR #379**, branch
  `l1-t7-atlas-concurrency`, concurrent open PR, cited by path and number,
  not depended on) — the atlas that names `[a,ell-a,9]` the true, least
  over-determined open frontier and calls it un-huntable; this note
  supplies the method.
- `experimental/notes/l1/l1_bounded_excess_structure.md` (**PR #368**,
  branch `l1-bounded-excess-structure`, concurrent open PR, cited by path
  and number, not depended on) — the excess identity and `q`-plane frame
  this note's sweep is consistent with.
- `experimental/notes/l1/l1_ell19_band_refuted.md` (**PR #364**, branch
  `l1-ell19-band-refuted`, concurrent open PR, cited by path and number, not
  depended on) — shares a prime (`ell=19,p=571`) with this note's own
  coverage table via a different construction; no conflict.
- `experimental/notes/l1/l1_sigma_calculus.md` (integrated) — the pairwise
  cap (Lemma 3), independently re-derived here via Theorem 2's lower-degree
  route; the N1 no-go this note's Sec 5 core answers to.
- `experimental/notes/l1/l1_e3_law_refuted.md` (integrated) — the W3 witness
  (`ell=17,p=137`, `[14,3^7]`) reproduced in Sec 3 via a different
  (cap-tight pair-plant) construction.
- `experimental/scripts/l1_minj_pencil_kit.py`,
  `experimental/scripts/verify_l1_minj_pencil_freeze.py`,
  `experimental/data/certificates/l1-e3-law/l1_minj_freeze_ledger.json` —
  this note's own artifacts.
