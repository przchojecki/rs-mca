---
workboard_item: K1
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: A hypothetical 69-source-map-class primitive equality-wall line has a common carrier-zero core whose normalized split complement locators span coefficient dimension at most 16. They form an exact fixed-domain Reed--Solomon agreement list in an affine polynomial space of dimension at most eight, with normalized excess delta at least 3912. A strengthened source parameter gives a coprime exact-degree-134944 pencil. The associated pushforward bundle has maximum splitting degree at most seven, so the generic-kernel-free branch has at most 63 selected parameters. The only remaining branch is a positive generic kernel, equivalently a rational-scroll family of split quotients. Its source-zero part descends by exactly 134944 degrees, but no cap 68 or active owner payment is proved for the universal-kernel branch.
architecture: GRANDE_FINALE_V4_KB_MCA_TANGENT_DEEP_SOURCE_RATIONAL_C5_BASE_TWIST_FROBENIUS_9208_FIRST_GAP_PENCIL_IMAGE_ADAPTER_V1
atom_or_cell: ACTIVE_FULL_OUTSIDE_EQUALITY_WALL_FIXED_DOMAIN_RANK16_NORMALIZATION
quantifier: Per hypothetical 69-map-class primitive transversal residue line in the scalar-unpaid rank-three equality packet
projection_and_unit: Distinct selected finite slopes and their actual graph records; fixed carrier-domain split locators after removal of the canonical common zero core
claimed_bound: Generic-kernel branch cap 63 only; the universal-kernel split-quotient branch remains open and no charge is booked
status: PROVED_REDUCTION_ROW_OPEN
impact: FIXED_DOMAIN_RANK16_AND_GENERIC_CAP63_PROVED_FIRST_OPEN_134943_UNCHANGED
falsifier: A valid 69-class equality packet whose normalized complement locators have coefficient rank above 16; whose normalized excess is below 3912; whose strengthened source pencil cannot be chosen coprime of exact degree e; or whose associated bundle map is generically injective despite 69 selected fiber kernels.
replay: python3 experimental/scripts/verify_kb_mca_v4_equality_wall_fixed_domain_rank16_normalization_v1.py --check
---

# KoalaBear equality-wall fixed-domain rank-16 normalization

## 0. Result and boundary

This note consumes the proved equality-wall residue-line packet and assumes a
hypothetical primitive transversal residue line with \(69\) occupied
source-map classes. It proves:

1. the \(69\) complement locators have coefficient-space rank at most \(16\);
2. all moving locator sets lie in one canonical carrier set \(U_0\), the
   union of at most nine actual moving sets;
3. after removing the common zero core, the normalized split locators have
   exact degree \(c+\delta\), pair intersections at most \(\delta\), empty
   total intersection, and span dimension at most \(16\);
4. the packet is an exact fixed-domain Reed--Solomon agreement list of
   \(69\) degree-\(\le\delta\) polynomials in an affine space of dimension at
   most eight;
5. elementary pair-incidence packing forces \(\delta\ge3{,}912\);
6. the source parameter can be chosen so the normalized source pencil is
   coprime, has degree \(e\), and every selected member has exact degree
   \(e\);
7. the associated vector-bundle map cannot be generically injective: that
   branch has the stronger cap \(63\); and
8. the remaining positive-generic-kernel branch has an exact
   source-zero degree-\(e\) recursion.

It does not eliminate the universal-kernel branch. No active owner or charge
is added, and the first open slack remains

\[
r=134{,}943.
\tag{0.1}
\]

The pinned constants are

\[
\begin{gathered}
p=2{,}130{,}706{,}433,\qquad
s=202{,}416,\qquad
e=134{,}944,\qquad
c=67{,}472,\\
|V|=1{,}894{,}736,\qquad
J=981{,}105,\qquad
\dim_FK_0=8.
\end{gathered}
\tag{0.2}
\]

## 1. Inherited graph packet

Index the \(69\) actual graph records by \(i\). Let

\[
Z_i=V\setminus Y_i,\qquad |Y_i|=J,\qquad
q_i=\Lambda_{Z_i}.
\tag{1.1}
\]

Parameterize the primitive transversal residue line by distinct
\(t_i\in\mathbf P^1(F)\). Its source-product pairs have the form

\[
R_i=R_0+t_iR_1,\qquad
S_i=S_0+t_iS_1.
\tag{1.2}
\]

The actual graph polynomials are

\[
P_i=q_iR_i,\qquad Q_i=q_iS_i.
\tag{1.3}
\]

