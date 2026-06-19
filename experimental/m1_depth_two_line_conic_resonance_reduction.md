# M1 Depth-Two Line-Conic Resonance Reduction

**Status:** PROVED / CONDITIONAL / AUDIT.

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

## Collapsed Diagonal Gate

On the diagonal `-8x=z y^2`, the two square-class filters are the same:

```text
chi_2(x)=chi_2(-2)chi_2(z).
```

Hence

```text
(1-chi_2(-2)chi_2(z))(1-chi_2(x))
  = 2(1-chi_2(-2)chi_2(z)).
```

Therefore the all-theta paired diagonal sum is equivalently

```text
sum_theta Pi_{eta,nu}(theta)
  = 2 kappa_{eta,nu}(p-1)/p
      sum_{z,y in F_p^*}
        nu(z)nu(1-y)
        (1-chi_2(-2)chi_2(z))
        eta(1-z)gamma(z+2)chi_2(1+z y^2/8).
```

Equivalently, with

```text
H_nu(z)=sum_{y in F_p^*} nu(1-y)chi_2(1+z y^2/8),
```

this is the one-variable transform

```text
2 kappa_{eta,nu}(p-1)/p
  sum_{z in F_p^*}
    nu(z)(1-chi_2(-2)chi_2(z))eta(1-z)gamma(z+2)H_nu(z).
```

Thus the paired diagonal no longer has two independent square-class gates:
the diagonal relation forces them to coincide.  The remaining main term is a
single square-class restricted outer Kummer twist against the explicit
quadratic trace `H_nu(z)`, plus the exceptional theta correction from the
previous section.

## Collapsed Inner Trace Spectrum

The new inner trace has an exact Mellin spectrum.  For

```text
H_nu(z)=sum_{y in F_p^*} nu(1-y)chi_2(1+z y^2/8),
```

one has

```text
H_nu(0)=-1,
H_nu(-8)=nu(2)J(nu chi_2,chi_2)-1.
```

The second identity follows from

```text
H_nu(-8)=sum_{y != 0} nu(1-y)chi_2(1-y^2)
```

and the substitution `t=(1-y)/2`; the omitted point `y=0` contributes the
subtracted `1`.  For every multiplicative character `rho`,

```text
sum_{z in F_p^*} rho(z)H_nu(z)
  = rho(-8)J(rho,chi_2)J(rho^(-2),nu).
```

Indeed, after interchanging the `z` and `y` sums, the change of variable
`w=-z y^2/8` gives

```text
sum_z rho(z)chi_2(1+z y^2/8)
  = rho(-8)rho^(-2)(y)J(rho,chi_2),
```

and the remaining `y`-sum is `J(rho^(-2),nu)`.  Therefore, for nonprincipal
`nu`,

```text
|sum_z rho(z)H_nu(z)| =
  1,        rho=epsilon or rho=chi_2,
  sqrt(p),  rho^2=nu,
  p,        otherwise.
```

The square-root line has two characters exactly when `nu(-1)=1` and is
empty when `nu(-1)=-1`.  Parseval gives the exact moment

```text
sum_{z in F_p^*} |H_nu(z)|^2 = p^2 - 3p - 2 - p nu(-1).
```

Thus the collapsed inner trace has RMS size `sqrt(p)+O(1)` and no hidden
large average, but its Mellin spectrum is still generically `p`-sized.  The
remaining M1 work is not to make `H_nu` small termwise; it is to exploit
cancellation when this explicit trace is multiplied by the square-class
restricted outer Kummer twist in the collapsed diagonal transform.

## Collapsed Inner Pointwise Bound

The inner trace also has a uniform conductor bound.  Put

```text
L_nu(z)=H_nu(z)+1
      = sum_{y in F_p} nu(1-y)chi_2(1+z y^2/8).
```

For `z notin {0,-8}`, this is a genus-zero Kummer sum on `P^1_y` with
finite support at

```text
y=1,        1+z y^2/8=0,
```

and with infinity as the remaining support point.  The two quadratic roots
are geometrically distinct and do not collide with `y=1` precisely away from
`z=-8`.  Since `nu` is nonprincipal, the local monodromy at `y=1` is
nontrivial, so the sheaf is not geometrically constant.  The standard
four-point genus-zero bound gives

```text
|L_nu(z)| <= 2sqrt(p),        z notin {0,-8},
```

and hence

```text
|H_nu(z)| <= 2sqrt(p)+1,      z notin {0,-8}.
```

At the two excluded values, the special formulas above give

```text
H_nu(0)=-1,        |H_nu(-8)| <= sqrt(p)+1.
```

Thus the collapsed inner trace has no pointwise spike beyond its expected
four-point conductor.  This supplies the local ceiling for the final
one-variable transform; the desired p-scale bound still requires
cancellation against the outer Kummer twist.

## Finite Singular Cancellation

The collapsed one-variable main term has no finite singular contribution.
Its finite candidate bad values are

```text
z=0,        z=1,        z=-2,        z=-8.
```

The first three are the outer Kummer points and the last is the new singular
point of `H_nu`.  In the collapsed summand

```text
nu(z)(1-chi_2(-2)chi_2(z))eta(1-z)gamma(z+2)H_nu(z),
```

they vanish termwise:

```text
z=0:        nu(z)=0,
z=1:        eta(1-z)=0,
z=-2:       gamma(z+2)=0,
z=-8:       1-chi_2(-2)chi_2(z)=0.
```

The last equality uses `chi_2(-8)=chi_2(-2)`.  Thus the new singular value
`H_nu(-8)` is exactly projected out by the same square-class gate that arose
from the quadratic pairing.  The collapsed main term is therefore supported
only on the lisse finite `z`-line; the remaining conductor issue is at the
open correlation and infinity, not at a finite exceptional value.

## Conditional Collapsed Conductor Bound

The previous reductions isolate a standard one-variable conductor import.
Let

```text
W_{eta,nu}(z)
  = nu(z)(1-chi_2(-2)chi_2(z))eta(1-z)gamma(z+2),
L_nu(z)=H_nu(z)+1.
```

Then the collapsed main transform splits as

```text
sum_z W_{eta,nu}(z)H_nu(z)
  = sum_z W_{eta,nu}(z)L_nu(z) - sum_z W_{eta,nu}(z).
```

The second term is already theorem-grade.  Write

```text
B(alpha,beta,gamma)=sum_z alpha(z)beta(1-z)gamma(z+2).
```

Then

```text
sum_z W_{eta,nu}(z)
  = B(nu,eta,gamma) - chi_2(-2)B(nu chi_2,eta,gamma).
```

Each `B` is a four-point genus-zero Kummer sum on `P^1_z`, supported at
`z=0,1,-2,infinity`.  In both summands the local monodromy at `z=1` is
`eta`, which is nonprincipal, so the sheaf is not geometrically constant.
The standard genus-zero bound gives

```text
|B(nu,eta,gamma)| <= 2sqrt(p),
|B(nu chi_2,eta,gamma)| <= 2sqrt(p),
```

and therefore

```text
|sum_z W_{eta,nu}(z)| <= 4sqrt(p).
```

Thus the only p-scale input still being imported is the first term.  This
term has a cleaner Mellin normal form.  Put

```text
r=(1-z)/(z+2),        z=(1-2r)/(r+1).
```

Then `z+2=3/(r+1)` and `z/(z+2)=(1-2r)/3`.  Since
`gamma=(eta nu)^(-1)`,

```text
eta(1-z)gamma(z+2)nu(z)
  = eta(r)nu(z/(z+2))
  = eta(r)nu((1-2r)/3).
```

Consequently

```text
sum_z W_{eta,nu}(z)L_nu(z)
  = sum_{r in F_p^*, r != -1} eta(r) Phi_nu(r),
```

where

```text
Phi_nu(r)
  = nu((1-2r)/3)
    (1-chi_2(-2)chi_2((1-2r)/(r+1)))
    L_nu((1-2r)/(r+1)).
```

The finite deleted/collision points are explicit: `r=1/2` maps to `z=0`
and is killed by `nu((1-2r)/3)`, while `r=-3/2` maps to `z=-8` and is
killed by the square-class gate.  The point `r=0` maps to `z=1` and is
outside the Mellin torus, and `r=-1` is the missing value corresponding to
`z=infinity`.

The remaining p-scale theorem is therefore a uniform Mellin-transform bound
for the `nu`-dependent trace `Phi_nu`.

There is already an average p-scale theorem in the `eta` aspect.  The active
`r`-support of `Phi_nu` has size

```text
A_p = (p-1)/2,  chi_2(-2)=1,
A_p = (p-3)/2,  chi_2(-2)=-1,
```

because the square-class gate selects `chi_2(z)=-chi_2(-2)`, the point
`z=0` is killed by the `nu(z/(z+2))` factor, and the selected point `z=1`
is outside the Mellin torus exactly when `chi_2(-2)=-1`.  On this active
support the pointwise inner bound gives

```text
|Phi_nu(r)| <= 4sqrt(p),
```

so

```text
E_nu := sum_{r in F_p^*} |Phi_nu(r)|^2
  <= 16p A_p
  <= 8p(p-1).
```

The exact full-energy ledger sharpens this.  From the collapsed inner
Mellin spectrum,

```text
sum_{z in F_p^*} |L_nu(z)|^2 = p^2 - 2p - 1 - p nu(-1).
```

Since `Phi_nu` is `2 L_nu(z)` times a unit character on one selected
square class and vanishes elsewhere,

```text
E_nu <= 4(p^2 - 2p - 1 - p nu(-1)) < 4p^2.
```

By Parseval on `F_p^*`,

```text
1/(p-1) sum_eta |sum_r eta(r)Phi_nu(r)|^2 = E_nu.
```

Thus the remaining rank-two transform is already `O(p)` in RMS over
`eta`, with RMS strictly below `2p`.  The missing theorem is not an
average-mass statement; it is a uniform pointwise Mellin-coefficient bound
for this explicit trace.

The selected square-class energy has a sharper parity refinement.  Let

```text
Q_nu = sum_{z in F_p^*} chi_2(z)|L_nu(z)|^2.
```

Then

```text
|Q_nu| <= p,        nu(-1)=-1,
|Q_nu| <= 3p,       nu(-1)= 1.
```

Here is the proof.  Write

```text
B(t)=sum_w chi_2(w(1+w)(1+t^2 w)).
```

Expanding `Q_nu`, setting `y=ts` for `s != 0`, and using the correlation

