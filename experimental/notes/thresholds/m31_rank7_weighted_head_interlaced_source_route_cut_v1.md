---
workboard_item: M1/L
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: Exact agreement-weight, full-projective-line deletion, planted-root source-lift, per-label dual-domain, and cofactor-weight theorems strengthen the rank-seven effective-deficit frontier. The dual-domain compiler pays every Q=26193 head distribution and proves a sharp method route cut at the Q=26194 outer maximizer. A separate deployed source construction realizes a rank-seven mixed-G interlaced family of eight codewords with exact lcm and full gcds and no complete T32/T2048 agreement or error fiber.
architecture: M31_RANK7_WEIGHTED_HEAD_INTERLACED_SOURCE_V1
atom_or_cell: Source-bound rank-seven route cut; no v4 atom value and no signed Xi_46 payment.
quantifier: Every rank-at-most-seven shallow master-denominator family for the two weighted theorems; one existential deployed received word for the eight-codeword obstruction.
projection_and_unit: Distinct LIST codewords per received word. Histograms and cofactor slices are explicitly labeled integer marginals.
claimed_bound: Weighted heads, a rank-seven full-line recurrence, a source-impossible one-level endpoint marginal, an all-distribution Q=26193 dual-domain head of 15775776, a sharp Q=26194 method route cut, a proper fixed-G moderate cap, and an eight-codeword source lower floor. No row upper bound.
status: PROVED LOCAL THEOREMS AND DEPLOYED SOURCE OBSTRUCTION / GLOBAL ROW OPEN
impact: ROUTE_CUT / LOWER_FLOOR_8 / NO_LEDGER_MOVEMENT
falsifier: A violation of either weighted double count; a legal projective-line partition exceeding a certified source-lift or dual-domain head; a Q=26194 legal split below the seven-interval lower cover; an exact arithmetic mismatch; failure of the pairwise CRT source construction; a complete T32/T2048 fiber in one certified support; or promotion of the remaining cofactor relaxation to a source family.
replay: Exact Python, optimized parity, semantic mutations, independent Sage arithmetic and direct finite-field source control, canonical JSON/hash checks, and fail-closed packet replay.
---

# M31 rank-seven weighted-head and interlaced-source route cut

## Status

This packet proves seven local statements.

1. The one-pivot compiler retains each member's actual \(E_0\)-agreement:
   \[
   \sum_{\delta_i\le Q}(g-\delta_i)\le R B_6(Q).
   \]
2. Exact full-projective-line deletion gives a rank-by-rank recurrence and
   a linear-time safe compiler through rank seven.
3. On the one-level specialization \(q_i=\delta_i=26\,144\), the
   planted-root lift lowers the exhaustive top-six head to
   \(15\,345\,533\), so that entire declared marginal is source-impossible.
4. A per-normalized-label two-domain split pays the complete
   \(Q=26\,193\) head and proves that the same method cannot improve the
   load-bearing \(Q=26\,194\), \(k=3\,145\) class.
5. A planted-zero cofactor pivot gives:
   \[
   \sum_{\delta_i\le Q}q_i\le g\Phi_Q(g).
   \]
6. Proper fixed-\(G\) moderate slices obey an exact cap \(F_q(g)\).
7. At the endpoint \(g=354\,972\), there exists an actual base-field,
   hence deployed target-field, received word with the zero anchor and seven
   linearly independent mixed-\(G\) companions.  Every certified agreement
   and error support is interlaced across the ambient \(T_{32}\) and
   \(T_{2048}\) fibers.

The weighted theorem invalidates the predecessor packet's particular
\(H_Q\)-saturated endpoint marginal.  The source lift invalidates the
strongest declared single-level replacement.  The dual-domain theorem then
handles all deficit/cofactor distributions through \(Q=26\,193\).  This
does not close rank seven: the adjacent \(Q=26\,194\) primitive class
requires an incidence mechanism beyond one per-label two-domain split.

The source construction has only eight certified codewords.  It is a sharp
adapter obstruction and lower floor, not a forbidden-size list.

## 1. Deployed source normalization

The exact parameters are

\[
\begin{aligned}
p&=2^{31}-1,& n&=2^{21},& K&=2^{20},\\
a&=1\,116\,023,&R&=981\,129,&w&=67\,447,\\
B_*&=16\,777\,215,&L&=15\,775\,933.
\end{aligned}
\tag{1.1}
\]

Here \(L=B_*-1\,001\,282\) is the shallow nonanchor count forced by a
hypothetical forbidden row after the proved deep-tail cap.

For one selected shallow family put

\[
P=\operatorname{lcm}_iG_i,\qquad g=\deg P,\qquad d=g-w,
\tag{1.2}
\]

\[
Q_i=P/G_i,\qquad f_i=Q_i b_i,
\tag{1.3}
\]

and

\[
H_i=\gcd(L_0,Y-f_i),\qquad
\delta_i=q_i-s_i=g-\deg H_i,\qquad q_i=\deg Q_i.
\tag{1.4}
\]

The normalized span

\[
\mathcal W=\operatorname{span}\{f_i\}
\subseteq\mathbb F_p[X]_{<d}
\tag{1.5}
\]

has dimension at most seven.  It has no common zero on \(Z(P)\).  On
\(E_0=Z(L_0)\), the received table is the nowhere-zero table

\[
u=P/V
\tag{1.6}
\]

and

\[
\operatorname{agr}_{E_0}(f_i,u)=g-\delta_i.
\tag{1.7}
\]

These are imported source identities, not support relaxations.

## 2. Exact agreement-weight pivot theorem

### Theorem 2.1

Let \(E\) be \(N\) distinct field points,
\(\mathcal W\subseteq\mathbb F[X]_{<d}\) a \(k\)-dimensional linear
space, and \(u:E\to\mathbb F^\times\) nowhere zero.  Let \(Z\) be the
common-zero set of \(\mathcal W\), \(z=|Z|\), and put

\[
\mathcal I_m=\{f\in\mathcal W:
\operatorname{agr}_E(f,u)\ge m\},
\qquad m=d+v\le N-z.
\tag{2.1}
\]

Then

