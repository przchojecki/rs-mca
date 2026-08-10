---
workboard_item: K3
row: KoalaBear MCA at 2^-128
object: MCA
agreement: 1116048
B_star: 274980728111395087
direct_statement: An explicit deployed KoalaBear record has shifted-lattice minimum 67473 under both K=k and K=k+1.  This is the boundary numerical profile under the code-dimension shift and the first-interior numerical profile under the effective shift.  The cited sources do not prove that either numerical profile equals the frozen Q or BC slope predicate.  Thus SEM-QBC remains an open prerequisite before ActiveRec_2_4; no Q, BC, or U_new owner is assigned.
architecture: GRANDE_FINALE_V4_KB_MCA_TANGENT_SOURCE_ADAPTER_V1
partition_digest: 4fade91abc408264989babcff6f8f9bbd80bcec52545a5db15ac376bf17d88fc
quantifier: one exact actual record proving profile sensitivity; the missing semantic repair must be uniform over every received line
projection_and_unit: distinct affine slopes per received line
claimed_bound: none; all K3 and Q/BC/new ledger values remain null
status: AUDIT
impact: OPEN MISSING-ADAPTER GAP; ledger movement zero
falsifier: failure of the actual-record arithmetic or two-shift lattice minimum, or an overlooked theorem already in the pinned source bundle supplying the frozen Q/BC projection or K-adapter; a future theorem may repair the gap without contradicting this audit
replay: python3 -B experimental/scripts/verify_kb_mca_v4_k3_actual_record_source_dimension_route_cut_v1.py --check --tamper-selftest --dag-root /path/to/rs-mca-prize-dag && /usr/local/bin/sage experimental/scripts/verify_kb_mca_v4_k3_actual_record_source_dimension_route_cut_v1.sage && ~/math_code/.venv/bin/python experimental/scripts/verify_kb_mca_v4_k3_actual_record_source_dimension_route_cut_v1_flint.py
---

# KoalaBear K3 actual-record dimension-sensitivity audit

## 0. Verdict

This packet proves a narrow exact fact about an actual deployed received line:
the same full-degree bad slope has shifted-lattice minimum (67473) under both
printed shifts, but crosses from the boundary numerical profile for (K=k)
to the first-interior numerical profile for (K=k+1).  The record has an
actual support, a degree-((<k)) explaining polynomial, pair noncontainment,
an empty tangent image, and an exact lattice minimum.

This is an **audit**, not success condition A or B.  It neither refutes the
KoalaBear target inequality nor proves source-level non-definability.  In
particular, the bound sources do not identify either numerical profile with
the frozen Q or BC slope predicate, so no Q, BC, or (U_{\rm new}) owner is
assigned to the record.

The first missing theorem remains `SEM-QBC`, not another K3 endpoint elimination:
the source must define executable Q and BC predicates on actual witnesses and
prove their slope projections agree with the frozen first-match cells.  Only
then can same-record `Q=6,s=6,u=2` endpoint realization begin.

The ledger remains

```text
U_paid             = 981104
U_Q                = null
U_BC               = null
U_new              = null
U_remaining        = null
U_positive         = null
U_sourcecover      = null
U_K3               = null
U_K3_allocation    = null
signed_slack       = null
ledger movement    = 0
```

## 1. The exact source gap

The actual MCA definition fixes a code

\[
 C=\operatorname{RS}[\mathbb F,D,k],\qquad \deg h<k,
\]

and counts distinct slopes of actual triples \((\gamma,S,h)\).  This is
source-bound at
`experimental/Conjectures_and_Barriers_RS_MCA_v4_1.tex:104-122,418-433`.
The same source requires declared algebraic predicates on actual witnesses
and performs first match only after projection to slopes
(`:540-609`).

Two different \(K\)'s then occur in the published programme.

1. The finite Q/prefix calibration uses
   \(K_{\rm eff}=k+1=1048577\) and
   \(w_{\rm eff}=m-K_{\rm eff}=67471\).  See
   `experimental/grande_finale.tex:4660-4681,4956-4977`.
