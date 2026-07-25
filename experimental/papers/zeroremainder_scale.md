# The missing zero-remainder scale: the lower endpoint was wrong
## Request worked from

Determine which side of the proved ordinary Reed--Solomon list-size bracket is misleading at the declared rate-half post-Johnson agreement, using only ratehalf_list_truth_paper.md, ratehalf_list_truth_note.md, ratehalf_list_lower_improved_paper.md, and cyclic_quotient_rotation_floor.tex.

## Executive verdict

The previously printed lower endpoint is provably the wrong end to trust as an approximation to the truth. The upper endpoint remains a valid theorem; no comparable defect is found in it.

The source quotient-rotation theorem assumes a strictly positive partial-fibre remainder 0 < s < c. Its proof extends to the boundary s=0. At that boundary there is no partial fibre, no distinguished deleted quotient point, and one may use all subsets of the quotient. The frozen agreement then admits the previously omitted specialization

```text
c = 1,
N = 2^41,
d = 2^34-1,
m = 2^40+2^34-1,
s = 0.
```

It gives the ordinary-list lower bound

```text
L_1
=
ceil(
  C(2^41, 2^40+2^34-1)
  /
  (2^41*q_0^(2^34-2))
),
q_0=6597069766657.
```

This is deliberately supplied in closed form. Its rigorously certified bit-length interval is

```text
1466604010422 <= bits(L_1) <= 1467447159516.
```

Consequently

```text
L_1 <= L_max(a) <= U_pack,
```

```text
1466604010422 <= bits(L_max(a)) <= 2095944040454.
```

The certified upper-to-lower bit-endpoint ratio is less than 143/100, because

```text
100*2095944040454 < 143*1466604010422.
```

The old bit gap of roughly 2.87 is therefore not a property of the row. It was caused mainly by omitting the zero-remainder boundary scale.

A second theorem identifies what cannot finish the job. An elementary greedy construction produces an abstract family of a-subsets with pairwise intersections at most k-1 whose cardinality has at least

1923364445404 bits.

Thus any upper-bound argument using only agreement-set sizes and the pairwise root bound cannot close the new bracket. A further improvement below that obstruction must use genuinely Reed--Solomon algebra, not only set packing.

The exact value of L_max(a) is not obtained.

## 1. Frozen row, object, and radius

Put

```text
q_0 = 6597069766657 = 3*2^41+1,
n   = 2^41 = 2199023255552,
k   = 2^40 = 1099511627776,
T   = 2^34 = 17179869184,
a   = k+T-1 = 1116691496959.
```

Let D be a multiplicative coset of size n in F_{q_0}, and let

```text
C = RS[F_{q_0},D,k].
```

For a received word u, let L_u(a) be the number of distinct degree-<k polynomials agreeing with u on at least a points of D, and define

```text
L_max(a) = max_u L_u(a).
```

The object is ordinary LIST, throughout. There is no CA or MCA numerator, no support-to-list conversion, no shift to C^+=RS(k+1), no radius shift, and no intrinsic-radius condition.

The exact closed-ball radius is

```text
delta = (n-a)/n
      = 1082331758593/2199023255552.
```

The row is strictly beyond the exact finite-field Johnson radius. In agreement form,

```text
a^2 < n(k-1),
n(k-1)-a^2 = 1170851739846527019909119.
```

The predecessor bracket was

```text
L_rot <= L_max(a) <= U_pack,
```

where

```text
L_rot
=
ceil(
  C(2^40-1,2^39+2^33-1)
  /
  (2^40*q_0^(2^33-2))
)
```

and

```text
U_pack
=
floor(
  C(2^41,2^40)
  /
  C(2^40+2^34-1,2^40)
).
```

The certified predecessor size bounds were

```text
721554505735 <= bits(L_rot) <= 738734374956,
bits(U_pack) <= 2095944040454.
```

The exact maximum was open.

