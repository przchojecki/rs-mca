# M1 Slack-Two Depth-Two Lift-Window Theorem

**Status:** PROVED / CONDITIONAL / AUDIT.

This note extracts the theorem-level content of
`m1_support_occupancy_scan.py` and
`verify_m1_slack_two_depth_two_kummer_saturation.py`. It is meant to make the
slack-two depth-two M1 contribution reviewable without reading the scanner
field list.

## Setup

Let `p` be prime and let `D subset F_p^*` be a cyclic multiplicative subgroup
of order `n`. Fix a quotient decomposition of `D` into `N` equal fibers of
size `m`, and write `K` for the fiber containing `1`. Consider the canonical
slack-two line

```text
X^(k+2) + z X^k
```

at exact support size `s=k+2`. In the depth-two frontier, write

```text
s = Lm + 4,        R = N-L.
```

The four residual points may be normalized by one of their elements and
written

```text
x {1,u,v,w},       w = -1-u-v.
```

The normalized depth-two slope factor is

```text
A(u,v) = -(u^2 + v^2 + uv + u + v + 1).
```

Multiplying the packet by `x in D` expands the nonzero slope factor by `D^2`.
Thus every active normalized shape contributes the square coset
`A(u,v)D^2`, with a possible zero slope when `A(u,v)=0`.

## Exact Lift-Window Reduction

The exact-support lift condition is purely quotient-fiber combinatorics. A
normalized shape is active if and only if the four entries

```text
1, u, v, -1-u-v
```

are distinct, lie in `D`, and touch at most `R` quotient fibers. Equivalently,
for `R < min(4,N)`, the active normalized catalog is the union over all
quotient windows `W` satisfying

```text
K subset W,        |W|=R,
```

of

```text
C_2^(2)(W) = {(u,v): 1,u,v,-1-u-v in W and distinct}.
```

Consequently the exact active depth-two slope image is

```text
{0 : A=0 occurs in the active catalog}
  union A(C_2^(2)(D;R)) D^2,
```

where `C_2^(2)(D;R)` denotes the normalized shapes touching at most `R`
quotient fibers. This proves the `R=1` kernel reduction, the `R=2`
two-fiber-window union reduction, and the general `R`-window reduction used by
the scanner.

The verifier checks the reduction on the running sample `p=97,n=48,N=6,m=8`:

```text
R=1: 18 active parameters, 6 zero parameters, 1 nonzero D^2-coset, 25 slopes.
R=2: 210 active parameters, 6 zero parameters, 4 nonzero D^2-cosets, 97 slopes.
R=3: 690 active parameters, 6 zero parameters, 4 nonzero D^2-cosets, 97 slopes.
```

Thus, in this sample, the exact-support image is sparse at `R=1` but already
saturated at `R=2`, before the all-shapes lift gate `R>=min(4,N)` applies.

## Lift-Limited Ceiling

The same quotient-window description gives the unconditional active-slope
ceiling. If a normalized shape touches `r` quotient fibers, one of those fibers
is the kernel fiber containing `1`; the other `r-1` fibers are chosen from
`N-1` fibers, and the ordered pair `(u,v)` has at most `(rm)^2` possibilities.
Therefore

```text
B_R = sum_{r=1}^{min(R,4,N)} binom(N-1,r-1) (rm)^2
```

bounds the number of ordered normalized parameters. Since every nonzero
four-point packet has exactly `24` normalizations, the active bad-slope image
satisfies

```text
|Bad_{t=2,d=2}^{active}|
  <= min(p, 1 + floor(B_R/24) |D^2|).
```

This bound is independent of the Kummer estimate. It is useful precisely when
too few quotient fibers remain for the raw saturated catalog to lift.

## Kummer Saturation Certificates

The saturation certificates are conditional on the standard two-variable
Kummer-Weil estimate with squarefree radical divisor

```text
u v (-1-u-v) A(u,v)
```