```text
sum_s nu(1-ts)nu^(-1)(1-s)
  = p-1,        t=1,
  = -nu(t),     t != 1,
```

with the `s=0` term removed gives

```text
Q_nu = chi_2(8)(pB(1)-T_nu),
T_nu = sum_t nu(t)B(t).
```

The two elementary identities used here are

```text
B(1)=-chi_2(-1),        sum_t B(t)=1.
```

Since `B(t)=B(-t)`, the term `T_nu` vanishes when `nu(-1)=-1`; hence
`|Q_nu|=p` in the odd case.  If `nu(-1)=1`, choose a character `alpha` with
`alpha^2=nu`.  Interchanging the `t` and `w` sums and evaluating the two
quadratic fibers gives

```text
T_nu = chi_2(-1)(
  J(alpha,chi_2)J(alpha^(-1)chi_2,chi_2)
  + J(alpha chi_2,chi_2)J(alpha^(-1),chi_2)).
```

Each Jacobi product has absolute value at most `p`, so `|T_nu|<=2p`, and
therefore `|Q_nu|<=3p`.

Consequently the selected energy satisfies the uniform bound

```text
E_nu
 = sum_z (1-chi_2(-2)chi_2(z))^2 |L_nu(z)|^2
 = 2 sum_z |L_nu(z)|^2 - 2 chi_2(-2)Q_nu
 <= 2p^2 - 2.
```

Indeed, when `nu(-1)=-1`, the full energy is `p^2-p-1` and the twisted
term costs at most `2p`; when `nu(-1)=1`, the full energy is `p^2-3p-1`
and the twisted term costs at most `6p`.  Parseval on `F_p^*` therefore
improves the RMS ceiling to

```text
RMS_eta <= sqrt(2p^2-2) < sqrt(2)p.
```

This also gives a clean large-coefficient sparsity statement.  For any
`Lambda>0`, let

```text
N_nu(Lambda)
  = #{eta : |sum_r eta(r)Phi_nu(r)| >= Lambda p}.
```

Then Parseval and the selected-energy bound give

```text
N_nu(Lambda)
  <= (p-1)(2p^2-2)/(Lambda^2 p^2).
```

In particular, coefficients of size at least `4p` occupy less than one
eighth of the Mellin characters:

```text
N_nu(4) <= floor((p-1)(p^2-1)/(8p^2)) < (p-1)/8.
```

So a finite row above `4p` is compatible with the average theory, but such
rows cannot form a dense obstruction.  The remaining conductor problem is
to bound these sparse exceptional Mellin coefficients, or to exploit their
cancellation in the paired generic ledger.

The same estimate applies after restricting `eta` to the actual
line-conic-resonant admissible set for fixed `nu`, since that set is a
subset of all Mellin characters.  Thus for each fixed `nu`, fewer than
`(p-1)/8` admissible `eta` can have a collapsed rank-two coefficient of
size at least `4p`.  The verifier audits the exact counts in the checked
range; the current maxima are one `4p`-scale coefficient in all characters
and one in the admissible slice.  This is a useful tension: the obstruction
to a sharp standalone `4p` theorem is genuine for `C_2^lc`, but it is
provably sparse in every fixed-`nu` Mellin slice.

The same audit rules out one tempting sharp shortcut.  A standalone `4p`
pointwise bound for the collapsed rank-two import is false in the checked
range: at `(p,eta,nu)=(97,13,91)` (exponents relative to the verifier's
primitive character),

```text
|sum_z W_{eta,nu}(z)L_nu(z)|/p = 4.1552812817,
|sum_z W_{eta,nu}(z)H_nu(z)|/p = 4.1800884464.
```

These are nonprincipal, nonquadratic character rows and not one of the
square-root exceptional relations.  They also satisfy the actual
line-conic-resonant admissible filter with
`a=-eta=83`, `b=nu=91` modulo `96`, so this is not only a broad-import
artifact.  Thus the remaining import should be treated as a p-scale
conductor theorem with its own constant, or combined with later
cancellation; it should not be replaced by an unsupported standalone `4p`
collapsed-transform claim.

Equivalently, split the square-class gate:

```text
W_{eta,nu}
  = nu(z)eta(1-z)gamma(z+2)
    - chi_2(-2)nu(z)chi_2(z)eta(1-z)gamma(z+2).
```

Each summand is the trace of the rank-two sheaf behind `L_nu` tensor a
rank-one Kummer twist supported at `z=0,1,-2,infinity`.  The finite singular
point `z=-8` of `L_nu` contributes no collapsed finite term by the previous
section.  Since `L_nu` is lisse at `z=1`, the Kummer twist contributes the
scalar local monodromy `eta` there; `eta` is nonprincipal, so no
geometrically constant summand can survive.

Consequently, if the standard one-variable Deligne/Katz conductor bound for
this bounded-conductor middle-extension trace sheaf of weight one gives an
absolute constant `K` such that

```text
|sum_z W_{eta,nu}(z)L_nu(z)| <= K p,
```

or, in the normalized coordinate,

```text
|sum_{r in F_p^*, r != -1} eta(r) Phi_nu(r)| <= K p,
```

then the full collapsed transform satisfies

```text
|sum_z W_{eta,nu}(z)H_nu(z)| <= K p + 4sqrt(p).
```

Together with the already separated exceptional theta contribution, this
gives a p-scale bound for the paired generic M1 nonsplit term.  This is a
conditional import statement: it identifies the exact sheaf-conductor theorem
needed after the elementary reductions above.  It does not claim the sharp
constant needed for the original `4p` target.

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

## Open Nonprincipal Second Moment

The actual open line-conic core has the same nonprincipal RMS scale.  Put

```text
S^o = {(u,v): u != 0, v != 0, -1-u-v != 0, A(u,v) != 0},
        x(u,v)=A(u,v)/u.
```

Let `T^o=#S^o`, let `P^o` be the collision count for the joint map
`(u,v) |-> (x(u,v),v)`, and define the open marginal moments

```text
N_x^o = sum_x #{(u,v) in S^o: x(u,v)=x}^2,
N_v^o = sum_v #{u: (u,v) in S^o}^2.
```

Then

```text
T^o = p^2 - 4p + 6 + 4chi_2(-3),

P^o = 2p^2 - 11p + 22
      - p chi_2(-3) + 12chi_2(-3) + chi_2(-2),

N_x^o = p^3 - 5p^2 + 17p - 50
        + (10p - 36)chi_2(-3),

N_v^o = p^3 - 7p^2 + 22p - 28
        + (8p - 24)chi_2(-3) - chi_2(-2) - 2chi_2(-1).
```

Consequently, for the open sum
`C^o_{eta,nu}=C_{eta,nu}-L_{eta,nu}`,

```text
sum_{eta != 1, nu != 1} |C^o_{eta,nu}|^2
  = (p-1)^2 P^o - (p-1)(N_x^o+N_v^o) + (T^o)^2

  = p^4 - 9p^3 + 23p^2 + 14p - 4
    + (-p^3 + 4p^2 + 21p)chi_2(-3)
    + (p^2 - p)chi_2(-2)
    + (2p - 2)chi_2(-1).
```

Thus the certificate-facing open family also has RMS `p+O(1)` over
nonprincipal character pairs.  The open-line correction does not hide a
larger second-moment obstruction.

The proof is the same orthogonality argument as above, with one extra
deleted line.  For fixed `v`, the open condition removes `u=-1-v` unless
`B(v)=0` or `v=-1`; hence

```text
#{u:(u,v) in S^o}
  = p - 3 - chi_2(-3v^2-2v-3)
    + 2 1_{B(v)=0} + 1_{v=-1}.
```

Squaring and summing gives `N_v^o`.  On joint `(x,v)` fibers, the deleted
point `u=-1-v` belongs to a two-point collision orbit `u u'=B(v)`, so it
removes exactly three ordered collisions for each
`v` with `B(v) != 0` and `v != -1`.  Therefore

```text
P^o = S_p - 3(p-3-chi_2(-3)).
```

For fixed `x`, the open cut `w=0` intersects the conic

```text
u^2+v^2+uv+(x+1)u+v+1=0
```

in

```text
u^2+(x+1)u+1=0.
```

Thus for `x notin {1,-2}`,

```text
#{(u,v) in S^o: x(u,v)=x}
  = p - 3 - 2chi_2(-3) - 2chi_2((x-1)(x+3)),
```

with special values

```text
M_1^o    = (1+chi_2(-3))(p-2),
M_{-2}^o = 1 + (1+chi_2(-3))(p-4).
```

Their squared sum is `N_x^o`.

The lower-order line-correction ledger is exact as well.  Over
nonprincipal `eta,nu`,

```text
sum |L_{eta,nu}|^2
  = p^3 - 7p^2 + 14p - 3
    + (-p^2 + 3p + 2)chi_2(-3),
```

and the real covariance with the closed core is

```text
Re sum C_{eta,nu} conjugate(L_{eta,nu})
  = p^3 - 4p^2 - 3p + 1
    - 7p chi_2(-3) + (1-p)chi_2(-1).
```

Thus

```text
sum |C^o|^2 = sum |C|^2 + sum |L|^2
              - 2 Re sum C conjugate(L)
```

holds with every term in closed form.  The line correction has RMS
`sqrt(p)+O(1)` over nonprincipal pairs, and its covariance with the p-scale
core is only `O(p^3)`.  This makes precise why removing the open line
changes the exact moment but not the leading `p` RMS scale.

The same nonprincipal moment gives a certified average bound on the actual
admissible `C_2^lc` character slice.  For full character order `e=p-1`, the
number of admissible pairs is

```text
R(p-1)=(p-2)(p-6)+3 1_{2 | p-1}+2(gcd(p-1,3)-1).
```

Since the admissible slice is a subset of the nonprincipal pairs,

```text
1/R(p-1) sum_{(eta,nu) admissible} |C^o_{eta,nu}|^2
  <= 1/R(p-1) sum_{eta != 1, nu != 1} |C^o_{eta,nu}|^2.
```

Thus the actual line-conic-resonant slice also has a theorem-grade p-scale
RMS bound.  The verifier audits the admissible slice directly for
`p=17,31,43`; the observed RMS ratios are `0.8161`, `0.8502`, and
`0.9043`, all below the inherited bounds `1.0137`, `0.9625`, and `0.9747`.
The largest observed open ratios in those audits are `1.3054`, `1.8423`,
and `2.2232`, respectively.  This does not prove the pointwise `4p`
conductor target, but it confirms that the real admissible slice has no
dense average obstruction.

