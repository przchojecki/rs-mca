# AGENTS.md — RS–MCA Resolution Protocol

> **Updated:** 2026-08-20
> **State snapshot:** `upstream/main@93fba1be3f3299b0ba4708d88715377bbb656e45`
> **Supersedes:** all older priority lists in this file.

Edit this workboard in place. Never append another “current focus”, “highest priority”, or competing task list.

Before starting, compare the snapshot with current `main`, then read the newest entry in `experimental/agents-log.md` and the live four-row completion packet. If the state changed, update the snapshot, authority table, and workboard before doing mathematics.

## 1. Mission and resolution standard

The target is the true numerator

```text
B^MCA_{C,Gamma}(a)
  = maximum, over received lines, of the number of distinct bad slopes.
```

The repository should be driven toward a direct proof or counterexample about this quantity, not toward more summaries, theorem skeletons, or a formally checked unresolved ledger.

Grande Finale v4 is the preferred current completion architecture, but it is not the definition of truth. A uniform direct theorem may bypass it. A counterexample to one proof route need not refute the target inequality.

The primary unresolved official benchmark in the four-row packet is

```text
KoalaBear MCA, target 2^-128:
B^MCA_C(1116048) <= 274980728111395087.
```

Agreement `1116047` is already proved unsafe. Proving the displayed upper bound therefore determines the first safe agreement exactly.


There is also a high-priority list-decoding objective: obtain better ordinary Reed--Solomon list-decoding bounds beyond the Johnson radius. These may come either directly from the list-side machinery in the papers and experimental notes, or indirectly from sufficiently strong CA/MCA upper bounds through the BCHKS25 and CS25 conversions surveyed in `open-proximity.tex` Theorems 5.2 and 5.3. Any such contribution must state the exact code (`C` or `C^+`), radius shifts, list-size bound, field denominator, and whether the result is theorem-level, conditional, or computational.

A result counts as resolution progress only if it does at least one of these:

1. proves or refutes a direct benchmark inequality;
2. replaces a live `null` atom by an independently reviewed exact integer;
3. supplies the missing source-bound architecture/owner bridge;
4. proves exhaustive coverage and the correct slope/codeword projection for a live residual;
5. rigorously removes a live route and updates the residual state; or
6. completes the exact add-back and row certificate.

For a family-level or asymptotic resolution, give a matching upper/lower bracket for the true numerator on a precisely declared family. The identity-profile formula remains an identity-candidate conjecture until witness exhaustion and every payment are proved.

Protocol consumption is downstream and is not a current resolution target.

In this file, `Q` means the pruned locator-prefix maximum-fiber atom; `BC` means the balanced-core distinct-slope atom; and `U_list_int` means the arbitrary-word interior codeword atom. These are ledger names, not assumptions that the corresponding bounds are proved.

## 2. Target correction and current verified state

The nonzero-budget packet contains one official primary MCA row and three auxiliary theorem-building rows:

| Row | Role and target | Unsafe `a0` | Candidate `a+` | `B*` | Full-budget Q multiplier floor | Verdict |
|---|---|---:|---:|---:|---:|---|
| KoalaBear MCA | **primary**, `2^-128` | 1116047 | 1116048 | 274980728111395087 | 4807520 | open |
| KoalaBear list | auxiliary, `2^-128` | 1116046 | 1116047 | 274980728111395087 | 4226236 | open |
| Mersenne-31 MCA | auxiliary, `2^-100` | 1116023 | 1116024 | 16777215 | 9 | open |
| Mersenne-31 list | **analytic stress test**, `2^-100` | 1116022 | 1116023 | 16777215 | 8 | open |

**Do not misstate the target.** For the Mersenne-31 code over `F_(p^4)`, target `2^-128` has integer budget `B*=0`; its complete safe set is empty. The `B*=16777215` Mersenne rows are `2^-100` stress tests, not unresolved `2^-128` Prize rows.

At this snapshot:

- CAP25 v13.2 proves the unsafe endpoints and reusable foundation results.
- Grande Finale v4 proves many local identities, order-32/rational-atom reductions, owner localization, and spread-core incidence bounds, but no adjacent safe row.
- The live compiler returns `ARCHITECTURE_ROUTE_CUT_CURRENT_ARTIFACT_SET`, not `SAFE`.
- Every deployed `U_Q` remains `null`.
- No row has complete active-architecture `U_paid`, exhaustive MCA balanced-core or list-interior payment, zero/exact residual, and chronology-correct add-back.
- The KoalaBear legacy M1 stack records local `U_paid=422354730332` and local remainder `274980305756664755`, but neither is banked in Grande Finale v4 because the source-bound owner/partition bridge is missing.
- Under the latest corrected direct extension charge, positive extension dimension is excluded on Mersenne-31 and dimension at least two is excluded on KoalaBear. These are route cuts, not payments or nonexistence theorems.
- The newly integrated M31 packets add local padding-bridge, masked-saturation, common-core add-back, rank-two/coloop, rooted-shell, C7--C9, and route-cut infrastructure.  These are not adjacent-row payments: source-bound owner/refund, rooted-shell completion, residual projection, and final finite-ledger terminals remain open.
- The integrated M31 rank-seven chain proves master-denominator, split-divisor, one-pivot, and interlaced-source route cuts.  It leaves mixed-`G`, cross-cofactor, deep-fiber, and higher-rank incidence terminals open and moves no deployed row value.
- The integrated M31 post-Johnson conversion contract gives an exact conditional CS25 bridge from a same-radius CA numerator at most `16777214` to the ordinary-list budget `16777215`, and cuts the BCHKS25 route at the deployed budget.  It does not prove the unconditional M31 list row.
- The fixed-`G` endpoint Plotkin theorem proves an ordinary-list cap `2310492` beyond the exact finite-field Johnson radius on two declared M31 endpoint subfamilies.  It is genuine Lane L progress, but not an unrestricted M31 list-row upper bound.
- The direct rate-half cyclic quotient-rotation theorem in `experimental/experiments.tex` proves, for every declared order-`2^41` multiplicative-coset family, an ordinary-list lower bound `ceil(binomial(255,129)/256)` at agreement `1116691496959`, strictly beyond Johnson.  It is a finite-family Lane L lower construction, not an MCA statement or deployed-row closure.
- The July 24--29 PR integration sharpens that rate-half Lane L construction on the declared field `q=3*2^41+1`: the zero-remainder boundary gives a lower endpoint with certified bit length at least `1466604010422`, while interpolation packing gives an upper endpoint with bit length at most `2095944040454`.  This is a finite-family ordinary-list bracket, not a deployed-row theorem.
- On the pinned M31 quotient profile, the proposed rooted-shell cap `1233` is refuted by an explicit deficiency-192 packet of size `1237`; a ragged non-`T16` collision and the signed-`T8` census further cut alignment-only routes.  The canonical-remainder inequality `|F_eta|<=1716*r(eta)+5577` forces at least `9774` represented remainders in any unsafe support fiber, but supplies no received-word or row-list projection.
- The cumulative M31 rank-seven compiler now reaches `Q=147594` locally.  Its adjacent `Q=147595`, `k=4981` survivor is reduced to a varying proper-`G`, zero-excess cross-cofactor incidence terminal requiring an aggregate cap `2157928`; no v4 atom, higher-rank theorem, or row closure follows.
- The KoalaBear equality-wall PR stack proves local normalization, a `Q=6,u=2` geometry reduction, and exclusion of 60 labelled `P3+C3` cases, but retains 405 labelled conic cases and lacks global ownership/add-back.  The separate column-far transverse-secant certificate is per fixed union only.  No large `U_paid` claimed by an abstract candidate-record compiler is banked; the live active value remains `null`.
- The exact adjacent fixed-`G` Hahn relaxation has optimum `20737821.0968...`, above the list target, and its complementarity identity shows the proposed selection-gap hypothesis is target-equivalent.  This cuts the ordinary pairwise-distribution route without proving an unsafe list or moving the M31 row.
- The affine-span transverse MCA compiler `thm:affine-span-mca` is refuted even under its printed direction-separation hypothesis.  An exact `GF(1009)` rank-one family has 31 pair-noncontained bad slopes against the claimed bound 23, with direction agreement `20<m=21`.  The corrected `thm:proper-subspace-mca` replaces its false extension factor, and the lifted-rank dichotomy isolates the full-lift branch.  There `W=C+<r_1>` has `d_1(W)=e` and every higher generalized weight MDS-sharp.  The punctured Johnson and Gram rungs lead to the exact-layer affine-line theorem, which pays every sparse-direction support `e<d`.  Beyond `d`, pair noncontainment caps the total common core of an affine explanation line; triple overlap synchronizes all top-third exact layers onto one global line, so its `N-m+1` cap is charged once.  Extending the exact suffix-minimum prefix with the mean-centered Gram cap, then absorbing one boundary layer by two top anchors and a second layer at residue two by an anchor/missed-set case split, leaves residual intervals `96151<=e<=1044238` on KoalaBear and `98232<=e<=1044241` on Mersenne-31.  At the first Mersenne residual, a normalized-direction Johnson count caps the boundary layer at `1450`; any unsafe family must then put at least `343071` slopes on the synchronized top line and give it a common core of size at least `m-2`.  That core absorbs every assigned pair of deficit at least `30791` into the same line, while the lower explanations form a punctured ordinary list of size at most `26`; the contradiction bound is `3535161<16777215`.  The fixed-cutoff generalization `h_0=65200` prices all intermediate exact layers and pays every Mersenne support through `e=101155`, directly through `101149` and by core absorption for the final six.  At the first wall `e=101156`, switching to `h_0=65258` and using residue two synchronizes both top boundary layers; the zero/one-top cases use an outside-core line cap or disjoint missed sets.  The largest of five exhaustive bounds is `16705799<16777215`.  Beyond that support, retaining every exact-layer direction class as an affine-line slot gives a global line bank; unsafe pigeonhole and total-core absorption pay all `23,649` supports through `e=124805`.  Recursive residual peeling then removes each forced parameterized affine line and either reaches the exact weighted prefix or violates the pairwise `K-1` intersection ceiling for the peeled inside cores.  Exact replay pays another `5,393` supports through `e=130198`, with at most five lines.  Bounding all removed lines jointly from their shared core budget gives a convex endpoint charge and pays 21 further supports through `e=130219`.  Retaining every forced total-core lower bound in that convex maximization pays `e=130220,130221`; both rows terminate after 38 lines with inside-core packing lower bound `142893`.  Splitting each subsequent selected line at actual core `e+10-65450` gives either weighted-prefix core absorption or a capped convex charge.  This pays `e=130222..130225`, with 14 lines on the first two rows and 70 on the last two.  Restoring each selected slot's exact-layer owner gives the inside-core bound `u>=ceil((lambda*h-e)/(lambda-1))`; with the capped-core branch, three lines pay every support `e=130226..130236`.  At adjacent `e=130237`, the bank forces only size-two shift-pair slots with inside core `807`; first-order packing reaches only `65529<e`.  A weight-`(1,5,5)` degree-264 interpolation kernel has dimension at least `938`; the capped bank still forces 2,705 distinct polynomial-pair cores, while two coprime kernel members have at most `52^2=2704` common pairs.  Thus every unsafe survivor forces a positive-`(Y,Z)`-degree common interpolation factor.  The full 7,583-line ledger and cofactor Bezout put at least 4,982 pairs on that factor; their core incidence forces the received pair onto it at least 126,188 times, leaving at most 4,049 inside exceptions.  The Mersenne residual starts at `e=130237`, with this near-total factor's classification open.  The adjacent KoalaBear cap loses its positive mean-centered denominator.  Neither remaining residual is an unsafe certificate.  The ordinary affine-span LIST theorem, common-core cancellation, directional Johnson compiler, gauge equivalence, and the selector-free all-LineRay error-affine-core set-pair theorem are not refuted by the example.
- In the first Mersenne full-lift residual, the degree-one common-factor branch is now an exact `F`-rational projective star.  Polynomial-section parameterization and an ordinary Johnson cap of `802` exclude every nonconstant-coefficient linear factor against the `4982` captured sections.  This identifies the primitive-star shape but does not pay its population; the complementary factor branch has `(Y,Z)` degree at least two.
- The same kernel's 938-dimensional quotient forces the primitive full gcd to have weight-`(1,5,5)` degree at most `217`, hence `(Y,Z)` degree at most `43`.  In the higher-degree branch this improves the factor mass to at least `5083` sections and `126266` inside points, leaving at most `3971` exceptions; reducible gcds remain allowed.
- Base-field descent now removes geometric field-of-definition ambiguity from that branch.  Since the Mersenne characteristic exceeds 43, conjugation and Bezout leave at least `5079` selected pairs on `F(X)`-defined components; one absolutely irreducible base-field component carries at least `132`, while their union has at most `3974` inside exceptions.
- The post-#1165 support-transverse refinement replaces the global final factor `L` by the exact selected-support margin `theta>=L`.  Its arbitrary-rank codeword gauge pays every intrinsic post-near KoalaBear family through affine error rank 9 by `110390969172308040`, with slack `164589758939087047`, conditional only on the separately pinned `2w` near-rational theorem.  At error ranks 10, 11, and 12, an over-budget family yields an actual identical support on which the original direction differs from a reconstructed codeword in at most `12`, `387`, or `12049` coordinates.  This is a direct distinct-slope route cut with zero active-v4 ledger movement; it does not transport first-match owners or close KoalaBear.
- The rank-ten margin/interleaving split now pays the complete direct post-near KoalaBear affine-error-rank-10 branch.  At threshold T=667, the support-transverse high part costs 5143522968716559, the common-support interleaved low part costs 56727790457914040, and the disjoint near add-back costs 134944, for total 61871313426765543 and slack 213109414684629544.  The projection-collapse guard uses the actual sextic line field |F|=2130706433^6.  The same exact one-threshold formula first fails at error rank 11, whose minimum is 1040506078215897711 at T=876; an exact post-near constant-code star proves the per-pair multiplicity factor n-A is sharp.  This moves no active-v4 atom and does not close KoalaBear.
- The raw-low rank-eleven successor closes the direct post-near affine-error-rank-eleven branch, conditional on the separately pinned near-rational deletion.  A weighted projective-line theorem bounds every complete shortened rank-one family by 4070947 slopes.  After separating raw from truncated support margins, fixed cutoffs through ranks 2--10 require at most 248706399341288370 post-near slopes, leaving slack 26274328769971774.  At affine error rank twelve the same single-cutoff mechanism already fails on the initial row: its unique best requirement is 546519697764383119, exceeding the available load by 271538969653122975.  The former 8681730 descendant and 279911 endpoint wall are withdrawn.  This is a direct-branch payment and method route cut with zero active-v4 ledger movement; it does not pay rank twelve or close KoalaBear.
- The post-#1174 all-level audit rules out the full scalar-margin / selected-support first-moment route at affine error rank twelve.  Its sharp abstract relaxation forces at most 120205662451376300 slopes through one coordinate, short of the rank-ten child by 128500736889912070; even granting every selected support all 1116048 core incidences remains short by 102369037220128024.  The actual-line supported-dual compiler identifies the exact local-polynomial gluing quotient.  Its received-pair image has rank zero, one, or two; rank zero is paid by 49106899082787469, with slack 199599500258500901 to the child target, while ranks one and two remain the source-realizable residual.  This is a partial direct-branch payment and maximal route cut with zero active-v4 ledger movement; it does not pay rank twelve or close KoalaBear.
- Grande Finale v4 explicitly supersedes the old v3 `prob:saturated-bc` status: primitive one-pencil MCA BC is proved; higher-dimensional MCA BC remains jointly governed by spread-component, large-owner, and exception routing; and the list-interior clause is governed by row-sharp list completion.  The spread-abundance and `prob:next` statements are intermediate forms, not additional terminal inputs.
- `experimental/proximity_prize_results_v4.tex` is the current compact synthesis of proved partial results.  It is exposition/status guidance, not a replacement proof source for a live atom or adjacent-row closure.
- A schema/hash pass is structural preflight only. The trusted-source registry is empty; parsing a manifest does not prove an atom.

