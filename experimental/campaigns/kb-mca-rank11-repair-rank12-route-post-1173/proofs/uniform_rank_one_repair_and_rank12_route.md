# Raw-low repair of KoalaBear affine error rank eleven

## 1. Exact interface

Write

\[
 R=n-K=1{,}048{,}576,\qquad d=m-K=67{,}472,
\]

so every complete shortening row is

\[
 (n_K,K,m_K)=(R+K,K,d+K).
\]

The conditional intrinsic near-rational deletion supplies at most
134,944 slopes.  The unsafe post-near load is therefore

\[
 L_{\rm unsafe}=B_*-134944+1
 =274{,}980{,}728{,}111{,}260{,}144. \tag{1}
\]

For a selected explanation family in an affine translate of a direction
subcode \(C'\) of dimension at most \(s\), retain one exact bad support,
explanation, and minimizing direction \(b_\gamma\) for every slope.  The
proved support resource controls the truncated margin

\[
 \theta_\gamma=\min\{d+1,\widetilde\theta_\gamma\},\qquad
 \widetilde\theta_\gamma=
 |\{x\in S_\gamma:r_1(x)\ne b_\gamma(x)\}|,
\]

and gives

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

The earlier unsubmitted descent used \(\theta\) as the raw mismatch.  That
is false when truncation is active.  The repaired argument uses only the
raw-low class for a cutoff \(T\le d\).

## 2. Raw-low heavy-core theorem

At most

\[
 H_s(K,T)=\left\lfloor C_s(K)/(T+1)\right\rfloor \tag{4}
\]

records have raw margin exceeding \(T\).  Every remaining pair core contains
at least \(d+K-T\) coordinates of the selected support.  Thus a family of
size \(L\) has a coordinate incident with at least

\[
 I_s(K,L,T)=
 \left\lceil
 \frac{(L-H_s(K,T))_+(d+K-T)}{R+K}
 \right\rceil \tag{5}
\]

raw-low pair cores.

Fix an incident base pair \(e_0=(a_0,b_0)\) and put

\[
 U_x=\operatorname{span}\{a_\gamma-a_0,b_\gamma-b_0:
 x\in H_\gamma\}\le C'. \tag{6}
\]

All generators vanish at \(x\).

- If \(U_x<C'\), subtract \(e_0\), divide by \(X-x\), and delete \(x\).
  The incident explanations lie in \(U_x\), giving a source-bound child of
  direction dimension at most \(s-1\).
- If \(U_x=C'\), every word in \(C'\) vanishes at \(x\).  Differences of
  every selected pair lie in \(C'\), so every pair agrees with the received
  pair at \(x\).  The whole family shortens without losing a slope.
- At \(K=s\), the second case is impossible because
  \(C'=\mathbb F[X]_{<s}\) contains \(1\).

The lift uses complete scalar agreement domains.  Any shortened pair
explanation lifts by multiplying by \(X-x\) and adding \(e_0\).  Pair
noncontainment and post-near status are therefore preserved.  An exact bad
support in the child follows from Reed--Solomon uniqueness on adjacent
subsets and connectedness of the Johnson graph.

Equivalently, the least parent load forcing a target child load \(M\) is

\[
 \Lambda_s(K;M,T)=
 H_s(K,T)+
 \left\lfloor\frac{(M-1)(R+K)}{d+K-T}\right\rfloor+1. \tag{7}
\]

## 3. Uniform rank-one base

For a rank-one direction polynomial \(P\), delete universal roots and put
\(j=K-u\).  Nonroot coordinates become affine graph lines in the parameter
plane; nonuniversal roots become vertical projective lines.  Merge identical
lines with their coordinate weights.

The low branch charges cross-class coordinate pairs.  The high branch has a
unique dominant line and reduces exactly to endpoint deficiencies
\(a_i\in\{1,q\}\).  The complete scan over
\(1\le j\le1{,}048{,}576\) gives

\[
 |Z_1|\le4{,}070{,}947. \tag{8}
\]

The maximum occurs at \(j=1\), with low contribution \(483\) and high
contribution \(4{,}070{,}464\).

## 4. Corrected rank-eleven induction

Set \(L_1=4{,}070{,}948\).  Use the following fixed raw cutoffs:

\[
\begin{array}{c|r|r|r|r}
s&T_s&L_{s-1}&L_s&\arg\max K\\ \hline
2&515&4070948&64241811&2\\
3&511&64241811&1013639041&3\\
4&507&1013639041&15991635730&4\\
5&503&15991635730&252259306484&5\\
6&499&252259306484&3978753104997&6\\
7&496&3978753104997&62747001947996&7\\
8&492&62747001947996&989431810807346&8\\
9&489&989431810807346&15600062750954861&9\\
10&485&15600062750954861&248706399341288370&1048576
\end{array} \tag{9}
\]

For every row, the release verifier checks all integers \(s\le K\le R\)
and proves

\[
 \Lambda_s(K;L_{s-1},T_s)\le L_s. \tag{10}
\]

Induction on \(s\) now closes.  A proper heavy-core span produces a child
with at least \(L_{s-1}\) slopes.  A full span shortens the whole family and
cannot persist through \(K=s\).  The base contradicts (8).

Finally,

\[
 L_{\rm unsafe}-L_{10}
 =26{,}274{,}328{,}769{,}971{,}774>0. \tag{11}
\]

Thus the direct post-near affine-error-rank-eleven branch is paid, conditional
only on the separately pinned near-rational deletion.

## 5. Guarded dense-core theorem

For a raw cutoff \(T\le d\), the low records have cores of size at least
\(h=d+K-T\).  Distinct pair cores meet in at most \(K-1\) coordinates.
Cauchy therefore bounds the number of represented raw-low pair types by

\[
 Q(K,T)=\max\left\{
 \left\lceil\frac n{2h}\right\rceil-1,
 \left\lfloor\frac{n(h-K+1)}{h^2-(K-1)n}\right\rfloor
 \right\},
\]

when the denominator is positive.  Fixed-pair exception sets are disjoint,
so a pair owns at most \(981{,}105\) slopes.  Hence

\[
 |Z_s|\le \left\lfloor\frac{C_s(K)}{T+1}\right\rfloor
+981105\,Q(K,T). \tag{12}
\]

This theorem is valid only with the raw-margin definition and \(T\le d\).

## 6. Exact rank-twelve method wall

Apply (7) at the initial rank-twelve row \(s=11,K=R\), targeting the paid
rank-ten threshold \(L_{10}\).  Scanning all \(67{,}472\) cutoffs gives

\[
 \min_T\Lambda_{11}(R;L_{10},T)
 =546{,}519{,}697{,}764{,}383{,}119, \tag{13}
\]

uniquely at \(T=d\).  This exceeds the available unsafe load by

\[
 271{,}538{,}969{,}653{,}122{,}975. \tag{14}
\]

Therefore the repaired single-threshold mechanism pays rank eleven but does
not begin the rank-twelve descent.  The previous \(8{,}681{,}730\)
descendant and \(279{,}911\) endpoint wall are withdrawn: they came from the
invalid truncated-to-raw recurrence, and the latter also described only the
exactly-three-deficiency-one histogram.

## 7. Boundary

Proved:

- complete-agreement locator shortening and the pair-difference-span
  dichotomy;
- the uniform rank-one cap \(4{,}070{,}947\);
- the raw-low rank-eleven payment with slack
  \(26{,}274{,}328{,}769{,}971{,}774\);
- the guarded dense-core pair-type theorem;
- the exact single-threshold rank-twelve method wall.

Not proved:

- an affine-error-rank-twelve payment or descendant;
- active-v4 chronology or any ledger movement;
- KoalaBear or prize closure.

The next rank-twelve theorem must couple multiple raw-margin levels, exploit
cross-pair/core structure, or construct a chronology-correct owner.
