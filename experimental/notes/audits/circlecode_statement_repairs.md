# CircleCode Statement Repairs (falsity witnesses + repaired uniformizations)

- **Status:** COUNTEREXAMPLE (two machine-checked negations of pre-repair
  skeleton statements) + PROVED (both repaired uniformization lemmas) +
  AUDIT (one PLAUSIBLE-graded statement-hygiene repair, proof still `sorry`).
- **Source:** `experimental/lean/cs25_cap_v12/cs25_cap_v12/CircleCode.lean`
  (pre-repair skeletons at repo base `02728b208ea785d02115ea967236aebf653b31ec`:
  `lem_circle_rs` `:823`–`:829`, `cor_circle_grand` `:839`–`:850`,
  `lem_stereographic` `:859`–`:864`); paper anchors in
  `tex/cs25_cap_v12.tex` (line numbers at the same base commit).
- **Companion note:**
  `experimental/lean/cs25_cap_v12/CIRCLE_FIBER_CORRESPONDENCE.md`
  (statement map and packet history).

This packet repairs the statements of the two circle-code uniformization
skeletons in `CircleCode.lean`, which were **false as stated**, and proves the
repaired statements in full.  It also adds a statement-hygiene repair to
`cor_circle_grand`.  Both falsity findings are **formalization omissions, not
paper defects**: in each case the paper carries the missing hypothesis
explicitly, and the skeleton dropped it.

## Finding 1: `lem_circle_rs` was false as stated (missing `(2 : F) ≠ 0`)

The pre-repair statement (base `:823`–`:828`) asserted, for any finite field
`F` with `i_unit² = −1`, circle points `pt`, `torus j = x_j + i·y_j` nonzero:

```text
circleCode pt w = (fun c i => (torus i)^(−w) * c i) '' RSpoly torus (2w+1)
```

