# M1 Depth-Two Kummer-Weil Import Contract

**Status:** CONDITIONAL / AUDIT.

This note isolates the remaining non-elementary two-variable character-sum
input used by the M1 slack-two depth-two certificates in
`m1_depth_two_lift_window_theorem.md`. It is not a proof of the imported
estimate; it states the exact import and records which hypotheses are already
checked by the scanner/verifier.  It also records the newer rank-two
beta-pushforward import isolated by
`m1_depth_two_line_conic_resonance_reduction.md`; that import is separate
from the raw `KW_2` line/conic arrangement below and is not consumed unless
explicitly stated.

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

The line-conic-resonant part of that dependency is now separated as
`C_2^lc`.  In a chart where `mu eta=1`, the core has the exact transform

```text
sum_{u,v} eta^(-1)(u) nu(v) eta(A(u,v))
  = sum_y eta(-y) sum_v nu(v)
      chi_2(y^2 - 2(v+1)y - 3v^2 - 2v - 3).
```

This is recorded in
`experimental/m1_depth_two_line_conic_resonance_reduction.md`.  Its
quadratic-fiber discriminant is `16(y-2)(y+1)`, and the candidate singular
support on the `y`-line is `{0,-1,2,3,infinity}`.  Thus the resonant
asymmetric slice is also a one-dimensional conductor problem; the clean
two-variable normal-crossing target is the nonresonant complement `C_2^anr`.
The explicit conditional replacement needed for the resonant slice is
`|C_{eta,nu}|<=4p` for the transformed core.  Together with its already
proved genus-zero line correction, this gives `4p+3sqrt(p)` on the open
line-conic-resonant terms.  The raw scanner reports this as the
`projective_equal_pair_all_asymmetric_conditional_*` ledger: if the
projective equal-pair, nonresonant, and line-conic-resonant conductor imports
are all accepted, the full residual asymmetric mass
`C_2^asym=C_2^anr+C_2^lc` is charged at the same `4p+3sqrt(p)` rate as
`C_2^peq`.  This remains conditional and is not consumed by the active
certificate.

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
constant cannot come from a naive surface Kummer estimate.  The
hypergeometric line-sheaf audit supplies the missing structure: in the
standard `2F1(chi_2,mu;alpha;t)` normalization, the `t=0` local characters
are `1` and `alpha^(-1)`, not the numerator characters.  After the visible
twists, each `B(s)=0` point has local characters `alpha` and `1`, so it has
one inertia invariant and costs only one conductor unit.  The corrected
line-sheaf ledger is `1+2+2+2=7` for rank `2`, hence
`dim H^1 <= 3`.
The pullback deck involution `tau(s)=-s/(s+1)` swaps the two `B(s)=0`
points, but the twist changes by `rho((s+1)^(-2))`; the conductor saving
comes from the local `2F1` table, not from bare deck symmetry.
In the quotient coordinate `z=s/(s+2)`, the paired sum introduces the
auxiliary trace `sum_{z^2=q} alpha^(-2)(1-z)`; this is the concrete object
that must supply any additional cancellation.
Equivalently, before quotienting by `z -> -z`, the equal-line twist completes
to the balanced kernel
`chi_2(1+3z^2) alpha((1+3z^2)/(1-z)^2)`. This has no Kummer zero or pole at
`z=infinity`, and the pullback main differs from the complete `z`-line sum
only by the regular fibers `H(1/4)` and
`alpha(3) chi_2(3) H(1/3)`.
The corrected completed-line conductor ledger is `1+2+2+2+0=7`: the old
infinity twist is moved to the finite regular point `z=1`, where the scalar
twist is `alpha^(-2)`, and the two `1+3z^2=0` points now each have one
invariant after the visible twists.
There is also a useful pushforward form: with
`y=(1+3z^2)/(1-z)^2`, the balanced kernel is simply
`(alpha chi_2)(y)`, and the projective completed trace is
`sum_{y in F_p^*} (alpha chi_2)(y) G(y)`, where the two lambda-values in a
generic fiber satisfy
`16y^2 lambda^2 + (-8y^2+4y)lambda + (y-1)^2=0`.
After interchanging the hypergeometric sum with the finite `y`-fiber, the
outer quadratic character cancels and the finite kernel has the single
quadratic factor `x+(3x-1)z^2`; the fiber resultant is
`16x^2y^2-8xy^2+4xy+y^2-2y+1`.
Compactifying that resultant in `P^1_x times P^1_y` gives a nodal bidegree
`(2,2)` curve with an ordinary node at `(x,y)=(infinity,0)`. Including the
boundary lines `x=0,1,infinity`, `y=0,infinity,3/4` gives complement Euler
target `6`, so the explicit two-variable kernel surface still does not
replace the imported line-sheaf/pushforward input.
The sharper one-dimensional pushforward support is generically the six
geometric values `y=0`, `y=1`, the two roots of `9y^2+2y+1`, `y=3/4`, and
`y=infinity`; `y=3` is an ordinary projective fiber except in the small
collision characteristic `p=11`.
The corrected local pushforward ledger after the Mellin twist is
`2+1+2+2+4=11` for rank `4`, hence `dim H^1 <= 3`.  This is the same
top-dimensional `3p` target in y-pushforward form.

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
Inside that final remainder, the equal-line diagonal submass is now audited
exactly:

```text
C_2^eq =
  3 # {a,d : 1<=a<e, 1<=d<q,
        3ga+2d == 0 mod q,
        2ga != 0 mod q},        g=q/e.
```

The corrected equal-line conductor ledger charges the residual part of this
submass by `3p`, but the full two-coordinate open sum also contains the
Jacobi term.  Thus the certificate-facing replacement is `4p+3sqrt(p)`
instead of `9p`, dropping the leading L1 weight by `5C_2^eq` and adding
square-root L1 mass `3C_2^eq`.  The verifier reports this as a conditional
alternative ledger, while the active certificate constants stay unchanged
until this standard `2F1` local-monodromy import is accepted as
theorem-grade.

The same symmetric-coordinate reduction covers the larger coordinate-diagonal
submass where the two active coordinate-line monodromies are equal, but the
line at infinity is not necessarily equal to them.  A projective chart change
extends this again to the mass `C_2^peq` where any two projective line
monodromies are equal; inclusion-exclusion gives
`C_2^peq = 3C_2^diag - 2C_2^eq`.  This broader slice now has the same
conditional `4p+3sqrt(p)` ledger: in the ramified diagonal chart,
`alpha^2=1` would force trivial infinity monodromy, and the possible `2F1`
cancellations `alpha=mu` or `alpha=chi_2` are excluded.  The finite local
conductor entries are uniform as well: the `s=0` character is `mu^2` after
the quadratic pullback, and the `mu^2=1` cases are precisely the projective
reciprocal terms already removed; the two `C(s)=0` roots cost at most one
each.  The active certificate remains conservative, but the reported
conditional ledger now includes the full `C_2^peq` mass, not only `C_2^eq`.
After removing `C_2^0`, `C_2^rec`, and this projective equal-pair mass, the
reported residual two-coordinate wall is the asymmetric mass
`C_2^asym=C_2-C_2^0-C_2^rec-C_2^peq`.  Its projective line monodromies are
nonzero, pairwise distinct, and have no reciprocal pair, so the projective
line-permutation action is free and the verifier records
`O_2^asym=C_2^asym/6`.
The later line-conic split writes
`C_2^asym=C_2^lc+C_2^anr`, where `C_2^lc` is the resonant transform family
above and `C_2^anr` is the clean nonresonant normal-crossing wall.
The optional all-asymmetric ledger further assumes the `C_2^lc` transformed
core bound `4p`, so that both asymmetric pieces can be charged by
`4p+3sqrt(p)`.

### `2F1` Local-Monodromy Import Consumed by the Equal-Line Audit

The equal-line conductor saving uses the following narrow standard input.
For the Gauss normalization

```text
2F1(A,B;C;t),
```

the tame local characters at `t=0` are

```text
1,        C^(-1).
```

Equivalently, the local exponents are `0` and `1-C`.  Katz's finite-field
hypergeometric-sheaf convention gives the same table after translating this
Gauss normalization to a `Hyp_psi(chi_i;rho_j)` sheaf: the semisimplified
tame local monodromy at `0` is the direct sum of the numerator characters
`chi_i`.  Katz, *Exponential Sums and Differential Equations*, 8.4.2(5), is
the underlying source; Katz--Tiep restate the convention in their
hypergeometric-sheaf monodromy paper.

