# F1 Syndrome-Pencil Normal Form

Status: PROVED / AUDIT.

This note extracts a self-contained theorem from the Cycle49
syndrome-transverse-secant audit. It does not prove F1. Its purpose is to
replace the informal "extension-line residue cloud" language by an exact
Hankel-pencil incidence problem with a proved noncontainment test.

The result applies over any field. In the F1 setting one takes
`B subset F`, `D subset B`, and studies `RS[F,D,k]`; genuinely `F`-valued
lines are then handled over the actual line field `F`.

## Set-Up

Let `F` be a field, let

```text
D = {x_1,...,x_n} subset F
```

have distinct points, and let

```text
C = RS[F,D,k],        r = n-k.
```

For each `x_i`, put

```text
lambda_i = 1 / product_{h != i} (x_i - x_h).
```

For a word `y:D->F`, define its Reed-Solomon syndrome by

```text
Syn(y)_m = sum_i lambda_i x_i^m y(x_i),        0 <= m < r.
```

The standard duality identity says `Syn(y)=0` if and only if `y in C`.

For a complement `T subset D` of size `j`, let

```text
L_T(X) = product_{x in T} (X-x)
       = ell_0 + ell_1 X + ... + ell_j X^j,    ell_j = 1.
```

Let `ell_T=(ell_0,...,ell_j)^T`. If `t=r-j`, define the Hankel window

```text
H_{t,j}(w)_{m,l} = w_{m+l},        0 <= m < t, 0 <= l <= j
```

for every `w in F^r`.

Finally, let `W_T` be the span of the parity-check columns indexed by `T`:

```text
W_T = span_F { lambda_x (1,x,x^2,...,x^{r-1}) : x in T } subset F^r.
```

Equivalently, `w in W_T` means that `w` is the syndrome of a word supported on
`T`.

## Theorem 1: Hankel Recurrence For A Support Complement

For every `w in F^r`,

```text
w in W_T    if and only if    H_{t,j}(w) ell_T = 0.
```

## Proof

If

```text
w_m = sum_{x in T} c_x x^m,
```

then, for `0 <= m < t`,

```text
(H_{t,j}(w) ell_T)_m
  = sum_{l=0}^j ell_l w_{m+l}
  = sum_{x in T} c_x x^m L_T(x)
  = 0.
```

Thus `W_T` lies in the displayed recurrence space.

Conversely, because `ell_j=1`, the recurrence

```text
sum_{l=0}^j ell_l w_{m+l}=0,        0 <= m < r-j,
```

determines all coordinates `w_j,...,w_{r-1}` from the first `j` coordinates.
Hence its solution space has dimension at most `j`. The columns indexed by the
distinct points of `T` form a Vandermonde system of rank `j`, so
`dim W_T=j`. The two spaces are equal.

## Theorem 2: Exact Line-Incidence And Noncontainment Test

Let `f,g:D->F`, write

```text
u = Syn(f),        v = Syn(g),
```

and let `S=D\T`, so `|S|=n-j=k+t`. For a slope `z in F`, the line point

```text
f + z g
```

is explained by a degree-`<k` codeword on `S` if and only if

```text
(H_{t,j}(u) + z H_{t,j}(v)) ell_T = 0.          (1)
```

Moreover, this explanation is support-wise noncontained for the line `f+zg`
on `S` if and only if, in addition to (1),

```text
H_{t,j}(v) ell_T != 0.                          (2)
```

Consequently the support-wise MCA bad slopes at agreement `k+t` are exactly
the slopes `z` for which there exists a squarefree `D`-split monic locator
`L_T` of degree `j=r-t` satisfying (1) and (2).

## Proof

The word `f+zg` is explained on `S` if and only if there exists a codeword
`c in C` such that `f+zg-c` is supported on `T`. Taking syndromes and using
`Syn(c)=0`, this is equivalent to

```text
u + z v in W_T.
```

Theorem 1 turns this into (1).

The same support `S` simultaneously explains `f` and `g` if and only if

```text
u in W_T        and        v in W_T.
```

Assume (1). If `v in W_T`, then `u=(u+zv)-zv` also lies in `W_T`, so the line
is contained on `S`. Conversely, simultaneous explanation implies `v in W_T`.
By Theorem 1, `v in W_T` is exactly `H_{t,j}(v)ell_T=0`. Thus noncontainment
is precisely (2).

## Corollary 3: Common-Core Dimension Reduction

For fixed line syndromes `u,v`, set

```text
K_0 = ker H_{t,j}(u) cap ker H_{t,j}(v) subset F^{j+1}.
```

Then every active locator vector `ell_T` is tested only through its image in

```text
V = F^{j+1}/K_0,
```

and

```text
dim V <= 2t.
```

Thus the F1 incidence problem at slack `t` is not an incidence problem in the
full `j`-dimensional locator coefficient space. After deleting the common
contained/tangent core, the moving part lives in a space whose dimension is
bounded only by the slack.

