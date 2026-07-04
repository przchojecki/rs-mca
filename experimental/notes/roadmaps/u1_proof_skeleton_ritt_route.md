# U1 proof skeleton — the Ritt/Lang route (roadmap-lane attempt)

- **Status:** PROOF SKELETON / two named gaps. Steps 1-2 are complete
  proofs (elementary); step 3 is a route through two classical
  imports with [CITATION NEEDED] markers; gaps alpha, beta are open.
- **Provenance:** roadmap-lane attempt (Fable), 2026-07-04, at user
  request. Everything below re-derivable from the statements.

## Step 1 (PROVED, one line): minimal trades are fibers, tautologically
A canonical trade with |P| = |Q| = t+1 has deg(L_P - L_Q) <= 0, so
L_P = L_Q - c: P = psi_Q^{-1}(c) for the degree-(t+1) polynomial map
psi_Q := L_Q. Fiber structure is FORCED at minimal size; U1's content
at h = t+1 is map-clustering, nothing else.

## Step 2 (PROVED, two lines): abundance = composite divisibility
K full fibers of one psi inside D = gamma mu_n (coset polynomial
X^n - delta): with G(Y) = prod(Y - y_i),
    G(psi(X)) | X^n - delta,     deg = K(t+1).
(All roots in D, distinct across disjoint fibers; critical fibers
cost <= t exceptions.)

## Step 3 (ROUTE, two classical imports):
(i) FEW-FIBER BOUND for non-structured maps: full fibers give
    ~K^2 t^2 / 2 points of the fiber-product curve psi(x) = psi(y)
    on mu_n x mu_n; subgroup-points-on-curves bounds
    [CITATION NEEDED: Ostafe/Shparlinski-type, F_q curves on small
    multiplicative subgroups, non-toral components <=
    deg^{O(1)} n^{2/3} points] cap K <= deg^{O(1)} n^{1/3}-ish for
    maps whose fiber-product has no toral component.
(ii) STRUCTURED = DICTIONARY: toral components (x^a y^b = c) of the
    fiber-product force monomial/Dickson structure of psi; TAME RITT
    [CITATION NEEDED: polynomial decomposition over F_q, tame case
    deg < char behaves as char 0; indecomposable exceptions are
    additive polynomials] then classifies: at official rows
    deg <= (log n)^2 << p, so the decomposition lattice is EXACTLY
    monomials + Dickson/Chebyshev conjugates = grammar v1's orbits,
    DERIVED. Additive exceptions are excluded by degree-vs-
    characteristic — explaining the program's every small-p
    pathology (F_193, F_17 witnesses, wild rows).

## Step 4 (heuristic anchor): at official rows sporadic trades are
empty-in-expectation by ~260 bits (H1's clean harness concurs).

## GAP alpha (open): sporadic-core bookkeeping
Per-map bounds must be summed over cores Q subset S0; bounding the
number of ACTIVE cores (those admitting any trade) needs a global
count — candidate: the trade relation is itself a curve condition
on Q's points; alternatively an energy/second-moment count over
(Q, P) incidences.

## GAP beta (open): the general-h reduction
Trades with h in (t+1, (log n)^2]: deg(L_P - L_Q) <= h-t-1 is a
band, not a constant; no automatic minimal sub-trade. Candidates:
(1) the pencil L_Q + f, deg f <= h-t-1, as a LINEAR SYSTEM of
divisors of X^n - delta — bounded-degree linear series on the coset
have classified splitting members? (2) induction on h via one
derivative/difference step; (3) the same fiber-product argument on
the correspondence psi_P(x) = psi_Q(y) of bidegree (h, h).

## Recommendation
Hand this skeleton to the strongest available prover (X-7): verify
the two imports exist at the stated strength, close alpha via the
incidence count, close beta via route (3) — the correspondence
version of step 3(i) needs no new geometry, only bihomogeneous
bookkeeping. Toy-check: the K-threshold at n = 64 (Codex, one
afternoon, F2 machinery).
