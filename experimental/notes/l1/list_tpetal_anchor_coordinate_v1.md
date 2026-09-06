---
workboard_item: T
row: symbolic smooth RS full-petal source cell at arbitrary t; not a deployed row
object: LIST
target_epsilon: target-free structural theorem; intended finite context 2^-128
agreement: one exact labelled support of total degree h with d<h<=2d+1
B_star: not_applicable
direct_statement: relative to one squarefree primitive anchor, the complete monic t-petal pair chart is affinely bijective to degree-at-most-(e-1) determinant coordinates, and one gcd recovers every common-defect owner
architecture: DIRECT
partition_digest: not_applicable
atom_or_cell: one fixed labelled arbitrary-t monic pair slice
quantifier: every field and every nonempty saturated slice satisfying the companion dimension theorem, with a squarefree anchor for owner recovery
projection_and_unit: monic degree-d locator candidates with their unique degree-at-most-d numerators
claimed_bound: exact affine coordinate bijection and exact gcd-owner recovery; no split-point or aggregate owner bound
status: PROVED
impact: ARCHITECTURE_BRIDGE
falsifier: a determinant-coordinate collision, a failure of reconstruction, or a common anchor root not detected by the coordinate gcd
replay: analytic proof; no computational claim
---

# General t-petal anchor determinant coordinate

## 1. Setup

Use the notation and hypotheses of
`list_tpetal_saturated_slice_dimension_v1.md`. Thus

```text
Lambda=product_i L_i,       h=deg Lambda,
e=2d+1-h>=0,
V={(G,B): deg G,deg B<=d and L_i divides B-c_iG for every i},
```

and `V` contains a primitive anchor `(F,W)` with `F` monic of degree `d`.
Let

```text
M={(G,B) in V: G is monic of degree d}.               (1.1)
```

The companion theorem proves that `M` is a nonempty affine space of
dimension `e` and that every locator in it has a unique numerator.

## 2. Complete monic coordinate

For `(G,B) in M`, define

```text
H=(FB-GW)/Lambda.                                     (2.1)
```

### Theorem 2.1

With `K[X]_(<=-1)={0}` when `e=0`,

```text
M -> K[X]_(<=e-1),       (G,B) -> H                  (2.2)
```

is an affine bijection sending the anchor to zero. Hence `H` determines the
complete pair `(G,B)` before splitness, primitivity, and exactness filters are
imposed.

#### Proof

The companion cross-determinant theorem makes `(2.1)` well defined and puts
its image in degree at most `e-1`. Suppose two points have the same `H`.
Their difference lies in the linear kernel, which is exactly the scalar line
`K(F,W)`. Thus their locator difference is `lambda F` for a scalar `lambda`.
Both locators are monic of degree `d`, while `F` is monic, so comparison of
leading coefficients forces `lambda=0`. The map is injective.

The source and target in `(2.2)` both have affine dimension `e`, so the map
is bijective. QED.

## 3. Exact owner recovery

Assume now that the anchor locator `F` is squarefree. For every distinct
primitive exact member,

```text
H!=0,       gcd(H,F)=gcd(G,F),                        (3.1)
```

where gcds are monic.

Indeed, let `x` be a root of `F`. Primitivity gives `W(x)!=0`, and primitive
petal disjointness from the companion theorem gives `Lambda(x)!=0`.
Evaluation of

```text
FB-GW=Lambda H
```

at `x` yields

```text
-G(x)W(x)=Lambda(x)H(x).
```

Thus `H(x)=0` exactly when `G(x)=0`. Squarefreeness of `F` proves `(3.1)`.
The bijection shows that only the anchor has `H=0`.

## 4. Consequence and nonclaim

The common-defect owner of every candidate is one gcd stratum of a single
degree-at-most-`e-1` coordinate body. In particular,

```text
deg gcd(G,F)<=e-1
```

for every distinct exact member, recovering the arbitrary-`t` overlap cap.

For a full-petal FPC5 cell, the remaining fixed-cell count is exactly the set
of coordinates `H` whose reconstructed locator splits on the core and whose
reconstructed pair passes the exact guards. The theorem closes coefficient
multiplicity and fixed-owner ambiguity, but it does not bound that set,
coalesce the realized gcd strata, aggregate source cells, or deploy a row.
