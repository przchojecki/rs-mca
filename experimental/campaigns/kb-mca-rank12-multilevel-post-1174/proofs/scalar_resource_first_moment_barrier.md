# Scalar margin-resource / first-moment barrier

## Statement

At the initial KoalaBear rank-twelve row let

\[
N=B_*-2d+1=274980728111260144,
\qquad (n,m)=(2R,R+d),
\]

and let

\[
C=C_{11}(R)=3313389801746721900417.
\]

Assume only that every selected record has raw support margin
\(r_\gamma\ge1\), truncated margin
\(\theta_\gamma=\min\{d+1,r_\gamma\}\), total resource

\[
\sum_\gamma\theta_\gamma\le C,
\]

and pair-core incidence \(|S_\gamma\cap H_\gamma|=m-r_\gamma\).
Then these scalar constraints and coordinate averaging can force a child of
size at most

\[
120205662451376300,
\]

which is short of the rank-ten target
\(248706399341288370\) by

\[
128500736889912070.
\]

This is a sharp barrier for the declared scalar relaxation.  A cyclic
balanced-incidence construction realizes the displayed maximum coordinate
load inside that relaxation.  It is not a Reed--Solomon counterexample and
not a lower bound on an actual family.

There is also a selected-support first-moment obstruction.  Even if every
one of the \(N\) records were granted all \(m\) selected-support core
incidences, coordinate averaging would force only

\[
\left\lceil\frac{Nm}{n}\right\rceil
=146337362121160346,
\]

still \(102369037220128024\) below the child target.  Thus no theorem whose
only output is one coordinate heavy by averaging the selected-support core
incidences can close the rank-twelve row, regardless of how it layers
margins.  A successful theorem must force concentration beyond the average
using complete-core or cross-core realization.

## Exact optimizer

Give every record its mandatory baseline \(\theta=1\), using \(N\) resource
units and guaranteeing \(m-1\) core incidences.  A record with
\(\theta\le d\) has \(r=\theta\), so an extra resource unit can remove only
one guaranteed core incidence.  Promoting a record from \(\theta=1\) to the
capped class \(\theta=d+1\) costs \(d\) additional units, while its raw
margin may become \(m\) and remove all \(m-1\) core incidences.  Since
\((m-1)/d>1\), every minimizer promotes as many records as possible before
spending resource inside the uncapped class.

Thus

\[
H=\left\lfloor\frac{C-N}{d}\right\rfloor
 =49103551414195675,
\]

and the residual resource is

\[
q=C-N-Hd=56673.
\]

The minimizing abstract histogram has:

- \(H\) capped records with raw margin \(m\) and zero core incidence;
- one uncapped record with margin \(1+q\);
- \(N-H-1\) records with margin one.

Its total core incidence is exactly

\[
(N-H)(m-1)-q
=252089545421228709377370.
\]

Coordinate averaging therefore guarantees only its ceiling after division
by \(n=2097152\), namely \(120205662451376300\).

This average is sharp within the scalar relaxation.  List the required
incidence units record by record, and give a record of incidence size \(s_i\)
the next \(s_i\) distinct residues in one cyclic traversal of the \(n\)
coordinates.  Since every \(s_i\le n\), no record repeats a coordinate, and
every coordinate receives either the floor or ceiling of the total
incidence divided by \(n\).

## Adding the known per-pair constraints still does not close

For a margin-one minimizing pair, the exception sets belonging to distinct
slopes are disjoint.  Hence one fixed pair owns at most

\[
n-(m-1)=R-d+1=981105
\]

records.  The \(N-H-1=225877176697064468\) margin-one records therefore
need only

\[
\left\lceil
\frac{225877176697064468}{981105}
\right\rceil
=230227321946
\]

distinct pair types.  The proved sub-square interleaving cap at (s=11),
margin one, is

\[
Q_{11}(1)=
\left\lfloor
\frac{\binom{R+11}{11}}{\binom{d-1+11}{11}}
\right\rfloor
=12761830235484.
\]

The required type count is smaller by (12531602913538), and
\(Q_{11}(1)^2<|\mathbb F|=(2130706433)^6\).  Thus the full package of total
margin resource, first core moment, fixed-pair exception disjointness, and
the current pair-type cap still permits the abstract over-budget packing.
This is stronger than the first-moment barrier alone, but it remains a
certificate-class no-go rather than a realizable RS counterexample.

## Consequence for the maximal attack

Neither another single cutoff nor an arbitrary scalar repackaging of the
proved nonuniform resource can produce the missing rank-ten child.  A valid
rank-twelve theorem must use information discarded by this relaxation:
cross-pair realizability, intersections among minimizing pair cores,
support-exception collisions, a source-bound circuit/Segre compiler, or a
chronology-compatible owner.

The older locator/four-block chain cannot be activated merely by feeding it
this first moment: it begins only after a rank-two family of size
\(5170912\) has already been produced, and #1174 supplies no such rank-twelve
descent.

## Verification boundary

`verify_kb_mca_rank12_scalar_resource_barrier_v1.py` recomputes all integers,
constructs the extremal abstract histogram, and rejects eight hostile unit
or scope mutations.  It also proves that the actual-line gluing quotient's
rank-zero branch is paid by
\[
981104+\left\lfloor\frac{C-981104}{67473}\right\rfloor
=49106899082787469,
\]
with slack \(199599500258500901\) to the rank-ten child target.  The
certificate deliberately records
`abstract_histogram_claimed_rs_realizable=false` and
`active_v4_ledger_movement=0`.
