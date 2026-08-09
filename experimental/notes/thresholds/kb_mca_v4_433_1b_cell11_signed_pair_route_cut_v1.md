```yaml
proof_status: EXPERIMENTAL_REVIEW_REQUIRED
proof_status_reason: exact local factorization and witness; fresh independent mathematical review is still required
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
direct_statement: the 433-1a cell-11 guard factorization does not transplant to the exact 433-1b compact tower; a quadratic residual and a guarded deployed signed-pair point survive
architecture: K3 coordinate-positive 433-1b source-role workboard
atom_or_cell: source-role cell 11
quantifier: the exact guarded common locus in the declared source-sign chart epsilon=(-1,-1), pivot 1
claimed_bound: route cut only; no witness-count or ledger improvement
status: COUNTEREXAMPLE_NEW_FLOOR
impact: LOCAL_ROUTE_CORRECTION
```

## Statement audited:

On the exact `c_row=5` compact tower from the predecessor packet, form the
complete necessary signed-pair equations

\[
 P=n_1d_0+n_0d_1,
\]

and

\[
 S=k^2w_0(1-w_0)^2d_1^2-k^2w_1(1-w_1)^2d_0^2
   -4n_0d_0d_1^2.
\]

Their resultant in `w1` has degree 16 and factors exactly in the tower as

\[
 \operatorname{Res}_{w_1}(P,S)
 =N_0D_0^5(w_0-t^2)(w_0+1)Q_2(w_0),
\]

where `Q2` has degree two.  In particular, the 433-1a candidate

\[
 N_0D_0^5(w_0-t^2)^2(w_0-r^2)(w_0+r^2)
\]

is not proportional to the 433-1b resultant.  The quadratic discriminant has
square norm in `F_p(r)` but is not itself a square in the declared degree-four
tower.  A deterministic deployed-field scan finds the guarded point

```text
r  =  976487466    t  = 1814604652
b  = 1722399428    c  =  463843441
w0 =   58144935    w1 = 1833131373
N0 = 1242524170    D0 =  796444780
```

at which both `P` and `S` are zero modulo `2130706433`.

This is a counterexample to the proposed 433-1a factor transplant and to an
empty residual conclusion from those guards.  It is not a counterexample to
the KoalaBear theorem, not an MCA witness, and not a proof that the residual
cannot be paid by a different owner or count.

## Files/sections read:

- `experimental/notes/thresholds/kb_mca_v4_433_1b_cell11_compact_tower_v1.md`.
- The predecessor compact-tower replayer, verifier, and JSON certificate.
- The public 433-1a cell-11 plane/kernel and signed-pair factorization programs,
  proof, audit, and frontier records.
- The public 433-1b common Vieta compiler at its source-bound commit.
- Gilles Villard's primary-source papers on bivariate elimination over finite
  fields: [JSC 1997](https://perso.ens-lyon.fr/gilles.villard/BIBLIOGRAPHIE/PDF/jsc24.pdf)
  and [ISSAC 2023](https://perso.ens-lyon.fr/gilles.villard/BIBLIOGRAPHIE/PDF/vil23.pdf).
- Wolfram documentation for
  [Resultant](https://reference.wolfram.com/language/ref/Resultant),
  [PolynomialReduce](https://reference.wolfram.com/language/ref/PolynomialReduce),
  and [finite fields](https://reference.wolfram.com/language/guide/FiniteFields).

## Dependencies:

- **IMPORTED / source-bound:** the predecessor's three exact towers, empty
  deployed leading boundaries, primitive coefficient kernel, and public 433-1b
  Vieta definitions.
- **PROVEN by exact local computation:** the tower substitution, degree-16
  resultant, exact extracted factorization, factor multiplicities, and
  nonsquare status of the quadratic discriminant in the nested tower.
- **PROVEN by an independent source-expression replay:** the displayed point
  satisfies the three tower equations, all declared source guards, label
  distinctness, `N0,D0 != 0`, B1 opposition, and both signed-pair equations.
- **INDEPENDENT SYMBOLIC CONTROL:** Wolfram `PolynomialReduce` returns zero for
  the generic quadratic-extension square-root reconstruction identity and
  confirms the separate trace-zero formula used by the exact nonsquare test.
- **UNPROVEN:** payment of the residual quadratic cover, all-source-sign
  transport, outside-role transport, labeled add-back, affine-slope projection,
  and any v4 ledger consequence.
- **UNVERIFIED:** a fresh reviewer has not yet approved the factorization or
  its interpretation.  The generator cannot bless its own calculation.

## Parameter dependence:

The result is finite and specific to `F_2130706433`, cell 11, source sign
`(-1,-1)`, pivot 1, and the declared compact tower.  It has no dependence on
`T`, `Y`, `L`, `L_barI`, `lambda`, `I`, or an asymptotic or dyadic parameter.

## Layer-cake / dyadic summability:

Not applicable.  No level-set integration or additive dyadic error occurs.

## Moment / Markov / Chebyshev:

Not applicable.  No moment inequality or probabilistic tail bound is used.

## Edge cases / notation:

The computation does not silently invert tower leading coefficients: those
boundaries are inherited from and checked by the predecessor packet.  The
resultant's leading specialization remains separate from the existence of the
displayed regular point.  The scan explicitly excludes the source guard,
`N0=0`, `D0=0`, source labels, zero new labels, and `w0=w1`.  Resultants can
carry leading-specialization artifacts, which is why the direct point replay
is load-bearing rather than the resultant alone.

The nested-square test includes both norm signs and the trace-zero exceptional
case in each quadratic extension.  A square total norm is only necessary, not
sufficient; here the total norm is square while the tower element is not.

## Numerical evidence:

The factorization and witness checks use exact finite-field arithmetic, not
floating point.  The deterministic scan used seed `43311`, stopped after four
`r` values, visited five tower points, found two residual roots, and found one
fully guarded signed-pair point.  The point itself is a proof of nonemptiness
for this local incidence.  The small stopping index is not evidence for an
asymptotic density or a global witness count.

## Verdict:

**YELLOW — COUNTEREXAMPLE_NEW_FLOOR.**  The exact witness rigorously blocks the
433-1a guard transplant as a cell-11 closure.  The cell remains open because a
different paid owner or a budget-fitting count of the quadratic cover may
still exist.  No global theorem or ledger movement is authorized.

## Remaining risks:

The load-bearing resultant factorization and tower nonsquare classification
need a fresh mathematical reviewer.  Sage 10.9 could reconstruct the tower but
its built-in function-field factorization delegated to a multivariate
factorizer that does not support this prime above `2^29`; that failed
independent-tool route is recorded here rather than treated as evidence.
The witness certifies the signed-pair incidence only, not every downstream
projection and add-back condition in the 433-1b proof chain.

## Minimal next action:

Freeze `Q2` as a new explicit residual owner candidate and compute the exact
degree/genus and rational-point projection of the corresponding signed-pair
cover, including leading and denominator fibers.  The maximal useful outcome
is either a budget-fitting count routed into v4 chronology or a proof that the
cover supplies a genuine unpaid primitive family.  Do not attempt another
guard-only factorization or claim cell-11 closure from the 433-1a pattern.
