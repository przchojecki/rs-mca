# L1: sigma calculus for the petal syzygy space (and the sigma-form of `E_3 <= ell`)

**Type: structural toolkit + one first-class NEGATIVE result.** This note packages, with
complete proofs, the five PROVED lemmas of the co-fiber syzygy space `sigma`, verifies every one
of them **on the `#330` counterexamples** (where they must hold — that is the point of a *correct*
reduction whose only false endpoint was `delta <= K`), and derives the **exact `sigma`-form of the
post-`#330` candidate law `E_3 <= ell`**. Along the way the note's own verifier finds and files the
**falsifier of prediction P2** (`K = 3 => sigma <= 1`), refuted by an explicit realizable `[6,6,6]`
config — by the *same* big-fiber undershoot that killed the old `E_3 <= ell-2` KEY LEMMA.

**Status legend:** PROVED (rigorous proof + exact `F_p` verification) / COUNTEREXAMPLE (refuted,
explicit object) / CONJECTURAL_WITH_FALSIFIER (well-supported, falsifier named) / SURVIVES
(unchanged from a cited note). All arithmetic exact over `F_p`, stdlib only; no floating point.

Notation inherited from `l1_prime_ell_frontier_corrected.md` §2-§3 and its `#330` companion. `ell`
odd prime, `ell | p-1`, `H = mu_ell`, cosets `bH` partition `F_p^*`, `n = (p-1)/ell`. A mixed
`Gamma(X) = sum_{r=1}^{ell-1} gamma_r X^r` (constant-free, `deg <= ell-1`) has, per coset,
level sets; the **max fiber** per coset (size `mu_b`) is the object of study. A **config** is the
collection of max-fibers `F_1, ..., F_K` on the `K` distinct cosets with `mu_k >= 2`;
`P = sum_k mu_k`, `W_k = c_k^ell` (distinct coset labels), `E_3 := sum_k (mu_k - 2)`. Per fiber:
`g_k = prod_{x in F_k}(X - x)` (deg `mu_k`, squarefree), and the **co-fiber locator**
`h_k := (X^ell - W_k)/g_k` (deg `ell - mu_k`), which vanishes exactly on
`cofiber_k := c_k H \ F_k` (`ell - mu_k` points). The syzygy space and its dimension:

> `V_k := h_k * F_p[X]_{<= mu_k-2}` `= {f : deg f <= ell-2, f vanishes on cofiber_k}` (dim `mu_k-1`);
> `Vsum := V_1 + ... + V_K`;  **`sigma := dim{(a_k) : deg a_k <= mu_k-2, sum_k a_k h_k = 0} = (P-K) - dim(Vsum)`.**

Duals: `D := {lambda in F_p^P : sum_{i in F_k} lambda_i = 0 forall k}` (within-fiber-mean-zero,
`dim = P-K`); `Z := {lambda : sum_i lambda_i V(x_i) = 0}`, `V(x) = (1, x, ..., x^{ell-1})`;
`delta := dim(D cap Z)`; `U := {A : deg A <= ell-1, A constant on each fiber}`; `rho :=` rank of
the `P-K` coincidence rows `{v(x)-v(anchor_k)}`, `v(x) = (x, ..., x^{ell-1})`.

**Objects of verification** (used throughout; every lemma is checked on **all** of them):
- **Witnesses** (`E_3 = ell-2`, the old extremal chart, `sigma = K`): `ell=11 p=331`
  `gamma=[97,29,97,239,171,92,143,155,270,1]` (spectrum `[5,5,4,3,2,2,2]`); and the reconstructed
  `ell=23 p=139` D3 witness `gamma=[12,79,132,135,100,118,97,22,50,20,86,134,91,89,92,110,11,56,39,17,0,1]`
  (spectrum `[8,8,6,4,4,3]`, `E_3=21`).
- **`#330` counterexample Gammas** (all seven of `l1_prime_ell_key_lemma_refuted.md` §1 — **unmerged
  companion branch** `l1-key-lemma-refuted`, not present on this branch; see Refs — plus the
  four sub-onset listers of §2.2): `ell=11 p in {67,199,331}`, `ell=13 p in {79,313}`,
  `ell=17 p in {103,409}`, `ell=19 p=191`, `ell=23 p in {139,599,691}` — 11 configs with
  `E_3 = ell-1` (and `E_3 = ell` at `ell=23 p=139`).

---

## 0. Headline

1. **The five lemmas are PROVED and hold verbatim on the counterexamples.** `sigma = delta`
   (moment bridge), `dim(Vsum) = ell - dimU`, pairwise `V_i cap V_j = 0` (hence `K=2 => sigma=0`),
   the syzygy recursion `sigma = sum_m t_m` with `t_1 = t_2 = 0` and the unconditional bound
   `sigma <= sum_{all-but-two-largest}(mu-1)`, and the `K=3` bound `sigma <= min_k mu_k - 1`.
   Verified `PASS` on all 13 objects (§1). This confirms `#330`'s claim that the reduction chain
   is **internally correct**; only its endpoint `delta <= K` was false.

2. **Exact `sigma`-form of the new law (§2).** The proved identity chain collapses to the single
   **master identity**
   > **`sigma = delta = E_3 + K - ell + dimU`**  (verified with `dimU in {2,4,7}` across configs
   > and sub-configs),
   whence for every constant `c`, `E_3 <= ell + c  <=>  sigma <= K + dimU + c`. Therefore the
   post-`#330` candidate law is exactly
   > **`E_3 <= ell   <=>   sigma <= K + dimU`**,  and on the extremal chart where every observed
   > max-`E_3` config lives (`dimU = 2`), **`sigma <= K + 2`** — precisely *one frontier
   > `m`-step* weaker than the refuted `sigma <= K` (`= E_3 <= ell-2`). The intermediate reading
   > `sigma <= K+1` (`= E_3 <= ell-1`) is **not** the law: it is falsified by the `ell=23 p=139`
   > witness (`sigma = K+2`, `E_3 = ell`).

3. **The unconditional recursion bound already proves the law *on the counterexamples* (§2.3).**
   `sigma <= sum_{all-but-two-largest}(mu-1) <= K+2` holds on **all 11** `#330` counterexample
   spectra (tight, `= K+2`, at `ell=23 p=139` and `ell=13 p=79`); the bound overshoots `K+2` only
   when the excess is *not* concentrated in the two largest fibers (`E_3 > mu_1+mu_2`), the single
   such object being the D3 witness `[8,8,6,4,4,3]` (`B_rec = 13 > 8`), where realizability alone
   closes the residual gap (actual `sigma = 6`).

4. **COUNTEREXAMPLE — prediction P2 (`K=3 => sigma <= 1`) is FALSE (§2.4).** Explicit realizable
   `K=3` config `[6,6,6]` at `ell=13, p=79` (three max-fibers of the `#330` `p=79` Gamma) has
   **`sigma = 4`**. Lemma 5 (`sigma <= min(mu)-1 = 5`, a THEOREM) survives; the *sharper* empirical
   P2 dies. The refuter is invisible to random `gamma`-sampling (1013 random realizable `K=3`
   configs: 0 violations, max `sigma = 1`) — the **identical small-fiber undershoot** that `#330`
   diagnosed for the KEY LEMMA. P2 converts from CONJECTURAL_WITH_FALSIFIER to COUNTEREXAMPLE.

5. **Two expanded falsifier hunts this session found nothing (§2.5).** A dedicated hunt for
   `E_3 >= ell+1` (the direct falsifier of the law in item 2) across `ell in {11,...,29}`
   (~10,600 configs) found **no counterexample**. A second-attempt `ell=19, m=10` listing hunt
   (`#330`'s companion open question, not this note's own claim) also found **nothing**. Neither
   changed the (then) 13-object table; both are recorded as additional (non-exhaustive) supporting
   evidence.