## 2. Main theorem: zero-remainder quotient rotation
### Theorem 2.1 — zero-remainder cyclic quotient-rotation list floor

Let F_q be a finite field, let D be a multiplicative coset of even size n, and let

```text
C = RS[F_q,D,n/2].
```

Suppose c | n/2, put N=n/c, and choose an integer

```text
1 <= d <= N/2-1,
m = N/2+d.
```

Then some received word has at least

```text
ceil(C(N,m)/(N*q^(d-1)))
```

distinct degree-<n/2 codewords agreeing with it in exactly

```text
n/2+d*c
```

positions.

This is a direct ordinary-list theorem. It uses no conversion and no code shift.

### Explicit falsifier

The theorem is falsified by any finite field, multiplicative coset, and legal tuple (n,c,N,d,m) for which every received word has fewer than the displayed number of degree-<n/2 codewords at exact agreement n/2+dc. At the proof level, a falsifier must exhibit at least one of the following failures:

the rotated polynomial has a high-degree coefficient depending on a coefficient other than a_0,...,a_{d-1} and the fixed monic coefficient;

the number of possible high-degree parts exceeds N*q^(d-1);

the rotated polynomial has a zero on D outside the chosen subset, or misses a chosen root; or

two distinct subsets in one prefix fibre yield the same degree-<n/2 codeword.

### Proof

Write D=gamma H, where H is the multiplicative subgroup of order n, and put

```text
Q = D^c = {x^c : x in D}.
```

The power map D -> Q has fibres of size c, so |Q|=N. There is a fixed nonzero Delta such that

```text
y^N = Delta
```

for every y in Q.

For every m-subset A of Q, write

```text
P_A(Y) = product_{b in A}(Y-b)
       = sum_{j=0}^m a_j(A)Y^j.
```

Define the cyclic rotation

```text
R_A(Y)
=
rem_{Y^N-Delta}(Y^(N-d) P_A(Y))
```

```text
=
sum_{j=0}^{d-1} a_j(A)Y^(N-d+j)
+
Delta*sum_{j=d}^{m} a_j(A)Y^(j-d).
```

Set

```text
L_A(X) = R_A(X^c).
```

The positive-remainder theorem in cyclic_quotient_rotation_floor.tex multiplies this expression by a partial-fibre locator L_0 of degree s, and deletes one quotient point to reserve that partial fibre. When s=0, take L_0=1; coefficient-block non-overlap is vacuous, and no quotient point needs to be deleted. This is the only structural change.

Let k=n/2=cN/2. For j<d, the exponent c(N-d+j) is strictly larger than k. The monic term j=m=N/2+d begins at degree exactly k. Every term with d<=j<m has degree at most

```text
c(m-1-d) = c(N/2-1) < k.
```

Therefore the complete degree->=k part of L_A is determined by

a_0(A),...,a_{d-1}(A)

and the fixed monic coefficient a_m(A)=1.

Up to its fixed sign, a_0(A) is the product of the elements of A. It lies in one multiplicative coset of the order-N group underlying Q, so it takes at most N values. Each of a_1(A),...,a_{d-1}(A) takes at most q values. Hence the C(N,m) subsets occupy at most

```text
N*q^(d-1)
```

high-degree parts. One high-part fibre has at least the displayed ceiling.

Fix that fibre and call its common degree->=k polynomial U. Write

```text
L_A = U+E_A,
deg(E_A)<k.
```

Then -E_A is a codeword of C, and the received word is the evaluation of U on D. For x in D,

```text
R_A(x^c) = (x^c)^(N-d) P_A(x^c),
```

because (x^c)^N=Delta. The first factor is nonzero. Thus L_A vanishes on exactly the mc points above A, giving exact agreement

```text
mc = c(N/2+d) = n/2+dc.
```

Distinct subsets have distinct zero sets. Within one common high-part fibre this forces distinct L_A, distinct low parts E_A, and distinct codewords -E_A.

This proves the theorem.

