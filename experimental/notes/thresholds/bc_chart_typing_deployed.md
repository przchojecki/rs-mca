# First deployed-row chart typing for prob:saturated-bc: the simple-pole/rank-one cell, placement decided by computation

**Status: EXPERIMENTAL / AUDIT — PROVED-LOCAL (placement argument,
non-pencil exclusion lemma, from cited upstream propositions) /
CITED-THEOREM (enumerative half) / CONDITIONAL_ON_NAMED_INPUT (the B*
budget fit) / MEASURED (toy placement replays).** Base
`2633895a66d3edf516120a87b2eb18c994f977ab`
(`experimental/grande_finale.tex` = gf; line anchors verified against the
blobs at base). **No `.tex`/`.pdf` edited.**

| item | value |
| --- | --- |
| object | the simple-pole/rank-one cell (`prop:pole-line` gf L583, `prop:rank-one-floor` gf L1523), typed at BOTH deployed MCA adjacent rows in `prob:saturated-bc`'s per-row grammar (gf L2191-2204) |
| the new move | the first-match PLACEMENT of the cell is DECIDED BY COMPUTATION (Gate 1), not presupposed: boundary-Q-owned vs fresh named (b)-cell were both admissible certificate outcomes |
| computed outcome | **BOUNDARY_Q_OWNED** — every computed pole-line profile is `d1 = w+1`, the boundary-Q profile (`prop:boundary-q` gf L1475-1492; `bc_section.tex` L24-29: interior is `w+2 <= d1 <= floor((n-K+1)/2)`) |
| type assignment | **(b)-via-Q**: a named cell whose own slope bound IS the row-sharp Q atom target (`def:q-row-atom` gf L2043-2059); quantitatively NOT type (a) (non-pencil exclusion lemma below) |
| lineage | third chart family overall, after the toy-row near-pencil family (`experimental/notes/bc_near_pencil_chart_reduction.md`) and the L4 planted interior family (`cap25_v13_bc_l4_interior_chart_to_q.md`: "(b), the charge goes to Q") — and the FIRST at a deployed `a_+` row |
| certificate | `experimental/data/certificates/bc-chart-typing/bc_chart_typing.json` |
| verifier / checker | `experimental/scripts/verify_bc_chart_typing.py` (`--emit-defaults`/`--check`), `experimental/scripts/verify_bc_chart_typing_check.py` (`--check`, no-import, no-Popov) |

**Use Rule.** Downstream material citing this packet must (i) cite the
cell at its computed placement — a boundary-Q-owned cell paid by
`prob:saturated-bc`'s first-match preamble BEFORE the residual chart set
begins — and not as a saturated-BC residual chart that has been
"resolved"; (ii) state every count at slope/ray-deduplicated scale only
(the `#679`/`#518` Use Rules, `r1_rawcount_refutation.md` /
`capg_split_pencil_refutation.md`, are inherited unchanged); and (iii)
treat the B* fit as CONDITIONAL_ON_NAMED_INPUT (depth-`w` max-fiber /
row-sharp Q) — the proved side is a floor pin, never an upper bound.

## Verdict block

- **Claim.** At both deployed MCA adjacent rows (KoalaBear
  `a_+ = 1116048`, Mersenne-31 `a_+ = 1116024`; `n = 2^21`, `K = k+1 =
  2^20+1`, `w = a_+ - K = 67471/67447`), the simple-pole/rank-one cell
  carries the typed certificate row: placement = boundary-Q profile
  `d1 = w+1` (computed, Gate 1; forced at deployed scale by the module
  element + near-rational dichotomy below), type = (b)-via-Q (its own
  slope bound is the Q atom target), NOT type (a) (its
  heaviest-fiber witness floor `B_B(a_+)`
  exceeds the one-pencil cap `floor((n-g)/(omega-g))` for every
  `g < omega`, Gate 3), extension-branch-excluded (`B_B(a_+) > H_ext`,
  `prop:extension-cell-target` gf L402-421), enumeratively exact by
  cited theorem, and B*-fitting only under the named input.
- **Status.** EXPERIMENTAL / AUDIT.  Per-row chart VERIFICATION progress
  on `prob:saturated-bc` — one named cell typed, enumeratively exact,
  budget fit CONDITIONAL_ON_NAMED_INPUT (depth-`w` max-fiber / row-sharp
  Q).  Not a resolution (see NON-CLAIMS).