There is also an aggregate L1 consequence that may be more useful to the
certificate than a pointwise tail statement.  Let `A_p` be the full-order
admissible set and write `M_o(p)` for the exact nonprincipal open moment above.
Cauchy's inequality gives

```text
sum_{(eta,nu) in A_p} |C^o_{eta,nu}|
  <= sqrt(R(p-1) M_o(p)).
```

Equivalently, the admissible line-conic slice has average absolute value at
most

```text
p sqrt(M_o(p)/(R(p-1)p^2)) = p(1+O(1/p)).
```

Thus, if a later saturation certificate groups the full fixed-resonant-line
slice before applying absolute values term by term, the line-conic-resonant
aggregate can be charged at an average `p`-scale coefficient rather than at
the uniform `4p` or old `9p` pointwise constants.  This is not yet consumed by
the active certificate: it is an aggregate L1 bound for the normalized
full-order chart, not the missing uniform conductor theorem.  The verifier now
audits the actual average L1 ratios for `p=17,31,43`; they are `0.7523`,
`0.7628`, and `0.7973`, below the Cauchy bounds `1.0137`, `0.9625`, and
`0.9747`.

This aggregate bound has a precise transfer limitation.  If a certificate uses
only an order-`e` quotient-character subgroup, with `e | p-1`, then the
inherited full-order moment proves only

```text
sum_{(eta,nu) in A_e} |C^o_{eta,nu}|
  <= sqrt(R(e) M_o(p)),
```

because `A_e` is merely a subset of the full nonprincipal character family.
Therefore the inherited argument gives an average `Kp` bound on that
suborder chart exactly when

```text
R(e) >= M_o(p)/(K^2 p^2).
```

For small quotient-character order this condition can fail badly; an exact
order-`e` moment would then be needed before the grouped-L1 idea can be
consumed by a low-index saturation certificate.  The verifier records this
threshold over divisors of `p-1`.  For `p=17,31,43`, the minimal orders
certifying average `Kp` by this inherited route are:

```text
K=1:  none, 30, 42
K=2:  16,   30, 42
K=4:   8,   10, 14
K=9:   8,    6, 14
```

Thus the full-order aggregate theorem is a genuine p-scale statement, but it
does not automatically upgrade the existing low-index certificate ledgers.

The finite suborder audit suggests that the transfer obstruction is an
artifact of using the full nonprincipal moment, not visible growth in the
actual low-order slices.  For every divisor `e | p-1` with nonempty admissible
set in `p=17,31,43`, the verifier directly evaluates the embedded order-`e`
characters.  It reports:

```text
p   e   R(e)  RMS/p   avg |.|/p  max/p   inherited avg/p
17   8    24  0.7518  0.7047     1.1326  2.6819
17  16   168  0.8161  0.7523     1.3054  1.0137
31   6    12  1.1590  1.1491     1.2915  7.5172
31  10    48  0.8276  0.7239     1.5350  3.7586
31  15   144  0.8432  0.7710     1.4948  2.1700
31  30   732  0.8502  0.7628     1.8423  0.9625
43   6    12  0.8446  0.6982     1.2032 10.9839
43   7    12  0.4423  0.3916     0.6819 10.9839
43  14   120  0.7200  0.6381     1.5406  3.4734
43  21   324  0.8783  0.7619     2.2231  2.1138
43  42  1524  0.9043  0.7973     2.2231  0.9747
```

So the audited low-order slices still look `p`-scale even where the inherited
bound is off by factors of `4` to `11`.  This is only finite evidence, but it
pinpoints the next useful theorem: an exact order-`e` admissible open moment,
or a structural order-`e` large-sieve bound, would make the grouped-L1 route
usable in low-index M1 certificates.

There is a theorem-grade reduction of that order-`e` problem to a quotient
collision energy.  Let `K_e=(F_p^*)^e` and let `[z]_e` denote the class of
`z` in `F_p^*/K_e`.  For the open support `S^o`, set

```text
x(u,v)=A(u,v)/u,
n_{ij}=# {(u,v) in S^o : [x(u,v)]_e=i, [v]_e=j},
n_i^x=sum_j n_{ij},        n_j^v=sum_i n_{ij},        T^o=sum_{i,j}n_{ij}.
```

Then the all-nonprincipal order-`e` open moment is exactly

```text
M_e^o =
  e^2 sum_{i,j} n_{ij}^2
  - e sum_i (n_i^x)^2
  - e sum_j (n_j^v)^2
  + (T^o)^2.
```

Indeed, for the order-`e` character group,

```text
sum_{eta != 1} eta(z/z') = e 1_{[z]_e=[z']_e} - 1,
```

and the same formula holds for `nu`; expanding the product gives the displayed
identity.  Hence the low-order grouped-L1 problem is not a black-box
character-sum average: it is equivalent to bounding the two-dimensional
quotient occupancy energy of the rational map `(u,v) -> (A(u,v)/u, v)`.

Equivalently,

```text
M_e^o
  = e^2 sum_{i,j}
      (n_{ij} - n_i^x/e - n_j^v/e + T^o/e^2)^2.
```

The moment is therefore the row-and-column-centered mixing energy of the
quotient occupancy matrix.  Pure imbalance in the `x`-cosets or `v`-cosets is
projected out; only the genuinely two-dimensional deviation from the
independent row/column model remains.  This is the exact low-index analogue of
the "without square-root loss" target: prove mixing for this centered quotient
matrix uniformly, not a pointwise conductor estimate for every coefficient.

The verifier checks this identity by comparing the coset-energy formula with
direct order-`e` character summation.  It gives the following inherited bounds
for the admissible slice, using `M_e^o` instead of the full-order moment:

```text
p   e   R(e)  centered/p  all-np RMS/p  admissible/p  full-order/p
17   8    24  0.7625      0.8714        1.2451        2.6819
17  16   168  0.8212      0.8759        1.0137        1.0137
31   6    12  0.9763      1.1716        1.6910        7.5172
31  10    48  0.8405      0.9339        1.2132        3.7586
31  15   144  0.8622      0.9238        1.0778        2.1700
31  30   732  0.8680      0.8979        0.9625        0.9625
43   6    12  0.9791      1.1750        1.6959       10.9839
43   7    12  0.7561      0.8822        1.5279       10.9839
43  14   120  0.7653      0.8242        0.9781        3.4734
43  21   324  0.8932      0.9379        1.0421        2.1138
43  42  1524  0.9059      0.9280        0.9747        0.9747
```

This improves the inherited low-order constants by large factors without any
pointwise conductor input.  A proof that this quotient occupancy energy is
`O(p^2/e^2 + p)` uniformly in the relevant low-index regime would give the
desired average `p`-scale grouped line-conic ledger.

The joint quotient energy has a further algebraic normal form.  Write
`alpha,beta in K_e` for the quotient collision ratios

```text
x(u',v')=alpha x(u,v),        v'=beta v,
```

and put `u'=r u`.  Since

```text
x(u,v)=-(u+v+1+B(v)/u),        B(v)=v^2+v+1,
```

the collision condition is equivalent, after multiplying by `r u`, to the
conic-fibration equation

```text
r(r-alpha)u^2
  + r((beta-alpha)v+1-alpha)u
  + B(beta v) - alpha r B(v) = 0.
```

Thus

```text
sum_{i,j} n_{ij}^2
```

is exactly the number of tuples `(alpha,beta,r,u,v)` satisfying this equation,
with `alpha,beta in K_e`, `r,u,v in F_p^*`, and with both `(u,v)` and
`(ru,beta v)` lying in the open support.  Conversely, every pair counted by
the joint energy gives a unique such tuple by taking
`alpha=x(u',v')/x(u,v)`, `beta=v'/v`, and `r=u'/u`.  The verifier checks this
ratio-surface count against the quotient joint energy for
`(p,e)=(17,8),(17,16),(31,6),(31,10),(43,6),(43,14)`, giving joint energies
`993,419,21059,8005,81875,15835`.

This turns the centered-mixing target into a family of explicit conics over
the ratio parameters `(alpha,beta,r)`.  Degenerate ratio fibers are now the
objects to classify; away from them, a uniform conic-fiber estimate is the
natural route to the desired quotient-energy bound.

The degeneracy test is explicit.  In affine coordinates the conic has
coefficients

```text
a = r(r-alpha),        b = r(beta-alpha),
c = beta^2-alpha r,    d = r(1-alpha),
e = beta-alpha r,      f = 1-alpha r,
```

so its projective closure has doubled symmetric matrix

```text
[ 2a   b   d ]
[  b  2c   e ]
[  d   e  2f ].
```

For `p>3`,

```text
det =
  2r Delta(alpha,beta,r),
```

where

```text
Delta =
 -2 alpha^3 r^2
 +3 alpha^2 beta^2 r
 -alpha^2 beta r^2 - alpha^2 beta r
 +3 alpha^2 r^3 - alpha^2 r^2 + 3 alpha^2 r
 -3 alpha beta^2 r^2 + alpha beta^2 r - 3 alpha beta^2
 +alpha beta r^2 + alpha beta r - 3 alpha r^2
 +2 beta^2 r.
```

Because `r in F_p^*`, a ratio fiber is singular exactly when
`Delta(alpha,beta,r)=0`.  Thus the exceptional quotient-collision parameters
lie on a concrete determinant hypersurface, the pullback of the cubic
discriminant in conic-coefficient space.  The verifier checks this determinant
identity over the same `(p,e)` cases as the joint-energy audit and reports the
number of degenerate ratio parameters.

This exceptional set is sparse in the ratio direction.  For fixed
`alpha,beta in F_p^*`, write

```text
Delta(alpha,beta,r)
  = 3 alpha^2 r^3
    + alpha(-2alpha^2-alpha beta-alpha-3beta^2+beta-3)r^2
    + (3alpha^2 beta^2-alpha^2 beta+3alpha^2
       +alpha beta^2+alpha beta+2beta^2)r
    - 3alpha beta^2.
```

Since `p>3` and `alpha != 0`, the leading coefficient `3alpha^2` is
nonzero.  Thus each fixed pair `(alpha,beta)` has at most three singular
ratios `r`.  Consequently,

```text
#{(alpha,beta,r) in K_e^2 x F_p^* : Delta(alpha,beta,r)=0}
  <= 3 |K_e|^2.
```