2. The received-word interpolation lattice says explicitly that \(K\)
   denotes the **code dimension**, defines
   \[
     \operatorname{wdeg}_K(W,N)
       =\max(\deg W,\deg N-(K-1)),
   \]
   and introduces numerical near-rational and balanced strata at
   \(d_1\le w=m-K\) versus \(d_1\ge w+1\). See
   `tex/cs25_cap_v13_2.tex:9482-9554`.  The same foundation source states
   explicitly that the census uses \(K=k\) on the deployed rows
   (`:7630-7631`). For the actual code this gives
   \(K_{\rm code}=k=1048576\) and \(w_{\rm code}=67472\).

The finite Q statements concern their declared prefix/quotient witness
families; they do not say that every arbitrary received word at the numerical
boundary belongs to the frozen Q cell. See
`experimental/grande_finale.tex:4997-5013`. The foundation source likewise
leaves the global priority map and coverage as future work
(`tex/cs25_cap_v13_2.tex:7823-7864`) and calls the per-line balanced reduction
intermediate (`:9992-9998`). Therefore there is no theorem transporting the
\(K=k+1\) prefix envelope to the degree-\((<k)\) received-word lattice, nor one
identifying either numerical profile below with the opaque Q and BC predicates
in the current row manifest.

## 2. An actual deployed record

Put

\[
 p=2130706433,\qquad n=2^{21},\qquad
 \zeta=1213133211\in\mathbb F_p.
\]

Exact modular arithmetic gives

\[
 \zeta^n=1,qquad \zeta^{n/2}=-1,
\]

so \(D=\langle\zeta\rangle\) has order exactly \(n\). Let

\[
 e=67473,qquad
 E=\{\zeta^i:0\le i<e\},qquad
 S=\{\zeta^i:e\le i<e+m\}.
\]

The intervals are disjoint and \(e+m=1183521<n\), so
\(|S|=m=1116048\). Let \(U=\mathbf 1_E:D\to\mathbb F_p\).

Work in the challenge field

\[
 \mathbb F=\mathbb F_p[\alpha]/(\alpha^6+\alpha+6).
\]

The displayed polynomial is irreducible over \(\mathbb F_p\), as replayed
independently by Sage.  Define the received line

\[
 v(x)=-\frac1{x-\alpha},\qquad
 u(x)=U(x)-\alpha v(x)=U(x)+\frac{\alpha}{x-\alpha}.
\]

Every \(x\in D\subset\mathbb F_p\) differs from \(\alpha\), so both words are
defined. At the full-degree affine slope \(\gamma=\alpha\),

\[
 u+\alpha v=U.
\]

On \(S\subseteq D\setminus E\), \(U=0\). Thus

\[
 (\alpha,S,0)
\]

is an agreement witness with \(\deg 0<k\).

### Lemma 2.1 (actual MCA-badness and tangent exclusion)

The pair \((u,v)\) is not simultaneously explained on \(S\), is column-far
at agreement \(m\), and therefore has empty canonical source-coordinate
tangent image. Hence \(\alpha\) is an actual non-tangent MCA-bad slope.

#### Proof

Suppose \(v\) agreed on any \(m\)-subset with a polynomial \(g\) of degree
less than \(k\). Then

\[
 (X-\alpha)g(X)+1
\]

would have at least \(m\) distinct roots but degree at most \(k<m\), a
contradiction. The same argument works even for degree less than \(k+1\):
the product has degree at most \(k+1<m\). Thus no size-\(m\) support explains
the direction word under either convention.  In particular the pair is not
simultaneously explained on \(S\), and no common explaining triple exists.
The source-bound tangent adapter defines the tangent image to be empty in the
column-far case. The displayed witness therefore makes \(\alpha\) MCA-bad
and not tangent-owned.  \(\square\)

This pole line is load-bearing.  The simpler base-slope control
\((\mathbf1_E,X^k)\) also produces an actual code-dimension witness, but
\(X^k\) becomes a codeword after changing to \(K=k+1\); it is retained only
as a mutation/regression control and is not used in the theorem.

## 3. Exact shifted-lattice minimum

For either shift, form the same word lattice

