# M1 Depth-Two Line-Conic Resonance Reduction

**Status:** PROVED / AUDIT.

## Claim

Let `p>3`, put

```text
w=-1-u-v,
A(u,v)=-(u^2+v^2+uv+u+v+1),
B(v)=v^2+v+1.
```

Extend multiplicative characters by zero at zero.  In the line-conic
resonant two-coordinate core with `mu eta=1`, write `mu=eta^(-1)` and define

```text
C_{eta,nu} =
  sum_{u,v in F_p} eta^(-1)(u) nu(v) eta(A(u,v)).
```

Then

```text
C_{eta,nu} =
  sum_{y in F_p} eta(-y) G_nu(y),

G_nu(y) =
  sum_{v in F_p} nu(v)
    chi_2(y^2 - 2(v+1)y - 3v^2 - 2v - 3).
```

Thus the line-conic-resonant slice is not a generic two-variable Kummer
problem.  It is a Mellin transform of a one-dimensional quadratic-fiber trace
family.

## Proof

For fixed `v`, the summand is zero unless `u` and `A(u,v)` are nonzero.  For
`u != 0`,

```text
eta^(-1)(u) eta(A(u,v))
  = eta(A(u,v)/u)
  = eta(-(u+v+1+B(v)/u)).
```

Use the degree-two map

```text
x = u + B(v)/u.
```

If `B(v) != 0`, the number of nonzero `u` mapping to `x` is
`1+chi_2(x^2-4B(v))`.  The contribution of the `1` term is

```text
sum_x eta(-(x+v+1)) = 0
```

because `eta` is nonprincipal.  Hence

```text
sum_u eta^(-1)(u) eta(A(u,v))
  = sum_x chi_2(x^2-4B(v)) eta(-(x+v+1)).
```

The same identity holds when `B(v)=0`: both sides are
`-eta(-(v+1))`.  Replacing `y=x+v+1` gives

```text
x^2-4B(v)
  = y^2 - 2(v+1)y - 3v^2 - 2v - 3,
```

and interchanging the `v` and `y` sums proves the claim.

## Singular-Value Checklist

For fixed `y`, the quadratic in `v` is

```text
Q_y(v) = -3v^2 - 2(y+1)v + y^2 - 2y - 3.
```

Its discriminant is

```text
disc_v(Q_y) = 16(y-2)(y+1).
```

The root collision values are therefore `y=-1` and `y=2`.  The collision of
a quadratic root with the coordinate line `v=0` is controlled by

```text
Q_y(0) = y^2 - 2y - 3 = (y-3)(y+1),
```

so it adds `y=3` and repeats `y=-1`.  The outer Mellin character adds
`y=0`, and infinity is the remaining projective point.  For `p>3`, the
candidate singular support is contained in

```text
y=0,        y=-1,        y=2,        y=3,        infinity.
```

This is the finite conductor target for the line-conic-resonant asymmetric
mass `C_2^lc`.  The active M1 certificate remains conservative: this note
does not prove the required conductor bound, but it replaces the residual
two-variable resonant slice by an explicit one-dimensional trace-family
problem.

## Finite Singular-Fiber Values

The finite singular values above do not hide a `p`-sized exceptional
contribution.  Write

```text
G_nu(y) = sum_v nu(v) chi_2(Q_y(v)).
```

For every nonprincipal `nu`,

```text
G_nu(-1) = 0,
G_nu(2)  = -chi_2(-3) nu(-1),
```

and

```text
G_nu(3)
  = chi_2(3) nu(-8/3) J(nu chi_2, chi_2),
```

where

```text
J(alpha,beta) = sum_t alpha(t) beta(1-t)
```

is the usual Jacobi sum with characters extended by zero.  Hence
`|G_nu(3)| = sqrt(p)` unless `nu=chi_2`, in which case
`G_nu(3)=-chi_2(-2)`.

The `y=0` term contributes nothing to `C_{eta,nu}` because `eta(0)=0`.
Therefore the whole finite singular contribution to the Mellin transform is
bounded by

```text
|eta(-2)G_nu(2) + eta(-3)G_nu(3)| <= 1 + sqrt(p).
```

Thus any `p`-scale obstruction to the desired `|C_{eta,nu}|<=4p` target
must come from the lisse open trace over

```text
P^1_y \ {0,-1,2,3,infinity},
```

not from a bad finite fiber.

Indeed, the identities follow by direct specialization:

```text
Q_{-1}(v) = -3v^2,        Q_2(v) = -3(v+1)^2,
Q_3(v)   = -v(3v+8).
```

The first gives `chi_2(-3) sum_{v!=0} nu(v)=0`.  The second gives
`chi_2(-3) sum_{v!=-1} nu(v)=-chi_2(-3)nu(-1)`.  For the third, write
`a=8/3`; then

```text
G_nu(3) = chi_2(-3) sum_v (nu chi_2)(v) chi_2(v+a).
```

Substituting `v=-at` gives the displayed Jacobi sum and the factor
`chi_2(3)nu(-a)`.

## Split-Fiber Hypergeometric Pullback

On the nonsingular part, the quadratic-fiber trace becomes a standard
three-point trace after the discriminant double cover.  Put

```text
z^2 = (y-2)(y+1),
```

and, away from `y=-1,2,3`, set

```text
r_+ = -(y+1+2z)/3,
r_- = -(y+1-2z)/3,
lambda = r_-/r_+.
```

Then `r_+` and `r_-` are the two roots of `Q_y(v)`, neither root is zero,
and `lambda` is distinct from `0` and `1`.  Define

```text
H_nu(lambda) = sum_x nu(x) chi_2((x-1)(x-lambda)).
```

On every split fiber over `F_p`, and geometrically after pulling back to the
double cover, one has

```text
G_nu(y) = chi_2(-3) nu(r_+) H_nu(lambda).
```

Indeed,

```text
Q_y(v) = -3(v-r_+)(v-r_-).
```

Substitute `v=r_+ x`.  Since `r_+ != 0`, the character factor separates as

```text
nu(v) chi_2(Q_y(v))
  = chi_2(-3) nu(r_+) nu(x) chi_2((x-1)(x-lambda)).
```

Summing over `x` proves the identity.

Changing the sign of `z` interchanges `r_+` and `r_-` and sends
`lambda` to `lambda^{-1}`.  The identity is independent of this choice
because

```text
H_nu(lambda) = nu(lambda) H_nu(lambda^{-1}).
```

Thus the transformed line-conic family is a quadratic pushforward of the
rank-two three-point trace `H_nu(lambda)`, with the outer Mellin twist
`eta(-y)` and the explicit root prefactor `nu(r_+)`.  This is the geometric
object whose conductor must be bounded for the `4p` target; the previous
finite singular-fiber calculation accounts for the points where this
hypergeometric chart degenerates.

## Lambda-Line Conductor Checklist

The double cover above is rational.  In terms of `lambda=r_-/r_+`, one has

```text
y = (9lambda^2+14lambda+9)/(3lambda^2+10lambda+3),
z = 6(1-lambda^2)/(3lambda^2+10lambda+3),
r_+ = -8(1+lambda)/(3lambda^2+10lambda+3).
```

The deck involution is `lambda -> lambda^{-1}`.  The three basic special
value identities are

