---
workboard_item: M1
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: >-
  On the pinned c=2048, (u,v)=(0,1) quotient profile (punctured 1022-label
  domain of the integrated band_mixing / t16_mixing_floor packages), two
  dyadic levels govern the depth-32 collision structure. LEVEL LAW: a
  complete dyadic class of size d in {16,32} has p_k class-independent for
  k<d (zero for odd k, d*2^(29k)*C(k,k/2) for even k), first class-dependent
  at k=d, with p_16(c) = 8*C(16,8) + 8*xi_c and p_32(a) = 8*C(32,16) +
  8*eta_a, xi_c = psi16^c + psi16^-c (psi16 = g^(2^23) order 256), eta_a =
  psi32^a + psi32^-a (psi32 = g^(2^24) order 128), B16 = 102960, B32 =
  513675826. NESTING: T_32(a) = T_16(a) U T_16(128-a); the order-256
  xi-weights cancel (xi_{128-c} = -xi_c) and the order-128 eta-weight
  doubles, recovering the T_32 weight. SAME-REMAINDER (T_32-aligned): a
  depth-32 collision is one equation Sum eta equal; the exhaustive C(25,9)
  census at the pinned e=224 anchor gives the deficiency spectrum 192:10,
  224:40, 256:30, 288:4 (s_224 = 40; masking C(5,2)C(4,1)=40 vs naive
  C(5,2)C(6,1)=60). CROSS-REMAINDER (T_16-aligned): a depth-32 collision is
  exactly two equations {E16: Sum xi equal, E32: Sum eta equal},
  overshooting to locator-prefix agreement nu = 47 (break at k=48). The
  exhaustive o_e meet-in-the-middle census at the standard anchor gives
  o_64=49, o_128=441, o_96=0, and o_192 = 1225 whole-T_64 + 8 mixed = 1233,
  reproducing the integrated rooted degree; the mixing floor is at e=192.
architecture: M31_C2048_U0_V1_DYADIC_WEIGHT_LAWS_V1
partition_digest: SUPPORT-LEVEL pinned quotient profile; no first-match ledger atom assigned
atom_or_cell: Q / dyadic T_16 & T_32 collision-weight census
quantifier: >-
  The dyadic level laws and nesting hold for every complete T_16 and T_32
  class. Same-remainder: exhaustive over all C(25,9) nine-class selections
  at the pinned 479-point e=224 anchor. Cross-remainder: exhaustive
  meet-in-the-middle over the 28/28 T_16-fold pools of the standard anchor
  for e<=128, constructive at e=192 (reproducing the integrated rooted
  degree), plus an alternate-anchor e=96 consistency pair.
projection_and_unit: >-
  479-subsets of the 1022-label punctured quotient domain, depth-32 monic
  quotient-locator prefixes, and selected complete T_16 / T_32 classes. No
  received word, codeword, ray, or slope projection.
claimed_bound: >-
  Dyadic level law + closed forms p_16 = 8C(16,8)+8xi, p_32 = 8C(32,16)+8eta.
  Same-remainder spectrum 192:10, 224:40, 256:30, 288:4 (84 total; s_224=40).
  Cross-remainder two-equation law {E16,E32}; nu=47; o-census o_64=49, o_128=441,
  o_96=0, o_192=1233 (= 1225 whole-T_64 + 8 mixed = integrated rooted degree).
status: EXPERIMENTAL
impact: LOCAL_ONLY
falsifier: >-
  A same-remainder depth-32 collision whose selected-class weight sum Sum eta
  differs from the anchor's; a spectrum entry other than 192:10, 224:40, 256:30,
  288:4; a T_16-aligned cross-remainder collision violating {E16, E32}; a mixed
  witness with locator-prefix agreement other than 47; an o_e census value
  differing from 0/49/441/1233; or any recomputed constant (B16=102960,
  B32=513675826, the even constants, the thirty p32(a), eta, the counterfactual
  60, or the alternate-anchor sigma sums) differing from the value in the note.
replay: >-
  python3 experimental/scripts/verify_m31_dyadic_weight_laws.py --check and
  --tamper-selftest (self-contained stdlib; recomputes both dyadic level
  laws and closed forms, the nesting, the eta byte-match, the T_32
  same-remainder C(25,9) census with direct prefix checks (85
  weight-matches, 3000 non-match sample), the eight T_16-mixed witnesses
  (nu=47), the exhaustive o_e MITM census (t<=8) and the constructive
  o_192=1233, the 1723-pair sufficiency and the 1000-pair necessity samples,
  and the alternate-anchor e=96 pair; exit 0 iff all pass / iff every
  injected mutation is caught). Stdlib Lean arithmetic shadow: cd
  experimental/lean/m31_dyadic_weight_laws && lake build; the Lean shadow
  uses native_decide (nine identities involving large powers of two) and
  decide (seven small combinatorial facts), each theorem followed by a
  #print axioms census.