## 3. Document authority

| File | Role |
|---|---|
| `experimental/notes/frontier-adjacent/four_row_exact_completion_compiler_v1.md` and `experimental/data/certificates/four-row-exact-completion-compiler-v1/four_row_exact_completion_compiler_v1.json` | **Live status authority:** current null atoms, route cuts, architecture IDs, exact row arithmetic, and replay contract. |
| `experimental/Conjectures_and_Barriers_RS_MCA_v4_1.tex` | **Direct problem/falsifier authority:** benchmark conjectures, exact compiler requirements, finite barriers, and separation of finite from conjectural asymptotic claims. |
| `experimental/grande_finale.tex` | **Active conditional completion architecture:** proved local theorems, order-32/rational-atom reductions, owner localization, spread-core incidence bounds, and exact completion problems. Hypotheses/problems are not row bounds. |
| `tex/cs25_cap_v13_2.tex` | **Foundation/unsafe authority:** exact unsafe endpoints, field/domain conventions, reductions, and certificate grammar. |
| `RS_MCA_Paving_v9.2.tex` | **Fixed ePrint basis for unconditional paving results:** shortening, MDS circuit, exact finite, exponential-budget, and conditional Sidon-to-flatness results from ePrint 2026/1463. It does not solve the subexponential near-capacity frontier. |
| `experimental/rs_mca_thresholds.tex` | **Exact-regime/exposition source:** staircases, below-half-distance results, syndrome geometry, and examples; not unrestricted near-capacity closure authority. |
| `experimental/experiments.tex` | **Experimental theorem ledger:** integrated direct list constructions, bridge lemmas, provenance, and scoped nonclaims. Each result retains its printed row and status; the file is not a deployed-row closure authority. |
| `experimental/proximity_prize_results_v4.tex` | **Current synthesis/index:** compact map of proved partial Prize results and status-preserving nonclaims. Follow its cited proof sources before banking any theorem or atom. |
| `tex/RS_disproof_v3.tex`, `tex/slackMCA_v4.tex`, `tex/snarks_v5.tex` | Stable background for no-slack obstructions, reserve/quotient theory, and later protocol accounting. |
| `archived/` predecessors | Provenance only. Never bank an archived owner or charge without an explicit source-bound bridge. |

