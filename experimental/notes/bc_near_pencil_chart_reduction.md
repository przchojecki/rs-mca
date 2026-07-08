# Near-pencil balanced-core charts: two structure lemmas, a reduction to
# a split-in-subspace locator census, and the q^-(t-1) residual
# calibration

- **Status:** two PROVED elementary structure lemmas + one PROVED
  reduction lemma (proofs inline, one page total), the reduction
  MACHINE-VERIFIED as an exact bijection on toy rows, and the residual
  density CALIBRATED on a 16x q-ladder. This packet does NOT prove
  row-sharp Q, and it does NOT close prob:saturated-bc; it discharges
  one named chart family (pairs near an exact pencil) into the grammar
  that problem asks for: a slope bound for the hard-wired part plus an
  explicitly named residual cell.
- **Script:** `experimental/scripts/verify_bc_near_pencil_reduction.py`
  (exact arithmetic, both sides of the bijection, about one minute,
  single process, small memory).
- **Data:** `experimental/data/bc_near_pencil_reduction.json`.

## 1. The chart family and where it sits in prob:saturated-bc

rem:bc-status-after-moving-root leaves a structural audit: every
residual balanced-core chart must be a paid type, present a
one-parameter locator pencil for cor:bc-one-pencil, or (prob:saturated-bc
type (b)) be a higher-dimensional coefficient family explicitly split
into such pencils or assigned to a named residual cell with a slope
bound. The natural first family to audit is the neighborhood of the
pencil cell itself: pairs (u, v) that are exact pencil pairs perturbed
in at most 2r coordinates,

    u = c0 + z0*w0 + du,   v = w0 + dv,

with c0, w0 codewords (deg < k), du, dv supported on R_u, R_v,
R = R_u u R_v, |R| <= 2r. These are the charts adjacent to the paid
quotient/pencil mass, and any slope census that first-matches tangent
and quotient cells must say what the leftover perturbed-pencil slopes
can do. Everything below is stated for a live triple (z, c, S):
agreement |S| = A = k + t between u + z*v and a codeword c, with the
validity condition that v restricted to S is not a degree-<k codeword
restriction (the invalid channel belongs to the raw census only; on the
saturated-ray side it carries no new parameters). Write
c' = c - (c0 + (z0 + z) w0), a codeword.

Field ledger for this note: the toy rows are prime fields
(q in {73, 193, 577, 1153}), D = the order-n multiplicative subgroup,
n = 24, k = 12, t = A - k = 3. All statements and proofs are
field-agnostic, but the residual-density law of Section 4 counts
value-field linear conditions; at deployed base-domain rows it must be
read in the generated field (ground rule 2), not blanket q_chal.

## 2. Two structure lemmas (proved)

**Support lemma.** Every live support S that is not tangent-charged
satisfies |S ∩ R| >= t + 1.

*Proof.* At an unperturbed x the coincidence c(x) = u(x) + z v(x) reads
c'(x) = 0. If c' = 0 identically, the aligned codeword is the pencil
member itself, with agreement >= n - |R|; at consumer-window rows that
exceeds A, so this mass is tangent-column mass and is charged by first
match. If c' != 0 it has at most k - 1 roots, so
|S ∩ (D \ R)| <= k - 1, i.e. |S ∩ R| >= A - (k-1) = t + 1. QED

**Validity lemma.** Every VALID live support meets R_v.

*Proof.* If S ∩ R_v is empty then v|_S = w0|_S is the restriction of a
degree-<k codeword, so the interpolant of v on S has vanishing top
coefficient block: the triple is invalid. QED

The validity lemma is load-bearing exactly where the chart is most
dangerous: on v-unperturbed supports the coincidence system below
becomes z-free and EVERY slope would go live simultaneously (a raw
support-locator census cannot see this; the slope census must).

## 3. The reduction lemma (proved): the chart is one-parameter after
## T-pinning, and its residual is a split-in-subspace census

Fix T ⊆ R with |T| = s >= t + 1, put D' = D \ R, and let
L(z) = [du|_T + z * dv|_T] be the projective line traced in P(F^T).
For supports at stratum s = |S ∩ R| (support lemma: s >= t + 1), write
Z = S ∩ D', |Z| = A - s.

