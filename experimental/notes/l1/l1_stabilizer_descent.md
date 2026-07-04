# L1 Stabilizer Descent: Composite-`ell` Mixed Minimal Kernel Sets Are Quotient-Pullbacks

## Setting

Background-free coset sunflower over `F_p`: `H = mu_ell` (order `ell`, `ell | p-1`);
petals `T_i = a_i H` (`i=1..t`, labels `alpha_i = a_i^ell` distinct), locators
`L_{T_i} = X^ell - alpha_i`; core `C = union_{j=1..m} b_j H` (labels
`beta_j = b_j^ell` distinct, disjoint from the `alpha_i`); distinct nonzero scalars
`c_i`; word `U = c_i L_C` on `T_i`, `0` on `C`; `N = t ell`. For `E subset C`,
`W_E` is the unique `deg < N` CRT representative of `(c_i L_E mod L_{T_i})_i`; `E`
is a KERNEL SET iff `ell <= |E| <= (t-1)ell` and `deg W_E <= |E|`; MINIMAL if no
proper nonempty subset is a kernel set; `P_E = W_E L_{C\E}`,
`M(E) = {x in E : W_E(x) != 0}`. By the PR #219 bijection
(`l1_general_reconstruction_collapse.md`, commit bee2b1d) listed full-petal
codewords `<->` minimal kernel sets, `M(E)=E` for minimal `E`. `E` is MIXED if not
a coset-union; `Stab_H(E) = {h in H : hE = E}`; PRIMITIVE if `Stab_H(E) = {1}`.
Hypothesis **(D)**: the `c_i` pairwise distinct (so `U` is not a codeword and every
kernel set has `M(E) != ∅`, PR #219 item 6 sub-`ell` floor); `t >= 2`.

**Power map / induced sunflower.** Fix `e | ell`, `ell' = ell/e`, `K = mu_e <= H`.
`pi(x) = x^e` collapses each `K`-coset to a point, injective on `K`-cosets — a
bijection `{K-invariant S subset C} <-> {subsets of pi(C)}` with `|pi(S)| = |S|/e`;
it restricts to `mu_ell ->> mu_{ell'}` (kernel `mu_e`). For `K`-invariant `E`,
`E^(e) := pi(E)`. The INDUCED `(t, ell', m)` sunflower has petals `a_i^e mu_{ell'}`,
core `b_j^e mu_{ell'}`, **same** scalars `c_i` (no correction factor: `alpha_i,
beta_j` are simultaneously the `ell`-th powers of `a_i, b_j` and `ell'`-th powers of
`a_i^e, b_j^e`). Primed `L', W', P', M', Stab'` refer to it, `N' = t ell'`.

## Theorem D2 (kernel descent) — PROVED-LOCAL

`E |-> E^(e)` is a bijection `{K-invariant subsets of C} -> {subsets of C'}` under
which `E` is a kernel set (level `ell`) **iff** `E^(e)` is a kernel set (level
`ell'`), with `|E^(e)| = |E|/e`, `deg W_E = e * deg W'_{E^(e)}`, and the window
`ell <= |E| <= (t-1)ell` descending to `ell' <= |E^(e)| <= (t-1)ell'`.

**Proof.** *(a)* A `K`-coset `yK` has `prod_{zeta in mu_e}(X - y zeta) = X^e - y^e`,
so `K`-invariant `S` has `L_S(X) = L_{pi(S)}(X^e)`. *(b)* By `H`-equivariance of the
CRT rep (`W_{zeta E}(X) = zeta^{|E|} W_E(zeta^{-1}X)`, CRT uniqueness), for
`zeta in K`, `zeta E = E` and `zeta^{|E|} = 1` (`e | |E|`), so `W_E` is
`mu_e`-invariant: `W_E(X) = Omega_E(X^e)`, `deg_X W_E = e deg_Z Omega_E`. Each
`W_E - c_i L_E = (X^ell - alpha_i) Q_i` is then an identity in `X^e`; setting
`Z = X^e`, `Omega_E ≡ c_i L_{E^(e)} mod (Z^{ell'} - alpha_i)` for all `i` (SAME
`c_i`), `deg_Z Omega_E < N'`, so `Omega_E = W'_{E^(e)}` (CRT uniqueness in
`F_p[Z]`). Hence `deg W_E = e deg W'_{E^(e)}`, `|E| = e|E^(e)|`, so
`deg W_E <= |E| <=> deg W'_{E^(e)} <= |E^(e)|`; divide the window by `e`. Reverse:
`hat W(X) := W'_{E^(e)}(X^e)` solves the level-`ell` congruences, `deg <= |E| < N`,
so `hat W = W_E`. ∎

**Corollary D2.1.** For `K`-invariant `E`: `P_E(X) = P'_{E^(e)}(X^e)` (so `P_E`
`K`-invariant); `M(E)^(e) = M'(E^(e))`, `M(E)` `K`-invariant; mixed `<=>` mixed; and
`Stab'(E^(e)) = pi(Stab_H(E))` — with `Stab_H(E) = mu_{e_0}` (`e | e_0`),
`Stab'(E^(e)) = mu_{e_0/e}`, so FULL-stabilizer descent (`e = e_0`) is PRIMITIVE.
*(`pi` injective on `K`-invariant sets and `pi(mu_{e_0}) = mu_{e_0/e}`.)* ∎

## Theorem D3 (minimality descent) — PROVED-LOCAL (iff, distinct scalars)

Under **(D)**, for `K`-invariant `E`: `E` is a minimal kernel set (over ALL subsets
of `C`) **iff** `E^(e)` is a minimal kernel set of the induced sunflower.

**Proof.** *(=>)* If `F subsetneq E^(e)` is a nonempty induced-kernel set, its lift
`pi^{-1}(F) cap C` is `K`-invariant, `subsetneq E`, nonempty, a kernel set by D2 —
a proper kernel subset of `E`, contradiction.

*(<=, collapse + rigidity — the substantive direction.)* Suppose `E^(e)` minimal but
`E` not: pick a kernel set `E'' subsetneq E`, shrink to a MINIMAL kernel set
`E_0 subseteq E''`. Both `E_0, E` are kernel sets, `E_0 subsetneq E`,
`|E| <= (t-1)ell < N`, so collapse (PR #219 item 1) gives `P_{E_0} = P_E`. But
`P_E = P'_{E^(e)}(X^e)` is `K`-invariant (Cor D2.1), so `P_{E_0}` is; as `U` is
`H`-invariant (hence `K`-invariant), `M(E_0) = {x in C : P_{E_0}(x) != 0}` is
`K`-invariant. By **(D)** `M(E_0) != ∅`, so rigidity (PR #219 item 3) forces
`M(E_0) = E_0`; hence `E_0` is `K`-invariant. Then D2 (forward) makes `E_0^(e)` a
nonempty induced-kernel set `subsetneq E^(e)`, contradicting minimality of
`E^(e)`. ∎

> Composite-`ell` descent needs the full collapse machinery: a general kernel subset
> of `E` need not be `K`-invariant, but `P_{E_0} = P_E` **forces** the minimal one to
> be. Combining D2+D3, `E |-> E^(e)` bijects `{K-invariant minimal kernel sets, level
> ell} <-> {minimal kernel sets, level ell'}`, respecting kernel/minimal/mixed/listed,
> missed cores, reconstructions, stabilizers.

## Theorem D4 (classification + divisor-sum) — PROVED-LOCAL

Apply D3 with `K = Stab_H(E)`. The map `E |-> (e := |Stab_H(E)|, E^(e))` is a
bijection

```
{ MIXED minimal kernel sets of level ell }
   <->  ⨆_{ d | ell, d >= 2 }  { PRIMITIVE mixed minimal kernel sets of level d } ,
```

`Stab_H(E) = mu_e` corresponding to a PRIMITIVE mixed minimal set at
`d = ell/e >= 2` (mixed forces `e < ell`) — so every mixed minimal kernel set is
either primitive or the `pi^{-1}`-lift of a primitive one at a strictly smaller
divisor level. For any functional invariant along the descent (a fixed scalar
vector, or the exact all-scalar minimal-**feasibility** count, which preserves `c`):

```
┌─────────────────────────────────────────────────────────────────────────┐
│    #MinMix(t, ell, m)  =  Σ_{ d | ell, d >= 2 }  #PrimMinMix(t, d, m)      │ (★)
└─────────────────────────────────────────────────────────────────────────┘
```

a Möbius-invertible recursion generating the composite count from the PRIMITIVE
divisor-level counts. PROVED-LOCAL scope of D4 = the bijection (★) itself, plus
this unconditional corollary: with companion Theorem A (`m <= t =>
#PrimMinMix(t,d,m) = 0` at every divisor level), (★) re-derives the coset
mixed-vacancy on the petal-heavy corner for all `ell`, composite included.

**Conditional consequences (on the OPEN primitive vacancy `PV`, below; NOT
proved).** The top term `#PrimMinMix(t,ell,m)` is exactly the input the
recursion cannot reduce (a primitive set has `e = 1`, an identity descent).
IF `PV(t,d,m)` holds at the relevant levels: **(i)** `m < ell` would give
`#PrimMinMix(t,ell,m) = 0`, i.e. every `m<ell` mixed minimal set imprimitive —
census-backed (59/59 below) but proved so far only for `<= 1` active sector
(companion Theorem B); for PRIME `ell` imprimitivity is impossible, so (i) there
MEANS full vacancy, the hard open target itself. **(ii)** `m <` (least prime
factor of `ell`) would empty every term of (★) — again `PV` at each divisor
level, open in general beyond Theorem A/B and PR #223's `(t=3, m=t+1)` slice.

## Ledger charge (v13 quotient-pullback vocabulary)

A mixed minimal set with `Stab_H(E) = mu_e` (`e>1`) has `P_E, U` both
`mu_e`-invariant (Cor D2.1), so its agreement set is `mu_e`-invariant: the codeword
is **not** stabilizer-primitive and is charged to `Q_e`, never `Q_1^{list}`. D2/D3
realize it as the `pi^{-1}`-pullback of a level-`ell/e` primitive codeword — the
full-reconstruction analogue of `lem:v13-quot-pullback` of
`experimental/cap25_v13_experimental.tex` (its `g(Y) -> g(X^M)` onto the
`M`-periodic stratum), lifted from the locator `L_E` to the whole kernel-set /
CRT-operator / missed-core / codeword structure (`M=e`, `n=ell`, `n/M=ell'`), v13's
"descent to a projective space of no larger dimension" becoming `deg -> deg/e`. D4
is exactly what `prob:v13-primitive-image-fiber` asks to "charge separately": the
imprimitive (`Stab != 1`) part of the full-petal `ImgFib` is in **exact** bijection
with the primitive parts at the proper quotient levels, reducing that problem's
coset slice to bounding `#PrimMinMix(t,d,m)` at each `d | ell`, `d <= m`. (Both v13
labels verified against the tex.)

## Experimental findings — EXPERIMENTAL / CERTIFICATE

- **Stabilizer census (re-verified).** 73 gathered mixed-minimal witnesses
  re-verified from scratch, **0** failures; of the **59** with `m < ell`, **0**
  primitive — all imprimitive `pi^{-1}`-lifts (the pattern the conditional
  consequence (i) predicts; data, not proof). The exact all-scalar count
  matches (★) at the calibration configs: `#MinMix(3,6,4) = 16 = 16+0+0` (`p=487`),
  `#MinMix(4,6,5) = 1306 = 112+1194+0` (`p=499`), both imprimitive terms confirmed
  **two independent ways** (level-`6` `mu_e`-block strata vs induced enumeration).
- **Prime-dependent `(3,3)` onset (data).** The primitive-mixed onset at `(3,3)` is
  arithmetic in `p`: first `m` with a primitive mixed minimal set is **`m=10` at
  `p=8011`** but **`m=8` at `p=9001`** (both top defect `d=6`; witnesses
  `E=[4,5,6,10,11,6841]`,`c=[344,4545,2873]` and
  `E=[4,11,988,1976,4786,5612]`,`c=[2935,4038,6254]`, re-verified). Gate (iv) pins
  it: primitive mixed present at `p=9001,m=8`, absent at `p=8011,m=8`.
- **Top-defect law is FALSE (certificate).** "Every mixed minimal sits at top defect
  `(t-1)ell`" fails: at `(4,3,6,p=8101)` the exhaustive count is `0`@`d=7`, **`27`@
  mid defect `d=8`(<top=9)**, `21651`@`d=9` (witness `[5,6,8,9,676,2123,2984,3751]`).
- **Open composite onsets (declared cap).** The `ell=6` primitive onsets `(3,6)`,
  `(4,6)` are **not** pinned: cores too large for exhaustive search, scanned at top
  defect only under declared caps (`EXACT_CAP=3·10^6`, `SAMPLE=2.5·10^5`) to `m=7`,
  no primitive set found there subject to those caps — not a vacancy claim.

**Named open target.** Primitive vacancy `PV(t,d,m)`: `m < d => #PrimMinMix(t,d,m)
= 0` (proved for `<= 1` active DFT-sector in companion Theorem B; open for `>= 2`).
Under `PV` at every level, (★) truncates to `#MinMix(t,ell,m) = Σ_{d|ell, 2<=d<=m}
#PrimMinMix(t,d,m)`. The descent makes `PV` the **only** remaining input for the
composite-`ell` full-petal question — orthogonal (a reduction, not a bound).

## Status, dependency, reproducibility

PROVED-LOCAL: D2, D3, D4 + recursion (★) (elementary, finitely re-verified).
CERTIFICATE: calibration count matches, `(3,3)` onset pair, top-defect refutation.
EXPERIMENTAL: census "0 primitive at `m<ell`". OPEN: `PV` for `>= 2` sectors, exact
composite-`ell` onsets. Consumes PR #219 bijection/collapse/rigidity (items 1/3/6)
and Theorems A,B of `l1_coset_mixed_vacancy_threshold.md` verbatim (no change to
either); supplies the composite-`ell` half of sub-obstruction (G2), and feeds the
`l1.tex` image-fiber / non-planted-extras ledger (`ImgFib` mass `= Σ_{d|ell} Q_d`,
each `Q_d` a level-`d` primitive-count pullback). No paper text changes; stays in
`experimental/`.

Verifier `experimental/scripts/verify_l1_stabilizer_descent.py` (stdlib-only,
offline, deterministic; exit 0 iff all gates pass): **(i)** set-level descent
bijection over EVERY `K`-invariant subset on 4 configs (kernel-iff, window
dictionary, mixed-iff, stabilizer transport, both sides directly); **(ii)**
minimality iff — anchor certifying immediate `=` full-subset minimality (`0`/28
kernels), two explicit `ell=6` witnesses (from `ell'=2` and `ell'=3`, FULL
minimality both sides), the K-invariant `<->` induced minimal-set bijection
(`6=6`, `10=10`); **(iii)** recursion (★) on the two `ell=6` configs (three terms
independently, imprimitive cross-checked block-strata vs induced) + `(3,4,4,8161)`
exhaustive end-to-end incl. the primitive top term; **(iv)** the `(3,3)` onset spot
pair. Scalar quantifier EXACT (nullspace + bad-hyperplane, no sampling).
`#PrimMinMix(t,6,m)=0` is DECLARED at the two `ell=6` configs (the `m<ell` residual,
confirmed exhaustively offline at `(3,6,4,487)`, beyond reach at `(4,6,5,499)`); the
`ell=4` gate exhausts it directly.
