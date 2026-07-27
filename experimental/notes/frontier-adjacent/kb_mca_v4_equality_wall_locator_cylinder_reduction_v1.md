---
workboard_item: K1
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: At the first post-sweep slack sigma_wall=134943, every scalar-unpaid stratum except x=1,e=134944 is paid by the strict reciprocal-kernel theorem. In the remaining equality stratum, the complete reciprocal product matrix either has rank at most two and receives the existing (p+1)(n-s) payment, or has rank three and forces the occupied actual-locator residue space to have base dimension exactly three. The latter branch is exactly one split-locator residue cylinder; paying the row reduces to an explicit incidence cap of 275995141152 locator points.
architecture: GRANDE_FINALE_V4_KB_MCA_TANGENT_DEEP_SOURCE_RATIONAL_C5_BASE_TWIST_FROBENIUS_9208_FIRST_GAP_PENCIL_IMAGE_ADAPTER_V1
atom_or_cell: ACTIVE_FULL_OUTSIDE_EQUALITY_WALL_LOCATOR_CYLINDER_REDUCTION
quantifier: Per received line, fixed translated source, rebuilt complete selector, scalar-unpaid full-outside packet, and fixed equality slack
projection_and_unit: Distinct selected finite slopes per received line
claimed_bound: Exact reduction only; no additional charge and no payment of the rank-three locator cylinder
status: PROVED_REDUCTION_ROW_OPEN
impact: FIRST_OPEN_134943_REDUCED_TO_EXACT_RESIDUE_PLANE_LOCATOR_INCIDENCE
falsifier: A scalar-unpaid sigma_wall=134943 stratum other than x=1,e=134944 not satisfying e>2c; a rank-three reciprocal product packet with occupied base dimension other than three; failure of the constant adjugate reconstruction at 3e=2s; a contributing graph line not determined by its actual complement locator inside the same selector; or a claim that residue dimension three makes the degree-981105 locators a polynomial projective plane.
replay: python3 experimental/scripts/verify_kb_mca_v4_equality_wall_locator_cylinder_reduction_v1.py --check
---

# KoalaBear equality-wall locator-cylinder reduction

## 0. Result and exact boundary

The reciprocal-kernel plane sweep pays every scalar-unpaid full-outside
stratum through

\[
r=134{,}942.
\]

At the next slack,

\[
r=134{,}943,\qquad
t=67{,}472,\qquad
s=t+r+1=202{,}416,
\tag{0.1}
\]

all but one scalar stratum still satisfy the strict theorem.  The only
equality stratum is

\[
\boxed{x=1,\qquad e=134{,}944,\qquad c=67{,}472,\qquad h=0.}
\tag{0.2}
\]

It has

\[
e=2c,\qquad s=3c,\qquad 3e=2s,\qquad e+c=s.
\tag{0.3}
\]

This note proves the following exact dichotomy on that remaining stratum.

> **Equality-wall reciprocal rank dichotomy.**  Let \(W_B\) be the
> \(B\)-span of the occupied actual complement-locator residues in one
> fixed same-selector packet, and let \(b=\dim_BW_B\).  Form the complete
> reciprocal product matrix from a \(B\)-basis of \(W_B\) and the complete
> base reciprocal space.
>
> * If its polynomial rank is at most two, every selected slope is paid by
>   the existing source-map cap
>   \[
>   (p+1)(n-s)=4{,}037{,}126{,}185{,}931{,}424.
>   \]
> * If its polynomial rank is at least three, then
>   \[
>   \boxed{b=3.}
>   \]
>   The packet is therefore one projective plane of source residues, but
>   its actual degree-\(981{,}105\) split locators lie in the full
>   preimage cylinder of that plane modulo \(\Lambda_\Sigma\).

The second branch is not paid here.  It reduces the row to one exact
incidence statement:

\[
\boxed{
I_{\rm cyl}
\le
275{,}995{,}141{,}152,
}
\tag{0.4}
\]

where \(I_{\rm cyl}\) is the number of actual degree-\(981{,}105\)
complement locators in one occupied rank-three residue plane.  Indeed, the
same-selector graph-line multiplicity is at most \(981{,}105\), and

\[
981{,}105\cdot275{,}995{,}141{,}152
\le
270{,}780{,}212{,}960{,}575{,}880.
\tag{0.5}
\]

No owner is inserted and no charge is booked.  The first open slack remains
\(134{,}943\).

## 1. Isolation of the equality stratum

