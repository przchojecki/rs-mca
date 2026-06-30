# Towards the Full Proximity Prize

**Purpose.** This document is a work plan for collaborators and agents working on the RS-MCA / slack-threshold program. It is written as an execution document, not as a polished paper. The goal is to move from the current finite obstruction frontier toward a full Proximity Prize solution.

**Core principle.** Smooth no-slack RCA/MCA is false. Do not try to resurrect it. Work with slack, track the agreement staircase, separate quotient-periodic floors from aperiodic mass, and aim to determine exact or near-exact thresholds.

---

## 0. Required sources

Agents should read these before making claims or opening implementation work.

1. **Proximity Prize statement**
   <https://proximityprize.org/>

2. **Open Problems in List Decoding and Correlated Agreement**
   Reconstructed local TeX: [`open-proximity.tex`](open-proximity.tex)
   Local PDF mirror: [`open-proximity.pdf`](open-proximity.pdf)

3. **RS-MCA frontier board**
   <https://www.rsmca.xyz/>

4. **Paper A: no-slack obstruction / smooth RCA disproof**
   <https://github.com/przchojecki/rs-mca/raw/refs/heads/main/tex/RS_disproof_v3.tex>

5. **Paper B: slack MCA program / quotient floors / corrected reserve**
   <https://github.com/przchojecki/rs-mca/raw/refs/heads/main/tex/slackMCA_v4.tex>

6. **Cycle120 ABF counterexample candidate note**
   <https://github.com/przchojecki/rs-mca/raw/refs/heads/main/experimental/notes/m1/m1_cycle120_abf_counterexample_candidate.md>

7. **strict264 audit**
   <https://github.com/przchojecki/rs-mca/raw/refs/heads/main/experimental/notes/m1/m1_strict264_audit.md>

8. **F1 syndrome-pencil normal form**
   <https://github.com/przchojecki/rs-mca/raw/refs/heads/main/experimental/notes/f1/f1_syndrome_pencil_normal_form.md>

9. **L2 codegree reduction theorem**
   <https://github.com/przchojecki/rs-mca/raw/refs/heads/main/experimental/notes/l2/l2_codegree_reduction_theorem.md>

10. **Current finite-row threshold note**
   Local TeX: [`experimental/notes/thresholds/f17_32_finite_mca_threshold.tex`](experimental/notes/thresholds/f17_32_finite_mca_threshold.tex)
   Local PDF: [`experimental/notes/thresholds/f17_32_finite_mca_threshold.pdf`](experimental/notes/thresholds/f17_32_finite_mca_threshold.pdf)

---

## 1. Executive summary

The current project is not yet a full Proximity Prize solution. It now has a clean solved finite-row threshold theorem for the main \(\mathbb F_{17^{32}}\), \(n=512,k=256\) row under the finite-slope support-wise MCA convention, plus a clear compiler theorem that explains which rows are solved by the high-agreement tangent regime.

The Proximity Prize asks for the MCA threshold for Reed-Solomon codes over smooth domains at rates

\[
\rho \in \{1/2,1/4,1/8,1/16\}
\]

against target error

\[
\varepsilon^* = 2^{-128}.
\]

The prize-shaped object is not merely a lower bound. It is the threshold

\[
\delta_C^*
\]

or, equivalently, the integer agreement threshold where the bad-line/slack count drops below the \(2^{-128}\) budget.

Current solved finite row:

\[
C = \mathrm{RS}[\mathbb F_{17^{32}}, H, 256],
\qquad |H| = 512,
\qquad \rho = 1/2.
\]

For this row,

\[
\left\lfloor 17^{32}/2^{128}\right\rfloor=6.
\]

The high-agreement tangent staircase proves the exact finite-slope support-wise MCA numerator

\[
B_C(a)=LD_{\mathrm{sw}}(C,a)=513-a
\qquad (a\ge427).
\]

Therefore

\[
LD_{\mathrm{sw}}(C,506)=7,
\qquad
LD_{\mathrm{sw}}(C,507)=6.
\]

Since

\[
6\cdot2^{128}<17^{32}<7\cdot2^{128},
\]

the pure finite-slope MCA grid threshold is pinned exactly:

```text
safe:   integer radius r <= 5, agreement a >= 507
unsafe: integer radius r >= 6, agreement a <= 506
```

With closed real Hamming balls, the safe interval is

\[
0\le\delta<6/512=3/256.
\]

Thus the supremal transition radius is \(3/256\), but the endpoint is unsafe. If a formulation asks for a maximum safe closed radius on the finite grid, the answer is \(5/512\).

This supersedes the old "strict264 next" plan. The strict264 and strict352 packets remain useful mechanism records, but they are no longer the shortest path to pinning the \(\mathbb F_{17^{32}}\), \(512,256\) row.

The full-prize path is:

1. finish the definition audit against the official MCA sampler: finite/projective slopes, endpoint convention, denominator, and support-wise predicate;
2. package the finite-row theorem as a clean threshold result, with scanner output attached;
3. promote the row-independent high-agreement threshold compiler:
   \[
   B_Q=\lfloor Q/2^{128}\rfloor,\qquad r=n-a;
   \]
4. prove the compiler theorem cleanly: if \(B_Q\le\lfloor(n-k)/3\rfloor\), then the line/MCA grid threshold is exactly \(r=B_Q\);
5. use the compiler to carve out the solved high-agreement region of the prize envelope;
6. isolate the remaining hard work: lower-agreement quotient cores, aperiodic local limits, extension transfer, and interleaved-list constants.

---

## 2. Glossary and notation

Use the following notation consistently.

### 2.1 Code parameters

Let

\[
C = \mathrm{RS}[\mathbb F, H, k],
\]

where

\[
n = |H|,
\qquad
\rho = k/n.
\]

The agreement level is

\[
a.
\]

The slack is

\[
\sigma = a-k.
\]

The relative radius is

\[
\delta = 1-a/n = 1-\rho-\sigma/n.
\]

The redundancy is

\[
r = n-k.
\]

The support-complement size is

\[
j = n-a.
\]

Thus

\[
\sigma = a-k = r-j.
\]

### 2.2 Field ledgers

Every note, script, and certificate must print all three field quantities:

```text
q_gen   = field generated by the domain or construction
q_line  = field from which MCA line slopes/challenges are sampled
q_chal  = field in the challenge/protocol interpretation, if different
```

Do not conflate these. Many false or overstated claims arise from silently replacing one by another.

### 2.3 Bad-slope count

Let

\[
B_C(a)
=
\#\{\text{bad MCA line slopes at agreement at least } a\}.
\]

Depending on the note, this may also be written as

\[
LD_{\mathrm{sw}}(C,a).
\]

The MCA error at radius \(\delta\) is, up to endpoint convention,

\[
\varepsilon_{\mathrm{mca}}(C,\delta)
=
\frac{B_C(\lceil (1-\delta)n\rceil)}{q_{\mathrm{line}}}.
\]

