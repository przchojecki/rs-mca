# L1 Petal Growth Table — `N_list(7,p)` at the `m=t+1` Onset (E16 / Q2.9, orthogonal-axis evidence)

Repo target: `experimental/notes/l1/l1_petal_growth_nlist_e16.md`.
Verifier: `experimental/scripts/verify_l1_petal_growth_nlist_e16.py` (this packet's
`verify_l1_petal_growth_nlist_e16.py`; zero-arg, stdlib-only, `.out` transcript
included).

Status legend on every claim (repo convention): **PROVED** (rigorous) /
**LEMMA** (proved step) / **NUMERIC** (verified by exact solve, never sampled
for existence) / **OPEN** (obstruction named, not closed).

Author: packaging pass over the wave_t1 `T4`/`D` agent's measurement
(`D_nlist_note.md`, `D_nlist.json`, `D_lib3.py`, `D_witnesses_p*.json`,
`D_capture_rate.{py,json,out}`, `D_fit.py`), auditing it, adding an independent
verifier, and adding the calibration items (lambda-freeness scope, `dim Z`
convention) this wave's PI review requires. All computation stdlib-only,
solve-based (existence claims are never established by random sampling).

## 0. Provenance and relation to E16 (what this is, and isn't)

**(a) Provenance.** This packet offers **axis-orthogonal NUMERIC steering
evidence** relevant to roadmap order **E16** and DAG node `pma_wide_residual`
— **alongside, not as a literal instance of,** the order's own ask, quoted
verbatim from `experimental/notes/roadmaps/overnight_orders_2026_07_03.md`:

> `E16 [petal growth table / Q2.9] (M)  Fixed-excess petal counts vs`
> `d - ell = c for c <= 6 on toy rows (CRT compression makes each`
> `finite).`
> `INTERPRET: flat/poly growth => imgfib prior up + selects between`
> `correlated-GS and descent for pma_wide_residual (the M-scaling`
> `exponent decides which) | growth in c => escalate R3 immediately.`

**E16's literal ask — a table indexed by fixed excess `c <= 6` — is already
fully and rigorously delivered by the sibling "bounds half" packet alone**
(item 1 below, PROVED-COMPILER). This packet's own axis is the prime `p` at
fixed petal count `t=4`, which is **neither** the order's `c` nor the DAG
node's `M`; at this packet's own razor witness the effective excess
`|M|-ell` is 14 (per `l1_prime_ell_pv_refutation.md` §3b: `|M|=21=(t-1)*ell`
at `ell=7`), far outside the order's literal `c<=6` scope. So this packet
does **not** itself close E16's literal fixed-excess-table request — what it
adds is a third, orthogonal-axis NUMERIC data point bearing on the *same
INTERPRET clause* (flat/poly growth vs. growth, now in a different
parameter), consistent with — but not a substitute for — the bounds-half
packet's literal closure (see §9 for how the two relate).

Three packets now jointly bear on E16/`pma_wide_residual`, along **three
different axes** — this is made explicit here because none of the three is a
re-measurement of another, and **only the first is a literal instance of
E16's own request**:

1. **Bounds half (proved, axis = excess `e=d-ℓ` at fixed petal count `M`):**
   `experimental/notes/l1/l1_petal_fixed_excess_compiler.md`, PROVED-COMPILER,
   citing `l1_full_list_quotient_proof_program.md` Lemma 16. For every fixed
   `E`, the fixed-excess full-petal layer count is
   `binom(M,2) q + 2^M Σ_{e=1}^E q^{e+1}`, and since `M = O(log n)` at the L1
   cutoff, `2^M q^{E+1} <= n^{O(1)}` for every fixed `E` — fixed-excess extras
   are polynomially controlled, cannot be the asymptotic obstruction.