The proved source-selector identification says that both
\(P_i-P_1\) and \(Q_i-Q_1\) represent words in the same
eight-dimensional selector kernel \(K_0\).

Remove the carrier roots of the line collision divisor:

\[
T=V\setminus Z(H_U).
\tag{1.4}
\]

Since \(\deg H_U\le c\),

\[
|T|\ge |V|-c=1{,}827{,}264.
\tag{1.5}
\]

For every \(x\in T\), the matrix

\[
\begin{pmatrix}
R_0(x)&R_1(x)\\
S_0(x)&S_1(x)
\end{pmatrix}
\tag{1.6}
\]

is invertible.

## 2. Simultaneous coefficient rank at most 16

Let \(L\) be the \(|T|\times69\) matrix whose \(i\)-th column is
\(q_i|_T\), and put

\[
\mathsf T=\operatorname{diag}(t_1,\ldots,t_{69}).
\tag{2.1}
\]

The evaluated pair columns \((P_i,Q_i)\), after the pointwise invertible
transformations (1.6), become

\[
\binom{q_i(x)}{t_iq_i(x)}.
\tag{2.2}
\]

The pair columns lie in an affine space of direction dimension at most
\(16\). Therefore

\[
\operatorname{rank}
\begin{pmatrix}
L\\L\mathsf T
\end{pmatrix}
\le17.
\tag{2.3}
\]

Let \(C\subseteq F^{69}\) be the row space of \(L\), with
\(r_C=\dim C\). If \(C\mathsf T\subseteq C\), then \(C\) is invariant under
a diagonal operator with \(69\) distinct eigenvalues. Hence \(C\) is a
coordinate subspace. Every coordinate projection of \(C\) is nonzero:
each \(q_i\) has degree

\[
|Z_i|=|V|-J=913{,}631<|T|,
\tag{2.4}
\]

so no column \(q_i|_T\) is zero. Thus an invariant \(C\) would have to be
all of \(F^{69}\), contradicting (2.3).

Consequently \(C\mathsf T\nsubseteq C\), whence

\[
\dim(C+C\mathsf T)\ge r_C+1.
\tag{2.5}
\]

Combining (2.3) and (2.5) gives

\[
\boxed{r_C\le16.}
\tag{2.6}
\]

Evaluation on \(T\) is injective for degree-\(913{,}631\) polynomials, so

\[
\boxed{
\dim_F\operatorname{span}\{q_1,\ldots,q_{69}\}\le16
}
\tag{2.7}
\]

in coefficient space.

## 3. Canonical common core

Root the canonical secant star at record \(1\), and let \(B\) be its first
independent basis. The preceding packet gives

\[
|B|\le8.
\tag{3.1}
\]

Put

\[
U_0=Y_1\cup\bigcup_{b\in B}Y_b.
\tag{3.2}
\]

For a nonbasis record \(j\), its canonical fundamental circuit contains
\(j\) and only records from \(\{1\}\cup B\). The no-singleton atom at \(j\)
therefore gives

\[
Y_j\subseteq Y_1\cup\bigcup_{b\in B_j}Y_b\subseteq U_0.
\tag{3.3}
\]

Thus

\[
\boxed{Y_i\subseteq U_0\quad(1\le i\le69).}
\tag{3.4}
\]

Because the star has a nonzero edge and every active exchange is at least
\(c\),

\[
|U_0|\ge J+c.
\tag{3.5}
\]

Write

\[
|U_0|=J+c+\delta=1{,}048{,}577+\delta,
\qquad
0\le\delta\le846{,}159.
\tag{3.6}
\]

Define

\[
Z_0=V\setminus U_0,\qquad
D_i=U_0\setminus Y_i,\qquad
p_i=\Lambda_{D_i}.
\tag{3.7}
\]

Then

\[
q_i=\Lambda_{Z_0}p_i,\qquad
\deg p_i=|D_i|=c+\delta.
\tag{3.8}
\]

Since \(U_0\) is already the union of the moving sets indexed by
\(\{1\}\cup B\),

\[
\bigcap_{i=1}^{69}D_i=\varnothing.
\tag{3.9}
\]

For each pair, with exchange distance \(\Delta_{ij}\ge c\),

\[
|D_i\cap D_j|
=|U_0|-|Y_i\cup Y_j|
=c+\delta-\Delta_{ij}
\le\delta.
\tag{3.10}
\]

Removing the common factor \(\Lambda_{Z_0}\) from (2.7) gives

