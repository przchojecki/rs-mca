# M1 Depth-Two Kummer-Weil Import Contract

**Status:** CONDITIONAL / AUDIT.

This note isolates the remaining non-elementary two-variable character-sum
input used by the M1 slack-two depth-two certificates in
`m1_depth_two_lift_window_theorem.md`. It is not a proof of the imported
estimate; it states the exact import and records which hypotheses are already
checked by the scanner/verifier.

## The Import

Let `p>3`, let `psi` be a multiplicative character of `F_p^*`, extended by
zero at `0`, and put

```text
w = -1-u-v,
A(u,v) = -(u^2 + v^2 + uv + u + v + 1).
```

For exponents `(a,b,c,d)` modulo the order of `psi`, with `d != 0` and at
least two of `a,b,c` nonzero, the imported degree-stratified estimates are

```text
| sum_{u,v in F_p} psi(u^a v^b w^c A(u,v)^d) | <=  9p
    if exactly two coordinate exponents are nonzero,

| sum_{u,v in F_p} psi(u^a v^b w^c A(u,v)^d) | <= 16p
    if all three coordinate exponents are nonzero.              (KW_2)
```

Equivalently, on the Kummer open set

```text
U = A^2 - V(u v (-1-u-v) A(u,v)),
```

the rank-one Kummer sheaf with local monodromy vector `(a,b,c,d)` has total
Frobenius trace bounded by the corresponding active radical-degree constant.

After the one-coordinate reductions below, this is the only non-elementary
estimate still used by the raw, two-fiber, fixed-window, and quotient-window
union saturation certificates. The current ledger applies it with the actual
squarefree radical support of each remaining mixed term: if exactly `r`
coordinate exponents among `a,b,c` are nonzero and `d!=0`, then the active
radical degree is `r+2` and the corresponding conditional constant is
`(r+1)^2`. The external two-variable import is now needed only for
two-coordinate mixed terms, charged by `9p`, and three-coordinate mixed terms,
charged by `16p`. All later coefficients are finite Fourier bookkeeping
around this same input.

When `d=0`, the unrestricted conic factor is absent and the main term is a
three-character Jacobi sum:

```text
sum_{u+v+w=-1} psi^a(u) psi^b(v) psi^c(w).
```

If `(a,b,c)` is not the zero triple, the standard Jacobi-sum recursion bounds
this by `p`. Indeed, after scaling the right side from `-1` to `1`, it is a
constant of modulus at most one times `J(psi^a,psi^b,psi^c)`, and the usual
two-character Jacobi bounds give absolute value at most `p`, including the
cases where one character or the product character is trivial.

In the actual nonzero square-coset expansion, the principal square-coset
character is extended by zero at `A=0`. Thus the `d=0` term is the Jacobi
sum with the conic `A=0` removed. On that smooth conic, the rational
function `u^a v^b w^c` has zero-pole support contained in the three
coordinate line sections and the two points at infinity, so the genus-zero
Kummer bound contributes at most `6 sqrt(p)`. The open-set `d=0` terms are
therefore bounded by `p + 6 sqrt(p)`.

When `d != 0` but `(a,b,c)=(0,0,0)`, the unrestricted sum is conic-only:

```text
sum_{u,v in F_p} psi^d(A(u,v)).
```

This also has an elementary `p` bound. Completing the square at
`u=v=-1/3` gives

```text
A(u,v) = -Q(U,V) - 2/3,
Q(U,V) = U^2 + UV + V^2.
```

The form `Q` is nondegenerate, and with `epsilon=chi(-3)` its value
distribution is

```text
#{(u,v): A(u,v)=-2/3} = p + epsilon(p-1),
#{(u,v): A(u,v)=t}    = p - epsilon        for t != -2/3.
```

Therefore every nontrivial multiplicative character `eta` satisfies

```text
sum_{u,v} eta(A(u,v)) = epsilon p eta(-2/3),
```

