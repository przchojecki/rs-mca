# M1 KoalaBear branch-3 low-excess common-carrier cut v1

**Status:** PROVED CONDITIONAL GLOBAL-CARRIER OWNER / EXACT EXCESS-\(10\)
BUDGET CUTOFF / FAIL-CLOSED ROUTE CUT / PARTIAL UPPER LEDGER.

This packet gives one rigorous owner inside the third KoalaBear first-match
branch at

\[
A=1{,}116{,}048.
\]

It does not prove that the owner is exhaustive.  It proves that one selected
actual-error family contained in one global carrier of excess at most ten has
a budget-fitting distinct-slope cap.  If no such single-carrier certificate is
available, the executable policy emits
`UNPAID_NOT_CERTIFIED_LOW_EXCESS` and leaves the ledger unchanged.

The packet therefore cuts the next branch into a paid low-excess side and an
explicit unpaid residual.  It does not close branch 3 or the KoalaBear row.

## Statement audited

Let

\[
C=\operatorname{RS}_{F}(D,k),\qquad |D|=n,
\]

and let \(f,g:D\to F\) be one received pair.  At agreement \(A\), put

\[
R=n-k,\qquad j=n-A,\qquad t=A-k=R-j.
\]

The predecessor packet defines the rank-drop envelope

\[
Z_{2,\mathrm{env}}(f,g)
=
\{\gamma\in\operatorname{Bad}_A(f,g):
\operatorname{rank}_{F}M_A(\gamma)<t\}.
\]

Define the safe full-row-rank successor envelope

\[
Z_{3,\mathrm{pre}}(f,g)
=
\operatorname{Bad}_A(f,g)\setminus Z_{2,\mathrm{env}}(f,g).
\tag{1}
\]

The literal first-match branch-3 residual first removes any realized earlier
cells and is therefore a subset of (1).  The envelope may still contain
full-row-rank slopes belonging to the incomplete branch-1 interface.  This is
safe: every bound below is monotone under deleting arbitrary earlier slopes.

Let \(Z\subseteq Z_{3,\mathrm{pre}}(f,g)\).  For every \(\gamma\in Z\),
choose one declared exact-\(A\) noncontained witness

\[
(\gamma,S_\gamma,c_\gamma),\qquad |S_\gamma|=A,
\]

and define

\[
y_\gamma=f+\gamma g,\qquad
e_\gamma=y_\gamma-c_\gamma,\qquad
E_\gamma=\operatorname{supp}(e_\gamma).
\tag{2}
\]

If one set \(U\subseteq D\) contains every selected \(E_\gamma\), put

\[
\kappa(U)=\max\{0,|U|-R\}.
\tag{3}
\]

Then:

1. if \(\kappa(U)=0\), the independent-union ray theorem gives
   \[
   |Z|\le j+1;
   \tag{4}
   \]
2. if \(\kappa(U)\ge1\), the agreement-weighted transverse-secant theorem
   gives
   \[
   |Z|
   \le
   B_{\kappa(U)}
   :=
   \left\lfloor
   \frac{\binom{R+\kappa(U)}{\kappa(U)+1}}
        {\binom{R+\kappa(U)-j-1}{\kappa(U)}}
   \right\rfloor.
   \tag{5}
   \]

Consequently any valid single global carrier with
\(\kappa(U)\le10\) supplies a budget-fitting global distinct-slope owner.
A supplied carrier of larger excess does not prove that the minimum possible
global excess is large; it only fails to certify this owner.

All uses of “global” in this packet mean global across the retained slopes of
one fixed received pair \((f,g)\), not across different received pairs.  The
empty retained set is trivial and is assigned minimum excess zero.

## Actual-witness semantics

The support \(E_\gamma\) in (2) is the actual nonzero error support.  It is not
the chosen size-\(j\) co-support \(D\setminus S_\gamma\), which may contain
zero-amplitude padding.

Because \(c_\gamma\) explains \(y_\gamma\) on \(S_\gamma\),

\[
E_\gamma\subseteq D\setminus S_\gamma,
\qquad
|E_\gamma|\le j.
\tag{6}
\]

The predecessor rank identity is

\[
\operatorname{rank}_F M_A(\gamma)
=\min\{t,|E_\gamma|\}.
\tag{7}
\]

