# Row-sharp Q Singleton-Heavy Top-Seam Route-D Packet v1

Status: `CONDITIONAL_ON_WEIGHTED_PRIMITIVE_SP_PADE_BOUND_AND_PLANTED_CORE_COST_BOUND_AND_STRICT_DISTANCE_AND_ROW_BUDGET_SCOPE`.

This packet records the local Route-D singleton-heavy top-seam compiler
extracted from the proof attempts. It does **not** prove `U(1116048) <= B*`,
does **not** certify the KoalaBear MCA first-safe agreement, and does **not**
prove the row-sharp Q-prefix atom theorem until the named branch payments,
finite weighted primitive SP/Padé bound, and row-budget scope below are
formalized with printed costs.

## Nonclaims

- U(1116048) <= B*
- KoalaBear MCA first-safe agreement
- row-sharp Q-prefix atom theorem without branch-payment realization
- zero-cost repeated side-pair deletion
- planted core-fiber cost bound |G_{beta,A}|-1
- finite numerical bound for weighted primitive SP/Pade certificates emitted by Rule 2
- strict-distance child payment unless it is already a named paid branch
- all-depth Route-D row-cell payment without the row-budget hypothesis |R_D|<=t
- a promoted Paper-D theorem

## Deployed Row

```text
p = 2130706433
n = 2097152
k = 1048576
agreement = 1116048
j = 981104
t = 67472
w = 67471
K_rem = 4805007
```

## Interaction with Open Q/Entropy/BC PRs

- `#414` (signed-e_m inverse / participation-ratio bound): keeps raw versus masked residual accounting separate; does not convert masked participation-ratio material into Row-sharp Q proof.
- `#416/#417` (masked participation ratio and lift-class cost model): does not rely on the lift-class cost model refuted by #417.
- `#418` (Lean correspondence audit): does not introduce Lean theorem-label dependencies or claim lake build/correspondence closure.
- `#419` (BC near-pencil split-in-subspace residual): treats the fixed-key split-shift residual as a shared unresolved object, not as a solved BC/SP payment.
- `#420/#421/#422` (entropy-inverse missing-cell and F_p-span cell): does not claim entropy-inverse removal-list completeness; #422-style F_p-span normalization remains adjacent open context.
- `#423` (KB-MCA Route-D residual support certificate): records a local singleton-heavy top-seam compiler and does not supersede a full Route-D residual support certificate.
- `#424` (row-sharp Q moment floor audit): does not use a moment-floor route as a closure; the weighted primitive SP/Pade and row-budget obligations remain explicit.

## Step 1: Exact Scope

The Route-D charged row set is:

```text
R_D = {rho(B): B contributes an unpaid top-seam Route-D branch-excess unit}, where rho(B)=m(B)+1.
|R_D| <= t
```

The budgeted all-depth compiler theorem is conditional on:

- top-seam scope: `e(B)=rho(B) for every singleton-heavy top-seam bucket B`
- row-budget scope: `|R_D| <= t`
- branch realization: `strict_distance_child is a genuine named paid first-match branch; repeated_side_pair_reuse is accounted for by the planted-switch core-fiber ledger; cross_pair_multiplicity_aware_sp_pade realizes same-cell distinct-U packets as marked weighted SP/Padé certificates with exact support cost, but still requires a printed finite weighted primitive SP/Padé bound.`

It concludes:

```text
sum_B(outdeg_unpaid(B)-1) <= |R_D|*(p-1) <= t*(p-1)
```

The first-exposed local specialization has `rho=w+1=t` and avoids the
row-budget issue, but it pays only first-exposed top-seam nodes.

## Step 2: Formal Branch Predicates

Common data are a branch-excess unit `(B,C)` and a canonical top-seam
boundary packet `Pi(B,C)=(r,c,G,U,V;S,S')`, with source side inside
the charged child and target side outside it.

### cross_pair_multiplicity_aware_sp_pade

Input: `two canonical packets Pi0, Pi with the same cell (r,c) and U != U0`

Predicate: `L_+=U0*(U-c), L_-=(U0-c)*U; after H=gcd(L_+,L_-), M_+=L_+/H and M_-=L_-/H are split, coprime, nonidentical, and deg(M_+-M_-) <= E-r-1 where E=deg(M_+)=deg(M_-).`

First-match priority: `P3`.

Paid/residual status: Rule 2 is realized as a marked multiplicity-aware SP/Padé certificate with exact support cost. The finite numerical payment remains conditional on a printed weighted primitive SP/Padé bound.