2. **Baseline (numeric evidence, axis = petal count `M` at fixed toy `p`):**
   `experimental/notes/l1/l1_petal_auxiliary_wide_regime_evidence.md` (E4, PR
   #186). Exact toy window `F_109, ℓ=3, d=5`: Johnson-covered rows (`M=3,4`)
   empty under both tested scalar schedules; wide sub-Johnson rows are
   nonempty from `M=9` on under both schedules, and at `M=6` only under the
   **geometric** schedule (`4` polys, max agreement `8`) — the **linear**
   schedule's `M=6` row is empty, same as `M=3,4` (`M=12` is tested only
   under the linear schedule: `2023` auxiliary polynomials, max agreement
   `11 < 36^3`) — verdict `NO_SUPERPOLY_SIGNAL_IN_EXACT_TOY_WINDOW`.
3. **This packet (numeric measurement, axis = prime `p` at fixed small
   `(t,ℓ,m)=(4,7,5)`):** `N_list(7,p)`, the aggregate listed-mixed-codeword
   *count* left open by the P2 frontier-theory note (§4b; pre-integration
   wave_t1 material, cited here the way `D_nlist_note.md` itself cites it —
   not yet an upstream repo path), measured across `p=71..337` at the
   smallest onset instance of the razor case in
   `l1_prime_ell_pv_refutation.md` §3b (`(t,ℓ,m)=(4,7,5)`, `m=t+1`).

**Notation warning (read before comparing (2) and (3)):** the roadmap/DAG
literature's capital `M` (petal count, as in E4's "`M=3,4,6,9,12`" and the
`pma_wide_residual` DAG node's "`M = O(log n)`") is the **same role** as the
coset-sunflower literature's lowercase `t` (petal count) in
`l1_prime_ell_pv_refutation.md`/`D_nlist_note.md`/this packet — **not** the
lowercase `m` (core/missed-coset count) used in the same coset-sunflower
literature. In this packet `t=4` is **fixed** throughout; the varying
parameter is the prime `p`. So despite the shared word "growth," (2) varies
petal-count-`M` at fixed `p`, and this packet varies `p` at fixed
petal-count-`t=4` — two different axes of the same qualitative question (see
§9 for how they combine).

**DAG node `pma_wide_residual`** (`experimental/data/prize-dag/prize_dag.json`
at upstream `3d7f341`), restated after the pullback counterexample:

> `L(D) = L_quot ∪ L_lowdef ∪ L_prim`. Quotient-pullback stratum: REAL,
> exponential-in-`M`, charged to the quotient-profile budget (poly-but-budgeted).
> Low-defect stratum: covered by fixed-excess machinery. **Corrected target: the
> PRIMITIVE RESIDUAL** — non-pullback, non-low-defect wide sub-Johnson lists are
> polynomial.
> Attack surface: (a) correlated-target strengthening of GS; (b) descent
> (auxiliary-problem extras are degree-`d` objects — same problem at smaller
> `(k,σ)`, iterate until Johnson-safe). **Q2.9 fixed-excess data calibrates
> both.** Falsifier: an adversarial many-petal family (R3 attack) with
> super-poly auxiliary list.

The `m=t+1` mixed/primitive listed codewords this packet counts are exactly
`L_prim`-type objects (primitive = not a union of full `H`-cosets; at prime
`ℓ` this is automatic for any mixed missed core, per
`l1_prime_ell_pv_refutation.md` §1) at the smallest nontrivial petal count.

## 1. Setting