## Proof

The equations in Theorem 2 only use `H(u)ell_T` and `H(v)ell_T`, so adding an
element of `K_0` to `ell_T` changes neither the landing condition nor the
noncontainment test.

Also,

```text
codim K_0
  = rank [ H_{t,j}(u) ; H_{t,j}(v) ]
  <= rank H_{t,j}(u) + rank H_{t,j}(v)
  <= 2t,
```

because each Hankel window has `t` rows.

## Corollary 4: Projective Slope Gate

For a complement `T`, put

```text
a_T = H_{t,j}(u) ell_T,        b_T = H_{t,j}(v) ell_T    in F^t.
```

Then `T` contributes a noncontained bad slope if and only if

```text
b_T != 0
```

and `a_T` is a scalar multiple of `b_T`. When this happens, the slope is
unique and is given by

```text
z_T = - a_{T,m} / b_{T,m}
```

for any coordinate `m` with `b_{T,m} != 0`.

Equivalently, `T` passes the slope gate exactly when

```text
a_{T,m} b_{T,l} - a_{T,l} b_{T,m} = 0
        for all 0 <= m < l < t,
```

and `b_T != 0`.

In particular:

- for `t=1`, every complement with `b_T != 0` contributes one slope;
- for `t=2`, the whole landing gate is the single determinant

```text
a_{T,0} b_{T,1} - a_{T,1} b_{T,0} = 0,
```

with the noncontainment condition `b_T != 0`.

## Proof

The landing equation from Theorem 2 is

```text
a_T + z b_T = 0.
```

If `b_T=0`, any landing is contained, by Theorem 2, so `T` contributes no
noncontained slope. If `b_T != 0`, a solution `z` exists exactly when `a_T`
lies on the one-dimensional line spanned by `b_T`; the scalar is forced by any
nonzero coordinate of `b_T`. The displayed minors are the usual rank-one
criterion for the two-column matrix `[a_T b_T]`.

## Corollary 5: Compatibility With Extension Coordinates

Let `B subset F` be a finite field extension, let `D subset B`, and choose a
`B`-basis `omega_1,...,omega_e` of `F`. For `y:D->F`, write

```text
y = sum_i y_i omega_i,        y_i:D->B.
```

Then syndrome formation commutes with coordinate expansion:

```text
Syn_F(y) = sum_i Syn_B(y_i) omega_i.
```

Consequently, if `M_z` is the multiplication-by-`z` matrix in this basis, then
the F1 Hankel-pencil condition over `F`,

```text
(H_F(Syn_F(f)) + z H_F(Syn_F(g))) ell_T = 0,
```

is exactly the coordinate/interleaved base-field condition

```text
H_B(Syn_B(Phi(f)) + M_z Syn_B(Phi(g))) ell_T = 0
```

in the `e` base coordinates.

Thus the syndrome-pencil normal form is the support-level version of the
previous extension-coordinate transfer theorem: extension-line MCA over `F`
is a multiplication-slice incidence problem inside the `e`-interleaved
base-code syndrome space.

## Proof

For `x in D subset B`, both `lambda_x` and `x^m` lie in `B`. Hence

```text
Syn_F(y)_m
  = sum_x lambda_x x^m sum_i y_i(x) omega_i
  = sum_i (sum_x lambda_x x^m y_i(x)) omega_i
  = sum_i Syn_B(y_i)_m omega_i.
```

The line identity follows from `B`-linearity of coordinate expansion and from
the definition of `M_z`.

## Corollary 6: Quotient-Periodic Locator Restriction

Assume now that `D=H` is a multiplicative subgroup of `F^*` of order `n`. Let
`M|n`, write

```text
pi_M(x)=x^M,        H_M=pi_M(H),
```

and let `A subset H_M` have size `j'`. Put `T=pi_M^{-1}(A)`, so
`|T|=j=M j'`. If

```text
L_A(Y) = c_0 + c_1 Y + ... + c_{j'} Y^{j'},
```

then

```text
L_T(X) = L_A(X^M).
```

Equivalently, the locator vector `ell_T` is supported only in degrees
divisible by `M`:

```text
ell_{M s}=c_s,        ell_l=0 if M does not divide l.
```

For every syndrome vector `w`, the Hankel product becomes the decimated
syndrome window

```text
(H_{t,j}(w) ell_T)_m
  = sum_{s=0}^{j'} c_s w_{m+M s},        0 <= m < t.
```

In particular, for `t=2`, a quotient-periodic complement contributes a
noncontained slope exactly when

```text
(B_0,B_1) != (0,0)
```

and

```text
A_0 B_1 - A_1 B_0 = 0,
```

where

```text
A_m = sum_s c_s u_{m+M s},        B_m = sum_s c_s v_{m+M s},
        m=0,1.
```

The slope, when it exists, is `-A_m/B_m` for any nonzero `B_m`.

## Proof

