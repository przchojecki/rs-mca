# C9 literal-interface counterexample and corrected proof boundary

**Status:** `COUNTEREXAMPLE_NEW_FLOOR` for the literal quantitative
`def:primitive-leaf` interface; `SPECIFICATION_BLOCKER` for the intended
smooth-row C1--C8 residual.

This is an adversarial interface audit, not a counterexample to the intended
smooth Reed--Solomon theorem.  The explicit data printed in
`experimental/asymptotic_rs_mca.tex`, `def:primitive-leaf`, admit a sequence
for which the image-normalized C9 moment has positive exponential rate.  The
additional phrase "surviving C1--C8" is not currently an evaluable predicate
on `(T,m,K,rho,Omega^circ,Phi)`.  Consequently, the current C9 input has two
readings:

1. under the displayed quantitative data alone, it is false;
2. under the intended C1--C8 complement, it is not yet a standalone theorem
   until that complement is specified exactly.

The packet also proves that C9 is equivalent to primitive Q at positive
exponential scale and gives a genuine positive range through zero-error
two-list recovery.

## 1. C9 is equivalent to primitive Q at exponential scale

For `F subset {0,1}^N`, let

\[
E(F)=\#\{(a,b,c,d)\in F^4:a-b=c-d\},
\qquad
\Delta(F)=E(F)/|F|^3,
\]

with differences taken in `Z^N`, as in the compact paper's Boolean
additive-combinatorics section.

Assume the quantitative BSG theorem used there: if

\[
E(F)\ge |F|^3/K,
\]

then some `F' subset F` satisfies

\[
|F'|\ge K^{-C}|F|,
\qquad
|F'-F'|\le K^C|F'|
\]

for an absolute constant `C`.  Also use the printed Boolean quasicube bound

\[
|A-A|\ge |A|^{3/2}.
\]

### Lemma 1: positive-rate Boolean families enter a fixed Sidon cut

If `|F| >= exp(cN)` and, contrary to the claim,

\[
\Delta(F)\ge \exp(-\sigma N),
\]

take `K=exp(sigma N)`.  BSG and quasicube growth give

\[
|F'|\ge \exp((c-C\sigma)N),
\qquad
|F'|\le \exp(2C\sigma N).
\]

For `sigma=c/(4C)`, the first bound is `exp(3cN/4)` and the second
is `exp(cN/2)`, a contradiction.  Hence

\[
|F|\ge \exp(cN)
\quad\Longrightarrow\quad
\Delta(F)<\exp\left(-\frac{c}{4C}N\right).
\]

### Proposition 2: C9 if and only if primitive Q

Let a frontier Boolean leaf have image size `L`, active-family size `M`,
average image-fiber size `barN=M/L`, and fibers `F_s`.  Primitive Q is

\[
\max_s |F_s|\le \exp(o(N))\bar N.
\]

The image-normalized C9 assertion is, for every fixed `sigma>0` and every
logarithmic `q=q_N -> infinity`,

\[
L^{-1}\sum_{\Delta(F_s)\le\exp(-\sigma N)}
\left(\frac{|F_s|}{\bar N}\right)^q
\le \exp(o(Nq)).
\]

Primitive Q implies C9 by replacing every summand by the maximum.

Conversely, if primitive Q fails, then along a subsequence there are
`eta>0` and a fiber with

\[
|F_s|\ge \exp(\eta N)\bar N\ge\exp(\eta N),
\]

because `barN>=1`.  Lemma 1 puts that fiber in the fixed cut
`sigma=eta/(4C)`.  Its contribution is at least

\[
L^{-1}\exp(\eta Nq).
\]

Since `L<=M<=2^N`, `log L=O(N)=o(Nq)`, contradicting C9.  Thus, for the
printed frontier Boolean objects,

\[
\boxed{\text{C9}\iff\text{primitive Q}.}
\]

This explains why signed-kernel, inverse Littlewood--Offord, entropy-cap,
logarithmic-moment, and local rank-collapse formulations kept returning the
same missing theorem.  The Sidon qualifier does not remove the
positive-exponential max-fiber obstruction.

## 2. Counterexample to the literal quantitative interface

Let `k -> infinity` through multiples of five and set

\[
N=4k,
\qquad m=2k,
\qquad R=2,
\qquad Q=100k+1.
\]

For `0<=i<k`, put

\[
a_i=Q^i,
\qquad
T_i=\{a_i,a_i+1,a_i+2,a_i+3\},
\qquad
T=\bigsqcup_i T_i.
\]

