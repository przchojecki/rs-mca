# Positive `433-1a -> O0b` complete-source outside reduction

**Status:** proved rank/kernel and necessary-equation compilers; route open.

**Row:** KoalaBear MCA at `2^-128`.

**Direct target:** workboard item K3, positive coordinate part of the
residual order-two type with `(m,r)=(2,4)`.

**Quantifier:** every deployed-field positive complete-source packet in the
unique residual graph route `433-1a -> O0b`, separately for every common
matching cell and cycle sign.

**Projection:** exact complete-source product and squared-sum Vieta rows.

**Impact:** deletes the common base-rank-drop branch, proves a unique common
coefficient kernel on every common survivor, compiles all necessary outside
product cases, and eliminates the target variables in two oriented triangle
templates. It does not delete the route or book an MCA payment.

**Parent:** the exact positive loop cap and residual workboard at commit
`4569b506d7c86b3b7fbca5b22701ef83988e76e8`.

## 1. Route data and common matrix

Use the target sign gauge

```text
common:  -c^2; b,b,-b,c;
outside: de,-de,df,-df,sigma ef,be,cf,  sigma in {+1,-1}.       (1.1)
```

The five common source labels are two deck pairs and a singleton.  Assigning
the roles

```text
LC, AB+1, AB+2, AB-, AC
```

to that shape gives fifteen matching cells and nine orbits under exchange of
the duplicate `AB+` roles:

```text
[0] | [1,2] | [3,6] | [4,7] | [5,8] |
[9,10] | [11] | [12,13] | [14].                  (1.2)
```

Write

```text
A_2(W)=d_0+d_1W+d_2W^2,
A_0(W)=e_0+e_1W+e_2W^2,
B_1(W)=beta_0+beta_1W.                            (1.3)
```

For common label `lambda_j`, target product `p_j`, source square root `z_j`,
and target sum `s_j`, the product and sum rows in coefficient order
`(d_0,d_1,d_2,e_0,e_1,e_2,beta_0,beta_1)` are

```text
P_j=(-p_j,-p_j lambda_j,-p_j lambda_j^2,
      1,lambda_j,lambda_j^2,0,0),
Q_j=(q_j,q_j lambda_j,q_j lambda_j^2,
      0,0,0,lambda_j,lambda_j^2),  q_j=z_j s_j.   (1.4)
```

The common base consists of the five `P_j` and the loop sum row.

## 2. Global product-base rank

The five product rows have rank five on every admissible point in all
fifteen matching cells.  Therefore the loop sum row raises the common base
rank to six everywhere.  This deletes the base-rank-drop branch which was
left open by the parent packet.

Six role orbits have short exact identities. Put `R=r^2,T=t^2`.  For cells
`4,7`, define

```text
A=-RT+3R+3T-1,  B=(R+1)(T+1).
```

Two stripped maximal minors have coefficient determinant

```text
B^2-A^2=8(R-1)(T-1)(R+T).                        (2.1)
```

For cells `5,8`, put `S=R+T`, `B=(R+1)(T+1)`, and
`C=(R-1)(T-1)`.  Eliminating `b` from two stripped minors gives

```text
c[(cB+C)(cC+B)-4cS^2]=cBC(c+1)^2.                (2.2)
```

For cells `3,6`, put

```text
U=-R^2-3RT+3R+T,  V=-R^2+RT-R+T.
```

Away from the explicit linear branch, two minors have determinant

```text
U^2-V^2=8R(T-1)(R-1)(R+T),                       (2.3)
```

and the retained linear branch has another guarded nonzero minor.  Cell
`14` reduces to

```text
E_2=-cR+2cT-c-R+1,
E_5=-cR+c-R+2T-1,
cE_5-E_2=-(c^2-1)(R-1).                          (2.4)
```

Cells `0` and `11` have direct guarded nonzero minors, including the
specialized alternative at the sole linear branch in cell `0`.

For representatives `1,9,12`, let `D_0,...,D_5` be the six guard-stripped
maximal product minors and put

```text
H=RTbc(b-1)(b+1)(c-1)(c+1)(b-c)(b+c)
  (R-1)(R+1)(T-1)(T+1)(T-R)(T+R).                (2.5)
```

