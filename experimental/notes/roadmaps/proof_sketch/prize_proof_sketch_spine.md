# Proximity Prize: heuristic proof-sketch spine (NOT RIGOROUS)

- **Status:** CONJECTURAL / SKETCH throughout. This document charts a heuristic
  path from the repo's current proved results to a resolution of the prize
  problem. Nothing here is a claim; every node carries one of the labels
  `PROVED-cited` (points at an existing repo result), `SKETCH` (heuristic
  argument written out), `CONJECTURE` (precise statement, evidence listed),
  `GAP-WALL` (named unknown with a frozen statement elsewhere).
- **Method:** top-down refinement, one node per loop turn, per the r2 roadmap
  §0.1. All arithmetic in this file was machine-checked before commit.
- **Parent:** `../proximity_prize_execution_roadmap_post_v10_r2.md`.

## 1. Targets and the resolution-shape conjecture

**Grand MCA.** For each official rate `rho`, determine the largest
`delta*_C` with `eps_mca(C, delta*_C) <= 2^-128` for the admissible smooth
rows. **Grand List.** Same for `|Lambda(C^{==m}, delta)| <= 2^-128 |F|`.
Adjacent-pin form: `B_C(a0) > B* = floor(q_line/2^128) >= B_C(a0+1)`.

**Conjecture R1 (resolution shape).** For prize-scale rows
(`q_line` near `2^256`) the threshold sits at

```text
delta*_C = 1 - rho - c_rho / log2(q_line) * (1 + o(1)),
```

i.e. capacity minus a reserve of order `1/log q`, with the reserve constant
bracketed by two computations:

```text
rate   first-moment crossover d_fm     Paper D cap        reserve: FM vs cap
1/2    0.496094                        0.498047           2^-8.00  vs 2^-9
1/4    0.746811                        0.748047           2^-8.29  vs 2^-9
1/8    0.872853                        0.873047           2^-8.86  vs 2^-9
1/16   0.936162                        0.936523           2^-9.55  vs 2^-10
```

(log2 q = 256 extreme row; the `128/n` correction is negligible at
`n <= 2^41`.) The cap column is PROVED-cited (Paper D, unsafe above);
the `d_fm` column is the SKETCH prediction below which the aperiodic term
stays under `B*`. Since `d_fm < cap` at every rate, the conjectured-unsafe
region contains the proved-unsafe region, consistently; the true `delta*`
lives in the corridor `[?, cap]` with the sketch pointing at `~ d_fm`.
The two regimes of the theory:

```text
small q_line (B* tiny):   tangent term pins thresholds at HIGH agreement
                          — this is the PROVED F_17^32 506/507 result;
prize-scale q_line:       tangent never reaches B* ~ 2^128; the threshold is
                          decided in the capacity corridor by quotient mass
                          (unsafe side, proved) vs aperiodic first-moment
                          (safe side, THE open half).
```

## 2. The exact counting frame (what is already rigorous)

Fix a pair `(u,v)` and exact agreement `A` (`t = A-k`, `j = n-A`). Locators
of co-supports are squarefree degree-`j` divisors of `X^n - 1`: a FINITE set
of size `C(n,j)` (points in P^j coefficient space). The Hankel pencil is
LINEAR in the slope:

```text
M(Z) l = a + Z b,   a = H_{t,j}(u) l,   b = H_{t,j}(v) l  in  F^t.
```

Hence, per valid locator `l` [SKETCH restatement of a PROVED-cited fact —
the Paper D v8 quotient-support ledger "one support pays for <= 1 slope"]:

```text
b != 0:            at most ONE bad slope Z = -a_r/b_r (consistency required
                   across all t rows);
b = 0, a != 0:     no slope;
b = 0, a = 0:      l explains u and v separately on the SAME support
                   -> the pair is same-support contained there -> EXCLUDED
                   by the noncontainment gate. The degenerate pencil case is
                   exactly the MCA exclusion. [SKETCH; matches the PR #171
                   split-locator gate H(v) l != 0.]
```

So exactly:

```text
B_C(A)  <=  #{ valid locators l : a(l) parallel b(l), b(l) != 0 }   ("aligned"),
```

