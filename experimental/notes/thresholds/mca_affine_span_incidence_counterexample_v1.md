---
workboard_item: T
row: "RS[GF(1009), {0,...,99}, 1]"
object: MCA
target_epsilon: not applicable; field-general theorem counterexample
agreement: 21
B_star: "23 (the refuted theorem's claimed bound)"
direct_statement: "the affine-span transverse MCA compiler is false under its printed direction-separation hypothesis"
architecture: DIRECT
partition_digest: not applicable
atom_or_cell: affine-span MCA rank compiler used in K3
quantifier: one explicit received line and 31 distinct affine slopes
projection_and_unit: distinct bad slopes on one received line
claimed_bound: "31 > 23"
status: COUNTEREXAMPLE
impact: ARCHITECTURE_ROUTE_CUT
---

# Affine-span MCA incidence counterexample v1

## Result

The affine-span transverse MCA compiler in
`experimental/grande_finale.tex`, formerly labelled
`thm:affine-span-mca`, is false even under its printed direction-separation
hypothesis.

Over `F=GF(1009)`, take

```text
D={0,...,99},
C=RS[F,D,1],
(n,K,m,w,s)=(100,1,21,20,1).
```

There is one received line with 31 distinct selected slopes such that:

1. the selected explanations lie in the one-dimensional constant code;
2. every selected maximal agreement support has size exactly 21;
3. every such support is same-support pair-noncontained;
4. `max_(c in C) agr(r_1,c)=20<21=m`; and
5. the theorem's two terms both floor to 23.

Thus `31>23` refutes the theorem.

## Construction

Partition the domain into

```text
C0={0,...,19}, E={20,...,49}, T={50,...,70}, W={71,...,99}.
```

Put `(r_0,r_1)=(0,0)` on `C0`.  On the `i`-th point of `E`, for
`1<=i<=30`, put

```text
(r_0,r_1)=(-i^2,i).
```

For each slope `i`, select the zero codeword.  It agrees exactly on the
20-point core and the `i`-th point of `E`.

On `T`, put `r_0=1` and choose 21 distinct fresh nonzero direction values
avoiding `1+i r_1=0` for all `1<=i<=30`.  At slope zero, select the constant
one codeword.  It agrees exactly on `T`.

On `W`, choose fresh direction values and choose each base value outside

```text
{0,1} union {-i r_1:1<=i<=30}.
```

The field has ample room for every choice.  The verifier uses the first
legal value at each step, so the record is deterministic.

The direction values are zero 20 times and otherwise pairwise distinct.
Since the code consists of constants, its maximum codeword agreement is
exactly 20.  The direction-separation hypothesis therefore holds.

## Pair noncontainment

On a zero-explanation support, the 20 core coordinates force any simultaneous
constant explanation pair to be `(0,0)`, while the remaining coordinate has
nonzero direction value.  On `T`, the base is constant one but all 21
direction values are distinct.  No selected support is pair-contained.

## Claimed bound

At `s=1`, both terms in the compiler are

```text
floor(100*99/(21*20))=23.
```

The selected family has size 31.

## Proof gap

Direction separation does force the incident normals on each selected
support to span the two-dimensional parameter space.  It does not supply the
proper-subspace occupancy bound used to count incident ordered bases.

For a zero-explanation support, 20 normals lie on one line and only one is
transverse.  There are only `2*20=40` ordered bases, while the rejected proof
charges the support for

```text
m*w=21*20=420
```

ordered bases.  This is the exact failed step.

## Scope

The counterexample refutes the MCA affine-span compiler and every active-row
payment that uses its denominator.  It does not refute:

- the ordinary affine-span LIST compiler;
- common-core cancellation;
- the directional Johnson ray compiler;
- codeword-direction gauge equivalence;
- the selector-free all-LineRay error-affine-core set-pair theorem; or
- the target KoalaBear MCA inequality itself.

The distinction matters for the common-core PR stack: its fixed-core
codeword-affine-span payments inherit the refuted denominator, while its
separate all-LineRay payment through error affine rank three does not.

## Correct replacement

The proved replacement is `thm:proper-subspace-mca`.  For affine explanation
rank `s`, direction-coset support

```text
e=min_(b in C) wt(r_1-b),    t=n-m,    L=max(1,e-t),
```

it gives

```text
|Z| <= floor((1/L) max{
  n_fall_(s+1)/(m (w+1)_rise_(s-1)),
  (n-K+s)_fall_(s+1)/(w+1)_rise_s
}).
```

The factor `L` is the exact safe repair: pair noncontainment gives one final
transverse normal, while direction-coset distance can raise that count.  It
is not replaced by `w` without proof.

At the first common-core-shortened rows, the corrected compiler pays all
KoalaBear ranks through 9 and Mersenne rank 1 for every `e`.  Its next exact
support walls are

```text
KoalaBear q=10,11,12,13: e>=981108,981153,981861,992852;
Mersenne  q=2,3,4,5:     e>=981144,981363,984779,1037876.
```

The top ranks remain unpaid by this compiler.

## Replay

```bash
python3 experimental/verify_mca_affine_span_incidence_counterexample_v1.py
python3 experimental/verify_mca_affine_span_incidence_counterexample_v1_independent.py
python3 experimental/verify_mca_proper_subspace_occupancy_compiler_v1.py
```

Expected output:

```text
MCA_AFFINE_SPAN_INCIDENCE_COUNTEREXAMPLE_V1_PASS slopes=31 bound=23 direction_max=20 mutations=4/4
MCA_AFFINE_SPAN_INCIDENCE_COUNTEREXAMPLE_V1_INDEPENDENT_PASS slopes=31 support_checks=31 field_values=1009 bound=23
MCA_PROPER_SUBSPACE_OCCUPANCY_COMPILER_V1_PASS zero_normal_cases=616 adjacent=8 regression=471 toy_selections=540
```