so the unrestricted conic-only terms have absolute value exactly `p`. The
Kummer open set also removes the three coordinate lines. On each removed line
`A` restricts to a separable quadratic for `p>3`, and the three pairwise line
intersections contribute only bounded point terms; this is absorbed by
another `6 sqrt(p)` correction. Hence the coordinate-principal `d!=0`
open-set terms are bounded by `p + 6 sqrt(p)`.

The one-coordinate mixed terms also reduce to one-dimensional input. Suppose
first that `d` is the quadratic
character and exactly one coordinate character is nonprincipal, say
`mu(u)`, with the other two coordinate characters principal. First ignore the
two principal-coordinate exclusions `v=0` and `w=0`. For fixed `u`, the
inner sum is a quadratic-character sum in `v` with discriminant

```text
Delta(u) = -3u^2 - 2u - 3.
```

It is constant except at the at most two roots of `Delta`. Since
`sum_u mu(u)=0`, the full unrestricted sum is supported only on those roots
and has absolute value at most `2p`. Restoring the principal-coordinate
exclusions removes the union of two affine lines, which has `2p-1` points.
Hence every one-coordinate/quadratic-conic mixed term has absolute value at
most `4p`; the cases with the nonprincipal character on `v` or `w` follow by
symmetry. The proof-level statement is isolated in
`experimental/m1_depth_two_quadratic_one_coordinate_lemma.md`.

If `d` is nonquadratic, the fixed-`u` inner sum is still explicit. For a
nontrivial nonquadratic character `eta`,

```text
sum_v eta(A(u,v))
  = eta(1/4) J(eta,chi_2) eta(Delta(u)) chi_2(Delta(u)),
```

with the same discriminant `Delta(u)=-3u^2-2u-3`; the right side is also zero
when `Delta(u)=0`, because `eta^2` is nonprincipal. Hence the unrestricted
sum factors as

```text
eta(1/4) J(eta,chi_2)
  sum_u mu(u) chi_2(Delta(u)) eta(Delta(u)).
```

The Jacobi factor has size at most `sqrt(p)`, and the discriminant sum is a
genus-zero Kummer sum with support `u=0`, the two roots of `Delta`, and
infinity, so it has size at most `2 sqrt(p)`. The unrestricted part is
therefore bounded by `2p`, and the principal-coordinate exclusions cost at
most `2p-1`. Thus the nonquadratic one-coordinate mixed terms also satisfy
the `4p` bound. The proof-level statement is isolated in
`experimental/m1_depth_two_nonquadratic_one_coordinate_lemma.md`.

The two-coordinate mixed terms have an exact one-dimensional fiber
decomposition. For example, when `u` and `v` are active and `w` is principal,

```text
S_open = sum_u mu(u) F_{nu,eta}(u) - L_{mu,nu,eta},
F_{nu,eta}(u) = sum_v nu(v) eta(A(u,v)).
```

The line correction `L_{mu,nu,eta}` is a genus-zero Kummer sum on the removed
line `w=0`, with absolute value at most `3 sqrt(p)`. The unresolved
degree-four input is therefore cancellation in the one-dimensional trace
family `sum_u mu(u)F_{nu,eta}(u)`, not the line correction. The same note
isolates the bad-parameter support for this trace family inside
`u=0`, `u^2+u+1=0`, `-3u^2-2u-3=0`, and infinity.

The diagonal reciprocal subfamily `nu=mu^{-1}` reduces further. In this case
the ratio substitution `v=tu` turns the core sum into a genus-zero Kummer sum
in `t`. The proof-level statement is isolated in
`experimental/m1_depth_two_reciprocal_two_coordinate_lemma.md`; it gives a
`4p` core bound for nonquadratic conic characters, a `2p+2 sqrt(p)` core
bound for the quadratic conic character, and the same `3 sqrt(p)` removed-line
correction. This does not close the general two-coordinate wall, but it
removes a structured diagonal slice from the unresolved trace family.
The same note also records the projective form of this reduction: if any two
of the three line monodromies `mu`, `nu`, and `(mu nu eta^2)^(-1)` are
reciprocal, an affine chart turns the core into the reciprocal slice. Thus
the ramified slices `nu eta^2=1` and `mu eta^2=1` are also removed from the
unresolved two-coordinate import.