Background-free coset sunflower over `F_p`, `H = μ_ℓ` (`ℓ | p−1`, `ℓ` odd
prime), `n = (p−1)/ℓ` cosets. `Γ(X) = Σ_{r=1}^{ℓ−1} γ_r X^r` (constant-free,
`dim = ℓ−1`); per coset `b`, `μ_b = max_λ #{x∈bH : Γ(x)=λ}`; `top-m` = sum of
the `m` largest `μ_b`. This is the **same `Γ`** as Route B's realizability
note and PV-refutation's §1 "`m=t+1` structure" section (which defines the
same `Γ` used later by Lemma LF in §2) — this packet's `γ ∈ F_p^6` (`ℓ=7 ⟹
dim=6`) is literally that object.

**Convention sentence (PI calibration, applies across this wave's packets):**
`dim Z = (P−ℓ)_+` for the full Vandermonde including constants, equivalently
`(P−ℓ+1)_+` for the constant-free system; `D∩Z` and the rank formula are
identical under both conventions. In this packet's own construction (two
3-fiber seed conditions, `P=6` points, `K=2` fibers, `ℓ=7`), `P−ℓ+1 = 0`, so
`dim Z = 0` is forced regardless of convention — consistent with (not
separately re-derived from) the empirical fact recorded in `D_nlist_note.md`
§1.3 that the seed system is rank-4/nullspace-dim-2 at **every** one of the
32,400 combos tried (`off_path_seen=0`), i.e. `δ=0` throughout. This packet
does not use Route B's `δ = dim(D∩Z)` rank formula directly (it solves each
system by Gaussian elimination instead); the sentence is recorded here for
cross-packet consistency, not as load-bearing machinery of this measurement.

**Listing threshold (Route B's convention, `l1_prime_ell_pv_refutation.md`
§1):** at `m=t+1`, `top-m ≥ 2ℓ` **iff** a mixed full-petal codeword is
*listed*, **conditional on λ-freeness, verified separately upstream**. See §5
below for exactly what this means for the numbers in this packet.

## 2. Headline (NUMERIC)

**`N_list(7,p)` is empirically FLAT/bounded across `p=71..337`
(`n=10..48` cosets) — not growing with anything like the trivial bound's
exponent.** Measured (orbit-corrected, documented **lower bound**, see §6):
**305, 1235, 1869, 1150, 1600, 1368** at `p=71,113,127,197,211,337`.
Excluding `p=71` (smallest `n=10`, a visible finite-size/boundary point), the
remaining 5 points sit in **1150–1869** (mean 1444) across a `2.98×` range in
`p` — under `1.7×` spread in the count. Trivial bound: `O(p^{ℓ−2+t+m})` =
`O(p^{5+4+5})=O(p^{14})`; at `p=337`, `p^{14} = 337^{14} ≈ 2.44×10^{35}`
(exactly `243,679,285,283,393,666,208,253,061,306,357,089`) vs the measured
`1368` — **~32 orders of magnitude** below the trivial bound. (Both figures
re-derived directly from the 6-prime table by this packet's verifier gate 7,
added after an earlier draft's arithmetic — `4.4×10^{35}`/`33 orders`/`2.75×`
— was found to have drifted from the table; see also the corrected pairwise
exponent in §4's Fit below.)

## 3. Method

Condensed from `D_nlist_note.md` §1 — see that note / `D_lib3.py` for the
full derivation; independently re-audited for this packet (§7 and the
verifier).

**"2-seed, let the top-5 emerge" construction.** Fix one seed coset at
position 0 (WLOG, shift symmetry) and a second at `gap` (all `gap=1..n−1`,
uncapped); impose a 3-fiber pattern at each (all `15×15=225` pattern pairs at
`ℓ=7`, uncapped) — 4 linear conditions in the 6-dim `γ`-space. **Empirically
always exactly rank 4** (nullspace dim 2) at every one of 32,400 combos tried
across the 6 primes (`off_path_seen=0` throughout). Scan **all `p+1` points
exactly** (not sampled) of the resulting 2-dim family via a precompute-once,
affine-update speedup (cross-validated byte-for-byte against a slow
from-scratch path, `D_test6.out`, 0 mismatches); for every point whose
**actual** (honestly computed, full `n`-coset) top-5 sum reaches `≥ 2ℓ`,
register `(config = its own top-5 coset tuple, normalize_γ(γ))` as one raw
witness.

**Orbit correction (LEMMA, PROVED — and independently re-derived and
strengthened for this packet, §7).** A raw `(config,γ)` pair's shift-orbit
(`γ_r → γ_r·c^r`) has `n` members; exactly `c := #{cosets in config with
honest fiber ≥3}` of them are reachable by this 2-seed construction (both
seeds require fiber `≥3`). Summing weight `n/c` over every distinct
discovered key recovers the orbit's exact true size. `c∈{3,4}` in every
witness found (`c=0,1` are impossible: `c≤1` caps the top-5 sum at
`≤7+4·2=15`... more precisely rules out reaching `14` reliably by this
construction's own requirement that both seeds show fiber `≥3`).

Config-class Burnside enumeration and config-fixed profile-A/B/C/D search
(`D_lib2.py`) were also built (exact) but used only for scoping/sampling, not
as the primary driver — see §6 for why, and for the undercount this exposes.

## 4. Data

| p | n=(p−1)/7 | combos (uncapped) | raw distinct (config,γ) | configs hit | c-histogram | **N_list (orbit-corrected)** |
|---|---|---|---|---|---|---|
| 71  | 10 | 2025  | 101 | 15 | {3:63, 4:38}  | **305.0** |
| 113 | 16 | 3375  | 240 | 33 | {3:206, 4:34} | **1234.7** |
| 127 | 18 | 3825  | 332 | 59 | {3:250, 4:82} | **1869.0** |
| 197 | 28 | 6075  | 141 | 37 | {3:70, 4:71}  | **1150.3** |
| 211 | 30 | 6525  | 184 | 52 | {3:88, 4:96}  | **1600.0** |
| 337 | 48 | 10575 | 94  | 15 | {3:60, 4:34}  | **1368.0** |

**Fit** (least squares, `log N_list = slope·log p + intercept`, stdlib-only,
reproduced exactly by this packet's verifier gate 1):

- **All 6 points:** slope = **+0.768** (`N_list ~ 22.8·p^{0.77}`).
- **Excluding p=71:** slope = **−0.071** (statistically flat).
- **Pairwise (consecutive) exponents:** +3.01, +3.55, −1.11, +4.81, −0.34 —
  wildly inconsistent in sign/magnitude: at this scale, **prime-to-prime
  arithmetic idiosyncrasy dominates any smooth trend** (the same phenomenon
  `d1_s1_frontier.md` §5 documented for the closely related max-top-m
  statistic). A single exponent should **not** be quoted as *the* answer.
  (The first value is corrected from an earlier draft's `+3.12`; recomputing
  `log(N_list(113)/N_list(71))/log(113/71)` from the table above gives
  `+3.009`, machine-checked by this packet's verifier gate 7. The other four
  values check out to rounding.)
- **Verdict (NUMERIC, conjecture-strength, not proof):** data are consistent
  with `N_list = O(1)` to `O(p^{0.1})` in the tested range — certainly not
  approaching `O(p^{14})` — but the data cannot distinguish "truly bounded"
  from "grows like `log p`" or "grows like `p^{0.05}`" at this scale (§10 OPEN).

## 5. Lambda-freeness scope

(PI calibration — read before citing `N_list` as a codeword count.)

`N_list(p,ℓ) = Σ_configs #{mixed Γ : top-m spectrum ≥ 2ℓ}` is, by construction
and by its own defining equation (P2 frontier-theory note §4b(b), quoted
there: `N_list(p,ℓ) = Σ_{configs} #{ mixed Γ : top-m spectrum on the m core
cosets ≥ 2ℓ }`), a count of **spectrum-side** `(config,Γ)` pairs — exactly
what that note calls "**the spectrum side**" ("*I certify the spectrum side;
V1 certifies the scalar side*"). Promoting a single such `Γ` to an actual
**listed mixed codeword** additionally needs, per **Lemma LF**
(`l1_prime_ell_pv_refutation.md` §2, PROVED there): the linear map
`(c_1..c_t,u,v) → (λ_1..λ_m)` is **unconditionally surjective** for any `t`
distinct petal labels and `m=t+1` distinct core labels (so *some* scalar
preimage always exists) — but a further **genericity** step, not automatic,
is required: a preimage with `c_i` pairwise **distinct and nonzero**
(avoiding `O(t^2)` bad hyperplanes), which Lemma LF's own proof states holds
"generically for large `p`" and is checked **per witness**, not for free.

**This packet stays entirely on the spectrum side.** No `(c,u,v)` scalar
system was solved, and no distinct-nonzero-`c` genericity check was run, for
any of the 1092 raw `Γ`'s in the 6-prime census. That per-witness gate — the
"V1"/lambda-freeness machinery ported from #260's `d1_v1_witness_check.py` —
was run in this wave only against 3 named witnesses at `ℓ=11,m=7,p∈{199,331}`
and `ℓ=13,m=8,p=313`, **none of which are `ℓ=7` instances from this packet**.
**Correction (this run): the actual location of that check is the sibling
Wave 2 packet's `note_l1_prime_ell_frontier_corrected.md` / repo target
`experimental/notes/l1/l1_prime_ell_frontier_corrected.md`
(`verify_l1_prime_ell_frontier_corrected.py` gate vi, itself commented "port
of #260 `d1_v1_witness_check.py`"; not yet an upstream path as of this
writing) — **not** "the routes B/C packets": the actual wave_t1 source notes
for those routes disclaim having done this (`B_realizability_note.md` calls
the `p=199` witness's lambda-freeness "the standing V1 task, not re-checked
here"; `C_frontier_fill.md`'s own Scope section states none of its witnesses
have had lambda-freeness checked). Re-running gate vi confirms a genuine
PASS (`lam_free=True`, full codeword assembled and checked point-by-point)
for all 3 witnesses. Consequently:

- **The `N_list` counts and the flat/bounded verdict (§2, §4) are NUMERIC
  claims about `Γ`-existence, unconditional on lambda-freeness** (they do not
  claim any specific codeword was assembled).
- **Any restatement of `N_list` as "this many distinct listed mixed
  codewords exist"** is additionally **conditional on lambda-freeness** in
  the same sense flagged in `l1_prime_ell_pv_refutation.md` §1 and Route B's
  note (`B_realizability_note.md`: "listed ... iff top-m ≥ 2ℓ (conditional on
  λ-freeness, verified separately upstream)") — this packet does not
  discharge that condition for its own witnesses and flags this explicitly
  rather than silently assuming it.
- Given Lemma LF's surjectivity is unconditional and only the finitely-many
  bad-hyperplane exclusion remains, this conditionality is expected to be
  generically vacuous at these prime sizes (consistent with the fact that it
  *was* discharged for the two hand-picked razor/primary witnesses at exactly
  this `(t,ℓ,m)=(4,7,5)`/`(5,7,6)` parameter point in
  `l1_prime_ell_pv_refutation.md` §3) — but "expected generically vacuous" is
  **not** the same as "checked for these 1092 instances," and this packet
  does not claim the latter.

## 6. Undercount (NUMERIC, documented, ~1.6–1.7×)

The 2-seed construction only discovers witnesses reachable via a clean
2-coset simultaneous-3-fiber seed — genuinely 3-or-more-way simultaneous
rank-drops (config-fixed profiles B/C/D: `[4,3,3,2,2]`/`[3,3,3,3,2]`/
`[3,3,3,2,2]`) are **not** covered by the primary driver. Running the
(config-fixed) profile A+B+C+D search on a **sample** of already-hit configs:

| p | configs sampled | 2-seed witnesses | profile-A/B/C/D witnesses | extra | missed by A/B/C/D |
|---|---|---|---|---|---|
| 71  | 6 | 35 | 59 | +24 (**+69%**) | 0 |
| 211 | 6 | 16 | 26 | +10 (**+63%**) | 0 |

**Zero misses**, consistently **~60–70% more** — every `N_list` number in §4
is a documented **lower bound**; the true value is plausibly **~1.6–1.7×**
higher (still the same order of magnitude, does not change the flat/`≪p^14`
verdict — a constant multiplicative factor doesn't change an exponent). This
1.6–1.7× is itself a small (12-config, 2-prime), non-exhaustive sample; a
fully "unrestricted" B/C/D construction was not attempted (time budget).

## 7. New audit finding: the orbit-correction weight is exact, not just generic

(LEMMA, PROVED — tightens `D_nlist_note.md`'s original hedge that the
orbit-correction weight `n/c` holds only "generically.")

`D_nlist_note.md` states the shift-orbit "has `n` members **generically**;
`n/5` in the rare fully-periodic case." This packet closes that hedge:

> **Lemma (exact pair-orbit size).** Fix `ℓ`, `p=nℓ+1`, nonzero
> `Γ=(γ_1,...,γ_{ℓ−1})`. If `Γ` has **at least two nonzero coordinates at
> distinct exponents** `r_1≠r_2` (`1≤r_1,r_2≤ℓ−1`), the `n` shift-images
> `normalize_γ(shift_k(Γ))`, `k=0,...,n−1`, are **pairwise distinct** — so the
> `(config,Γ)`-pair orbit under the `Z/n` shift action has size **exactly
> `n`, regardless of whether the underlying config is itself periodic**
> (invariant under a smaller rotation).
>
> *Proof.* `normalize_γ` divides by the first nonzero coordinate. For
> `k≠k'` in `0..n−1`, `shift_k(Γ) ~ shift_{k'}(Γ)` (projectively) forces, from
> the `r_1,r_2` coordinate ratio, `g^{(k−k')(r_2−r_1)}=1`, i.e.
> `(k−k')(r_2−r_1) ≡ 0 (mod nℓ)` (`ord(g)=p−1=nℓ`). But
> `nℓ − (n−1)(ℓ−2) = 2n+ℓ−2 > 0` always, so `|(k−k')(r_2−r_1)| < nℓ` whenever
> `0<|k−k'|<n`; the congruence then forces `(k−k')(r_2−r_1)=0` exactly, i.e.
> `k=k'` (since `r_2≠r_1`) — contradiction. So all `n` are distinct. `∎`
>
> The **only** case the `n/5` exception can occur is a **monomial** `Γ`
> (exactly one nonzero coordinate): then every shift normalizes to the same
> basis vector regardless of `k`, and the pair-orbit collapses exactly to the
> config's own rotation-orbit (`n`, or `n/5` if the config is periodic).

**Audit (NUMERIC):** a direct scan of all **1092** raw witnesses across the
full 6-prime census (`D_witnesses_p{71,113,127,197,211,337}.json`) found
**zero** monomial `Γ`'s — every witness has `≥2` active coordinates, so the
Lemma applies to all of them and the `n/c` weight used throughout §4/§6 is
**exact**, never `(n/5)/c`, for every witness actually discovered (including
on the one prime/config pair where the periodicity precondition is even
*available*: `p=71`'s periodic config `(0,2,4,6,8)`, hit by 21 of the 101 raw
witnesses there — none of the 21 is monomial, confirmed both by the direct
scan and by this packet's verifier gate 3, which reconstructs one such
witness's full 10-member shift-orbit from scratch and confirms it has
exactly 10 distinct members, not 2).

**Reproducibility scope of the "0/1092" figure (added post-audit).** The full
1092-witness scan above was run once, this session, against
`D_witnesses_p{71,113,127,197,211,337}.json` — pre-integration wave_t1
scratch files that are **not** shipped with this packet (§12 Files marks them
"not yet upstream paths"). As shipped, nothing in the repository lets a
future reader re-run that exact 1092-witness scan. To close as much of this
gap as the time budget allows, **this packet's verifier gate 6 independently
re-scans every raw witness its own gate 2 recomputes from scratch** (now
`p=71,113,127`, **673 of the 1092** witnesses, `61.6%`) for the same
monomial-`Γ` exception, in memory, with no dependency on the wave_t1 files,
and confirms 0 found. **The remaining 419 witnesses (`p=197,211,337`, 38.4%)
are covered only by this session's one-off scan and are not independently
reproducible from the artifacts this PR ships** — flagged here explicitly
rather than left implicit in the "0/1092" headline (see also `pr_body.md`
and `agents_log_entry.md`, updated to carry the same caveat).

## 8. Caps / truncations

(Consolidated, faithfully reproduced from `D_nlist_note.md` §2/§6 — nothing
below is newly softened or dropped.)

1. Only 6 primes tested (71,113,127,197,211,337), none above 337 (cost
   scales ~`n·p` per combo; `p≥421` would cost several minutes to hours,
   traded off against more, cheaper, mid-range points to characterize noise).
2. **Primary method (2-seed) is a proven LOWER BOUND**, not an exact count —
   only discovers witnesses reachable via a clean 2-coset simultaneous-
   3-fiber seed. Quantified undercount ~60–70% via a 12-config supplementary
   sample (§6), itself non-exhaustive.
3. Config-class Burnside enumeration was built and verified exact, but is
   **not** what produced the headline numbers (scoping/sampling use only).
4. Capture-rate check (§9) run only at `p=71` (200 random slices × 14
   configs in the original `D_capture_rate.py` run; this packet's own
   verifier reruns a further-reduced, seeded replica, see §9); not repeated
   at `p=211/337`.
5. `off_path_seen=0` at every prime tested (32,400 combos) means the
   dim`≥3` fallback path was never exercised in practice in the original
   census — flagged in case it fires on untested primes.
6. Gap range and pattern-pair range are full/uncapped at every tested prime
   (the one place a sub-sample would have been tempting and was not taken).
7. **(New, §7)** the exact-orbit-size lemma's hypothesis (`Γ` non-monomial)
   is verified for all 1092 witnesses actually found, not proved to hold for
   every conceivable future witness at untested primes (monomial `Γ`'s
   achieving top-5 `≥2ℓ` are not ruled out in general, just never observed
   here).
8. **(New, §5)** lambda-freeness / distinct-nonzero-`c` genericity is not
   checked per-witness for any of the 1092 `Γ`'s in this census; `N_list`
   is a spectrum-side count, and its promotion to a codeword count is
   conditional (see §5).

## 9. Capture-rate result: solve-don't-sample vs. descent/correlated-target

(NUMERIC steering, not proof.)

**Capture rate (task requirement, ground rule "solve, don't sample"):** at
`p=71`, pure random sampling of `γ`-space finds **0 of the 305 (orbit-
corrected)/101 (raw) witnesses**: **0/201,600** random-slice trial-points
(200 independent random 2-dim slices × 72 points/slice (`p+1` at `p=71`) × 14
configs (8 hit + 6 non-hit negative controls)) crossed the threshold, vs. 101
raw witnesses found by the planted/solved 2-seed construction on the same
prime. This is a clean, decisive, NUMERIC confirmation that solving the
coincidence conditions is not merely more efficient than random sampling here
— it is the *only* way any of these witnesses were ever going to be found
(random sampling would report `N_list≈0` and entirely miss this term).

**Relevance to E16's INTERPRET clause and `pma_wide_residual`.** Per §0's
notation warning, this packet's own growth axis is `p` (at fixed `t=4`), not
petal-count `M` — so this is **not** a direct measurement of the "`M`-scaling
exponent" `pma_wide_residual`'s attack surface names. What it *does* add: a
**second, axis-orthogonal NUMERIC data point** that the family of counts
around the primitive-residual question tends to stay small/flat rather than
exploding toward the trivial bound's exponent — reinforcing E4's own
(petal-count-axis, different toy model) `NO_SUPERPOLY_SIGNAL` finding rather
than re-deriving it. Per E16's own stated interpretation rule ("flat/poly
growth ⟹ imgfib prior up + selects between correlated-GS and descent... the
[scaling] exponent decides which"), both of these tame/flat, orthogonal-axis
NUMERIC results point the same way: they raise the prior on
`pma_wide_residual`'s `L_prim` stratum being tractable by **descent or
correlated-target strengthening rather than needing to counter a genuine
amplification mechanism** — stated here as **NUMERIC steering evidence for
which attack surface to prioritize, explicitly not a proof** that `L_prim` is
polynomial (that remains `pma_wide_residual`'s open TARGET status; this
packet does not close it and does not claim to).

*(E15 is not cited in this packet — E15's `worst_word_planted` sigma-scope
question is a different, unrelated evidence line and does not bear on
`N_list`.)*

## 10. OPEN

- **Bounded vs. `log p` vs. `p^{0.05}`-type growth are indistinguishable at
  this scale (OPEN).** The honest range, maximally conservative about the
  §6 undercount, is roughly 500–3200 across `p=71..337`, dwarfed by `p^{14}`
  either way — but the data cannot tell "genuinely `O(1)`" from "slowly
  growing, noise-dominated at these small `p`." Closing this needs either
  much larger `p` (this project's existing `ℓ=7` prime list already includes
  883,1009,1471,2017 — untested here; marginal cost scales roughly
  quadratically in `p`, so `p=2017` would cost on the order of 60–80× the
  `p=337` run's 219s, several hours, out of this pass's budget) or a
  theoretical argument (none attempted here).
- **Closing the profile-B/C/D "unrestricted" construction** to remove the
  §6 ~1.6–1.7× undercount rather than just bounding it (OPEN).
- **Lambda-freeness / distinct-nonzero-`c` genericity for this census's 1092
  `Γ`'s** is not checked (§5, OPEN as a per-witness question; expected
  generically vacuous, not verified).
- **Whether a monomial-`Γ` witness can achieve `top-5≥2ℓ`** at some untested
  prime (§7, OPEN; not observed in 1092 tested instances, not ruled out).

## 11. Reproducibility

```bash
python3 experimental/scripts/verify_l1_petal_growth_nlist_e16.py
```

Zero-arg, stdlib-only, ~20s total. Recomputes `N_list(7,p)` from scratch at
`p=71,113,127` (full/uncapped scope; this recomputation ports the same
`D_lib3.two_seed_census` algorithm the original wave_t1 measurement used —
it catches transcription/copy-paste drift between the stored table and its
source, not a bug shared by both, since no CAS is available in this
stdlib-only environment for a truly independent method), reproduces the
log-log fit arithmetic against the full 6-prime table, cross-checks **all
6** stored `N_list` entries at tight tolerance against the note's own
c-histogram data (gate 5 — added post-audit so a drift on the 3 entries
gate 2 does not recompute is no longer caught only by gate 1's much looser
fit tolerance), reconstructs the exact-orbit-size lemma (§7) from scratch on
two concrete `p=71` witnesses (one on the periodic config, one generic) and
separately monomial-scans all 673 witnesses gate 2 recomputes (gate 6, §7's
reproducibility caveat), re-derives the three headline narrative figures in
§2/§4 directly from the table (gate 7), reruns a reduced/seeded capture-rate
replica, and runs a tamper self-test (deliberately corrupted copies of the
reference data, the c-histogram cross-check, the monomial-scan, the
headline-number constants, and the "expected `c`" target must be, and are,
rejected) before trusting any real gate. Exit 0 + summary iff every gate (0-7)
passes; nonzero otherwise. See `verify_l1_petal_growth_nlist_e16.out` for a
transcript of a passing run.

## 12. Files

- `note_l1_petal_growth_nlist_e16.md` — this file.
- `verify_l1_petal_growth_nlist_e16.py` / `.out` — self-contained verifier +
  transcript.
- `agents_log_entry.md`, `pr_body.md` — packaging metadata.

Upstream sources cited: `experimental/notes/roadmaps/overnight_orders_2026_07_03.md`
(E16 order), `experimental/notes/l1/l1_petal_fixed_excess_compiler.md` (bounds
half), `experimental/notes/l1/l1_petal_auxiliary_wide_regime_evidence.md` (E4
baseline), `experimental/notes/l1/l1_full_list_quotient_proof_program.md`
(Lemmas 2/16), `experimental/notes/l1/l1_prime_ell_pv_refutation.md` (Lemma LF,
razor case §3b, lambda-freeness), `experimental/data/prize-dag/prize_dag.json`
node `pma_wide_residual` (all at upstream `3d7f341`).
Pre-integration wave_t1 sources (this packet's own measurement basis, not yet
upstream paths): `D_nlist_note.md`, `D_nlist.json`, `D_lib3.py`, `D_lib2.py`,
`D_s1_lib_copy.py`, `D_witnesses_p{71,113,127,197,211,337}.json`,
`D_capture_rate.{py,json,out}`, `D_fit.py`, `D_audit.{py,out}`.
Sibling Wave 2 packet cited directly (§5; not yet an upstream path as of this
writing): `note_l1_prime_ell_frontier_corrected.md` / repo target
`experimental/notes/l1/l1_prime_ell_frontier_corrected.md`, and its verifier
`verify_l1_prime_ell_frontier_corrected.py` (repo target
`experimental/scripts/verify_l1_prime_ell_frontier_corrected.py`) — gate vi
is where the 3 named `ℓ∈{11,13}` witnesses' lambda-freeness is actually
checked (ported from #260's `d1_v1_witness_check.py`), not the wave_t1
routes B/C source notes.