Route-D cell cost: `0`.

Dedup key: `(r,c)`.

### repeated_side_pair_reuse

Input: `two canonical packets Pi_min, Pi with the same planted-switch key (r,c,U,beta)`

Predicate: `r_min=r, c_min=c, U_min=U, beta_min=beta, and G_min != G`

First-match priority: `P2`.

Paid/residual status: Rule 1 is proved as exact planted-switch core-fiber descent.  It is paid exactly to the extent that the planted-core fiber ledger includes the printed cost |G_{beta,A}|-1.

Route-D cell cost: `0`.

Dedup key: `(r,c,U,beta)`.

Planted-switch cost: `1 per deleted repeated packet, aggregated as |G_{beta,A}|-1`.

### residual_route_d_cell_charge

Input: `canonical packet surviving P1-P3`

Predicate: `packet survives all earlier predicates and is charged to cell (r,c)`

First-match priority: `P4`.

Paid/residual status: r in R_D and |R_D| <= t

Route-D cell cost: `1`.

Dedup key: `n/a`.

### strict_distance_child

Input: `branch-excess unit (B,C), r=rho(B)`

Predicate: `d(S,S')=|S\S'| >= r+1 for every S in C and S' in B\C`

First-match priority: `P1`.

Paid/residual status: Paid only if the strict-distance Route-D/RIM/window-shadow payment theorem is imported; otherwise remains conditional residual.

Route-D cell cost: `0`.

Dedup key: `(B,C)`.

First-match order for this layer:

0. `earlier_global_first_match_branches`
1. `strict_distance_child(B,C)`
2. `construct canonical packet Pi(B,C)`
3. `repeated_side_pair_reuse / planted_switch_core_fiber(Pi_min_key, Pi)`
4. `cross_pair_multiplicity_aware_sp_pade(Pi_min_cell, Pi)`
5. `residual_route_d_cell_charge(Pi)`

## Step 3: Rule 1 Planted-Switch Descent

Status: `RULE_1_PROVED_AS_EXACT_PLANTED_SWITCH_DESCENT`.

Cost status: `RULE_1_COST_REQUIRES_PLANTED_CORE_LEDGER`.

Rule 1 is not a zero-cost row-cell deletion. If two packets reuse the
same side switch, then the repeated mass is exactly free variation of
the marked core inside a planted core prefix fiber.

For side data:

```text
A = Roots(U)
B = Roots(U-c)
Omega_AB = Omega \ (A union B)
```

The planted switch preserves rows before the seam and crosses row `r`:

```text
P_k(A)=P_k(B) for 1 <= k <= r-1
P_r(A)-P_r(B)=-r*c != 0
```

For parent prefix `beta`, repeated packets with fixed key are in
bijection with:

```text
G_{beta,A}={G subset Omega_AB: |G|=j-r and P_k(G)=beta_k-P_k(A) for 1<=k<=r-1}
```

The corrected all-depth dedup key is:

```text
(r,c,U,beta)
```

For the first exposed seam only, `(r,c,U)` is safe because `beta=z`
is fixed globally. For all-depth nodes, omitting `beta` silently
merges different core fibers.

Cost model:

```text
Route-D row-cell cost = 0
deleted repeated packet cost = 1
aggregate planted-switch cost = |G_{beta,A}|-1
```

Thus Rule 1 is proved as planted descent, while the PR remains
conditional until the planted/core ledger prints and accepts that
support cost.

## Step 4: Rule 2 Multiplicity-Aware SP/Padé Realization

Status: `RULE_2_MULTIPLICITY_AWARE_SP_PADE_REALIZED_WITH_EXACT_SUPPORT_COST`.

Payment status: `FINITE_WEIGHTED_PRIMITIVE_SP_BOUND_STILL_REQUIRED`.

For two same-cell packets with `U != U0`, construct:

```text
L_+ = U0*(U-c)
L_- = (U0-c)*U
L_+ - L_- = c*(U-U0)
```

After cancellation by `H=gcd(L_+,L_-)`, write `L_+=H*M_+` and
`L_-=H*M_-`.  The reduced pair satisfies:

```text
deg(M_plus-M_minus) <= E-r-1
```

Thus `(M_+,M_-)` is a multiplicity-aware depth-`r` weighted
SP/shift-pair normal form.  Squarefreeness is not required.  The same
degree inequality gives the finite Padé/Hankel moment certificate
`sum_a m_+(a)a^k = sum_a m_-(a)a^k` for `0<=k<=r`.

