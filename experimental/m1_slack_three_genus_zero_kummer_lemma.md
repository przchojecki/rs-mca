# M1 Slack-Three Genus-Zero Kummer Lemma

**Status:** CONDITIONAL / AUDIT.

## Claim

Assume the standard genus-zero multiplicative Weil bound on `P^1`. Then the
slack-three first-superboundary conic has the character-sum constants used in
`m1_slack_three_first_superboundary_theorem.md`.

Let `p>3`, and let

```text
C : U^2 + V^2 + UV + UZ + VZ + Z^2 = 0
```

with `W=-U-V-Z`. On the affine chart `Z=1`, write

```text
u=U/Z,        v=V/Z,        w=W/Z,
beta=-(1+uvw)=-(Z^3+UVW)/Z^3.
```

Let `D <= F_p^*` have index `e`, let `H=D^3`, and put
`h=[F_p^*:H]`. Choose compatible characters `chi` and `psi` with kernels
`D` and `H`.

For every nonprincipal tuple `(a,b,c) mod e`,

```text
S_{a,b,c} = sum_{C(F_p)} chi^a(u) chi^b(v) chi^c(w)
```

satisfies

```text
|S_{a,b,c}| <= 6 sqrt(p).
```

For every nonprincipal tuple `(a,b,c,d)` in the cube-coset expansion,

```text
S_{a,b,c,d} =
  sum_{C(F_p)} chi^a(u) chi^b(v) chi^c(w) psi^d(beta)
```

satisfies

```text
|S_{a,b,c,d}| <= 12 sqrt(p).
```

Characters are extended by zero, so the displayed sums omit the zeros and
poles of the relevant rational functions.

## Genus-Zero Input

The imported one-dimensional theorem is the usual Kummer bound on `P^1`:
if `lambda` is a nontrivial multiplicative character of order `m`, and
`f` is a rational function on `P^1` that is not an `m`-th power over
`\overline{F}_p`, then

```text
|sum lambda(f(t))| <= (R-2) sqrt(p),
```

where `R` is the number of geometric points in the zero-pole support of
`div(f)`.

Since `C` is a smooth conic for `p>3`, it is geometrically `P^1`, so this
input applies to rational functions on `C`.

## Divisor Audit

The four lines

```text
U=0,        V=0,        W=0,        Z=0
```

each meet `C` in a degree-two geometric divisor. These four degree-two
divisors are pairwise disjoint on `C`: imposing any two of the four linear
conditions forces the zero projective point or a nonzero square term.

Thus the zero-pole support of `u^a v^b w^c` is contained in the three
coordinate zero divisors and the common pole divisor at infinity. It has
support size at most `8`.

If `(a,b,c)` is nonzero modulo `e`, one of the three coordinate zero divisors
has coefficient nonzero modulo `e`. Hence `u^a v^b w^c` is not an `e`-th
power on `C`, and the Kummer bound gives

```text
(8-2) sqrt(p) = 6 sqrt(p).
```

For the cube-coset expansion, combine the characters through `psi`. Since
`H=D^3`, the order `h` is a multiple of `e`, and `chi` may be chosen as a
power of `psi`. The relevant rational function is therefore

```text
u^{r a} v^{r b} w^{r c} beta^d,        r=h/e.
```

The numerator of `beta` is the cubic

```text
B = Z^3 + UVW.
```

It has no common component with `C`, so it contributes at most six geometric
zero points. It does not meet the coordinate zero or infinity divisors on
`C`. At `beta=0`, the split-cubic form is

```text
G_0(Y)=Y^3+Y^2+Y+1=(Y+1)(Y^2+1),
```

and the roots are distinct for `p>3`, so these beta-zero points are simple.

If `d` is nonzero modulo `h`, a beta-zero point has divisor coefficient `d`,
which is not divisible by `h`. If `d=0`, a nonzero coordinate exponent gives
the same non-power certificate as above. Therefore every nonprincipal
`(a,b,c,d)` is Kummer-nontrivial.

The support is contained in the six coordinate-zero points, the at-most six
beta-zero points, and the two points at infinity. Thus `R<=14`, and the
Kummer bound gives

```text
(14-2) sqrt(p) = 12 sqrt(p).
```

## Consequences for the Slack-Three Theorem

The conic-count expansion has one principal term and `e^3-1`
nonprincipal terms, so

```text
|C_3(D)| <= ceil((p+1 + 6(e^3-1)sqrt(p))/e^3).
```

The cube-coset expansion has denominator `M=e^3 [F_p^*:D^3]`. Its
nonprincipal terms are bounded by `12 sqrt(p)`, and the degeneracy removal
used in the slack-three ledger costs at most `12` ordered parameters per
denominator bucket. Hence the low-index saturation numerator used there is

```text
p - 9 - 4 chi_2(-3) - (12 sqrt(p)+12) M.
```

This note only isolates the one-dimensional conic input. It does not prove
the remaining two-variable normal-crossing Kummer estimate used by the
slack-two depth-two saturation theorem.