consumers: >-
  M31 quotient-shell / census series (the integrated band_mixing and
  t16_mixing_floor rooted-shell line): supplies the exact same-remainder
  deficiency spectrum as one class-weight sum, and the exact cross-remainder
  o_e census as a two-equation law that reproduces the integrated rooted degree
  1233 and explains the integrated nu=47 mixed witnesses.
risk_limits: >-
  The dyadic level laws, nesting, antisymmetry, and the collision necessity
  directions are PROVED (elementary: roots-of-unity filter + Newton). The
  deployed spectra and the sufficiency of the weight equations on the deployed
  families are COMPUTED by exhaustive / constructive enumeration. Both censuses
  are per-anchor (the same-remainder census at the pinned e=224 anchor, the o_e
  census at the standard anchor, plus an alternate-anchor consistency pair); the
  two-equation law itself is anchor-invariant. NON-T_16-aligned (ragged)
  cross-remainder collisions are outside the census and remain open; the
  anchor-independent statement that no T_16-mixed collision exists below e=192 is
  a candidate law, not proved here. No received-word, codeword, ray, or slope
  claim; no row-ledger movement and no M31 row closure.
---

# M31 dyadic collision weight laws

## Status

```text
object                                        = dyadic (T_16 & T_32) depth-32 collision weight laws + censuses
Lemma A  (dyadic class decomposition)         = PROVED (definitional)
Lemma B  (dyadic level law + closed forms)    = PROVED (roots-of-unity filter)
Lemma C  (antisymmetry, nesting, T_64 split)  = PROVED (elementary)
same-remainder collision <-> one eq (Sum eta)
  necessity                                   = PROVED (Newton, p prime > 32)
  sufficiency on the deployed family          = COMPUTED (exhaustive C(25,9))
same-remainder deficiency spectrum            = COMPUTED   192:10 224:40 256:30 288:4 (s_224 = 40)
cross-remainder collision <-> two eqs {E16,E32}
  equation count = floor(depth/16), nu = 47   = PROVED (character spacing) + COMPUTED (8 witnesses)
  necessity                                   = PROVED (Newton + character additivity)
  sufficiency on the deployed family          = COMPUTED (1723 pairs)
cross-remainder o_e census (standard anchor)  = COMPUTED   o_64=49 o_128=441 o_96=0 o_192=1233
  o_192 = 1225 whole-T_64 + 8 mixed           = reproduces integrated rooted degree 1233
alternate-anchor e=96 consistency pair        = COMPUTED (law anchor-invariant, censuses per-anchor)
ragged (non-T_16-aligned) cross collisions    = out of scope, open
row-ledger movement                           = 0
M31 LIST row closed                           = false
```

This note isolates and proves the algebraic core behind the integrated
`m31_quotient_t16_mixing_floor` and `m31_quotient_band_mixing` censuses and turns
both the same-remainder and the T_16-aligned cross-remainder sides into **exact**
counts. Two dyadic levels appear: the `T_32` level (class size 32, character of
order 128) governs the same-remainder collisions by a single scalar equation,
and the finer `T_16` level (class size 16, character of order 256) governs the
T_16-aligned cross-remainder collisions by exactly two scalar equations. A `T_32`
class is two `T_16` classes whose order-256 weights are equal and opposite and
cancel, leaving the order-128 `T_32` weight; the same-remainder one-equation law
is the special case of the cross-remainder two-equation law in which the first
equation is automatically satisfied.

The results are deliberately local. Both censuses are per-anchor, and the
non-`T_16`-aligned ("ragged") cross-remainder sector, together with the
anchor-independent mixing-floor-at-192 claim, remains open. Nothing here projects
to codewords or slopes or moves the M31 row ledger.

---

## 1. Frozen definitions

All objects are those of the integrated packages
`experimental/lean/m31_quotient_band_mixing/` and
`experimental/lean/m31_quotient_t16_mixing_floor/` (`Witnesses.lean`,
`Witness.lean`) and the note
`experimental/notes/thresholds/m31_quotient_t16_mixing_floor.md`. Only the dyadic
power-sum analysis is new.

Put `p = 2^31 - 1 = 2147483647` (`fieldPrime`). In `F_p[i]`, `i^2 = -1`, use the
norm-one generator (`normOneGenerator`)

\[
 g = (1717986917, 1288490189), \qquad g^{2^{30}} = -1, \qquad g^{2^{31}} = 1,
\]

so `g` has order `2^31`. For odd `r`, `1 <= r <= 2047`, the quotient label
(`labelOfRep`, via `iterateMul` on `quotientBase = g^{2^19}`) is

\[
 q_r = 2^{30}\,\operatorname{Re}\!\left(g^{r\,2^{19}}\right) \bmod p,
 \qquad 2^{30} = 1073741824 = 2^{-2047}\bmod p
 \tag{1.1}
\]

(`monicT2048Scale`). The 1024 values are pairwise distinct; puncturing `q_1` and
`q_3` leaves the domain `D` (`puncturedReps` / `puncturedLabels`), `|D| = 1022`.

