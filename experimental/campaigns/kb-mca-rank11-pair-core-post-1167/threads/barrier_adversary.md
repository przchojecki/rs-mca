# Barrier adversary: rank-eleven pair/core certificate ceiling

Date: 2026-08-13

Role: independent barrier checker / computational adversary

Status: **PASS as a route cut; FAIL as a rank-eleven payment**

## Scope and dependencies

The audited objects are actual post-near, same-support-pair-noncontained
records after the #1166/#1167 gauge.  There is one fixed complete record per
distinct affine slope, and its explanation lies in the fixed affine
ten-flat.  Counts below are slopes, never witnesses, pair labels, graph
vertices, or passports.

The audit uses:

1. the printed support-local threshold theorem from #1166;
2. the ordinary affine-span pair cap and the #1167 sub-square interleaving
   theorem;
3. exact fixed-pair core identities proved below;
4. for the stronger weighted conclusions only, the new nonuniform resource
   lemma
   \(\sum_\gamma\theta_\gamma\le C_s\).

Items 1--3 already give an unconditional certificate-class no-go.  Item 4
has a direct ordered-basis proof, but it is a new theorem and must pass an
independent statement/quantifier review before it is banked.

## Nonuniform theta resource

For explanation dimension \(s\), define

\[
C_s=\left\lfloor\max\left\{
 \frac{n^{\underline{s+1}}}{m(w+1)^{\overline{s-1}}},
 \frac{(n-K+s)^{\underline{s+1}}}{(w+1)^{\overline s}}
\right\}\right\rfloor.
\]

The printed minimum-margin theorem does not by itself imply a sum bound.
Instead rerun its ordered-normal-basis proof recordwise.  With the proof's
global zero-normal parameters \(z,g\), record \(\gamma\) owns at least

\[
 (m-g)\theta_\gamma (w+1)^{\overline{s-1}}
\]

ordered independent normal tuples.  One tuple determines at most one
parameter point, because its \(s+1\) independent normals determine that
point uniquely.  Summing before minimizing therefore gives

\[
 (m-g)(w+1)^{\overline{s-1}}
 \sum_\gamma\theta_\gamma
 \le (n-z)^{\underline{s+1}}.
\]

The source proof's same maximization over \(g\le z\) and
\(0\le z\le K-s\) has its maximum at \(g=z\) and an endpoint
\(z\in\{0,K-s\}\).  Hence

\[
 \sum_\gamma\theta_\gamma\le C_s. \tag{R}
\]

This proof uses one fixed affine flat and basis.  It does not sum bounds
obtained from separately re-gauged subfamilies.

## Correct fixed-pair and endpoint terminals

Put \(E=B_*-2w+1\).  At a legal cutoff
\(1\le\tau<w\), define

\[
 Q_s(\tau)=\left\lfloor
 \frac{\binom{n-K+s}{s}}{\binom{w-\tau+s}{s}}
 \right\rfloor,
 \qquad Q_s(\tau)^2<|\mathbb F|.
\]

For a low record set
\(\lambda_\gamma=\tau+1-\theta_\gamma\).  If a line is over budget,
(R) gives

\[
 W_\tau:=\sum_{\theta_\gamma\le\tau}\lambda_\gamma
 \ge (\tau+1)E-C_s. \tag{W}
\]

The interleaving theorem bounds the number of distinct ordered pair types by
\(Q_s(\tau)\).  Thus one **fixed pair**, not merely one endpoint, has
weighted parallel load at least

\[
 P_s(\tau)=
 \left\lceil\frac{\max\{0,(\tau+1)E-C_s\}}{Q_s(\tau)}\right\rceil.
 \tag{P}
\]

There is no factor two in (P).  A secondary bipartite endpoint average does
have denominator \(2Q_s(\tau)\), and produces a common-first- or
common-second-component ray terminal.  It is weaker than (P) but may feed a
different owner.

Exact all-cutoff optimization gives:

| error rank | \(s\) | fixed-pair weight | \(\tau\) | forced parallel records | \(\tau\) |
|---:|---:|---:|---:|---:|---:|
| 10 | 9 | 13,579,567,671 | 6,758 | 4,807,625 | 298 |
| 11 | 10 | 743,449,148 | 6,486 | 200,632 | 1,795 |
| 12 | 11 | 4,392,470 | 16,667 | 273 | 15,540 |

The secondary endpoint optima are:

| error rank | weighted endpoint degree | \(\tau\) | endpoint record degree | \(\tau\) |
|---:|---:|---:|---:|---:|
| 10 | 6,789,783,836 | 6,758 | 2,403,813 | 298 |
| 11 | 371,724,574 | 6,486 | 100,316 | 1,791 |
| 12 | 2,196,235 | 16,665 | 137 | 15,540 |

For rank eleven, maximizing fixed-pair weight forces core deficiency at
most eight.  Maximizing the number of parallel records forces at least
200,632 records and deficiency at most four.

## Exact fixed-pair core identity

For a selected minimizing pair \(e=(a,b)\), put

\[
 H_e=\{x:r_0(x)=a(x),\ r_1(x)=b(x)\},
 \qquad \delta_e=\max\{1,m-|H_e|\}.
\]

The record equation on \(S_\gamma\) is

\[
 (r_0-a)+\gamma(r_1-b)=0.
\]

