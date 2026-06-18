# M1 Depth-Two Equal-Line Diagonal Reduction

**Status:** CONDITIONAL / AUDIT.

## Claim

Let `p>3`, put

```text
w=-1-u-v,
A(u,v)=-(u^2+v^2+uv+u+v+1),
B(s)=s^2+s+1,
```

and extend multiplicative characters by zero at `0`. Let `mu`, `eta`, and
`mu eta` be nonprincipal. Define the diagonal two-coordinate open sum

```text
S_open(mu,eta) =
  sum_{u,v in F_p} mu(u) mu(v) 1_{w!=0} eta(A(u,v)).
```

Then

```text
S_open(mu,eta) =
  J^-(mu,eta) sum_{s!=-1} (mu eta)(B(s))
  + R(mu,eta),
```

where

```text
J^-(mu,eta) = sum_t mu(t) eta(t-1),

R(mu,eta) =
  sum_{s!=-1} sum_t
    chi_2(s^2-4t) mu(t) eta(t-B(s)).
```

The first term is already one-dimensional and satisfies

```text
|J^-(mu,eta) sum_{s!=-1} (mu eta)(B(s))|
  <= p + sqrt(p).
```

Thus, in the equal-line-monodromy subfamily, the remaining analytic work is
concentrated in the residual trace `R(mu,eta)`.

The residual trace has a further one-parameter form. Let

```text
rho = mu eta chi_2,
lambda(s) = s^2 / (4B(s)),
H(lambda) = sum_x mu(x) eta(x-1) chi_2(x-lambda).
```

Then

```text
R(mu,eta) =
  chi_2(-4) sum_{s!=-1, B(s)!=0} rho(B(s)) H(lambda(s))
  + E_B(mu,eta),
```

where `E_B` is supported on the at most two roots of `B(s)=0`, and

```text
|E_B(mu,eta)| <= 2 sqrt(p).
```

The identities in this first section do not use the equal-line monodromy
relation.  They apply to every coordinate-diagonal two-coordinate term,
namely every active pair with the same coordinate character on the two active
lines.  The equal-line condition is a further specialization used later to
collapse the residual pullback to a single-character `alpha` form and to
identify the exact certificate submass `C_2^eq`.

## Equal-Line Monodromy

For the canonical active pair `(a,b,c)=(a,b,0)`, use a common character order
`h` and let the coordinate-character lift be `g=h/e`. The projective line
monodromies on the two active coordinate lines and infinity have exponents

```text
ga,        gb,        -(ga+gb+2d)       mod h.
```

The equal-line diagonal case is therefore

```text
a=b,        2d + 3ga == 0 mod h.
```

When `h=2e`, this is the congruence seen in the numerical stress scan:

```text
d == -3a mod e.
```

In character notation this says

```text
mu^3 eta^2 = 1.
```

Let

```text
alpha = mu eta.
```

Then the equal-line relation gives the single-character normal form

```text
mu = alpha^(-2),        eta = alpha^3,        rho = alpha chi_2.
```

Thus `alpha` and `alpha chi_2` are nonprincipal in the remaining-wall case:
if `alpha=1`, then `eta=mu^{-1}` is reciprocal; if `alpha=chi_2`, then
`mu=1`.

If also `mu eta=1`, then `eta=mu^{-1}` and the equality above forces
`mu=1`, contradicting the two-coordinate hypothesis. Hence the Jacobi
factor in the reduction is nondegenerate throughout the equal-line
remaining-wall family.

## Proof of the Reduction

Set

```text
s=u+v,        t=uv.
```

For fixed `(s,t)`, the number of ordered pairs `(u,v)` with
`u+v=s` and `uv=t` is

```text
1 + chi_2(s^2-4t).
```

Moreover

```text
mu(u)mu(v)=mu(t),
A(u,v)=t-B(s),
w!=0  <=>  s!=-1.
```

Therefore

```text
S_open(mu,eta) =
  sum_{s!=-1} sum_t
    (1+chi_2(s^2-4t)) mu(t) eta(t-B(s)).
```

Splitting the `1` and `chi_2` terms gives the displayed formula, except that
the first part is still

```text
sum_{s!=-1} sum_t mu(t) eta(t-B(s)).
```

