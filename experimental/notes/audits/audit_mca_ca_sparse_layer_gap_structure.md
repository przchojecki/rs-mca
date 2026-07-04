# Audit: structure of the MCA-minus-CA gap past the unique radius (toy census)

- **Status:** AUDIT / EXPERIMENTAL. Computational evidence at toy scale; exact
  but exponential oracles; not a theorem.
- **Agent/model:** Claude Fable 5 acting for latifkasuli.
- **Date:** 2026-07-04.
- **Certificate dir:**
  `experimental/data/certificates/mca-ca-sparse-layer-census/` (compact
  headline extract + sha256 pin of the full external frozen artifact,
  `github.com/latifkasuli/mca` commit `e16dd12`).
- **Upstream anchors (all line numbers at `c87675e`):** `thm:mca-from-ca`
  (`tex/cs25_cap_v12.tex:4939`), and in `tex/towards-prize.tex`:
  `prop:p2-half-sharp` (:522), `thm:sparsify` (:661), `thm:sparse-threshold`
  (:682), `thm:pinning` (:696), `thm:rigidity` (:718), `thm:transfer` (:780),
  `prob:mutual` (:852).  (Note: `tex/slackMCA_v4.tex:999` reuses the label
  `thm:rigidity` for an unrelated inverse-quotient theorem; everywhere below
  `thm:rigidity` means the towards-prize match-rigidity theorem.)

## The question

`thm:mca-from-ca` / `thm:sparse-threshold` prove, below half the minimum
distance (`2r <= n-k`), the containment

```text
MCA-bad \ CA-bad  subseteq  { tangent slopes of the nearest explanation }   (<= r slopes).
```

What is the shape of the Johnson-regime extension — the statement that would
let `thm:transfer` carry the BCIKS Johnson-range CA gap over to MCA?  The
natural candidate replaces the nearest explanation by the exact radius-`r`
interleaved pair list `L(r)`:

```text
(candidate)  MCA-bad \ CA-bad  subseteq  U_{(p1,p2) in L(r)} tangents(p1,p2),
```

which would give `|extras| <= |L(r)| * r`.  The census tests this candidate
one step past the unique radius and through the Johnson band on three toy rows
(F_17 n=8 k=4; F_17 n=8 k=2; F_97 n=16 k=8), with per-slope verdicts under the
finite-slope `q_line` convention of the sigma-c-sparse-census lane, and
`CA-bad subseteq MCA-bad` asserted everywhere with zero exceptions.

## The answer

1. **Containment is FALSE one step past the unique radius.**  Verbatim killer
   (row A, F_17, domain `(1,2,4,8,9,13,15,16)`, `k=4`, unique radius 2,
   `r=3`): `f1=[0,0,0,0,0,0,2,1]`, `f2=[0,0,0,0,0,1,1,1]` is 3-close to
   exactly one pair (`(0,0)`, joint error support `{5,6,7}`, tangents
   `{0,15,16}`) yet **all 17 slopes are MCA-bad** and CA-bad is empty: 14
   non-tangent extras, `|extras| = 17 > |L|*r = 3`.  At `r=2` (control) the
   same pair is pair-far and extras are empty.  Engine cross-checked
   (`evaluate_mca_instance`: 17/17 close, 17/17 same-set failures).
2. **Witness-depth invariant.**  All 1293 violating witnesses (805 at A r=3,
   5 at B r=4, 473 at B r=5, 10 at C r=6) decompose only at joint distance
   exactly `n-k`, minimizing over all `q^k` decompositions `q = a + z*b`
   (exact `T`-restricted interpolation for row C).  Depth `n-k` is the generic
   interpolation floor, so violations are exactly the witnesses invisible to
   every pair list `L(m)` with `m < n-k`.  Two natural repairs die: the
   `(r+1)`-list repair with multiplicity-`(D-r)` tangency covers A r=3
   (805/805) and B r=5 (473/473) but fails at B r=4 (all 5 violating slopes
   live only at depth `6 = n-k = r+2`); and `|extras| <= L*r` is dead outright.
