# Uniform rank-one repair and dense-core route for KoalaBear ranks eleven and twelve

## 1. Scope and exact interface

Write

\[
 R=n-K=1{,}048{,}576,\qquad d=m-K=67{,}472,
\]

so every complete shortening row has parameters

\[
 (n_K,K,m_K)=(R+K,K,d+K).
\]

The deployed budget and the disjoint near-rational charge are

\[
 B_*=274{,}980{,}728{,}111{,}395{,}087,
 \qquad N_{\rm near}=134{,}944.
\]

The exact unsafe post-near load is therefore

\[
 L_{\rm unsafe}=B_*-N_{\rm near}+1
 =274{,}980{,}728{,}111{,}260{,}144. \tag{1}
\]

For a selected explanation family in an affine translate of a direction
subcode \(C'\) of dimension at most \(s\), freeze one exact bad support and one
minimizing direction for every slope.  The pointwise support-margin theorem
gives

\[
 \sum_\gamma\theta_\gamma\le C_s(K), \tag{2}
\]

where

\[
 C_s(K)=\left\lfloor\max\left\{
 \frac{(R+K)^{\underline{s+1}}}
      {(d+K)(d+1)^{\overline{s-1}}},
 \frac{(R+s)^{\underline{s+1}}}
      {(d+1)^{\overline s}}
 \right\}\right\rfloor. \tag{3}
\]

For the corresponding minimizing pair \(e_\gamma=(a_\gamma,b_\gamma)\), put

\[
 H_\gamma=\{x:r_0(x)=a_\gamma(x),\ r_1(x)=b_\gamma(x)\}.
\]

On the selected support, scalar agreement and \(r_1=b_\gamma\) force
\(r_0=a_\gamma\).  Hence

\[
 |H_\gamma|\ge d+K-\theta_\gamma. \tag{4}
\]

The complete-agreement shortening and pair-difference-span dichotomy from the
predecessor stack will be used repeatedly:

* a proper incident pair-difference span shortens one coordinate and lowers
  direction dimension;
* a full incident span makes the coordinate a whole-family pair-core
  coordinate and shortens the complete family without losing a slope.

Minimizing pairs are refrozen after every shortening.

## 2. The gap in the first global-core draft

The earlier unsubmitted candidate
`d01c546f4dca70e256c18c142873821b3bb48ab5` correctly proved the heavy-core
dichotomy and the displayed load recurrence, but its written induction jumped
from an early rank drop to the final \(K=1\) rank-one cap without proving that
the intervening rank-one family could be transported to \(K=1\) intact.

That implication is not automatic: at \(K>1\), a rank-one family can first
drop to a rank-zero parallel star.  The repair below is a cap for the complete
rank-one family that is uniform in the ambient shortened dimension.  Once
that theorem is installed, the descent induction is valid.

## 3. Uniform weighted-line theorem for rank one

Let the current direction code be \(C'=\langle P\rangle\), with
\(0\ne P\in\mathbb F[X]_{<K}\).  After choosing a base pair, every pair type
has the form

\[
 (a_e,b_e)=(a_*,b_*)+(\alpha_eP,\beta_eP).
\]

For a coordinate with \(P(x)\ne0\), divide its affine error equation by
\(P(x)\).  In the parameter plane with coordinates \((\gamma,z)\), the
coordinate becomes an affine graph line

\[
 z=A_x+\gamma B_x,
\]

while a pair type becomes the graph line

\[
 z=\alpha_e+\gamma\beta_e.
\]

If \(P(x)=0\), then either the affine error vanishes identically, in which
case the coordinate is a universal pair-core coordinate, or the agreement
condition is a vertical line in the same projective parameter plane.
Identical lines are merged while retaining coordinate multiplicity.

Let \(u\) be the universal weight.  Since \(u\) is supported on the roots of
\(P\),

\[
 0\le u\le K-1.
\]

After deleting that universal core, put

\[
 j=K-u,\qquad n'=R+j,\qquad m'=d+j. \tag{5}
\]

Every selected parameter point is incident to weighted line mass at least
\(m'\).  Pair noncontainment says its exact support contains at least two
distinct line classes.

### Lemma 3.1 (weighted projective-line cap)

For \(n'\ge m'\ge2\), put

\[
 q=\left\lfloor\frac{m'}2\right\rfloor.
\]

The number of selected finite parameter points is at most

\[
 W(n',m')=W_{\rm low}(n',m')+W_{\rm high}(n',m'), \tag{6}
\]

where

\[
 W_{\rm low}
 =\left\lfloor\frac{\binom{n'}2}{q(m'-q)}\right\rfloor, \tag{7}
\]

and

\[
 W_{\rm high}
 =\max_{\substack{1\le t\le\lfloor n'/(q+1)\rfloor\\
                  a_i\in\{1,q\}\\
                  n'-tm'+\sum_i a_i\ge0}}
 \left\lfloor
 t(t-1)+
 \left(n'-tm'+\sum_i a_i\right)\sum_i\frac1{a_i}
 \right\rfloor. \tag{8}
\]

#### Proof

If no line class contributes more than \(q\) coordinates to an exact
\(m'\)-support, the support contains at least \(q(m'-q)\) unordered pairs
from different classes.  Two distinct projective lines meet at at most one
point, so these cross-pair charges are disjoint across selected points.  This
gives (7).

Otherwise there is a unique dominant class.  Let the globally distinct lines
capable of dominating have weights \(w_i\), \(1\le i\le t\).  Then
\(w_i\ge q+1\), so \(t\le\lfloor n'/(q+1)\rfloor\).  Define

\[
 a_i=\max\{1,m'-\min(w_i,m'-1)\},\qquad 1\le a_i\le q,
\]

and

\[
 W_0=n'-\sum_i(m'-a_i).
\]

A point charged to line \(i\) requires at least \(a_i\) coordinates from
other line classes.  At most \(t-1\) charged points lie on another dominant
line.  Every remaining charged point consumes non-dominant line weight, and
those weights are disjoint along a fixed line.  Thus

\[
 N_i\le t-1+\left\lfloor\frac{W_0}{a_i}\right\rfloor.
\]

Summing gives the objective in (8), before endpoint reduction.

Hold all variables but one \(a_i\) fixed.  With

\[
 C_0=n'-tm'+\sum_{j\ne i}a_j,\qquad
 Q_0=\sum_{j\ne i}\frac1{a_j},
\]

the variable part is

\[
 f(a)=(C_0+a)(Q_0+1/a).
\]

If \(C_0\ge0\), then \(f''(a)=2C_0/a^3\ge0\), so a maximum is at an
endpoint.  If \(C_0<0\), then \(f'(a)=Q_0-C_0/a^2>0\), so moving to
\(a=q\) increases the objective and preserves feasibility.  Iteration gives
\(a_i\in\{1,q\}\), proving (8).  The low and high cases are disjoint. ∎

### Exact deployed uniformity

Evaluate (6) at

\[
 (n',m')=(R+j,d+j),\qquad 1\le j\le1{,}048{,}576.
\]

An exact integer scan gives

\[
 \max_j W(R+j,d+j)=W(R+1,d+1)=4{,}070{,}947. \tag{9}
\]

At \(j=1\),

\[
 W_{\rm low}=483,\qquad
 W_{\rm high}=4{,}070{,}464,
\]

and the high extremizer is \(t=8\), with all eight effective deficiencies
equal to one.  The scan has no increase: there are \(423{,}092\) strict
decreases and \(625{,}483\) equal adjacent values.  Therefore every rank-one
family on every shortened row satisfies

\[
 |Z_1|\le4{,}070{,}947. \tag{10}
\]

This is the missing uniform base case.

## 4. Corrected rank-eleven payment

For \(2\le s\le10\), define recursively

\[
 L_{10}=L_{\rm unsafe},\qquad
 L_{s-1}=
 \left\lceil
 \frac{L_s(d+s)-C_s(s)}{R+s}
 \right\rceil. \tag{11}
\]

Exact evaluation gives

\[
\begin{array}{c|r|r}
s&C_s(s)&L_{s-1}\\ \hline
10&861057176799343503&17695628624859819\\
9&55413538236037195&1138737729126327\\
8&3566101912297072&73278302796469\\
7&229490967859328&4715427489703\\
6&14768331186162&303431536894\\
5&950366735057&19525148223\\
4&61156835934&1256382675\\
3&3935435218&80843204\\
2&253241283&5201865
\end{array} \tag{12}
\]

For every row in (12), the exact verifier checks all integers \(s\le K\le R\)
and proves

\[
 I_s(K,L_s):=
 \left\lceil\frac{L_s(d+K)-C_s(K)}{R+K}\right\rceil
 \ge L_{s-1}. \tag{13}
\]

We now induct on \(s\).  The case \(s=1\) is (10), since

\[
 L_1=5{,}201{,}865>4{,}070{,}947.
\]

For exact direction dimension \(s\), use a heavy coordinate.  A proper span
produces a family of dimension at most \(s-1\) and load at least
\(I_s(K,L_s)\ge L_{s-1}\), contradicting the induction hypothesis.  A full
span shortens the entire family and preserves its load and dimension.  It
cannot persist through \(K=s\), because the complete degree-\(<s\) code
contains the constant polynomial \(1\).  Thus a proper span eventually
occurs and gives the contradiction.

This proves, uniformly over all shortening histories,

\[
 \boxed{\text{the complete affine-error-rank-eleven branch is paid}.} \tag{14}
\]

The slack at the uniform base case is

\[
 5{,}201{,}865-4{,}070{,}947=1{,}130{,}918. \tag{15}
\]

## 5. Dense-core pair-type bound

The rank-twelve attack needs an additional population theorem.

Fix a cutoff \(T\), and let the low records be those with
\(\theta_\gamma\le T\).  Every represented low pair type has a core of size
at least

\[
 h=d+K-T. \tag{16}
\]

For distinct pair types \(e\ne f\),

\[
 |H_e\cap H_f|\le K-1, \tag{17}
\]

because a common coordinate is a common root of the two degree-\(<K\) pair
differences, not both zero.

Put

\[
 n=R+K,\qquad \lambda=K-1.
\]

Let \(t\) be the number of represented low pair types and let \(r_x\) be the
number of their cores containing coordinate \(x\).  With
\(S=\sum_xr_x\ge th\),

\[
 \sum_xr_x^2
 =S+2\sum_{e<f}|H_e\cap H_f|
 \le S+\lambda t(t-1). \tag{18}
\]

Cauchy gives \(S^2\le n\sum_xr_x^2\).  If
\(t<\lceil n/(2h)\rceil\), this already bounds \(t\).  Otherwise \(th\ge n/2\),
and \(z^2/n-z\) is increasing for \(z\ge n/2\).  Combining with (18) yields

\[
 t\le
 \left\lfloor\frac{n(h-\lambda)}{h^2-\lambda n}\right\rfloor
\]

whenever \(h^2>\lambda n\).  Therefore

\[
 Q(K,T)=
 \max\left\{
 \left\lceil\frac n{2h}\right\rceil-1,\,
 \left\lfloor\frac{n(h-\lambda)}{h^2-\lambda n}\right\rfloor
 \right\}. \tag{19}
\]

For one fixed pair type, put
\(\delta=\max\{1,m_K-|H_e|\}\).  The exception sets outside \(H_e\) owned by
distinct slopes are disjoint, and each has at least \(\delta\) coordinates.
Thus one pair owns at most

\[
 \left\lfloor\frac{n-|H_e|}{\delta}\right\rfloor
 \le R-d+1=981{,}105. \tag{20}
\]

The high-margin records number at most \(\lfloor C_s(K)/(T+1)\rfloor\).
Consequently, when the denominator in (19) is positive,

\[
 |Z_s|
 \le D_s(K,T):=
 \left\lfloor\frac{C_s(K)}{T+1}\right\rfloor
 +Q(K,T)\cdot981{,}105. \tag{21}
\]

## 6. Rank-twelve barrier descent

Start with direction dimension \(11\) and load \(L_{11}=L_{\rm unsafe}\).
Set

\[
 b_s=4280+s-3\qquad(3\le s\le11), \tag{22}
\]

and use \(T_s=249\) for \(4\le s\le11\), while \(T_3=380\).

At rank \(s\), whole-family shortening may continue while \(K>b_s\).  If it
reaches \(K=b_s\), (21) is strictly below the current load.  Therefore a
survivor must undergo a proper rank drop at some \(K\ge b_s+1\).  The exact
all-dimension scan proves that the child load is at least the next value in
the following table.

\[
\begin{array}{c|r|r|r|r|r}
s&b_s&T_s&L_s&Q(b_s,T_s)&D_s(b_s,T_s)\\ \hline
11&4288&249&274980728111260144&117&53518270603563833\\
10&4287&249&18729383598438495&117&3444228821986659\\
9&4286&249&1275719855410716&117&221654267733433\\
8&4285&249&86895415230834&117&14264522438473\\
7&4284&249&5918985683045&117&918078660722\\
6&4283&249&403186331995&117&59188114029\\
5&4282&249&27464496807&116&3915275120\\
4&4281&249&1870872170&116&358435523\\
3&4280&380&127444922&119&127080721
\end{array} \tag{23}
\]

The corresponding next-rank loads are

\[
\begin{array}{c|r}
\text{new rank}&\text{forced load}\\ \hline
10&18729383598438495\\
9&1275719855410716\\
8&86895415230834\\
7&5918985683045\\
6&403186331995\\
5&27464496807\\
4&1870872170\\
3&127444922\\
2&8681730
\end{array} \tag{24}
\]

The smallest barrier slack is \(364{,}201\), at rank three.

Hence every over-budget affine-error-rank-twelve line produces a source-bound
descendant of direction dimension at most two, ambient dimension at least
\(4280\), and at least

\[
 \boxed{8{,}681{,}730}
\]

distinct post-near slopes.  If the actual descendant dimension is at most
one, (10) already contradicts this load.  Thus the immediate survivor has
exact direction dimension two.

## 7. Exact rank-two endpoint wall

A rank-two survivor may either drop to rank one before reaching \(K=2\), or
shorten with full span to the complete \(K=2\) row.  Monotonicity gives a
rank-one descendant load of at least

\[
 I_2(2,8{,}681{,}730)=558{,}412, \tag{25}
\]

which is below the sharp uniform rank-one cap and is therefore a genuine
residual.

If full rank two persists to \(K=2\), use cutoff

\[
 T=1922.
\]

Then

\[
 \left\lfloor\frac{C_2(2)}{1923}\right\rfloor=131{,}690
\]

high-margin slopes remain, so the low family has at least

\[
 8{,}681{,}730-131{,}690=8{,}550{,}040 \tag{26}
\]

slopes.  Formula (19) gives at most fifteen low pair types.  Since one pair
has capacity at most

\[
 c_\delta=
 \left\lfloor\frac{981{,}104+\delta}{\delta}\right\rfloor,
\]

there must be at least nine pair types.  Moreover,

\[
 c_1=981{,}105,\qquad c_2=490{,}553,
\]

and two deficiency-one types plus thirteen types of deficiency at least two
cannot carry (26).  Therefore at least three represented pair types satisfy

\[
 |H_e|\ge m_2-1=67{,}473. \tag{27}
\]

The strongest independent-capacity relaxation is

\[
 3c_1+12c_2=8{,}829{,}951. \tag{28}
\]

It exceeds the required low load by only

\[
 8{,}829{,}951-8{,}550{,}040
 =279{,}911. \tag{29}
\]

Thus the exact remaining rank-two theorem is now small and source-specific:
prove a cross-pair compatibility saving of \(279{,}912\) slopes, or route the
near-saturated pair-core atlas to an already-paid rank-one anticode/rational
owner.  Summing the fifteen independent fixed-pair capacities is the first
unproved implication.

## 8. Literature and method boundary

The closest primary literature found in the targeted search is Rudnev and
Wheeler's incidence theory for Möbius hyperbolae and the multiplicative
subgroup intersection work of Shkredov and collaborators.  Those results do
not directly supply (29): the complete pair cores are arbitrary subsets of
the deployed evaluation subgroup, the slope field is the sextic extension,
and the fifteen ratio maps are coupled through one received pair.  No
external theorem is imported.

The remaining attack should work with the simultaneous ratio maps

\[
 \rho_e(x)=-
 \frac{r_0(x)-a_e(x)}{r_1(x)-b_e(x)}
\]

and prove that twelve near-perfect two-fiber matchings cannot coexist unless
the pair matrices enter one of the already-paid rank-one anticode geometries.
That is the first precise unproved implication after this packet.

## 9. Claims and nonclaims

This packet proves:

* the uniform rank-one weighted-line theorem;
* the corrected, history-uniform payment of affine error rank eleven;
* the dense-core pair-type theorem;
* the rank-twelve descent to the exact rank-one/rank-two residual above.

It does not pay affine error rank twelve, regenerate the active-v4 first-match
ledger, move a ledger atom, or close KoalaBear.