6. **ADDENDUM (Wave 11) — the law is PROVED on the covered chart; the residual is a sharp, TIGHT
   conjecture (§2A).** **Theorem 1:** if `T := sum_{k>=3}(mu_k-2) <= 4` then
   `E_3 <= mu_1+mu_2 <= ell` (`sigma <= K+dimU`) — i.e. the law `E_3 <= ell` **unconditionally on the
   covered chart**, from L3 + the master identity alone (no recursion). The residual chart `T >= 5`
   is the **Residual Conjecture RC**, the sole remaining piece, and it is **TIGHT**: two realizable
   residual configs attain `E_3 = ell` (`[11,10,5,4,3,2]` @ `(23,139)`,
   `[14,13,5,5,2,2,2,2]` @ `(29,233)`; re-verified from scratch), so RC admits **no** margin proof.
   A mid-session over-claim that the residual carried a 2-unit margin (prediction P-B) was caught by
   the mandated numeric closure and **retracted**; the law itself survives (0 falsifiers `E_3>=ell+1`
   across ~10,200 new configs). NO-GO diagnostics (§2A.3) rule out the linear-algebra / degree /
   moment routes. Verifier upgraded to **15 objects + gate (ix)** (both new witnesses gated).

---

## 1. The five PROVED lemmas (with proofs; verified on witnesses AND counterexamples)

