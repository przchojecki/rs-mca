# M1 Beta-Pushforward Spectral Audit

**Status:** EXPERIMENTAL / FINITE SPECTRAL AUDIT.

This note records a counterexample-first finite check of the remaining
`(BETA_2)` input in `m1_kummer_weil_import_contract.md`.  It does not prove the
bounded-conductor estimate.  It tests the exact quotient-character object that
would fail if the good beta pushforward had a hidden geometrically constant
piece, a beta-line Kummer-isotypic obstruction, or a two-dimensional coherent
component.

## Object Tested

For a quotient order `e | p-1`, let `Phi_e` be the quotient characters and let
`phi != 1`.  On the good beta cover from
`m1_depth_two_line_conic_resonance_reduction.md`, define

```text
G_{psi,phi}
  = sum_{(a,r) in G}
      psi(a) chi(rM(a,r)) (phi(beta_1)+phi(beta_2)),
```

with zero contribution on nonsplit fibers.  The `(BETA_2)` import asks for

```text
|G_{psi,phi}| <= C_beta(e) p
```

with `C_beta(e)` independent of `p`.  A counterexample search should therefore
look for `|G_{psi,phi}|` growing on the order of `p^2`, or even for rapidly
growing `|G_{psi,phi}|/p` across exact finite rows.

The full pointwise `(BETA_2)` estimate allows `psi=1` and `phi != 1`.
The M1 quotient-conic ledger also admits a weaker averaged target which uses
only the genuinely two-sided block `psi != 1`, `phi != 1`.  It is enough to
prove

```text
||G_e^circ||_F <= C_beta^avg(e) p,
```

where `G_e` is the quotient-label matrix of the good pushforward and
`G_e^circ` is its row/column-centered part.  The pointwise `(BETA_2)` estimate
implies this averaged estimate, but the averaged estimate alone already gives
`P_e=O_e(p^2)` and `M_e^o=O_e(p^2)` after adding the explicit bad-ledger
constant.  Thus the finite audit reports both the largest individual
coefficient and the centered Frobenius norm.

## Finite Scan

The verifier now scans every centered quotient-character pair in the existing
audited ratio-surface cases and reports three normalized maxima plus the
row/column-centered Frobenius norm of the exact good-pushforward quotient
matrix:

```text
(p, e, good_points, lower_points, exceptional_points,
 max_bad_two_sided/p, max_good_two_sided/p, max_good_beta2/p,
 max_good_left_principal/p, good_centered_frobenius/p,
 max_total_two_sided/p)

(17,  8,   98, 27,  70, 2.7058823529, 1.1361004999,
 1.1361004999, 1.0588235294, 0.4744784060, 3.7647058824)
(17, 16,   98, 27,  70, 2.7058823529, 1.5728968500,
 1.5728968500, 1.0588235294, 0.4632352941, 3.8054236055)
(31,  6,  486, 55, 164, 2.1612903226, 2.3225806452,
 2.3225806452, 2.2580645161, 0.6634504452, 4.4838709677)
(31, 10,  486, 55, 164, 2.3436282530, 1.8416183853,
 3.1043892896, 3.1043892896, 0.5965213065, 3.9213647064)
(43,  6, 1568, 79, 270, 2.8139534884, 3.0697674419,
 3.2558139535, 3.2558139535, 1.1366043634, 4.8139534884)
(43, 14, 1568, 79, 270, 2.4536425998, 2.5116279070,
 4.1755606367, 4.1755606367, 0.8267620588, 4.7441860465)
```

Here `max_good_beta2/p` is the direct finite proxy for the full pointwise
`(BETA_2)` statement.  In several rows this maximum is attained in the
left-principal block `psi=1`, so `max_good_two_sided/p` is the correct proxy
only for the centered two-sided block consumed by `(BETA_2^avg)`.  The bad
and total columns check the already proved two-sided ledger around it: the
bad pieces stay within the explicit `p+19(p-1)` bound, and the full singular
trace is the sum of the good pushforward and those controlled bad pieces.
The `good_centered_frobenius/p` column is the averaged version of the same
two-sided test: the verifier checks the exact Parseval identity

```text
||G_e^circ||_F^2
  = e^{-2} sum_{psi,phi != 1} |G_{psi,phi}|^2,
```

