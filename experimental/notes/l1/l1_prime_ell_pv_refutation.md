# L1 Prime-`ell` Primitive Vacancy is FALSE at the Onset `m = t+1`

Status legend on every claim: **PROVED** (rigorous) / **LEMMA** (proved step) /
**NUMERIC** (verified by exact solve, not sampled) / **OPEN** (obstruction named).

## 0. Headline — REFUTATION (NUMERIC-exact, explicit witnesses)

The **primitive `m < ell` mixed-vacancy** conjecture — named `PV(t,d,m)` in the
companion open PR #224 (`l1_stabilizer_descent.md`, L160-164) and stated in prose
in the companion open PR #222 (`l1_coset_mixed_vacancy_threshold.md`, L91-94) — is
**FALSE at prime `d = ell`, already at its onset `m = t+1`**. Explicit
**stabilizer-primitive mixed minimal kernel sets** exist at
`(t, ell, m) = (5, 7, 6)` and `(4, 7, 5)` (both `t < m < ell`), each exhibited by
construction and checked point-by-point at multiple primes: `deg P <= m*ell`
(kernel), agreements `>= s` (listed), each core coset's retained count equal to the
top fiber of the fixed `Gamma` (extremal), and proper coset traces (primitive) — all
by exact `F_p` polynomial arithmetic that does **not** use the reduction it feeds.
Divisibility-minimality of the **exact** missed core is then structural; the verifier
still exercises the deletion criterion and shows it discriminates (it flags a planted
non-minimal set). Verifier `verify_l1_prime_ell_pv_refutation.py` (offline, stdlib,
deterministic) replays both witnesses and the support lemmas; exit 0 iff all gates pass.

