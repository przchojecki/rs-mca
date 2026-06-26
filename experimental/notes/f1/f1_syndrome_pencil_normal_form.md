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
incidence problem.

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
crafted ruling-degenerate zero determinant form.