The projective Euler-characteristic target for the two-coordinate core is
smaller than the crude degree-four `9p` ledger suggests. After compactifying,
the line at infinity has monodromy `(mu nu eta^2)^{-1}`. If this monodromy is
nonprincipal, the active two lines, the conic, and infinity have complement
Euler characteristic `4`; if it is principal, the infinity line drops out and
the complement Euler characteristic is `2`. This calculation is isolated in
`experimental/m1_depth_two_two_coordinate_projective_euler_target.md`. It is
not yet used in the certificates because it still needs the appropriate clean
normal-crossing Kummer cohomology theorem.

The infinity-unramified subfamily `mu nu eta^2=1` no longer needs that
import. The ratio substitution `u=tv`, followed by `r=1/v`, reduces its core
to two genus-zero sums on `P^1_t`; the resulting bound is
`2p+2 sqrt(p)` for the core plus the same `3 sqrt(p)` removed-line
correction. This proof is isolated in
`experimental/m1_depth_two_infinity_unramified_two_coordinate_lemma.md`.
The remaining two-coordinate dependency is therefore the projective
line/conic case where all three line monodromies are nonprincipal and no pair
among them is reciprocal.

The finite stress scan in
`experimental/m1_remaining_two_coordinate_wall_experiment.md` suggests that
the near-sharp part of this remaining wall concentrates in the equal-line
diagonal subfamily. The symmetric-coordinate reduction in
`experimental/m1_depth_two_equal_line_diagonal_reduction.md` splits that
subfamily into a bounded one-dimensional Jacobi part and a residual
quadratic-discriminant trace, then rewrites the residual as a pullback of a
three-point hypergeometric trace along
`lambda=s^2/(4(s^2+s+1))`. The branch checklist for this pullback has
singular support contained in `s=0`, `s^2+s+1=0`,
`3s^2+4s+4=0`, and infinity. In the same equal-line family, setting
`alpha=mu eta` gives `mu=alpha^(-2)` and `eta=alpha^3`, so the pullback main
has a single-character Kummer normal form; this is a proof-guidance
reduction, not yet a replacement for the `9p` import.
The full-spectrum audit in
`experimental/m1_equal_line_pullback_spectrum_experiment.md` shows that the
unrestricted all-character exact `3p` version of this pullback target is
false. It also gives the fixed-domain character filter
`ord(alpha) | (p-1)n^{-1} gcd(2,n)` and shows that moderate-domain exact
violations can occur with only square-root-sized excess. Any proof should
therefore target a `3p+O(sqrt(p))` top-dimensional bound while keeping the
M1 domain-size arithmetic or the hypergeometric pullback structure visible.
A compactified plane-divisor audit for the same single-character presentation
gives the generic complement-Euler target `5`, so the desired `3p` leading
constant cannot come from a naive surface Kummer estimate.
The corresponding line-sheaf audit shows the same generic obstruction:
after the visible twists, the two `B(s)=0` points each have no local
invariants and cost two conductor units, giving generic `dim H^1 <= 5`.
The desired `3p` leading constant therefore requires an additional
two-unit saving beyond the standard local conductor count.
The pullback deck involution `tau(s)=-s/(s+1)` swaps the two `B(s)=0`
points, but the twist changes by `rho((s+1)^(-2))`, so the needed saving is
not an immediate deck-symmetry consequence.
In the quotient coordinate `z=s/(s+2)`, the paired sum introduces the
auxiliary trace `sum_{z^2=q} alpha^(-2)(1-z)`; this is the concrete object
that must supply any additional cancellation.
Equivalently, before quotienting by `z -> -z`, the equal-line twist completes
to the balanced kernel
`chi_2(1+3z^2) alpha((1+3z^2)/(1-z)^2)`. This has no Kummer zero or pole at
`z=infinity`, and the pullback main differs from the complete `z`-line sum
only by the regular fibers `H(1/4)` and
`alpha(3) chi_2(3) H(1/3)`.

