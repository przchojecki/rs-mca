# M1 Residue-Line Roadmap

**Status:** CONJECTURAL / AUDIT.

This is a compact working plan for the M1 residue-line packing program. The
current narrow focus is item 2. This is not a proof-status authority and
should be revised as the project learns more.

1. Keep PR #82 as the first deep low-slack packet theorem: the slack-two
   depth-two canonical frontier should stay in one focused experimental packet.
2. Close the two-coordinate residue-line wall: prove the trace-family conductor
   bound using the bad parameters `u=0`, `u^2+u+1=0`,
   `-3u^2-2u-3=0`, and infinity; carve out ratio-reducible slices such as
   `nu=mu^{-1}` when they collapse to genus-zero sums, and use the
   two-coordinate projective Euler split `chi=4/2` as the conductor target.
   The `chi=2` infinity-unramified slice is now reduced to genus-zero sums.
   Projective reciprocal line-pair slices are also reduced, and the raw
   projective L1 masses should stay in closed form so the remaining ramified
   nonreciprocal target is visible.
3. Use exact finite audits as guardrails: the current evidence supports a
   possible `4p` target and already obstructs constants below `3.977p`.
   Targeted remaining-wall scans suggest that near-sharp rows concentrate in
   the equal-line-monodromy diagonal subfamily; a symmetric-coordinate
   reduction now isolates a pulled-back three-point hypergeometric trace with
   explicit branch divisor. A full character-spectrum audit shows that the
   unrestricted all-character exact `3p` pullback bound is false, and the
   equal-line character filter points instead to a `3p+O(sqrt(p))`
   top-dimensional target with domain-size arithmetic kept explicit. A
   compactified plane-divisor audit gives only a generic `5p` route, but the
   hypergeometric pullback structure supplies the missing two-unit saving:
   the corrected `2F1` local table at `t=1/lambda=0` gives one invariant at
   each `B(s)=0` point, so the rank-two line-sheaf conductor ledger is
   `1+2+2+2=7` and `dim H^1 <= 3`. The deck involution swaps the two
   `B(s)=0` points but introduces the multiplier `rho((s+1)^(-2))`; this is
   useful for exact identities but is not the source of the conductor saving.
   In quotient coordinate this becomes the auxiliary trace
   `sum_{z^2=q} alpha^(-2)(1-z)`. Before quotienting, the same
   calculation gives a complete balanced `z`-line trace with kernel
   `chi_2(1+3z^2) alpha((1+3z^2)/(1-z)^2)` and only two regular-fiber
   corrections, so the next conductor target can ignore infinity Kummer
   ramification and focus on the four finite singular loci. The completed
   conductor ledger now totals `7`, since the old infinity twist moves to
   the finite regular point `z=1` while each `1+3z^2=0` point has one
   invariant. The latest reduction pushes the balanced kernel through
   `y=(1+3z^2)/(1-z)^2`, turning the projective completed trace into a
   Mellin transform `sum_y (alpha chi_2)(y) G(y)`. The next concrete target
   is the conductor of this degree-two hypergeometric pushforward `G`; after
   interchanging sums, its explicit kernel radical is `x+(3x-1)z^2` and its
   fiber resultant is `16x^2y^2-8xy^2+4xy+y^2-2y+1`. The compactified
   resultant surface has complement-Euler target `6`, so the pushforward
   structure, not a naive two-variable Kummer estimate, remains the object to
   exploit. Generically the pushforward has only six candidate singular
   values on the `y`-line: `0`, `1`, the two roots of `9y^2+2y+1`, `3/4`,
   and infinity. The corrected local pushforward conductor ledger is
   `2+1+2+2+4=11` for rank `4`, hence the same `dim H^1 <= 3` target in
   y-pushforward form. This conditionally closes the equal-line diagonal
   top-dimensional estimate and, by projective chart changes, the projective
   equal-pair top-dimensional estimate. The next certificate step is to get
   reviewer acceptance of the recorded `2F1` local table, then promote the
   reported conditional projective-equal ledger into the consumed certificate.
   Here `C_2^peq = 3C_2^diag - 2C_2^eq`, by inclusion-exclusion over the
   three projective line pairs.  The active certificate remains conservative
   until the imported `2F1` local table is accepted as theorem-grade.  The
   next two-coordinate target is therefore the ramified nonreciprocal
   remainder with no equal or reciprocal projective line pair.  Its exact
   mass is `C_2^asym = C_2-C_2^0-C_2^rec-C_2^peq`, and the free projective
   line-permutation action gives orbit count `O_2^asym=C_2^asym/6`.  The
   depth-two lift-window note now records closed forms for the
   coordinate-diagonal and equal-line pieces determining `C_2^peq`, so this
   residual is an explicit ledger rather than a hidden enumeration.  It also
   splits the next dense-edge obstruction: the line-conic-resonant submass is
   `C_2^lc=9((e-1)(e-5)+3 1_{2|e}+2(gcd(e,3)-1))`, and the complement
   `C_2^anr=C_2^asym-C_2^lc` is the clean normal-crossing nonresonant wall.
   The certificate reports the conditional combined ledger that would charge
   `C_2^peq+C_2^anr` at `4p+3 sqrt(p)`.  The line-conic-resonant slice has
   now been reduced to a Mellin transform of a one-dimensional quadratic-fiber
   family with candidate singular support `{0,-1,2,3,infinity}`.  Under the
   additional transformed-core conductor target `|C|<=4p`, the scanner also
   reports the fully conditional ledger charging
   `C_2^peq+C_2^anr+C_2^lc = C_2^peq+C_2^asym` at `4p+3 sqrt(p)`.
   The exact open nonprincipal second moment now gives a separate aggregate
   route for the line-conic slice: per fixed full-order resonant chart,
   `sum |C^o_{eta,nu}| <= sqrt(R(p-1)M_o(p)) = p(1+O(1/p))R(p-1)`.
   This is a possible grouped L1 certificate improvement, not a replacement
   for the missing pointwise `4p` conductor theorem.  For a smaller
   quotient-character order `e`, the inherited full-order moment gives only
   `sqrt(R(e)M_o(p))`; consuming the grouped route in low-index certificates
   therefore needs either `R(e) >= M_o(p)/(K^2p^2)` for the desired average
   `Kp` constant, or a new exact order-`e` moment.  Direct audits for
   `p=17,31,43` show the actual low-order slices remain p-scale even when the
   inherited bound is loose by large constants, making the exact order-`e`
   moment the next concrete grouped-L1 target.  That moment now has an exact
   Parseval reduction to the row/column-centered quotient occupancy energy of
   the map `(u,v) -> (A(u,v)/u, v)` in `(F_p^*/K_e)^2`; bounding this centered
   mixing energy uniformly is the concrete analytic route for low-index
   grouped certificates.
   The updated remaining-wall scan reports this asymmetric wall separately:
   in the current report grid the largest asymmetric ratio is
   `3.2173609608p`, while every near-`4p` top row lies in the projective
   equal-line slice already isolated by `C_2^peq`.
4. After the trace-family wall is closed, generalize to fixed low-slack
   templates, then separate tangent, quotient-periodic, finite-template, and
   genuinely aperiodic packing.
