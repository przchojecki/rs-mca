# Mu2 Fold-Defect Injection Ledger

## Claim

The packet measures the finite support-level map from destroyed aperiodic
parent supports under the `mu_2` fold `x -> x^2` to the rung-below doubleton
child support plus a complete signed singleton defect certificate.

## Status

EXPERIMENTAL / LEDGER.

## Parameters

- `q_gen = q_line = q_chal = p` row by row.
- Parent domains are dyadic multiplicative subgroups `mu_n`.
- Rows are `(F_5,mu_4,j=2)`, `(F_17,mu_8,j=3)`,
  `(F_17,mu_16,j=4)`, and `(F_97,mu_32,j=5)`.
- Only aperiodic supports with raw cyclic stabilizer `c(S)=1` are counted.

## Existing Paper Dependency

This is a finite Route-gamma stability ledger tied to `thm:fiber-descent` and
`lem:v13-quot-pullback`. The strategy note asks that "witnesses destroyed by
folding must be shown to inject, with controlled multiplicity, into a
rung-below problem via their folded multiset plus a defect certificate."

The measured map follows that object: the child is the folded image restricted
to doubleton fibers, and the defect certificate records every singleton
residue together with its sign, i.e. which of the two parent fiber elements is
present.

The certificate records the support-level child target as `n -> n/2`. Because
the destroyed parent supports contain singleton defects, the child degree is
the number of doubleton fibers in the parent support rather than a fixed
`k/2` or `ceil(a/2)` row parameter. Thus this packet measures the support
injection needed by the rung-below route; it does not instantiate a full
received-word transfer row.

## Proof Idea Or Experiment

For each `j`-subset support, the scanner computes its raw cyclic stabilizer.
Aperiodic supports are folded by the index map `i -> i mod n/2`, equivalent to
`x -> x^2` on `mu_n`. A support is destroyed when some folded fiber has
multiplicity one.

The complete key is:

```text
(child support from doubleton fibers, signed singleton defect certificate)
```

The scanner groups destroyed parent supports by that complete key, records the
injection multiplicity histogram, the singleton-count defect-complexity
histogram, and a child wellformedness sanity check. The wellformedness check
only verifies that the doubleton child is a set of distinct in-range folded
indices; it is not a rung-`(n/2)` split-witness validity claim. The scanner also
records a count-only diagnostic that drops signs; the growing `4/8/16/32`
count-only multiplicities come only from sign choices and are not the
Route-gamma risk.

The checker independently rebuilds the fold map from raw set arithmetic,
recomputes child supports and complete defects, rechecks child wellformedness,
and re-derives both the complete-key and count-only histograms.

## Ledger Impact

The substantive finite finding is that the complete-defect key is injective on
every recorded row: maximum complete-defect multiplicity is `1` throughout.
This is expected for the recorded key, because the key contains enough
information to reconstruct the parent support from the child doubletons and the
signed singleton defects.

The defect complexity is controlled by the number of destroyed singleton
fibers: it is at most `j`, with the exact singleton-count histograms printed
below. The count-only key still shows multiplicities `4`, `8`, `16`, and `32`,
but those are exactly the dropped singleton-sign choices and are retained only
as a diagnostic. Thus the earlier apparent growth is pure singleton-sign
degeneracy, not growth of the complete-defect key.

The child wellformedness rate is `1/1` throughout, but this is only a structural
sanity check on the generated child index set and is not used as evidence for a
fixed-rung transfer statement.

## Constants

```text
row              destroyed  complete buckets  max complete  child wellformed  count-only max
F_5,mu_4,j=2     4          4                 1             1/1               4
F_17,mu_8,j=3    56         56                1             1/1               8
F_17,mu_16,j=4   1792       1792              1             1/1               16
F_97,mu_32,j=5   201376     201376            1             1/1               32
```

Defect-complexity histogram by singleton count:

```text
F_5,mu_4,j=2     2:4
F_17,mu_8,j=3    1:24, 3:32
F_17,mu_16,j=4   2:672, 4:1120
F_97,mu_32,j=5   1:3360, 3:58240, 5:139776
```

## Reproducibility

```powershell
py -3.13 experimental/scripts/verify_gamma_fold_defect_injection.py --emit-defaults
py -3.13 experimental/scripts/verify_gamma_fold_defect_injection.py --check experimental/data/certificates/gamma-fold-defect/gamma_fold_defect_injection.json
py -3.13 experimental/scripts/verify_gamma_fold_defect_injection_check.py --check experimental/data/certificates/gamma-fold-defect/gamma_fold_defect_injection.json
```

## Non-Claims

This is not a Route-gamma transfer theorem, not an asymptotic
bounded-multiplicity result, and not a deployed parameter statement. It does
not instantiate the full `(n,k,a) -> (n/2,k/2,ceil(a/2))` received-word
transfer row, and does not prove that the complete-defect injection remains
multiplicity-one outside the recorded toy range. The fixed-rung child
split-witness validity question remains open; checking that stronger
received-word transfer row is the next step.
