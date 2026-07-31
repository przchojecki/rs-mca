---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: For each supplied degree-60 endpoint record, all 32099 canonical source-partition templates in inner degrees 2,3,4,6,10 and the unique inner-degree-12 pencil have deterministic exact source-rank and active-syndrome tests. After strict routing through proper right factors, an inherited irreducible bidegree-(4,4) component cannot be a same-inner-fiber component: the complete primitive-group catalogues in degrees 2,3,4,6,10,12 have no subdegree four, while degree 5 is already deleted. Every surviving actual component therefore induces a non-diagonal outer self-correspondence with exact degree relation delta*r=4m. Exact deployed-field divisor-interface controls show that the imported source and active divisor gates alone do not delete the inner-degree-2 or inner-degree-3 rows.
architecture: null
partition_digest: null
atom_or_cell: K3_DEGREE60_SOURCE_PENCIL_RANK_COMPILER
quantifier: every actual residual Q=6,s=6,u=2 endpoint record and every canonical source partition in the six surviving inner-degree profiles
projection_and_unit: exact per-record decomposition compiler and geometric route cut; not a carrier owner, received-line theorem, or distinct-slope payment
claimed_bound: 32099 exact raw templates per supplied endpoint record; every same-fiber quartic strictly routes or is impossible; every terminal actual survivor is a transverse outer correspondence with delta*r=4m
status: PROVED_EXACT_PER_RECORD_COMPILER_AND_TRANSVERSE_OUTER_ROUTE_CUT_ROW_OPEN
impact: REPLACES_UNBOUNDED_RATIONAL_MAP_SEARCH_BY_EXACT_LINEAR_ALGEBRA_AND_IDENTIFIES_THE_MISSING_OUTER_OR_SOURCE_SEMANTIC_THEOREM
falsifier: a valid source partition rejected by the rank tests, a primitive group in one of the terminal inner degrees with subdegree four, a same-fiber actual quartic surviving strict right-factor routing, or a claimed row deletion contradicted by a divisor-interface control
replay: python3 experimental/scripts/verify_kb_mca_v4_degree60_source_pencil_rank_compiler_v1.py --check --tamper-selftest && sage experimental/scripts/verify_kb_mca_v4_degree60_source_pencil_rank_compiler_v1.sage
---

# KoalaBear degree-\(60\) source-pencil rank compiler

## 0. Verdict

The decomposable \(u=2\) branch now has a deterministic exact compiler and
a sharper geometric terminal, but it is not closed.

For one **supplied actual endpoint record**

\[
K,\qquad
A(T)=\prod_{i=1}^{12}(T-\alpha_i),\qquad
V_{\rm act}(T)=\prod_{\nu=1}^{60}(T-\tau_\nu),
\qquad
f=\frac{V_{\rm act}}{A^5},
\tag{0.1}
\]

the source-fiber adapter leaves inner degrees

\[
m\in\{2,3,4,6,10,12\}.
\tag{0.2}
\]

There are exactly

\[
10395+15400+5775+462+66+1=32099
\tag{0.3}
\]

canonical source-partition templates.  Every template has an exact
source-rank test and an exact active symmetric-power membership test.  No
generic rational-map search is needed.

The number \(32099\) is a **per-record template count**.  The repository
does not contain one finite list of all possible pairs \((A,V_{\rm act})\).
Consequently (0.3) is not an exhaustive finite census of the KoalaBear row.
The compiler is uniform in the supplied record.

The inherited actual component

\[
\Gamma\subset\{f(T)=f(W)\}
\tag{0.4}
\]

is irreducible of bidegree \((4,4)\).  First route every candidate inner map
through proper right factors until its right component is geometrically
indecomposable.  Then \(\Gamma\) cannot lie in the same-inner-fiber divisor

\[
\Delta_h(T,W)
=H_0(T)H_1(W)-H_1(T)H_0(W).
\tag{0.5}
\]

Indeed, such a component would give the primitive monodromy of \(h\) a
subdegree four.  The complete primitive catalogues in degrees
\(2,3,4,6,10,12\) contain no such subdegree, while the sole degree where
the off-diagonal total degree can equal four, \(m=5\), was already deleted
by the challenge-field fifth-power contradiction.

Thus every actual terminal survivor is transverse to the inner fibers.  If

\[
C=\overline{(h\times h)(\Gamma)}
\subset\{F(Y)=F(Z)\}
\tag{0.6}
\]

has bidegree \((r,r)\), and
\(\delta=\deg(\Gamma\to C)\), then

\[
\boxed{\delta r=4m.}
\tag{0.7}
\]

