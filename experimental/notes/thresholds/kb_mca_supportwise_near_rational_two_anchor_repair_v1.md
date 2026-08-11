---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: "For m=K+w, w>=1, and 3w<=n-K, every actual received line has at most 2w near-rational support-wise MCA-bad finite slopes; the former +1 bound has an actual deployed >=67472-slope falsifier."
architecture: DIRECT
partition_digest: DIRECT
atom_or_cell: DIRECT (K3 regression only; no K3 owner or projection)
quantifier: every actual received line over every Reed-Solomon evaluation domain satisfying the displayed guard
projection_and_unit: distinct finite affine bad slopes per actual received line
claimed_bound: 134944 on the KoalaBear row; uniformly 2w
status: PROVED
impact: ROUTE_CUT
falsifier: a legal guarded received line with more than 2w near-rational support-wise bad finite slopes, or failure of any pinned deployed counterexample guard
replay: python3 -B experimental/scripts/verify_kb_mca_supportwise_near_rational_two_anchor_repair_v1.py --check --tamper-selftest && /usr/local/bin/sage experimental/scripts/verify_kb_mca_supportwise_near_rational_two_anchor_repair_v1.sage && ~/math_code/.venv/bin/python experimental/scripts/verify_kb_mca_supportwise_near_rational_two_anchor_repair_v1_flint.py
---

# Support-wise common-support route cut and two-anchor repair

## Verdict

The pinned foundation source makes a global-versus-local quantifier error:
the existence of one support on which the received pair is simultaneously
explained does **not** exclude an MCA-bad slope witnessed on a different
support.  This makes the printed common-support assertion in
`thm:capfp-slope-elim(b)` false and invalidates the printed one-slope
near-rational reductions `cor:capfr1-balanced-line` and `cor:capfp-line`.

This packet supplies both an actual deployed counterexample and a stronger
replacement theorem.  For a Reed--Solomon line at agreement (m=K+w), if

\[
  w\ge1,\qquad 3w\le n-K,
\]

then the number of support-wise MCA-bad slopes whose received word is within
distance at most (w) of a codeword is at most (2w).  Consequently

\[
 N_{\rm MCA\text{-}bad}(u,v;m)
 \le 2w+
 \#\{z:d_1(u+zv)\ge w+1,\ \operatorname{cen}(u+zv;m)>0\}.
\]

For KoalaBear this is the exact local charge

\[
 2w=2(1116048-1048576)=134944.
\]

This is a genuine theorem in distinct-slope units.  It does not define the
frozen Q/BC owner predicates, realize a K3 endpoint, or close the row.

## 1. Actual deployed counterexample to the old implication

Work over the deployed KoalaBear code

\[
 C=\operatorname{RS}[\mathbb F,D,K],\qquad
 (n,K,m,w)=(2097152,1048576,1116048,67472).
\]

Choose (w) distinct coordinates
(E=\{e_1,\ldots,e_w\}\subset D) and (w) distinct finite slopes
(\gamma_1,\ldots,\gamma_w\in\mathbb F).  Define

\[
 v(e_i)=1,\qquad u(e_i)=-\gamma_i,
\]

and set (u=v=0) on (D\setminus E).  The set (D\setminus E) has
size (n-w=2029680>m), so every (m)-subset of it is a common support,
explained by the zero codeword pair.

Fix (i).  Choose any (R\subset D\setminus E) with (|R|=m-1), and put

\[
 S_i=R\cup\{e_i\}.
\]

The word (u+\gamma_i v) vanishes on (S_i), so (h=0) explains it there.
The pair is not simultaneously explained on (S_i): if a polynomial of
degree less than (K) explained (v), it would vanish on the (m-1\ge K)
points of (R), hence be zero, contradicting its value (1) at (e_i).
Thus every (\gamma_i) is support-wise MCA-bad despite the common support
elsewhere.

Moreover every word (u+zv) is supported inside (E), so it is within
distance at most (w) of the zero codeword and has nonzero size-(m) census.
Therefore the old assertion that at most one near-rational slope remains has
an actual deployed counterexample with at least

\[
 w=67472
\]

distinct bad slopes.  This is a falsifier of the displayed conclusion, not
only of its proof prose.

## 2. Two-anchor near-rational theorem

Let (L) be the set of actual support-wise MCA-bad slopes (z) for which
the received word has a near-rational representation

\[
 u+zv=c_z+\eta_z,\qquad c_z\in C,\qquad \operatorname{wt}(\eta_z)\le w.
\]

The foundation's shifted-lattice dichotomy supplies exactly this
representation, with unique (c_z), whenever (d_1(u+zv)\le w) and the
agreement census is nonzero.

If (|L|\le1), then (|L|\le2w).  Otherwise choose two distinct anchors
(z_0,z_1\in L), and define

\[
 c_v=\frac{c_{z_1}-c_{z_0}}{z_1-z_0},\qquad
 c_u=c_{z_0}-z_0c_v,
\]

\[
 e_v=v-c_v
     =\frac{\eta_{z_1}-\eta_{z_0}}{z_1-z_0},\qquad
 e_u=u-c_u=\eta_{z_0}-z_0e_v.
\]

Hence

\[
 E:=\operatorname{supp}(e_u)\cup\operatorname{supp}(e_v)
 \subseteq
 \operatorname{supp}(\eta_{z_0})\cup
 \operatorname{supp}(\eta_{z_1}),
 \qquad |E|\le2w.
\]