The **dyadic classes** are the `T_d`-fold blocks (`t16BlockReps`, `t32BlockReps`,
`t64BlockReps`; the fold modulus is `4096/d`):

\[
 \mathcal T^{16}_c = \{q_r : r \bmod 256 \in \{c, 256-c\}\}\ (16\text{ pts}),\quad
 \mathcal T^{32}_a = \{q_r : r \bmod 128 \in \{a, 128-a\}\}\ (32\text{ pts}),
\]
\[
 \mathcal C_a = \{q_r : r \bmod 64 \in \{a, 64-a\}\}\ (64\text{ pts}).
\]

Class labels run over odds: `c in {1,...,127}` (64 `T_16` classes), `a in
{1,...,63}` (32 `T_32` classes). Two **level characters** are used throughout,

\[
 \xi_c = \psi_{16}^{\,c} + \psi_{16}^{-c},\quad \psi_{16} = g^{2^{23}}\ (\text{order }256);
 \qquad
 \eta_a = \psi_{32}^{\,a} + \psi_{32}^{-a},\quad \psi_{32} = g^{2^{24}}\ (\text{order }128).
\]

(The level pattern is `psi_d = g^{2^{19+\log_2 d}}` of order `2^{12-\log_2 d}`;
`T_64` would use `g^{2^{25}}` of order 64.) For a finite `E \subset D` write
`\operatorname{pref}_D(E) = (v_1,\ldots,v_D)`, `v_j = (-1)^j e_j(E)` the depth-`D`
locator prefix, `e_j` the `j`-th elementary symmetric function of the labels.
The **power sum** of a block is `p_k(\mathcal T) = \sum_{q\in\mathcal T} q^k \bmod
p`. The **canonical `T_32` remainder** of a support is the support minus every
complete `T_32` class it contains; two supports are **same-remainder** if these
coincide.

---

## 2. Lemma A: dyadic class decomposition

**Lemma A.** `D` decomposes at each dyadic level:

- `T_32`: the 32 classes `\mathcal T^{32}_a` partition `D`; 30 are complete (32
  labels) and classes `a=1,3` are incomplete (31 labels, missing `q_1,q_3`).
  `30\cdot32 + 2\cdot31 = 1022`.
- `T_16`: the 64 classes `\mathcal T^{16}_c` partition `D`; 62 are complete (16
  labels) and classes `c=1,3` are incomplete (15 labels, missing `q_1,q_3`).
  `62\cdot16 + 2\cdot15 = 1022`.

*Proof.* Odd `r` has odd residue mod 128 and mod 256. Among the 1024 odd
representatives, each odd residue mod 128 occurs `1024/64 = 16` times and each
odd residue mod 256 occurs `1024/128 = 8` times. A `T_32` class collects two mod-128
residues `\{a,128-a\}` (distinct, `a` odd), hence `16+16 = 32` labels; a `T_16`
class collects two mod-256 residues `\{c,256-c\}`, hence `8+8 = 16` labels.
Puncturing removes `q_1` (class `1` at both levels) and `q_3` (class `3`), each
dropping one label from two classes. The counts follow. `QED`

Write `INTACT_{32}` for the 30 complete `T_32` classes (odd `a in [1,63]` except
1 and 3) and `INTACT_{16}` for the 62 complete `T_16` classes (odd `c in [1,127]`
except 1 and 3).

---

## 3. Lemma B: the dyadic level law and the closed forms

**Lemma B.** Fix a level `d in \{16,32\}` and a complete class of that level.

1. `p_k = 0` for all odd `k`.
2. For even `k`, `2 <= k < d`, `p_k = d\cdot 2^{29k}\binom{k}{k/2} \bmod p`,
   the same value for every class of the level (class-independent).
3. The first class-dependence is at `k = d`, with the closed forms
   \[
    p_{16}(\mathcal T^{16}_c) = 8\binom{16}{8} + 8\,\xi_c,
    \qquad
    p_{32}(\mathcal T^{32}_a) = 8\binom{32}{16} + 8\,\eta_a
    \pmod p,
    \tag{3.1}
   \]
   i.e. `B_{16} + 8\xi_c` and `B_{32} + 8\eta_a` with
   `B_{16} = 8\binom{16}{8} = 102960` and
   `B_{32} = 8\binom{32}{16} = 513675826`. The level weights
   `8\xi_c = 16\operatorname{Re}(\psi_{16}^c)` (62 distinct) and
   `8\eta_a = 16\operatorname{Re}(\psi_{32}^a)` (30 distinct) separate the classes.

*Proof.* Fix a class `\mathcal T^{d}` with label `a` and set `\zeta = g^{a 2^{19}}`,
`\omega = g^{2^{19}\cdot(4096/d)}`. The fold modulus is `M = 4096/d`, so
`\omega = g^{2^{19}M}` has order `2^{31}/(2^{19}M) = 2^{12}/M = d`. As in the
`T_32` case, a representative `r \equiv a` or `-a \pmod M` gives
`g^{r 2^{19}} = \zeta\,\omega^{m}` or `\zeta^{-1}\omega^{m+1}`, and the `d`
representatives map bijectively onto
`\{2^{30}\operatorname{Re}(\zeta\,\omega^{j}) : j = 0,\ldots,d-1\}`. With
`u = \zeta\omega^{j}` (norm one, `u^{-1} = \bar u`) and
`2^{30}\operatorname{Re}(u) = 2^{29}(u + u^{-1})`,

