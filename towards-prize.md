# Towards the Proximity Prize: v12 Audit and Execution Plan

Status: working plan / source-of-truth roadmap

Date: 2026-07-01

This document is the current execution plan for turning the RS-MCA repository
into a serious Proximity Prize submission package.  It replaces the older
strict264/frontier-search roadmap.  The center of gravity is now Paper D v12:
the two-sided cap theorem, safe-side pincer, map/rational smooth extensions,
explicit witness machinery, certificate grammar, and the corresponding
proof-packet schema.

The goal is not to collect more impressive-looking lower bounds.  The goal is
to determine thresholds.  For a row \(C\), that means proving adjacent
safe/unsafe agreement levels for the exact MCA/list object used by the prize.

## 1. The Prize-Shaped Object

For
\[
        C=\operatorname{RS}[\mathbb F,D,k],
        \qquad n=|D|,\qquad \rho=k/n,
\]
the Proximity Prize regime uses
\[
        \rho\in\{1/2,1/4,1/8,1/16\},
        \qquad k\le 2^{40},
        \qquad |\mathbb F|<2^{256},
        \qquad \varepsilon^*=2^{-128}.
\]

For support-wise MCA, write
\[
        B_C(a)
        =
        \#\{\text{bad line parameters with agreement at least }a\},
\]
with the denominator \(q_{\rm line}\) explicitly stated.  Define
\[
        B_*(q_{\rm line})=\left\lfloor q_{\rm line}/2^{128}\right\rfloor .
\]

A row is threshold-pinned at adjacent agreement levels \(a_0,a_0+1\) if
\[
        B_C(a_0)>B_*(q_{\rm line})
        \quad\text{and}\quad
        B_C(a_0+1)\le B_*(q_{\rm line}).
\]
Everything else is secondary.  A lower bound without the adjacent safe-side
upper bound is useful evidence, but it is not a prize-shaped solution.

Endpoint conventions must be printed every time:

```text
agreement at least a
closed integer radius r = n-a
closed real radius via floor(delta n)
finite affine slope denominator |F|
projective slope denominator |P^1(F)| = |F|+1
challenge/protocol denominator q_chal, if different
```

## 2. Current State

### 2.1 Settled

The no-slack smooth-domain MCA/RCA optimism is dead.  Paper A gives explicit
obstructions.  Positive statements must include reserve and explicit quotient
floors.

Paper D v12 is the current Paper D package and the main object to audit.  It
preserves the universal-cap package, first-grid cap, aperiodic Hankel chart
atlas, and v10 quotient/extension ledgers, then adds the safe-side pincer and
deployed-row certificate layer:

```text
deep-regime MCA safe theorem for all linear codes;
MCA-from-CA reduction up to half the minimum distance;
self-contained half-Johnson CA bound and optional BCIKS half-distance import;
map/rational smooth caps, circle/genus-one transports, and explicit witnesses;
certificate grammar v2 with printed deployed-row integer certificates.
```

The immediate work is audit, not another lower-bound search: check the direct
conversion and radius conventions, the optional BCIKS import, the exact integer
certificates, and the scope of the circle/genus-one model transfers.

The PR 161--169 integration adds two important roadmap corrections:

```text
L1 targets codeword-image fibers ImgFib_U, not raw support fibers Fib_U;
the F_17^32 regular non-tangent window now has compact row, window, and
generic-minor artifacts, but still no root-table safe-side proof.
```

The image-fiber repair is now reflected in Papers B and C.  Raw support fibers
can be exponentially inflated by many supports explaining the same codeword;
the exact list object is the image fiber.

For the finite row
\[
        C=\operatorname{RS}[\mathbb F_{17^{32}},H,256],
        \qquad |H|=512,
\]
the pure finite-slope support-wise MCA threshold is pinned in the
high-agreement tangent range:
\[
        LD_{\rm sw}(C,506)=7,
        \qquad
        LD_{\rm sw}(C,507)=6,
\]
and
\[
        6\cdot2^{128}<17^{32}<7\cdot2^{128}.
\]
So the closed integer-grid transition is:

```text
safe:        radius <= 5, agreement >= 507
first unsafe radius: 6, agreement 506
real closed safe interval: [0, 6/512)
supremum: 6/512 = 3/256, not attained
```

This is a good partial result.  It is not the full prize.