For any (z\in L), the codeword

\[
 \Delta_z=c_z-(c_u+zc_v)=e_u+ze_v-\eta_z
\]

is supported on at most (3w) coordinates.  Since the Reed--Solomon minimum
distance is (n-K+1>3w), one has (\Delta_z=0), and therefore

\[
 \eta_z=e_u+ze_v.
\]

Choose an actual bad witness ((S,h)) for (z).  On
(S\setminus\operatorname{supp}(\eta_z)), the degree-less-than-(K)
polynomial (h-c_z) has at least (m-w=K) roots, so (h=c_z).  Thus
(e_u+ze_v=0) on (S).  Noncontainment on this same (S) supplies some
(x\in S) with ((e_u(x),e_v(x))\ne(0,0)), whence

\[
 e_v(x)\ne0,qquad z=-e_u(x)/e_v(x).
\]

Every slope in (L) is therefore one of the at most (|E|\le2w) coordinate
ratios.  This proves the theorem.

## 3. Source repairs and chronology

The source changes accompanying this packet make seven scoped repairs.

1. Both near-rational corollaries now charge (2w), not (1).
2. `thm:capfp-slope-elim(b)` now states the correct translation theorem:
   a common support yields a sparse pair with the identical bad-slope set.
3. The rank-one injection is reproved from one noncommon witness per bad
   slope, with the necessary `w>=1` exact-support hypothesis, and remains
   valid even when another common support exists.
4. A fixed identically split kernel is tangent-paid only at thresholds
   satisfying the existing guard `n-a'<=t` (including deficiency one).
   At arbitrary deficiency it remains a structural rank-one/spread route,
   not a payment; common-support deletion is never used.
5. The global code-line and owner-localization proofs now use the identical
   bad witness support.  They no longer infer global column-farness from
   support-wise badness.
6. Triple-collapse treats both small and large common coefficientwise cores
   by the same-support outside-coordinate injection.
7. The complete correction-ray theorem is explicitly scoped to MCA-rich
   records carrying a noncontained exact support; it makes no assertion for
   unrestricted rich agreement pairs.

For the two deployed MCA rows the literal charges are

| row | (w=m-K) | (2w) | `B_* - 2w` calibration (not an active remainder) |
|---|---:|---:|---:|
| KoalaBear | 67472 | 134944 | 274980728111260143 |
| Mersenne-31 | 67448 | 134896 | 16642319 |

These are standalone upper bounds for the full near-rational bad-slope
stratum, hence also for any first-match subset of it.  Integrating the charge
into a summed ledger still requires the declared owner order.  In the active
maximum-type order-32 route, the reserve and the `(S)/(A)/(E)` interfaces must
be updated rather than pretending this stratum costs one slope.

## 4. Public-DAG reconciliation

At public-DAG head
`3edb8b31b6735a0a2302a578a21dc6e50bd64046`, the node
`v13_2_near_rational_pair_proximity` correctly retains the two-anchor linear
algebra: two near-codeword slopes put the received pair within a common
`2w`-coordinate error support.  This packet imports that valid proximity
step and adds the missing same-witness argument.

The sibling node `v13_2_near_rational_supportwise_payment` correctly marks
the old support-wise inference REFUTED, but explicitly records that its
`GF(17)` fixture does not refute the final displayed one-slope inequality.
The deployed construction in Section 1 is strictly stronger at that seam:
it gives `67472` near-rational support-wise bad slopes while the balanced
set is empty, so the printed `+1` inequality itself is false.  The theorem
in Section 2 supplies the replacement `+2w` payment that the DAG node left
open.

The DAG's `l1_exact_shell_balanced_shifted_lattice_reduction` is a different
LIST exact-shell statement: its complete-agreement gcd guard removes one
codeword's non-exact support multiplicity.  This packet neither refutes nor
uses that result.  Likewise, the semantic balanced-core certificate nodes
remain conditional owner interfaces; the present theorem supplies no Q/BC
or K3 projection.

## 5. Relation to SEM-QBC and K3

This counterexample is a mandatory regression for any `SEM-QBC` adapter that
tries to globalize failure on one selected witness or delete slopes merely
because a common support exists elsewhere.  The packet does not evaluate or
decide the frozen Q/BC ownership of any post-tangent record.

Exact actual bad-slope witnesses feed the active Grande Finale first-match
classification without K3 endpoint realization.  The order-32 theorem
`thm:partial-relative` applies only after its common-factor branch is
separately routed; that unresolved routing remains inside spread frontier
`(S)`.  The other live frontiers are large-owner control `(A)` and exception
routing `(E)`.  This route must incorporate the exact near-rational charge and
same-support semantics; its reserve and interfaces have not yet been
regenerated.

## 6. Scope and nonclaims

- This is a finite-field proof, not numerical evidence.
- It has no layer-cake, moment, Markov, or Chebyshev step.
- It proves no value of `U_Q`, `U_BC`, `U_K3`, or `U_new`.
- It does not claim KoalaBear or universal closure.
- The actual counterexample refutes only the former source statements and
  any compiler that uses their global-common-support shortcut.
- The repaired (2w) theorem is uniform for every Reed--Solomon evaluation
  domain satisfying the displayed guard.
