# L2 Interleaved Lists: Dilation Symmetry and the Sharp-Constant Target

- **Status:** PROVED (dilation symmetry) / EXPERIMENTAL (constants scan) / AUDIT.
- **Agent/model:** Claude Opus 4.8.
- **Date:** 2026-06-19.
- **Scope:** L2 (sharp interleaved-list constants near capacity), `agents.md`;
  `tex/slackMCA_v3.tex` interleaved-list ledger and `tex/snarks_v4.tex` Paper C
  budget. Builds on `experimental/l2_interleaved_support_bridge.md` and
  `experimental/l1_l2_random_support_fiber_baseline.md`. This note does not edit
  Papers A--D and is list/locator side only; it does not touch the M1 work. It
  transfers the dilation-symmetry method developed for L1
  (`l1_prefix_divisor_count.md` §6, §9) to the interleaved setting.

## Goal

The bridge note reduces the interleaved (column-distance) list to the
common-intersection profile of full agreement supports, and shows the trivial
`mu`-th power exponent is not intrinsic. What is still missing (SUMMARY.md) is a
*worst-case sharp constant* for concrete arity `mu` and radius `1-a/n` near
capacity. This note adds the symmetry that cuts the worst case and frames the
target precisely, with a verifier.

## 1. Dilation symmetry of the interleaved list

`H = mu_n` acts on received words by dilation. For `h in H` and a `mu`-row word
`U = (U_1,...,U_mu)`, define the *diagonal* action
```text
(h . U)_i(x) = U_i(h^{-1} x),       i = 1,...,mu.
```

**Theorem (dilation invariance of the interleaved list).** For every `h in H`,
`a >= k`, and interleaved word `U`,
```text
|Lambda(Int(C,mu), 1 - a/n, h . U)| = |Lambda(Int(C,mu), 1 - a/n, U)|.
```
Hence the worst-case interleaved list
`Lst(Int(C,mu),1-a/n) = max_U |Lambda(...,U)|` is attained on a set of
dilation-orbit representatives of `(F_q^H)^mu`, cutting the worst-case search by
up to a factor `n`.

*Proof.* Per row, `P |-> P^h`, `P^h(x) = P(h^{-1}x)`, is a degree-preserving
bijection of `C` with agreement set `A_{P^h}(U_i^h) = h \cdot A_{P_i}(U_i)`
(`l1_prefix_divisor_count.md` §9). For an interleaved codeword
`c = (c_1,...,c_mu)`, the common agreement support of `c^h = (c_1^h,...,c_mu^h)`
with `h.U` is
```text
A_{c_1^h}(U_1^h) cap ... cap A_{c_mu^h}(U_mu^h)
   = h \cdot ( A_{c_1}(U_1) cap ... cap A_{c_mu}(U_mu) ),
```
which has the same size. So `c` is listed against `U` iff `c^h` is listed against
`h.U`, and `c |-> c^h` is a bijection of the two lists. ∎

This is the L2 analogue of the L1 dilation equivariance, and it composes with the
bridge note's quotient-core diagonalization: the dilation-*fixed* interleaved
words (those with `U_i = U_i(h^{-1}X)` for a nontrivial `K_d <= H`, i.e. periodic
rows) are exactly the structured packets whose interleaved count is diagonal, not
Cartesian.

## 2. The sharp-constant target

The random baseline (bridge note; `l1_l2_random_support_fiber_baseline.md`) is
```text
E |Lambda(Int(C,mu), 1 - a/n, U)|  <=  binom(n, a) q^{-mu (a-k)},
```
saving the factor `binom(n,a)^{mu-1}` against the product-of-row-lists baseline
`binom(n,a)^mu q^{-mu(a-k)}`. The **L2 sharp-constant conjecture** (target form):
for generated-field smooth domains, above the corrected reserve,
```text
Lst(Int(C,mu), 1 - a/n)  <=  binom(n,a) q^{-mu(a-k)} + Quot_mu + n^B,
```
where `Quot_mu` is the *aligned* quotient-core packet count
`L_mu(a,tau)` of the bridge note (diagonal, **not** raised to the `mu`-th power),
and the `n^B` is the aperiodic interleaved remainder. By §1 it suffices to bound
this on dilation-orbit representatives, and by the bridge formula it reduces to
the common-intersection profile of full agreement supports --- the same
quotient/aperiodic split as L1, now for `mu`-fold intersections.

