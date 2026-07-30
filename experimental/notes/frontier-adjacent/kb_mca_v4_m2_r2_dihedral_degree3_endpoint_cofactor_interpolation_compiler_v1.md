---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: Actual realization of the residual n=3 component is equivalent to a full-support kernel of one explicit 38-by-12 source-cofactor matrix. Every such kernel induces a flat multiplicative transport on the source-star graph. A pinned split s=6 locator packet satisfies the inherited ownership and four-edge color interfaces but has six nonidentity canonical square holonomies and a nonzero rank-twelve minor.
architecture: null
partition_digest: null
atom_or_cell: K3_M2_R2_DIHEDRAL_DEGREE3_ENDPOINT_COFACTOR_INTERPOLATION_COMPILER
quantifier: every actual endpoint realization of the sole residual n=3 component; one pinned split-field locator packet for the deleting fixture
projection_and_unit: exact endpoint-component divisibility and source interpolation; not a carrier owner, received-line theorem, slope projection, or payment
claimed_bound: H divides the actual endpoint form if and only if the stacked cofactor matrix has a kernel vector with all twelve entries nonzero; every star cycle then has holonomy one; the pinned admissible fixture has six nonidentity square holonomies and rank twelve
status: PROVED_EXACT_ENDPOINT_COFACTOR_COMPILER_ONE_ADMISSIBLE_PACKET_DELETED_ROW_OPEN
impact: REPLACES_THE_VAGUE_ACTIVE_PENCIL_GATE_BY_ONE_EXACT_FULL_SUPPORT_KERNEL_PROBLEM
falsifier: an actual factorization violating the two interpolation identities or star transport, a full-support kernel that does not reconstruct the cofactor, or failure of the pinned holonomies or determinant
replay: python3 experimental/scripts/verify_kb_mca_v4_m2_r2_dihedral_degree3_endpoint_cofactor_interpolation_compiler_v1.py --check --tamper-selftest
---

# KoalaBear cubic endpoint-cofactor interpolation compiler

## 0. Verdict

The abstract cubic realization does not yet realize the actual endpoint
source form. The first missing endpoint condition is now exact.

Let the twelve source labels be `alpha_i`, let `A` be their monic locator,
and use the inherited source presentation

```text
M(T,X)=sum_i kappa_i L_i(T) B(X)/z_i(X),             (0.1)
```

where `L_i` is the normalized Lagrange basis, all `kappa_i` are nonzero,
and the pairwise coprime coordinate quadratics `z_i` multiply to `B`. For
the residual bidegree-`(2,4)` component `H`, put

```text
H_i(X)=H(alpha_i,X),
E_i(X)=B(X)/(z_i(X)H_i(X)).                          (0.2)
```

Complete-source divisibility makes `E_i` a degree-18 form. Then

```text
H divides M
```

if and only if there are twelve nonzero scalars `w_i` such that

```text
sum_i w_i E_i=0,
sum_i alpha_i w_i E_i=0.                            (0.3)
```

Equivalently, the `38 x 12` coefficient matrix with columns
`(E_i,alpha_i E_i)` has a full-support kernel. This is necessary and
sufficient, not a rank heuristic.

At a simple root `x` of `B`, write `star(x)={a,b}` and let `c` be the
unique coordinate label with `z_c(x)=0`. Locator avoidance makes `a,b,c`
distinct. Evaluating the two identities above at `x` and eliminating the
`c` term gives

```text
(alpha_a-alpha_c)w_a E_a(x)
 +(alpha_b-alpha_c)w_b E_b(x)=0.                   (0.4)
```

Hence the directed edge `a -> b` has nonzero transport

```text
rho_(a->b)(x)=
 -[(alpha_a-alpha_c)E_a(x)]/[(alpha_b-alpha_c)E_b(x)],
```

and every directed star cycle must have transport product one. This is a
necessary local obstruction, not a sufficiency claim.

One pinned `F_47` packet satisfies the exact inherited `s=6` interfaces:
six invariant coordinate quadratics, a fixed-point-free invariant-fiber
bijection, a simple two-regular noninvariant pole graph, locator avoidance,
and exactly four pole edges carried by the degree-two component. Its first
coefficient block has rank 11 with only a sparse kernel. The stacked matrix
has rank 12; rows `0,...,10,19` have determinant `7 mod 47`. Its six
canonical `K_(2,2)` square holonomies are

