# M1 (BETA_2) Obstruction Floor: Conditional Close + Proven Localization to a Global Big-Monodromy Input

**Status:** AUDIT / PROOF-PROGRAM / CITABLE-CONDITIONAL. (Not a theorem; no leaderboard row; does not assert `(BETA_2)` or prove M1.)

**Agent/model:** holmbuar / Claude.

**Date:** 2026-07-01.

This note **supersedes** `m1_beta2_obstruction_floor.md` on the general-`psi`
reduction and on the dihedral-exclusion framing. It advances the M1 `(BETA_2)`
obstruction floor from *"one research-grade ℓ-adic residual gap, apparently
blocked because the sheaf is dihedral"* to:

1. a **CITABLE-CONDITIONAL close** for the operative general `psi`, resting on
   exactly **two named monodromy inputs**, with every other ingredient now
   **PROVEN-EXACT**; and
2. a **proof** that those two inputs cannot be closed by local / finite-field
   computation — closure provably requires a **global big-monodromy theorem**.

Three computational overclaims were caught and corrected by adversarial passes
during the work; they are recorded below in the interest of honesty.

## Object (unchanged from the prior note)

`F` is the pure weight-1 middle-extension constituent of
`F_psi = R¹π_!(ψ(a)·χ(rM(a,r)))` on the `z`-line (`z = b + 1/b`), `M = -3a²r +
4ar² - 2ar + 4a - 3r`. The floor `(BETA_2)`: *for every nonprincipal `psi`, `F`
has no rank-1 tame Kummer subquotient `L_{φ⁻¹}`.* Singular support is the
degree-13 dihedral locus `(z-2)(z+1)(9z+14)(9z²-6z-23)·Q8(z)` (full geometry in
`m1_kummer_weil_import_contract.md`).

## The conditional close (operative general `psi`, ord `psi > 2`)

> `F` is rank 8, carries a genuine unipotent transvection (at `z = -14/9`), and
> is **not self-dual** for general `psi`. Therefore **IF** (I) `F` is
> geometrically irreducible **AND** (II) `F` is primitive (not Kummer-induced
> from the `b→z` dihedral cover), **THEN** by Gabber's pseudoreflection
> criterion (Katz, *ESDE*, Annals 124, **Lemma 1.5**) together with the
> one-transvection trichotomy (Kantor; Arias-de-Reyna–Dieulefait–Wiese,
> **arXiv:1203.6552**; `ℓ ≥ 5` excludes the McLaughlin finite exceptions), the
> geometric monodromy group contains `SL₈` and acts **irreducibly** on the
> rank-8 stalk. Hence `F` has no one-dimensional sub or quotient of any kind, in
> particular no rank-1 tame Kummer subquotient — i.e. `(BETA_2)` holds, i.e. the
> M1 MCA-half bound follows (mod FFKS *Quantitative sheaf theory* Prop. 5.7).

| ingredient | status | source |
|---|---|---|
| rank `F` = 8 (stalk `H¹_c` = 11 = 8 ⊕ 3 Tate) | **PROVEN-EXACT** | dossier §rank; cert |
| genuine unipotent transvection at `9z+14`, **in the weight-1 constituent** | **PROVEN-EXACT** | §A below |
| `F` not self-dual for general `psi` ⇒ `SL` (not `Sp`/`SO`) branch | **PROVEN-EXACT** | dossier §pairing |
| `ℓ ≥ 5` ⇒ no McLaughlin finite exception | given (ℓ-adic) | — |
| consuming theorem (Gabber/ESDE 1.5 + Kantor/ADW) is non-circular | **verified** | §foreclosed |
| **(I) geometric irreducibility** | **CORROBORATED-ONLY** | §residual |
| **(II) primitivity** | **CORROBORATED-ONLY** | §residual |

The close is conditional on **(I)+(II)**, and on nothing else.

## Net-new PROVEN-EXACT results