\[
\boxed{
\sum_{f\in\mathcal I_m}\operatorname{agr}_E(f,u)
\le (N-z)B_{k-1}(z)}
\tag{2.2}
\]

where

\[
B_{k-1}(z)=
\left\lfloor
\frac{\binom{N-d+k-1}{k-1}}
     {\binom{v+z+k-1}{k-1}}
\right\rfloor.
\tag{2.3}
\]

### Proof

Divide every member by the locator \(L_Z\).  All points of \(Z\) are fixed
mismatches because \(u\) is nowhere zero.  On \(E\setminus Z\), for each
pivot \(x\), the slice

\[
\{f:f(x)=u(x)\}
\tag{2.4}
\]

is empty or an affine flat with direction dimension at most \(k-1\).
The recursive affine-span compiler on the punctured domain bounds this
slice by (2.3).  Count the exact pairs

\[
(f,x),\qquad f\in\mathcal I_m,\quad f(x)=u(x).
\tag{2.5}
\]

The left count is the sum in (2.2), not merely
\(m|\mathcal I_m|\).  The pivot count is at most
\((N-z)B_{k-1}(z)\).  This proves (2.2).

Weakening to \(z=0\) and \(k=7\), then substituting

\[
N=R,\qquad d=g-w,\qquad m=g-Q,\qquad v=w-Q,
\tag{2.6}
\]

gives

\[
\boxed{
\sum_{\delta_i\le Q}(g-\delta_i)
\le
R\left\lfloor
\frac{\binom{R-g+w+6}{6}}
     {\binom{w-Q+6}{6}}
\right\rfloor.}
\tag{2.7}
\]

The legal range is

\[
\max(g-R,-366\,886)
\le Q\le\min(w,g-w-1).
\tag{2.8}
\]

The old \(H_Q\) cap follows by replacing every summand by \(g-Q\).
Equation (2.7) is strictly stronger for a distribution over several
deficits.

### Theorem 2.2 (full projective-line deletion recurrence)

The exact source geometry gives a stronger recurrence than repeated
single-coordinate pivots.  Let

\[
\mathcal A=f_0+\mathcal V\subseteq\mathbb F[X]_{<K}
\]

be an affine flat whose direction \(\mathcal V\) has exact rank \(r\)
and no common zero on an \(N\)-point domain.  The received table may now
have zero labels.  Let

\[
\mathsf E_r(N,K,m)
\]

denote the largest possible number of members having at least \(m\)
agreements when the direction has **exact** rank \(r\), and put

\[
\mathsf C_r(N,K,m)=\max_{0\le j\le r}\mathsf E_j(N,K,m),
\qquad \mathsf E_0\le1.
\tag{2.9}
\]

For \(r=1\), distinct members have disjoint agreement supports: their
difference is a nonzero multiple of a direction polynomial that vanishes
nowhere on the domain.  Hence

\[
\mathsf E_1(N,K,m)=\mathsf C_1(N,K,m)
=\left\lfloor\frac Nm\right\rfloor.
\tag{2.10}
\]

For \(r\ge2\), group the nonzero evaluation functionals

\[
\operatorname{ev}_x|_{\mathcal V}\in\mathbb P(\mathcal V^*)
\]

by projective line.  Suppose one line contains \(s\) coordinates.  After
choosing a representative functional, its agreement equations partition
into normalized-label subclasses of sizes \(c_j\), with
\(\sum_jc_j=s\).  A fixed subclass cuts the direction to a rank at most
\(r-1\) kernel.  That kernel vanishes at every one of the \(s\)
coordinates in the full projective line, and nowhere else.  Deleting the
line and dividing by its locator therefore gives parameters

\[
(N,K,m)\longmapsto(N-s,K-s,m-c_j).
\tag{2.11}
\]

Monotonicity in the agreement threshold permits \(c_j\) to be replaced
by \(s\).  Thus the entire line contributes at most

\[
s\,\mathsf C_{r-1}(N-s,K-s,m-s)
\tag{2.12}
\]

agreement pairs.

If the projective-line sizes are sorted
\(s_1\ge s_2\ge\cdots\), then

\[
\sum_{i=1}^k s_i\le K-r+k,\qquad1\le k\le r-1.
\tag{2.13}
\]

Indeed, the intersection of \(k\) corresponding kernel hyperplanes has
rank at least \(r-k\), vanishes on the union of those lines, and after
division embeds into \(\mathbb F[X]_{<K-\sum_{i\le k}s_i}\).  Since the
parts are positive, all the inequalities in (2.13) are equivalent to

\[
\sum_{i=1}^{r-1}s_i\le K-1.
\tag{2.14}
\]

Counting exact agreement pairs gives the source-bound recurrence

\[
\boxed{
\mathsf E_r(N,K,m)
\le
\left\lfloor
\frac1m
\max_{\substack{\sum_i s_i=N\\
                 s_1\ge s_2\ge\cdots\ge1\\
                 \sum_{i=1}^{r-1}s_i\le K-1}}
\sum_i s_i\,
\mathsf C_{r-1}(N-s_i,K-s_i,m-s_i)
\right\rfloor.}
\tag{2.15}
\]

The at-most-rank cap is then
\(\mathsf C_r=\max(\mathsf C_{r-1},\mathsf E_r)\).
No convexity, generic-position assumption, or nonzero received-label
assumption enters (2.15).  The exact-rank distinction is load-bearing:
the projective evaluation columns span \(\mathcal V^*\), so an exact
rank-\(r\) direction has at least \(r\) projective lines, whereas a
lower-rank family is paid by \(\mathsf C_{r-1}\).

### Corollary 2.3 (linear-time two-tier envelope)

Put

\[
A=N-K,\qquad v=m-K,
\]

and abbreviate

\[
C_r(K;v)=\mathsf C_r(A+K,K,v+K).
\]

The quantities \(A,v\) are invariant under (2.11).  Define

\[
U_{r-1}(v)=\max_j C_{r-1}(j;v),
\tag{2.16}
\]

and, for \(D=K-1\),

\[
M_{r-1}(K;v)=
\max_{K-\lfloor D/(r-1)\rfloor\le j\le K-1}
C_{r-1}(j;v).
\tag{2.17}
\]