```text
11,26,17 and 2,41,31 mod 47,
```

so every one is nonidentity. Thus this admissible abstract packet is not an
endpoint component already by a four-edge local witness.

This does not delete every locator ownership or the deployed KoalaBear row.
It replaces the previous open-ended active-pencil instruction by one exact
finite-algebraic gate.

## 1. Interpolation proof

If `M=HN`, bidegrees give `bideg(N)=(9,18)`. Evaluating at a source label
and using the normalized Lagrange basis gives

```text
N(alpha_i,X)=kappa_i E_i(X).                        (1.1)
```

Conversely, any `T`-degree-at-most-nine form satisfying (1.1) makes `M-HN`
have `T`-degree at most eleven and twelve distinct roots, hence vanish.

The unique degree-at-most-eleven interpolant is

```text
N_11(T,X)=sum_i kappa_i E_i(X)
           A(T)/((T-alpha_i)A'(alpha_i)).            (1.2)
```

Write `s=sum_i alpha_i`. The `T^11,T^10` coefficients in the `i`th
Lagrange polynomial are

```text
1/A'(alpha_i),       (alpha_i-s)/A'(alpha_i).        (1.3)
```

Hence (1.2) has degree at most nine exactly when (0.3) holds with
`w_i=kappa_i/A'(alpha_i)`. Every `w_i` is nonzero. Conversely a
full-support solution recovers nonzero `kappa_i=w_i A'(alpha_i)` and the
required cofactor through (1.2).

## 2. Star transport

At a simple complete-source root, only `E_a,E_b,E_c` are nonzero: `a,b`
are the two star labels and `c` is the locator owner. Subtracting
`alpha_c` times the first identity in (0.3) from the second proves (0.4).
Since all source labels are distinct, the actual weights have full support,
and the three cofactor evaluations are nonzero, it gives the printed edge
transport. Multiplying `w_b/w_a` around any directed cycle telescopes to
one.

## 3. Deleting fixture

For the parent geometric maps over `F_47`, take cubic pole values `7,18`.
The source labels are

```text
5,10,17,19,21,23,24,26,28,30,37,42,
```

and the complete-source roots are

```text
3,6,8,11,12,13,14,15,16,18,20,21,
26,27,29,31,32,33,34,35,36,39,41,44.
```

Index the labels in the first order and assign coordinate roots by

```text
0:(32,31)   1:(11,36)   2:(6,41)    3:(16,33)
4:(3,39)    5:(12,35)   6:(18,29)   7:(34,14)
8:(20,27)   9:(44,13)  10:(21,26)  11:(15,8).       (2.1)
```

The invariant set is `I={1,2,5,6,8,10}` and the invariant-fiber map is

```text
1->10, 2->8, 5->6, 6->5, 8->2, 10->1.
```

The verifier reconstructs the maps, roots, stars, ownership, pole graph,
component color, cofactors, and matrix. The first block's kernel generator
is

```text
(0,13,0,0,0,19,14,0,0,0,1,0),
```

which cannot encode nonzero source weights. The stacked minor is already
nonzero, so no kernel survives. Independently, the source deck pairs split
the two star components into

```text
(0,11)|(2,9)|(4,7),       (1,10)|(3,8)|(5,6).
```

Orienting the three standard squares in each component gives the six
products `11,26,17,2,41,31`. Since none is one, each square separately
contradicts the necessary cycle law.

## 4. Scope

Proved: the exact actual-component interpolation equivalence, the necessary
star-cycle holonomy law, and deletion of the pinned admissible packet. Not
proved: a universal nonidentity-holonomy or rank theorem for all locator
ownerships or pole pairs, fixed active-root compatibility, a
parameter-to-carrier bridge, received-data or explaining-polynomial descent,
distinct-slope projection, owner, payment, K3 close, KoalaBear row, or either
Prize problem.

The next route-deciding action is to classify admissible `s=6` ownerships
up to the two `K_(2,2,2)` star automorphisms and source deck involution,
first proving one nonidentity cycle holonomy in every case and falling back
to the full stacked rank gate. A surviving kernel must instead be
reconstructed into its cofactor and tested against the actual active and
block fibers.