The fiber over `a in H_M` is the set of roots in `H` of `X^M-a`. Hence the
locator of the union of fibers over `A` is

```text
prod_{a in A} (X^M-a) = L_A(X^M).
```

Reading coefficients gives the sparse locator vector. Substituting this sparse
vector into the Hankel product gives the decimated formula. The final `t=2`
criterion is Corollary 4 applied to the two decimated vectors.

## Corollary 7: The Reduced `t=2` Gate Is A Quadric

Assume `t=2`. Let `E=F^{j+1}` be the locator-coefficient space, and define

```text
R:E -> Mat_{2 x 2}(F),        R(ell) = [ a(ell)  b(ell) ],
```

where

```text
a(ell)=H_{2,j}(u)ell,        b(ell)=H_{2,j}(v)ell.
```

Let `W=R(E)`. The bad-slope landing gate is the pullback of the determinant
quadric

```text
det : W subset Mat_{2 x 2}(F) -> F.
```

Equivalently,

```text
q(ell)
  = a_0(ell)b_1(ell) - a_1(ell)b_0(ell).
```

The common-core quotient of Corollary 3 is exactly the passage from `E` to
`W`, and `dim W <= 4`.

If `q` is not identically zero on `W`, then the `t=2` gate is a genuine
quadric hypersurface in the reduced moving image. If `q` is identically zero
on `W`, then `dim W <= 2`; when `dim W=2`, the projective line `P(W)` lies in
one of the two rulings of the rank-one quadric:

- either all matrices in `W` have image contained in one fixed line in `F^2`;
- or all matrices in `W` have kernel containing one fixed line in `F^2`.

Thus the degenerate rank/determinant branch is not an arbitrary high-
dimensional exceptional set. It is a ruled linear artifact. Outside that
artifact, `t=2` F1 becomes an incidence problem between projected split
locators and one explicit quadric in a space of dimension at most four.

For a fixed slope `z`, the fiber is the linear section

```text
a(ell) + z b(ell) = 0.
```

Hence the global `t=2` problem splits into:

```text
determinant incidence:       q(ell)=0,
slope-fiber collision:       ell lies in a two-equation linear section.
```

## Proof

Corollary 4 says exactly that the landing gate is

```text
det [ a(ell) b(ell) ] = 0,
```

and Corollary 3 says the kernel of `R` is the common core
`ker H(u) cap ker H(v)`. Hence the gate descends to `W=R(E)`, whose dimension
is at most four.

It remains only to record the elementary linear-algebra classification of the
identically-zero case. The determinant quadric in `Mat_{2 x 2}` is smooth: in
coordinates

```text
(A_0,A_1,B_0,B_1)
```

its gradient is

```text
(B_1,-B_0,-A_1,A_0),
```

which vanishes only at the zero matrix. Therefore no three-dimensional linear
subspace is contained in the determinant-zero cone, so `dim W<=2`.

If `dim W=2`, choose a rank-one matrix in `W` and change bases in the source
and target so it is

```text
[[1,0],[0,0]].
```

For any other matrix

```text
[[a,b],[c,d]]
```

in `W`, the vanishing of its determinant and of the determinant after adding
the first matrix force

```text
d=0,        bc=0.
```

Thus either `b=0` for the whole second generator, giving a common kernel line,
or `c=0`, giving a common image line. This is exactly the two-ruling
classification.

The fixed-slope statement is just the original landing equation
`a+zb=0`.

## Corollary 8: Fixed-Slope Fibers Are Usually Codimension Two

Assume `t=2` and fix a slope `z in F`. Put

```text
P_z = H_{2,j}(u) + z H_{2,j}(v).
```

Then the support complements contributing the slope `z` are exactly the
squarefree `D`-split monic locators `ell_T` satisfying

```text
P_z ell_T = 0
```

and

```text
H_{2,j}(v)ell_T != 0.
```

Thus same-slope collisions are split-locator intersections with the linear
space `ker P_z`, after deleting the contained part. If `rank P_z=2`, this is
a codimension-two linear section of the locator-coefficient space. If
`rank P_z<=1`, it is a rank-defective exceptional slope.

The rank-defective slope set is tiny unless the whole pencil is degenerate:

```text
#{ z in F : rank P_z <= 1 } <= 2
```

unless `rank P_z<=1` for every `z in F`.

Equivalently, outside at most two slopes, or outside the global rank-one
pencil branch, every same-slope collision problem in the `t=2` F1 reduction is
a split-locator count in a fixed codimension-two linear subspace.

## Proof

The fixed-slope criterion is Theorem 2 with `t=2`, and the noncontainment
condition is unchanged.

For the rank-defective assertion, write the two columns of `P_z` indexed by
`r<s` as affine-linear functions of `z`. The minor

```text
m_{r,s}(z)=det(P_z[:,r], P_z[:,s])
```