of component degrees `1,1,1,2`. The imported error constant is therefore
recorded as `(1+1+1+2-1)^2 = 16`.
The exact external dependency and its audited hypotheses are separated in
`m1_kummer_weil_import_contract.md`; the present note remains conditional on
that import.
The same contract proves elementary linear `p` bounds for the unrestricted
`d=0` Jacobi part and the unrestricted `d!=0` conic-only part with coordinate
characters principal. Because all principal characters are extended by zero
on the Kummer open set, these elementary parts also pay a genus-zero
open-set correction `6 ceil(sqrt(p))` times their L1 mass. In the additive
raw, fixed-window, and two-fiber ledgers, the contract also proves a `4p`
bound for the subcase where the conic character is quadratic and exactly one
coordinate character is nonprincipal; this elementary slice calculation is
isolated in `experimental/m1_depth_two_quadratic_one_coordinate_lemma.md`.
It also proves the nonquadratic one-coordinate `4p` bound by reducing the
fixed-coordinate conic sum to a Jacobi factor times a one-variable
discriminant Kummer sum; this is isolated in
`experimental/m1_depth_two_nonquadratic_one_coordinate_lemma.md`. The
conditional Kummer import is now charged only from two active coordinate
characters onward: two-coordinate mixed terms have degree `1+1+2` and pay
`9p`, and three-coordinate mixed terms have degree `1+1+1+2` and pay `16p`.
The two-coordinate term is further reduced in
`experimental/m1_depth_two_two_coordinate_fiber_reduction.md` to cancellation
in a one-dimensional fiber trace family plus a genus-zero line correction of
size at most `3 sqrt(p)`. Within that family, the reciprocal slice where the
two active coordinate characters are `mu` and `mu^{-1}` collapses further by
the ratio substitution `v=tu`; this is isolated in
`experimental/m1_depth_two_reciprocal_two_coordinate_lemma.md`.
The same reciprocal note applies projectively, removing the ramified slices
where one active coordinate monodromy is reciprocal to the infinity
monodromy.
The larger infinity-unramified slice `mu nu eta^2=1` also reduces to
one-dimensional genus-zero sums after the substitution `u=tv`, `r=1/v`,
giving a `2p+2 sqrt(p)` core bound plus the same line correction. This is
isolated in
`experimental/m1_depth_two_infinity_unramified_two_coordinate_lemma.md`.

For the raw normalized catalog on `D`, the verifier audits the character
expansion, the divisor nontriviality, the exact principal open-set count

```text
p^2 - 4p + 6 + 4 chi(-3),
```

and the exact six-line distinctness loss `6p-11`. With
`e=[F_p^*:D]` and `q=[F_p^*:D^2]`, the nonprincipal expansion splits into
the proved Jacobi part `e^3-1`, the proved conic-only part `q-1`, and the
proved one-coordinate mixed part `3(e-1)(q-1)`. For bookkeeping, write the
nonquadratic one-coordinate and higher-coordinate masses as:

```text
C_1 = 3(e-1)(q-2),
C_2 = 3(e-1)^2(q-1),
C_3 = (e-1)^3(q-1).
```

Let `g=q/e`, and let `C_2^0` be the exact two-coordinate L1 mass with
trivial infinity monodromy:

```text
C_2^0 =
  3 # {a,b,d : 1<=a,b<e, 1<=d<q, g(a+b)+2d == 0 mod q}.
```

Let `C_2^rec` be the exact remaining two-coordinate L1 mass where infinity
is ramified but two projective line monodromies are reciprocal:

```text
C_2^rec =
  3 # {a,b,d : 1<=a,b<e, 1<=d<q,
        g(a+b)+2d != 0 mod q,
        a+b == 0 mod e or ga+2d == 0 mod q or gb+2d == 0 mod q}.
```

The corrected equal-line diagonal conductor audit isolates one further
submass of the ramified nonreciprocal remainder:

```text
C_2^eq =
  3 # {a,d : 1<=a<e, 1<=d<q,
        3ga+2d == 0 mod q,
        2ga != 0 mod q}.
```

Here the three choices are the active coordinate pair.  The congruence
`3ga+2d=0` says that the two active line monodromies and the line at infinity
are all equal; the condition `2ga != 0` removes the order-two common
monodromy already counted in `C_2^rec`.

The verifier also reports the larger coordinate-diagonal submass

```text
C_2^diag =
  3 # {a,d : 1<=a<e, 1<=d<q,
        (ga,ga,-2ga-2d) is ramified nonreciprocal}.
```

The projective chart audit extends this further.  Let `C_2^peq` be the
ramified nonreciprocal mass where at least two of the three projective line
monodromies are equal.  Inclusion-exclusion gives

```text
C_2^peq = 3 C_2^diag - 2 C_2^eq.
```