Exact Singular calculation over the deployed field `F_2130706433` gives

```text
<D_0,...,D_5,zH-1>=<1>                           (2.6)
```

in all three representatives.  The duplicate-role involution transports
these certificates to cells `2,10,13`.  The certificate stores the six
canonical equation digests and complete Singular-program digest for each
representative; every replay output is exactly `UNIT`, basis size `1`, first
basis element `1`.  The verifier can regenerate and rerun all three inputs
with `--full-singular-replay` when Singular is available.

Equations (2.1)--(2.6), the direct cells, and (1.2) cover all fifteen cells.
No characteristic-free rank statement is claimed.

## 3. Unique common coefficient kernel

Let `lambda_0` be the loop label and `lambda_i` any nonloop common label.
Modulo the six-dimensional base, the loop and nonloop sum-row tails have
determinant

```text
lambda_0 lambda_i(lambda_i-lambda_0),             (3.1)
```

which is nonzero on the source guards.  Thus every nonloop sum row is
nonzero in the two-dimensional quotient.  On a common Vieta survivor, the
full common matrix consequently has rank exactly seven and its coefficient
kernel is one-dimensional.

There is also an explicit division-free reconstruction.  Let `(A_2,A_0)`
be any nonzero signed-maximal-cofactor kernel of the five product rows and
put

```text
Delta_i=lambda_i(lambda_i-lambda_0),

A_2_tilde(W)=Delta_i A_2(W),
A_0_tilde(W)=Delta_i A_0(W),
B_1_tilde(W)=-q_i A_2(lambda_i)(W-lambda_0).      (3.2)
```

These forms span the unique full common kernel.  Their nonvanishing follows
from the nonzero `(A_2,A_0)` block scaled by `Delta_i`; it does not require
`A_2(lambda_i)` to be nonzero.

## 4. Exhaustive necessary outside-product ledger

Put

```text
F(W)=A_0(W)/A_2(W),
K={lambda,-lambda,mu,-mu,M},  xi=-M.              (4.1)
```

If the missing mate `xi` carries target product `x`, every actual packet
satisfies

```text
A_0(xi)-xA_2(xi)=0.                              (4.2)
```

For proposed products `y,z` assigned to one unused source deck pair, define

```text
P_y(W)=A_0(W)-yA_2(W)=p_2W^2+p_1W+p_0,
Q_z(W)=A_0(-W)-zA_2(-W)=q_2W^2+q_1W+q_0.
```

Their exact paired-product eliminant is

```text
C_F(y,z)=(p_2q_0-p_0q_2)^2
          -(p_2q_1-p_1q_2)(p_1q_0-p_0q_1)=0.    (4.3)
```

This is `Res_W(P_y,Q_z)`.  For each fixed common row and cycle sign, the
exhaustive necessary product ledger has

```text
5 internal eta choices
* 7 missing-mate product choices
* 15 perfect matchings of the residual six products
= 525 cases.                                      (4.4)
```

If a target record has squared target sum `s^2`, the complete-source sum
row is the square-root-free equation

```text
W B_1(W)^2-s^2 A_2(W)^2=0.                       (4.5)
```

At the missing mate this gives the additional scalar cut

```text
xi B_1(xi)^2-s_x^2 A_2(xi)^2=0.                 (4.6)
```

For a residual pair `(y,z)` lifted to `{kappa,-kappa}`, both product
equations and both instances of (4.5) are retained.  A bare resultant
survivor need not lift to a distinct unused source deck pair, so (4.3) is
necessary and not sufficient.

## 5. One-edge scalar compiler

For one outside product `p` and squared target sum `s^2`, write

```text
P(W)=AW^2+BW+C=A_0(W)-pA_2(W),
Q(W)=q_4W^4+q_3W^3+q_2W^2+q_1W+q_0
    =WB_1(W)^2-s^2A_2(W)^2.                      (5.1)
```

On `A!=0`, polynomial pseudo-division gives

```text
R_1=q_4(-B^3+2ABC)+q_3A(B^2-AC)-q_2A^2B+q_1A^3,
R_0=q_4(-B^2C+AC^2)+q_3ABC-q_2A^2C+q_0A^3,

A^3 Res_W(P,Q)=A R_0^2-B R_0R_1+C R_1^2.        (5.2)
```