## 3. Numerical confirmation (`F_17, n=16, mu=2`)

`verify_l2_interleaved_constants.py` builds full agreement-support families for
several row words and computes the exact 2-row interleaved list and simultaneous
fiber. At `k=6, a=8`:

| rows | interleaved | fiber | cartesian (`|Supp|^2`) | ratio |
|---|---:|---:|---:|---:|
| rand0 x rand1 | 33 | 73 | 1089 | **0.030** |
| periodic x rand | 33 | 73 | 33 | 1.0 |
| monomial x periodic | 54 | 54 | 54 | 1.0 |

It verifies: the bridge `interleaved <= fiber <= min_i |Fib_Ui(a)|`; the
sub-Cartesian bound `interleaved <= prod |Supp|` (ratio `0.03` for the generic
random pair --- the saving in action); repeated-row diagonalization
`Lambda(Int,(V,V)) = Lambda(C,V)`; and the §1 dilation symmetry (invariance of
the interleaved list under `h.U` for sampled `h`).

## 4. Exact quotient-core interleaved count `Quot_mu`, brute-validated

The `Quot_mu` term of §2 is the bridge note's aligned-packet count
`L_mu(a,tau)`. This section pins it exactly (validated against direct
enumeration) and quantifies the diagonal<->Cartesian saving at prize parameters.

With `K <= H` of order `M`, `N = n/M`, `ell = k/M`, `Q = N-1`, slack overlap
`tau`, and `h(a,tau) = ceil((a-tau)/M)`,
```text
L_mu(a,tau) = sum_{c=h}^{ell} binom(Q,c) E_empty(Q-c, ell-c, mu),
E_empty(R,b,mu) = sum_{j=0}^b (-1)^j binom(R,j) binom(R-j, b-j)^mu
                = # of mu ordered b-subsets of [R] with empty common intersection.
```

**Validated (PROVED-by-check).** `verify_l2_quotient_core_count.py --self-check`
confirms `E_empty` and `L_mu` against brute enumeration across many
`(N,ell,mu,M,tau,a)`, and the two endpoints
```text
a = k+sigma  (h = ell)  =>  L_mu = binom(Q,ell)      (diagonal L),
h = 0                   =>  L_mu = binom(Q,ell)^mu   (full Cartesian).
```
The count is a step function of the threshold `a`: for `N=6, ell=2, mu=2, M=4,
sigma=tau=2` it is `10` (diagonal) for `a in {7,...,10}`, jumps to `70` for
`a in {3,...,6}`, and reaches `100 = 10^2` (Cartesian) for `a <= 2`.

**Prize-parameter saving.** At the quotient-core threshold `a = k+sigma` with
aligned slacks (`tau = sigma`), the packet is exactly diagonal:

| n | k | M | mu | `L_mu` at `a=k+sigma` | Cartesian `L^mu` |
|---|---|---|---|---|---|
| 256 | 64 | 4 | 2 | `binom(63,16) ~ 3.66e14` | `~1.3e29` |
| 256 | 64 | 4 | 3 | `binom(63,16) ~ 3.66e14` | `~4.9e43` |
| 1024 | 256 | 8 | 2 | `binom(127,32) ~ 1.11e30` | `~1.2e60` |

So the aligned quotient-core packet --- the dominant *structured* interleaved
obstruction --- contributes only its single-row size `binom(Q,ell)`, saving the
entire `binom(Q,ell)^{mu-1}` Cartesian factor. This is the exact value of
`Quot_mu` in the §2 sharp-constant conjecture: the structured part of the
interleaved list does **not** pay the interleaving exponent, consistent with the
§1 dilation invariance (these packets are the dilation-fixed periodic words).

## 5. Higher arity and the codegree certificate (`mu = 2, 3`)