\[
 M_U=\{(W,N):W(x)U(x)=N(x)\text{ for all }x\in D\}.
\]

### Lemma 3.1 (two-shift minimum)

The minimal shifted degree is exactly

\[
 d_1^{(k)}(U)=d_1^{(k+1)}(U)=e=67473.
\]

#### Proof

The vector \((\Lambda_E,0)\) belongs to \(M_U\): on \(E\) its first
coordinate vanishes, and off \(E\) the word \(U\) vanishes. Its shifted
degree is \(e\) for both shifts, so each minimum is at most \(e\).

Assume a nonzero \((W,N)\in M_U\) has shifted degree at most \(e-1\).
Then \(\deg W\le e-1=67472\). On the \(n-e=2029679\) points of
\(D\setminus E\), the lattice identity gives \(N=0\). For the code-dimension
shift,

\[
 \deg N\le (k-1)+(e-1)=1116047<2029679.
\]

For the effective shift,

\[
 \deg N\le k+(e-1)=1116048<2029679.
\]

Thus \(N=0\) in either case. On each of the \(e\) points of \(E\), \(U=1\),
so the lattice identity now gives \(W=0\). But \(W\) has \(e\) distinct roots
and degree at most \(e-1\), hence \(W=0\), contradicting nonzeroness.
Therefore both minima equal \(e\). \(\square\)

The zero codeword alone supplies exactly

\[
 \binom{n-e}{m}=\binom{2029679}{1116048}
\]

size-\(m\) support witnesses for \(U\). The certificate binds this exact
integer by bit length \(2015083\), big-endian byte SHA-256
`4d11045a6ab54a207e0c6ed148104a40f426f2ab4e5ef5e65453f1eca4710678`,
and three independent modular residues.  This support count is not converted
to a slope payment.

## 4. Exact profile sensitivity and its scope

Use the received-word lattice with its printed code-dimension shift \(K=k\).
Then

\[
 w_C=m-k=67472,qquad d_1=w_C+1.
\]

This is the boundary **numerical profile**. It is not, from the cited
statements alone, a proof that the actual slope belongs to the frozen Q cell:
the available Q theorem is stated for its special prefix witness family, not
for every arbitrary word with this value of \(d_1\).

Under the finite prefix calibration \(K=k+1\),

\[
 w_E=m-(k+1)=67471,qquad d_1=w_E+2.
\]

This is the first-interior **numerical profile**. It is likewise not a proof
that the actual slope belongs to the frozen BC cell. That implication is the
missing code-dimension/effective-dimension and owner adapter. Failure of
these two unproved candidate tests also cannot establish membership in
\(U_{\rm new}\), because the frozen Q and BC predicates remain independent
inputs to the first-match partition.

The row-degree identities show exactly what changed. Under the code-dimension
shift,

\[
 (d_1,d_2)=(67473,981104),\qquad
 m'=k-1+d_1=m,\qquad \deg B\le\omega-d_2=0.
\]

Under the effective shift,

\[
 (d_1,d_2)=(67473,981103),\qquad
 m'=(k+1)-1+d_1=m+1,\qquad \deg B\le1.
\]

Thus the \(K\mapsto K+1\) substitution creates exactly one additional
interior coefficient and changes the numerical profile label. This does not
preclude a future semantics-preserving owner adapter; it shows that such an
adapter requires proof rather than silent substitution.

The scope is exact. Put \(L_C=\prod_{x\in D\setminus E}(X-x)\) and let
\(R\) be the remainder of \(L_C\) modulo \(\Lambda_E\). Then

\[
 g_1=(\Lambda_E,0),\qquad g_2=(R,L_C)
\]

is a weak-Popov basis of \(M_U\), with determinant
\(\Lambda_E L_C=\Lambda_D\) and the row profiles printed above. The
basis claim is direct. For any \((W,N)\in M_U\), the identity off \(E\)
forces \(L_C\mid N\), say \(N=B L_C\). On \(E\), it then forces
\(W\equiv B L_C\equiv B R\pmod{\Lambda_E}\), so
\((W,N)=A g_1+B g_2\). Conversely both displayed rows satisfy the lattice
identity. Their shifted leading positions are distinct under both shifts,
because \(\deg R<e\) and the shifted \(L_C\)-degree is \(981104\), respectively
\(981103\), both larger than \(e\).