```text
y-2 = 3(lambda-1)^2/((lambda+3)(3lambda+1)),
y+1 = 12(lambda+1)^2/((lambda+3)(3lambda+1)),
y-3 = -16lambda/((lambda+3)(3lambda+1)).
```

Thus the old finite singular values lift as follows:

```text
y=2:        lambda=1        (ramified),
y=-1:       lambda=-1       (ramified),
y=3:        lambda=0,infinity,
y=infinity: lambda=-3,-1/3.
```

The outer Mellin point `y=0` pulls back to

```text
9lambda^2+14lambda+9 = 0.
```

Consequently, after the hypergeometric pullback, the finite conductor
checklist on the `lambda`-line is contained in the eight geometric points

```text
lambda = 0, infinity, 1, -1, -3, -1/3,
          roots of 9lambda^2+14lambda+9.
```

This ledger separates the remaining proof task cleanly.  The points
`0,1,infinity` are the standard singular parameters of the three-point trace
`H_nu(lambda)`.  The points `1,-1` are also the two ramification points of
the discriminant double cover.  The points `-3,-1/3` are the two preimages
of `y=infinity`, and the quadratic pair above is exactly the outer Mellin
zero `eta(-y)`.  The verifier checks these identities and the absence of
unexpected finite singular `y` values directly over the audited prime set.

## Pulled-Back Twist Divisor

The previous identity also gives the exact Kummer twist multiplying the
three-point trace.  On the `lambda`-line,

```text
eta(-y(lambda)) nu(r_+(lambda))
  = eta(-(9lambda^2+14lambda+9)/(3lambda^2+10lambda+3))
    nu(-8(1+lambda)/(3lambda^2+10lambda+3)).
```

Thus, apart from the three-point trace `H_nu(lambda)`, the finite local
monodromy is supported at

```text
lambda=-1,        lambda=-3,        lambda=-1/3,
9lambda^2+14lambda+9=0,
```

with infinity as one additional support point.  More explicitly:

```text
lambda=-1:                         nu
lambda=-3, -1/3:                   (eta nu)^(-1)
roots of 9lambda^2+14lambda+9:     eta
lambda=infinity:                   nu
```

At `lambda=0` and `lambda=1`, the Kummer twist is unramified; those points
enter only through the standard singular parameters of `H_nu(lambda)` and
the ramification of the double cover.  The full geometric support is
therefore the eight-point checklist recorded above.  Over a finite field the
two outer-Mellin points are rational precisely when `chi_2(-2)=1`, so the
verifier reports either six or eight rational projective support points.

## Nontriviality on the Admissible Range

In the actual `C_2^lc` character range, none of the twist-divisor characters
above is accidentally principal.  With the notation of the admissible filter,

```text
eta = chi^{-a},        nu = chi^b,        eta nu = chi^{b-a}.
```

The filter has `a,b != 0` and `b != a`, so `eta`, `nu`, and `eta nu` are all
nonprincipal.  Therefore:

```text
lambda=-1 and infinity:              nu is nonprincipal,
lambda=-3 and -1/3:                  (eta nu)^(-1) is nonprincipal,
roots of 9lambda^2+14lambda+9:       eta is nonprincipal.
```

Thus every support point introduced by the pulled-back Kummer twist is a
genuine ramified point for every admissible line-conic-resonant character
pair.  The conductor proof cannot discard any of these twist points by a
character-specialization shortcut; the only possible savings must come from
the hypergeometric local table, the quadratic pushforward structure, or
global cancellation.

## Finite-Field Pullback Descent

The `lambda`-pullback controls the split projection of the original core,
not the original core by itself.  Define the quadratic discriminant twist

```text
C^quad_{eta,nu}
  = sum_y chi_2((y-2)(y+1)) eta(-y) G_nu(y),
```

and the finite `lambda`-pullback trace

```text
P_{eta,nu}
  = sum_{3lambda^2+10lambda+3 != 0}
      eta(-y(lambda)) chi_2(-3) nu(r_+(lambda)) H_nu(lambda).
```

Then

```text
P_{eta,nu}
  = C_{eta,nu} + C^quad_{eta,nu} - eta(-3)G_nu(3).
```

Indeed, away from `y=infinity`, the map `lambda -> y` has
`1+chi_2((y-2)(y+1))` finite preimages, except at `y=3`: one preimage is
`lambda=0` and the other is `lambda=infinity`, outside the finite
`lambda`-sum and outside the affine hypergeometric chart.  The branch values
`y=-1,2` have one finite preimage and are counted correctly, while `y=0`
contributes zero because `eta(0)=0`.  Summing the split-fiber identity over
finite `lambda` therefore gives the displayed descent formula.

This identity is a useful guardrail: a conductor bound for the pulled-back
hypergeometric trace gives a bound for the split-projected combination
`C+C^quad`, up to the already evaluated `y=3` Jacobi term.  A complete proof
of the original `4p` target still has to control the companion quadratic
twist or descend the pushforward sheaf without losing a square-root factor.

## Split/Nonsplit Projection Criterion

The preceding descent can be stated as an exact projector identity on the
`y`-line.  Put

```text
C^+_{eta,nu}
  = C_{eta,nu} + C^quad_{eta,nu} - eta(-3)G_nu(3),

C^-_{eta,nu}
  = C_{eta,nu} - C^quad_{eta,nu}.
```

Then `C^+_{eta,nu}` is exactly the finite `lambda`-pullback trace
`P_{eta,nu}`.  On the lisse open set

```text
U = P^1_y \ {0,-1,2,3,infinity},
```

the two projectors have the elementary form

```text
C^+_U = sum_{y in U(F_p)}
          (1+chi_2((y-2)(y+1))) eta(-y)G_nu(y),

C^-_U = sum_{y in U(F_p)}
          (1-chi_2((y-2)(y+1))) eta(-y)G_nu(y).
```

Thus `C^+` is the split-fiber projection and `C^-` is the nonsplit-fiber
projection.  They reconstruct the original core and the companion twist by

```text
C_{eta,nu}
  = (C^+_{eta,nu} + C^-_{eta,nu} + eta(-3)G_nu(3))/2,

C^quad_{eta,nu}
  = (C^+_{eta,nu} - C^-_{eta,nu} + eta(-3)G_nu(3))/2.
```

The finite singular budgets are also separated exactly.  The split projector
has the same finite singular contribution as the lambda pullback,

```text
eta(-2)G_nu(2) + eta(-3)G_nu(3),
```

and the nonsplit projector has only

```text
eta(-2)G_nu(2).
```

Indeed `G_nu(-1)=0`, the outer `y=0` term vanishes, `chi_2((3-2)(3+1))=1`
so the `y=3` Jacobi term cancels from `C^-`, and the finite `lambda`-sum
counts only one of the two `y=3` pullback points in `C^+`.

Consequently a no-loss descent proof can be phrased in either of two
equivalent ways:

```text
control both C^+ and C^- at p-scale,
```

or prove a direct conductor bound for the quadratic pushforward on the
`y`-line.  A bound for `C^+=P` alone cannot prove the original `C` bound,
because the missing term is the whole nonsplit projection `C^-`.  Conversely,
if

```text
|C^+_{eta,nu}| <= K_+ p,        |C^-_{eta,nu}| <= K_- p,
```

then

```text
|C_{eta,nu}| <= (K_+ + K_-)p/2 + sqrt(p)/2
```