is a polynomial of degree at most two. The condition `rank P_z<=1` is exactly
the simultaneous vanishing of all these minors. If at least one minor is not
the zero polynomial, then all rank-defective slopes lie among the roots of
that one nonzero quadratic, hence there are at most two. If every minor is the
zero polynomial, then `rank P_z<=1` identically in `z`.

## Corollary 9: The `j=2` Fixed-Slope Fiber Is Linear-Sized

Assume `t=2` and `j=2`, so support complements have size two. Fix a slope
`z`, and put

```text
P_z = H_{2,2}(u) + z H_{2,2}(v).
```

Let `D` be the evaluation set. Then the number of two-point complements
`T={x,y}` satisfying the landing equation

```text
P_z ell_T = 0
```

obeys the following bounds:

- if `rank P_z=2`, there is at most one such complement;
- if `rank P_z=1`, there are at most `|D|` such complements;
- if `rank P_z=0`, this is a rank-zero exceptional slope and the landing
  equation imposes no restriction.

The same bounds hold after imposing the noncontainment condition
`H(v)ell_T != 0`.

## Proof

For `T={x,y}`, the monic locator vector is

```text
ell_T = (xy, -(x+y), 1).
```

If `rank P_z=2`, the homogeneous kernel of `P_z` is one-dimensional. Its
intersection with the affine monic slice `ell_2=1` is empty or a single point,
so at most one monic locator, and hence at most one complement, can land.

If `rank P_z=1`, the landing equation is one nonzero linear equation

```text
alpha c_0 + beta c_1 + gamma = 0
```

in the locator coefficients. Substituting `c_0=xy` and `c_1=-(x+y)` gives

```text
alpha xy - beta(x+y) + gamma = 0.              (3)
```

If `alpha=0` and `beta!=0`, then (3) fixes the sum `x+y`, giving at most one
partner for each `x` and hence at most `|D|/2` unordered complements. If
`alpha!=0`, then for every `x` except possibly `x=beta/alpha`, equation (3)
determines at most one `y`. At the exceptional `x`, either no `y` works or
the equation factors as

```text
(alpha x - beta)(alpha y - beta)=0,
```

which gives only the star through `x=beta/alpha`. In all cases there are at
most `|D|` unordered distinct complements. The noncontainment condition only
removes complements.

## Corollary 10: The `j=3` Monic-Rank-Two Fiber Is Linear-Sized

Assume `t=2` and `j=3`, so support complements have size three. Fix a slope
`z`, put

```text
P_z = H_{2,3}(u) + z H_{2,3}(v),
```

and let `A_z` be the `2 x 3` matrix formed from the first three columns of
`P_z`, i.e. the columns acting on the non-monic coefficients
`(c_0,c_1,c_2)`.

If `rank A_z=2`, then the number of three-point complements `T` satisfying

```text
P_z ell_T = 0
```

is at most `|D|`. The same bound holds after imposing the noncontainment
condition `H(v)ell_T != 0`.

Moreover, the monic-rank-defective slope set is tiny unless it is global:

```text
#{ z in F : rank A_z <= 1 } <= 2
```

unless `rank A_z<=1` for every `z in F`.

Thus, outside at most two monic-rank-defective slopes, or outside the global
monic-rank-one branch, every `j=3` fixed-slope fiber is linear-sized.

## Proof

Write the monic cubic locator as

```text
L_T(X)=X^3+c_2X^2+c_1X+c_0.
```

If `rank A_z=2`, the affine solution set to `P_z ell=0` in the monic slice is
empty or a line. Therefore every landing locator lies in a one-parameter
family

```text
P_lambda(X)=P_0(X)+lambda Q(X),
```

where `P_0` is monic cubic and `Q` has degree at most two and is not zero.

The common roots of every polynomial in this family are the roots of
`gcd(P_0,Q)`, hence there are at most two of them. A squarefree split cubic
with three roots in `D` therefore has at least one non-common root `x`. For
that root,

```text
P_0(x)+lambda Q(x)=0,        Q(x) != 0,
```

so `lambda` is uniquely determined by `x`. Assign to each landing cubic its
first non-common root in any fixed ordering of `D`; this gives an injection
from landing cubics into `D`. Hence there are at most `|D|` landings.
Noncontainment only deletes landings.

For the final assertion, the condition `rank A_z<=1` is the simultaneous
vanishing of the three `2 x 2` minors of the affine-linear `2 x 3` matrix
`A_z`. Each minor is a polynomial of degree at most two in `z`. If one minor
is not identically zero, there are at most two such slopes. If all minors
vanish identically, the monic-rank-defective branch is global.

## Corollary 11: Global `j=3` Monic-Rank-One Is A Fixed-Root Readout

Assume `t=2` and `j=3`. Suppose the monic-rank defect is global as a
polynomial identity in the slope, i.e.

```text
rank A_z <= 1        for every z
```

where `A_z` is the `2 x 3` matrix from Corollary 10. Then the first four
syndrome entries of the pencil lie on one fixed twisted-cubic line:

```text
(u_0,u_1,u_2,u_3)=a(s^3,s^2t,st^2,t^3),
(v_0,v_1,v_2,v_3)=b(s^3,s^2t,st^2,t^3)
```

for some `[s:t] in P^1(F)` and scalars `a,b in F`.

If `s != 0`, put `alpha=t/s`. For every slope with
`a+zb != 0`, the first row of the landing equation is

```text
(a+zb) s^3 L_T(alpha)=0.
```

Thus every split complement landing at such a slope must contain the fixed
point `alpha`. In particular:

- if `alpha notin D`, there are no such split complements;
- if `alpha in D`, all such split complements lie in the star through
  `alpha`, so there are at most `binom(|D|-1,2)` of them before the second
  row and noncontainment condition are imposed.

If `s=0`, then the first row is zero on the non-monic coefficients and equals
`(a+zb)t^3` on the monic coefficient. Hence every slope with `a+zb != 0` has
no landing split complement at all.

So the global monic-rank-one branch is not a new aperiodic incidence surface:
outside at most one scalar-zero slope, it is either empty or a fixed-root
star.

## Proof

The global hypothesis says that the projective line spanned by
`(u_0,u_1,u_2,u_3)` and `(v_0,v_1,v_2,v_3)` lies in the projective cone of
rank-one `2 x 3` Hankel matrices. This cone is the twisted cubic

```text
[s:t] -> [s^3:s^2t:st^2:t^3],
```

and it contains no projective line. Equivalently, a direct two-point
calculation shows that the sum of two non-proportional points of the above
form violates one of the `2 x 2` Hankel minors. Hence the two pencil vectors
are scalar multiples of one fixed twisted-cubic point.

For `s != 0`, the first row of `P_z` is

```text
(a+zb)s^3(1,alpha,alpha^2,alpha^3),
```

and its dot product with the monic locator vector
`(c_0,c_1,c_2,1)` is `(a+zb)s^3 L_T(alpha)`. This proves the finite-root
claims. The case `s=0` gives first row `(0,0,0,(a+zb)t^3)`, whose dot product
with a monic locator is nonzero whenever `a+zb != 0`.

## Corollary 12: Fixed-Root Stars Contract To `j=2`

Keep the finite-root case of Corollary 11, assume `alpha in D`, and consider
a slope with `a+zb != 0`. Every landing complement has the form

```text
T = {alpha} union U,        |U|=2.
```

Write

```text
L_U(X)=X^2+m_1X+m_0.
```

If the second row of `P_z` is

```text
r=(r_0,r_1,r_2,r_3),
```

then the remaining landing equation is exactly

```text
(r_1-alpha r_0)m_0
  + (r_2-alpha r_1)m_1
  + (r_3-alpha r_2) = 0.                    (4)
```

Thus the fixed-root star is a contracted `j=2` fiber on the punctured domain
`D \ {alpha}`.

Consequently, if the contracted row in (4) is nonzero, the number of landing
complements at this slope is at most `|D|-1`. If the contracted row is zero,
the whole star through `alpha` lands, giving at most `binom(|D|-1,2)`
complements before noncontainment is imposed.

Finally, unless the contracted row is identically zero as a function of the
slope, the zero-contraction slopes number at most one.

## Proof

For `T={alpha} union U`,

```text
L_T(X)=(X-alpha)L_U(X)
```

and therefore the coefficient vector of `L_T` is

```text
(-alpha m_0, m_0-alpha m_1, m_1-alpha, 1).
```

Taking the dot product with `r` gives (4). The finite bound is exactly the
rank-one `j=2` argument from Corollary 9 applied on `D \ {alpha}`. The
contracted row is affine-linear in `z`, so if one component is not the zero
linear polynomial, all simultaneous zeros lie at the root of that component.

## Corollary 13: Global Fixed-Root Stars Have Polynomial Slope Count

Keep the finite fixed-root setting of Corollary 12 with `alpha in D`. Outside
the possible scalar-zero slope `a+zb=0`, the number of noncontained bad slopes
coming from the fixed-root star is at most

```text
binom(|D|-1,2).
```

Including the scalar-zero slope gives the unconditional bound

```text
1 + binom(|D|-1,2).
```

If `alpha notin D`, the corresponding bound is `1`: only the scalar-zero
slope can remain. If the fixed point is infinity, the same bound is `1`.

## Proof

Assume `alpha in D` and `a+zb != 0`. By Corollary 11 every landing complement
has the form

```text
T={alpha} union U,        |U|=2.
```

By Corollary 12 the remaining landing equation is

```text
C_0(z)m_0 + C_1(z)m_1 + C_2(z)=0,              (5)
```

where the coefficients are affine-linear in `z`, and
`L_U(X)=X^2+m_1X+m_0`.