The zero-codeword census witnesses used here have coefficient \(B=0\): they
lie on the pure \(A g_1\) ray. Consequently this record proves profile
sensitivity *before* endpoint realization; it does not prove survival of a
later primitive/ray gate, \(r_{\rm out}=4\), or membership in any of the
thirteen K3 endpoint routes.

### Theorem 4.1 (dimension sensitivity and missing adapter)

For the displayed actual record,

\[
d_1^{(k)}=d_1^{(k+1)}=67473,
\]

but this value is the boundary numerical profile for \(K=k\) and the
first-interior numerical profile for \(K=k+1\). The cited sources prove no
equivalence from either numerical profile to the frozen Q or BC slope cell.
An explicit dimension/owner adapter is therefore required before this record
can be used in `ActiveRec_2_4`. No frozen first-match owner follows.

#### Proof

Lemma 3.1 gives the common minimum. Substitution into the two definitions of
\(w=m-K\) gives \(67473=67472+1\) and \(67473=67471+2\). The row-degree
identities above give the one-coefficient change. The Q theorem does not
cover arbitrary words of the displayed form, and the balanced source supplies
no proved effective-dimension projection to the frozen BC cell. Hence neither
numerical calculation establishes an owner. \(\square\)

## 5. Audit of the post-#1158 public DAG

At refreshed public-DAG commit
`3edb8b31b6735a0a2302a578a21dc6e50bd64046`, the node
`rate_half_kb_active_balanced_core_witness_compiler` is labelled `PROVED`.
Its exact files are pinned in the certificate.

The finite-selector lemma inside that node is correct after a valid relation
is supplied: a finite nonempty certificate fiber has a least element, and a
certificate storing its slope projects back to that slope. The node does not,
however, prove that its relation is executable or equivalent to the frozen BC
predicate, for four independent reasons.

1. The proof defines `bcCertified(line,z)` to mean existence of its new
   `ValidBC` relation.  Both containments are then substitution, not an
   equivalence with an independently defined frozen predicate.
2. The schema records required fields and guards as strings.  It contains no
   typed received pair, no actual polynomial equations, no degree-\((<k)\)
   explanation check, no pair-noncontainment check, and no executable Q
   relation.
3. Its verifier checks constants, uniqueness of strings, and proof tokens.
   It does not parse or verify one actual certificate.
4. It substitutes \(K=k+1\) into a lattice theorem whose source says \(K\)
   denotes the code dimension. The actual record above shows that this changes
   the numerical profile, so a semantics-preserving adapter needs a proof.

The public DAG's `rate_half_kb_active_bc_order32_adapter` inherits this
unproved semantic premise. Its `PROVED` label therefore cannot discharge
`SEM-QBC`. The upstream partial order-32 theorem itself remains available
directly for any 32 actual bad slopes; this route cut does not question that
theorem.  The public DAG's actual balanced-core component bridge correctly
remains conditional on same-record endpoint realization.

## 6. Weakest repair: `SEM-QBC`

Before `Rec_2_4`, prove one witness-level theorem with explicit predicates

\[
 P_Q(r,w),\qquad P_{BC}(r,w),\qquad w\in\mathcal W_r(m),
\]

such that, for every received line,

\[
 Q_{\rm frozen}(r)=\pi_\gamma\{w:P_Q(r,w)\},
\]

and

\[
 Z_{BC}(r)=
 \pi_\gamma\{w:P_{BC}(r,w)\}
 \setminus\left(Z_{\rm paid}(r)\cup
                 \pi_\gamma\{w:P_Q(r,w)\}\right).
\]

The theorem must include all of the following.

1. Soundness: every certificate reconstructs an actual MCA witness on the
   identical pair, slope, original support, and degree-\((<k)\) explanation.
2. Coverage: every slope in the independently defined frozen cell has a
   certificate.
3. Slope-global Q exclusion: no Q witness for the same slope exists.  A
   Boolean tag on one chosen BC witness is insufficient.
