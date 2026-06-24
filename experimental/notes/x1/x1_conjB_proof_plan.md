# X1: corrected proof plan for conj:B (MCA), and where my machinery actually fits

- **Status:** PLAN / ORIENTATION (no new theorem). Corrects an earlier skeleton
  after reading the precise Paper B statements; identifies the exact, bounded
  contribution this session's machinery makes to `conj:B`.
- **Agent/model:** Claude Opus 4.8 (L2/X1 lane, branch `allen/l2-x1-interleaved-mca`).
- **Date:** 2026-06-24.
- **Sources:** Paper B `slackMCA_v3.tex` `thm:normalform` (1197), `def:residue`
  (1189), `rem:strata` (1209), `prob:perfiber` (1227), `conj:B` (1231),
  `rem:aper` (1255). Does not edit Papers A–D.

## What conj:B actually is (precise)

- **`thm:normalform` (PROVED):** `emca(C,δ) = (1/q)·max_{1≤t≤r} Λ^NC_{t,δ}(D,k)`,
  where `Λ^NC_{t,δ}` is the **residue-line packing number** for degree-`t`
  denominators `E` (`def:residue`). So MCA *is* residue-line packing, exactly.
- **`rem:strata`:** the canonical/dominant stratum is **`t=r`**, the monomial
  slack line `x^{k+T}+zx^k` = datum `(E,B,w)=(X^r,−1,x^T)`; its noncontained slope
  set is exactly `B_T(D,k)` (`thm:exactslack`). "Every positive theorem of the
  paper is a statement about this stratum and its quotient refinements."
- **`conj:B`:** `max_t Λ^aper_{t,1−ρ−η} ≤ n^{1+o(1)}`, where `Λ^aper` separates the
  **quotient-periodic** residue lines (`rem:aper`: denominator a pullback through
  `x↦x^M`, `M | gcd(n,k)`, `M>1`); the periodic part is charged to the explicit
  quotient term, and the tangent floor (`rem:strata`, `prop:floor`) saturates the
  `n^{1+o(1)}` correction (so the conjectured constant is sharp).

## Correction to my earlier skeleton (honest)

My first skeleton said "step 1: deep-point bridge ⇒ `Λ` = deep image of fiber."
That is the **`t=1` simple-pole stratum** (`E=X−α`). But `conj:B`'s dominant
object is the **`t=r` monomial stratum**, whose positive half Paper B already
reduces — via `prob:perfiber` — to the **prefix-map fiber-collision bound**:

> `prob:perfiber`: every fiber of `Φ_σ(A)=(e_1(A),…,e_σ(A))` on `s`-subsets has
> `≤ n^{O(1)}` ordered pairs prefix-equal mod `p` but not in `ℤ[ζ]`; "this single
> divisibility statement implies the monomial-line positive half."

`prob:perfiber` is an **L1-family** statement (prefix/locator fiber) — Codex's
lane (#106 `Q_1 ≤ n^B`). So **the core of `conj:B` is `prob:perfiber`/L1, not my
deep-point bridge.** The deep-point bridge remains valid for the `t=1` stratum
(an independent cross-check / one term of `max_t`), but it is not the main path.

## Where this session's machinery genuinely fits

`conj:B`'s proof factors as:
```
conj:B  ⟸  [ monomial-stratum aperiodic bound: B_T^aper ≤ n^{O(1)} ]   (= prob:perfiber / L1, Codex)
            +
           [ QUOTIENT-PERIODIC SEPARATION: periodic residue lines confine,
             contributing exactly the quotient term, so Λ^aper is the
             genuinely-aperiodic object L1 bounds ]                     (= MY contribution)
```

The separation is exactly `rem:aper`, and my session's results are its tools:
- **confinement theorem** (`x1_confinement_from_stabilizer.md`): a ζ-equivariant
  word on a `K_M`-stable support gives a folded ⇒ **confined** slope;
- **quotient reduction** (`x1_quotient_reduction.md`): `Q_M(H_n)=Q_1(H_{n/M})`,
  the multi-scale recursion that places the periodic mass on the quotient;
- **isotypic refinement** (`x1_isotypic_decomposition.md`): the separation is
  *per-character*, the subtlety to handle.

## The exact correspondence to prove (the load-bearing step) — CORRECTED

**Correction (verify-first, 2026-06-24).** I first guessed the separation was
*slope-confinement*: "`E ∈ F[X^M]` ⟹ bad slopes confined to a proper subfield."
`verify_x1_conjB_residue_confinement.py` **FALSIFIED** this: a periodic-denominator
datum (`E = X²−γ`, generic extension `w,B`) gives 39 bad slopes, only 1 in `B`
(mostly genuinely `F`-valued). So `rem:aper`'s separation is **not** confinement.

**The corrected mechanism — quotient descent of the count.** A quotient-periodic
line `E = E₀(X^M)` (`E ∈ F[X^M]`) is a *pullback through `x ↦ x^M`*; it descends
to a residue line on the **quotient domain `H_{n/M}`** (with `Y = X^M`). So its
bad-slope **count** equals the residue-line packing on `H_{n/M}` — a *smaller
same-rate instance* (this is exactly my quotient reduction `Q_M(H_n)=Q_1(H_{n/M})`,
now on the residue-line/packing side). That count **is** the quotient term
(`thm:qnecessity`'s lower bound / Codex's `Quot_align_μ`). The non-periodic-
denominator lines are `Λ^aper`, bounded by `prob:perfiber`/L1.

So the step-2 lemma to prove is **the quotient descent**, not confinement:
```
   E ∈ F[X^M]  ⟹  the line descends through x↦x^M to a residue line on H_{n/M},
                  bad-slope-count-preserving  ⟹  contributes exactly the quotient term;
   E not periodic for any M>1  ⟹  the line is in Λ^aper (L1-bounded).
```
My confinement theorem is a *related but distinct* phenomenon (base-vs-`F` slopes
under fully `K_M`-equivariant data), useful as a sub-tool but not the separation
itself. NEXT: build the quotient-descent (count-preserving) verifier; re-read
`rem:aper` (1255) and `thm:qnecessity` (1323) precisely for the exact descent
statement before proving it.

## Honest scope

- **Not mine:** the monomial-stratum core (`prob:perfiber`/L1) — Codex.
- **Mine:** the quotient-periodic separation making `Λ^aper` the clean
  L1-bounded object; i.e. the rigorous form of `rem:aper`.
- So `conj:B` ⟸ (Codex's `prob:perfiber`/L1) + (my separation). I prove the
  second half; the first is L1.

## Next increments
1. Build a verifier for the residue-line correspondence
   `E ∈ F[X^M] ⟺ K_M-support ⟺ confined slope` on a small field (the exact step-2
   biconditional), per-character.
2. Prove the separation lemma; write up honestly (assumes `prob:perfiber`/L1).
3. Handle the tangent-floor/`o(1)` correction (`rem:strata`).
