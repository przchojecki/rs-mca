# X1: Interleaved Deep-Point Bridge (list -> interleaved CA/MCA, forward direction)

- **Status:** AUDIT (base identity, independently reproduced) / PROVED + PROVED-by-check
  (interleaved identity §2, a-regular collapse §2.3, overlap-graph §2.4, L2->L1
  reduction + clique cap §2.6) / CONDITIONAL (protocol budget §2.8, on the L1
  bound) / PROVED-by-check (extension-line forward case §2.10 over `F_{p^2}`).
  Self-contained forward-bridge note covering X1, L2, M2, and F1 (simple-pole).
- **Agent/model:** Claude Opus 4.8 (L2 loop, branch `allen/l2-x1-interleaved-mca`).
- **Date:** 2026-06-23 / 2026-06-24.
- **Scope:** Problem X1 (list <-> CA/MCA without square-root loss) and L2
  (interleaved-list constants), `agents.md`. Builds on
  `notes/f1/f1_deep_point_list_to_ca_mca.md` (avdeevvadim, Theorem 1.1/2.2) and
  `notes/l2/l2_interleaved_dilation_constants.md` (our L2 sharp-constant target).
  Does not edit Papers A--D.

## Lane / non-overlap statement

This note is the **forward, interleaved** half of the deep-point program:
turning interleaved *list upper bounds* (L2) into interleaved/curve **MCA**
bad-slope counts for `RS[F,D,k]`. It deliberately does **not** touch the
base-code *cap* / counterexample-arithmetic direction (consume a list *lower*
bound to cap `delta*`), which is the subject of the active M1 audit PR #100
(`codex/m1-cycle120-gate-audit`, the `n=512,k=256,delta=125/256` row). Files
here live under `notes/x1/`, `notes/l2/`, and `scripts/verify_x1_*` /
`scripts/verify_l2_*`; they do not collide with `notes/m1/` or `verify_m1_*`.

**Deference to the parallel Codex PRs.** Two later Codex PRs now own the M2 and
F1 lanes substantively, and the M2/F1 *touches* in this note (§2.7, §2.9-§2.10)
are subordinate cross-references, not competing claims:

- **M2** — PR #102 (`m2_abf_gg_line_decoding_parameter_match`) is the protocol
  parameter-match `epsilon_mca(C,delta) = LD_sw(C, ceil((1-delta)n))/|F|` under
  the ABF/GG convention. Our §2.7 only records that on the *simple-pole* family
  MCA = CA = line-decoding coincide; it defers to #102 for the parameter ledger.
- **F1** — PR #103 (`f1_fixed_rate_extension_counterexample`) proves extension
  lines give a *lower* bound on `emca` (a counterexample). Our §2.9-§2.10 give
  the complementary *upper* structure (the extension line is the `M_z`-slice of
  the interleaved bridge, list-controlled). These are consistent (see §2.10
  remark); #103 owns the F1 lower-bound/counterexample statement.

## Claim and results ledger

This note develops the **forward** direction of the deep-point bridge for the
*interleaved* object, turning interleaved list bounds (L2) into interleaved-MCA
bad-slope counts (X1) for `C = RS[F,D,k]`, consuming the `C_+ = RS[F,D,k+1]`
list at the same radius `delta_a = 1-a/n`, `a > k`.

| § | Result | Status |
|---|--------|--------|
| 1 | Base deep-point identity `Bad_CA = Bad_MCA = Deep_alpha(U,a)` | AUDIT (independently reproduced, 312 checks, all `alpha in F_p\D`) |
| 2 | Interleaved `mu`-row identity `BadVec(alpha;a) = Deep_alpha^{mu}(U,a)`; `mu`-independent transfer constant (`<= k` collisions) | PROVED + PROVED-by-check |
| 2.2 | Forward count chain `avg_lb <= BadVec_max <= L <= Cartesian`; interleaved list `L` constant in `mu` | PROVED-by-check |
| 2.3 | a-regular regime: worst-case interleaved list `= base list`, all `mu` (interleaving exponent exactly 1) | PROVED |
| 2.4 | `interleaved(mu=2) = #edges` of `>=a`-overlap graph; tight `=>` matching; over-agreement `=>` degree `>= 2` (hypothesis of §2.3 necessary) | PROVED + PROVED-by-check |
| 2.5 | `K_{2,2}` witness: interleaving amplifies beyond both rows (`4 > max(L_1,L_2)`), but below base | PROVED-by-check |
| 2.6 | L2 -> L1 reduction `Lst(Int) <= Lst(C_+)^mu` (= `Lst(C_+)` a-regular); `K_{m,m}` clique cap `n >= k+m^2(a-k)` | PROVED + PROVED-by-check |
| 2.7 | Line-decoding reading (M2): `LD = Bad_MCA = Bad_CA = Deep_alpha` coincide on the simple-pole family | AUDIT / PROVED-by-check |
| 2.8 | Conditional protocol budget: `Lst(C_+) <= n^B` => interleaved-MCA term `<= n^{eB}/q`; small `B` clears `2^-128` | PROVED (conditional on L1) |
| 2.9 | Extension-line outlook (F1): the `F`-line is the `M_z`-coupled slice of the `e`-fold interleaved bridge | OUTLOOK |
| 2.10 | Extension-line forward case realized over `F_{p^2}`: base identity, list control, `M_z` transfer | PROVED-by-check |