For a fixed pair `U`, either (5) is a nonzero affine-linear equation in `z`,
which contributes at most one slope, or (5) is identically zero in `z`. In the
identically-zero case both the `u`-row and the `v`-row contractions vanish.
Since `L_T(alpha)=0`, both rows of `H(v)ell_T` vanish, so this pair is
contained and is removed by the noncontainment condition. Hence each remaining
pair contributes at most one noncontained slope, giving
`binom(|D|-1,2)`.

If `alpha notin D`, Corollary 11 gives no landing complement away from
`a+zb=0`. If the fixed point is infinity, the first row is nonzero on the
monic coefficient away from `a+zb=0`, so again there are no landing
complements away from the scalar-zero slope.

## Corollary 14: Regular Fixed-Slope Fibers Lose Two Roots

Assume `t=2`, but now allow arbitrary complement size `j >= 2`. Fix a slope
`z`, put

```text
P_z = H_{2,j}(u) + z H_{2,j}(v),
```

and let `A_z` be the `2 x j` matrix formed from the first `j` columns of
`P_z`, acting on the non-monic coefficients `(c_0,...,c_{j-1})` of a monic
degree-`j` locator.

If

```text
rank A_z = 2,
```

then the number of squarefree `D`-split monic degree-`j` locators satisfying

```text
P_z ell_T = 0
```

is at most

```text
binom(|D|, j-2).
```

The same bound holds after imposing noncontainment
`H_{2,j}(v)ell_T != 0`.

Moreover, as `z` varies, the slopes with `rank A_z <= 1` number at most two
unless `rank A_z <= 1` identically in `z`. Hence outside at most two
monic-rank-defective slopes, or outside the global defective branch, every
fixed-slope fiber has the displayed codimension-two split-locator size.

## Proof

If the affine monic system is inconsistent, there is nothing to prove.
Otherwise its solution set is an affine family

```text
P_0(X) + V,
```

where `P_0` is monic of degree `j`, `V` is a vector space of polynomials of
degree `< j`, and

```text
dim V = j-2.
```

Let `L_T` be any landing locator in this family, with `T subset D` and
`|T|=j`. The evaluation map

```text
ev_T: V -> F^T
```

is injective: if `Q in V` vanishes on every point of `T`, then `Q` has at
least `j` distinct roots but degree `< j`, so `Q=0`. Thus some subset
`R subset T` of size `j-2` already makes

```text
ev_R: V -> F^R
```

an isomorphism. Choose the first such `R` in any fixed ordering of the
`(j-2)`-subsets of `T`.

For a fixed `R`, the equations

```text
P(x)=0,        x in R,
```

determine the element `P in P_0+V` uniquely, because `ev_R` is invertible on
`V`. Therefore the above choice injects landing locators into the
`(j-2)`-subsets of `D`, giving the claimed bound.

The noncontainment condition only deletes landing locators. The defective
slope assertion is the same minor argument as in Corollary 10: the `2 x 2`
minors of the affine-linear matrix `A_z` are quadratic polynomials in `z`; if
one is not identically zero, the simultaneous zero set is contained in its at
most two roots.

## Corollary 15: Global Monic-Rank-One Is Always A Fixed-Root Star

Assume `t=2` and `j >= 2`. Suppose the monic-rank defect is global as a
polynomial identity in the slope:

```text
rank A_z <= 1        for every z,
```

where `A_z` is the `2 x j` matrix from Corollary 14. Then the first `j+1`
syndrome entries of the pencil lie on one fixed rational-normal point:

```text
(u_0,...,u_j)=a(s^j,s^{j-1}t,...,st^{j-1},t^j),
(v_0,...,v_j)=b(s^j,s^{j-1}t,...,st^{j-1},t^j)
```

for some `[s:t] in P^1(F)` and scalars `a,b in F`.

If `s != 0`, put `alpha=t/s`. For every slope with `a+zb != 0`, the first
row of the landing equation is

```text
(a+zb)s^j L_T(alpha)=0.
```

Thus every split complement landing at such a slope must contain the fixed
point `alpha`. Consequently:

- if `alpha notin D`, there are no non-scalar-zero landing complements;
- if `alpha in D`, all such landing complements lie in the star
  `T={alpha} union U`, with `|U|=j-1`.

In the case `alpha in D`, the number of noncontained non-scalar-zero slopes
coming from this whole global branch is at most

```text
binom(|D|-1,j-1),
```

and including the possible scalar-zero slope gives

```text
1 + binom(|D|-1,j-1).
```

If `alpha notin D`, or if `s=0`, the corresponding total bound is `1`.

At any fixed non-scalar-zero slope in the fixed-root case, a nonzero
contracted row leaves at most `binom(|D|-1,j-2)` landing complements, while a
zero contracted row leaves the whole fixed-root star before noncontainment is
imposed.

## Proof

The global hypothesis says that the projective line spanned by
`(u_0,...,u_j)` and `(v_0,...,v_j)` lies in the projective variety cut out by
the `2 x 2` minors of

```text
[ w_0  w_1  ...  w_{j-1} ]
[ w_1  w_2  ...  w_j     ].
```

