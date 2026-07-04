# KoalaBear BCHKS25 JMCA bounds v1 report

## External source

- On Proximity Gaps for Reed-Solomon Codes.
- PDF: https://www.math.toronto.edu/swastik/rs-proximity-gaps-2025.pdf.
- DOI: https://dl.acm.org/doi/10.1145/3798129.3800827.
- PDF SHA256: `4ADDED3E55B83C15FCC8A698FB57E137F5BD83E79EA25CE79382817C1AD26A46`.
- Headline import: Theorem 4.6, List correlated agreement up to Johnson bound (pp. 27-28).
- Appendix dependency: Section 3.2 improved-bound proof, especially the unnumbered Hensel/useful-factor step beginning with |S_{x0,R,H}| > 2 D_X D_Y^(R) D_Y^(H) D_Z^(R), and the Theorem 4.6 paragraph generalizing that all-useful-factor bookkeeping to list correlated agreement. (Section 3.2, pp. 23-25; Theorem 4.6 proof paragraph, p. 28).

## Headline certificate

Status: `CONDITIONAL_ON_BCHKS25_THEOREM_4_6_AS_STATED`

- Exact reduced-rate endpoint: `r=604085`, `A=1493067`, `delta=604085/2097152`.
- Displayed-Theorem-4.6 bound: `ceil_N_JMCA=266853183557299442`.
- Budget: `274980728111395087`.
- Margin: `8127544554095645`.
- Next grid point under displayed formula: `r=604086`, `m=147`, `ceil_N_JMCA=276085988421839588`, which exceeds budget.

## Conservative endpoint

- With `rho=1/2`: `r=604084`, `A=1493068`, `ceil_N_JMCA=266852801820849253`.

## Parametric appendix

Status: `CONDITIONAL_ON_PARAMETRIC_LIST_MCA_LEMMA_V1`.

- Radius: `r=611983`, `A=1485169`, `delta=611983/2097152`.
- Parameters: `m=119`, `D_X=176735110 + 1/18446744073709551616`, `D_Y=168 + 1/18446744073709551616`, `D_Z=27542 + 1/18446744073709551616`.
- Interpolation slack: `4134221`.
- Root slack: `18446744073709551615/18446744073709551616`.
- `ceil(R)=274768452484563073` with margin `212275626832014`.
- Next grid search: `r=611984` has no budget-clearing integer-ceiling cell in the stated optimized family: `True`.

## Non-claims

The PR headline does not depend on the parametric appendix. The appendix becomes a deployed safe certificate only if reviewers accept the new parametric list-MCA bridge lemma.