## 3. Frozen specialization and certified size

Take

```text
c = 1,
N = n = 2^41,
d = T-1 = 2^34-1,
m = N/2+d = k+T-1 = a.
```

The exact agreement is

```text
n/2+d = k+T-1 = a.
```

### Theorem 2.1 gives

```text
L_1
=
ceil(
  C(2^41,2^40+2^34-1)
  /
  (2^41*q_0^(2^34-2))
)
<= L_max(a).
```

By binomial symmetry the numerator is also

C(128*T,63*T+1).
### Theorem 3.1 — certified bit interval for L_1

With bits(z) defined by

```text
2^(bits(z)-1) <= z < 2^bits(z)
```

for positive integers z, one has

1466604010422 <= bits(L_1) <= 1467447159516.
### Explicit falsifier

The interval is falsified by a failure of any one of these exact integer certificates or deductions:

2*63^22 > 65^22,
q_0 < 769*2^33,
2^19*769^46 < 1024^46,
T-2 = 46*373475417,
2^5*3^12 > 4^12,
ceil((T-1)/22) = 780903145,
ceil((T-2)/12) = 1431655766.
### Proof of the lower bit bound

The central binomial coefficient satisfies

```text
C(128*T,64*T) > 2^(128*T-42),
```

because the largest of the 128*T+1=2^41+1 binomial coefficients is at least their average, and 2^41+1<2^42.

For 1<=j<=T-1,

```text
C(128*T,64*T+j) / C(128*T,64*T+j-1)
=
(64*T-j+1)/(64*T+j)
>
63/65.
```

The exact certificate 2*63^22>65^22 implies that every block of at most 22 such ratios has product greater than 1/2. Since

```text
ceil((T-1)/22)=780903145,
```

we obtain

```text
C(128*T,65*T-1)
>
2^(128*T-42-780903145).
```

For the denominator,

```text
q_0 = 768*2^33+1 < 769*2^33
    = 2^43*(769/1024).
```

The exact certificate

```text
2^19*769^46 < 1024^46
```

and the exact division

```text
T-2 = 46*373475417
```

give

```text
q_0^(T-2)
<
2^(43*(T-2)-19*373475417).
```

After multiplying by 2^41, the real quotient inside the ceiling is greater than

```text
2^(85*T+3-780903145+19*373475417)
=
2^1466604010421.
```

Therefore

bits(L_1) >= 1466604010422.
### Proof of the upper bit bound

The numerator is strictly less than the full binomial sum:

```text
C(128*T,65*T-1) < 2^(128*T).
```

Also

```text
q_0 > 3*2^41 = 2^43*(3/4).
```

The exact certificate

```text
2^5*3^12 > 4^12
```

says (3/4)^12>2^-5. Partitioning the T-2 factors into

```text
ceil((T-2)/12)=1431655766
```

blocks of at most 12 gives

```text
q_0^(T-2)
>
2^(43*(T-2)-5*1431655766).
```

Hence the real quotient inside the ceiling is less than

```text
2^(85*T+45+5*1431655766)
=
2^1467447159515.
```

Its ceiling is at most that integral power of two, and therefore

bits(L_1) <= 1467447159516.
## 4. The product coordinate is exactly flat

The predecessor's d=1 exact character count showed that deleting one quotient point makes product fibres nonuniform. The zero-remainder construction uses the full quotient, where a different exact law holds.

### Theorem 4.1 — uniform full-quotient product fibres

Let Q be a multiplicative coset of a cyclic group of order N, and let 1<=m<=N-1 with gcd(m,N)=1. For every attainable product value z, the number of m-subsets A of Q satisfying

```text
product(A)=z
```

is exactly

```text
C(N,m)/N.
```

At the frozen specialization,

```text
N=2^41,
m=2^40+2^34-1
```

and m is odd, so gcd(m,N)=1. Thus the factor N=2^41 in the denominator of L_1 is exact, not a loose product-coordinate pigeonhole. All remaining possible looseness lies in the joint distribution of