with **no characteristic constraint** (the file's variable block imposes none).
The paper carries `p ≡ 3 (mod 4)` globally for this section
(`tex/cs25_cap_v12.tex` `:3888`, and `lem:circle-rs` itself `:3976`).

**Counterexample** (now the proved Lean lemma `RSCap.lem_circle_rs_false`):
`F = ZMod 2`, `ι = Fin 2`, `pt = ![(0,1), (1,0)]`, `i_unit = 1` (in `ZMod 2`
indeed `1² = 1 = −1`), `torus ≡ 1`, `w = 1`.  All hypotheses hold
(`hcircle`: `0+1 = 1`, `1+0 = 1`; `htorus`: `0 + 1·1 = 1`, `1 + 1·0 = 1`;
`htne`: `1 ≠ 0`).  The left side contains the non-constant word `![0, 1]`
via `f₀ = X`, `f₁ = 0` (`deg X = 1 ≤ 1`, `deg 0 = ⊥ < 1`), but `torus ≡ 1`
makes `RSpoly torus 3` the constant words and the twist `1^{−1} = 1` the
identity, so the right side is the constant words.  Set equality fails.

**Repair:** add `h2 : (2 : F) ≠ 0` (binder placed after `w`).  `htne` is
derivable from `hcircle`/`htorus`/`hi` via `u·(x − i·y) = x² + y² = 1`, but is
retained to keep the interface unchanged.

**Proof of the repaired statement (FULL, no `sorry`):**

- Forward (`⊆`): clearing denominators.  With `u = x + iy`, `u⁻¹ = x − iy`,
  `x = χ(u) = (u + u⁻¹)/2`, `y = (u − u⁻¹)/(2i)`, the explicit polynomial

  ```text
  Q := Σ_{k≤w}  a_k 2^{−k} X^{w−k} (X²+1)^k
     + Σ_{k<w}  b_k 2^{−k} (2i)^{−1} (X²−1) X^{w−1−k} (X²+1)^k
  ```

  (`a_k`, `b_k` the coefficients of `f₀`, `f₁`) has degree `≤ 2w` and satisfies
  `Q(u_j) = u_j^w · c(j)` pointwise.
- Reverse (`⊇`): Laurent symmetrization of `u^{−w}Q(u)`.  The center split
  `Σ_{m<2w+1} q_m u^{m−w} = q_w + Σ_{d<w} (q_{w+d} u^d + q_{w−d} u^{−d})`
  (helper `RSCap.sum_range_center`) decomposes into a symmetric part handled by
  the already-proved `RSCap.chebyshev_semiconjugacy` (`T_d(χ(u)) = χ(u^d)`,
  this file) and an antisymmetric part handled by the **one new helper**

  ```text
  RSCap.chebyshev_antisymm :  u^a − u^{−a} = (u − u⁻¹) · U_{a−1}(χ(u))
  ```

  proved by the file's `Nat.twoStepInduction` pattern against Mathlib's
  `Polynomial.Chebyshev.U` (ℤ-indexed; `a = 0` lands on `U_{−1} = 0`).  The
  witnesses are `f₀ = C q_w + Σ_d C(q_{w+d+1} + q_{w−d−1})·T_{d+1}` (degree
  `≤ w` by `Polynomial.Chebyshev.degree_T`) and
  `f₁ = Σ_d C((q_{w+d+1} − q_{w−d−1})·i)·U_d` (degree `< w` by
  `degree_U_natCast`).

## Finding 2: `lem_stereographic` was false as stated (`sdom`/`twist` untied)

The pre-repair statement (base `:859`–`:864`) quantified over **arbitrary**
`sdom, twist : ι → F` with only `twist i ≠ 0` — neither was tied to `pt`
(`hchar`/`hcircle` constrain only `F`/`pt`; binder audit in the verification
run).  The paper's statement fixes both: the domain is the stereographic image
`T = s(E)`, `s(x,y) = y/(1+x)`, and the twist is
`d := ((1 + s(P)²)^{−w})_{P∈E}` (`tex/cs25_cap_v12.tex` `lem:stereographic`
`:5276`–`:5296`).

**Counterexample** (now the proved Lean lemma `RSCap.lem_stereographic_false`):
`F = ZMod 5`, `ι = Fin 2`, `pt = const (1,0)`, `w = 0`, `sdom ≡ 0`,
`twist = ![1, 2]`.  The left side (`w = 0`) is exactly the constant words; the
right side is `{i ↦ twist i · Q(0)}`.  Membership of the constant word `1`
would force `κ = 1` and `2κ = 1` simultaneously in `ZMod 5` (`κ = Q(0)`), i.e.
`κ = 1` and `κ = 3` — contradiction.  Set equality fails.  (The file registers
a `private instance : Fact (Nat.Prime 5)` so `ZMod 5` is a field; Mathlib only
registers `2` and `3` globally.)

**Repair:** tie `sdom` to the stereographic coordinate via the inverse
parametrization with pole exclusion, and fix the twist to the explicit
denominator power:

```text
hden : ∀ j, 1 + sdom j² ≠ 0
hxs  : ∀ j, x_j = (1 − sdom j²)/(1 + sdom j²)
hys  : ∀ j, y_j = 2·sdom j/(1 + sdom j²)
conclusion: circleCode pt w = (fun c i => (1 + sdom i²)^(−w) * c i) '' RSpoly sdom (2w+1)
```

`hcircle` becomes derivable from `hxs`/`hys`/`hden` (paper `:5290`:
`1 + s² = 2/(1+x)`), so it is dropped.

**Proof of the repaired statement (FULL, no `sorry`):** both directions follow
the paper's proof (`:5289`–`:5303`).  Forward: the monomial `x^k` contributes
`(1−s²)^k(1+s²)^{w−k}` and `y·x^k` contributes `2s(1−s²)^k(1+s²)^{w−1−k}`,
giving an explicit `Q` of degree `≤ 2w`.  Reverse: parity split of the
coefficients of `Q` (helper `RSCap.sum_range_parity`) through the invertible
substitution — `f₀ = 2^{−w} Σ_k q_{2k}(1−X)^k(1+X)^{w−k}`,
`f₁ = 2^{−w} Σ_k q_{2k+1}(1−X)^k(1+X)^{w−1−k}`, using `1−x = 2s²/(1+s²)` and
`1+x = 2/(1+s²)`.  No Chebyshev machinery is needed.

## Finding 3: `cor_circle_grand` hygiene repair (`htorusB`) — graded PLAUSIBLE

The skeleton takes `B : Subfield F` and uses `Fintype.card B` in the field-size
hypothesis `hyp`, but had **no hypothesis tying `torus` to `B`**.  Its model
`thm_phi_cap` (Fiber.lean `:91`–`:104`) requires a `B`-valued domain
(`hdomB : ∀ i, dom i ∈ B`), and the paper instantiates a `B`-valued domain.
Model-mismatch argument: shrinking `B` weakens `hyp` (smaller `card B` makes
the inequality easier) while the fiber pigeonhole that `hyp` feeds needs
`B`-valued slopes — so the untied statement is likely unprovable as stated.

**Grade: PLAUSIBLE, not confirmed** — no concrete counterexample was
constructed, and **no falsity claim is made** for `cor_circle_grand`.  This is
a statement-hygiene repair only: `htorusB : ∀ i, torus i ∈ B` is added.  The
proof **remains `sorry`**: it is blocked on the sorried
`lem_phi_fiber_ii`/`thm_phi_cap` in Fiber.lean, and since `k = 2w+1` is odd,
`a ∤ k` in every 2-power instantiation (v12 parity note after the
`lem:circle-rs` proof, `:4010`), so the divisibility-free route is forced.
Fiber.lean is untouched by this packet.

## Sorry census

By `declaration uses 'sorry'` build warnings (clean rebuild from scratch,
`rm -rf .lake/build && lake build`, exit 0, pinned toolchain
`leanprover/lean4:v4.28.0` / mathlib `v4.28.0`):

- Before (base `02728b2`): package-wide **19**; `CircleCode.lean` **3**
  (warning lines `:823` `lem_circle_rs`, `:839` `cor_circle_grand`,
  `:859` `lem_stereographic`; `sorry` keyword lines `:829`/`:850`/`:864`).
- After: package-wide **17**; `CircleCode.lean` **1** (`cor_circle_grand`
  only).  Every other module's census is unchanged.

`#print axioms` on every new or repaired proved declaration
(`chebyshev_antisymm`, `sum_range_center`, `sum_range_parity`, `lem_circle_rs`,
`lem_circle_rs_false`, `lem_stereographic`, `lem_stereographic_false`):
`[propext, Classical.choice, Quot.sound]` — no `sorryAx`, no `native_decide`,
no added axioms.  `cor_circle_grand` reports `sorryAx`, as expected for the
one intentionally remaining skeleton.

## Self-Red-Team

- *Are the negation lemmas negating the real pre-repair statements?*  They
  negate the ∀-closure over `Type`-instantiated `ι F` of the exact pre-repair
  binder structure (same hypotheses, same conclusion, same order).  A
  universe-0 counterexample refutes the universe-polymorphic statement, since
  the latter specializes to universe 0.  The one intentional difference:
  the section variables `{ι F : Type*}` become explicit `∀ (κ K : Type)`
  binders inside the negation.
- *Could the counterexamples be artifacts of Lean's junk-value conventions?*
  No division or inverse is used at a zero denominator in either witness; the
  `ZMod 2` witness uses only ring operations, and the `ZMod 5` witness only
  the twist multiplication.  Both proofs go through `decide`-checked finite
  arithmetic plus explicit membership witnesses.
- *Does the `ZMod 2` counterexample secretly violate the circle geometry?*
  No: `(0,1)` and `(1,0)` are genuine `x² + y² = 1` points in every field, and
  `i_unit = 1` genuinely satisfies `i² = −1` in characteristic 2 (indeed it is
  forced: `(i+1)² = i² + 1 = 0`).  The degeneracy exploited is precisely the
  one the paper excludes by `p ≡ 3 (mod 4)`.
- *Is the repaired `lem_circle_rs` weaker than the paper's lemma?*  The Lean
  statement quantifies over abstract `F` with `i² = −1` and `(2 : F) ≠ 0` and
  an arbitrary nonvanishing torus assignment; the paper's `E' = ι(E) ⊆ 𝕌`
  instantiates it.  The list-size/`ε_ca`/`ε_mca` consequences
  (`lem:diag-invariance`) are not formalized here — only the set equality that
  feeds them, which is the load-bearing content.
- *Is the repaired `lem_stereographic` the paper's part (ii)?*  Yes, in the
  same abstract sense: parts (i) (injectivity of `s` on `E`, `|T| = 2M`,
  torsion-point exclusion) and (iii) (`(ψ,2)`-smoothness of `T`) are NOT
  formalized; the Lean lemma is exactly the code identity of part (ii), with
  the parametrization hypotheses playing the role of (i)'s inverse formula.
- *Could `htorusB` be the wrong repair for `cor_circle_grand`?*  It mirrors
  `thm_phi_cap`'s `hdomB` exactly (Fiber.lean `:92`), which is the intended
  model of the corollary; if `thm_phi_cap` is ever restated, `htorusB` should
  be revisited alongside it.  Since the corollary stays `sorry`, the repair
  costs nothing if it later proves redundant.
- *Private instance pollution?*  `private instance : Fact (Nat.Prime 5)` is
  file-local and cannot leak into downstream modules' instance caches beyond
  this module's interface; it exists only so `decide` sees closed terms.

## NON-CLAIMS

- **No M31 unblocking claim.**  The deployed circle rows
  `cor:circle-deployed(a)/(b)` remain **blocked**: their certifying route runs
  through `thm:phi-cap`/`cor:circle-grand`, which remains `sorry`.
- **Fiber.lean untouched** — its 3 sorried theorems (`lem_fiber_ii`,
  `lem_phi_fiber_ii`, `thm_phi_cap`) are unchanged.
- No claim about `lem:diag-invariance` (list-size/error transfer under diagonal
  twists) — not formalized.
- No claim that `cor_circle_grand` (pre- or post-repair) is false — the
  `htorusB` flag is PLAUSIBLE-graded statement hygiene, not a counterexample.
- No claim about the paper's prose: both falsity findings are formalization
  omissions; the paper's hypotheses (`p ≡ 3 (mod 4)`; the stereographic
  parametrization and twist) already exclude the counterexamples.
- No numeric/threshold claims; nothing here changes any ledger row.

## Use Rule

Cite `RSCap.lem_circle_rs` / `RSCap.lem_stereographic` **only as the repaired
statements** (with `h2` resp. `hden`/`hxs`/`hys`); the pre-repair statements
are refuted by `RSCap.lem_circle_rs_false` / `RSCap.lem_stereographic_false`
and must not be cited as available lemmas.  Any consumer of
`cor_circle_grand` must treat it as a sorried skeleton whose statement now
carries `htorusB`; do not build on it until the Fiber.lean route is proved.
Downstream text citing "CircleCode has 3 sorries" should be updated to 1.
