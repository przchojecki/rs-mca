# M1 Exact Target v0: Primitive Quotient-Normal Slope Packing

Status: CONJECTURAL / FALSIFICATION-FIRST / PROOF-PROGRAM.

Date: 2026-06-28.

Agent/model: Codex acting autonomously through AllenGrahamHart.

## Purpose

This note records a concrete M1 target suggested by the reductions in
`m1_boundary_off_external_anchor_normal_form.md`.  The point is to separate
all exact quotient-periodic support mass first, then ask for a polynomial bound
only on the quotient-normal primitive slope remainder.

This is not a proof of M1.  It is a proposed theorem-shaped target and a
counterexample-first protocol.  A counterexample should be useful: it must
produce many noncontained slopes whose agreement supports are all
stabilizer-primitive, after the tangent, contained, quotient-periodic,
presentation, reciprocal, and finite-domain alias identifications have been
charged.

## Setup

Let `F=F_q`, let `H <= F^*` be cyclic of order `n`, and let

```text
C = RS[F,H,k]
```

be the Reed-Solomon code of evaluations of polynomials of degree `<k`.
Write

```text
r=n-k,        a=k+t=n-j,        0<=t<=r.
```

For a word pair `(f,g):H->F`, define the finite support-wise noncontained
rank-one slope ledger

```text
Bad_nc(f,g,a)
 = { lambda in F :
     exists A in C and S subset H, |S|=a, such that
       A+lambda(-g)=f on S,
       not( (-g)|_S in RS[F,S,k] and f|_S in RS[F,S,k] ) }.
```

The exact-size threshold is harmless: by the threshold truncation argument
used in Corollaries 40.110--40.111, any noncontained witness on at least `a`
points has a noncontained `a`-subsupport.

For `lambda in Bad_nc(f,g,a)`, let

```text
Wit_lambda(f,g,a)
 = { S subset H : |S|=a and lambda has a noncontained witness on S }.
```

For a support `S subset H`, define its exact cyclic stabilizer

```text
Stab(S) = { h in H : hS=S }.
```

Now split the slope ledger into an exact quotient-periodic part and a
primitive remainder:

```text
Per_M1(f,g,a)
 = { lambda in Bad_nc(f,g,a) :
       exists S in Wit_lambda(f,g,a) with |Stab(S)|>1 },

Prim_M1(f,g,a)
 = Bad_nc(f,g,a) \ Per_M1(f,g,a).
```

Thus a slope is put into the periodic budget as soon as it has one
noncontained witness with nontrivial support stabilizer.  The primitive
remainder consists of slopes for which every noncontained `a`-witness support
has trivial stabilizer.

Define the exact M1 quotient-support budget of the line to be

```text
M1QuotBudget(f,g,a)=|Per_M1(f,g,a)|.
```

This is an exact support-stabilizer budget, not an asymptotic estimate.

## Conjectural M1-v0 Form

Fix a rate window `rho in (0,1)`, a polynomial field-size exponent `C_q`, and
an entropy slack `epsilon>0`.  There should be constants

```text
B=B(rho,C_q,epsilon),        C_0=C_0(rho,C_q,epsilon)
```

such that the following holds for every smooth cyclic sequence of domains
`H_n <= F_q^*` with `|H_n|=n`, `q<=n^C_q`, and

```text
k=rho n+O(1),
a=k+t,
t log_2(q) >= (1+epsilon) log_2 binom(n,a),
t >= C_0 n/log n.
```

For every line `(f,g):H_n->F_q`,

```text
|Prim_M1(f,g,a)| <= n^B.                           (M1-v0)
```

Equivalently,

```text
|Bad_nc(f,g,a)| <= M1QuotBudget(f,g,a) + n^B.       (M1-v0-ledger)
```

This is deliberately phrased as a primitive-remainder statement.  Large
quotient-periodic slope families do not refute this form; they belong to the
explicit quotient-support budget.  A refutation must produce a reserve-cleared
line with super-polynomially many slopes whose noncontained witnesses are all
stabilizer-primitive.

## Why This Would Close M1

The M1 residue-line local limit asks for polynomial control of support-wise
MCA bad slopes after the corrected reserve charges.  The reductions in
`m1_boundary_off_external_anchor_normal_form.md` separate the following
sources from the actual slope ledger:

1. contained and tangent branches;
2. nonprimitive residue presentations;
3. fixed-class coefficient multiplicity;
4. domain-root and root-free multiplier certificate multiplicity;
5. finite-domain divided-evaluation aliases;
6. global-codeword quotient gauges;
7. reciprocal `Qg`/`Qf` double counting away from the zero slope.

After these identifications, every surviving finite noncontained slope is
counted once in the quotient-normal rank-one ledger `Bad_nc(f,g,a)`.  If the
exact quotient-periodic support budget is charged by the Paper B reserve and
(M1-v0) supplies the polynomial primitive remainder, then the remaining
all-line M1 residue-packing contribution is polynomial.  Thus (M1-v0), plus
the existing quotient-periodic reserve ledger, is intended to be strong enough
to close the M1 local-limit route.

## Endpoint-Hankel Form Of The Same Target

Corollaries 40.166--40.168 give a second, more algebraic view of the same
target.  Rank-one coefficient sets are invariant under adding global
codewords to the direction and target:

```text
Mu_{phi+c}^{nc,>=a}(Y+d)=Mu_phi^{nc,>=a}(Y),        c,d in C.
```

The nonzero `Qg` and reciprocal `Qf` endpoint charts glue by inversion:

```text
Mu_{-g}^{x,nc,>=a}(f) <-> Mu_{-f}^{x,nc,>=a}(g),
lambda |-> lambda^{-1}.
```

Finally, a root-free denominator `Q` of degree `e<=r` presents the endpoint
quotient class `[-y] in F^H/C` exactly when

```text
Qy in RS[F,H,k+e],
```

or equivalently, with `w=Syn(y)`,

```text
H_{r-e,e}(w)Q=0.
```

Therefore a proof of (M1-v0) should not count raw denominator presentations or
reciprocal charts.  It should count quotient-normal endpoint Hankel-kernel
packets attached to primitive support witnesses, after quotient-periodic
support packets have been charged.

## First Falsification Pass

The following attacks do not prove the conjecture, but they remove several
ways a proposed counterexample could be spurious.

### 1. Presentation multiplicity is not a counterexample

If many primitive triples `(Q,B,w)` have the same divided evaluation datum
`(B/Q,w/Q)` on `H`, they define the same rank-one coefficient set.  This is
Corollary 40.165.  Such a family may be interesting denominator geometry, but
it does not by itself create many slopes.

### 2. Global quotient gauges are not a counterexample

If a line becomes large only after replacing an endpoint by endpoint plus a
global codeword, then it has not produced a new slope ledger.  Corollary
40.166 shows that rank-one noncontained coefficient sets depend only on
classes in `F^H/C`.

### 3. Reciprocal endpoint charts are not independent

If the same nonzero slopes appear in the `Qg` and `Qf` standard branches, this
is expected.  Corollary 40.167 identifies those branches by reciprocal
inversion.  A counterexample must be counted once projectively, with the
original zero slope checked separately.

### 4. Endpoint denominators are concrete kernels

A large denominator family must be visible as many root-free solutions of

```text
H_{r-e,e}(Syn(y))Q=0
```

for one of the endpoint words `y=f,g`.  Corollary 40.168 turns this into a
scanner-ready Hankel-kernel problem.  If the corresponding supports have
nontrivial cyclic stabilizer, the slopes are charged to `M1QuotBudget`; if
not, they are genuine candidates against (M1-v0).

### 5. What would refute v0

A useful refutation is therefore a sequence of smooth cyclic domains and
lines `(f_n,g_n)` satisfying the reserve guard for which

```text
|Prim_M1(f_n,g_n,a_n)| > n^B
```

for every fixed `B` along an infinite subsequence, or a finite family with a
clear mechanism forcing such growth.  The refutation must certify that the
large slope family is not explained by nontrivial support stabilizers,
reciprocal double counting, quotient gauges, or finite-domain presentation
aliases.

## Scanner Contract

A direct falsification scanner for this target should enumerate quotient
classes, not raw endpoint words.  For a small cyclic domain it should:

1. choose representatives for `F^H/C`;
2. enumerate quotient-normal pairs `(phi,Y)`;
3. compute `Bad_nc` from exact `a`-support witnesses;
4. split each slope by the stabilizers of all noncontained witness supports;
5. report `|Per_M1|`, `|Prim_M1|`, and the endpoint Hankel-kernel
   denominators from Corollary 40.168.

The first useful alert is not a large periodic packet.  It is a large
primitive packet whose supports all have trivial stabilizer after quotient
normalization.
