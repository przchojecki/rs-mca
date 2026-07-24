---
workboard_item: M1/L
row: Mersenne-31 list at 2^-100 — fixed-G ordinary boundary endpoint subfamily
object: LIST
target_epsilon: 2^-100
agreement: deployed 1116023; ordinary boundary agreements 72859 and 908270
B_star: 16777215
direct_statement: For every 981129-point boundary subset E0 of the deployed domain and every received word, an ordinary base-field RS(E0,d) list at agreement m=d+67447 has size at most 2310492 for d=5412 (agreement 72859) or d=840823 (agreement 908270) — respectively three and one error coordinates beyond the exact finite-p Johnson grid for target list bound 16777214; the corresponding zero-anchored fixed-G boundary list has size at most 2310493 <= B_star. Bound = floor((N/s) floor(D(N-1)/P)) with N=981129, D=67448, s=72859, P=385684.
architecture: DIRECT
partition_digest: null
atom_or_cell: DIRECT fixed-G ordinary boundary endpoint subfamily
quantifier: Every E0 subset D with |E0|=981129, every received word r:E0->F_p, and every family of distinct degree-less-than-d polynomials satisfying the closed-ball agreement gate, for d in {5412,840823}.
projection_and_unit: Ordinary Reed-Solomon codewords in one Hamming ball; under the fixed-G equivalence, zero anchor plus distinct nonanchors.
claimed_bound: Ordinary list size at most 2310492; zero-anchored fixed-G boundary list size at most 2310493. Safety margin (B_star-1)-2310492 = 14466722.
status: PROVED
impact: LOCAL_ONLY
falsifier: An ordinary list of 2310493 distinct degree-less-than-5412 codewords at agreement at least 72859, or degree-less-than-840823 codewords at agreement at least 908270, on any allowed E0 and received word; alternatively a failure of the one-coordinate incidence or constant-weight Plotkin inequality.
replay: |
  Lean arithmetic shadow (kernel-checked closed Nat facts + two omega implications; native_decide disclosed, no sorry, no custom axioms):
    cd experimental/lean/l_fixedg_endpoint_plotkin && lake build LFixedGEndpointPlotkin
  Full stdlib big-integer replay of every integer (Plotkin chain, exact finite-p Johnson grid, parent-Johnson middle interval, adjacent-shell route stop, margins):
    python3 experimental/scripts/verify_l_fixedg_endpoint_plotkin.py --check
    python3 experimental/scripts/verify_l_fixedg_endpoint_plotkin.py --tamper-selftest   # exit 0 iff every proof-critical mutation is caught
  The mathematical proof (Theorem 2.1 and the endpoint specialization) is in Sections 2 and 3 of the note; Lean and Python check only its arithmetic shadow.
consumers: None at the M31 row numerator — this is PROVED LOCAL, not a bankable atom. Corollary 5.2 of experimental/notes/thresholds/m31_fixed_g_universal_rs_embedding_v1.md still requires the uniform ordinary-list upper across the full middle interval 72859 <= m <= 908270 (all 835410 interior agreements) before any U_list_int payment; the two proved endpoints do not move the ledger or the official score.
risk_limits: Two proved endpoints (d,m) in {(5412,72859),(840823,908270)} only; the 835410 interior middle-interval agreements remain open (the next symmetric pair already has a negative one-shortening Plotkin denominator, reverse deficit 449727, and the two-shortening route misses B_star-1 by 13905232). No aggregation over lists mixing different G locators, no global M31 row closure or workboard-atom movement, no claim the Plotkin cap is sharp. Lean scope: the package kernel-checks only the exact arithmetic shadow, not the polynomial-root, incidence-averaging, or constant-weight double-count arguments, which are proved in the note.
---

# M31 fixed-G ordinary boundary endpoint Plotkin theorem

## 1. Result and exact Lane-L print blocks

Let

\[
p=2^{31}-1=2,147,483,647,\qquad
R=981,129,\qquad
w=67,447,\qquad
B^*=16,777,215.
\]

