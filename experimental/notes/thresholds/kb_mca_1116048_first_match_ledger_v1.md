# KB-MCA 1116048 first-match ledger v1

Status: CONDITIONAL / PARTIAL UPPER LEDGER AUDIT.

This packet does not prove `U(1116048) <= B*`, does not certify the
KoalaBear MCA first-safe agreement, and does not promote v13 raw material into
Paper D.  It is a partial first-match ledger/audit packet for the conjectured
adjacent row.

This note records exact paid-cell arithmetic for the KoalaBear sextic MCA
adjacent candidate row

```text
n = 2^21,  k = 2^20,  A = 1116048.
```

It computes the exact remaining primitive
allowance after the generated-field collision bucket and the Q0 quotient/planted
rung audit are applied.  Q0 proves dyadic quotient/planted descent, raw-pays the
terminal covered rungs, emits the nonterminal lower-rung obligations, and names
the open planted-tail rungs.  Q1 proves the exact split-prefix collision
decomposition by one-sided difference.  Q2 proves the twist-stabilizer forcing
step for heavy prefix targets and the exact-lift folding theorem for stabilized
prefix fibers.  The row still needs primitive-heavy-orbit exclusion, finite
generated-prefix bucket scoping, lower-rung certificates outside the stabilized
Q2 path, and the other open image ledgers before any safe-side upper certificate
can close.

The companion verifier is:

```bash
python3 experimental/scripts/verify_kb_mca_1116048_first_match_ledger_v1.py --check
python3 experimental/scripts/verify_kb_mca_1116048_first_match_ledger_v1.py --full --check
```

It emits:

```text
experimental/data/certificates/kb-mca-1116048-first-match-ledger-v1/
experimental/notes/certificate_scanner/outputs/kb_mca_1116048_first_match_ledger_v1.report.md
```

## Row constants

For the deployed KoalaBear row,

```text
p = 2^31 - 2^24 + 1 = 2130706433,
q_line = p^6,
B* = floor((q_line - 1) / 2^128)
   = 274980728111395087.
```

At the adjacent candidate agreement,

```text
A = 1116048,
j = n - A = 981104,
t = A - k = 67472,
w = t - 1 = 67471.
```

The v13 prefix/Q-fin average convention uses `w=t-1`, so

```text
avg = binom(n,j) / p^w,
K_raw = floor(B* / avg)
      = floor(B* p^w / binom(n,j))
      = 4807520.
```

Thus the primitive Q-fin theorem, before any paid branch deductions, would need
a multiplier at most `4807520`.

## Generated-field collision charge

Let

```text
O = Z[zeta_n],     K0 = Q(zeta_n),
red_p : O -> F_p, red_p(zeta_n)=omega,
```

where `omega` is an order-`n` element in `F_p`.

Consider an ordered affine row packet

```text
L_i(S,Z) = A_i(S) + Z B_i(S),       i = 0,...,R-1,
```

with `A_i(S),B_i(S) in O`.  Assume earlier first-match buckets have removed
pivot/rank-drop failures, so for the chosen pivot row

```text
red_p(B_0(S)) != 0.
```

Define the cross defects

```text
G_i(S) = B_0(S) A_i(S) - A_0(S) B_i(S).
```

Then every finite survivor over `F_p` that is not an honest survivor over
`Q(zeta_n)` has, for at least one row index `i`,

```text
G_i(S) != 0 in O,
red_p(G_i(S)) = 0 in F_p.
```

Assign the survivor to the first such `i` and to the generated slope

```text
lambda = -red_p(A_0(S)) / red_p(B_0(S)) in F_p.
```

This is a first-match image-cell assignment.  There are at most `R` row indices
and at most `p` generated slope values, so

```text
B_gen <= R p.
```

For the deployed high-row packet we use the conservative row count `R <= t`,
hence

```text
B_gen <= t p
      = 67472 * 2130706433
      = 143763024447376.
```

This is an image-cell cost, not a raw support count.  A generated cell may
contain many supports; that multiplicity is not paid here.

## Generated-collision arithmetic consequence

After deducting only the proved generated-field image-cell bucket,

```text
B_rem = B* - t p
      = 274836965086947711,

K_rem = floor(B_rem p^w / binom(n,j))
      = 4805007.
```

Adding the conditional `n+1` half-turn/pair-small image cost from the half-turn
packet does not change this integer multiplier:

```text
floor((B_rem - (n+1)) p^w / binom(n,j)) = 4805007.
```

The partial paid-cell ledger therefore leaves the primitive residual target

```text
max primitive Q-fin fiber <= 4805007 * binom(n,j) / p^w.
```

## Q0: dyadic quotient/planted rung audit

This is the Q0 step from `experimental/cap25_v13_missing_inputs_strategy.md`:
perform the rung-margin audit first, prove that quotient support mass must be
paid by image descent rather than raw support count, and emit the exact
lower-rung obligations for the finite adjacent row.

Let `D_n=<omega>` with `n=2^m`, and let

```text
Phi_w(S) = (lambda_1(S),...,lambda_w(S))
```

be the locator-prefix map for

```text
Lambda_S(X)=prod_{alpha in S}(X-alpha)
           = X^j + lambda_1 X^{j-1} + ... + lambda_j.
```

Fix a dyadic divisor `c|n` and let

```text
pi_c : D_n -> D_{n/c},   pi_c(alpha)=alpha^c.
```

Write

```text
j_c = floor(j/c),       r_c = j - c j_c,
w_c = floor(w/c).
```

A support is `c`-quotient/planted if

```text
S = P disjoint-union pi_c^{-1}(Q),
|Q| = j_c, |P| = r_c.
```

If `r_c <= w`, then inside each top prefix fiber `Phi_w^{-1}(z)`, the map

```text
S -> Q
```

injects the `c`-quotient/planted part into the lower-rung prefix fiber

```text
Phi_{w_c}^{-1}(z_c,z_{2c},...,z_{w_c c}).
```

Proof.  Write

```text
Lambda_P(X)=sum_{h=0}^{r_c} b_h X^{r_c-h},
Lambda_Q(Y)=sum_{ell=0}^{j_c} a_ell Y^{j_c-ell},
```

with `a_0=b_0=1`.  Then

```text
Lambda_S(X)=Lambda_P(X)Lambda_Q(X^c).
```

Since `0<=r_c<c`, the coefficient at deficit `d` from the top is nonzero only
when `d=h+c ell` with unique `0<=h<=r_c`; then it equals `b_h a_ell`.  The
deficits `1<=d<=r_c` recover all coefficients of `Lambda_P`, hence recover
`P`, because `r_c<=w`.  The deficits `c,2c,...,w_c c` recover
`a_1,...,a_{w_c}`.  Thus two top supports in the same top prefix fiber that
map to the same `Q` have the same recovered `P` and the same lifted quotient
core, hence are equal.  This proves the injection.

For the deployed row, this descent applies exactly to the rungs with
`r_c<=w`, namely through `c=131072`.  The rungs `c=262144,524288,1048576,2097152`
have arbitrary planted tails with `r_c>w` and remain open.

The Q0 status split is:

```text
PROVED_EXACT_QUOTIENT_DESCENT_NEEDS_LOWER_RUNG_BOUND:
  c = 2,4,8,16

PROVED_PLANTED_DESCENT_NEEDS_LOWER_RUNG_BOUND:
  c = 32,64,128,256,512,1024,2048,4096,8192,16384,32768

PROVED_DESCENT_AND_RAW_PAID:
  c = 65536,131072

OPEN_PLANTED_TAIL_R_GREATER_THAN_W:
  c = 262144,524288,1048576,2097152
```

For every nonterminal covered rung `c=2,...,32768`, Q0 reduces the top branch
to the lower-rung certificate

```text
max_u |Phi_{w_c}^{-1}(u)|
  <= K_c * binom(n_c,j_c) / p^w_c,
```

where

```text
K_c = floor(B_rem_proved * p^w_c / binom(n_c,j_c)).
```

These lower-rung certificates are not proved here; Q0 makes them explicit and
prevents the quotient/planted mass from being counted as top-rung primitive
mass.

The two terminal covered rungs are already raw-paid:

```text
c = 65536:  binom(32,14) = 471435600,
c = 131072: binom(16,7)  = 11440.
```

So

```text
B_quot_terminal = 471447040.
```

Together with the generated-field bucket,

```text
B_paid_proved = 143763024447376 + 471447040
              = 143763495894416,

B_rem_proved = 274836964615500671,
K_rem_proved = 4805007.
```

The integer multiplier remains unchanged.

## Split-prefix collision distance

