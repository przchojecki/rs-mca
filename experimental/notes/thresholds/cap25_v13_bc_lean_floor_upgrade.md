# CAP25 v13 raw: BC.lean interior census floor made non-vacuous (pigeonhole ceiling form)

Status: `FORMALIZATION` / `PROVED-IN-LEAN` (zero `sorry`/`admit`/`native_decide`).

**Package:** `experimental/lean/cap25_cap_v13_raw_compact/` (Lean `v4.28.0`,
mathlib `v4.28.0`). **File:** `cap25_cap_v13_raw_compact/BC.lean` -- additive: three
new theorems appended in `namespace RSMCA`; **no existing declaration modified**
(`143 -> 223` lines, `+80` insertions, `0` deletions).

## What this note is

The maintainer's `BC.lean` proves the unconditional **lower** obstruction to
`prob:saturated-bc` (formerly `prob:saturated-bc`; promoted grande_finale e749e9e) -- the base-field (`|𝔹|`-scale) floor on the binomial-moment census
`census D K m U = ∑_c binom(agr(U,c), m)`. Its interior floor `bc_census_floor`
reads (with `n = |D|`)

```text
∃ Ub, ⌊binom(n,m') / |𝔹|^{m'-K}⌋ · binom(m',m) ≤ census D K m (𝔹→𝔽 ∘ Ub)
```

and Lean `Nat` division is a genuine `⌊·⌋`. In the interior **below-one** regime
`binom(n,m') < |𝔹|^{m'-K}` -- which already holds at the first interior profile
`d₁ = w+2` (there `m'-K = d₁-1`) and is exactly where PR #369 pins the L4 fixture
(prefix average `< 1` from `d₁ = 4218`) -- that floor collapses to `0`, so
`bc_census_floor` degenerates to the vacuous `0 ≤ census`. The manuscript floor
`M_𝔹(d₁;m)` is the **ceiling** `⌈binom(n,m') / |𝔹|^{m'-K}⌉ · binom(m',m)`, and the
ceiling is `≥ 1` whenever `binom(n,m') ≥ 1` (i.e. `m' ≤ n`). This note supplies the
non-trivial below-one content the `⌊·⌋` form loses. It is the acknowledged seam the
maintainer's docstring flags ("here the honest integer floor `⌊·⌋`").

## The three new theorems (exact Lean statements)

```lean
theorem bc_census_floor_pigeonhole (D : Finset B) (K m m' : ℕ) (hKm' : K ≤ m')
    (hm'n : m' ≤ D.card) :
    ∃ Ub : D → B, m'.choose m ≤ census D K m (fun x => algebraMap B F (Ub x))

theorem bc_census_floor_ceil_below_one (D : Finset B) (K m m' : ℕ) (hKm' : K ≤ m')
    (hm'n : m' ≤ D.card)
    (hbelow : (D.card).choose m' ≤ (Fintype.card B) ^ (m' - K)) :
    ∃ Ub : D → B,
      (((D.card).choose m' + (Fintype.card B) ^ (m' - K) - 1) / (Fintype.card B) ^ (m' - K))
          * (m'.choose m)
        ≤ census D K m (fun x => algebraMap B F (Ub x))

theorem bc_boundary_census_floor_pos (D : Finset B) (K m : ℕ) (hKm : K ≤ m)
    (hmn : m ≤ D.card) :
    ∃ Ub : D → B, 1 ≤ census D K m (fun x => algebraMap B F (Ub x))
```

- **`bc_census_floor_pigeonhole`** is the candidate-[C] core: the non-vacuous
  interior floor `binom(m',m) ≤ census`. Proof is an elementary max-fiber `≥ 1`
  pigeonhole on the maintainer's own `Floor.lean` machinery: `m' ≤ n` makes
  `D.powersetCard m'` nonempty (`Finset.card_powersetCard`, `Nat.choose_pos`), so a
  single `m'`-subset `M ⊆ D` sits in the prefix fiber of its own locator prefix
  `pre K m' M`; `code_mem_RS` yields one degree-`< K` codeword, `code_agrees`
  makes it agree on all of `M` (`≥ m'` positions), and `Finset.single_le_sum` +
  `Nat.choose_le_choose` push `binom(m',m)` into the census. Since `binom(m',m) ≥ 1`
  for `m ≤ m'`, this is strictly stronger than `bc_census_floor` exactly on the
  below-one regime (and implied by it whenever the `⌊·⌋` is `≥ 1`).
- **`bc_census_floor_ceil_below_one`** makes the manuscript match syntactic: in the
  below-one regime the `Nat` ceil-division `(binom(n,m') + |𝔹|^{m'-K} - 1)/|𝔹|^{m'-K}`
  equals `1` (proved from `binom(n,m') ≥ 1` and `≤ |𝔹|^{m'-K}` via
  `Nat.add_div_right`, `Nat.div_eq_of_lt`), so the paper's floor
  `⌈·⌉·binom(m',m) = binom(m',m)` and is attained by a `𝔹`-valued received word.
