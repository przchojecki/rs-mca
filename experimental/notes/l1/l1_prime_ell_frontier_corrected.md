# L1 Prime-`ell` Listing Frontier, CORRECTED: `m*(ell) = (ell+3)/2`, refuting `ceil(2ell/3)`

Status legend on every claim: **PROVED** (rigorous) / **LEMMA** (proved step) /
**NUMERIC** (verified by exact solve-based `F_p` computation, not sampled, not yet
proved) / **OPEN** (obstruction named). Companion zero-arg verifier
`experimental/scripts/verify_l1_prime_ell_frontier_corrected.py` (stdlib, deterministic,
exit 0 iff all gates pass; a hidden `--tamper-selftest` flips one datum per gate class and
confirms each gate then fails). Upstream frame at 3d7f341: `l1_prime_ell_pv_refutation.md`
(the `m=t+1` reduction, Lemma LF, the refuted conjecture), `l1_prime_ell_onset.md`
(Theorem R, Lemma R), `l1_general_reconstruction_collapse.md` (PR #219, the reduction it
feeds), `l1_full_list_quotient_proof_program.md` (Lemma 8, the counting bound #219
supersedes). This note consolidates two independent derivation routes (A = rotation-coupling /
pencil-locality, B = exact rank criterion) plus a solve-based spectrum lab (C); the routes
were PI-cross-audited against each other (see §7).

Notation (all upstream-PROVED). `ell` odd prime, `ell | p-1`, `H = mu_ell <= F_p^*`,
cosets `bH` partition `F_p^*`, `n = (p-1)/ell`. `Gamma(X) = sum_{r=1}^{ell-1} gamma_r X^r`
constant-free, `deg <= ell-1`, mixed `<=> Gamma != 0`. Per coset `b`,
`mu_b = max_lambda #{x in bH : Gamma(x) = lambda}` (max fiber). `top-m` = sum of the `m`
largest `mu_b`. At the onset `m = t+1` a mixed full-petal codeword is **listed** (`=>` a
stabilizer-primitive mixed minimal kernel set at prime `ell`) iff its retained core
`R = top-m >= 2ell` (`l1_prime_ell_pv_refutation.md` §1). **Listing threshold: `top-m >= 2ell`.**

---

## 0. Headline