where `G_e^circ` is the row/column-centered quotient matrix of the good
pushforward.  This is the same Fourier normalization used by the surrounding
singular-excess matrix ledger.

## Averaged Pair-Correlation Form

The averaged target also has an exact collision-energy form.  Let
`x=(a_x,beta_x,r_x)` run over the good beta cover and put
`epsilon(x)=chi(d_UV(x))`.  Define the centered quotient kernel

```text
kappa_e(x,y) = 1_{xK_e = yK_e} - 1/e.
```

Then

```text
||G_e^circ||_F^2
  = sum_{x,y in Y_G(F_p)} epsilon(x) epsilon(y)
      kappa_e(a_x,a_y) kappa_e(beta_x,beta_y).        (PAIR_2)
```

Thus `(BETA_2^avg)` is equivalent to an `O_e(p^2)` bound for this signed
two-quotient pair correlation.  This is not a termwise-positive estimate;
it is nonnegative only after the full summation, because it is the squared
norm of the centered quotient matrix.  The standalone verifier checks this
identity in grouped form, in addition to the Fourier Parseval identity.

## One-Sided Marginal Split

The left-principal block in the full `(BETA_2)` audit is exactly the
beta-column marginal of the good quotient matrix.  Let

```text
c_j = sum_i (G_e)_{i,j},        c_j^circ = c_j - e^{-1} sum_l c_l,
R_e = G_e - row averages.
```

Then the Fourier basis gives the orthogonal identities

```text
e^{-2} sum_{psi any, phi != 1} |G_{psi,phi}|^2 = ||R_e||_F^2,

e^{-2} sum_{phi != 1} |G_{1,phi}|^2
  = e^{-1} sum_j |c_j^circ|^2,

||R_e||_F^2
  = ||G_e^circ||_F^2 + e^{-1} sum_j |c_j^circ|^2.
```

Equivalently, using the same kernel `kappa_e` as above, the one-sided
marginal energy is

```text
e^{-1} sum_{x,y in Y_G(F_p)}
  epsilon(x) epsilon(y) kappa_e(beta_x,beta_y).
```

Thus a full averaged pointwise theorem with `psi` allowed to be principal
splits cleanly into the M1-centered target `(BETA_2^avg)` plus a beta-marginal
bound.  The quotient-conic M1 ledger consumes only the first summand, while a
future full `(BETA_2)` proof must also control the marginal.

## Fiber-Product Component Ledger

The centered pair-correlation can be expanded into four signed quotient-fiber
product counts.  Put

```text
r_i = sum_j (G_e)_{i,j},        c_j = sum_i (G_e)_{i,j},
T = sum_{i,j} (G_e)_{i,j}.
```

Define

```text
C_ab = sum_{i,j} (G_e)_{i,j}^2,
C_a  = sum_i r_i^2,
C_b  = sum_j c_j^2,
C_0  = T^2.
```

Equivalently, `C_ab` is the signed count of pairs of good beta-cover points
whose `a`-labels and `beta`-labels both agree modulo `K_e`; `C_a` and `C_b`
drop one of those two quotient equalities; `C_0` drops both.  Then

```text
||G_e^circ||_F^2 = C_ab - e^{-1}C_a - e^{-1}C_b + e^{-2}C_0,

e^{-1}||c^circ||_2^2 = e^{-1}C_b - e^{-2}C_0,

||R_e||_F^2 = C_ab - e^{-1}C_a.
```

Thus a direct proof of `(BETA_2^avg)` may be phrased as an `O_e(p^2)` bound
for this signed four-term fiber product.  The standalone verifier now checks
these component identities exactly from the quotient matrix.

There is also a useful nonnegative sufficient target.  Since `C_a` and `C_b`
enter with negative signs,

```text
||G_e^circ||_F^2 <= C_ab + e^{-2} C_0.
```

Consequently `(BETA_2^avg)` follows from the two estimates

```text
C_ab = O_e(p^2),        |T| = O_e(p).
```

This route does not ask for cancellation in the row- or column-marginal
subtractions.  It isolates two positive targets: joint quotient-collision
energy for the good beta cover, and the principal total trace.

## Principal Total Trace Reduction

