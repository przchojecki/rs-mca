---
workboard_item: M1
row: Mersenne-31 ordinary LIST stress row at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: "For the natural 32-root one-error puncture/division lift, the exact target-list census is N=sum_alpha L_alpha+F-Omega. Partner-list size alone does not determine N; in particular the specialization N=32L-489471 requires the additional unproved identity Omega-F=489471."
architecture: DIRECT
partition_digest: N/A
atom_or_cell: DIRECT_ROOT_LIFT_CENSUS
quantifier: "Every received word after an exact 32-coordinate codeword translation, with all free-residue and cross-root multiplicities retained."
projection_and_unit: ordinary codewords in one Hamming ball
claimed_bound: "Conditional endpoint only: if all 32 partner lists have size at most L and Omega-F>=489471, then L<=539583 gives N<=16777185<B_star; L=539584 with equality gives N=16777217>B_star."
status: COUNTEREXAMPLE / AUDIT / CERTIFIED_STOP
impact: ROUTE_CUT
falsifier: "A deployed theorem proving equality of all 32 partner sizes and Omega-F=489471, with exact whole-ball exhaustivity, would invalidate the stop verdict."
replay: "python3 experimental/scripts/verify_m31_rootlift_bridge.py --check; python3 experimental/scripts/verify_m31_rootlift_bridge.py --tamper-selftest"
---

# M31 one-error root-lift census: corrected contract and certified stop

## Status

**PROVED exact root-lift census identity / COUNTEREXAMPLE to a
partner-size-only count law / PROVED conditional endpoint arithmetic /
CERTIFIED STOP for the reported deployed specialization.**

The previously reported numbers

\[
 L=539583\longmapsto 16777185,\qquad
 L=539584\longmapsto 16777217
\]

are arithmetically consistent with

\[
 N_{\rm reported}(L)=32L-489471.
\]

That affine expression is not, however, the count law of a one-error
Reed--Solomon root lift.  The exact law contains two further integers:

* the number \(F\) of target-list codewords with no selected root; and
* the overlap excess \(\Omega\) of target codewords that occur in more than one
  rooted slice.

For the canonical puncture/division lift proved below,

\[
 \boxed{N=\sum_{\alpha\in A}L_\alpha+F-\Omega.}
 \tag{1}
\]

If all 32 partner lists happen to have one common size \(L\), this becomes

\[
 \boxed{N=32L+F-\Omega.}
 \tag{2}
\]

Thus the reported formula is equivalent to the additional exact assertion

\[
 \boxed{\Omega-F=489471.}
 \tag{3}
\]

No repository artifact defines a deployed object for which (3), equality of the
32 partner-list sizes, and whole-ball exhaustivity are proved.  An exhaustive
finite Reed--Solomon counterexample over \(\mathbb F_{37}\) shows that even with
exactly 32 roots and the same partner-list size for every root, the target list
is not determined by that size.  The packet therefore records a certified stop,
not a deployed row closure.

## Mandatory packet block

```text
row:                 (F_(p^4), D, K=1048576, n=2097152, rho=1/2)
object:              ordinary LIST, not MCA
radius/agreement:    delta=981129/2097152 and agreement 1116023
Johnson comparison:  post-Johnson row; no Johnson theorem is invoked here
bound:               conditional N(L)=32L-489471 only under Omega-F=489471
route:               DIRECT_ROOT_LIFT_CENSUS
CA_or_MCA_input:     none
code_shift:          punctured C^-_alpha=RS(D\{alpha},K-1) -> C=RS(D,K)
status:              COUNTEREXAMPLE / AUDIT / CERTIFIED_STOP
```

## 1. Deployed arithmetic and the recovered numerology

Freeze

\[
 p=2^{31}-1=2147483647,\qquad
 q=p^4=21267647892944572736998860269687930881,
\]
\[
 n=2^{21}=2097152,\qquad K=2^{20}=1048576,
\]
\[
 a=1116023,\qquad R=n-a=981129,\qquad w=a-K=67447,
\]
and
\[
 B^*=\left\lfloor q/2^{100}\right\rfloor
     =16777215=2^{24}-1.
\]

The field size was recomputed both as \(p^4\) and as

\[
 2^{124}-4\cdot2^{93}+6\cdot2^{62}-4\cdot2^{31}+1.
\]

The numerical law is not random.  The order-32 calibration gives

\[
 n=32\cdot65536,
 \qquad
 a=17\cdot65536+1911,
 \qquad
 w=65536+1911.
\]

Also

\[
 B^*+1=8n.
\]

