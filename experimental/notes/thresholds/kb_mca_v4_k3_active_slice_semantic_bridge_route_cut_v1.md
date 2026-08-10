---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: "The printed degree-two source-pencil and rational-deck hypotheses do not imply preservation of the deployed evaluation carrier in the displayed endpoint coordinate.  The current active-v4 sources also do not define an executable post-Q balanced-core m_in=2,r_out=4 actual-record relation, so no chronology-correct K3 slope payment can yet be composed."
architecture: GRANDE_FINALE_V4_KB_MCA_TANGENT_SOURCE_ADAPTER_V1
partition_digest: 4fade91abc408264989babcff6f8f9bbd80bcec52545a5db15ac376bf17d88fc
atom_or_cell: ACTIVE_V4_BALANCED_CORE / K3 semantic bridge
quantifier: "Uniform row theorem remains open; countermodel is exact over the deployed base field and carrier."
projection_and_unit: DISTINCT_BAD_FINITE_SLOPES_PER_RECEIVED_LINE
claimed_bound: "No new bound. U_paid=981104 is independently repinned; U_Q, U_BC, U_new, and every K3 ledger quantity remain null."
status: PROVED DIRECT-COORDINATE ROUTE CUT / OPEN ACTUAL-SLICE BRIDGE
impact: ZERO PAYMENT / MAXIMAL SEMANTIC ROUTE CUT
falsifier: "An executable source-level Q/BC predicate and total actual-record relation with same-line reconstruction, exact projection fibers, chronology preservation, and an all-Z_BC complement fence would supersede this stop."
replay: "python3 experimental/scripts/verify_kb_mca_v4_k3_active_slice_semantic_bridge_route_cut_v1.py --check; python3 experimental/scripts/verify_kb_mca_v4_k3_active_slice_semantic_bridge_route_cut_v1.py --tamper-selftest; repeat both with python3 -O; /usr/local/bin/sage experimental/scripts/verify_kb_mca_v4_k3_active_slice_semantic_bridge_route_cut_v1.sage; ~/math_code/.venv/bin/python experimental/scripts/verify_kb_mca_v4_k3_active_slice_semantic_bridge_route_cut_v1_flint.py"
---

# KoalaBear K3 active-slice semantic bridge route cut v1

## Verdict

**OPEN GAP, with one exact direct-coordinate countermodel.**  The requested
source-bound K3 closure cannot currently be stated as an executable theorem on
actual active slopes, let alone proved and charged.  The first obstruction is
before the thirteen-route workboard:

1. the active row manifest gives English labels for the `Q` and `BC`
   predicates but no source-level relation on an MCA witness;
2. no source defines the subpredicate
   (Z_{BC}^{(m_{\rm in}=2,r_{\rm out}=4)});
3. the source-pencil compiler starts from a **supplied actual endpoint
   record**, while the active ledger starts from an actual received line and
   bad affine slope;
4. no map between those objects reconstructs the same received line, support,
   explaining polynomial, slope, first-match owner, and add-back position;
5. no exact projection-fiber bound converts endpoint labels or raw systems
   into distinct slopes.

The exact countermodel below proves a narrower negative statement.  Even over
the deployed base field, on the deployed carrier, and with all 36 selected
degree-two fibers split completely on that carrier, the printed
source-pencil/rational-deck identities do **not** imply that the displayed
deck involution preserves the carrier.  Thus a direct
endpoint-parameter-coordinate-to-evaluation-coordinate identification is
false.  This is a model-theoretic insufficiency result, not an actual MCA
bad-line counterexample and not a proof that every possible same-record
adapter fails.

Accordingly this packet makes zero ledger movement.  It does not replay the
eleven unresolved routes as payments because the premise needed to connect
them to actual slopes is absent.

## 1. Frozen active row and chronology

The active row is

