# KoalaBear BCHKS25 JMCA parameter squeeze v2

Status: `CONDITIONAL_ON_PARAMETRIC_LIST_MCA_LEMMA_V1`

This appendix records the stronger arithmetic certificate obtained by keeping
the BCHKS25/Haboeck interpolation parameters symbolic and then optimizing the
integer ceiling cell. It is not a direct invocation of BCHKS25 Theorem 4.6 as
displayed.

The bridge theorem is stated in:

```text
experimental/notes/audits/koalabear_bchks25_parametric_list_mca_lemma_v1.md
```

The bridge lemma cites BCHKS25 Theorem 4.6, pp. 27-28, for the list-MCA
predicate; BCHKS25 Section 3.2, pp. 23-25, for the Hensel/useful-factor
sublemma; and the paragraph after Theorem 4.6 on p. 28 for the list-MCA
all-useful-factor bookkeeping. The pinned source is:

```text
PDF: https://www.math.toronto.edu/swastik/rs-proximity-gaps-2025.pdf
DOI: https://dl.acm.org/doi/10.1145/3798129.3800827
PDF SHA256: 4ADDED3E55B83C15FCC8A698FB57E137F5BD83E79EA25CE79382817C1AD26A46
```

The PR headline remains the displayed-Theorem-4.6 edge
`delta <= 604085/2097152`. This appendix becomes a safe certificate only if the
new bridge lemma is accepted in review.

## Certificate

```text
r = 611983
n = 2097152
A = n-r = 1485169
delta = 611983 / 2097152 ~= 0.2918162346
```

Use multiplicity and degree parameters

```text
m = 119
epsilon = 2^-64
D_X = 176735110 + epsilon
D_Y = 168 + epsilon
D_Z = 27542 + epsilon
```

Thus

```text
ceil(D_X) = 176735111
ceil(D_Y) = 169
ceil(D_Z) = 27543
```

## Exact checks

Root/agreement condition:

```text
m*A - D_X = 1 - 2^-64 > 0.
```

Interpolation system:

```text
n_vars = sum_{j=0}^{168} (ceil(D_X) - k_BCHKS*j)(ceil(D_Z)-j)
       = 411830702773581

n_eqs = n * sum_{s=0}^{118} (ceil(D_Z)-s)(m-s)
      = 411830698639360

n_vars - n_eqs = 4134221 > 0.
```

Bridge-lemma exceptional-slope bound:

```text
R = 2*D_X*D_Y^2*D_Z + (r+1)*D_Y
ceil(R) = 274768452484563073
budget  = 274980728111395087
margin  = 212275626832014
```

Therefore, conditional on the parametric list-MCA bridge lemma, this would
certify

```text
delta <= 611983 / 2097152 ~= 0.2918162346
A >= 1485169.
```

## Optimized integer-ceiling search

For fixed monomial ceilings `U,V,W`, the smallest possible integer ceiling of
`R` is obtained by taking

```text
D_X = U-1+epsilon,
D_Y = V-1+epsilon,
D_Z = W-1+epsilon,
epsilon -> 0+.
```

The verifier exhausts this optimized family under the theorem admissibility
constraints. The best cell at `r=611983` is exactly

```text
m = 119
U = 176735111
V = 169
W = 27543
ceil(R) = 274768452484563073.
```

The next grid point has no budget-clearing cell in the same optimized family:

```text
r = 611984
result = no candidate for m <= 602.
```

The bound `m <= 602` is exhaustive for this budget because `V >= m`, `W >= V`,
and `U > k(V-1)` imply the lower bound `R >= 2*k*(m-1)^4`, which already
exceeds the budget for `m >= 603`.

## Files

```text
experimental/scripts/certify_koalabear_bchks25_jmca_bounds_v1.py
experimental/data/certificates/koalabear-bchks25-jmca-param-squeeze-v2/certificate.json
experimental/data/certificates/koalabear-bchks25-jmca-bounds-v1/run_output.json
experimental/notes/audits/koalabear_bchks25_parametric_list_mca_lemma_v1.md
```

## Validation

```text
python -m py_compile experimental/scripts/certify_koalabear_bchks25_jmca_bounds_v1.py
python experimental/scripts/certify_koalabear_bchks25_jmca_bounds_v1.py --write
python experimental/scripts/certify_koalabear_bchks25_jmca_bounds_v1.py --check
python experimental/scripts/certify_koalabear_bchks25_jmca_bounds_v1.py --squeeze
python -m json.tool experimental/data/certificates/koalabear-bchks25-jmca-param-squeeze-v2/certificate.json
python -m json.tool experimental/data/certificates/koalabear-bchks25-jmca-bounds-v1/run_output.json
git diff --check
```