The Proximity Prize threshold is the largest radius \(\delta_C^*\) such that

\[
\varepsilon_{\mathrm{mca}}(C,\delta_C^*) \le 2^{-128}.
\]

Equivalently, determine the agreement staircase

\[
B_C(k),B_C(k+1),B_C(k+2),\ldots
\]

well enough to locate the first safe level.

### 2.4 Endpoint convention

Every result must say whether it uses:

```text
agreement at least a
agreement greater than a
distance at most delta n
distance less than delta n
closed radius
strict radius
supremum threshold
maximum threshold
```

Do not hide endpoint choices.

---

## 3. Where we are

### 3.1 The no-slack direction is dead

Paper A establishes no-slack obstructions for smooth-domain Reed-Solomon MCA/RCA-type claims. The obstruction is quotient-locator mass: smooth domains with quotient structure produce many bad slopes at the no-slack boundary.

The correct response is not to try to repair no-slack RCA/MCA. The correct response is to work with slack and to determine how much slack is needed after quotient-periodic floors are accounted for.

Project rule:

```text
No collaborator should pursue smooth no-slack MCA/RCA as a positive theorem.
All positive statements must include slack and explicit quotient floors.
```

### 3.2 The current finite frontier is a real lower bound

Current row:

\[
C = \mathrm{RS}[\mathbb F_{17^{32}}, H, 256],
\quad |H|=512,
\quad \rho=1/2.
\]

Board value:

\[
N_{\mathrm{bad}} = 52{,}747{,}567{,}092.
\]

Denominator:

\[
q_{\mathrm{line}} = 17^{32}.
\]

This gives

\[
N_{\mathrm{bad}}/q_{\mathrm{line}} \approx 2^{-95.18}.
\]

The row is strong because it is more than 32 bits above the \(2^{-128}\) target. But it is not a full prize solution because it only proves unsafety at a radius. It does not prove the matching safe radius.

### 3.3 What has and has not been solved

The project has not yet determined the full Proximity Prize threshold for smooth-domain Reed-Solomon codes.

What is settled:

```text
smooth no-slack MCA/RCA optimism is false;
explicit smooth-domain obstruction floors exist;
the current finite frontier gives real bad-side certificates;
Paper D caps delta_C^*(2^-128) away from capacity across the challenge envelope.
```

What is not yet settled:

```text
the exact delta_C^*(2^-128) for every smooth-domain RS[F,L,k];
the matching safe-side upper bounds below the obstruction radius;
the full agreement staircase B_C(a) for the main finite rows;
the aperiodic local-limit theorem after quotient-periodic floors are removed.
```

In the language of the ePrint challenge, current results mostly prove statements of the form

\[
\delta_C^*(2^{-128}) \le \Delta_{\mathrm{cap}}
\]

or produce explicit radii where

\[
\varepsilon_{\mathrm{mca}}(C,\delta)>2^{-128}.
\]

That is necessary but not sufficient for resolving the challenge. To resolve it for a code \(C\), one must specify a candidate threshold \(\delta_C^*\) and prove both sides of the staircase:

1. for every \(\delta>\delta_C^*\), the MCA error is larger than \(2^{-128}\);
2. for every \(\delta<\delta_C^*\), or for the corresponding next safer agreement level after endpoint conventions are fixed, the MCA error is at most \(2^{-128}\).

Equivalently, in integer agreement language, one must locate the first agreement level \(a\) at which

\[
LD_{\mathrm{sw}}(C,a) \le \lfloor q_{\mathrm{line}}2^{-128}\rfloor
\]

and prove the adjacent lower level is still unsafe.

### 3.4 Position relative to Proximity Prize Table 1

The Proximity Prize survey table in `open-proximity.tex` separates four benchmark regimes for

\[
C=\mathrm{RS}[F,L,k],\qquad n=|L|.
\]

| Table 1 regime | Benchmark behavior | What it means for this project |
| --- | --- | --- |
| \(\delta=0\) | \(\varepsilon_{\mathrm{mca}}(C,\delta)=2/|F|\) | Baseline only. |
| \(\delta<\delta_{\min}(C)/2\) | \(\varepsilon_{\mathrm{mca}}(C,\delta)\le O(n)/|F|\) | Unique-decoding regime; not where the frontier row lives. |
| \(\delta=J(\delta_{\min}(C))-\eta\) | \(\varepsilon_{\mathrm{mca}}(C,\delta)\le n\cdot \mathrm{poly}(1/\eta)/|F|\) | Johnson-radius upper-bound regime; useful as the known safe side, but not the current obstruction frontier. |
| \(\delta\approx\delta_{\min}(C)-1/\Omega(\log n)\) | \(\varepsilon_{\mathrm{mca}}(C,\delta)\ge n^{\Omega(1)}/|F|\) for large enough \(F\) | Capacity-edge lower-bound regime; this is the row our current bad-slope certificates are trying to sharpen. |

So the answer to "are we doing case 3?" is no. Case 3 is the positive Johnson-radius result. The current RS-MCA frontier is a case-4 / capacity-edge lower-bound program.

For the active row

\[
n=512,\quad k=256,\quad \rho=1/2,
\]

the exact relative minimum distance is

\[
\delta_{\min}(C)=\frac{n-k+1}{n}=\frac{257}{512},
\]

and the Johnson radius is

\[
J(\delta_{\min}(C))
=1-\sqrt{1-\delta_{\min}(C)}
=1-\sqrt{255/512}
\approx 0.2943.
\]

The old lower-agreement frontier records certificates near

\[
\delta=249/512\approx 0.4863,
\]

and the former strict264 target used

\[
\delta=31/64=248/512\approx 0.4844.
\]

Both are far beyond the Johnson radius and very close to capacity. They are therefore useful negative-side mechanism records in the hard band between Johnson and capacity. For the finite \(\mathbb F_{17^{32}}\) row, however, the exact high-agreement tangent theorem now gives a complete threshold much closer to zero radius:

\[
\delta_{\rm grid}^{\rm safe}=5/512,
\qquad
\delta_{\rm grid}^{\rm first\ unsafe}=6/512.
\]

What remains missing for the full prize is not this finite-row threshold, but the lower-agreement local-limit theory needed near capacity for large prize-envelope rows.

The same source also makes line-decoding relevant: Theorem 4.21 says \((\delta,a,n+1)\) line-decodability implies \(\varepsilon_{\mathrm{mca}}(C,\delta)\le a/|F|\). Our M2 bridge and F1 normal form should be read as attempts to put the support-wise MCA staircase into that line-decoding language without losing the exact finite denominator.

### 3.5 How to approach the full threshold

The route to an actual \(\delta_C^*\) theorem has two tracks.

**Finite-row track.** The main board row