Aggregate verification (`experimental/scripts/verify_l1_sigma_calculus.py`, exact `F_p`): every
check below is `PASS` on all 13 objects of §1.6 (and — added in the Wave-11 Addendum §2A.2 — on the
**2 residual-tight witnesses**, so the shipped verifier's five-lemma gates run on **15** objects).
Per-object invariants (`sigma`, `delta`, `dimU`, `dimVsum`, `rho`) and the identity web are
tabulated in §1.6.

### Lemma 1 (MOMENT BRIDGE `=> sigma = delta`). PROVED.

> For `(a_k)` with `deg a_k <= mu_k - 2`, put `lambda_i := a_k(x_i)/g_k'(x_i)` (`i in F_k`). Then
> **`sum_k a_k h_k = sum_{s=0}^{ell-1} M_s X^{ell-1-s}`,  `M_s := sum_i lambda_i x_i^s`.**
> Consequently `sum_k a_k h_k = 0  <=>  lambda in Z`, and `deg a_k <= mu_k-2  <=>  lambda in D`,
> so the syzygy space is `D cap Z` and **`sigma = delta`.**

*Proof.* Since `deg a_k < deg g_k = mu_k` and `g_k` is squarefree,
`a_k/g_k = sum_{i in F_k} lambda_i/(X - x_i)` with `lambda_i = a_k(x_i)/g_k'(x_i)`. Hence
`a_k h_k = a_k(X^ell - W_k)/g_k = sum_{i in F_k} lambda_i (X^ell - W_k)/(X - x_i)`. For `x_i in F_k`
we have `x_i^ell = W_k`, so `X^ell - W_k = X^ell - x_i^ell = (X - x_i) sum_{s=0}^{ell-1} x_i^s X^{ell-1-s}`,
giving `(X^ell - W_k)/(X - x_i) = sum_s x_i^s X^{ell-1-s}`. Summing over `i` and `k`:
`sum_k a_k h_k = sum_i lambda_i sum_s x_i^s X^{ell-1-s} = sum_s (sum_i lambda_i x_i^s) X^{ell-1-s}`,
which is the claim. The coefficient of `X^{ell-1-s}` is `M_s = (sum_i lambda_i V(x_i))_s`, so the
LHS vanishes iff `sum_i lambda_i V(x_i) = 0`, i.e. `lambda in Z`. Finally
`a_k = g_k sum_i lambda_i/(X-x_i) = sum_i lambda_i prod_{j != i}(X - x_j)`, whose `X^{mu_k-1}`
coefficient is `sum_{i in F_k} lambda_i`; thus `deg a_k <= mu_k-2` iff that fiber-sum is `0`, i.e.
`lambda in D`. The map `(a_k) <-> lambda` is a bijection (Lagrange interpolation per fiber), so the
syzygy space `≅ D cap Z` and `sigma = dim(D cap Z) = delta`. ∎

*Verification.* `moment_bridge` identity holds for 25 random `(a_k)` on each object; `sigma == delta`
on all 13 (both computed by independent solves). **PASS.** [Resolves D1's "`sigma=delta` needs a
written proof".]

### Lemma 2 (LOCATOR DUALITY `dim(Vsum) = ell - dimU`). PROVED.

> **`dim(Vsum) = rho = ell - dimU`**, equivalently **`sigma + rho = P - K`** and
> **`dimU + dim(Vsum) = ell`.**

*Proof.* By construction `dim(Vsum) = (P-K) - sigma`. The `P-K` coincidence rows are the image of
`D` under `phi : e_i |-> V(x_i)`, whose kernel is `Z`; hence `rho = dim phi(D) = (P-K) - dim(D cap Z)
= (P-K) - delta` (the §2.2 rank formula). With Lemma 1 (`sigma = delta`) this gives
`dim(Vsum) = (P-K) - delta = rho`. For the second equality: `A in U` iff `A(x) = A(x')` for
`x, x'` in a common fiber, i.e. iff the coefficient vector of `A` (length `ell`) is annihilated by
every coincidence row; those rows carry a `0` in the constant slot, so their rank as `ell`-column
vectors equals `rho`, and `dimU = ell - rho`. Hence `dim(Vsum) = rho = ell - dimU`. ∎

*Verification.* `dVs == ell - dU` and `rho == dVs` on all 13. **PASS.** [Upgrades D_extra's
`V ⊆ U^perp` inequality to the equality D1 left open.]

### Lemma 3 (PAIRWISE `V_i cap V_j = 0`; hence `K=2 => sigma = 0`). PROVED.

> For any two fibers of one `Gamma`, `mu_i + mu_j <= ell` (pairwise cap), and then
> **`V_i cap V_j = 0`.** In particular for `K = 2`, **`sigma = 0`.**

*Proof (cap).* Choose `(alpha, beta, gamma)` nonzero solving `alpha W_i + beta lambda_i + gamma = 0`
and `alpha W_j + beta lambda_j + gamma = 0` (two equations, three unknowns), where `lambda_i,
lambda_j` are the fiber values. The form `Phi := alpha X^ell + beta Gamma + gamma` then vanishes on
`F_i` (where `X^ell = W_i`, `Gamma = lambda_i`) and on `F_j`; it is a **nonzero** polynomial (if
`alpha = 0` then `beta Gamma = -gamma` forces `beta = gamma = 0` since `Gamma` is constant-free of
positive degree) of degree `<= ell`, so `mu_i + mu_j <= ell`.
*Proof (intersection).* `V_i cap V_j = {deg <= ell-2 : vanishes on cofiber_i cup cofiber_j}`. The
two co-fibers lie in distinct cosets (distinct `W`), hence are disjoint, of total size
`(ell - mu_i) + (ell - mu_j) = 2ell - (mu_i + mu_j) >= ell`. A nonzero polynomial of degree `<= ell-2`
has at most `ell-2 < ell` roots, so it cannot vanish there: `V_i cap V_j = 0`. For `K = 2`,
`dim(Vsum) = dim V_1 + dim V_2 - 0 = (mu_1-1)+(mu_2-1) = P-K`, so `sigma = (P-K) - dim(Vsum) = 0`. ∎

*Verification.* worst `dim(V_i cap V_j)` over all pairs `= 0` on all 13; `K=2` sub-configs all give
`sigma = 0`. **PASS.** [Clean binomial reproof of the note's `K=2` `det-M` result.]

### Lemma 4 (RECURSION + UNCONDITIONAL BOUND). PROVED.

> Order the fibers arbitrarily; set `t_m := dim((V_1 + ... + V_{m-1}) cap V_m)`. Then
> **`sigma = sum_{m=1}^{K} t_m`**, with `t_1 = 0` (empty intersection) and `t_2 = 0` (Lemma 3).
> Ordering the two largest fibers first, `t_m <= dim V_m = mu_m - 1` gives the unconditional bound
> **`sigma <= sum_{all-but-two-largest fibers} (mu - 1)`.**

*Proof.* Iterating `dim(A + B) = dim A + dim B - dim(A cap B)`,
`dim(Vsum) = sum_m dim V_m - sum_m t_m = (P-K) - sum_m t_m`; since `sigma = (P-K) - dim(Vsum)`,
`sigma = sum_m t_m`. `t_1 = 0` trivially and `t_2 = dim(V_1 cap V_2) = 0` by Lemma 3. Each
`t_m <= dim V_m = mu_m - 1`; excluding the two largest (which carry the two vanishing terms)
maximizes the excluded mass, so `sigma <= sum_{m >= 3, largest-first}(mu_{(m)} - 1)`. ∎ (The only
realizability input is `t_2 = 0`; the rest is dimension counting.)

*Verification.* largest-first `t = [0, 0, ...]`, `sum t_m == sigma`, and `sigma <= B_rec :=
sum_{all-but-2-largest}(mu-1)` on all 13. **PASS.**

### Lemma 5 (`K=3` BOUND `sigma <= min_k mu_k - 1`). PROVED.

> For `K = 3`, `sigma = dim((V_i + V_j) cap V_k) <= dim V_k = mu_k - 1` for **each** labeling, so
> **`sigma <= min_k mu_k - 1`** (`<= 1` whenever some fiber has size 2).

*Proof.* `sigma` is symmetric in the fibers (it is `dim` of the syzygy space), so for any choice of
the "third" fiber `k`, `sigma = t_3(k) = dim((V_i+V_j) cap V_k) <= dim V_k = mu_k - 1`; minimize
over `k`. ∎

*Verification.* over **655** `K=3` sub-configs of the 13 objects (each realizable via its parent
`Gamma`) **plus** 1013 seeded random realizable `K=3` configs: **0** violations of
`sigma <= min(mu)-1`; max `sigma = 4` (attained by `[6,6,6]`, see §2.4). **PASS.**

### 1.6 Per-object invariant table (all 13; `dimU = 2` on every full config)

| object | `ell` | `K` | `E_3` | `sigma` | `delta` | `dimU` | `dim Vsum` | `rho` | `P` | `sigma-K` | `E_3-(ell-2)` |
|:-------|:-----:|:---:|:-----:|:-------:|:-------:|:------:|:----------:|:-----:|:---:|:---------:|:-------------:|
| WIT `ell=11 p=331` | 11 | 7 | 9 | 7 | 7 | 2 | 9 | 9 | 23 | `+0` | `+0` |
| WIT `ell=23 p=139` (D3) | 23 | 6 | 21 | 6 | 6 | 2 | 21 | 21 | 33 | `+0` | `+0` |
| CE `ell=11 p=67`  | 11 | 6 | 10 | 7 | 7 | 2 | 9 | 9 | 22 | `+1` | `+1` |
| CE `ell=11 p=199` | 11 | 5 | 10 | 6 | 6 | 2 | 9 | 9 | 20 | `+1` | `+1` |
| CE `ell=13 p=79`  | 13 | 5 | 12 | 6 | 6 | 2 | 11 | 11 | 22 | `+1` | `+1` |
| CE `ell=13 p=313` | 13 | 10 | 12 | 11 | 11 | 2 | 11 | 11 | 32 | `+1` | `+1` |
| CE `ell=17 p=103` | 17 | 6 | 16 | 7 | 7 | 2 | 15 | 15 | 28 | `+1` | `+1` |
| CE `ell=19 p=191` | 19 | 6 | 18 | 7 | 7 | 2 | 17 | 17 | 30 | `+1` | `+1` |
| CE `ell=23 p=139` | 23 | 6 | 23 | 8 | 8 | 2 | 21 | 21 | 35 | **`+2`** | **`+2`** |
| CE `ell=11 p=331` | 11 | 6 | 10 | 7 | 7 | 2 | 9 | 9 | 22 | `+1` | `+1` |
| CE `ell=17 p=409` | 17 | 10 | 16 | 11 | 11 | 2 | 15 | 15 | 36 | `+1` | `+1` |
| CE `ell=23 p=599` | 23 | 18 | 22 | 19 | 19 | 2 | 21 | 21 | 58 | `+1` | `+1` |
| CE `ell=23 p=691` | 23 | 17 | 22 | 18 | 18 | 2 | 21 | 21 | 56 | `+1` | `+1` |

Identity checks (all `PASS`): `sigma==delta`, `dVsum==ell-dimU`, `rho==dVsum`, `E_3==rho+delta-K`,
`E_3==P-2K`, **`sigma==E_3+K-ell+dimU`**, `sigma<=B_rec`. The `sigma-K` and `E_3-(ell-2)` columns
are equal on every row (they must be: their difference is `dimU - 2 = 0` on full configs).

---

## 2. REFRAME — the exact `sigma`-form of the new law `E_3 <= ell`

### 2.1 The master identity

Eliminating `P` and `rho` from the four PROVED facts
`sigma = delta` (L1), `delta = (P-K) - rho` (rank formula), `rho = ell - dimU` (L2), and the
combinatorial `E_3 = P - 2K` (all `mu_k >= 2`), gives

> **`sigma = delta = E_3 + K - ell + dimU`.**   (master identity ★; `sig==E3+K-ell+dU` = PASS on all 13)

Hence `E_3 - ell = sigma - K - dimU`, so for **every** constant `c`

> **`E_3 <= ell + c   <=>   sigma <= K + dimU + c`.**

This is the promised "same identities, shifted" statement (`#330` §4's chain
`delta <= K <=> E_3 <= ell-2 <=> dim(Vsum) >= E_3 <=> sigma <= K` is the `c = -2` slice
specialized to `dimU = 2`). Reading off the three relevant constants:

| law on `E_3` | exact `sigma`-form | on the `dimU=2` chart | status |
|:-------------|:-------------------|:----------------------|:-------|
| `E_3 <= ell-2` (OLD, refuted `#330`) | `sigma <= K + dimU - 2` | `sigma <= K` | **REFUTED** (every CE: `sigma = K+1` or `K+2`) |
| `E_3 <= ell-1` ("one unit weaker") | `sigma <= K + dimU - 1` | `sigma <= K+1` | **REFUTED** at `ell=23 p=139` (`sigma = K+2`) |
| **`E_3 <= ell` (NEW law)** | **`sigma <= K + dimU`** | **`sigma <= K + 2`** | **PROVED on covered chart `T<=4`** (Thm 1, §2A.1); residual `T>=5` = RC, now TIGHT (§2A.2); holds on all 15 |

### 2.2 Precise statement and the "one unit" reconciliation

> **The exact `sigma`-form of `E_3 <= ell` is `sigma <= K + dimU`** (an *equivalence*, by ★),
> equivalently `delta <= K + dimU`, equivalently **`dim(Vsum) >= E_3 - dimU`** (the corrected middle
> link: `sigma <= K+dimU  <=>  (P-K)-dim(Vsum) <= K+dimU  <=>  dim(Vsum) >= P-2K-dimU = E_3-dimU`).
> The bare `dim(Vsum) >= E_3` printed in an earlier draft here was a **copy-over from `#330`'s
> *refuted* `c=-2` chain** (correct there only at `dimU=2`); it holds on merely **2/13** objects,
> whereas `dim(Vsum) >= E_3 - dimU` holds **13/13** (equality iff `E_3 = ell`, i.e. only at the
> tight `CE ell=23 p=139`). [Wave-11 audit; re-verified from scratch — see Addendum §2A.] On the
> extremal chart `dimU = 2` — where **every** observed
> max-`E_3` config sits (all 13 rows of §1.6; a *property of the full max-fiber configs*, since
> `dimU = 2 <=> rho = ell-2 <=>` rank-maximal realizable) — it reads **`sigma <= K + 2`**.

The shift from the refuted `sigma <= K` to `sigma <= K+2` is **one frontier `m`-step**, not "one
unit": the frontier bound is `top-m <= 2m + E_3` and the vacancy band drops from `m <= (ell+1)/2`
(old) to `m <= (ell-1)/2` (new), i.e. by one `m`-step; each `m`-step is worth `2` in `2m + E_3`,
hence `+2` in the `E_3` ceiling (`ell-2 -> ell`) and, by ★ at `dimU=2`, `+2` in `sigma`
(`K -> K+2`). The naive "one unit" reading `sigma <= K+1` (`= E_3 <= ell-1`) is **not** the law and
is explicitly falsified: the `ell=23, p=139` witness has `sigma = K+2` (`E_3 = ell`, §1.6). `K+2`
is the tight ceiling — `sigma = K+2` is *attained*, so it cannot be lowered.

`dimU` is **not** universally `2` (sub-configs reach `dimU = 4, 7`; ★ is verified there too, e.g.
the `[8,8,6]` sub-config of the D3 witness has `dimU = 4`, `sigma = 0 = 16 + 3 - 23 + 4`). This is
why the *equivalence* carries `dimU`; the `sigma <= K+2` form is exactly the restriction to the
rank-maximal chart on which the extremal `E_3` (and thus the frontier) lives.

### 2.3 What the unconditional recursion bound gives toward the law (the gap on the CE spectra)

Lemma 4 gives, with **no** further input, `sigma <= B_rec := sum_{all-but-two-largest}(mu-1)`.
Since `B_rec = E_3 + K - (mu_1 + mu_2) + 2`, we have the clean criterion

> **`B_rec <= K + 2   <=>   E_3 <= mu_1 + mu_2`** (excess concentrated in the two biggest fibers),

and `mu_1 + mu_2 <= ell` by the pairwise cap (Lemma 3). Computed on the spectra:

| object | spectrum (head) | `sigma` | `K+2` | `B_rec` | `E_3` | `mu_1+mu_2` | `B_rec <= K+2`? |
|:-------|:----------------|:-------:|:-----:|:-------:|:-----:|:-----------:|:---------------:|
| WIT `ell=11 p=331` | `[5,5,4,3,2,2]` | 7 | 9 | 8 | 9 | 10 | yes (gap `+1`) |
| **WIT `ell=23 p=139`** | `[8,8,6,4,4,3]` | 6 | 8 | **13** | 21 | 16 | **no** (`E_3 > mu_1+mu_2`) |
| CE `ell=11 p=67`  | `[8,3,3,3,3,2]` | 7 | 8 | 7 | 10 | 11 | yes (gap `+1`) |
| CE `ell=13 p=79`  | `[6,6,6,2,2]` | 6 | 7 | 7 | 12 | 12 | yes (**tight**) |
| CE `ell=13 p=313` | `[8,5,3,3,3,2]` | 11 | 12 | 11 | 12 | 13 | yes (gap `+1`) |
| CE `ell=17 p=103` | `[10,7,3,3,3,2]` | 7 | 8 | 7 | 16 | 17 | yes (gap `+1`) |
| CE `ell=19 p=191` | `[11,8,4,3,2,2]` | 7 | 8 | 7 | 18 | 19 | yes (gap `+1`) |
| **CE `ell=23 p=139`** | `[13,10,4,3,3,2]` | 8 | 8 | 8 | 23 | 23 | yes (**tight**, `= K+2`) |
| CE `ell=11 p=331` | `[8,3,3,3,3,2]` | 7 | 8 | 7 | 10 | 11 | yes (gap `+1`) |
| CE `ell=17 p=409` | `[9,8,3,3,3,2]` | 11 | 12 | 11 | 16 | 17 | yes (gap `+1`) |
| CE `ell=23 p=599` | `[13,10,4,3,2,2]` | 19 | 20 | 19 | 22 | 23 | yes (gap `+1`) |
| CE `ell=23 p=691` | `[13,10,3,3,3,2]` | 18 | 19 | 18 | 22 | 23 | yes (gap `+1`) |

> **The unconditional recursion bound already proves the `E_3 <= ell` `sigma`-form
> (`sigma <= K+2`) on every one of `#330`'s 11 counterexample spectra** — `B_rec <= K+2` on all
> of them, *tight* (`B_rec = K+2`) exactly where `E_3 = mu_1 + mu_2` (`ell=23 p=139`, `ell=13 p=79`).
> It **fails to imply** the law only on the D3 witness `[8,8,6,4,4,3]` (`E_3 = 21 > 16 = mu_1+mu_2`,
> so `B_rec = 13 > 8 = K+2`), the one spectrum whose excess is *not* two-fiber-concentrated; there
> realizability alone closes the residual (`sigma = 6 < 13`). So the still-open content of the law
> is precisely: **rule out `E_3 > mu_1 + mu_2` combined with `sigma > K+2`** — a "two coexisting
> large fibers" phenomenon, exactly the `K >= 3` non-collinear affinely-independent chart `#330`
> and D1 flag as the sole obstruction (`(w,c)`-Veronese transversality).

### 2.4 The two falsifiable predictions P2/P3 — with status

**P2 (`K = 3` realizable `=> sigma <= 1`, i.e. `E_3 <= ell-4` on the `K=3` chart): REFUTED
(COUNTEREXAMPLE).** Explicit realizable `K=3` config at `ell=13, p=79` (three max-fibers of the
`#330` `p=79` Gamma), all size 6:

```
w=1 : {1, 8, 18, 64, 65, 67}
w=23: {4, 9, 23, 31, 32, 72}
w=55: {2, 13, 16, 20, 36, 51}
E_3 = 12,  rho = 11 = ell-2 (realizable, tight),  dimU = 2,  delta = 4,  sigma = 4.
```
`sigma = 4 > 1`, so **P2 is false**. Lemma 5 (`sigma <= min(mu)-1 = 5`) survives — P2 was the
*sharper* claim, and it is the sharper claim that dies. Further P2-refuters among the objects'
`K=3` sub-configs: `[8,3,3]` at `ell=11 p=67` (`sigma=2`), `[5,5,4]` at `ell=11 p=331` (`sigma=2`,
*inside the witness itself*), `[7,4,3]` at `ell=11 p=199` (`sigma=2`). **33** P2-violations across
the 655 sub-configs. Yet **1013 random realizable `K=3` configs give 0 violations** (max `sigma=1`):
random `gamma`-sampling never plants the big fibers that carry the excess — the **identical
undershoot** `#330` §3 identified as the root cause of the KEY LEMMA's spurious "0 violations".
P2 therefore moves from CONJECTURAL_WITH_FALSIFIER to **COUNTEREXAMPLE**, by the same mechanism and
family of objects as `#330`.
> **STATUS: COUNTEREXAMPLE.** FALSIFIER exhibited: `[6,6,6]` at `ell=13, p=79`, `sigma = 4`.

**P3 (the excess lives on the `dimU = 2` chart; `sigma = K+2` is a small-`n` extreme):
CONJECTURAL_WITH_FALSIFIER, holds on all tested.** Every one of the 13 max-fiber configs — the two
`sigma = K` witnesses and all 11 `sigma > K` counterexamples — has **`dimU = 2`** (§1.6). So the
saturation of the `sigma`-form `sigma <= K + dimU` occurs only at `dimU = 2` (rank-maximal
realizable), i.e. `sigma > K => dimU = 2` empirically, which is exactly why `sigma <= K+2` is the
operative frontier bound. In the original 13-object set the maximum `sigma = K+2` (`E_3 = ell`)
occurs only at `ell=23, p=139` (`n = 6`) — the Addendum §2A.2 adds two residual-tight `E_3 = ell`
configs (at `(23,139)` and `(29,233)`), both also `dimU = 2` (P3 further confirmed, not challenged);
the large-`n` `ell=23` configs (`p=599, n=26`; `p=691, n=30`)
saturate at `sigma = K+1` (`E_3 = ell-1`), matching `#330` §5's `~130k`-seed observation that
`max E_3 = ell-1` at large `n`.
> **STATUS: CONJECTURAL_WITH_FALSIFIER.** FALSIFIER: a realizable config with `sigma > K` **and**
> `dimU > 2` (excess off the rank-maximal chart), or a large-`n` config with `sigma = K+2`
> (`E_3 = ell`). Search tool: the `#330` big-fiber constructor `l1_bigfiber_e3_search.py`
> (**unmerged companion branch** `l1-key-lemma-refuted`; see Refs).

**The law's `sigma`-form (`sigma <= K + dimU`, i.e. `E_3 <= ell`): CONJECTURAL_WITH_FALSIFIER.**
Holds on all 13 objects, tight at `ell=23 p=139`. FALSIFIER: any realizable config with
`E_3 >= ell+1`, equivalently `sigma >= K + dimU + 1` (`= K+3` on the `dimU=2` chart) — it would list
at some `m <= (ell-1)/2` and drop `m*` below `(ell+1)/2` (`#330` §5). None found in the objects
above; `#330`'s `~130k` `ell=23` large-`n` seeds cap at `E_3 = ell-1`, with the single `E_3 = ell`
config sitting *on* the inclusive boundary. See §2.5 for an expanded, dedicated hunt run this
session directly against this falsifier.

### 2.5 Session falsifier-hunt evidence (expanded search; no update to the object set)

Two additional hunts ran this session, both **null results** that strengthen (do not weaken) the
claims above. Neither produced a counterexample or a new listing, so the 13-object table of §1.6
is **unchanged**; both are recorded here for completeness and because they specifically targeted
the mechanism (`#330`'s big-fiber / two-fiber-seed constructor) that produced every counterexample
and refuter in this note.

- **Law falsifier hunt (`E_3 >= ell+1`, i.e. `sigma >= K+dimU+1`, the direct falsifier named at the
  end of §2.4).** Ran across `ell in {11,13,17,19,23,29}` (~22 `(ell,p)` targets) plus a dedicated
  deep-dive at the current record witness (`ell=23, p=139`); ~10,600 exact-solved,
  true-spectrum-verified configurations tested. **NO COUNTEREXAMPLE FOUND**: the maximum `E_3`
  observed never exceeded `ell`, tight at `ell=23, p=139` (matching the §1.6 record). This search
  used the same big-fiber family that overturned the old `E_3 <= ell-2` KEY LEMMA and P2 (§2.4), so
  a null result here is meaningful supporting evidence — not a proof — for the
  `CONJECTURAL_WITH_FALSIFIER` status of `E_3 <= ell`.
- **`ell=19, m=10` listing hunt** (a second attempt, using a two-fiber-seed recipe per `#330`'s own
  mechanism, targeting `#330`'s *companion* open question of whether the frontier vacancy half is
  refuted at `ell=19` the way it already is at `ell in {11,17,23}`): ~944K candidate `Gamma` tested
  across all 9 eligible primes (~29 min compute). **NO LISTING FOUND** (no `top-10 >= 2*19 = 38`,
  no `E_3 >= 18`) at any prime — this run actually undershoots the *first* `ell=19` attempt's
  per-coset-greedy ceiling (`E_3 = 17`) at the same primes. This bears on `#330`'s open `ell=19`
  question, **not** on this note's own law directly (no `ell=19` object enters the 13-object
  table); it is recorded here for cross-reference since it reused this note's counterexample-hunt
  infrastructure. **Status: unaffected** — `#330`'s `ell=19` frontier question remains OPEN
  (neither confirmed nor refuted by this session's hunt).

---

## 2A. ADDENDUM (Wave 11) — covered-chart Theorem 1, residual-tight witnesses, NO-GO diagnostics

This addendum (a) upgrades §2.3's `B_rec` criterion to a clean **unconditional theorem on the
covered chart** that proves the law `E_3 <= ell` (`sigma <= K + dimU`) outright when `T <= 4`,
using **only** `L3 + the master identity` (no recursion `L4`); (b) isolates the residual chart
`T >= 5` as a single sharp conjecture **RC** and proves it **TIGHT** by exhibiting *two* realizable
residual configs with `E_3 = ell` (so RC admits **no** margin-based proof); (c) records the NO-GO
diagnostics that kill the linear-algebra / degree / moment routes; (d) issues corrected predictions.
All numbers below were re-derived from the raw `gamma` from scratch (independent spectrum) as part
of the mandated witness-vs-lemma closure.

> **One honest self-correction (process note).** A mid-session read of a profile-incomplete search
> over-claimed that the residual chart carries a **2-unit margin** (`E_3 <= ell-2`, "no tight case"),
> and issued prediction **P-B** ("extremal => covered", i.e. every `E_3 >= ell-1` config has
> `T <= 4`). The mandated numeric closure **refuted**
> this: a targeted realizability hunt *constructed* a realizable **residual** config with
> `E_3 = ell` (§2A.2). **P-B and the margin claim are RETRACTED.** The law `E_3 <= ell` itself
> **survives** (0 falsifiers `E_3 >= ell+1` across ~10,200 new configs + the prior ~150k); what dies
> is only the false claim that the residual is *slack*.

### 2A.1 Theorem 1 (covered chart) — unconditional, needs only `L3` + master

Sort `mu_1 >= mu_2 >= ... >= mu_K` and set the **tail excess** `T := sum_{k>=3}(mu_k - 2) >= 0`.
Since `E_3 = (mu_1-2)+(mu_2-2)+T`, one has `T <= 4  <=>  E_3 <= mu_1+mu_2`; call the config
**covered** if `T <= 4`, **residual** if `T >= 5` (this is exactly §2.3's `B_rec <= K+2` dichotomy,
recast on the invariant `E_3`).

> **Theorem 1 (covered chart).** For every realizable config with `T <= 4`,
> **`E_3 <= mu_1 + mu_2 <= ell`**, hence by the master identity ★ **`sigma <= K + dimU`**
> (`= K + 2` on the `dimU = 2` chart). The law `E_3 <= ell` is therefore **PROVED, unconditionally,
> on the entire covered chart** `T <= 4`.

*Proof.* `E_3 = (mu_1-2) + (mu_2-2) + T <= (mu_1-2) + (mu_2-2) + 4 = mu_1 + mu_2` by `T <= 4`. The
pairwise cap `mu_1 + mu_2 <= ell` is Lemma L3 (PROVED: the pencil member
`alpha X^ell + beta Gamma + gamma` through `(W_1,lambda_1),(W_2,lambda_2)` vanishes on `F_1 cup F_2`,
has degree `<= ell`, so `mu_1+mu_2 <= ell`; this is the only realizability input). Hence
`E_3 <= ell`. The master identity `sigma = E_3 + K - ell + dimU` (★, PROVED §2.1) then gives
`sigma = E_3 + K - ell + dimU <= ell + K - ell + dimU = K + dimU`. ∎

**Remark (what it does *not* use).** Theorem 1 needs **only** `L3` (pairwise cap) and the master
identity — **not** the recursion `L4`, and **not** any `dimU = 2` restriction: it delivers the
invariant `E_3 <= ell` for arbitrary `dimU`. This is strictly more elementary than the §2.3 route
`sigma <= B_rec <= K+2`. On the canonical 13-object set, **12/13 are covered** (`T <= 4`); the sole
residual object is the D3 witness `[8,8,6,4,4,3]` (`T = 9`). All 12 covered objects satisfy
`E_3 <= mu_1+mu_2 <= ell` (re-verified 13/13; new gate (ix)).

### 2A.2 Residual Conjecture RC — the whole remaining problem, and it is TIGHT

> **Residual Conjecture (RC).** Every realizable config with `T >= 5` satisfies `E_3 <= ell`
> (equivalently `sigma <= K + dimU`). **RC + Theorem 1 = the full law.**

Unlike the covered chart, RC is **not** reducible to the pairwise cap and — the key correction of
this wave — is **saturated**: two realizable residual configs attain `E_3 = ell`. Both were
re-derived from scratch (independent spectrum recomputation matches the `Config` spectrum; master
identity and realizability `rho = ell-2` re-checked):

> **Residual-tight witness 1** (`ell = 23`, `p = 139`).
> `gamma = [95,37,137,97,52,126,56,52,73,43,44,84,22,120,67,123,98,128,33,62,37,1]`.
> Spectrum **`[11,10,5,4,3,2]`** (`K = 6`); `E_3 = 23 = ell`; `mu_1+mu_2 = 21 < 23` so **`T = 6`
> (residual)**; `rho = 21 = ell-2` (**realizable**); `dimU = 2`; `sigma = delta = 8 = K + dimU`
> (**tight**); master ✓ (`8 = 23 + 6 - 23 + 2`).
>
> **Residual-tight witness 2** (`ell = 29`, `p = 233`).
> `gamma = [203,187,107,98,59,120,193,102,190,101,206,153,193,196,119,185,120,153,188,140,192,218,113,205,228,206,224,1]`.
> Spectrum **`[14,13,5,5,2,2,2,2]`** (`K = 8`); `E_3 = 29 = ell`; `mu_1+mu_2 = 27 < 29` so **`T = 6`
> (residual)**; `rho = 27 = ell-2` (**realizable**); `dimU = 2`; `sigma = delta = 10 = K + dimU`
> (**tight**); master ✓ (`10 = 29 + 8 - 29 + 2`). *(A companion residual `E_3 = ell-1` config
> `[11,10,5,3,3,2]` at `(23,139)`, `sigma = 7`, was also found.)*

**Neither witness is in the original 13-object canonical set** — which contained **no**
residual-tight object, and that blind spot is exactly what produced the retracted margin claim. Both
are now **added to the canonical set** (verifier objects, `kind = "RES"`) and gated (§5, gate (ix)).

> **Consequence (no margin).** `E_3 = ell` is *attained* in the residual, at two distinct primes.
> Therefore **any proof of RC must be SHARP** — a slack/margin argument is provably insufficient.
> The covered/residual split's value is precisely that it **isolates** this sharp core (`T >= 5`) and
> proves everything else unconditionally (Theorem 1), *without softening the core*. RC on the
> `dimU = 2` residual chart is `sigma <= K + 2` with `T >= 5`: the localized `(W,lambda)`-Veronese /
> split-pencil transversality in `R_K = F_p[X]/h_K` that D1 / `#330` name, with `>= 3` big fibers.

### 2A.3 NO-GO diagnostics — why the standard routes are provably dead (verified 13/13)

**(N1) Linear algebra on `(D, Z, U)` is circular.** Sublemma S3 (`lambda in D => sum_i lambda_i
Gamma(x_i)^j = 0` for all `j`; verified 13/13) gives `D + Z = eval(U)^perp` **as an equality**,
whence `sigma = dim(D cap Z) = dim D + dim Z - dim(D+Z) = (P-K) + (P-ell) - (P-dimU) =
E_3 + K - ell + dimU` — the master identity, an **identity, not an inequality**. Any bound obtained
purely by dimension-counting on these spaces therefore re-expresses `E_3 <= ell` as *itself*. The
best pure-LA upper bounds are `sigma <= dim Z = P - ell` (`<=> dimU <= K`) and, using `x^ell` constant
on fibers, `sigma <= P - (ell+1)` (`<=> dimU <= K-1`) — both far above `K + dimU`. *The content must
come from **which point sets can be fibers** (realizability), not from `(D,Z,U)` dimensions.*

**(N2) Single-polynomial / degree methods are `Theta(ell^2)` or vacuous on the extremal chart.**
- *Uncertainty.* Per coset `mu_c <= wt(Gamma) =: w` (13/13), but on the extremal chart **`w = ell-1`**
  (12/13; D3 has `w = ell-2`) — so it yields only `mu_c <= ell-1`, useless for `sum_c(mu_c-2)`. High
  `E_3` *forces* high `w`, precisely into the vacuous regime.
- *`Psi = X^ell - Gamma` level sets (S2).* The `eta_c := W_c - lambda_c` are **all distinct**
  (`J = K`, 12/13), so the grouped cap degenerates to the trivial per-coset `mu_c <= ell`.
- *Resultant / plane-curve genus / moments (S4, S5).* All count `Gamma`-collisions, whose total
  `sum_c binom(mu_c,2) <= binom(ell-1,2)` is `Theta(ell^2)` while `E_3 = O(ell)`; the ratio
  `E_3 / sum_c binom(mu_c,2)` runs **0.15–0.28** on the objects (S5 collision identity exact,
  13/13). This is *why* "resultant / moments / uncertainty are DEAD" — not merely weak but off by a
  factor `Theta(ell)`.

**(N3) The real obstruction: realizability caps balanced large-fiber mass.** Pairwise-legal
*balanced* profiles have huge naive `E_3` yet the plant-then-solve constructor cannot realize them:
in a `K = 3` sweep at `ell = 23`, no balanced `[x,x,x]` with `x >= 9` (e.g. `[11,11,11]`,
`[10,10,10]`, `[9,9,9]`) is realized as the top-3 spectrum — the achieved shapes collapse to
two-big-plus-tail (max realized top-3 `[11,10,6]`). This "one degree-`<=ell-1` `Gamma` cannot carry
`>= 3` half-size level sets" phenomenon is exactly what caps `E_3` at `ell`, and it is invisible to
every degree/dimension count in (N1)–(N2). *(Evidence, not a non-realizability proof: whether a
special-position balanced config exists is itself an instance of the open transversality question —
which is why RC is genuinely open, not merely unproven.)*

### 2A.4 Corrected falsifiable predictions (P-A / ~~P-B~~ / P-C / P-D)

- **P-A (law).** No realizable config has `E_3 >= ell+1` (`sigma >= K + dimU + 1`). **0 across
  ~10,200 new configs** (residual sweeps + targeted hunts) and 0 in the prior ~150k-seed sweeps. The
  law is now known **TIGHT in the residual** — `E_3 = ell` attained at *two* primes (§2A.2) — so a
  falsifier, if any, is a residual `[~ell/2, ~ell/2, medium-tail]` config; that is the sharpest place
  to keep searching. Falsifier: any `E_3 = ell+1` (would drop `m*` below `(ell+1)/2`).
- **~~P-B (extremal `=> covered`)~~ — RETRACTED / REFUTED this wave.** `[11,10,5,4,3,2]` at
  `(23,139)` is realizable, residual (`T = 6`), and tight (`E_3 = ell`). The extremal locus is **not**
  contained in the covered chart. *(This is the over-claim caught by the mandated numeric closure.)*
- **P-C (residual reaches the ceiling).** The residual chart attains `E_3 = ell` (`sigma = K+dimU`),
  witnessed by both §2A.2 configs; it does **not** stop at `ell-2`. A covered tight witness
  (`[13,10,4,3,3,2]`, `T = 4`) and a residual tight witness (`[11,10,5,4,3,2]`, `T = 6`) coexist at
  the *same* `(23,139)`. Falsifier: a residual `E_3 = ell+1` (= P-A).
- **P-D (small-`K` slack).** For fixed small `K` the law is far from tight: at `ell = 23` the max
  realized `K = 3` spectrum is `~[8,8,7]` (`E_3 ~ ell-6`); tight cases (`E_3 = ell`) need `K >= 5`
  (witnesses have `K = 6, 8`). So any `K`-bounded proof carries `Omega(K)` slack — the difficulty is
  intrinsically large-`K` + spread.

---

## 3. Relevance to `agents.md` steering and concurrent tracks

**Relevance.** This note is the **structural toolkit** for the post-`#330` residual
`prob:v13-l1-residuals` (`experimental/cap25_v13_experimental.tex`). It (a) supplies the *written
proofs* of the reduction identities `#330` uses but states numerically, so the reduction chain is
now PROVED end-to-end **except** its endpoint; (b) states the new law in its exact `sigma`-form
`sigma <= K + dimU`, pinning the still-open core to the single inequality `dim((V_1+V_2) cap V_3)`
transversality on the `K >= 3` non-collinear chart; and (c) *raises the residual floor a second
time* by refuting P2, so any `L1` cell budgeting `K=3` primitive listings must now count
`sigma` up to `min(mu)-1` (Lemma 5), not the withdrawn `sigma <= 1`. In the residual-branch enum
(`agents.md`: `PAID_BY_THEOREM` / `PAID_BY_EXACT_CERTIFICATE` / `CONDITIONAL_ON_NAMED_INPUT` /
`CONJECTURAL_WITH_FALSIFIER` / `COUNTEREXAMPLE_NEW_FLOOR`), the P2 refutation is a
**`COUNTEREXAMPLE_NEW_FLOOR`** event (a claimed-vacant sharper bound shown occupied by an explicit
certificate), stacking on `#330`'s vacancy-cell floor; the law's `sigma`-form is the branch's
`CONJECTURAL_WITH_FALSIFIER` payload with a printed falsifier (`E_3 >= ell+1`), now backed by the
§2.5 expanded hunt. The objects land in the `L_prim` stratum of `pma_wide_residual` and feed
`petal_mixed_amplification` on the low side (`experimental/data/prize-dag/prize_dag.json`).

**Concurrent tracks (relationship labels; no dependency taken).**
- **`#330`** (`experimental/notes/l1/l1_prime_ell_key_lemma_refuted.md`, verifier
  `experimental/scripts/verify_l1_key_lemma_refuted.py`, constructor
  `experimental/scripts/l1_bigfiber_e3_search.py`): **companion / consumes.** **Unmerged:** all
  three of these files live on the companion branch `l1-key-lemma-refuted` (not yet merged to
  `main`) and are absent from this branch's tree; this note's own verifier (§5) is self-contained
  and does not import, edit, or depend on any of them. This note *consumes*
  `#330`'s counterexample Gammas as its verification substrate (the lemmas must hold *on* them) and
  *supplies back* the exact `sigma`-form `sigma <= K + dimU` of `#330` §5's candidate law
  `E_3 <= ell`, plus the P2 refutation via `#330`'s own big-fiber mechanism. Fully consistent: every
  `#330` §4 "SURVIVES" identity is re-derived here with proof and re-verified `PASS`. `#330`'s own
  companion open question (`ell=19` frontier-vacancy listing) remains OPEN after this session's
  null-result hunt (§2.5); this note takes no position on it.
- **`#283` lineage** (AllenGrahamHart:
  `experimental/notes/l1/l1_petal_residue_kernel_reduction.md` and its four siblings
  `l1_petal_realizable_kernel_injection.md`, `l1_petal_residue_kernel_linear_bound.md`,
  `l1_petal_squarefree_classification_counting_soundness.md`,
  `l1_petal_squarefree_classification_ledger_soundness.md`): **unaffected-and-awaits.** Its lemmas
  are conditional-on-ledger; this note changes only the ledger side it awaits — any
  `petal_squarefree_classification_ledger_payload` must now (i) count `m = (ell+1)/2` primitive
  listings (`#330`) and (ii) budget `K=3` `sigma` up to `min(mu)-1` rather than `<= 1` (P2 refuted
  here). No lemma of `#283` is invalidated.
- **`l1_coset_chart_residue_bridge_v1.md`** (integrated): **consistent** — the `sigma > K`
  objects are new extremal inhabitants of its residue-line branch; the master identity ★ is the
  residue-line coordinate expression of `#330`/D1's `(w,c)`-Veronese barrier.

**Refs:** `experimental/notes/l1/l1_prime_ell_key_lemma_refuted.md` (`#330`, companion —
**unmerged**: branch `l1-key-lemma-refuted`, not present on this branch) |
`experimental/notes/l1/l1_prime_ell_frontier_corrected.md` (§2.2 rank formula, §3 chain; toolkit) |
`experimental/scripts/verify_l1_key_lemma_refuted.py` (**unmerged**, same companion branch),
`experimental/scripts/verify_l1_prime_ell_frontier_corrected.py`,
`experimental/scripts/l1_bigfiber_e3_search.py` (**unmerged**, same companion branch) |
`experimental/notes/l1/l1_coset_chart_residue_bridge_v1.md` |
`experimental/notes/l1/l1_petal_residue_kernel_reduction.md` (+ 4 siblings, `#283`) |
`experimental/cap25_v13_experimental.tex` `prob:v13-l1-residuals` |
`experimental/data/prize-dag/prize_dag.json` nodes `pma_wide_residual`, `petal_mixed_amplification`.

---

## 4. Status block

**PROVED (five lemmas + the master identity).**
- L1 Moment bridge `=> sigma = delta` (§1).
- L2 Locator duality `dim(Vsum) = rho = ell - dimU` (`sigma + rho = P-K`) (§1).
- L3 Pairwise `V_i cap V_j = 0` and the `K=2` corollary `sigma = 0` (§1).
- L4 Recursion `sigma = sum_m t_m`, `t_1 = t_2 = 0`, unconditional bound
  `sigma <= sum_{all-but-2-largest}(mu-1)` (§1).
- L5 `K=3` bound `sigma <= min_k mu_k - 1` (§1).
- Master identity `sigma = delta = E_3 + K - ell + dimU` and its consequence
  `E_3 <= ell + c <=> sigma <= K + dimU + c` (§2.1).
- **Theorem 1 (covered chart, Addendum §2A.1):** for `T := sum_{k>=3}(mu_k-2) <= 4`,
  `E_3 <= mu_1+mu_2 <= ell`, hence `sigma <= K + dimU` — i.e. **the law `E_3 <= ell` holds
  unconditionally on the entire covered chart**, using only L3 + the master identity (no recursion).
  12/13 canonical objects are covered.
All verified `PASS` on the 2 witnesses, all 11 `#330` counterexamples, **and the 2 residual-tight
witnesses** (§2A.2) — **15 objects** (§1.6, §2A; verifier gates i–ix), with `dimU` ranging over
`{2,4,7}` across configs and sub-configs.

**PARTIALLY PROVED + CONJECTURAL_WITH_FALSIFIER (the law, split by Addendum §2A).**
- The new law's `sigma`-form `E_3 <= ell <=> sigma <= K + dimU` (`= sigma <= K+2` on the observed
  `dimU=2` chart) is now **split**: **PROVED unconditionally on the covered chart `T <= 4`**
  (Theorem 1, §2A.1); the residual chart `T >= 5` is the **Residual Conjecture RC**, the sole open
  piece. RC is now known **TIGHT** — `E_3 = ell` is *attained* by two realizable residual witnesses
  (`[11,10,5,4,3,2]` @ `(23,139)`, `[14,13,5,5,2,2,2,2]` @ `(29,233)`; §2A.2), so any RC proof must
  be sharp (no margin). FALSIFIER of the full law: realizable `E_3 >= ell+1` (`sigma >= K+3` at
  `dimU=2`); **0 found across ~10,200 new configs + prior ~150k** (§2.5, §2A.4 P-A) — evidence, not
  proof. Holds on all 15 canonical objects.
- P3 (`sigma > K => dimU = 2`; `sigma = K+2` only at small `n`). FALSIFIER: `sigma > K` with
  `dimU > 2`, or large-`n` `sigma = K+2`.

**COUNTEREXAMPLE (new negative result).**
- P2 (`K=3 => sigma <= 1`) is FALSE. Explicit realizable `[6,6,6]` at `ell=13, p=79` has
  `sigma = 4`; refuted by the same big-fiber undershoot `#330` diagnosed (random `K=3` sampling:
  0/1013 violations). Lemma 5 (`sigma <= min(mu)-1`) is the surviving THEOREM.

**SURVIVES (from `#330` §4, re-derived with proof here).** The reduction-chain identities (they
hold *on* the counterexamples), the pairwise cap, the `det-M`/`K=2` no-go, the collinear/`P<=ell`
branch, Theorem R (`ell=7`), the upper-half witnesses, and the `ceil(2ell/3)` refutation.

**UNAFFECTED (this session, §2.5).** `#330`'s companion open question — whether the frontier
vacancy half lists at `ell=19, m=10` — remains OPEN; a second-attempt hunt found no listing (nor
does this note depend on one).

*(Deviation flagged for the packaging panel: the task brief anticipated P2/P3 as
CONJECTURAL_WITH_FALSIFIER; this note's own verification found and files P2's explicit falsifier, so
P2 is reported as COUNTEREXAMPLE — a stronger, evidence-backed result, consistent with the `#330`
self-correction lineage. P3 and the law's `sigma`-form remain CONJECTURAL_WITH_FALSIFIER as
anticipated.)*

---

## 5. Reproducibility — verifier gate list

Ships as a zero-arg, stdlib-only, deterministic `experimental/scripts/verify_l1_sigma_calculus.py`
(exit 0 iff all gates pass; `--tamper-selftest` flips one datum per gate class and confirms each
then fails). It reconstructs each object from its `gamma` (group `F_p^*` by `x^ell`, take the
max-fiber per coset with `mu >= 2`; independent of any inherited reconstruction). **Object set (15):**
the 2 witnesses + 11 `#330` counterexample Gammas + **2 residual-tight witnesses** (`[11,10,5,4,3,2]`
at `ell=23,p=139` and `[14,13,5,5,2,2,2,2]` at `ell=29,p=233`; Addendum §2A.2 — added this wave to
close the no-residual-tight-object blind spot) listed in the header (the `ell=23` `p in {599,691}`
`sigma`/`delta` solves are the heaviest; they finish in seconds — no offline gate needed). Gates:

- **Gate i — moment bridge / `sigma = delta` (L1).** For each object: 25 random `(a_k)`,
  `deg a_k <= mu_k-2`; assert `sum_k a_k h_k == sum_s M_s X^{ell-1-s}` with
  `M_s = sum_i lambda_i x_i^s`, `lambda_i = a_k(x_i)/g_k'(x_i)`; and assert
  `nullity(syzygy map) == dim(D cap Z)`. PASS iff equal on all.
- **Gate ii — locator duality (L2).** For each object assert `dim(Vsum) == rho`,
  `rho == ell - dimU`, and `sigma + rho == P - K`.
- **Gate iii — pairwise + `K=2` (L3).** For each object assert `dim(V_i cap V_j) == 0` for all
  pairs, and `sigma == 0` on every `K=2` sub-config.
- **Gate iv — recursion + unconditional bound (L4).** For each object, largest-first order:
  assert `t_1 == t_2 == 0`, `sum_m t_m == sigma`, and `sigma <= B_rec = sum_{all-but-2-largest}(mu-1)`.
- **Gate v — `K=3` bound (L5).** Over all `K=3` sub-configs of the objects **and** a seeded random
  realizable `K=3` sweep (>= 800 configs across `ell in {7,11,13,17,23}`): assert
  `sigma <= min(mu)-1`, 0 violations.
- **Gate vi — master identity + `sigma`-form (§2.1).** For each object assert
  `sigma == E_3 + K - ell + dimU`; assert the equivalences `(E_3 <= ell) == (sigma <= K+dimU)`,
  `(E_3 <= ell-2) == (sigma <= K+dimU-2)`; and (on a few sub-configs with `dimU > 2`, e.g. `[8,8,6]`
  of the D3 witness) re-assert ★ with `dimU != 2`.
- **Gate vii — P2 falsifier (teeth).** Assert the explicit `[6,6,6]` at `ell=13, p=79` is
  realizable (`rho == ell-2`) with `sigma == 4 > 1` (P2 refuted); and assert the seeded random
  `K=3` sweep of Gate v yields **0** configs with `sigma >= 2` (documents, does not hide, the
  small-fiber undershoot).
- **Gate viii — OLD/NEW stratification.** Assert on the 2 witnesses `E_3 <= ell-2` and `sigma <= K`;
  on all 11 counterexamples `E_3 > ell-2` and `sigma > K` (OLD refuted) but `E_3 <= ell` and
  `sigma <= K+2` (NEW holds); on the 2 residual-tight witnesses `E_3 == ell`, `sigma == K+2`, `T >= 5`
  (residual & tight); and `dimU == 2` on all 15.
- **Gate ix — Theorem 1 covered chart + residual-tight witnesses (Addendum §2A).** For every object,
  compute `T = sum_{k>=3}(mu_k-2)`; on the covered chart (`T <= 4`, 12 objects) assert
  `E_3 <= mu_1+mu_2 <= ell` (Theorem 1) and its master-image `sigma <= K+dimU`; on the residual chart
  (`T >= 5`, 3 objects) assert `E_3 <= ell`, and on the 2 residual-tight witnesses additionally assert
  `E_3 == ell`, `sigma == K+dimU`, `rho == ell-2` (realizable). Structural check: `covered == 12`,
  `residual == 3`, `residual_tight == 2` (the two new witnesses are present and tight).

`--tamper-selftest`: perturb one `gamma` coefficient (breaks i/ii/vi via changed spectrum), zero a
`t_m` (breaks iv), inflate a claimed `sigma` (breaks i/vii), flip the `[6,6,6]` `sigma` to `1`
(breaks vii), plus falsely tighten the Theorem-1 covered bound by 1 (breaks ix, caught by a
tight-covered object with `E_3 == mu_1+mu_2`) — assert each targeted gate then FAILS. The verifier is self-contained: it does not
import from, edit, or depend on any other script's claims being true; every number in §1.6-§2A is
reproduced here from the raw `gamma` coefficients (the two residual-tight witnesses of §2A.2 among
them), independent of the session prototypes that first produced them.