For `B(s)!=0`, substituting `t=B(s)x` gives

```text
sum_t mu(t) eta(t-B(s))
  = (mu eta)(B(s)) J^-(mu,eta).
```

For `B(s)=0`, both sides are zero because `mu eta` is nonprincipal and is
extended by zero at `0`. This proves the identity.

The bound on the first term is standard: since `mu`, `eta`, and `mu eta`
are nonprincipal, the Jacobi sum has size `sqrt(p)`. The polynomial
`B(s)=s^2+s+1` is separable for `p>3`; the genus-zero Kummer bound gives

```text
|sum_s (mu eta)(B(s))| <= sqrt(p),
```

and deleting the single value `s=-1` costs at most `1`.

## Contribution to the Remaining M1 Wall

The stress scan in
`experimental/m1_remaining_two_coordinate_wall_experiment.md` found that the
largest remaining-wall examples all lie in this equal-line diagonal family.
For the two largest rows, the reduction gives:

```text
(421,20,21,42),  (5,5,0,6):
  |S|/p = 3.9771715522,
  Jacobi part = 1.0485702499p,
  residual R = 2.9290031282p.

(461,20,23,46),  (18,18,0,15):
  |S|/p = 3.9643175123,
  Jacobi part = 1.0465694143p,
  residual R = 2.9412840316p.
```

This suggests the next proof target should be a sharp bound for the residual
quadratic-discriminant trace `R(mu,eta)`, ideally explaining a `3p`
top-dimensional coefficient in the equal-line case.

## Hypergeometric Pullback for `R`

For `B(s)!=0`, scale `t=B(s)x`. Then

```text
chi_2(s^2-4t) mu(t) eta(t-B(s))
  = chi_2(-4) rho(B(s))
    mu(x) eta(x-1) chi_2(x-lambda(s)).
```

This gives the displayed pullback formula. The trace `H(lambda)` is the
three-point hypergeometric trace with moving branch point `lambda`; the
outer variable only sees its pullback along

```text
lambda = s^2 / (4(s^2+s+1)).
```

If `B(s)=0`, then `s!=0` and the inner residual fiber is

```text
sum_t chi_2(s^2-4t) (mu eta)(t)
  = (mu eta)(s^2/4) J(mu eta, chi_2).
```

In the equal-line remaining-wall case, both `mu eta` and `mu eta chi_2` are
nonprincipal. Hence each exceptional fiber has size `sqrt(p)`, giving the
`2 sqrt(p)` bound above.

For the two largest rows, the residual pullback decomposition gives:

```text
(421,20,21,42),  (5,5,0,6):
  residual R = 2.9290031282p,
  pullback main = 2.9043632895p,
  exceptional contribution = 1.0000000000 sqrt(p).

(461,20,23,46),  (18,18,0,15):
  residual R = 2.9412840316p,
  pullback main = 2.9412840316p,
  exceptional contribution = 0.
```

Thus the next geometric target is not the original two-variable surface sum,
but the middle cohomology of this pulled-back three-point hypergeometric
sheaf. A `3p` bound for the pullback main term, plus the exceptional
`2 sqrt(p)` correction, would explain the observed near-`4p` diagonal
examples.

Using the single-character notation `alpha=mu eta`, the pullback main is
equivalently

```text
chi_2(-1) sum_{s!=-1, B(s)!=0} sum_x
  alpha(B(s)) alpha^(-2)(x) alpha^3(x-1)
  chi_2(4B(s)x-s^2).
```

This is the most concrete current form of the near-sharp diagonal problem:
one nonquadratic character `alpha`, one quadratic factor, and the divisor

```text
B(s),        x,        x-1,        4B(s)x-s^2.
```

The finite pullback scanner
`experimental/search_m1_equal_line_pullback.py` directly stress-tests the
target

```text
|M_alpha| <= 3p
```

for this single-character main term. Its report preset exhausts all
equal-line canonical active-pair tuples with `p <= 500` and `e <= 24`.
It tests `4804` tuples and finds no `3p` violation. The largest rows are:

```text
(461,20,23,46),  (18,18,0,15),  alpha=5:
  |M_alpha|/p = 2.9412840316,

(281,20,14,28),  (1,1,0,25),    alpha=27:
  |M_alpha|/p = 2.9391353527,

(397,44,9,18),   (1,1,0,15),    alpha=17:
  |M_alpha|/p = 2.9357869704.
```

The full character-spectrum scanner
`experimental/search_m1_equal_line_pullback_spectrum.py` shows that this
target should not be promoted to all nonquadratic `alpha` without the
M1-admissibility restrictions.  Its report preset scans all primes
`p <= 1601` and all nonquadratic characters, finding `28` violations of the
unrestricted `3p` bound, with top ratio `3.0600680546` at `p=1153`.
The scanner now also audits the exact equal-line character filter: if
`alpha` has order `r`, its maximum possible equal-line domain size is
`2(p-1)/r` for even `r>3`, `(p-1)/r` for odd `r>3`, and `0` for
`r in {1,2,3}`.  In the report preset all exact `3p` violations have
`n_max <= 12`; an extended scan to `p <= 3000` finds one conjugate
`n_max=24` violation at `p=1753`, but its excess over `3p` is only
`0.0655 sqrt(p)`.  Thus the natural proof target is the top-dimensional
bound `3p+O(sqrt(p))`, not a literal exact `3p` inequality.  The report is
recorded in `experimental/m1_equal_line_pullback_spectrum_experiment.md`.

## Plane Divisor Audit

The normalized two-variable Kummer presentation is still too crude if used as
a generic surface estimate.  Compactify the affine variables by

```text
s=S/Z,        x=X/Z
```

in `P^2`, and put

```text
B_h=S^2+SZ+Z^2,
D_h=4B_h X-S^2Z.
```

The `alpha`-part of the divisor is

```text
B_h (X-Z)^3 / (X^2 Z^3),
```

while the quadratic part is

```text
D_h / Z^3.
```

Thus the line at infinity has monodromy `alpha^(-3) chi_2`; it is unramified
only in the special case `alpha^3=chi_2`.  The affine deleted line `s=-1` is
not part of this ramification divisor and is a separate regular-fiber
correction.

Over an algebraic closure, `B_h=0` splits into two lines meeting at

```text
P=[0:1:0].
```

The cubic `D_h=0` is nodal at the same point, with tangent cone `B_h`.  The
remaining special intersection points are

```text
Q=[1:0:0],        R=[0:0:1],
```

and the two affine roots of `C(S,Z)=3S^2+4SZ+4Z^2` on `X=Z`.

Without the infinity line, the component Euler sum is

```text
2 + 2 + 2 + 2 + 1 = 9
```

for the two `B_h` lines, `X=0`, `X=Z`, and the nodal cubic `D_h`.
The intersection correction is

```text
2 at P,        2 at Q,        1 at R,
4 B/L points, 2 C-points,
```

for total correction `11`.  Hence the divisor union has Euler characteristic
`-2`, and

```text
chi(P^2 - divisor) = 3 - (-2) = 5.
```

If the infinity line is ramified, its component Euler `2` is exactly canceled
by the extra correction at `P` and `Q`, so the complement Euler
characteristic is still `5`.

Consequently a naive rank-one Kummer estimate on the compactified plane
suggests a `5p+O(sqrt(p))` top-dimensional bound, not the observed
`3p+O(sqrt(p))` target.  The proof must therefore exploit the pulled-back
hypergeometric middle-extension structure, or another cancellation beyond the
generic plane-divisor complement.

## Pullback Conductor Audit

The plane audit raises the question of whether the hypergeometric
presentation alone lowers the conductor to the desired leading constant.  Let
`F` denote the rank-two middle-extension sheaf on the `lambda`-line whose
trace is

```text
H(lambda)=sum_x mu(x) eta(x-1) chi_2(x-lambda).
```

Equivalently, `F` is the tame four-puncture hypergeometric sheaf attached to
the characters

```text
mu,        eta,        chi_2,        (mu eta chi_2)^(-1).
```

The desired pullback main term is the trace sum of

```text
lambda^*F tensor L_{rho(B(s))}
```

on the `s`-line, with `rho=mu eta chi_2=alpha chi_2`.  The singular support
is contained in

```text
s=0,        B(s)=0,        C(s)=0,        infinity,
```

