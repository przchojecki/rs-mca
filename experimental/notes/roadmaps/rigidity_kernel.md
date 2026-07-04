# The Rigidity Kernel (RK) — the one statement four problems consume

- **Status:** AUDIT / synthesis. The program's remaining mathematics,
  isolated. Everything here is a consolidation of proved results and
  named conjectures already in the DAG; RK itself is a CONJECTURE
  schema whose instances the four open faces consume.

## The kernel

**RK (rigidity kernel, schema).** Fix a row RS[F, D, k] on a 2-power
coset domain, a scale M in the quotient lattice of n (multiplicative
divisors AND dihedral composites), and an FM-suppressed operating
point (agreement/deficiency level where n^B x FM(instance) < the
integer allowance). Then every *agreement object* at that point —
an aligned support, a deeply-agreeing codeword, a rank-deficient
configuration, a concurrency point of evaluation traces — either

  (i)  lies in the PAID TAXONOMY: tangent/deep-divisor, multiplicative
       pullback g(X^M'), dihedral pullback X^e g(X^M' + X^-M'), or
       extension-type; or
  (ii) belongs to a primitive remainder of size <= n^{B_RK} x FM,
       uniformly in the fixed word/pair (WORST case), jointly across
       isotypic components.

"FM(instance)" is the instance's own first-moment scale; jointness
means the bound multiplies correctly across characters (per #212's
product structure).

## The four consumption maps

```text
FACE 1 (GAP-1 / Conjecture TR):   RK at the QUOTIENT ROWS.
  Each per-character set A_r is a same-rate quotient-row instance at
  scale n/M; TR = RK's clause (ii) + jointness there. Consumes axes:
  worst-case + general t + cross-character jointness; scale small.

FACE 2 (Conjecture F residue):    RK for EVALUATION FLATS.
  Descent (proved) reduces any flat to leaves; the leaves' D_j-point
  counts = RK's agreement objects (concurrency points). The 4-branch
  strip is clause (i); the leaf bound is clause (ii). Consumes axes:
  dimension growth + worst case; radius benign.

FACE 3 (spread classification):   RK for RANK-LOSS CONFIGURATIONS.
  Below-cap exceptions = agreement objects in design space; the
  observed classes (AG/net, v-degenerate, syzygy circuits) are the
  taxonomy's trace there. Consumes axes: worst case + configuration
  geometry; counts q-suppressed (locus density, provable-staged).

FACE 4 (clean-rate exclusion):    RK PER-PAIR at the BASE ROW.
  Post-audit form: no pair carries s+1 unpaid deep bad slopes at the
  decision point. Multiplicity s+1 forces support overlaps (pigeon-
  hole at corridor sizes), overlaps force words on intersections
  (two-slope, proved), forced words must land in clause (i). Consumes
  axes: corridor RADIUS + worst case; dimension benign.
```

## What is PROVED of RK (the instance table)

```text
radius <= (1-rho)/3, base row, 2-branch taxonomy:  thm:deep-mca (v12)
radius <= (1-rho)/2 via CA import:                 v12 pincer
flats, dim 1:                                      n/j voting bound
flats, dim 2:                                      pair bound + twins
flats, fixed dim d:                                n^{O(d)} lattice bd
MDS-dual flats (any dim):                          trivial lattice
average case (all radii, all s):                   the pair ledger
                                                   c(s,t) (moments)
t = 2, one exchange, local:                        #152 residual bound
cross-character reduction:                         #212 tower product
top-core cap => globalness (conditional):          the double count
```

## The frontier axes (why the faces differ in difficulty)

RK's proved instances sit in a box; each face needs an excursion
along different axes:

```text
axis R (radius):      third-distance -> corridor   [face 4's burden]
axis D (dimension):   fixed d -> growing d          [face 2's burden]
axis Q (quantifier):  average -> worst-case         [all faces]
axis T (deficiency):  t = 2 local -> general t      [faces 1, 4]
axis J (jointness):   single -> cross-character     [face 1's burden]
```

The average->worst-case axis (Q) is shared by every face and is
where the singleton/exceptional-pair phenomenon lives: RK is an
INVERSE/rigidity statement (excess forces membership), not a counting
statement — rare-but-existing exceptional objects must be classified,
not bounded away.

## Consequences of isolating RK

1. Any technique that moves axis Q at one face likely moves it at
   all four (the objects differ; the exceptional-classification
   problem is the same).
2. The dihedral discovery enlarged clause (i) for ALL faces at once —
   as taxonomy events always will.
3. The step-zero budget audit (xr_target_budget_audit) determines
   whether face 4 needs RK at multiplicity 1 (rigidity) or s+1
   (forcing) — materially different excursion lengths on axis R.
4. Partial RK instances are individually creditable: each proved
   box-excursion closes specific rows/consumers (per the maps above).
```
