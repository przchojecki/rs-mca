# Head-floor second-round repairs: char-2 pairing and ℕ-truncation (lane 22)

**Date:** 2026-07-19.  **Base:** `951ad20`.  **Module:**
`experimental/lean/cs25_cap_v12/cs25_cap_v12/InterleavingTransfer.lean`.
A packet in the #765/#822/#881/#961/#983 falsity-and-repair line; the first
packet that **revises one of our own prior repairs**.

## Executive summary

The 2026-07-18 packet (#961 line, integrated at `6c4ebb3`) repaired
`thm_explicit_head_floor_even` / `thm_explicit_head_floor_odd` by restoring the
paper's `(φ, c)`-smoothness hypothesis (`hsmooth`), and its audit note claimed the
`ZMod 17` countermodel "isolates the dropped hypothesis exactly"
(`skeleton_falsity_repairs.md` :307–:311).  That claim was too strong: **two
further defects survived the first-round repair**, each now certified by a proved
negation lemma against the *current* (post-`hsmooth`) statement, and both repaired
statements are now **proved** (constructive discharge, no sorry).  Census:
`InterleavingTransfer` 3 → 1 (`thm_explicit_pairs` remains, out of scope);
package 10 → 8.

| Item | Status |
|---|---|
| `thm_explicit_head_floor_even_char2_false` (D1) | new, **PROVED** (`GaloisField 2 3`, decide-free) |
| `thm_explicit_head_floor_even_deg_false` (D2) | new, **PROVED** (`ZMod 5`, `K = 0`) |
| `thm_explicit_head_floor_even` | repaired (`h2`, `hK` added), **PROVED** |
| `thm_explicit_head_floor_odd` | repaired (`h2` added; `1 ≤ K` derived), **PROVED** |
| `thm_explicit_pairs` | untouched, still sorried (out of scope) |

## D1 — the antipodal partition was never formalized (char-2 falsity)

**Paper.**  `thm:explicit-head-floor` (archived/cs25_cap_v12.tex :5334) assumes
`−Q = Q` and `0 ∉ Q`, "so that `Q` is partitioned into `N/2` antipodal classes
`{y, −y}`".  The partition into *pairs* is presented as a consequence — and it is
one only in characteristic `≠ 2`.  In characteristic 2, `y = −y`: the classes are
singletons, there are `N` of them, and the proof's `e₁(M) = 0` cancellation
(:5351) and the `C(N/2, m/2)` count both collapse.  The paper carries **no global
odd-characteristic convention** (global conventions at :120 fix only the
coset/subfield frame; the only characteristic sentences are the *derived*
`char ∤ a` at :662, which belongs to the power-map section, and the per-subsection
`p ≡ 3 (mod 4)` at :3888).  Both deployed towers are odd-characteristic
(KoalaBear `p = 2³¹ − 2²⁴ + 1`, :3620–:3621; Mersenne `p = 2³¹ − 1`, :3888,
:3892), so the gap is abstract-field-only: a formalization omission, not a paper
defect.

**Skeleton.**  The statement's `hnegQ : ∀ i, ∃ j, φ.eval (dom j) = −φ.eval (dom i)`
encodes `−Q = Q` and nothing else.  In characteristic 2 it is *trivially* true
with witness `j := i` (`CharTwo.neg_eq`).  No hypothesis excluded `y = −y`; the
partition content of :5334 was simply never formalized — and the #961 packet's
countermodel (odd characteristic, `K = 1`) could not see it.

**Countermodel** (`thm_explicit_head_floor_even_char2_false`): `F = GaloisField
2 3` (`GF(8)`), `ι = Fin 4`, `dom` = four distinct nonzero elements obtained from
the cardinality `|F^×| = 7 ≥ 4` via an abstract embedding (`GaloisField` does not
compute; the entire certificate is decide-free on the field — kernel `decide` is
used only on `Fin`/ℕ side conditions), `φ = X`, `c = 1`, `N = 4`, `m = 2`,
`K = 1`.  Every hypothesis of the current statement holds (`hsmooth` is
tautological at `c = 1` for injective `dom`; `hnegQ` by `CharTwo.neg_eq`; `hmK`:
`2 ≤ 0 + 2`).  Refutation: the claimed list has `C(2,1) = 2 > 0` members at radius
`1 − 2/4 = 1/2`, i.e. some codeword of `RS[F, D, 1]` (a constant, by
`RSpoly_one_const`) within 2 disagreements of `u = φ²|_D` on 4 points; but char-2
squaring is *injective* (Frobenius, `CharTwo.sq_injective`), so `u` takes 4
distinct values and any constant agrees with it at most once — at least 3
disagreements.  Contradiction `3 ≤ 2`.

## D2 — ℕ-truncated degree arithmetic admits `K = 0` (falsity, char-independent)

**Paper.**  The same statement line (:5334) requires `cm ≤ K − 1 + 2c` — integer
arithmetic; at `c = 1`, `m = 2` it reads `2 ≤ K + 1`, i.e. `K ≥ 1`.  (The paper
also writes `K ≤ n`, an upper bound; no lower bound is stated because none is
needed over ℤ.)

**Skeleton.**  `hmK : c * m ≤ K - 1 + 2 * c` in ℕ: at `K = 0` the truncation
gives `0 - 1 = 0`, so `2 ≤ 0 + 2` holds and the statement claims two *distinct*
codewords in `RS[F, D, 0]` — but `degree < 0` forces the zero polynomial, so that
code is `{0}`.

**Countermodel** (`thm_explicit_head_floor_even_deg_false`): `F = ZMod 5`,
`dom = (1, 2, 3, 4)`, `φ = X`, `c = 1`, `N = 4`, `m = 2`, `K = 0`.  All
hypotheses by `decide`/`norm_num` (plus the same tautological `hsmooth`).
Refutation needs no agreement analysis: `P 0 = P 1 = 0`-word contradicts
injectivity of the list enumeration.

**Cross-independence.**  D1's instance has `K = 1` (satisfies the `hK` repair) and
characteristic 2; D2's has characteristic 5 (satisfies the `h2` repair) and
`K = 0`.  Each added hypothesis is therefore *separately* necessary.

## Self-correction of the #961 packet

What #961 claimed (`skeleton_falsity_repairs.md`):

* F4 repair: "`hsmooth : DomSmooth dom (fun x => φ.eval x) c` — the same
  `(φ, c)`-smoothness form consumed by the proved `lem_phi_fiber_ii` /
  `cor_circle_grand`" (:152–:157) — **stands**; `hsmooth` was and remains
  necessary (the `ZMod 17` negation is untouched and still valid against the
  pre-#961 statement).
* "The instance satisfies every remaining hypothesis … so it isolates the dropped
  hypothesis exactly" (:307–:311) — **superseded**: it isolated the *smoothness*
  omission exactly, but the repaired statement still carried two independent
  defects (D1, D2 above) that the instance could not witness (it is
  odd-characteristic with `K = 1`).  The docstring line "A formalization
  omission, not a paper defect" grading survives (now plural in the even
  docstring) — it applies three times over.
* NON-CLAIMS :345 ("No claim that any repaired-but-sorried statement is
  provable as stated") — the #961 packet **did not** claim the repaired even
  statement was true, so the present falsity findings contradict no shipped
  claim; what they correct is the *adequacy* framing of the countermodel.

## Repairs and discharges

**Even** (`thm_explicit_head_floor_even`): added `(h2 : (2 : F) ≠ 0)` and
`(hK : 1 ≤ K)` after `hNeven`; no other signature change.  **Proved.**  Sketch:
`Q := image (φ.eval ∘ dom)` has `|Q| = N` (DomSmooth double count, ECFFT idiom);
squaring is exactly 2-to-1 on `Q` (`y'² = y²` factors as `(y'−y)(y'+y) = 0`;
`−y ∈ Q` by `hnegQ`-closure; `y ≠ −y` from `h0` + `h2`), so `Qsq := image (·²) Q`
has `|Qsq| = N/2`.  For each `T ∈ powersetCard (m/2) Qsq` the locator
`Λ_T = ∏_{r∈T}(φ² − C r)` expands as `(φ²)^{m/2} − e₁(T)(φ²)^{m/2−1} + tail`
with `natDegree tail ≤ 2c(m/2 − 2)` by the lane-21 `rational_locator_expansion`
(ECFFT.lean, imported; instantiated at `f = φ²`, `g = 1` — its `|S| ≤ 1 ⇒
tail = 0` clause is what makes the `m = 2` edge sound), so
`u − Λ_T|_D ∈ RS[F, D, K]` (degree `≤ c(m−2) ≤ K−1 < K`, using `hK`; the
`e₁`-term does not vanish and does not need to — it lands in the codeword).
Agreement: `Λ_T` vanishes on the two complete `c`-fibers of each of the `m/2`
antipodal pairs — `cm` points.  Injectivity: `natDegree Λ_T ≤ cm < cN = n`
forces equal polynomials (`eq_of_eval_eq_of_natDegree_lt`), and `T` is recovered
from vanishing at the fiber witnesses.  The enumeration is the full
`powersetCard`, giving exactly `C(N/2, m/2)`.

**Odd** (`thm_explicit_head_floor_odd`): added `(h2 : (2 : F) ≠ 0)` only, same
position.  `1 ≤ K` is *derived*: `m` odd with `hm_lo` gives `m ≥ 3`, so at
`K = 0` the ℕ-reading of `hmK` says `3c ≤ 2c` — impossible.  **Proved**, by the
even argument shifted by one head factor: `Λ_T = (φ − C t)·∏_{r∈T}(φ² − C r)`
over `T ∈ powersetCard ((m−1)/2) (Qsq ∖ {t²})`; the `t`-fiber contributes `c`
points disjoint from the pair fibers (their squares differ from `t²`), total
`c + c(m−1) = cm`; recovery works because a pair witness has square `≠ t²`, so
the `(φ − C t)` factor cannot be the vanishing one.  The char-2 defect is flagged
on the odd clause **by same-class propagation only** (mirroring #961's precedent
for `hsmooth`): no separate odd counterexample was constructed (it needs `m = 3`,
`N ≥ 6` over a char-2 field, and `GaloisField` does not `decide`) — with the
distinction that here the repaired odd statement is *proved*, so the flag is
non-blocking.

## Gates

* **G1** baseline at `951ad20` (lane-21 ECFFT cache): `lake build` exit 0, census
  10 (`InterleavingTransfer` 3: `:140`, `:235`, `:270`).
* **G2** final clean rebuild (`rm -rf .lake/build && lake build`): exit 0.
* **G3** `#print axioms` on `thm_explicit_head_floor_even_char2_false`,
  `thm_explicit_head_floor_even_deg_false`, `thm_explicit_head_floor_even`,
  `thm_explicit_head_floor_odd`: each exactly
  `[propext, Classical.choice, Quot.sound]`; module grep clean for
  `native_decide` / `axiom` / `admit`.
* **G4** census from the clean-rebuild log: package 8
  (`InterleavingTransfer` 1 = `thm_explicit_pairs`).
* **G5** statement diff vs `951ad20`: even — exactly the inserted line
  `(h2 : (2 : F) ≠ 0) (hK : 1 ≤ K)`; odd — exactly `(h2 : (2 : F) ≠ 0)`;
  the two new negation bodies match the `951ad20` statements binder-for-binder
  (with the `DomSmooth` binder in its statement position).
* **G6** commit touches only `InterleavingTransfer.lean`,
  `SKELETON_REPAIR_CORRESPONDENCE.md`, this note, `agents-log.md`.

## Self-Red-Team

* *Is D1's abstract `dom` a cheat?*  No hypothesis of the statement constrains
  `dom` beyond injectivity + the evaluated conditions, all of which are proved,
  not asserted; the embedding exists by cardinality (`7 ≥ 4`).  The refutation
  consumes only `HasList`'s existential, so non-canonicity of the `Fintype`
  instance on `GaloisField 2 3` is irrelevant (cardinalities are
  instance-independent).
* *Is D2 an artifact of `Nat.choose (N/2) (m/2) = 2 > 1`?*  Yes — deliberately:
  the claimed list size is what makes `K = 0` refutable without any distance
  argument.  A `K = 0` instance with list size `≤ 1` would not refute; the
  statement's own count supplies the contradiction.
* *Could the even discharge have silently weakened the radius?*  No: conclusion
  and radius are byte-identical to `951ad20`; only the two hypotheses were
  inserted (G5).
* *Does `h2` over-repair?*  `h2 : (2 : F) ≠ 0` is exactly "characteristic ≠ 2"
  for a field, the minimal reading of the paper's partition clause; both
  deployed towers satisfy it.  An alternative repair (hypothesizing the
  partition itself) would be strictly stronger syntax for the same content.
* *Does `hK` over-repair?*  The integer reading of :5334 at `m = 2` *is*
  `K ≥ 1`; the alternative (restating `hmK` over ℤ) changes an existing
  hypothesis rather than adding one — `hK` is the minimal audited-diff repair.
  D1 (`K = 1`, char 2) and D2 (`K = 0`, char 5) show neither repair subsumes
  the other.

## NON-CLAIMS

* No paper .tex was edited; all tex anchors cite archived/cs25_cap_v12.tex
  at base 951ad20 and were verified against that base blob.

* **No falsity claim for the odd clause's char-2 gap** — same-class PLAUSIBLE
  propagation only (and the repaired odd statement is proved, so nothing rests
  on it).
* **`thm_explicit_pairs` untouched** — still sorried, statement as repaired by
  #961; no claim about it.
* **No paper-defect claim.**  Both defects are formalization omissions; the
  paper's own clauses (:5334 partition wording; integer `cm ≤ K−1+2c`) carry the
  content.  The partition-as-consequence wording at :5334 silently assumes
  odd characteristic at the theorem's abstract-field generality — worth a
  half-sentence upstream at most, and both deployed instances are unaffected;
  we do not grade it a defect.
* **No numeric deployed-row claim.**  Deployed towers cited only to show the
  repairs cost them nothing (odd characteristic, `K ≥ 1`).
* **No claim of minimality for the counterexample fields** (`GF(8)` is the
  smallest char-2 field with 4 nonzero elements plus room, `ZMod 5` the
  package's established small odd prime; smaller instances may exist).