The only identically zero conic is the diagonal parameter
`(alpha,beta,r)=(1,1,1)`.  Indeed, if all six conic coefficients vanish, then
`r(r-alpha)=0` gives `r=alpha`, `r(beta-alpha)=0` gives `beta=alpha`, and
`r(1-alpha)=0` gives `alpha=1`; conversely `(1,1,1)` makes the equation
identically zero.  Hence the diagonal fiber contributes exactly the open
support size, while every other singular ratio fiber is a nonzero singular
projective conic and has at most `2p+1` projective `F_p`-points.  In
particular, the only `p^2` fiber in the quotient-collision fibration is the
identity diagonal; all non-diagonal singular fibers are line-sized.

This gives an immediate aggregate joint-energy bound.  Let

```text
J_e = sum_{i,j} n_{ij}^2,        k_e=|K_e|=(p-1)/e,
N_e = k_e^2(p-1),
T^o = #S^o = p^2-4p+6+4 chi_2(-3).
```

If `D_e` is the number of singular ratio parameters, including the identity
diagonal, then

```text
J_e <= T^o + (N_e-D_e)(p+1) + (D_e-1)(2p+1).
```

Indeed, the identity diagonal contributes exactly `T^o`; each smooth
projective conic contributes at most `p+1` affine open points; and each
nonzero singular projective conic contributes at most `2p+1` projective
points.  Combining this with `D_e <= 3k_e^2` gives the uniform form

```text
J_e <= T^o + (N_e-1)(p+1) + (3k_e^2-1)p.
```

So the conic fibration already recovers the correct leading scale
`J_e <= p^4/e^2 + O(p^3/e^2+p^2)`, with an explicitly separated diagonal
term.  The remaining centered-mixing problem is therefore not the existence
of a hidden two-dimensional exceptional fiber; it is to exploit the
row/column subtraction in `M_e^o` beyond this raw joint-energy estimate.

The row/column centering gives one automatic cancellation.  Put

```text
X_e=sum_i (n_i^x)^2,        V_e=sum_j (n_j^v)^2.
```

Cauchy's inequality gives `X_e >= (T^o)^2/e` and
`V_e >= (T^o)^2/e`.  Therefore

```text
M_e^o
  = e^2 J_e - eX_e - eV_e + (T^o)^2
  <= e^2 J_e - (T^o)^2.
```

Using the uniform conic bound above yields

```text
M_e^o
  <= e^2 (T^o+(N_e-1)(p+1)+(3k_e^2-1)p) - (T^o)^2.
```

This is the first centered theorem in the quotient-conic route: the leading
`p^4` term cancels formally.  For fixed low `e` it still leaves a
`p^3`-scale moment bound, hence a `p^{3/2}` pointwise RMS scale after
averaging over the `(e-1)^2` nonprincipal characters.  It is not enough for
the desired grouped line-conic certificate, but it proves that the remaining
loss is no longer a hidden large ratio fiber; it is the need for genuine
row/column-centered cancellation beyond Cauchy.  The verifier checks this
bound for every audited divisor `e | p-1` with nonempty admissible slice in
`p=17,31,43`.

There is also an exact centered ratio-fibration formula.  Define the
order-`e` centering weight

```text
W_e(z)=e 1_{z in K_e}-1,        z in F_p^*.
```

Then `sum_{z in F_p^*} W_e(z)=0`, and

```text
M_e^o
  = sum_{(u,v),(u',v') in S^o}
      W_e(x(u',v')/x(u,v)) W_e(v'/v).
```

After the same change of variables

```text
alpha=x(u',v')/x(u,v),        beta=v'/v,        u'=ru,
```

this becomes

```text
M_e^o
  = sum_{alpha,beta,r} W_e(alpha)W_e(beta)
      F(alpha,beta,r),
```

where `F(alpha,beta,r)` is the number of open affine points `(u,v)` on the
same conic fiber

```text
r(r-alpha)u^2
  + r((beta-alpha)v+1-alpha)u
  + B(beta v) - alpha rB(v) = 0
```

with `(u,v)` and `(ru,beta v)` both in `S^o`.  This is just multiplicative
orthogonality with the principal row and column removed, but it is the useful
form of the remaining problem: any parameter-independent smooth-conic main
term cancels because the two weight sums are zero.  The diagonal zero conic
still contributes `(e-1)^2T^o`, which is only `p^2` scale for fixed `e`.
Thus the low-index M1 task is a weighted trace and boundary-correction
problem over this conic fibration, not an uncentered occupancy count.  The
verifier checks the weighted ratio-fibration identity on the same
`(p,e)` cases used for the unweighted ratio-surface audit.

The preceding sentence can be made an exact decomposition.  Let
`\overline C_{alpha,beta,r}` be the projective closure of the conic fiber,
with the zero conic interpreted as the whole projective plane, and put

```text
Q(alpha,beta,r)=#\overline C_{alpha,beta,r}(F_p),
B(alpha,beta,r)=Q(alpha,beta,r)-F(alpha,beta,r).
```

Since

```text
sum_{alpha,beta,r} W_e(alpha)W_e(beta)(p+1)=0,
```

one has the exact identity

```text
M_e^o =
  sum_{alpha,beta,r} W_e(alpha)W_e(beta)(Q(alpha,beta,r)-(p+1))
  - sum_{alpha,beta,r} W_e(alpha)W_e(beta)B(alpha,beta,r).
```

For every nonzero nonsingular conic, `Q(alpha,beta,r)=p+1`; hence the first
sum is supported entirely on the determinant hypersurface `Delta=0`, together
with the zero conic at `(1,1,1)`.  The smooth projective main term is therefore
gone before any estimate is applied.  What remains is explicit:

- the diagonal zero conic, whose projective excess is `p^2`;
- nonzero singular conics on `Delta=0`, each with projective excess in
  `{-p,0,p}`;
- the boundary term `B`, accounting for infinity, deleted source lines, and
  deleted target lines.

Thus a low-index `p^2` moment theorem would follow from cancellation in this
weighted boundary term plus the already sparse singular support.  The verifier
audits the decomposition by summing the projective excess over all ratio
parameters for the existing `(p,e)` ratio-surface cases and checking that the
singular support has at most `3(p-1)^2` parameters and one zero conic.

For audit purposes the same verifier partitions `B` by the first failed
boundary condition in the ordered list

```text
infinity, u=0, v=0, source line, target line, source A=0, target A=0.
```

This is a disjoint bookkeeping partition, not a mathematical asymmetry: it
prevents overlaps between boundary components from being counted twice and
lets future work attack the infinity, line-deletion, and conic-deletion
pieces separately.

Four of these seven signed pieces vanish identically.  On `u=0`, if
`B(v) != 0`, the conic equation determines
`alpha=B(beta v)/(rB(v))`, so summing over `r in F_p^*` makes `alpha` run
through `F_p^*` and the total `W_e(alpha)` weight is zero.  If `B(v)=0`,
then `alpha` is free whenever the boundary equation is solvable, giving the
same zero by `sum_alpha W_e(alpha)=0`.  On `v=0`, the conic equation is
independent of `beta`, so `sum_beta W_e(beta)=0`.  On source `A=0`, the
identity

```text
A(ru,beta v) = alpha r A(u,v)
```

on the conic fiber shows that the equation is independent of `alpha` after
forcing target `A=0`; hence the source-`A=0` signed piece vanishes by the
free `alpha` weight.  Finally, target `A=0` together with the same identity
forces source `A=0`, so it has already been assigned to the previous boundary
piece in the ordered partition.  Therefore the only boundary components left
to bound are infinity, the source line, and the target line.  The verifier
asserts these four vanishings in the audited ratio-surface cases.

The surviving three pieces have one-dimensional formulas.  For infinity,
write the finite point at infinity as `[1:s:0]`; its equation is

```text
r^2 + r beta s + beta^2 s^2
  = alpha r B(s).
```

The point `[0:1:0]` contributes with `alpha=beta^2/r`.  Thus the infinity
piece is a weighted sum over `(beta,r,s)`, with `alpha` determined by the
displayed equation whenever `B(s) != 0`; the `B(s)=0` free-alpha cases vanish
by `sum_alpha W_e(alpha)=0`.

For the source line put `v=-1-u`, with `u,v != 0`.  Since
`B(v)=B(u)`, the conic equation becomes

```text
r^2u^2 + r(beta v+1)u + B(beta v) = alpha r B(u).
```

Again `alpha` is determined unless `B(u)=0`, and the free-alpha cases vanish.
For the target line put `v=(-1-ru)/beta` and discard points already assigned
to earlier boundary pieces.  The remaining conic equation is linear in
`alpha`, so it gives the third explicit one-dimensional weighted sum.  The
verifier evaluates these three solved-alpha formulas and checks that they
match the infinity, source-line, and target-line entries of the boundary
partition.

The infinity piece has a further quotient-autocorrelation reduction.  Put
`beta=rt`.  For a finite point at infinity `[1:s:0]` with `B(s) != 0`,

```text
alpha
  = r (1+ts+t^2s^2)/B(s),
```

and therefore

```text
alpha/beta = (1+ts+t^2s^2)/(tB(s)).
```

The inner sum over `r` is

```text
sum_r W_e(r alpha/beta) W_e(r)
  = (p-1) W_e(alpha/beta),
```

the autocorrelation identity for the quotient-centering weight.  If
`1+ts+t^2s^2=0`, then the corresponding `alpha` is zero and no
multiplicative parameter contributes.  The remaining point `[0:1:0]` gives
`alpha/beta=t`, whose total contribution is
`(p-1)sum_t W_e(t)=0`.  Thus the infinity boundary is exactly

```text
(p-1) sum_{t in F_p^*}
  sum_{s in F_p, B(s) != 0, 1+ts+t^2s^2 != 0}
    W_e((1+ts+t^2s^2)/(tB(s))).
```

The verifier checks this reduced two-variable formula against the original
infinity boundary partition and audits the autocorrelation identity directly.

This two-variable formula has a second reduction to a positive spectral
square.  The `s=0` row contributes `sum_t W_e(1/t)=0`; for `s != 0` put
`x=ts`.  Since

```text
(1+ts+t^2s^2)/(tB(s))
  = s B(x)/(x B(s))
  = F(x)/F(s),              F(z)=B(z)/z=z+1+z^{-1},
```

the infinity boundary equals

```text
(p-1) sum_{a,b in F_p^*} N(a)N(b) W_e(a/b),
```