The principal total trace in this nonnegative route is elementary.  It is

```text
T = sum_{i,j} (G_e)_{i,j},
```

which is independent of the quotient order `e`.  For a good base point
`(a,r)`, the two beta roots, when they are rational, have the same `U V`
squareclass.  The squareclass identities checked in
`m1_depth_two_line_conic_resonance_reduction.md` give

```text
chi(d_UV(a,beta_l,r)) = chi(rM(a,r)) = chi(aH(a,r))
```

on split good fibers.  Since `D_beta=a r M H`, the nonsplit good fibers have
`chi(rM)=-chi(aH)` and contribute no rational beta roots.  Thus, with an empty
root sum on nonsplit fibers,

```text
T = sum_{(a,r) in G} (chi(rM(a,r)) + chi(aH(a,r))).          (TRACE)
```

Now extend the two sums in `(TRACE)` from the good base `G` to the full torus
`(F_p^*)^2`.  For fixed `r`, `rM(a,r)` is a quadratic polynomial in `a`; for
fixed `a`, `aH(a,r)` is a quadratic polynomial in `r`.  Except for the roots
of fixed discriminant polynomials, each one-variable quadratic-character sum
is constant, and the exceptional parameters are finite in number.  Hence both
full-torus traces are `O(p)`.

More precisely, the discriminants are

```text
disc_a M = 16(r-1)^2(r^2+r+1),
disc_r H = 32(a-1)^2(a+2)(2a+1).
```

The quadratic-character sums over the full torus are therefore explicit:

```text
sum_{a,r in F_p^*} chi(rM(a,r)) = p + 2 chi(-3),
sum_{a,r in F_p^*} chi(aH(a,r)) = p + 2.
```

The standalone verifier checks these exact formulas on every expanded prime
row before applying the deleted-boundary correction below.

The difference between the good base and the full torus is contained in the
fixed-degree boundary

```text
A_beta=0,        C_beta=0,        D_beta=0,
a=r,             K_alpha(a,r)=0,
```

where `D_beta=0` is the union of the two branch curves `M=0` and `H=0` on the
torus.  This boundary has `O(p)` rational points, and each deleted point
changes `(TRACE)` by at most `2`.  Therefore

```text
|T| = O(p),        C_0 = T^2 = O(p^2).
```

Thus the nonnegative sufficient route has only one remaining positive target:
the joint quotient-collision estimate `C_ab=O_e(p^2)`.

## Joint-Energy Fourier Blocks

The remaining positive target `C_ab` also decomposes orthogonally into its
Fourier blocks.  With

```text
r_i = sum_j (G_e)_{i,j},        c_j = sum_i (G_e)_{i,j},
T = sum_{i,j} (G_e)_{i,j},
r_i^circ = r_i - T/e,           c_j^circ = c_j - T/e,
```

one has the exact identity

```text
C_ab = ||G_e^circ||_F^2
       + e^{-1} sum_i (r_i^circ)^2
       + e^{-1} sum_j (c_j^circ)^2
       + e^{-2} T^2.
```

Equivalently, this is Parseval split into the four character blocks

```text
psi != 1, phi != 1;     psi != 1, phi = 1;
psi = 1,  phi != 1;     psi = 1,  phi = 1.
```

The last block is controlled by the principal trace reduction above.  Thus a
proof of the nonnegative `C_ab=O_e(p^2)` route now amounts to proving p-scale
energy for the centered block and the two one-sided marginals.  The centered
block is the actual `(BETA_2^avg)` target consumed by M1; the two marginal
blocks are extra one-sided estimates needed only if one chooses to prove the
stronger positive joint-collision target.  The next two sections reduce those
two marginal blocks to one-parameter trace estimates; the centered block
remains the only genuinely two-sided M1 target.

## Alpha Marginal Reduction

One of the two one-sided marginal blocks also has a simpler descended form.
For a nonprincipal quotient character `psi`, the alpha-marginal coefficient is

```text
A_psi = sum_j sum_i (G_e)_{i,j} psi(i).
```

The same squareclass calculation used for the principal trace gives

```text
A_psi
  = sum_{(a,r) in G} psi(a) (chi(rM(a,r)) + chi(aH(a,r))).    (ALPHA)
```