`verify_l2_interleaved_constants.py` now also computes the exact `mu=3`
interleaved list and the intersection-codegree certificate. At
`F_17, n=16, k=6, a=8`:

| rows | interleaved | Cartesian `|Supp|^mu` | ratio |
|---|---:|---:|---:|
| rand0 x rand1 (`mu=2`) | 33 | 1089 | 0.030 |
| rand0 x rand1 x rand2 (`mu=3`) | 33 | 35937 | **0.0009** |

The generic interleaved list stays at the single-row value `33` while the
Cartesian product grows as `33^mu`, so the **saving grows with the arity** ---
the structural content of the bridge `|Lambda| <= min_i |Fib_Ui(a)|`, seen to be
far below the product at every `mu`. The codegree certificate
`|Lambda(Int(C,2),...)| <= |P| * Gamma_{>=a}(P,Q)` is verified and here *tight*:
`Gamma_{>=a} = 1` for the generic pair, so `33 = |P| * 1` is met with equality.
Repeated-row diagonalization and the §1 dilation invariance are re-checked at
`mu=3`.

This is evidence (not a worst-case theorem) that the sharp-constant conjecture's
`mu`-independence of the numerator holds for generic rows: the only `mu`-growth
is in the field-power denominator `q^{-mu(a-k)}` and the diagonal `Quot_mu`, not
in a Cartesian support exponent.

## 6. Extension-coordinate identity (L2 <-> extension lists), verified

The bridge note's basis-invariant identity `|Lambda(C_F,delta)| =
|Lambda(Int(C_B,e),delta)|` lets an extension-code list certificate reuse the L2
machinery. `verify_l2_extension_coordinate.py` checks it directly for `e=2` over
`B = F_17`, `F = F_{17^2} = F_17[t]/(t^2-3)`: the left side is computed by
list-decoding over `F_{289}`, the right side from the two base-field coordinate
support families `Supp_{pi_0(U)}(a), Supp_{pi_1(U)}(a)` and their intersection
profile. For every tested received word `U : H -> F_{289}` (`k=6, a=8`) the two
independent computations agree (e.g. `|Lambda(C_F)| = 33 =` coordinate-interleaved
base list).

**Consequence.** The dilation symmetry (§1), exact `Quot_mu` (§4), and codegree
certificate (§5) all transfer to extension-code lists through the `e` coordinate
rows: an extension challenge does *not* introduce a new support exponent, and the
generated-field entropy ledger is unchanged (the coordinate support families are
base-field `B` objects; only the final list-size-over-field denominator changes
when a protocol consumes the extension code). This is the list-side counterpart
of the F1 extension-line questions, kept strictly on the list ledger.

## Ledger impact

- **Interleaved list (improves):** the worst-case interleaved list is a
  dilation-orbit invariant, so a worst-case L2 certificate may restrict to orbit
  representatives.
- **Quotient (clarified):** the structured interleaved packets are the
  dilation-fixed (periodic) words, whose count is diagonal (bridge note), not
  Cartesian.

## Status / what to do next

- PROVED: dilation invariance of the interleaved list; worst-case reduction (§1).
- PROVED-by-check: the exact `Quot_mu = L_mu(a,tau)` count and its diagonal
  endpoint at prize parameters (§4), saving the full `binom(Q,ell)^{mu-1}` factor.
- TARGET: the sharp-constant conjecture above. Next: (a) bound the *aperiodic*
  `mu`-fold intersection remainder on orbit representatives (the L2 analogue of
  the L1 aperiodic step) --- the genuine open piece; (c) extend the scanner to
  `mu=3` and the extension-coordinate presentation
  `|Lambda(C_F,delta)| = |Lambda(Int(C_B,e))|`, with second-moment/codegree data.

## Reproducibility

```bash
python3 experimental/verify_l2_interleaved_constants.py
python3 experimental/verify_l2_interleaved_constants.py --a 9 --format json
python3 experimental/verify_l2_quotient_core_count.py --self-check
python3 experimental/verify_l2_quotient_core_count.py
python3 experimental/verify_l2_extension_coordinate.py
```