where `C(s)=3s^2+4s+4`.

The standard `2F1` normalization is

```text
H(lambda) = const * chi_2(-lambda)
  * 2F1(chi_2, mu; alpha; 1/lambda).
```

Near a root of `B(s)`, the parameter `t=1/lambda` is a local parameter.
For `2F1(A,B;C;t)`, the `t=0` local characters are `1` and `C^(-1)`.
Here `C=alpha`.  After the visible twist by `chi_2(t)` and then by
`rho(B(s))=alpha chi_2(B(s))`, the two local characters become

```text
alpha,        1.
```

Thus each of the two geometric roots of `B(s)=0` has one inertia invariant
and contributes only one conductor unit.  This is the two-unit saving missing
from the earlier conservative audit.

This is the standard Gauss `2F1` local table, translated from exponents
`0` and `1-C` at `t=0` to tame characters.  It is compatible with Katz's
hypergeometric-sheaf convention in which the semisimplified tame local
monodromy at `0` of `Hyp_psi(chi_i;rho_j)` is the direct sum of the
`chi_i`, as restated from Katz, *Exponential Sums and Differential
Equations*, 8.4.2(5), by Katz--Tiep.  In the present normalization the
corresponding `chi_i` are `1` and `alpha^(-1)`.  This local table is the
only sheaf-theoretic import in the corrected equal-line conductor ledger.

The generic tame conductor ledger on `P^1_s` is therefore

```text
s=0:        at most 1 unit,
C(s)=0:     2 geometric points, one unit each,
B(s)=0:     2 geometric points, one unit each,
infinity:   2 units from rho(B(s)) with monodromy alpha^(-2).
```

The total is

```text
1 + 2 + 2 + 2 = 7.
```

For a geometrically nonconstant rank-two middle extension with no global
invariants, Euler-Poincare then gives the generic estimate

```text
dim H^1 <= 7 - 2*2 = 3.
```

This supplies the desired top-dimensional `3p` target for the equal-line
pullback main term, up to the already separated regular-fiber and
`B(s)=0` exceptional terms of size `O(sqrt(p))`.  The finite verifier checks
the algebraic support and this corrected conductor ledger; the
hypergeometric local-monodromy table remains an imported standard `2F1`
input.

The same `B(s)=0` local calculation is actually coordinate-diagonal rather
than equal-line-specific.  For a general diagonal pair, put
`alpha=mu eta`; the standard normalization becomes

```text
H(lambda) = const * chi_2(-lambda)
  * 2F1(chi_2, mu; alpha; 1/lambda).
```

At a root of `B(s)=0`, the imported `t=0` characters are `1` and
`alpha^(-1)`.  After the visible `chi_2(t)` factor and the outer twist
`rho(B(s))=alpha chi_2(B(s))`, they again become

```text
alpha,        1.
```

Thus the two-unit local saving at `lambda=infinity` is not confined to the
equal-line sub-slice.  The first global-invariant audit is also elementary:
on the diagonal, `alpha=mu eta`, and the infinity monodromy is
`-(2mu+2eta)` in exponent notation, i.e. `-2alpha`.  Therefore
`alpha^2=1` would force the infinity monodromy to be trivial, placing the
term in the already removed infinity-unramified slice.  In the ramified
nonreciprocal diagonal remainder, the scalar Kummer twist at `s=infinity`
has nontrivial character `alpha^(-2)`, so it has no inertia invariants and
rules out global invariants for the rank-two pullback.

The same congruence audit removes the obvious degenerate `2F1` parameters:
`alpha=mu` would mean `eta=1`, excluded by `d!=0`, and
`alpha=chi_2` would again force `alpha^2=1`.  Thus the diagonal remainder
has no numerator-denominator cancellation in the imported
`2F1(chi_2,mu;alpha;t)` table.

The remaining finite local conductor entries are also uniform on the whole
coordinate-diagonal remainder.  At `s=0`, the point `lambda=0` has quadratic
contact.  In the `t=1/lambda` normalization, the local characters at
`t=infinity`, after the visible `chi_2(-lambda)` twist and the quadratic
pullback, are

```text
1,        mu^2.
```