### 2.2 Not Settled

The full prize still needs safe-side upper bounds in the lower-agreement,
near-capacity region where tangent exactness is not enough and quotient floors
are large.

The central unresolved object is:
\[
        B_C(a)
        \le
        B_{\rm tan}(a)
        +
        B_{\rm quot}(a)
        +
        B_{\rm ap}(a)
        +
        B_{\rm ext}(a),
\]
with each term explicitly defined, deduplicated, and divided by the correct
field denominator.

The v12 atlas is designed to attack \(B_{\rm ap}(a)\), the aperiodic
Hankel/residue-line term after tangent and quotient branches have been removed.

## 3. Strategic Decision

The best path now is:

1. keep the finite \(F_{17^{32}}\) threshold as the clean partial-submission
   result;
2. stop treating strict264/strict352 as the main frontier;
3. use strict264/strict352 only as mechanism tests and quotient-floor examples;
4. make Hankel proof packets the standard format for every new safe-side claim;
5. prove or refute the aperiodic local limit through the v12 chart atlas.

In practice, every useful PR should now answer one of these questions:

```text
Does it produce a v12 Hankel proof packet?
Does it reduce a residual v12 chart to quotient/tangent/extension structure?
Does it prove a reusable theorem needed by such packets?
Does it audit the exact prize object, denominator, or endpoint convention?
```

If the answer is no, it is probably not on the shortest path.

### 3.1 Post-v12 status: the band is underdetermined

The r2 roadmap audit in
`experimental/notes/roadmaps/proximity_prize_execution_roadmap_post_v12_r2.md`
adds an important correction.  The regular overdetermined Hankel branch exists
only when
\[
        t\ge j+1
        \quad\Longleftrightarrow\quad
        \delta\lesssim \frac{1-\rho}{2}.
\]
For every official prize rate, the Johnson-to-capacity band lies above this
range:
\[
        1-\sqrt{\rho}
        -
        \frac{1-\rho}{2}
        =
        \frac{(1-\sqrt{\rho})^2}{2}
        >
        0.
\]
Therefore the regular M3 window is a controlled proving ground for
stratification, root accounting, and packet format.  It is not, by itself, the
band-facing theorem needed for a full prize solution.

The critical safe-side program is now:

```text
regular window      -> develop and test v12 packet mechanics;
underdetermined M5  -> attack the actual prize band;
M4 assembly         -> subtract tangent, quotient, and extension ledgers;
M6 theorem          -> promote residual classification into a row theorem or
                       uniform aperiodic bound.
```

For the pinned `F_17^32`, `n=512`, `k=256` row, the first underdetermined
boundary is
\[
        A=384,\qquad t=j=128,
\]
where the Hankel matrix has shape \(128\times129\).  Kernel nonemptiness is
then vacuous for every slope, so the first meaningful filter must come from
Cramer-kernel locator validity, divisibility by \(X^{512}-1\), pivot charts, or
a labelled residual obstruction.

## 4. The v12 Hankel Proof Packet

Paper D v12 gives the contributor-facing atlas.  For a row and exact agreement
\[
        A,\qquad j=n-A,\qquad t=A-k,
\]
a proof packet must do the following.

### 4.1 Remove Paid Ledgers

Before calling anything aperiodic, remove the branches already paid by:

```text
tangent/common-code-line ledger
quotient-support ledger
quotient-image ledger
known subfield/confinement ledger
known projective or curve endpoint ledger
```

These removals must be referenced in the JSON packet.  The schema field is
`removed_ledgers`.

### 4.2 Regular Overdetermined Bucket

If
\[
        t\ge j+1
        \quad\Longleftrightarrow\quad
        2A\ge n+k+1,
\]
form
\[
        M_A(Z)=H_{t,j}(u)+Z H_{t,j}(v).
\]

A nonzero \((j+1)\times(j+1)\) minor
\[
        \Delta_A(Z)
\]
is a root-containment certificate:
\[
        \text{bad finite slopes at exact agreement }A
        \subseteq
        \{\Delta_A=0\},
\]
so the contribution is at most
\[
        \deg \Delta_A \le j+1=n-A+1.
\]

This is still the first thing to try.  Version 10 strengthens it: in the
regular overdetermined branch, use the canonical gcd of all nonzero maximal
minors, not one selected minor.  Across a closed ball, take the squarefree lcm
over exact agreement levels, then remove paid tangent/quotient roots by gcd.

