# L1 Coset Mixed-Vacancy Threshold: `m <= t` Kills Primitive Full-Petal Extras

## Setting

Background-free coset sunflower over `F_p`. Let `H = mu_ell` be the order-`ell`
subgroup of `F_p^*` (`ell | p-1`). Petals `T_i = a_i H` (`i=1..t`, distinct
cosets), locators `L_{T_i} = X^ell - alpha_i`, `alpha_i = a_i^ell`. Core
`C = union_{j=1..m} b_j H`, `beta_j = b_j^ell`; `phi(Y) = prod_i (Y - alpha_i)`
(deg `t`), `Lambda(Y) = prod_j (Y - beta_j) = L_C` (deg `m`, `L_C = Lambda(X^ell)`).
Distinct nonzero scalars `c_i`; received word `U = c_i L_C` on `T_i`, `0` on `C`.
`k = m*ell+1`, `s = (m+1)*ell`. A full-petal codeword is a degree-`<= m*ell`
polynomial agreeing with `U` on all `t*ell` petal points; it is LISTED if it
agrees with `U` in `>= s` points. By the PR #219 bijection
(`l1_general_reconstruction_collapse.md`), listed full-petal codewords biject
with divisibility-minimal kernel sets `E` (`ell <= |E| <= (t-1)ell`,
`deg W_E <= |E|`), `E` = exact missed core. `E` is MIXED if not a union of full
`H`-cosets; PRIMITIVE if `Stab_H(E) = {1}` (else it descends to the
quotient/`Q_{d>1}` ledger). Companion to PR #218
(`l1_coset_petal_rank_collapse.md`, the `t=3` coset dichotomy).

## Theorem (vacancy threshold) — PROVED

If `m <= t`, EVERY full-petal codeword `P` (listed or not, any scalars) is a
polynomial in `X^ell`, hence `H`-invariant; its missed core is a union of full
`H`-cosets, so there is NO mixed minimal kernel set. If `m < t` there is at most
one full-petal codeword in total.

**Proof (sector / `mu_ell`-DFT).** Write `P` by exponent residue mod `ell`,
`P(X) = sum_{r=0}^{ell-1} X^r P_r(X^ell)` with `deg P_0 <= m`, `deg P_r <= m-1`
(`r>=1`). For `x = a_i h in T_i` (`h in H`), `x^ell = alpha_i`, so
`P(a_i h) = sum_r a_i^r P_r(alpha_i) h^r`. Full-petal agreement gives
`P(a_i h) = c_i L_C(a_i h) = c_i Lambda(alpha_i) =: gamma_i`, constant in `h`.
Thus the degree-`<ell` polynomial `sum_r a_i^r P_r(alpha_i) h^r - gamma_i`
vanishes at all `ell` points of `mu_ell`; every coefficient is `0`, so
`P_r(alpha_i) = 0` (`1 <= r <= ell-1`) and `P_0(alpha_i) = gamma_i` for all `i`.
Each `P_r` (`r>=1`) has degree `<= m-1` and vanishes at the `t` distinct
`alpha_i`; if `m <= t` then `m-1 < t`, forcing `P_r = 0`. Hence `P = P_0(X^ell)`,
`H`-invariant. `U` is `H`-invariant (`L_C = Lambda(X^ell)`, each `c_i` constant on
the `H`-invariant petal, `0` on the `H`-invariant core), so the missed core
`{x in C : P(x) != 0}` is `H`-invariant, a coset union; by the PR #219 bijection
every minimal kernel set is the exact missed core of such a `P`, hence not mixed.
If `m < t`, `P_0` has degree `<= m` and is pinned at the `t > m` points `alpha_i`,
so it (and `P`) is unique if it exists. ∎

**Sharpness (why `m <= t` cannot be relaxed to `m <= t+1`).** Mixed needs some
`P_r != 0` (`r>=1`), i.e. `phi | P_r` with `deg P_r <= m-1`, needing
`m-1-t >= 0`, i.e. `m >= t+1`. The threshold `m = t+1` is attained: explicit
mixed minimal kernel sets (verifier-gated) at
- `(t=3, ell=4, m=4)`, `p=8161`, `c=(2408,3412,6002)`:
  `E = [4,5,6,7,8154,8155,8156,8157]`, `deg W_E = 8 = |E|`, agreement `s=20`,
  `Stab_H(E) = mu_2`;
- `(t=4, ell=3, m=5)`, `p=8101`, `c=(3487,4735,3412,6002)`:
  `E = [5,6,7,8,9,676,1534,2894,2984]`, `|E|=9`, agreement `s=18`,
  `Stab_H(E) = {1}` (primitive).

## Support-fraction corollary — scope, stated carefully

