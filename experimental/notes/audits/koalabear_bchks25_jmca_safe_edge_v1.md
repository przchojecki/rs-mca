# KoalaBear BCHKS25 displayed-Theorem-4.6 JMCA safe edge v1

Status: `CONDITIONAL_ON_BCHKS25_THEOREM_4_6_AS_STATED`

This is the PR headline certificate. It imports BCHKS25 Theorem 4.6 exactly as
printed and does not use the parameter-squeeze appendix.

## Imported source

```text
Ben-Sasson, Carmon, Habock, Kopparty, Saraf,
On Proximity Gaps for Reed-Solomon Codes.
PDF: https://www.math.toronto.edu/swastik/rs-proximity-gaps-2025.pdf
DOI: https://dl.acm.org/doi/10.1145/3798129.3800827
PDF date: 2025-11-11
Accessed: 2026-07-04
PDF SHA256: 4ADDED3E55B83C15FCC8A698FB57E137F5BD83E79EA25CE79382817C1AD26A46
Imported statement: Theorem 4.6, List correlated agreement up to Johnson bound,
pp. 27-28.
```

## Deployed row

```text
p = 2^31 - 2^24 + 1
q_line = p^6
n = 2^21
K = 2^20                         # deployed degree-<K dimension
k_BCHKS = K - 1 = 2^20 - 1        # BCHKS degree parameter, dimension k+1
budget = floor((p^6 - 1) / 2^128)
       = 274980728111395087
```

The exact reduced rate for the displayed theorem is

```text
rho = k_BCHKS / n = (2^20 - 1) / 2^21.
```

## Displayed Theorem 4.6 arithmetic

For `gamma = r/n`, `M=1`, and `t=m+1/2`, the displayed bound is

```text
N_JMCA = ((2t^5 + 3t gamma rho)/(3 rho^(3/2))) n + t/sqrt(rho),
m = max(ceil(sqrt(rho)/(1 - sqrt(rho) - gamma)), 3).
```

The verifier rewrites this as

```text
N_JMCA = X / sqrt(rho),
X = 2t^5 n/(3 rho) + t(r+1),
```

and compares by exact integer squaring. No floating point arithmetic is used.

## Exact reduced-rate endpoint

```text
r = 604085
A = n-r = 1493067
m = 146
ceil(N_JMCA) = 266853183557299442
budget       = 274980728111395087
margin       = 8127544554095645
```

Therefore the displayed imported theorem certifies

```text
delta <= 604085 / 2097152 ~= 0.2880501747
A >= 1493067
```

under status `CONDITIONAL_ON_BCHKS25_THEOREM_4_6_AS_STATED`.

The next grid point fails under the displayed bound:

```text
r = 604086
A = 1493066
m = 147
ceil(N_JMCA) = 276085988421839588 > budget.
```

## Conservative `rho = 1/2` endpoint

For consumers that do not want the degree-parameter off-by-one convention:

```text
r = 604084
A = 1493068
m = 146
ceil(N_JMCA) = 266852801820849253 < budget.
```

The next grid point fails under the displayed `rho=1/2` bound:

```text
r = 604085
m = 147
ceil(N_JMCA) = 276085593477759245 > budget.
```

## Files

```text
experimental/scripts/certify_koalabear_bchks25_jmca_bounds_v1.py
experimental/data/certificates/koalabear-bchks25-jmca-safe-edge-v1/certificate.json
experimental/data/certificates/koalabear-bchks25-jmca-bounds-v1/run_output.json
experimental/notes/certificate_scanner/outputs/koalabear_bchks25_jmca_bounds_v1_report.md
```

## Validation

```text
python -m py_compile experimental/scripts/certify_koalabear_bchks25_jmca_bounds_v1.py
python experimental/scripts/certify_koalabear_bchks25_jmca_bounds_v1.py --write
python experimental/scripts/certify_koalabear_bchks25_jmca_bounds_v1.py --check
python experimental/scripts/certify_koalabear_bchks25_jmca_bounds_v1.py --safe-edge
python -m json.tool experimental/data/certificates/koalabear-bchks25-jmca-safe-edge-v1/certificate.json
python -m json.tool experimental/data/certificates/koalabear-bchks25-jmca-bounds-v1/run_output.json
git diff --check
```