The top \(r-1\) projective lines contain at most \(D\) coordinates and
may each be charged \(U_{r-1}\).  Every remaining line has size at most
\(\lfloor D/(r-1)\rfloor\), so it may be charged
\(M_{r-1}(K;v)\).  Since the residual mass is

\[
(A+K)-D=A+1,
\]

(2.15) implies the safe exact-rank envelope

\[
\boxed{
\widehat E_r(K;v)\le
\left\lfloor
\frac{D\,U_{r-1}(v)+(A+1)M_{r-1}(K;v)}
     {K+v}
\right\rfloor.}
\tag{2.18}
\]

At every state the verifier takes the minimum of (2.18), the recursive
affine-span cap, and active common-zero Johnson, and then sets

\[
C_r(K;v)=\max\{C_{r-1}(K;v),\widehat E_r(K;v)\}.
\tag{2.19}
\]

It explicitly checks
\(\widehat E_r\ge C_{r-1}\) at every legal deployed state.  Both endpoints
of the window (2.17) increase with \(K\), so a monotone deque evaluates
every window maximum in \(O(K)\).  Ranks one through seven therefore cost
\(O(7K)\) exact-integer operations.

Initial common-zero coordinates are fixed mismatches in the present
source normalization.  Factoring \(t\) of them sends

\[
K\mapsto K-t,\qquad v\mapsto v+t.
\]

An induction using a dummy part of size \(t\), together with the local
monotonicity in \(v\), shows this cannot increase (2.17).  Thus the
deployed worst case occurs at \(t=0\).

The exact safe, but not partition-optimal, endpoint scan gives

\[
\begin{array}{c|c|c}
Q & C_7(d;w-Q) & L-C_7(d;w-Q)\\ \hline
26\,052 & 15\,775\,392 & 541\\
26\,053 & 15\,776\,368 & -435.
\end{array}
\tag{2.20}
\]

At \(Q=26\,052\), the successive uniform child maxima are

\[
\begin{array}{c|rrrrrr}
r&1&2&3&4&5&6\\ \hline
U_r&
16&253&3\,987&62\,817&989\,693&15\,592\,472\\
\operatorname*{argmax}K&
1&2\,620&2\,795&2\,806&2\,807&2\,808.
\end{array}
\tag{2.21}
\]

This advances every earlier weighted, two-stage Johnson, and
projective-pair frontier.  It is deliberately recorded as an
intermediate safe frontier: (2.17) charges all \(D\) top-line mass at the
single worst value \(U_{r-1}\), although the size constraint prevents all
top lines from realizing that maximizer simultaneously.

## 3. Cofactor-weight pivot theorem

Define

\[
\Phi_Q(g)=
\left\lfloor
\frac{R}{g-Q}
\left\lfloor
\frac{\binom{R-g+w+5}{5}}
     {\binom{w-Q+5}{5}}
\right\rfloor
\right\rfloor.
\tag{3.1}
\]

Both floors and their order are load-bearing.

### Theorem 3.1

Under the source hypotheses of Section 1,

\[
\boxed{
\sum_{\delta_i\le Q}q_i\le g\Phi_Q(g).}
\tag{3.2}
\]

### Proof

For each \(\alpha\in Z(P)\), no-common-zero exactness makes evaluation
\(\operatorname{ev}_\alpha|_{\mathcal W}\) nonzero.  Its kernel has rank at
most six.  Members in this kernel and in the \(Q\)-head have at least
\(g-Q\) agreements with the same nowhere-zero table on \(E_0\).
Theorem 2.1 at rank six bounds their number by \(\Phi_Q(g)\).

Sum over the \(g\) planted roots.  Member \(i\) occurs once for every root
of \(Q_i=\gcd(P,f_i)\), hence exactly \(q_i\) times.  This proves (3.2).

Since \(q_i=\delta_i+s_i\ge\delta_i\), for \(1\le D\le Q\),

\[
\#\{i:D\le\delta_i\le Q\}
\le\left\lfloor\frac{g\Phi_Q(g)}D\right\rfloor.
\tag{3.3}
\]

This is a band corollary.  It is not a license to sum overlapping heads.

## 4. Proper fixed-\(G\) moderate cap

Fix a proper recovered denominator \(G<P\), and put

\[
q=\deg(P/G)\ge1,\qquad m=g-q.
\tag{4.1}
\]

The proved proper-slice theorem reduces its zero-anchored rank to at most
six.  After division by \(P/G\), the slice lies in

\[
\operatorname{RS}(E_0,g-q-w)
\tag{4.2}
\]

around the nowhere-zero table \(G/V\).

For its moderate members \(\delta\le w\), one also has
\(\delta\le q\).  Thus their agreement is at least

\[
g-\min(q,w).
\tag{4.3}
\]

Theorem 2.1 gives

\[
\boxed{
F_q(g)=
\left\lfloor
\frac{R}{g-\min(q,w)}
\left\lfloor
\frac{\binom{R-g+q+w+5}{5}}
     {\binom{\max(q,w)+5}{5}}
\right\rfloor
\right\rfloor.}
\tag{4.4}
\]

At \(g=354\,972\),

\[
\begin{aligned}
F_1&=317\,828,\\
F_{15\,187}&=370\,007,\\
F_{67\,447}&=624\,046=\max_qF_q,\\
F_{100\,000}&=107\,399,\\
F_{287\,524}&=1\,576.
\end{aligned}
\tag{4.5}
\]

The two formula branches meet at \(q=w\).  The full-\(G\) slice \(q=0\)
may retain rank seven and is not covered by (4.4).

## 5. Endpoint corrections and rejected one-level marginal

Put

\[
g=354\,972.
\tag{5.1}
\]

The predecessor's \(H_Q\)-saturated histogram obeyed the scalar head
counts, but its exact weighted margins

\[
R B_6(Q)-
\sum_{\delta_i\le Q}(g-\delta_i)
\tag{5.2}
\]

are:

| \(Q\) | exact margin |
|---:|---:|
| 0 | \(279\,531\) |
| 1 | \(-3\,193\,224\) |
| 2,463 | \(-9\,044\,103\,237\) |
| 15,186 | \(-116\,880\,365\,780\) |