The diagonal terms with `mu^2=1` are exactly the projective-reciprocal terms
already removed from this slice, so `s=0` contributes one conductor unit.
At the two roots of `C(s)=0`, equivalently `lambda=1`, the standard `2F1`
local monodromy is a tame pseudoreflection; each root contributes at most one
unit, with possible extra cancellation only lowering the cost.  Together with
the two one-unit `B(s)=0` roots and the two-unit nontrivial scalar twist
`alpha^(-2)` at infinity, every ramified nonreciprocal coordinate-diagonal
term has the same conductor upper ledger

```text
s=0:        1,
C(s)=0:     2,
B(s)=0:     2,
infinity:   2,
total:      7.
```

Thus, subject to the same standard `2F1` local-monodromy import used above,
the full coordinate-diagonal mass has the conditional replacement
`4p+3sqrt(p)` instead of `9p`.  The certificate tooling now reports this
stronger coordinate-diagonal conditional ledger separately from the older
equal-line ledger, while the active saturation certificate remains the
conservative one.

## Projective Equal-Pair Extension

The same diagonal conductor ledger is projective, not tied to the original
affine choice of the two active coordinate axes.  The compactified
two-coordinate core has projective line monodromies

```text
mu,        nu,        lambda=(mu nu eta^2)^(-1)
```

on the two active coordinate lines and the line at infinity.  If any two of
these three projective line monodromies are equal, a projective chart change
chooses that equal pair as the two affine coordinate axes.  The conic-line
arrangement is projectively equivalent to the diagonal arrangement above, and
the open sum is carried exactly to a coordinate-diagonal open sum with the
same conic character.  The verifier checks this identity for the two
non-coordinate equal-pair cases `mu=lambda` and `nu=lambda`.

Consequently, the conditional `4p+3sqrt(p)` replacement applies to the
larger projective equal-pair mass, not only to the coordinate-diagonal mass.
For one active coordinate chart, inclusion-exclusion gives

```text
#{some equal projective line pair}
  = 3 #{first=second} - 2 #{first=second=infinity}.
```

In the full two-coordinate L1 ledger this is

```text
C_2^peq = 3 C_2^diag - 2 C_2^eq.
```

The new conditional ledger therefore drops the leading L1 weight by
`5C_2^peq` and adds square-root mass `3C_2^peq`.  The active certificate still
stays conservative until the imported `2F1` local table is promoted to an
accepted theorem-grade input.

## Deck Involution Audit

The degree-two map `lambda=s^2/(4B(s))` has deck involution

```text
tau(s) = -s/(s+1).
```

It satisfies

```text
lambda(tau(s)) = lambda(s),
tau^2(s)=s,
B(tau(s)) = B(s)/(s+1)^2,
C(tau(s)) = C(s)/(s+1)^2.
```

Thus `tau` fixes the two ramification points `s=0` and `s=-2`, swaps the two
geometric points above `lambda=infinity` (`B(s)=0`), swaps the two geometric
points above `lambda=1` (`C(s)=0`), and swaps the point at infinity with the
deleted regular point `s=-1`.

This confirms that the two `B(s)=0` points are naturally a single deck
orbit.  However, the Kummer twist is not deck-invariant:

```text
rho(B(tau(s))) = rho(B(s)) rho((s+1)^(-2)).
```

Thus the deck symmetry is not the source of the conductor saving above; the
saving comes from the corrected `2F1` local characters at `t=0`.  The deck
formula is still useful for checking exact identities and for relating the
deleted regular point to the point at infinity.

The quotient coordinate makes the same auxiliary structure explicit.  Put

```text
z = s/(s+2),        q=z^2.
```

Then `tau` is `z -> -z`, and

```text
s = 2z/(1-z),
B(s) = (1+3q)/(1-z)^2,
C(s) = 4(1+2q)/(1-z)^2,
lambda = q/(1+3q).
```

After pairing the two `z`-points over a generic `q`, the pullback main is

```text
chi_2(-4) sum_q H(q/(1+3q)) rho(1+3q)
  sum_{z^2=q} alpha^(-2)(1-z)
```

