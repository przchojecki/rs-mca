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
A=265: 506.7 vs 8*130.8+2.6 = 1049 -> FM ~ 2^-542; predicts the OPEN
       conjecture LD_sw(C,265) <= 6 is TRUE (aperiodic part ~ empty).
A=261 -> 260: FM crosses B* between t=5 and t=4; the PROVED cap construction
       (quotient mass) gives unsafe at A <= 258. FM-unsafe strictly contains
       proved-unsafe, gap = 2 grid steps. The corridor is real but thin.
```

**Falsifiable predictions this sketch stands or falls on:**

```text
P1: no unpaid aperiodic eliminant root survives in the M3 window
    (front alpha/beta outcomes are paid-or-empty);
P2: LD_sw(C,265) <= 6 for the pinned row (aperiodic ~ empty at t=9);
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
  prop:noanchor forecloses prime-averaging, polynomial method, subgroup
  exponential sums, anticoncentration.] Candidate mechanisms to refine in
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
next -> S3b.iii  rigidity mechanisms: one child file per candidate, starting
                 with the divisor-variety/pencil-incidence geometry (ties to
                 WP-2.6) and the displacement-rank route (#170 identities)
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
