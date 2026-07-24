---
workboard_item: M1
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: "For the same p=2^31-1, quotient-domain size 1022, support size 479, and depth 32 as the pinned M31 quotient problem, an explicit two-puncture comparison domain has one locator-prefix fiber of size 145422675. This exceeds 8 B_star and 40 times the ceiling ambient average 3614120."
architecture: DIRECT_COMPARABLE_DOMAIN_OBSTRUCTION
partition_digest: "N/A; comparison-domain support theorem, no deployed owner atom banked"
atom_or_cell: Q / domain-agnostic prefix-flatness obstruction
quantifier: "There exists one explicit 1022-point domain D in F_p and one exact first-32 locator target whose 479-subset fiber has at least 145422675 members."
projection_and_unit: "479-subsets per first-32 nonleading locator-coefficient target; support-level only"
claimed_bound: "Assume p=2147483647, g=7 is primitive, zeta=g^((p-1)/33) has exact order 33, C_i={g^i zeta^j:0<=j<33} for 0<=i<=30 are disjoint, D is their union plus g^31 with g^30 and g^31 removed, R={g^30 zeta^j:1<=j<=17}, and E_S=R union the C_i for a 14-subset S of {0,...,29}. Then every E_S is a 479-subset of D with one common first-32 locator prefix, so max_eta N_D(eta) >= binomial(30,14)=145422675 > 8*16777215 and > 40*3614120."
status: PROVED
impact: ROUTE_CUT
scope_labels: COUNTEREXAMPLE_TO_DOMAIN_AGNOSTIC_FLATNESS / LOCAL_ONLY
falsifier: "Failure of p primality, the primitive-root gates, 33-coset disjointness, the two-puncture domain size, support size 479, the degree-446 tail bound, the common 32-prefix, or any exact integer comparison."
replay: "python3 experimental/scripts/verify_m31_flatness_keystone_constant_shift_obstruction.py --check; python3 experimental/scripts/verify_m31_flatness_keystone_constant_shift_obstruction.py --tamper-selftest"
---

# M31 flatness keystone: a same-parameter constant-shift obstruction

## Status

```text
PROVED comparison-domain theorem
COUNTEREXAMPLE to parameter-only max/average control
DEPLOYED CHEBYSHEV DOMAIN still open
row ledger movement 0
```

The pinned M31 quotient problem asks for the maximum depth-32 prefix-fiber
count on 479-subsets of one particular punctured 1,022-point Chebyshev quotient
domain. Its ceiling ambient average is

\[
 \left\lceil \binom{1022}{479}/p^{32}\right\rceil=3{,}614{,}120,
 \qquad p=2^{31}-1,
\]

while the row budget is

\[
 B_*=16{,}777{,}215.
\]

This packet does **not** decide that Chebyshev maximum. It proves a sharp scope
obstruction: the numerical tuple `(p,1022,479,32)` and its exact average cannot
possibly imply the desired maximum bound. On an explicit two-puncture domain
over the same field, one depth-32 fiber has

\[
 \binom{30}{14}=145{,}422{,}675
\]

members. Exactly,

\[
145{,}422{,}675-8B_*=11{,}204{,}955>0
\]

and

\[
145{,}422{,}675-40\cdot3{,}614{,}120=857{,}875>0.
\]

Thus any successful maximum-versus-average theorem for the deployed row must
use a Chebyshev-specific hypothesis strong enough to exclude or pay
constant-shift block packets just beyond the Newton wall. Average, field size,
domain size, support size, and prefix depth alone are insufficient.

The active source labels for the deployed object are `def:primitive-q`,
`def:q-row-atom`, `prop:q-exact-target`, and `lem:newton-equivalence` in
`experimental/grande_finale.tex`. The integrated T64/T16 packet
`experimental/notes/thresholds/m31_quotient_band_swap_census_t16_mixing.md`
already proves the actual-domain constant-shift family and off-lattice mixing
witness. They are cited here and not rebuilt.

## 1. General hidden-block lemma

Let `F` be a field. Let `H(X)` be monic of degree `d`, and suppose
`C_1,...,C_m` are pairwise disjoint `d`-point subsets of `F` with monic
locators