Equivalently, let `D(e,g)=C_2^diag/3` and `E(e,g)=C_2^eq/3` be the
per-active-pair coordinate-diagonal and all-lines-equal counts. These are
closed forms. If `g=1`, then

```text
D(e,1) =
  (e-1)(e-3)                                      if e is odd,
  (e-2)(e-3) - 2(e/2-1-1_{4|e})                  if e is even,

E(e,1) =
  e - gcd(e,3)                                   if e is odd,
  2(e/2-1-1_{4|e}) - (gcd(e/2,3)-1)             if e is even.
```

If `g=2`, then

```text
D(e,2) = (e-1-1_{2|e})(2e-5),
E(e,2) = 2(e-1-1_{2|e}) - (gcd(e,3)-1).
```

Thus

```text
C_2^diag = 3D(e,g),       C_2^eq = 3E(e,g),
C_2^peq = 9D(e,g) - 6E(e,g).
```

The symmetric-coordinate reduction applies to this full projective equal-pair
mass, not only to `C_2^eq` or `C_2^diag`.  The verifier checks the
general-diagonal obstruction audit: `alpha^2=1` and `2F1` parameter
cancellation have zero mass in `C_2^diag`; the non-coordinate projective
equal-pair cases are then carried to this diagonal chart by an exact
projective open-sum identity.  The local conductor ledger has also been
promoted for the whole ramified nonreciprocal diagonal slice: `s=0`
contributes one unit because the `mu^2=1` cases are exactly the already
removed projective reciprocal diagonal terms; the two `C(s)=0` roots
contribute at most one unit each; the two `B(s)=0` roots use the corrected
`2F1` table; and infinity has the nontrivial scalar `alpha^(-2)`.

Since `g` is either `1` or `2`, the `C_2^0` and `C_2^rec` counts have closed
forms per active coordinate pair. If `g=1`, then

```text
C_2^0/3 =
  (e-1)(e-2)                  if e is odd,
  (e-1)(e-2)+1                if e is even,

C_2^rec/3 =
  3(e-1)(e-2)                 if e is odd,
  3(e-2)^2 + 2 1_{4|e}        if e is even.
```

If `g=2`, then

```text
C_2^0/3 = (e-1)(2e-3),
C_2^rec/3 = 6(e-1)(e-2) + 2 1_{2|e}.
```

The raw weighted error is therefore

```text
(e^3-1) + (q-1) + 12(e-1)
  + 4C_1 + 2C_2^0 + 4C_2^rec
  + 9(C_2-C_2^0-C_2^rec) + 16C_3.
```

If the conditional projective equal-pair conductor import is used for the full
two-coordinate open sum, the residual contributes `3p` and the Jacobi part
contributes one more `p` on `C_2^peq`.  Thus the linear part can instead
replace the last two-coordinate term by

```text
4C_2^peq + 9(C_2-C_2^0-C_2^rec-C_2^peq).
```

Equivalently, the leading L1 weight drops by `5C_2^peq`.  The corresponding
square-root mass is `3C_2^peq`: one unit from the Jacobi part and two from
the exceptional `B(s)=0` fibers.  The certificate code reports the older
equal-line and coordinate-diagonal conditional ledgers together with this
stronger projective-equal conditional ledger, but the active
`saturation_certificate` remains the conservative one until the
local-monodromy import is accepted as theorem-grade.

The exact post-reduction residual mass is therefore

```text
C_2^asym = C_2 - C_2^0 - C_2^rec - C_2^peq.
```

Writing `T(e,g)=(e-1)^2(ge-1)` for the raw two-coordinate mass per active
pair, this is the closed formula

```text
C_2^asym =
  3(T(e,g) - C_2^0/3 - C_2^rec/3 - 3D(e,g) + 2E(e,g)).
```

Every term counted by `C_2^asym` has three nonzero projective line monodromies
which are pairwise distinct and have no reciprocal pair.  Hence the
projective line-permutation action is free, and the verifier records the
integer orbit count

```text
O_2^asym =
  (T(e,g) - C_2^0/3 - C_2^rec/3 - 3D(e,g) + 2E(e,g))/2.
```

This is the exact remaining two-coordinate wall after the proved
infinity-unramified and projective-reciprocal reductions and the conditional
projective equal-pair ledger.

The next dense-edge split inside `C_2^asym` is line-conic resonance.  For
line monodromy exponents `(ell_1,ell_2,ell_infty)` and conic exponent `d`,
this is the condition

```text
ell_i + d == 0 mod q
```