a_1(A),...,a_{T-2}(A)

inside one fixed product class.

### Proof

Write Q=gamma H, with H=<h> cyclic of order N. Multiplication by h is a bijection on the m-subsets of Q, and

```text
product(hA)=h^m product(A).
```

Because gcd(m,N)=1, h^m generates H. Repeated multiplication therefore cycles transitively through all N product targets while preserving fibre cardinality. The C(N,m) subsets split into N equal fibres.

### Explicit falsifier

A falsifier is a cyclic coset Q, an integer m coprime to |Q|, and two attainable product targets with different m-subset counts. Equivalently, a falsifier must break the transitive action A -> hA or the identity product(hA)=h^m product(A).

## 5. New bracket and the answer to “which end?”

Combining Theorem 3.1 with the predecessor's deterministic cap gives

```text
L_1 <= L_max(a) <= U_pack,
```

where

```text
L_1
=
ceil(
  C(2^41,2^40+2^34-1)
  /
  (2^41*q_0^(2^34-2))
)
```

and

```text
U_pack
=
floor(
  C(2^41,2^40)
  /
  C(2^40+2^34-1,2^40)
).
```

The resulting certified bit bracket is

```text
1466604010422 <= bits(L_max(a)) <= 2095944040454.
```

The exact rational comparison

```text
100*2095944040454 < 143*1466604010422
```

shows that the upper endpoint now has fewer than 1.43 times as many bits as the guaranteed lower endpoint.

The predecessor's 33-scale census was correct under its strict positive-remainder contract 0<s<c. The present theorem adds one boundary scale, c=1,s=0; it does not refute that census. It refutes the interpretation of the c=2 slice as the strongest available quotient-rotation lower construction once the proof is closed under its natural zero-remainder boundary.

Thus the answer is:

The old lower endpoint is definitely wrong as a candidate for the true scale. The upper endpoint is still a valid cap and may also be loose, but that has not been proved here.

### Explicit falsifier of this verdict

The verdict is falsified if Theorem 2.1 fails at the frozen specialization, or if the displayed bit certificate for L_1 fails. A proof that U_pack is attained, or nearly attained, would not falsify the verdict; it would only show that the old lower endpoint was even farther from the truth.

## 6. A proved obstruction to packing-only upper bounds

The deterministic cap uses only one algebraic fact about distinct listed polynomials: their agreement sets with the same received word intersect in at most k-1 points. From each agreement set of size at least a, choose one a-subset; distinct codewords still give pairwise intersections at most k-1. The following theorem measures the limit of every argument restricted to that information.

Put

```text
s = T-1 = a-k.
```

Define the exact Johnson-neighbourhood volume

```text
V_pair
=
sum_{j=0}^{T-1} C(a,j) C(n-a,j)
```

and the greedy packing floor

P_pair
=
ceil(C(n,a)/V_pair).
### Theorem 6.1 — pairwise-intersection obstruction

There exists a family F of a-subsets of an n-element set such that

```text
|A intersect B| <= k-1
```

for all distinct A,B in F, and

```text
|F| >= P_pair.
```

At the frozen integers,

```text
bits(P_pair) >= 1923364445404.
```

Therefore no theorem whose only hypotheses are

```text
|A|=a,
|A intersect B|<=k-1 for A!=B
```

can prove a universal upper bound below P_pair. In particular, set packing and pairwise root counting alone cannot close the new RS bracket.

### Explicit falsifier

The existence theorem is falsified if the greedy selection process can delete more than V_pair candidate blocks in one step, or if two selected blocks can have intersection at least k. The bit bound is falsified by a failure of the displayed binomial lower bound, the factorial lemma below, or the exact exponent arithmetic.

### Proof of existence

For a fixed a-subset A, another a-subset B has intersection at least k exactly when

```text
j = a-|A intersect B|
```

lies in 0,...,T-1. For a fixed j, there are exactly