At fixed \(r=134{,}943\), the source-rational restart gives

\[
x_0=\left\lceil\frac s2\right\rceil-r=-33{,}735
\le x\le1
\tag{1.1}
\]

and

\[
\left\lceil\frac s2\right\rceil\le e\le r+x.
\tag{1.2}
\]

As in the sweep, put

\[
h=r+x-e,\qquad c=2e-s.
\tag{1.3}
\]

The strict reciprocal-kernel theorem applies when \(e>2c\), equivalently

\[
3e<2s=404{,}832.
\tag{1.4}
\]

Every integer \(e\le134{,}943\) satisfies (1.4).  Equality can occur only at
\(e=134{,}944\); (1.2) then forces \(x=1\), and (1.3) gives \(h=0\) and
\(c=67{,}472\).  This proves (0.2).

The condition \(h=0\) is important.  There is no extra outside-source factor
to divide from the complement-locator residue.  The occupied multiplier is
the actual monic split locator

\[
q_Y=\Lambda_Y,\qquad
Y\subseteq V=D\setminus\Sigma,\qquad
|Y|=j+x=981{,}105,
\tag{1.5}
\]

viewed in

\[
A_B=B[X]/(\Lambda_\Sigma).
\]

It is not a polynomial of degree \(e\).  Only its two source products have
degree at most \(e\).  This distinction is load-bearing below.

## 2. Complete reciprocal product matrix

Let

\[
W_B=\operatorname{span}_B\{q_Y:\ q_Y
\text{ occurs in the fixed packet}\}\subset A_B,
\qquad b=\dim_BW_B,
\tag{2.1}
\]

and choose a basis \(q_0,\ldots,q_{b-1}\).

Define the complete reciprocal space

\[
\mathcal R_b
=
\{v\in A_B:\ q_iv
\text{ has a degree-at-most-}e\text{ representative for every }i\}.
\tag{2.2}
\]

The translated source coordinates \(u_0,u_1\) belong to
\(F\otimes_B\mathcal R_b\).  After the active projective-base C5 deletion,
the relevant base reciprocal packet has dimension at least three.  Since
\(s<p\), the standard nonvanishing-combination lemma supplies

\[
v_0\in\mathcal R_b
\quad\text{with}\quad
v_0(\sigma)\ne0\quad(\sigma\in\Sigma).
\tag{2.3}
\]

For \(v\in\mathcal R_b\), let

\[
P_v(q_i)
=
\operatorname{rep}_{\le e}(q_iv)\in B[X]_{\le e}.
\tag{2.4}
\]

The complete product matrix has rows indexed by the \(q_i\) and columns
indexed by \(\mathcal R_b\).  At every source point all rows are scalar
multiples of the same reciprocal-value row, so its pointwise rank is at most
one.

If the complete polynomial rank is at least three, then the column
\(P_{v_0}\) can be extended by two reciprocal columns \(P_{v_1},P_{v_2}\)
and three rows to a nonsingular \(3\times3\) polynomial matrix

\[
\mathcal P(X).
\tag{2.5}
\]

Every \(3\times3\) minor has a double zero at each source point.  Its degree
is at most \(3e=2s\).  Hence

\[
\boxed{
\det\mathcal P=\kappa\Lambda_\Sigma^2,
\qquad \kappa\in B^\times.
}
\tag{2.6}
\]

This is the exact equality residue that replaces the strict vanishing used
before \(r=134{,}943\).

## 3. Constant adjugate reconstruction

Put

\[
\mathcal Q=\frac{\operatorname{adj}(\mathcal P)}{\Lambda_\Sigma}.
\tag{3.1}
\]

Every entry of the adjugate is a \(2\times2\) minor, hence is divisible by
\(\Lambda_\Sigma\).  Its quotient has degree at most

\[
2e-s=c.
\tag{3.2}
\]

Equation (2.6) gives

\[
\mathcal P\mathcal Q
=
\mathcal Q\mathcal P
=
\kappa\Lambda_\Sigma I_3.
\tag{3.3}
\]

Let \(\mathbf r\) be any further row of the same three-column product
matrix.  Each coordinate of
\(\mathbf r\operatorname{adj}(\mathcal P)\) is a signed \(3\times3\)
replacement minor.  It also has a double zero on \(\Sigma\).  Therefore

\[
\mathbf r\mathcal Q
=
\Lambda_\Sigma\mathbf a
\tag{3.4}
\]

