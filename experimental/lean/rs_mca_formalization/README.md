# Lean Formalization Starter

This directory starts a small Lean 4 formalization for the rs-mca project.
It is deliberately stdlib-only: no `mathlib` dependency is required.

The first module, `RsMca.Basic`, formalizes:

- proof-status labels used by the agent ledger;
- words over a finite domain and agreement on a support;
- support-wise line-MCA bad-support predicates, parameterized by an abstract
  line-combination operation;
- quotient-locator parameter arithmetic, including the identity
  `supportSize = a * ell` when `k = a * rank` and `ell = rank + 1`;
- a minimal script-certificate record matching the `agents.md` output standard.

The second module, `RsMca.DeepPoint`, formalizes the quantitative cores of the
X1/L2 forward interleaved deep-point bridge
(`notes/x1/x1_deep_point_interleaved_bridge.md`):

- the deep-image membership predicate (§1-§2);
- the `K_{m,m}` clique-amplification cap arithmetic (§2.6 C):
  `cliqueGridSize m a k = k + m^2 (a-k)`, with `cliqueSupport_over_a` proving the
  support exceeds `a` for `m >= 2`, `a > k` (two-sided over-agreement), and
  `cliqueGridSize_mono`;
- the conditional-budget exponent arithmetic (§2.6 R, §2.8):
  `listExponent_areg_le_worst` (a-regular exponent `1 <= mu`) and
  `budgetClears_mono` (an L1 bound clearing the budget at `mu` clears it
  a-regularly).

- the `mu`-independent collision bound (`simultaneousCollision_le_k`,
  `collision_bound_mu_independent`);
- the exact statements `DeepPointIdentity` and `ARegularCollapse` (recorded as
  `Prop`s; their finite-field/finite-set proofs need `mathlib` and are left as
  targets).

All `RsMca.DeepPoint` theorems are proved (no `sorry`); the two `Prop`-valued
statements (`DeepPointIdentity`, `ARegularCollapse`) record exact claims whose
proofs are the formalization targets.

The third module, `RsMca.HighAgreementLedger`, formalizes the stdlib-only
*integer ledger* arithmetic of the high-agreement tangent staircase
(`notes/high_agreement/tangent_staircase.tex`,
`data/generalized-ledgers/generalized_high_agreement_ledgers_summary.md`):

- the exact-range equivalence `tangentExact_iff_radius`
  (`3a - 2n >= k  <->  3 r <= R`, with `r = n-a`, `R = n-k`);
- the line / degree-`d` curve / interleaved numerators, `line_is_degree_one`,
  and monotonicity in the radius `r`;
- the `2^-128` safety gate `certified N Q := N <= B_Q` (`B_Q = floor(Q/2^128)`),
  with `line_first_unsafe` (first unsafe line radius is exactly `r = B_Q`) and
  `lineListSafe_iff` (`r <= B_Q - 2` for a line plus one interleaved-list term);
- the exact `F_{17^32}`, rate-`1/2` row (`n=512, k=256`): `f17_BQ_eq`
  (`floor(17^32/2^128) = 6`), `f17_bracket` (the 39-digit
  `6*2^128 < 17^32 < 7*2^128`), `f17_staircase` (agreement `507` clears the
  budget, `506` does not), and `f17_largest_safe_radius` (largest safe integer
  radius `5`).

All `RsMca.HighAgreementLedger` theorems are proved (no `sorry`). The concrete
numeric certificates are proved by kernel `decide` (not `native_decide`) and
`#print axioms` reports they depend on no axioms at all; the symbolic theorems
use only `[propext, Classical.choice, Quot.sound]`. This is a coding-ledger
certificate: it carries `LD_sw` as a definition and adds no protocol error term.

The fourth module, `RsMca.QuotientOverlap`, formalizes the stdlib-only
size/threshold arithmetic of the whole-fiber strict-overlap reduction
(`notes/m1/m1_quotient_periodic_overlap_profile.md`): with a domain split into
`N` fibers of size `m`, a whole-fiber support has size `L*m` and two such
supports differ by `|S\T| = h*m`, `|S∩T| = (L-h)*m`. At agreement `s = k+t`:

- `strict_overlap_iff` (strict overlap `|S∩T| > k` is exactly `|S\T| < t`);
- `no_strict_when_t_le_m` / `not_strict_when_t_le_m` (no strict high-overlap
  pairs when `t <= m`);
- `strict_needs_t_gt_fiber` (the first correction needs `t >= m+1`) and
  `first_band_unique` (in the band `m < t <= 2m` only `h = 1` is strict);
- `active_scale_iff` (an exchange scale `h` is strict-active iff
  `h <= floor((t-1)/m)`);
- `fiberSize_dvd_support` (the family is empty unless `m | s`).

All `RsMca.QuotientOverlap` theorems are proved (no `sorry`; `no_strict_when_t_le_m`
is axiom-free). The binomial COUNT identities (`|A_QP| = C(N,L)`, the Johnson
exchange profile) are the note's combinatorial content and need `Mathlib`; only
the size/threshold arithmetic the M1 reduction consumes is certified here.

## Build

```sh
cd experimental/lean/rs_mca_formalization
lake build
```

This is not a formal proof of the main rs-mca theorems. It is a typed starting
point for later agents to connect finite script certificates and locator
identities to theorem statements.