C(a,j) C(n-a,j)

such B: remove j points from A and add j points from its complement. Thus one selected block conflicts with at most V_pair candidates, including itself.

Repeatedly select one remaining block and delete its conflict neighbourhood. The selected blocks have pairwise intersection at most k-1, and at least ceil(C(n,a)/V_pair) blocks are selected.

### Certified size of the obstruction

The terms

C(a,j) C(n-a,j)

increase over 0<=j<=T-1, so

```text
V_pair
<=
T*C(a,T-1)*C(n-a,T-1).
```

For every positive integer r, the elementary factorial bound

```text
r! >= (r/3)^r
```

holds. One induction proof reduces the step to (1+1/r)^r<3, which follows from the binomial expansion and sum_{j>=0}1/j!<3. Consequently

```text
C(M,r) <= (3M/r)^r.
```

Here r=T-1, and

```text
a/r       = 65+64/(T-1) < 66,
(n-a)/r   = 63+64/(T-1) < 64.
```

Therefore

```text
C(a,r)     < 2^(8r),
C(n-a,r)   < 2^(8r),
V_pair     < 2^(16*T+18).
```

The numerator bound from Section 3 gives

```text
C(n,a) > 2^(128*T-42-780903145).
```

Hence

```text
P_pair
>
2^(112*T-60-780903145)
=
2^1923364445403,
```

and so

```text
bits(P_pair) >= 1923364445404.
```

This obstruction is not an RS lower bound. It proves that abstract agreement-set geometry is too permissive: an upper proof below this scale must exploit coefficient consistency, syndrome geometry, locator equations, or another specifically Reed--Solomon property.

## 7. Evidence for and against each endpoint
### Evidence that the lower endpoint was the defective one

The zero-remainder proof is the same cyclic rotation used in cyclic_quotient_rotation_floor.tex; the partial-fibre factor becomes 1, and the deleted quotient point is no longer needed.

The new scale uses the full domain N=2^41, rather than the N=2^40 quotient of the predecessor champion.

The exact product-flatness theorem shows that the first prefix coordinate is completely understood at this boundary.

The new certified lower bit count is far outside the predecessor interval, so this is not a rounding or entropy-estimate improvement.

### Evidence that L_1 may still be loose

The remaining T-2 coefficients are bounded only by the ambient count q_0^(T-2).

The earlier d=1 round proved that a coefficient-prefix pigeonhole can be strict after exact character analysis.

The construction is injective into one Hamming ball but is not exhaustive: arbitrary nearby codewords need not arise from this rotation family.

### Evidence for the upper cap

The interpolation-packing proof is deterministic and self-contained. If A_f is the agreement set of a listed polynomial f, then a fixed k-subset of D can lie in at most one A_f, because k values determine a degree-<k polynomial. Counting pairs (f,K) with K a k-subset of A_f gives

```text
L_u(a)*C(a,k) <= C(n,k).
```

This proves L_u(a)<=U_pack for every received word.

### Evidence against upper tightness

The cap forgets every algebraic relation except uniqueness from k evaluations. The abstract packing obstruction shows that pairwise set geometry alone remains enormous, but it does not show that such a packing can be realized by one RS received word. Tightness of U_pack therefore remains unsupported.

## 8. Routes killed

“The c=2 specialization is the strongest available rotation lower.” Killed by the legal zero-remainder extension at c=1, whose lower bit interval starts at 1466604010422.

“A positive partial fibre is essential to the rotation proof.” Killed by Theorem 2.1. At s=0, set L_0=1; non-overlap is vacuous, and all quotient points are available.

“The product-coordinate factor N may conceal another large gain at c=1.” Killed by Theorem 4.1. Because gcd(m,N)=1, the full-domain product fibres are exactly equal. Any further gain must come from the other T-2 coefficients.

“A sharper argument using only pairwise agreement-set intersections can close the bracket.” Killed by Theorem 6.1 and the exact obstruction P_pair, with at least 1923364445404 bits.