`experimental/agents-log.md` is a coordination record, not proof authority.

## 4. The one live workboard

Work on exactly one item below. Every contribution must name its row, direct target, item ID, quantifier, projection, and exact impact.

### Lane K — close or refute KoalaBear MCA at `2^-128`

#### K0. Freeze one active row contract

Maintain one canonical manifest containing fields, domain, `n`, `k`, target, endpoint convention, challenge denominator, active architecture ID, partition digest, owner order, object `MCA`, unit “distinct bad slopes per received line”, and exact budget. Every candidate atom binds to it.

#### K1. Make existing KoalaBear work bankable

Either:

- prove a source-bound, owner-by-owner bridge from the legacy M1 partition into the active Grande Finale v4 first-match partition, including inherited charge and exhaustive scope; or
- re-prove the useful local payments directly inside the active partition.

Do not add more legacy-local charges unless they independently prove the direct numerator inequality or include this bridge. Matching parameters and similar cell names are not a composition theorem.

#### K2. Prove the exact pruned row-sharp Q atom

Prove one joint maximum over the frozen first-match residual, using the actual domain, attained image, target map, orientation transport, support-to-parameter coalescing, and a uniform received-line quantifier. Output an exact integer `U_Q`.

The factor `4807520` is only a full-budget calibration before other atoms consume reserve. A shell bound, average, lower floor, target value, separately normalized residual, or conditional allocation is not `U_Q`.