This packet also proves a support-level collision-rigidity lemma for the prefix
map.  It is useful Q1 infrastructure, but it is not the missing primitive
max-fiber theorem.

Let `S,T subset D` be two distinct supports with

```text
|S| = |T| = j,
Phi_w(S) = Phi_w(T).
```

Write their monic split locators as

```text
Lambda_S(X)=prod_{alpha in S}(X-alpha),
Lambda_T(X)=prod_{alpha in T}(X-alpha).
```

Let

```text
G = gcd(Lambda_S,Lambda_T),
Lambda_S = G A,
Lambda_T = G B,
```

where `A,B` are split locators of degree

```text
e = |S \ T| = |T \ S|.
```

Since the first `w` prefix coefficients agree, the leading term and the next
`w` coefficients of `Lambda_S-Lambda_T` vanish.  Hence

```text
deg(Lambda_S-Lambda_T) <= j-w-1.
```

But

```text
Lambda_S-Lambda_T = G(A-B),
deg G = j-e.
```

Because `S != T`, the polynomial `A-B` is nonzero.  Therefore

```text
j-e + deg(A-B) <= j-w-1,
```

so `e >= w+1`.  Thus two distinct supports in a common prefix fiber differ in
at least

```text
w+1 = 67472
```

positions on each side, or at least

```text
2(w+1) = 134944
```

positions in symmetric difference.

This lemma only gives pairwise separation inside a fiber.  Constant-weight
packing bounds from this distance are far too weak to replace the required
finite primitive max-orbit certificate with multiplier `K_rem=4805007`.

## Exact-lift fiber bound, not finite-field payment

There is a useful honest cyclotomic observation for the same row.  Over
`Q(zeta_n)`, if two supports have equal first `w` prefix coefficients, then
Newton identities give equality of the first `w` power sums.  Since

```text
w = 67471 >= 2^16,
```

the mask difference polynomial vanishes at

```text
zeta_n, zeta_n^2, zeta_n^4, ..., zeta_n^{2^16}.
```

Therefore it is divisible by

```text
prod_{s=5}^{21} Phi_{2^s}(X) = (X^n - 1)/(X^16 - 1).
```

Because the mask polynomial has degree `<n`, the coefficient difference is
constant on each residue class modulo `16`.  Thus exact honest prefix fibers
vary only by whole terminal cosets of size `n/16=131072`.  With

```text
j = 981104,
floor(j / 131072) = 7,
```

each exact honest prefix fiber has size at most

```text
max_{0<=q<=7} binom(16,q) = binom(16,7) = 11440.
```

This is deliberately **not** deducted as a finite-field first-match payment in
this packet.  The tempting argument "remove all but one honest lift class per
finite prefix value at cost `w*p`" does not match the current image-cell
semantics: row-coordinate cells do not bound the number of finite prefix values
or raw supports.  A valid finite-field lift-class cost model remains a separate
target.

## First-match branches

This packet uses the following branch order.

```text
1. contained or noncontained failure
2. rank-drop or pivot failure
3. tangent / common-line / residue-line
4. quotient-periodic or divisor-stabilized
5. planted / prefix-structured
6. extension-valued slope
7. base generated-field collision
8. sparse sigma or sparse-support
9. M1 half-turn / coefficient-shadow
10. primitive Q-fin residual
```

Branches 4 and 7 now have proved deductions:

```text
branch 7: generated-field collision image cells, cost <= t*p;
branch 4: Q0 terminal quotient/planted raw-paid rungs c=65536,131072.
```

The other Q0-covered quotient/planted rungs descend to lower-rung max-fiber
obligations but are not yet paid.  Branch 6 is deliberately open: the line field
is `F_{p^6}`, while the generated-collision charge above is a base `F_p`
image-cell charge.  Extension-valued slopes in `F_{p^6} \ F_p` still need their
own image-cell theorem or chart bound.

## Guardrail

The verifier includes the small finite-field `{1,3}` guardrail

```text
F_17, n=16, omega=3, support exponents {0,1,3,14}.
```

The support satisfies the finite `{1,3}` rows modulo `17`, but its honest
cyclotomic cross-defect is nonzero and reduces to zero modulo `17`.  This
prevents the characteristic-zero half-turn theorem from being silently promoted
to a finite-field theorem; the finite-only survivor is instead charged to the
generated-field bucket.

## Remaining target

The next theorem is:

```text
KB-MCA 1116048 primitive Q-fin max-orbit flatness after first-match removal.
```

In the current partial paid-cell ledger, after generated-field and terminal quotient
deductions, the exact numerical target is:

```text
max primitive Q-fin fiber <= 4805007 * binom(n,j) / p^w.
```

Equivalently, define the first-match residual fiber

```text
R(z) =
{ S subset D :
    |S| = 981104,
    Phi_w(S)=z,
    S is not assigned to generated-field,
    S is not assigned to terminal quotient/planted,
    S is not assigned to tangent/common-line,
    S is not assigned to extension-confined,
    S is not assigned to sparse/Pade-Hankel,
    S is not assigned to known M1/half-turn,
    S is not assigned to contained/rank-drop }.
```

This residual estimate is necessary but not sufficient by itself.  A future
complete safe-side packet would need all named open first-match branches paid
by explicit theorems/certificates with printed costs, the primitive Q-fin
residual bound above, and a complete first-match paid-cell sum within `B*`.

The currently proved paid-cell budget is

```text
B_paid_proved = 143763495894416,
B_rem_proved = B* - B_paid_proved = 274836964615500671,
K_rem_proved = floor(B_rem_proved p^w / binom(n,j)) = 4805007.
```

So the displayed primitive residual certificate would fit inside the currently
remaining budget if all other named branches were also paid consistently.  The
complete row closure and the primitive residual certificate are not proved in
this packet.

Before that can close the row, the ledger still needs image-level handling for:

```text
extension-valued slopes;
Q0 lower-rung quotient/planted max-fiber certificates for c=2,...,32768;
arbitrary planted-tail bounds for c>=262144;
sparse sigma cells;
arbitrary M1 row-slice windows beyond the half-turn packets.
finite-field lift-class cost model if exact-lift bounds are to be used.
```

## Q1: exact split-prefix collision ledger

This packet now proves the Q1 collision-decomposition theorem from
`experimental/cap25_v13_missing_inputs_strategy.md`.

Let

```text
N_w(z) = |{S subset D : |S|=j, Phi_w(S)=z}|.
```

Then

```text
sum_z N_w(z)^2
  = binom(n,j) + sum_{e=w+1}^{min(j,n-j)} C_e,
```

where `C_e` counts ordered distinct support pairs `(S,T)` with

```text
|S|=|T|=j,
|S\T|=|T\S|=e,
Phi_w(S)=Phi_w(T).
```

More explicitly, if `I=S cap T`, `S=I disjoint-union A`,
`T=I disjoint-union B`, and

```text
Lambda_S = Lambda_I Lambda_A,
Lambda_T = Lambda_I Lambda_B,
```

then prefix equality is equivalent to

```text
deg(Lambda_A - Lambda_B) <= e-w-1.
```

Thus no nontrivial collision occurs for `1<=e<=w`, and minimal collisions
`e=w+1` are exactly the constant-shift split-pair packets

```text
Lambda_A - Lambda_B = constant.
```

For the deployed row,

```text
w+1 = 67472,
min(j,n-j) = 981104.
```

The verifier replays the identity on small cyclic-domain examples, checking
that the ordered-pair strata sum to the exact second moment and that every
nontrivial collision has `e>=w+1`.

What Q1 does not do is evaluate every deployed `C_e` summand.  Instead, it
turns the second moment into a precise residual split-pair count.  The next
use of Q1 is to feed Q2: heavy-fiber fewness, stabilizer detection, and
quotient/planted descent.

## Q2: heavy-fiber symmetry descent

This packet proves the first Q2 theorem: twist-stabilizer forcing.  Its target
is not mode-at-null.  Our small prefix-fiber scans found examples where the null
fiber is not maximal, so the correct object is a max-orbit or stabilizer descent
theorem.

Let `H_T` be any threshold-heavy target set:

```text
H_T = { z : N_w(z) >= T }.
```

For `eta in mu_n`, twisting supports by `eta` sends

```text
(z_1,...,z_w) -> (eta z_1, eta^2 z_2, ..., eta^w z_w)
```

and preserves fiber size.  Therefore `H_T` is a union of twist orbits.  If

```text
|H_T| <= M,
```

then every heavy target has orbit size at most `M`.  By orbit-stabilizer,

```text
|Stab(z)| >= n/M.
```

