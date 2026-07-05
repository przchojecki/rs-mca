# Growing-Dimensional d=3 Conjecture-F Census

## Claim

The packet records exact aperiodic incidence counts for structured flats and
directed common-normal searches of projective dimension `3` on the requested
`mu_16` toy rows, with dimension `2` retained as the fixed-dimension control.

## Status

EXPERIMENTAL / AUDIT.

## Parameters

- `q_gen = q_line = q_chal` is `97`, `113`, or `241`, row by row.
- Domain `mu_16`.
- Locator degree `j=4`.
- Projective dimensions `2` and `3`.

## Existing Paper Dependency

The packet targets `rem:v13-conjf-open` and `prob:band`, with the dimension-2
comparison tied to `thm:v13-dim2`.

## Proof Idea Or Experiment

For each row, the enumerator constructs coefficient flats, locator-span flats,
and seeded-random flats. It then adds a directed search: each sampled
projective hyperplane is the common normal of four random aperiodic locators,
which biases the census toward high-incidence flats. Evaluation hyperplanes
with normal `(1,a,a^2,a^3,a^4)` for `a in mu_16` are excluded because they are
exactly the non-gcd-trivial flats.

Every locator in `Dloc_j(mu_16)` is checked for membership in each recorded
flat by exact rank or by the recorded hyperplane normal. Periodic supports are
removed by the raw cyclic stabilizer, so the recorded incidence count is
aperiodic.

The checker independently rebuilds the subgroup and all locators, checks each
recorded max witness for gcd-triviality by a polynomial gcd with no domain
root, recomputes the support stabilizer, and recounts the witness incidence
from raw support enumeration. It also verifies the excluded evaluation
hyperplane identity by two routes: support containment through a fixed domain
point and the evaluation-normal dot product.

## Ledger Impact

This gives a finite d=2 to d=3 crossover census for the aperiodic Conjecture-F
object. The structured flats still top out at `48`, but the directed search
finds the meaningful gcd-trivial maxima `116`, `114`, and `114`, all below
the `binom(16,3)=560` envelope. The excluded evaluation hyperplanes contain
`C(15,3) - 7 = 448` aperiodic locators, so gcd-triviality is the visible
mechanism suppressing the admissible incidence.

## Constants

```text
rows: F_97, F_113, F_241 over mu_16
j: 4
structured d=3 max: 48 in each row
directed common-normal samples per row: 60000
directed d=3 maxima: 116, 114, 114
evaluation-hyperplane aperiodic count: C(15,3) - 7 = 448
envelope: binom(16,3) = 560
```

The directed maxima have ratios `29/140`, `57/280`, and `57/280` to the
envelope. The excluded evaluation hyperplanes have ratio `4/5` to the same
envelope. No sampled gcd-trivial flat exceeded `560`.

## Reproducibility

```powershell
py -3.13 experimental/scripts/verify_growing_dim_conjf_d3.py --emit-defaults
py -3.13 experimental/scripts/verify_growing_dim_conjf_d3_check.py --check experimental/data/certificates/growing-dim-conjf-d3/growing_dim_conjf_d3.json
```

## Non-Claims

This is not the growing-dimensional incidence theorem, not a proof or
refutation of Conjecture-F, and not a global maximum over the full
Grassmannian. The directed search is finite evidence over the recorded 60000
samples per row.
