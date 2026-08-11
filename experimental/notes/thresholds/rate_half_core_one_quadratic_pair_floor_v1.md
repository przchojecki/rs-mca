---
workboard_item: T
row: symbolic rate-half half-distance profile; official N=2^41, k=2^40, t=2^39
object: LINE
target_epsilon: 2^-128 context; target-free structural theorem
agreement: a=N-t=3N/4
B_star: floor(q/2^128); no payment claimed
direct_statement: the core-one scalar-quadratic u=4 profile has no actual-support pair of union rho+3; every pair has union at least rho+4
architecture: DIRECT
partition_digest: N/A
atom_or_cell: symmetric-Hankel core-one quadratic pair-union rho+3 cell
quantifier: every field and profile satisfying the exact interface below; in particular the official e=183251937963 specialization
projection_and_unit: supported affine slopes and actual error supports
claimed_bound: pair union at least rho+4; every assigned-center line obeys 4h+sum r<=rho+4
status: PROVED
impact: ROUTE_CUT
falsifier: a profile satisfying (P1)--(P4) with one rho+3 support pair, or a failure of either exact incidence contradiction
replay: python3 experimental/scripts/verify_rate_half_core_one_quadratic_pair_floor_v1.py --check
---

# Rate-half core-one quadratic pair-floor route cut

## 1. Relation to the repository frontier

The repository's half-distance LineRay compiler treats a rate-half
Reed--Solomon code through its affine syndrome Hankel pencil.  This note
cuts one exact residual profile that appears after the generic-rank and
fixed-core reductions: one fixed core row, primitive parameter degree `e`,
and scalar residual degree two at its minimum gap `u=4`.

This is a Lane-T structural route cut, not an adjacent-row payment.  It does
not bound the complete LineRay family, enter the v4 `U_Q/U_BC/U_new`
ledger, prove the base-field-normalized split-pencil census, or prove local
primitive shift-pair control.  A compiler adapter must first place a live
first-match atom in the exact profile `(P1)--(P4)` below.

The full source proof is pinned to
`AllenGrahamHart/rs-mca-prize-dag@04179c43ac45b7c53a03d2441487971da72f3069`:

```text
bidirectional localization statement
  fafe03c21890127aeef952a4e6282da6319f20a6c224d80338ce8e8529be22c8
bidirectional localization proof
  0e471cfc4abbf4d825cc73c4a3271b03c7b69ac197fbce8c1996cd078c9b719b
pair-floor statement
  09a93f1e8a2fdc283fc424b21217323d5ec8ce6c0e429086f62c1d3f50e1edcd
pair-floor proof
  a916c434e1ab321f9f731e5a62c70b670bb02964fcae4448a34f008333ac1742
```

## 2. Exact profile interface

Put

```text
N=4rho,       k=2rho,       d_min=2rho+1,
rho=3e-1,     T=rho+4=3e+3.                          (P0)
```

Let `Sigma` be a set of `T` supported affine slopes on one received line.
For each `gamma in Sigma`, let `c_gamma` be its assigned codeword center,
`S_gamma` its actual nonzero-error support, and `r_gamma` its locator
padding deficit.  The profile assumptions are:

```text
|S_gamma|=rho-r_gamma,
sum_(gamma in Sigma) r_gamma=e-6.                   (P1)
```

There is one fixed core row `s_0` in every `S_gamma`.  Every other actual
support row is light, occurs in exactly `e` of the supports, and is a root
of the specialized locator exactly when it is in the actual support.
Named padded heavy rows never occur in an actual support.                 (P2)

For every pair with

```text
|S_alpha union S_beta|=rho+3,                        (P3a)
```

put `X=S_beta\S_alpha`.  In either orientation, `|X|=r_alpha+3`, and the
complete symmetric-Hankel coefficient chain gives nonzero weights `eta_x`
and degree-at-most-`e` parameter forms `A,B` with

```text
eta_x L_X'(x) Q(-;x)=A+xB,       x in X.             (P3b)
```

Each row form has exact degree `e`, is squarefree, and its roots are
supported slopes.  The target endpoint `beta` is a root of every row form;
the source endpoint `alpha` is a root of none.                           (P3c)

Finally, the received word and every codeword pencil are affine in the
slope.  If three actual error supports have union at most `2rho`, minimum
distance puts their centers on one codeword line.  On such a line each
nonzero residual coordinate has at most one zero.                         (P4)

### Hankel origin of `(P3b)`

After moving `alpha` to parameter zero, write

```text
Q(z;X)=sum_(i=0)^e z^i Q_i(X).
```

The specialized symmetric middle Hankel matrix has kernel
`Q_min F[X]_(<=r_alpha)`.  Pairing these `r_alpha+1` kernel multiples with
the complete coefficient recurrence, including the terminal equation,
gives

```text
sum_(x in X) eta_x x^j Q_i(x)=0,
0<=j<=r_alpha,       0<=i<=e.                        (P3d)
```

Since `|X|=r_alpha+3`, this weighted Vandermonde matrix has nullity two.
Its standard basis is

```text
(1/L_X'(x))_(x in X),       (x/L_X'(x))_(x in X),
```

which is exactly `(P3b)`.  Thus `(P3)` is the explicit coefficient-chain
interface, not an arbitrary split-pencil assumption.

## 3. Bidirectional localization lemma

Assume `(P1)--(P4)` and a pair satisfying `(P3a)`.  Put

```text
X=S_beta\S_alpha,       Y=S_alpha\S_beta,
R=r_alpha+r_beta,       n=|X|+|Y|=R+6.              (L1)
```