\[
\boxed{
\begin{aligned}
&|U_0|=1{,}048{,}577+\delta,\\
&\deg p_i=67{,}472+\delta,\\
&\deg\gcd(p_i,p_j)\le\delta,\\
&\gcd_i p_i=1,\\
&\dim_F\operatorname{span}\{p_i\}\le16.
\end{aligned}}
\tag{3.11}
\]

All \(p_i\) are monic and split over the fixed carrier domain \(U_0\).

## 4. Exact fixed-domain agreement list

For the canonical full-domain source parameter, write

\[
A_i=U+t_iV,\qquad
F_i=\Lambda_{Z_i}A_i.
\tag{4.1}
\]

After factoring the common zero core,

\[
F_i=\Lambda_{Z_0}f_i,\qquad
f_i=p_iA_i.
\tag{4.2}
\]

The actual selector secant \(F_i-F_1\) vanishes on \(Z_0\), and the exact
quotient identity gives

\[
f_i=f_1+\Lambda_\Sigma h_i,
\qquad
\deg h_i\le\delta.
\tag{4.3}
\]

The \(h_i\) lie in an affine polynomial space of dimension at most eight,
because the corresponding secants lie in \(K_0\).

On \(U_0\), define

\[
y(x)=-\frac{f_1(x)}{\Lambda_\Sigma(x)}.
\tag{4.4}
\]

The full-domain source choice has \(A_i(x)\ne0\) on the carrier. Hence

\[
\boxed{
x\in D_i
\quad\Longleftrightarrow\quad
h_i(x)=y(x).
}
\tag{4.5}
\]

Thus the hypothetical line gives \(69\) distinct degree-\(\le\delta\)
polynomials in one affine space of dimension at most eight, each agreeing
with the same word \(y\) on exactly

\[
c+\delta=67{,}472+\delta
\tag{4.6}
\]

points of a fixed domain of size

\[
J+c+\delta=1{,}048{,}577+\delta.
\tag{4.7}
\]

Their pairwise common agreement is at most \(\delta\).

## 5. Exact pair-incidence boundary

Let \(m_x\) be the number of sets \(D_i\) containing \(x\). Then

\[
\sum_xm_x=69(c+\delta),
\qquad
\sum_x\binom{m_x}{2}
=\sum_{i<j}|D_i\cap D_j|
\le\binom{69}{2}\delta.
\tag{5.1}
\]

For fixed total incidence, the left side is minimized by balancing the
\(m_x\) over the \(|U_0|\) coordinates.

At \(\delta=3{,}911\), the balanced minimum is

\[
9{,}176{,}828,
\tag{5.2}
\]

while the intersection cap is

\[
9{,}175{,}206.
\tag{5.3}
\]

This is impossible. At \(\delta=3{,}912\), the corresponding values are

\[
9{,}177{,}094
\quad\text{and}\quad
9{,}177{,}552,
\tag{5.4}
\]

leaving margin only \(458\). Therefore

\[
\boxed{\delta\ge3{,}912.}
\tag{5.5}
\]

Pair counting alone does not exclude \(\delta=3{,}912\).

## 6. Coprime exact-degree source pencil

The line collision identity is

\[
R_0S_1-R_1S_0=\Lambda_\Sigma H_U,
\qquad
\deg H_U\le c.
\tag{6.1}
\]

At every geometric root of \(H_U\), the matrix in (1.6) has rank exactly
one. Rank zero would make every occupied pair \((R_i,S_i)\) share that root,
contradicting equality-stratum coprimality.

The original full-domain construction excludes at most

\[
130{,}941{,}546
\tag{6.2}
\]

parameters. Exclude in addition:

1. at most one parameter for each of the at most \(c\) roots of \(H_U\), so
   the resulting two pencil generators have no common root; and
2. at most one parameter for each of the \(69\) selected records, so every
   selected pencil member retains exact degree \(e\).

The total is

\[
130{,}941{,}546+67{,}472+69
=131{,}009{,}087
<p.
\tag{6.3}
\]

Choose the first remaining parameter. The resulting pencil

\[
A_t=U+tV
\tag{6.4}
\]

satisfies

\[
\boxed{
\gcd(U,V)=1,\qquad
\max(\deg U,\deg V)=e,\qquad
\deg A_{t_i}=e.
}
\tag{6.5}
\]

It defines a finite morphism

\[
f=[-U:V]\colon\mathbf P^1_X\longrightarrow\mathbf P^1_t
\tag{6.6}
\]

of degree \(e\), whose fiber over \(t\) is cut out by \(A_t\).