### 4.3 Affine Pivot Charts

If the regular bucket is singular or too weak, build locator charts \(X\) and
split by finite affine pivots
\[
        B_h(\ell)\ne0.
\]

On such a chart the slope is
\[
        Z=-A_h(\ell)/B_h(\ell),
\]
and the chart ideal is generated by the collinearity equations
\[
        A_mB_h-A_hB_m=0
\]
plus the graph equation
\[
        ZB_h+A_h=0,
\]
saturated by the chart denominator \(\Delta_X B_h\).

A nonzero eliminant
\[
        Q_{X,h}(Z)
        \in
        \widehat J^{\rm aff}_{X,h}\cap F[Z]
\]
bounds the chart contribution by \(\deg Q_{X,h}\).

### 4.4 Projective Infinity

For projective slopes \([Z_0:Z_1]\), the finite patch is the affine atlas.
The extra point is
\[
        [0:1],
\]
controlled by the chart
\[
        B=0,\qquad A\ne0.
\]

Each projective packet must certify the infinity chart as empty or nonempty.
If nonempty, it contributes at most one projective parameter.

### 4.5 Curve Pivots

For a finite-parameter degree-\(d\) power curve
\[
        W_\Gamma=f_0+\Gamma f_1+\cdots+\Gamma^d f_d,
\]
split by coefficient pivots
\[
        (V_i)_h\ne0.
\]

A nonzero eliminant
\[
        Q_{X,i,h}(\Gamma)
\]
in the saturated curve incidence ideal bounds the bad curve parameters in that
chart by \(\deg Q_{X,i,h}\).

### 4.6 Allowed End States

Every exact-agreement bucket and every chart must end as exactly one of:

```text
eliminant
empty
dimension_degree
residual_obstruction
```

Residual obstructions must be labelled as:

```text
quotient
tangent
extension
candidate_new_obstruction
unknown
```

Do not hide a singular bucket under "aperiodic evidence."  If the chart is not
closed, name the obstruction.

### 4.7 Machine Format

Use:

```text
scripts/aperiodic_eliminant_schema.json
```

Required packet fields:

```text
schema_version = "aperiodic-hankel-eliminant-v1"
row: n, k, field, domain_hash
agreement_threshold
sampler
removed_ledgers
exact_agreements
regular_minor records
chart records
pivot records
root_union_table_ref
declared_aperiodic_numerator
```

The schema is not a proof by itself.  It is the index of the proof packet.  The
packet must also include equation files, eliminant files, root tables, and
verification transcripts.

## 5. Immediate Milestones

These are ordered.  Do not jump to later milestones before the earlier ones
exist in a reviewable form.

### M0. Definition Freeze

Produce a short definition note that fixes the exact object for the prize-facing
MCA row:

```text
support-wise MCA predicate
same-support noncontainment
finite affine slope sampler versus projective sampler
endpoint convention
q_gen, q_line, q_chal
closed-grid versus supremum threshold
```

Exit criterion:

```text
one file under experimental/notes/audits/
one table saying which repo theorem uses which convention
no "officially solved" language
```

### M1. v12 Schema Verifier

Write a checker for `scripts/aperiodic_eliminant_schema.json`.

It should verify:

```text
JSON schema validity
j = n-A
t = A-k
removed ledgers are referenced
residual labels are present when required
degree/root counts are arithmetically consistent
declared numerator matches the root-union table
```

This checker does not need to verify Groebner/ideal membership at first.  It
should make bad packets impossible to pass off as complete.

Exit criterion:

```text
scripts/check_aperiodic_eliminant_packet.py
one passing toy packet
one intentionally failing packet
documented expected output
```

### M2. Smoke-Test v12 on a Settled Row

Create a proof packet for the already-settled high-agreement row
\[
        C=\operatorname{RS}[\mathbb F_{17^{32}},H,256],
        \qquad A=506,507.
\]

This is not mathematically new.  It tests the packet format on a row whose
answer is known:

```text
A=506: numerator 7, unsafe
A=507: numerator 6, safe
```

Exit criterion:

```text
experimental/data/certificates/hankel-smoke-f17-506-507/
JSON packet conforming to v1 schema
root/numerator table
auditor note explaining why this is a format test, not a new theorem
```