**What is proved.** The forward interleaved bridge is complete and `mu`-clean: an
interleaved list bound transfers to an interleaved-MCA bad-slope count at the
same radius with **no square-root loss and no interleaving exponent** (§2, §2.2).
In the generic **a-regular** regime the worst-case interleaved list **equals the
base-code list** for every `mu` (§2.3) -- the sharp L2 constant is the base
(`= L1`) constant, exponent exactly 1, the honest L2 -> L1 reduction. The
interleaved list is exactly the `>=a`-overlap graph edge count (§2.4).

**What remains open.** Whether `Lst(Int(C_+,mu)) > Lst(C_+)` can ever hold in the
**over-agreement** regime. §2.6 reduces this to L1: `Lst(Int) <= Lst(C_+)^mu`
always (`= Lst(C_+)` when a-regular), so the exact exponent in `[1,mu]` is
governed by the base (L1) list, and the only constructive amplification route
(`K_{m,m}` cliques) is geometrically capped at `n >= k+m^2(a-k)` and cannot beat
a large base list. The residual is whether a non-clique configuration pushes the
worst-case exponent strictly above `1` -- an L1-governed question.

## Paper-label crosswalk (promotion aid)

Which paper statement each result bears on (labels per
`notes/audits/theorem_label_map.md`; this note does not edit Papers A--D):

| § | Bears on | How |
|---|----------|-----|
| 1, 2 | `prob:X1` (list <-> CA/MCA); `notes/f1/f1_deep_point_list_to_ca_mca.md` Thm 1.1 | forward, √-loss-free list -> (interleaved) MCA; independently audited + extended to interleaving |
| 2.3, 2.6 | `slackMCA_v3.tex` `conj:prefix-local` / `conj:arbitrary-local` | the interleaved (L2) list is governed by the base (L1) list: `Lst(Int) <= Lst(C_+)^mu`, `= Lst(C_+)` a-regular -- so L2 needs no theorem beyond `conj:prefix-local` |
| 2.7 | Paper C line-decoding ledger (`snarks_v4.tex`) / M2 | MCA = CA = line-decoding coincide on the simple-pole family |
| 2.2, 2.8 | `snarks_v4.tex` `thm:ledger`, interleaving/list budget | the interleaved-list soundness term is `Lst/q` with no Cartesian `mu` exponent; small L1 exponent `B` clears `2^-128` |
| 2.9, 2.10 | `prob:F1`; Paper C `ass:extension-mca-lift`; Paper D `cor:Fvalued` | the extension `F`-line is the `M_z` multiplication-slice of the `e`-fold interleaved bridge; realized over `F_{p^2}` |

Net for promotion: this note supplies the **forward** (positive) direction of
`prob:X1` for the simple-pole family and reduces the L2 interleaved-list ledger
to the L1 `conj:prefix-local` target, with the protocol budget made explicit.

## 1. Base identity, independently audited

Theorem 1.1 of the deep-point note states, for `U : D -> F`, a deep point
`alpha in F \ D`, the simple-pole line

```text
f_alpha(x) = U(x)/(x-alpha),   g_alpha(x) = -1/(x-alpha),
```

and `k < a <= n`, `delta_a = 1 - a/n`:

```text
Bad_CA(f_alpha,g_alpha; delta_a)
  = Bad_MCA(f_alpha,g_alpha; delta_a)
  = Deep_alpha(U,a)
  = { P(alpha) : P in F[X]_{<k+1}, |{x in D : P(x)=U(x)}| >= a }.
```

The proof (note §1) is clean: forward, `Q(X)=(P(X)-P(alpha))/(X-alpha)` has
degree `< k` and explains `f_alpha + P(alpha) g_alpha` on the agreement support;
the global far condition is that `g_alpha` has no degree-`<k` explanation on any
support of size `> k` (else `H(X)=(X-alpha)G(X)+1` would vanish at `> k` points
yet `H(alpha)=1`). Reverse: multiply the support identity by `(x-alpha)`.

**Independent reproduction.** `scripts/verify_x1_deep_point_identity.py`
re-derives the three sets from scratch in a model independent of the existing
`f1_deep_point_list_to_ca_mca_sanity.py`:

- prime field `F_p` only, so the deep point `alpha` ranges over **all** of
  `F_p \ D` (prime-field deep points, not only an extension-valued `alpha=t`);
- many received words per configuration (monomial-prefix, degree-`k`, and
  several deterministic pseudo-random words), not one hand-picked word;
- `Bad_CA`, `Bad_MCA`, `Deep_alpha` each computed by a separate brute force and
  asserted mutually equal.

Result: PASS over `(p,n,k,a) in {(17,8,3,5),(17,8,4,6),(17,16,8,12),(41,8,3,5)}`,
**312 identity checks** (e.g. `p=41,n=8`: 33 deep points x 6 words). The global
far condition holds at every prime-field deep point in every configuration. This
upgrades the base identity from "one extension-field example" to "all
prime-field deep points x many words across four fields", with no exception.