where

```text
N(a)=#{z in F_p^* : F(z)=a}.
```

The fiber equation is `z^2+(1-a)z+1=0`, hence

```text
N(a)=1+chi((a-3)(a+1)).
```

The constant and linear terms vanish against the mean-zero weight `W_e`, so

```text
I_e/(p-1)
  = sum_{a,b in F_p^*}
      chi((a-3)(a+1)) chi((b-3)(b+1)) W_e(a/b).
```

Expanding `W_e` as the sum of the nontrivial characters of
`F_p^*/K_e` gives the exact spectral-square identity

```text
I_e/(p-1)
  = sum_{psi != 1, psi^e=1}
      | sum_{a in F_p^*} chi((a-3)(a+1)) psi(a) |^2.
```

Thus the infinity boundary is nonnegative and is controlled by a fixed
rank-one Kummer conductor: for `p > 3` each inner sum has branch points only
at `a=-1,0,3,infinity`, so the standard Weil bound gives
`|sum_a chi((a-3)(a+1)) psi(a)| <= 2sqrt(p)`.  Consequently

```text
0 <= I_e <= 4(e-1)p(p-1).
```

This is the first surviving boundary piece with an explicit
depth-independent conductor bound.  The verifier checks the `F`-fiber count,
the centered energy identity, the spectral-square formula, and the audited
`2sqrt(p)` ceiling on the existing ratio-surface grid.

The source and target line deletions also have a structural split.  The
ordered boundary partition assigns the intersection of the two deleted lines
to the source-line piece.  If this overlap is removed, the source-exclusive
and target-exclusive pieces are identical: swap the source point
`(u,v)` with the target point `(ru,beta v)`.  The parameters become
`r^{-1}`, `beta^{-1}`, and `alpha^{-1}`, and the weight is unchanged because
`W_e(z^{-1})=W_e(z)`.  Thus

```text
source line = target line + overlap.
```

The overlap itself is explicit.  Put both source and target points on the
deleted line, so `v=-1-u` and `beta v=-1-ru`.  With `x=ru`,
`H(z)=1+z`, and the same `F(z)=B(z)/z` as above, the conic equation gives

```text
alpha = F(x)/F(u),        beta = H(x)/H(u).
```

The overlap is therefore

```text
O_e =
  sum_{x,u in D} W_e(F(x)/F(u)) W_e(H(x)/H(u)),

D = { z in F_p^* : z != -1, B(z) != 0 }.
```

Expanding both quotient weights gives a second positive spectral square:

```text
O_e =
  sum_{psi,phi != 1, psi^e=phi^e=1}
    | sum_{z in D} psi(F(z)) phi(H(z)) |^2.
```

For `p > 3`, the branch points of `psi(F(z))phi(H(z))` lie among
`0`, `-1`, the two roots of `B`, and `infinity`.  Since both characters are
nontrivial, the divisor is not an `e`-th power, so the standard rank-one
Kummer bound gives

```text
|sum_{z in D} psi(F(z)) phi(H(z))| <= 3sqrt(p),
0 <= O_e <= 9(e-1)^2 p.
```

Thus the only line-deletion term not yet converted into a positive spectral
square is one source/target-exclusive line piece.  The verifier checks the
source-target involution numerically (`source-exclusive = target-line`), the
overlap formula, the overlap spectral-square identity, and the audited
`3sqrt(p)` ceiling.

The remaining target-line piece is nevertheless not a new independent
conductor problem.  Parameterize the target line by
`(x,y)=(x,-1-x)`.  For a source point `(u,v)` in the open support,

```text
beta = y/v,       alpha = (-B(x)/x)/(A(u,v)/u).
```

Here `A(u,v)=-(u^2+v^2+uv+u+v+1)`.  Expanding the two quotient weights gives
the exact spectral pairing

```text
T_e =
  sum_{psi,phi != 1}
    L_{psi,phi} C^o_{psi^{-1},phi^{-1}},

L_{psi,phi}
  = sum_{x in D} psi(-B(x)/x) phi(-1-x),

C^o_{psi^{-1},phi^{-1}}
  = sum_{(u,v) in U^o}
      psi^{-1}(A(u,v)/u) phi^{-1}(v),
```

where `D={x in F_p^* : x != -1, B(x) != 0}` and
`U^o={u,v != 0, u+v+1 != 0, A(u,v) != 0}`.  The first Parseval norm is
exactly the line-pair overlap `O_e`; the second Parseval norm is exactly the
open centered moment `M_e^o`.  Hence

```text
|T_e|^2 <= O_e M_e^o,
|T_e| <= 3(e-1) sqrt(p M_e^o)        (using O_e <= 9(e-1)^2p).
```

This converts the last boundary term into a controlled cross term between a
rank-one line spectrum and the main open M1 spectrum.  It is the boundary
analogue of completing a square: once `O_e` is conductor-bounded, the
exclusive line contribution can be absorbed by a quadratic inequality in
`sqrt(M_e^o)` rather than estimated by a separate pointwise Kummer theorem.
The verifier checks the spectral pairing itself, both Parseval identities,
and the resulting Cauchy bound against the exact target-line formula.

Putting the pieces together gives a closed boundary inequality.  Let `P_e`
denote the weighted projective singular excess, so

```text
M_e^o = P_e - I_e - O_e - 2T_e.
```

Here `I_e` and `O_e` are nonnegative spectral squares, and
`|T_e|^2 <= O_e M_e^o`.  With `P_e^+=max(P_e,0)` and
`Y=sqrt(M_e^o)`, this gives

```text
Y^2 <= P_e^+ - O_e + 2sqrt(O_e)Y,
```

hence

```text
(Y-sqrt(O_e))^2 <= P_e^+,
sqrt(M_e^o) <= sqrt(P_e^+) + sqrt(O_e).
```

Using the overlap conductor bound,

```text
M_e^o <= (sqrt(P_e^+) + 3(e-1)sqrt(p))^2.
```

Thus all open-boundary terms have been eliminated from the independent
target list: the remaining quotient-conic moment problem is to bound the
projective singular excess `P_e` sharply.  If `P_e=O(p^2)` for fixed `e`,
then the whole centered quotient-conic moment is `O(p^2)` as well.  The
verifier checks the exact recomposition
`M_e^o=P_e-I_e-O_e-2T_e` and both the exact-overlap and conductor-overlap
versions of the closed inequality.

The singular-excess target can be sharpened one more step.  For a singular
projective conic define

```text
epsilon(alpha,beta,r)
  = (Q(alpha,beta,r)-(p+1))/p.
```

The diagonal zero conic has `epsilon=p`; every other singular conic has
`epsilon in {-1,0,1}`.  Group singular parameters by quotient labels
`i,j in F_p^*/K_e`:

```text
Gamma_e(i,j)
  = sum_{alpha in i, beta in j, Delta(alpha,beta,r)=0}
      epsilon(alpha,beta,r).
```

If `w_0=e-1` and `w_i=-1` for the other quotient labels, then

```text
P_e = p w^T Gamma_e w.
```

Since `sum_i w_i=0`, row-only, column-only, and constant parts of
`Gamma_e` vanish in this bilinear form.  With `Gamma_e^circ` the
row/column-centered matrix,

```text
|P_e| <= p ||w||_2^2 ||Gamma_e^circ||_F
       = p e(e-1) ||Gamma_e^circ||_F.
```

Thus the exact remaining fixed-index target is

```text
||Gamma_e^circ||_F <= C_e p.
```

This is a much smaller object than the original boundary ledger: an `e x e`
matrix of signed singular-fiber excesses.  The verifier audits the
divisibility of `Q-(p+1)` by `p`, the allowed values of `epsilon`, the exact
bilinear identity for `P_e`, and the Frobenius Cauchy reduction.  On the
current grid the normalized centered Frobenius ratios are small constants,
which is consistent with the linear-in-`p` target but is not a proof of it.

Equivalently, this is a two-dimensional quotient-character trace problem.
For nontrivial characters `psi,phi` of `F_p^*/K_e`, set

```text
S_{psi,phi}
  = sum_{Delta(alpha,beta,r)=0}
      epsilon(alpha,beta,r) psi(alpha) phi(beta).
```

The row and column projections of `Gamma_e` disappear exactly when
`psi` and `phi` are both nontrivial.  Parseval gives

```text
||Gamma_e^circ||_F^2
  = e^{-2} sum_{psi,phi != 1} |S_{psi,phi}|^2,
```

and the special weight `w=e 1_{K_e}-1` has all nontrivial Fourier
coefficients equal to `e`, so

```text
P_e/p = sum_{psi,phi != 1} S_{psi,phi}.
```

Thus the fixed-index `P_e=O(p^2)` theorem would follow from the standard
looking trace estimate `|S_{psi,phi}| <= C_e p` for the signed determinant
surface, or even from the averaged square bound
`sum |S_{psi,phi}|^2 <= C_e p^2`.  The verifier checks these Fourier
normalizations against the same quotient matrix and reports the largest
normalized spectral coefficient on the audited grid.

The signed excess `epsilon` is itself a quadratic character on rank-two
charts.  For a homogeneous conic

```text
a U^2 + b UV + c V^2 + d UW + e VW + f W^2 = 0
```

write the three binary discriminants

```text
d_UV = b^2 - 4ac,
d_UW = d^2 - 4af,
d_VW = e^2 - 4cf.
```

On a rank-two singular conic, any nonzero one of these has the same square
class, and the projective point count is `2p+1` or `1` according as that
class is square or nonsquare.  Hence

```text
epsilon = chi(d)
```

for any nonzero `d` among the three discriminants.  If all three vanish, the
conic has rank at most one and `epsilon=0`, except for the zero conic already
separated with `epsilon=p`.  Thus the trace above is a genuine Kummer trace
on finitely many determinant-surface charts, not a black-box point-count
weight.  The verifier audits this discriminant formula against exact
projective counts on every singular ratio fiber in the grid.

For the ratio-surface conic, with parameters `a=alpha`, `b=beta`, and
`r`, these three discriminants are the explicit polynomials

```text
d_UV = r(-3a^2r + 4ab^2 - 2abr + 4ar^2 - 3b^2r),
d_UW = r(-3a^2r + 4ar^2 - 2ar + 4a - 3r),
d_VW = -3a^2r^2 + 4ab^2r - 2abr + 4ar - 3b^2.
```

Thus one may cover the determinant surface by the ordered rank-two charts

