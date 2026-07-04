# sigma_C Sparse Census Certificate

Status: EXPERIMENTAL / PROVED-by-enumeration for the finite rows in the JSON.

This packet records tiny prime-field census rows for the sparse mutual layer
from `tex/towards-prize.tex` (`prob:mutual`, `thm:sparsify`).  It is a CPU
exact verifier, not a GPU search result.

The checker counts finite slopes only, with denominator `q_line`.  For every
candidate close codeword `z`, the failure test is performed on the maximal
witness set

```text
S_z = {i in D : eps1_i + gamma eps2_i = z_i}.
```

No symmetry quotient is used in this certificate.  Optimized census searches
that feed this checker must preserve the finite-slope convention; in
particular, full Mobius reductions are out of scope because they can send a
finite slope to the projective point at infinity.

## Reproduction

```sh
python3 experimental/scripts/verify_sigma_c_sparse_census.py \
  --check experimental/data/certificates/sigma-c-sparse-census/sigma_c_sparse_census_toy_rows.json
```

The extended row packet is checked with its explicit row selector:

```sh
python3 experimental/scripts/verify_sigma_c_sparse_census.py \
  --row 7,6,3,2,7 \
  --check experimental/data/certificates/sigma-c-sparse-census/sigma_c_sparse_census_extended_rows.json
```

To regenerate:

```sh
python3 experimental/scripts/verify_sigma_c_sparse_census.py \
  --write experimental/data/certificates/sigma-c-sparse-census/sigma_c_sparse_census_toy_rows.json
```

```sh
python3 experimental/scripts/verify_sigma_c_sparse_census.py \
  --row 7,6,3,2,7 \
  --write experimental/data/certificates/sigma-c-sparse-census/sigma_c_sparse_census_extended_rows.json
```

The script uses only the Python standard library.  It brute-forces the listed
tiny rows and is intended as the exact CPU verification rung for later GPU
candidate searches.