Status: completed by the smoke packet

```text
experimental/data/certificates/hankel-smoke-f17-506-507/
```

The packet records the known finite-slope support-wise MCA transition:

```text
A=506: numerator 7, unsafe;
A=507: numerator 6, safe.
```

It is intentionally an "empty after tangent removal" v12 packet: the tangent
common-code-line ledger pays the entire numerator in this high-agreement
range, so the declared aperiodic numerator is `0`.  This validates packet
format and bookkeeping, not a new aperiodic eliminant theorem.

### M3. Regular Non-Tangent Window

For the \(F_{17^{32}}\), \(n=512,k=256\) row, the regular overdetermined minor
condition starts at
\[
        A\ge385,
\]
while the tangent exact theorem starts at
\[
        A\ge427.
\]

The window
\[
        385\le A\le426
\]
is the first useful v12 stress test: regular Hankel minors may give upper bounds
where tangent exactness does not.

Exit criterion:

```text
for each A in a selected subrange:
  nonzero minor or singular declaration
  degree bound
  root-count table
  comparison against tangent/quotient ledgers
```

If the minors vanish or give weak bounds, that is useful.  It identifies the
first real singular bucket.

Status: upgraded by Paper D v12.

```text
scripts/cs25_v12_regular_hankel_eliminant.py
```

The v12 regular branch no longer asks contributors to choose one minor.  It
takes the gcd of all nonzero maximal minors at each exact agreement, then an
lcm over exact agreements for the closed-ball packet.  This gives a canonical
root-count ledger for every nonsingular regular bucket.  The next M3 task is to
run this checker on selected agreements in `385 <= A <= 426` for the
`F_17^32` row and classify each result as regular-closed or singular.

The PR 161 selected integration supplies the compact starting artifacts:

```text
experimental/data/certificates/hankel-f17-32-row-descriptor/
experimental/data/certificates/hankel-regular-window-f17-385-426/
experimental/data/certificates/hankel-f17-32-generic-regular-minor/
experimental/scripts/extract_regular_hankel_minors.py
experimental/scripts/verify_f17_32_m3_generic_regular_minor.py
```

The generic-minor note proves that every maximal row-set regular minor in the
window is generically nonzero of degree `j+1`.  This rules out a structural
collapse of the regular method, but it does not bound a worst-case MCA line:
the degree-only sum is still `4515`, while the finite-slope budget is only `6`.
The next packet must compute actual root tables or identify singular buckets.

### M4. Quotient and Tangent Subtraction

Integrate the v12 packets with the existing quotient-image and tangent ledgers.
For each exact agreement \(A\), output:

```text
B_tan(A)
B_quot_support(A)
B_quot_image(A)
B_ap_regular(A)
B_ap_pivot(A)
B_ext(A)
deduped total upper bound
known lower bound
gap to B_*(q_line)
```

Exit criterion:

```text
one table for the F_17^32 row
one table for a Prime192 scanner row
no double-counting between removed ledgers and aperiodic roots
```

Status: partially upgraded by Paper D v12.

```text
scripts/cs25_v12_quotient_support_ledger.py
scripts/cs25_v12_quotient_image_ledger_prime.py
scripts/cs25_v12_dual_cosupport_ledger.py
scripts/cs25_v12_extension_pole_floor.py
```

The quotient part now has three separate ledgers: a support-union coefficient
ledger that removes cross-divisor support overlap, a gcd/lcm image ledger that
coalesces duplicate parameters inside declared quotient branches, and a dual
co-support form for near-capacity rows.  The extension part now has a lower-side
simple-pole source over `F \ B`.  The next M4 task is to combine these ledgers
with the M3 regular-Hankel root set and explicitly subtract paid roots.

### M5. Singular Bucket Program

For every singular bucket produced by M3/M4, build pivot charts.

Attack order:

1. affine pivots \(B_h\ne0\);
2. projective infinity \(B=0,A\ne0\);
3. curve coefficient pivots \((V_i)_h\ne0\);
4. dimension-degree fallback only as a diagnostic;
5. residual classification.

Exit criterion:

```text
each singular chart is eliminant / empty / dimension_degree / residual_obstruction
every residual has label quotient/tangent/extension/candidate_new_obstruction/unknown
candidate_new_obstruction has a minimal reproducible example
```