on the admissible nonprincipal range, using the Jacobi bound for `G_nu(3)`.
Thus a projector proof of the `4p` core target needs the combined constant
`K_+ + K_-` to be at most `8` up to lower-order terms; it does not require
matching `4p` bounds for the two projectors separately.

This distinction is not cosmetic.  The finite audit reports the largest
tested split-projector ratio as `3.2068909828p` and the largest tested
nonsplit-projector ratio as `4.0427466236p`.  So the naive same-constant
route "`|C^+|<=4p` and `|C^-|<=4p`" is already too rigid for the nonsplit
piece, even though the original core remains below `4p` in the same audit.
This is the precise form of the remaining descent problem: the finite
singular terms are harmless, and the possible square-root loss can only come
from bounding the lisse nonsplit projector, balancing the two projector
constants, or from an inefficient descent of the quadratic pushforward.

## Split/Nonsplit Full-Character Moment

The split and nonsplit projectors have no large average obstruction.  Sum
over all multiplicative characters `eta,nu` of `F_p^*`, extended by zero.
Then

```text
sum_{eta,nu} |C^-_{eta,nu}|^2
  = (p-1)^2(2p^2 - 4p + 1 + 2(p-1)chi_2(-2)),

sum_{eta,nu} |C^+_{eta,nu}|^2
  = (p-1)^2(2p^2 - 15p + 31 - 2(p-3)chi_2(-2)),
```

and the cross moment is

```text
sum_{eta,nu} C^-_{eta,nu} overline{C^+_{eta,nu}}
  = (p-1)^2(2p-3).
```

Thus both projectors have full-family RMS `sqrt(2)p+O(1)`, and they are
nearly orthogonal on average.  The observed nonsplit pointwise ratio slightly
above `4p` is therefore not an average-mass phenomenon.

For the proof, write

```text
d_y=(y-2)(y+1),        c_y=chi_2(d_y),
a_-(y)=1-c_y,          a_+(y)=1+c_y-1_{y=3}.
```

Then `C^-` and `C^+` are the Mellin transforms with coefficients `a_-`
and `a_+`.  Orthogonality gives

```text
sum_{eta,nu} C^sigma overline{C^tau}
  = (p-1)^2 sum_{y!=0} a_sigma(y)a_tau(y) M(y),
```

where

```text
M(y)=#{v in F_p^*: Q_y(v) != 0}
    = p-2-c_y+1_{y=-1}+1_{y=3}.
```

Indeed the quadratic in `v` has `1+c_y` roots over `F_p`, and `v=0` is one
of them exactly at `y=-1` and `y=3`.  Expanding the three sums uses only

```text
sum_{y!=0} c_y = -1-chi_2(-2),        sum_{y!=0} c_y^2 = p-3,
```

together with the exceptional values `c_{-1}=0`, `c_3=1`.  This gives the
three displayed formulas.

## Twisted Discriminant-Line Model for the Nonsplit Projector

The nonsplit projector also has an exact one-dimensional pullback, but it
lives on the quadratic twist of the discriminant cover rather than on the
split `lambda`-line.  Fix a nonsquare `delta in F_p^*` and define

```text
y_delta(t) = (2t^2 + delta)/(t^2 - delta),        t in F_p.
```

Since `delta` is nonsquare, the denominator never vanishes for finite `t`.
The elementary identities

```text
y_delta(t)-2 = 3delta/(t^2-delta),
y_delta(t)+1 = 3t^2/(t^2-delta),
y_delta(t)-3 = (4delta-t^2)/(t^2-delta)
```

give

```text
(y_delta(t)-2)(y_delta(t)+1)
  = 9 delta t^2/(t^2-delta)^2.
```

Thus for `t != 0`, the discriminant is nonsquare, while `t=0` maps to the
branch value `y=-1`.  The missing projective point `t=infinity` maps to the
other branch value `y=2`.  Consequently

```text
C^-_{eta,nu}
  = eta(-2)G_nu(2)
    + sum_{t in F_p} eta(-y_delta(t)) G_nu(y_delta(t)).
```

Indeed, every nonsplit `y` has exactly two preimages `t` and `-t`, giving
the coefficient `1-chi_2((y-2)(y+1))=2`; `t=0` contributes
`eta(1)G_nu(-1)=0`; the projective point at infinity supplies the branch
term `eta(-2)G_nu(2)`; and any finite preimage of `y=0` contributes zero
through the outer Mellin character.

This twisted-line model is the nonsplit analogue of the finite
`lambda`-pullback.  It does not split the quadratic `v`-fiber over `F_p`;
instead it packages the nonsplit projection as a rational-line Mellin
transform of the same trace family `G_nu`.  Its geometric conductor
checklist is the pullback of

```text
y=0,        y=-1,        y=2,        y=3,        y=infinity,
```

namely

```text
t=0,        t=infinity,        t^2=-delta/2,
t^2=4delta,        t^2=delta.
```

The `t^2=4delta` and `t^2=delta` pairs have no `F_p`-points for nonsquare
`delta`, but they remain geometric support points for a conductor proof.
This is the precise nonsplit target left by the projector criterion.

## Twisted-Line Fiber Trace

The twisted model can be pushed one step further: after pulling back to the
`t`-line, the quadratic fiber trace is itself a fixed translated
hypergeometric trace.  Put

```text
D(t)=t^2-delta,
K_{nu,delta}(t) = sum_x nu(x-t) chi_2(x^2-4delta).
```

For every finite `t`,

```text
G_nu(y_delta(t))
  = chi_2(-3) nu(t/D(t)) K_{nu,delta}(t),
```

where characters are extended by zero.  Therefore

```text
C^-_{eta,nu}
  = eta(-2)G_nu(2)
    + chi_2(-3) sum_t
        eta(-(2t^2+delta)/D(t))
        nu(t/D(t)) K_{nu,delta}(t).
```

For the proof, write `s=t^2`, `D=s-delta`, and
`y=(2s+delta)/D`.  A direct calculation gives

```text
D^2 Q_y(v) = -3((Dv+s)^2 - 4delta s).
```

Since `D` is nonzero for finite `t`, the change of variables
`m=Dv+s` gives

```text
G_nu(y_delta(t))
  = chi_2(-3)nu(D)^(-1)
    sum_m nu(m-t^2) chi_2(m^2-4delta t^2).
```

If `t != 0`, substitute `m=tx` to get the displayed formula.  If `t=0`,
the right side is zero because `nu(t/D)=0`, while the previous line is
`chi_2(-3)nu(D)^(-1) sum_m nu(m)chi_2(m^2)=0`; this is the already known
branch value `G_nu(-1)=0`.

This formulation isolates the nonsplit local table.  The trace
`K_{nu,delta}(t)` has geometric singularities only when the moving Kummer
point `x=t` collides with a quadratic branch point of `x^2-4delta`, namely
at

```text
t^2=4delta,
```

and at infinity.  The remaining finite support points in the full nonsplit
projector come only from the outer Kummer twist:

```text
t=0,        t^2=delta,        t^2=-delta/2.
```

Thus the nonsplit projector is reduced to a rank-two translated
hypergeometric trace on the same five-point geometric checklist recorded
above, rather than to an opaque two-variable sum.

## Twisted-Line Outer-Twist Divisor