```text
p                  = 2130706433
K                  = F_(p^6)
D                  = the subgroup of F_p^* of order 2^21
n                  = 2097152
k                  = 1048576
agreement          = 1116048
B*                 = 274980728111395087
architecture       = GRANDE_FINALE_V4_KB_MCA_TANGENT_SOURCE_ADAPTER_V1
partition digest   = 4fade91abc408264989babcff6f8f9bbd80bcec52545a5db15ac376bf17d88fc
unit               = distinct bad finite slopes per received line
```

For an actual received pair \(\mathbf r=(r_0,r_1)\), an MCA witness is

\[
  w=(\gamma,S,f_{\rm exp}),\qquad
  |S|\ge 1116048,
\]

with \((r_0+\gamma r_1)|_S=f_{\rm exp}|_S\),
\(\deg f_{\rm exp}<k\), and no simultaneous degree-\(<k\) explanation of
\((r_0,r_1)\) on \(S\).  MCA counts \(\gamma\), not witnesses, supports,
locators, endpoint labels, passports, gauges, or raw systems.

The exact active MCA chronology has four atoms:

\[
  U_{\rm MCA}=U_{\rm paid}+U_Q+U_{BC}+U_{\rm new}.
\]

The five-term chronology

\[
 U_{\rm paid}+U_Q+U_{\rm list-int}+U_{\rm ext}+U_{\rm new}
\]

belongs to the ordinary LIST certificate in
`experimental/grande_finale.tex`; `U_list-int` and `U_ext` are not MCA K3
atoms and are not imported here.

The exact #1139 tangent-pin repair has been replayed on the present source.
Both verifier modes and their tamper suites pass, so the only banked active
atom is

\[
 U_{\rm paid}=981104,
 \qquad
 B_*-U_{\rm paid}=274980728110413983.
\]

The second integer is the joint remaining reserve, not a K3 allocation.

A fresh build of the bound Lean package also passes.  Its checked declarations
use no user-declared axioms, but the pre-existing `CORRESPONDENCE.md` claim
that every printed axiom census is `[]` is too strong: Lean reports standard
`propext` and, for quotient-backed finite-set statements, `Quot.sound`.
This documentation drift does not change a theorem statement or the tangent
cardinality bound.  The exact three-file #1139 source-pin repair is preserved
rather than silently broadening it with an unrelated correspondence edit.

## 2. The missing typed theorem

Write \(\mathcal W_{\mathbf r}(a)\) for the actual witness relation above.
A usable K3 bridge must first define an executable relation

\[
 \operatorname{Rec}_{2,4}
 (\mathbf r,\gamma,S,f_{\rm exp};
 A_{\rm src},V_{\rm act},\Gamma,\psi,F,C,
 \text{orientation},\text{passport},\text{terminal}).
 \tag{SB}
\]

Every field in `(SB)` is source data, not prose metadata.  In particular it
must encode:

- the actual received line and slope;
- one valid support and explaining polynomial;
- the balanced-core witness after earlier-owner projection;
- the endpoint/source component and its field of definition;
- source line, orientation, source-cover/passport, and guards;
- the exact thirteen-route image;
- the first-match owner and add-back position.

Let \(Z_{<BC}(\mathbf r)\) denote the actual earlier-owner slope set.  The
first theorem needed is

\[
 Z_{BC}^{2,4}(\mathbf r)
 =\pi_\gamma\bigl(\operatorname{Rec}_{2,4}(\mathbf r)\bigr)
   \setminus Z_{<BC}(\mathbf r),
 \tag{COV}
\]

together with a public order giving a section \(s_{\mathbf r}\) and exact
fiber constants \(M_t\):

\[
 \pi_\gamma\circ s_{\mathbf r}=\operatorname{id},
 \qquad
 \#\{\gamma:\operatorname{Term}(s_{\mathbf r}(\gamma))=t\}\le M_t.
 \tag{FIB}
\]

Reconstruction from \(s_{\mathbf r}(\gamma)\) must return the identical
received line and slope and a valid support/explanation for it.  It must also
preserve the first-match owner, the add-back chronology, the field of
definition, all distinctness/nonvanishing guards, and any multiplicity used
in `(FIB)`.  A two-sided inverse is sufficient but not necessary.