\[
C=\mathrm{RS}[\mathbb F_{17^{32}},H,256],
\quad n=512,
\quad \rho=1/2.
\]

is now pinned in the high-agreement regime. The numerical cutoff is

\[
\lfloor 17^{32}/2^{128}\rfloor = 6.
\]

The tangent staircase gives

\[
LD_{\mathrm{sw}}(C,a)=513-a
\qquad(a\ge427),
\]

so

\[
LD_{\mathrm{sw}}(C,506)=7,
\qquad
LD_{\mathrm{sw}}(C,507)=6.
\]

This turns the row into an exact finite threshold computation under the finite-slope support-wise MCA convention. The immediate finite-row work is now packaging and audit, not strict264 search.

Concrete attacks:

- audit the finite-slope support-wise MCA definition against the official prize definition and paper definitions;
- state the theorem as a threshold theorem with exact closed endpoint language;
- attach scanner output for the pure MCA profile, not only the line-plus-list protocol profile;
- record the projective-slope variant separately, with denominator \(|F|+1\);
- keep strict264/strict352 as mechanism and lower-agreement stress tests, not as the active threshold target for this row.

**General smooth-domain track.** The next theorem is the row-independent high-agreement compiler. Let

\[
B_Q=\lfloor Q/2^{128}\rfloor,
\qquad
r=n-a.
\]

If

\[
B_Q\le \left\lfloor\frac{n-k}{3}\right\rfloor,
\]

then the high-agreement tangent theorem pins the single line/MCA/CA grid threshold exactly:

\[
r\le B_Q-1 \quad\text{is safe},\qquad r=B_Q\quad\text{is unsafe}.
\]

This gives a clean solved region of the prize envelope. Outside that region, prove the floor-corrected local-limit theorem. The target theorem should not say "smooth RS is safe up to capacity." It should say that above a stated reserve

\[
\eta = 1-\rho-\delta
\]

the bad-slope count is bounded by tangent, quotient-profile, and aperiodic terms divided by \(q_{\mathrm{line}}\). The quotient term must remain explicit.

Concrete attacks:

- prove generated-field locator local limits after quotient cores are budgeted;
- prove residue-line packing bounds in the F1 Hankel-pencil normal form;
- show interleaved-list codegree reductions do not lose the exponent needed for protocol fields;
- prove extension-line transfer theorems or exhibit extension-only counterexamples;
- convert the resulting bounds into explicit agreement thresholds for all prize rates and all admissible \(k\le2^{40}\), \(|F|<2^{256}\).

The end product should be a theorem or certificate generator that takes

```text
F, L, k, q_gen, q_line, q_chal
```

and outputs either a proved threshold interval for \(\delta_C^*(2^{-128})\) or a declared obstruction/counterexample floor.

### 3.6 strict264 is now a mechanism record

At \(a=264\),

\[
\sigma = a-k = 8.
\]

The target is

\[
LD_{\mathrm{sw}}(C,264)\ge 7.
\]

Since

\[
17^{32}/2^{128} \approx 6.9587,
\]

the inequality

\[
7/17^{32} > 2^{-128}
\]

holds.

The strict264 audit verifies much of the algebraic bridge:

- bridge arithmetic;
- slack-8 two-ended setup;
- common parity-check identity;
- triangular recovery;
- noncontainment rank checks;
- end-to-end support-wise line-decoding transfer.

The remaining open piece is the exact survivor count. That is still useful as a lower-agreement mechanism test and as input for the harder local-limit program. It is no longer the first clean finite prize push, because the high-agreement tangent theorem already pins the current row's finite-slope MCA threshold at \(a=506/507\).

### 3.7 The main theoretical gap is the aperiodic local limit

Paper B isolates the correct positive-theorem shape:

\[
\varepsilon_{\mathrm{mca}}(C_n,1-\rho-\eta_n)
\le
\frac{
n^{1+o(1)}
+
2^{(\beta(\rho)/H(\rho))\mathcal Q_{H_n}(\eta_n)(1+o(1))}
}{q_n}.
\]

The terms are:

```text
tangent floor
quotient-periodic floor
aperiodic residue-line mass
```

The quotient floor is real and must remain on the right-hand side. The missing hard theorem is a finite-field local-limit bound for arbitrary-word list decoding and all-line MCA after quotient cores have been removed.

### 3.8 The F1 normal form is the main algebraic tool

The F1 note turns all-line support-wise MCA into a Hankel-pencil incidence problem.

For a support complement \(T\) of size \(j\), let

\[
L_T(X)=\prod_{x\in T}(X-x)
\]

be its locator, with coefficient vector \(\ell_T\). A slope \(z\) is bad only if

\[
H_{t,j}(u+zv)\ell_T=0,
\qquad
t = r-j = \sigma.
\]

This gives an exact finite object for upper bounds. For agreement \(265\) in the main row:

\[
a=265,\quad j=247,\quad t=\sigma=9.
\]

Thus the finite upper-bound problem is:

\[
\#\left\{
z\in\mathbb F_{17^{32}}:
\exists\text{ split squarefree locator }\ell_T
\text{ of degree }247
\text{ with }
H_{9,247}(u+zv)\ell_T=0
\right\}
\le 6,
\]

with noncontainment enforced.

---

## 4. The win condition

### 4.1 Full-prize-shaped theorem

For each challenge row \(C\), determine

\[
\delta_C^*
\]

or the equivalent agreement threshold

\[
a_C^*.
\]

A full result should produce both:

1. a lower-bound floor showing unsafety below or at one agreement level;
2. an upper-bound theorem showing safety above the next agreement level.

A typical threshold statement should look like:

\[
B_C(a_0) > 2^{-128}q_{\mathrm{line}},
\]

but

\[
B_C(a_0+1) \le 2^{-128}q_{\mathrm{line}}.
\]

Then

\[
\delta_C^*
\]

is determined by the agreement/radius conversion and the endpoint convention.

### 4.2 Finite-row threshold target

For the current row:

\[
C = \mathrm{RS}[\mathbb F_{17^{32}},H,256],
\quad n=512.
\]

The desired finite theorem is:

\[
LD_{\mathrm{sw}}(C,a)=513-a
\qquad(a\ge427),
\]

with the target comparison

\[
LD_{\mathrm{sw}}(C,506)=7>17^{32}/2^{128},
\qquad
LD_{\mathrm{sw}}(C,507)=6\le17^{32}/2^{128}.
\]

This is not by itself the entire Proximity Prize, but it is the right local shape: it pins an agreement staircase, not merely a lower bound. The exact endpoint statement is:

```text
closed grid: largest safe integer radius is 5/512
closed grid: first unsafe integer radius is 6/512
real closed balls: safe interval is [0,6/512)
supremum: 6/512 = 3/256, not attained
```

### 4.3 Asymptotic/full theorem target

For families

\[
C_n = \mathrm{RS}[\mathbb F_{q_n},H_n,k_n],
\qquad |H_n|=n,
\qquad k_n=\rho n+O(1),
\]