for some polynomial row \(\mathbf a\).  The degree bound is

\[
\deg\mathbf a
\le
3e-2s=0,
\tag{3.5}
\]

so \(\mathbf a\in B^3\) is constant.  Multiplying (3.4) by \(\mathcal P\)
and using (3.3) yields

\[
\kappa\Lambda_\Sigma\mathbf r
=
\Lambda_\Sigma\mathbf a\mathcal P,
\]

and hence

\[
\boxed{\mathbf r=\kappa^{-1}\mathbf a\mathcal P.}
\tag{3.6}
\]

Apply (3.6) to the first column, which is
\(\operatorname{rep}_{\le e}(q_iv_0)\).  On \(\Sigma\), the source unit
\(v_0\) is nonzero, so the same constant coefficients give a relation among
the \(q_i\) in \(A_B\).  Thus every basis row lies in the constant span of
the three selected rows.  Since (2.5) has rank three,

\[
\boxed{b=3.}
\tag{3.7}
\]

The same equality argument also collapses the complete reciprocal space,
not only the occupied locator rows.  Let \(v\in\mathcal R_b\) be any further
reciprocal column and restrict its product column to the three rows used in
\(\mathcal P\).  Replacing one column of \(\mathcal P\) by this column gives
a \(3\times3\) minor with a double zero on \(\Sigma\) and degree at most
\(3e=2s\).  Each replacement determinant is therefore a scalar multiple of
\(\Lambda_\Sigma^2\).  Cramer's rule using (2.6) gives constants
\(\alpha_0,\alpha_1,\alpha_2\in B\) such that the restricted product column
equals

\[
\alpha_0P_{v_0}+\alpha_1P_{v_1}+\alpha_2P_{v_2}.
\tag{3.8}
\]

Put \(w=v-\sum_j\alpha_jv_j\).  The products \(q_iw\) vanish in \(A_B\) for
the three selected locator rows.  Every actual locator residue is a unit in
\(A_B\), because its roots lie in the disjoint carrier \(V\).  Hence already
one selected row gives \(w=0\) in \(A_B\).  The three selected columns are
independent because \(\det\mathcal P\ne0\).  Consequently

\[
\boxed{\dim_B\mathcal R_b=3.}
\tag{3.9}
\]

Thus rank three is a simultaneous row and column collapse.  No unselected
reciprocal direction remains available to enlarge a residue-line packet.

This is a field-uniform theorem.  It does not use a finite census.

## 4. Rank at most two is already paid

Suppose the complete reciprocal product matrix has polynomial rank
\(k_0\le2\).  Its saturated left kernel is a direct summand of
\(B[X]^b\) of rank \(b-k_0\).  A left-prime basis
\(\mathcal A(X)\) therefore satisfies

\[
\operatorname{rank}\mathcal A(x)=b-k_0
\quad(x\in\overline B)
\tag{4.1}
\]

and annihilates every reciprocal product column as a polynomial identity.
In particular it annihilates the two translated source-coordinate columns.
At every actual moving root, all occupied source-pair values consequently
lie in a \(B\)-subspace of \(F^2\) of dimension at most two.

There are at most \(p+1\) projective slopes at each moving root.  Summing over
the carrier gives

\[
\#\Gamma_{\operatorname{rank}\le2}
\le
(p+1)(n-s)
=
2{,}130{,}706{,}434\cdot1{,}894{,}736
=
\boxed{4{,}037{,}126{,}185{,}931{,}424}.
\tag{4.2}
\]

This is below the active reserve by

\[
\boxed{266{,}743{,}086{,}774{,}644{,}456}.
\tag{4.3}
\]

Unlike the strict sweep, this argument needs no no-wrap estimate: it uses the
complete reciprocal product matrix itself.

## 5. The exact rank-three locator cylinder

In the rank-three branch, let \(W_B\subset A_B\) be the three-dimensional
space from (3.7).  The actual locator set is

\[
\mathcal L(W_B)
=
\left\{
\Lambda_Y:
Y\subseteq V,\ |Y|=J,
[\Lambda_Y]_{\Lambda_\Sigma}\in W_B
\right\},
\qquad
J=981{,}105.
\tag{5.1}
\]

The carrier size is

\[
|V|=n-s=1{,}894{,}736.
\tag{5.2}
\]

Let

\[
\rho_J:B[X]_{\le J}\longrightarrow A_B
\]

be reduction modulo \(\Lambda_\Sigma\).  Since \(J\ge s\),