The nonsplit `t`-line also has an explicit Kummer twist divisor.  Apart from
the translated trace `K_{nu,delta}(t)`, the finite summand is multiplied by

```text
eta(-(2t^2+delta)/(t^2-delta)) nu(t/(t^2-delta)).
```

Hence the outer twist is supported at

```text
t=0,        t^2=delta,        t^2=-delta/2,
```

with infinity as one further support point.  Its local characters are

```text
t=0:                         nu
t^2=delta:                   (eta nu)^(-1)
t^2=-delta/2:                eta
t=infinity:                  nu.
```

The translated trace `K_{nu,delta}(t)` contributes the separate collision
pair

```text
t^2=4delta,
```

where the moving Kummer point `x=t` meets a branch point of `x^2-4delta`.
The outer twist is unramified at this pair.  For `p>3`, all four finite
geometric loci above are pairwise disjoint: the equalities

```text
0=delta,        delta=-delta/2,        delta=4delta,
        -delta/2=4delta
```

would force either `delta=0` or `p=3`.  Since `delta` is nonsquare, the
`t^2=delta` and `t^2=4delta` pairs have no `F_p`-points, but they remain
geometric singular points for conductor accounting.

On the admissible `C_2^lc` character range, the displayed outer-twist
characters are all nonprincipal: `eta`, `nu`, and `eta nu` are nonprincipal.
Thus the nonsplit line has the same no-disappearing-support feature as the
split `lambda`-line.  Any saving has to come from the local table of
`K_{nu,delta}` or from global cancellation, not from a character
specialization removing one of these outer-twist points.

## Twisted-Line Deck Symmetry

The nonsplit `t`-line trace is compatible with the deck involution
`t -> -t`.  The kernel satisfies

```text
K_{nu,delta}(-t) = nu(-1) K_{nu,delta}(t).
```

Indeed, substitute `x -> -x` in the defining sum:

```text
K_{nu,delta}(-t)
  = sum_x nu(x+t) chi_2(x^2-4delta)
  = nu(-1) sum_x nu(x-t) chi_2(x^2-4delta).
```

Since `D(-t)=D(t)` and `y_delta(-t)=y_delta(t)`, the full finite summand

```text
eta(-y_delta(t)) nu(t/D(t)) K_{nu,delta}(t)
```

is invariant under `t -> -t`.  Thus the twisted-line pullback is not
introducing two unrelated nonsplit traces over each `y`: the two preimages
are exactly paired.  Equivalently, the nonsplit projector can be descended
through the quotient `t^2` without a deck-asymmetry loss; the remaining
analytic work is the conductor bound for the descended rank-two trace.

For fixed `t`, the kernel is a genus-zero Kummer sum in `x` with local
characters

```text
x=t:              nu,
x^2=4delta:       chi_2,
x=infinity:       nu^(-1).
```

Away from the geometric collision `t^2=4delta`, the standard genus-zero
bound gives

```text
|K_{nu,delta}(t)| <= 2 sqrt(p).
```

At the collision the support can only merge or cancel, so the same bound
continues to hold by specialization.  This pointwise square-root bound is
not enough by itself to prove the `p`-scale estimate for `C^-`, but it
identifies the exact rank-two local table whose outer Mellin transform must
be bounded.

## Quotient-Line Descent of the Nonsplit Projector

The deck symmetry can be made completely explicit on the quotient
coordinate

```text
s=t^2.
```

For `s in F_p`, define

```text
J_{nu,delta}(s) = sum_r nu(r-1) chi_2(s r^2 - 4delta).
```

If `t != 0` and `s=t^2`, then

```text
K_{nu,delta}(t) = nu(t) J_{nu,delta}(s),
```

by the substitution `x=tr`.  Consequently the nonsplit projector descends to

```text
C^-_{eta,nu}
  = eta(-2)G_nu(2)
    + chi_2(-3) sum_{s != delta}
        (1+chi_2(s))
        eta(-(2s+delta)/(s-delta))
        nu(s/(s-delta))
        J_{nu,delta}(s).
```

The factor `1+chi_2(s)` is exactly the number of finite `t` with `t^2=s`
except at `s=0`; at `s=0` the additional factor `nu(s/(s-delta))=0`, so the
formula is still correct.  The point `s=delta` is omitted only because the
rational expression has a pole there; since `delta` is nonsquare, its
projector factor would be zero.

This is the quotient-line version of the nonsplit conductor target.  Its
finite geometric checklist is now the rational five-point set

```text
s=0,        s=delta,        s=-delta/2,        s=4delta,        infinity.
```

Here `s=0`, `s=delta`, `s=-delta/2`, and infinity come from the outer
Kummer/projector factors, while `s=4delta` is the collision of `r=1` with a
branch point of `s r^2-4delta` inside `J`.  Thus the twisted nonsplit
projector has been reduced from a two-variable sum to a single quotient-line
trace with a five-point conductor ledger.

## Quotient-Line Kernel Moment

The descended kernel has its own exact full `s`-line moment.  For every
nonprincipal `nu`,

```text
J_{nu,delta}(0) = 0,
sum_s |J_{nu,delta}(s)|^2 = p^2 - 2p - 1 - p nu(-1).
```

In particular the moment is `p^2-p-1` if `nu(-1)=-1` and
`p^2-3p-1` if `nu(-1)=1`.  The proof is a direct quotient-line
orthogonality count.  Put `a_r=nu(r-1)` and `c=-4delta`.  Then

```text
sum_s |J(s)|^2
  = sum_{r,u} a_r conj(a_u) sum_s chi_2(s r^2+c) chi_2(s u^2+c).
```

The inner sum is `p` for `r=u=0`, is `0` when exactly one of `r,u`
vanishes, is `p-1` for nonzero `r,u` with `u=r` or `u=-r`, and is `-1`
otherwise.  If

```text
D = sum_{r,u != 0, r^2=u^2} a_r conj(a_u),
```

then the nonzero off-diagonal contribution is `1-D`, because
`sum_{r != 0} a_r=-nu(-1)`.  Hence

```text
sum_s |J(s)|^2 = p-1+pD.
```

It remains to compute `D`.  The diagonal part is `p-2`, since `a_1=0`.
The cross term is

```text
sum_{r != 0} nu(r-1)nu^(-1)(-r-1).
```

The nonzero terms have `r notin {0,1,-1}`; the substitution
`z=(r-1)/(-r-1)` bijects this domain with `F_p^* \ {1,-1}`.  Therefore the
cross term is `-1-nu(-1)`, and `D=p-3-nu(-1)`, giving the displayed formula.

Thus the quotient-line trace also has root-mean-square size `sqrt(p+O(1))`.
This reinforces that the nonsplit obstruction is not hidden average mass in
the kernel, but cancellation in the outer `eta,nu`-twisted transform with the
five-point conductor ledger above.

## Quotient-Line Mellin Spectrum

The full multiplicative Mellin spectrum of `J` is also explicit.  Let
`theta` be any multiplicative character of `F_p^*`, extended by zero at `0`,
let `epsilon` be the principal character, put `c=4delta`, and use

```text
Jac(alpha,beta) = sum_x alpha(x) beta(1-x).
```

Then