For every \(R\)-subset \(E_0\) of the deployed domain, write
\(\operatorname{RS}_{\mathbb F_p}(E_0,d)\) for evaluations of polynomials of
degree \(<d\).  The radius convention is the closed Hamming ball: agreement at
least \(m\) means at most \(R-m\) errors.

The following two-point subfamily lies at the two endpoints of the packet's
Johnson-negative middle interval.

```text
row:                 (F_p, E0 subset D, d=5412, R=981129, rho=5412/981129)
object:              ordinary LIST, not MCA
radius/agreement:    delta=908270/981129 and integer agreement 72859=d+67447
Johnson comparison:  exact finite-p, ell=16777214 Johnson radius 908267/981129; post-Johnson gap 3/981129
bound:               |Lambda(RS_Fp(E0,5412),908270/981129)| <= 2310492 <= 16777214
route:               DIRECT_LIST
CA_or_MCA_input:     none
code_shift:          C=RS_Fp(E0,5412); no C^+ shift
status:              PROVED (uniform over every allowed E0 and received word)
```

```text
row:                 (F_p, E0 subset D, d=840823, R=981129, rho=840823/981129)
object:              ordinary LIST, not MCA
radius/agreement:    delta=72859/981129 and integer agreement 908270=d+67447
Johnson comparison:  exact finite-p, ell=16777214 Johnson radius 72858/981129; post-Johnson gap 1/981129
bound:               |Lambda(RS_Fp(E0,840823),72859/981129)| <= 2310492 <= 16777214
route:               DIRECT_LIST
CA_or_MCA_input:     none
code_shift:          C=RS_Fp(E0,840823); no C^+ shift
status:              PROVED (uniform over every allowed E0 and received word)
```

The exact safety margin is

\[
16,777,214-2,310,492=14,466,722.
\]

By Theorem 4.1 and Corollary 5.1 of
`m31_fixed_g_universal_rs_embedding_v1.md`, the corresponding zero-anchored
fixed-\(G\) boundary subclass has at most

\[
1+2,310,492=2,310,493
\]

codewords.  This is a theorem for a declared ordinary-RS subfamily.  It is not
a global upper bound for M31 lists that mix \(G\)'s.

## 2. General one-coordinate Plotkin lemma

### Theorem 2.1 (one-coordinate Plotkin list bound)

Let \(F\) be a field, let \(E\subset F\) have size \(N\), and let
\(1\le d\le m<N\).  Put

\[
D=m-d+1,\qquad s=\min(m,N-m).
\]

Assume \(1\le D\le s\) and

\[
P:=D(N-1)-(s-1)(N-s)>0. \tag{2.1}
\]

Then every received word \(r:E\to F\) has at most

\[
\left\lfloor
\frac{N}{s}
\left\lfloor\frac{D(N-1)}{P}\right\rfloor
\right\rfloor \tag{2.2}
\]

distinct degree-\(<d\) polynomials agreeing with \(r\) on at least \(m\)
coordinates.

### Proof

If \(L=0\), the conclusion is immediate.  Assume \(L\ge1\) and let
\(f_1,\ldots,f_L\) be such a list.  For each \(i\), choose an \(m\)-subset
\(A_i\) of its agreement set.  If \(i\ne j\), every point of
\(A_i\cap A_j\) is a root of the nonzero polynomial \(f_i-f_j\), so

\[
|A_i\cap A_j|\le d-1,\qquad
|A_i\setminus A_j|\ge m-d+1=D. \tag{2.3}
\]

The selected \(A_i\)'s are distinct because \(m\ge d\).

If \(m\le N/2\), set \(S_i=A_i\).  Otherwise set \(S_i=E\setminus A_i\).
Then every \(S_i\) has size \(s\), the \(S_i\)'s are distinct, and their
exchange distance is at least \(D\).  In the complement case this uses
\(|(E\setminus A_i)\setminus(E\setminus A_j)|
=|A_j\setminus A_i|=|A_i\setminus A_j|\), since the \(A_i\)'s have equal
size:

\[
|S_i\setminus S_j|\ge D. \tag{2.4}
\]