In the present M1 equal-line normalization,

```text
H(lambda) = const * chi_2(-lambda)
  * 2F1(chi_2, mu; alpha; 1/lambda),
```

so at a root of `B(s)=0`, with `t=1/lambda` a local parameter, the imported
characters are

```text
1,        alpha^(-1).
```

After the visible factor `chi_2(t)` and the outer twist
`rho(B(s))=alpha chi_2(B(s))`, the two characters become

```text
alpha,        1.
```

Thus each `lambda=infinity` branch has exactly one inertia invariant and
costs one tame conductor unit.  This is the sole imported fact behind the
corrected rank-two ledgers `1+2+2+2=7` and `1+2+2+2+0=7`, and the
rank-four pushforward ledger `2+1+2+2+4=11`.  It does not by itself change
the active certificate constants; it records the exact theorem that must be
accepted before the audited `C_2^peq` improvement is promoted from the
conditional ledger into the consumed certificate.

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

## Beta-Pushforward Import (`BETA_2`)

The line-conic-resonance reduction has isolated a second, narrower import for
the quotient-conic singular-excess route.  Work over `F_p`, fix a quotient
order `e | p-1`, and let `psi,phi` be multiplicative characters of
`F_p^*/K_e` with `phi != 1`.  On the good base

```text
G = {(a,r): A_beta C_beta D_beta (a-r)K_alpha != 0} <= G_m^2
```

consider the two-sheet beta cover

```text
Y_G: A_beta beta^2 + B_beta beta + C_beta = 0.
```

The trace sheaf on `Y_G` is the tame rank-one Kummer sheaf

```text
K_{psi,phi}
  = psi(a) phi(beta) chi(d_UV(a,beta,r)).
```

The imported estimate is:

```text
| sum_{(a,beta,r) in Y_G(F_p)} K_{psi,phi}(a,beta,r) |
  <= C_beta(e) p.                                      (BETA_2)
```

Equivalently, the rank-two pushforward `pi_! K_{psi,phi}` to the `(a,r)`-base
has bounded conductor depending only on `e`, has no geometrically constant
summand when `phi != 1`, and its compactly supported trace is `O_e(p)`.

The elementary hypotheses behind this import are now audited in
`verify_m1_depth_two_line_conic_resonance_reduction.py`:

- the beta cover is rank two on the good base, with branch divisor
  `D_beta=alpha*r*M*H`;
- the branch curves `M=0` and `H=0` are rational, are disjoint in the torus
  away from the separated point `(1,1)` for `p>5`, and are smooth away from
  that same separated point;
- the boundary pile-up at `(1,1)` is resolved by the fixed two-chart blow-up
  `r=1+t(a-1)` and `a=1+s(r-1)`: after removing exceptional powers, the strict
  transforms of `A_beta`, `Q_beta=C_beta/(ar)`, `K_alpha`, `a-r`, `M`, and `H`
  have explicit factors in both charts, and all pairwise intersections lie on
  the displayed finite slope-resultant supports;
- for every audited `p>5`, those strict transforms are smooth in both blow-up
  charts; characteristic `5` has only isolated `A_beta`/`Q_beta` strict-transform
  singularities and is already treated as a finite special case;
- for every audited `p>5`, the only open-torus nontransverse incidences after
  the blow-up are the four explicit tangencies
  `(A_beta,M)`, `(A_beta,H)`, `(Q_beta,M)`, `(Q_beta,H)`; there are no
  open-torus triple points, and the sole triple-or-higher point in each chart is
  the toric corner over `(a,r)=(0,0)`;
- on the good base, `D_beta != 0` and
  `(2A_beta beta+B_beta)^2=D_beta` at every beta root, so the projection
  `Y_G -> G` is finite etale of degree two; since `G` is an open subset of
  the torus, `Y_G` is smooth;
- equivalently, with `y=2A_beta beta+B_beta`, the good cover is the standard
  square-root cover `y^2=D_beta` and
  `beta=(y-B_beta)/(2A_beta)`, so the trace can be written as the base twist
  `psi(a)chi(rM)phi((2A_beta)^(-1))` times
  `sum_{y^2=D_beta} phi(y-B_beta)`;
