# X1: Interleaved Deep-Point Bridge (list -> interleaved CA/MCA, forward direction)

- **Status:** AUDIT (base identity, independently reproduced) / PROVED + PROVED-by-check
  (interleaved identity §2 and the mu-independent collision bound).
- **Agent/model:** Claude Opus 4.8 (L2 loop, branch `allen/l2-x1-interleaved-mca`).
- **Date:** 2026-06-23.
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
inherits the saving. (Matching `L` to the exact L2 `Quot_mu` formula at aligned
prize parameters is a parameter-alignment check left for a later pass; the
structural fact -- diagonal, not Cartesian -- is what transfers here.)

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
6. (next) attack the open core: does simultaneous two-sided over-agreement ever
   give `Lst(Int(C_+,mu)) > Lst(C_+)`? search at `n >~ 2a`, or prove a general
   matching/Koenig-type bound forbidding it.

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
```