```text
certificate key = (r,c,U0,G,H,M_plus,M_minus)
U = H*M_minus/(U0-c); V=U-c; marked core G recovers the deleted packet
cost = 1 support unit per marked multiplicity-aware SP/Padé certificate
```

So Rule 2 is now an unconditional multiplicity-aware branch realization
with exact support cost.  It is not yet a finite numerical payment
bound: the weighted primitive SP/Padé certificates still need a printed
ledger bound after the earlier first-match deletions.

### Step 4b: Weighted SP/Padé Dichotomy

Status: `WEIGHTED_SP_PADE_DICHOTOMY_PROVED_FULL_RANK_PRIMITIVE_COUNT_REQUIRED`.

For the signed weight `mu(a)=ord_a(M_+) - ord_a(M_-)` on
`D=supp(mu)`, the Padé normal form is:

```text
F_mu(Y)=Y^(r+1)*R_D(Y)/Q_D(Y), Q_D(Y)=prod_{a in D}(1-aY)
s=|D|-r-1 and deg R_D <= s-1
```

The first-match alternatives are:

- `support_collapse_or_common_divisor`: `|D| <= r+1`; impossible for nonzero reduced mu; route to cancellation/common-divisor if produced upstream.
- `extension_slope`: `R_D(0)=0, equivalently mu_{r+1}=0`; certificate extends from depth r to depth r+1.
- `rim_rank_drop_pivot`: `canonical RIM/Hankel pivot vanishes`; route to rank_drop_pivot branch.
- `bc_corank_one_chart`: `|D|=r+2 and the pivot is nonzero`; one-dimensional barycentric nullvector / BC chart.
- `structural_quotient_complete_common_planted`: `quotient-pullback, complete-fiber, common-divisor, or planted-core structure is present`; route to the corresponding named structural branch.
- `full_rank_primitive_weighted_stratum`: `|D|>=r+3, R_D(0)!=0, pivot nonzero, and no structural first-match predicate applies`; finite support-level chart count N_WSP_full(z) remains to be printed.

The final full-rank primitive weighted stratum is finite and support-level.
A canonical full-rank chart uses:

```text
(r,c,U0,G,H,D,P,mu_F)
mu_P=-V_P^{-1}V_F*mu_F
remaining count = N_WSP_full(z)
```

This dichotomy isolates the remaining numeric theorem. It does not bound
`N_WSP_full(z)` by itself.

### Step 4c: Fixed-Key Split-Shift Normal Form

Status: `FULL_RANK_WSP_REDUCED_TO_SPLIT_SHIFT_FLATNESS_PRINTED_FINITE_COUNT_REQUIRED`.

Rule-2 origin still gives a small-weight constraint:

```text
Because L_plus and L_minus are products of two squarefree degree-r locators, residual multiplicities in M_plus and M_minus are at most 2; hence mu(a) in {-2,-1,0,1,2}.
```

The sharper fixed-key normal form is:

```text
(r,c,U0,H), with V0=U0-c
H_A=gcd(H,U0)
H_B=gcd(H,U0-c)
H=H_A*H_B for exact same-key Rule-2 gcd data
U0=H_A*U0_prime
U0-c=H_B*V0_prime
U=U0+H*K
U-c=U0-c+H*K
deg K <= r-deg(H)-1
```

In this form the SP/Padé equation adds no further hidden rigidity:

```text
With M_plus=U0_prime*(V0_prime+H_A*K) and M_minus=V0_prime*(U0_prime+H_B*K), one has M_plus-M_minus=c*K.  Thus the weighted SP/Pade degree condition is exactly the degree bound on K.
```

The remaining fixed-key set is:

```text
X_{r,c,U0,H,beta}(z)
deg K <= r-deg(H)-1
U0+H*K is monic squarefree split degree r over Omega
U0-c+H*K is monic squarefree split degree r over Omega
the cross-pair gcd is exactly H
G satisfies parent-prefix compatibility for beta
all primitive first-match filters fail
```

Support-core constraints:

```text
G subset Omega \ (Roots(U) union Roots(U-c))
|G|=j-r
P_k(G)=beta_k-P_k(Roots(U)) for 1<=k<=r-1
```

The reduction also records why a shape-only proof cannot close the count:

```text
parameters: r=1, H=1, U0=X-a0, U=X-a
certificate: L_plus=(X-a0)(X-a-c), L_minus=(X-a0-c)(X-a), L_plus-L_minus=c*(a0-a)
lesson: SP/Pade shape alone allows many same-key full-rank split-shift members; a KB proof needs a finite split-locator flatness ledger or a new deletion branch.
```