```text
sum_s theta(s) J_{nu,delta}(s)
  = chi_2(-c) nu(-1)
      ( 1_{theta=epsilon}(p-1)
        + theta(c) Jac(theta,chi_2) Jac(theta^(-2),nu) ).
```

Indeed, after interchanging the `s` and `r` sums, the `r=0` term contributes
only for `theta=epsilon`, giving `chi_2(-c)nu(-1)(p-1)`.  For `r != 0`,
the change of variable `w=s r^2/c` gives

```text
sum_s theta(s) chi_2(sr^2-c)
  = chi_2(-c) theta(c) theta^(-2)(r) Jac(theta,chi_2).
```

The remaining `r`-sum is

```text
sum_r theta^(-2)(r) nu(r-1)
  = nu(-1) Jac(theta^(-2),nu).
```

Thus every multiplicative Mellin coefficient of the quotient-line kernel is
bounded by `p`.  For `theta=epsilon` the bracket equals exactly `p`; for
`theta != epsilon` the standard Jacobi bounds give the same `p` ceiling, with
smaller values in the degenerate Jacobi cases.  This identifies the descended
kernel as a hypergeometric Mellin object with no super-`p` coefficient before
the outer rational twist is imposed.

## Kernel Mellin Magnitude Ledger

The degenerate Jacobi cases in the formula above can be classified exactly.
For nonprincipal `nu`,

```text
|M_nu(theta)| =
  p,        theta=epsilon,
  1,        theta=chi_2,
  sqrt(p),  theta^2=nu,
  p,        otherwise.
```

The alternatives are disjoint: `theta=epsilon` or `theta=chi_2` both have
`theta^2=epsilon`, while `nu` is nonprincipal.  This is just the standard
Jacobi magnitude rule.  The factor `Jac(theta,chi_2)` is degenerate only for
`theta=epsilon` or `theta=chi_2`; the factor `Jac(theta^(-2),nu)` is
degenerate only for `theta^2=epsilon` or `theta^2=nu`, with the principal
`theta=epsilon` term already carrying the extra `(p-1)` contribution.

Equivalently, if `nu(-1)=-1`, then no square root of `nu` exists and the
kernel spectrum has `p-2` coefficients of size `p` and one coefficient of
size `1`.  If `nu(-1)=1`, it has `p-4` coefficients of size `p`, two
coefficients of size `sqrt(p)`, and one coefficient of size `1`.  Thus the
kernel side is generically full `p`-size; the remaining nonsplit saving
cannot come from sparsity or smallness of `M_nu(theta)`.

## Nonsplit Spectral Normal Form

The full nonsplit quotient-line transform can now be written as an exact
Mellin convolution.  Define

```text
A_{eta,nu}(theta)
  = sum_s theta(s)(1+chi_2(s))
      eta(-(2s+delta)/(s-delta)) nu(s/(s-delta)),
M_nu(theta)
  = sum_s theta(s) J_{nu,delta}(s).
```

The terms at `s=0` and `s=delta` vanish with the zero-extension convention
for multiplicative characters and with `delta` nonsquare.  Mellin inversion on
`F_p^*` gives

```text
C^-_{eta,nu}
  = eta(-2)G_nu(2)
    + chi_2(-3)/(p-1) sum_theta A_{eta,nu}(theta^(-1)) M_nu(theta).
```

The outer coefficient is itself a sum of two explicit three-point Kummer
coefficients.  If

```text
B_{alpha,beta,gamma}
  = sum_s alpha(s) beta(2s+delta) gamma(s-delta),
```

then

```text
A_{eta,nu}(theta)
  = eta(-1) (
      B_{theta nu, eta, (eta nu)^(-1)}
      + B_{theta nu chi_2, eta, (eta nu)^(-1)}
    ).
```

Thus the nonsplit projector is no longer an opaque one-variable trace.  The
kernel side `M_nu(theta)` is a product of Jacobi sums, and the outer side is a
pair of three-point Kummer coefficients supported at
`s=0`, `s=delta`, `s=-delta/2`, and infinity.  Termwise estimates give only a
`p^{3/2}`-scale fallback, so the desired `p`-scale nonsplit projector theorem
has been localized to cancellation across the Mellin parameter `theta`.

## Outer Kummer Fixed-Support Form

The outer Kummer coefficient has a fixed four-point normal form independent of
the nonsquare `delta`.  For

```text
B_{alpha,beta,gamma}
  = sum_s alpha(s) beta(2s+delta) gamma(s-delta),
```

put `z=-2s/delta`.  Then

```text
B_{alpha,beta,gamma}
  = alpha(-delta/2) beta(delta) gamma(-delta/2)
      sum_z alpha(z) beta(1-z) gamma(z+2).
```

Thus every outer coefficient is a scalar multiple of the same Kummer trace on
`P^1_z` with finite support at

```text
z=0,        z=1,        z=-2,
```

and infinity.  The nonsquare `delta` only changes the scalar character value;
the conductor geometry of the outer spectrum is the fixed
`{0,1,-2,infinity}` table.  This is the precise object whose phases must
correlate with the normalized kernel phases in the generic reduction below.

## Outer Mellin Square-Root Bound

The outer coefficients in the spectral normal form have a uniform
square-root bound.  Each term

```text
B_{alpha,beta,gamma}
  = sum_s alpha(s) beta(2s+delta) gamma(s-delta)
```

is a genus-zero Kummer sum on `P^1_s` with possible finite support at
`s=0`, `s=-delta/2`, and `s=delta`, plus infinity.  In the transformed
line-conic target `beta=eta` is nonprincipal, so the sheaf is not
geometrically constant even if `alpha` or `gamma` is principal.  The standard
genus-zero estimate therefore gives

```text
|B_{alpha,beta,gamma}| <= 2sqrt(p).
```

Since `A_{eta,nu}(theta)` is the sum of two such coefficients,

```text
|A_{eta,nu}(theta)| <= 4sqrt(p).
```

Combined with `|M_nu(theta)| <= p`, this recovers the termwise
`O(p^{3/2})` fallback in the spectral normal form.  The energy ledger below
is sharper on average, but it still does not supply the phase cancellation
needed for a pointwise `O(p)` theorem.

## Exceptional Mellin Parameters

The special Mellin parameters in the kernel magnitude ledger are harmless.
Let

```text
E_nu = {epsilon, chi_2} union {theta: theta^2=nu}.
```

The last set has two elements when `nu(-1)=1` and is empty when
`nu(-1)=-1`.  In the spectral pairing

```text
P_{eta,nu} = 1/(p-1) sum_theta A_{eta,nu}(theta^(-1))M_nu(theta),
```

the exceptional contribution satisfies

```text
|1/(p-1) sum_{theta in E_nu} A(theta^(-1))M(theta)|
  <= 4sqrt(p)(p+1+2sqrt(p) 1_{nu(-1)=1})/(p-1).
```

Indeed `|A(theta)| <= 4sqrt(p)`, while the exceptional kernel magnitudes are
`p`, `1`, and two possible `sqrt(p)` values.  This is `O(sqrt(p))`, and the
separate singular term `eta(-2)G_nu(2)` has size at most `1`.  Therefore all
p-scale difficulty in the nonsplit projector sits in the generic set
`theta notin E_nu`, where `|M_nu(theta)|=p`.

## Generic Phase Reduction

On the generic set `G_nu = {theta: theta notin E_nu}`, write