**(1) The `ceil(2ell/3)` frontier conjecture is REFUTED (NUMERIC-exact, explicit witnesses;
UNCONDITIONAL — independent of the KEY LEMMA of §3).**
`l1_prime_ell_pv_refutation.md` §4 (Frontier conjecture, L164-165; the pre-integration
draft's §2.3) states: *for prime `ell`, `m=t+1`, listing occurs iff `m >= m0 := ceil(2ell/3)`*.
This is false. We exhibit explicit constant-free `Gamma` whose full-petal codeword **lists**
at `m = (ell+3)/2 < ceil(2ell/3)`:

| `ell` | `ceil(2ell/3)` (conjectured `m*`) | corrected `m* = (ell+3)/2` | listing witness (this note) | verdict |
|------:|:---------------------------------:|:--------------------------:|:----------------------------|:--------|
| 7  | 5 | 5 | `top-5 = 14 = 2ell` (S1) | both agree (no refutation at `ell=7`) |
| 11 | 8 | **7** | `top-7 = 22` (`p=199`), `23` (`p=331`) | **`m*=7 < 8`: conjecture REFUTED** |
| 13 | 9 | **8** | `top-8 = 27` (`p=313`) | **`m*=8 < 9`: conjecture REFUTED** |

Each `ell in {11,13}` witness is a **full, lambda-free, primitive mixed kernel codeword**
assembled and checked point-by-point (§5, verifier gate vi) — the same NUMERIC-exact standard
as the upstream `ell=7` PV refutation. So the refutation is **unconditional** (a single
explicit object at each `ell`), not merely spectrum-side. It also corrects the upstream note's
own achieved-onset table, which reported `m*(11)=8`, `m*(13)=10` from *light* search: solve-based
rank-drop plants reading honest full-coset spectra reach `2ell` a full step lower (§6).

**(2) The corrected two-sided picture: `m*(ell) = (ell+3)/2` for every prime `ell >= 7`.**
The frontier is pinned from both sides:

> **Upper (`m* <= (ell+3)/2`): UNCONDITIONAL** — the explicit lambda-free witnesses above (§5).
>
> **Lower (`m* >= (ell+3)/2`, i.e. `top-m < 2ell` for all `m <= (ell+1)/2`): the VACANCY
> THEOREM, rigorous *modulo* the KEY LEMMA `E_3 <= ell-3`** (§3-§4); **unconditional at
> `ell=7`, where `(ell+1)/2 = 4` is exactly Theorem R.**

`(ell+1)/2` and `(ell+3)/2` are consecutive, so the two sides meet with no gap.
`(ell+3)/2 < ceil(2ell/3)` for every prime `ell >= 11` (`= (9-ell)/6 < 0`), so the
corrected law refutes the conjecture at every `ell >= 11`; at `ell = 7` both give `5`.
**Boundary `ell = 5` is excluded from the law:** there Theorem R already makes
`m = 4 = (ell+3)/2` vacant (`max_Gamma top-4 = 9 < 10 = 2ell`, `l1_prime_ell_onset.md` L86,
re-confirmed by **exhaustive** WLOG search over all constant-free `deg <= 4` `Gamma` at `p=41,61`;
`ell5_boundary.py`), and at `m=5`, `max_Gamma top-5 = 10 = 2ell` (**NUMERIC, spectrum-side**;
same exhaustive search; the §5 lambda-freeness/full-codeword chain is NOT run at `ell=5`), so
`m*(5) = 5 > (ell+3)/2` on the spectrum side.
The clean `(ell+3)/2` law begins at `ell = 7`.

**(3) What replaced the broken closing step.** Theorem R (`t=3`, `m=4`) closes by pair-cap
(Lemma R: `sum_b mu_b(mu_b-1) <= B := (ell-1)(ell-2)`) + Cauchy-Schwarz; the CS bound
`top-m <= (m + sqrt(m^2+4mB))/2` first reaches `2ell` at **`m=5` for every `ell`** (verifier
gate iii-analog / `B_checks` CHECK 7), so the moment method has no bite past `m=4`. The
missing ingredient is **realizability** — a rank statement, not a moment statement — captured
by the exact rank formula (§2) and the KEY LEMMA (§3). This is "Theorem R one notch up".

---

## 1. The `m = t+1` reduction and the object of study (upstream-PROVED)

At `m = t+1` every DFT sector `g_r` (`r >= 1`) of a full-petal codeword collapses to a constant,
so `Gamma(X) = sum_r gamma_r X^r` is one FIXED constant-free polynomial and the retained set on
each core coset is a single LEVEL SET of `Gamma`; hence `max R = top-m` of the `mu`-spectrum
(`l1_prime_ell_pv_refutation.md` §1, PROVED). The frontier question is therefore purely:
*how large can `top-m(Gamma)` be for constant-free `deg <= ell-1` `Gamma`?* The coincidence
conditions are **linear** in `gamma`: two points `x, x'` of one coset share a value iff
`gamma . (v(x)-v(x')) = 0`, `v(x) = (x, x^2, ..., x^{ell-1})`; a fiber of size `nu` imposes
`nu-1` such rows.

---

## 2. The PROVED toolkit

**2.1 Elementary bound (PROVED; verifier gate ii; `B_checks` CHECK 2, `A_checks` L7).**
Write `E_3 := sum_b (mu_b - 2)_+` and `a := #{b : mu_b >= 2}` (the spread). Then

> **`top-m <= 2m + E_3`**, and sharper **`top-m <= m + min(m,a) + E_3`.**

*Proof.* `max(mu_b, 2) = 2 + (mu_b-2)_+`, so `top-m <= sum_{top m} max(mu_b,2) <= 2m + E_3`;
if `a < m` the top-`m` includes `m-a` cosets with `mu=1`, giving `top-m = m + a + E_3`. ∎
Tight: the `ell=11` `p=199` witness saturates `top-7 = 2*7 + E_3 = 14+8 = 22` (gate ii anchor);
the concentrated `Gamma` (§2.3) saturates the sharper `m + min(m,a) + E_3` at `a=1`.

**2.2 Exact rank formula (PROVED; verifier gate iii; audited 0-violation on 45 configs
(`B_checks` CHECK 1) + 70 pattern configs (`B_e1.py`)).** For fibers `F_1,...,F_K` on distinct cosets,
`P = sum_k |F_k|` distinct points, the `P-K` coincidence rows `{v(x)-v(anchor_k)}` have

> **`rank = (P-K) - delta`,  `delta := dim(D cap Z)`,**

where in `F_p^P`: `D = {lambda : sum_{i in F_k} lambda_i = 0 for all k}` (within-fiber-mean-zero,
`dim = P-K`) and `Z = {lambda : sum_i lambda_i V(x_i) = 0}`, `V(x)=(1,x,...,x^{ell-1})`. A nonzero
`Gamma` realizing all `K` fibers exists **iff `rank <= ell-2`**.
*Proof.* the rows are `phi(D)` for `phi : e_i |-> V(x_i)` whose kernel is `Z` and whose image
lands in the constant-free `(ell-1)`-space; `dim phi(D) = (P-K) - dim(D cap Z)`. ∎

> **[PI-mandated dim-Z convention.]** `dim Z = (P-ell)_+` for the full Vandermonde including
> constants, equivalently `(P-ell+1)_+` for the constant-free system; `D cap Z` and the rank
> formula are identical under both conventions. (The fiber rows live on *differences*
> `v(x)-v(x0)`, which annihilate the constant `r=0` coordinate, so the intersection with `D` is
> convention-independent; the verifier computes `delta` from the full `V(x)` rows `r=0..ell-1`.)

*Corollary (generic `delta=0`, PROVED):* for points in general position `Gamma` exists iff
`sum(mu_k-1) <= ell-2`; rank drops (`delta > 0`) are exactly what the extremal spreads exploit.
The naive dimension cap `#{mu >= nu} <= floor((ell-1)/(nu-1))` is FALSE (the `ell=7` extremal
`[3,3,3,3,2,2,2]` has `#{mu>=3}=4 > 3`, `delta >= 3`).

**2.3 The geometric / concentrated `Gamma` is a NON-LISTER (LEMMA; verifier gate v;
`A_checks` L6-geom, `B_checks` CHECK 3; PI-cross-probed at 6 `(ell,p)` pairs).** The geometric
family `gamma_r = C tau^r` (in particular the concentrated `Gamma = X + X^2 + ... + X^{ell-1}`,
`tau=C=1`) has spectrum **`[ell-1, 1, 1, ..., 1]`**: one coset with `mu = ell-1`, all others
`mu = 1`. Hence `E_3 = ell-3` (saturated) but spread `a = 1`, and

> **`top-m = ell + m - 2 <= 2ell - 3 < 2ell` for every `m <= ell-1`** — it never lists.

*Proof.* On `bH`, `f(Y)=Gamma(bY)` is a Mobius map in `t=tau Y` of determinant `C(1 - (tau b)^ell)`,
injective off the single coset `(tau b)^ell = 1`, where it degenerates to the `(ell-1)`-fiber. ∎
So the pair-cap saturator (the natural worry, and the reason the moment method is exhausted)
is **disjoint** from the `top-m` extremal: listing is entirely about *spreads of small fibers*.

**2.4 `T1(ell in {5,7}) = Theorem R` (PROVED scope statement; `A_checks`
A_frontier_map).** Route A's realizability lemma T1 (`top-m < 2ell` for
`m <= ceil(2ell/3)-1`) has, for `ell in {5,7}`, **no content beyond Theorem R**: the pair-cap +
CS ceiling already covers `m <= 4`, and `ceil(2ell/3)-1 <= 4` there, so T1's window is empty and
the frontier at `ell in {5,7}` *is* the pair-counting result. Genuinely new content lives at
`ell >= 11`, window `m in [5, ceil(2ell/3)-1]`, where the pair-cap permits `top-m >= 2ell` but
realizability forbids it — exactly the regime the KEY LEMMA controls.