for one of the three projective lines.  Inside `C_2^asym` these three
conditions are disjoint: two simultaneous line-conic resonances would force
two projective line monodromies to be equal, already removed by `C_2^peq`.
For one fixed projective line, the per-active-pair count is

```text
R(e) = (e-1)(e-5) + 3 1_{2|e} + 2(gcd(e,3)-1).
```

Indeed, after fixing `ell_1+d=0`, write the two active line exponents as
`ga` and `gb`.  The asymmetric constraints reduce to

```text
b != a,        b != -a,        b != 2a,        2b != a        mod e.
```

Inclusion-exclusion over these four forbidden relations on
`(Z/eZ)^* x (Z/eZ)^*` gives the displayed `R(e)`: the correction
`3 1_{2|e}` comes from the order-two collision, and
`2(gcd(e,3)-1)` comes from the nonzero 3-torsion collisions. The same count
holds for each of the three projective lines.

This count is independent of `g=q/e`.  Thus the total asymmetric
line-conic-resonant mass and its complement are

```text
C_2^lc = 9R(e),          C_2^anr = C_2^asym - C_2^lc.
```

The corresponding free projective-line orbit counts are `C_2^lc/6` and
`C_2^anr/6`.  Terms counted by `C_2^anr` have no line-line reciprocal or
equal pair and no line-conic reciprocal pair, so they are the clean
normal-crossing nonresonant subwall.  The active certificate remains
conservative; this split only isolates the exact next conductor target.

If the projective equal-pair import and a clean nonresonant line/conic
Kummer theorem are both accepted at `4p+3 sqrt(p)`, the two-coordinate
linear ledger after `C_2^0` and `C_2^rec` becomes

```text
4(C_2^peq + C_2^anr) + 9C_2^lc.
```

Equivalently, relative to the current conservative `9p` charge on the
ramified nonreciprocal remainder, the leading L1 weight drops by
`5(C_2^peq+C_2^anr)` and the square-root mass adds
`3(C_2^peq+C_2^anr)`. The saturation verifier reports this combined
conditional ledger, but it is not consumed by the active certificate.

The resonant slice `C_2^lc` is no longer a black-box two-variable term:
`experimental/m1_depth_two_line_conic_resonance_reduction.md` proves that
each line-conic-resonant core is a Mellin transform of a one-dimensional
quadratic-fiber trace family with candidate singular support
`{0,-1,2,3,infinity}`.  A conductor bound for that trace family would remove
the last two-coordinate mass left at the old `9p` import in the combined
conditional ledger.
The scanner now reports this stronger optional ledger as well: if the
line-conic-resonant core satisfies `|C|<=4p`, then the open-set correction
gives `4p+3 sqrt(p)` on `C_2^lc`, and the two-coordinate residual after
`C_2^0` and `C_2^rec` is charged by

```text
4(C_2^peq + C_2^anr + C_2^lc)
  = 4(C_2^peq + C_2^asym).
```

This drops the leading L1 weight by `5(C_2^peq+C_2^asym)` and adds
square-root mass `3(C_2^peq+C_2^asym)`, but remains conditional and is not
consumed by the active `saturation_certificate`.

The currently consumed square-root correction has L1 mass

```text
6J + 5C_2^0 + 3C_2^rec,        J = (e^3-1) + (q-1).
```

Here `6J` is the elementary open-set correction isolated in
`experimental/m1_depth_two_elementary_open_set_lemma.md`, while `5C_2^0`
comes from the proved infinity-unramified two-coordinate bound
`2p+5 sqrt(p)` on the Kummer open set, and `3C_2^rec` comes from the
projective reciprocal open-set bound `4p+3 sqrt(p)`. The fixed-window and
quotient-union ledgers below remain conservative and do not yet split their
two-coordinate L1 masses by projective line monodromy.

For a fixed quotient window `W` of size `R`, let

```text
h = [F_p^*:K],        e = h/N,        q = [F_p^*:D^2].
```

Here `q` is even because `D^2` is contained in the square subgroup of
`F_p^*`, so there is a unique quadratic conic character in the `D^2`-coset
expansion.

The indicator of `W` has principal coefficient `R`. For its nonprincipal
one-dimensional quotient Fourier coefficients `c_W(a)`, Parseval and
Cauchy-Schwarz give

```text
sum_{a != 0 in D/K} |c_W(a)| <= sqrt((N-1)R(N-R)).
```

