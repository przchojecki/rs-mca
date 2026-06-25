# L2 sharp-constant conjecture — falsification log

- **Status:** FALSIFICATION-IN-PROGRESS / EXPERIMENTAL. Running the
  conjecture→falsify→iterate methodology on the L2 sharp-constant interleaved
  conjecture (`l2_interleaved_dilation_constants.md` §2) before any proof attempt.
- **Agent/model:** Claude Opus 4.8 (L2/X1 lane, branch `allen/l2-x1-interleaved-mca`).
- **Date:** 2026-06-24.
- **Conjecture under test:** above the reserve,
  `Lst(Int(C,μ), 1−a/n) ≤ binom(n,a)·q^{−μ(a−k)} + Quot_μ + n^B`, the open piece
  being the aperiodic μ-fold intersection remainder `n^B`.
- **Scanner:** `experimental/scripts/verify_l2_falsify_interleaved.py`.

## Iteration 1–2 (F_17, n=16, k=3, a=5, σ=2)

**Setup fact (used throughout).** The interleaved list at radius `1−a/n` is
`#{(c_1,…,c_μ) : |∩_i A_i(c_i)| ≥ a}`. Since distinct degree-`<k` codewords agree
on `≤ k−1 < a` points, a common agreement support `S` (`|S|≥a`) **pins one
codeword per row**, so each listed tuple is `(interp(U_1,S),…,interp(U_μ,S))` for a
common support `S`. Tuples ↔ common supports.

**Correction to a naive guess.** "interleaved ≤ min base fiber" is **FALSE**: when
one row is an exact codeword (`A_1 = H`), the interleaved list equals the *other*
row's fiber, which exceeds `min_base`. The right quantity to watch is
`max_i |Fib(U_i)|`.