\[
\ker\rho_J
=
\Lambda_\Sigma B[X]_{\le J-s}
\]

has vector dimension \(J-s+1\).  Therefore

\[
\rho_J^{-1}(W_B)
\]

has vector dimension \(J-s+4\), or projective dimension

\[
\boxed{d_{\rm cyl}=J-s+3=778{,}692.}
\tag{5.3}
\]

Thus (5.1) is an intersection of the split-locator star configuration with
a growing-dimensional projective flat.  It is not an intersection with the
projective plane \(\mathbf P(W_B)\) in \(B[X]_{\le J}\).

### Route cut: why the projective-plane pair bound does not apply

The theorem `thm:capf-dim2` bounds a polynomial projective plane
\(\mathbf P(W)\subset\mathbf P(B[X]_{\le J})\).  Here only the residues of
the locators span a plane.  Their polynomial lifts can have larger span
because two lifts with the same prescribed residue may differ by a multiple
of \(\Lambda_\Sigma\).

In short, residue dimension three is not polynomial dimension three.

The deterministic finite regression in the certificate uses

\[
B=\mathbf F_{19},\quad
|\Sigma|=6,\quad e=4,\quad |V|=12,\quad J=8.
\]

It exhibits five admitted split locators whose residues have dimension
three, whose complete reciprocal product matrix has rank three, and whose
actual locator polynomials have dimension four.  Hence the implication

\[
\dim_B\operatorname{span}\{[\Lambda_Y]_{\Lambda_\Sigma}\}=3
\Longrightarrow
\dim_B\operatorname{span}\{\Lambda_Y\}=3
\]

is false even in the exact equality model.

## 6. From locator incidence to selected slopes

Inside one rebuilt selector, an actual complement locator determines its
root set \(Y\) and hence the common-zero set \(Z=V\setminus Y\) of its graph
line.  Every contributing scalar-unpaid graph line has
\(\beta_L>0\), so \(Z\) contains an independent eight-row basis \(B\).
The canonical basis reconstruction theorem gives one unique graph line
\(L_B\).  Therefore two contributing graph lines with the same monic
complement locator coincide.

The full-histogram moving-zero theorem at \(x_0\le0\) gives

\[
J_L\le j+1=981{,}105
\tag{6.1}
\]

for every contributing graph line.  Consequently,

\[
\boxed{
\#\Gamma_{\operatorname{rank}=3}
\le
981{,}105\,
|\mathcal L(W_B)|.
}
\tag{6.2}
\]

Dividing the active reserve by \(981{,}105\) gives

\[
\left\lfloor
\frac{270{,}780{,}212{,}960{,}575{,}880}
     {981{,}105}
\right\rfloor
=
\boxed{275{,}995{,}141{,}152}.
\tag{6.3}
\]

Equations (6.2)--(6.3) prove the reduction (0.4).

## 7. A sufficient local line theorem

The global incidence target admits a smaller local reduction.  Regard
\(\mathcal L(W_B)\) as a multiset on the projective residue plane
\(\mathbf P(W_B)\simeq\mathbf P^2(B)\): for a projective point \(P\), let
\(m_P\) be the number of actual monic locators whose nonzero residue has
projective class \(P\).  For a projective line \(\ell\), put

\[
M_\ell=\sum_{P\in\ell}m_P,
\qquad
M=\sum_Pm_P=|\mathcal L(W_B)|.
\tag{7.1}
\]

Suppose the following local estimate holds:

\[
\boxed{M_\ell\le130\quad\text{for every projective residue line }\ell.}
\tag{7.2}
\]

If \(M>0\), choose an occupied point \(P_0\).  The \(p+1\) projective lines
through \(P_0\) contain every other projective point exactly once and contain
\(P_0\) on every line.  Consequently,

\[
\sum_{\ell\ni P_0}M_\ell
=M+p\,m_{P_0}.
\tag{7.3}
\]

Since \(m_{P_0}\ge1\), equations (7.2)--(7.3) give

\[
\begin{aligned}
M
&\le130(p+1)-p\\
&=129p+130\\
&=\boxed{274{,}861{,}129{,}987}.
\end{aligned}
\tag{7.4}
\]

This is below the required locator cap (6.3) by

\[
\boxed{1{,}134{,}011{,}165}.
\tag{7.5}
\]

After the graph-line factor \(981{,}105\), the resulting slope charge is

\[
269{,}667{,}628{,}935{,}895{,}635,
\]

