# Audit of PR #103: σ≥2 (higher-slack) extension-line counterexample

- **Status:** AUDIT / **VERIFIED** (σ=2 and σ=3 mechanism + fixed-tail injective
  count; independent exact-arithmetic brute check over `F_{p^2}`).
- **Agent/model:** Claude Opus 4.8 (L2/X1 lane, branch `allen/l2-x1-interleaved-mca`).
- **Date:** 2026-06-24.
- **Target:** PR #103 (`notes/f1/f1_fixed_rate_extension_counterexample.md`,
  Codex) — the general fixed-slack `σ≥1` extension-line family. This completes
  the gap left open by [`audit_pr103_f1_sigma_one.md`](audit_pr103_f1_sigma_one.md)
  (which verified σ=1 and flagged σ≥2/slow-slack as "not separately brute-checked").
- **Verifier:** `scripts/verify_audit_pr103_f1_sigma_two.py`.

## Claim audited

Over `B=F_p`, `F=F_{p^2}=B[α]`, `H=F_p^*`, `n=p-1`, `C_F=RS[F,H,k]`, fix slack
`σ≥1`, set `a=k+σ`, `δ=1-a/(p-1)`. The line `f(x)=x^a/(x-α)`, `g(x)=-1/(x-α)`
has, for every `a`-subset `S⊂H` with the **prefix-vanishing** conditions

```text
e_1(S) = e_2(S) = ... = e_{σ-1}(S) = 0,
```

a support-wise MCA-bad slope `z_S = Q_S(α)`, `Q_S = X^a - L_S`. Fixing a
`(k-1)`-tail `T` and varying `U` (`|U|=σ+1`) over admissible blocks
`S=T∪U` gives an injective slope map, hence `emca(C_F,δ) ≥ M_{p,k,σ}/p^2`,
with density `→ (1-ρ)^{σ+1}/(σ+1)!` at fixed rate.

## Verdict: CORRECT (σ=2 and σ=3 brute-verified)

### The mechanism (why prefix-vanishing is exactly the right condition)
`L_S = X^a - e_1 X^{a-1} + e_2 X^{a-2} - …`, so `Q_S = X^a - L_S =
e_1 X^{a-1} - e_2 X^{a-2} + …`. Imposing `e_1=…=e_{σ-1}=0` kills the top `σ-1`
coefficients, dropping `deg Q_S ≤ a-σ = k`. Then `Q_S - z_S` has degree `≤ k`,
and since `(Q_S-z_S)(α)=0` for `z_S=Q_S(α)`, the quotient
`c_S=(Q_S-z_S)/(X-α)` is an **exact** degree-`<k` codeword of the extension
code `C_F`. The closing codeword is genuinely `α`-bearing (extension-valued) —
the obstruction does not descend to the base field.

### Numerical verification (`verify_audit_pr103_f1_sigma_two.py`)
Exact `F_{p^2}` arithmetic, `α=(0,1)`. For `(p,k,σ) ∈
{(11,2,2),(13,3,2),(17,3,2),(23,2,3)}`, every admissible `S` passes:

```text
[OK] deg Q_S ≤ k                         (prefix-vanishing drops the degree)
[OK] c_S = (Q_S - z_S)/(X-α) divides EXACTLY, deg c_S < k   (real extension codeword)
[OK] f + z_S g agrees with c_S on all of S   (support |S| = k+σ)
[OK] noncontainment: g is not degree-<k explained on S
[OK] fixed-tail slope map INJECTIVE          (PR #103's exact count device; 8–22 blocks)
```

The overall distinct-slope count is also near-injective (e.g. 185 of 256
admissible at `(17,3,2)`), so the bad-slope density bound holds directly, not
only through the fixed-tail device. (The asymptotic `(1-ρ)^{σ+1}/(σ+1)!` is the
`p→∞` leading term; at these tiny `p` the `o(1)` dominates and the measured
density runs higher — informational only.)

## The three-lane unification (the headline cross-lane fact)

The prefix-vanishing condition `e_1=…=e_{σ-1}=0` is **exactly the fixed-jet
condition of PR #105's Lemma 1** ("the top `σ` coefficients of the locator
`P_J` are held common"), specialized to the common value `0`. Concretely, the
three constructions are one:

| lane | object | locator condition | bad slope |
|---|---|---|---|
| **F1** (#103, this audit) | extension line `x^a/(x-α)` | `e_1=…=e_{σ-1}=0` (prefix-vanishing) | `z_S = Q_S(α)`, `Q_S=X^a-L_S` |
| **M1** (#105, fixed-jet) | Cycle116 locator family | top `σ` coeffs of `P_J` common | `z_J = 1/P_J(β)` |
| **L2/X1** (#101, deep-point) | simple-pole line `u_z/(x-α)` | (heavy word / list) | `{P(α) : P in list}` (deep image) |

All three are **"a prefix-constrained locator fiber produces bad line-slopes via
a parity-check / deep-point evaluation, and the count is the size of the
evaluation image."** PR #103's `z_S=Q_S(α)` is literally the deep image of the
monomial received word `x^a` (already noted for σ=1 in the σ=1 audit; here it
extends to all `σ`, with the prefix-vanishing playing the fixed-jet role). This
is the strongest concrete evidence yet for the "everything = prefix-fiber +
deep-point bridge" theme spanning the F1, M1, and L2 lanes.

## Scope / honest limits
- **Slow-slack** (`σ = o(√p/log p)`, growing with `p`): the *fixed*-σ family is
  now brute-verified for σ=2,3; the growing-σ asymptotic uses the same mechanism
  plus a character-sum count for `#{admissible S}`. The mechanism is confirmed;
  the character-sum count itself was not re-derived here (it is a standard
  inclusion–exclusion / Weil-bound estimate, plausible but its constants are
  unaudited).
- **Higher extension degree** `e≥2`: as in the σ=1 audit, the slopes lie in the
  quadratic subfield `B[α]` (numerator `N=1`, denominator `X-α`), so only the
  denominator `|F|=p^e` changes; the `F_{p^2}` verification covers the mechanism.
- This remains a **sub-reserve** counterexample: fixed σ gives `η=σ/(p-1)`, far
  below the corrected `C/log n` reserve — PR #103 states this. It is a valid
  fixed-rate F1 obstruction in the sub-reserve regime, not a reserve breach.

## Bottom line
PR #103's higher-slack `σ≥2` family is **correct and independently reproduced**
(σ=2, σ=3, mechanism + fixed-tail injectivity). Together with the σ=1 audit, the
entire fixed-σ degree-one extension-line family is verified, and it is unified
with the M1 fixed-jet (#105) and L2 deep-point (#101) constructions as a single
prefix-locator-fiber mechanism.

## Reproducibility
```bash
python3 experimental/scripts/verify_audit_pr103_f1_sigma_two.py
python3 experimental/scripts/verify_audit_pr103_f1_sigma_two.py --json
```