In particular, if `M <= n/h`, then every heavy target has stabilizer size at
least `h`.  A stabilizer of order `h` forces

```text
z_d = 0 unless h divides d.
```

Thus the target is quotient-supported and its surviving prefix coordinates live
at lower depth

```text
floor(w/h).
```

For the deployed row, the first thresholds are:

```text
|H_T| <= 2^20  => stabilizer >= 2, lower depth 33735,
|H_T| <= 2^19  => stabilizer >= 4, lower depth 16867,
|H_T| <= 2^18  => stabilizer >= 8, lower depth 8433,
|H_T| <= 2^17  => stabilizer >= 16, lower depth 4216.
```

The verifier replays this on small cyclic-domain examples.  In one replay
(`F_17`, `n=16`, `j=8`, `w=3`), the max-heavy target set has size `8<n`, and
every max-heavy target has stabilizer `2`, exactly as the theorem predicts.

This packet also proves the Q2 folding bridge over exact lifted cyclotomic
fibers.

Let

```text
h = 2^r | n,        h/2 <= w.
```

Suppose an exact lifted target `z in Q(zeta_n)^w` is fixed by an element of
order `h` under the twist action.  Equivalently,

```text
z_d = 0 for every d <= w with h not dividing d.
```

If `S` lies in the exact lifted fiber over `z`, then

```text
lambda_1(S)=...=lambda_{h/2}(S)=0.
```

Newton identities give

```text
P_k(S)=sum_{x in S} x^k = 0,      1 <= k <= h/2.
```

In particular,

```text
P_1(S)=P_2(S)=P_4(S)=...=P_{h/2}(S)=0.
```

The standard `2`-power positive zero-sum lemma says that a subset of
`mu_{2^m}` with first power sum zero is antipodally balanced.  Applying this
iteratively after each quotient by `x -> x^2` proves that `S` is a union of
`h`-cosets.

Therefore:

```text
if h does not divide j, the exact lifted fiber is empty;
if h divides j, it descends bijectively to the quotient rung
    (n/h, j/h, floor(w/h)).
```

For finite KoalaBear fibers, the theorem is used with a generated-prefix
first-match wrapper.  If a finite support has

```text
lambda_d^F(S)=0
```

for `d<=h/2` but the honest lift satisfies

```text
lambda_d^K(S) != 0 in Z[zeta_n],
```

then the support is a generated-field prefix-coordinate collision.  Across all
applicable `h`, the first such `d` lies in `1<=d<=w`, so the image-cell count is
bounded by

```text
w*p = 143760893740943 <= t*p = 143763024447376.
```

This finite use is conditional on the generated-field first-match bucket being
scoped to include prefix-coordinate lift collisions.  It is an image-cell
cover, not a raw support bound.

For the deployed row,

```text
j = 981104 = 2^4 * 17 * 3607.
```

Thus the exact lifted outcomes are:

```text
h = 2,4,8,16:
  quotient descent to (n/h, j/h, floor(w/h)).

h = 32,64,128,...,131072:
  empty after generated-prefix collision removal, because h does not divide j.

h >= 262144:
  theorem not applicable, because h/2 > w.
```

So once primitive-heavy-orbit exclusion activates Q2 stabilizer forcing,
stabilized targets are no longer unstructured top-rung primitive mass: they
either descend to the Q0 quotient rungs `h=2,4,8,16`, or vanish in the exact
lift after generated prefix collisions are stripped.

The remaining Q2 path can therefore be stated as a conditional closure theorem.
Let `R_pre(z)` be the residual fiber after all first-match branches before Q2
have been removed, and set

```text
T_Q2 = 4805007 * binom(n,j) / p^w.
```

For a dyadic `h`, define

```text
H_h = { z : |R_pre(z)| > T_Q2 }.
```

The stronger global fewness certificate

```text
|H_h| <= n/h,
```

then Q2 stabilizer forcing makes every threatening target `h`-stabilized.  The
generated-prefix first-match bucket then removes every support whose lifted
prefix differs from the retained exact lift over the same finite target.  On
the remaining exact lifted fiber, the folding theorem above applies.

This is sufficient but stronger than necessary.  The exact Q2 trigger is the
orbitwise certificate

```text
Primitive-heavy-orbit exclusion:
if Stab(z) is trivial, then |R_pre(z)| <= T_Q2.
```