## 2. Interleaved deep-point bridge (the new target)

Let `U=(U_1,...,U_mu) : D -> F^mu` be a `mu`-row received word and let `Int(C,mu)`
be the `mu`-fold interleaving of `C=RS[F,D,k]` with **column distance**
(common agreement support). Fix a deep point `alpha in F \ D` and form the
*shared-pole* curve

```text
f_alpha^{(i)}(x) = U_i(x)/(x-alpha),    g_alpha(x) = -1/(x-alpha),   i=1..mu,
```

i.e. the same denominator `(x-alpha)` in every row. A slope **vector**
`z=(z_1,...,z_mu) in F^mu` is *interleaved-MCA-bad* at radius `delta_a` if there
is a common support `S`, `|S| >= a`, on which every row
`f_alpha^{(i)} + z_i g_alpha` is explained by `C`, while the curve is not
simultaneously explained on any support of size `> k`.

**Target Theorem (interleaved deep-point identity).** Define the
*interleaved deep image*

```text
Deep_alpha^{mu}(U,a)
  = { (P_1(alpha),...,P_mu(alpha)) :
      P_i in F[X]_{<k+1},
      |{x in D : P_i(x)=U_i(x)  for all i}| >= a }.
```

Then the interleaved-MCA-bad slope vectors of the shared-pole curve at
`delta_a` equal `Deep_alpha^{mu}(U,a)`; in particular

```text
|Bad_MCA^{int}(alpha; delta_a)| = |Deep_alpha^{mu}(U,a)| <= |Lambda(Int(C_+,mu), delta_a, U)|,
```

the interleaved (column-distance) list of `C_+ = RS[F,D,k+1]` at radius
`delta_a`. The forward inclusion is the per-row computation of §1 applied on the
**common** support `S` (the same `Q_i(X)=(P_i(X)-P_i(alpha))/(X-alpha)` has
degree `< k`); the reverse multiplies each row identity by `(x-alpha)` and uses
that the shared far condition for `g_alpha` is exactly the §1 far condition,
independent of `mu`.

**Why this is the L2 payoff (mu-independent transfer).** For the averaging
(Lemma 2.1 analogue), two *distinct* interleaved tuples `(P_i^{(s)})` and
`(P_i^{(t)})` differ in some row `i0`, and `{alpha : P_{i0}^{(s)}(alpha) =
P_{i0}^{(t)}(alpha)} <= k`. Hence the simultaneous-collision set has size `<= k`
**regardless of `mu`**, so the deep-point evaluation expansion gives the *same*

```text
M >= L / (1 + k(L-1)/|Omega|)
```

bound for the interleaved tuple list as for a single row. Combined with the L2
result that the interleaved list numerator does not pay the Cartesian exponent
(`l2_interleaved_dilation_constants.md` §2-§5: `binom(n,a) q^{-mu(a-k)} +
Quot_mu`), this says: **interleaving multiplies neither the transfer constant nor
the list numerator** -- the forward list->MCA conversion is `mu`-clean. This is
the positive/forward counterpart of the negative cap direction, and the exact
statement Paper C needs to consume interleaved lists as interleaved MCA.

## 2.1 Numerical confirmation (`verify_x1_interleaved_deep_point.py`)

The verifier builds full interleaved (column-distance) lists, deep images, and
bad-slope-vector sets by independent brute force and checks all three claims:

- **(A) identity** `BadVec(alpha;a) = Deep_alpha^{mu}(U,a)` for every tested
  word and deep point. Exercised on structured aligned quotient-locator words
  (and a dilated second row for genuinely non-diagonal interleaving) over
  `F_97, n=16, k=8, a=12`: at both `mu=2` and `mu=3` the interleaved list has
  size `L=4` and `|Deep^{mu}| = |BadVec| = 4`. The list size is **unchanged from
  `mu=2` to `mu=3`** -- interleaving does not grow it -- matching the L2
  no-Cartesian-exponent result.
- **(B) list bound** `|Deep_alpha^{mu}(U,a)| <= |interleaved C_+ list|` holds in
  every case.
- **(C) `mu`-independent collision bound.** A constructive demo over `F_97`,
  `k=8`: two distinct interleaved tuples differing in one row by
  `V = prod_i (X-d_i)` (`deg V = j <= k`, roots `d_i` deep points) agree on
  exactly `j` deep points; choosing `j=k` achieves collision `= k`, and `deg V`
  cannot exceed `k` while keeping the row in `RS_{<k+1}`. The achieved maximum is
  `k=8` and never exceeds `k`, **identically for `mu=1,2,3`**. This is the exact
  fact behind the `mu`-independent `M >= L/(1+k(L-1)/|Omega|)` expansion.

Result: PASS (configs `(p,n,k,a,mu)` = `(97,16,8,12,{2,3})` structured, plus
small spread cases for the collision scan).

## 2.2 Forward interleaved-MCA count (verified)

Combining §2 (identity), the §1 averaging (Lemma 2.1, applied to the interleaved
tuple list with the `mu`-independent `<= k` collision bound), and the L2 saving
gives the explicit forward count chain, for the shared-pole curve of a `mu`-row
word `U`:

```text
ceil( L / (1 + k(L-1)/|Omega|) )
   <=  BadVec_max  =  max_{alpha in Omega} |Deep_alpha^{mu}(U,a)|     (forward MCA count)
   <=  L           =  |Lambda(Int(C_+,mu), 1-a/n, U)|                 (interleaved C_+ list)
   <=  prod_i L_row_i                                                 (Cartesian product).
```

The protocol consequence: the interleaved-MCA bad-slope-vector density is
`|BadVec|/q^{mu} <= L/q^{mu}`, with `L` the L2-controlled interleaved list, **not**
the naive `(L_row/q)^{mu}`.

`verify_x1_forward_interleaved_count.py` confirms the full chain on structured
quotient-locator words (row 0 plus dilated rows, genuinely non-diagonal) over
`F_97` and `F_193`, `n=16, k=8, a=12`:

| p | mu | L_row | Cartesian | L (interleaved) | BadVec_max | avg_lb | L/Cart |
|---|---|---|---|---|---|---|---|
| 97 | 2 | [4,4] | 16 | 4 | 4 | 4 | 0.250 |
| 97 | 3 | [4,4,4] | 64 | 4 | 4 | 4 | 0.0625 |
| 193 | 2 | [4,4] | 16 | 4 | 4 | 4 | 0.250 |
| 193 | 3 | [4,4,4] | 64 | 4 | 4 | 4 | 0.0625 |

The interleaved list `L=4` is **constant in `mu`** while the Cartesian product
grows as `4^{mu}`; the forward interleaved-MCA count `BadVec_max` equals `L` and
inherits the saving.

*Relation to the L2 `Quot_mu`.* The `Quot_mu` term of the sharp-constant
conjecture is the aligned quotient-core count `L_mu(a,tau) = sum_{c=h}^{ell}
binom(Q,c) E_empty(Q-c,ell-c,mu)` (`notes/l2/l2_interleaved_dilation_constants.md`
§4; brute-validated in `scripts/verify_l2_quotient_core_count.py`), with diagonal
endpoint `binom(Q,ell)` at `a=k+sigma`. This is the **combinatorial maximum** of
the structured contribution -- the count of *all* `mu`-tuples of coset-union
packets -- not a single word's list: it upper-bounds, and is generally not equal
to, the structured part of a given `L` (e.g. at `n=16,k=8,M=2` the diagonal
`L_mu = binom(7,4) = 35`, while the heavy quotient-locator word above realizes
only the `4` packets consistent with it). So the right reading is
`structured part of Lst(Int) <= Quot_mu` (diagonal, not Cartesian), exactly as the
L2 §4 count states; the per-word `L=4` here is one such realization. No separate
alignment is needed.

## 2.3 Worst-case interleaved list = base list (a-regular regime)

The §2.2 chain bounds the forward count by the interleaved list `L`. This section
pins the worst case of `L` itself. Using the bridge note's full-agreement
formula (`l2_interleaved_support_bridge.md`, PROVED)

```text
|Lambda(Int(C_+,mu),1-a/n,U)|
  = #{ (A_1,...,A_mu) : A_i in Supp_{U_i}^{>=a}, |A_1 cap ... cap A_mu| >= a },
```

call a row word `V` **a-regular** if every `C_+`-codeword agreeing with `V` on
`>= a` points agrees on exactly `a` (the generic maximal-radius case; distinct
`C_+ = RS[F,D,k+1]` codewords agree on `<= k < a` points).

**Theorem.**
- (i) *(diagonal lower bound, any words)* `Lst(Int(C_+,mu),1-a/n) >=
  Lst(C_+,1-a/n)` for every `mu`, with equality of the diagonal word's
  interleaved list and the base list (off-diagonal tuples are impossible: two
  distinct codewords share `<= k < a` points).
- (ii) *(a-regular upper bound)* if every row `U_i` is a-regular then
  ```text
  |Lambda(Int(C_+,mu),1-a/n,U)| = | intersect_i Supp_{U_i}^{=a} | <= min_i |Lambda(C_+,1-a/n,U_i)|.
  ```
  *Proof.* `|A_i| = a` and `|intersect A_i| >= a` force every `A_i` to equal the
  common `a`-set `T`, so the tuple is `(T,...,T)` with `T` a full agreement
  support of every row; `tuple <-> T` is a bijection onto
  `intersect_i Supp_{U_i}^{=a}`. ∎

Combining (i) and (ii): **in the a-regular regime the worst-case interleaved
list equals the base-code list for every `mu` -- the interleaving exponent is
exactly `1`, not `mu`.** Via §2, the interleaved-MCA bad-slope-vector count is
then governed by the base-code list, `mu`-independently; and the base list is
exactly the L1 locator-fiber object, so the L2 worst-case constant coincides
with the L1 constant in this regime (the honest reduction L2 -> L1).

`verify_x1_worst_case_interleaved.py` confirms (i), (ii), and the exact formula
`|interleaved| = |common supports|` over `F_97`/`F_193`, `n=16,k=8,a=12`, for
`mu=1,2,3` (a-regular quotient-locator words; base list `4`, interleaved `4` at
every `mu`).