**Decisive question tested:** can interleaving **create mass**, i.e.
`interleaved > max_i |Fib(U_i)|`? (Yes ⟹ L2 has content beyond L1; a super-poly
such remainder would threaten the conjecture. No ⟹ interleaved ≤ a single-row
fiber ≤ L1's poly above the reserve.)

**Adversarial sweep:** exact codeword row; near-codewords; aligned 2-codeword
gluings; **misaligned** gluings (block vs even/odd vs mod-3 partitions — the
construction meant to realize cross pairs); monomial; quotient-periodic; `μ=2,3`.

**Result: NO mass creation.** `interleaved ≤ max_base` in every family. Notable:
- exact-codeword × glued(8-fiber): interleaved `= 8 = max_base` (bounded by the
  larger fiber, as predicted for a codeword row).
- aligned gluings: interleaved `= 2 = max_base` (only the diagonal cross pairs).
- **misaligned gluings: interleaved `= 0`** — distinct-region overlaps fall below
  `a`, so the rows share *no* common support. Misalignment *destroys* the list
  rather than creating cross-mass (the opposite of the naive worry).
- The random-baseline term `binom(n,a)q^{−μ(a−k)} ≈ 0.05` here, so the observed
  mass is entirely the structured/base-fiber part — consistent with `Quot_μ + n^B`.

## Reading (honest)

This is **supporting evidence**, not proof. Across this sweep the interleaved
list is bounded by a single-row base fiber, so above the reserve (base fibers
poly by L1) it would be poly — i.e. **L2's aperiodic remainder looks subsumed by
L1** (`interleaved ≤ max base fiber`). That would both harden the conjecture and
simplify it (reduce L2's open piece to L1). But the sweep is small and
hand-picked; the "create mass" construction tried here self-destructs (overlaps
< a), so it does not yet *rule out* a cleverer cross-mass word.

## Iteration 2 (engineered witness + random search, F_17 n=16 k=3 a=5)

**Mass creation IS achievable — correcting iteration 1's tentative reading.** A
pure 2-codeword-per-row gluing has cross-overlaps `|P_1^a ∩ P_2^b|` that (for pure
partitions) **sum to `n`**, so "all 4 cross-pairs ≥ a" needs `4a ≤ n` (`20 > 16`,
impossible) but **3 cross-pairs** (`5+5+5+1=16`) is possible. Engineered witness:
`interleaved = 3 > max_base = 2` (predicted 3). So **`interleaved ≤ max_base` is
FALSE** — L2 is *not* trivially subsumed by L1.

**But the excess is `O(1)`.** Random search (4000 gluings): max `interleaved = 4`,
`max_base = 2`, **max ratio 2.0**. The empirical search **caught an error** in my
clean bound: I predicted `interleaved ≤ n/a = 3`, but the agreement sets are
slightly larger than the partition cells (codewords coincidentally agree on up to
`k−1` extra points), so cross-overlaps don't *exactly* sum to `n` and the count
reached 4. The honest statement: the cross-overlaps sum to `~n` (exact for pure
partitions + small `≤k−1` corrections), so `#cross-pairs ≥ a` is `~n/a`, and the
excess over a single-row fiber is `O(1)` across this search — **no super-poly
threat from the gluing attack**, but the precise constant slightly exceeds `n/a`.

**Reading:** the conjecture looks robust against gluing attacks (the natural
adversary creates only `O(1)` extra mass, absorbed by `n^B`). The decisive open
test is whether the max ratio **grows with `n`** (super-poly) or stays `O(1)`.

## Iteration 3 (n-scaling, grid construction) — and a key reframe

First attempt capped `interleaved` at `4` by gluing only 2 codewords/row (`2²`) —
caught before claiming. Fixed with a **grid construction**: tile `H` into
`s₁·s₂` size-`a` blocks, codeword `dᵢ` on row-1 block-rows, `eⱼ` on row-2
block-cols ⇒ all `s₁·s₂` cross-pairs realized.

**Result (k=2, a=4):** `interleaved` tracks `n/a` linearly —
```
n:        12  16  20  24  48   (88)
interleaved: 3   4   5   6  12   (28, n/a=22; max_base=105 = small-block artifact)
n/a:       3   4   5   6  12    22
```
Linear in `n` (polynomial), **not** exponential. So the gluing/grid attack
creates only `~n/a` mass.

**The reframe (important).** `interleaved ≤ (base fiber)^μ ≤ (n^B)^μ = poly`
**trivially** (μ constant). So the conjecture's `n^B` polynomial remainder is
**already subsumed by L1** — it is *not* the open piece. The genuinely
L2-specific content is **only the sharp constant / the saving**
(`binom(n,a)q^{−μ(a−k)}` vs the Cartesian `binom(n,a)^μ`). The gluing attack tests
*that*: `interleaved ~ n/a ≪ Cartesian`, so the saving **holds** robustly.
Domain reason: fiber agreement sets pairwise overlap `≤ k−1` (RS distance), so the
cross-overlaps sum to `~n` and `#cross-pairs ≥ a` is `~n/a` — linear/poly, never
super-poly.

**Status:** the conjecture is robust against the gluing adversary. The naive
"interleaved ≤ max_base" is false (iter 2) but irrelevant — polynomiality comes
free from L1, and the saving survives. OPEN: (a) *prove* the sharp saving (the
finer second-moment / codegree argument, already partly in
`l2_interleaved_dilation_constants.md §5`); (b) test NON-gluing adversarial words.

## Iteration 4 — the saving reduces to punctured-RS list decoding (PROVED + verified)

Now that polynomiality is free (iter 3), attacked the *saving* directly and found
a clean **provable decomposition** (`verify_l2_codegree_decomposition.py`):

> **Lemma (codegree decomposition, μ=2).** A tuple `(c₁,c₂)` is interleaved-listed
> iff `c₂` agrees with `U₂` on `≥ a` points of `A₁(c₁) = {x: c₁(x)=U₁(x)}`. Hence
> ```
> |Λ(Int(C,2), 1−a/n, U)| = Σ_{c₁∈Fib₁(U₁)} | Λ( RS[F, A₁(c₁), k], 1−a/|A₁(c₁)|, U₂ ) |,
> ```
> a sum over the row-1 fiber of the list of `U₂` on the **punctured domain**
> `A₁(c₁)` (size `≤ n`). General `μ`: the inner object is the `(μ−1)`-fold
> interleaved list on the puncture (recurse).

**Verified exactly** (identity `interleaved == codegree_sum`) for gluing *and*
non-gluing words (codeword+noise, mod-3 interleaved, near-codeword clusters), with
the inner punctured lists small (`≤ 2`; often `1` = unique decoding).

**Why this matters:** it pins the L2 sharp saving to a *known* object — the saving
is exactly that each inner term is a punctured-RS list (unique-decoding `=1` when
`a > (|A₁(c₁)|+k)/2`, Johnson-bounded otherwise), **not** `|Fib₂|`. So
`interleaved = |Fib₁| · (small punctured list)`, not `|Fib₁|·|Fib₂|`. This is the
structural skeleton of a proof of the saving: bound the punctured-RS list (Johnson)
and sum over `Fib₁` (L1). Remaining gap: the worst-case punctured-list constant
across all `A₁(c₁)` and the `μ>2` recursion constants — the genuine sharp-constant
content, now reduced to standard RS list-decoding on punctured domains.

## Next iterations (planned)

1. **Engineer genuine cross-mass:** partitions whose pairwise cross-regions are
   each `≥ a` (needs `n` larger, or `a` smaller relative to `n`), to actually test
   whether `interleaved > max_base` is achievable at all.
2. **Randomized adversarial search** over many words (not hand-picked), larger
   fields `F_p`, `F_{p^2}`, and rates `ρ ∈ {1/2,1/4,1/8}`; record the worst
   observed `interleaved / max_base`.
3. **Directly test the bound** `interleaved ≤ binom(n,a)q^{−μ(a−k)} + Quot_μ + n^B`
   with the exact `Quot_μ = L_μ(a,τ)` count, hunting a reserve-cleared excess.
4. If `interleaved ≤ max_base` keeps holding, attempt to *prove* it (it would be
   the clean structural statement reducing L2's aperiodic part to L1).

## Iteration 5 — exact `Quot_rem_μ` + quotient-periodic stress (planned-item 3)

Implemented the explicit quotient budget `Quot_rem_μ(n,k,a)` from
`l2_sharp_target_conjecture.md` §2 and tested the **full** V0 right-hand side on
quotient-periodic words (the stress case the packets target).
Scanner: `experimental/scripts/verify_l2_quotient_budget.py`.

**Rigorous core (conjecture-independent, all verified):**
- `E_empty(R,b,μ) = Σ_j (−1)^j C(R,j) C(R−j,b−j)^μ` matches a **brute-force** count of
  ordered μ-tuples of `b`-subsets of `[R]` with empty common intersection
  (`R≤5`, all `b`, `μ∈{1,2,3}`); and `E_empty(R,b,1)=[b=0]`.
- Aligned endpoint `L_{M,μ}(a,u_M)=C(Q,ℓ_M)` (the note's key non-Cartesian fact —
  it is `C(Q,ℓ_M)`, **not** `C(Q,ℓ_M)^μ`).
- Active-scale criterion: a scale `M` contributes iff `M|n` and `σ<M≤a`.

**Probe (n=16,k=3,a=5,μ=2; only active scale `M=4`, `Quot_rem_2 = 3`):** swept 322
quotient-periodic words per scale (all linear `g(x^M)=g₀+g₁x^M` + random full
coset-assignments), precomputed fibers, all ordered pairs.
- worst `interleaved = 18`, but `= max_base` — **entirely single-row (L1) mass**.
- worst **genuine μ-fold cross-mass** `interleaved − max_base = 0`: quotient-periodic
  words create **no** cross-mass here (`interleaved ≤ max_base` always), so they do
  **not** violate V0 and do not even stress `Quot_rem_μ` (cross-mass `0 ≤ 3`).

**Grid gluing attack vs the FULL V0 bound at scale** (the cross-mass family of
iters 2–3, now with the exact `Quot_rem_μ`; `k=2,a=4`, `μ=2`):

| n | interleaved | rand term | `Quot_rem_μ` | residual→`n^B` | n/a |
|---|---|---|---|---|---|
| 12 | 3 | 0.017 | 5 | −2.0 | 3 |
| 16 | 4 | 0.022 | 3 | +1.0 | 4 |
| 20 | 5 | 0.002 | 4 | +1.0 | 5 |
| 24 | 6 | 0.000 | 12 | −6.0 | 6 |
| 48 | 12 | 0.002 | 26 | −14.0 | 12 |

The grid cross-mass is `~ n/a` (polynomial), and the residual `interleaved − rand −
Quot_rem_μ` is small (often **negative** — `Quot_rem_μ` alone already covers it). So
the full V0 bound holds with margin for the worst gluing attack at scale.

**Reading (honest).** Consistent with the conjecture on both natural family types:
the large interleaved counts from periodic words are the single-row quotient (L1)
list charged to `n^B`, the aligned packet is `C(Q,ℓ_M)` not `C(Q,ℓ_M)^μ` (no
Cartesian blow-up), μ-interleaving does **not** amplify periodic mass (cross-mass
`=0`), and the grid gluing cross-mass stays `~n/a ≪ rand+Quot_rem_μ+n^B`.

## Falsification status (honest ceiling)

Across iters 1–5 the L2-Sharp V0 conjecture has survived every natural adversary:
- **gluing/grid** (the only family that creates cross-mass): cross-mass `~n/a`,
  polynomial, within `rand + Quot_rem_μ + n^B` at scale (iter 3, iter 5 table);
- **quotient-periodic** (the quotient-packet stress case): **no** μ-fold cross-mass
  (`interleaved ≤ max_base`), so no `Quot_rem_μ` stress (iter 5);
- the explicit `Quot_rem_μ` budget is **verified** (brute-force `E_empty`, aligned
  endpoint `C(Q,ℓ_M)`, active-scale criterion) (iter 5);
- polynomiality of the remainder is **free** from L1 (`interleaved ≤ (base)^μ`,
  iter 3 reframe); the genuine L2 content is the **sharp saving**, which iter 4
  reduced to **punctured-RS list decoding + L1** (codegree decomposition → PR #108).

**No super-polynomial excess over `rand + Quot_rem_μ` was found in any tested
family.** The conjecture is well-hardened at small/below-reserve scales and `μ=2`
(μ=3 periodic is `≤` by the more-rows-shrink-the-support monotonicity). The
remaining open piece — the **sharp saving** — is not a falsification target but a
proof obligation, and it is **L1-gated** (the punctured-list/codegree constant rests
on L1's aperiodic profile bound, Codex's lane). Falsification has reached its honest
ceiling; further progress on L2 is the L1-gated proof, not more small-model search.

## Reproducibility
```bash
python3 experimental/scripts/verify_l2_falsify_interleaved.py
python3 experimental/scripts/verify_l2_quotient_budget.py
```