Status after v12: narrowed.

The nonsingular regular overdetermined branch is now handled by the canonical
rank-drop gcd/lcm ledger.  M5 should focus on:

```text
underdetermined exact agreements;
rank-drop singular exact agreements;
affine pivot eliminants;
projective infinity charts;
curve coefficient-pivot charts.
```

Status after the post-v12 PR sweep: the first underdetermined boundary packet
has been added at

```text
experimental/notes/m5/m5_underdetermined_a384_pivot_packet.md
```

It is deliberately `ACTIVE / EXPERIMENTAL`: it identifies the `A=384`
deficiency-one bucket and the Cramer/divisibility route, but it does not claim
a threshold bound.  This is now the first concrete M5 rung to refine.

### M6. M1 Theorem Candidate

Once enough rows/charts are understood, state the theorem we actually want:

\[
        B_{\rm ap}(a)\le n^B
\]
after quotient, tangent, and extension-confined branches are removed.

There are two acceptable forms:

```text
finite-row theorem:
  proves a specific row's threshold

uniform theorem:
  proves an explicit n^B bound for all rows satisfying printed hypotheses
```

The finite-row theorem is enough for a partial result.  The uniform theorem is
the route to the full prize.

## 6. Parallel Mathematical Lanes

The v12 Hankel lane is central, but it cannot finish the whole prize alone.
These lanes feed into or consume the Hankel packets.

### L1. Generated-Field Locator Local Limit

Needed for list decoding and for converting arbitrary received-word locator
fibers into usable ledgers.

Target:
\[
        \#\{\text{aperiodic locator image fibers}\}\le n^B
\]
above the corrected reserve, with quotient-periodic fibers explicitly budgeted.

Use `ImgFib_U(a)` for the list object.  Do not state the positive conjecture
for raw `Fib_U(a)`: low-degree words can have exponentially many explaining
supports for one codeword.  The raw fiber remains useful only as a coarse upper
bound or when multiplicity is explicitly budgeted.

First deliverables:

```text
monomial-prefix proof packets
quotient-removed toy enumerations
arbitrary-word Hankel/catalecticant reductions
bad-prime or finite-collision classification
full-petal sunflower branch bounds
```

Current new inputs:

```text
monomial dyadic descent replay packet for the F_17^32 row;
full-petal growing-defect witnesses showing that branch is nonempty.
```

Do not use \(q_{\rm line}\) to pay a \(q_{\rm gen}\) entropy bill.

### M1. Aperiodic Residue-Line Packing

This is the main MCA theorem lane.  It should now be written in v12 language:

```text
tangent and quotient branches removed
regular minors tested
affine/projective/curve pivot charts built
singular residual buckets classified
deduped root count compared to B_*(q_line)
```

The first useful theorem is not "MCA is small."  It is:

```text
Every non-small v12 residual bucket is quotient, tangent, extension-confined,
or a named new obstruction.
```

Current new inputs:

```text
full-overlap low-tail completion is proved;
projection-to-Graver remains a real wall;
BETA_2 is localized to a global monodromy/conductor input, not closed by finite
local data.
```

### F1. Extension-Line Lift or Counterexample

Needed because extension-valued lines may not be explained by base-field
witnesses.

Target:

```text
Either prove base/generated-field MCA bounds lift to F-valued lines,
or produce a genuinely F-valued obstruction with its own ledger.
```

Paper D v12 supplies the lower-side mechanism:

```text
large list + pole alpha in F \ B
=> genuinely F-valued simple-pole witness line
=> numerator ceil(L(|F|-|B|)/(|F|-|B|+kL)).
```

So F1 is no longer asking whether extension-valued witnesses exist below the
reserve.  The remaining question is safe-side classification: prove these
witnesses are covered by the extension/aperiodic ledger in the corrected
reserve, or print explicit bucket tables when they are counterexamples.

The new Lean F1 extension ledger formalizes a sigma-1 algebraic core and typed
bridge target.  Treat it as formalization support, not as the full extension
MCA lift theorem.

Every F1 result must say:

```text
B, F
q_gen, q_line, q_chal
whether the line is B-valued, F-valued, or subfield-confined
whether the bad slopes live in a proper subfield
```

### L2. Interleaved-List Constants

Needed for the list side of the prize and for protocol ledgers.