#### K3. Pay MCA projection and residual geometry

Produce exhaustive balanced-core coverage in units of distinct affine slopes. The moving-root theorem pays only charts proved to be genuine pencils. A line-by-line decomposition also needs an exact count of relevant lines. Higher-dimensional cores require a proved ray/slope compiler with exact multiplicities.

#### K4. Close algebraic routing and add-back

Pay or eliminate quotient, extension, periodic/descent, rank, padding, common-core, planted, sparse, shortened, interleaved-list, and every other named cell in the same first-match chronology. Prove `U_new=0` or give an exact integer for each survivor.

#### K5. Emit the row certificate

Prove with exact integers

```text
U_total = U_paid + U_Q + U_BC + U_new
        <= 274980728111395087.
```

Replay it with independent implementations and mutation tests. Then state:

```text
first safe agreement       = 1116048
largest safe grid radius   = 981104/2097152
real safe set              = [0, 981105/2097152)
real supremum              = 981105/2097152, not attained
```

A direct uniform proof of `B^MCA_C(1116048)<=B*` may replace K1-K5, but it must still provide independently checkable constants and endpoint conversion.

### Lane M — use Mersenne-31 list at `2^-100` as the tight falsification test

#### M0. Decide the direct inequality

Prove or refute

```text
B^list_C(1116023) <= 16777215.
```