Within the sunflower's own support (`n_supp = (t+m)ell` points), `k-1 = m*ell`,
so the support fraction is `(k-1)/n_supp = m/(m+t)`, and `m <= t <=>
m/(m+t) <= 1/2` (exactly, no edge cases): the Theorem covers precisely the
PETAL-HEAVY coset sunflowers — at least as many petals as core cosets. This
support fraction is NOT the ambient rate `rho = k/n` of `l1.tex` (`n = |H|`,
`k = rho n + O(1)`): the sunflower is carved from a larger evaluation domain
(petals lie in `H_n \ C`), so `n >= n_supp` and, at ANY ambient rate `rho` —
including every point of the displayed dyadic window `{1/2,1/4,1/8,1/16}` —
the petal count `t` is a free parameter: configurations with `m > t`
(uncovered by the Theorem) coexist with covered ones at the same `rho`. In
the prize regime (`m = O(log n)`, `ell ~ n/log n`, `t` free) the load-bearing
statement therefore remains the OPEN primitive `m < ell` vacancy below; the
Theorem contributes the petal-heavy corner `m <= t` unconditionally, and
Theorem B removes the single-sector stratum for every `(t, m)`.

## Refutation (composite `ell`) — EXPERIMENTAL, certificate-backed

The naive statement "`m < ell` => no mixed minimal kernel set" is FALSE for
COMPOSITE `ell`. Certificates at `(t=3, ell=6, m=4)` (so `m < ell = 6`), each with
`|E| = (t-1)ell = 12`, `deg W_E = 12`, agreement `s = 30`, `M(E) = E`, minimal,
mixed, and IMPRIMITIVE `Stab_H(E) = mu_3` (order 3):
- `p=487`, `c=(486,317,379)`, `E=[4,5,6,42,63,170,186,296,324,418,441,480]`;
- `p=2011`, `c=(381,1494,991)`,
  `E=[5,7,569,781,824,981,1025,1191,1236,1435,2005,2007]`;
- `p=499`, `c=(97,23,83)`,
  `E=[5,6,7,18,61,158,196,298,335,442,474,495]`.

Petals/core are `cs[:t]` / `cs[t:t+m]` in primitive-root coset order; all data is
embedded in the verifier. Structural finding (EXPERIMENTAL): every observed
`m < ell` mixed minimal kernel set is a union of cosets of a PROPER subgroup
`H' < H` (order 2 or 3), i.e. imprimitive; NO primitive mixed minimal set was
found anywhere at `m < ell`.

**Corrected open target (named).** PRIMITIVE `m < ell` mixed-vacancy: `m < ell`
=> no stabilizer-primitive mixed minimal kernel set. This is the object the L1
residual actually needs (`Q_1^list`); imprimitive mixed sets are correctly charged
to `Q_{d>1}`. Two proved partials narrow it:

- **Theorem B (single active sector, all `ell`) — PROVED.** Let
  `S = {r >= 1 : P_r != 0}` (active sectors) and suppose `|S| = 1`, sector `r0`,
  `d0 = gcd(r0, ell)`. On core coset `j`, `P(b_j h) = v_{j,0} + v_{j,r0} h^{r0}`;
  its zeros in `mu_ell` are empty or one fiber of `h -> h^{r0}` (a `mu_{d0}`-coset),
  so the retained set on every coset is `mu_{d0}`-invariant and `Stab_H(E) supset
  mu_{d0}`. A count (write `P_{r0} = phi * g_{r0}` — possible since
  `P_{r0}(alpha_i) = 0` for all `i` — so `deg g_{r0} <= m-t-1`; a DEAD coset,
  sector `r0` vanishing at `beta_j`, is a root of `g_{r0}` because
  `phi(beta_j) != 0`, so dead cosets `<= m-t-1`; live cosets retain `<= d0` each)
  gives `retained <= (m-t-1)ell + d0(t+1)`; if `d0(t+1) < 2ell` the word is
  unlisted. Hence a LISTED `|S|=1` mixed word has `d0 >= 2`, so `Stab_H(E) supset
  mu_{d0}` is nontrivial — NON-primitive. For prime `ell` (`d0=1`) there is no
  listed `|S|=1` mixed word whenever `t+1 < 2ell` — in particular throughout the
  `t < m < ell` regime. Unconditional (only the fiber count of `h -> h^{r0}`); it
  explains the composite witnesses (`r0=3`, `d0=gcd(3,6)=3`, `mu_3`-invariant).
- **Lemma L2 — PROVED.** A mixed minimal kernel set fully contains at most `t-2`
  core cosets, hence meets `>= t+1` cosets (`>= 3` only partially). Proof: if
  `>= t-1` cosets were fully inside `E`, any `t-1` of them form a coset-union
  kernel set `E_J subset E` (`|E_J| = (t-1)ell`, `deg W_{E_J} = ell*deg w_J <=
  ell(t-1) = |E_J|`); minimality forces `E_J = E`, contradicting `E` mixed.
  The "meets `>= t+1`" step also uses the fully-retained bound: the codeword of a
  mixed `E` has some sector `P_r != 0` (`r >= 1`) with `g_r = P_r/phi` of degree
  `<= m-t-1`, and a coset disjoint from `E` (fully retained) forces
  `g_r(beta_j) = 0` for ALL `r >= 1`; so `<= m-t-1` cosets are disjoint from `E`
  (else every `g_r = 0`, `E` not mixed), i.e. `E` meets `>= t+1`; subtracting the
  `<= t-2` fully-contained ones leaves `>= 3` met only partially.