## 7. The generic-kernel branch has cap 63

All normalized graph polynomials have degree

\[
N=(c+\delta)+e=s+\delta.
\tag{7.1}
\]

Let

\[
\mathcal E=f_*\mathcal O_{\mathbf P^1_X}(N).
\tag{7.2}
\]

This is a rank-\(e\) vector bundle on \(\mathbf P^1_t\). Write

\[
N=qe+\rho,\qquad0\le\rho<e.
\tag{7.3}
\]

Projection formula gives

\[
h^0(\mathcal E(a))
=h^0\!\left(\mathcal O_{\mathbf P^1_X}(N+ae)\right)
\tag{7.4}
\]

for every integer \(a\), which determines the splitting

\[
\boxed{
\mathcal E
\simeq
\mathcal O(q)^{\rho+1}
\oplus
\mathcal O(q-1)^{e-\rho-1}.
}
\tag{7.5}
\]

Since

\[
\delta\le846{,}159,\qquad
N\le1{,}048{,}575<8e=1{,}079{,}552,
\tag{7.6}
\]

we have

\[
q\le7.
\tag{7.7}
\]

By (4.3), the polynomial space

\[
W=\operatorname{span}\{F_1,\ldots,F_{69}\}
\tag{7.8}
\]

has dimension

\[
m=\dim W\le9.
\tag{7.9}
\]

It defines the evaluation map

\[
\Phi:W\otimes\mathcal O_{\mathbf P^1_t}\longrightarrow\mathcal E.
\tag{7.10}
\]

At \(t_i\), the nonzero element \(F_i=A_{t_i}p_i\) vanishes on the
scheme-theoretic fiber, so

\[
\ker\Phi(t_i)\ne0.
\tag{7.11}
\]

If \(\Phi\) is generically injective, then
\(\bigwedge^m\Phi\) is a nonzero section of \(\bigwedge^m\mathcal E\).
Every line-bundle summand of the latter has degree at most

\[
mq\le9\cdot7=63.
\tag{7.12}
\]

But (7.11) makes the complete wedge vanish at all \(69\) distinct
parameters. A nonzero component cannot have \(69\) zeros. Therefore

\[
\boxed{
\text{the generic-kernel-free branch has at most }63\text{ records}.
}
\tag{7.13}
\]

Any hypothetical \(69\)-record packet must satisfy

\[
\boxed{
\ker(\Phi\otimes F(t))\ne0.
}
\tag{7.14}
\]

## 8. Exact universal-kernel remainder

A rational section of the generic kernel is a family

\[
F(t,X)=A_t(X)P(t,X)
\tag{8.1}
\]

whose coefficient functions lie in the fixed space \(W\).

All elements of \(W\) restrict on \(\Sigma\) to scalar multiples of the
same nonzero source word \(f_0|_\Sigma\). Thus

\[
F(t,\sigma)=\lambda(t)f_0(\sigma)
\qquad(\sigma\in\Sigma)
\tag{8.2}
\]

for one rational scalar \(\lambda(t)\).

Let \(\lambda_1,\ldots,\lambda_L\) be the distinct projective values of the
source map \(f=[-U:V]\) on \(\Sigma\). At \(t=\lambda_j\), the factor
\(A_t\) vanishes at every source point in the corresponding fiber. Since
\(f_0\) is nonzero at every source point, (8.2) forces
\(\lambda(\lambda_j)=0\). After clearing denominators, the numerator of
\(\lambda(t)\) is therefore divisible by all \(L\) corresponding projective
linear factors. This source-Cauchy divisor is an exact constraint on every
non-source-zero universal-kernel section.

The source-zero subspace is

\[
W_0
=W\cap\Lambda_\Sigma F[X]_{\le\delta}
=\Lambda_\Sigma H,
\qquad
\dim H\le8.
\tag{8.3}
\]

If a generic-kernel family belongs to \(W_0\otimes F(t)\), then

\[
A_tP=\Lambda_\Sigma h.
\tag{8.4}
\]

Since \(\gcd(A_t,\Lambda_\Sigma)=1\) in \(F(t)[X]\),

\[
h=A_tQ,\qquad
P=\Lambda_\Sigma Q,\qquad
\deg_XQ\le\delta-e.
\tag{8.5}
\]

Thus every source-zero universal-kernel component descends by exactly
\(e=134{,}944\) polynomial degrees. The recursion is finite because

\[
\delta\le846{,}159<7e.
\tag{8.6}
\]

