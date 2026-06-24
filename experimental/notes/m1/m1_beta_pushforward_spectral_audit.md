# M1 Beta-Pushforward Spectral Audit

**Status:** EXPERIMENTAL / FINITE SPECTRAL AUDIT.

This note records a counterexample-first finite check of the remaining
`(BETA_2)` input in `m1_kummer_weil_import_contract.md`.  It does not prove the
bounded-conductor estimate.  It tests the exact quotient-character object that
would fail if the good beta pushforward had a hidden geometrically constant
piece or a two-dimensional coherent component.

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
stronger positive joint-collision target.

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

In particular, a standard fixed-conductor `M_psi^tor=O_e(p)` estimate would
prove the alpha-marginal p-scale bound.  The standalone verifier checks the
identity `(ALPHA)`, the exact full-torus `H` formula, and the boundary
correction for every expanded quotient row.

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

Thus the averaged M1 target remains substantially smaller than the largest
individual full pointwise coefficient and smaller than the full
right-nonprincipal RMS in the finite rows, matching the point of the
`(BETA_2^avg)` reformulation.

This is useful only as evidence and as a regression guard.  It cannot certify
`(BETA_2)`: the proof still needs a bounded-conductor/no-constant-summand
argument for the explicit rank-two beta pushforward, or a direct proof of the
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
