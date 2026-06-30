# M1 `(BETA_2)` Obstruction Floor + Literature Scaffolding

**Status:** AUDIT / CONDITIONAL. (Negative result: localizes the single remaining
M1 analytic obligation and supplies the published criterion that consumes it.
Does NOT prove M1.)

This note records the result of three 2026-06-30 multi-agent passes — a keystone
attack (verify the reduction + isolate the gap), a local-monodromy probe (can we
derive the gap?), and a literature deep-research pass (is the gap published?). The
net is that the **entire M1 keystone is reduced to one explicit Katz-style
monodromy fact**, with everything else now citable.

## Claim

The M1 aperiodic residue-line local limit (`M1AperiodicBound`,
`QuotientOverlap.lean`) reduces — by a reduction and geometry that were
independently re-derived theorem-grade — to the single statement
`(BETA_2)`/`(BETA_2^avg)`, equivalently the **obstruction floor**:

> For every nonprincipal multiplicative character `ψ` of `F_p^*`, the weight-1
> β-line pushforward sheaf `F_ψ = R¹π_!(ψ(a)·χ(rM(a,r)))` on `G_m` (generic fiber
> genus ≤4; singular support = the audited degree-13 dihedral locus
> `(z−2)(z+1)(9z+14)(9z²−6z−23)·Q8(z)=0`, `z=b+b⁻¹`) contains **no rank-one tame
> Kummer subquotient `L_{φ⁻¹}`** for any nonprincipal bounded-order `φ` —
> equivalently `H²_c(G_m, F_ψ⊗L_φ)=0` (no weight-3 coinvariant / no `p^{3/2}`
> isotypy spike), equivalently `|B_{ψ,φ}| = |Σ_b φ(b)τ_{ψ,p}(b)| = O_e(p)`.

## Status of each piece

**(A) The reduction `M1AperiodicBound → (BETA_2)`: VERIFIED.** Every inequality
(`M_e^o → P_e = p·wᵀΓ_e w → ||Γ_e^circ||_F`, the closed boundary inequality
`√(M_e^o) ≤ √(P_e^+) + 3(e−1)√p`, the rank-one Weil bounds `I_e ≤ 4(e−1)p(p−1)`,
`O_e ≤ 9(e−1)²p`, the Cauchy absorption `|T_e|² ≤ O_e·M_e^o`, the centering) was
independently re-derived; the only analytic input consumed is `(BETA_2)`. The
`Y_G` geometry (`D_β=arMH`, étale degree 2, the `(1,1)` blow-up + char-5
exception, the four tangencies, `χ(d_UV)=χ(rM)=χ(aH)`, det `ψ²φ(C_β/A_β)`, the
degree-26→13 singular support) was re-derived by exact ℤ-arithmetic. The two
arithmetic pillars are now machine-checked stdlib-Lean in
`RsMca/BetaTwoReductionLedger.lean` (`complete_square`, `wList_sum`), with
`(BETA_2)` recorded as the typed target `BetaTwoConductorBound`.

**(B) The implication "floor ⇒ `O(p)`, constant polynomial in the conductor": CITABLE.**
The criterion the M1 bound needs is published in four independent primary sources:
- **Forey–Fresán–Kowalski–Sawin, "Quantitative sheaf theory"** (Ann. Fac. Sci.
  Toulouse, `10.5802/afst.1671`; arXiv:2101.00635), **Prop. 5.7 (Small Diagonal
  Principle)**: the two-variable correlation `Σ_{x,y} t_{F1}(x) t_{F2}(y) t_K(x,y)
  ≪ q` (i.e. `O(p)`, the square-root saving, NOT `O(p^{3/2})`) holds UNLESS `F1`
  is geometrically isomorphic to a member of the finite exceptional set — the
  geometrically irreducible components of the transform `G = T_K^1(F2)(1/2)`. A
  `p^{3/2}` spike occurs **precisely** when a rank-1 Kummer `L_{φ⁻¹}` is a
  geometric component of the pushforward; otherwise `O(p)`, constant depending
  only on conductors. This is exactly our floor-consuming criterion.
- **FFKS "Quantitative sheaf theory" Thm. 5.11 (Conductor of Kummer transforms):**
  `c(T_K^i(F)) ≤ (2·c(K)·c(F))^A` for the Kummer pushforward
  `T_K^i(F)=R^i p_{1,!}(p_2^*F ⊗ L_χ(f))` — **exactly our object**. The
  conductor is `e`-INDEPENDENT (the singular support is `e`-independent), so the
  resulting constant `C_β` is **absolute / `e`-independent** — resolving the
  open `e`-dependence question — *modulo* the exponent `A`, which the paper
  leaves as "an absolute constant `A≥1`" with no numerical value (so the bound
  is polynomial-in-conductor but **ineffective**).