`PV(t,d,m)` as posed (quoted verbatim, PR #224 L160-164):

> **Named open target.** Primitive vacancy `PV(t,d,m)`: `m < d => #PrimMinMix(t,d,m)
> = 0` (proved for `<= 1` active DFT-sector in companion Theorem B; open for `>= 2`).

The prose precursor it generalizes (quoted verbatim, PR #222 L91-94):

> **Corrected open target (named).** PRIMITIVE `m < ell` mixed-vacancy: `m < ell`
> => no stabilizer-primitive mixed minimal kernel set.

Our witnesses have **all `ell-1` DFT sectors active** (`Gamma` full support), so they
sit squarely in the `>= 2`-active-sector regime that `PV` left open and conjectured
vacant; they do **not** contradict PR #222's Theorem B (`<= 1` active sector `=>`
non-primitive), which is untouched.

## 1. Setting and the listing convention

Background-free coset sunflower over `F_p`, `H = mu_ell` (order `ell | p-1`, `ell`
an odd **prime**). Petals `T_i = a_i H` (`i=1..t`, `alpha_i = a_i^ell`), core
`C = union_{j=1..m} b_j H` (`beta_j = b_j^ell`; all `t+m` labels distinct nonzero),
`phi(Y) = prod_i (Y-alpha_i)`, `L_C = prod_j(X^ell - beta_j)`. Distinct nonzero
scalars `c_i`; received word `U = c_i L_C` on `T_i`, `0` on `C`. `k = m*ell+1`,
`s = (m+1)*ell`.

**Reduction (companion open PR #219; the reduction itself PROVED-LOCAL there).** By
**items 2 ("Agreement formula") + 4 ("Bijection")**
of the Claim list in the companion open PR #219
(`l1_general_reconstruction_collapse.md`, branch `l1-general-reconstruction-collapse`
— there is no "Lemma D"), a **LISTED** full-petal codeword (agreements `>= s`)
corresponds to a **divisibility-minimal kernel set** `E` = its exact missed core; `E`
is **MIXED** when it is not a union of full `H`-cosets. At **prime** `ell`, `mu_ell`
has no nontrivial proper subgroup, so a mixed minimal kernel set is automatically
**stabilizer-primitive**.

**Listing convention (PR #223 sec 1).** Listed `<=>` agreements `>= s = (m+1)ell`
`<=>` retained core `R := sum_j rho_j >= (m-t+1)ell`, where
`rho_j = #{x in b_j H : P(x)=0}`. At `m = t+1` the threshold is `R >= 2ell`.

**`m = t+1` structure (PR #223).** A full-petal codeword is
`P(X) = w(X^ell) + phi(X^ell) g(X)`, `w` fixed by the scalars (`w(alpha_i)=c_i`,
`deg w <= t-1`), and at `m=t+1` every DFT sector `g_r` (`r>=1`) collapses to a
CONSTANT `gamma_r`, so `Gamma(X) = sum_{r=1}^{ell-1} gamma_r X^r` is one FIXED
sector polynomial (mixed `<=> Gamma != 0`) and `g_0 = u + vY`. On core coset `j` a
point `x = b_j h` is retained `<=> Gamma(x) = lambda_j := -P_0(beta_j)/phi(beta_j)`
(`P_0 = w + phi g_0`, `phi(beta_j) != 0`): the retained set on coset `j` is a single
LEVEL SET of the fixed `Gamma`, so `max R = ` sum of the top-`m` values of the
`mu`-spectrum `{ mu(b) := max_lambda #{x in bH : Gamma(x)=lambda} }`.

## 2. Lemma LF (`lambda`-freeness at `m = t+1`) — PROVED

> **Lemma LF.** For any `t` distinct nonzero petal labels `alpha_1..alpha_t` and
> `m = t+1` distinct core labels `beta_1..beta_{t+1}` (all `t+m` distinct), the
> linear map `(c_1..c_t, u, v) -> (lambda_1,..,lambda_{t+1})`,
> `lambda_j = -w(beta_j)/phi(beta_j) - (u + v beta_j)` with `w` the degree-`<=t-1`
> interpolant `w(alpha_i)=c_i`, is **surjective** (rank `t+1`). Hence any target
> level vector `(lambda_j)` — in particular the modal fibers of a fixed `Gamma` — is
> realized by scalars and a `g_0`; a **distinct-nonzero** preimage `c` (avoiding the
> `O(t^2)` hyperplanes `c_i=0`, `c_i=c_j`) then exists generically for large `p` and
> is exhibited for each witness (verified).

*Proof (general `m=t+1`).* The map is linear with zero constant term (`t+2` inputs,
`m=t+1` outputs); surjective `<=>` no nonzero left-null `kappa` with
`sum_j kappa_j lambda_j == 0` identically. Reading off input blocks:
the `u`-block gives **(A)** `sum_j kappa_j = 0`; the `v`-block gives **(B)**
`sum_j kappa_j beta_j = 0`; the `c_i`-block gives, using
`prod_{i'!=i}(beta_j - alpha_{i'}) = phi(beta_j)/(beta_j - alpha_i)`, the clean form
**(C')** `sum_j kappa_j/(beta_j - alpha_i) = 0` for each `i=1..t`.

Form `N(Z) := sum_j kappa_j prod_{j'!=j}(Z - beta_{j'})`, degree `<= m-1 = t`. Then
`N(Z) = [prod_j (Z-beta_j)] * sum_j kappa_j/(Z-beta_j)`, so (C') is exactly
`N(alpha_i) = 0` for the `t` distinct `alpha_i` (each `prod_j(alpha_i-beta_j) != 0`).
Its top coefficients are `[Z^{m-1}] N = sum_j kappa_j` and, once (A) holds,
`[Z^{m-2}] N = sum_j kappa_j beta_j`; so (A) and (B) kill the two leading
coefficients, dropping `deg N <= m-3 = t-2`. A degree-`<= t-2` polynomial with `t`
distinct roots is `0`, so `N == 0`; the `m` polynomials `prod_{j'!=j}(Z-beta_{j'})`
are linearly independent, whence `kappa = 0`. QED

**Instantiation (verifier gate LF).** The map has rank `m` for both witnesses and
for every seeded distinct-coset draw at `ell in {7,11,13}`; the bridge identity, the
two coefficient formulas, the partial-fraction identity, and the reduced-system rank
`= m` (`=> kappa = 0`) are all checked, at `ell=7` and `ell=11`. The full witness
chain (Sec. 3) is executed at **`ell=7` only**; the `ell=11,13` rows are
**spectrum `>= 2ell` replayed from an embedded `Gamma` by gate FR** (Sec. 4), with
`lambda`-freeness confirmed as rank `= m` at those `ell` but the explicit codeword
(scalar side) not assembled.

## 3. The witnesses

### 3a. Primary: `(t, ell, m) = (5, 7, 6)` — NUMERIC-exact refutation

Full chain, verified independently of the #219/#223 reduction at `p in {211,421}`
(and, across the V1 sweep, at all 9 primes
`{113,197,211,337,379,421,449,463,631}` — at `p=449` the reduced `R=15` is still
listed, `50 >= 49`):

| link | object | status | value at `p=211` (`p=421`) |
|---|---|---|---|
| spectrum | `top6` of the `mu`-spectrum of a fixed `Gamma` | NUMERIC | `16 >= 2ell=14` (`16`) |
| `lambda`-free | `(c,u,v) -> (lambda_j)` surjective | PROVED (Lemma LF) | rank `6`; solved with `c` distinct nonzero |
| codeword | `P = w(X^7)+phi(X^7)(g0(X^7)+Gamma)` | PROVED (identity) | `deg P = 41 <= 42`; `Gamma != 0` (mixed) |
| petals | `P = c_i` on all `35` petal points | PROVED | `35/35` |
| listed | agreements `= 35 + R >= s = 49` | NUMERIC | `51 >= 49` (margin `2`) |
| kernel | `M` = missed core, `P = W_M * L_{C\M}`, `deg W_M <= |M|` | PROVED (division) | `|M| = 26`, `deg W_M = 25` |
| extremal | each core coset's `rho_j` = top fiber `mu(b_j)` of `Gamma` | NUMERIC (from `Gamma`) | `[3,3,3,3,2,2]` |
| minimal | `M` divisibility-minimal (criterion discriminates on a planted set) | PROVED (structural) | minimal |
| primitive | `M` meets each core coset in a proper nonempty subset | PROVED | traces `[4,4,4,4,5,5]` (`[3,4,4,5,5,5]`) |

`Gamma` at `p=211`: `[161,178,120,90,1,10]` (coeffs of `X^1..X^6`); scalars
`c=[116,25,171,73,27]`, `u=187`, `v=0`; retained profile `[3,3,3,3,2,2]`. The kernel
is certified by exact long division `P / L_{C\M}` (remainder `0`, quotient degree
`25`), independent of the CRT interpolation that produced `P`, and each `rho_j` equals
the top fiber of `Gamma` on coset `j`, read straight off `Gamma` (independent of
`c,u,v`). Divisibility-minimality of the **exact** missed core is then automatic; the
verifier still runs the deletion criterion `P / L_{(C\M)+x}` and confirms it
discriminates by flagging the deliberately non-minimal set `M + {r}` (`r` a retained
point) — so the minimality gate is not vacuous.

### 3b. Razor: `(t, ell, m) = (4, 7, 5)` — NUMERIC-exact, zero-margin

Here `m = t+1 = 5 < ell = 7`, threshold `R >= (m-t+1)ell = 2ell = 14`. The witnesses
hit `R = 2ell = 14` **exactly** (agreements `42 = s = 42`, **zero margin** — one
retained point short would unlist), `|M| = 21 = (t-1)ell`, `deg W_M = 20`, `M`
minimal and primitive (traces `[4,4,4,4,5]` at `p=211`, `[3,4,4,5,5]` at `p=421`).
The full chain passes at **9 of 10** primes in the V1 sweep
`{113,197,211,281,337,379,421,449,463,631}`; the tenth, `p=449`, is
**search-limited** at `top5 = 13` (vacancy there is **not** claimed). The independent
solve-based frontier lab (S1) reaches `R = 2ell` at **all 8** of its tested primes
`{211,337,421,631,883,1009,1471,2017}` (a disjoint set, not including `p=449`), once
the coset-position search depth is matched to `n=(p-1)/ell`. So the mixed/primitive
onset at `ell=7` is `m = t+1` for **both** `t=4` and `t=5`.

## 4. Corrected frontier: onset `m0 = ceil(2ell/3)` — NUMERIC

At `m = t+1` the threshold `R >= 2ell` holds for every `t`, so the frontier is the
smallest `m` with `max_Gamma top-m(spectrum) >= 2ell`. A profile of `k` three-fibers
and `(m-k)` two-fibers over `m` cosets retains `2m + k`; setting `= 2ell` gives the
**exact fiber accounting**

> `k = 2(ell-m)` three-fibers `+ (3m-2ell)` two-fibers, feasible in `m` cosets
> `<=> k <= m <=> m >= 2ell/3`.

> **Frontier conjecture (NUMERIC).** For prime `ell`, `m=t+1`: listing occurs iff
> `m >= m0 := ceil(2ell/3)`, i.e. `t0(ell) = ceil(2ell/3) - 1`.

(At `ell=7`, `m0=5`: the profile is exactly `[3,3,3,3,2]` — the `t=4` witness of
Sec. 3b.) Evidence, achieved onset `m*` (smallest `m` with a listing `Gamma`; gate FR
replays the `ell=11,13` rows from embedded `Gamma`):

| `ell` | `ceil(2ell/3)` (pred) | achieved onset `m*` | `m* =` |
|---|---|---|---|
| 7 | 5 | **5** | `ceil(2ell/3)` |
| 11 | 8 | **8** | `ceil(2ell/3)` |
| 13 | 9 | **10** | `ceil(2ell/3)+1` (search-limited) |
| 17 | 12 | **13** | `ceil(2ell/3)+1` (search-limited) |

**Monotonicity fills the band above `m*` — NUMERIC.** For a **fixed** `Gamma`,
`top-(m+1) >= top-m` (one more nonnegative fiber), so `max_Gamma top-m` is
nondecreasing in `m`: a single listing witness at `m*` forces listing for **every**
`m* <= m <= ell-1` (gate FR replays the embedded `ell=11` (`m*=8`) and `ell=13`
(`m*=10`) `Gamma` and confirms the whole band `m* <= m <= ell-1` lists). So the
refutation is **not** confined to the corner `t=ell-2`; it fills `m* <= m <= ell-1`
(e.g. `ell=17` lists already at `m=13 < ell-1=16`).

**Bracket by rigor (OPEN only below `m*`).** Rigorous lower bound `t0(ell) >= 4`:
Theorem R (PR #223) proves `t=3`, `m=4` vacant for every prime `ell`, and the pair-cap
already permits listing from `m=5`, so no better rigorous lower bound follows from
pair-counting alone [**PROVED** `t0 >= 4`; exact value **OPEN**]. What stays **OPEN**
is strictly on the low side: proving non-listing for `m < m*` (rigorous only at
`t=3`/`m=4`), and whether the onset can be pushed down to `ceil(2ell/3)` for
`ell >= 13` (i.e. is the `+1` real, or a search limit).

## 5. Salvage upper bound and moment-method boundary

### 5a. Pair-cap closed form — PROVED

Lemma R (PR #223, every `m=t+1`, any `t`): `sum_b mu(mu-1) <= B := (ell-1)(ell-2)`.
With Cauchy-Schwarz `sum_b mu^2 >= R^2/m` over the `m` contributing cosets:

> **`R <= (m + sqrt(m^2 + 4mB))/2`, `B = (ell-1)(ell-2)`.**

- **`m=4` (`t=3`):** the bound is `2 + 2 sqrt(ell^2-3ell+3) < 2ell`, so `R <= 2ell-1`
  — this **re-derives Theorem R** as the `m=4` slice (verifier: `floor = 2ell-1` at
  `ell in {5,7,11,13,17,23}`).
- **`m=ell-1`:** `R <= (ell-1)(1+sqrt(4ell-7))/2 = Theta(ell^{3/2})`, so the
  permitted extras `R - 2ell = Theta(ell^{3/2})` — **not** `O(ell)`.

The closed form is `>=` the exact integer program `max sum rho_j` at every `ell,m`
tested (gate SB, brute-force IP at `ell=5,7`, all `m`).

### 5b. Moment method cannot beat `O(ell^{3/2})`

**Triple cap — PROVED (negative; gate MM).** The concentrated
`Gamma(X) = X + X^2 + ... + X^{ell-1}` (value `-1` taken `ell-1` times on `H`)
**saturates** the pair-cap with a **single** coset (`sum mu(mu-1) = (ell-1)(ell-2)
= B`) yet has triple-count `T3 = (ell-1)(ell-2)(ell-3) = Theta(ell^3)`
(`T3/B = ell-3 -> infinity`); so **no triple-cap sits below `Theta(ell^3)`**.

**Higher moments — LEMMA (scaling).** For every factorial moment `k > 2` the
concentrated `Gamma` (`~ ell^k`) dominates the pair-cap-tight spread `R`-maximiser
(`~ ell^{1+k/2}`), so `k=2` is the unique extremal moment; any real improvement must
inject **realizability** (a single `deg <= ell-1` `Gamma` cannot spread medium fibers
over many cosets) — precisely what Theorem R used at `t=3` and what is **OPEN** for
`t>=4`.

## 6. Replication Lemma — PROVED

> For `1 <= d < ell`, `Gamma(X) = Gtilde(X^d)` with `Gtilde` constant-free of degree
> `D`, `dD <= ell-1`: for **every** coset `b`, `mu_Gamma(bH) = mu_Gtilde(b^d H)`.

*Proof.* `Gamma(bh) = Gtilde(b^d h^d)`; `d` invertible mod the prime `ell` makes
`h -> h^d` a bijection of `H`, so the value-multiset of `Gamma` on `bH` equals that
of `Gtilde` on `b^d H`; take maxima. QED Since `n=(p-1)/ell` is even for odd
`ell`, `d=2` always gives replication factor `gcd(2,n)=2` (and `-1 not in mu_ell`), so
the frontier at degree `ell-1` pulls back from lower degree and the `-1` symmetry is
free. (Gate RP verifies the identity at `ell in {7,11,13}`.)

## 7. The night-numerics correction

The night high-`t` search `w2_r2_hight.py` reported `maxRet = 9` at `(ell=7,t=5,m=6)`
(gap `5` below `2ell=14`) and concluded `m=t+1` vacancy holds for high `t`. That run
**fixed one random scalar vector** `c` and searched only `(u,v,gamma)`, leaving the
`m=t+1` targets `lambda_j` tunable through `(u,v)` alone — **2 DOF against `m=t+1`
targets** — with greedy/random point-forcing (30 restarts); its `maxRet` is a
**search artifact**, not the true maximum. Decoupling the scalars (Lemma LF supplies
the missing `t-1` DOF; the `lambda`-map is surjective) and reading the exact spectrum
gives `top6 = 16` at the same cell. PR #223's own `## Scope — honest` section
(L113-121) already flagged the `t>=4` numerics as OPEN/non-probative and named the
exact open question — "a single `deg <= ell-1` `Gamma` cannot have medium fibers on
many cosets at once" — which the exact solve now answers in the affirmative.

## 8. Where this lands in the ledger

The witnesses feed the pre-registered TARGET nodes **`petal_mixed_amplification`**
and **`pma_wide_residual`** (`key: true`): a nonzero primitive mixed count at
`m=t+1`, prime `ell`. No proved chart claims zero mixed extras here — the
fixed-excess full-petal charts (`petal_fixed_excess`, PR #197) are delivered only
through excess `e <= 6`, while these witnesses sit at excess
`e = |M| - ell = 19` (at `t=5`; `~20`, growing with `t`), inside the declared-open
growing-defect residual `prob:v13-l1-residuals`; there is **no upstream
inconsistency**. The
refutation also does **not** touch the displayed prize regime: mirroring PR #222's
Support-fraction corollary (L56-71), the sunflower support fraction at `m=t+1` is
`(t+1)/(2t+1) = 1/2 + 1/(2(2t+1)) > 1/2` strictly, above the petal-heavy `m<=t`
corner that Theorem A (PR #222) covers unconditionally, and the prize regime is the
**discrete** rate set `rho in {1/2,1/4,1/8,1/16}` (`towards-prize.md` v12, L42-49), not
a continuous window.

## 9. Status summary and artifacts

**PROVED:** Lemma LF (`lambda`-freeness, general `m=t+1`); the pair-cap salvage
closed form and its `m=4` re-derivation of Theorem R; the moment-method triple-cap
boundary (gate MM; the higher-moment generalization is a scaling LEMMA); the
Replication Lemma. **NUMERIC (exact):** the two explicit witnesses at `(5,7,6)` and
`(4,7,5)` (full chain, `ell=7`) refuting `PV(t,d,m)` (`d=ell`) at `m=t+1`; the
spectrum `>= 2ell` replayed by gate FR at `ell in {11,13}` (`m*=8,10`); the frontier
onset `m0 = ceil(2ell/3)` (achieved `m* = m0` at `ell=7,11`; `m* = m0+1` search-limited
at `ell=13,17`). **OPEN (low side only):** non-listing for `m < m*` (rigorous just at
`t=3`/`m=4`, giving `t0 >= 4`) and whether the onset drops to `ceil(2ell/3)` for
`ell >= 13`; the `t>=4` realizability constraint that would upgrade the frontier to a
theorem; composite `ell` (routes through the PR #224 stabilizer-descent
classification). No paper-text change; material stays in `experimental/`. Companions
#218, #219, #222, #223, #224 are **open PRs** (not merged).

| file | content |
|---|---|
| `experimental/notes/l1/l1_prime_ell_pv_refutation.md` | this note |
| `experimental/scripts/verify_l1_prime_ell_pv_refutation.py` | self-contained verifier (embedded witness constants; W5a/W5b, W4a/W4b, LF, SB, MM, FR, PB, RP, TR); exit 0 iff all gates pass |

Provenance: the two-3-fiber onset was first spotted by the PI probe
`pi_probe_two3fibers.py` (a lower-bound-only scan of the first nullspace vector);
the exact witnesses come from decoupling the scalars via Lemma LF and scanning the
projective nullspace. Verifier arithmetic is own (modular, Gaussian elimination,
polynomial division); no sampling — all extrema by exact linear solves.