This is a codeword-count statement; the MCA ray compiler is inapplicable.

#### M1. Resolve the binding primitive-fiber/list-interior problem

The full-budget target is only about `8.4152` times the full-slice average, and the true allowance is smaller after other payments. Prove a realized-image, frozen-residual maximum or construct a received word exceeding the budget. Existing one-shell and rooted-shell packets are local reductions, not exhaustive row bounds.

#### M2. Transfer the theorem or record a new floor

If true, isolate exactly what transfers to KoalaBear Q or other list/MCA cells, with field and projection hypotheses explicit. If false, record the witness mechanism, update the benchmark conjecture/lower floor, and remove every invalidated closure route.

Never describe this auxiliary `2^-100` row as an unresolved `2^-128` Prize row.

### Lane L — improve ordinary RS list decoding beyond Johnson

Produce a theorem, conditional theorem, or exact computational certificate giving a better ordinary Reed--Solomon list-size bound at a radius beyond the Johnson radius. This lane is separate from MCA: the output unit is codewords in a Hamming ball around one received word.

The current Mersenne-31 conversion packet supplies only a conditional CS25 bridge and a BCHKS25 route cut.  The fixed-`G` endpoint Plotkin theorem gives the scoped unconditional cap `2310492` beyond Johnson on two endpoint subfamilies.  The rate-half cyclic quotient-rotation theorem gives an exact finite-family lower construction of size `ceil(binomial(255,129)/256)` at agreement `1116691496959`.  Lane L remains open for a broader unconditional upper bound or a matching upper/lower bracket on a precisely declared family.

Valid routes include:

- direct list-side proofs from the locator-prefix, shortening, prefix-fiber, affine-span, rank-flat, or interior-list machinery in `slackMCA_v4.tex`, `RS_MCA_Paving_v9.2.tex`, `tex/cs25_cap_v13_2.tex`, and `experimental/grande_finale.tex`;
- computational certificates for exact finite list-size upper bounds or counterexamples at declared rows;
- indirect derivations from a proved CA/MCA upper bound using `open-proximity.tex` Theorem 5.2 (BCHKS25) or Theorem 5.3 (CS25), with the theorem's radius shift, intrinsic-radius condition, and `C` versus `C^+` code shift printed explicitly.

A useful list-decoding packet must print:

```text
row:                 (F, D, k, n, rho)
object:              ordinary LIST, not MCA
radius/agreement:    exact delta and integer agreement
Johnson comparison:  exact Johnson radius and post-Johnson gap
bound:               exact list-size upper bound, or exact lower counterexample
route:               DIRECT_LIST / BCHKS_CA_TO_LIST / CS_CA_TO_LIST / COMPUTATIONAL
CA_or_MCA_input:     exact epsilon bound if using a conversion
code_shift:          C or C^+ = RS(k+1)
status:              PROVED / CONDITIONAL / EXPERIMENTAL / COUNTEREXAMPLE / AUDIT
```

Do not claim an MCA bad-slope numerator as a list bound. Conversely, if a list lower bound is converted into MCA failure by a simple-pole or deep-point argument, record it under the MCA row as a lower/unsafe result, not as list safety.

### Lane T — cross-row theorems only when they specialize to a live integer

A Sidon/Fourier, entropy, incidence, shortening, or ray theorem belongs here only if it supplies:

- a bankable exact atom in Lane K, L, or M;
- a direct benchmark upper theorem;
- a direct benchmark counterexample; or
- a rigorous route cut that updates the compiler residual.

An `exp(o(n))` bound, unspecified polynomial loss, fixed low moment, heuristic, or theorem skeleton does not decide the few-bit Mersenne margins and does not automatically fit KoalaBear.

## 5. Exact bankability contract

For Grande Finale v4, every bad object enters one declared, non-oracular, witness-exhaustive first-match partition.

```text
MCA:  U_total = U_paid + U_Q + U_BC       + U_new
LIST: U_total = U_paid + U_Q + U_list_int + U_new
```

Every atom shares the same row/target, object, architecture ID, partition digest, owner order, received-line/word quantifier, unit, and source-bound dependencies. Every value is an exact nonnegative integer.

No atom may consume the full budget unless all other atoms are proved zero. Lower bounds, capacities, headrooms, averages, and allocations are not upper payments.

A direct theorem outside the compiler is welcome, but it must state the same row, object, uniform quantifier, unit, and exact target inequality.

Every note, audit, script packet, or PR begins with:

```yaml
workboard_item: K0/K1/K2/K3/K4/K5/M0/M1/M2/T
row: exact row name
object: MCA/LIST/CA/LINE/OTHER
target_epsilon: exact value
agreement: exact integer
B_star: exact integer
direct_statement: exact theorem or inequality
architecture: DIRECT or exact architecture id
partition_digest: required unless DIRECT
atom_or_cell: exact owner/atom, or DIRECT
quantifier: exact maximum/uniform statement
projection_and_unit: slopes/rays/codewords/supports/pairs
claimed_bound: exact integer or symbolic theorem
status: PROVED/CONDITIONAL/CONJECTURAL/EXPERIMENTAL/AUDIT/COUNTEREXAMPLE
impact: ROW_CLOSURE/ROW_COUNTEREXAMPLE/BANKABLE_ATOM/ARCHITECTURE_BRIDGE/ROUTE_CUT/LOCAL_ONLY
falsifier: explicit invalidating condition or witness
replay: commands and source hashes, when computational
```

`PROVED LOCAL` is not automatically `BANKABLE_ATOM`. State the remaining bridge to the row numerator.

## 6. Stop rules

The following do not count by themselves as resolution progress:

```text
new theorem statements without proofs;
Lean stubs, axiomatized global conjectures, or correspondence names;
new survey or “final” paper drafts;
theorem-label maps and clean rewrites;
toy examples not testing a live claim;
random-fiber heuristics or small scans without a lifting theorem;
structural JSON/schema acceptance;
proofs inside an unmapped archived architecture;
a lower construction falling below budget;
a shell, pencil, or chart silently treated as exhaustive;
an asymptotic loss substituted for an exact finite reserve.
```

Do not start protocol accounting, broad end-to-end formalization, or another grand synthesis paper while the direct benchmark and live atoms remain open.

## 7. Audit, replay, and Lean

### Adversarial audits