3. **Exact-equality window at the Johnson edge.**  Row C (F_97, n=16, k=8,
   `n(1-sqrt(rho)) = 4.69`, GS-complete radius 5.42) at `r=5`: across all 9
   censused instances, extras equal the radius-5 tangent union EXACTLY — zero
   exceptions in either direction.
4. **J-density law: the wall is at capacity, not Johnson.**  With
   `J(n,k,q,r) = sum_{s>=n-r} C(n,s)(q-1)^(n-s)/q^(n-k)`, violation density
   per close slope tracks `J` across every censused cell (A r3 `J=2.83` vs
   `0.577`/slope; B r4 `0.20` vs `0.008`; B r5 `2.63` vs `0.472`; C r5
   `0.0046` vs `0`; C r6 `0.80` vs `~0.43`).  Heuristic flood mass per
   instance is `q*J ~ C(n,r) * q^(1+r-(n-k))`: negligible for `r < n-k-1`,
   `poly(n)` at `r = n-k-1`, `~q` at `r = n-k`.  The toy floods (q=17) are
   small-field manifestations of the capacity transition band; at deployed
   field sizes the same `J` is astronomically small throughout the Johnson
   band.

## Sharpest supported statement

For every instance and radius censused (1048 row A/B instance-radius records,
exhaustive over all 17 slopes; 10 row C engine records):

> Every MCA-bad slope outside CA-bad either lies in the tangent union of the
> exact radius-`r` pair list `L(r)`, or carries only witnesses that decompose
> at joint distance exactly `n-k`, with `>= D-r` simultaneous cancellations at
> the slope.  Equivalently: the containment holds with `L(r)` replaced by the
> depth-`(n-k)` generalized pair list with multiplicity-`(D-r)` tangency —
> `m = n-k` is sufficient in every censused cell and necessary (B `r=4`).
> The number of slopes needing the deep clause has empirical density `<= J`
> per close slope, exactly zero in the Johnson-edge window `J << 1`.

Not claimed: any statement for general `(n,k,q)`, any bound past the censused
radii, or any proof of the `J` heuristic.

## Relation to the towards-prize objects

- **`thm:sparsify` (:661) / `prob:mutual` (:852).**  By the translation
  bijection in `thm:sparsify`, the extras of a pair-close `(f1,f2)` equal the
  MCA-bad set of its sparse residual `(eps1,eps2)`; each pair-close instance
  therefore lower-bounds `sigma_C(r/n)`.  The killer pair is itself sparse
  (support `{5,6,7}`, `e = 3 = r`) and shows `sigma_C(3/8) = 17 = q` on row A:
  one step past half distance the sparse layer can saturate the whole field at
  toy scale.
- **`thm:transfer` (:780).**  The density form is exactly the shape of the
  `sigma_C` bound `thm:transfer`'s hypothesis needs:
  `sigma_C <= |tangent union| + flood`, with measured flood density tracking
  `J` — zero in the Johnson-edge window (C r=5), `Theta(1)`-per-slope only as
  `r` approaches `n-k`.  Since `n-k >= n(1-sqrt(rho))` at every rate, the
  `J`-wall sits strictly above the entire band `delta <= 1-sqrt(rho)-eta` of
  the hypothesis `sigma_C(delta) <= P(n)`: the toy data is consistent with
  that hypothesis exactly where the theorem needs it, and pinpoints where (and
  how) it fails beyond.
- **`thm:pinning` (:696) / `thm:rigidity` (:718).**  Every violating witness
  realizes the pinning formula — the argmin decomposition always matches
  `>= 1` active coordinate (cancellation histograms in the artifact, e.g. A
  r=3: 790 slopes at 1 cancellation, 15 at 2) — and the `>= D-r`
  simultaneous-cancellation requirement in the generalized predictor is the
  census form of the rigidity budget.  The depth invariant `D_min = n-k`
  locates all violating witnesses at the normal-form boundary of
  `thm:pinning`(2): they are exactly the budget-coupled system's generic
  solutions, invisible below the `n-k` floor.