Extending `(ALPHA)` to the full torus separates a completely explicit
`H`-part from one remaining rank-one torus trace.  For fixed `a`,
`aH(a,r)` is a quadratic polynomial in `r` with discriminant

```text
32(a-1)^2(a+2)(2a+1).
```

Therefore, for every nonprincipal `psi`,

```text
sum_{a,r in F_p^*} psi(a) chi(aH(a,r))
  = p(1 + psi(-2) + psi(-1/2)).
```

The deleted good-base boundary is the same fixed union of curves as in the
principal trace section, so it contributes `O_e(p)` to every fixed quotient
character.  Hence the alpha marginal is reduced to the single full-torus
rank-one Kummer trace

```text
M_psi^tor = sum_{a,r in F_p^*} psi(a) chi(rM(a,r)).
```

This remaining middle trace is a one-dimensional elliptic trace problem, not
a rank-two beta-pushforward problem.  For fixed `a`,

```text
rM(a,r) = r(4ar^2 + (-3a^2-2a-3)r + 4a),
disc_r(rM) = 48a^2(a-1)^2(a+3)(3a+1).
```

Thus over the torus the only singular parameters are

```text
a = 1,        a = -3,        a = -1/3.
```

For nonsingular `a`, the curve `y^2=rM(a,r)` is an elliptic curve.  Its
finite nonzero branch roots have product `1`; writing them as `rho` and
`rho^{-1}`, one has

```text
rho + rho^{-1} = (3a^2+2a+3)/(4a),
```

so the cross-ratio of the four branch points varies nontrivially with `a`.
Consequently `M_psi^tor` is the Mellin transform of a fixed-conductor
non-isotrivial elliptic trace sheaf on
`P^1 - {0,1,-3,-1/3,infinity}`.  The standard curve Weil bound for this
middle-extension sheaf gives `M_psi^tor=O_e(p)` for fixed quotient order.
Therefore the alpha marginal is p-scale.  The beta marginal is reduced below
to a separate one-parameter trace over the beta line.  After these two
marginal reductions, the centered rank-two block is the minimal M1 target
left by the quotient-conic ledger.

The standalone verifier checks the identity `(ALPHA)`, the exact full-torus
`H` formula, the boundary correction, the cubic discriminant ledger, the
three singular parameters above, and the fiberwise Hasse bound on every
expanded prime row.

## Beta Marginal One-Parameter Reduction

The opposite one-sided marginal is the full `(BETA_2)` row with `psi=1`.
For a nonprincipal quotient character `phi`, it is

```text
B_phi = sum_i sum_j (G_e)_{i,j} phi(j).
```

Equivalently, define the exact beta-column trace

```text
tau_p(b) =
  sum_{(a,r) in G, Delta_b(a,r)=0}
    chi(d_UV(a,b,r)).
```

Then

```text
B_phi = sum_{b in F_p^*} phi(b) tau_p(b).
```

On the open good locus, the squareclass identities rewrite
`chi(d_UV(a,b,r))` as `chi(rM(a,r))`.  After adding or deleting only the
fixed good-base boundary, the beta-column model is therefore a Mellin
transform over the beta coordinate of the torus surface

```text
Delta_b(a,r) = 0,
```

where, as a cubic in `a` for fixed `(b,r)`,

```text
Delta_b(a,r)
 = -2r^2 a^3
   + r(3b^2 - br - b + 3r^2 - r + 3)a^2
   + (-3b^2r^2 + b^2r - 3b^2 + br^2 + br - 3r^2)a
   + 2b^2r.
```

Thus the beta marginal is not another alpha-style elliptic trace, but it does
form a bounded one-parameter family: `Delta_b` has bidegree `(3,3)` on
`P^1_a x P^1_r`, and the Kummer factor `chi(rM(a,r))` has bounded divisor on
these fibers.

The singular beta-values of this family are confined to a fixed finite
support.  Let

```text
Q16(b) =
  6561b^16 + 8019b^15 - 4860b^14 - 29727b^13
  + 4023b^12 + 57528b^11 + 54777b^10 - 73453b^9
  - 139136b^8 - 73453b^7 + 54777b^6 + 57528b^5
  + 4023b^4 - 29727b^3 - 4860b^2 + 8019b + 6561.
```