The abstract resultant has 22 terms and total coefficient degree six.  The
degree-drop branch is not discarded: for `A=0,B!=0`, the exact cleared cut
is

```text
q_4C^4-q_3C^3B+q_2C^2B^2-q_1CB^3+q_0B^4=0.     (5.3)
```

If `A=B=0`, then `C!=0` on the guarded common products, so no product root
exists.  Applying (5.2) or (5.3) to all seven outside records is still only
a necessary relaxation because it forgets root distinctness and deck-pair
coupling.

## 6. Two target-free triangle templates

The 525-case ledger contains the following two explicitly oriented
templates with `x=F(xi)=ef`.  Let the residual source deck pairs be
`{u,-u}`, `{v,-v}`, and `{w,-w}`, and put

```text
H(W)=W B_1(W)^2/A_2(W)^2.                        (6.1)
```

### Template A

```text
(F(u),F(-u))=(de,-df),
(F(v),F(-v))=(-de,cf),
(F(w),F(-w))=(df,be).                            (6.2)
```

Eliminating `d,e,f` gives

```text
F(v)=-F(u),
F(w)=-F(-u),
F(-v)F(-w)=bcF(xi),                              (6.3)

H(u)F(xi)F(-u)+F(u)(F(-u)-F(xi))^2=0.           (6.4)
```

### Template B

```text
(F(u),F(-u))=(de,cf),
(F(v),F(-v))=(-de,df),
(F(w),F(-w))=(-df,be).                           (6.5)
```

Elimination gives

```text
F(v)=-F(u),
F(w)=-F(-v),
F(-u)F(-w)=bcF(xi),                              (6.6)

H(u)c^2F(xi)^2F(-u)^2
 -(F(u)F(-u)^2+c^2F(xi)^2)^2=0.                 (6.7)
```

After substitution of (1.3), these are division-free polynomial equations
once the displayed denominators are cleared.  They retain the three
distinct outside deck pairs and all source/common support guards.

Templates A and B are not proved to exhaust the deployed-field matching
orbits, and neither template is proved empty.

## 7. Exact next task and nonclaims

The rank and kernel work replaces every common survivor by one projective
quadratic map `F` and one linear numerator for `B_1`.  The next exact attack
should therefore work in each guarded one-dimensional common-chart
coordinate ring: reduce the three product-chain equations and one compact
sum cut there, and only saturate after the system becomes zero-dimensional.
Do not retry a raw seven-variable degree-order basis or expand (6.4)/(6.7)
in the ambient ring before this reduction.

This packet does **not** prove that the two templates are exhaustive or
empty; delete either alignment branch; delete `433-1a -> O0b`; close the
positive coordinate orientation or order-two type; identify an owner or
payment; close K3 or the KoalaBear row; or prove either Prize result.

## 8. Replay

The default exact replay is deliberately small:

```bash
python3 experimental/scripts/verify_kb_mca_v4_m2_r4_coordinate_positive_433_1a_outside_reduction_v1.py \
  --check --tamper-selftest
```

It pins the parent commit/blobs/payload, replays the finite cell and matching
censuses, checks every displayed polynomial identity symbolically, checks
the certificate seal, and rejects hostile status mutations.  A machine with
Singular can additionally reconstruct the six product minors and replay the
three localized unit ideals:

```bash
python3 experimental/scripts/verify_kb_mca_v4_m2_r4_coordinate_positive_433_1a_outside_reduction_v1.py \
  --check --full-singular-replay
```

An independent clean Modal image with Singular and SymPy replayed all three
localized cells successfully (`SINGULAR_REPLAYED 3`, app
`ap-Iz1TrNvOrldVFaJExtbKt8`).

**Falsifier:** an admissible deployed-field matching cell with product rank
below five; a common survivor whose matrix rank is not seven or whose kernel
violates (3.2); an actual outside assignment absent from (4.4); an actual
edge violating (5.2)/(5.3); or an actual lift of (6.2) or (6.5) violating
its corresponding target-free identities.