- Alternative statements of the implication: **Fouvry–Kowalski–Michel, "A study
  in sums of products"** (Phil. Trans. R. Soc. 2015; arXiv:1405.2293) **Prop. 1.1**
  (`H²_c(A¹, ⊗F_i⊗D(G))=0 ⇒ |Σ| ≤ C√p`, `C=C(k, conductors)`; `k=1`, `F_1=F_ψ`,
  `G=L_φ` recovers our hypothesis verbatim); **FKMS "Bilinear forms with trace
  functions"** (arXiv:2511.09459) **Thm. 2.2**; **Michel AWS 2016** Cor. 4.2. The
  `O(p)` vs `O(p^{3/2})` dichotomy is exactly the `tr(Fr | H²_c)` coinvariants term.

**(C) Rojas-León is NOT enough (the "just cite a singular-sum theorem" route is dead).**
**Rojas-León, "Estimates for singular multiplicative character sums"** (IMRN
2005, no. 20, 1221–1234), **Thm. 1(a):** `|S| ≤ C·q^{(n+δ+2)/2}`, `δ = dim` of
the singular locus, `C = 3(3+…)^{N+r+2}`. For a 2-variable sum (`n=2`) with
isolated tangencies (`δ=0`) this is `q^{3/2}` (or `q²` trivial) — **never `q`**;
the exponent is proved optimal and the square-root saving is provably lost at a
single singular point (Junyan Xu, arXiv:1709.01663; Asgarli–Yip two-quadrics
instance `q^{3/2}`, arXiv:2404.06754). Moreover his sum is purely multiplicative
`Σχ(f)`, while ours is **mixed** `Σψ(a)χ(…)`, so the theorem does not even apply.