Let `S_tot=sum_{t in T} t` and choose a prime `p>2S_tot`.  Work in
`K=F_p`, set `rho(t)=1`, and use

\[
v_t=(1,t),
\qquad
\Phi(x)=\left(|x|,\sum_{t\in T}x_tt\right).
\]

All subset sums lie in `[0,S_tot]`, so equality modulo `p` is equivalent to
integer equality.  The points of `T` are distinct in `F_p`.

### 2.1 One exponential fiber

In block `i`, define

\[
P_i^0=\{a_i,a_i+3\},
\qquad
P_i^1=\{a_i+1,a_i+2\}.
\]

Both choices have cardinality two and sum `2a_i+3`.  Therefore

\[
F=\left\{\bigcup_iP_i^{\epsilon_i}:\epsilon\in\{0,1\}^k\right\}
\]

is one `Phi`-fiber in the weight-`m` slice, and `|F|=2^k`.

### 2.2 Exponentially many singleton image fibers

Let `C_k` be the words in `{0,1,2,3,4}^k` having exactly `k/5` occurrences
of every digit.  Then

\[
A_k:=|C_k|=\frac{k!}{(k/5)!^5}
=\exp(k\log 5-O(\log k)),
\qquad
\sum_i c_i=2k.
\]

For `c in C_k`, define

\[
G_c=\bigcup_i\{a_i,a_i+1,\ldots,a_i+c_i-1\}.
\]

Its second image coordinate is

\[
S(c)=\sum_i\left(c_iQ^i+\frac{c_i(c_i-1)}2\right).
\]

For distinct `c,d`, take the largest index `j` where they differ.  Balanced
words cannot differ in only one coordinate, so `j>=1`.  The leading term has
absolute value at least `Q^j`; the lower base-`Q` terms have absolute value at
most `4 sum_{i<j}Q^i`, and the correction terms have absolute value at most
`6(j+1)`.  Since `Q=100k+1`, the leading term dominates.  Hence all `S(c)`
are distinct.  For the same reason, comparison with the blockwise heavy sum
`sum_i(2Q^i+3)` is nonzero: a balanced word is not the constant word `2`, its
largest non-`2` index is at least one, and the leading base-`Q` term dominates
the lower terms and the `O(k)` correction.  Thus no filler has the heavy
image.  The support families are disjoint.

Set

\[
\Omega^\circ=F\cup\{G_c:c\in C_k\}.
\]

Then

\[
L=A_k+1,
\qquad
M=A_k+2^k,
\qquad
\bar N=\frac{M}{L}
=1+\frac{2^k-1}{A_k+1}=1+o(1).
\]

Thus `log barN=o(N)`.  This construction satisfies the displayed finite-set,
fixed-density, field, nonzero-weight, weighted-Vandermonde, subset-of-slice,
image-normalization, and frontier requirements.  It does not claim to satisfy
an unprinted C1--C8 survival predicate.

### 2.3 Exact additive energy

Each local two-point choice set has difference multiplicities `2,1,1`, so
its energy is `6`.  The block coordinates are disjoint, hence

\[
E(F)=6^k,
\qquad
\Delta(F)=\frac{6^k}{(2^k)^3}
=\left(\frac34\right)^k
=\exp\left(-\frac{\log(4/3)}4N\right).
\]

Fix `0<sigma<log(4/3)/4` and take `q_N=ceil(log N)`.  The heavy fiber lies
in the C9 cut and contributes

\[
\mathcal G^{\rm Sid}_{q,\sigma}
\ge L^{-1}\left(\frac{2^k}{\bar N}\right)^q.
\]

Using `log L=k log 5+O(log k)`, `log barN=o(1)`, and `N=4k`,

\[
\frac{1}{Nq}\log\mathcal G^{\rm Sid}_{q,\sigma}
\longrightarrow\frac{\log2}{4}>0.
\]

Therefore the C9 bound `exp(o(Nq))` fails under the literal quantitative
interface.

## 3. Scope of the counterexample

The construction has visible block and trade structure.  An exact future C3,
C6, C7, or C8 predicate may classify and delete it.  It also uses `R=2`, a
rapidly growing field, and a domain that is not asserted to be one of the
intended smooth multiplicative or circle-type rows.

Those facts do not invalidate the interface audit: none is excluded by the
displayed algebraic data in `def:primitive-leaf`.  They do limit the conclusion.
This packet does **not** refute:

- C9 for the intended smooth-domain row sequences;
- C9 under `R asymp N`;
- C9 after exact C1--C8 predicates and quantitative negations are printed;
- the conditional compiler theorem in `experimental/asymptotic_rs_mca.tex`.

