# LineRay dedup census re-recording: the tier-(4) census lemma, restated once on `|LineRay_E|`

**Status: RE-RECORDING / AUDIT — PROVED (free parts, from upstream
ingredients) / MODEL CORRECTION (part (b): strip `C(m',m)`) / MEASURED
(toy gates A--C, incl. the first `F_{p^2}` pole-line toy) / OPEN (the
recorded dedup target itself).** Base `ea4eb07`
(`experimental/cap25_cap_v13_raw.tex` = cap25, 10083 lines;
`experimental/grande_finale.tex` = gf, 2429 lines). **No `.tex`/`.pdf`
edited.**

| item | value |
| --- | --- |
| re-recorded object | the tier-(4) "Main aperiodic effort" census lemma (cap25 L8077), restated once, per line, on the slope/ray-deduplicated pair count `\|LineRay_E(u,v;m)\|` |
| feeds | `prob:saturated-bc` alternative (b) (gf L2191-2204) — the middle object of `prop:line-ray-saturation`'s two-loss chain (gf L1874-1881); NOT a new independent problem |
| model correction | part (b) of `prop:capg-census-floor`: the dedup interior floor strips the per-witness saturation factor `C(m',m)` from `M_B(d_1)` |
| subsumed problems | `prob:capfp-R1`, `prob:capfr1-rank-one-census`, `prob:capg-split-pencil-B`, `prob:capfr1-split-pencil` -> SUBSUMED-INTO-DEDUP-TARGET; `prob:capg-active-BC` by inheritance |
| oracle certificates consumed | `split_pencil_ray_collapse.json` (#666), `r1_rawcount_refutation.json` (#679) — payload-hash-verified, replayed as Gate A |
| certificate | `experimental/data/certificates/lineray-census-rerecording/lineray_census_rerecording.json` |

**Use Rule.** Downstream material must cite the recorded dedup target
below — not `prob:capfp-R1`, `prob:capfr1-rank-one-census`,
`prob:capg-split-pencil-B`, or `prob:capfr1-split-pencil` in raw
(with-multiplicity) form — as the live census input of the tier-(4)
aperiodic chain.  The raw statements survive only as audit objects and
as the floors of `prop:capg-census-floor` (lower side, untouched).  Any
future bound on the recorded target converts into a per-line MCA-bad
slope bound via `N_slopes <= |LineRay_E|` (loss-1, gf L1874-1881) and
feeds `cor:capfr1-Q-R1-closing` / `prop:capfp-closing` unchanged.  This
packet **does not prove** the recorded target: it is a statement
re-recording with proved free parts, one model correction, and gates.

## The re-recorded target (stated once; OPEN)

Let `C = RS[F, D, K]`, `|D| = n`, `q = |F|`, `p = |B|` for a subfield
`B` with `D <= B`, census dimension `K` (`K = k` at the deployed rows),
`w' = m - K`, `omega = n - m`.

> **Recorded target (LineRay dedup census).** For every primitive affine
> line `(u, v)` at normalized-band agreements
> (`prob:capfr1-normalized-band`, cap25 L7639; finite deployed form at
> the `a_0+1` of `cor:capg-adjacent-pairs`), with `E` the residual
> finite slopes after the first-match paid branches of
> `prob:saturated-bc`'s preamble (quotient, boundary-Q, common-support,
> tangent, extension, degree-drop, common-GCD), prove
>
>     |LineRay_E(u,v;m)|  <=  e^{o(n)} * max( 1,
>                              ceil( C(n,m) p^-w' ),
>                              C(n,m) q^-(w'-1) ),
>
> the middle term achieved from below by the non-`B`-rational pole lines
> of `prop:capg-census-floor`(c).  Equivalently, per word `U = u + zv`
> at interior profile `d_1 in [w'+2, floor((n-K+1)/2)]` (boundary
> `d_1 = w'+1` delegated to (Q), `rem:capg-boundary-offbyone` cap25
> L9827-9839), with `m' = K-1+d_1`:
>
>     |Ray(U;m)|  <=  e^{o(n)} * max( 1,
>                      ceil( C(n,m') p^-(d_1-1) ),
>                      C(n,m) q^-(w'-1) ).

The two raw `q`-terms of the subsumed problems coincide: split-pencil's
`C(n,omega) q^{1-w'}` (cap25 L8022 (its `w` = our `w'`), L9850) equals R1's
`C(n,m) q^{-(w'-1)}` (L8281) since `omega = n - m`; one `q`-term
suffices.  The target is stated on the **pair count** `|LineRay_E|`
(gf `def:line-rays` L1857-1865), not on `N_slopes`: the census floor
survives *exactly* at pair level (below), while the slope count carries
the collision correction of `thm:capg-aperiodic-floor` (cap25
L9260 ff.; `rem:capg-subfield-scope`(ii) L9881-9885) — recording the
model on `N_slopes` would attach an `o(1)` collision caveat to the
floor.  `N_slopes` stays on the loss-1 side of the compile-through.

**Why this object.** The tier-(4) work-queue item (cap25 L8077) still
points at the refuted raw census: "Prove the split-pencil census of the
split-pencil reduction `prob:capfr1-split-pencil`.  This would imply the
balanced-core census ..., then R1, then the normalized aperiodic
input."  Under deduplication the three stages collapse into the single
statement above: #666's ray-collapse theorem gives
`#(SPCen/ray-equivalence) = |Ray(U;m)|` at **every** profile
(`split_pencil_ray_collapse.md` L26-29, L67-70), summed over slopes
`= |LineRay_E|`; #679's identity gives raw `#R1` = the
with-multiplicity LineRay census (`experimental/notes/audits/r1_rawcount_refutation.md`
L133-146).  The maintainer's own prose pre-authorizes the dedup
reading — `prob:saturated-bc` demands per-chart "its own slope, not
raw-support, bound" (gf L2195) and demotes the raw census to "only an
audit object" (gf L2197); the gf Conclusion states "the raw BC support
count is replaced by exact saturation and line-ray identities" (gf
L2339) — but nothing upstream prints the deduplicated count as a
quantified census model (`split_pencil_ray_collapse.md` L72-75).  This
note records it.

## Part (b) is a model correction, not a free transfer

`prop:capg-census-floor`(b) (cap25 L9743-9755, proof L9784-9803) builds
the interior floor as ray-count times same-ray multiplicity:
each member `M'` of the level-`m'` fiber yields a codeword `c_{M'}`
agreeing "on exactly the `m'` points of `M'`, and distinct `M'` give
distinct codewords" (L9794-9797) — those are **distinct rays** — and
"Each such codeword contributes `\binom{m'}m` valid size-`m` supports"
(L9797-9799) — that is per-witness saturation, i.e. exactly loss-2 of
gf L1874-1881.  Under the dedup reading the `C(m',m)` factor must be
**stripped**: the interior dedup floor is the fiber cardinality

    ceil( C(n,m') p^-(d_1-1) )      (m' = K-1+d_1),

not `M_B(d_1) = C(m',m) * ceil(C(n,m') p^-(d_1-1))`.  At the boundary
`d_1 = w'+1` (`m' = m`) the stripped form reproduces part (a)'s
`ceil(C(n,m) p^-w')` verbatim.  For `m' > n/2` (deployed
`m/n ~ 0.532`) the stripped term strictly decreases in `d_1`, so the
per-line middle term `ceil(C(n,m) p^-w')` dominates the interior terms.
Exact recompute at the paper's orientation rows (`(K,m) = (k,1116046)`
KoalaBear, `(k,1116022)` Mersenne-31; Gate B, generator `deployed`
section; all paper-printed values reproduced to their printed
precision):

| row | boundary floor | raw `M_B` bits (paper prints) | stripped dedup floor |
| --- | --- | --- | --- |
| KB, `d_1=w'+2` | 2^67.0958 ("67.1") | 2^56.0111 ("56.0") | `65065153468` = 2^35.9212 |
| KB, `d_1=w'+3` | | 2^43.9265 ("43.9") | `27` = 2^4.7549 |
| KB, `d_1=w'+4` | | 2^31.2569 ("31.3") | `1` (collapsed into `max(1, .)`) |
| M31, `d_1=w'+2` | 2^52.1129 ("52.1") | 2^41.0169 ("41.0") | `1993678` = 2^20.9270 |
| M31, `d_1=w'+3` | | 2^28.9210 ("28.9") | `1` (collapsed) |
| M31, `d_1=w'+4` | | 2^16.2401 ("16.2") | `1` (collapsed) |

(The paper's printed `d_1 = w'+3, w'+4` values are the un-ceiled
products; both forms are recomputed and displayed in the certificate.)
The KB stripped first-interior value `65065153468` equals the #679
certificate's `deployed.budget.corrected_middle_ceil` exactly (asserted
in Gate B), and the four stripped/witness-scale displays `35.9212`,
`35.7352`, `20.9270`, `20.7411` reproduce all four `B_B(a+)` floors of
the budget-fit fixture (`cap25_v13_saturated_bc_budget_fit.md`,
Sec. "Margins" table) — the list-row floors at depth `w'`, the MCA-row
floors at the witness-fiber depth `w'-1` (next section).  Toy pin (Gate
B, `F_73`, `n=24, K=12, m=15`): at the heaviest level-16 prefix word
(`d_1 = 5`), RAW census `48 = C(16,15) * 3` with exactly `3` rays, every
ray at agreement exactly `16` — the stripping identity
`RAW = C(m',m) * RAYS` holds exactly with zero extras; at `d_1 = 6`,
RAW `418 = C(17,15) * 3 + 10` — the three level-`17` rays carry
`C(17,15) = 136` supports each and ten extra rays sit at agreement
exactly `15` (they add `1` each to both sides of the saturation
identity; extras are reported, not assumed absent).

## Parts (a) and (c) survive verbatim — at pair level

**(a) Boundary, free.** The floor is stated on
`Cen(U_z;m) = |Phi_{m,w'}^{-1}(z)|` and its witnesses are distinct-ray,
one support per ray: `prop:capff1-witness-exact` (cap25 L7126-7132)
gives "the list size equals the fiber size exactly; moreover no
codeword agrees with `U_z` on more than `m` points".  Agreement exactly
`m` makes every saturation factor `C(m,m) = 1`: loss-2 vanishes
identically, `Cen(U_z;m) = |Ray(U_z;m)|`, and the boundary numbers
(67.1 / 52.1 bits) transfer to the dedup form unchanged.  Toy pin
(Gate B): heaviest depth-3 prefix word at `F_73` has
`RAW = RAYS = LIST = 13 >= ceil(C(24,15) 73^-3) = 4`, every ray at
agreement exactly `15`, `d_1 = w'+1 = 4`.

**(c) Pole lines, free — but by ray-distinctness, not by "distinct
slopes".** The proof text of (c) says each fiber member `T` "carries
the single close slope `zeta_T = U_{z*}(alpha) - Lambda_T(alpha)`" and
that "distinct `T` are distinct supports" (L9804-9816) — supports,
never slopes.  Slopes provably collide at a fixed `alpha`
(`thm:capg-aperiodic-floor`'s collision count;
`rem:capg-subfield-scope`(ii): the slope and support counts agree only
"to within the collision correction"; gf separates
`prop:rank-one-floor` L1523 from `prop:rank-one-distinct-slope-floor`
L1546, which loses `C(N,2)(K-1)/(q-|B|)` after averaging).  The correct
free proof of verbatim survival is **pair-distinctness**: by
`lem:capg-witness`(i) (cap25 L9183-9205) every threshold-`m`
explanation on the pole line forces `|S| = m` exactly, so two distinct
supports with the same `(zeta, c)` would make `c` agree on `> m`
points — impossible.  Hence `T |-> (zeta_T, c_T)` is injective,
agreement is exactly `m` (loss-2 = 0), and

    |LineRay_E(f_alpha, g_alpha; m)|  >=  |Fib_{w'}(z*)|
                                      >=  ceil( C(n,m) p^-w' )

at every `alpha` not in `D u B` — the same constant as (c), stronger
than the slope floor, with loss-1 exactly the priced collision
correction.  Two sentences of the integrated #679 packet carry the
support-level overclaim and are corrected here while keeping the (true)
survival conclusion: `r1_rawcount_refutation.md` L114-115 ("each fiber
member of the pole line carries its own slope") and L171-172 ("their
supports each carry distinct slopes") must be read as "each fiber
member carries its own distinct **(slope, codeword) ray**".  Gate C
exhibits the witnessed slope collision: at `F_{17^2}` the pole line has
`|LineRay| = 40` at every tested `alpha` but `N_slopes = 39 < 40` at
`alpha = 18` (204 of the 272 admissible `alpha` carry at least one
collision; min `N_slopes = 35`).

**Witness-fiber calibration (precision, build finding; cert field `recorded_target.witness_fiber_calibration`).** At census
dimension `K` the exact witness set of the pole line is the
depth-`(w'-1)` fiber, not the depth-`w'` fiber: `rem:capg-witnessrel`
(cap25 L9246-9258) is the one-dimension-up bijection
`c |-> (X-alpha)c + zeta` from degree-`<K` line explanations to
`RS[F,D,K+1]`-explanations of `U_{z*}`, i.e. `lem:capg-witness` applies
with its `k := K`, fiber depth `m - K - 1 = w'-1`.  Consequently, at
the pole line of `U_{z*}`,

    #R1  =  |LineRay|  =  |Fib_{w'-1}(pi_{w'-1}(z*))|
         ~  ceil( C(n,m) p^-(w'-1) ),

a factor `<= p` above the recorded middle term — absorbed by the
`e^{o(n)}` slack along fixed-rate rows (when the `p`-term is alive,
`p^{w'} <= C(n,m) <= 2^n` forces `log2 p <= n/w'`, `~ 31` deployed),
but decisive for the **finite** deployed form: the finite middle term
must be pinned at the witness-fiber scale `ceil(C(n,m) p^-(w'-1))` of
its row convention.  The budget-fit fixture's MCA-row floors
(`B_B(a+) = 2^35.7352` KB, `2^20.7411` M31) already sit exactly at this
scale (Gate B asserts the displays), so no deployed arithmetic changes.
Toy pin (Gate C): `|LineRay| = |Fib_2| = 40` against the depth-3 floor
`|Fib_3(z*)| = 5 >= ceil(C(16,9) 17^-3) = 3` — floor verbatim, exact
value one depth up.

## Compile-through corollary (proved, free)

For every line `(u,v)` at threshold `m > n/2` with `E` its residual
finite slopes: if some `m`-support is common, `N_MCA-bad = 0`
(`thm:capfp-slope-elim`(b), cap25 L8262); otherwise every MCA-bad slope
is close, hence has an explaining codeword with `s_{z,c} >= m`, hence
lies in the slope projection of `LineRay_E`, so

    N_MCA-bad(u,v;m)  <=  |{z in E : exists c, (z,c) in LineRay_E}|
                      <=  |LineRay_E(u,v;m)|        (gf L1874-1881).

Therefore any bound on the recorded target is a per-line MCA-bad-slope
bound, and — through `thm:capfp-slope-elim`, `cor:capfr1-balanced-line`'s
"+1" near-rational slope (cap25 L7940-7948), and the first-match paid
compilers — it supplies the `U_A`/`U_R1` numerator of
`cor:capfr1-Q-R1-closing` (L7829-7835) / `prop:capfp-closing` (L8525)
**unchanged**: the same compile-through that
`prob:capg-split-pencil-B` itself claims for its corrected models
(L9863-9868, "the implication chain of
`cor:capfr1-terminal-package`,`prop:capfp-closing` is unchanged").
This promotes #666's compile-through remark
(`split_pencil_ray_collapse.md` L97-99) from prose to a stated
corollary.  Unlike the refuted raw `#R1`, the dedup numerator is immune
to the #679 plant: at the planted toy line, `|LineRay| = 206` vs raw
`#R1 = 15709`.

## Chain restoration

`prob:band` (cap25 L4624-4630) counts **slopes** — "the number of
MCA-bad finite slopes of any received line".  It is refuted as stated
and re-pointed by `rem:capg-band` (L9397-9428): item (i) makes
`prob:capfr1-normalized-band` (L7639) the operative band input "by
necessity rather than by convention"; item (ii) (L9415-9419) re-reads
every citation inside the conditional theorems and closing statements.
The dedup re-recording **restores** the chain to the object
`prob:band` always counted: slopes, reached through
`N_slopes <= |LineRay_E|` rather than through the raw support census
that #518/#679 refuted.  The tier-(4) chain (split-pencil ->
balanced-core -> R1 -> normalized aperiodic input, L8077) is realized
by the single recorded target; refuting the recorded target refutes
R1's dedup form, so the strategic-conclusion dichotomy (L8100, "a
super-polynomial primitive split-pencil family, refuting
`prob:capfr1-split-pencil` and hence R1") is preserved with
"split-pencil family" read at ray level — a counterexample still cannot
fail silently.

## Subsumption grades

All five gradings leave the raw statements in place upstream (this
packet edits no `.tex`); they record how each problem's content is
carried by the recorded target.

- **`prob:capfp-R1` (L8278) — SUBSUMED-INTO-DEDUP-TARGET.** Raw form
  refuted by #679 (planted line, factor `>= 2^2015046` over the
  corrected model at the deployed KB census row; certificate
  `r1_rawcount_refutation.json`); the identity `#R1` =
  with-multiplicity LineRay census makes the recorded target its unique
  repair.  `thm:capfp-slope-elim`(c)'s `N_MCA-bad <= #R1` remains true
  but is superseded by the tighter `N_slopes <= |LineRay_E|` (loss-1).
  The "Known unconditional strata" sentence (L8283: `B`-rational
  confinement, deficiency-one SPI) transfers verbatim — both are
  slope-level facts.  No in-tree consumer uses the raw form as an
  input (checked: label-pin lists and survey grades only); the one live
  re-pointing is the budget-fit note, below.
- **`prob:capfr1-rank-one-census` (L7819) — SUBSUMED-INTO-DEDUP-TARGET,
  resolving #679's REFUTED-WITH-AMBIGUITY-FOOTNOTE.** The footnote
  (`r1_rawcount_refutation.md` L148-155) hinged on "all paid cells" not
  being a closed printed list.  The re-recording makes the ambiguity
  moot: on the printed-cell reading the raw statement is refuted
  (#679); on any unprinted reading that pays the plant, the added cell
  is precisely ray-deduplication — i.e. the statement's content becomes
  the recorded target.  Either way the raw form has no independent
  content left.  Its direct consumer `cor:capfr1-Q-R1-closing` (L7829)
  compiles through via loss-1.
- **`prob:capg-split-pencil-B` (L9841-9871) —
  SUBSUMED-INTO-DEDUP-TARGET.** Raw form refuted at interior profiles
  by #518 (factor `>= 2^2015057` vs the +3.3/+22.2-bit margins of
  `cor:capg-adjacent-pairs`; certificate
  `capg_split_pencil_refutation.json`); its mutatis-mutandis R1 clause
  (L9860-9863) refuted by #679.  #666 proved its dedup quotient IS
  `|Ray(U;m)|` at every profile, with the base-field term stripped to
  `ceil(C(n,m') p^-(d_1-1))` per the part-(b) correction above.
- **`prob:capfr1-split-pencil` (L8012) — SUBSUMED-INTO-DEDUP-TARGET.**
  Already conceded superseded upstream twice over
  (`rem:capfr1-split-pencil-active-reading` L8028-8035: "a proof
  reduction, not the final census scale";
  `rem:capg-boundary-offbyone`'s boundary/interior split); the raw
  interior form falls to #518's mechanism, and the challenge-field
  model was conceded refuted at `sec:capg-subfield`'s preamble
  (L9721-9723: "As stated, all three problems are therefore refuted").
  As the label the tier-(4) item L8077 and the closing sentence L8100
  cite, its chain position is taken over by the recorded target as
  stated under "Chain restoration".
- **`prob:capg-active-BC` (L9919-9924) — SUBSUMED by inheritance.** It
  asks to "prove the base-field-normalized census of
  `prob:capg-split-pencil-B`"; #518 proved the hypothesis of
  `prop:capg-final-active-package` (L9934 ff.) "unsatisfiable as
  stated" (`capg_split_pencil_refutation.md` L10-13).  The re-recording
  is what makes that package's BC input **satisfiable again**: the
  base-field-normalized census now exists in recorded, unrefuted (open)
  form.
- *Siblings (one line each, same mechanism):* `prob:capfp-split`
  (L8433 — its "Internal structure, fully proved" ray paragraph is
  #666's ingredient), `prob:capfp-balanced` (L8380), and
  `prob:capfr1-balanced-core` (L7960) are subsumed identically via
  #666's profile-independence; no separate grading content.

**Floors are unaffected.** `capg_split_pencil_b_floor.md` (lower side)
and the Lean floor upgrade note realize `M_B(d_1)` as a raw-census
floor: raw-census floors remain true statements about the raw
(audit) object; their dedup forms are the stripped `ceil` terms above.
The `m1` floor notes are lower-side and survive as audit objects.

**Budget-fit re-pointing (the one live consumer).**
`cap25_v13_saturated_bc_budget_fit.md` Sec. 5 records "The missing
lemma, verbatim" in raw form, and its slope refinement routes through
raw `#R1` (`N_slopes <= #R1 <= e^{o(n)} max(1, C(n,m)p^-w,
C(n,m)q^-(w-1))`) — the second inequality is exactly what #679 refuted.
Those displays are superseded by the recorded target; the note's margin
identity, P1/P2, and its finite target (BC-fin) — stated on `N_slopes`
— are untouched.  No arithmetic changes anywhere (its `B_B(a+)` floors
coincide with the stripped/witness-scale values, asserted in Gate B).

## The #666-withheld item, discharged

`split_pencil_ray_collapse.md` L158-160 withheld: "A separate
observation that its corrected model may inherit the raw-count trap is
deliberately withheld pending its own verification; it is not asserted
here."  #679 is that verification: it refutes `prob:capfp-R1`
*including* the corrected mutatis-mutandis model
(`r1_rawcount_refutation.md` L7, L29-32), with the verdict banked as
exact integer facts (`margins_bits.planted_R1_vs_corrected = 2015046`,
`corrected_middle_ceil = 65065153468`, per-row
`corrected_holds_raw = false` / `corrected_holds_lineray = true`).  The
inheritance is now **asserted as verified**, citing both packets; no
residual check is needed beyond this citation wiring.  The one honest
residual — both integrated toys were `p = q`, so no in-tree toy had
ever exercised the `p`-term and the one-ray plant on the same census —
is closed by Gate C.

## Verification

`experimental/scripts/verify_lineray_census_rerecording.py`
(`--emit-defaults` / `--check`) + independent no-import checker
`verify_lineray_census_rerecording_check.py` (`--check`).  Exact
arithmetic only; stdlib only; deterministic; no timing or machine data
in any frozen output.

- **Gate A (oracle replay).** Both sibling certificates are consumed by
  repo-relative path (the #690 pattern), payload-self-hash verified,
  and their banked per-slope/per-ray data replayed: #666 — 11/11
  in-scope words with `RAYS == LIST` and `RAW == sum C(agr,m)`; #679 —
  per line, `sum_z mult(z) == #R1`, per-slope `mult(z) == sum_c
  C(agr,m)`, `lineray == sum_z #rays(z)` (206/210/211/218), loss-2
  `== #R1 - lineray` (15503/3905/905/0), loss-1 `N_slopes <= lineray`
  (72/69/70/68), and the recorded per-line dedup model **HOLDS at every
  menu line including the plants** (`<= max(1, ceil = 4, 245.36)`),
  upgrading #679's evidence-only comparison into the recorded target's
  own gate.
- **Gate B (part (a)/(b) survival + deployed).** `F_73` (`n=24, K=12,
  m=15, w'=3`): boundary word `RAW == RAYS == LIST == 13 >= 4`, all
  agreements exactly `15`, `d_1 = 4`; interior `d_1 = 5`:
  `RAW = 48 = C(16,15) * RAYS`, `RAYS = 3 >= 1`, all agreements exactly
  `16`, zero extras; interior `d_1 = 6`: `RAW = 418 = C(17,15)*3 + 10`,
  three level-`17` rays plus ten agreement-`15` extras (reported),
  `d_1 = 6` verified by two routes.  Deployed: the table above,
  all eight paper-printed values reproduced, stripped floors exact,
  `65065153468` == #679's `corrected_middle_ceil`, budget-fit `B_B`
  display cross-links asserted.
- **Gate C (the new `F_{p^2}` toy, `p = 17, q = 289`, `t^2 = 3`;
  `n = 16` on `D = F_17^*`, `K = 6, m = 9, w' = 3`).** The `p`-term and
  `q`-term separate: `ceil(C(16,9) 17^-3) = 3 > 1 >
  C(16,9) 289^-2 ~ 0.137`.  Pole line of the heaviest depth-3 prefix
  word (`|Fib_3(z*)| = 5 >= 3`): at every tested
  `alpha in {17, 18, 288}`, full-scan `#R1 == |LineRay| ==
  |Fib_2(pi(z*))| == 40`, every ray at agreement exactly `9`,
  `common == beta-zero == 0`, floor `40 >= 5 >= 3` — part (c) verbatim
  at pair level, witness-fiber calibration pinned; slope collision
  witnessed (`N_slopes = 39 < 40` at `alpha = 18`; 204/272 collision
  `alpha`; min 35).  Planted near-codeword line (`e = w'+2 = 5`,
  `d_1 = e` verified by two routes, single interior profile
  `floor((n-K+1)/2) = 5`): raw `#R1 = 55 = C(11,9)` **FAILS** the
  corrected raw model (`max(1, 2.33, 0.137)`) and the literal `q`-scale
  model (`= 1`), while the dedup count `|LineRay| = 1` **HOLDS** the
  recorded model (`<= 3`) **with the `p`-term alive and binding** — the
  first in-tree toy separating the two terms.  Random control line:
  `#R1 = 0`, everything HOLDS.
- **Gate D (pins).** All statement pins re-hashed at build (cap25
  L8278 / 7819 / 9842 / 8012 / 8077 / 9919 / 9728 / 9874 and the
  witness-lemma block L9183 / 9246 / 9397 / 9828 / 7639; gf L1857 /
  1867 / 2191), 16-hex line hashes recorded, expected line numbers
  asserted; the checker re-scans them fresh.

## Self-Red-Team

- *"Isn't this just #666 again?"*  No.  #666 proved the identity
  (dedup census = list count) and deferred: no quantified model, no
  target recorded ("never printed upstream as a count").  This packet
  records the target with its model, corrects part (b), grades the five
  problems, and wires the chain.  The overlap is by design: the
  identity is the reason the re-recording is possible.
- *"Does this collide with #666's retirement of
  `prob:capg-split-pencil-B` / `prob:capg-active-BC` as independent
  problems?"*  No: the recorded target is framed as the tier-(4) census
  lemma **feeding** `prob:saturated-bc` alternative (b) — the middle
  object of the gf L1874-1881 chain — not as a new independent problem.
  Greps at base: `LineRay` occurs in exactly three notes, none of which
  states a quantified dedup census target; open PRs #699-#712 are
  unrelated (#705's "dedup by reflection" is a comb-trade census; #706
  names a C8 cell in an atlas print audit).
- *"A toy at `n = 16` or `n = 24` cannot prove an `e^{o(n)}`
  statement."*  Correct and not attempted: every gate is a floor,
  identity, or model-comparison at frozen words; the recorded target
  stays OPEN.
- *"Why state the model on pairs instead of slopes?"*  The floor bites
  exactly on pairs (`lem:capg-witness`(i) rigidity); on slopes it
  inherits the collision correction — Gate C exhibits a real collision
  (`39 < 40`), so a slope-form floor claim would simply be false at
  fixed `alpha`.
- *"The middle term is `p` below the pole line's actual dedup census."*
  Yes — the witness-fiber calibration above: the exact witness set is
  the depth-`(w'-1)` fiber (`rem:capg-witnessrel`), factor `<= p`
  absorbed by `e^{o(n)}` along fixed-rate rows; the finite middle term
  must be pinned at witness-fiber scale, where the budget-fit fixture
  already sits.  The recorded floor claim uses only `>=`, which is
  verbatim true (Gate C: `40 >= 5 >= 3`).
- *"Part (b) presented as 'free survival' would be an overclaim."*  It
  is presented as a **correction**: the `C(m',m)` factor is loss-2 mass
  by the proof's own construction (L9794-9801), and the deployed
  stripped floors are recomputed exactly (35.9 -> 4.8 -> collapsed at
  KB; 20.9 -> collapsed at M31).
- *"Maybe an unprinted paid cell already excludes the #679 plant, so R1
  needs no re-recording."*  That reading is graded, not dodged: any
  cell that pays the plant is ray-deduplication itself, i.e. the
  recorded target — the ambiguity footnote resolves either way.
- *"Does the `F_{p^2}` toy's domain-in-subfield setup bias the plant?"*
  The plant construction is #679's verbatim recipe transplanted
  (`U = c0 + eta`, `e = w'+2`, `u := U - z0 v`), with the deterministic
  first-attempt hygiene playing the role of the deployed union-bound
  existence argument; at `q = 289` the hygiene bound is not certified
  below 1, so the generator searches deterministically and freezes the
  first `v` realizing it (attempt index recorded).  The pole-line gates
  use no randomness at all.

## NON-CLAIMS

- **The recorded target is OPEN.**  No upper bound is proved on
  `|LineRay_E|` or `|Ray(U;m)|` beyond the floors already proved
  upstream; the open core is unchanged and is the prize frontier
  (exact list-size control below the Johnson radius at the deployed
  rows).
- No refutation of anything: this packet is a statement re-recording
  (verdict NO ISSUE), not a counterexample.
- No chart verification for `prob:saturated-bc`'s alternatives (a)/(b)
  for any chart; no progress on `R_post <= 16 n^3`.
- The aperiodic core (Q, quotient/prefix flatness, shift-pairs) is
  untouched; nothing here bears on `prob:capg-active-Q` or
  `prob:capg-active-shiftpairs`.
- No claim that upstream text is edited or must be edited; the grades
  are recorded here, in `experimental/`, only.
- The toy gates pin mechanisms and identities, not asymptotics; the
  deployed recomputes are orientation arithmetic, not new bounds.

## Reproducibility

```
python3 experimental/scripts/verify_lineray_census_rerecording.py --emit-defaults   # ~15 s
python3 experimental/scripts/verify_lineray_census_rerecording.py --check           # ~15 s
python3 experimental/scripts/verify_lineray_census_rerecording_check.py --check     # ~1 min
```

stdlib only, deterministic (seed 20260712; the `F_{p^2}` menu — words,
planted codeword coefficients, error positions, `z0 = 18`, attempt
index — is frozen in the certificate), byte-stable regeneration, no
timing or machine data in any frozen output.

## Provenance

Base `ea4eb0784417ca5ab503a3c31a7eef6464ad100a` (origin/main at build).
All statement pins are line-hashed in the certificate and re-scanned by
the checker; every upstream line citation in this note was verified
against the blobs at base.  Design lineage: #518 (raw split-pencil
census refuted at interior profiles; profile-localization lemma) ->
#666 (ray collapse: dedup census = list count at every profile) -> #679
(raw R1 refuted incl. corrected model; `#R1` = with-multiplicity
LineRay census) -> this packet (the re-recording those three make
possible and the maintainer's own prose pre-authorizes).  Oracle
certificates consumed read-only with payload-hash verification;
their `payload_sha256` values are frozen in this packet's certificate.
