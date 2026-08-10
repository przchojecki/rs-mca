---
workboard_item: T
row: symbolic smooth RS full-petal source cell at arbitrary t; not a deployed row
object: LIST
target_epsilon: target-free structural theorem; intended finite context 2^-128
agreement: one exact labelled support of total degree h with d<h<=2d+1
B_star: not_applicable
direct_statement: every determinant coordinate in a primitive monic t-petal anchor chart has an explicit remainder inverse and an exact root-local primitive guard
architecture: DIRECT
partition_digest: not_applicable
atom_or_cell: one fixed labelled arbitrary-t monic pair slice
quantifier: every field and every saturated slice satisfying the companion anchor-coordinate theorem; squarefree split locators for the root-local guard
projection_and_unit: degree-at-most-(e-1) determinant coordinates and their uniquely reconstructed monic degree-d locators
claimed_bound: exact inverse and exact primitive predicate; no split-point, owner-aggregate, deployed-row, or endpoint bound
status: PROVED
impact: ARCHITECTURE_BRIDGE
falsifier: a failed exact division, a reconstructed pair outside the labelled slice, a coordinate collision, or a primitive root misclassified by the printed local test
replay: analytic proof; no computational claim
---

# General t-petal anchor Pade chart

## 1. Setup

Use the notation and hypotheses of
`list_tpetal_anchor_coordinate_v1.md`. Thus

```text
Lambda=product_i L_i,       h=deg Lambda,
e=2d+1-h>=0,
V={(G,B): deg G,deg B<=d and L_i divides B-c_iG for every i},
```

and `(F,W)` is a primitive anchor with `F` monic of degree `d`. The
complete monic chart is

```text
M={(G,B) in V: G is monic of degree d}.
```

The companion note proves that

```text
(G,B) -> H=(FB-GW)/Lambda
```

is an affine bijection from `M` to `K[X]_(<=e-1)`.

## 2. Explicit inverse

Primitivity gives `gcd(F,W)=1`. Let

```text
I=W^(-1) mod F,       deg I<d.
```

### Theorem 2.1

For every `H` with `deg H<=e-1`, put

```text
R_H=rem_F(-Lambda H I),       G_H=F+R_H,
B_H=(G_H W+Lambda H)/F.                              (2.1)
```

The division defining `B_H` is exact, `G_H` is monic of degree `d`,
`deg B_H<=d`, and `(G_H,B_H)` is the unique point of `M` with determinant
coordinate `H`. Hence the locator chart is exactly

```text
{F+rem_F(-Lambda H I): deg H<=e-1}.                  (2.2)
```

#### Proof

The anchor congruences and primitivity imply `gcd(F,Lambda)=1`: a common
factor of `F` and some `L_i` would also divide `W`. By the definition of
`R_H`,

```text
G_H W+Lambda H==0 mod F,
```

so `B_H` is a polynomial. Since `deg R_H<d`, `G_H` is monic of degree `d`.
The identity

```text
h+e-1=2d
```

also gives `deg B_H<=d`.

For each `i`,

```text
F(B_H-c_iG_H)=G_H(W-c_iF)+Lambda H
```

is divisible by `L_i`. Since `F` is a unit modulo `L_i`, the reconstructed
pair belongs to `V`, and its determinant coordinate is `H`.

Conversely, reducing `FB-GW=Lambda H` modulo `F` gives

```text
G==-Lambda H I mod F.
```

Because `G-F` has degree below `d`, this forces `G=G_H`, and then the
determinant identity forces `B=B_H`. QED.

## 3. Exact primitive predicate

Assume `F` and `G_H` are squarefree split locators whose roots avoid the
petal roots. At a root `x` of `G_H`, one has

```text
F(x)!=0:       B_H(x)!=0 iff H(x)!=0;                (3.1)
F(x)=0:        B_H(x)!=0 iff
               G_H'(x)W(x)+Lambda(x)H'(x)!=0.       (3.2)
```

For `(3.1)`, evaluate `FB_H-G_HW=Lambda H`. For `(3.2)`, first note that a
common root forces `H(x)=0`, then differentiate the same identity:

```text
F'(x)B_H(x)-G_H'(x)W(x)=Lambda(x)H'(x).
```

Squarefreeness gives `F'(x)!=0`. Thus `gcd(G_H,B_H)=1` is exactly the
conjunction of `(3.1)--(3.2)` over the roots of `G_H`.

## 4. Consequence and nonclaim

Every surviving arbitrary-`t` full-petal fixed cell is now an explicit
primitive remainder cell. Its exact contributors are the coordinates `H`
for which `(2.2)` splits on the prescribed source core and the reconstructed
pair passes the local primitive and remaining exact guards.

This theorem does not bound how many such coordinates exist, coalesce gcd
owners, aggregate source cells, deploy a LIST row, or move an endpoint. It
does not say that a generic `H` reconstructs a split locator.