Equivalently, no trivial-stabilizer target orbit is heavy.  Once this holds,
every threatening target has nontrivial dyadic stabilizer, so Q2 folding
applies.  The certificate should therefore target primitive-heavy-orbit
exclusion directly; `|H_h|<=n/h` is only one possible, overstrong way to prove
it.

For heavy-target generated-prefix cells indexed by `(z,d)`, the count is

```text
B_gen_prefix_heavy <= |H_h| * w <= (n/h) * w.
```

At the first useful scale `h=2`,

```text
(n/2) * w = 1048576 * 67471 = 70748471296.
```

This is far below the existing generated allowance

```text
t*p = 143763024447376.
```

If these prefix-coordinate lift collisions are explicitly coalesced into the
generated first-match bucket, no new deduction is needed.  If they are treated
as a separate paid branch, this worst-case deduction drops the top multiplier
from

```text
4805007 to 4805006.
```

Do not silently double-use the generated allowance: the certificate must say
which generated row universe contains these prefix-coordinate cells.

There is a tempting stronger route: for each finite target `z`, retain one exact
lifted prefix class and send every other exact lifted class over the same `z` to
generated-prefix collisions.  If such a lift-class bucket were proved as a
finite first-match support payment, every residual finite fiber would lie in one
exact lifted cyclotomic fiber.  The exact-lift terminal-16 bound below would
then give

```text
|R_pre(z)| <= 11440
```

for every target `z`, so no target would be heavy at all.  This packet does not
mark that route as proved: the assignment depends on the finite target and its
retained exact lift class, while a row-indexed `w*p` image-cell count does not
by itself bound the number of removed exact lift classes or raw supports.

This is a real support-vs-image obstruction, not just a missing phrase.  A
small replay over `F_17` with `n=16`, `D=<3>`, `j=8`, and `w=1` takes the
primitive finite target `z=1`.  Direct enumeration gives

```text
finite fiber size over z=1:                757
number of exact Q(zeta_16) lift classes:   193
largest exact lift class:                   20
non-retained supports after keeping largest exact class: 737
w*p:                                        17
```

Thus non-retained exact lift classes can be labelled by genuine generated
prefix-coordinate collisions, but their support multiplicity is not paid by the
image-cell count.  The deployed theorem still needs a support/fiber
multiplicity certificate, or an equivalent primitive orbitwise flatness
certificate.

The failed-route evidence should be recorded with this same status split:

| route | status | key diagnostic |
| --- | --- | --- |
| Route A / Delsarte-distance | `OPEN_MISSING_ROUTE_A_DUAL_EXCESS_CERTIFICATE` | Q1/distance-only information leaves a Gilbert-style lower-bound gap of about `1,368,895` bits versus `t*p`. |
| Route B / split-pair rank | `PROVED_LOCAL_FULL_ROW_RANK_ONLY_INSUFFICIENT` | The Vandermonde pivot gives local row rank `w`, but at `e=w+1` the remaining nullity is still `1` and the naive global count is astronomically above `t*p`. |
| Route C / primitive excess | `OPEN_REQUIRED_PRIMITIVE_EXCESS_CERTIFICATE` | The excess-to-tuple amplification is formal, but no certificate proves `sum_{primitive O} X_O^3=0` or `sum_{primitive O} X_O^4=0`. |
| Route D / folding defect | `OPEN_MISSING_ROUTE_D_FOLDING_DEFECT_SUPPORT_CERTIFICATE` | Folding identities and small signed-defect emptiness are proved, but the first allowed nonzero signed defect has size `33737`, and large-defect multiplicity is still unpaid. |

Route D is the most useful next structure.  Its missing theorem is:

```text
Large signed folding-defect transfer:
every large signed defect satisfying the odd prefix equations is either
quotient-descended, sparse/Pade-Hankel, M1/half-turn/window-shadow, rank-drop
with printed pivot cost, generated-field support-paid, or bounded in a
primitive full-rank defect stratum by <= t*p.
```

For the four quotient-descended Q2 rungs, the exact-lift terminal-16 certificate
also closes the lifted fibers.  Each row has

```text
W >= N/32.
```

Thus equality of the first `W` prefix coefficients forces the difference mask
to be divisible by

```text
(X^N - 1)/(X^16 - 1),
```

so exact lifted fibers differ only by whole terminal residue classes modulo
`16`.  Since `floor(J/(N/16))=7` in each row, every exact lifted fiber has size
at most