Finally an all-\(Z_{BC}\) fence must route every record outside this slice to
an earlier owner, a separately paid component, or explicit `U_new`.  Defining
the slice as the image of endpoint records would make `(COV)` tautological
and would not prove coverage of actual active slopes.

None of `(SB)`, `(COV)`, `(FIB)`, or the complement fence appears in the
pinned source set.  The row manifest's `predicate_available=true` flags for
Q and BC are not executable predicates: their values are the strings
`BAD_SLOPE_NOT_EARLIER_AND_HAS_ACTIVE_V4_*_CERTIFICATE`.  In particular, a
witness-first lexicographic selector is unsafe because another witness for
the same slope may trigger Q before BC.

## 3. Exact deployed-carrier countermodel to the direct-coordinate shortcut

Let

\[
 p=2130706433,
 \qquad n=2^{21},
 \qquad \zeta=1213133211\in\mathbf F_p.
\]

Exact arithmetic gives \(\operatorname{ord}(\zeta)=n\).  Put

\[
 D=\langle\zeta\rangle\subset\mathbf F_p^\times,
 \qquad |D|=n.
\]

On the endpoint parameter line define

\[
 \tau(T)=1-T,
 \qquad h(T)=T(1-T).
\]

Then \(\tau\) is a nontrivial order-two element of
\(\operatorname{PGL}_2(\mathbf F_p)\subset\operatorname{PGL}_2(K)\), and

\[
 h\circ\tau=h.
\]

The exact carrier census has 1,071 unordered two-cycles
\(\{x,1-x\}\subset D\).  Take the first 36 in increasing-first-coordinate
order.  Use the first 30 as active fibers and the next six as source fibers.
Writing

\[
 u_i=h(x_i),\qquad v_j=h(y_j),
\]

define

\[
 P(Y)=\prod_{i=1}^{30}(Y-u_i),\qquad
 Q(Y)=\prod_{j=1}^{6}(Y-v_j),
\]

\[
 V_{\rm act}(T)=P(h(T)),\qquad A(T)=Q(h(T)),
\]

and

\[
 \frac{V_{\rm act}(T)}{A(T)^5}
 =F(h(T)),\qquad F(Y)=\frac{P(Y)}{Q(Y)^5}.
 \tag{CM}
\]

The verifier proves exactly:

- all 36 outer values are distinct and all fibers are unramified;
- the 60 active and 12 source roots are distinct elements of the actual
  deployed carrier \(D\);
- \(V_{\rm act}\) and \(A\) are monic, squarefree, and coprime, of degrees
  60 and 12;
- with \(W=\langle1,h\rangle\), every complete source locator
  \(h-v_j\) lies in \(W\), while
  \(V_{\rm act}\in\operatorname{Sym}^{30}(W)\);
- the rational composition identity `(CM)` holds over \(\mathbf F_p\), hence
  after scalar extension to \(K=\mathbf F_{p^6}\).

Nevertheless \(1\in D\) while \(\tau(1)=0\notin D\).  More globally, if
\(\tau(D)=D\), the two monic root polynomials would agree:

\[
 X^n-1=(1-X)^n-1.
\]

Their \(X^{n-1}\) coefficients are respectively \(0\) and \(-n\), and
\(p\nmid n\), a contradiction.  Therefore

\[
 \boxed{\tau(D)\ne D.}
\]

This proves that the printed local divisor, pencil, composition, and
rational-deck hypotheses do not themselves authorize the direct carrier
descent.

### Conjugacy disclosure

This countermodel is deliberately **direct-coordinate only**.  If
\(g(T)=T-\tfrac12\), then

\[
 g\tau g^{-1}(T)=-T.
\]

Since \(n\) is even, \(-1\in D\), so \(-T\) preserves \(D\).  The packet
therefore does **not** prove that no conjugated fold can preserve the
carrier.  Such a conjugacy is useful only if a new theorem proves that it
also transports the actual received line, support, explaining data, owner,
chronology, and all record guards.  No such record-level conjugacy theorem is
currently present.