This variety is the degree-`j` rational normal curve

```text
[s:t] -> [s^j:s^{j-1}t:...:st^{j-1}:t^j].
```

Indeed, if `w_0 != 0`, the adjacent minors force a single ratio
`w_{m+1}/w_m`; if the first nonzero coordinate occurred strictly between
`w_0` and `w_j`, the minor using the previous column would force its square
to vanish. Hence the only remaining endpoint case is `[0:...:0:1]`. Since a
rational normal curve contains no projective line for `j >= 2`, the two
pencil vectors are scalar multiples of one fixed rational-normal point.

For `s != 0`, the first row of `P_z` is

```text
(a+zb)s^j(1,alpha,...,alpha^j),
```

and its dot product with the monic locator vector is
`(a+zb)s^j L_T(alpha)`. This proves the fixed-root or empty landing
alternative away from the scalar-zero slope. If `s=0`, the first row has only
the monic coordinate nonzero, so no monic locator can land away from the
scalar-zero slope.

It remains to count noncontained slopes in the fixed-root case
`alpha in D`. Write

```text
T={alpha} union U,        L_T(X)=(X-alpha)L_U(X),
```

where `L_U(X)=m_0+m_1X+...+m_{j-1}X^{j-1}` is monic. If
`r=(r_0,...,r_j)` is the second row of `P_z`, then

```text
r . ell_T = sum_{h=0}^{j-1} (r_{h+1}-alpha r_h)m_h.       (6)
```

For a fixed `U`, the right side is affine-linear in `z`. If it is not the
zero affine-linear function, it contributes at most one slope. If it is
identically zero, then the corresponding contractions for both `u` and `v`
vanish. Since `L_T(alpha)=0`, the first row of `H(v)ell_T` also vanishes, and
(6) gives the second row. Thus `H(v)ell_T=0`, so this landing is contained
and is removed by noncontainment.

Therefore each choice of `U subset D \ {alpha}` with `|U|=j-1` contributes at
most one noncontained non-scalar-zero slope. There are
`binom(|D|-1,j-1)` such choices.

For the fixed-slope landing bound, a nonzero contracted row is one affine
linear equation on monic degree-`j-1` locators over `D \ {alpha}`. The same
evaluation-injection argument as in Corollary 14, with dimension `j-2`, gives
`binom(|D|-1,j-2)`. If the contracted row is zero, every `U` in the punctured
domain lands before noncontainment is checked.

## Corollary 16: The `t=2` Branch Ledger

Assume `t=2` and `j >= 2`. For each slope put

```text
P_z = H_{2,j}(u) + zH_{2,j}(v),
```

and let `A_z` be the `2 x j` non-monic block of `P_z`. Let `Bad` be the set
of noncontained bad slopes. Then exactly one of the following alternatives
holds.

1. **Global monic-rank defect.** If `rank A_z <= 1` for every `z`, then
   Corollary 15 applies. The branch is empty, an infinity branch, or a
   fixed-root star. In particular, if the fixed root is `alpha in D`, then

   ```text
   |Bad| <= 1 + binom(|D|-1,j-1),
   ```

   while if the fixed point is infinity or `alpha notin D`, then `|Bad| <= 1`.

2. **Non-global monic-rank defect.** Otherwise the defective slope set

   ```text
   Z_def = { z in F : rank A_z <= 1 }
   ```

   has size at most two. Every bad slope outside `Z_def` lies in the regular
   branch `rank A_z=2`, and at each such fixed slope the number of landing
   complements is at most

   ```text
   binom(|D|,j-2).
   ```

   Thus all bad slopes outside the two exceptional defective slopes come from
   the non-global determinant incidence problem: squarefree `D`-split monic
   locators whose projective gate of Corollary 4 is noncontained and whose
   induced slope has `rank A_z=2`.

If in addition `D=H` is a multiplicative subgroup and the complement is
quotient-periodic, the quotient part of this ledger is exactly the sparse
pullback/decimated determinant branch of Corollary 6. Hence, after quotient
cores are budgeted separately, the remaining `t=2` F1 obstruction is the
aperiodic non-global determinant incidence branch in the reduced space of
Corollary 7.

## Proof

If `rank A_z <= 1` identically, Corollary 15 gives the fixed rational-normal
readout and the displayed slope counts.

Otherwise at least one `2 x 2` minor of `A_z` is a nonzero quadratic
polynomial in `z`. All slopes with `rank A_z <= 1` are roots of this one
quadratic, so `|Z_def| <= 2`. For `z notin Z_def`, Corollary 14 applies and
gives the fixed-slope landing bound `binom(|D|,j-2)`. Corollary 4 identifies
the remaining regular bad slopes as the image of the noncontained determinant
gate on split locators. Corollary 6 supplies the quotient-periodic
specialization when `D` is a subgroup.

## Why This Helps F1

