# Annulus MCA-from-CA finite check

## Claim

This packet records two finite A.3 findings for small Reed-Solomon rows:

1. The stated A.3 side condition `n-2r > sqrt((k-1)n)` is unsatisfiable in the
   strict annulus `2r > n-k`.
2. Under the natural replacement reading that applies the Johnson list bound at
   explanation agreement `a=n-r`, the raw pair-explanation cluster size is
   insufficient to bound the MCA-bad slopes on every recorded toy row.

The packet includes a deep-regime oracle gate before the annulus rows. It is
not a proof of an annulus MCA-from-CA theorem and does not resolve `prob:band`.

## Status

EXPERIMENTAL.

## Headline finding

The literal A.3 cluster condition has no strict-annulus instances. Indeed,

```text
2r > n-k  =>  n-2r <= k-1,
and for k<n, k-1 < sqrt((k-1)n).
```

Therefore `n-2r > sqrt((k-1)n)` cannot hold in the annulus `2r > n-k`. The
finite check uses the natural `a=n-r` Johnson reading instead. On the recorded
rows, `a^2 > (k-1)n` holds and the cluster-size Johnson bound passes.

## Parameters

The checked annulus rows are:

| q | n | k | r | a=n-r | strict annulus | n-2r <= k-1 | a-Johnson | shape result |
|---:|---:|---:|---:|---:|:---:|:---:|:---:|:---:|
| 11 | 10 | 3 | 4 | 6 | yes | yes | yes | pass |
| 13 | 12 | 5 | 4 | 8 | yes | yes | yes | gap |
| 17 | 16 | 7 | 5 | 11 | yes | yes | yes | pass |
| 31 | 10 | 3 | 4 | 6 | yes | yes | yes | pass |

All listed rows satisfy the agreement check `a^2 > kn`, the below-boundary
check `2a < n+k`, and the Johnson-list check at explanation agreement `a`,
namely `a^2 > (k-1)n`.

## Existing paper dependency

- `def:ca` and `def:mca` define the CA/MCA bad-slope predicates and the
  `eca`/`emca` normalizations.
- `thm:deep-mca` supplies the `r+1` deep-regime oracle gate.
- `thm:johnson-list` supplies the finite explanation-cluster bound checked at
  agreement `a=n-r`.
- `thm:mca-from-ca`, `rem:half-scope`, and `cor:band-reduction` identify the
  below-half-distance explanation-cluster issue.
- `prop:v13-tangent` supplies the tangent-cell oracle witness attaining
  `r+1` bad slopes.

## Proof idea or experiment

The enumerator builds exact prime-field RS analyzers, counts finite slopes, and
records:

```text
# MCA-bad slopes, # CA-bad slopes, |cluster|,
Johnson bound at a=n-r, cluster <= Johnson, and the naive shape inequality.
```

The independent checker replays the certificate with direct agreement-set
enumeration and interpolation, and uses a specialized degree-zero replay for
the tiny exhaustive oracle row. No GPU, floats, or numerical approximations are
used.

## Oracle gate

| row | result |
|---|---|
| `F_5, n=4, k=1, r=1` | exhaustive `5^8` pair replay gives max MCA = 2 and max CA = 2, matching `r+1` |
| `F_13, n=12, k=6, r=2` | tangent-cell witness gives MCA = 3 and CA = 3, matching `r+1` |

## Finite insufficiency witness

Under the natural `a=n-r` reading, the row `(q,n,k,r,a)=(13,12,5,4,8)` has a
deterministic seeded close sample with:

```text
MCA slopes = [0, 2, 6, 11, 12]
CA slopes = []
|cluster| = 1
Johnson bound at a=n-r = 3
naive left count = 5
naive right count = 0 + 1*4 = 4
```

This is evidence that the naive `|cluster|*r/q` correction is insufficient
under the natural reading. It is not presented as a failure of A.3 as literally
written, because the literal A.3 annulus side condition has no valid instances.
The constructive takeaway is that A.3 needs either a corrected cluster notion
that charges off-explanation-line MCA witnesses, or a different regime.

## Ledger impact

This packet isolates the A.3 annulus MCA-from-CA shape as a finite test object
separate from the split-locator, prefix-fiber, and incidence packets. The
strongest contribution is the explicit correction to the stated A.3 side
condition; the finite row then shows that the simplest raw-cluster correction
is still too weak under the natural `a=n-r` interpretation.

## Constants

All constants are exact integers or `Fraction` values in the JSON certificate.
The payload hash is:

```text
2f0f1263f9a55e87cb516fe101cbd11e5fb2471d514fb568d3de3133dac878fd
```

## Deviations

The strategy condition `n-2r > sqrt((k-1)n)` cannot hold together with the
strict annulus condition `2r > n-k` when `k<n`. The packet records this as a
positive finding and applies the Johnson bound at explanation agreement
`a=n-r`.

The annulus rows are constructed and deterministically sampled finite pairs,
not exhaustive `q^(2n)` pair censuses. The exhaustive replay is restricted to
the tiny deep-regime oracle row.

## Reproducibility

```text
py -3.13 experimental/scripts/verify_annulus_mca_from_ca.py --emit-defaults
py -3.13 experimental/scripts/verify_annulus_mca_from_ca.py --check experimental/data/certificates/annulus-mca-from-ca/annulus_mca_from_ca.json
py -3.13 experimental/scripts/verify_annulus_mca_from_ca_check.py --check experimental/data/certificates/annulus-mca-from-ca/annulus_mca_from_ca.json
```