## 2.4 The interleaved list as an overlap-graph edge count, and the open core

§2.3 left the non-a-regular (over-agreement) regime open. This section localizes
it exactly. For `mu=2`, the full-agreement formula reads

```text
|Lambda(Int(C_+,2),1-a/n,(U_1,U_2))|
  = #{ (c_1,c_2) in list(U_1) x list(U_2) : |A_{c_1}(U_1) cap A_{c_2}(U_2)| >= a }
  = #edges of the bipartite ">=a-overlap" graph G(list U_1, list U_2).
```

**Tight-support degree bound (PROVED).** A codeword whose full agreement support
has size exactly `a` has degree `<= 1` in `G`: if two opposite-side codewords
both have support meeting it in `>= a = |support|` points, both supports contain
that `a`-set, so the two codewords agree on `> k` points and coincide. Hence
**a-regular rows make `G` a matching**, giving `|interleaved| <= min row list <=
base`, which re-derives the §2.3 collapse purely from the graph.

**Over-agreement breaks the matching (PROVED-by-check).** A codeword with support
`> a` can have degree `>= 2`. Witness over `F_97, n=16, k=4, a=8`
(`verify_x1_overlap_graph.py`): an over-agreeing `c_2` with support `2a-k = 12`
is adjacent to two tight row-1 codewords `c_1, c_1'` (built on overlapping
`a`-sets `S, S'` inside `A_2`), so `deg(c_2)=2`. The edge-count identity
`interleaved == edges` holds in both the tight and the witness case.

**Consequence / open core.** The §2.3 a-regular hypothesis is *necessary*: drop
it and `G` need not be a matching. For the worst-case interleaved list to
*exceed* the base list one needs the edge count to beat the larger side, which
requires **simultaneous over-agreement on both rows** (codewords of support `> a`
on each side with compatible overlaps). This is geometrically constrained: two
same-row codewords of support `b` overlap in `<= k`, forcing `n >= 2b-k`, so the
construction needs `n` large relative to `a`. The witness above already has a
degree-2 vertex but `interleaved = 2 = L_1` (a single over-agreeing `c_2`), so it
does not beat base. **Whether `Lst(Int(C_+,mu)) > Lst(C_+)` ever holds is the
precise open over-agreement core of L2**, now reduced to a bipartite/hypergraph
overlap-density question rather than a vague "Cartesian exponent" worry.

## 2.5 Interleaving amplification: a concrete K_{2,2} over-agreement witness

§2.4 said a separation needs two-sided over-agreement. This section realizes the
smallest such design with actual codewords and measures it.

Over `F_41, n=20, k=4, a=8` (so `C_+ = RS` deg `<= 4`; distinct codewords agree
on `<= 4 = k`; over-agreement support `2a-k = 12`), choose four size-12 supports

```text
A_1,A_2  (row 1),   B_1,B_2  (row 2),   |A_i cap A_j| = |B_i cap B_j| = 4 = k,
all four cross overlaps |A_i cap B_j| = 8 = a,
```

realized by codeword pairs agreeing exactly on a shared `k`-set `T`
(`g_2 = g_1 + prod_{x in T}(X-x)`) and words `U_1,U_2` producing exactly those
agreement supports. The `>=a`-overlap graph is then the complete bipartite
`K_{2,2}`. `verify_x1_interleaving_amplification.py` measures (all by brute force):

```text
interleaved list = 4 = edges,   L_1 = 3,   L_2 = 2,   max supports = (12, 12) > a.
```

So **`interleaved = 4 > 3 = max(L_1, L_2)`: interleaving strictly amplifies beyond
the larger participating row list** -- impossible in the a-regular regime (§2.3,
`interleaved <= min row list`). This is the over-agreement effect, realized.

**But it does not beat the global base.** At these parameters a single
quotient-locator word already has a row list of `10`, so `interleaved = 4` is far
below `Lst(C_+)`; this is amplification beyond the *participating* rows, not a
`Lst(Int(C_+,mu)) > Lst(C_+)` separation. A true separation needs a `K_{m,m}`
overlap design giving `interleaved = m^2 > Lst(C_+)`, i.e. the overlap design
must scale (larger `n`) faster than the base list grows. **That scaling question
is the sharp open core of L2**, and §2.4's overlap-graph reduction is the tool to
attack it. Net honest status: interleaving can exceed both rows in the
over-agreement regime, but no worst-case-vs-base separation is exhibited at toy
scale; the a-regular collapse (§2.3) remains the proven worst-case statement.

## 2.6 L2 reduces to L1, and the clique-amplification cap

Two honest statements close the over-agreement analysis (without claiming the
open separation either way).

**(R) Reduction (PROVED).** Since the interleaved list is the `>=a`-overlap edge
count (§2.4), for every `mu`-row word
```text
|Lambda(Int(C_+,mu),delta_a,U)|  <=  prod_i |Lambda(C_+,delta_a,U_i)|  <=  Lst(C_+,delta_a)^mu,
```
and `= Lst(C_+,delta_a)` in the a-regular regime (§2.3). Hence **the worst-case
interleaved list is polynomial iff the base (L1) list is**: the L2 interleaved
problem reduces to the L1 base-list problem, with exponent in `[1,mu]` (exactly
`1` when a-regular). An L1 bound `Lst(C_+) <= n^B` immediately gives
`Lst(Int(C_+,mu)) <= n^{mu B}`. No separate L2 list theorem is needed; the
trivial Cartesian exponent `mu` is the worst case and `1` the generic case.