- **Verifier.** Exact big-int replay + toy placement replay, stdlib-only,
  deterministic, byte-stable, no timing or machine data; the deployed
  arithmetic is computed TWO independent ways inside the generator
  (Legendre floor-sum + product tree vs Kummer carry-count + heap merge,
  opposite anchors, opposite stepping directions; gate name
  `two_routes_agree_exactly_on_all_four_rows`) and a THIRD way in the
  independent checker (binary-splitting factorial products + one exact
  division, with `math.lgamma` cross-estimates), because the M31 margin
  (3.2589 bits) is adjacency-critical.
- **Consumers.** `prob:saturated-bc`'s per-row audit (the boundary-Q
  first-match line of its preamble now has a deployed-row certificate
  with exact integers); `prob:row-sharp-q`/`def:q-row-atom` (the cell's
  entire charge is routed there, quantified); the thresholds draft's
  hard inputs 1/3 (its four proved ray compilers are vacuous at this
  cell's deployed scale — kappa/t/k-c all huge — so this cert supplies
  the exact ray payment those compilers cannot reach).
- **Risk-limits.** The growing-deficiency BC interior core (dim
  `omega-w+1 = 913634/913682`) is `prob:band`-hard (Gamma_r route,
  budget-fit Sec. 6: misses the floor by `~2.07M` bits against 22-/3-bit
  margins, tractability LOW) — this packet types one boundary-owned cell
  and cannot reach that core.  The M31 row is margin-adjacent twice
  over: +3.2589 bits here, and the same row already carries the #690
  `-0.3938`-bit TIGHT watch-item rung.

## 1. The cell, in prob:saturated-bc's grammar

`prob:saturated-bc` (gf L2191-2204) demands, per active MCA adjacent
row, that "after quotient, boundary-Q, common-support, tangent,
extension, degree-drop, and common-GCD branches have been paid by first
match", every remaining balanced-core split-pencil chart be (a) a
projective one-parameter locator pencil covered by `cor:bc-one-pencil`,
or (b) "explicitly split into such pencils, or else assigned to a
separate named residual cell with its own slope, not raw-support,
bound."

The **simple-pole/rank-one cell** at a deployed MCA row is the received
line family

```
(f_alpha, g_alpha) = ( U_z/(X-alpha), -1/(X-alpha) ),
alpha not in D u B,   z in B^w a depth-w prefix value,
```

(`prop:pole-line` gf L583: explaining supports at threshold `m = a_+`
are EXACTLY `S in Fib_w(z)` with `ell_S(alpha) = U_z(alpha) - zeta`;
`prop:rank-one-floor` gf L1523: at a heaviest prefix value `z*`,
`|Fib_w(z*)| >= ceil(C(n,a_+) p^-w) = B_B(a_+)`, and the line is
genuinely extension-valued).  By the #715 witness-fiber calibration
(`lineray_census_rerecording.md`), this depth-`w` MCA-route fiber is
cap25's depth-`(w'-1)` witness fiber — one dimension BELOW the census
depth `w' = a_+ - k` — and the budget-fit MCA-row floors already sit
exactly at this scale (`2^35.7352` KB / `2^20.7411` M31; consumed by
payload hash, Gate 4).

## 2. The placement computation (the outcome is computed, not presupposed)

For a slope `zeta`, the pole-line word `U = f_alpha + zeta g_alpha =
(U_z - zeta)/(X - alpha)` admits the module element

```
(W, N) = (X - alpha, U_z - zeta)  in  M_U,
```

since `(x - alpha) * U(x) = U_z(x) - zeta` for every `x in D`
(`prop:lattice-split` gf L1336).  Its shifted degree is

```
wdeg(W, N) = max( deg(X - alpha), deg(U_z - zeta) - (K-1) )
           = max( 1, a_+ - K + 1 )  =  w + 1
```

(deployed values `w+1 = 67472` KB / `67448` M31), so `d1 <= w+1` at
EVERY scale.  On the other side, `d1 <= w` is exactly the near-rational
branch (`thm:near-rational` gf L1350), and `cor:near-rational-line` (gf
L1381) leaves at most one near-rational finite slope per line, paid
outside the balanced core.  Hence all but at most one slope of the cell
sits at `d1 = w+1` exactly.