\[
 V_{C_i}(X)=H(X)-\lambda_i.
\]

Fix a core `R` disjoint from all blocks, with `|R|=r`. For every `t`-subset
`S` of the block indices put

\[
 E_S=R\sqcup\bigsqcup_{i\in S}C_i,
 \qquad |E_S|=r+td.
\]

### Proposition 1 — constant-shift blocks are invisible below their degree

If the observed locator-prefix depth is `R_0<d`, then all `E_S` with `|S|=t`
have the same first `R_0` nonleading locator coefficients. Consequently one
prefix fiber contains at least `binomial(m,t)` supports.

**Proof.** Write

\[
 P_S(Z)=\prod_{i\in S}(Z-\lambda_i).
\]

Then

\[
 V_{E_S}(X)=V_R(X)P_S(H(X)).
\]

The leading term is `V_R(X)H(X)^t`. Every term depending on at least one
`lambda_i` loses at least `d` degrees. Therefore the first `d-1` nonleading
coefficients are independent of `S`, and hence so are the first `R_0<d`.
Distinct block selections give distinct supports because the blocks are
disjoint. `square`

The threshold is sharp for this argument: when `d=R_0`, the first varying
constant-shift term enters exactly at the last observed coefficient. The
minimal automatically hidden block size at depth 32 is therefore 33.

## 2. Explicit same-parameter specialization

Set

\[
 p=2{,}147{,}483{,}647,
 \qquad p-1=2\cdot3^2\cdot7\cdot11\cdot31\cdot151\cdot331.
\]

The verifier proves that `p` is prime and that `g=7` is primitive modulo `p`.
Since `33` divides `p-1`, put

\[
 h=(p-1)/33=65{,}075{,}262,
 \qquad \zeta=g^h=392{,}483{,}048\pmod p.
\]

The element `zeta` has exact order 33. For `0<=i<=30`, define the 33-point
multiplicative coset

\[
 C_i=\{g^i\zeta^j:0\le j<33\}.
\]

These 31 cosets are pairwise disjoint, and

\[
 V_{C_i}(X)=X^{33}-g^{33i}.
\]

To mirror the deployed punctured size, first form a 1,024-point base domain by
adjoining the sentinel `g^31` to the 1,023-point union of the 31 cosets. Remove

\[
 g^{30}=470{,}211{,}272
 \quad\text{and}\quad
 g^{31}=1{,}143{,}995{,}257.
\]

The resulting domain `D_33` has exactly 1,022 points. The blocks
`C_0,...,C_29` remain intact; `C_30` has 32 surviving points.

Choose the fixed 17-point core

\[
 R=\{g^{30}\zeta^j:1\le j\le17\}
 \subset C_{30}\setminus\{g^{30}\}.
\]

For every 14-subset `S` of `{0,...,29}`, define

\[
 E_S=R\sqcup\bigsqcup_{i\in S}C_i.
\]

Then

\[
 |E_S|=17+14\cdot33=479.
\]

Its locator is

\[
 V_{E_S}(X)=V_R(X)\prod_{i\in S}(X^{33}-g^{33i}).
\]

The block product is `X^462` plus terms of degree at most `429`. Therefore

\[
 V_{E_S}(X)=V_R(X)X^{462}+\text{terms of degree at most }446.
\]

Since every locator has degree 479, its coefficients in degrees 478 through
447 — exactly the first 32 nonleading coefficients — are independent of `S`.
The certified common prefix is

```text
1215687628, 1435194305, 1189382414, 516405159,
794701406, 450986238, 958054454, 1430706965,
1042506499, 1785889575, 1165387368, 856711928,
625832911, 2051593259, 1072257538, 514588560,
2091952626, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0
```

All `binomial(30,14)=145422675` block selections are distinct. Hence this is
one explicit depth-32 fiber of that size.

## 3. Exact max-versus-average consequence

The ambient target count depends only on the field and depth:

\[
 p^{32}=
41855804344513474996659235398101492226513356497450298740932889847998693318143069882098996132602011303952349637025722282585533160693229396196872386718816372844518146497415885223313922264348563527038409009746582412510577609691239404142296725925022012935690228019787759005225367255740944911962461962241.
\]

