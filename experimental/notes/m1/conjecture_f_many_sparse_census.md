# Conjecture F Many-Sparse Census

- **Status:** EXPERIMENTAL / exact toy evidence.
- **Agent:** Codex acting autonomously for Allen Graham Hart.
- **Roadmap link:** Fable evidence task `E9` / `QF.8`
  (`f_many_sparse_structure`).
- **Verifier:** `experimental/scripts/verify_conjecture_f_many_sparse_census.py`.
- **Artifact:** `experimental/data/certificates/conjecture-f-many-sparse-census/conjecture_f_many_sparse_census.json`.

This packet performs the pre-registered many-sparse toy census for Conjecture
F.  It does not prove Conjecture F.  Its purpose is to decide which version of
the residue statement is still plausible before the proof program invests in a
global induction.

## Object

Let `K = F_17` and `H = F_17^*`, so `|H| = n = 16`.  For `j in {3,4}`, the
verifier enumerates every codimension-one projective flat

```text
P(ker a) <= P(K[X]_{<=j}).
```

Equivalently, it enumerates every projective normal `a` in the dual
coefficient space.  For a support `S subset H`, `|S|=w`, the flat has a
support-`w` sparse dual word precisely when

```text
a in span{ (1,x,x^2,...,x^j) : x in S }.
```

The verifier counts these incidences for `w = 1,2,3` and assigns each flat to
the first applicable bucket:

```text
common_root       support-1 sparse dual word
twin              no support-1 word, but a support-2 word
sparse3_only      no support-1/2 word, but a support-3 word
dual_distance_ge_4 no support <= 3 word
```

The first two buckets are the expected common-divisor/twin structures.  The
third bucket is the sparse-dependence descent branch, not a paid quotient or
tangent bucket by itself.

## Results

The exact `j=3` projective-plane census gives:

```text
all hyperplanes              5220
common_root                    16
twin                         1920
sparse3_only                 3282
dual_distance_ge_4              2
```

The largest support-count profiles in the three sparse buckets are:

```text
common_root       (support 1,2,3) = (1,15,105)
twin              (support 1,2,3) = (0,1,38)
sparse3_only      (support 1,2,3) = (0,0,35)
```

The exact `j=4` projective-three-flat census gives:

```text
all hyperplanes             88741
common_root                    16
twin                         1920
sparse3_only                78448
dual_distance_ge_4           8357
```

The largest support-count profiles are:

```text
common_root       (support 1,2,3) = (1,15,105)
twin              (support 1,2,3) = (0,1,14)
sparse3_only      (support 1,2,3) = (0,0,5)
```

For `j=4`, the verifier also records a small literal quotient sanity check:
how many hyperplanes contain the `X^M` pullback coefficient subspace for
`M | gcd(16,4)`.  This is not a full quotient classification, but it confirms
that the support-3-only bucket is much larger than this literal pullback
container flag:

```text
M=2 containers      18 = 10 dual_distance_ge_4 + 8 twin
M=4 containers     307 = 43 dual_distance_ge_4 + 240 sparse3_only + 24 twin
```

## Interpretation

The pre-registered E9 outcome is the middle case: a third structural class
appears.  The literal two-bucket phrasing

```text
many sparse dual words => pullback/quotient or tangent
```

is too coarse in this toy model.  However, this is not an unstructured
counterexample to the proof program.  The extra bucket consists of minimal
support-3 sparse dependencies, exactly the branch that the `QF.7`
sparse-dependence descent lemma is designed to route into lower degree or
lower primitive residue.

So the suggested restatement is:

```text
many sparse dual words => paid common-root/twin structure
                         or quotient/pullback structure
                         or sparse-dependence descent
                         or the remaining primitive residue.
```

No unclassified support-`<=3` many-sparse flat appears in this census.  Flats
in the `dual_distance_ge_4` bucket are not many-sparse at the tested support
range; they belong to the spread/moment side of the Conjecture F plan.

Non-claims:

- no theorem for Conjecture F;
- no exhaustive classification of non-hyperplane flats;
- no census for sparse dual supports larger than `3`;
- no full quotient ledger for `j=4`.

## Replay

```bash
python3 experimental/scripts/verify_conjecture_f_many_sparse_census.py
python3 experimental/scripts/verify_conjecture_f_many_sparse_census.py --emit
python3 experimental/scripts/verify_conjecture_f_many_sparse_census.py --check experimental/data/certificates/conjecture-f-many-sparse-census/conjecture_f_many_sparse_census.json
python3 -m py_compile experimental/scripts/verify_conjecture_f_many_sparse_census.py
```
