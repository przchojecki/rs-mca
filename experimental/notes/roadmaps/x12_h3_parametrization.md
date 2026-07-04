# X12-H3: rational parametrization of active cores

- **DAG node:** `active_core_count_bound`.
- **Status:** PROVED auxiliary lemma for the `h=3` terminal-node route.
- **Verifier:** `experimental/scripts/verify_x12_h3_parametrization.py`.
- **Certificate:**
  `experimental/data/certificates/x12-h3-parametrization/x12_h3_parametrization.json`.

## Statement

Let `H = mu_n` in a field of odd characteristic and let

```text
P = {1, a, b},        a,b in H,        1,a,b distinct.
```

An ordered triple `(x,y,z)` has the same top two elementary symmetric sums as
`P` exactly when

```text
x + y + z      = 1 + a + b,
xy + xz + yz   = a + b + ab.
```

Every nontrivial affine solution with `x != 1` is obtained from one parameter
`t` by

```text
D  = t^2 + t + 1,

x(t) = (-a t + b t + b + t^2 + t) / D,
y(t) = ( a t + a + b t^2 + b t - t) / D,
z(t) = ( a t^2 + a t - b t + t + 1) / D,
```

with `D != 0`.  Conversely, whenever `D != 0`, the three displayed rational
functions have the same first two elementary symmetric sums as `{1,a,b}`.

Therefore the `h=3` active-core problem reduces exactly to the subgroup
incidence problem:

```text
a, b in H,
x(t), y(t), z(t) in H,
{x(t), y(t), z(t)} disjoint from {1,a,b},
D(t) != 0,
```

modulo the finite ordering multiplicity of the partner triple.

## Cubic Cap Corollary

For `h=3`, the weakest terminal-node rung L3 is already proved:

```text
# anchored active pairs < n^3.
```

Indeed, fix the anchored core `{1,a,b}`.  A partner produced by the
parametrization has `x(t) in H`, so

```text
Nx(t)^n - D(t)^n = 0.
```

This is a nonzero polynomial.  If it vanished identically, then over the
algebraic closure `Nx = zeta D` for some `n`-th root of unity `zeta`; the
leading coefficients force `zeta = 1`, and then

```text
Nx - D = (b-a)t + (b-1)
```

would force `a=b=1`, impossible for a valid core.

Thus each fixed anchored core has at most `2n` possible slope parameters.
There are `C(n-1,2)` anchored cores, so

```text
C(n-1,2) * 2n = n(n-1)(n-2) < n^3.
```

The bound counts all active pairs, before any toral/full-strip removal, so it
also bounds the fully stripped `h=3` residue.

## Proof

Put

```text
S = 1 + a + b,        E = a + b + ab.
```

Eliminating `z` from the two equations gives the conic

```text
F(x,y) = x^2 + xy + y^2 - Sx - Sy + E = 0.
```

The known point `(1,a)` lies on this conic.  Parametrize the line through that
point by

```text
y = a + t(x - 1).
```

Substitution factors as

```text
F(x, a+t(x-1))
  = (x - 1) * ((t^2+t+1)x - (-a t + b t + b + t^2 + t)).
```

The root `x=1` is the base point.  If a second affine intersection exists and
is not the vertical trivial point, then `D=t^2+t+1` is nonzero and the second
root is the displayed `x(t)`.  Then `y(t)` is obtained from the line equation
and `z(t)=S-x(t)-y(t)`, giving the displayed formulas.

The forward identities are

```text
Nx + Ny + Nz = (1+a+b)D,
Nx Ny + Nx Nz + Ny Nz = (a+b+ab)D^2,
```

where `Nx, Ny, Nz` are the three numerators.  Hence division by `D` gives the
same `(e1,e2)` as `P`.

If a disjoint partner triple has `x=1`, then the remaining two entries must
have the same sum and product as `{a,b}`, hence are `{a,b}`.  So no disjoint
partner is lost by requiring `x != 1`.  Thus every active `h=3` partner is
captured by the rational parametrization after choosing an ordering of `Q`.

## Verifier Coverage

The verifier checks:

```text
1. the conic-line factorization symbolically;
2. the two numerator identities symbolically;
3. every active pair in the boundary rows F_17921/mu_128 and F_65537/mu_256
   is recovered by the formula;
4. the denominator is nonzero on every observed active pair;
5. a small forward exhaustive run over F_97/mu_16.
```

The active boundary replay reproduces the X-12 counts:

```text
F_17921 / mu_128: 18 active anchored pairs
F_65537 / mu_256: 129 active anchored pairs
```

and every checked active core has one partner.

The verifier also checks the cubic-cap arithmetic at representative `n`,
including `n=1024`.

## Verification

Run:

```bash
python3 experimental/scripts/verify_x12_h3_parametrization.py
```

To refresh the certificate:

```bash
python3 experimental/scripts/verify_x12_h3_parametrization.py --write-certificate
```

Current replay: **23 PASS, 0 FAIL**.