\[
 p_k = 2^{29k}\sum_{j=0}^{d-1}\sum_{i=0}^{k}\binom{k}{i}u^{k-2i}
     = d\cdot 2^{29k}\!\!\sum_{\substack{0\le i\le k\\ d\,\mid\,(k-2i)}}
       \binom{k}{i}\,\zeta^{\,k-2i},
 \tag{3.2}
\]

using `\sum_{j=0}^{d-1}\omega^{j(k-2i)} = d\cdot[\,d\mid(k-2i)\,]`.

- **`k` odd:** `d \mid (k-2i)` forces `k-2i \equiv 0 \pmod d`, impossible for odd
  `k-2i` (even `2i`, `d` even). The sum is empty: `p_k = 0`.
- **`k` even, `2 <= k < d`:** the only `i in [0,k]` with `d \mid (k-2i)` is
  `i = k/2` (the next, `i = k/2 + d/2`, needs `i \le k`, i.e. `k \ge d`). So
  `p_k = d\cdot 2^{29k}\binom{k}{k/2}`, class-independent.
- **`k = d`:** `d \mid (d-2i)`, `0 \le i \le d`, gives `i \in \{0, d/2, d\}`,
  `d-2i \in \{d,0,-d\}`. Now `\zeta^{d} = g^{a 2^{19} d}`. For `d = 16`,
  `\zeta^{16} = g^{a 2^{23}} = \psi_{16}^a`; for `d = 32`,
  `\zeta^{32} = g^{a 2^{24}} = \psi_{32}^a`. Hence
  `p_d = d\cdot 2^{29d}\,[\zeta^{d} + \binom{d}{d/2} + \zeta^{-d}]`. The scalar
  reduces mod `p` via `2^{31}\equiv1`: for `d=16`,
  `16\cdot 2^{464} = 2^{468} \equiv 2^{3} = 8`; for `d=32`,
  `32\cdot 2^{928} = 2^{933} \equiv 2^{3} = 8` (since `468 \equiv 3` and
  `933 \equiv 3 \pmod{31}`). Both give prefactor 8, so (3.1) holds with
  `\binom{16}{8} = 12870` (`B_{16}=102960`) and `\binom{32}{16}=601080390`
  (`B_{32}=513675826`). `QED`

The two even-constant tables (each checked against `d\cdot2^{29k}\binom{k}{k/2}`):

```text
 T_16 (d=16)                      T_32 (d=32)
  k :  p_k                         k :  p_k              k :  p_k
  2 :  2                           2 :  4               18 :  48620
  4 :  805306368                   4 :  1610612736      20 :  536882459
  6 :  167772160                   6 :  335544320       22 :  1275071171
  8 :  36700160                    8 :  73400320        24 :  417333908
 10 :  8257536                    10 :  16515072        26 :  1504444574
 12 :  1892352                    12 :  3784704         28 :  554418214
 14 :  439296                     14 :  878592          30 :  527689737
                                  16 :  205920
```

Note `T_32`-even`(k) = 2\cdot T_16`-even`(k)` for `2 <= k <= 14` (a `T_32` class
has twice the labels), and `T_32`-even`(16) = 205920 = 2\cdot B_{16}` (Section 4).

---

## 4. Lemma C: antisymmetry, the dyadic nesting, and the `T_64` split

**Lemma C.**

1. **Antisymmetry.** `\xi_{128-c} = -\xi_c` and `\eta_{64-a} = -\eta_a \bmod p`;
   equivalently the `T_16` weight `8\xi` is odd under `c\mapsto128-c` and the
   `T_32` weight `w(a) = 8\eta_a` is odd under `a\mapsto64-a`.
2. **Dyadic nesting.** `\mathcal T^{32}_a = \mathcal T^{16}_a \sqcup
   \mathcal T^{16}_{128-a}` (disjoint, `16+16=32`), for every odd `a in [1,63]`.
   In the sum `p_{32}(\mathcal T^{32}_a) = p_{32}(\mathcal T^{16}_a) +
   p_{32}(\mathcal T^{16}_{128-a})` the order-256 `\xi`-parts cancel and the
   order-128 `\eta`-parts double, giving
   `p_{32}(\mathcal T^{32}_a) = 8\binom{32}{16} + 8\eta_a` — the `T_32` closed
   form of Lemma B.