Instead it proves that the phrase "surviving C1--C8" carries indispensable
mathematical content and cannot remain an informal qualifier in a standalone
C9 theorem.

## 4. A positive theorem from zero-error two-list recovery

Let `H` be the `R x N` weighted Vandermonde matrix with columns `v_t`.  Fix
`x_0 in F_s` and put

\[
D_s=\{x-x_0:x\in F_s\}\subseteq\ker H.
\]

Because every `R` columns are independent, `ker H` is an
`[N,N-R,R+1]` MDS code.  At coordinate `t`, every word in `D_s` belongs to
the two-symbol set `{-x_{0,t},1-x_{0,t}}`.  Thus `|F_s|` is a zero-error
list-recovery list with input-list size two.

Let `J=|F_s|`.  Every pair of distinct codewords agrees in at most
`N-R-1` coordinates.  At each coordinate, splitting `J` words between at
most two symbols gives at least `J^2/4-J/2` agreeing unordered pairs.  Hence

\[
N\left(\frac{J^2}{4}-\frac J2\right)
\le \binom J2(N-R-1).
\]

If `2R+2>N`, then

\[
\boxed{J\le\frac{2(R+1)}{2R+2-N}.}
\]

In particular, `R/N>=1/2+epsilon` gives `J=O_epsilon(1)` and proves C9
pointwise.

The fixed-weight condition gives another exact pair count.  If `a_t` of the
`J` supports contain coordinate `t`, then

\[
(R+1)\binom J2
\le\sum_t a_t(J-a_t)
\le\frac{J^2m(N-m)}N.
\]

Writing `D=R+1` and `B=2m(N-m)/N`, if `D>B` then

\[
\boxed{J\le\frac{D}{D-B}.}
\]

Thus bounded fibers also follow uniformly when

\[
\frac RN>2\frac mN\left(1-\frac mN\right)+\epsilon.
\]

Recent discrete Brascamp--Lieb work proves strong zero-error list-recovery
bounds for random Reed--Solomon codes and explicit folded or multiplicity
codes.  It does not automatically cover every ordinary smooth GRS row here,
but it identifies a clean corrected target: prove zero-error two-list recovery
with list size `exp(o(N))` uniformly on the exact C1--C8 residual.

## 5. Required specification repair

A valid standalone C9 theorem must print at least:

1. the quantitative range of `R/N`;
2. the allowed smooth domains, weights, characteristics, and field conventions;
3. the exact first-match operation producing `Omega^circ`;
4. exact C1--C8 predicates, thresholds, and quantitative negations;
5. a proof that `Omega^circ` is their complement;
6. uniformity over the required frontier windows;
7. an independent minor-arc condition, such as a zero-error list-recovery,
   subspace-design, or summable Fourier partition-function estimate.

"Primitive" must not be defined by the absence of a positive-rate Sidon-heavy
fiber, because Proposition 2 would make that definition circular.

The strongest honest status is therefore:

```text
COUNTEREXAMPLE_NEW_FLOOR for the literal quantitative interface.
SPECIFICATION_BLOCKER for the intended smooth-row C9 theorem.
```

## 6. Replay and provenance

Run:

```bash
python experimental/scripts/verify_c9_literal_interface_counterexample_v1.py --check
python experimental/scripts/verify_c9_literal_interface_counterexample_v1.py --tamper-selftest
python experimental/scripts/verify_c9_literal_interface_counterexample_v1.py --k 5 --brute-energy
```

The verifier checks the fixed-weight condition, heavy image collision, filler
image separation, no-wrap field threshold, exact energy `6^k`, Sidon cutoff,
and positive finite normalized C9 lower bound.  The note's asymptotic family
proof supplies the limiting rate `log(2)/4`.

Primary repo context:

- `experimental/asymptotic_rs_mca.tex`, labels `def:primitive-leaf`,
  `def:sidon-paid`, `ass:image-normalized-sidon-input`, `thm:bsg`,
  `thm:quasicube`, and `thm:primitive-q`;
- `experimental/grande_finale.tex`, the primitive entropy-inverse problem;
- PR #433, the missing C9 source audit;
- PR #439, the image-normalized B1 interface repair.

Related external source:

- J. Brakensiek, Y. Chen, M. Dhar, and Z. Zhang,
  [Combinatorial Bounds for List Recovery via Discrete Brascamp--Lieb
  Inequalities](https://arxiv.org/abs/2510.13775), 2025.
