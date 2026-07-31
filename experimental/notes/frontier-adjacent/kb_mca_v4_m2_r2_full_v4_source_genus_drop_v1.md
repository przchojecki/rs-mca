---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: In the full-V4 inner-degree-2 row (r,delta)=(2,4), the actual bidegree-(2,4) source normalization has genus 0 or 1. Genus 2 and 3 are impossible; the diagonal endpoint/source-deck lift has respectively 2 or 0 fixed points.
architecture: null
partition_digest: null
atom_or_cell: K3_M2_R2_FULL_V4_SOURCE_GENUS_DROP
quantifier: every actual residual (m,r,delta)=(2,2,4) component after the line/conic coefficient-image exclusions
projection_and_unit: exact source-curve automorphism and tame Riemann-Hurwitz reduction; not an m2 deletion or payment
claimed_bound: source genus drops from at most 3 to the exact alternatives g=0,1 in the full-V4 row
status: PROVED_M2_R2_SOURCE_GENUS_ZERO_OR_ONE
impact: NARROWS_THE_FULL_V4_M2_ROW_TO_RATIONAL_OR_ELLIPTIC_GEOMETRY
falsifier: an actual full-V4 source normalization of genus 2 or 3, a commuting second endpoint involution not forcing the excluded conic image, or failure of the printed fixed-point identity
replay: python3 experimental/scripts/verify_kb_mca_v4_m2_r2_full_v4_source_genus_drop_v1.py --check --tamper-selftest
---

# KoalaBear m2 r2 full-V4 source genus drop

## 0. Verdict

In the `(m,r,delta)=(2,2,4)` row, the actual source normalization has

```text
(genus, fixed points of tau x b)=(0,2) or (1,0).
```

Genus two and three are impossible. Neither remaining regime is deleted.

## 1. The source V4 cover

Let `eta` be the involution of the degree-two source projection
`Gamma->P1_X`. Let `a` and `c` denote the lifts of `tau x 1` and
`1 x tau`. The preceding full-V4 router proves that

```text
a:(T,X)->(tau(T),b(X)),
```

where `b` is the deck involution of `psi(X)=W`. Both `eta` and `a` fix `W`,
they commute, and the map to the `W` line has degree four. Thus

```text
Deck(Gamma/P1_W)=<eta,a>=V4.
```

## 2. Conjugation by the second endpoint involution

The automorphism `c` fixes `T`, transports `W` by `tau`, normalizes the
deck V4, and fixes `a` under conjugation. It sends `eta` to `eta` or
`eta*a`.

If it fixed `eta`, it would descend to a nontrivial involution `j` of the
source parameter line. Since `c` fixes `T`, the unordered pair of `T` roots
of the source quadratic would be equal at `X` and `j(X)`. The degree-four
coefficient map would factor through `P1_X/<j>`, so its image would have
degree at most two. That is the already-excluded line/conic coefficient
branch. Hence

```text
c eta c^-1=eta*a.
```

## 3. Tame fixed-point arithmetic

Write `g=g(Gamma)` and `n_s=#Fix(s)`. The quotient by `eta` is `P1_X`, so

```text
n_eta=2g+2.
```

The V4 quotient to `P1_W` is tame. Distinct nontrivial involutions have
disjoint fixed sets because a tame point stabilizer is cyclic, and
Riemann-Hurwitz gives

```text
n_eta+n_a+n_(eta*a)=2g+6.
```

The conjugation result makes `n_(eta*a)=n_eta`, hence

```text
n_a=2-2g.
```

Nonnegativity leaves exactly `(g,n_a)=(0,2),(1,0)`.

## 4. Scope

This packet proves no source-genus lower bound and does not classify the
outer bidegree-`(2,2)` correspondence. It does not delete either rational or
elliptic regime, affect the other two `m=2` types, construct a
carrier/data/explaining-polynomial/slope owner, close `u=2`, K3, or the
KoalaBear row, or move any ledger quantity.
