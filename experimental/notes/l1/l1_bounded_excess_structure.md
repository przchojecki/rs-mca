# L1: bounded-excess structure on `E_3 <= ell + C'` (`C'` localized to `+2`; three exact reasons)

**Type: AUDIT + PROVED-LOCAL (two items) + EXPERIMENTAL (coverage) + ROUTE-CUT (no-go).
Non-superseding: this note edits, supersedes, and depends on nothing already integrated.**
This is the first structural work on the post-refutation open target of
`experimental/notes/l1/l1_e3_law_refuted.md` / `experimental/notes/l1/l1_sigma_calculus.md`:
after `E_3 <= ell` was PROVED on the covered chart (`T <= 4`, Theorem 1) and REFUTED on the
residual chart (`T >= 5`, six witnesses up to `E_3 = ell+2`), the open question became whether a
uniform ceiling `E_3 <= ell + C'` exists at all. This note supplies three exact pieces of structure
that jointly narrate the observed ceiling `C' = 2` without proving it extremal: **(1)** an identity
reducing "`excess >= 3`" to a precise combinatorial existence question ("a realizable tail-excess
`T >= 7`"); **(2)** a proof that the canonical extremal shape's excess is bounded by
`(2*ell-20)/3` from the pairwise cap + Lemma R alone (an `O(ell)` bound, exceeding `+2` already at
`ell = 17`); **(3)** a geometric reformulation (a concurrency condition in a fixed projective plane)
that explains, via a dedicated hunt (425 plants, full projective sweeps, `ell in {17,19}`), why the
Lemma-R headroom is not realized: concurrency counts observed are `7, 5, 5, 3` — *dropping*, not
rising, as more cosets become available. No new law is claimed; `C' <= 2` remains open, and its
sharp form (no realizable `T >= 7` tail) is named precisely in §6.

Filed at `experimental/notes/l1/l1_bounded_excess_structure.md`. Companion zero-arg verifier:
`experimental/scripts/verify_l1_bounded_excess_structure.py` (stdlib, offline, deterministic, exit 0
iff all gates pass; `--tamper-selftest`). Companion data:
`experimental/data/certificates/l1-e3-law/l1_bounded_excess_ledger.json` (identity table,
sub-ceiling table, coverage ledger; ported from the source hunt's raw JSON, with two corrections
noted in §5). Source material: an internal hunt ("Lane G") whose own analysis and results are not
shipped as repo files; every number below was independently re-derived from the raw `gamma`
vectors of the six already-integrated witnesses, or re-run from scratch for the toy sweep of §5.

Notation inherited from the integrated notes. `ell` odd prime, `ell | p-1`, `n = (p-1)/ell` cosets,
`Gamma(X) = sum_{r=1}^{ell-1} gamma_r X^r` constant-free mixed; per coset `mu_b` = max fiber size;
sorted spectrum `mu_1 >= mu_2 >= ...`; `E_3 := sum_k (mu_k-2)_+`; `K` = number of fibers of size
`>= 2`; `T := sum_{k>=3}(mu_k-2)_+` (from the third-largest fiber onward); `excess := E_3 - ell`.
All arithmetic exact over `F_p`, stdlib only.

**Status legend:** AUDIT (root-cause / structural observation, independently recomputed) /
PROVED-LOCAL (proof included, finite scope stated) / EXPERIMENTAL (well-supported, coverage stated
honestly) / ROUTE-CUT (a proof route shown algebraically insufficient; no positive claim).

---

## 0. Headline

1. **AUDIT — the excess identity.** `excess = T - 4 - capslack`, `capslack := ell - (mu_1+mu_2) >= 0`
   (the PROVED pairwise cap). Verified exactly on all six residual-chart witnesses of
   `l1_e3_law_refuted.md` (§1). Consequence: `excess >= 3` iff a realizable config carries
   `T >= 7 + capslack` (`T >= 7` at a cap-tight top pair).
2. **PROVED-LOCAL (two items).** (i) The pairwise cap forces the canonical fat-tail shape: a
   size-`(ell-3)` fiber forces every other fiber `<= 3`. (ii) For that shape `[ell-3, 3^k]`, Lemma R
   alone gives `excess <= floor((2*ell-20)/3)` — PROVING `excess <= 2` for `ell <= 13`, but only
   `<= 4` at `ell = 17` (the record witness W3 attains `+2`, a gap of `2`).
3. **AUDIT — the q-plane obstruction.** For that same shape, realizability is exactly "`k` points of
   a fixed projective plane `P^2(F_p)` all concurrent". Observed concurrency counts:
   `7` (`ell=17,p=137,n=8`), `5` (`ell=17,p=239,n=14`), `5` (`ell=17,p=307,n=18`),
   `3` (`ell=17,p=409,n=24`, undercovered), and — a different `ell` shown for the same qualitative
   trend — `5` (`ell=19,p=229,n=12`, exhaustive-per-plant). More cosets give *fewer*, not more,
   concurrent threes; `k >= 8` (needed for `excess >= 3`) was never seen.
4. **ROUTE-CUT — the identity web alone cannot bound `C'`.** Lemma R + the pairwise cap, even
   restricted to the single best-understood shape, permit `excess = Theta(ell)`, not `O(1)`; the
   fully unshaped combination is even weaker (`Theta(ell^2)`). Only realizability content — not any
   dimension count on `(D,Z,U,V_k)` — can close the gap (this is exactly the sigma-calculus note's
   own N1 diagnostic, re-confirmed here on the shape-specific bound).
5. **EXPERIMENTAL — coverage.** 425 plants swept (full `P^2(F_p)` sweep per plant, no member
   skipped), `ell in {17,19}`; zero configs with `excess >= 3`. `ell in {23,29}` not run (justified
   by the same mechanism, §5). Consistent with, and citing as concurrent, PR #364's independent
   finding that `m*(19)` stays in `{8,9}`.
6. **Two corrections to the source hunt, found by independent recompute (§5); no silent fixes.**

---

## 1. The excess identity (reduces the whole question to a fat tail)

Write the min-mu>=3-normalized sorted spectrum `mu_1 >= mu_2 >= ...` (dropping size-2 fibers is
free: `l1_e3_law_refuted.md` §2 item 2, PROVED — it preserves `E_3`, `T`, and realizability exactly).
By definition `E_3 = (mu_1-2) + (mu_2-2) + T`. By the PROVED pairwise cap (statement quoted verbatim (its proof is condensed here) in §2),
`mu_1 + mu_2 <= ell`; write `capslack := ell - (mu_1+mu_2) >= 0`. Substituting
`mu_1+mu_2 = ell - capslack`:

> **`E_3 = (mu_1+mu_2) - 4 + T = ell - capslack - 4 + T`, i.e. `excess := E_3 - ell = T - 4 - capslack`.**

This is pure bookkeeping (a decomposition + a substitution), not a new inequality; it is exact for
*every* realizable config, not just extremal ones. Verified on all six `T >= 5` witnesses of
`l1_e3_law_refuted.md` (raw `gamma` re-evaluated fresh; gate i of the verifier):

| id | `ell` | `p` | spectrum | `E_3` | `mu_1+mu_2` | `capslack` | `T` | `excess` | `T-4-capslack` |
|:---|:-----:|:---:|:---------|:-----:|:-----------:|:----------:|:---:|:--------:|:--------------:|
| W3 | 17 | 137 | `[14,3,3,3,3,3,3,3]` | 19 | 17 | 0 | 6 | **+2** | 2 |
| W1 | 29 | 233 | `[15,14,4,3,3,3,2,2]` | 30 | 29 | 0 | 5 | +1 | 1 |
| W2 | 23 | 139 | `[14,9,4,4,3,2]` | 24 | 23 | 0 | 5 | +1 | 1 |
| EXTRA1 | 29 | 233 | `[20,9,4,3,3,3,2,2]` | 30 | 29 | 0 | 5 | +1 | 1 |
| EXTRA2 | 29 | 233 | `[16,13,4,3,3,3,2,2]` | 30 | 29 | 0 | 5 | +1 | 1 |
| EXTRA3 | 17 | 103 | `[11,5,5,4,3,2]` | 18 | 16 | **1** | 6 | +1 | 1 |

All six match exactly (`excess == T-4-capslack`), including EXTRA3, the one non-cap-tight witness
(`capslack=1`), which is the sharpest sanity check available: the identity is not merely calibrated
on the cap-tight majority.

**Consequence (exact, PROVED given the identity above).**

> `excess >= 3` &nbsp;iff&nbsp; a realizable config carries `T >= 7 + capslack`; at a cap-tight top
> pair (`capslack=0`, the case of every record witness so far) this is exactly `T >= 7`.

So the entire open question "does a uniform ceiling `E_3 <= ell+C'` exist" is, at fixed `capslack`,
*exactly* the question of how large a realizable tail excess `T` can be. The canonical shape for
concentrating `T` is `[ell-3, 3^k]` (W3's own shape): top pair `[ell-3,3]` is cap-tight
(`capslack=0`), tail is `k-1` further threes (`T = k-1`, since `T` starts counting from the *third*-
largest fiber and the second-largest is itself one of the threes), so `excess = (k-1)-4-0 = k-5`:
**`excess = +3` needs exactly `k >= 8` size-3 fibers coexisting with one size-`(ell-3)` fiber.**

## 2. PROVED-LOCAL (two items)

**Item (i): the pairwise cap forces the fat-tail shape.** Quoting Lemma 3 of
`experimental/notes/l1/l1_sigma_calculus.md` in full (PROVED there; re-verified in gate (ii) below on
all six witnesses plus the general form on all six spectra's every pair, not just the top one):

> **Lemma 3 (PAIRWISE `V_i cap V_j = 0`; hence `K=2 => sigma = 0`). PROVED.**
> "For any two fibers of one `Gamma`, `mu_i + mu_j <= ell` (pairwise cap), and then
> `V_i cap V_j = 0`. In particular for `K = 2`, `sigma = 0`."
> *Proof (cap).* "Choose `(alpha, beta, gamma)` nonzero solving `alpha W_i + beta lambda_i + gamma = 0`
> and `alpha W_j + beta lambda_j + gamma = 0` (two equations, three unknowns) ... The form
> `Phi := alpha X^ell + beta Gamma + gamma` then vanishes on `F_i` ... and on `F_j`; it is a nonzero
> polynomial ... of degree `<= ell`, so `mu_i + mu_j <= ell`."

This directly answers the reading the source hunt used and this note now certifies against the exact
lemma text: the proof is stated **"for any two fibers"** — it is not a fact about the top pair only,
it holds pairwise for **every** distinct-coset pair `(i,j)`, proved by the identical pencil
construction applied to that pair's own `(W,lambda)` data. Separately, and only as an *arithmetic*
consequence of the sorted order (not a further use of the lemma): since `mu_1 >= mu_2 >= mu_i` and
`mu_1 >= mu_2 >= mu_j` for every other index `i,j >= 2`, the top-pair sum `mu_1+mu_2` dominates every
other pair-sum, so checking the lemma on the top pair alone already certifies it on all others — this
is the sense in which "the top pair is the active/binding constraint" while the lemma itself "binds
all pairs" directly. Both readings are correct and are not in tension; gate (ii) checks both
(the lemma holds pairwise on every pair of all six witnesses, and separately that the top pair's sum
is the maximum over all pairs on each witness).

Consequence for the canonical shape: if `mu_1 = ell-3` (a size-`(ell-3)` fiber is planted), the
pairwise cap applied to `(1,2)` gives `mu_2 <= ell - mu_1 = 3`; since fibers below size 3 are freely
dropped by the min-mu>=3 normalization, every remaining fiber is *exactly* size 3 — this is exactly
the shape `[ell-3, 3^k]`, forced (not chosen) by the cap once the big fiber is planted. Checked
concretely on W3 (`ell=17`): `mu_1 = 14 = ell-3` forces `mu_2 <= 3`, and indeed `mu_2 = 3` (gate ii).

**Item (ii): the Lemma-R sub-ceiling for `[ell-3,3^k]`.** "Lemma R" is the pair-cap Proposition of
`experimental/notes/l1/l1_e3_charsum_paircap.md` (PROVED, elementary character-sum/root-count;
consistent with the same-named citations in `l1_prime_ell_onset.md` and
`l1_prime_ell_pv_refutation.md`):

> **Proposition (pair-cap).** With `Delta_zeta(X) := Gamma(X) - Gamma(zeta X)` for `zeta in mu_ell`:
> `sum_b sum_c N_b(c)(N_b(c)-1) = sum_{zeta != 1} #{x in F_p^* : Delta_zeta(x)=0} <= (ell-1)(ell-2)`.
> *Proof.* Each `Delta_zeta` (`zeta != 1`) is constant-free of degree `<= ell-1` (mixedness gives
> `Delta_zeta != 0`), hence has `<= ell-2` nonzero roots; sum over the `ell-1` nontrivial `zeta`.

Specialized to one config's max-fiber spectrum, this reads `sum_k mu_k(mu_k-1) <= (ell-1)(ell-2)`.
For the shape `[ell-3, 3^k]` (one fiber of size `ell-3`, `k` of size `3`):

```
(ell-3)(ell-4) + 6k <= (ell-1)(ell-2)
6k <= (ell-1)(ell-2) - (ell-3)(ell-4) = 4*ell - 10
k <= (4*ell-10)/6 = (2*ell-5)/3
```

Since `excess = k - 5` on this shape (§1), and `floor((2*ell-5)/3) - 5 = floor((2*ell-20)/3)`:

> **`excess <= floor((2*ell-20)/3)` for the `[ell-3,3^k]` shape, from Lemma R alone.**

| `ell` | `k_max = floor((2ell-5)/3)` | excess ceiling `floor((2ell-20)/3)` | status |
|:-----:|:---------------------------:|:------------------------------------:|:-------|
| 11 | 5 | **0** | Lemma R alone proves excess `<= 0` (hence `<= 2`) here |
| 13 | 7 | **+2** | Lemma R alone proves excess `<= 2` here (tight to the stated consequence) |
| 17 | 9 | +4 | realizability-limited: observed max is `+2` (W3) — gap of 2 |
| 19 | 11 | +6 | realizability-limited |
| 23 | 13 | +8 | realizability-limited |
| 29 | 17 | +12 | realizability-limited |

**Consequence:** Lemma R alone *proves* `excess <= 2` for this shape at `ell in {11,13}` (the only
two odd primes `<= 13` for which `ell-3 >= 3`, i.e. the shape is non-degenerate). It does **not**
prove `excess <= 2` at `ell = 17` — it permits up to `+4` there, a full `2` units above the record
`+2` witness (W3). This is the precise sense in which "`ell=17` is the smallest `ell` where the shape
can algebraically exceed `+2`, yet empirically (this note's coverage, §5) it does not."

## 3. The `q`-plane obstruction (AUDIT)

A size-`(ell-3)` fiber `F_0` (locator `g_0 = prod_{x in F_0}(X-x)`, monic, degree `ell-3`) forces
`Gamma` to have the form `Gamma = g_0*q + lambda_0` for some `q` of degree `<= 2` and constant
`lambda_0` (`= Gamma`'s common value on `F_0`) — because `Gamma - lambda_0` vanishes on `F_0`, hence
is divisible by `g_0`, and `deg(Gamma) - deg(g_0) = (ell-1)-(ell-3) = 2`. Since the fiber structure of
`Gamma` is unchanged by scaling `Gamma` by a nonzero constant or shifting `lambda_0`, only `q` up to
overall scalar matters: **`q` is a point of the projective plane `P^2(F_p)`** (this is exactly the
`d=3` nullspace dimension seen throughout the hunt). For any *other* coset, a candidate 3-fiber
`{x,y,z}` requires `Gamma(x)=Gamma(y)=Gamma(z)`, i.e. `g_0(x)q(x) = g_0(y)q(y) = g_0(z)q(z)` — two
linear homogeneous equations in `q`'s three coefficients, i.e. **one point of `P^2(F_p)`** (generic
2-equation/3-unknown system). So:

> A `[ell-3,3^k]` realization &nbsp;=&nbsp; `k` cosets whose independently-derived 3-fiber points of
> `P^2(F_p)` **all coincide at a single `q`**. A generic `q` gives zero 3-fibers; a fat tail is a
> rigid coincidence, not a generic feature.

**Concretely verified on W3** (`ell=17,p=137`; gate iii of the verifier, all arithmetic exact over
`F_137`): `F_0` = the known 14-point fiber, `g_0` its degree-14 monic locator, `lambda_0 = 124`. From
the raw `gamma`, `q = 26 + 0*X + 1*X^2` (degree exactly 2; `Gamma = g_0*q + 124` reproduces the shipped
`gamma` exactly). The other 7 cosets each carry one size-3 fiber; solving each one's own two linear
equations *independently* (without using the global `Gamma` at all) recovers, in every one of the 7
cases, the **identical** normalized point `q = (1 : 0 : 58)` (`= 26^{-1}*(26,0,1) mod 137`, since
`26*58 == 1 mod 137`) — matching the global `q` exactly. This is the concurrency claim, demonstrated
by direct, per-coset, from-scratch recomputation rather than asserted.

**Why the cap is empirically `+2` and not higher (the coverage finding, §5 for full ledger).** A
dedicated hunt (425 plants: `[ell-3,3^k]` at `ell in {17,19}` across primes `p in {137,239,307,409}`
(`ell=17`) and `p=229` (`ell=19`), plus the companion pair-plant shape `[ell-4,4,3^k]`) swept, for
each plant, the *entire* projective nullspace family (no member skipped) and read the true emergent
spectrum. Zero configs reached `excess >= 3` (equivalently, zero reached `k >= 8` concurrent threes).
The concurrency counts actually seen — `7` at `ell=17,n=8` (the record, `p=137`); `5` at `ell=17,
n=14` (`p=239`) and `n=18` (`p=307`); `3` at `ell=17,n=24` (`p=409`, undercovered — one plant only);
`5` at `ell=19,n=12` (`p=229`, exhaustive per-plant, 130 dropsets tried) — show concurrency counts
*dropping* as more cosets become available at fixed `ell=17`, with the extra cosets' candidate points
falling to generic (non-concurrent) position and contributing only inert size-2 fibers instead. This
directly refutes the naive hope that a larger `n` would fatten the tail past `k=7`: the opposite is
observed. (The `ell=19,n=12` data point is a *different* `ell`, included because it shows the
identical qualitative mechanism — not because it continues the `ell=17` sequence; see the correction
in §5.)

## 4. No-go (ROUTE-CUT): the identity web alone cannot bound `C'`

Neither identity-side tool in hand — used alone, together, or shape-restricted to the single
best-understood extremal family — produces an `O(1)` ceiling:

- **Unshaped:** Lemma R alone (all fibers merged into one quadratic budget, ignoring shape) gives
  only `E_3 <= (ell-1)(ell-2)/6 = Theta(ell^2)` (`l1_e3_charsum_paircap.md`'s own stated verdict:
  "`E_3 <= ell-2` is a rank / realizability statement, not a character-sum inequality" — the gap
  is a factor `~2-3`, "not a fixable constant").
- **Shape-restricted (`[ell-3,3^k]`, this note's §2):** Lemma R + the pairwise cap together give
  `excess <= floor((2*ell-20)/3) = Theta(ell)` — linear, still growing without bound in `ell`, and
  already exceeding the observed `+2` by `ell=17`.
- **The dimension web is not an independent route at all.** On `(D,Z,U,V_k)`, the master identity
  `sigma = E_3+K-ell+dimU` (`l1_sigma_calculus.md` §2.1, PROVED) is an *identity*, not an inequality
  (its own NO-GO diagnostic N1, §2A.3: "Any bound obtained purely by dimension-counting on these
  spaces therefore re-expresses `E_3 <= ell` as *itself*."). The excess identity of §1 above is the
  same phenomenon one level up: it is bookkeeping that *reformulates* the question (down to a
  tail-`T` existence question, or down to a `q`-plane concurrency-count question) without supplying
  new content. **Only realizability — which point sets can simultaneously be fibers of one shared
  low-degree `Gamma` — can close the gap to a constant `C'`,** exactly as `l1_e3_charsum_paircap.md`
  and the sigma-calculus N1/N3 diagnostics already concluded for the weaker `ell-2` ceiling; this
  note's contribution is confirming the same conclusion transports unchanged to the `+C'` question,
  and giving one shape's worth of concrete, checked evidence (§3) for what the realizability content
  looks like geometrically.

## 5. Coverage ledger (honest)

425 plants swept in total (`P^2(F_p)` exhaustive per plant — no member skipped; the *choice* of
plant is a deterministic sample, not exhaustive, except where the possible-plant count is itself
small enough to be stated exactly below):

| family | `ell` | `p` | `n` | plants swept | of possible | max `E_3` | max excess | best spectrum | `k3` | secs |
|:---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:---|:-:|:-:|
| `[ell-3,3^k]` (calibration) | 17 | 137 | 8 | 40 | 680 (`=C(17,3)`) | 19 | **+2** | `[14,3^7]` | 7 | 36.0 |
| `[ell-3,3^k]` | 17 | 239 | 14 | 101 | 680 | 17 | +0 | `[14,3^5,2^2]` | 5 | 569.1 |
| `[ell-3,3^k]` | 17 | 307 | 18 | 51 | 680 | 17 | +0 | `[14,3^5,2^2]` | 5 | 677.3 |
| `[ell-3,3^k]` | 17 | 409 | 24 | 1 | 680 | 15 | -2 | `[14,3^3,2^2]` | 3 | 29.2 |
| `[ell-3,3^k]` | 19 | 229 | 12 | 130 | 969 (`=C(19,3)`) | 19 | +0 | `[16,3^5,2^6]` | 5 | 661.8 |
| `[ell-4,4,3^k]` | 17 | 239 | 14 | 41 (of 150 requested) | not computed exactly (`>= 10^5`) | 17 | +0 | `[14,3^5,2^2]` | 5 | 313.9 |
| `[ell-4,4,3^k]` | 19 | 229 | 12 | 61 (of 120 requested) | not computed exactly (`>= 10^5`) | 19 | +0 | `[16,3^5,2^6]` | 5 | 380.8 |

Totals: **425** plants, **2668.1 s** (~44.5 min) compute, **0** configs with `excess >= 3` anywhere.
The calibration row independently rediscovers the already-shipped W3 witness's exact invariants
(`E_3=19`, spectrum `[14,3^7]`) from the hunt's own combinatorial generation, validating the method
against a known answer before trusting it on the negative (no-`+3`) results. Under-covered:
`ell=17,n=24` (`p=409`, only 1 of 680 possible dropsets tried — slowest prime here, `|P^2(F_409)| =
167,691` members per plant); `ell in {23,29}` not run at all. This is not an arbitrary gap: the
`n=14/18` trend at `ell=17` (concurrency count *falling* to 5 as `n` grows from 8) already refutes
the hope that larger `n` helps, and Lemma R *permits* strictly more excess at `ell in {23,29}`
(`+8`, `+12`) than at `ell=17` (`+4`) — so, by the same realizability mechanism identified in §3,
these are expected to be at least as excess-capped as `ell=17`, not less; they were left unrun by
budget, not by any claimed proof.

**Two corrections found by independent recompute (no silent fixes):**

1. **The `(ell=19,p=229,n=12)` row was labeled "130/130 (exhaustive triples)" in the source hunt.**
   `C(19,3) = 969`, and only 130 dropsets were attempted — a deterministic spread sample (`~13.4%`
   coverage of the possible dropsets), not exhaustive over them. What *is* exhaustive, and correctly
   so: the `P^2(F_229)` sweep within each of the 130 attempted plants (every one of `229^2+229+1 =
   52,671` projective points evaluated), and the 130-of-130 *completion* rate (no time-cutoff, unlike
   the `p=409` row). The qualitative finding (max excess `= 0`, no win) is unaffected; only the word
   "exhaustive" (describing dropset coverage, not per-plant sweep coverage) is corrected here.
2. **The maximum excess at that same row is `+0`, not `+1`.** Both the source hunt's own JSON
   (`max_excess: 0`, spectrum `[16,3,3,3,3,3,2,2,2,2,2,2]`, `E_3=19=ell` exactly) and an independent
   from-scratch recompute of the reported best plant (dropset excluding `{0,2,15}` from coset 0 at
   `ell=19,p=229`; fresh nullspace + full `52,671`-member `P^2` sweep, `4.14 s`) agree exactly:
   `E_3=19`, `excess=0`. `E_3=19=ell` reaches the covered/residual boundary here but does not cross
   it; this row contributes no `T>=5` excess evidence either way, only a (correctly) null result for
   the `excess>=3` hunt.

## 6. Non-claims

`C' <= 2` is **not proved** — it is a localized, three-times-corroborated observation (§0.1-3), not a
theorem. The open core is exactly what `l1_e3_dim_syz_crux_refuted.md` (PR #365, concurrent, cited by
path and number, not depended on) already names: **no realizable configuration carries a tail-excess
`T >= 7`**, an instance of the `(W,lambda)`-Veronese transversality the residual conjecture RC already
flags as its own open core (`l1_sigma_calculus.md` §2A.2/§2A.3) — this note narrows that transversality
question, for one shape, to a concrete concurrency-of-`>=8`-points-in-`P^2` statement (§3), and shows
by direct hunt that `k=7` is the largest concurrency count found so far, but proves neither an upper
bound `k <= 7` nor its negation for larger, unswept primes or shapes. Does not claim the `[ell-3,3^k]`
family is the only relevant shape (the companion `[ell-4,4,3^k]` pair-plant family was also swept, to
`+0`, but not analyzed geometrically here). Does not claim coverage completeness anywhere in §5
(explicitly partial; `ell in {23,29}` unrun). Does not claim any relationship between this note's
`excess` question and the `m*(19)` vacancy question beyond the consistency noted in §0.5: this note's
own sweeps never reached the `E_3 >= ell+3`, top-`8`-concentrated, listing-eligible configuration a
crossing at `m=8` would need, which is consistent with, but does not itself establish, PR #364's
(`experimental/notes/l1/l1_ell19_band_refuted.md`, concurrent, cited by path and number, not depended
on) conclusion that `m*(19)` remains `{8,9}`. Promotes nothing — AUDIT / PROVED-LOCAL / EXPERIMENTAL /
ROUTE-CUT scope only, `experimental/` placement.

## 7. Verifier contract

`experimental/scripts/verify_l1_bounded_excess_structure.py`, zero-arg, stdlib only, offline,
deterministic, exit 0 iff all gates pass; self-contained (does not import any sibling script, the
source hunt's scratch files, or the concurrent PRs' files):

- **Gate i — excess identity.** For each of the six `l1_e3_law_refuted.md` witnesses (raw `gamma`
  embedded here), recompute the spectrum fresh, then `E_3`, `T`, `mu_1+mu_2`, `capslack`, and check
  `E_3 - ell == T - 4 - capslack` exactly; also checks the pairwise cap holds on *every* pair (not
  just the top one) and that the top pair's sum is the maximum over all pairs, on all six.
- **Gate ii — Lemma-R sub-ceiling.** Recomputes the `(2*ell-20)/3` table for `ell in
  {11,13,17,19,23,29}` from the stated formula; checks the `ell<=13 => excess<=2` consequence
  arithmetically; checks Lemma R's raw inequality `sum mu(mu-1) <= (ell-1)(ell-2)` holds on all six
  witnesses (not just the shape-restricted table); checks the W3-specific `mu_1=ell-3 => mu_2<=3`
  instance and the stated `+4`-permitted-vs-`+2`-attained gap at `ell=17`.
- **Gate iii — `q`-plane spot-check on W3.** From W3's raw `gamma` and its known 14-point big fiber,
  recovers `g_0`, `lambda_0`, and the global `q` (degree exactly 2) by exact polynomial division;
  reconstructs `Gamma = g_0*q+lambda_0` and checks it matches the shipped `gamma` exactly; identifies
  the other 7 cosets' 3-fibers directly from the spectrum; for each of the 7, independently solves
  its own 2-equation/3-unknown linear system for `q` (without using the global `Gamma`) and checks
  all 7 normalized solutions are identical to each other and to the global `q`.
- **Gate iv — bounded-time toy re-run at `(ell=19,p=229,n=12)`.** The full 130-dropset sweep took
  `661.8 s` offline (embedded here as certificate data, matching `laneG_results.json`'s independent
  ledger exactly); reproducing it live would exceed a reasonable verifier budget, so this gate
  instead (a) reproduces from scratch, live, the specific reported best dropset (excluding
  `{0,2,15}` from coset 0), confirming `E_3=19`, `excess=0`, spectrum `[16,3^5,2^6]` exactly
  (`~4 s`), and (b) sweeps a small deterministic subsample of 4 further dropsets (the
  lexicographically first four triples of `C(19,3)`), confirming none reach `excess >= 3` either
  (`~4 s` each) — stated explicitly as a bounded subsample, not a claim of reproducing the full
  130-plant coverage live.
- `--tamper-selftest`: flips one datum per gate (an identity term, a Lemma-R table entry, one of the
  7 recovered `q` points, the toy re-run's claimed spectrum) and confirms each targeted gate then
  FAILS.

Runtime target < 60 s for gates i-iii; gate iv adds `~20 s` for its 5 live dropset sweeps (total
`< 90 s`). Companion certificate:
`experimental/data/certificates/l1-e3-law/l1_bounded_excess_ledger.json`.

## Refs

- `experimental/notes/l1/l1_e3_law_refuted.md` (the six witnesses; Theorem 1; the pairwise cap;
  the master identity; the `min-mu>=3` normalization).
- `experimental/notes/l1/l1_sigma_calculus.md` (Lemma 3 pairwise cap, statement quoted verbatim (its proof is condensed here) in §2; the
  master identity; Theorem 1 and RC; the N1/N2/N3 no-go diagnostics reused in §4).
- `experimental/notes/l1/l1_e3_charsum_paircap.md` (Lemma R / the pair-cap Proposition, quoted in
  full in §2; its own `Theta(ell^2)` no-go verdict reused in §4).
- `experimental/data/certificates/l1-e3-law/l1_e3_law_refutation.json` (source of the six raw
  `gamma` vectors re-verified in gate i).
- `experimental/notes/l1/l1_ell19_band_refuted.md` (PR #364, branch `l1-ell19-band-refuted`,
  **concurrent open PR, not integrated, not depended on**: independently concludes `m*(19)` stays
  `{8,9}`, consistent with this note's own no-`m=8`-crossing observation, §0.5/§6).
- `experimental/notes/l1/l1_e3_dim_syz_crux_refuted.md` (PR #365, branch `l1-dim-syz-crux`,
  **concurrent open PR, not integrated, not depended on**: independently names the identical
  bounded-excess target `E_3 <= ell+C'` and the same `(W,lambda)`-Veronese transversality as the
  open core; this note supplies one shape's worth of concrete structure toward that same target).