- **`prop:p2-half-sharp` (:522).**  The census upgrades "the wall is sharp —
  one non-tangent bad slope exists" to a quantitative failure profile:
  field-flooding at toy scale, `J`-controlled density, depth-pinned witnesses.

## Relation to the sigma-c-sparse-census lane

`experimental/data/certificates/sigma-c-sparse-census/` records **sigma_C
values** per row: `sigma_C = r` under theorem guard in the trivial regime
`2r <= n-k`, and saturation `sigma_C = q_line` past it, certified by extremal
finite-slope witness sets `S_z = {i : eps1_i + gamma eps2_i = z_i}`.  This
packet is complementary: it characterizes the **structure** of the same layer
— where it is nonempty, why (depth-`(n-k)` generic witnesses), and how it
grows (`J`).  Conventions were verified identical (finite slopes only,
denominator `q_line`, no Mobius quotient; our engine `same_set_failures`
semantics is equivalent to their eps2-only maximal-`S_z` check by
`lem:line`'s final equivalence).  No row collides.

Two caveats so the lanes are not conflated:

- `sigma_C` is a max over all sparse pairs; the census densities are averages
  over a frozen instance family.  The extremal pair can saturate at modest
  `J`: upstream's `(q,n,k,r) = (11,10,2,5)` row has `J ~ 0.13` yet
  `sigma_C = 11 = q_line`, while our comparable-`J` cell (B r=4, `J = 0.20`)
  shows typical density `0.008`/slope.  Not a contradiction — max vs typical.
  The structural claim (tangent union + depth-`(n-k)` witnesses) is
  per-instance universal in the censused cells; the density claim is
  family-average.
- Toy saturation does not falsify `thm:transfer`'s poly-`sigma_C` hypothesis,
  because `q_line ~ n` at toy scale (`sigma_C = q_line = O(n)` is itself
  polynomial); and the flood heuristic `q*J ~ q^(1+r-(n-k))` decays in `q`
  below capacity, so saturation is expected to be a small-field artifact
  except in the band `r in {n-k-1, n-k}`.

## Connection to PR #272

PR #272 (conditional BCHKS25 Thm 4.6 / Hab25 Johnson-regime MCA import for
the deployed KoalaBear row) cites this external census as the toy
statement-shape cross-check of Thm 4.6.  This packet is that cross-check,
ported: the exact-equality window at the integer Johnson radius and the
capacity-located wall are consistent with a Johnson-radius mutual statement of
Thm 4.6's shape, while the killer counterexample shows which naive
strengthening (tangent containment with the radius-`r` list) is already false
one step past the unique radius.

## Honest scope

- Toy rows only; A/B exhaustive (all 17 slopes, 1048 instance-radius records,
  109 verbatim counterexample dumps), row C engine-driven (GS exact at r=5;
  r=6 is one targeted 28-challenge instance — densities there are estimates).
- All oracles exact but exponential (`q^k` enumeration, `C(n,n-r)` pair
  lists); nothing scales to deployed rows.
- The `J`-law is a measured correlation across 8 cells, not a proved bound.
- Deterministic and frozen: seeds `20260704` (A/B) and `97161604` (C); the
  external artifact is byte-stable, sha256
  `e7c559652692fdf4d62a1c2a5cf1c60f6ab6a9b216300b7ab87315b8254dc98b`,
  reproduced here via `--quick` (67 s, headline pins assert on regeneration).

## What to do next

- Decide whether the depth-`(n-k)` generalized-pair-list form of the sharpest
  supported statement is worth stating as a conjecture next to `prob:mutual`
  (it is the exact containment shape that survived the census).
- If the sigma-c lane's Pade-Hankel scanner is extended past `r = 2`, its
  extremal witnesses can be checked against the depth-`(n-k)` +
  multiplicity-`(D-r)` predictor for free — a cross-lane consistency test.
- A proof attempt for the `J`-density form should target the transition band
  `r in {n-k-1, n-k}` where the toy floods live; below it the census saw
  literally zero violations.