This is the explicit terminal

```text
TRANSVERSE_OUTER_CORRESPONDENCE(r,delta)
```

and remains unpaid.

Finally, exact controls over the deployed field show why the result must
stop there.  The source and active divisor gates alone admit
geometrically indecomposable degree-two and degree-three pencils.  They
also admit composite examples in degrees \(4,6,10,12\), all routing to
degree two.  These controls do not satisfy the inherited
bidegree-\((4,4)\) actual-component or design semantics and are not endpoint
survivors.  They rigorously rule out a source-only deletion of the live
prime-degree rows.

No carrier owner, received-data descent, explaining-polynomial descent,
slope projection, ledger movement, \(u=2\) closure, or KoalaBear row closure
is claimed.

## 1. Imported statement and scope

The parent source-fiber adapter proves, for every geometric decomposition

\[
f=F\circ h,\qquad \deg h=m,\qquad\deg F=n,\qquad mn=60,
\tag{1.1}
\]

that:

1. the \(60\) active roots are a disjoint union of complete reduced
   \(h\)-fibers;
2. the \(12\) source roots split into complete reduced fibers and
   index-five exceptional fibers;
3. \(m=5\) is impossible over \(K=\mathbf F_{p^6}\);
4. \(m=30\) routes to \(m=6\);
5. the remaining rows are

\[
\begin{array}{c|c|c|c}
m&n&a&b\\ \hline
2&30&6&0\\
3&20&4&0\\
4&15&3&0\\
6&10&2&0\\
10&6&1&1\\
12&5&1&0.
\end{array}
\tag{1.2}
\]

Here \(a\) counts complete source fibers of size \(m\), while \(b\) counts
exceptional source blocks of size \(m/5\), whose locators occur to the
fifth power in the inner pencil.

The earlier primitive-subdegree-four theorem supplies the actual irreducible
component (0.4) and its bidegree.  Those are imported facts, not reconstructed
by this packet.

The endpoint parameter line is not the Reed--Solomon evaluation carrier.
Nothing below identifies the variables, transports a pencil to the carrier,
or supplies an owner in the active Grande Finale chronology.

## 2. Canonical source templates

For a finite source block \(E\), write

\[
L_E(T)=\prod_{\alpha\in E}(T-\alpha).
\tag{2.1}
\]

For a row \((m,n,a,b)\), a canonical source partition is an unordered tuple

\[
(S_1,\ldots,S_a;R_1,\ldots,R_b),
\quad |S_i|=m,\quad |R_j|=m/5,
\tag{2.2}
\]

whose blocks partition the twelve source points.  The forced degree-\(m\)
forms are

\[
\mathcal G_\pi
=\{L_{S_i}:1\le i\le a\}
\cup\{L_{R_j}^5:1\le j\le b\}.
\tag{2.3}
\]

The unordered-block convention gives

\[
N_m=
\frac{12!}{(m!)^a a!\,((m/5)!)^b b!}.
\tag{2.4}
\]

For the six rows in (1.2),

\[
\begin{array}{c|rrrrrr}
m&2&3&4&6&10&12\\ \hline
N_m&10395&15400&5775&462&66&1.
\end{array}
\tag{2.5}
\]

This proves (0.3).

Any two distinct generators in (2.3) have disjoint zero sets.  They are
therefore coprime and linearly independent.  When the span of all
generators has dimension two, the first two generators in canonical order
determine the unique source pencil

\[
\mathcal W_\pi=\langle H_0,H_1\rangle.
\tag{2.6}
\]

## 3. Exact source-rank and active-syndrome compiler

Place the coefficient vectors of \(\mathcal G_\pi\) as columns of a matrix
\(S_\pi\), using degrees \(0,\ldots,m\) as rows.  The source gate is exactly

\[
\boxed{\operatorname{rank}S_\pi=2.}
\tag{3.1}
\]

The shapes and determinantal codimensions are

\[
\begin{array}{c|c|c}
m&\text{shape of }S_\pi&
\text{independent rank-\(\le2\) codimension}\\ \hline
2&3\times6&4\\
3&4\times4&4\\
4&5\times3&3\\
6&7\times2&0\\
10&11\times2&0.
\end{array}
\tag{3.2}
\]

The last two source gates are automatic once the blocks are disjoint.

For a passing source pencil define

\[
C_{m,n}(H_0,H_1)
=
\begin{bmatrix}
\operatorname{coeff}(H_0^n)&
\operatorname{coeff}(H_0^{n-1}H_1)&\cdots&
\operatorname{coeff}(H_1^n)
\end{bmatrix}.
\tag{3.3}
\]