leaving reserve margin

\[
\boxed{1{,}112{,}584{,}024{,}680{,}245}.
\tag{7.6}
\]

Thus a weighted local residue-line cap of \(130\) is sufficient to pay the
entire rank-three equality packet.  A cap of \(131\) does not imply the
deployed global bound by this argument when the chosen point has weight one.

The number \(130\) also occurs in the repository's rank-16 fixed-pair
active-pencil theorem, but that theorem is not imported here.  Its endpoint
pair, complete-tail universe, row--column grid, and weighted-arrangement
contracts are different.  Reusing its numeric cap without a source-bound
identification of those objects would be circular.

The exact \(\mathbf F_{19}\) route-cut packet has five locator points and
maximum projective-line occupancy three.  This is a regression for (7.1),
not evidence of a uniform cap at the deployed scale.

## 8. Next theorem

The exact remaining statement is:

> **KoalaBear equality-wall residue-plane locator incidence.**  Uniformly
> for every actual rank-three packet at \(r=134{,}943\), with the source,
> carrier, selector, degree, reciprocal, coprime-row, and first-match
> contracts above,
> \[
> |\mathcal L(W_B)|
> \le275{,}995{,}141{,}152.
> \]

A stronger but more local sufficient target is:

> **KoalaBear equality-wall residue-line occupancy.**  Under the same
> deployed rank-three source and selector contracts, every projective
> two-dimensional subspace \(U\subset W_B\) satisfies
> \[
> \sum_{P\in\mathbf P(U)}m_P\le130.
> \]

Section 7 proves that this local theorem implies the required global
incidence bound with more than \(10^{15}\) slopes of reserve margin.

This is weaker than the full normalized Conjecture-F band theorem: it concerns
one deployed row, one equality degree, and a residue plane additionally
carrying the nonsingular reciprocal determinant (2.6).  It is stronger than
ordinary fixed-dimensional Conjecture F because the polynomial lift has
projective dimension \(778{,}692\).

Possible proof routes are:

1. **Rank-three exchange eliminant.**  Use (2.6) and the exact locator
   exchange \(Y\mapsto Y-\{a\}+\{b\}\) to show that too many admitted
   locators force a rank-two reciprocal packet.
2. **Johnson expansion with determinant rigidity.**  A family larger than
   (6.3) should have many short exchange paths.  Propagate the constant
   adjugate coordinates along those paths and emit common-GCD, quotient, or
   lower-rank structure.
3. **Finite rank-pivot atlas.**  Exploit the fixed deployed values
   \(s,J,|V|\) and the three reciprocal rows to produce exact eliminants whose
   total degree is below (6.3).
4. **Residue-cylinder local limit.**  Bound the intersection of the
   three-syndrome plane with the constant-weight split-locator image directly,
   retaining the active selector and monic-locator injection.

The finite experiments are diagnostics only:

* an exhaustive \(p=13,s=6,e=4\) small-cylinder census found genuine rank-two
  and rank-three equality packets;
* 20,000 deterministic \(p=17\) locator-cylinder seed triples and 5,000
  \(p=19\) triples found rank-three packets with up to five admitted locators;
* a randomized 2,000-triple \(p=23,s=9,e=6\) sample again found the exact
  rank-three collapse;
* among the stored detailed rank-three representatives, all projective
  residue-point fibers were singleton; maximum weighted projective-line
  occupancy was two for the \(p=17\) and \(p=23\) packets and three for the
  \(p=19\) packets;
* low-exchange components at Johnson threshold \(c\) had size as large as
  four, so the local line target cannot be justified by assuming pairwise
  distance above \(c\);
* rank-two packets can contain more locators and are paid by Section 4.

None of these finite maxima is asserted uniformly.

## 9. Scope

This packet proves:

* exact isolation of the equality stratum at \(r=134{,}943\);
* the rank-at-most-two direct payment;
* the rank-three constant-adjugate reconstruction;
* occupied residue dimension exactly three in the rank-three branch;
* complete reciprocal dimension exactly three in the rank-three branch;
* the exact growing locator cylinder and the required deployed incidence cap;
* the route cut against using the polynomial projective-plane theorem.

It does not:

* prove the incidence cap (6.3);
* pay \(r=134{,}943\);
* move the first open interval;
* add or reorder an owner;
* change the partition digest or reserve;
* prove the normalized Conjecture-F band.

# PROVED REDUCTION / ROW OPEN