**Gate 1 computes this profile end-to-end** at two toys (harnesses
ported from the in-tree #715 Gate B/C machinery), by exact shifted
weak-Popov reduction in the generator and by Popov-free rank tests in
the independent checker:

| toy | fiber | alphas | distinct slopes | computed d1 (all) | near-rational | interior range |
| --- | --- | --- | --- | --- | --- | --- |
| `F_73` (n=24, K=12, m=15, w'=3; p = q) | 13 | `alpha = 0` | 8 | **4 = w'+1** | 0 | `[5, 6]` |
| `F_{17^2}` (n=16, K=6, m=9, w'=3; extension-valued) | 40 (witness, depth w'-1) | `17, 18, 288` | 40 / 39 / 39 | **4 = w'+1** | 0 | `[5, 5]` |

(Toy convention, inherited from the #715 census-toy harnesses: in these
two rows `w' := m - K`, which plays the deployed `w = a_+ - K` role, so
the computed boundary value `d1 = w'+1` is the same `(m-K)+1` endpoint
as the deployed `d1 = w+1` — distinct from Sec. 1's census depth
`w' = a_+ - k`.)

Every computed profile is the boundary value; none lands in the
interior.  `d1 = w+1` is the **boundary-Q profile**: `prop:boundary-q`
(gf L1475-1492) — "Consequently Q is the boundary profile of the
split-pencil problem, and BC starts only after this profile is removed"
— and `bc_section.tex` L29: "The excluded endpoint `d_1=w+1` is the
quotient/prefix boundary profile and belongs to Q, not to BC."

> **Computed placement outcome: BOUNDARY_Q_OWNED.**  The cell is paid by
> the boundary-Q first-match branch of `prob:saturated-bc`'s preamble
> before the residual chart set begins.  It is NOT a fresh saturated-BC
> residual cell.  (The other admissible outcome — a fresh interior
> (b)-cell — was a well-formed certificate too; the computation ruled it
> out.)

## 3. Non-pencil exclusion lemma (the cell can never be typed (a))

**Lemma.** Let `Fib` be a set of `N >= 2` distinct `m`-subsets of `D`,
`|D| = n`, `omega = n - m`, and for `S in Fib` let
`W_S = ell_{D\S}` be the monic degree-`omega` `D`-split locator with
root set `D\S`.  If every `W_S` lies in a single projective locator
pencil `L_[s:t] = sA + tB` (`def:projective-locator-pencil` gf L1722)
with `g = deg G_D(A,B) < omega`, then

```
N  <=  floor( (n-g)/(omega-g) )  <=  n - omega + 1  =  m + 1 .
```

*Proof.* Distinct `S` give distinct root sets `D\S`, hence distinct
monic degree-`omega` polynomials `W_S`; two pencil members with the same
projective parameter are proportional, and proportional monic
polynomials of equal degree coincide — so `S |-> [s_S : t_S]` is
injective.  Every `W_S` is `D`-split with `omega` distinct roots in `D`
and is divisible by the common `D`-part `G`, so `W_S/G` has exactly
`omega - g` distinct roots in `D \ Z(G)`: each counted parameter has at
least `h = omega - g >= 1` moving roots.  `thm:bc-moving-root` (gf
L1735: each moving domain point `x` satisfies `sA(x) + tB(x) = 0` for
exactly one `[s:t]`, so the incidence count gives
`|Z| <= floor((n-g)/h)`) yields `N <= floor((n-g)/(omega-g))`.  For
`0 <= g < omega` and `n > omega` this bound is nondecreasing in `g` and
peaks at `g = omega - 1` with value `n - omega + 1 = m + 1`. ∎

This is `prop:bc-not-q`'s mechanism made quantitative for this cell:
the boundary cell is "a high-dimensional affine divisor slice" of
dimension `omega - w = 913633` (KB) / `913681` (M31) (`prop:bc-not-q`
gf L2120-2145, its table matched exactly by Gate 2), and "a
line-by-line decomposition without a bound on the number of lines gives
no row budget" (gf L2144).

**Gate 3 (deployed, exact).** Full sweep of `floor((n-g)/(omega-g))`
over all `0 <= g < omega` at the corrected `omega` (and, robustness, at
the printed `omega - 1000`):

| row | omega (correct) | max_g pencil cap (at g = omega-1) | cell witness floor B_B(a_+) | excess | factor |
| --- | --- | --- | --- | --- | --- |
| KB-MCA | 981104 | 1,116,049 | 57,198,030,366 | 57,196,914,317 | `2^15.6453` |
| M31-MCA | 981128 | 1,116,025 | 1,752,700 | **636,675** | `2^0.6512` |

The cell's witnesses at a single heaviest-fiber line do not fit in ANY
single one-parameter pencil — at M31 by only 0.65 bits, an
adjacency-flavored exact integer (`1752700 > 1116025`), which is why the
sweep is exact and not an estimate.  The exclusion also holds at slope
level unconditionally: choosing exactly `B_B(a_+)` fiber members,
`C(B_B,2)(K-1) < q - p` at both rows (exact big-int comparisons, Gate
3), so `prop:rank-one-distinct-slope-floor`'s averaging (gf L1546)
yields an `alpha` with zero slope collisions.  Toy halves: the 13/40
witness locators span rank 6 > 2 at both toys (a pencil is a
2-dimensional space); the counting cap bites at `F_{17^2}` (40 > 10)
but not at `F_73` (13 <= 16) — the counting exclusion is
scale-dependent, the deployed rows are on the biting side.

## 4. Typed certificate rows (both deployed MCA rows)

Corrected `omega` throughout — the `cor:bc-one-pencil` worked table (gf
L1771-1777) prints `omega = n - m - 1000` (980104/980128), a 1000-off
typo ALREADY BANKED in-tree with `parks_for_ken = true`
(`bc_one_pencil_omega.json`, consumed by payload hash; `floor(n/omega) =
2` unaffected either way).  This packet cites that certificate and does
not re-park.

| field | KoalaBear MCA | Mersenne-31 MCA |
| --- | --- | --- |
| cell | simple-pole/rank-one | simple-pole/rank-one |
| `a_+`, `w` | 1,116,048; 67,471 | 1,116,024; 67,447 |
| placement (computed) | BOUNDARY_Q_OWNED (`d1 = w+1 = 67472`) | BOUNDARY_Q_OWNED (`d1 = w+1 = 67448`) |
| type | (b)-via-Q: named cell whose own slope bound IS the Q atom target (`def:q-row-atom`) | same |
| NOT type (a) | `57198030366 > 1116049` (every `g`) | `1752700 > 1116025` (every `g`) |
| `omega` (correct / printed) | 981,104 / 980,104 | 981,128 / 980,128 |
| `dim` (affine slice, `omega-w`) | 913,633 | 913,681 |
| `B*` | 274,980,728,111,395,087 (`floor(p^6/2^128)`) | 16,777,215 (`floor(p^4/2^100)`) |
| floor `B_B(a_+) = ceil(C(n,a_+)p^-w)` | 57,198,030,366 = `2^35.7352` | 1,752,700 = `2^20.7411` |
| margin `log2 B* - log2 B_B` | **22.1969 bits** | **3.2589 bits** |
| `H_ext` (gf printed, reproduced exactly) | 4,807,520 | 9 |
| extension exclusion | `B_B > H_ext`: the paid extension branch cannot absorb the cell | `1752700 > 9` |
| enumerative half | CITED-THEOREM (below) | CITED-THEOREM |
| B* fit | CONDITIONAL_ON_NAMED_INPUT | CONDITIONAL_ON_NAMED_INPUT |

All four deployed rows (both list rows too: `B_B = 65065153468 =
2^35.9212`, margin 22.0109; `1993678 = 2^20.9270`, margin 3.0730;
`H_ext = 4226236 / 8`) are recomputed by the two independent in-generator
routes and cross-asserted for exact big-int equality — the named gate
`two_routes_agree_exactly_on_all_four_rows` — and by the checker's third
route.  The `H_ext` column reproduces `prop:extension-cell-target`'s
printed table (gf L412-418) exactly from `H_ext = floor(p^w B* /
C(n,a_+))`; note this is the margin identity in integer floor form.

**Enumerative half (CITED-THEOREM, not new).**
`thm:exact-list-line-bijection` + `cor:exact-prefix-ray-realization`
(`asymptotic_rs_mca_frontiers.tex` L2097/L2157): at a separating pole
the cell's slope set is in bijection with the prefix fiber, occupancy
one; a separating pole exists in any field with `q > n + k*C(L,2)` (its
eq. 4.6).  Under the named input (`max fiber <= B*`), that inequality
holds at both deployed rows (exact comparisons in Gate 3).  #721's
`M_RH` theorem covers the reduced rational-host stratum containing this
cell and explicitly disclaims novelty for the separating simple pole
while retaining the nonseparating `d = 1` formulas as a
collision-literal audit; its printed `F_17`, `J = -1` census (`F_RH =
M_RH = 76`, 16 slopes, max same-slope fiber 7, slope 13 absent) is
replayed in full by both scripts (#721 has no JSON certificate in-tree;
it is consumed by whole-file sha256 + content pins + this replay).
Loss-2 = 0 on pole lines (pair rigidity) and the per-alpha slope
collision structure are #715's banked content, consumed by payload hash
(Gate C values 40/39/35, 204/272 collision alphas — our three-alpha
replay agrees where it overlaps).

## 5. The Q-conditional budget line, printed against the #690 watch-item

What a first-match ledger (`def:first-match-ledger` gf L148) needs from
this cell is `max_z |P_Q(z)| <= B*` with `P_Q(z) subseteq Fib_w(z)` —
`def:q-row-atom`'s "sufficient integer form", i.e. row-sharp Q at
depth `w`, one dimension below the census depth.  What is PROVED today
is only the two-sided pin of the heaviest-fiber pole-line class at
`B_B(a_+) = B* * 2^-Delta` (budget-fit P1, consumed by file sha256 +
field equality: "fixes the TARGET CONSTANT for a general upper bound;
is NOT itself a general upper bound").

```
KB-MCA:   B_B = 2^35.7352  vs  B* = 2^57.9321   margin +22.1969 bits
M31-MCA:  B_B = 2^20.7411  vs  B* = 2^24.0000   margin  +3.2589 bits
watch:    #690 m31_mca Gceil c=2048: M = 12,769,758 vs B* = 16,777,215
          margin -0.3938 bits, TIGHT, non-firing (payload-hash consumed)
```

Reading: the M31 row's ledger already carries a sub-bit-tight rung.  Any
flatness multiplier `>= 2^3.2589` on the M31 heaviest depth-`w` fiber
would overrun `B*`; the fit is therefore left CONDITIONAL_ON_NAMED_INPUT
and every row integer above is exact and triple-routed.  Budget-fit P2
is the fixed-deficiency complement (deficiency 1 -> 2 slopes/pencil;
deficiency 2 -> `C(n,2)/(omega-1) ~ 2^21.10`, which alone would eat
`~2^21.1` of M31's `2^24` budget) — cited, not re-derived.

## 6. Weave / collision

- **#666 / #715 / #679 / #518** (`split_pencil_ray_collapse.md`,
  `lineray_census_rerecording.md`, `r1_rawcount_refutation.md`,
  `capg_split_pencil_refutation.md`): the dedup vocabulary, the
  witness-fiber calibration, and the two Use Rules this note inherits.
  #715's own NON-CLAIM ("No chart verification ... for any chart") is
  exactly the line this packet crosses, on one cell.
- **Near-pencil chart** (`bc_near_pencil_chart_reduction.md`): typed at
  toy rows; its next-step ask ("replay at an MCA-route adjacent row
  shape (K = k+1)") is executed here for a different cell at the
  deployed rows themselves.
- **L4 interior chart** (`cap25_v13_bc_l4_interior_chart_to_q.md`):
  the "(b), charge goes to Q" precedent at the L4 fixture; same
  discharge shape, now at deployed scale with the placement computed.
- **Open PRs**: #764 (retained-pair paving, loss-2 bookkeeping,
  thresholds lane), #771 (fixed-deficiency LineRay absorption,
  weighted-RS), #759/#760 (hard inputs 4/2) — cousins, no overlap, no
  block (checked at feasibility, 2026-07-13).
- **Thresholds draft** (856d836): its four proved ray compilers
  (RC_ker, RC_circ, DRC, RC_core) are all vacuous at this cell's
  deployed scale; this cert supplies exact ray payment where they
  cannot reach, feeding hard inputs 1/3 in the draft's vocabulary.

## Self-Red-Team

- *"You typed a cell that the preamble already pays — is that
  content?"*  The placement itself was the open question (the
  feasibility read flagged 'certify the simple-pole chart as a
  saturated-BC chart' as a category error precisely because nothing
  in-tree had COMPUTED where first match puts it at a deployed row).
  The packet's content is the computed placement, the exact typed rows,
  the quantitative non-pencil exclusion, and the extension-headroom
  exclusion — none previously recorded at any deployed row.
- *"The placement could have been presupposed from prop:boundary-q."*
  No: `prop:boundary-q` says the boundary profile is Q; it does not say
  the pole-line words SIT at the boundary profile.  That needs the
  module element (upper) + near-rational dichotomy (lower) + the
  computation confirming zero near-rational slopes and exact `d1 = w+1`
  at every tested word.  An interior placement would have produced a
  different, equally valid certificate.
- *"Two toys cannot type a deployed cell."*  The toys verify the
  MACHINERY (the profile computation and the rank exclusion); the
  deployed typing rests on the scale-free module element, the cited
  dichotomy, and exact deployed integers.  Nothing asymptotic is
  claimed.
- *"The non-pencil lemma is only about ONE pencil; type (a) failure
  needs more?"*  Type (a) per gf L2195 is 'a projective one-parameter
  locator pencil covered by cor:bc-one-pencil' — one pencil.  A
  decomposition into MANY pencils is type (b)'s first clause, and for
  this cell it is exactly what `prop:bc-not-q` proves has no row budget
  without a pencil-count bound.
- *"Is the M31 exclusion excess (0.65 bits) too thin to trust?"*  It is
  an exact integer comparison (`1752700 > 1116025`, excess 636,675),
  computed from `B_B` values that two in-generator routes and a third
  checker route reproduce bit-for-bit.
- *"Would the counting exclusion have been visible at a toy?"*  Not at
  `F_73`: the counting cap does NOT bite there (`13 <= 16 = n - omega +
  1`); it bites at `F_{17^2}` (`40 > 10`) and at both deployed rows
  (Sec. 3).  The counting exclusion is scale-dependent, which is
  exactly why the toys also carry the scale-free rank exclusion
  (witness locators span rank 6 > 2 at both toys) and why the deployed
  statement rests on exact integers, not on toy extrapolation.
- *"Why not bound the cell's slope count and be done?"*  That bound IS
  `prob:row-sharp-q`'s atom target; claiming it would be claiming the Q
  theorem.  This packet routes the charge and quantifies the fit
  conditionally — the same honest shape as the L4 precedent.

## NON-CLAIMS

- **Not a resolution of `prob:saturated-bc`.**  The growing-deficiency
  interior residual (dim `omega-w+1 = 913634/913682`) remains open,
  missing the floor by `~2.07M` bits (budget-fit Sec. 6); its core is
  `prob:band`-hard (Gamma_r route) and no progress on it is claimed or
  implied.
- **No claim `U(a_0+1) <= B*`** at any row, and no unconditional upper
  bound on `max_z |Fib_w(z)|` or on the cell's slope count (that is the
  row-sharp Q atom target).