The remaining finite split-shift ledger is:

```text
N_WSP_full(z) = sum_{r,c,U0,H,beta} |X_{r,c,U0,H,beta}(z)| after canonical first-match partitioning
prove sum_{r,c,U0,H,beta} |X_{r,c,U0,H,beta}(z)| <= B_WSP_full with printed constants
```

This proves the support-level fixed-key split-shift reduction. It does not
provide the small printed bound for the total fixed-key `K`-pencil count.

## Proved Local Content

Lemma A is a local proof that every singleton child of a top-seam bucket
either has a canonical distance-`r` top-seam witness or is strict-distance
separated from the rest of the bucket.

Lemma B verifies the algebraic same-cell collision guard.  The load-bearing
identity is:

```text
U0*(U-c) - (U0-c)*U = c*(U-U0)
```

Since `U0` and `U` are monic degree `r`, `deg(U-U0) <= r-1`. Step 4
upgrades this from a raw degree identity to a marked multiplicity-aware
SP/Padé-Hankel certificate after cancellation. The certificate carries
exact support cost one, but the finite adjacent row still needs the
weighted primitive SP/Padé ledger bound.

The same-side-polynomial case is now handled by Step 3 as a planted
switch core-fiber descent, with support cost charged to the planted/core
ledger rather than to a Route-D row cell.

Lemma C is the counting compiler: choose one canonical base child in each
unpaid top-seam bucket, assign every other surviving child a canonical
top-seam packet, and inject surviving packets into cells `(r,c)`.

## Required Branch Realization

### planted_switch_core_fiber_cost

Status: `RULE_1_PROVED_AS_PLANTED_DESCENT_OPEN_REQUIRED_PLANTED_CORE_LEDGER`.

Repeated side-pair reuse with key (r,c,U,beta) is exactly the planted core fiber G_{beta,A}.  The noncanonical repeats are removed from Route-D row-cell mass, but their printed support cost |G_{beta,A}|-1 must be included in a planted/core ledger.

Risk: The descent is proved, but it is not zero-cost and cannot be hidden inside image-cell accounting.

### weighted_primitive_sp_pade_bound

Status: `RULE_2_MULTIPLICITY_AWARE_REALIZED_OPEN_REQUIRED_WEIGHTED_PRIMITIVE_SP_BOUND`.

If U != U0 in a common cell (r,c), cancellation produces a marked multiplicity-aware SP/Pade certificate (r,c,U0,G,H,M_+,M_-) with deg(M_+-M_-) <= E-r-1 and exact support cost one.  The weighted SP/Pade dichotomy first-matches cancellation/common-divisor, extension-slope, RIM rank-drop, BC corank-one, and structural quotient/planted classes.  The full-rank primitive residual reduces to fixed-key split-shift sets X_{r,c,U0,H,beta}(z).  The finite ledger still needs a printed bound for their total count, equivalently for N_WSP_full(z).

Risk: Exact support-cost realization is not the same as a small printed finite adjacent bound.

### strict_distance_child

Status: `OPEN_REQUIRED_BRANCH_PAYMENT_CHECK`.

A child separated from the rest of a top-seam bucket by distance at least r+1 is already paid or routed by strict-distance Route-D/RIM/window-shadow rules.

Risk: If not already a named branch, this is a new payment obligation.

### charged_row_budget

Status: `OPEN_REQUIRED_SCOPE_CHECK`.

All charged top-seam rows r used by the compiler lie in a row set of size at most t, or the theorem is explicitly restricted to the first exposed seam.

Risk: Without this, the cell count t*(p-1) does not follow.

## Conditional Counting Closure

If the branch-realization checks hold and `|R_D| <= t`, then:

```text
sum_B(outdeg_unpaid(B)-1) <= |R_D|*(p-1) <= t*(p-1)
unpaid supports <= 1 + t*(p-1) <= t*p
```

For the deployed row:

```text
t*p = 143763024447376
retained exact-lift bound = 11440
t*p + retained = 143763024458816
target floor = 274836936291722953
integer slack = 274693173267264137
integer slack bits = 57.930598670
multiplicative gap bits = 10.900667525
```

## PR Use

This is a useful PR packet because it turns the latest proof attempts into
a narrow formalization target.  It should be reviewed as a conditional
Route-D compiler and branch-predicate checklist, not as a complete safe-side
upper ledger.