Outside \(H_e\), the quantity \(r_1-b\) cannot vanish; otherwise the
record equation also forces \(r_0-a=0\).  Conversely, on
\(S_\gamma\cap H_e\), it vanishes.  Since the record is low,
\(\theta_\gamma\le\tau<w+1\), the truncation in the margin is inactive,
and the fixed selected minimizer satisfies

\[
 \theta_\gamma=|S_\gamma\setminus H_e|\ge\delta_e. \tag{C1}
\]

For two distinct slopes, their exception sets are disjoint: at a fixed
coordinate outside \(H_e\), the displayed affine equation determines at
most one slope.  Consequently a pair of deficiency \(\delta\) owns at most

\[
 c_\delta=left\lfloor\frac{n-m+\delta}{\delta}\right\rfloor \tag{C2}
\]

records.  These are exact actual-record statements; they do not assert
distinct graph neighbors.

## Unconditional and conditional LP ceilings

Let \(G(t)\) be the number of selected pair types with
\(\delta_e\le t\).  The pair agrees with the received pair on at least
\(m-t\) coordinates, so the interleaved list theorem gives
\(G(t)\le Q_s(t)\).  Since \(c_t\) decreases, Abel summation gives the
low ceiling

\[
 L(J)=Q_s(1)c_1+
 \sum_{t=2}^{J}(Q_s(t)-Q_s(t-1))c_t. \tag{L}
\]

Without using (R), the already printed threshold theorem gives

\[
 U_{\rm printed}(J)=2w+H_s(J+1)+L(J).
\]

The exact legal, sub-square scan has its minimum at \(J=19{,}737\):

\[
 U_{\rm printed}=813{,}929{,}118{,}931{,}913{,}384,
\]

which exceeds \(B_*\) by
\(538{,}948{,}390{,}820{,}518{,}297\).  This is the unconditional
certificate-class no-go.

Conditional on the independently reviewed resource lemma (R), each low
record of deficiency \(t\) costs at least \(t\) resource units and each
high record costs at least \(J+1\).  The exact integral relaxation fills
the available prefix-constrained low slots in increasing \(t\), then spends
the remaining resource on high records.  Its exact minimum occurs at
\(J=26{,}033\):

\[
\begin{aligned}
 Q_{10}(J)&=107{,}486{,}241{,}601{,}454,\\
 L_J&=811{,}957{,}734{,}614{,}064{,}312,\\
 R_J&=106{,}597{,}778{,}100{,}457{,}375{,}003,\\
 U_{\rm coupled}(J)&=811{,}958{,}533{,}186{,}703{,}629.
\end{aligned}
\]

This still exceeds \(B_*\) by
\(536{,}977{,}805{,}075{,}308{,}542\).  Thus the stronger weighted
compiler sharpens the no-go but does not approach payment.

The previously explored number
\(813{,}808{,}634{,}916{,}868{,}793\) used an unjustified altered
deficiency denominator/tail recurrence and is withdrawn.

## Negative control and its scope

The smallest singleton-exception star with a legal low cutoff has
\((n,K,m,w)=(6,1,3,2)\) over \(\mathbb F_7\).  Use a two-point core
with received pair \((0,0)\), and on each of the four remaining
coordinates put \((-\gamma,1)\) for one distinct slope \(\gamma\).
Each slope has exact support equal to the core plus its coordinate, is
same-support pair-noncontained, is strictly post-near, and maps to the
same low pair.  It attains four parallel records, equal to \(n-A\).

This control falsifies any inference from the visible local hypotheses to
distinct-neighbor expansion or a smaller fixed-pair multiplier.  It does
**not** realize KoalaBear affine error rank eleven and therefore does not
refute a rank-eleven theorem using additional cross-pair structure.

## Sharp certificate-class extremizer

At rank eleven and \(\tau=1\), the current numerical interfaces permit
\(Q_{10}(1)=821{,}289{,}819{,}491\) abstract pair types, each with the
sharp singleton-exception multiplicity \(981{,}105\).  The resulting
abstract count including the near add-back is

\[
 805{,}771{,}548{,}351{,}852{,}499,
\]

over budget by \(530{,}790{,}820{,}240{,}457{,}412\), while satisfying
the theta-resource and field-size inequalities.  This is a ceiling witness
for the declared certificate abstraction, not a claim that all stars are
simultaneously Reed--Solomon realizable.  Their simultaneous realizability
is exactly the missing cross-pair information.

## Weakest genuinely new missing theorem

The next theorem must couple **different actual minimizing pairs**.  A
usable form is:

> On the same actual received line and chronology slice, route every fixed
> minimizing pair with either deficiency at most eight and weighted load at
> least 743,449,148, or deficiency at most four and at least 200,632 records,
> to a named paid owner; alternatively prove an aggregate overlap/collision
> inequality across different dense cores that makes iterative removal fit
> the budget.

For the secondary ray lane, the corresponding common-endpoint terminal is
100,316 records.  Any owner must be chronology-disjoint under iteration.
A one-pair multiplier improvement, an ordinary distinct-neighbor theorem,
or another scalar threshold optimization is ruled out.

No rank-eleven payment, active-v4 ledger movement, or KoalaBear closure is
authorized.

## Reproducibility

- Main campaign replay:
  `experiments/verify_nonuniform_theta_pair_route_cut.py`.
- Independent adversarial arithmetic:
  `/private/tmp/rank11_weighted_barrier_fast.py` and
  `/private/tmp/rank11_core_deficiency_lp.py`.
- Finite-field control shipped with this campaign:
  `controls/gf7_parallel_star.sage`.