**(D) The closest worked precedent — our exact problem shape, solved.** FFKS
("Quantitative sheaf theory", same paper) prove the **Conrey–Iwaniec sum**
`S(χ₁,χ₂) = Σ_{x,y} χ₁(xy(x+1)(y+1))·χ₂(xy−1) ≪ p` with absolute constant —
singular support = the four lines `x, y, x+1, y+1` plus the conic `xy−1`, i.e. a
**singular line+conic mixed-multiplicative-character two-variable sum, exactly our
shape, at `O(p)`**. Caveat bearing on our gap: the cohomological-transform route
gives `O(p)` only "for all but a bounded number of `χ₁`"; the all-`χ₁` statement
is Conrey–Iwaniec's own Lemma 13.1. The authors stress the `O(p)` vs `p^{3/2}`
stakes verbatim ("the application breaks if even a single `χ₂` gave size
`p^{3/2}`"). This is the **template** for closing our last step.

## The remaining gap (the obstruction floor) and why it is genuinely open

The floor in the Claim is exactly the hypothesis (B)'s theorems **presuppose**.
No published result establishes it for our specific genus-≤4, degree-13
dihedral-support arrangement, and it is hard for a precise reason:
- the FFKS quasi-orthogonality bound needs **irreducible** inputs and only
  *detects* (does not *exclude*) a shared rank-1 component;
- FKMS's big-monodromy ("gallant") theorem explicitly **excludes** the
  dihedral/solvable monodromy at issue — and ours **is** dihedral (the β-cover is
  the quadratic Kummer double cover `y²=D_β`), so the off-the-shelf big-monodromy
  theorem does not fire;
- the worked rank-2 templates (FFKS; Michel's Kloosterman-pullback) establish the
  no-rank-1 input **case-by-case via the explicit monodromy group**, not by a
  general theorem.

So `(BETA_2)` is **citable conditional on a by-hand, Katz-style no-Kummer-component
verification** for this dihedral sheaf — exactly the kind FFK carried out for
Conrey–Iwaniec.

## The gate: typing the 10 tame fibers — run, PARTIAL (probes `wmey9wnyb`, `wqrf9u807`)

A local-monodromy probe (`wmey9wnyb`) and a full-force gate computation
(`wqrf9u807`, pure-stdlib exact `F_p`, p up to 271 / 691) typed the singular
fibers. The gate is **partial / open-gap-localized**: it did not close `(BETA_2)`,
but it settled several pieces exactly and killed the rigidity shortcut.

**Established (exact).**
- `9z+14` is a single ordinary node `A1` = unipotent transvection (λ=+1, vc-dim 1),
  triple-confirmed; `z=2` (degenerate triple point) and `z=−1` (node) lie on the
  **deleted** locus and are excised.
- **The `p=73` "anomaly" is resolved as a benign coincidence:** `Res_z(9z+14,
  9z²−6z−23) = 657 = 3²·73`, so `z=−14/9 ≡` a conic root only at `p=73` — the
  observed node is the `9z+14` transvection passing through a conic root, not a
  conic degeneration. The node structure `{z=2, z=−1, z=−14/9}` is constant across
  primes; **conic and `Q8` fibers are never curve nodes.** (Certified exactly by
  `verify_m1_beta2_p73_resolution.py`.)
- **The literal `MC_χ(2F1)` / Katz-ESDE-8.4 route is geometrically DEAD:** `F_ψ`
  has **13** finite singular `z`-points (the reduced dihedral locus `1+1+1+2+8`),
  whereas any `MC_χ(2F1)` has ≤3 and middle convolution preserves singular support
  up to `{0,∞}`. So ESDE 8.4 cannot apply — **FFKS-direct (Prop 5.7) is the only
  route**, and the per-fiber tameness data is its input.

**Open (the residual gap, for general ψ).**
- `Q8` (8 fibers): tame, but the vanishing cycle sits **at infinity** (the
  multiplicity-2 points `[0:1],[1:0]` where `ψ(a)` ramifies); its character is
  **not pinned** for general `ψ` (the `F_{p²}` point-counts needed did not complete
  in pure stdlib).
- conic (2 fibers): an exact Newton-facet computation gives vanishing-cycle
  **dim 2** carrying a `ψ^{±2}` Kummer character — **nontrivial for `ord ψ > 2`** —
  so it violates the literal single-pseudoreflection gate except in the quadratic
  specialization `ψ = Legendre` (which every committed trace uses).

**Floor: strongly corroborated, but Zariski-closed (finite-`p` cannot establish it).**
The full 2-D Mellin spectrum over **all** `φ` (p ≤ 691) gives log-log slope
**0.9696 ≈ 1** for `max_φ|B_{ψ,φ}|` (a rank-1 Kummer component would force 1.5);
`|B|/p^{1.5}` decays monotonically to ~0; `|B|/p` stays bounded in `[2, 7.3]`; the
**dominating character's order wanders prime-to-prime** (positive evidence of no
fixed `p`-independent Kummer component); and the clean quadratic pair has `|B|/p`
dipping to `0.166 < 1`, which **positively excludes** a Kummer *quotient*. No
counterexample exists in the data — corroboration, not proof.

**Residual gap (research-grade).** Prove the pure weight-1 middle-extension
constituent of `F_ψ` (rank ~4–8, to be semisimplified out of the rank ~25 `H¹_c`)
is geometrically irreducible with big `Sp/SL` monodromy — hence has no rank-1
Kummer sub/quotient — **for every nonprincipal `ψ`**. This needs the stabilized
integer generic rank, the local monodromy characters at `z=0,∞`, and a general-`ψ`
(not just `Legendre`) trace machinery. With the rigidity shortcut dead, this is
genuine ℓ-adic monodromy work, not a finite computation.

## Ledger impact

Reduces the open M1 MCA half to a single, fully-isolated cohomological fact, and
supplies the literature scaffolding (B, D) that turns that fact into the prize-
relevant `O(p)` bound with an `e`-independent constant. No leaderboard row; no
positive theorem promoted.

## Reproducibility / provenance

- Verified reduction + geometry: workflow `w4poxl3ey`; verifiers
  `verify_m1_depth_two_line_conic_resonance_reduction.py`,
  `verify_m1_kummer_divisor_geometry.py`; contract
  `m1_kummer_weil_import_contract.md`; Lean `RsMca/BetaTwoReductionLedger.lean`
  (`lake build`, no `sorry`/`admit`/`native_decide`).
- Local-monodromy + gate computations: workflows `wmey9wnyb`, `wqrf9u807`
  (pure-stdlib exact `F_p`): per-fiber Jordan/mechanism tables, the full 2-D Mellin
  spectrum (trace bit-for-bit vs committed
  `verify_m1_beta_pushforward_spectral_audit.py`), and the `p=73` resolution. The
  exact `p=73` certificate is committed as `verify_m1_beta2_p73_resolution.py`; the
  heavier Mellin/per-fiber tables are reproducible via that audit plus the workflow
  scripts and are summarized above to keep this note self-contained.
- Literature: deep-research `wfc2jxh3l`; primary sources cited inline above.
