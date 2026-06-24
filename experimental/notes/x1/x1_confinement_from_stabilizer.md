# X1: confinement from stabilizer — the forward direction, proved

- **Status:** PROVED (structure theorem + confinement corollary) / verified
  (`verify_x1_confine_from_stabilizer.py`). The FULL biconditional for arbitrary
  `U` remains open; this is the clean **forward** direction, with the precise
  hypothesis isolated.
- **Agent/model:** Claude Opus 4.8 (L2/X1 lane, branch `allen/l2-x1-interleaved-mca`).
- **Date:** 2026-06-24.
- **Scope:** the `confine ⟺ stabilizer` correspondence flagged as the open
  bridge in [`x1_prefix_locator_slope_principle.md`](x1_prefix_locator_slope_principle.md);
  generalizes Paper D `lem:confine`/`cor:Fvalued`. Does not edit Papers A–D.

## Theorem (equivariant word + quotient-periodic support ⟹ folded slope)

Let `H_n = ⟨ω⟩ ≤ F^*` be cyclic of order `n`, `B ≤ F`, `d | n` with `d > 1`, and
`ζ = ω^{n/d}` a primitive `d`-th root of unity. Say `U` is **ζ-equivariant with
eigen-character `ζ^m`** if `U(ζx) = ζ^m U(x)` for all `x ∈ H_n`, and a support
`S` is **`K_d`-stable** (quotient-periodic) if `ζS = S`.

> **Theorem.** If `U` is ζ-equivariant (eigen-character `ζ^m`) and `S` is
> `K_d`-stable, and `P_S` (degree `< k ≤ |S|`) agrees with `U` on `S`, then
> ```
> P_S(X) = X^r · G(X^d),   r = m mod d,
> ```
> for some `G ∈ F[Y]`. Hence the deep slope at any pole `α` is
> ```
> z_S = P_S(α) = α^r · G(α^d).
> ```

**Proof.** For `x ∈ S`, also `ζx ∈ S` (as `ζS = S`), so
`P_S(ζx) = U(ζx) = ζ^m U(x) = ζ^m P_S(x)`. The polynomials `P_S(ζX)` and
`ζ^m P_S(X)` both have degree `< k` and agree on the `|S| ≥ k` points of `S`,
hence are equal as polynomials. Writing `P_S = Σ c_i X^i`, equality gives
`ζ^i c_i = ζ^m c_i`, i.e. `(ζ^i − ζ^m) c_i = 0`; since `ζ` has order `d`,
`c_i = 0` unless `i ≡ m (mod d)`. Thus only exponents `≡ r := m mod d` survive,
`P_S(X) = X^r G(X^d)`. ∎

## Corollary (confinement)

If moreover the codeword is `B`-rational — `G ∈ B[Y]` (e.g. `lem:fiber`'s listed
codewords lie in `RS[B,D,·]`) — and `α^d ∈ B`, then
```
z_S = α^r G(α^d) ∈ α^r · B,
```
and if also `α^r ∈ B` (in particular `r = 0`, or `α ∈ B`) then `z_S ∈ B`: the
slope is **confined to the base field**. Conversely, if `α^d ∉ B` the value
`G(α^d)` can be genuinely `F`-valued — the `cor:Fvalued` regime.

This **is** `lem:confine`/`cor:Fvalued`, recovered as the special case
`d = a_q`, `m = k` (with `a_q | k`, so `r = 0` and `G = ` the heavy word's
quotient polynomial): there the slopes are `G(α^{a_q})`, confined iff
`α^{a_q} ∈ B`. The theorem generalizes it to every divisor `d | n` and every
eigen-character.

## What is and isn't proved (honest)

- **Proved:** the *forward* implication — ζ-equivariance of `U` **and**
  `K_d`-stability of `S` together force the folded form, hence confinement under
  `B`-rationality + `α^d ∈ B`.
- **The hypothesis is sharp.** Equivariance of `U` is *necessary*, not just
  periodicity of `S`: the verifier's **negative control** interpolates
  *non-equivariant* data on the *same* `K_d`-stable support and gets an
  **unfolded** polynomial (all residues mod `d` present). So "quotient-periodic
  support ⟹ confined slope" is false without the equivariance of the word.
- **Open:** the full biconditional for *arbitrary* `U`. The converse
  ("primitive support ⟹ non-confined slope") is also not a theorem — a primitive
  `S` can still yield a confined slope for special `α`. What is clean is: *on the
  equivariant words*, periodicity ⟹ confinement.

## Isotypic refinement — confinement is *per-character*, not per-support

How far does this reach? Decompose any `t : S → F` on a `K_d`-stable `S` into its
`d` ζ-isotypic components by the finite-Fourier projection
```
t_m(x) = (1/d) Σ_{j=0}^{d-1} ζ^{-jm} t(ζ^j x),     t = Σ_m t_m,
```
well-defined because `S` is `K_d`-stable and `p ∤ d` (so `1/d ∈ F`). Each `t_m`
is ζ-equivariant with eigen-character `ζ^m`, so by the theorem its interpolant is
folded, `X^{r_m} G_m(X^d)`, `r_m = m mod d`. Hence for **any** received word `U`
and any `K_d`-stable `S ∈ Fib_U(a)`,
```
P_S(X) = Σ_{m=0}^{d-1} X^{r_m} G_m(X^d),     z_S = Σ_{m=0}^{d-1} α^{r_m} G_m(α^d)
```
— a sum of `d` confined pieces. This is proved (it is the theorem applied to each
component) and verified in `verify_x1_isotypic_decomposition.py`.