```text
omega_nu(theta) = M_nu(theta)/p.
```

The magnitude ledger gives `|omega_nu(theta)|=1` on `G_nu`.  Hence the
nonsplit projector has the exact residual form

```text
C^-_{eta,nu}
  = eta(-2)G_nu(2)
    + chi_2(-3)P^exc_{eta,nu}
    + chi_2(-3) p/(p-1)
        sum_{theta in G_nu} A_{eta,nu}(theta^(-1)) omega_nu(theta),
```

where `P^exc_{eta,nu}` is the exceptional contribution bounded above by
`O(sqrt(p))`.  Thus the pointwise p-scale nonsplit theorem is now exactly a
square-root cancellation problem for the generic phase sum

```text
sum_{theta in G_nu} A_{eta,nu}(theta^(-1)) omega_nu(theta),
```

whose individual terms have size at most `4sqrt(p)`.  No further saving can
come from kernel magnitude on this generic set: the kernel contributes only a
unit phase after the factor `p` is extracted.

## Delta-Free Quadratic-Pair Correlation

The generic phase sum has one more exact normalization.  The generic set is
stable under `theta -> theta chi_2`, and the outer coefficient is invariant
under this shift:

```text
A_{eta,nu}(theta chi_2) = A_{eta,nu}(theta).
```

Indeed, the outer summand contains the square-projector factor
`1+chi_2(s)`, and `(1+chi_2(s))chi_2(s)=1+chi_2(s)` on `F_p^*`.  Therefore,
for any representative set `R_nu` of `G_nu/{1,chi_2}`,

```text
sum_{theta in G_nu} A(theta^(-1))omega_nu(theta)
  = sum_{theta in R_nu}
      A(theta^(-1))(omega_nu(theta)+omega_nu(theta chi_2)).
```

This folded summand is independent of the nonsquare parameter.  Put

```text
c=4delta,        q=-delta/2,        gamma=(eta nu)^(-1),
S_alpha=sum_z alpha(z) eta(1-z) gamma(z+2).
```

The fixed-support form gives

```text
A(theta^(-1))
  = eta(2)theta(q)^(-1)
      (S_{theta^(-1)nu} - chi_2(-2)S_{theta^(-1)nu chi_2}).
```

On the generic set the kernel formula gives

```text
omega_nu(theta)+omega_nu(theta chi_2)
  = chi_2(-c)nu(-1)theta(c)J(theta^(-2),nu)
      (J(theta,chi_2)-J(theta chi_2,chi_2))/p,
```

because `chi_2(c)=-1`.  Multiplying the two identities cancels the
`delta`-dependent theta factor:

```text
A(theta^(-1))(omega_nu(theta)+omega_nu(theta chi_2))
  = -chi_2(-1)eta(2)nu(-1)theta(-8)
      (S_{theta^(-1)nu} - chi_2(-2)S_{theta^(-1)nu chi_2})
      J(theta^(-2),nu)
      (J(theta,chi_2)-J(theta chi_2,chi_2))/p.
```

Thus the whole generic obstruction is a fixed character-correlation table in
`theta`: the outer support is `{0,1,-2,infinity}`, the kernel is the
quadratic-paired Jacobi difference above, and no nonsquare `delta` remains in
the paired summand.  Also

```text
J(theta,chi_2)J(theta chi_2,chi_2)=chi_2(-1)p
```

for generic `theta`, so the paired kernel factor has absolute value at most
`2`.  This does not yet prove the required `p`-scale bound, but it removes a
spurious nonsquare-parameter degree of freedom from the remaining
correlation problem.

## Quadratic-Pair Square-Class Filters

The paired formula above has an even sharper elementary form: both
differences are square-class filters.  Define

```text
S_alpha^{[-2]}
  = sum_z alpha(z)(1-chi_2(-2)chi_2(z)) eta(1-z) gamma(z+2),

D_theta^-
  = sum_x theta(x)(1-chi_2(x))chi_2(1-x).
```

Then

```text
S_alpha^{[-2]} = S_alpha - chi_2(-2)S_{alpha chi_2},
D_theta^-      = J(theta,chi_2)-J(theta chi_2,chi_2).
```

Thus the delta-free paired summand is

```text
A(theta^(-1))(omega_nu(theta)+omega_nu(theta chi_2))
  = -chi_2(-1)eta(2)nu(-1)theta(-8)
      S_{theta^(-1)nu}^{[-2]}
      J(theta^(-2),nu)
      D_theta^- / p.
```

The kernel factor `D_theta^-` is supported only on nonsquare `x`.  The outer
factor is supported only on the opposite square class to `chi_2(-2)`:
on nonsquare `z` if `chi_2(-2)=1`, and on square `z` if
`chi_2(-2)=-1`.  The remaining generic M1 obstruction is therefore not a
correlation of two arbitrary four-point Kummer traces; after quadratic
pairing, it is a product of fixed Kummer tables with explicit square-class
gates.  This is the natural form for any later sheaf-correlation or
diagonal/off-diagonal attack on the paired theta sum.

## Paired Diagonal Expansion

The square-class filtered paired sum can be collapsed completely by
multiplicative orthogonality.  Write

```text
Pi_{eta,nu}(theta)
  = -chi_2(-1)eta(2)nu(-1)theta(-8)
      S_{theta^(-1)nu}^{[-2]}
      J(theta^(-2),nu)
      D_theta^- / p.
```

Let

```text
kappa_{eta,nu} = -chi_2(-1)eta(2)nu(-1),
gamma=(eta nu)^(-1).
```

Expanding the three filtered factors and summing over all multiplicative
characters `theta` gives

```text
sum_theta Pi_{eta,nu}(theta)
  = kappa_{eta,nu}(p-1)/p
      sum_{z,y in F_p^*, -8x=z y^2}
        nu(z)nu(1-y)
        (1-chi_2(-2)chi_2(z))(1-chi_2(x))
        eta(1-z)gamma(z+2)chi_2(1-x).
```

Indeed the theta dependence in the expanded summand is
`theta(-8x/(z y^2))`, so the theta sum vanishes unless `-8x=z y^2`,
where it contributes `p-1`.  The zero-extension convention is already
accounted for by `z,y in F_p^*`; then `x` is automatically nonzero.

The actual generic phase sum is obtained from this diagonal sum by deleting
the exceptional theta orbits:

```text
sum_{theta in G_nu} A(theta^(-1))omega_nu(theta)
  = 1/2 (
      sum_theta Pi_{eta,nu}(theta)
      - sum_{theta in E_nu} Pi_{eta,nu}(theta)
    ).
```

The factor `1/2` appears because `Pi(theta chi_2)=Pi(theta)`, so the
all-character sum counts each quadratic pair twice.  This is an exact
finite-field identity.  It turns the remaining M1 generic obstruction into a
single constrained two-variable sum plus the already isolated exceptional
theta correction.

## Spectral Energy Ledger

The spectral normal form has exact energy identities.  By Parseval on
`F_p^*` and the quotient-line moment above,

```text
sum_theta |M_nu(theta)|^2
  = (p-1)(p^2 - 2p - 1 - p nu(-1)).
```