---

## 3. The KEY LEMMA `E_3 <= ell-3` (NUMERIC, tight)

> **KEY LEMMA (NUMERIC).** Every mixed `Gamma` has `E_3 = sum_b (mu_b - 2)_+ <= ell-3`.
> Equivalently (rank form): any **realizable** `K`-fiber config has `sum_k (mu_k - 2) <= ell-3`,
> i.e. the rank drop `delta <= K-1`.

**Evidence.** 0 violations over **> 4·10^5** exact solve-based `Gamma` at `ell = 7, 11, 13`
(441,118, summed over the five `(ell,p)` runs of `B_e5.py`; verifier gate iv reruns a bounded
seeded solve-based sweep). **Saturated** by two
structurally different extremals: the concentrated `Gamma` (`E_3 = ell-3`, `a=1`, every `ell`)
and the spread witnesses (`ell=7`: `[3,3,3,3,2,2,2]`; `ell=11`: `[4,4,3,3,3,3,2,2]`, `E_3=8=ell-3`).
The **non-realizable** high-excess configs (`[6,6],[5,5],[4,4,4],[4,4,3,3]` at `ell=7`) all have
`sum(mu-2) >= ell-2` and full rank `ell-1` (`delta > K-1`) — the contrapositive (`B_checks` CHECK 5).

