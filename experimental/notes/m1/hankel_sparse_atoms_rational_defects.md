# Hankel Sparse Atoms As Rational Defects

Status: PROVED.

Source DAG node: `hankel_sparse_atoms_as_rational_defects`.

## Statement

For a Hankel state, sparse annihilator atoms are small defect sets of rational
approximants to the spectral weight. In the RS-dual normal form,

```text
Ann_E(P) = GRS_{n_E-j-1}(E, lambda) + omega RS_t(E).
```

Atoms are defect sets for rational approximants `-lambda g/h` to `omega`.
Distinct-closure atoms satisfy

```text
|T_1 union T_2| >= j - t + 2.
```

Atoms coming from the same rational approximant saturate to one closure by the
punctured-GRS/MDS collapse on the defect block. The description is hereditary
under the stability operation `omega -> omega ell_A`.

## Proof

The RS-dual identity gives every sparse annihilator atom as the set where a
rational approximant `-lambda g/h` fails to match the spectral weight `omega`.
For two distinct approximants `g_1/h_1` and `g_2/h_2`, eliminate `omega` by
forming

```text
F = g_1 h_2 - g_2 h_1.
```

Outside `T_1 union T_2`, both approximants agree with `omega`, so `F` vanishes.
The degree bound is

```text
deg F <= n_E - j + t - 3.
```

A nonzero polynomial cannot vanish on too many domain points. Therefore the
union of the two defect sets has the required lower bound. In the same-
approximant case, the atoms are rescalings of a Reed-Solomon segment on the
defect block, and the punctured-GRS/MDS property forces one saturated closure
rather than many independent closures.

Multiplying the spectral weight by a locator factor `ell_A` preserves the same
rational-defect description after the corresponding defect-set update, giving
the hereditary form consumed by the rank-profile entropy packet.

## Non-Claims

This packet identifies and bounds Hankel sparse atoms in the rational-defect
normal form. It does not by itself prove the full rank-profile dichotomy or
the final termination theorem.

## Replay

```bash
python3 experimental/scripts/verify_hankel_sparse_atoms_rational_defects.py --emit
python3 experimental/scripts/verify_hankel_sparse_atoms_rational_defects.py \
  --check experimental/data/certificates/hankel-sparse-atoms-rational-defects/hankel_sparse_atoms_rational_defects.json
```