- in this normalized model, the vertical projection to the `r`-line has
  branch polynomial `P_r(a)=aM(a,r)H(a,r)` with discriminant
  `51840000 r^8(r-1)^12(r^2+r+1)(9r^2+14r+9)`, and its intersections with
  `A_beta`, `Q_beta`, `K_alpha`, `a-r`, and `B_beta/(ar)` occur only over the
  displayed fixed `r`-supports; hence the remaining import has no hidden
  unbounded family of bad vertical fibers;
- the deleted lower-chart and exceptional main-chart loci are curve-sized;
  more sharply, in centered rows the zero conic plus vertical beta tail costs
  at most `p`, the lower chart costs at most `5(p-1)`, and the nonvertical
  exceptional main-chart roots cost at most `14(p-1)`, giving the uniform
  bad-ledger bound `|S_{psi,phi}-G_{psi,phi}| < 20p`;
- the beta-zero boundary
  `Q_beta=-2a^2r+3ar^2-ar+3a-3r=0` carries nontrivial local monodromy `phi`;
- the beta-infinity boundary `A_beta=0` carries nontrivial local monodromy
  `phi^{-1}`; the quadratic pole of `d_UV` is invisible to `chi`, and the
  leading coefficient is `r(4a-3r)`;
- `Q_beta=0` has no common component with `B_beta`, `d_UV`, `A_beta`, `M`,
  `H`, `a-r`, or `K_alpha`, by the explicit resultants recorded in
  `m1_depth_two_line_conic_resonance_reduction.md`;
- `A_beta=0` has no common component with `B_beta`, `C_beta`, the
  beta-infinity leading `U V` coefficient, `M`, `H`, `a-r`, or `K_alpha`,
  by the corresponding explicit resultants recorded there;
- the finite `U V` sign divisor is absent on the good cover:
  `Res_beta(A_beta beta^2+B_beta beta+C_beta, d_UV/r)
   = a^2 r^2 (a-r)^2 K_alpha^2`, so every finite `d_UV=0` point is already on
  the deleted diagonal or lower-chart curve;
- more strongly, the descended quadratic sign is the explicit base twist
  `chi(d_UV)=chi(rM)=chi(aH)` on the good cover, by the cleared square
  identities `M^2 d_UV=rM N_M^2` and `H^2 d_UV=aH N_H^2`;
- the determinant of the rank-two good pushforward is the base Kummer
  character `psi^2 phi(C_beta/A_beta)`, since
  `beta_1 beta_2=C_beta/A_beta` and the descended quadratic sign occurs on
  both sheets;
- the verifier checks that the finite intersections lie in those displayed
  resultant root supports.

Thus the only remaining non-elementary input in `(BETA_2)` is the standard
bounded-conductor Deligne--Katz/Rojas-Leon style trace estimate for this
explicit tame rank-two pushforward.  If `(BETA_2)` is accepted, then

```text
||Gamma_e^circ||_F = O_e(p),   P_e = O_e(p^2),   M_e^o = O_e(p^2),
```

by the quotient-character Parseval and closed-boundary reductions in
`m1_depth_two_line_conic_resonance_reduction.md`.

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

- Nicholas M. Katz, *Exponential Sums and Differential Equations*, Annals of
  Mathematics Studies 124, Princeton University Press, 1990, especially
  8.4.2 for the hypergeometric sheaf local-monodromy table.
- Nicholas M. Katz and Pham Huu Tiep, *Monodromy groups of Kloosterman and
  hypergeometric sheaves*, Geometric and Functional Analysis 31 (2021),
  562-660, Section 1B, restating the `Hyp_psi(chi_i;rho_j)` local
  monodromy convention from Katz 8.4.2.
- Nicholas M. Katz, *Estimates for nonsingular multiplicative character
  sums*, International Mathematics Research Notices 2002, no. 7, 333-349,
  DOI `10.1155/S1073792802106088`.
- Antonio Rojas-Leon, *Estimates for singular multiplicative character
  sums*, International Mathematics Research Notices 2005, no. 20, 1221-1234,
  DOI `10.1155/IMRN.2005.1221`.
