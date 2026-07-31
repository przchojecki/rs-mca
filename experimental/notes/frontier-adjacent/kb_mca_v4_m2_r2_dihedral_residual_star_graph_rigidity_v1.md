---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: In every surviving full-V4 n=3 or n=6 dihedral profile, the complete source-star graph is respectively two K_(2,2,2) components or the two-point blow-up of C6; all 24 weights are one and all twelve source rows have degree four.
architecture: null
partition_digest: null
atom_or_cell: K3_M2_R2_DIHEDRAL_RESIDUAL_STAR_GRAPH_RIGIDITY
quantifier: every actual residual (m,r,delta)=(2,2,4) component with dihedral factor degree n in {3,6}
projection_and_unit: exact normalized complete-source stars; not a carrier, slope, or payment count
claimed_bound: the residual source-star defect is exactly zero and further defect counting cannot delete n=3 or n=6
status: PROVED_M2_R2_DIHEDRAL_RESIDUAL_STAR_GRAPH_RIGIDITY
impact: REPLACES_THE_TWO_RESIDUAL_ORIENTATION_PROBLEMS_BY_EXACT_GRAPH_REALIZATION_PROBLEMS
falsifier: a non-cycle generic Dn incidence, failure of the c eta c^-1=eta*a orientation exchange, a repeated residual star, or a source-label degree other than four
replay: python3 experimental/scripts/verify_kb_mca_v4_m2_r2_dihedral_residual_star_graph_rigidity_v1.py --check --tamper-selftest
---

# KoalaBear m2 r2 residual dihedral star-graph rigidity

## 0. Verdict

The surviving `n=3,6` profiles have exact complete-source graph shapes:

```text
n=3: two disjoint copies of K_(2,2,2);
n=6: the two-point blow-up of C6.
```

Every one of the 24 star weights is one and every source-label degree is
four. This is a rigidity theorem, not an existence or deletion theorem.

## 1. Generic dihedral incidence

On a regular `D_n=<u,v>` orbit, the two reflection quotients are the
two-element orbit partitions of `u` and `v`. Alternating their matchings
traverses an orbit of `uv` of length `n`, so the quotient incidence is the
bipartite cycle `C_(2n)`. For `n>=3`, distinct `Z` values therefore see
distinct unordered pairs of adjacent `Y` values.

## 2. The orientation exchange

Fix adjacent `Y` values and endpoint labels `w,tau(w)` above their `Z`
value. If the two stars over `D_w=psi^*[w]` are

```text
{t,s}, {tau(t),tau(s)},
```

then the source-cover laws

```text
a:(T,X)->(tau(T),b(X)),       c eta c^(-1)=eta*a
```

force the stars over `D_(tau(w))` to be

```text
{t,tau(s)}, {tau(t),s}.
```

Thus each `Z` value contributes every edge of its cross `K_(2,2)` exactly
once. This is forced complementary orientation, not an orientation choice.

## 3. Complete graph

For `n=3`, one pole of `G` gives the two-point blow-up of a triangle,
`K_(2,2,2)`, and there are two disjoint generic pole fibers. For `n=6`,
the sole generic pole gives the two-point blow-up of a six-cycle.

The selected quotient fibers contain all six poles of `F`; their endpoint
preimages are all twelve source labels. The complete-source pullback has
degree 24, so the displayed 24 distinct stars account for the whole source
divisor. All weights are one, the defect is zero, and every source label has
two cycle neighbors contributing two edges each, hence degree four.

## 4. Scope

This packet does not construct or delete `n=3` or `n=6`, delete the
full-V4 type or either other `m=2` type, construct an owner, or close K3,
an endpoint row, the KoalaBear row, or either Prize problem. The next task
is exact realization of these graphs by the birational quartic coefficient
map and the genus-zero/genus-one source-cover passport.