Test witness exhaustion, first-match chronology, uniformity, attained-image normalization, projection to slopes/codewords, field/orbit/rank/degree multiplicities, owner composition, integer rounding, endpoints, and any local-to-exhaustive jump.

End every audit with exactly one verdict:

```text
NO ISSUE
FIXED
OPEN GAP
COUNTEREXAMPLE_NEW_FLOOR
```

An `OPEN GAP` names the workboard item and smallest missing theorem/integer. A counterexample updates the direct target, compiler residual, or obstruction floor.

### Computational packets

A closing packet includes exact inputs, source labels and hashes, integer-only gates, canonical JSON, human-readable proof summary, an independently written verifier, optimized/non-optimized replay where relevant, mutation tests, and explicit nonclaims. Floating point never decides a gate. A stale source pin is a failed provenance gate.

### Lean policy

Lean verifies frozen mathematics; it is not a substitute for missing mathematics. High-value targets are proved local theorems used by live atoms, first-match/add-back kernels, endpoint/integer conversion, final row certificates, and counterexample correspondence.

A declaration is certified only after the package builds and its statement is manually matched to the proof source. An axiom, `sorry`, theorem target, or skeleton is not a proof or success criterion. Do not formalize Grande Finale v4 “end to end” while its global inputs remain hypotheses.

## 8. Stable invariants

- Keep base/coefficient field, ambient/code field, line field, challenge field, and every denominator distinct unless a theorem transfers them.
- Keep list, CA, support-wise MCA, line decoding, supports, pairs, rays, and affine slopes distinct.
- MCA counts each affine slope once; an enormous support census may represent one slope.
- Use exact integer budgets and closed-ball endpoint conventions.
- Do not use an extension field to pay a base-field image/entropy deficit without a transfer theorem.
- Do not call a residual predicate a payment or a first-match list exhaustive merely because its last cell is “other”.
- Do not merge atoms from different partitions, owner orders, normalizations, or quantifiers.
- Keep Papers A-D stable unless the maintainer requests edits; new work starts in `experimental/`.
- Log every material experimental change in `experimental/agents-log.md`.
- Preserve status labels; never promote conditional, experimental, or local results to proved row statements.

## 9. Minimal reading path and promotion

1. Live four-row compiler note and canonical JSON.
2. Introduction, exact compiler, finite benchmark, and finite-closure problem in `Conjectures_and_Barriers_RS_MCA_v4_1.tex`.
3. Audited-status, finite-Q barrier, and exact-completion sections of `grande_finale.tex`.
4. Exact unsafe-row/certificate sections of `cs25_cap_v13_2.tex`.
5. Main theorem/status sections of root-level `RS_MCA_Paving_v9.2.tex` (ePrint 2026/1463).
6. Only then, row-specific notes and scripts named by the live compiler.
7. Use `rs_mca_thresholds.tex` for solved exact regimes; use archives only for provenance.

Do not begin by reading every historical note. Start from the direct inequality and follow only dependencies that can change its truth or exact bound.

Promote a result only after its direct statement and quantifiers are frozen, dependencies are source-bound, finite specialization is replayed, projection/ownership is audited, status is proved, and the workboard is updated. Close or refute a row before writing the paper that calls it a resolution.

## 10. Definition of done

The primary finite program is done when one of these is checked in and independently audited:

### KoalaBear safe resolution

```text
B^MCA_C(1116047) > 274980728111395087
B^MCA_C(1116048) <= 274980728111395087
```

with the exact half-open safe set and endpoint data from K5.

### KoalaBear counterexample/new floor

An explicit received line has more than `274980728111395087` bad slopes at agreement `1116048`, together with the resulting later unsafe edge or obstruction mechanism.

### Uniform theorem

A proved theorem specializes to the KoalaBear inequality and states exactly whether and how it transfers to the auxiliary list and Mersenne stress rows.

For the broader RS-MCA problem, “done” means a direct, peer-auditable classification of the true numerator or safe set on the declared family, not completion of a chosen ledger, a conditional identity profile, or a formalized conjecture.
