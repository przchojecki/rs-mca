# Rate-half three-petal LS6 reductions

```yaml
workboard_item: T
row: symbolic rate-half smooth RS FPC5 M=4,t=3 Johnson-nonpositive tail; not a deployed row
object: LIST
target_epsilon: target-free structural theorem; intended finite context 2^-128
agreement: symbolic source chart with locator degree j=2*ell-a
B_star: N/A
direct_statement: short-syzygy LS6 sources are empty, common-pencil LS6 atoms are empty, and every low-multiplier LS6 slice is an exact locator-prefix ladder
architecture: DIRECT
partition_digest: N/A (DIRECT structural theorem)
atom_or_cell: one fixed guarded three-petal complement-divisor atom LS6
quantifier: every field and every parameter tuple satisfying the printed hypotheses
projection_and_unit: monic locator candidates in one fixed LIST source cell
claimed_bound: zero on the source-ratio-degree-below-a stratum; exact Q0^(e-a)-cell prefix decomposition in the low-multiplier stratum
status: PROVED
impact: ARCHITECTURE_BRIDGE
falsifier: a guarded common-pencil solution, or a low-multiplier solution outside the displayed bijection
replay: python3 experimental/scripts/verify_list_fpc5_three_petal_ls6_reductions_v1.py
```

## 1. Purpose and nonclaim

This note isolates two exact reductions for the three-petal guarded divisor
atom that occurs in the rate-half, four-petal LIST route.  The reductions are
stated directly at the polynomial level, so they can be reviewed without
importing an owner ledger.

They do **not** prove a deployed LIST row, a maximum-versus-average theorem,
or an exhaustive source-to-row projection.  Their useful consequence is more
specific:

1. every source with a modular locator ratio of degree below defect `a`
   contributes no guarded LS6 candidates; common pencils are the degree-zero
   case; and
2. below the multiplier-degree wall, the remaining linear slice is exactly a
   tower of ordinary locator-prefix cells, with no loss in the normalized
   average scale when the tower is expanded.

This is an `ARCHITECTURE_BRIDGE` to the repository's `Q` and split-pencil
work, not a bankable row atom.

## 2. The guarded LS6 atom

Let `K` be a field.  Fix integers

```text
ell>a>=1,       s=ell-a,       j=2ell-a.
```

Let `L_2,L_3 in K[X]` be coprime monic polynomials of degree `ell`, put
`M=L_2L_3`, and let `E in K[X]` be the canonical representative of a unit in
`K[X]/(M)`, so `deg E<2ell` and `gcd(E,M)=1`.  For any monic polynomial `D`
of degree `j`, write

```text
D E=M Q+V,       deg V<2ell.                         (2.1)
```

The unguarded LS6 slice consists of the `D` for which `deg V<=s`.  A guarded
LS6 atom additionally imposes

```text
D divides a declared split core locator L_C,
gcd(D,V)=1.                                           (2.2)
```

Only the second guard is needed for the common-pencil exclusion below.  Both
guards merely delete members from the prefix cells in Section 4.

### Lemma 2.1 (multiplier-degree gate)

If the guarded atom is nonempty, then

```text
deg E>=a.                                             (2.3)
```

**Proof.**  If `e=deg E<a`, then `deg(DE)=2ell-a+e<2ell`, so no reduction
modulo `M` occurs.  The remainder is `DE` itself and has degree at least
`2ell-a>s`, contrary to the LS6 degree condition.  QED.

### Theorem 2.2 (inverse source-ratio gate)

Let `F` be the canonical inverse of `E` modulo `M`.  Every nonempty guarded
atom on the branch `a<=ell/2` satisfies

```text
deg F>=ell+a.                                         (2.4)
```

For the source multiplier defined by (3.2) below, put

```text
U=rem_(L_3)(L_1 L_2^(-1)).                           (2.5)
```

Then nonemptiness forces the source-only condition

```text
deg U>=a.                                             (2.6)
```

