# Coordinate-clone subcritical-class payment

Status: `PROVED_LOCAL_THEOREM / SELF_CONTAINED_PROOF / INDEPENDENT_REVIEW_REQUESTED`

This note pays all subcritical coordinate-clone classes in the owner-pencil
geometry of `experimental/grande_finale.tex` and concentrates every unpaid
clone exception on one large component. It is a partial result toward the
MCA exception-routing terminal `(E)`, not a proof of that terminal.

## Setup

Use the owner pencil and coordinate equations from
`thm:owner-pencil`:

```text
F_x(gamma,tau)
 = A_tau(x)+gamma B_tau(x)
   -Q_tau(x)(r0(x)+gamma r1(x)).
```

Each `F_x` has bidegree at most `(1,1)` on
`P^1_gamma x P^1_tau`. The source shared-component trichotomy separates:

1. fixed-slope vertical components;
2. fixed-owner horizontal components;
3. common irreducible `(1,1)` components, the coordinate-clone cell.

Identically zero coordinate equations are fixed-owner coordinates. Route
those and the vertical/horizontal branches separately before applying this
theorem.

For one irreducible `(1,1)` component `V(F_C)`, let `C` be all coordinates
whose nonzero coordinate curve contains it, and put `c=|C|`. Since the curve
has the full allowed bidegree, every `F_x` in the class is a scalar multiple
of `F_C`. Distinct clone classes are therefore disjoint coordinate sets.

## Theorem: simultaneous subcritical clone payment

Assign each rich parameter point lying on more than one clone component to
one component by any fixed deterministic order. For a clone class with

```text
2 <= c < m,
```

let `N_C` be the number of assigned rich parameter points. Then

```text
N_C(m-c) <= 2(n-c),
N_C <= 2c.                                             (1)
```

Consequently all subcritical clone classes together contribute at most

```text
sum_C N_C <= 2 sum_C c <= 2n = 4194304.               (2)
```

This is below both deployed MCA challenge budgets. Moreover, since `n<2m`,
at most one clone class can have size at least `m`.

### Proof

Fix `C`. Every assigned rich point on `V(F_C)` automatically satisfies the
`c` equations in the clone class and must satisfy at least `m-c` coordinate
equations outside `C`. An outside coordinate curve does not contain
`V(F_C)`. Its intersection number with that component is at most

```text
(1,1).(1,1)=2.
```

Double-counting incidences between the assigned rich points and outside
coordinates gives the first inequality in (1).

For `2<=c<=m-1`,

```text
c(m-c+1) >= 2(m-1) >= n.                              (3)
```

Indeed `c(m+1-c)` is concave in `c` and has endpoint value `2(m-1)` at both
`c=2` and `c=m-1`. The deployed rows satisfy `n<=2(m-1)`. Rearranging (3)
gives

```text
2(n-c)/(m-c) <= 2c,
```

which proves the second inequality in (1). The clone classes are disjoint,
so summation proves (2). The exact budget check is

```text
4194304 < 16777215 < 274980728111395087.
```

Finally, two disjoint classes of size at least `m` would consume at least
`2m>n` coordinates. Thus at most one large class remains.

## Source route and remaining wall

This theorem turns the coordinate-clone branch from an arbitrary collection
of shared components into:

```text
all classes c<m                              [PAID TOGETHER BY 2n]
identically-zero / fixed-owner coordinates  [SEPARATE SOURCE BRANCH]
one possible class c>=m                      [UNIQUE LARGE COMPONENT]
```

The unique large component is the live clone target. On at least `m>k`
coordinates, the four coefficient evaluations

```text
A_0-Q_0r_0,
A_1-Q_1r_0,
B_0-Q_0r_1,
B_1-Q_1r_1
```

are pointwise proportional to one common `(1,1)` coefficient vector. The
proportionality scalar may vary with the coordinate; treating it as constant
would be invalid. A completion must force a coherent owner/global affine
line or assign the resulting positive-dimensional component to `(S)` with
the same received-line owner retained.

There is a second, subtler non-implication. The shared equation
`F_x(gamma,tau)=0` records equality with the rational owner line, not
membership of `x` in the selected agreement support. The atom identity is

```text
Q_tau h + c Lambda = A_tau + gamma B_tau,
```

and hence, even at `Q_tau(x)!=0`, the clone equation yields
`Q_tau(x)(h-r_gamma)(x)=-c Lambda(x)`. It gives an actual agreement only
when the selected locator vanishes as well. Thus the automatic `c>=m`
curve zeros cannot be treated as a common support, and the varying
denominator-root sets do not inject the clone slopes into coordinates. Any
large-class continuation must retain the locators or construct an explicit
same-owner `(S)`/`(A)` route from the coefficient proportionality.

## Nonclaims

- No payment of identically-zero, vertical, or horizontal branches.
- No payment or absorption of the unique class with `c>=m`.
- No conversion of shared owner-line zeros into selected support roots.
- No permission to add `2n` to unrelated first-match costs without an exact
  allocation.
- No complete coordinate-clone or exception routing `(E)`.
- No adjacent-row closure or official score movement.

The universal proof is the argument above. The companion verifier checks
the exact row inequalities, finite-field bidegree intersection seams, the
all-class budget, and hostile metadata mutations under normal and optimized
Python.