## 4. Architecture mismatch

The older equality-wall source chain contains genuine source-bound
ingredients, but it is not in the active partition.  Its architecture is

```text
GRANDE_FINALE_V4_KB_MCA_TANGENT_DEEP_SOURCE_RATIONAL_C5_BASE_TWIST_
FROBENIUS_9208_FIRST_GAP_PENCIL_IMAGE_ADAPTER_V1
```

with partition digest

```text
7a57fa877417920862ed2fe2e5c569852555f78b73b046d320d5e7a65d98ebaa
```

and seven paid owners before Q and BC.  The current tangent-only partition
has digest `4fade91a...` and only the tangent owner before Q.  No theorem maps
old graph records into the current first-match partition while preserving the
same received line and inherited charge.

Nor is the historical result already a cap of 68 slopes.  Its target is at
most 68 distinct source-map equivalence classes per transversal projective
residue line, after globally deduplicating directions that induce the same
map.  An occupied projective residue direction has a source-map image of at
most 1,894,736 slopes; a class/direction is not itself an affine slope.

The historical reduction separately empties the lower (q=1) range and,
for the exact (q=2) range, excludes splitting degrees 2 through 11.  Its
proved no-packet interval is precisely the integer interval

\[
  3912\le \delta\le118076.
\]

The remaining low-excess windows are windows in (h=\delta-g), subject to
(67472\le\delta<134944):

```text
degree 12: 118077 <= h <= 132382
degree 13: 119375 <= h <= 134943
degree 14: 120487 <= h <= 134943
degree 15: 121451 <= h <= 134943
degree 16: 122294 <= h <= 134943
```

The general-excess branch \(\delta\ge134944\) also remains open.  The exact
historical arithmetic is

```text
U_paid                 =   4,200,515,150,819,207
remaining budget       = 270,780,212,960,575,880
hypothetical cap-68    = 270,487,454,459,300,144
cap-68 margin          =     292,758,501,275,736
hypothetical cap-69    = 274,524,580,645,231,568
cap-69 deficit         =   3,744,367,684,655,688
```

The source-bound historical owner manifest and three load-bearing
equality-wall certificates are pinned by full commit and SHA-256 in this
packet.  They mark the cap-68 and primitive 69-point exclusions open.  Thus
a current-partition adapter would be necessary but not sufficient: the
remaining low-excess/general-excess geometry and exact class-to-slope
multiplicity must still close.

## 5. PR reconciliation

The pinned and refreshed upstream audit gives the following disjoint roles:

- **#1130** proves the degree-60 source-pencil compiler per supplied actual
  endpoint record and explicitly leaves the parameter-to-carrier bridge open.
- **#1132** reduces the transverse frontier to the two order-two types and
  compiles their interfaces; it leaves the actual-record selector and owner
  conversion open.
- **#1139** proves the conditional any-69 outer implication, records a
  different recurrence route cut, and supplies the tangent source-pin repair
  imported exactly here.
- **#1143** compiles the thirteen positive-coordinate routes as necessary
  raw graph conditions, not an exhaustive actual-slope atlas.
- **#1152** closes the raw `433-1b -> O0a` workboard but assigns no
  distinct-slope payment.
- **#1155** is a valid guard-transplant route cut with a surviving quadratic
  cover, not a K3 payment.
- **#1156** concerns denominator-root and coordinate-clone exception routing;
  its scalar-locator source-pin repair is not duplicated.
- **#1157** freezes the selector/reconstruction/projection gap and the
  thirteen-route fail-closed ledger.  This packet does not reopen raw cell-11
  algebra; it strengthens the first semantic cut and repairs the tangent pin.

No inspected PR supplies `(SB)`--`(FIB)`, an all-\(Z_{BC}\) complement fence,
or a K3 allocation in distinct-slope units.

## 6. Exact ledger consequence

After the source-pin repair, the honest active chronology is

```text
U_paid       = 981104      banked and source-replayed
U_Q          = null        open
U_BC         = null        open
U_new        = null        open
known sum    = 981104
joint reserve= 274980728110413983
row closed   = false
```