with

\[
\rho \in \{1/2,1/4,1/8,1/16\},
\]

prove an explicit floor-corrected MCA theorem.

Desired form:

\[
\varepsilon_{\mathrm{mca}}(C_n,1-\rho-\eta_n)
\le
\frac{
A_\rho(n,\sigma_n)
+
Q_\rho(H_n,\sigma_n)
}{q_n},
\]

where:

- \(A_\rho\) is the tangent/aperiodic term, ideally \(n^{1+o(1)}\) or an explicit \(n^B\);
- \(Q_\rho\) is the quotient-profile floor;
- \(\sigma_n = \eta_n n\);
- the constants are explicit enough to compare against \(2^{-128}\).

Then solve:

\[
A_\rho(n,\sigma)+Q_\rho(H,\sigma)
\le
2^{-128}q
\]

for \(\sigma\), and convert to

\[
\delta = 1-\rho-\sigma/n.
\]

---

## 5. Project lanes

Run the project in five coordinated lanes.

```text
Lane A: finite certificate lane
Lane B: finite threshold lane
Lane C: general MCA theorem lane
Lane D: list/interleaving lane
Lane E: extension-field and sampler lane
```

A sixth support lane should handle formalization and peer-review packaging.

```text
Lane V: verification, formalization, and review lane
```

Each lane has concrete tasks and exit criteria below.

---

# Lane A: finite certificate lane

## A.0 Objective

Make the historical \(52.7\)B row, strict264 packet, and strict352 packet independently replayable as lower-agreement mechanism records. The current finite-row threshold itself is handled by the high-agreement tangent theorem and belongs to Lane B / Lane V packaging.

This lane is about trust. Its output should be:

```text
small certificate files
independent verifiers
exact field/domain ledgers
deduped bad-slope lists or compressed proof of slope count
noncontainment certificates
radius/agreement/endpoint checks
```

## A.1 Freeze the finite row

For

\[
C=\mathrm{RS}[\mathbb F_{17^{32}},H,256],
\qquad |H|=512,
\]

freeze:

```text
field polynomial for F_17^32
basis convention
domain generator
domain ordering
hash of H
k=256
n=512
rho=1/2
line field
challenge denominator q_line
received words f1, f2 or their reproducible construction
support convention
endpoint convention
```

Every certificate must be reproducible from these data.

### Acceptance checklist

A frozen row is accepted only if an independent checker can print:

```text
n = 512
k = 256
rho = 1/2
field = F_17^32
q_line = 2367911594760467245844106297320951247361
2^128 = 340282366920938463463374607431768211456
floor(q_line / 2^128) = 6
7 * 2^128 > q_line
```

## A.2 Certificate schema

For each bad slope \(\gamma\), or for each compressed orbit class, the certificate should contain:

```text
gamma
agreement a
slack sigma = a-k
support S_gamma or complement J_gamma
locator L_J(X)
explaining polynomial P_gamma(X), or enough data to recover it
rank / syndrome proof that explanation exists
noncontainment proof
deduplication key
endpoint convention
```

Mathematically, the verifier should check:

\[
\deg P_\gamma < k,
\]

\[
(f_1+\gamma f_2)|_{S_\gamma} = P_\gamma|_{S_\gamma},
\]

\[
|S_\gamma|\ge a,
\]

and

\[
(f_1,f_2)
\text{ are not simultaneously explained by codewords on }S_\gamma.
\]

The noncontainment condition is essential. A bad line slope without support-wise noncontainment is not an MCA obstruction.

## A.3 Independent verifiers

Build two independent verifiers.

### Verifier 1: high-level algebra verifier

Suggested stack:

```text
Sage
Magma
PARI/GP
```

Checks:

```text
field construction
domain construction
locator splitting
interpolation
degree bound
agreement count
slope distinctness
noncontainment rank
```

### Verifier 2: low-level arithmetic verifier

Suggested stack:

```text
Rust
C++
minimal Python
```

Do not reuse Sage's finite-field implementation.

Checks:

```text
polynomial-basis multiplication mod m(alpha)
addition/subtraction
inversion if needed
evaluation on H
Vandermonde/rank check
hash of certificate
```

### Acceptance checklist

A slope certificate is accepted only if both verifiers agree on:

```text
gamma hash
support hash
agreement a
deg P < k
noncontainment = true
```

## A.4 Replay the 52.7B row

The current row

\[
N_{\mathrm{bad}}=52{,}747{,}567{,}092
\]

must be converted into one of the following accepted formats:

1. full slope list;
2. compressed orbit list with exact orbit-size proof;
3. slot-model count with proof of injection into distinct slopes;
4. deterministic generator with transcript hash;
5. algebraic family with proof of deduplicated slope count.

Unacceptable formats:

```text
raw support count
pre-deduplication count
count over wrong field
count without endpoint convention
count without noncontainment
count imported from an external cycle without in-repo reproduction
```

### Acceptance criterion

The row is replayed when an independent machine can verify:

\[
LD_{\mathrm{sw}}(C,263)
\ge
52{,}747{,}567{,}092
\]

or a corrected number with a clear explanation of the correction.

## A.5 strict264 task

Parameters:

\[
n=512,
\qquad k=256,
\qquad a=264,
\qquad \sigma=8,
\qquad j=248,
\qquad r=256.
\]

Target:

\[
LD_{\mathrm{sw}}(C,264)\ge 7.
\]

Because

\[
7/17^{32} > 2^{-128},
\]

this proves failure at radius

\[
\delta = 1-264/512 = 31/64.
\]

### Corrected two-ended fixed-jet condition

The strict264 audit caught an off-by-one. The valid setup fixes:

```text
e_1, e_2, ..., e_7
plus the endpoint condition
```

Do not use a version that frees the last top coefficient.

### Work plan

1. Recover or reconstruct the seven-slot co-support model.
2. Implement the corrected fixed-jet filter.
3. For each candidate co-support \(J\):
   - compute locator \(P_J(X)\);
   - check the fixed \(e_1,\ldots,e_7\) conditions;
   - check the endpoint condition;
   - compute \(P_J(\beta)\);
   - compute slope \(z_J=-1/P_J(\beta)\);
   - deduplicate slopes.
4. Verify support-wise noncontainment.
5. Output at least seven distinct slopes with certificates.

### Minimal output

Do not wait for a massive count. The minimal accepted result is:

```text
strict264-seven.jsonl
strict264-row.md
verifier-1 transcript
verifier-2 transcript
```

containing exactly seven verified slopes.

## A.6 If strict264 fails

A failed strict264 attempt is still useful if it is exact.

If the seven-slot model yields fewer than seven slopes, output:

```text
model definition
candidate count
post-filter count
post-dedup count
reason for each rejection class
```

Then try alternatives in this order:

1. different \(\beta\notin H\);
2. different endpoint;
3. different two-ended jet family;
4. three-ended or mixed-ended constraints;
5. non-slot aperiodic search through the Hankel-pencil normal form;
6. nearby fields with \(512\mid(q-1)\) and \(q\) close enough to \(2^{128}\) that a small number of slopes suffices.

---

# Lane B: finite threshold lane

## B.0 Objective

Move from finite lower bounds to finite threshold pinning.

For the current row, prove:

\[
LD_{\mathrm{sw}}(C,264)\ge 7
\]

and

\[
LD_{\mathrm{sw}}(C,265)\le 6.
\]

The first inequality is a lower-bound certificate. The second is an all-line upper-bound theorem.

**Status caveat, 2026-06-30.**  Under the finite-slope support-wise convention
used by the threshold notes, the displayed agreement-265 upper target is already
false.  The integrated coset-packet finite-slope floor proves
\[
LD_{\mathrm{sw}}(C,265)\ge \binom{31}{16}=300{,}540{,}195,
\]
and the same lower-floor package gives more than six bad finite slopes through
agreement \(288\).  See
`experimental/notes/thresholds/agreement265_status_audit.md`.  Therefore this
lane should be read as an old finite-row target unless a different sampler
convention is intended; for the finite-slope predicate, the first agreement not
ruled out by the current lower-floor package is \(a=289\).

## B.1 Formulate agreement 265 as a Hankel-pencil problem

At \(a=265\),

\[
j=n-a=247,
\qquad
t=r-j=256-247=9.
\]

Use the F1 normal form:

\[
H_{9,247}(u+zv)\ell_T=0.
\]

The upper-bound target is:

\[
\#\left\{
z\in\mathbb F_{17^{32}}:
\exists T\subset H,\ |T|=247,\ L_T \text{ split squarefree},
H_{9,247}(u+zv)\ell_T=0,
\text{ noncontainment}
\right\}
\le 6.
\]

## B.2 Branch classification

Every potential bad slope/support pair must be classified as exactly one of:

```text
quotient-periodic
tangent/fixed-root
rank-defective
subfield-confined
aperiodic residue-line
collision-borne finite-field artifact
unresolved
```

The quotient-periodic class is not an error. It is part of the lower and upper theorem.

## B.3 Prove small-t ledgers first

Before trying \(t=9\), write clean proofs for low \(t\).

Tasks:

```text
B3.1 Reprove t=1.
B3.2 Reprove t=2 from the F1 note.
B3.3 Extend to t=3.
B3.4 Identify which arguments scale to t=8 and t=9.
B3.5 Record exactly where scaling fails.
```

The \(t=2\) ledger should include:

```text
determinant quadric
fixed-slope codimension-two fibers
rank-defective slopes
fixed-root stars
global monic-rank defects
quotient-periodic sparse pullbacks
```

## B.4 Use \(X^{512}-1\)

In the current row, \(H\) has size \(512\), and split squarefree locators over \(H\) correspond to divisors of

\[
X^{512}-1.
\]

Use the quotient ring

\[
\mathbb F_{17^{32}}[X]/(X^{512}-1)
\]

to reduce the upper-bound problem.

Allowed strategies:

```text
orbit reduction under H-multiplication
quotient-map reduction X -> X^M
resultants eliminating locator coefficients
Gröbner basis on reduced branch variables
Nullstellensatz certificates for no-seven-slope branches
syndrome-rank certificates for exceptional branches
```

## B.5 Upper-bound artifact

An acceptable agreement-265 upper-bound artifact should include:

```text
finite branch decomposition
for each branch:
  branch definition
  proof all cases in branch are covered
  maximum number of bad slopes from branch
  certificate or symbolic proof
global union bound
deduplication handling
endpoint convention
```

The target is

\[
LD_{\mathrm{sw}}(C,265)\le6.
\]

A weaker but useful intermediate target is:

\[
LD_{\mathrm{sw}}(C,265)\le n^{O(1)}
\]

with quotient and aperiodic branches separated.

---

# Lane C: general MCA theorem lane

## C.0 Objective

Prove the floor-corrected all-line MCA theorem above the corrected reserve.

The theorem should cover the rates:

\[
\rho\in\{1/2,1/4,1/8,1/16\}.
\]

It should output explicit slack thresholds that can be compared with \(2^{-128}\).

## C.1 Desired theorem shape

Let

\[
C_n=\mathrm{RS}[\mathbb F_{q_n},H_n,k_n],
\quad |H_n|=n,
\quad k_n=\rho n+O(1).
\]

Let

\[
a_n=k_n+\sigma_n,
\qquad
\eta_n=\sigma_n/n.
\]

For slack above the corrected reserve, prove:

\[
\varepsilon_{\mathrm{mca}}(C_n,1-\rho-\eta_n)
\le
\frac{
A_\rho(n,\sigma_n)
+
Q_\rho(H_n,\sigma_n)
}{q_n}.
\]

Interpretation:

```text
A_rho = tangent + aperiodic residue-line contribution
Q_rho = quotient-periodic floor
```

A useful asymptotic version is:

\[
A_\rho(n,\sigma_n) = n^{1+o(1)}
\]

and

\[
Q_\rho(H_n,\sigma_n)
=
2^{(\beta(\rho)/H(\rho))\mathcal Q_{H_n}(\eta_n)(1+o(1))}.
\]

But a prize-grade theorem must eventually be explicit:

\[
A_\rho(n,\sigma) \le C_\rho n^{B_\rho}
\]

or better, with computable constants.

## C.2 Lower-bound floor theorem

First, make the lower floors clean and computable.

For every smooth domain \(H\), slack \(\sigma\), and rate \(\rho\), compute:

```text
tangent floor
quotient-periodic floor
finite collision floor, if present
```

The quotient floor is necessary. Do not sweep it into an error term.

Deliverable:

```text
theorem: explicit MCA lower floors
inputs:
  H, n, k, sigma, q_line
outputs:
  lower bound on B_C(k+sigma)
  lower bound on epsilon_mca
  class labels for each floor
```

## C.3 Aperiodic residue-line bound

This is the central mathematical problem.

After quotient-periodic and tangent branches are removed, prove:

\[
\#\{\text{aperiodic bad slopes}\}
\le n^{1+o(1)}
\]

or an explicit \(n^B\) bound.

Equivalently, prove that many bad slopes force structure:

\[
\text{many bad slopes}
\Rightarrow
\text{many locator collisions}
\Rightarrow
\text{quotient periodicity or template structure}.
\]

## C.4 Local-limit program

Attack the local-limit theorem in stages.

### C4.1 Prefix-map local limit

For subsets \(S\subset H\) of size \(a\), study

\[
\Phi_\sigma(S) = (e_1(S),\ldots,e_\sigma(S)).
\]

After quotient cores are removed, prove small fibers:

\[
\#\{S:\Phi_\sigma(S)=c\}
\le n^B.
\]

Start with:

```text
monomial-prefix words
canonical multiplicative subgroups
zero-base lines
fixed direction lines
arbitrary base lines
```

### C4.2 Locator-fiber local limit

Generalize from elementary-symmetric prefixes to arbitrary received-word locator constraints.

Target:

\[
\#\{T\subset H:\ |T|=j,\ H_{t,j}(w)\ell_T=0\}
\le
Q(H,\sigma,w)+n^B.
\]

### C4.3 Residue-line local limit

Now allow line data \(w=u+zv\). Bound the number of slopes \(z\) for which there exists an admissible split squarefree locator.

Target:

\[
\#\{z:\exists T,\ H_{t,j}(u+zv)\ell_T=0,\ T \text{ aperiodic}\}
\le n^B.
\]

### C4.4 Inverse theorem

Prove:

```text
If an aperiodic branch produces too many slopes,
then the support complements must have quotient-periodic,
subfield, or low-template structure.
```

This converts high multiplicity into one of the already-budgeted floors.

## C.5 Constants and finite ranges

The asymptotic theorem is not enough for the prize. The target error \(2^{-128}\) forces explicit constants.

For each rate

\[
\rho\in\{1/2,1/4,1/8,1/16\},
\]

produce:

```text
C_rho
B_rho
n0_rho
```

such that for \(n\ge n0_\rho\),

\[
\varepsilon_{\mathrm{mca}}(C,1-\rho-C_\rho/\log n)
\le 2^{-128}
\]

whenever the quotient floor is below budget.

For \(n<n0_\rho\), use finite verification.

---

# Lane D: list-decoding and interleaving lane

## D.0 Objective

Prove the list-decoding local-limit inputs needed by the MCA theorem, and use the L2 codegree theorem correctly.

Do not conflate:

```text
ordinary list decoding
interleaved list decoding
CA
MCA
support-wise line decoding
protocol soundness
```

Every claim must say which object it proves.

## D.1 Arbitrary-word list theorem

Target:

\[
\#\{S\subset H:\ |S|=k+\sigma,\ \text{locator constraints match }U\}
\le
Q(H,\sigma,U)+n^B.
\]

Here \(Q\) captures quotient-periodic floors.

Prove in stages:

```text
monomial-prefix received words
sparse received words
quotient-periodic received words
random-looking received words
arbitrary received words
```

## D.2 Higher-agreement decay

The L2 codegree theorem reduces interleaved list size to base-code list sizes at agreements \(a\) and \(2a-k\). Since

\[
2a-k = a+\sigma,
\]

we need stronger decay at the higher agreement.

Target:

\[
M_U(a+\sigma)\le \mathrm{poly}(n)
\]

for aperiodic \(U\).

## D.3 Use the L2 theorem

The L2 note gives a reduction of the form:

\[
\Lambda_2^{(a)}
\le
|Fib_{U_2}|
+
M_{U_2}(2a-k)|Fib_{U_1}|.
\]

For higher interleaving arity \(\mu\), apply the recursive version.

Work sequence:

```text
D3.1 Prove L1 aperiodic list bound at agreement a.
D3.2 Prove L1 higher-agreement decay at 2a-k.
D3.3 Plug into L2 codegree theorem.
D3.4 Keep quotient tails explicit.
D3.5 State interleaved theorem with all floors visible.
```

Do not claim an interleaved-list solution until D3.1 and D3.2 are proved.

---

# Lane E: extension-field and sampler lane

## E.0 Objective

Prevent false conclusions caused by subfield confinement or wrong denominators.

Every line/slope count must specify the actual sampling field.

## E.1 Field-ledger rule

Every public result must contain:

```text
q_gen
q_line
q_chal
```

Example for the main finite row:

```text
q_gen  = 17^32, unless domain generation says otherwise
q_line = 17^32 for the ABF line sampler
q_chal = explicitly stated; do not assume it equals q_line
```

## E.2 Classify witnesses by field origin

Each witness family must be labeled:

```text
B-valued line
F-valued line
mixed-valued line
subfield-confined
genuinely extension-field
```

A base-field witness over \(B\subset F\) may deflate by \(|B|/|F|\) when slopes are sampled from \(F\). This distinction matters.

## E.3 Build genuinely extension-field witnesses

Use the F1 residue-line normal form to search for line data \(u,v\) that are genuinely \(F\)-valued and whose bad slopes are not confined to a small subfield.

Deliverable:

```text
explicit F-valued f,g
field ledger
bad-slope certificates
subfield-confinement test
comparison to base-field baseline
```

---

# Lane V: verification, formalization, and review

## V.0 Objective

Make every finite and threshold claim reviewable.

The prize page expects public academic materials and peer review. Build this infrastructure early.

## V.1 Formalize easy finite gates first

Recommended formalization targets:

```text
V1 endpoint monotonicity
V2 agreement/radius staircase
V3 7 * 2^128 > 17^32
V4 Vandermonde rank noncontainment lemma
V5 Hankel recurrence equivalence
V6 duplicate-slope semantics
V7 quotient-periodic locator definition
```

Do not start formalization with the hardest local-limit theorem. Formalize the finite gates and the bridges reviewers will inspect first.

## V.2 Reproducibility package

Every public result should ship with:

```text
README
exact claim
non-claims
field/domain ledger
certificate files
verifier scripts
expected transcript
hashes
license
```

## V.3 Peer-review strategy

Prepare papers in modules, not one sprawling manuscript.

### Paper 1: finite-row MCA threshold theorem

Claim:

\[
\mathrm{RS}[\mathbb F_{17^{32}},H,256]
\quad\text{has finite-slope support-wise MCA grid threshold}\quad
r=6.
\]

Equivalently, \(r=5\) is safe, \(r=6\) is unsafe, the real closed-ball safe interval is \([0,6/512)\), and the endpoint \(6/512=3/256\) is unsafe.

Contents:

```text
definitions
field/domain ledger
high-agreement tangent theorem
finite/projective slope definition audit
closed endpoint convention
pure-MCA scanner output
non-claims
```

### Paper 2: high-agreement threshold compiler

Claim:

\[
B_Q=\lfloor Q/2^{128}\rfloor,\quad r=n-a,\quad
B_Q\le\lfloor(n-k)/3\rfloor
\quad\Longrightarrow\quad
\text{threshold pinned at }r=B_Q.
\]

This identifies the solved high-agreement region of the prize envelope and isolates where the lower-agreement local-limit work begins.

### Paper 3: floor-corrected MCA theorem

Claim:

\[
\varepsilon_{\mathrm{mca}}(C,1-\rho-\eta)
\le
\frac{
\text{tangent}
+
\text{quotient}
+
\text{aperiodic}
}{q}.
\]

This is the main full-prize paper.

### Paper 4: arbitrary-word list and interleaving theorem

Claim:

```text
Above corrected reserve, arbitrary-word lists are polynomial
after quotient cores are separated,
and interleaving reduces via the codegree theorem.
```

---

## 6. Agent work packages

Use these as task briefs.

---

### Work package A1: finite-field verifier

**Goal.** Build an independent verifier for \(\mathbb F_{17^{32}}\) certificates.

**Inputs.**

```text
field polynomial m(alpha)
basis convention
domain H
certificate JSONL
```

**Outputs.**

```text
verified/failed status
hash of H
hash of each slope certificate
agreement count
degree check
noncontainment check
deduplication check
```

**Acceptance tests.**

```text
Print q_line exactly.
Print floor(q_line / 2^128) = 6.
Print 7 * 2^128 > q_line.
Verify at least one known certificate.
Reject a certificate with a duplicated slope.
Reject a certificate with missing noncontainment.
```

---

### Work package A2: strict264 seven-slope search

**Goal.** Produce seven strict264 bad slopes.

**Parameters.**

```text
n = 512
k = 256
a = 264
sigma = 8
j = 248
r = 256
q_line = 17^32
```

**Core condition.**

```text
Fix e_1,...,e_7 plus endpoint.
Do not use the off-by-one relaxed condition.
```

**Outputs.**

```text
strict264-seven.jsonl
strict264-proof.md
deduped slopes
support complements
locators
rank proofs
verifier transcripts
```

**Acceptance test.**

\[
LD_{\mathrm{sw}}(C,264)\ge 7.
\]

---

### Work package A3: current-row replay

**Goal.** Replay or replace the \(52.7\)B count.

**Outputs.**

```text
compressed count proof or deterministic replay
deduped slope count
endpoint convention
noncontainment proof
field ledger
```

**Acceptance test.**

\[
LD_{\mathrm{sw}}(C,263)
\ge
52{,}747{,}567{,}092
\]

or a corrected count with exact explanation.

---

### Work package B1: F1 normal form rewrite

**Goal.** Rewrite the syndrome-pencil normal form into final notation.

**Outputs.**

```text
definitions.md
hankel-pencil-theorem.md
proof of equivalence
noncontainment lemma
examples for t=1,2
```

**Acceptance test.**

Given \(u,v,T,z\), the note proves equivalence between bad support and

\[
H_{t,j}(u+zv)\ell_T=0.
\]

---

### Work package B2: agreement-265 upper-bound branch ledger

**Goal.** Start the proof of

\[
LD_{\mathrm{sw}}(C,265)\le6.
\]

**Parameters.**

```text
a = 265
j = 247
t = 9
```

**Outputs.**

```text
branch definitions
coverage proof
bound per branch
unresolved branch list
```

**Acceptance test.**

All possible bad slopes/supports are assigned to one branch:

```text
quotient-periodic
tangent/fixed-root
rank-defective
subfield-confined
aperiodic residue-line
finite collision
unresolved
```

---

### Work package C1: quotient-floor theorem

**Goal.** State and prove the explicit quotient lower floor.

**Outputs.**

```text
definition of quotient profile Q_H(eta)
lower-bound theorem
examples for rho = 1/2, 1/4, 1/8, 1/16
computation script
```

**Acceptance test.**

For a given smooth \(H\) and slack \(\sigma\), the script outputs the quotient-periodic lower floor that must appear in any upper theorem.

---

### Work package C2: prefix local-limit theorem

**Goal.** Bound fibers of the elementary-symmetric prefix map after quotient cores are removed.

**Map.**

\[
S\mapsto(e_1(S),\ldots,e_\sigma(S)).
\]

**Target.**

\[
\#\{S:\Phi_\sigma(S)=c,\ S\text{ aperiodic}\}
\le n^B.
\]

**Acceptance test.**

Prove the theorem for at least one nontrivial smooth-domain family beyond the trivial random model.

---

### Work package C3: residue-line local-limit theorem

**Goal.** Bound the number of bad slopes after quotient and tangent branches are removed.

**Target.**

\[
\#\{z:\exists T,\ H_{t,j}(u+zv)\ell_T=0,\ T\text{ aperiodic}\}
\le n^B.
\]

**Acceptance test.**

Prove or experimentally validate the bound in a finite row where all quotient branches have been separated.

---

### Work package D1: arbitrary-word list bound

**Goal.** Prove list-size bounds above corrected reserve.

**Target.**

\[
\#\{S:\ |S|=k+\sigma,\ U\text{ matches on }S\}
\le Q(H,\sigma,U)+n^B.
\]

**Acceptance test.**

Handle quotient-periodic received words separately and prove aperiodic polynomial bound for a nontrivial class.

---

### Work package D2: L2 integration

**Goal.** Use the L2 codegree theorem without overclaiming.

**Required inputs.**

```text
L1 bound at agreement a
L1 higher-agreement bound at 2a-k
quotient-tail accounting
```

**Acceptance test.**

State a theorem for interleaving arity \(\mu=2\) with explicit dependence on the L1 inputs.

---

### Work package E1: subfield-confinement audit

**Goal.** Audit every finite witness for subfield confinement.

**Outputs.**

```text
witness field label
B-valued/F-valued classification
bad-slope field span
q_line denominator
deflation factor, if any
```

**Acceptance test.**

No public row may be listed unless this audit is complete.

---

### Work package V1: formal finite gates

**Goal.** Formalize the arithmetic and endpoint lemmas.

**First targets.**

```text
7 * 2^128 > 17^32
agreement/radius conversion at n=512, a=264
monotonicity of B_C(a)
Vandermonde degree/rank lemma
```

**Acceptance test.**

A formal checker verifies the strict264 threshold inequality and the agreement/radius conversion.

---

## 7. Milestones

### Milestone 0: definitions freeze

**Exit criterion.**

A single definitions note fixes:

```text
epsilon_mca
LD_sw
agreement/radius conversion
closed vs strict endpoint
q_gen/q_line/q_chal
support-wise noncontainment
duplicate-slope semantics
```

### Milestone 1: current-row replay

**Exit criterion.**

\[
LD_{\mathrm{sw}}
(
\mathrm{RS}[\mathbb F_{17^{32}},H,256],263
)
\ge
52{,}747{,}567{,}092
\]

with a replayable or compressed certificate.

### Milestone 2: finite-row threshold package

**Exit criterion.**

\[
LD_{\mathrm{sw}}(C,506)=7,
\qquad
LD_{\mathrm{sw}}(C,507)=6,
\]

with the definition audit and scanner output included.

### Milestone 3: row-independent compiler

**Exit criterion.**

\[
B_Q\le\lfloor(n-k)/3\rfloor
\quad\Longrightarrow\quad
\text{safe for }r\le B_Q-1,\ \text{unsafe at }r=B_Q.
\]

This turns the high-agreement tangent theorem into a reusable threshold certificate generator.

### Milestone 4: quotient-floor theorem