plus the fixed ramification contribution at `z=infinity` (`s=-2`).  The
excluded pair `z=1,-1` is exactly the point at infinity on the `s`-line
together with the deleted regular point `s=-1`, and the exceptional
`B(s)=0` pair is the single quotient point `q=-1/3`.

Thus the deck quotient does combine the two `B(s)=0` points into one point,
but it introduces the auxiliary two-point trace

```text
sum_{z^2=q} alpha^(-2)(1-z).
```

This is the precise auxiliary trace introduced by quotienting.  The quotient
alone is therefore not the cleanest way to see the conductor saving; the
unquotiented `2F1` local table already gives it.

There is, however, a cleaner complete-sum form before taking the quotient by
`z -> -z`.  Let `rho=alpha chi_2` and put

```text
Lambda(z) = z^2/(1+3z^2),
K_alpha(z) =
  chi_2(1+3z^2) alpha((1+3z^2)/(1-z)^2).
```

The finite `z`-line completion is

```text
C_alpha = sum_{z in F_p, 1+3z^2 != 0}
  K_alpha(z) H(Lambda(z)).
```

Here the point `z=1` contributes zero, while `z=-1` is the deleted regular
point `s=-1`.  The fixed point `z=infinity` is `s=-2`.  Thus the pullback
main satisfies the exact identity

```text
M_alpha =
  chi_2(-4) (C_alpha - H(1/4)
    + alpha(3) chi_2(3) H(1/3)).
```

The two correction terms are regular hypergeometric fibers, hence are only
`O(sqrt(p))` in the same imported rank-two Weil framework.  Therefore the
leading `3p+O(sqrt(p))` target is equivalent to the same leading bound for
`C_alpha`.

The useful structural point is that the equal-line twist is balanced at
infinity:

```text
rho(1+3z^2) alpha^(-2)(1-z)
  = chi_2(1+3z^2) alpha((1+3z^2)/(1-z)^2).
```

The numerator and denominator of `(1+3z^2)/(1-z)^2` have the same degree, so
there is no Kummer zero or pole at `z=infinity`; the infinity value is
`alpha(3) chi_2(3)`.  The completed `z`-line trace has finite singular support
contained in

```text
z=0,        1+2z^2=0,        1+3z^2=0,        z=1,
```

with `z=infinity` regular.

On the completed `z`-line, the visible Kummer divisor is

```text
div((1+3z^2)/(1-z)^2) = [1+3z^2=0] - 2[1],
```

with no degree at infinity.  The quadratic factor `chi_2(1+3z^2)` also has no
infinity ramification, since its pole at infinity has even order.  The
corrected imported local characters at the two points above
`lambda=infinity`, after the visible twists, are

```text
alpha,        1,
```

so each point contributes only one conductor unit.  The regular point `z=1`
carries the nontrivial scalar twist

```text
alpha^(-2).
```

For the remaining equal-line wall, none of these three characters is
principal: `ord(alpha)` is not `1`, `2`, or `3`.  Hence the conservative
tame conductor ledger becomes

```text
z=0:              at most 1 unit,
1+2z^2=0:         2 geometric points, one unit each,
1+3z^2=0:         2 geometric points, one unit each,
z=1:              2 units from the regular-fiber scalar twist,
z=infinity:       0 units.
```

The total is

```text
1 + 2 + 2 + 2 + 0 = 7,
```

so Euler-Poincare gives the desired `dim H^1 <= 3` route for the complete
rank-two `z`-line trace, again up to the regular-fiber corrections already
separated above.

The same finite cluster has a more useful pushforward form.  Put

```text
y = (1+3z^2)/(1-z)^2.
```

This map has deck involution

```text
sigma(z) = (z+1)/(3z-1),
```

fixing `z=1` and `z=-1/3`.  It sends `z=1` to `y=infinity`, sends the two
points `1+3z^2=0` to `y=0`, has finite branch value `y=3/4` at `z=-1/3`,
and pairs `z=1/3` with `z=infinity` over `y=3`.

For `z` away from `z=1` and `1+3z^2=0`, the balanced kernel collapses to a
single ordinary multiplicative character in `y`:

```text
K_alpha(z)
  = chi_2(1+3z^2) alpha((1+3z^2)/(1-z)^2)
  = (alpha chi_2)(y).
```

