# Routing exhaustiveness on the printed first-match order

## Status

`ROUTING ORDER EXTRACTED (AUDIT) / DETECTABILITY TABLE (AUDIT+PROVED) /
DETECTION EXHAUSTIVE = THEOREM (PROVED) / RANK CERTIFICATE INERT ON PARABOLA
(PROVED) / RUNG-3 UNACCOUNTED-MASS HOLE REFUTED (PROVED-negative) /
RESIDUAL = PROJECTION-DEGREE PAYMENT (OPEN, = #626, unchanged)`.

The final step of the span-face arc. It decides whether the frontiers paper's
**printed** first-match routing order (`asymptotic_rs_mca_frontiers.tex`
**L5180--5183**) fires a pre-primitive trigger on every `(S_E)`-violating
product profile — and, critically, whether that trigger is **decidable from the
data the router has at routing time** (the profile occupancy combinatorics) or
secretly needs the spectral quantities (`G_1`, `Q_img`, `E`) known only
post-hoc. The detectability distinction is where the C7 enumerative input
originally hid; this packet makes it a precise table and reads the printed
accounting against the two violator classes.

Every number below is recomputed by
`experimental/scripts/verify_routing_exhaustiveness.py` (stdlib-only, zero-arg,
`RESULT: PASS (3417/3417)`, ~0.2 s under `ulimit -v 2097152`).

Label key: **PROVED** (hand derivation, exact), **MEASURED** (exact finite toy,
asymptotics not proved from the toy), **AUDIT** (interface reading of the tex or
a sibling note), **WALL** (identified obstruction), **OPEN**.

**Credit.** The block-parabola family and the `(CF*)` identities are
**avdeevvadim's** (PR #558, integrated at `e190193`). The depth-`w` prefix-fibre
atlas is our **#536** (`atlas_missing_witness.md`); the finding that the C7
collapse routing is an **assumed enumerative input, not a theorem** is our
**#539** (`fi_full_image_primitive.md`); the Gap-2 span-collapse `=>` C5
classification (vacuous on admissible, `w<char`) is our **#545**
(`gap2_collapse_routing.md`); the J2 magnitude-blindness impossibility is our
**#609** (`frame_image_completion.md`); the master identity `L>=A_eff/(1+E)` and
the supplement `(S_E)` are our **#614** (`minimal_phase_supplement.md`); the
`(S_E)`-on-admissible-leaves stratification and multiplicativity **T3** are our
**#622** (`se_on_admissible_leaves.md`); **MASTER-2** and the two-cell partition
are our **#625** (`c7_routing_spectrum.md`); and the binomial-tail
projection-degree count is our **#626** (`c7_degree_enumeration.md`). This packet
consumes all of them and adds the **routing-order detectability analysis** — the
one thing the arc had not yet done: read the *printed order* itself, cell by
cell, and separate what the router *decides* from what it *pays*.

---

## HEADLINE (read first): detection is a THEOREM, payment is the (old) residual,
## and the suspected rung-3 hole does not exist

The routing conjecture of #622/#625 (*routing = spectrum*: every `(S_E)`-violator
is caught before the primitive step) **splits cleanly along the detectability
line**, and the split is already **printed in the tex**:

> "**Payment is an enumerative assertion about an actual slope projection;
> constructibility alone is not payment.**" (**L1497--1498**)
>
> "closure is an enumerative statement about distinct slope projections.
> **Constructibility**, a raw support count, or a support-pair moment alone
> **does not close a ledger**." (**L1120--1122**)

