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
   grouped certificates.  The joint quotient energy further reduces to the
   explicit conic fibration
   `r(r-alpha)u^2+r((beta-alpha)v+1-alpha)u+B(beta v)-alpha rB(v)=0`;
   its projective determinant is `2r Delta(alpha,beta,r)`, so the degenerate
   ratio fibers are exactly the explicit hypersurface `Delta=0`.  Since
   `Delta` is a nonzero cubic in `r` for every fixed `alpha,beta`, there are
   at most `3|K_e|^2` singular ratio parameters, and the only zero conic is
   the identity diagonal `(1,1,1)`.  This gives the aggregate bound
   `J_e <= T^o+(N_e-D_e)(p+1)+(D_e-1)(2p+1)`, and hence the uniform
   `J_e <= T^o+(N_e-1)(p+1)+(3|K_e|^2-1)p`; the remaining task is to exploit
   row/column centering beyond this raw joint-energy estimate.  Cauchy on the
   quotient row/column marginals gives the first centered bound
   `M_e^o <= e^2(T^o+(N_e-1)(p+1)+(3|K_e|^2-1)p)-(T^o)^2`, cancelling the
   leading `p^4` term but still leaving the low-index `p^3` moment gap.  The
   exact signed ratio-fibration formula
   `M_e^o=sum W_e(alpha)W_e(beta)F(alpha,beta,r)` now gives the structural
   target beyond Cauchy: parameter-independent smooth-conic main terms cancel
   because `sum W_e=0`, so the remaining work is weighted trace and boundary
   cancellation over the conic fibration.  The exact projective decomposition
   makes this explicit:
   `M_e^o=sum W_eW_e(Q-(p+1))-sum W_eW_eB`; the first sum is supported only
   on `Delta=0` plus the zero conic, and the second is the open-boundary
   deletion term.  The verifier now partitions that boundary term into
   infinity, coordinate, source/target line, and source/target `A=0` pieces;
   the coordinate and `A=0` pieces vanish by mean-zero weights and the
   identity `A(ru,beta v)=alpha r A(u,v)`, leaving only infinity and the two
   line-deletion terms.  These three survivors now have direct solved-alpha
   formulas: infinity over projective slopes, source line with `v=-1-u`, and
   target line with `v=(-1-ru)/beta`.  The infinity term further reduces by
   `beta=rt` to the quotient-weight autocorrelation
   `(p-1)sum_{t,s} W_e((1+ts+t^2s^2)/(tB(s)))`, with the `[0:1:0]` point
   cancelling by `sum W_e=0`.  Substituting `x=ts` then turns this infinity
   term into the spectral square
   `(p-1)sum_{psi != 1, psi^e=1}|sum_a chi((a-3)(a+1))psi(a)|^2`, giving
   the uniform conductor bound `0 <= I_e <= 4(e-1)p(p-1)` for `p > 3`.
   The source/target line pair now splits as
   `source line = target line + overlap`; the overlap is another positive
   spectral square over `z -> (B(z)/z,1+z)` and satisfies
   `0 <= O_e <= 9(e-1)^2p`.  Thus the boundary wall is reduced to one
   source/target-exclusive line term plus already squared pieces.  That
   final term is now an exact spectral pairing between a target-line
   rank-one sum and the open M1 character sum, so Cauchy gives
   `|T_e|^2 <= O_e M_e^o`; after the overlap bound it can be absorbed by a
   quadratic inequality in `sqrt(M_e^o)`.  Combining all boundary pieces now
   gives the closed inequality
   `M_e^o <= (sqrt(P_e^+)+3(e-1)sqrt(p))^2`, where `P_e` is the weighted
   projective singular excess.  The remaining quotient-conic target is
   therefore a sharp fixed-index `P_e=O(p^2)` singular-excess theorem.
   The latest reduction packages `P_e` as
   `P_e=p w^T Gamma_e w`, where `Gamma_e` is the `e x e` quotient-label
   matrix of signed projective singular excesses; since `sum w=0`, only
   the row/column-centered matrix `Gamma_e^circ` matters, and it is enough
   to prove `||Gamma_e^circ||_F <= C_e p`.  Equivalently, prove an averaged
   square bound for the nonprincipal determinant-surface traces
   `S_{psi,phi}=sum_{Delta=0} epsilon psi(alpha)phi(beta)`.  The signed
   excess `epsilon` is now identified as the Legendre symbol of any nonzero
   binary discriminant on rank-two singular conic charts, so this is a
   charted Kummer trace problem on the determinant surface.  The ordered
   discriminant cover is now explicit: first use `d_UV`, then `d_UW`, then
   `d_VW`; the all-zero residual has rank at most one and contributes zero,
   except for the separated zero conic.  The non-`d_UV` lower chart is now
   collapsed to the diagonal curve `alpha=beta=r` plus the residual
   quadratic curve `K_alpha(alpha,r)=K_beta(beta,r)=0`, so it has at most
   `5(p-1)` points and is already `O(p)` in every trace.  The remaining
   surface-cancellation target is the main `d_UV != 0` chart.  This chart
   is now projected to a projective two-sheet beta cover over
   `(alpha,r)`, with branch divisor
   `M(alpha,r)H(alpha,r)=0`; the vertical fiber, beta-zero/beta-infinity
   deletions, branch fibers, and lower-chart companions are all curve-sized.
   On the remaining split two-root fibers, `chi(d_UV)` is now identified as
   the base twist `chi(rM)=chi(aH)` by cleared square identities on the
   beta cover, so the last trace problem is the open two-sheet cover with an
   explicit base-twisted beta Kummer pushforward.  The branch
   curves `M=0` and `H=0` are now rationally parametrized from `(1,1)`,
   and for `p>5` they meet in the torus only at that already separated
   vertical point; characteristic `5` is a finite audited exception.  On the
   good base the beta cover is finite etale of degree two, with derivative
   square equal to `D_beta`, so the good beta-cover surface is smooth and
   all ramification is on deleted branch fibers.  The branch curves are now
   also audited smooth away from the separated point
   `(1,1)`, so there is no hidden singular branch component on the good
   locus.  The boundary pile-up at `(1,1)` is now also resolved by the fixed
   two-chart blow-up `r=1+t(alpha-1)` and `alpha=1+s(r-1)`: the strict
   transforms of `A_beta`, `Q_beta`, `K_alpha`, `alpha-r`, `M`, and `H` have
   explicit factors and pairwise intersections supported on finite slope
   resultants; for audited `p>5` those strict transforms are smooth, with
   only isolated characteristic-`5` exceptions.  The remaining non-normal
   incidences are a bounded explicit set: four open tangencies and the toric
   corner over `(alpha,r)=(0,0)`, with no open-torus triple points.  The main
   `U V` trace now has an exact pushforward identity over
   the good base `A_beta C_beta D_beta (alpha-r)K_alpha != 0`, with all
   deleted pieces contributing only `O(p)`.  The final analytic object is
   the good-base rank-two beta pushforward
   `psi(alpha)chi(rM)(phi(beta_1)+phi(beta_2))`, equivalently the
   square-root cover `y^2=D_beta` with kernel
   `psi(alpha)chi(rM)phi((2A_beta)^(-1))phi(y-B_beta)`.  Its vertical
   `r`-pencil now has explicit genus-two branch polynomial
   `P_r(alpha)=alpha M H` and fixed bad parameters
   `r=1`, `r^2+r+1=0`, and `9r^2+14r+9=0`, with branch-boundary collisions
   confined to the recorded resultant supports.  The beta sheets now
   have an explicit fixed-ratio resonance curve
   `lambda B_beta^2=A_beta C_beta(1+lambda)^2`; after removing the torus
   factor this has degree at most four in `alpha` on every vertical fiber
   unless `lambda=-1`, where it collapses to two lines.  Thus every fixed
   beta-root ratio has at most `4(p-1)` good-base points, so no fixed
   beta-root ratio supports a two-dimensional family on the good base.
   Consequently the nonprincipal quotient-character beta-sheet energy is
   exactly `(2e-4)N_split+2eN_K` and satisfies
   `E_e^beta <= (2e+4)(p-1)^2`; the beta sheets do not create a hidden
   `p^3` averaged obstruction.  The full singular trace is now partitioned
   as zero conic plus lower-chart plus exceptional-main ledger plus the
   good beta pushforward; in centered rows the first three pieces satisfy
   the uniform algebraic bound `|bad| <= p+19(p-1)<20p`.  Therefore the
   depth-two singular-excess target has been reduced to cancellation for
   this one good rank-two beta pushforward.  Its conductor ledger is now
   explicit: the beta-zero boundary `Q_beta=0` has nontrivial `phi`
   monodromy for every centered row (`phi != 1`) and shares no component
   with the beta-linear, `U V` sign, beta-infinity, or branch divisors.
   The component separations are recorded by explicit resultants, including
   the diagonal and `K_alpha` deleted divisors, and the verifier checks the
   corresponding finite intersection root supports.
   Thus, under the `(BETA_2)` bounded-conductor import now isolated in
   `m1_kummer_weil_import_contract.md`, the singular trace satisfies
   `S_{psi,phi}=O_e(p)`.  Parseval then gives
   `||Gamma_e^circ||_F=O_e(p)`, so `P_e=O_e(p^2)` and the closed boundary
   inequality gives `M_e^o=O_e(p^2)`.  The verifier now checks the
   good/bad singular-trace partition on every nonprincipal quotient
   character pair for the audited quotient orders.
   The vertical beta-boundary audit has also been doubled: beta zero carries
   monodromy `phi`, beta infinity carries monodromy `phi^{-1}`, and explicit
   resultants show both boundaries avoid the beta-linear, sign, branch,
   diagonal, and lower-chart divisors componentwise.
   The finite `U V` sign divisor is now removed from the good cover by the
   resultant
   `Res_beta(beta equation,d_UV/r)=a^2r^2(a-r)^2K_alpha^2`, so sign zeros
   occur only on already deleted diagonal/lower-chart fibers; the stronger
   square-class identities give `chi(d_UV)=chi(rM)=chi(aH)`.  The rank-two
   good pushforward now also has explicit determinant
   `psi^2 phi(C_beta/A_beta)`, so no sheet-dependent determinant ramification
   remains hidden in `(BETA_2)`.
   The updated remaining-wall scan reports this asymmetric wall separately:
   in the current report grid the largest asymmetric ratio is
   `3.2173609608p`, while every near-`4p` top row lies in the projective
   equal-line slice already isolated by `C_2^peq`.
4. After the trace-family wall is closed, generalize to fixed low-slack
   templates, then separate tangent, quotient-periodic, finite-template, and
   genuinely aperiodic packing.