Eliminating `a` and `r` from `Delta_b=partial_a Delta_b=partial_r Delta_b=0`
gives the reduced support

```text
b(b-1)(b^2+b+1)(9b^2+14b+9)
  (9b^4-6b^3-5b^2-6b+9)Q16(b) = 0,
```

with beta infinity handled by the compactification.  More explicitly, if

```text
D_a = Res_a(Delta_b, partial_a Delta_b)/(2r^4),
E_a = Res_a(Delta_b, partial_r Delta_b)/(36b^2r^2(r-b)(r-1)),
```

then

```text
Res_r(D_a,E_a)
 = 5^8 b^12(b-1)^24(b^2+b+1)^2(9b^2+14b+9)^2
   (9b^4-6b^3-5b^2-6b+9)^4 Q16(b)^2.
```

The removed special lines `r=b` and `r=1` have no extra generic common
component; their three-way singular resultants add only the already displayed
`b=1` case.  The standalone verifier checks, on every expanded prime row,
that every torus singular fiber lies in the displayed support.  The largest
support count in the audit is `9` beta-values.

The displayed finite support is compatible with the inversion quotient.  On
`G_m`, every nontrivial support factor is reciprocal, and the degree-16 factor
descends by

```text
Q16(b) = b^8 Q8(b+b^{-1}),
Q8(z)=6561z^8+8019z^7-57348z^6-85860z^5+164403z^4
      +318429z^3-110031z^2-450805z-217802.
```

Set-theoretically, after `z=b+b^{-1}` the finite bad quotient support is
contained in

```text
(z-2)(z+1)(9z+14)(9z^2-6z-23)Q8(z)=0.
```

The factor `b-1` gives the fixed quotient point `z=2`, while `b=0` and
`b=infinity` map to the quotient point at infinity.  The standalone verifier
checks that the beta support is inversion-stable and that its image in the
`G_m/<b~b^{-1}>` quotient is exactly the root set of this degree-13 polynomial
restricted to the actual quotient image.  In the expanded rows the largest
visible finite quotient support has only `5` z-values, while the full
polynomial root set in `F_p` has at most `6` roots in the same rows.

Thus the beta marginal is a fixed-conductor beta-column family.  On the
regular beta-line complement, the family has bounded bidegree and bounded
Kummer divisor.  The finite singular support has `O(1)` fibers, each of size
`O(p)`.  The remaining issue is the usual one-variable top-cohomology
obstruction: after tensoring by `phi(b)`, the beta-line sheaf must have no
geometrically constant summand.  Equivalently, before tensoring it should
have no `phi^{-1}` Kummer-isotypic summand on `G_m`.  Under this standard
no-Kummer-isotypic input, the one-variable middle-extension trace bound gives

```text
B_phi = O_e(p)
```

for every fixed quotient order `e` and every nonprincipal `phi` of
`F_p^*/K_e`.  This reduces the beta marginal to a standard one-parameter
Kummer-isotypy check; it is not the centered rank-two `(BETA_2^avg)` target
itself.

The same beta-line viewpoint localizes every full `(BETA_2)` coefficient.
For a quotient character `psi`, put

```text
tau_{psi,p}(b) =
  sum_{(a,r) in G, Delta_b(a,r)=0}
    psi(a) chi(d_UV(a,b,r)).
```

Then

```text
G_{psi,phi} = sum_{b in F_p^*} phi(b) tau_{psi,p}(b).
```

Equivalently, after grouping beta labels modulo `K_e`,

```text
g_{psi,j} = sum_i psi(i)(G_e)_{i,j},
G_{psi,phi} = sum_j phi(j) g_{psi,j}.
```

Thus the remaining centered block is exactly the
`psi != 1, phi != 1` Kummer-isotypic spectrum of these beta-line trace
families.  A full pointwise `(BETA_2)` proof would follow from showing that,
for every quotient character `psi`, the corresponding beta-line pushforward
has no `phi^{-1}` Kummer constituent for `phi != 1`, with conductor bounded
only in terms of `e`.  The standalone verifier checks the grouped
beta-line identity for all quotient-character blocks on every expanded row.