Let `rho=alpha chi_2`, and define the projective completed trace

```text
P_alpha = C_alpha + rho(3) H(1/3).
```

Then

```text
P_alpha = sum_{y in F_p^*} rho(y) G(y),
```

where `G(y)` is the sum of `H(Lambda(z))` over the projective fiber
`(1+3z^2)/(1-z)^2=y`.  Equivalently the two hypergeometric parameters in a
generic fiber are the two roots of

```text
16 y^2 lambda^2 + (-8y^2+4y)lambda + (y-1)^2 = 0.
```

The pullback main is therefore

```text
M_alpha = chi_2(-4) (sum_{y in F_p^*} rho(y) G(y) - H(1/4)).
```

This does not change the theorem to be proved, but it turns the completed
`z`-line problem into a Mellin transform of an explicit degree-two
pushforward trace.  The singular cluster `z=1` and `1+3z^2=0` is now the
standard `y=infinity`/`y=0` boundary of the outer Kummer character, while the
nontrivial hypergeometric pairing is concentrated in the quadratic relation
for `lambda`.

One can also remove the remaining denominator inside the quadratic character.
For finite `z`, write

```text
A_y(x,z) = x + (3x-1)z^2.
```

Since

```text
1+3z^2 = y(1-z)^2,
```

we have

```text
chi_2(x-Lambda(z)) = chi_2(y) chi_2(A_y(x,z)).
```

Multiplying by the outer character `rho(y)=alpha(y)chi_2(y)` cancels the
quadratic factor and leaves the finite part of the projective trace as

```text
sum_z sum_x
  alpha(y(z)) alpha^(-2)(x) alpha^3(x-1)
  chi_2(x+(3x-1)z^2),
```

with the separate projective contribution over `y=3` equal to
`rho(3)H(1/3)`.  Thus the y-pushforward can be studied either as the
degree-two Mellin transform above or as an explicit two-variable kernel sum
with a single quadratic radical.

For a split finite `y`-fiber, the product of the two quadratic arguments is

```text
prod_{z: y(z)=y} (x+(3x-1)z^2)
  = (16x^2y^2 - 8xy^2 + 4xy + y^2 - 2y + 1)/(y-3)^2.
```

Equivalently the numerator is the resultant of
`y(1-z)^2-(1+3z^2)` and `x(1+3z^2)-z^2` in `z`.  This gives a concrete
kernel divisor for the next conductor calculation:

```text
x=0,        x=1,        x=infinity,
y=0,        y=infinity, 4y-3=0,
16x^2y^2 - 8xy^2 + 4xy + y^2 - 2y + 1=0,
```

with `y=3` only marking the ordinary projective fiber
`lambda=1/12,1/3`.

The compactified resultant divisor gives another useful warning.  In
`P^1_x times P^1_y`, the resultant curve has bidegree `(2,2)`, but it is not
a smooth genus-one curve.  In the chart `u=1/x`, it is

```text
u^2y^2 - 2u^2y + u^2 - 8uy^2 + 4uy + 16y^2 = 0,
```

and has an ordinary node at `(u,y)=(0,0)`, i.e. at
`(x,y)=(infinity,0)`, with tangent cone

```text
4y(4y+u).
```

Thus its normalization has genus zero and the singular curve has Euler
characteristic `1`.  The special restrictions are

```text
R(0,y)       = (y-1)^2,
R(1,y)       = 9y^2+2y+1,
R(x,0)       = 1                 on the affine chart,
R(x,3/4)     = (12x-1)^2/16,
R(x,infty)  = (4x-1)^2,
R(infty,y)  = 16y^2.
```

The discriminants are

```text
disc_x R = 16y^2(4y-3),
disc_y R = -16x(3x-1).
```

If one includes the three `x`-boundary lines `0,1,infinity`, the three
`y`-lines `0,infinity,3/4`, and the nodal resultant curve, the component
Euler sum is `12+1=13`.  The line grid contributes correction `10`, because
`(x,y)=(infinity,0)` is also the resultant node, and the remaining
resultant-line intersections contribute `5`.  Hence

```text
chi(divisor union) = 13 - 15 = -2,
chi(P^1 x P^1 - divisor) = 4 - (-2) = 6.
```