Rows are degrees \(0,\ldots,60\), so \(C_{m,n}\) has shape
\(61\times(n+1)\).  Substitution

\[
P(U,V)\longmapsto P(H_0,H_1)
\tag{3.4}
\]

is injective: on the open set \(H_1\ne0\), a homogeneous relation would
give a nonzero one-variable polynomial vanishing on the nonconstant
rational function \(H_0/H_1\).  Hence

\[
\operatorname{rank}C_{m,n}=n+1.
\tag{3.5}
\]

The active gate is exactly

\[
\boxed{
\operatorname{rank}
\big[C_{m,n}\mid\operatorname{coeff}(V_{\rm act})\big]
=n+1.}
\tag{3.6}
\]

Equivalently, \(60-n\) independent left-kernel syndromes vanish.  The exact
matrix shapes are

\[
\begin{array}{c|c|c}
m&C_{m,n}\text{ shape}&\text{active syndromes}\\ \hline
2&61\times31&30\\
3&61\times21&40\\
4&61\times16&45\\
6&61\times11&50\\
10&61\times7&54.
\end{array}
\tag{3.7}
\]

By the parent binary source-pencil theorem, (3.1) and (3.6) are necessary
and sufficient for that source partition to yield the declared geometric
decomposition profile.

The compiler therefore has the deterministic per-record terminal order:

```text
SOURCE_RANK_FAILURE
ACTIVE_SYNDROME_FAILURE
STRICT_RIGHT_FACTOR_ROUTE
SAME_FIBER_SUBDEGREE4_IMPOSSIBLE
TRANSVERSE_OUTER_CORRESPONDENCE(r,delta)
```

This order is an existence compiler.  Quotienting templates by an exact
record stabilizer is permitted as an optimization, but no generic
stabilizer or multiplicity saving is assumed.

## 4. Reduced inner-degree-twelve gate

For \(m=12\), the source partition is unique.  The parent adapter recovers
the canonical pencil

\[
\mathcal W_{12}=\langle A,N_0\rangle,
\qquad
N_0^5\equiv V_{\rm act}\pmod A,\quad \deg N_0<12.
\tag{4.1}
\]

Fifth powering is bijective in the split algebra
\(K[T]/(A)\simeq K^{12}\), so \(N_0\) is unique.  Moreover
\(\gcd(A,N_0)=1\) is automatic: at a source root \(\alpha_i\),
\(V_{\rm act}(\alpha_i)\ne0\), so (4.1) gives \(N_0(\alpha_i)\ne0\).

Put

\[
B=\frac{V_{\rm act}-N_0^5}{A},
\qquad \deg B\le48.
\tag{4.2}
\]

Then the six-column degree-\(60\) membership gate reduces exactly to

\[
\boxed{
B\in\operatorname{span}
\{A^4,A^3N_0,A^2N_0^2,AN_0^3,N_0^4\}.}
\tag{4.3}
\]

The five displayed forms are independent by the same substitution
argument as in (3.4).  Thus (4.3) is a \(49\times5\) rank-five test with
\(44\) independent syndromes.

## 5. Strict right-factor routing

Before analyzing (0.5), decompose the recovered rational map \(h\) exactly.
If

\[
h=s\circ r,\qquad 1<\deg r<m,
\tag{5.1}
\]

then

\[
f=(F\circ s)\circ r.
\tag{5.2}
\]

Thus \(r\) is itself a right component of the same endpoint record.  The
parent divisor adapter applies again and transports the active fibers of
\(r\) to a target normalization over \(K\).  The only strict routes are

\[
\begin{array}{c|l}
m&\text{possible proper right degrees}\\ \hline
4&2\\
6&2,3\\
10&2,5\\
12&2,3,4,6.
\end{array}
\tag{5.3}
\]

Degree five terminates in the already-proved challenge-field contradiction.
All other arrows strictly lower the inner degree.  Iteration therefore
terminates at a geometrically indecomposable right component in

\[
\{2,3,4,6,10,12\},
\tag{5.4}
\]

or at the deleted degree-five row.

This routing is geometric.  It is not yet the active invariant-quotient
owner, because no carrier or data semantics have been transported.

## 6. Same-fiber quartics are impossible at the terminal inner map

Let \(h=[H_0:H_1]\) now be a terminal geometrically indecomposable right
component.  Its same-fiber divisor is (0.5).  If the irreducible
\(\Gamma\) in (0.4) satisfies

\[
\Gamma\subset V(\Delta_h),
\tag{6.1}
\]