The outer side is also exact.  The finite values of the outer summand have
magnitude `2` precisely when `s` is a nonzero square and
`2s+delta != 0`; they vanish at `s=0`, at nonsquares, and at
`s=-delta/2` if that point is a square.  Since `delta` is nonsquare,
`-delta/2` is square exactly when `chi_2(-2)=-1`.  Therefore

```text
sum_s |(1+chi_2(s)) eta(-(2s+delta)/(s-delta))nu(s/(s-delta))|^2
  = 2(p-2+chi_2(-2)),
```

and Parseval gives

```text
sum_theta |A_{eta,nu}(theta)|^2
  = 2(p-1)(p-2+chi_2(-2)).
```

Consequently the exact Cauchy fallback from the spectral normal form is

```text
|1/(p-1) sum_theta A_{eta,nu}(theta^(-1))M_nu(theta)|
  <= sqrt(2(p-2+chi_2(-2))(p^2 - 2p - 1 - p nu(-1))).
```

This is a theorem-grade `O(p^{3/2})` bound, not the desired `O(p)` bound.
Thus separate control of the outer and kernel spectra is not enough.  The
remaining nonsplit problem is now sharply phrased as cancellation in their
correlation across `theta`.

## Twisted-Line Kernel Moment

The translated kernel has no hidden large average.  For every nonprincipal
`nu`,

```text
sum_t K_{nu,delta}(t) = 0,
sum_t |K_{nu,delta}(t)|^2 = p^2 - 1.
```

For the first identity, interchange sums:

```text
sum_t K_{nu,delta}(t)
  = sum_x chi_2(x^2-4delta) sum_t nu(x-t) = 0.
```

For the second, write `b_x=chi_2(x^2-4delta)`.  Since `delta` is nonsquare,
`x^2-4delta` never vanishes over `F_p`, so `b_x^2=1` for all `x`, and

```text
sum_x b_x = -1.
```

By multiplicative-character correlation,

```text
sum_t nu(x-t) nu^(-1)(z-t)
  = p-1        if x=z,
  = -1         if x!=z.
```

The off-diagonal value follows from the fractional-linear change of variable
`r=(x-t)/(z-t)`, which misses only `r=1`, and from nonprincipal
orthogonality.  Therefore

```text
sum_t |K(t)|^2
  = (p-1) sum_x b_x^2
    - sum_{x!=z} b_x b_z
  = p(p-1) - ((sum_x b_x)^2 - sum_x b_x^2)
  = p(p-1) - (1-p)
  = p^2-1.
```

Thus the kernel's root-mean-square size is exactly `sqrt(p-1/p)`.  This is
much smaller than the pointwise `2sqrt(p)` conductor ceiling on average, and
it rules out a hidden large kernel-average obstruction behind the nonsplit
projector.  The remaining problem is cancellation in the outer
`eta,nu`-twisted transform of this rank-two trace.

## Open-Set Line Correction

For the actual two-coordinate open sum, the principal coordinate line
`w=0`, i.e. `v=-1-u`, must be removed.  The correction is

```text
L_{eta,nu} =
  sum_u eta^(-1)(u) nu(-1-u) eta(-(u^2+u+1)).
```

This is a genus-zero Kummer sum on `P^1_u` with support contained in

```text
u=0,        u=-1,        u^2+u+1=0,        infinity.
```

Since `eta` is nonprincipal, the local monodromy at `u=0` is nontrivial, so
the standard genus-zero bound gives `|L_{eta,nu}| <= 3 sqrt(p)`.  Thus the
remaining conductor issue for the open line-conic-resonant slice is exactly
the one-dimensional `y`-family above, plus this already understood
line correction.

## Relation to the M1 Wall

The line-conic-resonant mass was isolated in
`experimental/m1_depth_two_lift_window_theorem.md` as `C_2^lc`.  Combining
this reduction with a future conductor bound for `G_nu(y)` would remove the
last two-coordinate slice still charged at the old `9p` import after the
conditional projective-equal and nonresonant ledgers.

## Admissible Character Filter

The transformed pair `(eta,nu)` is not arbitrary in the actual asymmetric
`C_2^lc` ledger.  Fix one projective line-conic resonance and divide the
common character order by the coordinate-character lift.  Write the resonant
line exponent as `a` and the second active line exponent as `b`, with
`a,b in Z/eZ` nonzero.  The conic exponent is then `-a`, so in the notation
of this note

```text
eta = chi^{-a},        nu = chi^b.
```

The three projective line exponents are

```text
a,        b,        a-b.
```

The already removed equal-line and reciprocal-line slices are exactly the
four forbidden relations

```text
b = a,        b = -a,        b = 2a,        2b = a        mod e.
```

Thus the actual character range for the transformed `C_2^lc` conductor
target is

```text
a,b != 0,        b != a,        b != -a,
b != 2a,         2b != a        mod e.
```

In this range the other two possible line-conic resonances are also absent:
`nu eta=1` would give `b=a`, and `lambda eta=1` would give `b=0`, where
`lambda=(nu eta)^(-1)` is the infinity-line monodromy.

Inclusion-exclusion over the four forbidden relations gives the per-fixed
resonant-line count

```text
R(e) = (e-1)(e-5) + 3 1_{2|e} + 2(gcd(e,3)-1).
```

This is the character-side form of the `C_2^lc` split:

```text
C_2^lc = 9R(e).
```

The factor `9` is the product of the three active coordinate pairs and the
three possible resonant projective lines.  The finite verifier checks the
filter, its equivalence with "no equal or reciprocal projective line pair",
and the displayed count directly for character orders `2 <= e <= 40`.

## Conditional Ledger Target

The precise conductor target is now the following one-dimensional statement:

```text
|C_{eta,nu}| <= 4p
```

for every nonprincipal line-conic-resonant pair occurring in `C_2^lc`.  Since
the open two-coordinate sum differs from `C_{eta,nu}` by the genus-zero line
correction above, this would give the certificate-facing replacement

```text
|S_open| <= 4p + 3 sqrt(p)
```

on the whole `C_2^lc` slice.  This is intentionally recorded as a
`CONDITIONAL` target, not as a proved theorem: the missing input is the
middle-extension conductor bound for the rank-two quadratic-fiber
pushforward on the `y`-line.

The saturation scanner now reports this optional ledger separately.  If the
projective equal-pair import, the clean nonresonant line/conic import, and
this line-conic-resonant conductor import are all accepted, the residual
ramified nonreciprocal two-coordinate mass after the proved
`C_2^0` and `C_2^rec` reductions is charged at

```text
4(C_2^peq + C_2^anr + C_2^lc)
  = 4(C_2^peq + C_2^asym).
```

Equivalently, relative to the conservative `9p` charge on that residual, the
leading L1 weight drops by `5(C_2^peq+C_2^asym)` and the square-root mass
adds `3(C_2^peq+C_2^asym)`.  The active `saturation_certificate` remains
unchanged.

The verifier also performs a finite counterexample-first audit for this
target.  It exhausts all nonprincipal `(eta,nu)` for `p=17,31` and checks
targeted larger cases; in the current audit it reports no `4p` violation for
the core or open sums and no `3 sqrt(p)` violation for the line correction.
The remaining-wall scanner also has a dedicated line-conic-resonant pass:
in its current report grid, the largest `C_2^lc` asymmetric ratio is
`2.7649691518p`, below the nonresonant asymmetric maximum
`3.2173609608p`.

## Full-Character Second Moment