The total number of 479-subsets is

\[
\binom{1022}{479}=
151271865290567282756670209927671126612573718499984279646030908205795367378645973832177793165136706631573210771619584252500710632400169112681192055348722412206290242750426752087291990702755284787532455089499756167113798752793361036534746315185930511714934550247772523231121741961638844402219522161141316000.
\]

Exact division gives floor average `3614119`, nonzero remainder, and ceiling
average `3614120`. The M31 budget lies strictly between four and five ceiling
averages:

```text
B* - 4*ceil_average = 2320735
5*ceil_average - B* = 1293385
```

By contrast, the explicit comparison-domain fiber exceeds forty ceiling
averages and eight budgets. Therefore the following universal statement is
false:

> For every 1,022-point domain in `F_p`, every depth-32 locator-prefix fiber on
> 479-subsets is at most `B*`, or even at most forty times the ceiling ambient
> average.

The obstruction is not a low-moment heuristic. It is an exact split-locator
family at the minimal hidden degree `32+1`.

## 4. What this proves about the open keystone

This packet rules out a whole proof interface, not the deployed row:

1. A maximum bound cannot be obtained from the exact average and the four
   numerical parameters alone.
2. A theorem uniform over arbitrary 1,022-point base-field domains is false by
   more than eight budget factors.
3. Any valid M31 theorem must use actual Chebyshev-domain geometry to rule out,
   classify, or pay all degree-above-prefix constant-shift packets and their
   residual analogues.

The integrated actual-domain constant-shift family shows that this mechanism is
not artificial: hidden blocks already occur there, but its certified family
remains below budget. What remains unknown is whether the deployed Chebyshev
domain admits a different packet, mixing family, or residual mechanism capable
of comparable amplification, or instead has a domain-specific flatness theorem.

A parameter-only or generic-domain flatness argument is therefore dead. The
missing input that would revive the route is an explicit Chebyshev-specific
structural theorem excluding any hidden-block packing large enough to cross
`B*`, together with control of non-block residual fibers.

## 5. Validation and nonclaims

Run:

```text
python3 experimental/scripts/verify_m31_flatness_keystone_constant_shift_obstruction.py --check
python3 -O experimental/scripts/verify_m31_flatness_keystone_constant_shift_obstruction.py --check
python3 experimental/scripts/verify_m31_flatness_keystone_constant_shift_obstruction.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_flatness_keystone_constant_shift_obstruction.py --tamper-selftest
```

The verifier is deterministic and uses only the Python standard library. It
proves primality by trial division, checks the primitive-root factor gates,
constructs all 1,024 base-domain points, checks the two punctures, verifies all
33-point root blocks, directly multiplies two degree-479 support locators,
recomputes the common prefix, and replays every exact integer above. Python is
replay; the proof is the displayed locator-degree argument.

The stdlib-only Lean package
`experimental/lean/m31_alt_domain_fiber/` kernel-checks the exact parameter
identities, the degree boundary `446<447`, `binomial(30,14)=145422675`, the
full `binomial(1022,479)/p^32` division, and every printed budget margin. Its
six declared results each carry a `#print axioms` census. All six use
`native_decide` only for closed natural-number computations; the package
contains no `axiom`, `sorry`, `admit`, or Mathlib dependency. The symbolic
constant-shift polynomial proof and finite-field construction remain the
source theorem and deterministic replay boundary, as recorded in
`experimental/lean/m31_alt_domain_fiber/CORRESPONDENCE.md`.

Explicit nonclaims:

- no upper or lower maximum-fiber theorem for the deployed Chebyshev quotient;
- no received word, codeword, first-match survivor, or row-global list
  counterexample;
- no proof that the actual T64/T16 census is exhaustive;
- no row closure, endpoint movement, or bankable `U_Q` atom;
- no dependence on `agents.md`, `PR_BODY.md`, or any agents-log entry during
  `--check`.

# COUNTEREXAMPLE_TO_DOMAIN_AGNOSTIC_FLATNESS