Use the codegree reduction, but do not oversell it.  It reduces interleaved
lists to base-list fibers at agreements \(a\) and \(2a-k\); it does not prove
the base L1 input.

Target:

```text
base aperiodic list bound at a
higher-agreement decay at 2a-k
quotient tails kept explicit
interleaved numerator divided by the correct challenge field
```

### M2. Line-Decoding Formulation

Needed to state the corrected MCA theorem in the language many protocols use.

Target:

```text
exact equivalence or one-way implication between support-wise MCA bad slopes
and line-decoding ambiguity, with agreement/radius endpoints explicit
```

M2 should consume the M1/Hankel packets and output line-decoding threshold
statements without changing denominators.

### X1. List-CA-MCA Bridges

Needed only when a proof crosses objects.  Every bridge must state the loss:

```text
radius loss
field-size loss
square-root or no-square-root loss
support-wise versus ordinary support convention
finite/projective/curve sampler
```

No bridge may be used silently.

## 7. Full-Prize Assembly Theorem

The final theorem should not be vague.  It should have this form.

Input:

```text
field tower B <= F
smooth domain D
n, k, rho
q_gen, q_line, q_chal
sampler type
target epsilon = 2^-128
quotient profile
certificate packets for relevant exact agreements
```

Output:

```text
safe agreement a_safe
unsafe agreement a_unsafe = a_safe - 1
delta convention
B_tan, B_quot, B_ap, B_ext, B_list ledgers
proof status for each ledger
final comparison against B_*(q_line) or protocol denominator
```

The final comparison should look like:

\[
        B_{\rm total}(a_{\rm safe})
        \le
        \left\lfloor q_{\rm line}/2^{128}\right\rfloor
\]
and
\[
        B_{\rm lower}(a_{\rm unsafe})
        >
        \left\lfloor q_{\rm line}/2^{128}\right\rfloor.
\]

For protocol/list statements replace \(q_{\rm line}\) by the exact denominator
used by that statement and print the replacement.

## 8. What To Work On Next

The next useful PRs, in order:

1. **Schema checker.**
   Validate v12 proof packets before any new math is claimed.

2. **Hankel smoke packet for \(F_{17^{32}}\), \(A=506,507\).**
   Exercise the format on a settled row.

3. **Regular-minor extractor.**
   Given row data and exact agreement \(A\), compute candidate nonzero minors
   and root-count bounds.

4. **Regular-window audit \(385\le A\le426\).**
   Determine where the regular bucket succeeds and where singular buckets begin.

5. **Quotient/tangent subtraction table.**
   Produce one deduped table combining existing ledgers with v12 root counts.

6. **First singular pivot packet.**
   Pick one singular bucket and close it by affine pivots or certify the
   residual obstruction.

7. **F1 denominator audit for any extension-valued packet.**
   Prevent base-field witnesses from being overcounted under extension sampling.

8. **L1 base-list proof packet.**
   Prove a locator local-limit statement that the interleaved/list side can
   reuse.

9. **M2 line-decoding statement.**
   Convert the support-wise MCA theorem into line-decoding language without
   changing the object.

10. **Submission note.**
    Package the finite-row \(506/507\) threshold as a partial, human-reviewed
    result, with clear non-claims.

## 9. Non-Claims

Do not claim any of the following until the corresponding proof packet exists:

```text
full Proximity Prize solved
all smooth RS rows safe or unsafe at a stated radius
ordinary list decoding failure from an MCA row
protocol soundness break
extension-field lift without F1 proof
interleaved-list theorem from base-list theorem without L2 constants
aperiodic local limit from quotient/tangent examples
official acceptance by prize judges
```

## 10. Success Criteria

The project is moving toward the prize if it produces:

```text
v12 Hankel proof packets with checked eliminants
named and minimized singular residual buckets
explicit quotient/tangent/aperiodic/extension ledger tables
threshold-pinned rows, not just lower bounds
definition-audited sampler and endpoint statements
human-reviewable finite proof notes
formalized or independently replayed arithmetic gates
```

The shortest current path is:

```text
finite threshold package for F_17^32
  +
v12 Hankel proof-packet pipeline
  +
M1 aperiodic residual classification
  +
L1/F1/L2/M2 assembly
```

That is the route from the current repository to a credible full Proximity
Prize solution.