```text
U V:  d_UV != 0,                         epsilon = chi(d_UV),
U W:  d_UV = 0, d_UW != 0,               epsilon = chi(d_UW),
V W:  d_UV = d_UW = 0, d_VW != 0,        epsilon = chi(d_VW).
```

The residual locus where all three discriminants vanish has rank at most one
and contributes zero, except for the separated zero conic.  Consequently
each `S_{psi,phi}` is now a finite sum of explicit Kummer traces on these
three determinant-surface charts.  The verifier checks the displayed
formulas against the coefficient discriminants and records how singular
fibers distribute among the ordered charts.

The lower charts are not another two-dimensional surface.  Let

```text
K_alpha(a,r) = -a^2r + 3ar^2 - 4ar + 3a - r,
K_beta(b,r)  = (3r-2)b^2 + (3r^2-8r+3)b + r(3-2r).
```

Eliminating `b` from `Delta=0` and `d_UV=0` gives

```text
Res_b(Delta,d_UV) = a^2 r^4 (a-r)^2 K_alpha(a,r)^2.
```

On the diagonal branch `a=r`,

```text
Delta = r(r-1)(b-r)(b-r^2),        d_UV = r^2(b-r)^2,
```

so the lower chart contains only `a=b=r` from this branch.  On the residual
branch `K_alpha=0`, eliminating `a` from `(K_alpha,Delta)` and from
`(K_alpha,d_UV)` has common factor `K_beta`; hence every residual
`Delta=d_UV=0` point has `K_beta(b,r)=0`.  Therefore, for each fixed
`r in F_p^*`, the non-`U V` part is contained in one diagonal point plus at
most four residual points.  In particular

```text
#{Delta=0, d_UV=0} <= 5(p-1).
```

Thus the non-`U V` contribution to every `S_{psi,phi}` is already `O(p)` by
counting alone.  Moreover, away from the zero conic and for `p>5`, the
ordered lower chart is actually `U W`: on the diagonal
`d_UW=r^2(r-1)^2`, while modulo `K_alpha` one has
`d_UW=-5ar(r-1)^2`.  The verifier audits the finite collapse, including the
small characteristic `p=5` sample.  The only remaining surface-cancellation
problem is therefore the main `d_UV != 0` determinant chart.

That main chart has a useful two-sheet presentation.  View `Delta` as a
homogeneous quadratic in `beta=[B:Z]`:

```text
A_beta B^2 + B_beta BZ + C_beta Z^2 = 0,

A_beta = 3a^2r - 3ar^2 + ar - 3a + 2r,
B_beta = -ar(a-1)(r+1),
C_beta = ar(-2a^2r + 3ar^2 - ar + 3a - 3r).
```

Its discriminant factors as

```text
D_beta = B_beta^2 - 4A_beta C_beta
       = ar M(a,r) H(a,r),

M(a,r) = -3a^2r + 4ar^2 - 2ar + 4a - 3r,
H(a,r) = -8a^2r + 9ar^2 - 2ar + 9a - 8r.
```

The only all-zero projective `beta` fiber is `(a,r)=(1,1)`, a vertical line
which is `O(p)`.  Away from it, the projective fiber has
`1+chi(D_beta)` `F_p`-points.  Hence the branch divisor of the
projective `beta` cover is explicitly contained in the two curves
`M(a,r)=0` and `H(a,r)=0`.  Passing back to the affine nonzero-`beta`
trace only deletes the coordinate curves `A_beta=0` (the beta-infinity
sheet) and `C_beta=0` (the beta-zero sheet), again `O(p)` sets.

Finally, on the open split two-root fibers which avoid the lower chart, the
singular-excess sign is invariant under beta-conjugation.  Indeed

```text
Res_beta(Delta,d_UV)
  = a^2 r^4 (a-r)^2 K_alpha(a,r)^2,
```

so, when both roots are finite nonzero main-chart roots,
`d_UV(beta_1)d_UV(beta_2)` is a square.  Therefore
`chi(d_UV(beta_1))=chi(d_UV(beta_2))`.  Fibers meeting the lower chart lie
over the already curve-sized projection `a=r` or `K_alpha(a,r)=0`, so their
main-sheet companions are also only an `O(p)` contribution.  The remaining
trace problem is thus the open two-sheet beta cover over `(a,r)`, branched
only over `M(a,r)H(a,r)=0`, with the quadratic sign descending through the
cover involution.  The verifier audits the discriminant factorization,
projective beta-root count, exceptional coordinate curves, and conjugate
sign equality on split fibers.

The branch divisor is itself elementary.  Both `M=0` and `H=0` are singular
at `(a,r)=(1,1)` and are rationally parametrized by the slope
`t=(r-1)/(a-1)` through that point:

```text
M=0:
  a = -3(t-1)/(t(4t-3)),
  r = -4t(t-1)/(4t-3),

H=0:
  a = -8(t-1)/(t(9t-8)),
  r = -9t(t-1)/(9t-8).
```

The resultants are

```text
Res_a(M,H) = 25 r^2 (r-1)^4,
Res_r(M,H) = 25 a^2 (a-1)^4.
```

Thus, for `p>5`, the two branch curves meet in the torus only at the
already separated vertical point `(1,1)`.  In characteristic `5` there are
extra branch intersections, and the verifier records that finite special
case separately.  Consequently the final two-sheet cover has an explicitly
rational branch divisor with no hidden high-genus branch component.
The branch curves also have no hidden singular component on the good locus.
For `M`, the relevant derivatives are

```text
M_a = -6ar + 4r^2 - 2r + 4,
M_r = -3a^2 + 8ar - 2a - 3,
```

and

```text
Res_a(M,M_a) = 48r(r-1)^2(r^2+r+1),
Res_a(M,M_r) = 144(r-1)^2(r+1)^2.
```

For `H`,

```text
H_a = -16ar + 9r^2 - 2r + 9,
H_r = -8a^2 + 18ar - 2a - 8,
```

and

```text
Res_a(H,H_a) = 72r(r-1)^2(9r^2+14r+9),
Res_a(H,H_r) = 5184(r-1)^2(r+1)^2.
```

Thus in the torus, for `p>3`, each branch curve is singular only at
`(a,r)=(1,1)`, the same separated point already removed from the good base.
The verifier checks this directly over the audited prime grid.

The same single point is the whole boundary pile-up for the beta conductor
ledger.  The first affine chart of its blow-up is the finite-slope chart

```text
r = 1 + t(a-1).
```

After removing the exceptional powers of `a-1`, the relevant strict
transforms are

```text
A_beta = (a-1) A#,
Q_beta = (a-1) Q#,
K_alpha = (a-1)^2 K#,
a-r = (a-1) L#,
M = (a-1)^2 M#,
H = (a-1)^2 H#,
```

where `C_beta=ar Q_beta` and

```text
A# = -3a^2t^2 + 3a^2t + 3at^2 - 5at + 3a + 2t - 2,
Q# =  3a^2t^2 - 2a^2t - 3at^2 + 5at - 2a - 3t + 3,
K# =  3at^2 - at + t - 1,
L# =  1 - t,
M# =  4at^2 - 3at + 3t - 3,
H# =  9at^2 - 8at + 8t - 8.
```

The pairwise strict-transform intersections have no hidden common
component.  Eliminating `a`, the nontrivial resultant supports are

```text
Res(A#,Q#) = -3t^2(t-1)(6t^2-10t+5),
Res(A#,K#) =  3t^2(t-1)(t+1)(3t-2),
Res(A#,M#) = -t^2(t-1)(2t-3)^2,
Res(A#,H#) = -6t^2(t-1)(3t-2)^2,

Res(Q#,K#) = -3t^2(t-1)(2t-1)(3t+1),
Res(Q#,M#) = -3t^2(t-1)(2t-1)^2,
Res(Q#,H#) = -3t^2(t-1)(3t-4)^2,

Res(K#,M#) =  5t^2(t-1),
Res(K#,H#) = 15t^2(t-1),
Res(M#,H#) =  5t^2(t-1),
```

with the diagonal transform `L#=1-t` meeting every other strict transform
only on the slope `t=1`.  Thus one fixed blow-up separates the high
multiplicity point into bounded-degree strict transforms whose remaining
intersections are supported on an explicit finite slope set.  The verifier
checks these strict-transform identities, including `C_beta=ar Q_beta`, and
every displayed pairwise support over the audited primes; the largest
pairwise intersection count in the affine blow-up chart is `3`, and the
largest open-torus count is `2`.

The reciprocal chart covers the vertical tangent direction:

```text
a = 1 + s(r-1).
```

After removing powers of `r-1`, write

```text
A_beta = (r-1) Ahat,
Q_beta = (r-1) Qhat,
K_alpha = (r-1)^2 Khat,
a-r = (r-1) Lhat,
M = (r-1)^2 Mhat,
H = (r-1)^2 Hhat,
```

where

```text
Ahat =  3r^2s^2 - 3r^2s - 3rs^2 + 7rs - 3r - 3s + 3,
Qhat = -2r^2s^2 + 3r^2s + 2rs^2 - 5rs + 3r + 3s - 3,
Khat = -rs^2 + 3rs - 3s + 3,
Lhat =  s - 1,
Mhat = -3rs^2 + 4rs - 4s + 4,
Hhat = -8rs^2 + 9rs - 9s + 9.
```

Eliminating `r`, the nontrivial pairwise supports in this chart are

```text
Res(Ahat,Qhat) =  3s^3(s-1)(5s^2-10s+6),
Res(Ahat,Khat) =  3s^2(s-1)(s+1)(2s-3),
Res(Ahat,Mhat) =  s^2(s-1)(3s-2)^2,
Res(Ahat,Hhat) =  6s^2(s-1)(2s-3)^2,

Res(Qhat,Khat) = -3s^2(s-2)(s-1)(s+3),
Res(Qhat,Mhat) =  3s^2(s-2)^2(s-1),
Res(Qhat,Hhat) =  3s^2(s-1)(4s-3)^2,

Res(Khat,Mhat) = -5s^2(s-1),
Res(Khat,Hhat) = -15s^2(s-1),
Res(Mhat,Hhat) = -5s^2(s-1),
```

and `Lhat=s-1` again meets every other strict transform only at slope
`s=1`.  The verifier checks the reciprocal strict-transform identities and
all displayed supports; the largest pairwise intersection count in this
chart is `4`, and the largest open-torus count is `3`.  Thus the full
two-chart blow-up has bounded-degree strict transforms and no unresolved
high-multiplicity boundary component.