Read against **MASTER-2** (`E+1 = A_eff P_2 <= (A_eff/L)(L\max\mu) = G_1 Q_img`,
#625) this is decisive:

1. **DETECTION is exhaustive and router-decidable — a THEOREM.** Every
   `(S_E)`-violator has `G_1` exponential **or** `Q_img` exponential (MASTER-2 +
   no-third-mode, #625). Both firing predicates are **finite functions of the
   profile occupancy vector** the router holds at routing time:
   `G_1 = A_eff/L` (image size `L = |\Phi(\Omega)|`) fires the
   **effective-image-collapse** trigger (L2453--2454, "exponentially fewer
   boundary values than its ambient codomain"); `Q_img = L\max\mu` (max fiber
   over image mean) fires the **ray-saturation** trigger (L2440--2449, "passing
   through these displayed images with their actual fiber cardinalities"). No
   character sum, no `E`, no `L^2` norm is needed to *decide firing*.
   **The C7 cell is "constructible in the projective locator and explanation
   incidence" (L2450--2451) — the tex's own word for router-decidable.**

2. **The rung-3 unaccounted-mass hole DOES NOT EXIST.** The primitive step's own
   payment is **max-fiber Q** (`def:primitive-q` L4918:
   `\max_s f_s \le e^{o(N)}\barN^{\rm img}`). Its **failure predicate**
   (`\max_s f_s > \barN^{\rm img}`, i.e. `Q_img > 1`) is *identical* to the
   pre-primitive **ray-saturation** trigger. So a leaf that fails the primitive
   step's payment is, by definition, a leaf the pre-primitive ray-saturation
   exclusion fires on. **There is no leaf that escapes every pre-primitive
   trigger and then fails primitive payment.** The suspected hole is refuted by
   an *identity of predicates*, backstopped by MASTER-2.

3. **The residual is PAYMENT, not detectability — unchanged from #626.** The
   *projection degree* of the detected cells (collapse: a binomial tail of
   `e^{\Omega(N)}` profiles; saturation: a uniform lower occupancy defeated by
   the light tail) "remains an enumerative input" (L2451--2452). Detection is
   proved exhaustive; the **budget charge** for the detected cells is the single
   open input.

**Net verdict: the span face CLOSES modulo the projection-degree PAYMENT, and
the detectability caveat the mission floated is DISCHARGED.** The C7 enumerative
input never hid in an undecidable trigger — it hid, and still sits, in the
projection *degree*, exactly where the tex prints it. What this packet buys the
ledger: the routing conjecture is now a **proved-detection half** plus an
**open-payment half** (`= #626`), the rank certificate is shown **inert** on the
canonical collapse violator, and the heavy-atom "unaccounted mass" scenario is
**refuted**. The arc ends: the only residual is the projection-degree count,
already quantified by #626.

---

## Rung 1 — TRIGGER INVENTORY: the detectability table (AUDIT + PROVED)

### 1.1 The printed order (verbatim, L5180--5183)

> "The first-match order is: **algebraic major arcs first, then a separately
> certified Sidon/Fourier cell, and only then the high-energy primitive inverse
> step.** Naming a large low-energy fiber a cell does not pay it."

and the primitivity content (`def:primitive-first-match-residual` **L1510--1513**,
prose **L4804--4812**):

> "*primitive* means that the row-specific **quotient, planted, field-descent,
> rank, and ray-saturation** certificates named by the atlas have **all been
> applied**... it **does not assume the Fourier, Sidon, max-fiber, or ray
> estimates that will be imposed below**." (**L4807--4812**)

So the pre-primitive cells are the **five algebraic certificates** (quotient,
planted, field-descent, rank, ray-saturation), fired in "algebraic major arcs",
plus the **Sidon/Fourier** cell. The primitive residual is what survives; its
own payment is max-fiber Q + the analytic estimates.

### 1.2 The detectability table (each row: trigger verbatim → router-decidable?)

For each pre-primitive cell, the **firing predicate** (what makes the cell
detect/route a leaf) versus whether that predicate is a **finite combinatorial
function of the profile the router holds** (occupancy vector, support, image
size `L`, ambient sizes, rank of `V_g`, field of definition) — as opposed to a
spectral/analytic quantity that is only *paid*, not *computed*.

| cell (anchor) | printed firing predicate | router-decidable firing? | payment (what is *paid*, not decided) |
|---|---|---|---|
| **Quotient/periodic** (L2374) | "the locator or boundary map **factors through the quotient coordinate**" (support constant on `π`-fibers) | **YES** — factorization / fiber-constancy (combinatorial) | quotient term in `E_n`; entropy loss `binom(n-b,a-b)` |
| **Dihedral/Chebyshev** (L2385) | "detected by **inversion invariance** after a multiplicative change / composition with Dickson–Chebyshev maps" | **YES** — composition/invariance test | 2-to-1 dihedral fiber count |
| **Planted-block** (L2399) | "a polynomial factor `P` **common to every support locator `Q_S`**" (divisibility) | **YES** — divisibility (combinatorial) | subexp census of `P` **+ slope projection** (enum) |
| **Tangent/deep/common-line** (L2409) | "**rank-defective contact** ... differential of the slope projection has **smaller than its expected rank**" | **YES** (rank test) — but "**rank drop alone is not payment**" (L2416) | independent minors **+ slope projection** (enum) |
| **Extension/field-descent** (L2422) | "**defined over a proper subfield** (field descent) ... **Frobenius invariance is constructible**" | **YES** — field of definition (combinatorial) | "direct **field-sensitive slope count**" (enum) |
| **Differential-locator** (L2429) | "the **Vandermonde/Hasse Jacobian loses its expected rank**" | **YES** (rank test) — "rank loss need not equal codimension" | independent minors + slope projection (enum) |
| **Ray-saturation** (L2440--2449) | "passing through these displayed images **with their actual fiber cardinalities**" (a fiber **above the image mean**, `Q_img>1`) | **YES** — fiber cardinalities (occupancy vector) | "the **occupancy or image–fiber bound** ... **projection degree remains an enumerative input**" (L2449--2452) |
| **Effective-image collapse** (L2453--2454) | "a boundary map **reaches exponentially fewer boundary values than its ambient codomain**" (`L \ll A`, `G_1` exp) | **YES** — image size `L` vs `A` (both combinatorial) | routed to an earlier profile **or** `(FI)` proved (L877, L1115); projection degree = enum input |
| **Balanced-core/split-pencil** (L2456) | equal-degree monic pair with common depth-`w` prefix; **projective dimension** of the core family | **PARTIAL** — dim decidable; pencil pays by root count, higher-dim needs a proved decomposition | `floor((n-g)/h)` (pencil) or direct ray estimate |
| **Fourier/Sidon-heavy** (L2476) | "a primitive prefix fiber ... having **exponentially small additive energy** (few additive quadruples)" | **NO** — additive energy is an `L^2`/spectral quantity, "**kept separate from the constructible atlas**" (L2490--2492) | analytic moment bound `(MI)/(MA)` or a "direct max-fiber theorem" |

**Reading (AUDIT + PROVED).** *Every* cell in the constructible algebraic atlas
fires on a **finite combinatorial/algebraic property** — factorization,
divisibility, rank of `V_g`, field of definition, projective dimension, image
size, fiber cardinalities. The **only** spectrally-triggered cell is the
**Fourier/Sidon-heavy component** (additive energy), and the tex deliberately
holds it "separate from the constructible atlas" and *after* the algebraic arcs.
Crucially, the **two C7 triggers we need** — collapse (`L\ll A`) and
ray-saturation (`\max_s f_s > \barN^{\rm img}`) — are **both** in the
router-decidable column. This is not merely an interface reading: **BLOCK 6**
recomputes `G_1` and `Q_img` from the occupancy vector `f` **alone** and matches
the spectral values exactly, and exhibits two leaves with the **same fiber
multiset** `{1,1,1,1}` but **different additive energy** (`e_{\rm AP}=44` vs
`e_{\rm Sidon}=28` on `\{0,1,2,3\}` vs `\{0,1,3,7\}`) — so additive energy is
**provably not** a function of the profile the router holds, while both C7
triggers **provably are**. The detectability split of the table is therefore
**PROVED for the load-bearing rows**, AUDIT for the rest.

---

## Rung 2 — COLLAPSE VIOLATORS: the `(FI)` route (PROVED)

A `G_1`-exponential product profile (block-parabola) has image exponentially
smaller than its span. **Which pre-primitive trigger provably fires on all of
these, and is it router-decidable?** Candidate-by-candidate:

- **Effective-image-collapse trigger (L2453--2454): PROVED-FIRES, router-decidable.**
  The predicate is `L \ll A` ("exponentially fewer boundary values than its
  ambient codomain"). On **admissible** leaves there is no Gap-2 span/ambient
  collapse (`A_eff = A`, #545, vacuous for `w<char`), so
  `G_1 = A_eff/L` exponential `\iff L \ll A_eff = A \iff` the trigger fires.
  Router-decidable: `L=|\Phi(\Omega)|` and `A=|B^R|` are finite counts. The
  routing is **L877--881**: *"the ambient scale ... may replace `\barN_\lambda`
  only after `(FI): L\ge e^{-o(n)}A` has been proved uniformly. Otherwise
  effective-image collapse is routed — assigned by the first-match rule to an
  earlier profile so that its slopes and all witnesses above them are removed
  from the later residual."* **BLOCK 1** recomputes the leaf: `N=pk`, `m=k`,
  `A_eff=A=p^{2k}`, `L=p^k`, `G_1=p^k`, `Q_img=1`, `E=p^k-1`, `L/A=p^{-k}`.

- **Rank certificate (`lem:rank-defect-payment` L2534, `prop:rank-pivot`
  L4710): FAILS — INERT on the parabola (WITNESS, PROVED).** The block-parabola
  has **full** effective rank: `\rank_{\F_p} V_g = 2k = R` (BLOCK 2 builds the
  per-block generators `\{(t,t^2)-(t_0,t_0^2)\}` and computes `\rank=2` per
  block by exact `\F_p` Gaussian elimination, hence `2k` in the product). The
  rank-defect locus `\{\rank \le R-h,\ h\ge1\}` is therefore **empty** on it —
  the trigger does **not** fire. The collapse is `|\Phi(\Omega)|=p^k \ll p^{2k}`,
  a property of the **image**, not the **span rank**. Exactly as printed:
  "**generic rank alone gives no such conclusion**" (L2542). So the collapse is
  caught by the *image-size* trigger, **not** by the rank certificate. WITNESS
  recomputed BLOCK 2 (`rank_Vg = 2k = R` full, yet `L<A` fires).

- **Quotient/field-descent certificates: do not carry the collapse alone.** The
  per-block parabola is a **profile** (#622: its faithful chart is per-block,
  `R_{\rm prod}=2k\ge\char`), and field-descent (Frobenius closure) is the
  **Gap-2** span-collapse, which is `C5`, **vacuous on admissible** (#545). The
  Gap-1 image collapse with `A_eff=A` that the parabola exhibits is **not** a
  field-descent event; it is precisely the effective-image-collapse trigger.

**Verdict (rung 2, PROVED).** Every collapse violator PROVED-fires the
router-decidable effective-image-collapse trigger (`L\ll A`), routed by
L877--881. The **rank certificate is inert** (full rank; a witness, not a
detector, of collapse). The **residual** is the *count* of collapse profiles —
the binomial tail `\sum_{j\ge\theta k}\binom{k}{j}=e^{\Omega(N)}` (#626,
recomputed BLOCK 8: `N_{\rm coll}(20,0.6)=263950`,
`N_{\rm coll}(40,0.6)=147\,437\,500\,478`) — the **projection-degree payment**,
which detection does not discharge. Detection PROVED; payment OPEN (= #626).

---

## Rung 3 — SATURATION VIOLATORS: the max-fiber-Q route, and the hole (PROVED-neg)

A `Q_img`-exponential **heavy-atom** product has a **full image** (`L=A_eff`,
`G_1=1`, `(FI)` **holds** — its span face is fine) and a **heavy fiber**
(`Q_img` exponential). So the **collapse trigger is silent** on it. The printed
order sends high-energy leaves to the primitive inverse step **last**; and the
primitive step's own payment is **max-fiber Q**, which by #625 T-A forces
`(S_E)` on anything that pays it. The mission's sharp question: the heavy-atom
**cannot** pay max-fiber Q (`Q_img` exponential `\iff` image-normalized Q fails
by definition, `def:primitive-q` L4918) — so it **fails primitive payment**;
**then where does it route?** Is there a printed catch-all after primitive
failure, or does the budget silently assume it was caught earlier? This is the
prime hole suspect: *a leaf that fails every pre-primitive trigger AND fails
primitive payment = unaccounted mass.*

**The hole does not exist (PROVED-negative), because two predicates coincide.**

- **The primitive step's rejection predicate IS the pre-primitive
  ray-saturation trigger.** `def:primitive-q` (**L4915--4918**): primitive Q
  holds iff `\max_{s}f_s \le e^{o(N)}\barN^{\rm img}`. Its **negation** —
  `\max_s f_s > \barN^{\rm img}`, i.e. `Q_img = L\max\mu > 1` — is *word for
  word* the ray-saturation firing predicate (L2440--2449: "passing through
  these displayed images with their actual fiber cardinalities"; the printed
  contrast at L886--887: "a **ray-saturation profile** ... records many raw
  witness representatives producing the same explanation or slope ray"). So a
  leaf that **fails the primitive payment** is **identically** a leaf the
  pre-primitive **ray-saturation** exclusion (one of the five primitivity
  certificates, L4807) fires on. **BLOCK 4** verifies the predicate identity
  `\{Q_{\rm img}>t\} = \{\max_s f_s > t\,\barN^{\rm img}\}` at
  `t\in\{1,\tfrac32,2,5,10\}` on 400 random profiles, and the implication
  `\text{fails-primQ} \Rightarrow \text{fires-ray-saturation}` on all of them.

- **MASTER-2 backstop (no leaf escapes both triggers).** If a leaf fails
  primitive payment it has `Q_img` exponential — so it **fires ray-saturation**.
  If instead it had `Q_img` sub-exponential *and* `G_1` sub-exponential, then
  `E+1\le G_1 Q_img` is sub-exponential and `(S_E)` **holds** — it is not a
  violator (no-third-mode, #625; **BLOCK 5**: both ratios `\le t \Rightarrow
  E+1\le t^2`, 300 profiles). Hence **there is no `(S_E)`-violator that escapes
  both pre-primitive triggers**, and in particular none that reaches the
  primitive step, fails its payment, and is unaccounted.

- **The heavy-atom's saturation cell is DETECTED but its printed payment is
  DEFEATED (= #626 budget B).** The saturation payment (`lem:saturation-principle`
  L2574, `prop:saturation-payment` L4726) needs a **uniform lower occupancy
  `H`**: `|Z(\Ccal)|\le\lfloor|\Ccal|/H\rfloor`. The heavy-atom has a **light
  tail**, `\min` occupancy `H=1`, so the bound is `|Z|\le|\Ccal|` — **no
  compression** (BLOCK 7, exact for `A_eff\in\{16,81,256,625\}`). As printed,
  "**an upper bound on the number of profile lifts goes in the wrong
  direction**" (L4738). So the cell **fires** (constructible, detected) but is
  **paid only** by "a direct distinct-slope estimate at the profile scale" — the
  enumerative input.

**Verdict (rung 3, PROVED-negative + PARTIAL).** The heavy-atom is caught **at
the ray-saturation trigger**, which is the **same predicate** as its own
primitive-Q failure — so failing primitive payment is *not* an escape, it is the
detection. **No unaccounted mass.** The residual is again the
**projection-degree payment** (occupancy/direct-slope estimate), OPEN (= #626).
**BLOCK 3** recomputes the exact heavy-atom rows (`E=49/15,169/20,1323/85,961/39`;
`Q_img=8,27,64,125`; `G_1=1`), byte-identical to #625.

---

## Rung 4 — THE THEOREM (outcome (a)): routing-exhaustiveness-as-detection

### T-DET (PROVED). Detection is exhaustive and router-decidable.

> **Theorem (routing-exhaustiveness-as-detection).** In the printed first-match
> order (L5180--5183), every `(S_E)`-violating admissible product profile fires
> a **router-decidable** pre-primitive trigger before the high-energy primitive
> inverse step:
>
> - if `G_1 = A_eff/L` is exponential, the **effective-image-collapse** trigger
>   (L2453--2454), predicate `L\ll A`, decided from `L=|\Phi(\Omega)|` and
>   `A=|B^R|`; routed by L877--881;
> - if `Q_img = L\max\mu` is exponential, the **ray-saturation** trigger
>   (L2440--2449), predicate `\max_s f_s > \barN^{\rm img}`, decided from the
>   occupancy vector; and this predicate is **identical** to the negation of
>   `def:primitive-q`, so the primitive step's own max-fiber-Q rejection
>   **coincides** with it.
>
> The partition is **exhaustive**: by MASTER-2 (`E+1\le G_1 Q_img`, #625) every
> violator has `G_1` exp **or** `Q_img` exp; by no-third-mode both sub-exp
> `\Rightarrow (S_E)`. In particular **no leaf escapes all pre-primitive
> triggers and then fails primitive payment**.

**Proof.** MASTER-2 and no-third-mode are #625 (PROVED). Router-decidability of
the two predicates is the definitional fact that `L`, `A`, and the fiber
cardinalities are finite functions of the profile (BLOCK 6). The predicate
identity `\{\text{fails primitive-Q}\}=\{\text{ray-saturation fires}\}` is
`def:primitive-q` L4918 read against L2440--2449 (BLOCK 4). On admissible leaves
`A_eff=A` (#545) makes the collapse predicate `L\ll A` coincide with `G_1` exp.
∎

### The caveat (the ONLY residual): the projection-degree PAYMENT

Detection is exhaustive; the **budget charge** for the detected cells is the
assumed enumerative input, and it is exactly #626, **unchanged**:

- **collapse**: the number of collapse profiles routed by L877--881 is the
  binomial tail `e^{\Omega(N)}` (#626 T-COLLAPSE), which busts A2's "`e^{o(n)}`
  profiles" (L905--907, L869); the `(FI)`-routing must delete them before the
  `E_n` sum, and the **exhaustiveness of that deletion at the degree scale** is
  the open input;
- **saturation**: the uniform lower occupancy `H` is defeated by the light tail
  (`H=1`), so the printed occupancy bound does not pay it; only "a direct
  distinct-slope estimate at the profile scale" does — the open input.

This is precisely the tex's own split: the C7 cell is "**constructible** ... but
its **projection degree remains an enumerative input**" (L2451--2452), and
"**constructibility alone is not payment**" (L1497--1498). The mission's
detectability caveat — that the C7 input might hide in an *undecidable* trigger
— is **DISCHARGED**: the triggers are decidable; the enumerative input is purely
the projection degree.

### Span-face verdict

The span face is `(FI): L\ge e^{-o(N)}A_eff`. It is threatened **only** by
`(FI)`-violators = the `G_1`-exponential **collapse** class (the heavy-atom has
`(FI)`, no span-face threat). Every collapse violator is **detected** by the
router-decidable collapse trigger and **routed out** (L877--881). Therefore:

> **The span face CLOSES modulo the collapse projection-degree payment (= #626
> budget A).** Under the stronger `(S_E)` framing, both violator classes are
> detected; the saturation class bears on the MCA count (max-fiber Q), and its
> detection coincides with the primitive-Q rejection.

**This ENDS THE ARC.** The routing = spectrum conjecture (#622 Rung 3 / #625)
**factors** into a **proved-detection half** (this packet, T-DET) and an
**open-payment half** (`= #626` projection-degree budget). The suspected rung-3
unaccounted-mass hole is **refuted** (predicate identity + MASTER-2). Nothing new
is open; the single residual is the count #626 already quantified.

---

## Rung 5 — CENSUS (MEASURED, verifier-recomputed BLOCK 9)

The extracted triggers, run on the three regimes; the firing table is the
empirical content. `E = A_eff P_2 - 1` exact via `fractions.Fraction`.

**(a) Single admissible power-sum leaves** (global chart, `R<\char`; reproduces
#622/#625/#626 census byte-for-byte):

| p | N | R | m | L | A_eff | E | collapse? | ray-sat? |
|---|---|---|---|---|-------|---|-----------|----------|
| 3 | 2 | 1 | 1 | 2 | 3  | 1/2   | no | no |
| 5 | 3 | 2 | 2 | 3 | 25 | 22/3  | no | no |
| 7 | 4 | 2 | 2 | 6 | 49 | 43/6  | no | no |

`Q_img=1` (uniform image) ⇒ ray-saturation silent; `G_1=A_eff/L` bounded ⇒
collapse silent; `(S_E)` safe. Neither trigger fires — as it must, single leaves
are not violators.

**(b) Collapse products (block-parabola):** collapse trigger **FIRES**, rank
**INERT**, ray-saturation **silent**.

| p | k | N=pk | L=p^k | A_eff=p^{2k} | E=p^k−1 | G_1 | Q_img | collapse? | rank defect? |
|---|---|------|-------|--------------|---------|-----|-------|-----------|--------------|
| 3 | 2 | 6  | 9   | 81      | 8    | 9   | 1 | **YES** | no (rank 2k=R full) |
| 3 | 4 | 12 | 81  | 6561    | 80   | 81  | 1 | **YES** | no |
| 5 | 4 | 20 | 625 | 390625  | 624  | 625 | 1 | **YES** | no |
| 7 | 4 | 28 | 2401| 5764801 | 2400 | 2401| 1 | **YES** | no |

**(c) Saturation products (heavy-atom per block, `p=5,a=2/5`):** ray-saturation
**FIRES**, collapse **silent**, MASTER-2 slack.

| k | A_eff=5^k | L=5^k | G_1 | Q_img=2^k | E+1=(5/4)^k | collapse? | ray-sat? |
|---|-----------|-------|-----|-----------|-------------|-----------|----------|
| 1 | 5    | 5    | 1 | 2  | 5/4     | no | **YES** |
| 2 | 25   | 25   | 1 | 4  | 25/16   | no | **YES** |
| 3 | 125  | 125  | 1 | 8  | 125/64  | no | **YES** |
| 4 | 625  | 625  | 1 | 16 | 625/256 | no | **YES** |

**Trigger-firing dichotomy (MEASURED).** Single leaves fire neither trigger;
every product violator fires exactly one (collapse XOR saturation, per its mode);
the rank certificate never fires on the collapse products (full rank). No leaf in
the census fails both triggers — matching T-DET.

---

## Verdict ledger

| item | verdict | label |
|------|---------|-------|
| printed order = arcs → Sidon → primitive; five pre-primitive certificates | verbatim (L5180, L4807) | **AUDIT** |
| every algebraic-atlas trigger is combinatorial; only Fourier/Sidon is spectral | detectability table | **AUDIT + PROVED** (BLOCK 6) |
| the two C7 triggers (`L\ll A`, `\max f_s>\barN^{\rm img}`) are router-decidable | functions of occupancy vector | **PROVED** (BLOCK 6) |
| additive energy is NOT router-decidable (same fiber multiset, diff. energy) | the one spectral outlier | **PROVED** (BLOCK 6) |
| MASTER-2 `E+1\le G_1 Q_img`; no third mode | Hölder + #625 | **PROVED** (BLOCK 0/5) |
| **collapse violators PROVED-fire the effective-image-collapse trigger** | `L\ll A` on admissible (`A_eff=A`) | **PROVED** (BLOCK 1) |
| **rank certificate INERT on the block-parabola** (full rank `2k=R`) | "generic rank ... no conclusion" | **PROVED** (BLOCK 2) |
| **primitive-Q failure predicate = ray-saturation trigger** | `def:primitive-q` L4918 ≡ L2440 | **PROVED** (BLOCK 4) |
| **rung-3 unaccounted-mass hole REFUTED** (no escape-both, no fail-primitive-only) | predicate identity + MASTER-2 | **PROVED-negative** (BLOCK 4/5) |
| saturation payment defeated on the light tail (`H=1`) | `lem:saturation-principle` | **PROVED** (BLOCK 7) |
| `(FI)`-routing image scale `\barN=1`; collapse count = binomial tail `e^{\Omega(N)}` | L877 + #626 | **PROVED** (BLOCK 8) |
| **routing-exhaustiveness-as-DETECTION theorem** (span face closes mod payment) | T-DET | **PROVED** (BLOCK 0–9) |
| projection-degree PAYMENT (collapse count + saturation occupancy) | the enumerative input | **OPEN** (= #626) |

**Proposed ledger entry (for the maintainer).** *Closing the span-face arc on
the printed order. Read cell by cell, the frontiers atlas splits its triggers
along the detectability line the paper already states ("constructibility alone
is not payment", L1497--1498): every algebraic-atlas cell fires on a finite
combinatorial property (factorization, divisibility, rank of `V_g`, field of
definition, image size, fiber cardinalities) and is router-decidable, and the
only spectrally-triggered cell (Fourier/Sidon-heavy, additive energy) is held
separate and after the arcs. In particular the two C7 triggers are
router-decidable: effective-image collapse fires on `L\ll A` (image size), and
ray-saturation fires on `\max_s f_s > \barN^{\rm img}` (occupancy) — the latter
being word-for-word the negation of `def:primitive-q`. Consequently (i)
DETECTION is exhaustive: by MASTER-2 every `(S_E)`-violator fires collapse or
ray-saturation before the primitive step, and the primitive step's own
max-fiber-Q rejection coincides with the pre-primitive ray-saturation trigger,
so there is no leaf that escapes all pre-primitive triggers and then fails
primitive payment (the "unaccounted mass" scenario does not occur); the block-
parabola is caught by the image-size trigger, not the rank certificate, which is
inert on it (full rank `2k=R`). (ii) The residual is exactly the projection-
degree PAYMENT of the detected cells — the collapse binomial-tail count
`e^{\Omega(N)}` and the saturation occupancy defeated by the light tail — i.e.
`#626`, unchanged. The routing = spectrum conjecture therefore factors into a
proved detection half and an open payment half; the span face closes modulo the
projection-degree budget. Print the C7 projection-degree budget (or `(S_E)`) as
the single open input, and record that detection needs no new hypothesis. This
is an OPEN input, not an established fact — this packet proves the routing order
DETECTS every violator with a router-decidable trigger and refutes the
unaccounted-mass hole, but does not enumerate the atlas.*

### The 2–3 steps the PI should re-derive

1. **The detectability table (Rung 1).** For each pre-primitive cell, read the
   printed firing predicate and check it is a finite function of the occupancy
   vector: quotient (factorization), planted (divisibility), rank (`\rank V_g`),
   field-descent (field of definition), collapse (`L` vs `A`), ray-saturation
   (fiber cardinalities). The single exception is Fourier/Sidon (additive
   energy) — confirm via two leaves with the same fiber multiset and different
   additive energy (BLOCK 6) that it is *not* decidable from the profile.
2. **The predicate identity (Rung 3, the hole).** `def:primitive-q` L4918 says
   primitive Q `\iff \max_s f_s\le e^{o}\barN^{\rm img}`; its negation is the
   ray-saturation firing predicate L2440--2449. Hence "fails primitive payment"
   `\equiv` "fires the pre-primitive ray-saturation trigger". With MASTER-2's
   no-third-mode, no `(S_E)`-violator escapes both triggers, so the unaccounted-
   mass scenario cannot occur.
3. **The rank inertia + the split (Rung 2/4).** The block-parabola has full rank
   `\rank_{\F_p}V_g=2k=R` (Gaussian elimination over `\F_p`), so the rank-defect
   locus does not contain it; the collapse `|\Phi(\Omega)|=p^k\ll p^{2k}` is an
   image event caught by the `L\ll A` trigger. Conclude: routing = spectrum
   factors into DETECTION (proved here, router-decidable, exhaustive) and PAYMENT
   (the projection-degree count of #626, OPEN). The span face closes modulo the
   latter.

---

## Reproducibility

```sh
ulimit -v 2097152
python3 experimental/scripts/verify_routing_exhaustiveness.py   # RESULT: PASS (3417/3417)
```
