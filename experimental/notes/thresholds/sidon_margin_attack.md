# Sidon payment thin-margin attack (W50-M1)

## Status
EXPERIMENTAL. **Rung: MEASURED-ROBUST.**

Hard input (b) / C9. Reuses W49 model. Weave W49 / #527.

## Phase 0 — model re-validation
Reproduced `image_scale_mi_ma` cert row `sidon_energy_cube3`:

```text
energy = 216 (diff-Counter and 4-tuple/sum-histogram)
Delta = 27/64
cert_match = True
```

## Dual routes
- **generator:** zoom grid around W49 thin locus (17,8,4,1); adversarial AP/sum/heavy-fiber Ω; scale-in-p families; margin=τ−rate
- **checker:** sum-histogram energy; algebraic margin recompute; extremal re-eval; trend recompute

## Zoom (80 configs)
```text
zoom_fail = 0/80
min_margin_zoom ≈ 0.03610457  (same thin locus as W49)
max_rate_zoom ≈ 0.01389543
extremal: (p,N,m,R)=(17,8,4,1)
```

## Adversarial
At W49 locus and extremal locus: AP-biased, sum-extremes, heavy-fiber collapse, random samples.

```text
any_counterexample = false
min_margin_adv ≈ 0.03610457
```

No construction crossed rate>τ=0.05.

## Scale-in-p trends
| family | trend |
|--------|-------|
| N=8,m=4,R=1 vary p | **BOUNDED** |
| density≈1/2, R=1 grow N | **BOUNDED** |

Margin does not shrink toward 0 along these families in the scanned range.

## Verdict
**MEASURED-ROBUST.** Thin margin persists under zoom + adversarial max-energy constructions + p-scale; no finite CE; no negative trend. Evidence *for* payment robustness at toy scale — not a proof of C9.

## Nonclaims
- Incomplete adversarial search ≠ proof.
- Finite τ-gate ≠ asymptotic e^{o(Nq)}.

## Reproducibility
```text
py -3.13 experimental/scripts/verify_sidon_margin_attack.py --check
payload_sha256: b3295c93230eae29a7ba97b9d204a80cba98078c6f28631c1d8d514cf78cad02
```