## Inversion Symmetry

The beta-line trace family has an exact involution which cuts the independent
Kummer-isotypy checks in half.  On the torus set

```text
I(a,b,r) = (a^{-1}, b^{-1}, r^{-1}).
```

For the beta equation `Delta(a,b,r)=0` and the good-base factors, direct
expansion gives

```text
a^3 b^2 r^3 Delta(I(a,b,r)) = -Delta(a,b,r),
a^2 r^2 M(I(a,r)) = M(a,r),
a^2 r^2 H(I(a,r)) = H(a,r),
a^2 r^2 K_alpha(I(a,r)) = K_alpha(a,r).
```

Moreover `a-r`, `A_beta`, and `C_beta` are exchanged up to torus units, and

```text
a^2 b^2 r^4 d_UV(I(a,b,r)) = d_UV(a,b,r).
```

Thus `I` preserves the good beta cover and the quadratic sign.  It sends the
rank-one summand `psi(a)phi(b)chi(d_UV)` to
`psi^{-1}(a)phi^{-1}(b)chi(d_UV)`.  Consequently

```text
tau_{psi,p}(b) = tau_{psi^{-1},p}(b^{-1}),
G_{psi,phi} = G_{psi^{-1},phi^{-1}},
(G_e)_{i,j} = (G_e)_{-i,-j}.
```

For the beta marginal, this specializes to `tau_p(b)=tau_p(b^{-1})`.  The
symmetry does not prove the no-Kummer-summand input: a Kummer constituent
could still occur in an inverse pair.  It is nevertheless a structural
constraint on any route-killing obstruction and on any eventual monodromy
proof.  The standalone verifier checks good-locus preservation, inverse-root
pairing, sign preservation, the exact quotient-matrix symmetry, and the
induced grouped beta-line coefficient identity on every expanded row.

For the beta marginal, the same involution gives a one-dimensional quotient
form.  Put

```text
z = b + b^{-1},        bar_tau_p(z) = tau_p(b).
```

This is well-defined because `tau_p(b)=tau_p(b^{-1})`.  For any nonprincipal
right character `phi`, define the Chebyshev kernel

```text
C_phi(z) = sum_{b in F_p^*: b+b^{-1}=z} phi(b).
```

Then the beta marginal coefficient is exactly

```text
B_phi = sum_z bar_tau_p(z) C_phi(z).
```

The kernel itself has exact p-scale orthogonality.  For nonprincipal `phi`,

```text
sum_z |C_phi(z)|^2 =
  p - 3,        if phi^2 != 1,
  2p - 4,       if phi is quadratic.
```

Also `|C_phi(z)| <= 2` pointwise.  Hence this quotient reduction introduces
no hidden growth in the test kernel; the remaining beta-marginal issue is the
correlation of the descended trace `bar_tau_p` with these explicit
Chebyshev/Kummer kernels.

Thus the one-sided beta marginal is not an arbitrary Kummer Mellin transform
on `G_m`: trace-theoretically it factors through the inversion quotient of
the beta line and is paired with the rank-two Chebyshev/Kummer kernel
`C_phi`.  This still does not prove square-root cancellation, but it
rephrases the remaining one-sided Kummer obstruction as a dihedral quotient
problem on the `z`-line.  The standalone verifier checks the quotient-orbit
trace identity and this Chebyshev-kernel formula on every expanded row.

For nonprincipal `psi`, the beta-line family does not descend as a scalar
trace on the `z`-line.  Instead, the pair `(psi,psi^{-1})` descends as a
two-component dihedral trace.  If an inversion orbit has two points
`{b,b^{-1}}`, then

```text
tau_{psi,p}(b^{-1}) = tau_{psi^{-1},p}(b),
```

and its contribution to `G_{psi,phi}` is

```text
phi(b) tau_{psi,p}(b) + phi(b)^{-1} tau_{psi^{-1},p}(b).
```

The two fixed beta orbits `b=1,-1` contribute the single scalar term
`phi(b)tau_{psi,p}(b)`.  Hence the centered beta-line block can also be
viewed on the inversion quotient, but with a two-component dihedral trace
instead of the scalar marginal trace.  The standalone verifier computes
`tau_{psi,p}(b)` at the individual beta level, checks
`tau_{psi,p}(b^{-1})=tau_{psi^{-1},p}(b)`, checks that grouping by quotient
labels recovers the matrix `G_e`, and checks this dihedral formula for every
left/right quotient-character block on every expanded row.