- The enumerative half is a CITED THEOREM (frontiers bijection + #715
  calibration), not new mathematics.
- No bound at raw-support scale anywhere; the #679/#518 Use Rules are
  honored.
- No edit to upstream `.tex`; the omega typo stays parked via the
  banked `bc_one_pencil_omega` certificate (cited, not re-parked).
- The toy gates pin mechanisms (placement, rank exclusion), not
  asymptotics; the deployed statements are exact integers plus cited
  theorems.

## Reproducibility

```
python3 experimental/scripts/verify_bc_chart_typing.py --emit-defaults  # ~5 s
python3 experimental/scripts/verify_bc_chart_typing.py --check          # ~5 s
python3 experimental/scripts/verify_bc_chart_typing_check.py --check    # ~1 min
```

stdlib only, deterministic (no randomness anywhere), byte-stable
regeneration, no timing or machine data in any frozen output.  The
generator's two deployed big-int routes and the checker's third route
must agree exactly on all four rows for any run to pass.

## Provenance

Base `2633895a66d3edf516120a87b2eb18c994f977ab` (origin/main at the
2026-07-15 packaging re-verification; rebased from `c35a6da` after
upstream's frontier PR wave landed — no pinned or oracle file changed
in `c35a6da..2633895a`, re-verified file-by-file).  Every upstream line
citation in this note was verified against the blobs at base; all
statement pins are line-hashed in the certificate and re-scanned fresh
by the checker.  Oracles consumed read-only: #715
`lineray_census_rerecording.json`, `bc_one_pencil_omega.json`, #690
`envelope_rung_ledger.json` (payload-hash verified);
`saturated_bc_budget_fit_v1.json` (old-style, no payload field:
whole-file sha256 + field equality); #721
`canonical_reduced_rational_host_compiler.md` (no JSON cert in-tree:
whole-file sha256 + content pins + full census replay).  Design
lineage: budget-fit (first packet on the promoted problem; P1/P2 and
the gap ledger) -> #666/#679/#715 (dedup reading and calibration) ->
this packet (first deployed-row chart typing, placement computed).
