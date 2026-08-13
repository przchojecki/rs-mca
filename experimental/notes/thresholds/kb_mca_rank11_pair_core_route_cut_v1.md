# KoalaBear rank-eleven pair-core route cut

Status: **PROVED LOCAL ROUTE CUT / ZERO DEPLOYED LEDGER MOVEMENT**

Exact parent: PR #1167 head
`491ccdf53d54846f5a013b808960645275c64ed3`.

This packet answers the next question left by the rank-ten
margin/interleaving payment.  It does not pay affine error rank eleven.
It proves the strongest actual fixed-pair terminal currently forced by the
support-local margin, interleaved pair cap, and exact pair-core geometry, and
then proves that the complete core-deficiency use of those inputs still
misses the KoalaBear budget.

## 1. Actual-record input

Use the intrinsic near deletion and exact post-deletion record selection of
PR #1166.  One complete record is fixed for every distinct post-near bad
affine slope before gauging or choosing a margin minimizer.  At error rank
eleven, the reversible gauge puts all explanations in an affine ten-flat
without changing the errors, slopes, supports, or same-support
pair-noncontainment.

For each record define

\[
 \theta_\gamma=\min\left\{w+1,
 \min_{b\in C'}|\{x\in S_\gamma:r_1(x)\ne b(x)\}|\right\}.
\]

Every selector and minimizer is fixed once.  Labels, pair types, supports,
and graph edges are never counted as slopes.

## 2. Nonuniform margin resource

The ordered-normal-basis proof of the support-transverse compiler can be
summed before replacing all final extension counts by their minimum.  It
gives

\[
 \sum_\gamma\theta_\gamma\le
 C_s=\left\lfloor\max\left\{
 \frac{n^{\underline{s+1}}}{m(w+1)^{\overline{s-1}}},
 \frac{(n-K+s)^{\underline{s+1}}}{(w+1)^{\overline s}}
 \right\}\right\rfloor.
\]

This is a new theorem, not a formal summation of the old minimum-margin
statement.  Each parameter point owns its own
`theta_gamma`-weighted collection of ordered normal bases; an independent
coordinate tuple determines at most one parameter point.  The zero-normal
endpoint maximization is exactly the one already proved in the repaired
compiler.

## 3. Fixed minimizing pairs

For a cutoff `tau`, every record with `theta_gamma <= tau` chooses a
minimizing direction `b_gamma` and

\[
 a_\gamma=h_\gamma-\gamma b_\gamma,
 \qquad \lambda_\gamma=\tau+1-\theta_\gamma.
\]

The pair agrees with the received pair on at least `m-tau` coordinates.
Ordinary affine-span plus the sub-square interleaving collapse gives at most

\[
 Q_s(\tau)=\left\lfloor
 \frac{\binom{n-K+s}{s}}{\binom{w-\tau+s}{s}}
 \right\rfloor
\]

distinct ordered pairs.  If an over-budget line leaves
`E=B_*-2w+1` post-near slopes, one fixed pair has weight at least

\[
 \left\lceil\frac{\max\{0,(\tau+1)E-C_s\}}{Q_s(\tau)}\right\rceil.
\]

There is no factor two: the interleaving theorem counts complete ordered
pairs.  A bipartite endpoint formulation has twice the total degree and
twice as many available endpoints and gives the same average.

For a fixed pair `(a,b)`, set

\[
 H_{a,b}=\{x:r_0=a,\ r_1=b\},
 \qquad \delta=\max\{1,m-|H_{a,b}|\}.
\]

On an assigned support, the margin is exactly
`|S_gamma \ H_ab|`.  These exception sets are disjoint across different
finite slopes, because an outside coordinate determines the slope by its
affine ratio.  Consequently the pair owns at most

\[
 c_\delta=\left\lfloor\frac{n-m+\delta}{\delta}\right\rfloor
\]

records and has cutoff weight at most
`c_delta (tau+1-delta)`.

## 4. Exact KoalaBear terminal

For

\[
 (n,K,m,w,B_*)=
 (2097152,1048576,1116048,67472,274980728111395087)
\]

over the deployed sextic field, every over-budget error-rank-eleven line
forces, for each row, a fixed actual pair satisfying that separately
optimized statement.  The fixed pairs supplied by the two rows need not
coincide:

| cutoff `tau` | fixed-pair weight | distinct owned slopes | deficiency |
|---:|---:|---:|---:|
| 6,486 | 743,449,148 | at least 114,624 | `delta <= 8` |
| 1,795 | 360,132,809 | at least 200,632 | `delta <= 4` |

The slope counts are parallel edge records, not distinct neighbors.  The
second row is the strongest record-load terminal; the first is the strongest
weighted-load terminal.

## 5. Complete declared-certificate-class wall

Fix one minimizing direction and hence one pair type for every selected
record once, before scanning the cutoff.  For each deficiency `delta`,
cumulative interleaving bounds the number of pair types by `Q_s(delta)`,
while one type owns at most `c_delta` records.
Since `c_delta` decreases, the exact greedy/Abel bound through cutoff `J` is

\[
 L(J)=Q_s(1)c_1+
 \sum_{\delta=2}^{J}
 (Q_s(\delta)-Q_s(\delta-1))c_\delta.
\]

Adding the printed high-margin tail and scanning every legal cutoff gives the
unique minimum

\[
\begin{aligned}
 J&=19737,\\
 U_{\rm high}&=5401690553097387,\\
 U_{\rm low}&=808527428378681053,\\
 U_{\rm total}&=813929118931913384,\\
 U_{\rm total}-B_*&=538948390820518297.
\end{aligned}
\]

Thus all cumulative pair-list caps, all core deficiencies, every exact
fixed-pair ratio fiber, and the printed high-margin theorem still miss by a
factor exceeding 2.9.  The stronger nonuniform resource can lower this
method ceiling, but its own exact optimizer also remains over budget; neither
route pays rank eleven.

## 6. Sharpness and missing theorem

A deterministic `GF(7)` constant-code star has exact size-three supports,
strict post-near distance, pair noncontainment, and four parallel slopes on
one fixed pair.  It is the smallest local countermodel to a distinct-neighbor
or reduced per-pair-multiplicity inference.  It is not an error-rank-eleven
example; it tests only that local implication.

The next theorem is therefore precise:

> Couple different fixed minimizing pairs on the identical actual received
> line, or route every dense parallel pair-core group chronology-correctly to
> an earlier owner.  It must handle the exact `delta <= 4`, `200632`-slope
> terminal above.

Another scalar threshold, one-pair ratio bound, or simple-graph expansion is
ruled out.  No active-v4 atom, S/A/E chronology, or KoalaBear closure is
claimed here.

## 7. External search

An Exa sweep covered 55 results around generic RS list decoding, higher-order
MDS intersections, simultaneous partial inverses, and combinatorial
cycle-space list-decoding arguments.  The most relevant primary sources were
Brakensiek--Gopi--Makam on generic RS list-decoding capacity, Yu--Loeliger on
simultaneous partial inverses, and Shangguan--Tamo on combinatorial
list-decoding.  None supplies the required worst-case same-line correlation
theorem on this special deployed evaluation domain.  No external lemma is
load-bearing in this packet.
