---
workboard_item: T
row: symbolic smooth RS full-petal source cell at arbitrary t; not a deployed row
object: LIST
target_epsilon: target-free structural theorem; intended finite context 2^-128
agreement: one exact labelled support of total degree h with d<h<=2d+1
B_star: not_applicable
direct_statement: one primitive degree-d anchor forces the complete t-petal pair slice and its locator image to have dimension e+1, with a monic affine e-flat chart, for e=2d+1-h
architecture: DIRECT
partition_digest: not_applicable
atom_or_cell: one fixed labelled full-petal pair slice
quantifier: every field, every pairwise-coprime petal-locator tuple, and every nonempty saturated slice satisfying the printed degree hypotheses
projection_and_unit: monic degree-d locator candidates with their unique degree-at-most-d numerators
claimed_bound: exact dimension e+1 for the pair and locator spaces and exact monic affine dimension e; no split-point or aggregate bound
status: PROVED
impact: ARCHITECTURE_BRIDGE
falsifier: a saturated slice with dimension different from e+1, a nonzero locator-projection kernel under h>d, or a primitive member sharing a petal root
replay: analytic proof; no computational claim
---

# General t-petal saturated-slice dimension theorem

## 1. Purpose and nonclaim

The three-petal LS6 note in this PR gives exact coordinates inside one
specific complement-divisor atom. This companion note isolates the linear
theorem needed before such coordinates can be sought at arbitrary `t`.

One saturated pair determines the exact dimension of the complete labelled
pair slice. In the LIST range `h>d`, projection to the locator is injective,
so the result is an actual affine split-locator chart rather than only a pair
space dimension count.

The theorem does **not** count split locators in that chart, bound a list,
aggregate source cells or owners, deploy a finite row, or move a Prize
endpoint.

## 2. Setup

Let `K` be a field. Let `L_1,...,L_t` be pairwise coprime monic
polynomials and put

```text
Lambda=product_i L_i,       h=deg Lambda.             (2.1)
```

Fix labels `c_1,...,c_t` in `K`; distinctness is not required. For an
integer `d` satisfying

```text
d<h<=2d+1,       e=2d+1-h>=0,                         (2.2)
```

define

```text
V={(G,B): deg G<=d, deg B<=d,
            L_i divides B-c_iG for every i}.          (2.3)
```

Assume `V` contains a saturated anchor `(F,W)` with

```text
F monic,       deg F=d,       gcd(F,W)=1.             (2.4)
```

## 3. Exact dimension

### Theorem 3.1

Under `(2.1)--(2.4)`,

```text
dim_K V=e+1.                                           (3.1)
```

Projection to the locator coordinate is a linear isomorphism

```text
V -> V_F={G:(G,B) in V for some B}.                   (3.2)
```

Consequently `dim V_F=e+1`, and its monic degree-`d` chart is a nonempty
affine `e`-flat. Every primitive exact contributor injects into the split
locators in that flat, with its numerator reconstructed uniquely.

#### Proof

The ambient pair space has dimension `2d+2`. The congruences in `(2.3)`
impose at most `h` linear conditions, so

```text
dim V>=2d+2-h=e+1.                                    (3.3)
```

Fix the saturated anchor and define

```text
Phi: V -> K[X],       Phi(G,B)=(FB-GW)/Lambda.        (3.4)
```

For every `i`, both pairs obey the same labelled congruence modulo `L_i`,
so `L_i` divides `FB-GW`. Pairwise coprimality makes `(3.4)` well defined.
Its image has degree at most

```text
2d-h=e-1,
```

and therefore lies in an `e`-dimensional polynomial space, with the target
understood as zero when `e=0`.

If `Phi(G,B)=0`, then `FB=GW`. Since `gcd(F,W)=1`, one has `F|G`. The degree
caps and `deg F=d` force `G=lambda F` for a scalar `lambda`, and then
`B=lambda W`. Thus

```text
ker Phi=K(F,W),       dim ker Phi=1.                  (3.5)
```

Rank-nullity gives `dim V<=e+1`, which with `(3.3)` proves `(3.1)`.

For `(3.2)`, a pair `(0,B)` in `V` has every `L_i` dividing `B`; hence
`Lambda|B`. Since `deg B<=d<h`, this forces `B=0`. Locator projection is
injective. The anchor makes the degree-`d` leading-coefficient functional
nonzero on `V_F`, so setting it equal to one gives a nonempty affine
hyperplane of dimension `e`. QED.

## 4. Primitive disjointness is automatic

No separate assumption that defect roots avoid petal roots is needed for a
primitive member. If `L_i(x)=F(x)=0`, the congruence in `(2.3)` gives
`W(x)=c_iF(x)=0`, contradicting `gcd(F,W)=1`. Thus the locator roots of every
primitive member are automatically disjoint from all petal roots.

## 5. FPC5 specialization and remaining bridge

For a full-petal FPC5 cell, `h=t*ell` and

```text
e=2d+1-t*ell.
```

On a nonpositive-Johnson residual, `e>=1`. The exact list threshold has
`h>=d+g` with `g>=1`, so `h>d`. Every nonempty exact cell contains a
primitive monic anchor. The theorem therefore gives a monic affine
`e`-flat locator chart at every `t`, including `t>=4`; no general-`t`
syzygy or mu-basis theorem is needed for this dimension statement.

What remains is a dimension-uniform maximum-versus-average theorem for the
split locators that survive the exact guards, together with chronology-valid
aggregation across source cells and owners. The dimension theorem supplies
the typed input to that problem but no part of its required count.