```text
binom(16,7) = 11440.
```

The Q2 descended rows are:

| `h` | `N=n/h` | `J=j/h` | `W=floor(w/h)` | `K_h` | exact-lift bound |
| --: | ------: | ------: | -------------: | ----: | ---------------: |
| 2 | 1048576 | 490552 | 33735 | 749194961 | 11440 |
| 4 | 524288 | 245276 | 16867 | 7866613560 | 11440 |
| 8 | 262144 | 122638 | 8433 | 21435171266 | 11440 |
| 16 | 131072 | 61319 | 4216 | 29753587796 | 11440 |

These are exact-lift certificates.  Finite use still requires the
generated-prefix lift-collision bucket described above.

What remains of Q2 is now the orbitwise quantitative trigger and finite bucket
scoping:

```text
1. Use Q1 and exact r=3,4 collision ledgers to prove primitive-heavy-orbit
   exclusion at the threshold T_Q2.
2. Prove a support-level generated-prefix multiplicity certificate for
   non-retained exact lift classes, or an equivalent primitive orbitwise
   flatness certificate.  A sufficient deployed bound is
   (|G_gen_prefix(z)|+11440)*p^67471 <=
   4805007*binom(2097152,981104) for every primitive target z.
3. Pursue Route D: prove the large signed folding-defect transfer theorem,
   with every large defect either quotient-descended, sparse/Pade-Hankel,
   M1/half-turn/window-shadow, rank-drop with printed pivot cost,
   generated-field support-paid, or bounded in a primitive full-rank defect
   stratum by <= t*p.  If this fails, produce a counterpacket.
```

This matches the experimental evidence: finite `{1,3}`/`{1,4}` extras are
generated-field collisions, quotient mass must be image-descended rather than
support-counted, and mode-at-null is not reliable enough for the finite adjacent
row.

Q1 distance alone cannot prove the remaining target.  If `e=w+1=67472`, the
Johnson ball of one-sided radius `e-1` has

```text
log2 V ~= 721930.785,
log2 binom(n,j) ~= 2090873.280,
log2 greedy distance-code lower bound ~= 1368942.495.
```

By contrast,

```text
log2(n*T_Q2) ~= 78.931.
```

So the split-prefix distance gap leaves astronomical room at the level of
abstract constant-weight packings.  The missing theorem must use the actual
moment-curve algebra and first-match branch structure, not distance alone.

## Relation to current v13 threshold PRs

- PRs #372 and #374: this packet agrees that the adjacent arithmetic and
  lower-side margins are audited, but does not instantiate a complete
  one-step `U(1116048)` upper certificate.
- PRs #366 and #384: Q moment/head/packing routes are not used here as
  closures.  Q1/Q2 entries are structural inputs plus failed-route evidence.
- PR #380: composite Q-prefix multiplicity must be read with quotient scale
  `c = gcd(e,N)` after rebase.  This packet keeps composite directions as
  lower-rung or open residual obligations.
- PRs #369, #378, and #383: BC floors, orientation facts, and saturated-budget
  fits are not consumed here as paid upper cells.
- PRs #376 and #375: SP remains a primitive shift-pair residual after
  quotient-scale subclasses are deleted or paid; no SP upper payment is taken.
- PRs #367 and draft #355: the M1 material used here is structural
  coefficient-window routing.  It is separate from the `a=327`, `mu_8`,
  `INTERLEAVED_LIST`, non-MCA route-cut lane.

## Nonclaims

- This note does not prove `U(1116048) <= B*`.
- This note does not prove the KoalaBear MCA first-safe agreement.
- This note does not prove primitive Q-fin max-orbit flatness.
- This note does not prove extension-valued slope safety over `F_{p^6}`.
- This note does not prove lower-rung quotient/planted max-fiber bounds for
  `c=2,...,32768`.
- This note does not prove arbitrary planted-tail bounds for `c>=262144`.
- This note does not supply sparse-sigma bounds.
- This note does not close arbitrary M1 row-slice compression.
- This note does not prove finite-field lift-class removal at cost `w*p` for
  prefix-vector fibers.
- This note does not prove support multiplicity bounds for non-retained
  generated-prefix exact lift classes.
- This note does not prove primitive-heavy-orbit exclusion needed to activate
  Q2 stabilizer forcing.
- This note does not bound raw support multiplicity inside a generated-field
  image cell.