### 3.1 Both row families have rank two

If `A,B` in one orientation were dependent, all rows on `X` would share
one squarefree set of `e` supported slopes.  Every such slope has actual
support containing `X` and `s_0`, so `(P4)` puts all its centers on the
endpoint codeword line.  Adding the source endpoint gives `e+1` selected
line slopes.

The line's joint support is `S_alpha union S_beta`.  After removing `s_0`,
it has `rho+2=3e+1` light rows.  Each is present at least `e` times on the
selected line and has global degree exactly `e`, so it is missing exactly
once.  But slope `gamma` misses `r_gamma+3` rows.  The total is at least
`3(e+1)=3e+3`, impossible.  Hence both orientations have rank two.

Let their common gcds be `G_X,G_Y`.  Every nonendpoint root of `G_X` is
center-owned by the endpoint line and therefore supports all of `Y`; the
reverse argument gives

```text
Z(G_X)=C disjoint_union {beta},
Z(G_Y)=C disjoint_union {alpha},
deg G_X=deg G_Y=g,       |C|=g-1.                   (L2)
```

### 3.2 Residual roots are disjoint and deficit free

Outside its gcd, each row form has `e-g` roots, disjoint within one
orientation.  A residual root supports `s_0` and its defining difference
row.  If its deficit were positive, those two actual intersections already
make the endpoint triple union at most `2rho`; `(P4)` would put it on the
endpoint line and turn it into a gcd root.  Thus every residual root has
deficit zero.

A root residual in both orientations would support `s_0`, one point of
`X`, and one point of `Y`.  Its triple union would again be at most
`2rho`, giving the same contradiction.  Hence all `n` residual root sets
are mutually disjoint.

Let

```text
L=C union {alpha,beta},       |L|=g+1,
W=Sigma \ (L union all residual root sets).
```

The exact slack is

```text
s=|W|=T-(g+1)-n(e-g)
       =(R+5)g-(R+3)e+2.                             (L3)
```

Every positive deficit lies in `L union W`.  This is the precise
heavy-incidence localization.

## 4. Exclusion theorem

**Theorem.**  Every profile satisfying `(P0)--(P4)` obeys

```text
|S_alpha union S_beta|>=rho+4                       (T1)
```

for all distinct supported slopes.

**Proof.**  Suppose equality `(P3a)` held and put

```text
J=(S_alpha intersect S_beta)\{s_0},
|J|=rho-R-4=3e-R-5.                                 (T2)
```

A residual slope cannot support a point of `J`: together with its unique
difference row and `s_0`, that would trigger `(P4)`.  A slack slope supports
no difference row.  It supports at most one point of `J` at deficit zero,
none at deficit one, and cannot have deficit at least two.

Every row in `J` has global degree `e`, at most `g+1` incidences on `L`,
and none on residual slopes.  If `q=e-g>=2`, its required slack incidences
would force

```text
(3e-R-5)(q-1)<=s=2e-(R+5)q+2.                       (T3)
```

The left side minus the right side is

```text
e(3q-5)+R+3>0.                                      (T4)
```

Therefore `g=e-1`, the maximum possible degree for the gcd of two
independent degree-`e` forms.

Now `|L|=e` and `s=2e-R-3`.  Put
`d_L=sum_(delta in L)r_delta`.  Exact missing-incidence counting on the
line gives `d_L<=1` and says that

```text
M_J=3e-R-6+d_L                                      (T5)
```

rows of `J` miss one line slope.  Each needs exactly one outside incidence.
Residual slopes provide none.  The total deficit `e-6`, residual deficit
zero, and the slack restrictions leave only

```text
|W_0|=s-(e-6-d_L)=e-R+3+d_L                         (T6)
```

eligible zero-deficit slack slopes, each providing at most one.  Equations
`(T5)--(T6)` force `2e<=9`, contradiction.  This proves `(T1)`.  QED.

## 5. Center-line and expansion consequences

If one codeword line contains assigned centers at `h>=2` slopes, its joint
support contains a pair union of size at least `rho+4`.  Counting nonzero
linear coordinates gives

```text
(h-1)(rho+4)<=h rho-sum r_gamma,
4h+sum r_gamma<=rho+4.                               (C1)
```

Consequently, for every fixed pair, at least

```text
rho+4-floor((rho+4-r_alpha-r_beta)/4)
=ceil((3rho+12+r_alpha+r_beta)/4)                    (C2)
```

other supported slopes have full-locator triple union at least `2rho+1`.
At equality in `(T1)`, `(P3d)` gives coefficient-row rank at most three.
That rank-three boundary is the next profile-level target.

## 6. Official specialization

For the full rate-half prize row,

```text
N=2^41,
rho=t=2^39=549755813888,
e=(rho+1)/3=183251937963,
T=rho+4=549755813892.                                (O1)
```

The terminal contradiction has gap

```text
2e-9=366503875917.                                   (O2)
```

No large computation is involved; the verifier replays all symbolic
identities, endpoint ranges, and official integers.

## 7. Nonclaims and next adapter

This packet does not prove that every active BC/SP cell has `(P1)--(P4)`.
It does not change any v4 atom value or row ledger and does not move a
leaderboard score.  Its reusable statement is:

```text
symmetric core-one quadratic u=4 profile
  + exact bidirectional coefficient chain
  => pair union rho+3 is empty.
```

The maximal next integration step is to identify the precise first-match
owner that produces this profile, preserve its actual-support and deficit
semantics through the adapter, and then delete its `rho+3` cell.  The
remaining local geometry starts at the rank-three `rho+4` boundary.
