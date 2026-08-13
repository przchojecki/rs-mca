# Mersenne-31 semantic owner profiles: deployed one-pencil payment and an exact `F_241` line regression

**Status:** `PROVED LOCAL PROFILE COMPILERS / PROVED FINITE SEMANTIC REGRESSION / OPEN DEPLOYED EXHAUSTIVITY AND RESIDUAL THEOREM`

**Lean authority:** `experimental/lean/m31_q_rooted_shell/`, stdlib only.

## 1. Purpose and proof boundary

The previous semantic packet fixed the required types:

```text
received line -> explanation -> witness -> explaining codeword
              -> codeword ray -> distinct slope,
```

an executable fixed-before-line C1--C8 owner function, separate denominators
`q_prof^w` and `q_slope`, and the literal post-deletion residual
`{classify = none}`.  It also proved that a valid `3+7` bound on the ten-neighbor
`F_241` shell requires at least two genuine earlier-owner certificates.

This packet makes two next steps without repeating the rooted-shell reduction or
its support-only counterexamples.

1. It instantiates theorem-level paid line-local profiles for two active
   Mersenne-31 list-row branches: the near-rational finite-slope branch and the
   primitive one-pencil branch after common-GCD deletion.
2. It lifts the `F_241` support star to one explicit received line with eleven
   genuine explanation/codeword/ray/slope states, constructs an exact
   two-slope earlier owner, and proves `3+7` on the resulting executable
   eight-neighbor residual.

The universal deployed theorem

```text
p^w * max(d_e(A)-3,0) <= 7 H_e
```

for every executable post-C1--C8 Mersenne-31 residual shell remains open.  The
active sources still do not supply an exhaustive row-level C1--C8 semantic
classifier, a chart-multiplicity theorem for all paid profiles, or the required
all-shell residual estimate.

## 2. Actual deployed line-local profiles

Use the active Mersenne-31 list-row constants

```text
p       = 2^31-1 = 2,147,483,647,
n       = 2^21   = 2,097,152,
a+      = 1,116,023,
omega   = n-a+   = 981,129,
w       = 67,447,
ceil(C(n,a+)/p^w) = 1,993,678.
```

The active Grande Finale source gives two scoped slope-level producers.

### 2.1 Near-rational supplied-certificate compiler

The former source claim that an arbitrary received line leaves at most one
finite near-rational support-wise MCA-bad slope is withdrawn.  Its replacement
is the MCA-only two-anchor bound `<=2w` under `3w<=n-K`; it supplies no payment
for this note's list-row near-rational branch.  The Lean constructor here remains
valid only as a compiler for an independently supplied
`M31NearRationalCertificate` whose deduplicated line-local slope image already
has length `<=1`; it does not produce that certificate or pay the whole
near-rational branch.  On such a supplied singleton profile it returns

```text
U_owner = 1,
q_slope = p,
natural numerator = 1 + 1,993,678 = 1,993,679.
```

### 2.2 Primitive C8 one-pencil branch

After the common-GCD first-match strip, `cor:bc-one-pencil` and the moving-root
incidence bound give, on a primitive projective locator pencil,

```text
#distinct slopes <= floor(n/omega) = floor(2,097,152/981,129) = 2.
```

`M31PrimitiveOnePencilCertificate` records the actual deduplicated slope list
and the source-theorem cap.  `m31PrimitiveOnePencilProfile` produces

```text
U_owner = 2,
q_slope = p,
q_prof^w = p^67,447,
natural numerator = 1,993,679.
```

The Lean theorem `m31PrimitiveOnePencilProfile_denominators` prints the two
denominators separately; no ambient/slope-field identification is hidden.
`m31PrimitiveOnePencilProfile_budget` carries the exact chain

```text
#slopes <= 2 <= q_slope
and
2 <= natural numerator.
```

These constructors pay supplied theorem-certified line profiles.  They do not
classify all explanations into those profiles, count all pencils on one line,
or claim that the one-pencil branch exhausts C8.

## 3. Explicit semantic `F_241` received line

Let the domain be the existing order-twenty subgroup of `F_241`, indexed by
`D_i=235^i`.  The new fixture uses

```text
u0 = [108,150,68,65,34,129,22,52,33,226,174,0,...,0],
u1 = [  5, 28,224,117,204,112,224,189,230, 72, 55,0,...,0].
```

There are eleven exact-cardinality explanation states: the ten members of the
rooted distance-six shell followed by its anchor.  Their distinct slopes are

```text
[115,44,22,133,230,0,74,107,56,9,193].
```

For every state the Lean fixture stores:

- the ten-point support;
- a degree-`<8` polynomial `h` agreeing with `u0 + gamma*u1` on that support;
- a nonzero normalization scalar and the normalized coefficient ray;
- a dual parity row on the support.

The executable checks prove all eleven support agreements, all eleven ray
normalizations, and duplicate-freeness of both the ray and slope tables.

### 3.1 Why the states are noncommon

For one support `S={x_1,...,x_10}`, let the stored parity weights be
`lambda_1,...,lambda_10`.  The certificate verifies

```text
sum_i lambda_i x_i^t = 0  in F_241,  0 <= t < 8,
sum_i lambda_i u1(x_i) != 0.
```