Consequently

\[
 8(1911+1)=15296,
\]
\[
 32\cdot15296-1=489471,
\]
and therefore

\[
 32L-489471
 =1+32(L-15296).
 \tag{4}
\]

The two reported inputs are

\[
 539583=8(w+1)-1,
 \qquad
 539584=8(w+1)=15296+2^{19}.
\]

Equation (4) explains why the endpoint pair straddles \(B^*\), but it does not
supply a code, a received word, a lift map, or an overlap theorem.

The exact evaluations are

\[
 32\cdot539583-489471=16777185=B^*-30,
 \tag{5}
\]
\[
 32\cdot539584-489471=16777217=B^*+2.
 \tag{6}
\]

Moreover,

\[
 B^*+489471
 =32\cdot539583+30,
\]

so, **conditional on the affine specialization**, the maximal integral input is

\[
 \left\lfloor\frac{B^*+489471}{32}\right\rfloor=539583
\]

with exact slack 30.  The next integer exceeds the budget by 2.

Without any overlap credit, even a rooted exhaustive union of 32 lists would
only give the crude threshold

\[
 \left\lfloor B^*/32\right\rfloor=524287,
\]
because
\[
 32\cdot524287=B^*-31,\qquad
 32\cdot524288=B^*+1.
\]

The improvement from \(524287\) to \(539583\) therefore depends entirely on the
missing free-residue/overlap identity (3).

## 2. Precise one-error partner-list object

Let \(\mathbb F\) be a field, let \(D\subseteq\mathbb F\) be a set of \(n\)
distinct evaluation points, and let

\[
 C=\operatorname{RS}_{\mathbb F}(D,K)
   =\{g|_D:\deg g<K\}.
\]

Fix a received word \(U:D\to\mathbb F\), an agreement threshold \(a\), and a
selected set \(A\subseteq D\) of 32 coordinates.  Assume \(K\ge32\), as in the
deployed row.

### 2.1 Exact normalization

Interpolation on \(A\) gives a polynomial \(h\) with

\[
 \deg h<32\le K,\qquad h(\alpha)=U(\alpha)\quad(\alpha\in A).
\]

Replace the received word by

\[
 U_0=U-h|_D.
\]

Translation by the codeword \(h|_D\) is a bijection between the original list
and the normalized list, and

\[
 U_0(\alpha)=0\qquad(\alpha\in A).
\]

This normalization changes neither list size nor Hamming agreement.

### 2.2 The punctured partner

For each \(\alpha\in A\), put

\[
 D_\alpha=D\setminus\{\alpha\},
\]
\[
 C^-_\alpha
 =\operatorname{RS}_{\mathbb F}(D_\alpha,K-1).
\]

Define the partner received word

\[
 V_\alpha(x)=\frac{U_0(x)}{x-\alpha}
 \qquad(x\in D_\alpha).
\]

The partner list is

\[
 P_\alpha
 =
 \left\{
 f\in\mathbb F[X]_{<K-1}:
 \#\{x\in D_\alpha:f(x)=V_\alpha(x)\}\ge a-1
 \right\}.
 \tag{7}
\]

Its exact parameters are:

```text
code:       RS_F(D\{alpha}, K-1)
length:     n-1
agreement:  a-1
errors:     (n-1)-(a-1)=n-a=R
radius:     R/(n-1)
```

At the deployed row this is

\[
 \operatorname{RS}_{\mathbb F_{p^4}}
   (D\setminus\{\alpha\},1048575),
\]
with length \(2097151\), agreement \(1116022\), errors \(981129\), and radius

\[
 \delta^-=\frac{981129}{2097151}.
\]

This is not the full-domain \(C^-\) used by the literal CS25 conversion.

### 2.3 Lift map and exact bijection

Define

\[
 \lambda_\alpha:P_\alpha\longrightarrow C,
 \qquad
 \lambda_\alpha(f)=((X-\alpha)f)|_D.
 \tag{8}
\]

The degree is \(<K\), so the image is in \(C\).  At \(\alpha\), both the lifted
polynomial and \(U_0\) are zero.  At every other coordinate,

\[
 (x-\alpha)f(x)=U_0(x)
 \iff
 f(x)=V_\alpha(x).
\]

Therefore every partner codeword with \(a-1\) agreements lifts to a target
codeword with at least \(a\) agreements.

Conversely, if a target-list polynomial \(g\) vanishes at \(\alpha\), then
\(g=(X-\alpha)f\) for a unique polynomial \(f\) of degree \(<K-1\).  Since the
target agreement includes \(\alpha\), \(f\) has at least \(a-1\) agreements with
\(V_\alpha\).