**Rank-lemma reduction (PROVED equivalence).** On `Z`, the sum of the `K` fiber-sum functionals
`fs_k` is the `r=0` Vandermonde row, `≡ 0`, so `rank(fs|_Z) <= K-1` and
`delta = dim Z - rank(fs|_Z) >= dim Z - (K-1)`. Hence the KEY LEMMA is exactly:

> **realizable `<=>` the fiber-sum functionals are NOT full-rank on `Z` (`rank(fs|_Z) <= K-2`)**;
> equivalently, if `sum(mu_k-2) >= ell-2` then `rank(fs|_Z) = K-1` (non-realizable). **This is the
> single OPEN core.**

**Three PROVED cases of the reduction.**
1. **Generic (`delta=0`): PROVED.** `sum(mu_k-1) <= ell-2` forces `E_3 <= ell-2-K <= ell-4 < ell-3`.
2. **Single shared value: PROVED (degree bound).** Fibers sharing one value `lambda` are roots of
   `Gamma - lambda`, total size `<= deg Gamma <= ell-1`; so if the `K` fibers share a value,
   `sum mu_k <= ell-1` and `sum(mu_k-2) <= ell-1-2K <= ell-3`. The obstruction to a full proof is
   precisely the coupling **across distinct fiber-values** (one `Gamma`, many cosets).
3. **`P = ell+1` (the `[4,4]`, `[5,3]` case at `ell=7`): PROVED-numerically non-realizable.**
   `dim Z = 1`; the unique dependency is the divided-difference `lambda_i = 1/prod_{j != i}(x_i-x_j)`,
   and realizable `<=>` it is within-fiber-mean-zero; over the **complete** reduced search
   (0 realizable / 35525 configs at `p=211`, 0/57575 at `p=337`) it never is (`B_checks` CHECK 4).
   `ell`-specific: at `ell=11`,
   `P=8<ell` so `dim Z=0` and `[4,4]` IS realizable (matching the S1 census). Route A supplies the
   parallel balanced-two-fiber residue identity for this stratum (`A_checks` L5b).

*(A sharper NUMERIC form `E_3 <= max(0, deg Gamma - 2)`, 0 violations over 22400 exact-degree
`Gamma`, specializes to `E_3 <= ell-3` at `deg = ell-1` and may be the more tractable proof route;
`B_e7.py`.)*

---

## 4. The VACANCY THEOREM (LEMMA-conditional on §3)

Combining §2.1 (`top-m <= 2m + E_3`) with §3 (`E_3 <= ell-3`):

> **VACANCY THEOREM (rigorous *modulo* the KEY LEMMA).** For prime `ell`, `m = t+1`:
> **`top-m < 2ell` for all `m <= (ell+1)/2`** — i.e. no primitive mixed kernel set below the
> frontier. Unconditionally PROVED at `ell = 7` (`(ell+1)/2 = 4`, this is Theorem R).

*Proof.* `top-m <= 2m + (ell-3) < 2ell <=> 2m < ell+3 <=> m <= (ell+1)/2`. ∎
This strictly extends Theorem R (only `m=4`, all `ell`) to `m <= (ell+1)/2` (`= 6, 7, ...` at
`ell = 11, 13, ...`) **through realizability**, the ingredient the moment method provably cannot
reach (§2.4). Together with §5 it forces `m* = (ell+3)/2` (ell >= 7). **Label: this vacancy band is
LEMMA-conditional** (on the KEY LEMMA); the witness side (§5) is not.

---

## 5. The listing witnesses (NUMERIC spectrum-side; lambda-freeness PASS `=>` UNCONDITIONAL)

