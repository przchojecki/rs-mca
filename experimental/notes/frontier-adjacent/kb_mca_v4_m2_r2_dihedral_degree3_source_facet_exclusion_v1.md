---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: The common-five source facet forces an independent five-set in the exact residual cubic source-star graph, so n=3 is empty; together with the certified n=2,5,6 exclusions this deletes the full-V4 (m,r,delta)=(2,2,4) type.
architecture: null
partition_digest: null
atom_or_cell: K3_M2_R2_DIHEDRAL_DEGREE3_SOURCE_FACET_AND_FULL_V4_EXCLUSION
quantifier: every actual graph-free Q=6,s=6 residual full-V4 n=3 component, followed by the exhaustive full-V4 factor-degree split
projection_and_unit: exact source-facet and source-star component exclusion; not a carrier, received-line theorem, distinct-slope projection, owner, or payment
claimed_bound: alpha(K_(2,2,2) disjoint_union K_(2,2,2))=4<5, hence n=3 and then the full-V4 type are empty
status: PROVED_N3_AND_FULL_V4_TYPE_EMPTY_K3_OPEN
impact: REDUCES_THE_THREE_M2_STABILIZER_TYPES_TO_THE_ORDER_TWO_AND_TRIVIAL_TYPES
falsifier: failure of the common-five horizontal fiber, a cubic complete-coordinate fiber outside the omitted-pair law, a five-vertex independent set in the exact graph, or a full-V4 factor degree outside 2,3,5,6
replay: python3 experimental/scripts/verify_kb_mca_v4_m2_r2_dihedral_degree3_source_facet_exclusion_v1.py --check --tamper-selftest
---

# KoalaBear cubic source-facet and full-V4 exclusion

## 0. Verdict

The residual full-V4 cubic profile is empty. The inherited `Q=6,s=6`
source-facet deck supplies a five-set `K` inside a six-set `I`. The exact
cubic source-star graph is

```text
G=K_(2,2,2) disjoint_union K_(2,2,2).
```

For each `k in K`, the two component stars above the complete source
fiber indexed by `k` have endpoint union `N_G(k)`, and the source facet
forces that union into `I^c`. Thus `K` is independent. But
`alpha(G)=2+2=4`, contradicting `|K|=5`.

The outer-factor theorem gives the exhaustive full-V4 list
`n in {2,3,5,6}`. Existing exact packets delete `n=2,5,6`, so the cubic
deletion also proves that the complete

```text
(m,r,delta)=(2,2,4)
```

type is empty. The order-two and trivial component-stabilizer types
`(r,delta)=(4,2),(8,1)` remain open. No slope owner or payment is booked.

## 1. Common-five source facet

At repository commit
`44542e91e459364a521870ed2ebde7f6fe5055bf`, Corollaries 9.25 and 9.27
of the pole-disjoint conic facet-collinearity theorem prove the following
for every actual graph-free `Q=6,s=6` packet. There are source-label sets

```text
K subset I,       |K|=5,       |I|=6,                         (1.1)
```

and, for every `k in K` and every
`pi in psi^(-1)(alpha_k)`,

```text
Root_T F_out(T,pi)={alpha_j:j notin I}.                       (1.2)
```

Equation (1.2) is equation (9.103) of the source theorem. If `H` is one
irreducible outgoing component, every horizontal root of `H(T,pi)` is
therefore in `I^c`.

This use is narrower than the component-color problem left open in
Corollary 9.28 and Guardrails 9.29--9.31. It does not identify a pole-graph
cycle with an irreducible component. It uses only the exact horizontal
root set of the whole outgoing factor and containment for one already
identified component.

## 2. Twist-safe cubic contradiction

The residual star-graph theorem applies to every actual `n=3` full-V4
profile. Fix `k in K`. The regular `D_3` incidence and the forced
cross-edge orientations say that the two points of
`psi^(-1)(alpha_k)` contribute two opposite edges between two deck-pair
parts in one six-label component of `G`. Let `U_k` be their four endpoints
and `P_k` the omitted deck pair:

```text
component(k)=U_k disjoint_union P_k,       |U_k|=4, |P_k|=2.  (2.1)
```

This formulation deliberately retains the relative second-endpoint
projective twist. It does not identify the `Z`-fiber pair with a
first-coordinate deck pair.

Because `H` divides `F_out`, equation (1.2) gives

```text
U_k subset I^c.                                             (2.2)
```

On the other hand, `k in K subset I`, so `k notin U_k`. The indexed
source label `k` and `U_k` belong to the same six-label common-pole
component: `F(h(alpha_k))` is the same outer pole that supports the two
horizontal cubic fibers. Equation (2.1) therefore forces `k in P_k`.
Every vertex in one part of `K_(2,2,2)` has the four vertices in the
other two parts as its neighborhood. Hence

```text
U_k=N_G(k) subset I^c.                                     (2.3)
```

If `k,k'` were adjacent and both in `K`, then (2.3) would put
`k' in I^c`, contradicting `K subset I`. Thus `K` is independent.
An independent set in one complete tripartite component lies in one
two-vertex part, so

```text
alpha(G)=2+2=4<5=|K|.
```

This contradiction deletes every actual `n=3` component.

## 3. Exhaustive full-V4 synthesis

The exact outer-factor reduction proves

```text
n in {2,3,5,6}.
```

The degree-two source-star packet deletes `n=2`, Section 2 deletes `n=3`,
the totally ramified source-star packet deletes `n=5`, and the
common-pole/source-cover packet deletes `n=6`. The list is exhaustive, so
the full-V4 `(m,r,delta)=(2,2,4)` type is empty.

The earlier endpoint-cofactor/gain-flatness compiler remains an exact and
useful audit theorem, but universal gain nonflatness is no longer needed
to delete this type.

## 4. Scope

Proved: the common-five outgoing-fiber consequence, the twist-safe cubic
independence contradiction, deletion of `n=3`, and deletion of the full-V4
inner-degree-two type. Not proved: deletion of either remaining `m=2` type,
an actual carrier/data/explaining-polynomial/slope owner, a ledger payment,
K3, the KoalaBear row, an adjacent certificate, or either Prize problem.

The next full-strength K3 action is the order-two stabilizer type
`(r,delta)=(4,2)`; the trivial type `(8,1)` remains behind it.
