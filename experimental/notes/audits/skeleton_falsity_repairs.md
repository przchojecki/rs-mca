# cs25_cap_v12 skeleton falsity-and-repair packet (five negation certificates, first-grid chain discharged)

Packet type: statement-layer falsity audit + repair + discharge (lane 20; fourth
Lean packet in the #765/#822/#881 line, same conventions as the CircleCode
repair packet and the Fiber-discharge packet).  Target: the four remaining
skeleton files of `experimental/lean/cs25_cap_v12` — the README's own "main
completion queue" — before anyone spends proof effort on false targets.

Base: `3404d21b64c876c6d9b995ad3e29d7120ab27a54` (origin/main at packet time,
the reviewed-PR integration sweep).  A pre-edit scan of all open PRs found none
touching `cs25_cap_v12/`; the four target modules were untouched since the
sweep.

Package: `experimental/lean/cs25_cap_v12` (pinned `leanprover/lean4:v4.28.0`,
mathlib per the package's own `lake-manifest.json`).

Honesty discipline (as in the prior packets): **negation claims are never
sorried** — every "false as written" verdict below is a fully proved,
kernel-checked Lean theorem over a concrete instance; where a negation proof
would be disproportionate, the finding is graded PLAUSIBLE, documented, and
**no falsity claim is made**.

## What was done

1. Five skeleton statements shown **FALSE as written**, each with a proved
   negation lemma and a paper-anchored statement repair (findings 1–5 below).
2. Three statements **PROVED**: the repaired
   `RSCap.prop_graded_rational_floor` (wrapper over the proved deep floor),
   `RSCap.cor_quantitative_first_grid_floor` (statement unchanged; via the new
   explicit-witness lemma `RSCap.hasList_first_grid`), and the new
   `RSCap.cor_first_grid_cap_one` (the `c = 1` clause of `cor:first-grid-cap`,
   both `ε_ca` and `ε_mca`).  Together these put the paper's unconditional
   deployed-row **first-grid cap chain at `c = 1` end-to-end in Lean**
   (`cor:augmented-slack-one` witness → `thm:quotient-remainder-deep-floor` →
   `cor:quotient-remainder-trigger` → `cor:first-grid-cap` `c = 1` →
   `fact:chain` for `ε_mca`), which is exactly the clause the paper's
   deployed-row corollary consumes (tex `:1153`: "By
   Corollary~`cor:first-grid-cap` with `c = 1`, it is enough to check
   `C(n, k+1) ≥ q/k + 1`").
3. Two untied-binder statement repairs with **PLAUSIBLE** grade and no falsity
   claim (findings 6–7): `RSCap.cor_ecfft_macroscopic` (band bound `Δ ≤ 2⁻⁹` +
   `hfB`/`hgB` subfield ties) and the two `AperiodicHankel` certificates
   (`u`/`v` tied to newly defined RS syndromes).  Their proofs stay sorried
   where they were.
4. Documentation: new
   `experimental/lean/cs25_cap_v12/SKELETON_REPAIR_CORRESPONDENCE.md`
   (statement map, falsity findings, scope boundaries, verification); this
   audit note; agents-log entry.

No `.tex` file was touched.  No files outside
`experimental/lean/cs25_cap_v12/`, this note, and the agents-log were touched.
Import graph change: `ECFFT.lean` and `InterleavingTransfer.lean` now import
`cs25_cap_v12.QuotientRemainder` (for the proved deep floor and the shared
constants pigeonhole); no cycles, root module unchanged.

## Findings

Every falsity finding is a **formalization defect, not a paper defect**: in
each case the quoted paper line carries exactly the constraint the skeleton
dropped.  Defect classes: quantifier inversion (1, 2), missing band/radius
constraint (3), dropped smoothness hypothesis (4), dropped size constraint (5),
untied binders (6, 7).

### F1 — `lem_quotient_remainder_prefix`: certificate weight universally quantified (FALSE, machine-checked)

The skeleton's implicit binder list `{c N K m s A₀ wₒ : ℕ}` left the
certificate weight `wₒ` to the *caller*, and `wₒ` appears only in the
denominator `|B|^{wₒ}` of the list bound.  At `wₒ = 0` the statement demands a
received word carrying the **full** quotient-remainder count `M_{c,m,s}` of
distinct codewords with no pigeonhole loss.

Counterexample (proved: `RSCap.lem_quotient_remainder_prefix_false`):
`F = ZMod 17`, `ι = Fin 16`, `dom = (3^0, 3^1, …, 3^15)` the unit group in
primitive-root order (injective by `decide`; squaring is 2-to-1, so
`DomSmooth dom (·²) 2` holds — proved by `decide` after
`Finset.filter_congr_decidable`), `B = ⊤`,
`(c, N, K, m, s, A₀, wₒ) = (2, 8, 1, 4, 0, 8, 0)`.  Then
`qrCount = C(8,4)·C(8,0) = 70`, so the demanded list has `L ≥ 70` distinct
codewords of `RS[F, D, 1]` — but degree-`< 1` codewords are constants and
`|F| = 17 < 70` (`RSCap.hasList_const_le_card`).

Repair (paper anchor `lem:quotient-remainder-prefix`, tex `:735`, denominator
display `:752`): the weight is the *fixed* prefix weight `w_c(s, A₀−K)`, now
formalized as `RSCap.certWeight c s σ = #{h : 1 ≤ h ≤ σ, h mod c ≤ s}`
(tex `:725`–`:733`; sanity: `w_c(0,σ) = ⌊σ/c⌋`, so here `w_2(0,7) = 3` and the
true floor is `⌈70/17³⌉ = 1` — consistent with the 17 constants).

### F2 — `lem_heaviest_prefix_locator_floor`: heaviest-prefix count inverted (FALSE, machine-checked)

The skeleton bound `H` universally, constrained only from **below**
(`hHbound : M/|B|^{wₒ} ≤ H`), then demanded a list of size `H` — the
constraint is inverted: any huge `H` above the coarse bound was asserted to be
a list size.  Counterexample (proved:
`RSCap.lem_heaviest_prefix_locator_floor_false`): the F1 instance with
`H = 70`, `wₒ = 0` (`hHbound : 70/1 ≤ 70` holds); 70 distinct constants do not
exist in `ZMod 17`.

Repair (paper anchors tex `:806`–`:838`, `:842`–`:860`): the paper's `H` is
the construction's **output** — the heaviest prefix fiber `H_{c,m,s}^K`, which
dominates `⌈M/I⌉` for the prefix-image size `I ≤ |B|^{w_c}`.  The repaired
statement existentially quantifies the certified pair `(I, H)` with
`0 < I ≤ |B|^{certWeight c s (A₀−K)}` and `M/I ≤ H`, keeping the
sharper-than-ambient-box content (image certificates) visible without
formalizing the prefix map `Φ` itself.  (`0 < I` is required: without it
`I = 0` makes the real-division bound vacuous and the statement trivially
true.)

### F3 — `prop_graded_rational_floor`: vacuous radius hypothesis (FALSE, machine-checked; repaired AND discharged)

The skeleton's only radius constraint was `hδ : 1 − k/n ≤ 1` — a tautology —
while the list hypothesis sat at the conclusion radius `δ` itself, so `δ = 1`
was admissible.  At `δ = 1` every pair is `intClose` (the two-row relative
distance never exceeds 1 on a nonempty index type), so no slope is CA-bad and
`ε_ca(C, 1, 1) = 0`, while `ecaFloor > 0` whenever `q > n`.

Counterexample (proved: `RSCap.prop_graded_rational_floor_false`):
`F = ZMod 2`, `ι = Fin 1`, `dom ≡ 0`, `B = ⊤`, `f = X`, `g = 1`,
`(a, e, N, k, H, δ) = (1, 0, 1, 1, 1, 1)`: the zero word carries the trivial
one-element list at radius 1; `𝓔_{2,1}(1) = 1·(2−1)/(2·(2−1+1·1)) = 1/4 > 0 =
ε_ca`.

Repair (paper anchor `prop:graded-rational-floor`, tex `:5209`: floor at the
deep radius `1 − am/n` with `am ≥ K`, band-assembled strictly below capacity):
anchor the list at a deep agreement `A > k` and constrain
`δ ∈ [1 − A/n, 1 − k/n)`.  The repaired statement is then a direct wrapper
over the already-proved `thm_quotient_remainder_deep_floor` — **proved**, so
this finding is simultaneously a discharge (ECFFT census 4 → 3).  The
rational-smoothness binders are retained for paper-setting faithfulness
(deliberate unused-variable warnings, documented in the docstring, following
the `lem_phi_fiber_ii`/`hdomB` precedent).

### F4 — `thm_explicit_head_floor_even`: smoothness dropped (FALSE, machine-checked)

The paper opens `thm:explicit-head-floor` with "Let `D` be `(φ, c)`-smooth
over `B`" (tex `:5334`); complete `φ`-fibers of size `c` are what make the
locator `Λ_M` collect `cm` agreement points.  The skeleton carried **no
smoothness hypothesis at all** — `hcN : c·N = n` only fixes a count.

Counterexample (proved: `RSCap.thm_explicit_head_floor_even_false`):
`F = ZMod 17`, `φ = X²`, `c = 2`, `N = 4`, `ι = Fin 8`,
`dom = (1, 4, 6, 7, 2, 8, 5, 3)`.  The squares are
`(1, 16, 2, 15, 4, 13, 8, 9)` — pairwise distinct, so every `φ`-fiber inside
`D` is a **singleton** (not 2-smooth), yet `Q = φ(D)` is antipodally symmetric
(`−1 = 16`, `−2 = 15`, `−4 = 13`, `−8 = 9`) and `0 ∉ Q`, so every stated
hypothesis holds with `m = 2`, `K = 1` (`hmK : 4 ≤ 0 + 4` in ℕ).  The word
`u = φ²|_D = (1,1,4,4,16,16,13,13)` takes each of its four values exactly
twice, so every constant codeword of `RS[F, D, 1]` disagrees with `u` on at
least 6 of the 8 points (checked by `decide` over all 17 constants):
`relDist ≥ 3/4 > 1/2 = 1 − cm/n`.  Even a list of size 1 is unreachable; the
skeleton claimed `C(2,1) = 2`.

Repair: `hsmooth : DomSmooth dom (fun x => φ.eval x) c` — the same
`(φ, c)`-smoothness form consumed by the proved `lem_phi_fiber_ii` /
`cor_circle_grand`.  `thm_explicit_head_floor_odd` carries the identical
omission; the even countermodel does not apply (odd needs `m = 3`, hence
`N ≥ 6` — a larger instance), so the odd clause gets the same repair as a
same-class flag, graded **PLAUSIBLE**, with **no falsity claim**.

### F5 — `thm_explicit_pairs`: family size unconstrained (FALSE, machine-checked)

The paper fixes `L₀ := ⌈(q−n)/k⌉` (tex `:5370`) and its Markov +
Cauchy–Schwarz count needs a family that large; the skeleton left `L₀` a free
binder while the conclusion still demanded `⌈(q−n)/(3K)⌉` distinct values at
half the poles.

Counterexample (proved: `RSCap.thm_explicit_pairs_false`): `F = ZMod 7`,
`ι = Fin 2`, `dom = (0, 1)`, `K = 1`, `A = 2`, `L₀ = 1`, `u = P₀ = X` (full
agreement on both domain points, so `hagree` holds).  For every pole
`α ∈ Ω = F ∖ {0,1}` the value set `{P₀(α)}` has size `1 < ⌈5/3⌉ = 2`, so the
good-pole set is empty, while `|Ω| = 5 > 0 = 0·2`.

Repair: `hL₀ : ⌈(q − n)/K⌉ ≤ (L₀ : ℤ)`.  The paper's exact choice satisfies
it with equality, and the counting bound `L₀/(1 + 2K(L₀−1)/(q−n))` stays above
`(q−n)/(3K)` as `L₀` grows past `(q−n)/K` (for `2K < q−n` the function is
increasing; for `2K ≥ q−n` the target ceiling is at most 1 and any nonempty
family reaches it) — so the abstracted lower-bound form is the faithful
monotone generalization of the paper's fixed choice.

### F6 — `cor_ecfft_macroscopic`: unbounded band width + missing subfield ties (PLAUSIBLE repair, no falsity claim)

Two defects repaired, no negation lemma:

* `Δ` had only `0 < Δ`, so the band `[1 − ρ − Δ, 1 − ρ)` admitted `δ < 0`,
  where no support satisfies `(1−δ)n ≤ |S|`, `mcaBad` never holds, and
  `emcaErr = 0` — strictly below the threshold whenever `q > n`, `k ≥ 1`.
  This is a genuine falsity *of the statement shape*, but a machine-checked
  negation additionally needs a satisfiable `(ψ, 2)`-smooth ECFFT-shaped
  instance of the binomial hypothesis `hyp` — constructible (e.g. a `GF(p²)`
  twin-coset-style domain with `C(N, ℓ)` large) but disproportionate for this
  packet; per the honesty discipline the finding is graded **PLAUSIBLE** and
  no falsity claim is made.  Repair: `hΔhi : Δ ≤ 1/512`, the paper's
  certified band width `2⁻⁹` (`cor:ecfft-macroscopic`(i), tex `:5251`).
* `hfB`/`hgB` (`f, g ∈ B[X]` coefficient ties), present in
  `prop_rational_floor` and `cor_ecfft_onestep`, were missing here — the
  exact untied-binder class of the pre-repair `lem_phi_fiber_ii` (`hQB`).
  Restored.

Residual, explicitly documented in the docstring and correspondence note: the
skeleton's `hyp` is the *one-step* binomial count, while the paper's
macroscopic proof derives a graded count at `m = ⌈(k+1+2⁻⁹n)/2⌉` from envelope
hypotheses (`ρ ∈ [1/16, 1/2]`, `n ≥ 2^14`, `q < 2^256`, `log₂|B| ≤ 64`; tex
`:5241`–`:5245`) that the skeleton never carried.  The repaired statement is
**not claimed provable as stated**; a discharger will likely need to swap
`hyp` for the graded form or add the envelope.

### F7 — `AperiodicHankel` eliminant/packing: syndromes untied (PLAUSIBLE repair, no falsity claim)

`lem_regular_exact_agreement_eliminant` and
`thm_regular_closed_ball_hankel_packing` took `u, v : ℕ → F` as free binders
never related to the line `(f, g)`; their docstrings promised `u = Syn(f)`,
`v = Syn(g)` but no `Syn` existed anywhere in the package.  As stated, a
regular Hankel certificate for *unrelated* sequences was asserted to bound the
bad slopes of `(f, g)`.  A refutation needs a Hankel-singular line with more
bad slopes than the unrelated certificate's degree budget — scriptable, but
disproportionate here — so this is graded **PLAUSIBLE** with no falsity claim.

Repair: define the paper's parity-check data (tex `:1550`–`:1560`):
`RSCap.synTwist dom i = (∏_{j ≠ i}(x_i − x_j))⁻¹` and
`RSCap.rsSyndrome dom Y m = ∑_i λ_i x_i^m Y(x_i)` (total in `m`; the Hankel
windows only read `m ≤ n − k − 1 < r`), and substitute
`u := rsSyndrome dom f`, `v := rsSyndrome dom g` in both statements
(syndrome convention also at tex `:2065`–`:2075`, `:2184`–`:2188`).  These
feed the already-proved scanner ledger
`thm_scanner_checkable_residual_aperiodic_ledger`, which consumes the chart
predicates abstractly and needed no repair.

## Discharges (the first-grid chain)

* `RSCap.hasList_first_grid` (new, PROVED): on any injective `n`-point domain,
  the explicit monomial word `x^{k+1}|_D` carries `C(n, k+1)` distinct
  codewords of `RS[F, D, k+1]` at radius `1 − (k+1)/n` — the `c = 1` clause of
  `cor:augmented-slack-one` (tex `:1063`–`:1078`, "One may take
  `U_c(x) = x^{k+c}`"; the `c = 1` statement "holds for any set `D ⊆ B` of `n`
  distinct points").  Proof: for each `(k+1)`-subset `S`, the monic locator
  `Λ_S = ∏_{s∈S}(X − s)` gives the codeword `c_S = u − Λ_S|_D` of degree
  `≤ k` (`Polynomial.degree_sub_lt` on two monic degree-`(k+1)` polynomials)
  agreeing with `u` on `S`; injectivity because `Λ_S − Λ_{S'}` has degree
  `≤ k < n` yet vanishes on all of `D` (root-count via
  `Polynomial.card_roots'`), and equal locators have equal root multisets
  (`Polynomial.roots_prod_X_sub_C` over `S.image dom`); the family is
  enumerated by `Finset.powersetCard` with `Finset.card_powersetCard`.
* `RSCap.cor_quantitative_first_grid_floor` (statement unchanged, PROVED):
  feed `hasList_first_grid` to the proved deep floor at `A = k+1`,
  `L = C(n, k+1)` (QuotientRemainder census 4 → 3).
* `RSCap.cor_first_grid_cap_one` (new, PROVED): `C(n,k+1) ≥ q/k + 1 >
  (q−n)/k` triggers `cor_quotient_remainder_trigger` at
  `δ = 1 − (k+1)/n`, giving the `ε_ca` clause; the `ε_mca` clause follows
  from the proved `eca_le_emca` (`fact:chain`).  This is exactly the paper's
  `cor:first-grid-cap` at `c = 1` ("no smoothness is needed", tex `:1093`) —
  the clause consumed by the deployed-row corollary `cor:first-grid-grand`
  (tex `:1153`).
* `RSCap.prop_graded_rational_floor` (repaired, PROVED): see F3.

## Census (by `declaration uses 'sorry'` build warnings)

* Before (base `3404d21`, baseline build exit 0): package-wide **14** —
  Fiber 1 (`lem_fiber_ii`), QuotientRemainder 4, InterleavingTransfer 3,
  AperiodicHankel 2, ECFFT 4.
* After (clean rebuild, exit 0): package-wide **12** — Fiber 1 (unchanged),
  QuotientRemainder 3 (`lem_quotient_remainder_prefix`,
  `lem_heaviest_prefix_locator_floor`, `cor_first_grid_cap` — all repaired or
  audited, none newly claimed), InterleavingTransfer 3 (all three repaired),
  AperiodicHankel 2 (both repaired), ECFFT 3 (`prop_rational_floor`,
  `cor_ecfft_onestep` audited-no-defect; `cor_ecfft_macroscopic` repaired).
* Discharged: `cor_quantitative_first_grid_floor`,
  `prop_graded_rational_floor`.  Newly proved sorry-free:
  `hasList_first_grid`, `cor_first_grid_cap_one`, the five negation lemmas,
  `RSpoly_one_const`, `hasList_const_le_card`.

## Gates

* Toolchain-first: baseline `lake build` at base `3404d21` **exit 0** before
  any edit (8043 jobs; after one transient disk-space failure of
  `lake exe cache get`, retried successfully).
* Clean rebuild after edits: package build artifacts (`.lake/build`) removed,
  all 16 package modules recompiled from source: **exit 0** (8043 jobs),
  census 12 as above.
* `#print axioms` on all 14 new/repaired proved declarations: exactly
  `[propext, Classical.choice, Quot.sound]` — no `sorryAx`, no
  `native_decide`, no added axioms.  All finite checks are kernel `decide`;
  the `DomSmooth` counterexample instances route through
  `Finset.filter_congr_decidable` because `DomSmooth`'s definition (over an
  abstract field) bakes in a classical `Decidable` instance that the kernel
  cannot evaluate.
* Source-only: no `.lake` artifacts, no `lake-manifest.json` churn, no
  toolchain churn, no `.tex` edits.
* Tex citations verified against the base blob
  `origin/main:tex/cs25_cap_v12.tex`.

## Self-Red-Team

* **Do the negation lemmas refute the actual skeletons, or strawmen?**  Each
  negation quotes the pre-repair statement with the same hypothesis list, in
  the same order, with implicit binders made explicit and the two type
  parameters instantiated at universe 0 — the same convention as
  `lem_circle_rs_false` / `lem_stereographic_false` (universe-0 instantiation
  refutes the universe-polymorphic ∀-closure).  The pre-repair statements are
  recoverable verbatim from the base blob
  `origin/main:experimental/lean/cs25_cap_v12/cs25_cap_v12/{QuotientRemainder,ECFFT,InterleavingTransfer}.lean`.
* **Could the F1/F2 counterexamples be artifacts of a wrong `DomSmooth`?**
  No — `DomSmooth` demands *every* fiber have exactly `c` elements, and for
  the unit group of `ZMod 17` under squaring this is the true 2-to-1 count,
  checked by kernel `decide` over all 16 × 16 pairs.  The instance is a
  genuine multiplicative-coset domain (the full unit group), i.e. squarely
  inside the paper's setting; only the skeleton's free `wₒ`/`H` made the
  statements false.
* **Is the F4 domain artificial?**  It selects one square root per antipodal
  class — a *section* of the 2-to-1 map, which is precisely what the paper's
  smoothness hypothesis exists to exclude.  The instance satisfies every
  remaining hypothesis (checked by `decide` after reducing polynomial
  evaluation), so it isolates the dropped hypothesis exactly.
* **Does `cor_first_grid_cap_one` really cover the paper's `c = 1` clause?**
  At `c = 1`: `N = n`, `k/c + 1 = k + 1`, radius `1 − (k+1)/n`, `hyp` is
  `q/k + 1 ≤ C(n, k+1)` with no `|B|` division — the Lean statement matches
  the paper's clause including the "no smoothness" remark (no `B`, no
  `DomSmooth` binder).  The general `cor_first_grid_cap`'s `c = 1` instance
  follows from it (its extra binders `B`, `hsmooth`, `hcnk` are unused at
  `c = 1`), but the general statement is left sorried rather than partially
  proved — a `sorry` in one branch would make the whole declaration sorried
  anyway and hide the discharged content.
* **Is the repaired heaviest-prefix statement weaker than the paper?**  It is
  the paper's statement with `H_{c,m,s}^K` and `I_{c,m,s}^K` abstracted to an
  existential certified pair `(I, H)` satisfying the paper's own inequalities
  (`def:prefix-fiber-certificate`).  It does not pin `H` to the concrete
  maximum fiber of a concrete prefix map (formalizing `Φ` is real content,
  left to the discharger); it is strictly stronger than the repaired prefix
  lemma (image certificates beat the ambient box) and no longer refutable by
  the quantifier inversion.
* **Could the `Δ ≤ 1/512` repair be too generous or too strict?**  It matches
  the paper's certified band width exactly (`:5251`).  Too-strict is
  impossible (the paper proves nothing wider); too-generous is possible only
  if the residual `hyp`-form mismatch (documented) also bites — which is why
  the grade is PLAUSIBLE, not TRUE.
* **Instance hygiene:** several proofs must bridge the classical `Decidable`
  instances baked into def-site filters (`DomSmooth`, `numDiff`, the skeleton
  statements' `Finset.filter`/`Finset.image` over an abstract field) against
  computable instances needed by `decide`.  This is done by
  `Finset.filter_congr_decidable`, membership-level `simp only
  [Finset.mem_filter]`, unification-anchored `refine`/`absurd`, and in one
  place an explicit `@`-application with the statement's own `propDecidable`
  instance — never by `native_decide` and never by adding axioms.

## NON-CLAIMS

* **No claim that any repaired-but-sorried statement is provable as stated.**
  In particular `cor_ecfft_macroscopic` post-repair likely still needs a
  `hyp`-form swap (documented residual), and the two `AperiodicHankel`
  certificates need genuine syndrome-recurrence content.
* **No falsity claim** for `thm_explicit_head_floor_odd`,
  `cor_ecfft_macroscopic`, or the two `AperiodicHankel` statements (PLAUSIBLE
  flags only; no counterexamples constructed).
* **`cor_first_grid_cap` for `c > 1` is NOT proved** and is out of scope; the
  multiplicative-coset quotient floor behind `cor:augmented-slack-one` at
  `c > 1` is not formalized.
* **No numeric deployed-row claim**: `cor:first-grid-grand`'s four rate rows
  (`k ≥ 127/78/58/47`) and every deployed-row instantiation remain
  unformalized; nothing here moves the pay-per-bit ledger.
* **No paper-defect claim anywhere**: all five falsity findings are
  formalization omissions/inversions relative to the quoted paper lines.
* The quotient-remainder *construction* (locator-prefix pigeonhole, prefix
  map `Φ`, heaviest-fiber certificates) remains unformalized; only its
  consuming conversion layer is proved.

## Use Rule

Treat the five `*_false` lemmas as **permanent statement-level regression
guards**: any future discharge attempt on these files must target the
*repaired* statements; re-introducing the pre-repair forms (free `wₒ`/`H`/`L₀`,
missing `hsmooth`, vacuous `hδ`, untied `u`/`v`) is machine-refuted by this
packet.  Cite `cor_quantitative_first_grid_floor` / `cor_first_grid_cap_one`
as PROVED only for the `c = 1` first-grid clause on an abstract injective
domain with the stated binomial hypothesis — never as a deployed-row or
`c > 1` result.  The PLAUSIBLE-graded repairs may be tightened further by a
discharger; they must not be cited as verified-true statements.