3. **`T_64` split.** `\mathcal C_a = \mathcal T^{32}_a \sqcup
   \mathcal T^{32}_{64-a}` (64 labels), and for the 14 complete pairs
   `(a,64-a)`, `a in \{5,\ldots,31\}` odd,
   `p_{32}(\mathcal T^{32}_a) + p_{32}(\mathcal T^{32}_{64-a}) = 2B_{32} =
   1027351652`. Any exchange of a whole complete `T_64` class for another leaves
   `\sum p_{32}` unchanged; moreover `\sum_{c\in\mathcal C_a}\xi_c = 0`.

*Proof.* (1) `\psi_{16}^{128} = g^{2^{23}\cdot128} = g^{2^{30}} = -1` and
`\psi_{32}^{64} = g^{2^{24}\cdot64} = g^{2^{30}} = -1`. So
`\xi_{128-c} = \psi_{16}^{128}\psi_{16}^{-c} + \psi_{16}^{-128}\psi_{16}^{c}
= -(\psi_{16}^{-c}+\psi_{16}^{c}) = -\xi_c`, and likewise
`\eta_{64-a} = -\eta_a`.

(2) `\mathcal T^{16}_a` has `r \bmod 256 \in \{a,256-a\}` and
`\mathcal T^{16}_{128-a}` has `r \bmod 256 \in \{128-a,128+a\}`; the four residues
reduce mod 128 to `\{a,128-a\}`, so the disjoint union is `\mathcal T^{32}_a`.
By (3.2) at `d=16`, `k=32` (survivors `i \in \{0,8,16,24,32\}`, i.e. characters
`\zeta^{0}, \zeta^{\pm16}=\psi_{16}^{\pm c}, \zeta^{\pm32}=\psi_{32}^{\pm c}`),
\[
 p_{32}(\mathcal T^{16}_c) = 4\binom{32}{16} + 4\binom{32}{8}\,\xi_c + 4\,\eta_c
 \pmod p
\]
(scalar `16\cdot2^{928} = 2^{932} \equiv 2^{2} = 4`). Summing over `c = a` and
`c = 128-a`: the constant doubles to `8\binom{32}{16}`, the `\xi`-term carries
`\xi_a + \xi_{128-a} = 0` and vanishes, and `\eta_{128-a} = \eta_a` (because
`\psi_{32}^{128} = g^{2^{31}} = 1`, so `\eta_{128-a} = \psi_{32}^{-a} +
\psi_{32}^{a} = \eta_a`) so the `\eta`-term doubles to `8\eta_a`. Thus
`p_{32}(\mathcal T^{32}_a) = 8\binom{32}{16} + 8\eta_a`, matching (3.1). This is
the mechanism: the finer `\xi`-weights of the two halves are equal and opposite
and cancel, and the `\eta`-weight is shared and survives.

(3) `\mathcal T^{32}_a` and `\mathcal T^{32}_{64-a}` collect mod-128 residues
`\{a,128-a\}` and `\{64-a,64+a\}`, disjoint, reducing mod 64 to `\{a,64-a\}` =
`\mathcal C_a`. For complete pairs `p_{32}(\mathcal T^{32}_a) +
p_{32}(\mathcal T^{32}_{64-a}) = 2B_{32} + (\eta_a\cdot8 + \eta_{64-a}\cdot8) =
2B_{32}` by (1). A whole-`T_64` exchange changes `\sum p_{32}` by
`2B_{32}-2B_{32}=0`. Finally `\mathcal C_a` is four `T_16` classes
`\{c, 128-c, ...\}` closed under `c\mapsto128-c`, so
`\sum_{c}\xi_c = 0` by (1). `QED`

Classes 61 and 63 have `T_64` partners 3 and 1 (punctured), so they stand alone;
they are the two "singleton" `T_32` weights. Part 3 is the elementary source of
the integrated `49 = 7^2`, `441 = 21^2`, `1225 = 35^2` whole-`T_64`-swap families
(Section 6.2).

### Closed-form `T_32` weight table

All 30 complete `T_32` classes, grouped by the antisymmetric pair `(a,64-a)`;
`p_{32}(a) = (B_{32} + 8\eta_a) \bmod p`, `B_{32}=513675826`. Each pair satisfies
`8\eta_a + 8\eta_{64-a} \equiv 0` and `p_{32}(a)+p_{32}(64-a) = 2B_{32}`.

```text
   a   8*eta_a          p32(a)          |  64-a   8*eta_{64-a}     p32(64-a)
   5   1590749127       2104424953      |   59    556734520       1070410346
   7     99910478        613586304      |   57   2047573169        413765348
   9    526221414       1039897240      |   55   1621262233       2134938059
  11    232480480        746156306      |   53   1915003167        281195346
  13   2114958684        481150863      |   51     32524963        546200789
  15   1251605585       1765281411      |   49    895878062       1409553888
  17    998021454       1511697280      |   47   1149462193       1663138019
  19    114309104        627984930      |   45   2033174543        399366722
  21   1508662977       2022338803      |   43    638820670       1152496496
  23   1676708738         42900917      |   41    470774909        984450735
  25   2054273900        420466079      |   39     93209747        606885573
  27       996335        514672161      |   37   2146487312        512679491
  29   1052145471       1565821297      |   35   1095338176       1609014002
  31    830574365       1344250191      |   33   1316909282       1830585108
singletons (T_64 partner punctured):
  61    156859168        670534994      (partner class 3 punctured)
  63    892336617       1406012443      (partner class 1 punctured)
```

