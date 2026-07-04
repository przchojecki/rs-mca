# QX.11 — top-core globalness: the tangent cap propagates to every link (DAG node `xr_globalness_from_ledger`)

- **Status:** PROVED for the mathematics of this note (Theorem G1,
  Corollaries G2/G3 — full elementary proofs written below, machine-checked)
  **+ AUDIT** for SS4 (the `L_tan` convention question — stated against the
  T0–T7 tree, deliberately NOT resolved here) **+ INPUT/HYPOTHESIS** for the
  cap itself on actual post-strip alignment families (grounded at `t = 2`
  by #152; general `t` is the open node `exchange_ledger_gen_t`).
- **Provenance (per `execution_queue.md` QX.11):** the double count was
  externally derived (GPT Pro) and independently checked (hand algebra +
  400 brute-force trials) before this packaging; this note writes the full
  proof in repo-standard form and re-verifies it from scratch.
- **DAG node:** `xr_globalness_from_ledger` (Tier D4, QX.11; Fleet-A task
  A-M2 of `campaign_split_2026_07_03.md`).
- **Parents:** `proof_sketch/s3b_iii_2_displacement_spectral.md` (XR
  mechanism, exchange calculus), `proof_sketch/s2_paid_ledger.md` SS1
  (B_tan / staircase), `wp_detail/wp2_3_stratification_case_tree.md`
  (the T0–T7 strip), `experimental/notes/m1/
  m1_t2_one_exchange_residual_degree.md` (#152, the grounded case),
  `qx6_qx8_kms_bridges.md` (cells/junta bridge), `qx14_xr_coverage_table.md`
  (row conventions, operating points).
- **Consumers:** QX.12 KLLM import (A-M3) — this is the globalness
  certificate it consumes; Q3R.1/X-1 slack composition; Q3R.2 leak
  adjudication (via Corollary G3's localization).
- **Verifier:** `python3 experimental/scripts/
  verify_qx11_topcore_globalness.py` — standalone, stdlib-only,
  deterministic (seed 20260703), exact integer/Fraction arithmetic.
  GREEN: 39/39 PASS including certificate replay.
- **Certificate:**
  `experimental/data/certificates/qx11-topcore-globalness/qx11_topcore_globalness.json`.

## Critical-path role

This is a foundation packet for the conditional prize proof spine.  QX.13 is
an averaged pair ledger; this packet is the deterministic bridge needed by the
worst-case route.  It proves that a top-core completion cap for one fixed
post-strip family propagates to all lower links with density `L/(n-j+1)`.

The packet does not prove the actual post-strip cap.  Its role is to make the
later `active_core_count_bound` / small-core cap usable globally once that cap
is supplied, while preserving the `L_tan` convention and leak-localization
issues as explicit separate inputs.

## 0. Pinned notation

```text
D           ground set (the evaluation domain), |D| = n; WLOG D = {0..n-1}.
J(n,j)      vertex set C(D,j) = {T subset D : |T| = j} (co-supports; row
            conventions as in qx14 SS0.1: exact agreement A, j = n - A,
            locator l_T(X) = prod_{x in T}(X - x)).
A           a family of j-sets, A subset C(D,j).  In the intended
            application: the post-strip aligned co-support family of ONE
            fixed pair (u,v) at exact agreement A — a fixed-pair,
            worst-case object, NOT a moment-level average.
top core    H in C(D, j-1) (a (j-1)-set).  A COMPLETION of H is a j-set
            T = H u {x}, x notin H; there are exactly n - j + 1 of them.
c_A(H)      = #{T in A : H subset T}, the number of completions of H in A.
cap(L)      the TOP-CORE CAP hypothesis: c_A(H) <= L for EVERY top core H.
            (Trivially L <= n - j + 1 is the only nonvacuous range.)
A_R         = {T in A : R subset T}, the link of an r-set R (r = |R|).
link density  |A_R| / C(n-r, j-r)   (the denominator = #{T in C(D,j) :
            R subset T} = all j-sets through R).
```

Row-convention arithmetic used in SS5: `j = n - A` gives
`n - j + 1 = A + 1` (verified per pinned row, part [8]).

## 1. Theorem G1 — the cap propagates to every level with NO loss [PROVED]

**Theorem G1.** Let `n >= j >= 1` and let `A subset C(D,j)` satisfy
`cap(L)`. Then for every `0 <= r <= j-1` and every `R in C(D,r)`:

```text
|A_R|  <=  L * C(n-r, j-1-r) / (j-r),      equivalently

|A_R| / C(n-r, j-r)  <=  L / (n-j+1).
```

*Proof.* Double-count the pair set

```text
P  =  { (T, H) :  T in A,  H in C(D, j-1),  R subset H subset T }.
```

ROW COUNT (over `T`). If `(T,H) in P` then `R subset H subset T`, so
`T in A_R`. Fix `T in A_R`. The sets `H` with `R subset H subset T`,
`|H| = j-1`, are exactly the deletions `H = T \ {y}` with
`y in T \ R`; there are exactly `|T \ R| = j - r` of them (each contains
`R` because only a non-`R` element was deleted). Hence

```text
|P|  =  (j - r) * |A_R|.
```

COLUMN COUNT (over `H`). Fix `H` with `R subset H`, `|H| = j-1`. The
`T`'s paired with `H` are exactly the completions of `H` lying in `A`:
indeed any such `T` satisfies `H subset T`, `T in A`; and conversely every
completion `T = H u {x} in A` automatically contains `R` (since
`R subset H subset T`), so it is paired with `H`. Thus `H` contributes
exactly `c_A(H) <= L` pairs. The number of admissible `H` is
`C(n-r, j-1-r)` (choose `H \ R` inside `D \ R`). Hence

```text
|P|  <=  L * C(n-r, j-1-r).
```

Combining (and `j - r >= 1` since `r <= j-1`):

```text
|A_R|  <=  L * C(n-r, j-1-r) / (j - r).
```

DENSITY FORM (the exact cancellation). By factorials,

```text
C(n-r, j-1-r) / C(n-r, j-r)  =  (j-r)! (n-j)! / ((j-1-r)! (n-j+1)!)
                              =  (j-r) / (n-j+1),
```

so dividing the count bound by `C(n-r, j-r)` cancels the `(j-r)` exactly:

```text
|A_R| / C(n-r, j-r)  <=  L/(n-j+1) .                                 QED
```

The cancellation identity `(n-j+1) C(n-r,j-1-r) = (j-r) C(n-r,j-r)` is
machine-checked for ALL `(n, j, r)` with `n <= 40` (11480 triples, part
[1]); the double-count skeleton (both counts, plus the per-`T` count
`= j - r`) is checked exhaustively on `J(9,4)` for seeded random families
with no cap imposed (650 cells, part [2]).

**Remarks.**

```text
R1 (top level = hypothesis).  At r = j-1 the statement reads
   |A_H| <= L * (n-j+1)/(n-j+1) = L — the cap itself.  The theorem is
   exactly tight at the top and propagates DOWNWARD with zero loss:
   the deletion multiplicity (j-r) is cancelled by the binomial ratio.
   In particular eps := L/(n-j+1) is UNIFORM in r — no dependence on
   the core size, unlike a naive level-by-level induction which would
   stack a loss per level.
R2 (global density).  r = 0 gives mu(A) = |A|/C(n,j) <= L/(n-j+1):
   a cap-respecting family is automatically eps-sparse globally.
R3 (equality characterization).  Every inequality used is an equality
   iff every top core H containing R has EXACTLY L completions in A.
   Steiner systems S(j-1, j, n) realize this with L = 1 at every R
   simultaneously (SS below; Fano S(2,3,7) and SQS(8), verified), so
   the constant L/(n-j+1) cannot be improved.
R4 (deterministic / worst-case).  No probability enters: G1 holds for
   THE family at hand, per fixed pair (u,v).  This is precisely the
   currency the worst-case conversion needs (qx14 SS7 flagged that its
   own table is moment-level only; G1 is the fixed-pair complement).
```

## 2. Corollaries: mixed restrictions and leak localization [PROVED]

**Corollary G2 (mixed restrictions / junta cells).** Let `A` satisfy
`cap(L)`, let `Z subset D` with `|Z| = z` and `n - z >= j`, and let
`R subset D \ Z`, `|R| = r <= j-1`. Then

```text
#{T in A : R subset T, T cap Z = empty} / C(n-z-r, j-r)
      <=  L / (n - z - j + 1).
```

*Proof.* Put `D' = D \ Z` (size `n' = n - z`) and
`A' = {T in A : T subset D'} subset C(D', j)`. For every top core
`H in C(D', j-1)`, the completions of `H` inside `A'` are a subset of its
completions inside `A`, so `c_{A'}(H) <= c_A(H) <= L`: the cap is
HEREDITARY under domain restriction. Apply Theorem G1 on the ground set
`D'`. QED

In the notation of `qx6_qx8_kms_bridges.md` SS2, the set in G2 is exactly
the junta cell `Cell_C(tau)` with `C = R u Z`, `tau = R`: **G2 says every
cell with bounded core is `L/(n-|C\tau|-j+1)`-light.** Combined with
qx6_qx8 Proposition 2.4 (junta correlation pigeonholes onto one cell at a
`2^-d` discount), the cap kills junta correlation above
`2^d * L/(n-j+1-z)` — this is the composition handle the KMS/KLLM branch
consumes. (Checked exhaustively for `|Z| <= 2`, `r <= 2` on `J(9,4)`,
part [7].)

**Corollary G3 (leak localization — the Q3R.2 instrument).** If the
conclusion of G1 fails for some `(r, R)` — i.e. some link of `A` has
density `> L/(n-j+1)` — then some TOP core `H` with `R subset H` has
`c_A(H) >= L + 1`.

*Proof.* Contrapositive of the column count: if every `H` containing `R`
had `c_A(H) <= L`, the chain in G1 would bound `|A_R|`. QED

Consequence for the adjudication workflow: **every link leak, at any core
size `r`, localizes upward to a top-core leak over the same `R`.**
Adjudicating the 10 post-strip link-leak candidates from the #209 corpus
(Q3R.2 / Fleet C-1) therefore only requires classifying top cores — and
E19's per-`r` link measurements are subsumed by the single top-level
measurement once the cap is what is being tested.

## 3. Why the cap is the tangent ledger [the geometry; grounded case cited]

The completions of a fixed top core `H` share the degree-`(j-1)` divisor

```text
l_T  =  (X - y) * l_H,        l_H = prod_{x in H} (X - x),
```

i.e. the family `{T = H u {y}}` is ONE moving root `y` against a fixed
divisor — exactly the moving-root/staircase geometry that the tangent
ledger prices (`s2_paid_ledger.md` SS1: `B_tan(A) <= n - A + 1`,
PROVED-cited #147 staircase range; the common-divisor plane of the T2
stratum). Many aligned completions of the same core = alignment surviving
the atomic one-exchange move anchored at `H` (`s3b_iii_2` SS2: the
exchange is a rank-one Cauchy update) = tangent-type structure. So
"post-strip families satisfy `cap(L_tan)` for small `L_tan`" is the
assertion that the strip charged all the per-core repetition — the cap IS
the tangent ledger read as a local degree bound on top cores.

**Grounded case (`t = 2`, PROVED-LOCAL, #152 =
`m1_t2_one_exchange_residual_degree.md`).** In the `t = 2` Hankel-pencil
normal form, for a fixed core `R` (there `|R| = j-1`) the one-exchange
determinant `Delta_R(y)` is a polynomial of degree `<= 2` in the anchor
`y` (#152 Lemma 1, DET2): if it is not identically zero, AT MOST TWO
anchors pass the alignment gate; if three or more pass, the core is ruled
and #152 Lemma 2 (Hankel ruled-core collapse) forces it to be inactive or
fixed-slope — i.e. already charged by the fixed-slope root-slice ledger.
Post-charging, #152's Theorem (DEG1/EDGE1) states: each `(j-1)` core
supports at most ONE residual one-exchange edge. Since any two
completions of the same core are adjacent through it, this is exactly
`cap(2)` for the residual `t = 2` family — the grounded instance of the
hypothesis this note's theorem consumes.

**What is NOT grounded:** for general in-band `t`, the analogous per-core
gate is the named open target `exchange_ledger_gen_t` (Q4.1; s3b_iii_2
SS8: "#152 `t=2` exchange ledger -> general `t`"). At general `t` the
determinant gate heuristic suggests `<= t` anchors per core pre-collapse
[HEURISTIC — no proof in the repo], which would give a poly cap but NOT
`L_tan in {1,2}`; whether the Hankel collapse strips the excess at
general `t` is open. This note does not close that; it makes the cap the
SINGLE hypothesis to test (via G3, top cores only).

## 4. The `L_tan` convention — an explicit AUDIT question [NOT resolved here]

Theorem G1 is proved for every `L`; the composition needs a VALUE, and
two conventions are in play. They differ by exactly a factor 2 in `eps`,
which propagates linearly through every consumer. **Stated, not
resolved:**

```text
Convention S ("first-unpaid-support stripping"):   L_tan = 1.
   The strip normal form charges, per top core, the FIRST surviving
   completion to a stripping ledger (one designated support per core,
   charged alongside the T2/root-slice events it extends); the residual
   family then has c(H) <= 1 for every core.
   COST: the stripping ledger's own price must be shown to sit inside
   Paid(A).  That pricing step is NOT written anywhere in the repo —
   the wp2_3 tree does not name a "first completion per core" charge.

Convention E ("residual-edge", #152's literal form):   L_tan = 2.
   The strip charges only what #152 actually charges (ruled/fixed-slope
   cores via the root-slice ledger); the surviving guarantee is DEG1/
   EDGE1: at most one residual one-exchange EDGE per core, i.e. at most
   TWO completions per core.  No new ledger is needed — but the bound
   is only PROVED at t = 2, and two genuinely residual completions of
   one core (non-ruled quadratic gate with both roots active) are
   allowed to stand.
```

**Against the T0–T7 stratification tree
(`wp_detail/wp2_3_stratification_case_tree.md`).** The tree is
first-match-wins: T0 (containment) and T1 (degenerate) excise their
strata; T2 (tangent overlap -> B_tan) plus the fixed-slope root-slice
charging inside the `t = 2` packet are where per-core repetition is
paid; T3 (quotient) folds; what reaches T4–T7/LEAF is "the post-strip
family" that the cap hypothesis speaks about. The open normal-form
question is precisely: **does the tree's strip leave at most one
completion per top core (Convention S — then WHERE is the first-support
charge priced?), or does it only guarantee #152's residual-edge shape
(Convention E — then `L_tan = 2` and the `t = 2` proof is the only
grounded case)?** Neither reading changes Theorem G1; only `eps` moves
by the factor 2 shown in SS5.

**Adjudication corpus.** The 10 post-strip link-leak candidates from the
#209 corpus (Q3R.2 / Fleet C-1 in `campaign_split_2026_07_03.md`) are
the decision data: each candidate is either (i) strippable under
Convention S (evidence that `L_tan = 1` with a REAL, priceable stripping
ledger), or (ii) consistent with Convention E only (`L_tan = 2`), or
(iii) a genuine unpaid tangent leak — `c_A(H) > 2` at a top core
post-strip — which breaks BOTH conventions at that core and is
R2-relevant (report loudly, per E19's protocol). By Corollary G3 the
classification only needs top-core counts. Until that adjudication
lands, downstream consumers must carry `L_tan in {1, 2}` symbolically.

## 5. The KLLM interface — what the composition consumes

```text
INPUT (hypothesis; per fixed pair (u,v), post-strip; gated by Q3R.2):
    cap(L_tan):  c_A(H) <= L_tan for every top core H,  L_tan in {1,2}.

OUTPUT (this note; unconditional given the input):
    (a, eps)-GLOBALNESS in the uniform-slice sense, with
        eps = L_tan / (n-j+1) = L_tan / (A+1),   for ALL a <= j-1:
    every restriction fixing a coordinates to 1 (core R, |R| = a) has
    link density <= eps        [Theorem G1 — eps uniform in a];
    mixed patterns (additionally fixing z coordinates to 0) have
    density <= L_tan / (A+1-z) [Corollary G2 — the junta-cell form].

CONSUMERS:
    QX.12 (A-M3) KLLM import — this is the globalness certificate the
        small-set engine needs; matching this (a,eps) form to the
        paper's own globalness definition (and to the UNIFORM-SLICE
        variant — cube statements do not transfer verbatim, per
        QX.12-FLAGS) is QX.12's verification obligation
        [CITATION NEEDED — no KLLM statement is quoted or used here];
    Q3R.1 / X-1 slack composition (strip -> cap globalness -> KLLM ->
        E_3 bridges -> pair ledger);
    qx6_qx8 Prop 2.4: junta correlation lands on a cell; G2 caps every
        bounded-core cell, so junta correlation above 2^d * eps is
        excluded under the cap.
```

`eps` at the operating shapes (rows pinned from
`qx14_xr_coverage_table.md` SS4; `n-j+1 = A+1` re-verified per row,
part [8]):

```text
row                       A                log2 eps (L_tan=1)  (L_tan=2)
(a)  n=512, t*=5          261              -8.03               -7.03
(c)  rate 1/2,  t*        1108104540515    -40.01              -39.01
(c)  rate 1/4,  t*        556770474278     -39.02              -38.02
(c)  rate 1/8,  t*        279600463336     -38.02              -37.02
(c)  rate 1/16, t*        140382131272     -37.03              -36.03
```

So the cap delivers a `1/poly` link bound — in fact `~ 2^-40` at prize
scale, uniformly over all core sizes `a <= j-1` — with the only
convention uncertainty a single bit (`L_tan = 1` vs `2`). Whether
`eps ~ 2^-40` clears the KLLM loss exponents per rate is exactly
QX.9/QX.10/Q3R.1's arithmetic, not claimed here.

## 6. Non-claims (honesty ledger)

```text
N1  The CAP ITSELF is not proved for actual post-strip alignment
    families.  Grounded case: t = 2 only (#152, PROVED-LOCAL, in the
    t = 2 Hankel-pencil normal form after fixed-slope root-slice
    charging).  General in-band t is OPEN (`exchange_ledger_gen_t`,
    Q4.1).  Empirical gates: E19's measurements and the 10 #209 leak
    candidates (Q3R.2).  This note proves cap => globalness, nothing
    about cap-validity.
N2  No KLLM/KMS/DKKMS statement is quoted, used, or asserted.  The
    matching of SS5's (a,eps) form to the literature definition, in the
    uniform-slice variant, is QX.12's job [CITATION NEEDED there].
N3  The L_tan value is NOT resolved (SS4): Convention S's stripping
    ledger is unpriced in the repo; Convention E is proved only at
    t = 2.  Consumers carry L_tan in {1,2} symbolically.
N4  G1 alone does not give R2: it converts the cap into a link bound
    per pair; the composition still needs the cap per pair (N1), the
    KLLM engine (N2), and the assembly (Q3R.1).
N5  The heuristic "<= t anchors per core at general t" in SS3 is
    labelled HEURISTIC and consumed nowhere.
N6  Adversarial greedy values below the integer ceiling (e.g. 7/9 on
    J(9,4), r=1, L=1) are greedy achievements, not proved maxima; the
    rigorous tightness content is R3 + the verified Steiner witnesses
    (Fano S(2,3,7), doubled SQS(8)) and the reached ceiling 3/3 at
    J(9,4), r=2, L=1.
N7  No claim that Steiner-type extremal families occur as actual
    alignment families; they only pin the constant in G1.
N8  General-(n,j) statements are proved abstractly; the verifier
    grounds them on J(7,3), J(8,4), J(9,4), J(10,5) and the n <= 40
    identity sweep — toy scale only, per the campaign's RAM rule.
```

## 7. Verifier

`experimental/scripts/verify_qx11_topcore_globalness.py` — standalone
python3, stdlib only, deterministic (seed 20260703), exit 0 iff green.
It pins and replays
`experimental/data/certificates/qx11-topcore-globalness/qx11_topcore_globalness.json`.
39/39 PASS including certificate replay at writing (~0.1 s):

```text
[1] the cancellation identity, all (n,j,r), n <= 40 (11480 triples);
[2] the double-count skeleton on J(9,4), seeded random families (no cap),
    all r-cores: direct pair enumeration == (j-r)|A_R| == sum_H c_A(H),
    and each T in A_R carries exactly j-r admissible H (650 cells);
[3] Theorem G1 on greedy cap-respecting families (seeded insertion
    order), J(9,4) L in {1,2} and J(10,5) L in {1,2,3}, 3 seeds each:
    realized cap re-measured, ALL r-core links checked exactly (130/386
    cores per family); worst density/bound ratio = 1.0000 in every run
    (the top level is exactly at cap — R1's tightness, observed);
[4] tightness witnesses verified from scratch: Fano S(2,3,7) and the
    doubled SQS(8) are Steiner (every top core hit exactly once), and
    meet G1 with EXACT equality at every r-core (density 1/5); full
    family at L = n-j+1 likewise;
[5] adversarial targeted max-packing (load one target core first,
    subject to the cap): bound never exceeded on any of 6 cases; the
    provably-attainable integer ceiling 3 at J(9,4), r=2, L=1 is
    reached (3/3); achieved/ceiling reported per case;
[6] negative control: the cap-violating family (all 6 completions of
    one top core) breaks the claimed L=1 bound and the scanner detects
    it (worst ratio 6.00 at R = that core) — the hypothesis is
    load-bearing;
[7] Corollary G2 exhaustively on J(9,4) (|Z| <= 2, r <= 2, 1377 cells
    per family, L in {1,2});
[8] interface arithmetic: A + j == n and n-j+1 == A+1 on the five
    pinned qx14 rows; log2 eps printed for L_tan in {1,2}.
```

To refresh the pinned certificate:

```bash
python3 experimental/scripts/verify_qx11_topcore_globalness.py --write-certificate
```