Thus that marginal is not source-feasible.

Successive source-bound corrections move the first unclosed scalar
relaxation as follows:

| compiler | last paid \(Q\) | paid head | next \(Q\) | next head |
|---|---:|---:|---:|---:|
| common-zero/Johnson second pivot | 15,838 | 15,774,764 | 15,839 | 15,776,639 |
| recursive two-tier full-line deletion | 26,052 | 15,775,392 | 26,053 | 15,776,368 |
| full top-six size coupling | 26,143 | 15,775,194 | 26,144 | 15,776,151 |
| per-label dual-domain compiler | 26,193 | 15,775,776 | 26,194 | 15,800,402 |

The third row is the precursor to the source lift below.  Its target
margin at \(Q=26\,143\) is \(738\).  At \(Q=26\,144\), the exact
inequality-feasible top-six shape

\[
(284\,730,614,545,545,545,545)
\tag{5.3}
\]

saturates the top-six sum \(d-1=287\,524\).  Its exact local caps are

\[
(15\,738\,557,1\,014\,371,
  1\,014\,361,1\,014\,361,1\,014\,361,1\,014\,361).
\tag{5.4}
\]

The remaining \(693\,605\) coordinates split as

\[
693\,605=1\,272\cdot545+365,
\tag{5.5}
\]

with local caps \(1\,014\,361\) and \(1\,014\,344\).  The exact
agreement-pair capacity is

\[
5\,187\,639\,320\,584,
\tag{5.6}
\]

whose quotient by \(h=328\,828\) is \(15\,776\,148=L+215\).  This is an
inequality-feasible relaxation, not a common source family.

Accordingly put all shallow scalar mass at

\[
s=0,\qquad q=\delta=26\,144,\qquad h=g-\delta=328\,828.
\tag{5.7}
\]

Then

\[
B_6(26\,144)=22\,416\,731,
\qquad
H_{26\,144}=66\,885\,134,
\tag{5.8}
\]

and

\[
R B_6-Lh=16\,806\,136\,372\,775>0.
\tag{5.9}
\]

The cofactor resource has

\[
\Phi_{26\,144}=3\,983\,444,
\tag{5.10}
\]

\[
g\Phi_{26\,144}-Lq
=1\,001\,565\,091\,216>0.
\tag{5.11}
\]

The predecessor affine head cap is \(376\,385\,666\).

The exact moments are

\[
M_1=412\,445\,992\,352,
\tag{5.12}
\]

\[
M_2=10\,782\,988\,024\,050\,688,
\tag{5.13}
\]

\[
gM_1-M_2=135\,623\,790\,773\,123\,456.
\tag{5.14}
\]

The five scalar utilizations, in parts per billion, are

```text
69,379,632
87,522,529
19,233,358
127,683,710
91,623,946
```

The \(E_0\) rank-flag utilizations for \(k=0,\ldots,6\) are

```text
3,699,023
8,786,552
19,876,982
45,605,940
105,301,025
243,213,036
561,762,488
```

The harmonic interval remains

\[
10\,411\,669\le x\le10\,411\,790.
\tag{5.15}
\]

At its lower endpoint the only nonzero transport row is

\[
(\delta,n_{\delta,0},n_{\delta,e})
=(26\,144,10\,411\,669,5\,364\,264).
\tag{5.16}
\]

The placement margins are \(263\,313\) and \(586\,786\).

Canonical compact-JSON-with-newline hashes are:

```text
histogram
c393b083f7b71a8b03c8823153cae6e4c81044cd3924bfae002f8dd257a853d5

dense transport
e4fd2bbef5e5f983a9c6edeb75baf592c4f3c8aa1157816b998e978f5e29c2ae

sparse transport
8bd18793245255c785979c0f447ac0cfeb7f3057c5504e6ffa38cbb49261ea20
```

This is an exact joint scalar marginal.  The next theorem proves that it
cannot be a common \(\mathcal W,b,H,V\), full-gcd source family.

### Theorem 5.1 (full planted-root source lift)

Assume the declared one-level source specialization

\[
q_i=\delta_i=q=26\,144
\tag{5.17}
\]

for every member.  Let \(S\subset E_0\) be one complete projective-line
class in the rank-seven agreement-pair recurrence, with \(s=|S|\), and
fix one member \(f_*\) in the corresponding compatible slice.  Every
other member in that slice has the form

\[
f_i=f_*+L_Sa_i,\qquad \deg a_i<k'=d-s.
\tag{5.18}
\]

Each \(f_i=Q_ib_i\) vanishes at the \(q\) planted roots of \(Q_i\).
Because \(S\subset E_0\) and \(E_0\cap Z(P)=\varnothing\), the locator
\(L_S\) is nonzero on \(Z(P)\).  Hence, at every root of \(Q_i\),

\[
a_i=-f_*/L_S.
\tag{5.19}
\]