There is also an exact beta-sheet quotient-energy ledger before any
`alpha,r` cancellation is used.  On a good split base fiber with beta roots
`beta_1,beta_2`, quotient-character orthogonality gives

```text
sum_{phi in Phi_e, phi != 1} |phi(beta_1)+phi(beta_2)|^2
  = 2e - 4 + 2e 1_{beta_1/beta_2 in K_e}.
```

Thus, if `N_split` is the number of good split base fibers and `N_K` is the
number whose beta-root ratio lies in the quotient kernel `K_e`, then the
raw beta-sheet right-character energy is

```text
E_e^sheet = (2e-4)N_split + 2e N_K.
```

The fixed-ratio resonance equation

```text
lambda B_beta^2 = A_beta C_beta(1+lambda)^2
```

has bidegree at most `(4,4)` on the torus after removing the irrelevant
`ar` factor, with the `lambda=-1` case contained in two lines.  Hence each
oriented fixed beta-root ratio contributes at most `4(p-1)` split good base
fibers, so

```text
N_K <= 4(p-1)|K_e|,        E_e^sheet = O_e(p^2).
```

The standalone verifier checks the resonance identity for both root-ratio
orientations, the exact orthogonality formula above, and this quotient-kernel
collision bound on every expanded row.  The largest expanded-row value is
`E_e^sheet/(p-1)^2 = 26.1241426612` at `(p,e)=(109,27)`, and the largest
actual split fixed-ratio count is `114`, far below the bound `4(p-1)`.  This
does not prove the beta-line Kummer-isotypy theorem, but it rules out a
separate oversized right-character kernel on the two beta sheets; the
remaining obstruction is the coherent base trace, not sheet multiplicity.

## Interpretation

The scan finds no hidden `p^2` component in the tested quotient rows.  The good
pushforward coefficients are p-scale in every audited case.  In the broad
six-row scan, the largest full `(BETA_2)` coefficient ratio is
`4.1755606367` at `(p,e)=(43,14)`, while the largest two-sided coefficient
ratio is `3.0697674419` and the largest centered-Frobenius ratio is
`1.1366043634`, both at `(p,e)=(43,6)`.

The standalone verifier expands the scan to 20 rows through `p=127`, without
adding those larger rows to the broad line-conic verifier.  In the expanded
audit the largest full `(BETA_2)` coefficient ratio is

```text
max_{psi any, phi != 1} |G_{psi,phi}|/p
  = 5.6717827398 at (p,e)=(109,12),
```

the largest two-sided coefficient ratio is

```text
max_{psi != 1, phi != 1} |G_{psi,phi}|/p
  = 4.8036624425 at (p,e)=(127,14),
```

while the largest centered-Frobenius ratio is still

```text
||G_e^circ||_F/p = 1.1366043634 at (p,e)=(43,6).
```

The marginal split gives the additional expanded-row maxima

```text
e^{-1/2} ||r^circ||_2 / p = 0.9002934041 at (p,e)=(43,6),
e^{-1/2} ||c^circ||_2 / p = 1.2278896782 at (p,e)=(109,12),
||R_e||_F / p             = 1.6565244248 at (p,e)=(109,12).
```

The largest raw joint-collision component in the expanded rows is

```text
C_ab/p^2 = 3.4704149482 at (p,e)=(109,12).
```

The largest finite value of the nonnegative sufficient bound is

```text
sqrt(C_ab + e^{-2}C_0)/p = 1.8842592703 at (p,e)=(109,12).
```

The principal-trace audit checks the exact identity `(TRACE)` on the expanded
prime rows.  The largest audited value is

```text
|T|/p = 3.9527559055 at p=127.
```

The alpha-marginal reduction gives the additional coefficient maxima

```text
max_{psi != 1} |A_psi|/p = 4.6632993198 at (p,e)=(61,20),
max_{psi != 1} |M_psi^tor|/p = 2.8331969382 at (p,e)=(73,8).
```