4. A proof choosing \(K=k\), or an exact adapter from the \(K=k+1\) prefix
   envelope to the degree-\((<k)\) lattice, including the boundary.
5. Preservation of a source support of size at least \(m\); if an exact-\(m\)
   subsupport is selected, prove that every downstream guard still holds.
6. A complement fence for every BC slope not routed to the eventual
   ((2,4,2)) endpoint type.

After `SEM-QBC`, define a complete endpoint relation

\[
 \operatorname{Rec}_{2,4}(r,\gamma,c,e)
 =\operatorname{ValidBC}(r,\gamma,c)
  \wedge\operatorname{End}_{2,4}(r,\gamma,c,e),
\]

where `End` contains the actual `Q=6,s=6,u=2` record, component, source maps,
field data, route, passport, and every guard.  A canonical selector must be
taken on the complete realizable tuple, not on a witness before realization,
unless all selected witnesses are proved realizable.  Exact route preimage
multiplicities, not raw label counts, are still required.

## 7. Upstream and dependency reconciliation

At the final refresh, upstream `przchojecki/rs-mca` `main` was
`93fba1be3f3299b0ba4708d88715377bbb656e45`. PRs #1157 and #1158 remained
open and were neither ancestors of `main` nor present there by artifact
content. No open PR newer than #1158 duplicated this actual-record
dimension-sensitivity audit.

- #1130 and #1132 classify supplied endpoint records and explicitly disclaim
  the received-line/slope bridge.
- #1139 supplies the tangent source pin used here.
- #1143 and #1152 supply raw K3 workboards, not actual-slope projection.
- #1155 remains a valid guard-transplant route cut.
- #1156 concerns a different exception/scalar-locator route.
- #1157 supplies the thirteen-route workboard and first bridge cut.
- #1158 supplies the repaired tangent pin and direct-coordinate carrier cut.

No raw cell-11 elimination is reopened.  The two raw-zero K3 routes and all
eleven surviving routes retain their prior scope.  Since the source owner is
not established before endpoint realization, no K3 integer can be moved.

The public proof board has advanced beyond its older website export.  The
live DAG is useful because it exposes the exact attempted semantic repair;
the public leaderboard website remains a status display, not proof authority.

## 8. Independent computation and literature controls

The Python verifier checks the actual row, field and subgroup arithmetic,
root-count proof, exact binomial fingerprint, both numerical profiles,
source hashes, null ledger, and hostile mutations in normal and optimized
modes.  Sage independently checks the extension modulus, deployed subgroup,
the exact pole-line identities, and a complete toy-field analogue.  FLINT
independently checks the integer and polynomial controls.  Wolfram replays
the exact thresholds, root-degree inequalities, field budget, and profile
arithmetic. No owner assertion is part of these computation checks.

An Exa search found primary interpolation-module literature using the
\((1,k-1)\)-weighted degree for an `RS[n,k]` code, consistent with the
foundation source.  This is corroboration only; the repository's pinned
source statement and the direct record proof are load-bearing.  A targeted
TheoremSearch query returned no usable project-specific theorem and is not
used.

## 9. Proof tier and nonclaims

**Proved here:** one actual deployed non-tangent MCA-bad record; its exact
minimum under both shifts; the corresponding boundary and first-interior
numerical profiles; the one-coefficient row-profile change; and the precise
open `SEM-QBC` repair interface.

**Imported:** the actual MCA definition, tangent column-far rule, two printed
\(K\)-conventions, first-match set algebra, and the #1157/#1158 raw and
semantic route cuts.

**Not proved:** the correct final Q/BC predicate, any `Rec_2_4` endpoint,
same-record Q6 realization, thirteen-route payment, all-BC complement,
`U_Q`, `U_BC`, `U_new`, K3 allocation, KoalaBear closure, or universal
smooth-domain result. In particular, the actual record is a pure
\\(A g_1\\) census ray and is not claimed to be a primitive
\\((m_{\\rm in},r_{\\rm out})=(2,4)\\) survivor.

# AUDIT: EXACT DIMENSION SENSITIVITY; SEM-QBC AND ROW OPEN