Equivalently, the complementary source stratum has a short syzygy

```text
L_1=U L_2+R L_3,       deg U,deg R<a,                (2.7)
```

and its guarded LS6 atom is empty.

**Proof.**  Multiplying `DE==V mod M` by `F` gives
`D=rem_M(FV)`.  If `deg F<ell+a`, then `deg(FV)<2ell`, so `D=FV` without
modular reduction.  Since `deg D=2ell-a` and `a<=ell/2`, `V` is
nonconstant, contradicting `gcd(D,V)=1`.

The source residues (3.2) give

```text
F==L_1                 mod L_2,
F==lambda^(-1)L_1      mod L_3.
```

Consequently

```text
F=L_1+L_2 A,
A=(lambda^(-1)-1)U,
```

where `deg A<ell`.  Since the scalar is nonzero, `deg F>=ell+a` is
equivalent to `deg U>=a`.  Finally, (2.5) says exactly that
`L_1-U L_2=R L_3`; if `deg U<a`, degree comparison gives `deg R<a`.  QED.

## 3. The common-pencil stratum is empty

Assume now that the three touched petal locators have the form

```text
L_i=P-z_i,       i=1,2,3,                            (3.1)
```

where `P` is monic of degree `ell` and the scalars `z_1,z_2,z_3` are
distinct.  Normalize the three source labels to `(0,1,lambda)`, with
`lambda` nonzero and different from one.  The complement multiplier `E` is
the unique polynomial of degree below `2ell` satisfying

```text
E L_1 == 1       mod L_2,
E L_1 == lambda  mod L_3.                            (3.2)
```

For (3.1), the ratio in (2.5) is the constant

```text
U=(z_3-z_1)/(z_3-z_2).
```

Thus Theorem 2.2 already excludes every common pencil.  The two direct
computations below are retained because they identify the separate aligned
degree obstruction and misaligned common-factor obstruction.

### Theorem 3.1 (aligned pencil)

If

```text
lambda=(z_3-z_1)/(z_2-z_1),                          (3.3)
```

then the guarded LS6 atom is empty.

**Proof.**  The constant `E=(z_2-z_1)^(-1)` satisfies both congruences in
(3.2), hence is the canonical multiplier.  Lemma 2.1 excludes it because
`a>=1`.  QED.

### Theorem 3.2 (misaligned pencil)

If (3.3) fails, the guarded LS6 atom is again empty.

**Proof.**  Put

```text
e_2=(z_2-z_1)^(-1),       e_3=lambda*(z_3-z_1)^(-1).
```

The congruences (3.2) say that `E` takes the constant values `e_2,e_3`
modulo `P-z_2,P-z_3`.  Their unique representative is

```text
E=A(P-z_0),       A!=0,                              (3.4)
```

for a scalar `z_0` distinct from `z_2,z_3`; misalignment is exactly the
condition `A!=0`.

Suppose an LS6 solution exists and use (2.1).  Degree comparison gives
`deg Q=s`.  Reducing (2.1) modulo `P-z_0` shows that

```text
(z_0-z_2)(z_0-z_3)Q+V
```

is divisible by `P-z_0`.  Its degree is at most `s<ell`, so it vanishes:

```text
V=-(z_0-z_2)(z_0-z_3)Q.                              (3.5)
```

Using

```text
(P-z_2)(P-z_3)-(z_0-z_2)(z_0-z_3)
  =(P-z_0)(P+z_0-z_2-z_3)
```

in (2.1), then cancelling `P-z_0`, gives

```text
A D=Q(P+z_0-z_2-z_3).                                (3.6)
```

Since `deg Q=s>0`, equations (3.5)--(3.6) make `Q` a nonconstant common
divisor of `D` and `V`.  This contradicts (2.2).  QED.

Together, Theorems 3.1 and 3.2 exclude every common-pencil source,
independently of the distinct normalized labels.