Thus (8) is an exact bijection

\[
 P_\alpha
 \simeq
 T_\alpha
 :=
 \{g\in\Lambda(C,U_0,a):g(\alpha)=0\}.
 \tag{9}
\]

Write

\[
 L_\alpha=|P_\alpha|=|T_\alpha|.
\]

Equation (9) is the complete theorem supplied by one-error root lifting.  It
does not assert that the 32 values \(L_\alpha\) are equal.

## 3. Correct count law

Let

\[
 T=\Lambda(C,U_0,a),\qquad
 T_{\rm root}=\bigcup_{\alpha\in A}T_\alpha,
\]
and let

\[
 F=|T\setminus T_{\rm root}|
\]

be the **free residue**, the target codewords that vanish at none of the 32
selected coordinates.

For \(g\in T_{\rm root}\), define its rooted multiplicity

\[
 m(g)=|\{\alpha\in A:g\in T_\alpha\}|.
\]

The **overlap excess** is

\[
 \Omega=\sum_{g\in T_{\rm root}}(m(g)-1).
 \tag{10}
\]

Double-counting the incidence set
\(\{(\alpha,g):g\in T_\alpha\}\) gives

\[
 \sum_{\alpha\in A}L_\alpha
 =
 \sum_{g\in T_{\rm root}}m(g)
 =
 |T_{\rm root}|+\Omega.
\]

Since \(T\) is the disjoint union of its rooted part and free residue,

\[
 \boxed{
 |T|=\sum_{\alpha\in A}L_\alpha+F-\Omega.
 }
 \tag{11}
\]

This is the full derivation.  No endpoint interpolation is used.

If every partner list has size \(L\), (11) reduces to

\[
 |T|=32L+F-\Omega.
 \tag{12}
\]

Hence

\[
 |T|=32L-489471
\]

holds **if and only if**

\[
 \Omega-F=489471.
\]

A suggested “one free anchor” interpretation would require

\[
 F=1,\qquad
 \Omega=489472=32\cdot15296.
\]

Neither statement follows from the partner-list definition.

## 4. Exact finite RS counterexample to an \(L\)-only law

The obstruction already occurs for an ordinary Reed--Solomon code over
\(\mathbb F_{37}\).

Take

\[
 D=\mathbb F_{37}=\{0,\ldots,36\},
 \qquad
 A=\{0,\ldots,31\},
\]
\[
 C=\operatorname{RS}_{\mathbb F_{37}}(D,2),
 \qquad
 a=2.
\]

Thus target codewords are affine polynomials.  For each \(\alpha\in A\), the
partner is

\[
 C^-_\alpha
 =
 \operatorname{RS}_{\mathbb F_{37}}(D\setminus\{\alpha\},1),
\]

the constant code, at agreement \(1=a-1\), length 36, errors 35, radius
\(35/36\).

Consider two normalized received words.  Both are zero on \(A\), and their
values at \(32,33,34,35,36\) are

\[
 U_A=(0,0,0,1,2),
 \qquad
 U_B=(0,0,0,1,1).
\]

These words are already normalized on all 32 selected roots.  The interpolation
step of Section 2.1 is therefore not invoked in this counterexample; its target
dimension \(K=2\) is not being used to interpolate 32 arbitrary values.

For every selected root \(\alpha\), the partner received word is zero on the
zero coordinates and has two distinct nonzero values at 35 and 36.  Therefore,
in both examples and for every \(\alpha\),

\[
 |P_\alpha|=3.
\]

The verifier exhausts all \(37^2=1369\) affine target polynomials and all
\(32\cdot37\) constant partner candidates.  It obtains:

| word | every \(L_\alpha\) | \(\sum L_\alpha\) | rooted union | \(\Omega\) | \(F\) | target list |
|---|---:|---:|---:|---:|---:|---:|
| \(U_A\) | 3 | 96 | 65 | 31 | 5 | 70 |
| \(U_B\) | 3 | 96 | 65 | 31 | 7 | 72 |

In each row,

\[
 |T|=96+F-31.
\]

The multiplicity histogram of the rooted union is the same in both examples:
64 codewords occur in exactly one rooted slice, and the zero polynomial occurs
in all 32 slices.  The target counts differ solely because the free residues
have sizes 5 and 7.

Therefore even the complete vector

\[
 (L_\alpha)_{\alpha\in A}=(3,\ldots,3)
\]