After lifting from quotient characters to ambient characters modulo `K`, the
one-dimensional nonprincipal L1 is bounded by

```text
A_R = (e-1)R + e ceil(sqrt((N-1)R(N-R))).
```

In the complement-window case `R=N-1`, this is the exact value

```text
A_R = (2e-1)R,
```

because the nonprincipal quotient Fourier coefficients of a window missing
one label all have absolute value `1`.

Thus the three-coordinate window tensor has nonprincipal L1 at most
`(R+A_R)^3-R^3`, split by active coordinate count as
`3R^2 A_R`, `3R A_R^2`, and `A_R^3`. Hence the conservative lower numerator
for a fixed `D^2`-coset is obtained by putting

```text
M_{R,h,q} = ((R+A_R)^3-R^3) + R^3(q-1)
            + 12R^2 A_R(q-1)
            + 27R A_R^2(q-1)
            + 16A_R^3(q-1).
```

The elementary open-set mass in this fixed-window numerator is

```text
J_{R,h,q} = ((R+A_R)^3-R^3) + R^3(q-1).
```

It is

```text
R^3 (p^2 - 4p + 6 + 4 chi(-3))
  - p M_{R,h,q}
  - 6 ceil(sqrt(p)) J_{R,h,q}
  - (6p - 11) h^3 q.
```

The conservative uniform sufficient threshold for this fixed-window numerator
uses `ceil(sqrt(p))<=p`:

```text
p >= ceil((M_{R,h,q} + 6J_{R,h,q} + 6h^3q)/R^3) + 4.
```

When this numerator is positive, that fixed `R`-window already hits every
nonzero `D^2`-coset. If the exact-support complement has at least those `R`
remaining quotient fibers, this is an exact-support saturation certificate.

The verifier audits:

```text
R=2, p=919, n=918, N=3: positive two-fiber certificate.
R=2, p=7351, n=3675, N=3: positive fixed-window certificate.
R=3, p=2213, n=2212, N=4: positive fixed-window certificate.
```

In the second case, exact fixed-window enumeration gives `2,055,708`
parameters, `996` zero parameters, and both nonzero `D^2`-cosets, agreeing
with the certificate.

There is also a stronger certificate for the full quotient-window union. Let
`Q=D/K` have order `N`, and let

```text
T_R(N) = #{(a,b,c) in Q^3 : |{1,a,b,c}| <= R}.
```

Equivalently,

```text
T_R(N) = sum_{j=0}^{min(R-1,3,N-1)}
           binom(N-1,j)
           sum_{i=0}^j (-1)^i binom(j,i) (j+1-i)^3.
```

In particular,

```text
T_1(N)=1,        T_2(N)=7N-6,
T_3(N)=1+7(N-1)+12 binom(N-1,2),        T_4(N)=N^3.
```

Expanding the indicator of the union of all `R`-windows by quotient-kernel
characters gives principal weight `T_R(N)`. The nonprincipal coefficients are
smaller. A quotient-Fourier calculation gives the coefficient bounds

```text
C_1(N)=1,
C_2(N)=3N-6,
C_3(N)=max(6,(N-2)(N-3)).
```

The `R=2` formula follows by writing each coefficient as `zN-6`, where `z`
counts zero subset sums among the three quotient frequencies. For `R=3`, the
complement is the ordered catalog of three distinct nonidentity quotient
labels; inclusion-exclusion gives

```text
U(r)U(s)U(t) - U(r+s)U(t) - U(r+t)U(s) - U(s+t)U(r)
  + 2U(r+s+t),
```

where `U(a)=N-1` if `a=0` and `U(a)=-1` otherwise. The displayed bound is the
maximum absolute nonprincipal value of that expression.

The Kummer expansion is over ambient characters modulo `K`, not only over
characters of `D/K`. Put

```text
e = [F_p^*:D],        h = [F_p^*:K] = eN,
q = [F_p^*:D^2].
```

The `e^3` ambient character triples that restrict trivially to `D/K` still
have coefficient `T_R(N)`. All other ambient triples have coefficient bounded
by `C_R(N)`. Hence the quotient-label L1 bound is

```text
S_R <= e^3 T_R(N) + (h^3-e^3) C_R(N),
```

For `R=2`, the quotient L1 term is exact. If `z(r,s,t)` is the number of
nonempty subset sums among `r,s,t` that vanish in `D/K`, the coefficient is
`zN-6`. The distribution is:

```text
N odd:
  z=0: (N-1)(N-3)^2,    z=1: (N-1)(7N-17),
  z=2: 3N-3,            z=3: 6N-6,      z=7: 1.

N even:
  z=0: N^3-7N^2+15N-10, z=1: (N-2)(7N-10),
  z=2: 3N-6,            z=3: 6N-5,      z=7: 1.
```

Thus

```text
S_2 = e^3 sum_z count_z |zN-6|.
```

For `R=3`, the quotient L1 term is also exact. The principal coefficient is
`T_3(N)`. For odd `N`, the remaining coefficient/count pairs are

```text
-(2N-6): (N-1)(4N-5),       -(N-6): 3(N-1)(N-3),
6: N^3-7N^2+15N-9,          (N-2)(N-3): 6N-6.
```

For even `N`, they are

```text
-(3N-6): 1,                 -(2N-6): (N-2)(4N-1),
-(N-6): 3(N-2)^2,           6: N^3-7N^2+15N-10,
(N-2)(N-3): 6N-6.
```

Thus `S_3=e^3` times the resulting absolute coefficient sum. After the
`D^2`-coset expansion, the total nonprincipal coefficient L1 bound is

```text
E_R <= q S_R - T_R(N).
```

The active-coordinate parts of the quotient-window L1 also separate exactly.
Let `O_{R,j}` be the ambient L1 mass of quotient-label Fourier coefficients
with exactly `j` nonprincipal coordinate characters. For `j=1`, this is

```text
O_{R,1} = 3((e-1)T_R(N) + e sum_{a in Q^*} |c_R(a,0,0)|),
```

where `c_R` is the quotient-label Fourier coefficient. Equivalently,

```text
O_{1,1} = 3(h-1),
O_{2,1} = 3((e-1)(7N-6) + e(N-1)(3N-6)),
O_{3,1} = 3((e-1)T_3(N) + e(N-1)(N-2)(N-3)).
```

The first term in `O_{R,1}` counts ambient characters that are nontrivial on
the kernel but quotient-principal; the second counts nonprincipal quotient
characters. The verifier computes `O_{R,2}` and `O_{R,3}` by exact ambient
quotient-Fourier enumeration, and checks
`O_{R,1}+O_{R,2}+O_{R,3}=S_R-T_R(N)`.

The Jacobi/conic/Kummer split is sharper than applying the `16p` bound to all
of `E_R`: the `d=0` part has L1 at most `S_R-T_R(N)`, the conic-only
`d!=0` part has L1 at most `(q-1)T_R(N)`, and the mixed `d!=0` part has L1
at most `(q-1)(S_R-T_R(N))`, split by active coordinate count. Put

```text
W_R = (S_R-T_R(N)) + (q-1)T_R(N)
      + (q-1)(4O_{R,1} + 9O_{R,2} + 16O_{R,3}).
```

The elementary open-set mass is

```text
J_R = (S_R-T_R(N)) + (q-1)T_R(N).
```

Thus the conservative lower numerator for the whole active union is

```text
T_R(N) (p^2 - 4p + 6 + 4 chi(-3))
  - p W_R
  - 6 ceil(sqrt(p)) J_R
  - (6p - 11) h^3 q.
```

The conservative uniform sufficient threshold is

```text
p >= ceil((W_R + 6J_R + 6h^3q)/T_R(N)) + 4.
```

When this is positive and `R<min(4,N)`, the exact-support active
quotient-window catalog itself hits every nonzero `D^2`-coset. This can prove
saturation by using all active quotient labels at once. After the
complement-window refinement above, the small positive union samples are also
fixed-window certified:

```text
R=2, p=181, n=180, N=3: union and complement-window positive.
R=3, p=113, n=112, N=4: union and complement-window positive.
```

## Contribution to M1

This theorem closes a coherent low-slack subproblem: the slack-two depth-two
canonical frontier is now split into exact quotient-window lift regimes, a
lift-limited sparse regime, and Kummer-certified saturation regimes. The
quotient-window union certificate narrows the remaining lift-limited window by
using all active quotient labels at once, not only one fixed window. It does
not prove the full M1 corrected-reserve local limit. What remains is to remove
or prove the imported Kummer-Weil estimate in a standalone algebraic-geometry
argument and extend beyond this canonical depth-two frontier toward the
genuinely aperiodic residue-line packing problem.
