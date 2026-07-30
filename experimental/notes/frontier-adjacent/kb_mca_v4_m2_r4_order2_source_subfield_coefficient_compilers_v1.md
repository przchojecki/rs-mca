---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: The diagonal order-two source descent has an exhaustive source-line/biquadratic split, both branches have exact coefficient tests, and every order-two source-star packet has a 45-by-12 source interpolation gate.
architecture: null
partition_digest: null
atom_or_cell: K3_M2_R4_ORDER_TWO_SOURCE_SUBFIELD_AND_COEFFICIENT_COMPILERS
quantifier: every actual graph-free Q=6,s=6 inner-degree-two component in the order-two V4-stabilizer row
projection_and_unit: exact source-component and endpoint-component coefficient interfaces; not a carrier, received-line theorem, distinct-slope projection, owner, or payment
claimed_bound: exhaustive diagonal descent dichotomy, 8/7-dimensional reciprocal norm forms or split quartic resolvent, and a shared 45-by-12 full-support source-row kernel equivalence
status: PROVED_COMPILERS_ORDER_TWO_TYPE_OPEN_K3_OPEN
impact: REPLACES_THE_DIAGONAL_SOURCE_DESCENT_AMBIGUITY_AND_GENERIC_SOURCE_COMPONENT_SEARCH_BY_EXACT_LOW_DIMENSIONAL_GATES
falsifier: an actual diagonal component outside the source-field dichotomy, failure of the reciprocal norm or split resolvent in its branch, or an actual source-row packet failing the 45-by-12 kernel/resultant identities
replay: python3 experimental/scripts/verify_kb_mca_v4_m2_r4_order2_source_subfield_coefficient_compilers_v1.py --check --tamper-selftest
---

# KoalaBear order-two source-subfield and coefficient compilers

## 0. Verdict

The preceding order-two packet separates the coordinate and diagonal
orientations and supplies the diagonal whole-fiber interpolation gate. This
extension resolves the remaining source-descent ambiguity and makes the
actual bidegree-`(2,4)` source-component test explicit.

For the diagonal orientation, either the stabilizer preserves the known
quadratic source intermediate field, giving a reciprocal source-line lift,
or its conjugate is a second rational quadratic intermediate field, forcing
the quartic projection to be a low-genus `V4` cover. The two branches become
respectively a quadratic-norm equation and a split cubic-resolvent equation.

Independently of orientation, twelve projective source-row quartics come
from a bidegree-at-most-`(2,4)` source form exactly when a concrete
`45 x 12` matrix has a full-support kernel.

These are exact K3/source-component interfaces. They delete no order-two
subgroup by themselves, book no owner or payment, and do not close K3 or the
KoalaBear row.

## 1. Diagonal source-subfield dichotomy

Let `E` be the function field of the normalization of the actual endpoint
component. Its birational source model gives

```text
F=K(W) subset K(X) subset E,
[K(X):F]=[E:K(X)]=2,       W=psi(X).                (1.1)
```

Let `sigma` be the diagonal stabilizer automorphism. It preserves `F` as a
field and sends `K(X)` to another quadratic intermediate field `K_1`.

If `K_1=K(X)`, then `sigma` descends to a projective source involution `s`
which commutes with the deck involution `b` and satisfies

```text
psi(sX)=tau(psi(X)).                                 (1.2)
```

Geometrically there are compatible coordinates

```text
b(X)=-X,       s(X)=1/X,       psi(X)=X^2,
tau(Z)=1/Z.                                         (1.3)
```

The source equation is reciprocal or anti-reciprocal:

```text
T^2X^4H(1/T,1/X)=epsilon H(T,X),
epsilon in {+1,-1}.                                 (1.4)
```

Individual stars may be transported by this proved lift.

If `K_1!=K(X)`, the two distinct quadratic extensions fill the degree-four
field `E`, so `E/F` is biquadratic. Let `eta,eta'` fix the two rational
quadratic subfields and put `mu=eta eta'`. Tame Riemann--Hurwitz gives only

```text
g=0: inertia eta,eta',mu;
g=1: inertia eta,eta,eta',eta'.                     (1.5)
```

Equivalently `#Fix(mu)=2-2g`. This function-field `V4` is not the full
ambient component stabilizer deleted in the preceding K3 work.

## 2. Branch coefficient equations

In the source-line branch, decompose uniquely into even and odd `X` parts:

```text
H(T,X)=U(T,W)+X V(T,W),       W=X^2,
deg U<=(2,2),       deg V<=(2,1).                   (2.1)
```

The source deck conjugate changes the sign of the odd part, so after one
projective rescaling the endpoint equation is

```text
G(T,W)=U(T,W)^2-WV(T,W)^2.                          (2.2)
```

For the same sign `epsilon` as in (1.4),

```text
T^2W^2U(1/T,1/W)=epsilon U(T,W),
T^2W  V(1/T,1/W)=epsilon V(T,W).                   (2.3)
```

The positive and negative source spaces have dimensions `8` and `7`.
In both cases the endpoint is positive reciprocal:

```text
T^4W^4G(1/T,1/W)=G(T,W).                            (2.4)
```

In the biquadratic branch, make the endpoint quartic monic over `K(W)`:

```text
g(Z)=Z^4+aZ^3+bZ^2+cZ+d.
```

Its cubic resolvent

```text
R(Y)=Y^3-bY^2+(ac-4d)Y+(4bd-a^2d-c^2)              (2.5)
```

splits into three distinct linear factors over `K(W)`, and the quartic
discriminant is a square. Conversely, for an irreducible separable quartic,
complete splitting of (2.5) is equivalent to `V4` Galois group. Clearing
denominators makes this a polynomial-identity gate.

## 3. Shared source-row interpolation gate

Let `[q_i(X)]` be the twelve projective nonzero binary quartic rows proposed
for a source component, and write

```text
q_i(X)=sum_(b=0)^4 q_(i,b)X^b.
```

Let `P` be a `9 x 12` parity-check matrix for degree-at-most-two evaluation
at the twelve source labels. Form

```text
N_(s,b),i=P_(s,i)q_(i,b),       N in K^(45 x 12).   (3.1)
```

There is a biform `H` of bidegree at most `(2,4)` and nonzero row scales
`c_i` with

```text
H(alpha_i,X)=c_iq_i(X)                              (3.2)
```

if and only if `Nc=0` for a full-support vector `c`. For fixed `c`, `H` is
unique: each of its five `X` coefficients is the unique degree-at-most-two
interpolant of the restored twelve values.

The branch-independent complete-source saturation clause also gives

```text
product_i q_i(X) ~ B(X)^2,
Res_T(A(T),H(T,X)) ~ B(X)^2.                        (3.3)
```

Ramified fibers are included by divisor multiplicity. In the lifted
coordinates (1.3), `B(X)~A(X^2)`.

## 4. Scope and next action

Proved: the exhaustive source-field dichotomy, reciprocal normal form,
low-genus biquadratic passports, quadratic norm, split resolvent, shared
source-row interpolation equivalence, and square resultant.

Not proved: universal failure of any branch gate, exact-degree and
irreducibility checks for a passing interpolant, deck-conjugate distinction,
outer self-correspondence divisibility, deletion of an orientation or the
order-two type, an owner, payment, K3, the row, or a Prize result.

The next exact order is:

1. route each coordinate or diagonal source-facet packet through (3.1);
2. reconstruct the unique source form for a survivor;
3. impose (2.1)--(2.5), as appropriate, together with irreducibility and
   the branch passport; and
4. only then reconstruct the endpoint biform and test the outer factor.
