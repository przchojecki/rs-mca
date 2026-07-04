# U2-C — the giant-regime statement (draft for attack; the last U2 piece)

- **Status:** TARGET / statement draft (pre-registered before attack,
  per program law). Consumer: x4b_moment_trade_exclusion piece (C);
  gates the prize-max rows' moment column.

## Setting

Official prize-max rows: n = 2^41, tame domain D (coset of mu_n),
q < 2^256, t in {4.29e9, 8.59e9} per rate; block sizes b >= t+1
(the small window (t, C log n] is EMPTY here — piece A's arithmetic).

## The statement (two-exit form)

**U2-C (dichotomy exit).** Every B subset of D with |B| = b >= t+1
and e_1(B) = ... = e_t(B) = 0 is a disjoint union of full mu_M-cosets
(2-power M | n, M > t) together with a t-null remainder that is
itself such a union — i.e., B lies in the v1 dictionary's giant
instances (fibers of X^M), the already-charged, QA.22-affordable
quotient staircase.

**U2-C' (absorbency exit — the fallback that suffices).** The number
of t-null b-subsets of D outside the dictionary is at most N(b) with
sum over the b-window of N(b) x (their star-family sizes) <= 2^27
(the smallest verified QA.22 prize-row margin). Existence without
countability is what must be excluded; countable-and-charged fits.

## Structural handles (in expected order of force)

1. THE COMPLEMENT DUALITY (new, one line): L_B * L_{D\B} = X^n - gamma
   (all subsets of a coset have locators dividing the coset
   polynomial); comparing top coefficients: e_r(D\B) determined by
   e_r(B), and t-nullity of B forces t-nullity of the complement.
   The giant regime is thus PINCHED: blocks and co-blocks are both
   t-null, so WLOG b <= n/2, and every construction must survive
   both views.
2. THE DIMENSION COUNT: monic degree-b polynomials with zero top-t
   coefficients form an affine space of dimension b - t; requiring
   ALL b roots in D is b conditions of density ~ n/q each — the
   naive solution count n^b-ish / q^t vanishes utterly at t ~ 1e9
   (q < 2^256!): t log2 q >= 4e11 bits of suppression vs b log2 n
   <= 41b. NOTE: at b ~ t this reads: random existence is
   impossible by ~1e11 bits; only algebraically forced families
   (coset unions) survive. The gap between this heuristic and a
   proof is the exceptional-component analysis — but unlike the
   small-b case, here the FORCED components are known (cosets) and
   the sparse-relation mechanism needs relations of weight ~ b ~
   1e9 whose resultants' prime factors must align with q < 2^256:
   quantify.
3. THE STAR-PTE PINCH: distinct blocks in a family trade at order t
   with trade size >= t+1; disjoint families cap at n/(t+1) <= 256
   gadgets; the switch lattice is 2^256-sized BEFORE charging —
   absorbency needs the charged fraction to dominate.
4. The antipodal-descent argument (proved, char 0) suggests the
   FINITE-FIELD analogue: e_1(B) = 0 over F_q with B in mu_n and
   2-power n — does a direct mod-q descent exist when q's
   2-adic structure is compatible? (The X-6 counterexample used
   2048 NOT dividing p-1 — the extension-field escape; official
   tame rows have n | q-1 by definition: check whether n | q-1
   CLOSES the escape: the antipodal argument needs indicator
   coefficients in {0,1} which mod-q says nothing about... the
   honest gap; but the n | q-1 structure is unexplored.)

## Falsifier

A verified t-null non-coset block at ANY admissible-shaped toy
analogue of the giant regime (scaled: n = 256, t = 16, b in
[17, 128], q ~ 2^60 with n | q-1): searchable with F2's MITM at
the trade level (search trades of size t+1, not blocks of size b).
