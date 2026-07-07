# Lean package for `experimental/grande_finale.tex`

This folder contains a Mathlib-based Lean formalization track for selected
self-contained parts of `experimental/grande_finale.tex`, the current
proof-audited final-input note for RS-MCA.

The Lean package is normalized as:

```text
package: RequestProject
library: RequestProject
toolchain: leanprover/lean4:v4.28.0
dependency: mathlib v4.28.0
```

The main modules are:

- `RequestProject.GrandeFinale`
- `RequestProject.BC`
- `RequestProject.SP`

Build command, in an environment where Mathlib dependencies are already
available:

```sh
cd experimental/lean/grande_finale
lake build
```

Codex did not run Lake during this source audit.

## Formalized Scope

The package formalizes theorem-level kernels from the note:

- integer budget conventions and first-match ledger counting;
- support-wise CA/MCA predicates, bad-slope numerators, monotonicity, and
  `eca <= emca`;
- Cauchy-Schwarz distinct-value counting and prefix-pigeonhole kernels;
- finite moment inequalities for the Q route;
- selected exact arithmetic anchors for the deployed MCA rows;
- BC-side slope elimination, saturation, line-ray bookkeeping, moving-root
  incidence bounds, and one-parameter pencil floor checks;
- SP-side quotient-pullback arithmetic, coefficient-scale detection,
  prefix-collision rigidity, second-moment ledger splitting, and the formal
  implication that a max-fiber Q theorem discharges the SP ledger;
- composite-prefix power-map descent (`prop:composite-descend`): the
  generating-function factorization and its `gcd(e,N)` power-map multiplicity,
  in product form and `[Tᵐ]` coefficient reading.

## Not Formalized

This is not a complete proof of `grande_finale.tex`.

The dense-frontier safe side remains open. In particular, the package does not
prove the row-sharp Q atom theorem, does not prove the finite BC
chart-decomposition audit, and does not prove the adjacent deployed safe rows.
The large binomial derivations behind the packet numerators are also not
re-derived in Lean; the current arithmetic anchors check the integer comparisons
recorded by the packets.

The package does not yet formalize every theorem-level local lemma in the TeX
note; full coverage of the Q audit section remains partial (the row-sharp
max-fiber Q atom theorem is the main remaining target).

## Correspondence

| TeX label | Lean declaration(s) | mapping_confidence | audit_status |
| --- | --- | --- | --- |
| `prop:composite-descend` | `GrandeFinale.composite_descend` (product form), `GrandeFinale.composite_descend_coeff` (`[Tᵐ]` reading); assembled from `prod_pow_of_fiber_card`, `composite_descend_prod`, `card_fiber_pow`, `coeff_prod_one_add_X_mul_C` | `exact_label_match` | `statement-audited-against-TeX` |

Scope note for `prop:composite-descend`.  The multiplicative coset `S` of order
`N` in `𝔽ₚˣ` is modeled as a finite cyclic group `G` (the identity coset `1·H`,
`N = |G|`); a general coset `α·H` is its translate under the bijection
`a ↦ α·a`, which preserves every power-map fiber cardinality, so the multiplicity
`c = gcd(e,N)` and the identity are unchanged.  The purely combinatorial core
(`prod_pow_of_fiber_card` / `composite_descend_prod`) holds for an arbitrary
exactly-`c`-to-one map into any commutative ring and needs no character
property.  The manuscript's analytic reading (`ψ : 𝔽ₚ → ℂˣ` a nontrivial
additive character, `g(x) = h(xᵉ)`) is the instance `R := ℂ`, `v := ψ∘h`, giving
`v(aᵉ) = ψ(g a)` and image `Gᵉ = Sₑ`; the character property is used only to read
the coefficient's multiplicative product `∏_{a∈A} ψ(g a)` as `ψ(∑_{a∈A} g a)`.

## Audit Status

Status: `FORMALIZATION / AUDIT`.

During this repository pass, the source was inspected for obvious trust
placeholders. The scanned `.lean` files contain no `sorry`, `admit`, added
`axiom`, or `@[implemented_by]`. Several numeric anchors use `native_decide`,
which should be reviewed as executable arithmetic certificates before any claim
is advertised as Lean-certified.

The `CompositeDescend` section (`prop:composite-descend`) was built with
`lake build` (green) against cached Mathlib v4.28.0; it adds no `native_decide`,
no `sorry`/`admit`/`axiom`, and each of its six declarations `#print axioms`-
reduces to only `[propext, Classical.choice, Quot.sound]`.

Before relying on this package, run `lake build` in a controlled Mathlib-enabled
environment and inspect `#print axioms` for the declarations being cited.