and the whole safe-side problem is: **how many of the `C(n,j)` divisor-
locators can a worst-case pair align?** Tangent and quotient branches are
the KNOWN alignment mechanisms; `B_ap` is the count of alignments with no
mechanism.

## 3. The first-moment model (the sketch's engine) [SKETCH]

Model the aperiodic stratum as generic: for a locator with no shared
structure with `(u,v)`, the vectors `a, b in F^t` behave as uniform, so
`P[aligned] ~ q^{1-t}`, giving

```text
E[B_ap(A)]  ~  C(n,j) * q^{1-t}          (q = q_line),
unsafe crossover:   log2 C(n,j)  >  t log2 q - 128        (count > B*).
```

For `n -> infty` this is `H(delta) = log2(q) * (1 - delta - rho)`: the
capacity-minus-`1/log q` shape of R1 and the table above. The model is
EXACTLY what `prop:noanchor` says cannot be certified by standard tools —
that is why it is the sketch's engine and the prize's core in one object.

**Consistency checks (all machine-verified, pinned row `q = 17^32`,
`log2 q = 130.799`, `B* = 6`):**

```text
A=506: log2 C(512,6) = 44.5  vs  249*130.8 = 32571  -> FM ~ 0; matches the
       PROVED aperiodic numerator 0 (tangent pays all 7) in the smoke packet.
A=427..385 (M3 window): FM astronomically below B*  -> predicts the window
       closes with tiny aperiodic root counts (fronts alpha/beta should
       succeed, or fail only via PAID structure).
A=265: 506.7 vs 8*130.8+2.6 = 1049 -> FM ~ 2^-542 for the APERIODIC part.
       [CORRECTED turn 5: the raw row has LD_sw(C,265) >= 248 via the
       tangent floor; the open A=265 target is the quotient/tangent-
       STRIPPED slack instance (F1 t=9 / Lambda^aper), and FM predicts
       THAT stripped count is ~ empty — supporting it, no raw-row claim.]
A=261 -> 260: FM crosses B* between t=5 and t=4; the PROVED cap construction
       (quotient mass) gives unsafe at A <= 258. FM-unsafe strictly contains
       proved-unsafe, gap = 2 grid steps. The corridor is real but thin.
```

**Falsifiable predictions this sketch stands or falls on:**

```text
P1: no unpaid aperiodic eliminant root survives in the M3 window
    (front alpha/beta outcomes are paid-or-empty);
P2: the quotient/tangent-stripped A=265 slack instance (F1 t=9 object,
    Lambda^aper) has ~ empty aperiodic count [corrected turn 5: the raw
    row is tangent-unsafe at 265; P2 is a stripped-object prediction];
P3: WP-2.6 rung 1 (A=384, deficiency 1) ends in eliminant-or-paid,
    NOT in an unpaid identically-valid pencil;
P4: any counterexample to alpha/beta factors through quotient or tangent
    structure (i.e. is paid) — an UNPAID collision kills the sketch's
    de-correlation premise and moves delta* strictly below d_fm.
```

## 4. Spine: S0-S9

**S0 — object equality [AUDIT-open].** Repo `B_C(a)` counting = official ABF
`eps_mca` sampler, or a printed bridge. Gate for everything prize-facing;
axes and seeds in WP-0.1. Fork: any inequivalent axis becomes a ledger
column and the sketch's denominators re-print.

**S1 — decomposition [PROVED-in-form].**
`B_C <= B_tan + B_quot + B_ap + B_ext`, deduped (v10 atlas + checker).
Refinement: dedup as checker logic (WP-0.4).