The transformed core also has an exact orthogonality check.  Sum over all
multiplicative characters `eta,nu` of `F_p^*`, including the principal
character extended by zero.  Then

```text
sum_{eta,nu} |C_{eta,nu}|^2 = (p-1)^2 S_p,

S_p = 2p^2 - 8p + 13 - chi_2(-3)p + 9chi_2(-3) + chi_2(-2).
```

Indeed, character orthogonality gives `(p-1)^2` times the number of
collisions

```text
v=v' != 0,        A(u,v)/u = A(u',v)/u' != 0.
```

For fixed `v`, this is the collision count of

```text
u |-> -(u+v+1+B(v)/u),        u in F_p^*.
```

If `B(v) != 0`, the only collisions are

```text
u=u'        or        uu'=B(v).
```

Thus the count for that `v` is

```text
2(p-1) - (1+chi_2(B(v))) - (1+chi_2(Delta(v)))^2,
Delta(v) = -3v^2 - 2v - 3,
```

where the first subtraction removes the double-counted branch points and the
second removes the zero value `A=0`.  If `B(v)=0`, the map is linear on
`F_p^*` and the nonzero-value count is `p-2`.

Summing over `v in F_p^*` uses

```text
sum_{v in F_p^*} chi_2(B(v)) = -2,
sum_{B(v)!=0} chi_2(Delta(v)) = -1 - 3chi_2(-3),
#{v in F_p^*: B(v)!=0, Delta(v)!=0}
  = p - 3 - chi_2(-3) - chi_2(-2),
```

which gives the displayed formula for `S_p`.  In particular the full-family
root-mean-square core size is `sqrt(S_p) < sqrt(2)p`.  This does not prove
the pointwise `4p` target, but it rules out any hidden large average behind
the line-conic resonant family.

The removed line has an even simpler full-character moment:

```text
sum_{eta,nu} |L_{eta,nu}|^2
  = (p-1)^2 (p - 3 - chi_2(-3)).
```

Here orthogonality forces `-1-u=-1-u'` and then `u=u'`; the support excludes
`u=0`, `u=-1`, and the `1+chi_2(-3)` roots of `u^2+u+1`.

## Nonprincipal Second Moment

The full-character moment above still includes the principal `eta` and `nu`
rows, which are not part of the line-conic-resonant M1 target.  These rows
carry a visible part of the average.  Removing them gives an exact
nonprincipal moment.

Let

```text
S = {(u,v): u != 0, v != 0, A(u,v) != 0},
        x(u,v)=A(u,v)/u.
```

Write

```text
T_p = #S,
N_x = sum_{x in F_p^*} #{(u,v) in S: x(u,v)=x}^2,
N_v = sum_{v in F_p^*} #{u: (u,v) in S}^2.
```

Then

```text
T_p = p^2 - 3p + 3 + 3 chi_2(-3),

N_x = p^3 - 3p^2 + 5p - 19
      + (6p - 16) chi_2(-3),

N_v = p^3 - 5p^2 + 11p - 11
      + (6p - 13) chi_2(-3) - chi_2(-2).
```

Consequently

```text
sum_{eta != 1, nu != 1} |C_{eta,nu}|^2
  = (p-1)^2 S_p - (p-1)(N_x+N_v) + T_p^2

  = p^4 - 8p^3 + 22p^2 - 6p + 1
    + (-p^3 + 5p^2 + 4p - 2) chi_2(-3)
    + (p^2 - p) chi_2(-2).
```

Thus the true nonprincipal family has root-mean-square size
`p+O(1)`, rather than the `sqrt(2)p+O(1)` full-character RMS.  The
principal rows account for the missing average mass; the actual resonant
target has no hidden large second moment.

For the proof, nonprincipal orthogonality gives

```text
sum_{eta != 1} eta(x/x') = (p-1) 1_{x=x'} - 1,
sum_{nu != 1} nu(v/v') = (p-1) 1_{v=v'} - 1.
```

Expanding the product gives the displayed formula in terms of `S_p`, `N_x`,
`N_v`, and `T_p`.

It remains only to compute the two marginal collision sums.  For fixed
`v != 0`,

```text
#{u: (u,v) in S}
  = p - 2 - chi_2(-3v^2-2v-3) + 1_{v^2+v+1=0}.
```

Squaring and summing over `v != 0`, using the elementary quadratic sums for
`-3v^2-2v-3` and `v^2+v+1`, gives the displayed `N_v`.

For fixed `x != 0`, the equation `x=A(u,v)/u` is the affine conic

```text
u^2+v^2+uv+(x+1)u+v+1=0
```

with `u,v != 0`.  Its projective determinant is
`-(x-1)(x+2)/4`.  For `x != 1,-2`, the conic is nonsingular; it has
`p+1` projective points, `1+chi_2(-3)` points at infinity, and the removed
coordinate lines contribute `1+chi_2(-3)` points with `u=0` and
`1+chi_2((x-1)(x+3))` points with `v=0`.  Hence

```text
#{(u,v) in S: x(u,v)=x}
  = p - 2 - 2 chi_2(-3) - chi_2((x-1)(x+3)).
```

At the two degenerate values, the singular points are `(-1,0)` for `x=1`
and `(1,-1)` for `x=-2`, with tangent cone `U^2+UV+V^2`.  Therefore

```text
M_1    = (1+chi_2(-3))(p-2),
M_{-2} = 1 + (1+chi_2(-3))(p-3).
```

Summing these squared fiber sizes over `x in F_p^*` gives the displayed
`N_x`.

## Principal-Row Leakage

The principal rows excluded above have exact formulas.  They explain why the
full-character moment has RMS `sqrt(2)p+O(1)` while the actual nonprincipal
target has RMS `p+O(1)`.

If `eta=1` and `nu` is nonprincipal, then

```text
C_{1,nu}
  = -sum_v nu(v) chi_2(-3v^2-2v-3)
    + sum_{v^2+v+1=0} nu(v).
```

This is only a genus-zero-size row: the first term is a Kummer sum on
`P^1_v` with support contained in `v=0`, the two roots of
`-3v^2-2v-3`, and infinity, while the second term has at most two summands.

If `nu=1` and `eta` is nonprincipal, then

```text
C_{eta,1}
  = -sum_x eta(x) chi_2((x-1)(x+3))
    + chi_2(-3) p (eta(1)+eta(-2)).
```

Thus the `nu=1` row contains the two `p`-scale exceptional conic
degeneracies at `x=1` and `x=-2`.  These rows are not part of `C_2^lc`, but
they account for the extra full-character second-moment mass.

Finally,

```text
C_{1,1} = T_p = p^2 - 3p + 3 + 3chi_2(-3).
```

The first formula follows from fixed `v`: the number of contributing
`u != 0` is

```text
p - 2 - chi_2(-3v^2-2v-3) + 1_{v^2+v+1=0},
```

and the constant term vanishes against nonprincipal `nu`.  The second follows
from fixed `x=A/u`: the generic conic count is

```text
p - 2 - 2chi_2(-3) - chi_2((x-1)(x+3)),
```

but at the two degenerate values `x=1,-2` the actual count differs by
`chi_2(-3)p`, giving the exceptional term.

The finite verifier is

```bash
python3 experimental/verify_m1_depth_two_line_conic_resonance_reduction.py
```