**(C) Clique cap (PROVED).** The only known constructive way to push the exponent
above `1` is the `K_{m,m}` two-sided over-agreement design (§2.5). It is
geometrically capped: `m` row-1 supports sharing exactly the `k`-set `T` have
pairwise-disjoint non-`T` parts (similarly row 2), and each of the `m^2` cells
`A_i cap B_j` needs `>= a-k` non-`T` points, so
```text
n  >=  k + m^2 (a - k).
```
Thus a `K_{m,m}` clique realizes `interleaved = m^2` only at `n >= k+m^2(a-k)`;
its amplification `m^2 <= (n-k)/(a-k)` is **linear in `n`**. Beating the base via
this route needs `Lst(C_+) < (n-k)/(a-k)` -- a base list already linear-small,
i.e. never the hard large-list L2 regime. `verify_x1_clique_cap.py` builds the
grid designs for `m=2,3,4` (`n=20,40,68`, `edges=4,9,16`, supports `12,16,20 > a`)
and cross-checks `m=2` against the field-realized construction of §2.5.

**Net.** The L2 sharp-constant question is governed by L1: exponent `1` generically
(§2.3), `<= mu` always (R), and the only clique route to a strict increase is
capped (C) and cannot beat a large base list. Whether a non-clique configuration
pushes the *worst-case* exponent strictly above `1` while exceeding the base
remains open, but it cannot come from the `K_{m,m}` family and is bounded by the
L1 list either way.

## 2.7 Line-decoding reading (M2)

The simple-pole family is a concrete **line**, so the bridge has a line-decoding
reading useful for Paper C. The line-decoding list of `f_alpha + z g_alpha` at
radius `delta_a` is the set of slopes whose line passes within `delta_a` of a
codeword of `C = RS[F,D,k]`:
```text
LD(alpha; delta_a) = { z : exists c in C, |{x : f_alpha(x)+z g_alpha(x)=c(x)}| >= a }.
```
By §1, `f_alpha + z g_alpha` is `delta_a`-close to `C` iff `z in Deep_alpha(U,a)`,
so
```text
LD(alpha; delta_a) = Bad_MCA(alpha; delta_a) = Bad_CA(alpha; delta_a) = Deep_alpha(U,a).
```