then \(\Gamma\) is an irreducible component of the self-fiber product of
\(h\).  The monodromy/suborbit dictionary makes its degree in either
coordinate a point-stabilizer subdegree.  Since
\(\operatorname{bideg}\Gamma=(4,4)\), that subdegree is four.

For \(m=2,3,4\), this is already impossible because, after removing the
diagonal, \(\Delta_h\) has bidegree \((m-1,m-1)<(4,4)\).

For \(m=6,10,12\), separability follows from \(p>12\), while geometric
indecomposability makes the monodromy primitive.  The complete small-degree
primitive catalogues give:

\[
\begin{array}{c|c|l}
m&\#\text{ primitive groups}&
\text{complete subdegree rows}\\ \hline
2&1&(1,1)\\
3&2&(1,1,1),\ (1,2)\\
4&2&(1,3)\\
5&5&(1,1,1,1,1),\ (1,2,2),\ (1,4)\\
6&4&(1,5)\\
10&9&(1,3,6),\ (1,9)\\
12&6&(1,11).
\end{array}
\tag{6.2}
\]

Repeated rows in the last column correspond to different primitive groups.
No terminal degree has subdegree four.  Degree five is exactly the profile
where an off-diagonal degree-four component can occur, and that entire
profile is already empty by the parent theorem.

Therefore:

\[
\boxed{\Gamma\not\subset V(\Delta_h)}
\tag{6.3}
\]

for every terminal actual survivor.

This conclusion is unaffected by reducibility of \(\Delta_h\): an
irreducible \(\Gamma\) satisfying (6.1) would lie in one irreducible factor
and would still give the forbidden suborbit.

## 7. Exact transverse outer terminal

By (6.3), the image

\[
C=\overline{(h\times h)(\Gamma)}
\tag{7.1}
\]

is irreducible and non-diagonal.  Since \(f=F\circ h\),

\[
C\subset\{F(Y)=F(Z)\}.
\tag{7.2}
\]

Write \(\operatorname{bideg}C=(r_Y,r_Z)\) and
\(\delta=\deg(\Gamma\to C)\).  The map
\(\Gamma\to\mathbf P^1_Y\) has degree \(4m\): projection
\(\Gamma\to\mathbf P^1_T\) has degree four and \(h\) has degree \(m\).
The identical calculation in the second coordinate also gives degree
\(4m\).  Factoring both maps through \(C\) gives

\[
\delta r_Y=4m=\delta r_Z.
\tag{7.3}
\]

Thus \(r_Y=r_Z=:r\), so \(C\) has bidegree \((r,r)\), and

\[
\delta r=4m.
\tag{7.4}
\]

Because \(C\) is a non-diagonal component of the degree-\(n\) outer
self-fiber product, \(r\le n-1\).  Moreover \(h\times h\) has degree
\(m^2\), so its restriction gives

\[
\delta\le m^2.
\tag{7.5}
\]

Hence the only possible \(r\) are:

\[
\begin{array}{c|c|l}
m&n&r\\ \hline
2&30&2,4,8\\
3&20&2,3,4,6,12\\
4&15&1,2,4,8\\
6&10&1,2,3,4,6,8\\
10&6&1,2,4,5\\
12&5&1,2,3,4.
\end{array}
\tag{7.6}
\]

For each \(r\), \(\delta=4m/r\).  This is a finite, falsifiable outer
correspondence interface.  It is not an owner: the actual
source-star/component incidence, received data, explaining polynomial, and
slope semantics have not yet been imposed on \(C\).

## 8. Exact deployed-field divisor-interface controls

The deployed characteristic is

\[
p=2{,}130{,}706{,}433.
\tag{8.1}
\]

### 8.1 Power controls

Work in \(\mathbf F_{p^2}\subset K\).  Since \(p\equiv2\pmod3\), let
\(\omega^2+\omega+1=0\).  Also

\[
\iota=16{,}711{,}679,\qquad \iota^2=-1\pmod p.
\tag{8.2}
\]

For \(m=2,3,4,6,12\), choose

\[
\zeta_2=-1,\quad
\zeta_3=\omega,\quad
\zeta_4=\iota,\quad
\zeta_6=-\omega,\quad
\zeta_{12}=\iota\omega.
\tag{8.3}
\]

These elements have the indicated exact orders, because

\[
m\mid p^2-1
\quad(m=2,3,4,6,12).
\tag{8.4}
\]

Take \(h(z)=z^m\).  For the \(a+n\) small integers
\(u=1,\ldots,a+n\), the target values \(u^m\) are pairwise distinct
modulo \(p\), and

