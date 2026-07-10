# Necessary hypotheses for finite-prize census statements
# (three counterexample families, each excluded by a named guard)

- **Status:** PROVED (counterexample constructions + exact replays).
- **Track:** the FINITE prize (not the asymptotic paper). Safe to
  park until the finite pivot.
- **Source:** the fork's finite-track campaign; full record at
  https://github.com/AllenGrahamHart/rs-mca-prize-dag
  (notes/kernel_basis/, SOL_TARGET_3*). Constructions due to
  GPT-5.6 attack rounds against our public targets; replayed and
  banked by us the same day.
- **Verifier:** `python3 experimental/scripts/verify_finite_census_necessary_hypotheses.py`

## Why this note exists

Whoever writes the first finite-prize census statement (extras
bounds for t-null blocks of mu_N) will face three traps. Each is
now a THEOREM-GRADE counterexample family, and each is excluded by
a specific hypothesis. Statements missing any one of the guards
are FALSE. (This is the census-side sibling of the C9 lesson:
"exact residual predicate, not vague survival language.")

## Trap 1 — characteristic-divisible moment indices (guard: p-free
## effective conditions)

In characteristic p, p_{pi} = (p_i)^p: conditions at p-divisible
indices are REDUNDANT. Effective condition count t*_eff =
#{p-free i <= t}, and any sub-balance hypothesis must read
|B0|^{t*_eff} >= 2^N at the GENERATED field B0 = F_p(D).
COUNTEREXAMPLE (char 3): eta in mu_16 of F_81 a root of
X^4 + X^2 - 1; E = {0,1,2,8,10,11,13}; B = {eta^e} has
p_1(B) = p_2(B) = 0 exactly (verifier), and p_3 = p_1^3 = 0 free.
Per-mu_16-coset rotations in mu_512(F_{3^128}) give 16^32 = 2^128
"3-null" primitive blocks at a row whose NAIVE balance test
|K|^3 = 3^384 > 2^512 passes. The p-free reading gives t*_eff = 2
and 3^256 < 2^512: the row is correctly excluded.

## Trap 2 — tensor/level-lift amplification (guard: the aspect
## ratio)

THEOREM (necessity of the aspect guard). Generated-field p-free
sub-balance does NOT imply the N^3 census bound. Explicitly:
omega in F_{7^4} a root of X^4 - X^2 - 1 (order 32);
E = {0,1,2,3,5,9,11,15,16,18,23}; the block B = {omega^e} is
5-null (p_1..p_5 = 0, verifier), as is its 21-element complement.
At K_N = F_{7^{N/8}}, D = mu_N, independent per-mu_32-coset choices
of rotations/complements give 64^{N/32} = 2^{3N/16} five-null
blocks that are unions of no mu_M-cosets (odd local intersections).
All hypotheses of trap 1's guard hold (t*_eff = 5, sub-balance
passes), yet the count beats N^3 from N = 128 onward. The family
crosses super-budget EXACTLY where log|B0| / log N exceeds the
official aspect 256/41 = 6.244 (verifier prints the table; the
aspect-valid scale N = 64 is sub-budget). Hence the aspect guard
  |B0|^41 <= N^256
(or the official parameters themselves) is LOAD-BEARING in any
finite census statement; "official-like scaled rows" must be
defined aspect-respecting.

## Trap 3 — boundary-scale lifts (guard: pay the M_0 class, or
## strip it)

For M | N and A a subset of mu_{N/M}-quotient values, the lift
B_A = {x in mu_N : x^M in A} satisfies p_i(B_A) = 0 for all
i != M below 2M, and p_M(B_A) = M * sum(A) (verifier, exact).
So zero-sum quotient subsets lift to t-null blocks for any t < 2M
that are NOT coset unions of scale > t when A is not antipodal.
At N = 2^41, t ~ 2^33..2^34 this class has size ~2^{2^8} unless
paid or stripped. Any census statement must either subtract the
boundary-scale class (unions of mu_{M_0}-cosets with zero-sum
quotient pattern, M_0 = 2^{floor log2 t}) explicitly, or restrict
to a primitivity predicate that excludes all 2-power-coset unions
up to scale M_0.

## Non-claims

No positive census bound is asserted here. The correctly guarded
finite census conjecture (all three guards + the primitivity
predicate + two-sided complement-weighted counting) is posed at
the fork as TARGET 3C and is open; it survived an adversarial
checklist in which each family above provably fails its
hypotheses.