**Reduction lemma.** Live triples (z, c, S) at stratum s biject (up to
the measure-zero degeneracies listed below) with polynomials

    c' != 0,  deg c' <= k - 1,  c' = ell_Z * g with deg g <= s - t - 1,
    [c'|_T] on the line L,

where ell_Z is the monic split locator with root set Z. The slope z is
read off the projective class [c'|_T] in L, injectively (dv not
identically zero on T and the delta-tuples non-proportional). At the
base stratum s = t + 1 (g constant) this says: hits correspond exactly
to COMPLETELY-SPLIT-over-D' polynomials of degree k - 1 lying in the
explicit codimension-(t-1) subspace

    V_T = eval_T^{-1}( span(du|_T, dv|_T) ) ,

and higher strata are the partially-split members of the same subspace
family. Excluded degeneracies: c'|_T = 0 (the common-root branch) and
[c'|_T] = [dv|_T] (the z = infinity direction).

*Proof.* Forward: on S the coincidence says c' vanishes on Z, so
ell_Z | c', and on T it says c'(x) = du(x) + z dv(x), which is the
statement [c'|_T] in L with parameter z. Backward: given such a c', set
c = c0 + (z0 + z) w0 + c', read z off [c'|_T]; the T-equations and the
Z-roots reproduce agreement on S = Z u T. Root-set <-> monic-locator is
the standard bijection; injectivity of the slope readout is the
non-proportionality of (du|_T, dv|_T). QED

In the grammar of prob:saturated-bc: after T-pinning the chart presents
a one-parameter projective family (the line L), with the slope, not the
raw support, as the counted parameter; the higher-dimensional residual
is not a new object but the split-members census of the explicit
subspace family {V_T}. Both halves of type (b) are therefore met for
this family: the hard-wired part is split into pinned one-parameter
pieces, and the remainder is a NAMED cell (split-in-subspace census)
with a slope bound.

**Uniform overdetermination.** At every stratum s the T-system has s
equations in (s - t) + 1 unknowns (g, z): overdetermination exactly
t - 1, independent of s. So one density condition controls all strata
at once, and the full mining mass is

    sum_s C(2r, s) * C(n - 2r, A - s) * q_v^-(t-1)   ~   C(n, A) * q_v^-(t-1)

up to the small ratio of the split-binomial to the full binomial (q_v =
the value field of the condition count, see the ledger note above).
This is the same first-moment bookkeeping as the entropy ledger: the
residual cell is sub-mean exactly when the row window is.

## 4. Machine verification and the q^-(t-1) calibration

The verifier enumerates the FULL Z-space (C(20,11) = 167,960 sets per
trial, exact arithmetic) on both sides of the bijection with identical
RNG streams: side 1 solves the T-coincidence system for (gamma, z) and
verifies every hit end-to-end (the agreement set contains S; validity;
both structure lemmas); side 2 tests only membership of ell_Z in V_T
with the z = infinity direction removed — no slope solving. Five trials
per row, r-perturbation at |T| = t + 1 = 4 with du, dv nonzero on all
of T:

    (n,q)       predicted C(20,11)/q^2   valid hits per trial   side-2
    (24,73)     31.5                     27,25,29,33,37         match
    (24,193)    4.51                     2,4,5,4,7              match
    (24,577)    0.50                     0,0,0,0,2              (side 1 only)
    (24,1153)   0.13                     0,0,0,1,0              (side 1 only)

Findings: (i) side 1 == side 2 on every trial, before AND after the
validity filter — the reduction lemma verified digit-for-digit; (ii)
the residual obeys the q^-(t-1) mean law across a 16x q-ladder; (iii)
zero structure-lemma violations on any hit; (iv) every count is far
below the hard-wired slope budget C(2r, t+1) = C(8,4) = 70 even at the
mean-scale row. These numbers were first produced on independent cloud
runs (2026-07-07); the script asserts them digit-for-digit.

## 5. The resulting charge line for this chart family

For a pair within joint distance 2r of an exact pencil pair, at a row
whose window makes the mining mean sub-unit:

    N_slopes(u, v)  <=  C(2r, t+1)                    PAID_BY_THEOREM
                                          (support + validity + pinning)
                     +  split-in-subspace residual    CONDITIONAL_ON_NAMED_INPUT

The named input is a split-in-subspace census bound of mean order:
count <= max(1, mean) * poly(n) for the codim-(t-1) subspaces V_T over
the generated field. Given that input, the residual dies by the window
arithmetic of Section 3 and the near-pencil chart contributes only the
finitely many slopes the adversary can hard-wire through (t+1)-subsets
of the perturbed set.

## 6. What this does and does not settle

It settles the STRUCTURE half for one chart family: near-pencil charts
are not a higher-dimensional mystery cell; they are pinned
one-parameter families plus an explicitly named split-in-subspace
residual, with the danger channel (the z-free v-unperturbed branch)
provably dead by validity.

It does NOT settle the census half. The mean-order split-in-subspace
count is a worst-instance anti-concentration statement of the same
class as row-sharp Q (def:q-row-atom) and the split-pencil censuses:
character/moment routes hit the moment-order floor
(prop:q-moment-order-floor), and we record honestly that the elementary
exchange recursion we tried — m*N(m, W) <= C(n', m-1) + n'*N(m-1, W_2),
with W_2 the one-shift deepening of the annihilator — unrolls to a
poly-below-total bound only and cannot see the window. No sharp census
claim is made here.

It also does not audit far-from-pencil charts; this packet is one named
family out of the decomposition prob:saturated-bc asks for.

## What to do next

If useful, the same two lemmas + reduction should be replayed at an
MCA-route adjacent row shape (K = k + 1) and folded into the chart
inventory of the finite BC audit; the split-in-subspace residual cell
should be tracked as a single named input shared with the Q/BC frontier
rather than re-derived per chart.