---

## 5. The collision laws (depth 32)

Both laws come from power-sum additivity over disjoint unions together with the
level law (Lemma B): a collision of two aligned supports is equality of the
depth-32 locator prefix, which by Newton (`p` prime `> 32`) is equality of the
first 32 power sums, which the level law reduces to finitely many character
equations. The equations enter at multiples of the fold size.

### 5.1 Same-remainder sector (`T_32`-aligned): one equation

Fix a canonical `T_32` remainder `\rho` and the set `\mathrm{Av}` of complete
`T_32` classes disjoint from `\rho`; a support is
`E_S = \rho \sqcup \bigsqcup_{a\in S}\mathcal T^{32}_a`, `|S| = m`.

**Theorem.** For `E_S,E_{S'}` in one same-remainder sector with `|S|=|S'|=m`,
`\operatorname{pref}_{32}(E_S) = \operatorname{pref}_{32}(E_{S'})` **iff**
`\sum_{a\in S}\eta_a \equiv \sum_{a\in S'}\eta_a`, i.e.
`\sum_{a\in S}p_{32}(\mathcal T^{32}_a) \equiv \sum_{a\in S'}p_{32}(\mathcal
T^{32}_a) \pmod p`.

*Necessity is PROVED.* For `1 <= k <= 31` the `T_32` class term `p_k(\mathcal
T^{32}_a)` is class-independent (Lemma B, `k < 32`), so `\sum_{a\in S}p_k =
m\cdot(\text{const})` depends only on `m`; hence `p_k(E_S)=p_k(E_{S'})` for
`k \le 31`, and by Newton `e_1,\ldots,e_{31}` agree. At `k=32`,
`e_{32}(E_S)-e_{32}(E_{S'}) = \pm32^{-1}(p_{32}(E_S)-p_{32}(E_{S'}))`, and
`p_{32}=B_{32}+8\eta` with `mB_{32}` cancelling, so the prefixes agree iff the
`\eta`-sums agree. *Sufficiency on the deployed family is COMPUTED*: the same
Newton inversion gives the converse abstractly; at the pinned anchor (Section
6.1) all 85 weight-matching selections are confirmed to share the depth-32
prefix and 3000 weight-distinct selections do not.

### 5.2 Cross-remainder sector (`T_16`-aligned): two equations

Now the differing part is a union of complete `T_16` classes. By Lemma B (`d=16`)
and (3.2), a `T_16` class term `p_k(\mathcal T^{16}_c)` is class-independent for
`k \le 14`, and for larger `k` its class-dependent part is a combination of the
characters `\psi_{16}^{jc}` with `1 \le j \le \lfloor k/16\rfloor`: the character
`\psi_{16}^{c}` (`= \xi`) enters at `k=16`, `\psi_{16}^{2c}` (`= \eta`) at
`k=32`, `\psi_{16}^{3c}` at `k=48`, spaced by 16. Hence for equal class counts a
depth-`D` collision is `\lfloor D/16\rfloor` scalar equations.

**Theorem (depth 32).** A depth-32 collision of two `T_16`-aligned supports with
equal class count is exactly the two equations
\[
 (E16)\ \ \sum_{c\in R}\xi_c = \sum_{c\in A}\xi_c,
 \qquad
 (E32)\ \ \sum_{c\in R}\eta_c = \sum_{c\in A}\eta_c \pmod p.
 \tag{5.1}
\]
Their solutions automatically match through `k=47` and first differ at `k=48`
(the third character `\psi_{16}^{3c}`), so the locator-prefix agreement is
exactly `\nu = 47 = 3\cdot16 - 1`.

*Necessity is PROVED* (Newton + character additivity: a depth-32 collision forces
equal `p_1..p_{32}`; the class-dependent content up to `k=32` is spanned by
`\xi` and `\eta`, so equality forces (E16) and (E32)). *The two-equation
structure and `\nu=47` are PROVED* (character spacing above). *The eight
integrated `T_16`-mixed witnesses* (`m31_quotient_t16_mixing_floor.md` Section 5;
`Witness.lean` `mixedSpecs`) *are COMPUTED* to satisfy (E16) and (E32), to have
first power-sum difference at `k=48`, and to agree with the anchor to
locator-coefficient 47 and break at 48 — reproducing the integrated
`mixed_neighbors_match_exactly_forty_seven`.

**Specialization.** A complete `T_32` class is `\mathcal T^{16}_a \sqcup
\mathcal T^{16}_{128-a}` with `\xi_a + \xi_{128-a} = 0` (Lemma C.1), so a
`T_32`-aligned support contributes 0 to every `\sum\xi`: (E16) is automatically
satisfied and only (E32) survives. The one-equation same-remainder law (5.1
of §5.1) is exactly this special case of the two-equation cross-remainder law.