The strict transforms themselves are smooth in the good characteristics.
The verifier checks the partial derivatives of `A#`, `Q#`, `K#`, `L#`, `M#`,
`H#` and of `Ahat`, `Qhat`, `Khat`, `Lhat`, `Mhat`, `Hhat` on the full
affine charts.  For every audited `p>5` there is no point where a strict
transform and both of its partials vanish.  The only audited exception is
the already special characteristic `5`, where the finite-slope chart has one
isolated singular point on each of `A#` and `Q#`, and the reciprocal chart
has the analogous isolated `Ahat` and `Qhat` singular points.  Thus for
`p>5` the beta-boundary blow-up has smooth strict-transform components; no
singular boundary component remains hidden in the conductor ledger.

The remaining non-normal-crossing incidences are also bounded and explicit.
For every audited `p>5`, each blow-up chart has exactly one triple-or-higher
point, namely the toric corner `(a,t)=(0,1)` in the finite-slope chart and
`(r,s)=(0,1)` in the reciprocal chart; these both lie over `(a,r)=(0,0)`
and are outside the torus.  There are no open-torus triple points.  The only
open-torus tangencies are four pairwise boundary tangencies, recorded in the
finite-slope chart as

```text
A# tangent M#:  3a+1 = 0, 2t-3 = 0,
A# tangent H#:  a+2 = 0, 3t-2 = 0,
Q# tangent M#:  a+3 = 0, 2t-1 = 0,
Q# tangent H#:  2a+1 = 0, 3t-4 = 0,
```

and equivalently in the reciprocal chart as

```text
Ahat tangent Mhat:  r+1 = 0, 3s-2 = 0,
Ahat tangent Hhat:  r+1 = 0, 2s-3 = 0,
Qhat tangent Mhat:  r+1 = 0, s-2 = 0,
Qhat tangent Hhat:  r+1 = 0, 4s-3 = 0.
```

The additional tangency `Q#` with `L#` (and `Qhat` with `Lhat`) occurs only
at the toric corner.  Thus the blow-up boundary is normal crossing away from
a fixed finite incidence set of bounded size; the verifier checks the
gradient determinants, absence of open triple points, and the displayed
tangency supports on the audited prime grid.

On the good base, the cover is finite etale of degree two: at any beta root,
`2A_beta beta+B_beta` is nonzero and its square is `D_beta`.  Since the good
base is an open subset of `G_m^2`, the good beta-cover surface is smooth;
all ramification is confined to the deleted branch divisor `D_beta=0`.

This gives an exact pushforward form for the main-chart trace.  Put

```text
G = {(a,r): A_beta C_beta D_beta (a-r) K_alpha(a,r) != 0}.
```

Equivalently, over `G`, the good beta cover is the standard square-root cover.
Put

```text
y = 2A_beta beta + B_beta.
```

Then on the open good base, where `A_beta != 0`,

```text
y^2 = D_beta,              beta = (y-B_beta)/(2A_beta).
```

Thus the remaining good pushforward can be written without a general
quadratic equation as

```text
G_{psi,phi}
 = sum_{(a,r) in G}
     psi(a) chi(rM) phi((2A_beta)^(-1))
       sum_{y^2=D_beta(a,r)} phi(y-B_beta).
```

The deleted beta-zero boundary is exactly the excluded locus where
`y-B_beta=0` on the square-root cover, and beta infinity is the excluded
`A_beta=0` boundary.  The verifier checks the two-way bijection between
affine beta roots and `y^2=D_beta` roots, the nonvanishing of
`y-B_beta` on the good cover, and the normalized character-trace identity
for the audited pushforward character pairs.

The same normalization gives a vertical Lefschetz-pencil ledger for the
remaining conductor import.  Fix `r != 0`.  Since

```text
D_beta = a r M(a,r)H(a,r),
```

the finite branch polynomial in the `a`-line is

```text
P_r(a) = a M(a,r)H(a,r),
```

with a stable branch point at infinity because the leading coefficient is
`24r^2`.  For `p>5`,

```text
disc_a(P_r)
 = 51840000 r^8(r-1)^12(r^2+r+1)(9r^2+14r+9).
```

Thus, away from the fixed bad set

```text
r=1,        r^2+r+1=0,        9r^2+14r+9=0
```

(and the toric value `r=0`), the vertical fiber of the square-root cover is
a smooth genus-two hyperelliptic curve with bounded marked divisor.  The
intersections of this branch divisor with the deleted beta-infinity,
beta-zero, lower-chart, diagonal, and beta-linear boundaries are also
confined to fixed vertical parameters:

```text
Res_a(P_r,A_beta)          =  108 r^5(r-1)^4(r+1)^4,
Res_a(P_r,Q_beta)          = -162 r^5(r-1)^4(r+1)^4,
Res_a(P_r,K_alpha)         = -5625 r^5(r-1)^8,
Res_a(P_r,a-r)             = -r^3(r-1)^4,
Res_a(P_r,B_beta/(ar))     =  36 (r-1)^4(r+1)^5.
```

So the remaining `(BETA_2)` estimate can be viewed as cancellation in a
one-parameter family of bounded-conductor curve traces over the `r`-line:
there is no unbounded set of bad vertical fibers hidden inside the normalized
square-root model.  The verifier audits this by checking that every finite
branch collision or branch-boundary intersection over the audited primes lies
over the displayed `r`-supports.

For `(a,r) in G`, either the beta fiber is nonsplit over `F_p` and
contributes no rational beta points, or it has two roots `beta_1,beta_2 in
F_p^*`.  In the split case both roots lie in the main chart and have the
same singular-excess sign; write

```text
eps(a,r) = chi(d_UV(a,beta_1,r)) = chi(d_UV(a,beta_2,r)).
```

The descended sign is in fact an explicit base character.  In the coordinate
ring of the beta cover, with

```text
N_M = a^2r + a beta r - 2a beta - 2ar^2 + ar + beta r,
N_H = r(2a beta + ar - 3a - 3 beta r + beta + 2r),
```

one has the cleared square identities

```text
M^2 d_UV = r M N_M^2,
H^2 d_UV = a H N_H^2.
```

On the good base `M H != 0`, so

```text
eps(a,r) = chi(r M(a,r)) = chi(a H(a,r)).
```

The equality of the two base formulas is also forced by
`D_beta=arMH` being a square on split fibers.  The verifier checks both
cleared square identities and the resulting character equalities on all
audited good split fibers.

For any multiplicative characters `psi,phi`, the main `U V` trace therefore
splits as

```text
S^UV_{psi,phi}
  = sum_{(a,r) in G}
      psi(a) chi(rM(a,r)) (phi(beta_1)+phi(beta_2))
    + E_{psi,phi},
```

where the summand is `0` on nonsplit fibers.  The corresponding rank-two
pushforward has explicit determinant.  On a split good fiber,

```text
beta_1 beta_2 = C_beta/A_beta,
```

and the descended sign appears on both sheets, so

```text
(psi(a) eps phi(beta_1))(psi(a) eps phi(beta_2))
  = psi(a)^2 phi(C_beta/A_beta).
```

Thus, after the descended quadratic sign twist, the determinant is the base
Kummer character `psi^2 phi(C_beta/A_beta)`.  In particular the determinant
has no hidden sheet-dependent ramification: its finite zero/pole support is
only the already deleted `A_beta C_beta=0` boundary (and the toric boundary
of the compactification).  The verifier checks this determinant identity on
all audited good split fibers for the pushforward character cases.

The error term is supported
only on the curve-sized exceptional ledger

```text
A_beta=0,  C_beta=0,  D_beta=0,  a=r,  K_alpha(a,r)=0,
```

together with the separated vertical fiber, so `E_{psi,phi}=O(p)` by
counting.  For centered rows (`phi != 1`), the all-zero vertical fiber has
the exact contribution

```text
p + sum_{beta in F_p^*, beta != 1} phi(beta) = p-1,
```

so the zero conic together with the vertical tail costs at most `p`.  Away
from that vertical fiber, each deleted beta-infinity, beta-zero, and branch
base contributes at most one affine beta root, while the deleted diagonal
and lower-chart bases contribute at most two.  Since in the torus

```text
#A_beta <= 2(p-1),   #C_beta <= 2(p-1),   #D_beta <= 4(p-1),
#(a=r) = p-1,        #K_alpha <= 2(p-1),
```

the nonvertical exceptional main-chart ledger has at most `14(p-1)` points.
Together with the `5(p-1)` lower-chart bound, every centered bad contribution
outside the good beta pushforward is bounded by

```text
p + 19(p-1) < 20p.
```

The verifier checks this identity against direct main-chart summation for
several full-character pairs and audits the same sharpened bad-ledger bound
for every nonprincipal quotient-character pair in the tested quotient
orders.  The remaining analytic input is now exactly a conductor bound for
the good-base rank-two beta pushforward with kernel
`psi(a) chi(rM(a,r)) (phi(beta_1)+phi(beta_2))`.

The beta sheets also have no fixed-ratio surface.  If a good split fiber has
`lambda=beta_1/beta_2`, then the elementary symmetric relations give

```text
lambda B_beta^2 = A_beta C_beta (1+lambda)^2.
```

Conversely, for each fixed `lambda in F_p^*`, the possible good-base points
with beta-root ratio `lambda` are contained in the explicit curve

```text
R_lambda(a,r)
  = lambda B_beta^2 - A_beta C_beta (1+lambda)^2 = 0.
```

On the torus this polynomial has bidegree at most `(4,4)` after the
irrelevant `ar` factor is removed.  The special value `lambda=1` is exactly
the branch divisor already deleted from `G`, while `lambda=-1` gives the
line condition `B_beta=0`.  More explicitly, for `lambda != -1` the
torus-normalized `R_lambda` has leading `a`-coefficient
`6r^2(lambda+1)^2`, so for each fixed `r != 0` it has at most four
`a`-solutions.  For `lambda=-1`, the resonance condition is contained in
the two lines `a=1` and `r=-1`.  Hence every fixed beta-root ratio
contributes at most `4(p-1)` good-base points.  The verifier checks the
identity for both orientations `beta_1/beta_2` and `beta_2/beta_1` on every
split good fiber in the audit grid, and records the largest fixed-ratio
fiber against this explicit bound.