In particular, if \(\delta<e\), no nonzero source-zero generic-kernel
section exists. The full generic kernel then has rank at most one, because
the restriction of \(W\) to the source has dimension one.

There is also exact uniqueness at a fixed parameter in this low-\(\delta\)
range. Suppose

\[
pA_t=f_0+\Lambda_\Sigma k,\qquad
p'A_t=f_0+\Lambda_\Sigma k',
\tag{8.7}
\]

with \(\deg k,\deg k'\le\delta\). Subtraction and
\(\gcd(A_t,\Lambda_\Sigma)=1\) give

\[
A_t\mid(k-k').
\tag{8.8}
\]

If \(\delta<e=\deg A_t\), then \(k=k'\) and \(p=p'\). Hence each fixed
parameter supports at most one normalized split quotient in the low-excess
range. The remaining problem is to bound how many distinct parameters can
occur on the rank-one scroll.

This recursion does not bound the number of split quotients in a
non-source-zero rank-one scroll. That is the remaining branch.

## 9. Owner shortcuts that do not follow

None of the normalized auxiliary objects is automatically an active owner:

1. \(h_i\), \(k_i\), or \(Q\) is an auxiliary same-selector quotient, not
   the selected-slope effective multiplier required by the Frobenius owner.
2. The common zero core \(Z_0\) does not bound one record's actual error
   support and therefore does not instantiate the deep owner.
3. The source-rational owner requires an anchored pair-global map agreeing
   with all source labels; one low-degree difference quotient does not
   supply that interface.
4. C5/base and twist are earlier pair-global source predicates, not
   packet-local common factors.
5. The first-gap source-pencil owner is tied to its fixed
   \(s=2e=134{,}944\) interpolation line; the equality packet has
   \(s=202{,}416\).
6. The unrelated rank-16 cap-\(130\) theorem has an endpoint grid and
   complete-tail interface absent from this packet.

The pure Johnson bound also does not close the boundary: at
\(\delta=3{,}912\), its cap is approximately \(72.6\), above \(69\).
Formal-root GM--MDS independence cannot replace a fixed-domain minor, and
\(\dim C\le16\), \(\dim(C+C\mathsf T)\le17\) does not by itself eliminate
coordinate/coloop components.

## 10. Corrected next theorem

The shortest remaining packing target is:

> **Universal-kernel split-quotient lemma.** Let
> \(f=[-U:V]\) have degree \(e=134{,}944\), with
> \(\gcd(U,V)=1\). Let
> \[
> W\subseteq H^0(\mathbf P^1,\mathcal O(s+\delta)),
> \qquad \dim W\le9,
> \]
> and suppose \(W\) restricts to a one-dimensional nonzero space on the
> \(s=202{,}416\) source points. For distinct \(t_i\), suppose
> \[
> F_i=A_{t_i}p_i\in W,
> \]
> where the \(p_i\) are monic, split over one fixed carrier domain, and
> satisfy
> \[
> \deg p_i=c+\delta,\qquad
> \deg\gcd(p_i,p_j)\le\delta,\qquad
> \gcd_i p_i=1.
> \]
> If the associated map
> \(W\otimes\mathcal O\to f_*\mathcal O(s+\delta)\) has positive generic
> kernel, then there are at most \(68\) such distinct parameters.

The generic-kernel-free branch is already proved with cap \(63\). A proof of
this universal-kernel lemma therefore proves the required line cap \(68\)
and pays the equality-wall rank-three packet.

An alternative valid completion is a same-record adapter from the
universal kernel to one of the seven earlier active owners.

## 11. Scope

This packet proves:

* coefficient rank at most \(16\) for all \(69\) complement locators;
* the canonical common carrier-zero core and fixed domain \(U_0\);
* the normalized split-locator intersection ledger;
* the exact eight-dimensional fixed-domain RS agreement list;
* the sharp elementary boundary \(\delta\ge3{,}912\);
* the strengthened coprime exact-degree-\(e\) source pencil;
* the exact pushforward-bundle splitting;
* generic-kernel branch cap \(63\); and
* the source-zero universal-kernel degree-\(e\) recursion;
* the source-value divisor constraint on a non-source-zero kernel section;
  and
* fixed-parameter uniqueness when \(\delta<e\).

It does not:

* eliminate the non-source-zero universal-kernel scroll;
* prove cap \(68\);
* emit an active owner;
* book a charge;
* pay \(r=134{,}943\); or
* move the first open interval.

# PROVED REDUCTION / UNIVERSAL-KERNEL BRANCH OPEN