Each witness is a fixed constant-free `Gamma` at a fixed prime. **Spectrum** (`top-m >= 2ell`) is
**NUMERIC-exact**, recomputed by two independent implementations (generator-coset power-sum vs
`x^ell`-grouping Horner) that agree (verifier gate i). **Lambda-freeness** is then checked by the
ported #260 V1 chain (verifier gate vi; `d1_v1_witness_check.py` machinery, adapted to
`(t,m) = (6,7)`/`ell=11` and `(7,8)`/`ell=13`): the surjectivity `rank = m` instantiates the
PROVED Lemma LF (`l1_prime_ell_pv_refutation.md` §2, general `m=t+1`); a **distinct-nonzero** scalar
preimage `c_1..c_t` and a `g_0` are exhibited; an explicit `P` of `deg <= m*ell` agrees `= c_i` on
all `t*ell` petal points, retains `R = top-m >= 2ell` on the core, and its missed core is a
**minimal, primitive (mixed)** kernel set (independent CRT-degree oracle, not the #219 reduction).

| `ell` | `p` | `m=t+1` | `gamma` (X^1..X^{ell-1}) | spectrum head | `top-m` | `R` (per core coset) | `deg P` | `|M|` (min. kernel) | lambda-free |
|------:|----:|:-------:|:-------------------------|:--------------|:-------:|:---------------------|:-------:|:-------------------:|:-----------:|
| 11 | 199 | 7 | `[1,172,129,7,90,84,119,194,176,1]` | `[4,4,3,3,3,3,2,2,1]` | **22** = 2ell | 22 = `[4,4,3,3,3,3,2]` | 76 <= 77 | 55 | **PASS** |
| 11 | 331 | 7 | `[97,29,97,239,171,92,143,155,270,1]` | `[5,5,4,3,2,2,2,1,1]` | **23** > 2ell | 23 = `[5,5,4,3,2,2,2]` | 76 <= 77 | 54 | **PASS** |
| 13 | 313 | 8 | `[254,289,29,276,242,219,201,261,79,232,133,1]` | `[5,4,4,3,3,3,3,2,2,2]` | **27** > 2ell | 27 = `[5,4,4,3,3,3,3,2]` | 104 <= 104 | 77 | **PASS** |

**Verdict of the lambda-freeness gate (from this note's verifier run, gate vi):** all three
witnesses PASS the full chain — `lam_free = True`, full primitive-mixed-kernel codeword assembled
and checked point-by-point. Per PI-calibration (ii), **because the gate PASSES the listing claims are
UNCONDITIONAL** (full codewords exhibited, NUMERIC-exact), not spectrum-side-only. This is a genuine
advance over the upstream note, which assembled the explicit codeword at `ell=7` only and confirmed
merely `rank = m` (surjectivity) at `ell = 11, 13` — here the distinct-nonzero scalars, the explicit
`P`, the retention `R = top-m`, minimality, and primitivity are all exhibited at the LOWER onset
`m = (ell+3)/2`. (Had any witness FAILED lambda-freeness, its claim would revert to spectrum-side
NUMERIC; none did.)

**Methodology — solve, don't sample.** Every witness was found by *solving* the coincidence
conditions (exact `F_p` nullspace), never by sampling `gamma`-space. This is not a convenience: at
the closely related `N_list` measurement, pure random sampling of `gamma`-space found
**0 of 201600** trial points crossing the threshold (D's capture-rate check), so the planted/solved
construction is the only route by which any of these rare, rigid witnesses is reachable.

---

## 6. Reconciliation with the upstream onset table

`l1_prime_ell_pv_refutation.md` §4 reported achieved `m*(11)=8`, `m*(13)=10` (the latter flagged
"search-limited"), from the *light* S1 search (2-3 simultaneous fiber-coincidence patterns).
Solve-based rank-drop plants using 4-8 simultaneous patterns (a greedy beam chain-builder, every
extension an exact nullspace solve over the full coset range, triple-cross-checked spectra) reach
`top-7 = 22-23` at `ell=11` and `top-8 = 27` at `ell=13` — a full step below. The apparent
"`+2 per t`" smoothness of the shallow search is a **search-depth artifact**: the achievable
`top-m` jumps sharply (discontinuously) between `m=6` and `m=7/8`. At `ell=13`, `m=8` is a HARD
positive (explicit witness), while `m=7` topped out at `top-7 = 24 < 26` in a deep-but-bounded
search — evidence for, not proof of, `m*(13) = 8` exactly (the VACANCY THEOREM supplies the missing
`m <= 7` vacancy, modulo the KEY LEMMA).

---

## 7. Cross-audit, caps, and status ledger

**Cross-audit.** Routes A (pencil-locality) and B (exact rank) were developed independently and
agree on every shared claim; the geometric non-lister (A) was PI-cross-probed at 6 `(ell,p)` pairs;
the rank formula (B) was audited 0-violation on 45 (`B_checks` CHECK 1) + 70 (`B_e1.py`) configs. The listing witnesses
were triple-cross-checked (methodA=methodB=methodC) in lab C. `A_checks.py` (41/41 PASS) and
`B_checks.py` (all CHECK 1-7 PASS) were both re-run to green before this note's claims were used.

**Caps (explicit).**
- KEY LEMMA `E_3 <= ell-3` is **NUMERIC** (> 4·10^5 solve-based `Gamma` at `ell in {7,11,13}`;
  441,118 via `B_e5.py`, 0 violations, saturated), **not proved**; the OPEN core is the fiber-sum full-rank statement on `Z`
  (§3). Consequently the VACANCY THEOREM (§4) and the *lower* half of `m* = (ell+3)/2` are
  LEMMA-conditional. The **upper** half (witnesses, §5) and the **refutation of `ceil(2ell/3)`**
  (§0.1) are unconditional.
- The `(ell+3)/2` law is stated for **`ell >= 7`**; `ell = 5` is the excluded boundary
  (`m*(5) = 5`: the `m=4` vacancy half is Theorem R (PROVED); the `m=5` listing half is
  NUMERIC spectrum-side only — `top-5 = 10 = 2ell` by exhaustive search, `ell5_boundary.py`,
  lambda-freeness not checked). Witnesses are exhibited only at `ell in {7,11,13}`; `ell >= 17`
  (where `(ell+3)/2 < ceil(2ell/3)` also predicts refutation) is **not** witnessed here — OPEN.
- The verifier's gate-iii/iv sweeps are **bounded and seeded** (16 rank configs incl.
  `rank == ell-2`/`ell-1` boundary and `delta>0` cases; ~700 solve-based `Gamma` at
  `ell in {7,11}`); they are a spot-suite re-confirmation, not the full `B_e5` census.
- Whether the spread `E_3` attains `ell-3` for *every* `ell` (hence `m* = (ell+3)/2` sharply) is
  confirmed at `ell = 7, 11, 13`; larger `ell` is OPEN (a harder-search question, orthogonal to the
  vacancy theorem).

**PROVED.** §2.1 elementary bounds; §2.2 rank formula (+ generic corollary); §2.3 geometric
non-lister; §2.4 T1(`ell in {5,7}`)=Theorem R; §3 the rank-lemma reduction and its three cases
(generic, single-value, `P=ell+1`); Lemma LF surjectivity (upstream). **UNCONDITIONAL (witnesses).**
The `ell in {11,13}` full lambda-free primitive-mixed-kernel codewords listing at `m = (ell+3)/2`,
refuting `ceil(2ell/3)` (§0.1, §5). **NUMERIC (tight, 0 violations, saturated).** KEY LEMMA
`E_3 <= ell-3`; the frontier `m* = (ell+3)/2` at `ell = 7, 11, 13`. **LEMMA-conditional.** The
VACANCY THEOREM `top-m < 2ell` for `m <= (ell+1)/2` (on the KEY LEMMA). **OPEN.** A proof of the KEY
LEMMA (= the fiber-sum full-rank statement on `Z`); whether `m* = (ell+3)/2` persists for `ell >= 17`.

---

## 8. Ledger placement

The three witnesses are **stabilizer-primitive mixed minimal kernel sets** at prime `ell`; they land
in the `L_prim` (primitive) stratum of `pma_wide_residual` (`L(D) = L_quot ∪ L_lowdef ∪ L_prim`,
3d7f341), the stratum that node restated as open — supplying explicit occupants at the corrected
onset `m = (ell+3)/2` and lowering the recorded onset (`m*(11): 8 -> 7`, `m*(13): 10 -> 8`) under the
problem tag `prob:v13-l1-residuals`. The VACANCY THEOREM's band (`top-m < 2ell` for
`m <= (ell+1)/2`, modulo the KEY LEMMA) feeds `petal_mixed_amplification`: it is the realizability
input — a rank statement the pair-count cannot see — that closes the low side of the amplification
window and pins where primitive listings can first appear.

Related normal form on `main`: the coset-chart residue bridge
(`experimental/notes/l1/l1_coset_chart_residue_bridge_v1.md`, integrated
2026-07-04) classifies capped kernel sets in this same coset-petal frame as
quotient-coset vs residue-line; the witnesses above are nonvacuous instances
of its residue-line branch at the corrected onset.