The naive extension-field lift is already false: genuinely `F`-valued lines
can create slopes that no `B`-valued theorem sees. The theorem here gives the
replacement target:

```text
count z in F for which a Hankel pencil
H(u)+zH(v)
has a squarefree D-split locator in its kernel,
with H(v)ell != 0.
```

For `D subset B` and `F/B` an extension, this is a basis-free statement over
the actual line field `F`. Combined with the coordinate-transfer note, it is
also the base-field multiplication-slice problem in the `e`-interleaved code.
Corollary 5 makes this compatibility exact at the syndrome-pencil level.

The remaining positive F1 theorem should therefore be an inverse-incidence
bound in the reduced space `V`: after quotient-periodic locator families and
contained/tangent cores are separated, the number of slopes whose moving
kernel meets the projected `D`-split locator variety should be polynomial in
`n` above the corrected reserve. Corollary 4 is the finite gate for that
program: first count split locators satisfying the determinant equations, then
control collisions of the resulting rational slope map `T -> z_T`.
Corollary 6 makes the quotient-periodic part explicit: it is the sparse
pullback subspace `L_A(X^M)`, and the `t=2` gate is the corresponding
decimated-syndrome quadratic. Corollary 7 separates the remaining
rank/determinant branch into a ruled linear degeneracy and a genuine quadric
incidence problem. Corollary 8 then controls the slope-collision side: except
for at most two rank-defective slopes, or the global rank-one pencil branch,
same-slope fibers are codimension-two split-locator intersections. Corollary 9
closes the first nontrivial complement size: for `j=2`, every fixed-slope
fiber is either unique, linear-sized, or one of the explicitly marked
rank-zero exceptional slopes. Corollary 10 handles the next complement size:
for `j=3`, the monic-rank-two branch is already linear-sized, so only the
monic-rank-defective slopes remain as the first genuinely new incidence
branch. Corollary 11 then identifies the global monic-rank-one branch as a
fixed-root star or empty branch, leaving only the scalar-zero slope and the
non-global exceptional slopes as special cases. Corollary 12 reduces that
fixed-root star to a contracted `j=2` fiber, with at most one additional
zero-contraction slope unless the contraction vanishes globally. Corollary 13
uses noncontainment to bound the whole fixed-root star branch by
`1+binom(|D|-1,2)` slopes, so it is polynomial and no longer part of the
aperiodic obstruction. Corollary 14 then removes the special role of `j=3`
from the regular fixed-slope analysis: for every complement size, a
monic-rank-two slope loses two roots, leaving only the two exceptional
monic-rank-defective slopes or the global defective branch as the genuine
same-slope obstruction. Corollary 15 then identifies that global defective
branch in every degree as a fixed-root star, with an explicit noncontained
slope count, so the remaining F1 obstruction is pushed back to the non-global
quadric/rank-defective incidence rather than an uncontrolled all-depth
same-slope family. Corollary 16 records this as a branch ledger: scalar-zero
slopes, non-global monic-rank-defective slopes, global fixed-root stars, and
quotient-periodic pullbacks are now explicit ledger entries. The unresolved
positive F1 estimate is therefore concentrated in one named place, the
aperiodic non-global determinant incidence branch in the reduced `t=2`
quadric.

## Verification

The companion verifier

```text
experimental/scripts/verify_f1_syndrome_pencil_normal_form.py
```

checks Theorem 2 and Corollary 3 by exhaustive enumeration over small
quadratic-extension cases. It compares the Hankel-pencil criterion against
direct interpolation on every support complement and every extension-field
slope, checks the projective gate, checks coordinate-syndrome compatibility,
and checks the quotient-periodic pullback formulas where the parameters admit
nontrivial quotient fibers. It also runs fast algebraic checks for the
`t=2` reduced quadric, including a full-rank nonzero determinant form and a
crafted ruling-degenerate zero determinant form. The quadric checks also
enumerate fixed slopes and verify the rank-defective dichotomy of
Corollary 8. In the `j=2` exhaustive cases, the verifier also checks the
fixed-slope fiber bounds of Corollary 9, and it includes constructed
rank-two, rank-one fixed-sum, rank-one star, and rank-zero `j=2` fibers so all
branches of the bound are exercised. It also includes constructed `j=3`
fixed-slope fibers for the monic-rank-two line, monic-rank-one plane,
monic-rank-defective rank-two, and rank-zero branches, plus global
monic-rank-one finite-root, outside-domain, and infinity checks for
Corollary 11. The finite-root check also verifies the contracted `j=2` star
bound of Corollary 12 and the noncontained slope-count bound of Corollary 13.
Finally, constructed `j=4` and `j=5` fixed-root fibers verify the arbitrary
`j` codimension-two bound of Corollary 14. Additional `j=4` global
monic-rank-one cases verify the fixed-root, contained-star, outside-domain,
and infinity branches of Corollary 15. Corollary 16 is the formal branch
ledger obtained by combining those audited pieces.