\[
h^{-1}(u^m)=\{u\zeta_m^j:0\le j<m\}.
\tag{8.5}
\]

Use the first \(a\) fibers as complete source fibers and the remaining
\(n\) as active fibers.  This gives split, squarefree, disjoint source and
active locators satisfying the exact rank compiler.

The \(m=2\) and \(m=3\) controls are geometrically indecomposable because
their degrees are prime.  The other controls route explicitly through
\(z^2\):

\[
z^4=(z^2)^2,\qquad
z^6=(z^2)^3,\qquad
z^{12}=(z^2)^6.
\tag{8.6}
\]

### 8.2 Degree-ten control

The congruence \(10\nmid p^2-1\) prevents the analogous power construction.
Instead, over \(\mathbf F_p\), put

\[
r(z)=z+\frac2z,\qquad
s(x)=x^5+x^2+x,\qquad
h=s\circ r.
\tag{8.7}
\]

In homogeneous coordinates,

\[
\begin{aligned}
R_n&=Z^2+2W^2,&R_d&=ZW,\\
N&=R_n^5+R_n^2R_d^3+R_nR_d^4,&D&=R_d^5.
\end{aligned}
\tag{8.8}
\]

The seven values

\[
243,\ 3459,\ 3574,\ 8607,\ 19677,\ 30437,\ 43384
\tag{8.9}
\]

have ten distinct \(\mathbf F_p\)-rational preimages each.  Use the
\(y=243\) fiber as the complete ten-point source fiber and the other six as
active fibers.  The simple outer pole at infinity pulls back to
\(\{0,\infty\}\), each with ramification index five.

The inherited source locator must have twelve **finite** roots.  Conjugate
the source coordinate by

\[
z=1+\frac1t,\qquad [Z:W]=[T+S:T].
\tag{8.10}
\]

Because \(h(1)=255\) is absent from (8.9), no selected fiber meets \(z=1\).
All selected points therefore become finite, while the exceptional pair
\(\{0,\infty\}\) becomes \(\{-1,0\}\).  With

\[
N'(T,S)=N(T+S,T),\qquad D'(T,S)=D(T+S,T),
\tag{8.11}
\]

the source locator is

\[
A'(T,S)=T(T+S)\bigl(N'-243D'\bigr),
\tag{8.12}
\]

and the active locator is

\[
V'_{\rm act}
=\prod_{y\in\{3459,3574,8607,19677,30437,43384\}}
(N'-yD').
\tag{8.13}
\]

The source pencil is

\[
\langle N'-243D',\,D'\rangle=\langle N',D'\rangle,
\tag{8.14}
\]

so its source matrix has rank two and (8.13) lies in its sixth symmetric
power.  Equation (8.8) exhibits the strict degree-two right factor after
conjugation.

All roots and polynomial identities in this control are checked exactly by
the Python, Sage, and Wolfram replays.  It is a nonempty divisor interface,
not an inherited actual \(\Gamma\).

## 9. What this proves and what remains

### Proved

- The six surviving source profiles have exactly \(32099\) canonical raw
  templates per endpoint record.
- Equations (3.1), (3.6), and (4.3) give exact deterministic
  necessary-and-sufficient pencil tests.
- Proper right components route strictly through the profile ladder.
- A terminal actual bidegree-\((4,4)\) component cannot be a same-fiber
  component.
- Every actual terminal survivor has the explicit transverse outer
  interface (7.4)--(7.6).
- The imported divisor gates alone admit exact deployed-field controls,
  including indecomposable \(m=2,3\) controls.

### Imported

- The actual endpoint record and irreducible bidegree-\((4,4)\) component.
- The source-fiber adapter and degree-five deletion.
- The monodromy-factor/suborbit dictionary.
- Geometric indecomposability \(\Longleftrightarrow\) primitive monodromy
  for separable rational maps.
- Completeness of the GAP `PrimGrp` catalogues in the displayed degrees.

### Not proved

- A finite census of all endpoint records.
- Existence of an inherited actual component for any control in Section 8.
- Elimination or ownership of the transverse outer correspondences.
- Parameter-to-carrier transport.
- Preservation of the evaluation domain or received data.
- Descent of an explaining polynomial or affine slopes.
- Any value of \(U_{\rm paid},U_Q,U_{\rm BC},U_{\rm new}\).
- Closure of \(u=2\), K3, or the KoalaBear row.

The next maximal theorem is therefore source-coupled and outer, not another
source-only rank calculation: impose the inherited quartic/source-star
incidence on the finite transverse rows (7.6), and terminate each row in an
actual-producer contradiction or a chronology-valid carrier/data/slope
owner.
