# Audit of PR #103: σ=1 extension-line counterexample

- **Status:** AUDIT / **VERIFIED** (σ=1 core; independent re-derivation + brute check).
- **Agent/model:** Claude Opus 4.8 (L2 loop, branch `allen/l2-x1-interleaved-mca`).
- **Date:** 2026-06-24.
- **Target:** PR #103 (`notes/f1/f1_fixed_rate_extension_counterexample.md`, Codex)
  — the degree-one extension-line fixed-rate counterexample.
- **Verifier:** `scripts/verify_audit_pr103_f1_sigma_one.py` (independent of the
  PR's own `verify_f1_fixed_rate_extension_counterexample.py`).

## Claim audited

Over `B=F_p`, `F=F_{p^2}=B[alpha]` (`alpha^2=d` nonsquare), `H=B^*`, `n=p-1`,
`C_F=RS[F,H,k]`, `a=k+1`, `delta=1-a/n`, the line `f(x)=x^a/(x-alpha)`,
`g(x)=-1/(x-alpha)` has, for each `a`-subset `S`, the support-wise MCA-bad slope
`z_S = Q_S(alpha)` with `Q_S=X^a-L_S`; a fixed `(a-2)`-subset `T` gives
`binom(p-a+1,2)` distinct slopes, so `emca(C_F,delta) >= binom(p-a+1,2)/p^2`,
i.e. `(1-rho)^2/2 - o(1)` at fixed rate.

## Verdict: CORRECT

### Independent re-derivation
For `z=z_S`, the polynomial `x^a - z - c(x)(x-alpha)` is monic of degree `a=k+1`
(since `deg c < k`), so it vanishes on the `k+1`-point support `S` iff it equals
`L_S`. That forces `c(x)(x-alpha)=Q_S(x)-z`, which has a polynomial solution `c`
of degree `< k` over **F** exactly when `(x-alpha) | (Q_S-z)`, i.e. `z=Q_S(alpha)`.
So `u_{z_S}` agrees on `S` with the genuine `C_F`-codeword
`c_S=(Q_S-z_S)/(X-alpha)`. The far condition holds because `(X-alpha)G+1` has
degree `<= k` and cannot vanish on `|S|=k+1` points (its value at `alpha` is 1).
Distinctness: `z_{T∪{x,y}} = alpha^a - L_T(alpha)(alpha-x)(alpha-y)`, and
`(alpha-x)(alpha-y) = d+xy-(x+y)alpha` is injective in the unordered pair
`{x,y}` (distinct elementary symmetric functions), giving `binom(p-a+1,2)`
distinct slopes. All steps check.

### Cross-framework confirmation (deep-point bridge)
`z_S` is exactly the deep image of the **monomial received word** `U(x)=x^a`:
`Q_S` is the degree-`<= k` polynomial that agrees with `x^a` on `S`
(`Q_S(s)=s^a` since `L_S(s)=0`), and `z_S=Q_S(alpha)`. So PR #103's σ=1 family is
the monomial instance of the deep-point identity of `notes/x1` §1 — the two
independent constructions agree. (This is the *lower-bound* use; `notes/x1` §2.10
is the consistent *upper* structure.)

### Numerical verification
`verify_audit_pr103_f1_sigma_one.py` brute-checks over `F_{p^2}` for
`(p,k) in {(11,3),(13,4),(11,2)}`: every `a`-subset yields an exact deg-`<k`
`C_F`-codeword witness (MCA-bad), the deep framing holds, the fixed-`T` family
gives exactly `binom(p-a+1,2)` distinct slopes, and the total distinct bad-slope
count exceeds it. PASS.

### Note on a subtlety (and a corrected check)
`C_F = RS[F,H,k]` is the **extension** code: the closing codeword `c_S` has
`F`-valued (α-bearing) coefficients, which is legitimate. (An initial version of
this audit wrongly required `c_S` to be base-field and flagged a false failure;
the corrected check confirms `c_S` is an exact degree-`<k` codeword **over F**.)
The counterexample does *not* descend to a base-field codeword — the closeness
witness is genuinely extension-valued, which is the whole point of an
extension-line obstruction.

## Scope / not covered here
- The **σ=2** family and **σ=3** are now independently brute-checked in
  [`audit_pr103_f1_sigma_two.md`](audit_pr103_f1_sigma_two.md)
  (`verify_audit_pr103_f1_sigma_two.py`): prefix-vanishing
  `e_1=…=e_{σ-1}=0` drops `deg Q_S ≤ k`, `c_S` divides exactly, line agrees on
  `S`, noncontainment holds, and the fixed-tail slope map is injective. The
  growing-σ **slow-slack** asymptotic uses the same mechanism plus a character-sum
  count whose constants remain unaudited.
- The **higher extension degree** `e>=2` claim follows from the same numerator:
  the `binom(p-a+1,2)` slopes lie in the quadratic subfield `B[alpha]`, so only
  the denominator `|F|=p^e` changes; the σ=1 verification (`e=2`) covers the
  mechanism.

## Bottom line
PR #103's headline σ=1 fixed-rate extension-line counterexample is **correct and
independently reproduced**, and it coincides with the monomial-word deep image of
the `notes/x1` bridge. It is a valid prize-facing F1 obstruction (modulo the
σ=2 / slow-slack sub-claims, which were not separately brute-checked).

## Reproducibility
```bash
python3 experimental/scripts/verify_audit_pr103_f1_sigma_one.py
python3 experimental/scripts/verify_audit_pr103_f1_sigma_one.py --json
```
