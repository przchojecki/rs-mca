# M1 Deficiency-One U1-U5 Chart Chain

## Status

PROVED-SYMBOLIC, with an exact finite-field toy replay.

This note packages the roadmap nodes

```text
u1_cramer, u2_nondegeneracy, u3_divisibility, u4_pseudoremainder, u5_dichotomy.
```

It is the local chart theorem consumed by the dimension-one SPI eliminant
packet: a deficiency-one one-parameter Hankel pencil is routed to rank-drop,
low-degree contained, or top pseudo-remainder eliminant/residual.

## Setup

Let `F` be a field and let `H` be the full root set of `X^n-1` in `F`, with
`char(F)` not dividing `n`.  Fix an exact-agreement bucket with

```text
t = A-k,        j = n-A,        t = j.
```

Let

```text
M(Z) = M_0 + Z M_1
```

be a `t x (j+1)` matrix pencil whose entries are affine-linear in `Z`.  For
`0 <= i <= j`, let `M_i(Z)` be the maximal minor obtained by deleting column
`i`, and define

```text
c_i(Z) = (-1)^i M_i(Z),
L_Z(X) = sum_{i=0}^j c_i(Z) X^i.
```

## U1: Cramer Kernel

For every specialization `z`, the signed maximal-minor vector
`c(z)=(c_0(z),...,c_j(z))` satisfies

```text
M(z)c(z) = 0.
```

This is the Laplace expansion of the determinant obtained by appending a copy
of any row of `M(z)`.  If `rank M(z)=t`, then `ker M(z)` is one-dimensional,
so `c(z)` spans the kernel.  If `rank M(z)<t`, all maximal minors vanish, and
this is the rank-drop chart.

## U2: Nondegeneracy

The generic Cramer chart is nondegenerate exactly when some maximal minor is
not the zero polynomial.  Equivalently,

```text
rank_{F(Z)} M(Z) = t.
```

For a declared family, one nonzero minor evaluation `M_i(z_0) != 0` certifies
membership in this chart.  Families with all maximal minors zero are not
failures of U1; they are lower-rank/proportional strata and must be routed
outside this chart.

## U3: Validity Equals Divisibility

On the top chart `c_j(z) != 0`, the locator `L_z(X)` has degree `j`.  Since
`X^n-1` is squarefree with root set `H`, this locator has `j` distinct roots
in `H` if and only if

```text
L_z(X) | X^n - 1.
```

If `rank M(z)=t` but `c_j(z)=0`, the Cramer locator has degree `<j`; it is a
contained higher-agreement branch, not a new exact-`A` degree-`j` contribution.

## U4: Pseudo-Remainder Chart

On the top chart, pseudo-divide

```text
c_j(Z)^delta (X^n - 1) = Q(Z,X)L_Z(X) + R(Z,X),
delta = n-j+1,
R(Z,X) = sum_{m=0}^{j-1} rho_m(Z) X^m.
```

For every `z` with `c_j(z) != 0`,

```text
L_z(X) | X^n - 1    iff    rho_m(z)=0 for all m.
```

Each `c_i(Z)` has degree at most `t`, so every top-chart coefficient satisfies

```text
deg_Z rho_m <= (n-j+1)t.
```

The coarser global one-parameter cap that also covers one rank-drop side
minor is

```text
t + (n-j+1)t.
```

For the pinned `n=512`, `k=256`, `A=384` row, this is
`128 + 385*128 = 49408`.

## U5: Dichotomy

Exactly one of the following holds for the top chart.

```text
(E) Some rho_m is nonzero.
    The valid top-chart slopes are contained in the roots of a nonzero
    eliminant, for instance a nonzero rho_m or the gcd of all rho_m.

(V) Every rho_m is zero in F[Z].
    Then L_Z(X) divides X^n-1 in F(Z)[X], so every top-chart slope is valid.
    This is an identically valid residual branch, not a bounded eliminant.
```

Together with rank-drop and low-degree routing, this proves the U1-U5
deficiency-one chart chain.

## Exact Toy Replay

The verifier replays the chain on two small one-parameter `4 x 5` Hankel
families and uses the `F_97 / mu_16` family as the acid-scale U3-U5 toy.

For `p=97`, `n=16`, `k=8`, `A=12`, the verifier checks all `97` slopes.  It
confirms:

- the Cramer vector spans the RREF kernel at every full-row-rank slope;
- `|mu_16|=16` and `X^16-1` is separable;
- direct divisibility, pseudo-remainder vanishing, and having four roots in
  `mu_16` agree on every top-chart slope;
- the four pseudo-remainder coefficient functions have degree `52`;
- their monic gcd is `1`, so this declared toy top chart is empty.

This toy replay is not evidence for the real `F_17^32` root table.  It is a
machine check that the algebraic gates are wired correctly.

## Scope

This note proves the local deficiency-one chart reduction.  It does not count
the real `F_17^32` roots, does not classify identically valid residuals, and
does not close higher-dimensional SPI.

## Reproducibility

Regenerate:

```bash
python3 experimental/scripts/verify_m1_deficiency_one_u1_u5_chain.py --emit
```

Replay:

```bash
python3 experimental/scripts/verify_m1_deficiency_one_u1_u5_chain.py \
  --check experimental/data/certificates/m1-deficiency-one-u1-u5-chain/m1_deficiency_one_u1_u5_chain.json
```
