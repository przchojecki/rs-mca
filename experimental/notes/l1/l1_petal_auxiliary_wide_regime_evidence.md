# L1 Petal Auxiliary Wide-Regime Evidence

- **Status:** EXPERIMENTAL / AUDIT.
- **Agent/model:** Codex, acting autonomously for AllenGrahamHart.
- **Date:** 2026-07-02.
- **DAG target:** `E4 / pma_wide_residual`.

## Purpose

This packet tests the mixed-petal wide-regime evidence question from Fable's
roadmap:

```text
Do the auxiliary pieced-word lists behind the sunflower residual stay small
once the petal count crosses the ordinary Johnson cutoff, or do they show a
new amplification mechanism?
```

This is evidence only.  It does not prove the L1 image-fiber theorem and does
not change any Paper A-D statement.

## Model Tested

The verifier uses the auxiliary incidence isolated in
`experimental/notes/l1/l1_full_list_quotient_proof_program.md` Lemma 2.
For sunflower petals \(T_i\) and missed-core locator \(L_D\), it counts
degree-\(\le d\) polynomials \(W\) satisfying

\[
        W(x)=c_i L_D(x) \quad\text{for many }x\in T_i.
\]

The exact test family is:

```text
field:          F_109
petal domain:  multiplicative subgroup, chunked into consecutive exponent petals
petal size:    ell = sigma + 1 = 3
core defect:   d = 5
threshold:     a = d + ell = 8          (the R_P = 0 proof-program convention)
scalar sets:   c_i = i+1 and c_i = 2^i
petal counts:  M = 3,4,6,9,12 for linear scalars; M = 3,4,6,9 for geometric scalars
```

With this convention the ordinary Johnson cutoff for the auxiliary word is

\[
        M_J=\frac{(d+\ell)^2}{d\ell}=\frac{64}{15}\approx4.27 .
\]

Thus \(M=3,4\) are Johnson-covered and \(M\ge6\) is the intended wide
sub-Johnson side of the toy model.

## Results

The verifier exactly enumerates the auxiliary list by interpolating every
degree-\(d\) support of size \(d+1\), deduplicating polynomials, and checking
the full agreement count.

| schedule | M | petal points | Johnson margin | auxiliary list | max agreement |
|---|---:|---:|---:|---:|---:|
| linear | 3 | 9 | 19 | 0 | 0 |
| linear | 4 | 12 | 4 | 0 | 0 |
| linear | 6 | 18 | -26 | 0 | 0 |
| linear | 9 | 27 | -71 | 177 | 9 |
| linear | 12 | 36 | -116 | 2023 | 11 |
| geometric | 3 | 9 | 19 | 0 | 0 |
| geometric | 4 | 12 | 4 | 0 | 0 |
| geometric | 6 | 18 | -26 | 4 | 8 |
| geometric | 9 | 27 | -71 | 123 | 9 |

The largest row, \(M=12\), checks \(1,947,792\) supports and sees
\(1,538,275\) distinct degree-\(\le5\) candidates before deduplication.  Its
largest witness has agreement profile

```text
3,2,2,1,1,1,1
```

across touched petals, so the population is genuinely mixed-petal rather than
a single full-petal copy.

## Interpretation

The exact toy window gives a mixed answer in the useful sense:

1. The Johnson-covered rows are empty.
2. The wide rows are not empty; the residual mechanism is real.
3. The observed growth is still modest in this exact window.  The verifier
   classifies the packet as

```text
NO_SUPERPOLY_SIGNAL_IN_EXACT_TOY_WINDOW
```

because the largest auxiliary list size is \(2023 < 36^3\).  This is not a
proof of polynomial growth, but it supports the working hypothesis that E4
should be attacked through a correlated-target or descent argument before
revising the L1 image-fiber conjecture.

If later larger-scale runs find super-polynomial growth, this packet should be
used as the baseline for a COUNTEREXAMPLE/S9 update: isolate the first
amplifying sunflower mechanism and add it as a new ledger rather than treating
it as noise.

## Reproducibility

```bash
python3 experimental/scripts/verify_l1_petal_auxiliary_wide_regime.py --emit
python3 experimental/scripts/verify_l1_petal_auxiliary_wide_regime.py --quick
```

The first command regenerates
`experimental/data/certificates/l1-petal-auxiliary-wide-regime/petal_auxiliary_wide_regime.json`.
The quick command skips only the slow \(M=12\) linear row.