Therefore the parity functional annihilates every evaluation of a polynomial of
degree below eight but not `u1|_S`.  Hence `u1` is not explained on `S`.  Since
the stored `h` explains `u0+gamma*u1` on `S`, the state is a genuine semantic
noncommon line explanation, not a bare support.

The module `SemanticLineRegression.lean` kernel-checks every finite arithmetic
certificate with `native_decide`; the preceding linear-functional argument is
the source proof connecting those exact checks to the Reed--Solomon semantic
condition.

## 4. Exact earlier owner and paid line profile

Choose the shell states with slopes `115` and `22`.  Their support locators are

```text
L_A = [25,68,25,95,0,89,90,46,135,149,1],
L_B = [201,179,205,0,146,154,35,0,135,149,1],
```

with coefficients written constant term first.  They have exactly the common
support roots

```text
G = {0,1,15}.
```

After removing `G`, a split member of the projective pencil
`span(L_A,L_B)` needs seven moving roots.  Parameterize finite points by
`L_A + lambda L_B` and use the sentinel `lambda=241` for the point at infinity.
The exact root census over all 242 projective parameters is

```text
#{lambda : at least seven moving roots} = {0, infinity}.
```

In particular, the chart has exactly two split endpoints.  This is a genuine
line-local common-GCD/pencil owner certificate: it uses the received line,
explaining codewords, rays, and actual slopes.  The fixed owner function assigns
exactly these two explanations to `OwnerId.c3`; its paid profile is

```text
slopes = [115,22],
U_owner = 2,
q_slope = 241,
q_prof^w = 241^2 = 58,081,
natural numerator = 5.
```

The owner ID records the earlier common-GCD/planted branch in the fixed C1--C8
order.  The common core alone is not the trigger: the executable classification
is sound only because the complete semantic line certificate and exact
line-local slope profile are present.

## 5. Exact executable residual

The full rooted shell contains ten semantic explanations.  Filtering by the
same fixed owner function gives

```text
ownedNeighbors    = [slope 115, slope 22],
residualNeighbors = the other eight explanations.
```

Thus the literal `classify = none` residual has degree eight.  At the imported
natural scale and shell size,

```text
58,081 * (8-3) = 290,405
                  <= 308,700 = 7 * 44,100,
margin = 18,295.
```

Lean proves:

- both owned explanations have `EarlierOwnerCertificate`;
- the owner profile carries the full exact/natural budget chain;
- `residualShell` is the actual `none` fibre;
- the residual satisfies `LocalNaturalEnvelopeAt ... 3 7 H_6`;
- the residual theorem compiles to the semantic owner-or-shell statement on the
  original ten-neighbor shell; and
- the inherited generic minimum of two owned neighbors is attained exactly.

This is the required mandatory regression in positive form: two real semantic
owner certificates, not support symmetry or an empty planted core, are exactly
what repairs the false full-shell inequality.

## 6. Lean declaration map

| Claim | Declaration |
|---|---|
| exact M31 primitive one-pencil arithmetic | `m31List_onePencilCap_eq_two` |
| calibrated natural denominator/numerator | `M31ListNaturalScaleCalibration.denominator_eq`, `.naturalNumerator_eq` |
| deployed near-rational paid profile | `m31NearRationalProfile` |
| deployed primitive C8 paid profile | `m31PrimitiveOnePencilProfile` |
| separate deployed denominators | `m31PrimitiveOnePencilProfile_denominators` |
| deployed one-pencil budget chain | `m31PrimitiveOnePencilProfile_budget` |
| all eleven exact semantic checks | `all_explanations_semantically_valid` |
| support agreement and parity certificates | `all_explanations_agree_on_their_supports`, `all_parity_certificates_valid` |
| distinct rays and slopes | `semantic_rays_nodup`, `semantic_slopes_nodup` |
| exact two-endpoint pencil | `splitPencilParameters_exact` |
| fixed semantic C3 trigger | `ownerFn`, `classify_eq_some_iff` |
| paid two-slope ledger | `ledger`, `c3Profile_budget_chain` |
| exact owned/residual filters | `ownedNeighbors_exact`, `residualNeighbors_exact` |
| two genuine owner certificates | `ownerA_has_certificate`, `ownerB_has_certificate` |
| exact residual degree and `3+7` | `residualShell_degree_exact`, `residualShell_three_plus_seven` |
| semantic compilation | `semantic_owner_or_shell` |
| sharp two-owner regression | `exactly_two_owned_neighbors`, `generic_two_owner_regression_is_sharp` |

## 7. Sorry/axiom census and nonclaims

The new Lean modules use no `sorry`, no `axiom`, and no Mathlib.  Their printed
axiom census is empty apart from Lean's trusted kernel mechanisms used by
`native_decide`.

Not proved here:

- executable deployed definitions and theorem-backed payments for all eight
  C1--C8 triggers;
- witness-exhaustive deployed first-match classification;
- per-line census of every realized paid chart;
- the `3+7` bound on every deployed Mersenne-31 residual shell;
- row-sharp Q, the complete `U_paid + U_Q + U_list-int + U_new` ledger, or an
  adjacent safe row.

The next theorem must either extend the deployed profile constructors into a
source-bound exhaustive owner atlas or prove the local `3+7` inequality on the
remaining exact residual.  Support-only quotient/dihedral symmetry and planted
core pruning remain inadmissible as semantic ownership.