Every slope in \(Z_{3,\mathrm{pre}}\) has full row rank, so (7) gives

\[
t\le |E_\gamma|\le j.
\tag{8}
\]

Write

\[
y_0=s(f),\qquad y_1=s(g)
\]

for the received syndromes.  From (2),

\[
y_0+\gamma y_1=s(e_\gamma)\in V_{E_\gamma}.
\tag{9}
\]

The incidence is transverse:

\[
\{y_0,y_1\}\not\subseteq V_{E_\gamma}.
\tag{10}
\]

Indeed, if both syndromes lay in \(V_{E_\gamma}\), then both received
coordinates would be simultaneously explained on \(D\setminus E_\gamma\).
By (6), that set contains \(S_\gamma\), contradicting the declared
noncontainment on \(S_\gamma\).

This is why an arbitrary explaining codeword detached from a declared bad
witness is not an admissible input to the classifier.

## One global carrier

Equations (4)--(5) apply to one set \(U\) containing the selected actual error
supports for the entire retained slope set \(Z\).

They do not justify:

- choosing a different carrier for every slope;
- splitting \(Z\) among many carriers and taking the maximum cap;
- charging \(B_\kappa\) once per support, chart, or carrier; or
- replacing the actual supports by padded size-\(j\) co-supports.

If several carrier cells are used, their charges must be summed after a
separate disjoint or covering argument.  No such bounded-cover theorem is
proved here.

For \(\kappa\ge1\), definition (3) already gives \(|U|=R+\kappa\), which is
the carrier size required by the imported theorem.

## Imported owner for positive excess

The proved agreement-weighted transverse-secant theorem applies to a weighted
RS parity restriction on a carrier of size \(R+\kappa\), \(\kappa\ge1\).
For selected errors of weight at most \(j<R\) satisfying (9)--(10), it gives

\[
\sum_{\gamma\in Z}
\binom{|U\setminus E_\gamma|-1}{\kappa}
\le
\binom{R+\kappa}{\kappa+1}.
\tag{11}
\]

Since

\[
|U\setminus E_\gamma|
\ge R+\kappa-j,
\]

every slope contributes at least

\[
\binom{R+\kappa-j-1}{\kappa}
\]

to (11), proving (5).  The theorem explicitly remains valid after arbitrary
earlier first-match deletion.

The case \(\kappa=0\) is handled separately by the independent-union ray
bound in `experimental/rs_mca_thresholds.tex`, giving (4).

## Minimum global excess and executable policy

Mathematically one may define

\[
\kappa_*(Z)
=
\min_{\substack{\text{one valid declared witness}\\
                 \text{for every }\gamma\in Z}}
\max\left\{
0,
\left|\bigcup_{\gamma\in Z}E_\gamma\right|-R
\right\}.
\tag{12}
\]

Thus the pair-level alternatives

```text
kappa_*(Z) <= 10
kappa_*(Z) >= 11
```

are exhaustive, and the first alternative is paid by (4)--(5).

The certificate does not compute the minimum in (12).  Its fail-closed policy
is instead:

```text
valid supplied actual-witness selection
+ one global carrier
+ all selected actual supports contained
+ transversality
+ certified excess <= 10
    -> CERTIFIED_LOW_EXCESS_COMMON_CARRIER;

otherwise
    -> UNPAID_NOT_CERTIFIED_LOW_EXCESS.
```

The fallback does not assert \(\kappa_*(Z)\ge11\).  It records only that the
low-excess owner has not been certified.

## Exact KoalaBear cutoff

At the deployed row,

\[
\begin{aligned}
n&=2{,}097{,}152,\\
k&=1{,}048{,}576,\\
R&=1{,}048{,}576,\\
A&=1{,}116{,}048,\\
j&=981{,}104,\\
t&=67{,}472.
\end{aligned}
\]

The exact caps are:

| excess \(\kappa\) | global cap |
|---:|---:|
| 0 | \(981{,}105\) |
| 1 | \(8{,}147{,}918\) |
| 2 | \(84{,}416{,}263\) |
| 3 | \(983{,}902{,}549\) |
| 4 | \(12{,}232{,}092{,}309\) |
| 5 | \(158{,}406{,}193{,}634\) |
| 6 | \(2{,}109{,}949{,}210{,}211\) |
| 7 | \(28{,}689{,}347{,}099{,}870\) |
| 8 | \(396{,}280{,}526{,}311{,}830\) |
| 9 | \(5{,}542{,}092{,}977{,}392{,}141\) |
| 10 | \(78{,}289{,}526{,}705{,}722{,}101\) |
| 11 | \(1{,}115{,}145{,}741{,}750{,}273{,}207\) |