The K3-local outputs remain

```text
U_remaining       = null
U_positive        = null
U_sourcecover     = null
U_K3              = null
U_K3_allocation   = null
signed slack      = null
ledger movement   = 0
```

The reserve is not `U_K3_allocation`; raw zero is not slope zero; 32,099
partitions per supplied record are not a record census; 1,575 labels and
25,200 signed systems are not slopes; and the eight source-cover
row/passport combinations are not realized terminals.

## 7. What is and is not proved

### Proved

- the exact #1139 tangent source-pin repair and `U_paid=981104` replay;
- the absence of executable current source predicates/relations needed for
  the declared post-Q `m_in=2,r_out=4` slice;
- the precise typed theorem that would repair the gap;
- the deployed-carrier degree-two countermodel to direct-coordinate carrier
  preservation;
- the current/older partition mismatch;
- zero ledger movement and the four-atom MCA chronology.

### Not proved

- an actual received pair or received line for the countermodel;
- an MCA witness `(gamma,S,f_exp)`;
- membership in active Q, BC, or the declared K3 slice;
- an actual irreducible `(4,4)` component or K3 orientation;
- explaining-polynomial or received-data descent;
- failure of every conjugated carrier fold;
- failure of every possible same-record adapter;
- an all-`Z_BC` theorem, a projection-fiber bound, a K3 allocation, a K3
  payment, the KoalaBear row, or any official endpoint change.

The source-side fixture is therefore neither `UNPAID_PRIMITIVE` nor an
`ACTUAL_RECORD_COUNTEREXAMPLE`.  Missing actual component/source-star
hypotheses could force additional compatibility not visible in the printed
source-pencil identities.

## 8. Tool status

- Python reconstructs the 2,097,152-point carrier, all 1,071 internal
  involution pairs, the exact polynomial identities, source hashes, canonical
  JSON, ledger, and hostile mutations.
- Sage independently rebuilds the finite field, carrier, selected fibers,
  polynomials, gcds, and conjugacy disclosure.
- FLINT independently replays the selected exact polynomials, squarefreeness,
  composition, and integer identities.
- Wolfram's connected evaluator independently replayed the finite-field
  selected-fiber identities, degrees, gcds, direct carrier witness, and
  conjugacy identity.  The corrected local command is `wm.sh -file`; its
  final repeat was unavailable because the cloud account returned
  `Insufficient credits`, not because of an algebra or command-line failure.
- The tangent Lean package builds.  Its actual axiom census contains only
  standard `propext`/`Quot.sound`; the bound correspondence's older `[]`
  wording is recorded above as non-payment-invalidating documentation drift.
- Exa found relevant primary work on automorphisms of Reed--Solomon codes and
  finite-field PGL actions.  It reinforces that evaluation-set preservation
  is an additional hypothesis, but no literature statement is used as a
  load-bearing source for this project-specific same-record compiler.
- Singular/Macaulay2 are not used because no fixed residual ideal survives
  the earlier semantic gate.
- Lean remains deferred.

Layer cake, dyadic summability, moments, Markov, and Chebyshev are not used.

## 9. Maximal next theorem

The primary closure attack is to instantiate `(SB)`--`(FIB)` from actual
slope-level Q/BC predicates in the current architecture, including the
all-\(Z_{BC}\) complement fence.

There is also an independent alternative lane: complete the older
equality-wall packet in its five remaining low-excess degrees and
general-excess range, then prove a source-bound partition adapter into the
current four-atom chronology with its exact class-to-slope multiplicity.
That historical lane is conditional and parallel, not a theorem already
coupled to the active row.

The older 69-object contradiction route may ultimately avoid selecting every
individual slope, but it is not presently a shortcut to cap 68: its objects
are source-map equivalence classes per transversal projective residue line,
not slopes, and the per-direction image cap is 1,894,736.  Either route must
still print identical received-line reconstruction and exact distinct-slope
fibers before any raw K3 result is charged.

OPEN GAP