The largest audited elliptic-fiber trace in the alpha-middle family is

```text
max_a |sum_r chi(rM(a,r))|/sqrt(p) = 1.8299828440 at p=43.
```

The beta-fiber singular-support audit gives

```text
max_beta_support_count = 9 at p=43,73,97.
```

The exact beta-column trace audit also checks

```text
B_phi = sum_{b in F_p^*} phi(b) tau_p(b)
```

against the left-principal quotient coefficients.  In the expanded rows, the
largest regular beta-fiber trace outside the fixed singular support is

```text
max_regular |tau_p(b)|/sqrt(p) = 2.8736848324 at p=31, b=30,
```

while the largest support-fiber trace is

```text
max_support |tau_p(b)|/p = 1.9527559055 at p=127, b=1.
```

The grouped beta-line audit further checks

```text
G_{psi,phi} = sum_j phi(j) sum_i psi(i)(G_e)_{i,j}
```

for all quotient-character blocks, with zero formula error in the printed
rows up to floating tolerance.  The inversion-symmetry audit also checks
`G_{psi,phi}=G_{psi^{-1},phi^{-1}}` on the same rows.  Thus the finite
spectral scan is now testing exactly the beta-line Kummer-isotypic obstruction
described above.

The beta-marginal Chebyshev quotient audit checks the further identity

```text
B_phi = sum_z bar_tau_p(z) C_phi(z)
```

on the same rows.  The quotient has `(p+1)/2` points: two fixed orbits
`b=1,-1` and `(p-3)/2` paired orbits.  It also checks the exact kernel
second-moment formulas `p-3` and `2p-4`.

The centered beta-line dihedral audit checks the same quotient after retaining
the two-component `(psi,psi^{-1})` trace.  This is the quotient form relevant
to the actual `psi != 1, phi != 1` M1 block.

Thus the averaged M1 target remains substantially smaller than the largest
individual full pointwise coefficient and smaller than the full
right-nonprincipal RMS in the finite rows, matching the point of the
`(BETA_2^avg)` reformulation.

This is useful only as evidence and as a regression guard.  It cannot certify
`(BETA_2)`: the proof still needs a bounded-conductor/no-`phi^{-1}`-Kummer
summand argument for the beta-line pushforwards, or a direct proof of the
averaged `(BETA_2^avg)` matrix bound.  The value of the scan is that it tests
precisely that remaining analytic object, rather than a cruder two-variable
Kummer surface or the already controlled exceptional ledger.

## Verifier

Run:

```bash
python3 experimental/scripts/verify_m1_depth_two_line_conic_resonance_reduction.py
python3 experimental/scripts/verify_m1_beta_pushforward_spectral_audit.py
python3 experimental/scripts/verify_m1_beta_pushforward_spectral_audit.py --json
```

The relevant output line is
`ratio_surface_quotient_trace_reduction_checked`; its tuple entries now include
`max_good_two_sided/p`, `max_good_beta2/p`,
`max_good_left_principal/p`, and `good_centered_frobenius/p` between
`max_bad_two_sided/p` and `max_total_two_sided/p`.  The standalone
beta-pushforward verifier checks a larger fixed grid, hard-codes the audited
row values as regression data, and also checks the grouped pair-correlation
identity `(PAIR_2)`, the beta-marginal Parseval identity, and the orthogonal
decomposition `||R_e||_F^2=||G_e^circ||_F^2+e^{-1}||c^circ||_2^2`.  It also
checks the four component identities for `C_ab`, `C_a`, `C_b`, and `C_0`,
and reports the nonnegative sufficient bound `sqrt(C_ab+e^{-2}C_0)/p`.
It also checks the fixed beta-fiber singular-support ledger for the beta
marginal family, the exact beta-column Mellin identity, and the regular versus
fixed-support beta-fiber trace maxima.  Finally, it checks the grouped
beta-line identity, the inversion symmetry, and the beta-marginal Chebyshev
quotient formula and kernel second moments for every quotient-character block.
It also checks the two-component beta-line dihedral quotient formula for every
left/right quotient-character block, and the degree-13 quotient support
polynomial for the finite beta singular fibers.  Finally, it checks the
beta-sheet quotient-energy formula and fixed beta-root-ratio bound.
