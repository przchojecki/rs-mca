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
   compactified plane-divisor audit gives only a generic `5p` route, so the
   `3p` leading term must come from the hypergeometric pullback structure.
   The current narrow import is a rank-two line-sheaf conductor calculation:
   save two units beyond the generic `dim H^1 <= 5` count, most likely at
   the two `B(s)=0` points or by pairing their contributions. The deck
   involution swaps those points but introduces the multiplier
   `rho((s+1)^(-2))`; in quotient coordinate this becomes the auxiliary
   trace `sum_{z^2=q} alpha^(-2)(1-z)`.
4. After the trace-family wall is closed, generalize to fixed low-slack
   templates, then separate tangent, quotient-periodic, finite-template, and
   genuinely aperiodic packing.