---

## 6. The deployed censuses

### 6.1 Same-remainder `T_32` spectrum at the pinned `e=224` anchor

The pinned anchor `A*` has canonical `T_32` remainder
`\rho = (\mathcal T^{32}_1\setminus\{q_1\}) \cup (\mathcal T^{32}_3\setminus\{q_3\})
\cup \rho_{17}\cup\rho_{47}\cup\rho_{23}\cup\rho_{41}\cup\rho_{61}` (`|\rho|=191`,
with `\rho_{17},\rho_{47},\rho_{23},\rho_{41}` 31 labels each and `\rho_{61}` 5
labels) and the 9 complete selected classes `S_{A*} =
\{13,19,25,33,35,37,43,59,63\}`, so `|A*| = 191 + 9\cdot32 = 479`. The available
complete classes are `\mathrm{Av} = INTACT_{32}\setminus\{17,47,23,41,61\}`
(`|\mathrm{Av}|=25`); the anchor weight target is
`\sum_{a\in S_{A*}}p_{32}(\mathcal T^{32}_a) = 520865170`. (A byte-match
cross-check: the integrated `T_16`-mixing-floor anchor
`R_{31}\sqcup\bigsqcup_{a\in\{7,9,13,19,21,23,27\}}\mathcal C_a` reproduces its
depth-32 target vector `\eta` exactly under this note's `locator_prefix`.)

Enumerating all `\binom{25}{9}=2042975` selections and keeping the `\eta`-weight
matches gives the **exact same-remainder deficiency spectrum**:

```text
   deficiency e :   192   224   256   288    (all other e : 0)
   count  s_e   :    10    40    30     4     (84 neighbours; identity e=0 : 1)
```

so `\boxed{s_{224} = 40}`. The 40 neighbours at `e=224` are exactly
`\{21,27,31\}` fixed together with two of the five anchor "one-pairs"
`\{[5,59],[13,51],[19,45],[25,39],[29,35]\}` swapped for their partners and one
of the four available "zero-pairs" `\{[7,57],[9,55],[11,53],[15,49]\}`,
`40 = \binom{5}{2}\binom{4}{1}`, each verified a genuine deployed collision. The
naive count with all zero-weight pairs available is `\binom{5}{2}\binom{6}{1}=60`;
the deployed `\rho` consumes two zero-weight pairs `(17,47),(23,41)`, masking the
count to `\binom{5}{2}\binom{4}{1}=40`. Restoring the two pairs (available set 29)
reproduces the counterfactual 60. [COMPUTED.]

### 6.2 Cross-remainder `o_e` census at the standard anchor

The standard anchor is the integrated `T_16`-mixing-floor anchor `A`. Its inside
and outside pools are the `T_16` folds of the 7 inside and 7 outside `T_64`
blocks, `28` classes each. By Lemma C.3 every `T_64` block has
`\sum\xi = 0` (and constant `\sum\eta`), so whole-`T_64` swaps automatically
satisfy (E16) and (E32). A meet-in-the-middle enumeration on `(\sum\xi,\sum\eta)`
gives the **exact `o_e` census** (the number of `T_16`-aligned cross-remainder
collisions at deficiency `e`):

```text
   e   :   16   32   48   64   80   96  112  128  |  192
  o_e  :    0    0    0   49    0    0    0  441  | 1233
```

- `o_{16..128}` (folds `t \le 8`) are **exhaustive** MITM counts:
  `o_{64} = 49 = \binom{7}{1}^2`, `o_{128} = 441 = \binom{7}{2}^2` (whole-`T_64`
  single/double swaps), and **`o_{96} = 0`** — the `\xi`-only matches number
  132552 and the `\eta`-only matches 5798464, but their conjunction is empty.
- `o_{192} = 1233`: the whole-`T_64` triple swaps `\binom{7}{3}^2 = 1225` all
  satisfy (E16)`\wedge`(E32) and collide, plus the 8 genuinely-`T_16`-mixed
  witnesses of §5.2, `1225 + 8 = 1233`. This **reproduces the integrated rooted
  degree** `allNeighbors.length = 1233` (`m31_quotient_t16_mixing_floor.md`), so
  the two-equation law captures exactly the integrated neighbour set. The
  exhaustive fold-`t=9..12` tail is corroborated by an independent
  meet-in-the-middle census. [COMPUTED.]

The **`T_16` mixing floor is `e = 192`**: below 192 every two-equation collision
is a whole-`T_64` swap, and the first genuinely-`T_16`-mixed collisions appear at
`e=192` and number exactly 8 (`o_{96}=0` is the precise "no mixing at `e=96`"
statement at this anchor). Sufficiency `(E16)\wedge(E32)\Rightarrow` collide is
confirmed on all 1723 satisfying selection pairs (`49+441+1225+8`); necessity on
a 1000-pair non-satisfying sample (none collide).

### 6.3 Alternate-anchor consistency

The two-equation law is a statement about `T_16` class characters and is
**anchor-invariant**; the `o_e` counts are per-anchor. The integrated
`band_mixing` packet supplies an independent `e=96` pair at a different
("mixing") anchor: its exchanged `T_16` class sets satisfy both (E16) and (E32),
its supports have deficiency 96 and agree to locator-coefficient 47 and break at
48, and its anchor differs from the standard one. A Chebyshev cross-check
(`band_mixing` `sigma`) gives `\sum\sigma = 281588527` and
`\sum\sigma^2 = 1888686693` equal on both sides. Thus the same law holds at a
second anchor even though `o_{96}=0` there for the standard pools. [COMPUTED.]

---

## 7. Scope guard

- **Proved (elementary).** Lemma A (both levels); Lemma B (the dyadic level law
  and both closed forms, by the roots-of-unity filter); Lemma C (antisymmetry,
  the dyadic nesting with `\xi`-cancellation / `\eta`-doubling, the `T_64`
  split); the two-equation structure and `\nu=47` (character spacing); and the
  **necessity** direction of both collision laws (Newton, `p` prime `> 32`).
- **Computed.** The same-remainder spectrum (`192:10, 224:40, 256:30, 288:4`,
  `s_{224}=40`) and the masking; the sufficiency of the weight equations on the
  deployed families; the eight `T_16`-mixed witnesses (`\nu=47`); the `o_e`
  census (`o_{64}=49`, `o_{128}=441`, `o_{96}=0`, `o_{192}=1233`) reproducing the
  integrated rooted degree; and the alternate-anchor `e=96` pair.
- **Out of scope / open.** Both censuses are **per-anchor**. Non-`T_16`-aligned
  ("ragged") cross-remainder collisions are not enumerated by the two-equation
  law and remain open. The anchor-independent statement that no `T_16`-mixed
  collision exists below `e=192` is a candidate law, not proved here. No
  received-word, codeword, ray, or slope claim; nothing moves the M31 row ledger
  or closes the row.

---

## 8. Routes killed

- **Count search above 40 at `e=224` (same-remainder).** The exact `\binom{25}{9}`
  census resolves the `[40,60]` ambiguity to `40`: there is no 41st distinct
  same-remainder `e=224` neighbour.
- **Collision-graph enumeration.** Neither census needs the collision graph: the
  same-remainder `s_e` is the count of `\eta`-weight-matching selections, and the
  cross-remainder `o_e` is the count of `(\sum\xi,\sum\eta)`-matching pairs.
- **Whole-`T_64` classification of the `e=192` neighbours.** The integrated
  A1 classification (all same-prefix `e=192` pairs are whole-`T_64` swaps) is
  refined exactly: `o_{192} = 1225` whole-`T_64` `+ 8` genuinely-mixed, the eight
  mixed being precisely the two-equation solutions that agree to `\nu=47` and
  break at `k=48`.

---

## 9. Replay

```text
python3 experimental/scripts/verify_m31_dyadic_weight_laws.py --check
python3 experimental/scripts/verify_m31_dyadic_weight_laws.py --tamper-selftest
```

`--check` rebuilds the labels from the frozen definitions and recomputes, for
both dyadic levels: the class decompositions (Lemma A); the odd/even power-sum
flatness and both even-constant tables against `d\cdot2^{29k}\binom{k}{k/2}`, and
the closed forms `p_{16}=B_{16}+8\xi` and `p_{32}=B_{32}+8\eta` for all complete
classes (Lemma B); the antisymmetries, the dyadic nesting with the
`\xi`-cancellation / `\eta`-doubling identity, and the `T_64` split (Lemma C);
the `\eta` byte-match; the non-`T_64` `e=192` collision pair; the full
`\binom{25}{9}` same-remainder census with direct depth-32 prefix checks on all
85 weight-matches and a 3000-selection non-match sample, the forty explicit
`e=224` witnesses, and the counterfactual 60; the eight `T_16`-mixed witnesses
(E16, E32, first difference `k=48`, prefix agreement `\nu=47`); the exhaustive
`o_e` MITM census for `e\le128` and the constructive `o_{192}=1233`; the
1723-pair sufficiency and 1000-pair necessity; and the alternate-anchor `e=96`
pair. `--tamper-selftest` corrupts each load-bearing constant in turn and
confirms the comparison layer rejects it (exit 0 iff every mutation is caught).

An optional stdlib Lean arithmetic shadow of the closed constants is at
`experimental/lean/m31_dyadic_weight_laws/` (`lake build`); it kernel-checks the
exact arithmetic identities (`B_{16}=102960`, `B_{32}=513675826`, the even
constants at both levels, the weight antisymmetry table,
`40 = \binom{5}{2}\binom{4}{1}`, `60 = \binom{5}{2}\binom{6}{1}`, spectrum sum
84, `o_{192} = 1225 + 8 = 1233`, `49 = 7^2`, `441 = 21^2`, `1225 = 35^2`), not
the roots-of-unity, Newton, or census arguments, which are proved / computed
above.
