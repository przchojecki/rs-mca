# sigma_C Sub-Capacity k=1 Failure Family

Status: COUNTEREXAMPLE / PROVED for the listed finite enumerations; CONJECTURAL
for the refined empirical law.

Date: 2026-07-04.

## Claim

The empirical dichotomy

```text
2r > m and r <= m-1  =>  sigma_C(r) = q_line
```

is false for all smooth-domain Reed-Solomon rows under the finite-slope
convention used by `tex/towards-prize.tex`.

The failure is not isolated.  Three exact `k=1` sub-capacity rows now give
intermediate values:

```text
q_gen  q_line  n  k  m=n-k  r  band check          sigma_C
5      5       4  1  3      2  2r=4>3, r<=m-1    3
13     13      4  1  3      2  2r=4>3, r<=m-1    3
7      7       6  1  5      3  2r=6>5, r<=m-1    4
```

All three rows satisfy

```text
r < sigma_C(r) < q_line.
```

Thus sub-capacity rows can exceed the tangent floor without immediately
saturating every finite slope.

## Refined Empirical Law

The original empirical law is false as stated.  The surviving pattern in the
tested data is:

```text
sub-capacity band and k >= 2  =>  sigma_C(r) = q_line.
```

This is only an empirical/conjectural pattern.  It is consistent with the
`k=3` control row `(q,n,k,r)=(7,6,3,2)`, which gives `sigma_C=7=q_line`, and
with the committed `k>=2` sigma_C census tables.  The open question is whether
`k=1` is the exact boundary for intermediate sub-capacity values, or whether
some untested `k=2` row also fails to saturate.

## Endpoint Conventions

The packet uses:

```text
r = floor(delta*n)
finite slopes only
slope denominator = q_line
q_gen = q_line for these toy prime-field rows
q_chal = not used
domain = multiplicative subgroup of F_q^* of order n
```

No extension-field or challenge-field soundness division is claimed.

## Reproducibility

The original one-row certificate is still present:

```text
experimental/data/certificates/sigma-c-sparse-census/sigma_c_subcapacity_dichotomy_counterexample_q5.json
```

The strengthened family certificate is:

```text
experimental/data/certificates/sigma-c-sparse-census/sigma_c_subcapacity_dichotomy_k1_family.json
```

Replay command for the family packet:

```sh
python experimental/scripts/verify_sigma_c_sparse_census.py \
  --row 5,4,1,1,1 \
  --row 5,4,1,2,3 \
  --row 13,4,1,1,1 \
  --row 13,4,1,2,3 \
  --row 7,6,1,2,2 \
  --row 7,6,1,3,4 \
  --check experimental/data/certificates/sigma-c-sparse-census/sigma_c_subcapacity_dichotomy_k1_family.json
```

Observed output after rebasing onto current `origin/main`:

```text
sigma_C sparse census verifier
  object: sparse support-wise MCA bad-slope count
  theorem/problem: towards-prize prob:mutual / thm:sparsify
  status: AUDIT; finite rows PROVED-by-enumeration
  conventions: finite slopes only; maximal S_z failure check; no Mobius quotient
  row q=5 n=4 k=1 r=1: sigma_C=1 pairs=97 bad_pairs=80
  row q=5 n=4 k=1 r=2: sigma_C=3 pairs=3553 bad_pairs=3440
  row q=13 n=4 k=1 r=1: sigma_C=1 pairs=673 bad_pairs=624
  row q=13 n=4 k=1 r=2: sigma_C=3 pairs=170017 bad_pairs=169104
  row q=7 n=6 k=1 r=2: sigma_C=2 pairs=34849 bad_pairs=34272
  row q=7 n=6 k=1 r=3: sigma_C=4 pairs=2246689 bad_pairs=2241792
RESULT: PASS
```

The guard rows `(5,4,1,r=1)`, `(13,4,1,r=1)`, and `(7,6,1,r=2)` are in the
trivial regime `2r <= m` and recover `sigma_C=r`.

## Witness Sample

One extremal pair for the first band row is recorded in the certificate as:

```text
eps1 = [0, 1, 0, 0]
eps2 = [1, 2, 0, 0]
bad slopes = [0, 2, 4]
```

The family certificate records the close codeword index, distance, and maximal
witness set for every bad slope in each sampled extremal pair.

## Ledger Impact

This is a finite toy-row counterexample family to the strongest
sub-capacity immediate-saturation heuristic.  It does not refute
`thm:sparsify`, does not change any deployed-row or prize-band claim, and does
not supply an asymptotic obstruction.

## Related Work

Open PR #273 ("MCA-vs-CA sparse-layer gap structure") studies the general-pair
containment structure of the mutual-only layer and positions itself as the
structure complement to this census lane; its rows ((17,8,4,r=3) and
(97,16,8,r=5)) are all `k >= 2` and do not overlap the `k=1` family here.  Its
(17,8,4,r=3) all-slopes-bad example is consistent with the refined `k >= 2`
saturation law recorded above.

## Non-Claims

- No theorem proving the refined `k>=2` law is claimed.
- No claim is made about GF(9), extension fields, or deployed rows.
- No GPU result or histogram upgrade is included.
- No upper bound on `sigma_C` outside the listed rows is claimed.

## Scope And Omitted Rows

A fuller dichotomy census was planned for this lane, including GF(9)
extension-field rows and higher-cost Hankel/parity-check rows.  This note
instead packages the first exact counterexample and two additional exact
`k=1` family rows because they refute the headline dichotomy and sharpen the
surviving empirical law.

The remaining rows are not silently claimed:

- GF(9) support is not present in the current repo verifier.
- The higher-cost prime rows requiring Hankel/parity-check enumeration are not
  included here.
- No large-scale census or histogram upgrade is claimed here.

Those rows remain future work for a separate Hankel/parity-check census
branch.
