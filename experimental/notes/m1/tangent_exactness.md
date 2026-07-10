# Tangent-cell exact numerator (rem:capf-tangent-calibration)

**Status:** EXPERIMENTAL / AUDIT
**Verdict:** `NO ISSUE` (confirmation on toys + exact calibration arithmetic)
**Object:** `prop:capf-tangent` / `rem:capf-tangent-calibration` in
`experimental/cap25_cap_v13_raw.tex`
**Evidence type:** `ORACLE_GATED_VS_COMMITTED_VALUE`
**Not a re-proof of deep-MCA; not a deployed-row certificate.**

## Primary finding

On exhaustive `k=1` Reed–Solomon toys in the tangent range `3r ≤ n−k`, the true
maximum number of support-wise MCA-bad finite slopes at agreement `A = n−r` is
exactly

```text
N(A) = n − A + 1 = r + 1
```

matching `prop:capf-tangent`. The constructive lower witness from the proposition
achieves `r+1` on every tested row (including larger `q` where only the
constructive side is run). The remark’s worked integers

```text
n=512, k=256, B_* = floor(17^32 / 2^128) = 6,
R_tan = floor((n−k)/3) = 85,  a_* = 507,  N(506)=7, N(507)=6
```

recompute exactly. Outside the range (`r=2` on `(q,n,k)=(5,4,1)`), the measured
max is `5 > 3`, so the formula is **not** silently valid off-hypothesis — recorded
as a diagnostic, not a claim failure.

## Pinned statements

| label | role |
|-------|------|
| `def:capf-tangent-cell` | `R_tan = floor((n−k)/3)`, paid `r+1` when `r ≤ R_tan` |
| `prop:capf-tangent` | exact max `= r+1` under `3r ≤ n−k` |
| `rem:capf-tangent-calibration` | `N(A)=n−A+1` strictly decreasing; worked `a_*=507` |
| `thm:deep-mca` | supplies the upper bound used in the prop |

## Exhaustive menu (k=1)

| (q,n,r) | A | pred N | true max | match |
|---------|---|--------|----------|-------|
| (5,4,0) | 4 | 1 | 1 | yes |
| (5,4,1) | 3 | 2 | 2 | yes |
| (7,4,0) constructive | 4 | 1 | ≥1 | yes |
| (7,4,1) constructive | 3 | 2 | ≥2 | yes |
| (11,6,1) constructive | 5 | 2 | ≥2 | yes |
| (5,4,2) **outside** | 2 | (3) | **5** | diagnostic |

## Method

- MCA-bad (k=1): slope γ is bad if for some constant codeword the agreement
  support S has `|S|≥A` and `(f1,f2)` is not jointly constant on S.
- Exhaustive over all pairs in `F_q^n` for `q=5,n=4`.
- Constructive lower: place `T` of size `r+1`, set `f2=1_T` spikes and
  `f1=−γ_i` on `T` as in the prop proof.

## Self-red-team

Overclaim risk: “we proved the proposition.” **No** — toys + calibration only;
`k>1` exhaustive census is out of scope. Outside-range max `5>3` would be easy
to bury; it is headlined as diagnostic honesty.

## Reproducibility

```bash
python experimental/scripts/verify_tangent_exactness.py --emit-defaults
python experimental/scripts/verify_tangent_exactness.py --check
python experimental/scripts/verify_tangent_exactness_check.py --check
```