“The predecessor's 33-scale census was arithmetically wrong.” Killed as a criticism of that theorem: its census was for 0<s<c. The new result enlarges the theorem to a boundary case rather than finding an error inside the stated census.

“The exact list size is now determined.” Not obtained. The full high-prefix fibre and arbitrary off-construction codewords remain uncontrolled.

## 9. Certified stop, open questions, and natural next step
### Certified stop verdict

The round settles which endpoint was demonstrably misleading: the old lower endpoint. It does not determine L_max(a) and does not prove that the new lower is essentially tight.

The precise remaining obstruction has two faces.

Lower/construction face. On the fixed product class of a-subsets of D, no exact or sharply bounded maximum fibre is known for

```text
A -> (a_1(A),...,a_{T-2}(A)).
```

Upper/global face. No theorem in the supplied material bounds the number of RS agreement sets using algebra beyond the pairwise root condition and k-point interpolation uniqueness.

The stop verdict is falsified by either:

an exact or sharply bounded maximum-fibre theorem for the displayed full-domain prefix map; or

an RS-specific upper theorem that uses locator, syndrome, secant, or coefficient consistency and lowers U_pack at the frozen agreement.

### Natural next step

The highest-value next calculation is the c=1 full-domain prefix fibre, not the old c=2 fibre. Product flatness removes a_0; the exact target is therefore

```text
max_z
#{A subset D : |A|=a, product(A)=z_0,
  (a_1(A),...,a_{T-2}(A))=z}.
```

A lower-side success would enlarge L_1. An upper-side success would prove that the boundary construction is close to its own optimum. In parallel, an upper attack should model error supports as circuits through one syndrome in the Vandermonde parity-check geometry; any useful theorem must exclude the abstract packings counted by P_pair using genuinely RS-specific constraints.

## 10. References

Only the attached material was used.

cyclic_quotient_rotation_floor.tex:

sec:rate-half-cyclic-quotient-rotation-floor;

thm:rate-half-cyclic-quotient-rotation-floor;

eq:rate-half-list-floor;

eq:rate-half-exact-agreement;

eq:rate-half-cyclic-rotation.

ratehalf_list_truth_paper.md.

ratehalf_list_truth_note.md.

ratehalf_list_lower_improved_paper.md.

The round-internal names above resolve in this repository as follows.

- `cyclic_quotient_rotation_floor.tex` is the integrated source theorem carried in
  `experimental/experiments.tex`, at the labels
  `sec:rate-half-cyclic-quotient-rotation-floor`,
  `thm:rate-half-cyclic-quotient-rotation-floor`, `eq:rate-half-list-floor`,
  `eq:rate-half-exact-agreement`, and `eq:rate-half-cyclic-rotation`.
- `ratehalf_list_truth_paper.md` and `ratehalf_list_truth_note.md` are
  `experimental/papers/ratehalf_list_truth.md` and
  `experimental/notes/thresholds/ratehalf_list_truth.md`; both were submitted and
  were not yet integrated when this round ran.
- `ratehalf_list_lower_improved_paper.md` is
  `experimental/papers/ratehalf_list_lower_improved.md`; it was submitted and was
  not yet integrated when this round ran.