**Exit criterion.**

For every smooth \(H\) and slack \(\sigma\), the tangent and quotient-periodic floors are:

```text
explicit
necessary
computable
included in both lower and upper theorem statements
```

### Milestone 5: aperiodic local-limit theorem

**Exit criterion.**

\[
\#\{\text{aperiodic bad slopes}\}
\le n^{1+o(1)}
\]

or an explicit \(n^B\) version, after quotient floors are removed.

### Milestone 6: explicit threshold theorem

**Exit criterion.**

Given

```text
C
rho
n
q
H
epsilon* = 2^-128
```

the theorem outputs

```text
sigma_C^*
```

or a one-step endpoint interval with matching lower and upper bounds.

### Milestone 7: peer-review package

**Exit criterion.**

```text
main paper
certificate repository
independent verifier
review/audit notes
formalized finite gates
clear relation to the Proximity Prize
```

---

## 8. Risk register

### Risk 1: strict264 slot model does not yield seven slopes

**Impact.** The clean \(a=264\) finite obstruction fails in its current form.

**Mitigation.**

```text
try alternative beta
try alternative endpoint
try alternative two-ended jet family
try three-ended constraints
use F1 non-slot search
switch to nearby field with favorable q_line
```

### Risk 2: the 52.7B count is not replayable

**Impact.** The strongest public row remains source-scoped and weak for review.

**Mitigation.**

```text
produce corrected smaller count if needed
prefer seven-slope strict264 proof
write exact failure audit
```

### Risk 3: agreement-265 upper bound is false

**Impact.** Threshold is lower/higher than expected; finite pinning target changes.

**Current status.** This risk has materialized for the finite-slope
support-wise predicate: the coset-packet finite-slope floor gives more than six
bad finite slopes for every agreement \(265\le a\le288\), and hence pushes the
first possible finite-slope upper edge to at least \(288/289\).  See
`experimental/notes/thresholds/agreement265_status_audit.md`.

**Mitigation.**

```text
record the agreement-265 witness status as settled for finite slopes
do not attempt LD_sw(C,265) <= 6 under the finite-slope convention
if no different sampler convention is intended, move the next finite-slope
upper-bound target to a=289
keep staircase approach
```

### Risk 4: aperiodic local-limit theorem needs larger slack

**Impact.** Corrected reserve may be larger than expected.

**Mitigation.**

```text
make constants explicit
accept larger sigma if threshold can still be computed
separate finite small-n verification from asymptotic theorem
```

### Risk 5: subfield confinement deflates witnesses

**Impact.** Some extension-field lower bounds vanish under the intended sampler.

**Mitigation.**

```text
maintain q_gen/q_line/q_chal ledger
classify B-valued vs F-valued lines
construct genuinely F-valued witnesses
```

---

## 9. Non-claims and forbidden shortcuts

Do not claim any of the following unless separately proved.

```text
protocol soundness failure
ordinary list-decoding lower bound
full delta_C^* from a one-sided obstruction
base-field sampler result from extension-field data
no-slack smooth RCA/MCA theorem
interleaved-list theorem without L1 higher-agreement input
```

Do not do any of the following.

```text
Do not count supports when the quantity is slopes.
Do not report pre-deduplication counts.
Do not omit noncontainment.
Do not hide endpoint conventions.
Do not use q_gen, q_line, q_chal interchangeably.
Do not treat quotient-periodic mass as negligible.
Do not publish a huge count without replayable certificate.
```

---

## 10. Recommended immediate sequence

The shortest credible path toward the prize is:

```text
1. Freeze definitions and field ledgers.
2. Finish the official-definition audit for the finite-row theorem.
3. Keep the F_17^32 pure-MCA scanner output replayable.
4. Package the a=506/507 row as a finite threshold note/paper.
5. Promote the row-independent high-agreement threshold compiler theorem.
6. Use the compiler to mark the solved high-agreement region of the prize envelope.
7. Audit the projective-slope and no-loss CA variants with their denominators.
8. Keep strict264/strict352 as lower-agreement mechanism records.
9. Generalize beyond the compiler range via quotient/residue-line local limits.
10. Prove the aperiodic local-limit theorem with explicit constants.
```

The main finite slogan:

\[
\boxed{
LD_{\mathrm{sw}}(C,506)=7
\quad\text{and}\quad
LD_{\mathrm{sw}}(C,507)=6.
}
\]

The main theoretical slogan:

\[
\boxed{
\text{slack}+\text{quotient floors}+\text{aperiodic local limit}
\Rightarrow
\text{threshold theorem}.
}
\]

The main collaboration slogan:

\[
\boxed{
\text{Every claim must be replayable, field-ledgered, endpoint-explicit, and floor-separated.}
}
\]

---

## 11. Agent handoff prompt

Use the following prompt when handing this plan to a coding/proof agent.

```text
You are contributing to the RS-MCA path toward the full Proximity Prize.
Read towards-prize.md and the required sources listed at the top.

Core rules:
- Smooth no-slack RCA/MCA is false; work with slack.
- Always print q_gen, q_line, q_chal.
- Always state agreement a, slack sigma, radius delta, and endpoint convention.
- Separate quotient-periodic floors from aperiodic mass.
- Never count supports as slopes.
- Never report pre-deduplication counts.
- Never omit noncontainment.
- Prefer small replayable certificates over huge unverified counts.

Pick exactly one work package from Section 6.
Before coding or proving, restate:
1. the target theorem or artifact;
2. the exact parameters;
3. the acceptance test;
4. the non-claims.

Then produce either:
- a certificate,
- a verifier,
- a proof note,
- a branch ledger,
- or a failure audit with exact reasons.

Do not claim full prize progress unless your output moves one of the numbered milestones.
```

---

## 12. Current top priority

The top priority is:

\[
\boxed{
\textbf{finite-row threshold packaging and compiler theorem}
}
\]

Specifically, for

\[
C=\mathrm{RS}[\mathbb F_{17^{32}},H,256],
\quad n=512,
\quad k=256,
\quad \rho=1/2,
\]

the current theorem is:

\[
LD_{\mathrm{sw}}(C,a)=513-a
\qquad(a\ge427),
\]

so

\[
LD_{\mathrm{sw}}(C,506)=7,
\qquad
LD_{\mathrm{sw}}(C,507)=6.
\]

The deliverables are:

- definition audit against the official MCA sampler and endpoint convention;
- finite-row note/paper with scanner output attached;
- row-independent compiler theorem using
  \[
  B_Q=\lfloor Q/2^{128}\rfloor,\qquad r=n-a;
  \]
- a clear statement that if \(B_Q\le\lfloor(n-k)/3\rfloor\), then the single line/MCA grid threshold is pinned exactly at \(r=B_Q\).

The strict264 seven-slope certificate remains a useful lower-agreement experiment, but it is no longer the top priority for threshold determination.