So the explicit kernel surface still gives only a generic `6p+O(sqrt(p))`
route if treated as an ordinary rank-one Kummer surface.  The useful outcome
is negative but sharp: the next proof must exploit the degree-two
pushforward/Mellin structure of `G(y)`, not just the compactified
two-variable divisor.

The one-dimensional pushforward has a much smaller singular-value checklist.
For `p>3`, away from the small collision `p=11`, the candidate singular
values of `G(y)` are

```text
y=0,                 from lambda=infinity,
y=1,                 from lambda=0,
9y^2+2y+1=0,          from lambda=1,
y=3/4,               from the branch point z=-1/3,
y=infinity,          from the branch point z=1.
```

Thus the generic support has six geometric points on `P^1_y`.  The projective
fiber over `y=3` is ordinary:

```text
z=1/3 gives lambda=1/12,        z=infinity gives lambda=1/3.
```

It is not a singular value in the generic calculation.  In characteristic
`11`, however, `1/12=1`, and the two roots of `9y^2+2y+1` collide with
`y=3/4` and `y=3`; this is a small-prime degeneration to keep out of any
generic conductor statement.

This six-point checklist is the current sharp target for the degree-two
pushforward sheaf.  A proof of the desired leading constant would need to
show that, after the Mellin twist by `rho=alpha chi_2`, the corrected
lambda-infinity local table lowers the total conductor by two units.

The local pushforward conductor audit gives the following standard tame
ledger for the generic equal-line wall.  The sheaf `G` has generic rank `4`.
At `y=0`, the two branches go to `lambda=infinity`; after the Mellin twist
each branch has one invariant and contributes one conductor unit.  At `y=1`,
the singular branch has quadratic contact with `lambda=0`, while the other
branch is the regular `lambda=1/4` fiber, so the standard local cost is one.
The two roots of `9y^2+2y+1` give the two `lambda=1` costs.  The branch
value `y=3/4` lies over the regular fiber `lambda=1/12` and costs two units
as a quadratic pushforward branch.  Finally, `y=infinity` is a regular
`lambda=1/4` branch, but the Mellin twist makes the rank-four local
representation nontrivial.

Thus the generic pushforward ledger is

```text
y=0:                 2
y=1:                 1
9y^2+2y+1=0:          2
y=3/4:               2
y=infinity:          4
total conductor:    11
rank:                4
dim H^1 target:      11 - 2*4 = 3.
```

This is the y-pushforward form of the same two-unit saving seen on the
`s`- and `z`-lines.  Subject to the imported standard `2F1` local monodromy
table, it gives the desired top-dimensional `3p` ledger for the equal-line
pullback main term; the already separated regular fibers and exceptional
`B(s)=0` fibers contribute only `O(sqrt(p))`.

## Pullback Branch Checklist

The rational pullback

```text
lambda(s) = s^2 / (4B(s)),        B(s)=s^2+s+1,
```

has the following exact geometry for `p>3`:

```text
lambda=0:        s=0, with ramification index 2,
lambda=infinity: B(s)=0, two simple geometric points,
lambda=1:        C(s)=3s^2+4s+4=0, two simple geometric points.
```

The derivative is

```text
lambda'(s) = s(s+2) / (4B(s)^2).
```

Thus the second ramification point is `s=-2`, and it maps to the regular
value `lambda=1/3`. The deleted open point `s=-1` maps to the regular value
`lambda=1/4`. The finite branch and singular polynomials

```text
s,        B(s),        C(s),        s+1,        s+2
```

are pairwise separated in the ways needed above:

```text
B(0)=1,        C(0)=4,
B(-1)=1,       C(-1)=3,
B(-2)=3,       C(-2)=8.
```

Consequently, the remaining `3p` target can be phrased as a conductor
problem for the middle extension of

```text
rho(B(s)) H(lambda(s))
```

on the `s`-line, with geometric singular support contained in

```text
s=0,        B(s)=0,        C(s)=0,        infinity,
```

and with the regular deleted point `s=-1` handled separately by the usual
pointwise genus-zero bound for `H(1/4)`.

The finite verifier is

```bash
python3 experimental/verify_m1_depth_two_equal_line_diagonal_reduction.py
```