The current post-branch-2 budget is

\[
B_{\mathrm{remaining}}
=274{,}980{,}725{,}509{,}174{,}142.
\]

Therefore

\[
B_{10}
=78{,}289{,}526{,}705{,}722{,}101
<B_{\mathrm{remaining}},
\tag{13}
\]

while

\[
B_{11}
=1{,}115{,}145{,}741{,}750{,}273{,}207
>B_{\mathrm{remaining}}.
\tag{14}
\]

The \(10/11\) boundary is exact.  For the unfloored positive-excess ratio,

\[
\frac{B_{\kappa+1}^{\mathrm{raw}}}{B_\kappa^{\mathrm{raw}}}
=
\frac{(R+\kappa+1)(\kappa+1)}
     {(\kappa+2)(R+\kappa-j)}.
\tag{15}
\]

The numerator minus denominator in the comparison with \(1\) is

\[
j(\kappa+2)-R+1>0
\qquad(\kappa\ge1),
\tag{16}
\]

so the raw caps are strictly increasing across the checked range.  The
verifier independently evaluates every binomial using Python exact integers.

## Ledger effect

No deployed global carrier certificate is supplied.  Hence this packet banks
no charge; its machine-readable `charges` list is empty and its branch-3
charge is null:

\[
U_{\mathrm{paid}}
=2{,}602{,}220{,}945,
\qquad
B_{\mathrm{remaining}}
=274{,}980{,}725{,}509{,}174{,}142.
\]

If a later exhaustive theorem certified \(\kappa_*\le10\), the worst allowed
conditional update would be

\[
\begin{aligned}
U_{\mathrm{paid}}
&\le78{,}289{,}529{,}307{,}943{,}046,\\
B_{\mathrm{remaining}}
&\ge196{,}691{,}198{,}803{,}452{,}041.
\end{aligned}
\]

Those numbers are printed only as a conditional consequence.  They are not
the current ledger.

\(U_2\), \(U_Q\), and \(U_A\) remain null.  Branch 3, branches 4--5, the
field-full quadratic support union, and the complete row inequality remain
open.

## Reproducibility

```bash
python3 experimental/scripts/verify_m1_kb_branch3_low_excess_carrier_cut_v1.py --check
python3 experimental/scripts/verify_m1_kb_branch3_low_excess_carrier_cut_v1.py --tamper-selftest
python3 experimental/scripts/verify_agreement_weighted_transverse_secant.py

python3 experimental/scripts/verify_m1_kb_branch2_rank_deep_owner_v1.py --check
python3 experimental/scripts/verify_m1_kb_branch2_rank_deep_owner_v1.py --tamper-selftest
```

The new verifier checks source hashes, predecessor interfaces, all exact caps
for excess \(0\) through \(11\), the monotonicity margins, the \(10/11\)
budget boundary, fail-closed classifier controls, null open terms, and the
absence of a ledger deduction.

## Audit summary

- **Parameter dependence:** the owner is general in \(R,j,\kappa\); the
  budget cutoff \(10\) is KoalaBear-specific.
- **Layer-cake / dyadic summability:** not applicable.
- **Moment / Markov / Chebyshev:** not applicable.
- **Numerical evidence:** exact big-integer arithmetic only; no numerical
  experiment is used as proof.
- **Verdict:** GREEN for the conditional global-carrier owner and executable
  route cut.  YELLOW for branch 3 and the complete row.

## Minimal next action

Attack the explicit unpaid residual:

```text
UNPAID_NOT_CERTIFIED_LOW_EXCESS.
```

The next theorem must either prove a witness-exhaustive global carrier of
excess at most ten, produce a budget-fitting disjoint bounded carrier cover,
or derive a new named owner from genuinely high global shadow excess.  Do not
sum unrelated carrier caps, do not bank \(B_{10}\) prematurely, and do not
move to degree three.