and the same overlap excess do not determine the target-list size.  A fortiori,
one scalar partner-list size \(L\) cannot imply an affine target count.

There is also no automatic disjointness of multiplication-by-root images.  For
distinct roots \(0\) and \(1\),

\[
 X(X-1)=(X-1)X.
\]

Equivalently, the root-0 lift of the partner polynomial \(X-1\) equals the
root-1 lift of the partner polynomial \(X\).  Any deployed disjointness claim
requires a separate theorem.

## 5. Conditional closure conversion

The endpoint arithmetic remains useful as a sharply stated **conditional**
contract.

Assume all of the following for one deployed received word after normalization:

1. every target codeword is included in the census (11);
2. all 32 partner lists have a common size at most \(L\); and
3. the overlap/free balance satisfies
   \[
   \Omega-F\ge489471.
   \]

Then

\[
 |T|
 \le32L-489471.
\]

Consequently

\[
 L\le539583
 \quad\Longrightarrow\quad
 |T|\le16777185=B^*-30<B^*.
 \tag{13}
\]

Under equality in the census balance, the next integer gives

\[
 L=539584
 \quad\Longrightarrow\quad
 |T|=16777217=B^*+2.
 \tag{14}
\]

Thus \(539583\) is the exact maximal partner input for the reported affine
formula, with slack 30, and \(539584\) is the exact first failing input, with
excess 2.

What is missing is not arithmetic.  It is a deployed theorem proving the common
partner size and the overlap/free balance.

## 6. Relation to the deployed order-32 calibration

The constants in the affine expression visibly reuse the deployed order-32
decomposition:

\[
 n=32\cdot65536,\qquad
 a=17\cdot65536+1911.
\]

This explains \(32\), \(1911\), \(15296=8(1911+1)\), and the endpoint
\(539584=8(67447+1)\).

It does **not** identify the order-32 quotient object with the coordinate-root
partner (7):

* an order-32 Chebyshev quotient has 32 quotient points whose complete fibres
  have 65536 row coordinates each;
* puncturing one coordinate has length \(n-1\), not 32;
* removing one quotient point changes agreement by 65536 row coordinates, not
  one;
* the proved order-32 sum-fibre theorem counts supports in one quotient target
  and gives a direct fibre cap, not the free-residue/overlap identity (11).

The numerical decomposition is provenance for the guessed formula, not a lift
theorem.

## 7. Relation to CS25

The CS25 route is genuinely independent.

The literal target-code bridge uses the full-domain source

\[
 C^-=\operatorname{RS}_{\mathbb F_{p^4}}(D,K-1)
\]

at the **same full-domain radius** \(R/n\), and concludes a list bound for

\[
 (C^-)^+=\operatorname{RS}_{\mathbb F_{p^4}}(D,K)=C.
\]

The alternative same-code route uses \(C\) as the CA source and bounds the
containing \(C^+=\operatorname{RS}(D,K+1)\), then uses containment.

By contrast, the root partner (7):

* is punctured to \(D\setminus\{\alpha\}\);
* has radius \(R/(n-1)\);
* depends on a selected root and normalized received word;
* has 32 separate lists;
* requires the free-residue and overlap census.

No CS25 hypothesis or conclusion supplies \(F\), \(\Omega\), equality of
partner-list sizes, or (3).  Conversely, a partner-list bound does not provide
the CA numerator required by CS25.

## 8. Relation to the fixed-\(G\) ordinary-RS embedding

The fixed-\(G\) construction is also a different object.  It embeds one
ordinary-RS list on the error complement into the deployed target list and adds
one anchor.  Its exact lower transfer is

\[
 L_{\rm partner}\longmapsto L_{\rm partner}+1.
\]

It has no 32-root family and no negative affine intercept.  It cannot be used
to recover (3).

## 9. Routes killed

Every route attacked in recovering the claim is recorded here.

### 9.1 Exact-number and history search

The integers \(539583\), \(539584\), \(16777185\), \(16777217\), and \(489471\)
were searched across current repository files, commits, issues, upstream PR
descriptions, and fork validation PRs.  No artifact contains the asserted
bridge or a definition of its partner object.

**Verdict:** provenance absent.

### 9.2 Two-endpoint affine interpolation

Two points determine the affine formula \(32L-489471\), but do not prove a
counting theorem.  Rewriting the intercept exposed the order-32 numerology but
no list map.

**Verdict:** arithmetic only.

### 9.3 Order-32 quotient-fibre interpretation