This gives a quotient-beta energy bound.  Fix a quotient order `e` and let
`Phi_e` be the `e` multiplicative characters trivial on the kernel `K_e`.
For the good split fibers, put `z=beta_1/beta_2`.  Character orthogonality
gives the exact local identity

```text
sum_{phi in Phi_e, phi != 1} |phi(beta_1)+phi(beta_2)|^2
  = 2e - 4 + 2e 1_{z in K_e}.
```

Therefore, if `N_split` is the number of good split fibers and `N_K` is the
number with beta-root ratio in `K_e`, then

```text
E_e^beta = (2e-4)N_split + 2e N_K.
```

The fixed-ratio bound gives

```text
N_K <= 4(p-1)|K_e| = 4(p-1)^2/e,
```

and hence

```text
E_e^beta <= (2e+4)(p-1)^2.
```

Thus the beta-sheet part of the good pushforward has fixed-quotient
nonprincipal character energy `O_e(p^2)` before any cancellation in
`alpha` or `r` is used.  The verifier checks the exact orthogonality
formula and the quotient-kernel collision bound for the audited quotient
orders.

Putting the chart reductions together gives the final singular-trace
decomposition.  For every multiplicative-character pair in the determinant
surface trace,

```text
S_{psi,phi}
  = Z_{psi,phi} + L_{psi,phi}
    + G_{psi,phi} + X_{psi,phi},
```

where `Z` is the separated zero conic, `L` is the non-`U V` lower chart,
`G` is the good-base beta pushforward just described, and `X` is the
main-chart exceptional ledger

```text
A_beta=0,  C_beta=0,  D_beta=0,  a=r,  K_alpha(a,r)=0
```

together with the vertical beta fiber.  The zero conic and centered vertical
tail contribute at most `p`, the lower chart has at most `5(p-1)` torus
points, and the nonvertical exceptional main ledger has at most `14(p-1)`
points by the degree/root-count argument above.  Thus the direct full
singular trace differs from the good beta pushforward by the explicit
uniform bound

```text
|S_{psi,phi} - G_{psi,phi}| <= p + 19(p-1) < 20p.
```

Consequently this depth-two M1 singular-excess problem has been reduced to
one analytic statement: a conductor/cancellation bound for the good
rank-two beta pushforward.  The zero conic, lower charts, branch fibers,
coordinate deletions, and vertical fiber cannot by themselves create a
superlinear obstruction.

The conductor ledger for that last pushforward is now explicit.  On the
good base, the two-sheet cover is

```text
A_beta beta^2 + B_beta beta + C_beta = 0
```

and the rank-one summand on the cover is

```text
K_{psi,phi}
  = psi(a) phi(beta) chi(d_UV(a,beta,r)).
```

All its zero/pole and ramification divisors lie in the bounded-degree
compactified boundary consisting of the toric boundary together with

```text
A_beta=0, C_beta=0, D_beta=0, a=r, K_alpha=0, d_UV=0.
```

Thus the finite pushforward has rank `2` and conductor bounded only in
terms of the fixed quotient order, not in terms of `p`.  The remaining
top-cohomology obstruction would be a geometrically constant summand.  For
the centered M1 target `phi` is nonprincipal, and the beta-zero boundary
rules this out visibly.  Namely

```text
C_beta = ar Q_beta(a,r),
Q_beta = -2a^2r + 3ar^2 - ar + 3a - 3r,
```

while at `beta=0`

```text
d_UV(a,0,r) = ar^2(-3a+4r).
```

The needed component-separation resultants are all explicit:

```text
Res_a(Q_beta, B_beta/(ar))       =  3(r-1)^2(r+1)^2,
Res_r(Q_beta, B_beta/(ar))       =  (a-1)^2(a+3)(2a+1),

Res_a(Q_beta, d_UV(a,0,r))       = -3r^6(2r-3)^2,
Res_r(Q_beta, d_UV(a,0,r))       =  27a^5(a-2)^2,

Res_a(Q_beta, A_beta)            = -3r^2(r-1)^2(3r^2+4r+3),
Res_r(Q_beta, A_beta)            =  9a^2(a-1)^2(a+1)^2,

Res_a(Q_beta, M)                 = -3r^2(r-1)^2(r+1)^2,
Res_r(Q_beta, M)                 =  a^2(a-1)^2(a+3)^2,

Res_a(Q_beta, H)                 = -18r^2(r-1)^2(r+1)^2,
Res_r(Q_beta, H)                 =  9a^2(a-1)^2(2a+1)^2,

Res_a(Q_beta, a-r)               =  r^2(r-1),
Res_r(Q_beta, a-r)               =  a^2(a-1),

Res_a(Q_beta, K_alpha)           =  3r^2(r-1)^2(2r-3)(3r-2),
Res_r(Q_beta, K_alpha)           =  9a^2(a-2)^2(a-1)^2.
```

Thus `Q_beta=0` has no common component with the beta-linear coefficient
`B_beta` (so `beta` is generically a local parameter), the `U V` sign
divisor, beta infinity, either branch curve, the diagonal `a=r`, or the
lower-chart divisor `K_alpha=0`.  The verifier audits the corresponding
finite intersections by checking that every intersection point lies in the
displayed resultant root supports.  Hence at the generic point of the
beta-zero boundary, the local monodromy of `K_{psi,phi}` is exactly `phi`,
which is nontrivial.  Therefore the good pushforward has no geometrically
constant summand in the nonprincipal `phi` rows relevant to the centered
singular matrix.

The opposite vertical beta boundary is equally controlled.  Write
`gamma=1/beta`; then the beta equation is

```text
A_beta + B_beta gamma + C_beta gamma^2 = 0,
```

so the beta-infinity sheet lies over `A_beta=0`.  At `gamma=0`,
`phi(beta)=phi(gamma)^(-1)` and

```text
d_UV(a,beta,r) = gamma^{-2} r(4a-3r) + O(gamma^{-1}),
```

so the quadratic pole is invisible to `chi` and the generic local monodromy
is `phi^{-1}`.  The component separations are again explicit:

```text
Res_a(A_beta, B_beta/(ar))       = -3(r-1)^2(r+1)^2,
Res_r(A_beta, B_beta/(ar))       = -(a-1)^2(a+2)(3a+1),

Res_a(A_beta, Q_beta)            = -3r^2(r-1)^2(3r^2+4r+3),
Res_r(A_beta, Q_beta)            =  9a^2(a-1)^2(a+1)^2,

Res_a(A_beta, 4a-3r)             = -r(3r-2)^2,
Res_r(A_beta, 4a-3r)             = -3a(2a-1)^2,

Res_a(A_beta, M)                 = -3r^2(r-1)^2(r+1)^2,
Res_r(A_beta, M)                 =  a^2(a-1)^2(3a+1)^2,

Res_a(A_beta, H)                 = -18r^2(r-1)^2(r+1)^2,
Res_r(A_beta, H)                 =  9a^2(a-1)^2(a+2)^2,

Res_a(A_beta, a-r)               =  r(r-1),
Res_r(A_beta, a-r)               =  a(a-1),

Res_a(A_beta, K_alpha)           =  3r^2(r-1)^2(2r-3)(3r-2),
Res_r(A_beta, K_alpha)           =  9a^2(a-1)^2(2a-1)^2.
```

Thus the beta-infinity boundary also has no common component with the
beta-linear, beta-zero, `U V` leading-coefficient, branch, diagonal, or
lower-chart divisors.  At its generic point the local monodromy is
`phi^{-1}`, again nontrivial for the centered rows.  The verifier audits
these finite intersections in the same root-support style as the beta-zero
ledger.

The quadratic `U V` sign itself has no finite divisor on the good cover.
After removing the harmless unit `r`,

```text
d_UV/r = (4a-3r) beta^2 - 2ar beta - 3a^2r + 4ar^2.
```

Taking the resultant with the beta equation gives the exact square

```text
Res_beta(A_beta beta^2+B_beta beta+C_beta, d_UV/r)
  = a^2 r^2 (a-r)^2 K_alpha(a,r)^2.
```

Thus every finite common point of the beta cover with `d_UV=0` projects to
the already deleted diagonal `a=r` or lower-chart curve `K_alpha=0` (on the
torus `a,r != 0`).  On the good base `G`, `d_UV` is everywhere nonzero on
`Y_G`.  Hence the `chi(d_UV)` factor contributes no additional finite branch
divisor to the good beta pushforward; its finite zeros are already in the
bad ledger, and its beta-infinity leading coefficient was handled in the
vertical-boundary audit above.  The verifier checks the resultant identity
and confirms that there are no good-base common roots on the audited prime
grid.

Consequently, under the bounded-conductor rank-two beta-pushforward import
`(BETA_2)` recorded in `m1_kummer_weil_import_contract.md`, the good
pushforward satisfies

```text
G_{psi,phi} = O_e(p)
```

for every fixed quotient order `e` and every centered character pair
(`psi,phi`) with `phi != 1`.  Combined with the explicit `O(p)` bad-ledger
decomposition above, this conditionally gives the desired
`S_{psi,phi}=O_e(p)` singular-trace bound for the depth-two M1
determinant-surface target.  The conditional input is now isolated: it is
only the bounded-conductor trace estimate for this explicitly charted
rank-two beta pushforward, not any further combinatorial or bookkeeping
loss.

At the quotient-matrix level the implication is completely explicit.  Suppose
the imported pushforward estimate gives

```text
|G_{psi,phi}| <= C_beta(e) p
```

for all nonprincipal characters of a fixed quotient order `e`.  Since the
bad ledger above gives `|S_{psi,phi}-G_{psi,phi}| <= 20p`, every centered
singular trace satisfies

```text
|S_{psi,phi}| <= (C_beta(e)+20)p.
```

Therefore Parseval gives

```text
||Gamma_e^circ||_F
  <= ((e-1)/e)(C_beta(e)+20)p,
```

and the singular projective excess obeys

```text
|P_e| <= (e-1)^2(C_beta(e)+20)p^2.
```

Finally the closed boundary inequality already proved above yields

```text
M_e^o
  <= ((e-1)sqrt(C_beta(e)+20)p + 3(e-1)sqrt(p))^2.
```

Thus the conditional beta-pushforward estimate would close the depth-two
quotient-conic M1 target in the precise required form
`M_e^o=O_e(p^2)`.  The verifier now audits the singular-trace partition not
only on sample full-character pairs but on every nonprincipal quotient
character pair for the tested quotient orders, using the quotient-label
matrix before applying Fourier inversion.

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