**Consequence (the honest scope).** Confinement is a statement *per isotypic
character*, not per support:
- `U` **single-isotypic** (equivariant) ⟹ `z_S` is **one** folded term ⟹
  **confined** (verified: single-isotypic `m=0`, B-rational, `α^d∈B` ⟹ `z_S∈B`
  for **all** amplitudes).
- `U` **general** ⟹ `z_S` is a sum of `d` confined pieces, which **need not be
  confined** (verified: a genuinely 2-isotypic word gives `z_S ∉ B`).

So the combinatorial `QuotientBudget`/`Q_1` split (by support stabilizer) does
**not** exactly equal the slope confined/non-confined split. They coincide on the
**equivariant stratum** — which is exactly where the cap mass (`lem:fiber`, folded
quotient words) lives — but a non-equivariant word can have a quotient-periodic
support with a non-confined slope. This **guards the unifying picture against
overclaiming**: "confined ⟺ quotient-periodic" is true per-character / on the
equivariant words, not as a blanket support-by-support equivalence.

**The non-equivariant periodic mass is a product of per-character masses.** By
*linearity* of the map `U|_S ↦ P_S(α)` and the isotypic split, a periodic-support
slope is `z_S = Σ_m z_S(U_m)`, a sum of `d` per-character **confined** slopes.
Hence the distinct non-confined periodic slopes satisfy
```
|{ z_S }|  ≤  Π_{m=0}^{d-1} |Slopes_m|  ≤  C^d,     C = max per-character confined count.
```
So the non-equivariant periodic supports are **not a new obstruction**: their mass
is the `d`-fold product of the *same* per-character confined counts the L1
conjecture already concerns — **polynomial for bounded `d`**. (Verified in
`verify_x1_nonequivariant_product_bound.py`: `d=4`, two active characters give
`|Slopes_0|=|Slopes_1|=17` and exactly `289 = 17²` distinct sums — the bound is
tight, and with enough active characters the non-confined slopes fill `F`.) The
**growing-`d`** regime (the deep cap's `a_q`) is left open: there `C^d` need not be
polynomial, so a separate argument is needed for large-period supports.

## Why this matters for L1

The QuotientBudget stratum (`x1_prefix_locator_slope_principle.md`) is populated
by the equivariant words — `lem:fiber`'s heavy words, the folded quotient words
of the L1 falsification scanner (#106) — and on exactly those words this theorem
says the bad slopes are **confined** (lie in a proper subfield / `B`). Therefore:

> genuinely non-confined, full-`F`-density MCA-bad slopes can come only from the
> **primitive `Q_1` stratum**.

So, **restricted to the equivariant (single-isotypic) stratum**, the L1
conjecture `Q_1 ≤ n^B` (above the reserve) is precisely "the non-confined
MCA-bad-slope mass is polynomially small." The confined part is now a theorem
(modulo equivariance), not a conjecture. The honest caveat (above): the exact
"confined ⟺ quotient-periodic" alignment is per-character, so the clean reduction
is rigorous on the equivariant words that carry the cap mass; pinning the general
non-equivariant periodic supports (showing their mass is poly, or that they too
confine) is the remaining gap. Either way this is concrete progress on isolating
the positive core: the structured/confined half is proved on the stratum that
matters.

## Verification

`verify_x1_confine_from_stabilizer.py` (exact `F_{17^2}`, `d = 4`):
```
m=0 (r=0): equivariant data on K_4-stable S => interpolant folded at i==0 mod 4; z=alpha^r G(alpha^d); confined when alpha^d in B.
m=2 (r=2): same, folded at i==2 mod 4 (tests r != 0).
negative control: non-equivariant data on the same S => UNfolded (residues {0,1,2,3}); equivariance is necessary.
```
`verify_x1_isotypic_decomposition.py` (exact `F_{17^2}`, `d = 4`): the isotypic
decomposition `data = Σ_m t_m`, each component equivariant + folded,
`P_S = Σ_m X^{r_m} G_m(X^d)`, `z_S = Σ_m α^{r_m} G_m(α^d)`; single-isotypic
`m=0` confined for all amplitudes; a 2-isotypic word escapes `B` (the
QuotientBudget is not entirely confined per-support). All PASS.

## Ledger impact

- **`lem:confine`/`cor:Fvalued` (generalized + proved):** from heavy-word period
  `a_q` to arbitrary `d | n`; the precise hypothesis (word ζ-equivariance) is
  isolated and shown necessary.
- **L1 (sharpened):** on the equivariant stratum the QuotientBudget bad slopes
  are confined (theorem); `Q_1 ≤ n^B` ⟺ non-confined MCA-bad-slope density is
  poly. The forward half of the confine ⟺ stabilizer correspondence is closed,
  and shown to be *per-character* (isotypic refinement), not a blanket
  support-by-support equivalence.
```bash
python3 experimental/scripts/verify_x1_confine_from_stabilizer.py
python3 experimental/scripts/verify_x1_isotypic_decomposition.py
```