The order-32 packet supplies a 32-point quotient and a 65536-fold row fibre.
It changes row agreement by whole fibres and counts a quotient sum fibre.
It is not a one-coordinate, one-error lift.

**Verdict:** wrong code and radius.

### 9.4 Puncture-only one-error bound

The natural puncture/division object gives exact slice bijections (9), but a
target codeword may lie in zero, one, or several slices.  Puncturing alone gives
no target count from one partner size.

**Verdict:** corrected by (11).

### 9.5 Multiplication-by-root disjoint union

The lift maps are injective individually, but their images need not be
disjoint.  The explicit identity \(X(X-1)=(X-1)X\) is the smallest obstruction.

**Verdict:** false without a cross-root exclusion theorem.

### 9.6 Uniform common-core subtraction

A common core of size \(b\) in all 32 lists would give
\(b+32(L-b)=32L-31b\), not \(32L-489471\); moreover
\(489471\) is not divisible by 31.

**Verdict:** cannot produce the reported intercept.

### 9.7 Fixed-\(G\) ordinary-RS embedding

The source-bound map gives \(L+1\), not \(32L-489471\).

**Verdict:** independent lower adapter.

### 9.8 CS25 same-code containment

This route converts a CA numerator into a full-domain \(C^+\) list bound.  It
has no puncture, selected-root family, or overlap census.

**Verdict:** independent conditional theorem.

### 9.9 CS25 literal \(C^-\) partner

The literal target-code source is full-domain \(\operatorname{RS}(D,K-1)\) at
radius \(R/n\).  The root partner is punctured and has radius \(R/(n-1)\).

**Verdict:** same dimension shift, different object.

### 9.10 Whole-ball boundary or frozen-face reduction

Current whole-ball compiler notes explicitly record that boundary-shell and
frozen-face certificates do not exhaust the ordinary list ball.  They do not
supply the free residue \(F\).

**Verdict:** exhaustivity missing.

### 9.11 Partner-size-only closure

The \(\mathbb F_{37}\) counterexample has the same 32 partner sizes and the same
rooted overlap census but target counts 70 and 72.

**Verdict:** counterexample.

## 10. Adversarial epilogue

The strongest attack on the stop verdict is that the earlier phrase
“two-stage root lift” may have referred to a more specialized first-match
object in which the free residue and overlap excess were already fixed.  The
arithmetic suggests the intended hidden hypotheses could have been

\[
 F=1,\qquad\Omega=489472=32\cdot15296.
\]

That possibility is not logically excluded.  It does not rescue the reported
claim as a theorem: no code, radius, received-word normalization, second-stage
owner, exhaustivity statement, or proof of those two equalities exists in an
artifact.  The exact corrected contract (11) states the smallest missing
theorem.  A future source-bound proof of the displayed hypotheses would turn
the endpoint arithmetic in Section 5 into a valid conversion; until then the
specialization remains conditional.

**Outcome of adversarial attack:** the arithmetic specialization survives as a
conditional implication, but the deployed Reed--Solomon bridge does not.

## 11. Verification and formal boundary

The deterministic verifier

```text
python3 experimental/scripts/verify_m31_rootlift_bridge.py --check
python3 experimental/scripts/verify_m31_rootlift_bridge.py --tamper-selftest
```

runs in under one minute and checks every integer in the packet, including the
full \(\mathbb F_{37}\) enumeration.

The stdlib-only Lean package is

```text
experimental/lean/l_rootlift_bridge
```

and uses `native_decide` for the deployed arithmetic and finite counterexample
computations.  This is disclosed explicitly.  It imports no Mathlib and
contains no `sorry`, `admit`, or custom axiom.  In accordance with repository
policy, it was not built locally; no PR was opened in this task.

Steering files are provenance only.  The verifier does not hash-check
`agents.md`, does not require `PR_BODY.md`, and does not require an agents-log
entry.

## Nonclaims

* No unconditional M31 list upper bound is proved.
* No deployed equality of the 32 partner-list sizes is proved.
* No deployed value of \(F\) or \(\Omega\) is proved.
* No MCA bad-slope numerator is treated as a list count.
* No order-32 quotient root is treated as a one-coordinate root.
* No CS25 CA-input theorem is proved.

## Terminal verdict

```text
CERTIFIED STOP:
the reported endpoint arithmetic is exact, but the natural one-error root lift
obeys N=sum_alpha L_alpha+F-Omega, not a law in L alone.  The specialization
N=32L-489471 requires the missing deployed theorem Omega-F=489471 together with
uniform partner sizes and whole-ball exhaustivity.
```