Thus the fixed-window, quotient-window, and two-fiber certificates still use
the conservative common ledger:

```text
d=0, coordinate nonprincipal:               p + 6 sqrt(p)
d!=0, coordinate principal:                 p + 6 sqrt(p)
d quadratic, exactly one coordinate active: 4p   (elementary)
d nonquadratic, exactly one coordinate:     4p   (one-dimensional)
d!=0, two coordinates active:               9p   (degree 4 Kummer)
d!=0, three coordinates active:            16p   (degree 5 Kummer)
```

The raw full-domain certificate additionally splits the two-coordinate mass
by projective line monodromy. The exact `mu nu eta^2=1` mass pays the proved
open-set bound `2p+5 sqrt(p)`, the ramified projective-reciprocal mass pays
`4p+3 sqrt(p)`, and only the ramified nonreciprocal remainder pays the
imported `9p` constant.

The finite audit

```bash
python3 experimental/verify_m1_depth_two_elementary_open_set_lemma.py
python3 experimental/verify_m1_depth_two_quadratic_one_coordinate_lemma.py
python3 experimental/verify_m1_depth_two_nonquadratic_one_coordinate_lemma.py
python3 experimental/verify_m1_depth_two_reciprocal_two_coordinate_lemma.py
python3 experimental/verify_m1_depth_two_infinity_unramified_two_coordinate_lemma.py
python3 experimental/verify_m1_depth_two_equal_line_diagonal_reduction.py
python3 experimental/verify_m1_depth_two_kummer_constant_audit.py
python3 experimental/verify_m1_kummer_divisor_geometry.py
python3 experimental/verify_m1_depth_two_two_coordinate_fiber_reduction.py
python3 experimental/verify_m1_depth_two_two_coordinate_sharp_target.py
```

checks the finite geometry behind the elementary open-set correction and
the one-coordinate slice lemmas, verifies the two-coordinate fiber reduction,
and exhausts representative small prime/index cases against the exact
character sums. The proof-level statement of the open-set correction is isolated in
`experimental/m1_depth_two_elementary_open_set_lemma.md`; the quadratic and
nonquadratic mixed slices are isolated in
`experimental/m1_depth_two_quadratic_one_coordinate_lemma.md` and
`experimental/m1_depth_two_nonquadratic_one_coordinate_lemma.md`.
The two-coordinate fiber reduction and finite sharp-target audit are isolated
in `experimental/m1_depth_two_two_coordinate_fiber_reduction.md` and
`experimental/m1_depth_two_two_coordinate_sharp_target_audit.md`; the latter
is only finite evidence for a possible future `4p` replacement of the current
conditional `9p` import and is not used by the present certificates.
The reciprocal two-coordinate slice is isolated in
`experimental/m1_depth_two_reciprocal_two_coordinate_lemma.md`.
The projective Euler target for the two-coordinate core is isolated in
`experimental/m1_depth_two_two_coordinate_projective_euler_target.md`.
The infinity-unramified two-coordinate slice is isolated in
`experimental/m1_depth_two_infinity_unramified_two_coordinate_lemma.md`.

## Audited Hypotheses

The scanner and verifier already check the following finite algebraic
conditions.

The radical divisor is reduced with component degrees

```text
1, 1, 1, 2,
```

so its total degree is `5`. The constant used in the certificates is

```text
(5-1)^2 = 16.
```

The three linear factors are distinct for `p>3`, and the conic `A=0` is a
nonzero smooth conic. The conic shares no component with the three lines.

The projective compactification is also elementary. Homogenize with
coordinates `[U:V:Z]`:

```text
Q(U,V,Z) = U^2 + V^2 + UV + UZ + VZ + Z^2.
```

The compactified boundary consists of

```text
U=0,        V=0,        U+V+Z=0,        Z=0,        Q=0.
```

The conic is smooth because its gradient matrix has determinant `4`, which is
nonzero for `p>3`. The four lines are distinct and have six pairwise
intersection points. At all six of these line-line intersections, `Q=1`, so
there is no triple point involving the conic. Restricting `Q` to each of the
four lines gives a binary quadratic with discriminant `-3`; since `p>3`, the
geometric intersections are simple. Thus the compactified divisor is a simple
normal-crossing line/conic arrangement over the algebraic closure.

The finite verifier

```bash
python3 experimental/verify_m1_kummer_divisor_geometry.py
```

checks these line-line, line-conic, smoothness, and transversality identities
on representative primes. It also checks the affine value distribution of
`A`, which is the finite audit behind the conic-only `p` bound. The symbolic
proof above is what matters for the uniform `p>3` statement.

For every imported two-variable mixed character tuple, at least three
component exponents are nonzero: the conic exponent and at least two
coordinate-line exponents.
For every such tuple, at least one component exponent among

```text
u=0, v=0, -1-u-v=0, A=0
```

is nonzero. Hence the Kummer sheaf has nontrivial local monodromy around some
boundary component; equivalently, the summand is not a hidden character power
with trivial divisor data. This is the
`*_divisor_nontriviality_check` audited by
`verify_m1_slack_two_depth_two_kummer_saturation.py`.

The principal term and the elementary admissibility loss are independent of
the import and are computed exactly:

```text
|U(F_p)| = p^2 - 4p + 6 + 4 chi(-3),
```

and the six distinctness-failure lines have union size

```text
6p - 11.
```

## Why This Is Not a Direct Nonsingular Citation

Katz's nonsingular multiplicative character-sum theorem is the right
background source for constants of the form `(degree-1)^n q^(n/2)` in smooth
several-variable settings. However, the M1 divisor is the reducible divisor

```text
u v (-1-u-v) A(u,v)=0,
```

a union of three lines and a conic. It is singular at its crossings. Therefore
one should not cite the nonsingular single-hypersurface theorem as if it
directly applied to this product divisor.

The normal-crossing audit narrows the correct route to either:

1. a tame normal-crossing multiplicative character-sum theorem whose
   conductor/Euler-characteristic bound gives `16p` for this line/conic
   arrangement, or
2. a direct cohomology calculation for the rank-one Kummer sheaf on the above
   five-component compactified complement.

Rojas-Leon's singular multiplicative character-sum estimates are a plausible
reference class for this step, but the exact constant must still be checked
before the PR's conditional status can be upgraded to proved.

## Replacement Constant Ledger

If a later proof supplies

```text
|S(a,b,c,d)| <= C p
```

instead of `16p`, all M1 depth-two certificates remain valid after replacing
the scanner parameter `nonprincipal_constant=16` by `C` for the
three-coordinate degree-five part. The one- and two-coordinate Kummer
constants remain the degree-three and degree-four values `4` and `9` unless a
future import ledger replaces those separately. The verifier already checks
that the reported radical degree, nontriviality audit, active-coordinate L1
ledger, lower numerators, and thresholds are internally consistent for the
chosen constants.

Thus the import dependency is narrow: the rest of PR #79 is finite
character-expansion algebra, exact quotient-window reduction, and exact L1
coefficient accounting.

## Source Pointers

- Nicholas M. Katz, *Estimates for nonsingular multiplicative character
  sums*, International Mathematics Research Notices 2002, no. 7, 333-349,
  DOI `10.1155/S1073792802106088`.
- Antonio Rojas-Leon, *Estimates for singular multiplicative character
  sums*, International Mathematics Research Notices 2005, no. 20, 1221-1234,
  DOI `10.1155/IMRN.2005.1221`.