**S2 — paid ledgers exact [mixed].** `B_tan = n - a + 1` on the staircase
range [PROVED-cited #147]; `B_quot` via v10 support/image/gcd-lcm ledgers
[machinery PROVED-accounting, closure per row open]; `B_ext` lower side
exists (extension-pole floor), safe side = S6. Refinement target: a single
"paid mass function" `Paid(A)` computable per row + quotient profile.

**S3 — the aperiodic core [the hard half].**
- S3a regular regime (`delta <= (1-rho)/2`, below Johnson by
  `(1-sqrt(rho))^2/2` — never the prize band): canonical gcd/lcm ledgers +
  fronts alpha (spectral disjointness) and beta (rank-6 boundary). FM
  predicts paid-or-empty (P1). Proving ground only.
- S3b in-band (underdetermined): make the first-moment model rigorous on the
  aperiodic stratum. Sub-path: (i) the alignment frame of §2 [exact];
  (ii) strip quotient-periodic supports — the proved confinement/equivariance
  results say periodic supports = confined slopes = the structured stratum
  [PROVED-cited x1 notes]; (iii) the residual rigidity step: worst-case
  aligned-count over aperiodic locators <= poly(n) * FM. THIS is
  prob:perfiber / conj:B / T2 / the M1 lane in one sentence. [GAP-WALL:
  prop:noanchor forecloses characteristic-zero-anchor / prime-averaging
  methods ("the words being quantified after the prime"); prob:perfiber
  records where the polynomial method, subgroup exponential sums, and
  anticoncentration each terminate — see s3b_iii_3, corrected turn 4.] Candidate mechanisms to refine in
  later turns: Hankel displacement rank (the #170 spectral identities),
  Hooley-Katz odd moments, the BETA_2 monodromy route (M1 instantiation),
  Graver/projection route, and the WP-2.6 divisor-variety/pencil-incidence
  geometry (the moving `d`-plane vs the fixed finite divisor variety).

**S4 — reserve unification [CONJECTURE].** The MCA safe-side condition
`log2 C(n,j) <= t log2 q - 128` and the L1 list-side reserve
`sigma log q >= (1+eps) log C(n,a)` are the SAME entropy budget in two
coordinates. One reserve function should feed both grand challenges.
Evidence: identical shape; the quotient-budget/Q_1 split mirrors
paid/aperiodic. Refinement: exact dictionary + where the 128 bits sit.

**S5 — uniform per-rate theorem [shape].** For each rate: hypotheses
(2^s-domain, characteristic exclusions, quotient profile), conclusion
`a_safe(C) = ceil(n(1 - d_rho))` with `d_rho` from the reserve function;
dither/hypothesis-coverage table per WP-4.4.

**S6 — extension lift [open, bounded].** F-valued witnesses exist below the
naive reserve (extension-pole floor, PROVED-cited); safe side = classify
them under the extension ledger or print bucket tables (WP-6.1). FM version:
extension slopes add `|F|/|B|` scale factors to the denominator — refine.

**S7 — list side [reduces].** L2 codegree reduction [PROVED-cited, Theorems
A/B/C] converts interleaved lists to base fibers at `a` and `2a-k`; the base
input is L1 `ImgFib_U <= n^B` above the reserve [CONJECTURE; concrete open
sub-battle: full-petal sunflower growth]. FM predicts it by the same
entropy count applied to `q_gen`. Never let the reduction claim its input.

**S8 — assembly [engineering].** Compiler: row + quotient profile + packets
-> `a_safe/a_unsafe` vs `B*`; refuses conjectural ledgers outside labeled
conditional mode (WP-7.1). Output for the dossier: per-rate threshold
functions, plus the pinned-row partial as the worked small-q example.

**S9 — negative-resolution branch [first-class].** If P4 fails (an unpaid
alignment mechanism exists in-band), then `delta*` sits strictly below
`d_fm`; the program still RESOLVES the prize by determining the new
mechanism's ledger and re-running S5 with `Paid(A)` enlarged. Determination,
not optimism, is the deliverable.

## 5. Refinement queue (one node per loop turn)

```text
DONE    S3b.iii.1  divisor-variety/pencil-incidence rigidity
                 -> s3b_iii_1_divisor_pencil_incidence.md (R2, SPI wall,
                 WP-2.6 = SPI at dim 1, budget B <= 3 at n = 2^41)
DONE    S3b.iii.2  displacement/spectral exchange-rigidity
                 -> s3b_iii_2_displacement_spectral.md (subgroup Hankel =
                 V^T D V verified; alignment = first-t Fourier vanishing;
                 one-exchange = Cauchy rank-one; Johnson gap lam0-lam1 = n;
                 XR wall frozen; alpha = XR's regular shadow; averaged XR
                 = Hooley-Katz-shaped and plausibly provable)
DONE    S3b.iii.3  fiber rigidity + noanchor ground-truth
                 -> s3b_iii_3_fibers_and_noanchor.md (window correction
                 m=1..t; planted-fiber law verified, tangent = rank-drop
                 common-divisor planes; Conjecture F = parent of
                 prob:perfiber (coordinate planes), fiber(Z) (kernel
                 planes), L1 Q_1; noanchor attribution corrected —
                 mechanisms are fixed-prime tech, crystallization must
                 exceed even moments)
DONE    S2       Paid(A) + refined threshold bracket
                 -> s2_paid_ledger.md (Lemma FM1: the first moment is a
                 THEOREM, toy-verified exactly; quotient zones a/b/c with
                 the norm threshold; crossings ordered quot < FM < cap at
                 every rate; R1' bracket; zone (b) collisions =
                 prob:perfiber at sigma=1 — both sides of the threshold
                 reduce to the collision family; P2 mislabel corrected)
DONE    S3b.ii   strip-periodic
                 -> s3b_ii_strip_periodic.md (periodic strata = C(n/M,j/M)
                 verified; the stratum is an INDEPENDENT SET in the
                 exchange graph, every one-exchange exits, coset-moves =
                 quotient Johnson — dynamics factor through the quotient
                 exactly as the counting does; GAP-1 non-equivariant
                 periodic mass; GAP-2 gcd(n,j)-vs-gcd(n,k) seam;
                 operative R2 stated)
DONE    S4       reserve dictionary
                 -> s4_reserve_dictionary.md (FM crossover = tau* IDENTITY,
                 verified 6 digits all rates — pigeonhole and alignment-FM
                 are one entropy budget; thm:normalform quoted: emca =
                 (1/q)max_t Lambda^NC exact; three t's disambiguated;
                 GAP-2 seam closed via pullback => M | t_denom; 128 bits
                 shift crossover by ~2^-42 only; q_gen-vs-q_line column is
                 the real asymmetry, pinned row generates: ord(17)=32)
DONE    S7       list side
                 -> s7_list_side.md (poly-threshold 1/log n vs prize-gate
                 1/log q distinguished; list-unsafe half at the gate is
                 UNCONDITIONAL via thm:qcore pure counting — crossing
                 window [H/256, H/128] per rate, FARTHER from capacity
                 than the MCA corridor (H vs beta compression) => grand
                 challenge 2's safe side binds first; interleaved budgets
                 re-derived B <= 1.60 worst / 3.20 a-regular; L1 petal
                 battle = Conjecture F fourth appearance)
DONE    S3a      regular window
                 -> s3a_regular_window.md (4515 = capacity not count; FM
                 in-window ~2^-16000 => any alignment is structured; P1
                 refined to P1a/b/c; alpha shift-collision ~2^-116.8;
                 beta ambient-vs-Hankel codim ~29068 => realizability
                 must be forced; window theorem prediction: aperiodic
                 numerator 0 throughout; fiber content invisible in the
                 window — only the deficiency ladder probes Conj F)
DONE    S6       extension lift
                 -> s6_extension_lift.md (B-rational pencils lift free;
                 the pole floor's N(L) ~ L below saturation 2^216 =>
                 B_ext crosses the gate exactly at the S7 list window —
                 the extension mechanism IMPORTS the list threshold into
                 MCA; live only for non-generating rows, which are forced
                 tiny (q_gen < 2^128, doubled reserve); classification
                 conjecture (i) B-rational / (ii) pole / (iii) tower;
                 sigma=1 audit as calibration)
DONE    S5+S0    statements + object axes
                 -> s5_s0_statements_and_object.md (master table verified:
                 list_lo < quot < tau* = list_hi < cap at every rate;
                 per-rate theorem shape with hypothesis block H1-H6;
                 exact-rate rule => 2-power k => quotient structure
                 MAXIMAL; dither latitude would swing ~half the reserve
                 (rules question, F2); projective gate +1 edge case
                 demonstrated; S0 ledger: 3 verified, axes 1/2/4 open
                 definitional audits, 8/9 rules lookups — zero-OPEN gate)
DONE    S8/S9    assembly + negative branches
                 -> s8_s9_assembly_and_negative.md (compiler contract with
                 verdict logic + refusal rule; unconditional coverage =
                 everything up to q ~ 2^128 (n-k)/3, a ~90-bit open band
                 remains; minimal win set = {R2, zone-(b), S0 zero-OPEN}
                 — at bottom ONE collision family + care; consolidated
                 negative-branch table; corridor widths verified
                 2.17/2.00/1.12/1.67 grid steps; low-confidence bet
                 recorded)
DONE    FINAL    coherence pass (turn 13): s2 corridor widths corrected
                 (2.17/2.00/1.12/1.67 grid steps); all cross-file
                 references machine-checked as resolving; labels present
                 in every node; prediction ledger added below.
                 SKETCH COMPLETE — 12 content nodes + spine, turns 1-13.

## 7. Prediction ledger (added turn 13 — what tests the sketch, and where)

| # | prediction | tested by | if it fails |
|---|---|---|---|
| P1a/b | alpha scan: gcd = 1 everywhere, or every collision is paid | WP-2.1 full-grid scan (post-replay) | P1c: unpaid collision = candidate_new_obstruction in the easiest regime; crystallization demoted (S9) |
| P-beta | rank-6 ambient sharpness not Hankel-realizable, or realizable only paid | WP-2.2 realizability search | direction-rank methods insufficient in-window; M5 charts mandatory |
| P2 | the quotient/tangent-STRIPPED A=265 slack instance has ~empty aperiodic count (raw row is tangent-unsafe; corrected turn 5) | F1-lane instance work; agreement-265 status audit | FM wrong at small t; small-t partial XR (the #152 generalization) is the diagnostic |
| P3 | WP-2.6 rung 1 (A=384, d=1) ends eliminant-or-paid, not unpaid-valid-pencil | PR #172 turns (paused loop, resumable) | an unpaid identically-valid pencil at d=1 kills the de-correlation premise early |
| P4 | no unpaid alignment mechanism exists in-band | the whole program; earliest signals: P1c, P3, GAP-1 | delta* strictly below d_fm; determine the new ledger and re-run S5 (S9 posture) |
| window-0 | the M3 window theorem ends with aperiodic numerator 0 throughout 385-426 | the M3/M4/M5 campaign end-state | paid-subtraction bookkeeping or crystallization fails on checkable ground |

## 8. The sketch in one paragraph (added turn 13)

Count aligned locators: finitely many divisor-locators, a pencil linear in
the slope, one slope per locator (v8), containment = pencil degeneracy.
The exact first moment (FM1) makes the aperiodic count's mean a theorem;
tau* (= the FM crossover, verified identical) is the one entropy scale on
both the list and MCA sides. Strip quotient-periodic structure (the
strata are exchange-graph independent sets; dynamics and counting factor
through the same quotient recursion); pay tangent by fibers = common-
divisor planes (Conjecture F, whose coordinate-plane case is the paper's
prob:perfiber). What remains is ONE rigidity statement (R2, reachable via
incidence SPI or exchange XR, poly budget B <= 3) plus the zone-(b)
e_1-collision behavior — together with the S0 conventions audit, these
are the minimal win set. Everything below q ~ 2^128 (n-k)/3 is already
pinned; the prize's open content is a ~90-bit band of field sizes, with
delta* = 1 - rho - c_rho/log2(q_line) and c_rho bracketed in a corridor
~2 grid steps wide. Negative resolutions stay first-class throughout.
        S2       Paid(A) as a single computable function (quotient closure)
        S3b.ii   the strip-periodic step: exact statement of the aperiodic
                 stratum via the proved confinement/equivariance results
        S7       list-side FM + petal-growth sub-battle
        S4       reserve dictionary (MCA <-> L1), where the 128 bits sit
        S3a      alpha/beta heuristic arguments (why FM predicts paid-or-empty)
        S6       extension FM + classification sketch
        S5       per-rate theorem statements with explicit d_rho tables
        S0       object-equality axes (sketch-level; execution in WP-0.1)
        S8/S9    assembly + negative-branch bookkeeping
        FINAL    coherence pass over the whole tree, then flag for review
```

## 6. What would falsify this sketch

An unpaid in-band alignment mechanism (P4); an unpaid alpha/beta collision
(P1); `LD_sw(C,265) = 7` (P2); an unpaid identically-valid pencil at A=384
(P3); or an object-equality failure at S0 that changes denominators. Each
lands in a named branch (S9 or WP failure branches) — the sketch is built to
bend, not break silently.