Double-count incidences \((i,x)\) with \(x\in S_i\).  Some coordinate
\(x\in E\) belongs to a subfamily of size

\[
M\ge\left\lceil\frac{Ls}{N}\right\rceil. \tag{2.5}
\]

Delete \(x\) from every set in that subfamily.  This gives \(M\) distinct
\(k=s-1\) subsets of an \(n'=N-1\) point set, still at exchange distance at
least \(D\).

For completeness, the constant-weight Plotkin inequality is derived directly.
Let \(c_y\) be the number of shortened sets containing \(y\).  The sum of all
pairwise exchange distances is

\[
\binom M2 k-\sum_y\binom{c_y}{2}.
\]

Since \(\sum_y c_y=Mk\), Cauchy--Schwarz gives
\(\sum_y c_y^2\ge M^2k^2/n'\), hence

\[
\binom M2 D
 \le \frac{M^2k(n'-k)}{2n'}.
\]

After cancellation,

\[
M\bigl(Dn'-k(n'-k)\bigr)\le Dn'. \tag{2.6}
\]

The parenthesis is \(P\), so

\[
M\le \left\lfloor\frac{D(N-1)}P\right\rfloor. \tag{2.7}
\]

Combining (2.5) and (2.7) gives
\(Ls\le N\lfloor D(N-1)/P\rfloor\), which is exactly (2.2). \(\square\)

The proof is deterministic, does not use the shape of \(E\), and counts
ordinary codewords rather than supports: the selected-support map is injective
by the degree bound.

## 3. M31 endpoint specialization

For both endpoint triples

\[
(d,m)\in\{(5,412,72,859),(840,823,908,270)\},
\qquad m=d+w,
\]

support complementation reduces (2.3) to the same constant-weight family:

\[
N=981,129,\qquad s=72,859,\qquad D=w+1=67,448.
\]

After the one-coordinate incidence step,

\[
n'=981,128,\qquad k=72,858,\qquad n'-k=908,270.
\]

The exact Plotkin numerator and denominator are

\[
Dn'=67,448\cdot981,128=66,175,121,344,
\]

\[
P=66,175,121,344-72,858\cdot908,270=385,684>0.
\]

Exact division gives

\[
66,175,121,344
 =171,578\cdot385,684+231,992,
\]

so the shortened subfamily has size at most \(171,578\).  Pulling back the
incidence average gives

\[
L\le
\left\lfloor\frac{981,129\cdot171,578}{72,859}\right\rfloor
=2,310,492,
\]

with remainder \(14,934\).

## 4. Exact Johnson comparison

The target ordinary-list upper is
\(\ell=B^*-1=16,777,214\).  For the \(p\)-ary Johnson function
\(J_{p,\ell}\) from `open-proximity.tex`, clear the square root at integer
agreement \(A\) by defining

\[
\begin{aligned}
M_{p,\ell,d}(A)
={}&(\ell-1)(pA-R)^2\\
&-\Bigl(R^2(p-1)^2(\ell-1)
 -R(p-1)p\ell(R-d+1)\Bigr). \tag{4.1}
\end{aligned}
\]

The integer agreement \(A\) is Johnson-covered for the target \(\ell\) when
\(M_{p,\ell,d}(A)\ge0\).  For \(A\ge1\), the term \(pA-R\) is positive,
so this expression is strictly increasing in \(A\).  The exact boundary signs
are:

| \(d\) | row \(A\) | first Johnson-covered \(A_J\) | \(M(A_J-1)\) | \(M(A_J)\) | exact Johnson errors \(R-A_J\) | row errors | gap |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 5,412 | 72,859 | 72,862 | \(-8,221,003,905,619,924,567,540,362,320,760\) | \(3,053,765,018,644,647,902,938,550,527,393\) | 908,267 | 908,270 | 3 |
| 840,823 | 908,270 | 908,271 | \(-34,579,558,183,296,310,721,328,734,410,451\) | \(105,968,468,789,629,159,598,961,272,090,208\) | 72,858 | 72,859 | 1 |

Thus both rows are strictly outside the exact finite-\(p\), target-list Johnson
grid.  They are also outside the limiting quadratic Johnson region:

\[
m^2-R(d-1)=-455,138
\]

at both endpoints.  The limiting integer Johnson agreements are \(72,863\)
and \(908,271\), respectively.

## 5. Fixed-G consequence and scope

The universal embedding packet proves that every ordinary list of size at most
\(B^*\) in the declared boundary family becomes, after one common constant
translation, distinct nonanchors sharing one \(G\), together with the zero
anchor.  Conversely, a canonical fixed-\(G\) boundary list gives the ordinary
received table \(r_{G,V}=G/V\).

Therefore Theorem 2.1 and the endpoint arithmetic imply:

> At either endpoint triple, every canonical zero-anchored fixed-\(G\)
> boundary list contains at most \(2,310,493\) codewords.

This uses no CA or MCA numerator, no \(C\) versus \(C^+\) shift, no random
puncturing, and no generic-evaluation hypothesis.  It is uniform over every
allowed boundary subset and received word.

Nonclaims:

- no upper bound for the other \(835,410\) integer agreements in the packet's
  middle interval;
- no aggregation theorem for lists mixing different \(G\)'s;
- no global M31 row closure or workboard atom movement;
- no claim that the Plotkin cap is sharp.

## 6. Precise route stop immediately inside the middle interval

The next symmetric pair has

\[
(d,m)=(5,413,72,860)\quad\text{or}\quad(840,822,908,269),
\]

so \(s=72,860\).  After one coordinate deletion the would-be Plotkin
denominator is negative:

\[
(72,859)(908,269)-67,448(981,128)=449,727. \tag{6.1}
\]

Thus Theorem 2.1 stops exactly after the two proved endpoints.

A second incidence deletion makes the denominator positive:

\[
67,448\cdot981,127-72,858\cdot908,269=391,094,
\]

and the shortened Plotkin cap is

\[
\left\lfloor\frac{66,175,053,896}{391,094}\right\rfloor=169,204.
\]

However, exact nested incidence pullback gives only

\[
L\le30,682,446,
\]

because

\[
\left\lceil\frac{30,682,446\cdot72,860}{981,129}\right\rceil
 =2,278,521,
\quad
\left\lceil\frac{2,278,521\cdot72,859}{981,128}\right\rceil
 =169,204,
\]

whereas \(L=30,682,447\) forces \(2,278,522\) and then \(169,205\).
The resulting upper misses \(B^*-1\) by

\[
30,682,446-16,777,214=13,905,232.
\]

This is the precise obstruction to extending the same unstructured
shortening--Plotkin route by one more agreement value.  A successor must use
more than repeated incidence averaging plus the ordinary constant-weight
Plotkin inequality.

## 7. Lean correspondence

The stdlib-only package

```text
experimental/lean/l_fixedg_endpoint_plotkin
```

contains namespace `LFixedGEndpointPlotkin`.  It kernel-checks:

- both endpoint parameter identities;
- exact finite-\(p\), \(\ell=16,777,214\) Johnson boundary signs;
- the one-coordinate Plotkin numerator, denominator, quotient, and remainders;
- the arithmetic implications from the cross-multiplied Plotkin and incidence
  inequalities to \(L\le2,310,492\);
- the exact budget margin and fixed-\(G\) anchor add-back;
- the adjacent-shell one-step failure and two-step route-stop arithmetic.

`native_decide` is used only for closed natural-number propositions.  The two
variable arithmetic implications use the stdlib `omega` tactic.  Every theorem
has a `#print axioms` census.  The package does not axiomatize or claim a
kernel proof of the polynomial root bound, incidence averaging, or the
constant-weight double-counting argument; those proofs are given above.

## 8. Source labels

The source-bound dependencies are:

- `experimental/notes/thresholds/m31_fixed_g_universal_rs_embedding_v1.md`,
  Theorem 4.1, Corollaries 5.1 and 5.2, equation (5.2), and interval (6.1);
- `open-proximity.tex`, definition of \(J_{q,\ell}\) and the Johnson bound;
- the Lane-L print-block contract in `agents.md`.

# PROVED
