# Image-normalized Sidon/Fourier payment — computational hard attack (W49)

## Status
EXPERIMENTAL. **Rung: MEASURED-SUPPORT** (not PROVED, not COUNTEREXAMPLE).

Hard input **(b)** / C9 core. Weave #527 / #528. No `.tex` edits.

## What the payment asserts (computable form)

At image scale, with folding map \(\Phi:\Omega\to\Sigma\), \(L=|\mathrm{im}\,\Phi|\),
\(\bar N=|\Omega|/L\), fiber sizes \(f_s\), and normalized energy
\(\Delta_s=E(F_s)/f_s^3\), the Sidon-heavy logarithmic moment is

\[
\Gamma^{\mathrm{sid}}_{q,\sigma}
 = L^{-1}\sum_{\Delta_s\le e^{-\sigma N}}\Bigl(\frac{f_s}{\bar N}\Bigr)^q.
\]

Payment (def:sidon-paid-cell / def:sidon-heavy) requires
\(\Gamma^{\mathrm{sid}}_{q,\sigma}\le e^{o(Nq)}\) for every fixed \(\sigma>0\)
and logarithmic \(q\).

**Finite gate used here:** \(\mathrm{rate}=\log(\Gamma^{\mathrm{sid}})/(Nq)\le\tau\)
with \(\tau=0.05\), \(q=2\), and absolute energy cutoff \(\mathrm{thr}=0.5\) as a
stand-in for \(e^{-\sigma N}\). An instance **FAILS** if rate \(>\tau\).

**Deep case not covered by shallow MI/MA:** `thm:unconditional-shallow-mi-ma`
needs \(R\sqrt p=o(N)\) (SFM1). Numerically we flag
`shallow_ratio = R*sqrt(p)/N`; shallow if \(<0.25\), deep if \(\ge1\).
The open regime is deep (and borderline) power-sum charts where SFM1 fails.

## Label honesty (rule 1b)

Live pins in `asymptotic_rs_mca_frontiers.tex` @ `e190193`:

```
1501:\label{def:primitive-first-match-residual}
4837:\tag{9.2}\label{eq:image-ambient-scales}
4866:\label{lem:image-ambient-moment-conversion}
5093:\begin{definition}[Sidon-heavy logarithmic moment]\label{def:sidon-heavy}
5130:\begin{definition}[Sidon moment payment]\label{def:sidon-paid-cell}
5267:\label{thm:unconditional-shallow-mi-ma}
```

**Named packaging:** `ass:image-normalized-sidon-input` appears in B1 notes /
PR #439 (`barN = |Omega^o|/|im Phi|`) but has **no live `\label`** in
`asymptotic_rs_mca_frontiers.tex` at this base. Operational content is
`def:sidon-heavy` + `def:sidon-paid-cell` at image scale
(`eq:image-ambient-scales`).

## Model

- Domain \(T=\{1,\ldots,N\}\subset\mathbb F_p\) (\(p>N\)).
- \(\Omega=\) all (or sampled) \(m\)-subsets of \(T\) — full profile-slice toy
  for a primitive residual (not a full first-match atlas residual).
- \(\Phi(S)=(\sum t,\sum t^2,\ldots,\sum t^R)\in\mathbb F_p^R\).
- Fibers \(F_s=\Phi^{-1}(s)\); Boolean additive energy on incidence vectors
  in \(\{0,1\}^T\).
- Dual energy routes: difference multiset \(\sum r(v)^2\) vs sum-histogram /
  4-tuple (\(a+b=c+d\)).

## Validation (model faithfulness)

Reproduced `image_scale_mi_ma` cert row `sidon_energy_cube3`:

| quantity | value |
|----------|-------|
| \(E(\{0,1\}^3)\) | **216** (both routes) |
| \(\Delta\) | **27/64** |
| cert_match | True |

## Dual routes

- **generator route:** enumerate/sample \(m\)-subsets; power-sum \(\Phi\);
  Counter difference energy; finite rate gate; adversarial sample max-rate.
- **checker route:** sum-histogram energy \(a+b=c+d\); algebraic synthetic
  fail recompute; live instance largest-fiber dual energy.

## Falsifiability exhibit

Synthetic heavy low-energy fiber (\(N=12\), \(f/\bar N\approx e^{0.25N}\),
\(L=10\)):

```text
Gsid = 40.0
rate ≈ 0.1537 > tau=0.05
payment_holds = False
```

So the gate **can fail**. Field sweep did not hit it.

## Sweep (cert-sourced)

```text
n_sweep = 21
n_payment_pass = 21
n_payment_fail = 0
n_deep = 5  (deep_fail = 0)
n_shallow = 1 (shallow_fail = 0)
max_rate ≈ 0.01390
min_margin_vs_tau ≈ 0.03610
energy routes agree on all 21 rows
adversarial any_counterexample = false
adv_best_rate ≈ -0.0426  (Gsid < 1)
```

Tightest observed rate ~0.014 on \((p,N,m,R)=(17,8,4,1)\) (borderline SFM1).
Safety margin vs \(\tau\) is positive and did not collapse in the deep toys;
rates stay \(O(10^{-2})\) or negative (Gsid≤1).

## Verdict / rung

**MEASURED-SUPPORT.** Payment holds across the full finite sweep including
deep SFM1-violation toys; adversarial sampling found no field counterexample.
This is evidence **for** the assumption at toy scale, **not** a proof of
`ass:image-normalized-sidon-input` / C9 at deployed parameters.

Secondary reduction (not a theorem): controlling
\(\max_s(f_s/\bar N)\) among Boolean-low-energy fibers bounds the finite Gsid gate
on power-sum charts.

## Nonclaims

- Not PROVED at any deployed or asymptotic row.
- Finite \(\tau\)-gate ≠ asymptotic \(e^{o(Nq)}\).
- Not full Weil / (PF)/(MA) Fourier payment.
- Full \(m\)-subset slice ≠ atlas residual \(\Omega^\circ\).

## Reproducibility

```text
py -3.13 experimental/scripts/verify_image_normalized_sidon_attack.py --emit
py -3.13 experimental/scripts/verify_image_normalized_sidon_attack.py --check
py -3.13 experimental/scripts/verify_image_normalized_sidon_attack_check.py --check
payload_sha256: 594159a6711cf186696988afb19d67c4feb5850c23ca76d9e1602c5c7e245b99
```