**Coincidence (M2).** On the simple-pole line family, support-wise **MCA**,
no-loss **CA**, and **line-decoding** all coincide -- each equal to the deep
image. So there is **no MCA-vs-line-decoding separation on this family**; any
genuine separation (M2's "small MCA but large line-decoding, or vice versa")
must come from *other* line families. A single slope may carry several closing
codewords (distinct `C_+` list elements `P` with equal `P(alpha)`), so the
`(z,c)` incidence multiplicity equals the relevant list size, while the slope
count `|LD| = |Deep_alpha| <= |Lambda(C_+,delta_a,U)|`.

Parameters: radius `delta_a = 1-a/n`, line pencil `{f_alpha + z g_alpha}`,
decoding-list size `<= |Lambda(C_+,delta_a,U)|`. The interleaved `mu`-row
shared-pole curve has simultaneous line-decoding list `Deep_alpha^{mu}(U,a)`
(§2). `verify_x1_line_decoding.py` confirms the coincidence across
`(p,n,k,a) in {(17,8,3,5),(17,8,4,6),(41,8,3,5)}` (306 checks), reporting the
list multiplicity per slope. For the protocol-facing M2 parameter ledger
(`epsilon_mca = LD_sw/|F|` under the ABF/GG convention) this defers to PR #102.

## 2.8 Conditional protocol budget: what an L1 bound buys

The forward bridge (§1-§2) and the L2 -> L1 reduction (§2.6) compose into a
conditional statement that lands the protocol impact.

**Conditional theorem.** Suppose the L1 generated-field locator bound holds above
the corrected reserve, `Lst(C_+, delta_a) <= n^B`. Then:
```text
Lst(Int(C_+,mu), delta_a)            <= n^{mu B}   (worst case, §2.6)
                                     <= n^{B}      (a-regular regime, §2.3)
interleaved-MCA bad-slope count      <= Lst(Int(C_+,mu), delta_a)   (§2, no sqrt loss)
```
so the Proximity-Prize soundness schematic (readme),
`MCA_error + |interleaved_list|/|challenge field| + query_error`, has its
interleaved term bounded by `n^{mu B}/q` (worst case) or `n^{B}/q` (a-regular).
**An L1 list theorem converts directly into the interleaved-MCA / interleaved-list
soundness budget Paper C consumes** -- no separate MCA theorem, no square-root
loss, and no Cartesian `mu` exponent in the generic case.

**Budget.** `verify_x1_conditional_budget.py` prints the largest L1 exponent `B`
for which the interleaved term already clears `2^-128` over `|F| < 2^256`
(`e*B*log2 n <= log2 q - 128`, `e in {1, mu}`). E.g. at `n = 2^40`:

| mu | a-regular `B <=` | worst-case `B <=` |
|---|---|---|
| 1 | 3.2 | 3.2 |
| 2 | 3.2 | 1.6 |
| 3 | 3.2 | 1.067 |

A **polynomial L1 list bound with a small exponent suffices** for the entire
prize regime once routed through the bridge -- which is exactly what the L1
program (`l1_prefix_divisor_count.md`, `conj:prefix-local`) is trying to prove.

## 2.9 Extension-line outlook (connection to F1)

*Status: OUTLOOK / connection (composes proved pieces; full F1 development is its
own lane). No new claim beyond the cited results.*

The interleaved bridge specializes to **extension `F`-lines** and meets the F1
program. Let `B subset F` have degree `e`, `D subset B`, and fix a `B`-basis to
get the coordinate map `Phi` with `Phi(C_F) = C_B^e`
(`notes/f1/f1_extension_coordinate_transfer.md`, PROVED). For the simple-pole
`F`-line at a deep point `alpha in F \ D`:

1. by §1-§2 over `F`, its support-wise MCA-bad slopes are the `F`-valued deep
   image `Deep_alpha(U,a)`, i.e. the `alpha`-evaluation of the
   `C_{F,+} = RS[F,D,k+1]` list;
2. by the extension-coordinate list identity
   (`notes/l2/l2_interleaved_dilation_constants.md` §6;
   `tex/snarks_v4.tex` `eq:extension-list`), `|Lambda(C_F,delta_a)| =
   |Lambda(Int(C_B,e),delta_a)|`, so that list is the `e`-interleaved base-code
   list;
3. by the F1 transfer, `Phi` carries the `F`-line to the **multiplication-slice**
   family `Phi(f)+M_z Phi(g)` inside `C_B^e`, where the scalar `z in F` becomes
   the multiplication matrix `M_z`.

So the simple-pole **extension-line is a one-parameter, matrix-coupled slice of
the `e`-fold interleaved bridge of §2** (`mu = e`): its MCA-bad slopes are the
deep image, list-controlled by the `e`-interleaved base list. The only
difference from the free `F^e` slope vectors of §2 is the `M_z` coupling -- the
extension challenge restricts to the `1`-parameter slice. This connects the
forward bridge to `prob:F1` (extension-line MCA) and shows the F1 object is the
matrix-parameter restriction of the L2/X1 object developed here; a sharp F1
constant would specialize the §2.6 reduction to the multiplication-slice family.
Full F1 development is deferred to the F1 lane.

## 2.10 Extension-line forward case, realized (F1)

§2.9 outlined the extension-line connection; this section develops and verifies it
for the simple-pole family. Over `B = F_p`, `F = F_{p^2}`, `D subset B`, the
simple-pole `F`-line at an extension-valued deep point `alpha in F \ D` is
realized and `verify_x1_extension_line.py` confirms (over `F_{17^2}`, `alpha=t`):

1. **Base identity over the extension.** `Bad_MCA_F(alpha; delta_a) =
   Deep_alpha^F(U,a)` for `F`-valued words and an extension-valued `alpha` --
   extending the §1 audit (prime-field deep points) to the genuine extension
   setting. Verified including a planted word with a non-trivial extension list
   (`|Deep^F| = 5` at `n=8,k=3,a=5`).
2. **List control.** `|Deep_alpha^F(U,a)| <= |Lambda(C_{F,+},delta_a,U)|`, and by
   the extension-coordinate identity `|Lambda(C_F)| = |Lambda(Int(C_B,2))|`
   (`notes/l2/l2_interleaved_dilation_constants.md` §6), the `F`-line MCA is
   governed by the **`2`-interleaved base-code list** -- i.e. the L2/X1 object of
   §2 with `mu = e = 2`.
3. **Multiplication-slice transfer.** Under `Phi` (`Phi(C_F) = C_B^2`), each
   `F`-bad slope `z` yields a closing `F`-codeword whose coordinate words are
   both `deg < k` over `B`, i.e. `Phi(f_alpha) + M_z Phi(g_alpha) in C_B^2|_S`
   (`notes/f1/f1_extension_coordinate_transfer.md`). So the extension `F`-line is
   exactly the `M_z`-coupled slice of the `e=2` interleaved bridge.

This realizes the F1 forward direction for the simple-pole family (`prob:F1`):
extension-line MCA bad slopes are the `F`-valued deep image, list-controlled by
the interleaved base list, with the scalar `z in F` acting as the multiplication
matrix `M_z`. It composes the deep-point identity (§1-§2), the extension-coordinate
list identity (§2.9), and the F1 transfer into one verified forward statement; the
general (non-simple-pole) F1 lift remains the open F1 question.

**Remark (consistency with PR #103).** This is an *upper* structure, not a
positivity claim. PR #103 (`f1_fixed_rate_extension_counterexample`) proves a
matching *lower* bound: degree-`>= 1` extension lines force
`emca(C_F, 1-(k+sigma)/(p-1)) >= (1-rho)^{sigma+1}/(sigma+1)! - o(1)`, with
higher-degree numerator amplification giving constant-density counterexamples in
every fixed extension degree. The two are consistent and complementary: §2.10
says the extension-line bad slopes *are* the (interleaved-list-controlled) deep
image; #103 says that image is *large* in this regime. So the extension case is a
genuine counterexample regime — the bridge transfers it faithfully, it does not
make it small. #103 owns the F1 lower-bound statement; §2.10 owns the structural
identification with the `e`-fold interleaved bridge.

## 3. Plan (incremental commits on this PR)

1. (done) Independent audit + broadened verifier of the base identity (§1).
2. (done) Interleaved identity (§2) + `scripts/verify_x1_interleaved_deep_point.py`
   confirming `Bad_MCA^{int} = Deep_alpha^{mu}`, the list bound, and the
   `mu`-independent collision bound (§2.1).
3. (done) Forward X1 count chain (§2.2) +
   `scripts/verify_x1_forward_interleaved_count.py`: explicit
   `avg_lb <= BadVec_max <= L <= Cartesian`, with `L` constant in `mu`.
4. (done) Worst-case interleaved list = base list in the a-regular regime
   (§2.3) + `scripts/verify_x1_worst_case_interleaved.py`: interleaving exponent
   exactly 1; the honest L2 -> L1 reduction.
5. (done) Overlap-graph reduction (§2.4): interleaved (mu=2) = bipartite
   >=a-overlap edge count; tight => matching (=> §2.3); over-agreement => degree
   >= 2 (a-regular hypothesis necessary). `scripts/verify_x1_overlap_graph.py`.
6. (done) K_{2,2} amplification witness (§2.5): `interleaved=4 > max row list=3`
   in the over-agreement regime, but below the base; `verify_x1_interleaving_amplification.py`.
7. (done) §2.6: L2 -> L1 reduction (`Lst(Int) <= Lst(C_+)^mu`) + `K_{m,m}` clique
   cap (`n>=k+m^2(a-k)`); `scripts/verify_x1_clique_cap.py`.
8. (open) whether a NON-clique configuration pushes the worst-case exponent
   strictly above 1 while exceeding the base -- bounded by the L1 list (R), not
   from the clique family (C). This is now an L1-governed residual.
9. (done) §2.7 line-decoding reading (M2): MCA = CA = line-decoding coincide on
   the simple-pole family; `scripts/verify_x1_line_decoding.py`.
10. (done) §2.8 conditional protocol budget: an L1 bound `Lst(C_+)<=n^B` yields
    the interleaved-MCA soundness budget; `scripts/verify_x1_conditional_budget.py`.
11. (done) §2.9 extension-line outlook: the F-line is the `M_z`-coupled slice of
    the `e`-fold interleaved bridge (connection to prob:F1).
12. (done) §2.10 extension-line forward case realized over `F_{p^2}`:
    `scripts/verify_x1_extension_line.py` (base identity, list control, M_z transfer).
13. (done) Lean: `lean/rs_mca_formalization/RsMca/DeepPoint.lean` machine-checks
    the §2.6 clique-cap and §2.8 budget arithmetic (no `sorry`).

## Ledger impact

- **X1 (forward, new):** a square-root-loss-free list->MCA transfer in the
  interleaved setting, with a `mu`-independent transfer constant.
- **L2 (sharpened):** the interleaved-list bound becomes an interleaved-MCA
  statement, not merely a list statement.
- **Field ledger:** all objects stay over the same `F`; no `q_gen`/`q_chal`
  swap. The deep point `alpha` is in `F \ D`; the list is the `C_+ = RS[F,D,k+1]`
  list at the *same* radius `delta_a`.

## Reproducibility

```bash
python3 experimental/scripts/verify_x1_deep_point_identity.py
python3 experimental/scripts/verify_x1_deep_point_identity.py --json
python3 experimental/scripts/verify_x1_interleaved_deep_point.py
python3 experimental/scripts/verify_x1_interleaved_deep_point.py --json
python3 experimental/scripts/verify_x1_forward_interleaved_count.py
python3 experimental/scripts/verify_x1_forward_interleaved_count.py --json
python3 experimental/scripts/verify_x1_worst_case_interleaved.py
python3 experimental/scripts/verify_x1_worst_case_interleaved.py --json
python3 experimental/scripts/verify_x1_overlap_graph.py
python3 experimental/scripts/verify_x1_overlap_graph.py --json
python3 experimental/scripts/verify_x1_interleaving_amplification.py
python3 experimental/scripts/verify_x1_interleaving_amplification.py --json
python3 experimental/scripts/verify_x1_clique_cap.py
python3 experimental/scripts/verify_x1_clique_cap.py --json
python3 experimental/scripts/verify_x1_line_decoding.py
python3 experimental/scripts/verify_x1_line_decoding.py --json
python3 experimental/scripts/verify_x1_conditional_budget.py
python3 experimental/scripts/verify_x1_conditional_budget.py --json
python3 experimental/scripts/verify_x1_extension_line.py
python3 experimental/scripts/verify_x1_extension_line.py --json
(cd experimental/lean/rs_mca_formalization && lake build)
```