The residual danger is `|S| >= 2`. The tempting char-`0` Fourier/uncertainty bound
(`a`-sparse `=> <= a-1` roots) is UNSOUND over `F_p` (`5 + h + 2h^3` has 3 roots
in `mu_11 subset F_23`), so `|S| >= 2` is not Fourier-controlled; the target needs
an arithmetic descent/minimality argument (rigidity hierarchy for prime `ell`,
subgroup-peeling descent for composite `ell`).

## Sampling-artifact correction — EXPERIMENTAL honesty note

The `(t=4, ell=3, m=5)` cell has a GENUINE primitive mixed minimal kernel set
(`p=8101`, `c=(3487,4735,3412,6002)`, `E` as above, `Stab_H(E) = {1}`, agreement
`s=18`, `deg W_E = 9`). An earlier informally-sampled scan (maximizing over a few
hundred scalar vectors per cell) reported `mixed = 0` here; that was a sampling
artifact — an exact all-scalar search finds the set. This datum supersedes that sampled zero, is verifier-gated (gate iv), and
is consistent with primitive mixed sets appearing only at `m >= ell` (`5 >= 3`).

## Status

PROVED-LOCAL: the vacancy Theorem (`m <= t`; merged from two independent
sector-decomposition proofs, cross-checked against a linear-algebra decode
battery); Theorem B (`|S|=1` primitive vacancy, all `ell`); Lemma L2. The `m=t+1`
sharpness and composite-`ell` `m<ell` refutation are verifier-gated CERTIFICATES.
EXPERIMENTAL / OPEN: the "all `m<ell` mixed sets are imprimitive" finding and the
primitive `m<ell` vacancy for `|S| >= 2` (no primitive mixed set known at `m<ell`).

## Parameters

Theorem battery: `p in {29,31,41}`, `ell in {2,3,4}`, `t in {2,3}`, `m <= t`, two
scalar vectors each (30 configs). Sharpness: `(3,4,m=4)` `p=8161`, `(4,3,m=5)`
`p=8101`. Refutation: `ell=6`, `t=3`, `m=4`, `p in {487,499,2011}`. All scalars
distinct nonzero; petals/core are genuine `mu_ell` cosets.

## Existing paper dependency

Uses the PR #219 bijection verbatim; provides the base-theorem floor and the
CORRECTED (primitive) form of the `m < ell` mixed-vacancy that PR #219's ledger
flagged as the named next target, superseding its provisional "no mixed observed
at `m < ell`" with the exact composite-`ell` counterexamples. Feeds `l1.tex` Prop.
`dyadic planted crossings` and its remark (primitive image-fiber theorem /
non-planted extras ledger): the primitive full-petal contribution of PETAL-HEAVY
(`m <= t`) coset configurations is `0` unconditionally; the general
displayed-window demand remains on the open primitive `m < ell` target. No paper
text changes; material stays in `experimental/`.

## Evidence and coverage

Method: exact all-scalar linear-algebra feasibility over `F_p` (`W_E` = CRT rep by
petal interpolation, kernel iff `deg W_E <= |E|`; lift space by Gaussian
elimination). Coverage limits (verbatim honest): the SCALAR quantifier is always
EXACT — for each tested subset, existence of a qualifying scalar vector is decided
by nullspace + bad-hyperplane linear algebra, no scalar sampling. For PRIME
`ell in {3,5}` the SUBSET lattice was also exhaustive at every tested `m < ell`
config: NO mixed minimal-feasible set exists there. For COMPOSITE `ell = 6` the
subset lattice was FUNNELED (defects `{ell, ell+1, (t-1)ell}` only, with random
subset sampling inside the largest top-defect layers), so the composite refutation
is by explicit certificate plus funnel search, and composite full-vacancy at the
skipped defects is not claimed. The single-sector
Fourier route provably fails over `F_p`, so `|S| >= 2` is not Fourier-controlled.

## Reproducibility and constants

Verifier `experimental/scripts/verify_l1_coset_mixed_vacancy_threshold.py`
(stdlib-only, offline, deterministic; exit 0 iff all gates pass), four gates:
(i) base theorem over 30 coset configs with `m <= t` — lift space `H`-invariant by
exact Gaussian elimination AND zero mixed minimal kernel set by core enumeration;
(ii) sharpness at `m = t+1` for `(3,4)` and `(4,3)`; (iii) the three composite-`ell`
`m < ell` refutation certificates (kernel, EXHAUSTIVE minimality over all proper
subsets of size `>= ell`, `M(E)=E`, mixed, listed, `Stab = 3`); (iv) the
`(4,3,m=5)` primitive correction (`Stab = 1`). Constants: kernel range
`[ell, (t-1)ell]`; listedness `s = (m+1)ell`; stabilizer orders `3,3,3`
(refutation), `2`/`1` (`(3,4)`/`(4,3)` sharpness); witness point-sets embedded.