- **§A — the `9z+14` transvection lives in the rank-8 constituent.** A unique
  ordinary `A1` node (Hessian ≠ 0 ⇒ Milnor number 1 ⇒ rank drop exactly 1);
  coefficient `L` lisse at the node (`a ≠ 0`, `rM ≠ 0`) ⇒ the vanishing cycle is
  a Picard–Lefschetz ODP class, **pure weight 1** (Deligne, Weil II); the
  weight-0 Tate part (3 dims at the `M = 0` tangencies) is undisturbed (node not
  on `M = 0`). So the unit of drop lands in `gr₁^W = F`, giving a genuine rank-8
  transvection. Verified `p`-independently on 14 fibers.
- **§B — `Q8` is benign for every `psi`** (the last open local datum, removed
  unconditionally). All 8 `Q8` roots are **interior** (`z ≠ 0,∞`, except the
  already-excised bad primes `{2,3,13,8377}`); a rank-1 Kummer sheaf is lisse at
  interior points, so the subquotient question is decided **only** at `z = 0,∞`.
  Hence `Q8` cannot host or force a Kummer subquotient regardless of its
  vanishing-cycle dimension `d ∈ {1,2}` (which stays finite-`p`-inseparable but
  is **provably irrelevant**). Exact identity `disc_b = a·r·M·H` confirmed over `ℤ[a,r]`.
- **§C — pairing split.** `F^∨ = F_{ψ⁻¹}(-1)` (`p`-independent). For general
  `psi` (`ψ² ≠ 1`, the operative case) `F` is **not self-dual** (dual partner is
  the distinct sheaf `F_{ψ⁻¹}`) ⇒ target `GL₈/SL₈`. Only `psi = Legendre`
  (`ψ² = 1`) is self-dual symplectic `Sp₈`. Orthogonal excluded throughout.
- **§D — the dihedral branch fibers `z = ±2`.** `z = -2` (`b = -1`): `C_{b=-1}`
  is **smooth, genus 2**, the `L`-divisor transverse ⇒ `G = π*F` lisse upstairs
  ⇒ the deck monodromy `γ` at `z = -2` is tame with `γ² = 1`. `z = 2` (`b = 1`):
  the degenerate **ordinary triple point**, `χ`-ramified (`M(1,1) = 0`) — the
  fiber that supports the order-2 character. Descent involution
  `σ(a,r) = (1/a, 1/r)`, quotient genus 1.

## The two residual inputs — and the proof they need a *global* theorem

**(I) Geometric irreducibility — CORROBORATED-ONLY, provably not closable by local data.**
The 2nd moment `M₂(p) = mean_b|τ(b)|²/p → 1` (single geometric constituent;
Deligne equidistribution) over primes ≤ 181. But this is a `p → ∞` /
Zariski-closed limit no finite computation can promote, and the exact
no-common-invariant-subspace route is **provably insufficient**: with the
mandatory `Q8` support the local-class tuple is vastly **non-rigid** (Katz
moduli dimension ≥ 74), and there is an **explicit reducible block-diagonal
witness** that reproduces every pinned local type while preserving a 4-dim
invariant subspace. So local conjugacy classes do not determine the global rep;
(I) requires a global big-monodromy input.

**(II) Primitivity — CORROBORATED-ONLY, reduced exactly to one integer, elementary route proven dead.**
`F` is induced from the `b→z` dihedral cover iff `F ≅ F ⊗ L_{χ}` with
`χ = L_{Leg(z²-4)}` (ramified only at `z = ±2`). All **non-dihedral** candidate
self-twist characters are **killed** (transvection-twist lemma: `loc ⊗ χ` has all
eigenvalues `−1` at a unipotent transvection, so cannot be a self-twist).
Compatibility at `z = -2` reduces primitivity **exactly and `p`-independently** to
a single integer:

> `(II)` holds  ⟺  `Tr(γ|V) = m₊ − m₋ ≠ 0` at `z = -2`
> (the deck involution's eigenvalue split on the rank-8 stalk; imprimitive iff the `(4,4)` split).

This integer is **provably out of reach of the elementary Lefschetz route**: the
deck involution `σ(a,r) = (1/a,1/r)` **permutes the `psi`-variable `a`**, so
`σ*L ≇ L` for ord `psi > 2` — there is no `L`-equivariant involution, hence no
finite fixed-point trace. The `det mod 4` parity cross-check is itself blocked by
the unpinned conic + `Q8` + `z=∞` local determinants.

**Net localization.** `(BETA_2)` (operative `psi`) is reduced to a single global
statement — *`G_geom(F) ⊇ SL₈`* — about the explicit rank-8 sheaf `F`, for which
(a) the consuming theorem is fully citable once big-ness holds, and (b) big-ness
**provably cannot be certified** by the finite-field / local-monodromy methods
available here. This is the precise object to hand to a `ℓ`-adic monodromy expert.

## Foreclosed routes (recorded, not to be re-walked)

- **Katz, *Convolution and Equidistribution*** (Tannakian Mellin `GL/SL`):
  **circular** — its admissibility hypothesis (no negligible Kummer sub/quotient
  of the perverse object) is logically equivalent to (I) + `(BETA_2)` itself.
- **Hall, *Big symplectic or orthogonal monodromy mod ℓ*** (`Sp₈`): applies only
  to the single self-dual `psi = Legendre`, where primitivity **fails** —
  `F_Legendre` is `b→b²` Kummer-induced (self-twist `T → +1`, two enumerations),
  so Hall does **not** fire. (Legendre `(BETA_2)` descends instead to a rank-4
  cover-sheaf question.)
- **Rigid local systems / hypergeometric / `MC_χ(2F1)`**: 13 finite singular
  `z`-points vs `≤ 3` for rigidity. Dead.

## Honest corrections (overclaims caught by the adversarial passes)

1. `LOC0INF` "`χ`-ramified simple" `M=0` points → **`χ`-unramified tangencies**
   (caught internally; this is what makes `8 + 3 = 11` close).
2. "primitivity **PROVEN-EXACT** for all `psi`" → **CORROBORATED** (the prior
   drop-table silently omitted the branch punctures `z = ±2`; `psi = Legendre`
   is the explicit counter-witness — it is genuinely imprimitive).
3. Method-2 "`(4,4)` IMPRIMITIVE" → only the `psi = quadratic` specialization
   (it had dropped the additive `ψ(a)` and summed the Legendre character — the
   wrong sheaf).

Also: two hand-coded-derivative bugs (a dropped `−4a³` term) were caught and
re-verified via auto-derivatives; and the census re-classifies `z = -1` from
"excised" to a likely **second** genuine transvection (a refinement; the close
chain needs only the rock-solid `9z+14`).

## Reproducibility

Pure-stdlib, offline, exact-`F_p` verifiers; each header labels its claims
`PROVEN-EXACT` / `CORROBORATED` / `CITABLE-CONDITIONAL`:

- `verify_m1_beta2_local_data_dossier.py` — the PROVEN baseline (rank ledger
  `11 = 8 ⊕ 3`, `disc_b = arMH`, the dihedral locus + `Q8` irreducibility, node
  structure, square-class identities, the `p=73` resolution). **6/6 PASS**.
- `verify_m1_beta2_conditional_close.py` — §A (transvection in the constituent),
  §B (`Q8` interior-benignness), §D (`z = ±2` branch fibers, `σ` closed form), and
  the (II) reduction to `Tr(γ|V)` with the elementary-route obstructions made
  explicit (so the limitation is self-documenting).

Provenance: a four-phase localization → close → upgrade program (pin local data;
hunt the citable theorem; complete the branch-locus argument; attempt the deck
trace), each phase adversarially verified. `m1_beta2_obstruction_floor.md` is
superseded on the general-`psi` reduction and the dihedral-exclusion framing.

## Ledger impact

Reduces the open M1 MCA-half to a **single global monodromy fact** about an
explicit rank-8 sheaf, supplies the fully-citable theorem that consumes it, and
**proves** that fact is beyond finite-field reach — so the residual is correctly
addressed to a human `ℓ`-adic monodromy expert, not to more computation. No
positive theorem promoted; no leaderboard row.