## 11. Derivation-direction ledger
| Printed quantity | Direction | Derivation or certification |
| --- | --- | --- |
| q_0=6597069766657=3*2^41+1 | frozen | request and attached predecessor material |
| n=2^41=2199023255552 | frozen | request |
| k=2^40=1099511627776 | frozen | request |
| T=2^34=17179869184 | defined / derived | abbreviation for the agreement excess plus one |
| a=k+T-1=1116691496959 | frozen / derived identity | request and exact addition |
| radius numerator 1082331758593 and denominator 2199023255552 | derived | exact subtraction n-a and the frozen n |
| Johnson squared gap 1170851739846527019909119 | frozen / derived | exact subtraction supplied in the predecessor material |
| predecessor L_rot and its bit interval | derived from proved theorem / bounded | ratehalf_list_truth_paper.md and ratehalf_list_truth_note.md |
| U_pack and bits(U_pack)<=2095944040454 | derived from proved theorem / bounded | interpolation double count and the predecessor's integer certificate |
| zero-remainder theorem | derived from proved source mechanism | the proof of thm:rate-half-cyclic-quotient-rotation-floor, with L_0=1 and no deleted quotient point |
| c=1,N=2^41,d=T-1,m=a,s=0 | derived | exact solution of n/2+dc=a at the zero-remainder boundary |
| L_1 closed form | derived from Theorem 2.1 | frozen specialization |
| 2*63^22>65^22 | enumerated exact certificate | finite integer comparison; intended native_decide target in the Lean suggestion |
| ceil((T-1)/22)=780903145 | derived / enumerated | exact Euclidean division |
| q_0<769*2^33 | derived | q_0=768*2^33+1 and 1<2^33 |
| 2^19*769^46<1024^46 | enumerated exact certificate | finite integer comparison; intended native_decide target |
| T-2=46*373475417 | derived / enumerated | exact Euclidean division |
| lower exponent 1466604010421 | bounded / derived | central-binomial average, 22-step ratio blocks, and the upper field-power certificate |
| lower bit endpoint 1466604010422 | bounded | one more than the strict lower power exponent |
| 2^5*3^12>4^12 | enumerated exact certificate | finite integer comparison; intended native_decide target |
| ceil((T-2)/12)=1431655766 | derived / enumerated | exact Euclidean division |
| upper exponent 1467447159515 | bounded / derived | binomial-sum upper bound and lower field-power certificate |
| upper bit endpoint 1467447159516 | bounded | one more than the integral upper power exponent |
| comparison 100*2095944040454<143*1466604010422 | derived / enumerated | exact multiplication and comparison |
| uniform product-fibre count C(N,m)/N | derived from proved group action | transitive multiplication action and gcd(m,N)=1 |
| V_pair closed form | enumerated definition | exact conflict-neighbourhood count in the Johnson graph |
| P_pair closed form | derived | finite greedy packing construction |
| factorial constant 3 in r!>=(r/3)^r | bounded | elementary induction via (1+1/r)^r<3 |
| V_pair<2^(16*T+18) | bounded | monotonicity of the conflict terms and two binomial bounds |
| obstruction exponent 1923364445403 | bounded / derived | numerator lower exponent minus conflict-volume upper exponent |
| obstruction bit endpoint 1923364445404 | bounded | one more than the strict power exponent |
| source-scale counts 33, c=2, and the added boundary c=1,s=0 | frozen / derived | the predecessor census under 0<s<c, and Theorem 2.1 at the newly admitted boundary |
| small ratio-block constants 22,63,65,46,19,769,1024,12,5,3,4 | chosen then enumerated | rational lower/upper approximants selected for exact power-of-two block certificates |
| small packing constants 66,64,198,192,256,8,16,18,112,60 | derived / bounded | exact rewritings of a/(T-1) and (n-a)/(T-1), followed by power-of-two domination and exponent subtraction |
| comparison constants 143 and 100 | chosen / enumerated | exact rational certificate that the new bit-endpoint ratio is below 1.43 |
| exact L_max(a) | not obtained / open | full prefix fibre and off-construction codewords are unclassified |
## Serendipity epilogue

The most interesting unasked-for feature is that the strongest scale is not another interior quotient at all. It is the point where the quotient construction stops quotienting: c=1. The strict remainder condition hid this boundary because the partial-fibre gadget disappears there, but its disappearance is beneficial—it restores the deleted quotient point and doubles the logarithmic scale of the candidate universe. At the same time, the full cyclic symmetry makes the product coordinate exactly flat, so the boundary both strengthens the construction and simplifies the first unresolved statistic.