## 4. Exact low-multiplier prefix ladder

Write `e=deg E` and `c=lc(E)`.  Assume

```text
a<=e<=s.                                             (4.1)
```

### Theorem 4.1 (prefix-ladder parametrization)

The complete monic unguarded LS6 slice is in bijection with pairs `(Q,R)`
such that

```text
deg Q=e-a,       lc(Q)=c,
deg R<=s-e.                                           (4.2)
```

For each `Q`, divide

```text
M Q=E T_Q+R_Q,       deg R_Q<e.                      (4.3)
```

The bijection and its inverse are

```text
D=T_Q+R,       V=-R_Q+E R.                           (4.4)
```

**Proof.**  In (2.1), leading degrees force
`deg Q=e-a` and `lc(Q)=c`.  Reducing (2.1) modulo `E` gives
`V==-R_Q mod E`.  Under (4.1), every polynomial in this residue class of
degree at most `s` is uniquely `-R_Q+ER` with `deg R<=s-e`.  Substitution
in (2.1) gives (4.4), and the same calculation in reverse proves
surjectivity.  The degree and leading-coefficient constraints make `D`
monic of degree `j`.  QED.

For fixed `Q`, all coefficients of `D` in degrees above `s-e` are fixed.
Thus each `Q` gives one ordinary monic locator-prefix cell of nonleading
prefix depth

```text
h_e=j-(s-e)-1=ell+e-1.                               (4.5)
```

If `K` is finite of order `Q_0`, there are exactly `Q_0^(e-a)` such cells.
Consequently their coarse ambient-normalized split mass has the exact
cancellation

```text
Q_0^(e-a) * binom(n,j)/Q_0^(ell+e-1)
  =binom(n,j)/Q_0^(ell+a-1).                         (4.6)
```

The right side is independent of `e`.  At `e=a` there is one prefix cell of
depth `ell+a-1`.  Equivalently, allowing arbitrary leading coefficient
shows that the underlying truncated vector slice has dimension

```text
(e-a+1)+(s-e+1)=ell-2a+2,                            (4.7)
```

so its projectivization has dimension `ell-2a+1` and satisfies

```text
j-2(ell-2a+1)=3a-2>=1.                               (4.8)
```

The split-core and coprimality guards only remove points from these cells.

## 5. Interface with the live upstream program

Theorem 2.2 removes every source carrying a degree-below-`a` locator syzygy,
including the full split-pencil stratum, before any maximum-fiber estimate.
Theorem 4 turns the range `a<=deg E<=ell-a` into a
precise instance of the repository's pruned locator-prefix problem `Q`:
increasing `deg E` creates `Q_0^(e-a)` targets but fixes exactly `e-a`
additional prefix coefficients.  Hence a depth-uniform prefix
maximum-to-mean theorem would traverse the complete ladder without a
field-sized union-bound loss.

What remains outside this packet is explicit:

- classification of source-ratio degrees at least `a` and the
  maximum-to-mean estimate for the realized guarded prefix cells;
- the high-multiplier range `deg E>ell-a`, which remains a genuine
  split-in-subspace/balanced-core problem;
- quotient, reciprocal/dihedral, and first-owner transport; and
- exhaustive projection from this symbolic FPC5 source cell to a deployed
  row numerator.

The existing quotient/prefix discussion in
`experimental/notes/l1/l1_prefix_divisor_count.md` is the nearest upstream
consumer.  The present note contributes a source-side exact ladder and a
split-pencil exclusion; it does not change that note's maximum-fiber status.

## 6. Replay

Run

```bash
python3 experimental/scripts/verify_list_fpc5_three_petal_ls6_reductions_v1.py
```

The stdlib-only exact finite-field replay checks both degree gates, the exact
inverse source-ratio form, aligned and misaligned pencil identities, the
forbidden common factor, the prefix parametrization, cell depth, cell count
exponent, and the invariant effective depth. The script is a regression
companion to the proofs, not their source.