The \(a_i\) therefore form an affine family of rank at most six on the
\(g\) planted points, of degree below \(k'\), with at least \(q\)
agreements with the one fixed table \(-f_*/L_S\).  Whenever \(k'\le q\),
the ordinary affine-span compiler gives

\[
A_q(k')
=
\left\lfloor
\frac{\binom{g-k'+6}{6}}
     {\binom{q-k'+6}{6}}
\right\rfloor.
\tag{5.20}
\]

For a class of size \(s\), define the source-valid cap

\[
\mathcal F_q(s)=
\begin{cases}
\min\{C_6(d-s;w-q),A_q(d-s)\},&d-s\le q,\\
C_6(d-s;w-q),&d-s>q,
\end{cases}
\tag{5.21}
\]

and

\[
\mathcal M_q(x)=\max_{1\le s\le x}\mathcal F_q(s).
\tag{5.22}
\]

Write the six largest projective-line sizes as
\(s_1\ge\cdots\ge s_6\).  Their total is at most \(d-1\).  For a fixed
\(s_1\), put

\[
B=d-1-s_1,\qquad
u=\min(s_1,B-4),\qquad
b=\min\left(s_1,\left\lfloor B/5\right\rfloor\right).
\tag{5.23}
\]

The other five largest classes have total mass at most \(B\) and sizes
at most \(u\).  Every tail class has size at most \(b\), while the tail
mass is

\[
R-(d-1)=693\,605.
\tag{5.24}
\]

Consequently every legal projective-line partition has agreement-pair
capacity at most

\[
s_1\mathcal F_q(s_1)
+B\mathcal M_q(u)
+693\,605\mathcal M_q(b).
\tag{5.25}
\]

The exact scan over every integer \(1\le s_1\le d-6\) attains its maximum
at

\[
\begin{aligned}
s_1&=283\,663,&d-s_1&=3\,862,\\
\mathcal F_q(s_1)&=15\,294\,703,&
B&=3\,861,\\
u&=3\,857,&
\mathcal M_q(u)&=1\,014\,887
  &&\text{at size }3\,846,\\
b&=772,&
\mathcal M_q(b)&=1\,014\,383
  &&\text{at size }757.
\end{aligned}
\tag{5.26}
\]

At the largest class, the old and planted caps are respectively
\(15\,294\,703\) and \(15\,295\,049\); the minimum in (5.21) is
load-bearing across the full scan, even though the old cap wins at the
new maximizer.  The exact maximum numerator is

\[
5\,046\,040\,936\,511.
\tag{5.27}
\]

Division by \(g-q=328\,828\) gives

\[
\boxed{
\#\mathcal I_q\le15\,345\,533
=15\,775\,932-430\,399.}
\tag{5.28}
\]

Initial common zeros on \(E_0\) cannot worsen this result.  If \(t\) fixed
mismatches are factored first, then

\[
(R,d,v)\longmapsto(R-t,d-t,v+t),
\tag{5.29}
\]

while \(q\) and the denominator \(g-q\) remain fixed.  Add \(t\) to the
largest class of its projective partition.  Every prefix gate becomes

\[
\sum_{i\le j}s_i+t
\le d-t-7+j+t=d-7+j,
\tag{5.30}
\]

so the image is legal for \(t=0\).  The largest residual dimension is
unchanged; every other residual dimension \(k'\) becomes \(k'+t\).
The old compiler obeys

\[
C_6(k';v+t)\le C_6(k'+t;v)
\tag{5.31}
\]

(with \(C_6(k';v+t)\le C_6(k';v)\) for the enlarged largest class).
For completeness, (5.31) follows by induction on rank.  At rank one its
two denominators are both \(k'+v+t\), while the right numerator has the
extra \(t\).  At the inductive step, append a dummy part of size \(t\) to
the largest part.  The denominator is unchanged, the prefix gates remain
legal by (5.30), the largest child is weakened by lowering \(v+t\) to
\(v\), and every other child is bounded by the induction hypothesis.
Taking the maximum and the lower-rank maximum preserves the inequality.

Moreover \(A_q(k')\) is nondecreasing in \(k'\): before taking floors its
binomial ratio is
\[
\prod_{j=1}^6\frac{g-k'+j}{q-k'+j},
\]
and every factor increases when \(k'\) increases because \(g>q\).
An inactive planted cap is \(+\infty\).
Thus every \(t>0\) capacity maps to a weakly larger \(t=0\) capacity.
The verifiers check the exact planted-cap monotonicity for
\(0\le k'\le26\,144\); its minimum consecutive increment is \(1\,331\).

Therefore the entire one-level marginal (5.17), not merely the former
dominant-class optimizer, is source-impossible.  This remains a local
route cut.  The next theorem performs the required mixed-distribution
coupling.

### Theorem 5.2 (per-label dual-domain compiler)

For exact local arithmetic, write \(C_r(A,v;k)\) for the at-most-rank
projective cap on a domain of size \(A+k\), polynomial degree below \(k\),
and agreement threshold \(v+k\).  Its exact-rank semantics are

\[
C_1(A,v;k)=\left\lfloor\frac{A+k}{v+k}\right\rfloor
\tag{5.32}
\]

and, for \(r\ge2\),

\[
\begin{aligned}
U_{r-1}(k)&=\max_{r-1\le j\le k-1}C_{r-1}(A,v;j),\\
M_{r-1}(k)&=
\max_{k-\lfloor(k-1)/(r-1)\rfloor\le j\le k-1}
C_{r-1}(A,v;j),\\
T_r(A,v;k)&=
\left\lfloor
\frac{(k-1)U_{r-1}(k)+(A+1)M_{r-1}(k)}
     {v+k}
\right\rfloor.
\end{aligned}
\tag{5.33}
\]

Intersect this with the affine one-pivot cap

\[
S_r(A,v;k)=
\left\lfloor
\frac{A+k}{v+k}
\left\lfloor
\frac{\binom{A+r-1}{r-1}}
     {\binom{v+r-1}{r-1}}
\right\rfloor
\right\rfloor
\tag{5.34}
\]

and, when its denominator is positive, Johnson's cap

\[
J_r(A,v;k)=
\left\lfloor
\frac{(A+k)(v+1)}
     {(v+k)^2-(A+k)(k-1)}
\right\rfloor.
\tag{5.35}
\]

Thus

\[
\widehat E_r=\min(T_r,S_r,J_r\text{ when active}),
\qquad
C_r=\max(C_{r-1},\widehat E_r).
\tag{5.36}
\]

The final maximum in (5.36) is load-bearing: \(\widehat E_r\) is an
exact-rank cap, while \(C_r\) is an at-most-rank cap.  Both verifiers
retain the whole child array before writing exact-rank entries.

Now fix a \(Q\)-head and a compatible normalized-label subclass of one
\(E_0\)-projective line.  After deleting its complete line, let
\(k=d-|S|\) be the residual degree.  Put

\[
\begin{aligned}
C^E_{6,z}(k)&=C_6(R-d,w-z;k),\\
C^P_6(k,x+1)&=C_6(g-k,x+1-k;k),\\
\Phi_Q&=\Phi_Q(g).
\end{aligned}
\tag{5.37}
\]

For any legal split

\[
k-1\le x\le Q-1,
\tag{5.38}
\]

members with \(\delta_i\le x\) are bounded by \(C^E_{6,x}(k)\).
Every remaining member has

\[
q_i\ge\delta_i\ge x+1
\tag{5.39}
\]

and hence at least \(x+1\) agreements with the fixed planted-root table
obtained from (5.19).  If the high subfamily has a common planted
agreement, all its original \(f_i\) vanish at that root, so Theorem 3.1's
per-root proof bounds it by \(\Phi_Q\).  Otherwise its common direction
zeros are fixed mismatches; factor them and apply the local planted-domain
compiler \(C^P_6\).  Therefore the subclass cap is

\[
\boxed{
D_Q(k,x)=
\min\left\{
C^E_{6,Q}(k),\
C^E_{6,x}(k)+\max\{\Phi_Q,C^P_6(k,x+1)\}
\right\}.}
\tag{5.40}
\]

This split is performed inside each normalized-label subclass before the
agreement-pair sum, so no codeword or agreement pair is charged twice.

The monotonicities used below are exact.  \(C^E_{6,x}(k)\) is
nondecreasing in \(x\), while
\(\max(\Phi_Q,C^P_6(k,x+1))\) is nonincreasing.  At rank one this is
immediate; the affine and two-tier terms preserve it inductively.  For the
active Johnson term, differentiation in \(v\) has sign numerator

\[
A-(A+1)k-v^2-2v<0.
\tag{5.41}
\]

Floors, minima, and the at-most-rank maximum preserve the stated
directions.

#### The \(Q=26\,193\) closure

The coarse local-prefix outer scan has 239 target-exceeding largest-class
sizes,

\[
284\,499\le s\le284\,737,
\qquad
2\,788\le k=d-s\le3\,026.
\tag{5.42}
\]

For these 239 classes only, use the declared linear schedule

\[
\boxed{x_{\rm lin}(k)=44\,835-\left\lfloor\frac{67k}{10}\right\rfloor.}
\tag{5.43}
\]

It satisfies (5.38) throughout (5.42).  In increasing \(k\), the raw
dual sums in (5.40) run from

\[
7\,899\,882
\quad(k,x)=(2\,788,26\,156)
\tag{5.44}
\]

to

\[
12\,277\,361
\quad(k,x)=(3\,026,24\,561),
\tag{5.45}
\]

with zero monotonicity violations.  After replacing all 239 class caps
and rebuilding every size-prefix maximum, zero target-exceeding class
remains.  The new maximizer is the unmodified class

\[
(s,k,C^E_{6,Q}(k))=(284\,498,3\,027,15\,738\,077).
\tag{5.46}
\]

Its exact agreement-pair numerator is

\[
5\,186\,744\,182\,280,
\tag{5.47}
\]

so

\[
\boxed{
N_{\delta\le26\,193}
\le15\,775\,776
=15\,775\,932-156.}
\tag{5.48}
\]

This includes initial \(E_0\) common zeros.  If their number
\(t\ge23\,730\), the direct rank-seven affine cap is

\[
\left\lfloor
\frac{\binom{693\,604+7}{7}}
     {\binom{(67\,447-26\,193)+t+7}{7}}
\right\rfloor
\le15\,774\,894,
\tag{5.49}
\]

already \(1\,038\) below target.  At \(t=23\,729\) it is
\(15\,776\,593\), so the threshold is exact.

For \(t<23\,730\), the remaining degree \(K_0=d-t\) is at least
\(263\,796>2Q\).  Two lines with residual dimensions at most \(Q\) would
have combined size at least \(2(K_0-Q)\), exceeding the top-two prefix
cap \(K_0-5\) by at least \(211\,415\).  Hence at most one line is
planted-active, and it is the largest.  Add all \(t\) dummy mass to that
line.  Its residual \(k\), linear split, and planted cap are unchanged;
the other lines have \(k>Q\), where (5.40) is inactive, and map by the
ordinary \(E_0\) recurrence.  Thus the \(t=0\) scan dominates every
initial-common-zero branch.

#### The sharp \(Q=26\,194\) route cut

For diagnostic separation, the adjacent scan uses the explicitly
different tangent schedule

\[
x_{\rm tan}(k)=
\max\left\{
k-1,\
w+k-\left\lfloor\sqrt{(693\,604+k)(k-1)}\right\rfloor-11
\right\}.
\tag{5.50}
\]

It gives outer numerator

\[
5\,194\,824\,788\,248
\tag{5.51}
\]

and head \(15\,800\,402\).  Its maximizer is

\[
(s,k,C^E_{6,Q}(k))=(284\,380,3\,145,15\,762\,647).
\tag{5.52}
\]

This class is not a schedule accident.  Here
\(\Phi_{26\,194}=4\,008\,251\).  Every legal split
\(3\,144\le x\le26\,193\) is covered by the following seven monotone
intervals.  On \([a,b]\), (5.41) gives the lower bound
\(C^E_{6,a}(k)+\max(\Phi_Q,C^P_6(k,b+1))\).

| \(a\) | \(b\) | \(C^E_{6,a}\) | high cap at \(b\) | sum |
|---:|---:|---:|---:|---:|
| 3,144 | 23,768 | 18 | 15,764,297 | 15,764,315 |
| 23,769 | 23,775 | 16,772 | 15,746,404 | 15,763,176 |
| 23,776 | 23,778 | 26,254 | 15,736,663 | 15,762,917 |
| 23,779 | 23,780 | 34,649 | 15,732,593 | 15,767,242 |
| 23,781 | 23,785 | 44,038 | 15,718,801 | 15,762,839 |
| 23,786 | 23,816 | 136,553 | 15,627,111 | 15,763,664 |
| 23,817 | 26,193 | 11,031,141 | 8,136,412 | 19,167,553 |

The minimum is \(15\,762\,839\), which exceeds the old class cap in
(5.52) by \(192\).  Thus no legal per-label two-domain split can improve
the load-bearing \(Q=26\,194\) class.  This is a sharp route cut on the
present method, not a claim that the class is source-realizable or that
rank seven is globally open for every stronger incidence theorem.

## 6. Exact 39-slice cofactor/lcm relaxation

Since

\[
\left\lceil\frac{L}{412\,817}\right\rceil=39,
\tag{6.1}
\]

assign 412,817 abstract members to each of slices \(0,\ldots,37\) and
88,887 to slice 38.

On the cyclic \(g\)-point planted-root universe, set

\[
Q_j=\{jq,jq+1,\ldots,jq+q-1\}\pmod g,
\qquad q=26\,144.
\tag{6.2}
\]

Because

\[
\gcd(q,g)=4,\qquad39q=2g+309\,672,
\tag{6.3}
\]

the 39 supports are distinct.  Exactly 45,300 planted roots have load two
and 309,672 have load three.  Therefore

\[
\min_\alpha\operatorname{load}(\alpha)=2,\qquad
\max_\alpha\operatorname{load}(\alpha)=3.
\tag{6.4}
\]

The total intersection of the \(Q_j\) is empty.  For
\(G_j=P/Q_j\), this gives

\[
\operatorname{lcm}_jG_j=P.
\tag{6.5}
\]

The largest planted-root word load is at most

\[
3\cdot412\,817=1\,238\,451<\Phi_{26\,144}.
\tag{6.6}
\]

Thus the fixed-slice and cofactor-pivot marginals coexist exactly.
This remains a combinatorial relaxation.  No common polynomial space,
numerators, locators, common unit, or exact full gcds are supplied.

## 7. Why another cofactor pivot is not automatic

Let \(Q\mid P\) be split and nonconstant, and suppose
\(\deg Q+5<d\).  Take

\[
\mathcal W
=\langle1\rangle\mathbin{\oplus}
Q\langle1,X,\ldots,X^5\rangle.
\tag{7.1}
\]

It has dimension seven and no common zero on \(Z(P)\).  At every
\(\alpha\mid Q\), evaluation in the displayed basis is

\[
[1,0,0,0,0,0,0].
\tag{7.2}
\]

All \(Q\)-root evaluation columns are proportional.  Arbitrarily many
planted roots may therefore refund only one rank.  This is a structural
polynomial-space witness, not a received-word source family.

## 8. Deployed interlaced mixed-\(G\) source family

### 8.1 Boundary layout

Partition the \(n\) evaluation points into 1,024 ambient \(T_{2048}\)
blocks, each containing 64 \(T_{32}\) blocks.

Take 887 large blocks with two \(T_{32}\) subblocks of \(S_0\)-occupancy
18 and 62 of occupancy 17.  Take 137 large blocks with one occupancy-18
subblock and 63 occupancy-17 subblocks.  Then

\[
887\cdot1090+137\cdot1089=1\,116\,023,
\tag{8.1}
\]

so every \(T_{32}\) block has \(E_0\)-occupancy 14 or 15 and every
\(T_{2048}\) block has \(E_0\)-occupancy 958 or 959.

Refine each \(T_{32}\) block into 16 \(T_2\) pairs and place at most one
\(E_0\) point in each pair.  Choose all \(P\)-roots from distinct \(T_2\)
pairs and at most six per \(T_{32}\) block.  The capacities are

\[
354\,972<1\,048\,576,
\qquad
354\,972<6\cdot65\,536.
\tag{8.2}
\]

### 8.2 Seven split numerators

Put

\[
m=w+1=67\,448.
\tag{8.3}
\]

Choose disjoint private root sets \(U_i\) of sizes

\[
(33\,973,33\,973,33\,973,33\,973,
33\,972,33\,972,33\,972).
\tag{8.4}
\]

For each pair \(i<j\), choose a disjoint pair-only root set of size 5,579,
adding one root for pairs

\[
12,\ 34,\ 56,\ 67,\ 57.
\tag{8.5}
\]

The pair-incidence degrees are

\[
(33\,475,33\,475,33\,475,33\,475,
33\,476,33\,476,33\,476).
\tag{8.6}
\]

Let \(G_i\) contain \(U_i\) and all pair sets incident with \(i\).
Then

\[
\deg G_i=67\,448
\tag{8.7}
\]

and

\[
\deg\operatorname{lcm}_iG_i
=237\,808+117\,164
=354\,972.
\tag{8.8}
\]

Each \(G_i\) has private roots.

### 8.3 Interlaced \(H_i\) and global labels

Give every \(H_i\) one distinct \(E_0\) point in each \(T_{32}\) block
and 1,912 additional distinct points, with at most two points of one
\(H_i\) in a block.  This is feasible because after the seven baseline
choices there remain at least seven \(E_0\) points in every block and

\[
7\cdot1\,912=13\,384<7\cdot65\,536.
\tag{8.9}
\]

Thus

\[
1\le|H_i\cap B|\le2
\tag{8.10}
\]

for every \(T_{32}\) block \(B\), and the seven \(H_i\) are disjoint.

Choose nonzero scalar labels \(b_i\) sequentially.  At stage \(j\), avoid

\[
b_j=b_i\,\frac{G_j(x)}{G_i(x)}
\qquad(i<j,\ x\in E_0).
\tag{8.11}
\]

There are at most

\[
6R=5\,886\,774<p-1
\tag{8.12}
\]

forbidden nonzero values.  Hence the choice is possible, and

\[
W_{ij}=G_i b_j-G_j b_i
\tag{8.13}
\]

is nonzero at every \(E_0\) point.

Because the \(H_i\) are disjoint,

\[
\gcd(H_i,H_j)=1,
\qquad
\gcd(H_iH_j,W_{ij})=1.
\tag{8.14}
\]

The proved pairwise CRT equivalence produces one unit \(V\bmod L_0\) with

\[
H_i=\gcd(L_0,G_i-b_iV)
\tag{8.15}
\]

for all seven indices.

### 8.4 Exact codewords and master data

Let \(H_0=V^{-1}\bmod L_0\), set \(U=A_0H_0\), and put

\[
c_i=\frac{A_0}{G_i}b_i.
\tag{8.16}
\]

Then

\[
\deg c_i=a-m=1\,048\,575<K.
\tag{8.17}
\]

Its agreement support is exactly

\[
(S_0\setminus Z(G_i))\mathbin{\dot\cup}Z(H_i),
\tag{8.18}
\]

of size

\[
(a-m)+m=a.
\tag{8.19}
\]

Its exact error support is

\[
Z(G_i)\mathbin{\dot\cup}(E_0\setminus Z(H_i)),
\tag{8.20}
\]

of size \(R\).

Equation (8.10) makes the agreement support miss at least twelve \(E_0\)
points in every \(T_{32}\) block.  The six-per-block placement of \(P\)
makes the error support miss at least eleven \(S_0\) points in every block.
Neither support contains a complete \(T_{32}\), hence neither contains a
complete \(T_{2048}\).

Evaluate the seven codewords at one private root from each \(U_i\).
The resulting matrix is diagonal with nonzero diagonal, so

\[
\dim\operatorname{span}\{c_1,\ldots,c_7\}=7.
\tag{8.21}
\]

For the master normalization,

\[
Q_i=P/G_i,\qquad f_i=Q_i b_i,
\tag{8.22}
\]

\[
q_i=\deg Q_i=287\,524=d-1,
\qquad s_i=0,\qquad\delta_i=287\,524.
\tag{8.23}
\]

The exact source identity gives

\[
\gcd(PL_0,Y-f_i)=Q_iH_i.
\tag{8.24}
\]

The lcm is exactly \(P\), equivalently the \(f_i\) have no common zero on
\(Z(P)\).  Thus the zero anchor and seven companions are a genuine
deployed source family.  Base-field embedding makes the same eight
codewords and received word valid in the quartic target code.

## 9. Grande Finale v4 chronology

The unit throughout the source construction is distinct codewords per one
received word.  The seven companions are genuine
`HIGH_BOUNDARY_EXACT_CODEWORD` objects.  All have error weight \(R\), above
the low paid cutoff.

This packet does not determine the complete list of the constructed center.
It therefore does not compute its complete exact-weight histogram or signed
\(\Xi_{46}\) credits.

The v4 movement is exactly

```text
U_paid     += 0
U_Q        += 0
U_list_int += 0
U_ext      += 0
U_new      += 0
signed Xi_46 payment: none
```

The rejected one-level object and the 39-slice cofactor relaxation do not
enter the first-match chronology at all.

The exact remaining rank-seven theorem starts at the
\(Q=26\,194,\ k=3\,145\) primitive class and must go beyond one
per-label two-domain split.  It must jointly control cross-subclass
incidence, varying cofactors, partial fibers, Wronskians, and complete
codeword add-back.  A complete-fiber count, block metric, fixed template,
summed per-\(G\) cap, or unsigned marked key count is insufficient.

## 10. Proof audit

Statement audited:

The weighted agreement and cofactor double counts, exact full-line
recurrence, planted-root source lift, per-label dual-domain compiler and
global-\(E_0\)-zero reduction, \(Q=26\,194\) seven-interval route cut,
proper fixed-\(G\) moderate cap, endpoint marginal correction, 39-slice
cofactor relaxation, no-second-pivot witness, and deployed eight-codeword
source construction.

Files/sections read:

- effective-deficit one-pivot predecessor;
- shallow master-denominator predecessor;
- common-\(V\) pairwise CRT equivalence;
- v4 source adapter and five-atom global compiler.

Dependencies:

- **PROVEN by predecessors:** master normalization, proper fixed-\(G\) rank
  loss, recursive affine-span compiler, nowhere-zero one-pivot theorem,
  common-\(V\) pairwise CRT equivalence, and v4 codeword chronology.
- **PROVED here:** Theorems 2.1, 2.2, 3.1, 5.1, and 5.2; Corollary 2.3;
  formula (4.4); the structural witness; and the deployed source
  construction.
- **VERIFIED EXACTLY:** all endpoint margins, resource utilizations, cyclic
  root loads, lcm gate, block occupancies, and finite-field controls.
- **SOURCE-IMPOSSIBLE HERE:** the single-level \(L\)-histogram at
  \(q=\delta=26\,144\).
- **PAID HERE:** every rank-seven \(Q=26\,193\) head distribution.
- **METHOD ROUTE CUT HERE:** no legal per-label two-domain split improves
  the load-bearing \(Q=26\,194,\ k=3\,145\) class.
- **RELAXATION ONLY:** the 39-slice cofactor marginal.
- **UNPROVEN:** an \(L\)-member source realization or contradiction,
  chronology-valid signed payment, global rank-seven closure, and ranks at
  least eight.

Parameter dependence:

All numerical claims use exactly (1.1).  There is no asymptotic constant.

Layer-cake / dyadic summability:

Not applicable.  The v4 signed identity is finite and is not consumed as a
payment.

Moment / Markov / Chebyshev:

No probabilistic moment inequality is used.  Chebyshev refers only to the
ambient polynomial fold.

Edge cases / notation:

- \(q=0\) is the full-\(G\) slice and is excluded from \(F_q\).
- Both nested floors are load-bearing.
- The \(Q\)-heads overlap and may not be summed.
- \(\delta\le q\) uses \(s\ge0\).
- The two \(F_q\) branches meet at \(q=w\).
- The structural witness is not a source list.
- Absence of complete dyadic fibers does not exclude every possible
  non-dyadic quotient owner.

Numerical evidence:

All deployed arithmetic is exact.  The Sage \(\mathbb F_{101}\) realization
is an algebraic control, not deployed-scale evidence.  The deployed source
construction is proved existentially by exact counting and the pairwise CRT
theorem.

Verdict:

GREEN under two fresh independent audits for the full-line, source-lift,
and dual-domain theorems and certificates.  YELLOW for global rank seven
and the M31 LIST row; neither audit authorizes a global closure.

Remaining risks:

- The \(Q=26\,194,\ k=3\,145\) class needs a cross-subclass, third-domain,
  or other incidence theorem; the proved two-domain method is exhausted
  there by \(192\).
- The complete list at the constructed center is unknown.
- No weighted partial-fiber/Wronskian theorem supplies v4 signed refunds.
- Rank at least eight remains separate.

Maximal next attack:

Build an exhaustive cross-subclass or third-domain incidence compiler for
the \(Q=26\,194,\ k=3\,145\) class, starting from the seven certified
split intervals.  It must retain exact codeword add-back and signed
cross-weight credits and terminate in a paid v4 owner or an explicit
source-compatible primitive route cut.

OPEN GAP