- **`bc_boundary_census_floor_pos`** is the `m'=m` corollary: `binom(m,m)=1 ≤ census`,
  the non-vacuous form of `bc_boundary_census_floor` (its `⌊·⌋` reads `0` below one),
  i.e. the decoding list at level `m` is nonempty.

## Build evidence

```text
toolchain: leanprover/lean4:v4.28.0                     (lean-toolchain, pinned)
mathlib:   v4.28.0 (manifest rev 8f9d9cff6bd728b17a24e163c9402775d9e6a365)

$ lake build cap25_cap_v13_raw_compact.BC
  ...
  ✔ [8027/8027] Built cap25_cap_v13_raw_compact.BC (25s)
  Build completed successfully (8027 jobs).

$ grep -nE 'sorry|admit|native_decide' BC.lean
  (no hits)
```

The pre-existing `native_decide` uses elsewhere in the package
(`Certificates.lean`, `Main.lean`) are the maintainer's numeric-instance
certificates and are untouched; the three new declarations use none of
`sorry`/`admit`/`native_decide`.

## Non-claims

This note does **not**:

```text
prove or make progress on conj:BC (the open UPPER bound on primitive split-pencil cells);
provide any upper bound on census, or on primitive split-pencil cell counts;
prove the full ceiling floor ⌈binom(n,m')/|𝔹|^{m'-K}⌉·binom(m',m) in the HIGH-DENSITY
   regime binom(n,m') > |𝔹|^{m'-K}  (see Gap below);
touch conj:Q or conj:SP;  move the frontier edge.
```

It is purely the **lower** side of BC, made non-vacuous in the interior below-one
regime.

## Gap vs the full manuscript ceiling

The full ceiling `⌈binom(n,m')/|𝔹|^{m'-K}⌉·binom(m',m) ≤ census` in the
high-density regime (`binom(n,m') > |𝔹|^{m'-K}`) is **not** delivered. There
`bc_census_floor` already gives `⌊·⌋·binom(m',m)`; the ceiling needs one extra
`binom(m',m)`, i.e. a max-fiber `≥ ⌈avg⌉` pigeonhole, whereas the mathlib pigeonhole
in `Floor.lean` (`Finset.exists_le_card_fiber_of_mul_le_card_of_maps_to`, hypothesis
`buckets · n ≤ items`) yields only `⌊avg⌋`. The `⌊·⌋` and `≥ 1` floors are for
different `𝔹`-witnesses, so the two `∃`-floors do not combine into `⌈·⌉` in general.
Exactly the below-one regime (`⌈·⌉ = 1`) -- where the seam mattered and where #369's
fixture lives -- is fully closed. Upgrading the high-density case to `⌈·⌉` would need
a ceiling/strict pigeonhole (`exists_lt_card_fiber_of_mul_lt_card_of_maps_to`), left
open.

## Refs

- `experimental/lean/cap25_cap_v13_raw_compact/cap25_cap_v13_raw_compact/BC.lean`
  -- the three new theorems and the maintainer's `census`, `bc_census_floor`,
  `bc_boundary_census_floor` they strengthen.
- `experimental/lean/cap25_cap_v13_raw_compact/cap25_cap_v13_raw_compact/Floor.lean`
  -- `identity_floor`, `code_mem_RS`, `code_agrees`, `exists_heavy_fiber` (the
  pigeonhole machinery reused).
- `experimental/grande_finale.tex` -- `prop:subfield-census-floor`,
  `prop:base-field-floor` (`M_𝔹(d₁)`), `prob:saturated-bc`; the raw frontier package's
  `prop:capg-census-floor` / `prob:capg-split-pencil-B` and
  `thm:bc-interior-prefix-floor` (the ceiling floor
  `M_𝔹(d₁) = binom(m',m)·⌈binom(n,m')/p^{d₁-1}⌉` this formalizes on the lower side).
- PR #369 (`latifkasuli`, agent Codex, `codex/v13-next-frontier`) -- concurrent
  OPEN PR pinning the L4 numeric fixture (`K=65537, m=69753, w=4216`, first interior
  `d₁=4218`, prefix average `< 1`); **cited, not duplicated**. The Lean statements
  here are manuscript-level and independent of that fixture.

**Direction note (post-promotion):** per the promoted note's
`cor:raw-bc-fails`, a raw support-census quantity like the one floored
here can exceed the MCA ray count exponentially — this packet's floors
are list-decoding-style LOWER statements and make no contact with the
open upper target `prob:saturated-bc`.
