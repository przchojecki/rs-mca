# Agents Log

This file is the working ledger for agent-created material in `experimental/`.
Use it to record every new note, script, scan, formalization stub, or audit before
the material is promoted into `tex/` or `scripts/`.

The log is not a proof-status authority. It is a coordination record: what was
added, why it might matter, and what a human or later agent should check next.
Keep entries concise and link to the relevant files.

## Entry Format

```markdown
### YYYY-MM-DD - Short title

- **Agent/model:** Name the agent or model, for example `GPT-5.5 Pro`,
  `Claude Fable 5`, or `Codex`.
- **Files added or changed:** List paths under `experimental/`, `tex/`,
  or `scripts/`.
- **Status:** PROVED / CONDITIONAL / CONJECTURAL / EXPERIMENTAL / AUDIT /
  COUNTEREXAMPLE.
- **What is being added:** State the claim, note, scan, script, proof,
  heuristic, or computation
  in one or two sentences.
- **How it is useful:** Say which paper, theorem, problem, ledger, or toy case
  the material supports.
- **What to do next:** Give the next verification, cleanup, proof step,
  experiment, or promotion decision.
```

## Entries

### 2026-06-30 - Paper D v8 quotient ledger promotion

- **Agent/model:** Codex.
- **Files added or changed:** `tex/cs25_cap_v8.tex`, `cs25_cap_v8.pdf`,
  `site/papers/cs25_cap_v8.pdf`,
  `experimental/notes/audits/paperD_v8_vs_v7_audit.md`, scanner status labels,
  `readme.md`, and site paper/leaderboard/update data.
- **Status:** AUDIT / VERSION-PROMOTION / PROVED_PAPERD_V8_CAP /
  PROVED_PAPERD_V8_FIRST_GRID.
- **What is being added:** Paper D v8 is promoted as the current public Paper D
  source. It preserves the v7 universal and first-grid caps, restores the
  explicit `q>n` and endpoint-radius fixes, and adds quotient-support plus
  distinct-parameter quotient image ledgers.
- **How it is useful:** The new ledgers give future staircase scanners and
  proof notes a safe way to account for declared quotient-remainder branches
  without double-counting supports or slope images.
- **What to do next:** Treat these ledgers as branch accounting only. The
  full safe-side theorem still needs the aperiodic Hankel-packing and
  extension-line completion inputs.
### 2026-06-30 - M1 projective endpoint-pair inversion

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / AUDIT.
- **What is being added:** The overlapping endpoint-pair inversion is lifted
  from finite slopes to projective endpoints `E=[Z:W]`, with
  `lambda_0=c_1(E_0)/c_0(E_0)` and
  `lambda_1=2lambda_0-lambda_0^2 c_0(E_1)/c_1(E_1)`.
- **How it is useful:** Infinity endpoint cases no longer need a separate
  residual exception: for a fixed initial row basis, the ordered projective
  endpoint pair determines the nondegenerate overlapping square-norm packet.
- **What to do next:** Use projective endpoint-pair injectivity to replace
  square-norm packet counts by endpoint-pair counts, with only row-basis
  variation remaining.

### 2026-06-30 - M1 diagonal endpoint collapse

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / AUDIT.
- **What is being added:** In the nondegenerate overlapping Plucker chart, if
  the finite `H_0` and `H_1` endpoints coincide, endpoint-pair inversion
  forces `lambda_1=lambda_0`, hence `H_1=lambda_0^2 H_0`.
- **How it is useful:** Coincident finite zero/pole endpoints are therefore
  constant-norm packets, not residual nonconstant square-norm packets.  This
  removes the diagonal endpoint-pair branch from the M1 square-norm ledger.
- **What to do next:** Count only off-diagonal finite endpoint pairs in the
  nonconstant square-norm branch, with projective-infinity cases handled by
  the same chart formulas.

### 2026-06-30 - M1 overlapping endpoint-pair inversion

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / AUDIT.
- **What is being added:** In the nondegenerate overlapping Plucker chart,
  a finite `H_0` endpoint recovers `lambda_0=c_1(z_0)/c_0(z_0)`, and a finite
  `H_1` endpoint then recovers
  `lambda_1=2lambda_0-lambda_0^2 c_0(z_1)/c_1(z_1)`.
- **How it is useful:** For a fixed adjacent row basis, an ordered finite
  zero/pole endpoint pair supports at most one nondegenerate square-norm
  Plucker packet, turning this branch into an injective endpoint-pair count
  after the charged degeneracies are removed.
- **What to do next:** Use this injectivity to bound simultaneous finite
  endpoint pairs across admissible row bases or identify the remaining basis
  variation as quotient/template structure.

### 2026-06-30 - M1 Plucker-chart endpoint slope map

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / AUDIT.
- **What is being added:** The signed-square Hankel factor gives an explicit
  finite endpoint formula
  `z_i=(lambda_i a_i-a_{i+1})/(b_{i+1}-lambda_i b_i)`, with the denominator
  zero case forced to the projective endpoint at infinity; the reverse chart
  has the symmetric formula.
- **How it is useful:** For fixed adjacent row basis, the moving
  square-norm endpoint image is a projective line map in one Plucker
  parameter.  This should make later endpoint-support counts sharper than
  treating endpoints as generic quadratic roots.
- **What to do next:** Combine the slope map with the overlapping
  two-parameter recurrence to count surviving finite endpoint pairs.

### 2026-06-30 - M1 Plucker-chart Hankel square factorization

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / AUDIT.
- **What is being added:** On a nonzero Plucker endpoint chart, the adjacent
  Hankel minor factors as a signed square:
  `H_i=-(c_{i+1}-lambda_i c_i)^2`, with the symmetric reverse-chart formula
  `H_i=-(c_{i+1}-mu_i c_{i+2})^2`.
- **How it is useful:** This replaces a generic discriminant-zero endpoint
  condition by an explicit row-linear double-endpoint form, which is a sharper
  object for later M1 residue-line packing and endpoint-support counts.
- **What to do next:** Use the linear endpoint forms in overlapping charts to
  bound how many distinct finite endpoints can survive after fixed-root and
  quotient charges.

### 2026-06-30 - M1 overlapping Plucker-chart recurrence

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / AUDIT.
- **What is being added:** When the adjacent Plucker endpoint conics for
  `i=0,1` both hold and `P_0!=0`, either `lambda_0=0` puts the second triple
  in the proportional-row degeneracy, or the rows satisfy an explicit two-step
  recurrence for `r_2,r_3` from `r_0,r_1`.
- **How it is useful:** This is a local packing reduction for simultaneous
  square-norm endpoint production: the residual nondegenerate branch is
  controlled by two scalar recurrence parameters instead of an unconstrained
  four-row image.
- **What to do next:** Use the two-step recurrence packet to count or
  eliminate simultaneous endpoint supports after quotient-periodic and
  fixed-root charges are removed.

### 2026-06-30 - M1 Plucker-chart row recurrence

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / AUDIT.
- **What is being added:** On the nonzero Plucker chart `P_i!=0`, the
  endpoint conic is rewritten as the row recurrence
  `r_{i+2}=2lambda_i r_{i+1}-lambda_i^2 r_i`, with the symmetric reverse
  recurrence on `R_i!=0`.
- **How it is useful:** This turns the residual moving endpoint-support chart
  from a generic conic condition into a one-parameter adjacent-row recurrence,
  which is a sharper local normal form for M1 residue-line packing.
- **What to do next:** Study overlapping endpoint charts for `i=0,1` to see
  whether simultaneous zero and pole endpoint production forces a bounded
  recurrence packet or a previously charged degeneracy.

### 2026-06-30 - M1 square-norm Plucker-chart decomposition

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / AUDIT.
- **What is being added:** The square-norm endpoint Plucker conic
  `S_i^2=4P_iR_i` is split into affine charts.  On `P_i!=0`,
  `lambda_i=S_i/(2P_i)` gives `S_i=2P_i lambda_i` and
  `R_i=P_i lambda_i^2`; on the complementary zero-minor charts, endpoint
  support is forced into zero-row or proportional-row degeneracy.
- **How it is useful:** This separates bookkeeping endpoint charges from the
  residual moving Plucker chart, giving a sharper local normal form for the
  M1 aperiodic residue-line packing program.
- **What to do next:** Use the moving chart to bound or classify the remaining
  endpoint-support image after tangent, fixed-root, quotient, and zero-row
  charges are removed.

### 2026-06-30 - M1 square-norm Plucker-minor discriminants

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / AUDIT.
- **What is being added:** The adjacent Hankel-minor discriminants are
  rewritten as Plucker-minor conics:
  `Delta(H_i)=S_i^2-4P_iR_i`, where `P_i,R_i,S_i` are the three 2x2 minors
  of the adjacent row-pair triples.
- **How it is useful:** This gives a rank/minor-level endpoint-support
  certificate.  Fully proportional row triples are separated as the rank-one
  degeneracy, while nontrivial moving endpoint supports must lie on an explicit
  conic relation among the three adjacent minors.
- **What to do next:** Use the Plucker-minor conic to split rank-one endpoint
  families from residual conic endpoint-support families.

### 2026-06-30 - M1 square-norm Hankel-minor discriminants

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / AUDIT.
- **What is being added:** The square-norm endpoint discriminants are written
  as explicit adjacent Hankel-minor discriminants.  For
  `c_i(z)=a_i+z b_i`, the minors
  `H_i=c_i c_{i+2}-c_{i+1}^2` have coefficients
  `h_{i,0},h_{i,1},h_{i,2}`, with endpoints forcing
  `h_{i,1}^2-4h_{i,0}h_{i,2}=0`.
- **How it is useful:** This expresses moving square-norm support production
  directly in the active root-core row data.  The endpoint-support image can
  now be attacked as the vanishing of two explicit binary-Hankel
  discriminants, rather than as an abstract moving-quadratic condition.
- **What to do next:** Use the `H_0` and `H_1` discriminant equations to split
  endpoint-support families into constant-support and genuinely moving-core
  cases.

### 2026-06-30 - M1 square-norm endpoint discriminant certificate

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / AUDIT.
- **What is being added:** The raw finite endpoint equations are converted
  into a scalar discriminant certificate.  Writing
  `B_R=b_0+b_1 z+b_2 z^2` and `Q_R=q_0+q_1 z+q_2 z^2`, live finite endpoints
  force `b_1^2-4b_0b_2=0` or `q_1^2-4q_0q_2=0`, with endpoint slope
  `-b_1/(2b_2)` or `-q_1/(2q_2)` when the quadratic coefficient is nonzero.
- **How it is useful:** This turns moving square-norm support production into
  discriminant-zero equations in the raw recurrence coefficients, so the
  endpoint-support image is a scalar condition on the active root core rather
  than a free moving-root choice.
- **What to do next:** Use these discriminant equations to separate constant
  endpoint-support families from genuinely moving square-norm supports.

### 2026-06-30 - M1 square-norm raw endpoint certificate

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / AUDIT.
- **What is being added:** The finite square-norm endpoint certificate is
  moved from reduced norm factors to the raw recurrence coefficients:
  zero endpoints satisfy `B_R=B_R'=0, Q_R!=0`, and pole endpoints satisfy
  `Q_R=Q_R'=0, B_R!=0`.
- **How it is useful:** This removes cancellation bookkeeping from the global
  endpoint-support charge.  The moving support image can now be controlled
  directly by double-root equations in the recurrence polynomials `B_R` and
  `Q_R`.
- **What to do next:** Use the raw double-root equations to classify which
  active root-core families can produce moving square-norm packet supports.

### 2026-06-30 - M1 square-norm double-root endpoint certificate

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / AUDIT.
- **What is being added:** The repeated-endpoint gate is converted into
  derivative equations for the reduced norm boundary: finite square-norm zero
  endpoints satisfy `bar B_R=bar B_R'=0`, and finite pole endpoints satisfy
  `bar Q_R=bar Q_R'=0`, with the opposite reduced factor nonzero.
- **How it is useful:** This gives the endpoint-support image a concrete
  double-root/discriminant-zero certificate as the root core varies.  It is
  the algebraic form needed to charge the exceptional support image rather than
  treating it as generic moving-quadratic roots.
- **What to do next:** Use these derivative certificates to relate moving
  endpoint-support families to fixed-root, line-packet, or boundary-core
  ledgers.

### 2026-06-30 - M1 square-norm endpoint-charge corollary

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / AUDIT.
- **What is being added:** The finite endpoints of the square-norm packet are
  charged explicitly: a zero endpoint with `Q_R != 0` has `p_R=0` and is a
  fixed-root line, while a pole endpoint is a denominator-zero slope that is
  either unsolvable or already in the full-plane/fixed-root charge.
- **How it is useful:** This makes the square-map packet an open slope-line
  object whose finite boundary points are existing ledger charges, not extra
  residual aperiodic slopes.  It narrows the remaining global M1 task to
  bounding the packet interiors and support image after endpoint charges.
- **What to do next:** Use the repeated-endpoint and endpoint-charge gates to
  bound or classify the active endpoint-support image as the root core varies.

### 2026-06-29 - M1 square-norm repeated-endpoint gate

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / AUDIT.
- **What is being added:** The nonconstant square-norm exception is sharpened
  into a repeated-endpoint gate: after cancelling the gcd of the degree-two
  norm numerator and denominator, every finite zero or pole has valuation
  `+-2`, and infinity has valuation `0` or `+-2`.
- **How it is useful:** This places the square-map packet support image on
  repeated-root/discriminant-zero norm-boundary loci, rather than on the full
  generic root image of `B_R` and `Q_R`.  It is a more chargeable algebraic
  target for the downstream M1 endpoint-support ledger.
- **What to do next:** Relate these repeated-root loci for `B_R` and `Q_R` to
  fixed-root, line-packet, or boundary-core charges as the active root core
  `R` varies.

### 2026-06-29 - M1 square-map packet-count corollary

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / AUDIT.
- **What is being added:** The square-map support palette is converted into
  an explicit counting corollary: a finite family of degree-one square-map
  packets has at most `(e/2)` distinct slope sets per unordered zero-pole
  support, and a single nonconstant square-norm branch contributes only one
  such support.
- **How it is useful:** This gives the downstream M1 ledger a direct packet
  count to use when summing square-norm and one-root-square branches over root
  cores; repeated square roots or parallel/inverse parameters are multiplicity
  inside a fixed endpoint palette, not new slope growth.
- **What to do next:** Bound the image of endpoint supports produced by active
  root-core recurrences or charge that image to fixed-root, line-packet, and
  boundary-core ledgers.

### 2026-06-29 - M1 square-norm endpoint palette

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / AUDIT.
- **What is being added:** The square-map support palette is tied back to the
  root-core recurrence data.  If the reduced square norm is
  `B_R/Q_R=gamma M^2` with `M` degree one, then `div(B_R/Q_R)=2 div(M)`, so
  the palette support is exactly the zero/pole boundary of the norm divisor.
- **How it is useful:** The square-norm packets are now indexed by the bounded
  norm-boundary endpoints coming from the roots of `B_R`, roots of `Q_R`, and
  infinity, rather than by arbitrary square-root choices.  This gives the
  downstream M1 ledger a concrete endpoint image to charge when summing
  square-norm palettes over active root cores.
- **What to do next:** Relate the norm-boundary endpoint image to already
  isolated fixed-root, denominator-zero, line-packet, or boundary-core ledgers.

### 2026-06-29 - M1 square-map support-class palette

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / AUDIT.
- **What is being added:** The square-map packet overlap gate is sharpened to
  a finite support-class palette.  For a fixed unordered zero-pole support
  `Pi` on the slope line, every degree-one parameter with that support is
  scalar-parallel or scalar-inverse to a chosen representative, and all
  two-coset square-map packets belong to exactly `e/2` disjoint packets
  partitioning `P^1 \\ Pi`.
- **How it is useful:** This converts quotient-parallel/inverse high-overlap
  components from arbitrary repeated Kummer branches into an `O_e(1)` palette
  per zero-pole support.  The downstream M1 square-norm ledger can now try to
  bound the image of zero-pole supports rather than every repeated packet
  occurrence separately.
- **What to do next:** Use the palette when summing square-norm and rational
  one-root-square packets over active `(j-2)` root cores; isolate whether the
  zero-pole support image itself is already paid by fixed-root, line-packet, or
  boundary-core ledgers.

### 2026-06-29 - M1 square-map packet intersection gate

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / AUDIT.
- **What is being added:** The square-norm and one-root-square branches are
  now given a degree-one packet-overlap gate: two quotient-class packets pulled
  back by degree-one slope parameters have a geometrically trivial mixed
  character term only when the parameters are scalar-parallel or scalar-inverse,
  with the corresponding exponent relation.  Off those relations, square-map
  packets have product-density intersection up to `O_e(sqrt(p))`; on those
  relations their intersection is again an explicit quotient-class packet.
- **How it is useful:** This turns the explicit square-map branches isolated in
  the root-core recurrence chart into structured slope-coset packets with a
  usable overlap/energy ledger, rather than leaving their overlaps as possible
  hidden Kummer failures.
- **What to do next:** Use the packet-overlap gate when summing square-norm
  branches over active `(j-2)` root cores or when isolating quotient-parallel
  packet families for a downstream M1 ledger.

### 2026-06-29 - M1 boundary root-core recurrence chart

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / BOUNDARY-CORE REDUCTION / AUDIT.
- **What is being added:** For a fixed `(j-2)` root core and finite slope,
  formal two-root extensions are recovered by a length-four Hankel recurrence.
  Off the denominator `Q_R(z)=c_0c_2-c_1^2`, the coefficients `(s,p)` are
  unique rational functions of `z`, and the split-root condition is a quartic
  numerator in `z`.  Equivalently, after charged denominator-zero cases are
  removed, residual split slopes are filtered points on the bounded cover
  `Y^2=Theta_R(z)` with `deg Theta_R<=4`.  The subgroup domain/outside filter
  expands into Kummer traces of `r_+^a r_-^b` on this same cover, and the
  fixed-zero-root branch `B_R=0` is charged to the fixed-root line `p=0`.
  The diagonal pair terms `S_{a,a}` descend to bounded-support `P^1` Kummer
  traces involving `B_R/Q_R` and `Theta_R`; for index-two domains the
  remaining one-root cover terms cancel by sheet symmetry.  On the open cover,
  the outside-root condition factors through the slope-line norm `B_R/Q_R`,
  and mixed points inject into the norm-outside slope set.  The degree-two
  norm-power exceptions are classified as constant norm or quadratic
  square-norm; constant norm is charged to the fixed-root/product-Mobius
  line-packet ledger, while nonconstant square norm has only the quadratic
  norm-filter Fourier coefficient as a possible large term.  The
  positive-parity square-norm branch gets the genus-free norm-outside bound
  `(e-2)|D|+O_e(sqrt(p))` and is the `(e-2)`-coset slope-line square-map
  packet.  Only the negative-parity square-norm branch remains a slope-line
  obstruction, and even there the mixed-domain count collapses to one-root
  sums.  Its only cover-level power is the explicit one-root square
  branch, which is fixed-root or rational because `deg(r_+)<=2`; the
  negative root-square sign cancels the main one-root term, while the positive
  sign is the two-coset square-map packet `chi(h)^2=chi(alpha)^(-1)` and gives
  the `2|D|` rational branch.  Pushing divisors down by the
  slope-cover norm shows that, after those norm exceptions, the only
  cover-level power branches left are the anti-diagonal ratio terms
  `chi^a(r_+/r_-)`; the anti-ratio has degree at most four and the same
  square class as `B_R/Q_R`, so after square-norm is isolated only the cubic
  anti-ratio branch can remain.  A genuine cubic anti-ratio power forces a
  degree-one cube root, hence a rational cover; genus-one root-core covers
  have no genuine cover-level power branch after the norm exceptions.  On the
  rational cubic branch, only the two coefficients `a=e/3,2e/3` can be large,
  and their conjugate cubic constants improve the explicit bound to
  `(1/e)|C_R^x|+O_e(sqrt(p))`.  These cases are packaged as the classified
  per-core bound (RKCLASS).
- **How it is useful:** The denominator-zero solvable case is exactly a
  fixed-root line or the full-plane lift, both already charged.  Thus the
  residual non-line root-core target is a one-variable slope-cover problem
  of genus at most one after squarefree reduction.  The filter has bounded
  zero-pole support, so non-power character terms have depth-independent
  conductor under the standard Kummer-Weil input, giving an explicit per-core
  mixed-domain bound once nonprincipal power branches are absent, with the
  diagonal product terms removed from the genuinely cover-level workload and
  the quadratic-residue case reduced entirely to `P^1` Kummer sums.  The norm
  filter isolates the outside-root dependence on the slope line and gives a
  genus-free fallback bound from the rational map `B_R/Q_R`, with explicit
  noncancellation branches.  The constant-norm exception is not new geometry,
  and the square-norm exception is now split into a bounded positive-parity
  branch plus a negative-parity one-root ledger whose rational/fixed-root
  square obstruction has an explicit sign split.
  The norm-pushforward obstruction localizes the remaining cover-level
  obstruction to anti-norm ratio terms, and the anti-ratio square-class
  reduction removes every noncubic order after square-norm is isolated.  The
  cubic term is now separated into a rational-cover algebraic branch and a
  nontrivial genus-one Kummer sum, with a proportional rational-branch ledger.
  The downstream M1 ledger can now consume the root-core branch through the
  explicit genus-one, rational-cubic, split-square, and index-two alternatives.
- **What to do next:** Use this recurrence chart when attacking the active
  `(j-2)` root-core image after quotient, tangent, fixed-root, and full-plane
  charges.

### 2026-06-29 - M1 boundary quartic Kummer power gate

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/notes/m1/m1_boundary_off_external_anchor_audit.md`,
  `experimental/notes/m1/m1_hankel_variable_line_packet_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / CONDITIONAL-STANDARD-WEIL / AUDIT.
- **What is being added:** The full-subgroup boundary quartic count is
  expanded into character sums
  `sum_y chi^a(y) chi_2(Disc_R(y))`, and the exact `lcm(e,2)` power-divisor
  gate for geometrically trivial terms is identified.  The gate is sharpened
  to the forced normal forms `Disc_R=cG^2` with `a=0` or
  `Disc_R=c y G^2` with even index and `a=e/2`.
- **How it is useful:** If the power gate fails, the standard `P^1`
  Kummer-Weil bound has support contained in the four discriminant roots plus
  `0` and `infinity`, giving a depth-independent `4 sqrt(p)` term.  Thus any
  no-cancellation quartic branch is an explicit rational graph or fixed
  square-root rational graph case rather than hidden growing conductor.  Since
  at most one Fourier term is geometrically trivial, the full-subgroup fixed
  core has live count at most `2|D|+4 sqrt(p)+O(1)`.  Combining with the
  graph bound gives the ledger multiplier
  `min(2(n-j+2), 2|D|+4 sqrt(p)+O(1))` for the non-line conic branch.
- **What to do next:** Combine this fixed-core quartic bound with the active
  fixed-core/root-image ledger and quotient/tangent charges; the variable-line
  packet note now records this refined boundary-core substitution.

### 2026-06-29 - M1 boundary-core slope-fiber injection

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/notes/m1/m1_boundary_off_external_anchor_audit.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / BOUNDARY-CORE REDUCTION / AUDIT.
- **What is being added:** For a fixed boundary core and finite slope, the
  same-slope fiber in the elementary `(s,p)` plane is empty, one point, an
  affine line, or the whole plane.
- **How it is useful:** A repeated live slope on the boundary-core conic
  therefore returns to a charged fixed-root line, a constant-slope non-fixed
  line packet, or the full-plane lift.  After those charges, the quartic
  boundary-core point count also controls live slope count.
- **What to do next:** Prove the remaining quartic/Kummer estimate with the
  quotient, outside-domain, and active filters imposed.

### 2026-06-29 - M1 boundary quartic bounded cover

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/notes/m1/m1_boundary_off_external_anchor_audit.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / BOUNDARY-CORE REDUCTION / AUDIT.
- **What is being added:** After zero-discriminant cases are charged, the live
  boundary-core quartic target is identified with the double cover
  `W_R^2=Disc_R(y)` via `W_R=2A_R(y)beta+B_R(y)`, away from at most two
  linear exceptional fibers where `A_R(y)=0`.
- **How it is useful:** Since `deg Disc_R<=4`, the squarefree normalization
  has genus at most one.  This turns the remaining non-line boundary-core
  task into a uniformly bounded genus-zero/genus-one Kummer trace rather than
  an unstructured bidegree incidence.
- **What to do next:** Prove the required nonzero quartic Kummer/character-sum
  cancellation after quotient, outside-domain, and active filters.

### 2026-06-29 - M1 boundary discriminant degeneracy discharge

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/notes/m1/m1_boundary_off_external_anchor_audit.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / BOUNDARY-CORE REDUCTION / AUDIT.
- **What is being added:** The identically-zero quartic discriminant case in
  the fixed-core boundary conic is classified: over odd characteristic the
  elementary determinant is either a scalar affine-line square or a scalar
  multiple of the envelope conic `s^2-4p`.
- **How it is useful:** Scalar line squares are already fixed-sum, fixed-root,
  or product-Mobius line-packet branches, while the envelope contributes only
  `beta=y` on the mixed boundary slice and is removed by the
  outside-domain/distinct-root filters.  Thus the live conic target has a
  nonzero quartic discriminant after existing charges.
- **What to do next:** Prove cancellation or a polynomial image bound for the
  remaining nonzero quartic discriminant trace with quotient and active
  filters imposed.

### 2026-06-29 - M1 boundary-core discriminant gate

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/notes/m1/m1_boundary_off_external_anchor_audit.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / BOUNDARY-CORE REDUCTION / AUDIT.
- **What is being added:** For the fixed-core elementary determinant
  `F_R(s,p)`, the boundary equation `F_R(beta+y,beta y)=0` is written as an
  explicit quadratic in `beta` with coefficient polynomials of degree at most
  two in `y`; in odd characteristic its nondegenerate root count is controlled
  by a quartic discriminant.
- **How it is useful:** This turns the remaining non-line boundary-core conic
  branch into a concrete quartic Kummer/discriminant trace over domain roots,
  while the fully zero fiber is identified with a fixed-root line component
  already charged by the root-slice ledger.
- **What to do next:** Attack the resulting quartic character-sum target after
  quotient, tangent/contained, outside-domain, and active filters are imposed.

### 2026-06-29 - M1 mixed-domain line-packet trace

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/notes/m1/m1_boundary_off_external_anchor_audit.md`,
  `experimental/notes/m1/m1_hankel_variable_line_packet_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / BOUNDARY-CORE REDUCTION / AUDIT.
- **What is being added:** The mixed-domain slice of each surviving non-fixed
  two-root line packet is made explicit: fixed-sum packets have
  `beta=s_0-y`, and product-Mobius packets have `beta=c+mu/(y-c)`.
- **How it is useful:** This shows that boundary-core points on non-fixed
  packets are escaped-root traces of the same involutions already used in the
  all-domain line-packet ledger, with at most `n-j+2` pairs per fixed core and
  line after fixed-root degeneracies are charged.
- **What to do next:** Use this escaped-root interpretation when attacking the
  remaining boundary-core/root-image and different-slope two-exchange ledgers.

### 2026-06-29 - M1 boundary-core elementary pullback

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/notes/m1/m1_boundary_off_external_anchor_audit.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / BOUNDARY-CORE REDUCTION / AUDIT.
- **What is being added:** The fixed-core bidegree determinant is identified
  as the pullback `Delta_R(beta,y)=F_R(beta+y,beta y)` of the ordinary
  two-root elementary determinant `F_R(s,p)`.
- **How it is useful:** This connects the one-outside boundary-core target to
  the existing fixed-root, fixed-sum, and product-Mobius line-packet geometry
  instead of leaving it as a separate boundary-specific incidence.
- **What to do next:** Use the existing two-root line-packet ledger or the
  two-coordinate wall machinery to bound the remaining mixed-domain slice.

### 2026-06-29 - M1 fixed-core bidegree determinant target

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/notes/m1/m1_boundary_off_external_anchor_audit.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / BOUNDARY-CORE REDUCTION / AUDIT.
- **What is being added:** For each fixed `(j-2)` domain core `R`, the
  residual one-outside boundary incidence is cut out by the symmetric bidegree
  `(2,2)` determinant
  `Delta_R(beta,y)=det(U_2-(beta+y)U_1+beta y U_0,
  V_2-(beta+y)V_1+beta y V_0)`.
- **How it is useful:** The fixed-shadow and fixed-anchor quadratic gates are
  now the two coordinate specializations of one explicit low-dimensional
  incidence curve, clarifying the exact target left by the boundary-core
  reductions.
- **What to do next:** Bound this bidegree-two active core incidence or connect
  it to the existing two-coordinate/Kummer wall ledger.

### 2026-06-29 - M1 fixed-core boundary graph reduction

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/notes/m1/m1_boundary_off_external_anchor_audit.md`,
  `experimental/notes/m1/m1_hankel_variable_line_packet_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / BOUNDARY-CORE REDUCTION / AUDIT.
- **What is being added:** For each fixed `(j-2)` domain core `R`, the residual
  one-outside incidences between external anchors and domain extension roots
  form a bipartite graph of degree at most two on both sides after the
  boundary-shadow and fixed-anchor root-slice charges.
- **How it is useful:** This gives
  `|Core_off^res(R)| <= 2(n-j+2)` and
  `|Core_off^res| <= 2(n-j+2)|Root_off^res|`, isolating the remaining
  one-outside target as an active domain-core image.
- **What to do next:** Relate the active boundary-root image to quotient,
  different-slope codegree, or the two-coordinate wall ledger.

### 2026-06-29 - M1 boundary-core closure substitution

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_variable_line_packet_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / LEDGER REDUCTION / AUDIT.
- **What is being added:** The fixed-anchor boundary-core fiber bound
  `(j-1)|Boundary_off| <= 2|Core_off|` is substituted into the rate-half
  variable-line closure criterion.  The one-outside ledger term becomes
  `2 binom(n-j+1,2)|Core_off|`, giving the closure estimate
  `sum_L r_L <= n^B_Q + 2 n^B_E + n^(B_T+4) + 2 n^(B_C+2)`.
- **How it is useful:** This converts the remaining one-outside hypothesis for
  the non-fixed line-packet branch from a boundary-image/shadow-image bound to
  a lower-dimensional boundary-core image bound, with one less crude power of
  `n` in the bookkeeping loss.
- **What to do next:** Prove a polynomial bound or further charge decomposition
  for the residual boundary-core image.

### 2026-06-29 - M1 fixed-anchor boundary-core fibers

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/notes/m1/m1_boundary_off_external_anchor_audit.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / BOUNDARY-SHADOW REDUCTION / AUDIT.
- **What is being added:** After fixing an external anchor `beta`, the
  one-root determinant over a `(j-2)` domain core is quadratic in the domain
  extension root.  Nonzero determinants give at most two residual extensions;
  identically-zero branches are inactive or fixed-slope and lift to
  `H_{3,j-1}(u+zv)(X-beta)ell_R=0`.
- **How it is useful:** This pushes the conic-secant one-outside target down
  from boundary shadows to a lower-dimensional boundary-core image after the
  appropriate lifted root-slice charges.
- **What to do next:** Bound or charge the resulting boundary-core image inside
  the quotient-aware M1 residue-line ledger.

### 2026-06-29 - M1 boundary-shadow conic-secant gate

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/notes/m1/m1_boundary_off_external_anchor_audit.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / BOUNDARY-SHADOW REDUCTION / AUDIT.
- **What is being added:** The boundary-shadow quadratic slope gate is
  rewritten as an equivalent anchor gate
  `A_S(beta)=det(a,b,(1,beta,beta^2))`; residual active one-outside pairs are
  exactly the nondegenerate conic-secant intersections, with charged zero-core
  and inactive proportional branches removed.
- **How it is useful:** This puts the outside-domain condition directly on a
  quadratic in the external anchor, giving a cleaner target for the remaining
  M1 boundary-shadow image bound.
- **What to do next:** Bound the conic-secant shadow image after quotient,
  tangent/contained, and fixed-slope boundary charges.

### 2026-06-29 - M1 boundary-shadow quadratic gate

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/notes/m1/m1_boundary_off_external_anchor_audit.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / BOUNDARY-SHADOW REDUCTION / AUDIT.
- **What is being added:** For each fixed boundary shadow, the recovered-anchor
  condition is the quadratic slope gate
  `Q_S(z)=c_1(z)^2-c_0(z)c_2(z)`.  If the gate is nonzero it has at most two
  candidate finite slopes; if it is identically zero, the line lies on one
  rank-one cone generator and any recovered anchor is inactive or already
  charged.
- **How it is useful:** This sharpens the residual one-outside M1 boundary
  target from a rank-one shadow incidence into a nonzero quadratic-root shadow
  problem.
- **What to do next:** Bound shadows whose nonzero quadratic gate has an
  outside-domain active recovered root.

### 2026-06-29 - M1 boundary-shadow anchor recovery

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/notes/m1/m1_boundary_off_external_anchor_audit.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / BOUNDARY-SHADOW REDUCTION / AUDIT.
- **What is being added:** A residual one-outside shadow and slope recover
  their external anchor from the lifted Hankel triple: outside the already
  charged zero core, the condition is `c_0 != 0`, `c_1^2=c_0 c_2`, and
  `beta=c_1/c_0`.
- **How it is useful:** This removes the existential external-anchor
  quantifier from the boundary-shadow task, turning it into a scalar rank-one
  Hankel condition plus the recovered-anchor outside-domain and active filters.
- **What to do next:** Bound the resulting rank-one boundary shadow image in
  the quotient-aware residue-line ledger.

### 2026-06-29 - M1 boundary-off shadow reduction

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/notes/m1/m1_boundary_off_external_anchor_audit.md`,
  `experimental/notes/m1/m1_hankel_variable_line_packet_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / BOUNDARY-LEDGER REDUCTION / AUDIT.
- **What is being added:** The one-outside boundary target image is reduced
  to its domain-shadow image after fixed-slope boundary root slices are
  charged: each residual shadow fiber has size at most two, and repeated
  finite slopes in a fiber already lift to `H_{3,j-1}`.
- **How it is useful:** This converts the boundary term left by the
  non-fixed line-packet closure criterion from an external-anchor
  multiplicity problem into a lower-dimensional shadow-image problem.
- **What to do next:** Prove a polynomial bound for the residual boundary
  shadow image, alongside the active different-slope two-exchange codegree.

### 2026-06-29 - M1 variable-line hypothesis discharge

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_variable_line_packet_lemma.md`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / LEDGER-INTEGRATION / AUDIT.
- **What is being added:** The variable-line packet reduction is updated to
  consume the constant non-fixed line-packet collapse from
  `m1_same_slope_root_slice_lemma.md`: after fixed-root and full-plane
  charges, surviving fixed-sum and product-Mobius packets automatically have
  injective finite-slope maps.
- **How it is useful:** This removes an extra local hypothesis from the
  non-fixed line-packet ledger, so the reduction applies directly to every
  surviving non-fixed two-root line packet in the `t=2` Hankel branch.
- **What to do next:** Bound the two live objects left by the closure
  criterion: active different-slope two-exchange codegree and one-outside
  boundary target image.

### 2026-06-29 - M1 non-fixed line-packet collapse

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / LINE-PACKET REDUCTION / AUDIT.
- **What is being added:** In the `t=2` Hankel setting, a fixed-sum or
  nondegenerate product-Mobius two-root line packet that is constant at one
  finite slope forces the full-plane lift `H_{4,j-2}(u+zv)ell_R=0`.
- **How it is useful:** After fixed-root and full-plane charges, every
  surviving non-fixed line packet has injective finite-slope map.  This
  removes the extra variable-slope hypothesis from the local variable-line
  packet reduction.
- **What to do next:** Use this injective packet branch together with the
  different-slope two-exchange and one-outside boundary ledgers.

### 2026-06-29 - M1 affine packet average ledger

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / LEDGER-COROLLARY / AUDIT.
- **What is being added:** The residual exchange-degree bound is substituted
  into the average support-collinearity ledger for one affine `h`-exchange
  packet, giving an explicit higher-exchange bound for
  `B_tau^max(A_res)` after full moving fibers are charged.
- **How it is useful:** This turns the local moving-fiber filtration into the
  average-ledger input needed by the M1 aperiodic residue-packing program,
  while keeping the statement local rather than claiming a global packing
  theorem.
- **What to do next:** Combine this packet-local ledger with packet counting
  and the quotient, tangent/contained, split-root, and fixed-slope ledgers.

### 2026-06-29 - M1 residual exchange-degree bound

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / GRAPH-DEGREE COROLLARY / AUDIT.
- **What is being added:** The moving-fiber count is converted into a local
  residual graph bound: after full moving `r`-root fibers are charged, the
  residual `r`-exchange graph inside one affine packet has maximum degree at
  most `binom(h,r)(|F|^(r-1)-1)`.
- **How it is useful:** This is the codegree-facing form of the packet
  filtration.  It gives zero residual one-exchange degree, the line-packet
  ceiling for two-exchange moves, and a uniform local degree input for higher
  exchange ledgers.
- **What to do next:** Feed this local degree bound into the remaining
  different-slope and average-collinearity ledgers after quotient and
  tangent/contained filters.

### 2026-06-29 - M1 moving-fiber finite-field count

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / COUNTING-COROLLARY / AUDIT.
- **What is being added:** The moving-fiber dimension drop is converted into
  an explicit finite-field count: after the full moving `r`-root fiber is not
  present, a fixed fiber contributes at most `|F|^(r-1)` formal residual
  parameters.
- **How it is useful:** This is the packet-counting input for the residual M1
  ledger.  It recovers the one-root singleton bound and two-root line-packet
  ceiling, and it gives the corresponding formal ceiling for every moving
  rank `r`.
- **What to do next:** Combine this local fiber count with quotient,
  tangent/contained, split-root, and different-slope ledgers to get global
  residual packet estimates.

### 2026-06-29 - M1 general moving-fiber dimension drop

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / FULL-PACKET REDUCTION / AUDIT.
- **What is being added:** The rank-defect packet filtration now has a general
  moving-fiber theorem: for a fixed `(h-r)` core, the coefficient map from a
  moving monic `r`-root factor is an affine embedding, so the preimage of any
  affine packet is an affine subspace of `F^r`.
- **How it is useful:** If that preimage has full affine rank `r`, the whole
  moving `r`-root fiber is present and is charged to the `(t+r,j-r)` full
  elementary-packet lift; otherwise the residual intersection drops to
  dimension at most `r-1`.  This packages the one-root edge removal and
  two-root line-packet reduction into a single lossless dimension-drop rule.
- **What to do next:** Use the dimension-drop rule as the organizing invariant
  for residual affine packets before attacking the remaining different-slope
  and quotient/tangent ledgers.

### 2026-06-29 - M1 affine two-root fiber dichotomy

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / TWO-EXCHANGE PLANE REDUCTION / AUDIT.
- **What is being added:** The affine rank-defect packet filtration now has a
  two-root fiber dichotomy: if a packet contains three non-collinear points of
  a fixed `(s,p)` two-root coefficient plane, then it contains the whole plane;
  otherwise the intersection is at most a line packet.
- **How it is useful:** The whole-plane case is exactly the already proved
  `(t+2,j-2)` Hankel full-plane lift.  After full planes are charged, residual
  affine rank-defect packets reduce on every two-root fiber to line packets,
  matching the fixed-root/fixed-sum/product-Mobius classification.
- **What to do next:** Attack the remaining line-packet and different-slope
  ledgers after quotient, tangent/contained, root-slice, and full-plane
  charges.

### 2026-06-29 - M1 affine-subpacket fiber dichotomy

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / ROOT-SLICE REDUCTION / AUDIT.
- **What is being added:** The one-root fiber dichotomy is extended from
  coefficient hyperplanes to every affine rank-defect packet `A=c_*+W`: a
  fixed one-root fiber meets `A` in at most one point unless the whole fiber
  lies in `A`.
- **How it is useful:** After full one-root fibers are charged to the lifted
  root-slice ledger, residual affine rank-defect packets have no one-exchange
  edges.  This pushes the lossless packet filtration beyond codimension-one
  hyperplanes and removes another possible source of hidden same-slope
  clustering.
- **What to do next:** Use the edge-free residual affine packets as the input
  to the remaining different-slope and two-exchange ledgers.

### 2026-06-29 - M1 coefficient-hyperplane fiber dichotomy

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / ROOT-SLICE REDUCTION / AUDIT.
- **What is being added:** A codimension-one coefficient hyperplane now has a
  one-root fiber dichotomy: along any fixed monic `(h-1)` core, its equation is
  affine-linear in the new root `y`, so the fiber has at most one extension
  unless the whole affine one-root line lies in the hyperplane.
- **How it is useful:** In the killed same-slope packet setting, a full
  one-root line is exactly a root-slice event and lifts to the `(t+1,j-1)`
  Hankel core.  After charging these full fibers, residual hyperplane packets
  have no one-exchange edges, tightening the rank-defect packet filtration.
- **What to do next:** Use this fiber dichotomy when attacking the remaining
  non-evaluation hyperplane packets and their different-slope/two-exchange
  ledgers.

### 2026-06-29 - M1 same-slope one-exchange root-slice lemma

- **Agent/model:** AllenGrahamHart / Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_same_slope_root_slice_lemma.md`,
  `experimental/scripts/verify_m1_same_slope_root_slice_lemma.py`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / ROOT-SLICE REDUCTION / AUDIT.
- **What is being added:** Same-slope one-exchange collisions in the
  Hankel-pencil landing equation force a whole fixed-slope root slice:
  two extensions through a common `(j-1)` core imply
  `L_z ell_R=L_z(X ell_R)=0`, equivalently a lifted
  `H_{t+1,j-1}(u+zv)ell_R=0` core.  In the `t=2` gate, anchors through the
  same core also satisfy a quadratic determinant equation, so three anchors
  force a ruled determinant branch.  Ruled affine cores are classified into
  fixed finite slope, inactive direction, or rank-one moving-slope branches,
  and the Hankel shift identity collapses the moving branch: every active ruled
  Hankel core is fixed finite slope.  One-exchange triangles are classified as
  either star triangles through a `(j-1)` core or top-packet triangles inside a
  `(j+1)` set, and residual top-packet edges with distinct slopes lift to a
  common `t=1` Hankel kernel.  The top-packet edge and triangle ledgers then
  compress into the simultaneous lifted `t=1` top-kernel family `K_top(u,v)`.
  One-exchange collisions inside the simultaneous top-kernel family are also
  shown to recurse losslessly: two `K_{r,d}(u,v)` extensions through a common
  `(d-1)` core force that core into `K_{r+1,d-1}(u,v)`.
  A two-exchange full-plane lift is also proved: three non-collinear
  same-slope points in a two-root plane force the lifted
  `H_{t+2,j-2}(u+zv)ell_R=0` core, so residual same-slope two-exchange
  components are line packets after full planes are charged.  This is now
  generalized to full affine-rank `h`-exchange packets: `h+1` affinely
  independent same-slope coefficient points force the lifted
  `H_{t+h,j-h}(u+zv)ell_R=0` core, and the simultaneous `K_{r,d}(u,v)` version
  lifts full-rank packets to `K_{r+h,d-h}(u,v)`.  The complementary
  affine-span normal form identifies every lower-rank killed packet as the
  whole affine subpacket `c_*+W` cut out by the corresponding base and
  direction equations on the shifted Hankel landing vectors.  Codimension-one
  coefficient packets are fixed-root slices exactly when their hyperplane is
  an evaluation hyperplane `P_c(alpha)=0`, equivalently projectively
  `(a_0,...,a_{h-1},b)=(1,alpha,...,alpha^h)`.  The residual affine two-root
  lines are classified as fixed-root, fixed-sum, or product-Mobius;
  after fixed-root charging, the residual variable-line models are exactly
  fixed-sum and nondegenerate product-Mobius packets.
  The same Hankel shift collapse classifies the one-outside external-anchor
  ruled branch: after fixed-slope boundary slices are charged, each shadow has
  at most two active non-ruled external anchors.
  The resulting residual degree bound is also inserted into the existing
  average-collinearity max-codegree ledger.
- **How it is useful:** After fixed-slope root slices are charged, the
  residual one-exchange graph has only different-slope edges and the charged
  same-slope mass is explicitly assigned to the higher-slack Hankel ledger.
  Since ruled Hankel cores collapse to fixed-slope or inactive cores, each
  `(j-1)` core contributes at most one unordered residual one-exchange edge;
  consequently the residual `t=2` one-exchange graph has maximum degree at most
  `j` and average-ledger error term at most `(1-p_z)/(M p_z)+4jQ/M`.  Residual
  one-exchange triangles must be top-packet triangles lying over the lifted
  `t=1` kernel target from the all-line Hankel audit, with edge and triangle
  counts bounded by `binom(j+1,2)|K_top|` and `binom(j+1,3)|K_top|`.  The
  one-outside ruled branch is no longer a separate unclassified residual; it
  is either inactive or charged to the lifted fixed-slope boundary root-slice
  ledger.  The variable-line packet note's `full-plane removed` hypothesis is
  now backed by a proved `(t+2,j-2)` Hankel lift and an explicit classification
  of the residual affine line packets.  The top-kernel recursion records the
  residual-depth frontier shift as an exact identity, so one-exchange
  clustering inside `K_top` is charged additively to the next simultaneous
  Hankel kernel rather than treated as a new multiplicative loss source.  The
  full `h`-exchange lift extends that lossless frontier shift from edges and
  planes to arbitrary full affine-rank elementary packets.  The rank-defect
  normal form makes the remaining same-slope packet classification explicit:
  after full-rank charges, only lower-dimensional affine coefficient packets
  remain.  The fixed-root hyperplane criterion charges the evaluation
  hyperplanes inside that residual filtration to the lower-exchange
  root-slice ledger.
- **What to do next:** Bound the remaining different-slope one-exchange or
  two-exchange codegree ledgers, the isolated simultaneous top-kernel family,
  and the one-outside boundary image after quotient-periodic,
  tangent/contained, and root-slice charges.

### 2026-06-29 - Paper D v7 first-grid cap promotion

- **Agent/model:** Codex.
- **Files added or changed:** `tex/cs25_cap_v7.tex`, `cs25_cap_v7.pdf`,
  `site/papers/cs25_cap_v7.pdf`,
  `experimental/notes/audits/paperD_v7_vs_v6_audit.md`, scanner status labels,
  `readme.md`, and site paper/leaderboard/update data.
- **Status:** AUDIT / VERSION-PROMOTION / PROVED_PAPERD_V7_CAP /
  PROVED_PAPERD_V7_FIRST_GRID.
- **What is being added:** Paper D v7 is promoted as the current public Paper D
  source. It preserves the v6 universal fixed-divisor MCA cap, extends the
  no-loss CA endpoint to `floor(delta n) <= n-k-1`, and adds the first-grid
  deep-point cap for large official-envelope rows.
- **How it is useful:** The public board can now show two Paper D theorem
  layers: the older uniform fixed-divisor cap and the stronger large-row
  first-grid cap `delta*_C(2^-128) <= 1-rho-1/n`.
- **What to do next:** Keep first-grid rows separate from exact-threshold
  claims. The missing safe-side work remains the L1/M1/F1/M2 completion package.

### 2026-06-29 - PR #136 width-one fixed-root closure

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:** `experimental/notes/m1/m1_width_one_fixedroot_closure.md`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`, and
  `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / CONDITIONAL-CLOSURE / AUDIT.
- **What is being added:** A compact width-one M1 closure note: width-one
  maximal root shadows are bounded-complement rank tests, descend losslessly
  under fixed-root absorption, and inject into one-root fixed-divisor/root-slice
  ledgers.
- **How it is useful:** It reduces the width-one critical-tail branch to the
  existing one-root fixed-root ledger in fixed surplus, giving a smaller target
  for the M1 proof program without promoting a full all-line theorem.
- **What to do next:** Prove or import the polynomial fixed-surplus bound for
  `FixedRootOneRoot_{r1}` after quotient-periodic, tangent, fixed-root, and
  aperiodic charges; do not treat this as a leaderboard row.

### 2026-06-29 - PR #131--#135 triage and frontier rows

- **Agent/model:** Codex, auditing PRs from AllenGrahamHart, Scott Hughes, and
  Vadim Avdeev.
- **Files added or changed:** `experimental/notes/triage/pr-triage-2026-06-29.md`,
  `experimental/notes/m1/m1_boundary_off_external_anchor_audit.md`,
  `experimental/notes/m1/m1_a507_adjacent_bridge_theorem.md`,
  `experimental/notes/m1/m1_a507_plus_one_slope_hunt.md`,
  `experimental/notes/m1/m1_interleaved_list_*.md`,
  `experimental/notes/m1/m1_random_simple_pole_entropy_floor.md`,
  `experimental/notes/m1/m1_coset_packet_finite_slope_floors.md`,
  matching JSON certificates under `experimental/data/`, matching verifiers
  under `experimental/scripts/`, `experimental/experiments.tex`, and site data.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM / PROOF_RECORD / LOWER_BOUND /
  ROUTE_CUT / AUDIT.
- **What is being added:** The PR wave adds three useful frontier-facing
  packets: Scott Hughes's interleaved-list hybrid certificate
  `Lambda_mu(C,326) >= 7`, Vadim Avdeev's random simple-pole finite-slope floors
  for `a=257..260`, and Vadim Avdeev's coset-packet finite-slope floors for
  `a=261..288`. AllenGrahamHart's boundary-off external-anchor M1 normal form is
  distilled into a compact proof-program audit, and Scott Hughes's `a=507`
  adjacent-bridge packet is integrated as a route cut rather than a new row.
- **How it is useful:** The finite-slope floors strengthen the low-agreement
  side of the `F_17^32, n=512, k=256` MCA ledger, while the interleaved-list
  packet moves the separate list-track lower-bound row up to agreement `326`.
  The route-cut notes prevent accidental mixing of adjacent line/list
  numerators into the same finite-slope MCA denominator.
- **What to do next:** Human-review the finite-slope-to-MCA noncontainment
  convention before paper promotion, keep #131 as proof-program material until
  it proves a global M1 bound, and treat the Sage scripts in #133 as optional
  independent audits rather than required local verification.

### 2026-06-29 - Paper D v6 promotion and completion-program audit

- **Agent/model:** Codex.
- **Files added or changed:** `tex/cs25_cap_v6.tex`, `cs25_cap_v6.pdf`,
  `site/papers/cs25_cap_v6.pdf`,
  `experimental/notes/audits/paperD_v6_vs_v5_audit.md`, scanner status labels,
  `readme.md`, and site paper/leaderboard/update data.
- **Status:** AUDIT / VERSION-PROMOTION / PROVED_PAPERD_V6_CAP.
- **What is being added:** Paper D v6 is promoted as the current public Paper D
  source. It keeps the v5 universal MCA cap constants and CS25-free route,
  tightens the conversion collision-count derivation, and adds the
  prize-facing integer-staircase/completion program.
- **How it is useful:** Public rows now cite the strongest Paper D package:
  same cap theorem, clearer prize posture, and explicit conditional MCA/list
  completion theorems for turning the one-sided cap into a full threshold
  determination.
- **What to do next:** Use `PROVED_PAPERD_V6_CAP` for verified Paper D cap rows,
  while keeping the missing L1/M1/F1/M2 completion obligations separate from
  the proved cap itself.

### 2026-06-27 - Root-level paper PDF relocation

- **Agent/model:** Codex.
- **Files added or changed:** `cs25_cap_v5.pdf`, `slackMCA_v4.pdf`,
  `snarks_v5.pdf`, removed generated PDF outputs from `tex/`,
  `site/data/papers.json`, `site/index.html`, `experimental/agents-log.md`.
- **Status:** AUDIT / RELEASE-HYGIENE.
- **What is being added:** The generated Paper B/C/D PDFs are moved out of
  `tex/` into the repository root, matching the README convention that TeX
  sources live under `tex/` and PDFs live at the root. Site-local mirrors under
  `site/papers/` remain for static hosting.
- **How it is useful:** Keeps GitHub PDF links and repository layout aligned
  with the public paper set: B v4, C v5, and D v5.
- **What to do next:** Keep future TeX compile outputs copied to root and, when
  needed, mirrored into `site/papers/` for static-site serving.

### 2026-06-27 - Paper B/C/D version promotion and leaderboard source audit

- **Agent/model:** Codex.
- **Files added or changed:** `tex/slackMCA_v4.tex`,
  `slackMCA_v4.pdf`, `tex/snarks_v5.tex`, `snarks_v5.pdf`,
  `site/papers/slackMCA_v4.pdf`, `site/papers/snarks_v5.pdf`, `readme.md`,
  `site/data/rate-leaderboards.json`, `site/data/updates.json`,
  `site/index.html`, `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** Two clarification edits are added to the promoted
  Paper B/C versions: the Paper B unsplit curve-envelope lower bound is
  explicitly the line witness embedded as a degree-`d` curve, and Paper C now
  says the curve compiler applies to the finite power-curve/evaluation-domain
  model rather than arbitrary protocol samplers. The README records the current
  public versions B v4, C v5, and D v5.
- **How it is useful:** Keeps the paper prose aligned with the public board:
  Paper D v5 cap rows are proved under their printed scanner hypotheses,
  high-agreement/list rows cite Paper B v4 after promotion, and Paper C v5 is
  framed as protocol-ledger packaging rather than a new cap row.
- **What to do next:** Commit the version promotion after final review, and
  keep future leaderboard rows explicit about whether they are Paper B
  high-agreement theorem rows, Paper D v5 cap rows, or Paper C protocol-ledger
  packaging rows.

### 2026-06-27 - M1 variable-line packet and singleton lemmas

- **Agent/model:** AllenGrahamHart / Codex audit.
- **Files added or changed:**
  `experimental/notes/m1/m1_hankel_variable_line_packet_lemma.md`,
  `experimental/experiments.tex`, `site/data/updates.json`,
  `site/index.html`, `experimental/agents-log.md`.
- **Status:** PROVED-LOCAL / PROOF-PROGRAM / AUDIT.
- **What is being added:** Local packet lemmas for non-fixed variable Hankel
  determinant lines: active-new packet mass is reduced to active domain
  singletons, quotient defects, and a different-slope two-exchange codegree
  image.  The singleton term is then reduced to contained/tangent and
  one-outside target images, with the zero-lower class eliminated in the
  high-agreement range `a>(n+1)/2`.
- **How it is useful:** This extracts a reviewable M1 reduction from the
  all-line Hankel packet while keeping it out of the leaderboard.  It narrows
  the remaining non-fixed variable-line branch to explicit target-image and
  codegree estimates.
- **What to do next:** Prove polynomial bounds for the active different-slope
  two-exchange codegree and the one-outside boundary target image inside the
  quotient-aware residue-line ledger; do not cite this as the final M1 theorem.

### 2026-06-27 - Paper D v5 cap status promotion in scanner and board

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/certificate_scanner/certificate_scanner.py`,
  `experimental/notes/certificate_scanner/README.md`,
  `experimental/notes/certificate_scanner/outputs/`,
  `experimental/notes/audits/a0_cs25_rational_constant_derivation.md`,
  `experimental/notes/audits/theorem_label_map.md`,
  `experimental/notes/audits/codex-f1-l1-20260617/README.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / ARITHMETIC-AUDIT.
- **What is being added:** The scanner now emits `PROVED_PAPERD_V5_CAP` for
  active Paper D v5 cap rows whose divisor, binomial, and field hypotheses pass,
  and `NO_ACTIVE_PAPERD_V5_CAP` when no such row is found. Existing scanner
  reports and leaderboard-sweep outputs are regenerated or mechanically updated
  to remove the old draft/CS25-import status, and stale experimental audit notes
  now mark that import route as relevant only to older CA/list comparisons.
- **How it is useful:** Aligns the public leaderboard and scanner with Paper D
  v5's self-contained MCA cap route. Verified Paper D cap rows are no longer
  marked with the older conditional-import or draft-example statuses.
- **What to do next:** Keep CA/list comparison statements separate from the MCA
  cap status, and update any remaining paper-level prose that still discusses
  the older CS25-dependent route as the main Paper D theorem.

### 2026-06-27 - Finite-row threshold note and pure-MCA scanner profile

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/notes/thresholds/f17_32_finite_mca_threshold.tex`,
  `experimental/notes/thresholds/f17_32_finite_mca_threshold.pdf`,
  `experimental/notes/certificate_scanner/examples/f17_512_mca_only.json`,
  `experimental/notes/certificate_scanner/outputs/f17_512_mca_only.report.json`,
  `experimental/notes/certificate_scanner/outputs/f17_512_mca_only.report.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL-SCANNER.
- **What is being added:** A standalone finite-row threshold note packages the
  \(\F_{17^{32}}, n=512,k=256\) row as an exact finite-slope support-wise MCA
  threshold: agreement \(506\) is unsafe, agreement \(507\) is safe, and the
  closed-real safe interval is \([0,6/512)\). A pure-MCA scanner profile is
  added so the 506/507 endpoint is not mixed with the optional line-plus-list
  protocol ledger.
- **How it is useful:** Supersedes the old strict264-next threshold plan for
  this finite row and gives the clean packaging needed for the public board and
  `towards-prize.md`. It also isolates the next theorem target: the
  row-independent high-agreement threshold compiler with
  \(B_Q=\lfloor Q/2^{128}\rfloor\).
- **What to do next:** Audit the official MCA sampler definition against the
  finite/projective slope conventions and decide whether to promote the
  row-independent compiler from experimental notes into a paper-level theorem.

### 2026-06-27 - Prime192 leaderboard sweep rows

- **Agent/model:** Codex, auditing `leaderboard_sweep_192`.
- **Files added or changed:** `experimental/notes/certificate_scanner/outputs/leaderboard_sweep_192/`,
  `experimental/notes/certificate_scanner/certificate_scanner.py`,
  `site/data/rate-leaderboards.json`, `site/data/updates.json`, and
  `site/index.html`.
- **Status:** PROVED_PAPERD_V5_CAP / AUDIT.
- **What is being added:** The scanner sweep contributes four concrete
  prime-field rows with `q` near `2^192`, `k=2^40`, smooth power-of-two
  subgroup domains, and one row per official prize rate. It also records a
  small `F_17^32` Paper D example at agreement `258`.
- **How it is useful:** These rows instantiate the Paper D v5 cap with exact
  field/domain arithmetic, making the theorem-envelope rows concrete without
  claiming a new theorem beyond Paper D or an explicit slope census.
- **What to do next:** Regenerate the sweep from a checked-in sweep script if
  the scanner API changes, and keep CA/list comparison statements separate from
  the proved MCA cap status.

### 2026-06-27 - PR #122--#129 triage and selective integration

- **Agent/model:** Codex, auditing PRs from AllenGrahamHart, Scott Hughes,
  and Vadim Avdeev.
- **Files added or changed:** `experimental/notes/triage/pr-triage-2026-06-27.md`,
  `experimental/notes/l1/l1_prefix_dual_d3_subgroup_twisted_collision_bound.md`,
  `experimental/notes/l1/l1_monomial_dyadic_descent_survivors.md`,
  `experimental/notes/f1/f1_arbitrary_anchor_locator_split.md`,
  `experimental/notes/m1/m1_all_line_hankel_aperiodic_packet_audit.md`,
  `experimental/data/adjacent-ledgers/`, selected verifier scripts, and
  `experimental/experiments.tex`.
- **Status:** PROVED / IMPORTED-STANDARD-INPUT / AUDIT / PROOF PROGRAM /
  EXPERIMENTAL.
- **What is being added:** New bounded L1/F1/M2 notes are integrated, while
  PR #127's large M1 generated packet is distilled into a smaller audit note.
  The public board is updated only for tangent-floor-backed status corrections:
  Cycle116/119 gates are unconditional but their exact Cycle84 numerator remains
  conditional, and reserve272/288/313 are marked as proved only because they are
  subsumed by tangent/strict352 floors.
- **How it is useful:** Adds useful L1 `d=3` proper-subgroup and monomial-prefix
  toy theorems, sharpens the F1 arbitrary-anchor ledger, and records
  challenge-map pullback accounting for protocol-facing high-agreement ledgers
  without promoting non-verified material to theorem status.
- **What to do next:** Split the M1 all-line aperiodic packet into small
  separately auditable verifiers before considering any stronger theorem claim;
  human-review the imported Katz/Gauss inputs in the L1 `d=3` note before moving
  it toward Paper B.

### 2026-06-27 - Promoted high-agreement TeX split

- **Agent/model:** Codex, verifying and promoting the user-supplied
  `experiments_v2.tex` split.
- **Files added or changed:** `experimental/experiments.tex`,
  `experimental/experiments.pdf`, `experimental/notes/high_agreement/`,
  `experimental/scripts/verify_promoted_high_agreement_ledgers.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / CONDITIONAL-PROTOCOL-LEDGER / AUDIT.
- **What is being added:** The bulky high-agreement tangent, CA/projective,
  curve, interleaved-list, current-row protocol, and general threshold compiler
  material is split into reusable TeX fragments under
  `experimental/notes/high_agreement/` and included from the canonical
  `experimental/experiments.tex` wrapper.
- **How it is useful:** Keeps the stable high-agreement theorem package
  reviewable in smaller files while preserving the compiled experimental memo.
  The split also fixes the stale missing backslash before the
  `Towards-Prize Finite-Threshold Theorems` section header.
- **What to do next:** Human-review the curve sampler caveat before citing the
  curve statements in protocol settings, and keep protocol query/folding,
  extension-lift, challenge-field, and cryptographic losses as separate ledger
  terms.

### 2026-06-26 - Generalized high-agreement ledgers

- **Agent/model:** GPT-5.5 Pro generalized-ledgers packet, audited and
  integrated by Codex.
- **Files added or changed:** `experimental/data/generalized-ledgers/`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`,
  `experimental/data/README.md`, `site/data/updates.json`, `site/index.html`.
- **Status:** PROVED / CONDITIONAL-PROTOCOL-LEDGER / ARITHMETIC-AUDIT.
- **What is being added:** A row-independent high-agreement ledger calculus for
  `RS[F,D,k]` rows: with `R=n-k`, `r=n-a`, and `B_Q=floor(Q/2^128)`, the exact
  line/CA/projective numerator is `r+1` in the range `r <= floor(R/3)`, the
  degree-`d` curve numerator is `d(r+1)` in the range
  `r <= floor(R/(d+2))`, and interleaved-list uniqueness holds for
  `r <= floor(R/2)`.
- **How it is useful:** This moves the adjacent-ledger conclusions beyond the
  special `F_17^32` row.  It gives a reusable integer calculator for deciding
  when tangent-star high-agreement terms alone can pin a `2^-128` threshold,
  and shows that at prize-scale dimensions the method stops pinning thresholds
  once field sizes are roughly above `2^166` to `2^170`, depending on rate.
- **What to do next:** Use this calculator before adding any new row to the
  public board, and keep quotient-core, generated-field entropy, challenge
  field, folding, query, and cryptographic terms as separate ledgers.

### 2026-06-26 - High-agreement adjacent CA/curve/list ledgers

- **Agent/model:** GPT-5.5 Pro adjacent-ledgers packet, audited and integrated
  by Codex.
- **Files added or changed:** `experimental/data/adjacent-ledgers/`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`,
  `site/data/frontier.json`, `site/data/updates.json`,
  `site/data/rate-leaderboards.json`, `site/index.html`.
- **Status:** PROVED / CONDITIONAL-PROTOCOL-LEDGER / ARITHMETIC-AUDIT.
- **What is being added:** The high-agreement tangent staircase is extended to
  no-loss CA, projective-slope support-wise MCA, finite-parameter degree-`d`
  curve CA/MCA, and MDS interleaved-list uniqueness.  For
  `RS[F_17^32,H,256]`, the line-plus-list coding ledger is unsafe at
  agreement `a=507` and safe at `a=508` when no query/folding loss is added.
- **How it is useful:** This answers the immediate adjacent-ledger question
  past the finite-slope `506/507` gate: the high-agreement CA/projective/curve
  and interleaved-list coding objects are now pinned by explicit integer
  formulae, rather than left as open checks.
- **What to do next:** Human-review protocol reductions before using the
  conditional ledger in SNARK claims, and add any query, folding, hash,
  extension-lift, or cryptographic error terms explicitly.

### 2026-06-26 - Tangent-star extremizer barrier

- **Agent/model:** GPT-5.5 Pro tangent-star packet, audited and integrated by
  Codex.
- **Files added or changed:** `experimental/data/tangent-star/`,
  `experimental/experiments.tex`, `experimental/agents-log.md`,
  `site/data/frontier.json`, `site/data/updates.json`,
  `site/data/rate-leaderboards.json`, `site/index.html`.
- **Status:** PROVED / NEW-LOCAL / FINITE-SLOPE STRUCTURAL BARRIER.
- **What is being added:** A refinement of the high-agreement tangent
  staircase: in the exact range `3a-2n >= k`, extremal finite-slope
  support-wise `LD_sw` lines are tangent-star lines.  For
  `RS[F_17^32,H,256]`, this rules out a seventh finite-slope bad branch at
  every agreement `a >= 507`.
- **How it is useful:** It closes the previous finite-slope follow-up question
  left by the tangent staircase: no non-tangent mechanism can push the current
  `F_17^32`, `n=512`, `k=256` row past the `506/507` gate under the
  finite-slope support-wise MCA convention.
- **What to do next:** Use the adjacent-ledgers packet for the high-agreement
  CA/projective/curve/list coding objects, and keep protocol, challenge-field,
  extension-lift, folding, query, and cryptographic losses as separate ledgers.

### 2026-06-26 - High-agreement tangent staircase

- **Agent/model:** GPT-5.5 Pro tangent packet, audited and integrated by Codex.
- **Files added or changed:** `experimental/data/tangent/`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`.
- **Status:** PROVED / ARITHMETIC-AUDIT / FINITE-SLOPE-THRESHOLD.
- **What is being added:** A generic moving-root tangent floor
  `LD_sw(C,a) >= n-a+1` for Reed--Solomon codes, plus a matching upper bound in
  the very-high-agreement range `3a-2n >= k` using the common code-line
  residual budget.
- **How it is useful:** For `RS[F_17^32,H,256]` with `|H|=512`, this proves
  `LD_sw(C,a)=513-a` for every `a>=427`, so `LD_sw(C,506)=7` and
  `LD_sw(C,507)=6`.  Thus the finite-slope support-wise `2^-128` staircase is
  pinned between agreements `506` and `507`; agreement `353` and the strict352
  quotient-core frontier are superseded by the tangent floor.
- **What to do next:** Human-review the endpoint convention and use the
  adjacent-ledgers packet for the high-agreement CA/projective/curve/list
  coding objects; protocol-facing losses still need separate ledgers.

### 2026-06-26 - L1 d=2 cubic subgroup twisted bound

- **Agent/model:** Scott Hughes PR #121, integrated by Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_prefix_dual_d2_cubic_subgroup_twisted_bound.md`,
  `experimental/notes/triage/l1-prefix-dual-d2-cubic-subgroup-twisted-bound-import-audit-2026-06-26.md`,
  `experimental/scripts/verify_l1_prefix_dual_d2_cubic_subgroup_twisted_bound.py`,
  `experimental/notes/triage/pr-triage-2026-06-26-round2.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / STANDARD-WEIL-INPUT / AUDIT.
- **What is being added:** A `d=2` cubic proper-subgroup collision bound for
  the actual `H^{2k}` object, using exact Fourier reconstruction,
  multiplicative-character expansion of `1_H`, and a conservative
  one-variable mixed character-sum bound.
- **How it is useful:** Separates proper-subgroup counting from full-affine
  Hooley--Katz geometry and gives an L1 template for higher odd-moment twisted
  subgroup bounds.  It is not a new MCA leaderboard row.
- **What to do next:** Pin the imported Katz/Gauss source constants and test
  whether the method extends to higher odd moments with reserve-scale margins.

### 2026-06-26 - L1 odd-moment Hooley-Katz audit

- **Agent/model:** Scott Hughes PR #120, integrated by Codex.
- **Files added or changed:**
  `experimental/notes/l1/l1_prefix_dual_odd_moment_projective_geometry.md`,
  `experimental/notes/triage/l1-prefix-dual-odd-moment-hooley-katz-import-audit-2026-06-26.md`,
  `experimental/scripts/verify_l1_prefix_dual_odd_moment_hooley_katz_audit.py`,
  `experimental/notes/triage/pr-triage-2026-06-26-round2.md`,
  `experimental/agents-log.md`.
- **Status:** PROVED / IMPORTED-VERIFIED / AUDIT / ROUTE CUT.
- **What is being added:** A projective odd-moment collision-geometry theorem
  for `k>d`, affine-cone conversion, and a Hooley--Katz/Ghorpade--Lachaud
  constant ledger for the full-affine point-count route.
- **How it is useful:** Records why the generic full-affine point-count route
  is not enough for the subgroup L1 reserve-scale problem and prevents ledger
  mixing between full-affine, full-torus, and proper-subgroup counts.
- **What to do next:** Human-check imported theorem citations and use the
  audit as a route cut unless sharper geometry-specific constants are found.

### 2026-06-26 - Strict352 dyadic quotient-core MCA floor audit

- **Agent/model:** Codex, auditing user-supplied strict352 packet.
- **Files added or changed:** `experimental/data/strict352/`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / SUPPORT-WISE-MCA-LOWER-BOUND.
- **What is being added:** A dyadic quotient-core proof packet for
  `RS[F_17^32,H,256]`, `|H|=512`, showing `LD_sw(C,a) >= 7` for every
  agreement `264 <= a <= 352`, with `LD_sw(C,352) >= 16` under the
  finite-slope support-wise MCA convention.
- **How it is useful:** Records a quotient-core mechanism for agreements up to
  `352`.  This was briefly the lower-bound frontier, but it is now superseded
  by the generic tangent floor, which gives `LD_sw(C,352) >= 161` and
  `LD_sw(C,353) >= 160`.
- **What to do next:** Keep the packet as a quotient-core mechanism record and
  compare it against any non-tangent mechanisms that might survive past
  agreement `507`.

### 2026-06-26 - Strict264 quotient-floor proof packet

- **Agent/model:** Codex, with user-supplied strict264 packet.
- **Files added or changed:** `experimental/data/strict264/`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT.
- **What is being added:** A strict264 quotient-core proof packet: generated
  field entropy/list-floor notes, a deep-point list-to-MCA conversion section,
  a calculator for entropy/MCA floors, and the concrete
  `RS[F_17^32,H,256]`, `|H|=512`, agreement-264 quotient-floor obstruction.
  The local audit fixed two TeX transcription errors and regenerated the saved
  calculator output with the exact value `log2(17^32)`.
- **How it is useful:** Gives a direct quotient-core route to
  `epsilon_mca(C,31/64)>2^-128`: `binom(64,33)` augmented-code list points
  imply at least nine support-wise bad slopes after the deep-point conversion,
  while seven slopes already clear the `F_17^32` denominator.
- **What to do next:** Keep the theorem package as a quotient-core mechanism
  record.  The moving-root tangent floor supersedes the old strict264/265
  target by giving `LD_sw(C,264) >= 249`.

### 2026-06-26 - Towards-prize finite-threshold theorem section

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/experiments.tex`,
  `experimental/agents-log.md`.
- **Status:** PROVED / CONDITIONAL / AUDIT.
- **What is being added:** A new `Towards-Prize Finite-Threshold Theorems`
  section for `experiments.tex`: certificate-to-`LD_sw`, fixed-locator
  unique-slope, base-valued subfield confinement, the exact seven-slope
  arithmetic gate over `F_17^32`, and the one-step staircase pinning criterion.
- **How it is useful:** Converts the strict264 and 265 goals into theorem-level
  proof obligations that agents can attack without claiming a new numerator or a
  corrected-reserve MCA theorem.
- **What to do next:** Use the fixed-locator principle to build
  duplicate-aware strict264 and 265 search certificates.

### 2026-06-26 - One-by-one experiment run

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/data/experiment-run-2026-06-26.json`,
  `experimental/notes/triage/experiment-run-2026-06-26.md`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`,
  `site/data/updates.json`.
- **Status:** AUDIT / EXPERIMENTAL RUN.
- **What is being added:** A sequential run of the current Cycle120,
  strict264, reserve-ladder, F1, L2, A0, and M2 validators.  All executed
  scripts passed, but no script produced a new retained-slope certificate or
  improved frontier numerator.
- **How it is useful:** Confirms that the current proof infrastructure is
  internally consistent and isolates the exact next strict264 blocker:
  seven explicit retained bad slopes at agreement `264` for the
  `RS[F_17^32,H,256]` row.
- **What to do next:** Build the strict264 seven-slope certificate and an
  independent replayable certificate for the existing `52,747,567,092` count.

### 2026-06-26 - PR #108--#119 proof and audit integration

- **Agent/model:** AllenGrahamHart PRs #108--#112, #114--#118, Scott Hughes
  PRs #113 and #119, reviewed and integrated by Codex with topic-split validity
  checks.
- **Files added or changed:** `experimental/notes/triage/pr-triage-2026-06-26.md`,
  `experimental/data/pr-triage-2026-06-26.json`,
  `experimental/experiments.tex`, `experimental/experiments.pdf`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`, plus new or updated
  notes and scripts under `experimental/notes/{audits,f1,l1,l2,m1,m2}/` and
  `experimental/scripts/`.
- **Status:** PROVED / CONDITIONAL / AUDIT / EXPERIMENTAL.
- **What is being added:** A one-by-one integration of PRs #108--#119.  The
  theorem-level additions are the F1 syndrome-pencil normal form, the L2
  codegree reduction, the A0 deep-point MCA-cap dependency split, and the M2
  common code-line residual budget.  The remaining material is kept as route
  cuts, audits, or proof programs.
- **How it is useful:** Gives future theory work cleaner local statements for
  F1, L2, Paper D/A0, and M2, while preserving conservative public status.  No
  new prize-worthy numerator or frontier point is claimed.
- **What to do next:** Human-review the theorem-level additions before any
  main-paper promotion, citation-check the mixed-Weil route in PR #119, and
  require a retained-slope proof before treating strict264 as more than a
  target.

### 2026-06-25 - Latest PR integration and estimate audit

- **Agent/model:** AllenGrahamHart PRs #101--#107, ScottDHughes PR #99, and
  Cycle120 audit material from PR #100/#105, integrated by Codex.
- **Files added or changed:** `experimental/notes/triage/pr-triage-2026-06-25.md`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`, plus new or updated
  notes and scripts under `experimental/notes/{audits,f1,l1,l2,m1,m2,x1}/`,
  `experimental/scripts/`, and `experimental/lean/rs_mca_formalization/`.
- **Status:** AUDIT / EXPERIMENTAL / PROOF-CHECK-NEEDED / CONDITIONAL.
- **What is being added:** A one-by-one integration of PRs #99--#107. The
  Cycle120 numerator is unchanged at `52,747,567,092`; the useful improvements
  are the standalone Cycle120 `LD_sw` proof note, the exact M2
  `epsilon_mca = LD_sw/|F|` bridge, stronger F1 extension-line lower floors,
  an M1 beta-pushforward spectral audit, and sharper L1/L2 proof-program
  targets.
- **How it is useful:** Gives future theory work better normalized estimates
  without editing Papers A--D. In particular, the current ABF-row obstruction
  still points to `epsilon_mca(C,125/256)>2^-128` and the Cycle119 strict
  endpoint `delta*_C <= 249/512`, while L1/L2/F1/X1 now have cleaner
  follow-up notes and standard-library verifiers.
- **What to do next:** Do a human proof review of the standalone Cycle120
  proof chain, then run selected nonmutating verifiers in a controlled pass.
  Treat PR #100's raw generated packet as superseded by the compact audit and
  standalone proof note unless a reviewer explicitly needs the raw replay
  material.

### 2026-06-23 - Cycle119 admissibility review

- **Agent/model:** DannyExperiments PR #96, reviewed by Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_cycle119_strict263_admissibility_review.md`,
  `experimental/notes/triage/pr-triage-2026-06-23.md`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`, plus wording cleanup
  in the prior Cycle84 public replay audit.
- **Status:** AUDIT / PROOF-CHECK-NEEDED / COMPUTATION-DEPENDENT.
- **What is being added:** A compact review of the Cycle119 strict-263 claim:
  `LD_sw(RS[F_17^32,H,256],263) >= 52,747,567,092`, with `|H|=512`, and an
  admissibility check against the local ABF-aligned definitions and public
  Proximity Prize page.
- **How it is useful:** Separates the potentially important theorem claim from
  Danny's raw/generated PR branch. The branch is not integrable as-is, but the
  two-ended locator transfer is now the right object to demand as a clean proof.
  If the proof and finite computation check out, the right public framing is a
  prize-facing negative counterexample candidate under the printed ABF
  formulation, not an accepted prize solution.
- **What to do next:** Independently fetch and check the ABF PDF, then ask Danny
  for a standalone human-readable proof of the two-ended locator transfer and a
  separate minimal record of the Cycle84 finite computation it consumes.

### 2026-06-23 - Cycle120 ABF counterexample candidate integration

- **Agent/model:** DannyExperiments PR #96, reviewed by Codex.
- **Files added or changed:**
  `experimental/notes/m1/m1_cycle120_abf_counterexample_candidate.md`,
  `experimental/notes/m1/m1_cycle119_strict263_admissibility_review.md`,
  `experimental/notes/triage/pr-triage-2026-06-23.md`,
  `experimental/SUMMARY.md`, and `experimental/agents-log.md`.
- **Status:** CONDITIONAL / PROOF-SPINE-CHECKED / COMPUTATION-DEPENDENT /
  SOURCE-AUDIT.
- **What is being added:** A cleaned integration of the Cycle120 ABF-facing
  negative result. It records that Cycle116 agreement `262` is enough for the
  printed ABF closed threshold at `delta=125/256`, while Cycle119 agreement
  `263` checks as a strict-ball strengthening. The note now states explicitly
  that this is only a negative obstruction to
  `epsilon_mca(C,125/256) <= 2^-128` for one row, not ordinary list decoding,
  protocol soundness, or an exact determination of `delta*_C`. It also records
  the endpoint nuance: Cycle116 gives `delta*_C <= 125/256` under a supremum
  convention, while Cycle119 gives `delta*_C <= 249/512 < 125/256`.
- **How it is useful:** Moves the useful part of PR #96 into a compact
  experimental note without importing zips, generated checkers, copied PDFs,
  rendered pages, or raw prompt archives. It gives the project a concrete
  human-review target: the Cycle84/Cycle116 finite proof chain plus the
  optional Cycle119 strict-ball proof.
- **What to do next:** Independently retrieve the ABF PDF, review the finite
  count and fixed-jet transfer, and ask Danny for a minimal nonmutating reviewer
  packet in proof/computation/audit language.

### 2026-06-22 - PR #96-#98 experimental triage

- **Agent/model:** DannyExperiments, avdeevvadim, scottdhughes; integrated by
  Codex.
- **Files added or changed:**
  `experimental/notes/triage/pr-triage-2026-06-22.md`,
  `experimental/notes/m1/m1_cycle84_public_replay_audit.md`,
  `experimental/notes/f1/f1_deep_point_list_to_ca_mca.md`,
  `experimental/scripts/f1_deep_point_list_to_ca_mca_sanity.py`,
  `experimental/notes/l1/l1_prefix_fourier_orbit_cancellation.md`,
  `experimental/scripts/verify_l1_fourier_orbit_cancellation.py`,
  `experimental/SUMMARY.md`, `experimental/README.md`,
  `experimental/scripts/README.md`, and `experimental/agents-log.md`.
- **Status:** AUDIT / FINITE_MODEL_PROOF / PROVED / CONDITIONAL /
  EXPERIMENTAL.
- **What is being added:** A conservative triage of PRs #96--#98. PR #96's
  useful Cycle84 public replay record is kept as an inert audit note:
  `m_max(beta)=2`, `Occ(beta)=52,747,567,092`, `D=24`, twelve double fibers,
  and no fibers of size at least three. PR #97 adds the F1 simple-pole
  deep-point list-to-CA/MCA conversion note and sanity script. PR #98 adds the
  L1 dual-dilation Fourier orbit-kernel reduction note and verifier.
- **How it is useful:** Cycle84 now has a public replay record for the finite
  M1 wall without importing the live workflow or raw archive. The F1 note gives
  a direct special list-to-CA/MCA mechanism to audit against Paper D. The L1
  note moves prefix-local work from individual Fourier frequencies to orbit
  kernels and records a concrete route cut for pointwise kernel saving.
- **What to do next:** Do not treat Cycle84 as a prize-level theorem until a
  transfer theorem is proved. Audit #97 against the exact main-paper `eca` and
  `emca` predicates before any promotion. Run the new scripts only after
  reviewer approval; this triage pass inspected them as text but did not
  execute PR code.

### 2026-06-19 - Experimental folder streamlining

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/README.md`,
  `experimental/notes/README.md`, `experimental/scripts/README.md`,
  `experimental/data/README.md`, plus repository moves under
  `experimental/notes/`, `experimental/scripts/`, `experimental/data/`, and
  `experimental/lean/`.
- **Status:** AUDIT.
- **What is being added:** Reorganized the experimental workspace into four
  durable buckets: notes, scripts, compact data, and Lean. Removed generated
  Python caches and raw/prompt transcript dumps from dated AI-loop outputs.
- **How it is useful:** Future agents now have a small root surface and a clear
  placement policy. Audited summaries and reproducible scripts remain, while
  bulky model-run provenance that was not needed for review is gone.
- **What to do next:** Keep new work inside the existing buckets, update
  `README.md` if a genuinely new bucket is needed, and avoid adding raw
  transcript archives unless they are the only reproducibility record.

### 2026-06-19 - PR #82/#84-#95 experimental integration

- **Agent/model:** AllenGrahamHart, scottdhughes, latifkasuli,
  DannyExperiments PRs, integrated by Codex.
- **Files added or changed:** `experimental/notes/triage/pr-triage-2026-06-19.md`,
  `experimental/SUMMARY.md`, `experimental/agents-log.md`,
  `experimental/notes/l1/l1_prefix_divisor_count.md`,
  `experimental/notes/l1/l1_quotient_defect_closure.md`,
  `experimental/notes/l1/l1_repaired_locator_theorem_package.md`,
  `experimental/notes/l2/l2_interleaved_dilation_constants.md`,
  the NFB frontier JSON data folder,
  `experimental/notes/m1/m1_residue_line_roadmap.md`, M1 depth-two Kummer notes and
  verifiers, L1/L2 verifier scripts, and the selected
  `experimental/notes/f1/fable-loop/PRZ_REVIEW_INDEX.md` Cycle 49--57 audit
  layer.
- **Status:** PROVED / CONDITIONAL / CONJECTURAL / EXPERIMENTAL / AUDIT, as
  marked per file.
- **What is being added:** Manual integration of the useful recent PRs:
  PR #93 supersedes #85--#91 as the Scott L1 consolidation; PR #84 adds the
  L1 prefix/divisor/Fourier split; PR #92 adds L2 interleaved dilation and
  quotient-core constants; PR #94 adds a compact `F\B` deep-hole proof
  record; PR #82 adds the M1 low-slack Kummer/depth-two packet; PR #95 is
  integrated only as review index plus cycle audits, not as a raw 225k-line
  archive.
- **How it is useful:** Gives future work clear entry points: L1 quotient
  floors versus aperiodic Fourier cancellation, M1 two-coordinate/conductor
  targets, L2 aligned interleaved constants, an F1/Paper D explicit-line
  proof target, and a compact Fable-loop upper-side route map.
- **What to do next:** Run and review the integrated verifiers, add a
  standalone verifier for the NFB JSON record, audit the M1 Kummer imports
  before consuming constants, and continue the Fable-loop program from the
  high-`j` constant-rate prompt rather than the cut `t=2,j=2` toy regime.

### 2026-06-18 - PR #79-#81 experimental integration

- **Agent/model:** AllenGrahamHart and scottdhughes PRs, integrated by Codex.
- **Files added or changed:** `experimental/m1_depth_two_lift_window_theorem.md`,
  `experimental/m1_kummer_weil_import_contract.md`,
  `experimental/m1_support_coefficient_test.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/verify_m1_kummer_divisor_geometry.py`,
  `experimental/verify_m1_slack_two_depth_two_kummer_saturation.py`,
  `experimental/l1_arbitrary_fiber_repair.md`,
  `experimental/verify_l1_arbitrary_fiber_repair.py`,
  `experimental/a0_external_import_source_check_20260618.md`,
  `experimental/a0_import_source_probe.py`,
  `experimental/pr-triage-2026-06-18-round3.md`, and
  `experimental/agents-log.md`.
- **Status:** CONDITIONAL / AUDIT / EXPERIMENTAL / COUNTEREXAMPLE.
- **What is being added:** Manual integration of PR #79's M1 depth-two
  Kummer-window material, PR #80's L1 arbitrary-fiber repair note, and PR
  #81's A0 external-import source check.  The M1 material is explicitly
  conditional on the isolated Kummer-Weil import; the L1 material repairs a
  false raw-support arbitrary-fiber route; the A0 material records source
  reachability without closing the Paper D import audit.
- **How it is useful:** Narrows three active ledgers without editing Papers
  A--D: M1 gains a sharper lift-window/saturation audit, L1 gets a corrected
  list-object target, and A0 has a reproducible source-access record for the
  universal-cap import chain.
- **What to do next:** Prove or cite the M1 `16p` Kummer estimate, decide
  whether Paper B should promote `ImgFib_U(s)` or another repaired L1 object,
  and obtain the CS25/ABF PDFs needed to close the remaining A0 checks.

### 2026-06-18 - Four-item packet label clarification

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/experiments.tex`,
  `experimental/experiments.pdf`, `experimental/agents-log.md`.
- **Status:** AUDIT / CLARIFICATION.
- **What is being added:** Adds a self-contained explanation of what the
  AI-packet labels (a)--(d) mean: weak-slack positive regime, finite
  Fermat-prime packet, exponential-field construction, and imported BCHKS
  quotient-locator packet.
- **How it is useful:** Makes the experimental PDF readable without knowing
  the earlier discussion, and separates imported locator material from the
  independent local Paper B divisibility-gate theorem.
- **What to do next:** If the original four-item packet is archived in the
  repo, cross-link this clarification to the exact source file or PR.

### 2026-06-18 - Streamlined imported-locator ledger

- **Agent/model:** Human-provided streamlined note, logged by Codex.
- **Files added or changed:** `experimental/experiments.tex`,
  `experimental/experiments.pdf`, `experimental/agents-log.md`.
- **Status:** AUDIT / IMPORTED / WRAPPER / TARGET / NEW-LOCAL.
- **What is being added:** Replaces the narrower attribution note with a
  unified experimental ledger titled *Experimental Theorems and
  Imported-Locator Ledger for RS-MCA*.  The note explicitly imports the
  Ben-Sasson--Carmon--Habock--Kopparty--Saraf quotient-locator construction,
  gives the smooth-quotient notation dictionary, records the shared locator
  identity as imported rather than new, adds a list-fiber pigeonhole wrapper,
  states a slack-two/subfield target for the Paper D route, and preserves the
  Cycle 14--18 Paper B divisibility-gate theorem.
- **How it is useful:** Streamlines promotion decisions for Papers A--D:
  locator proofs from BCHKS must be cited at theorem and proof entry points;
  repository-side contributions are limited to dictionary/wrapper/ledger
  packaging unless separately proved; Paper D gets a precise augmented-code
  and subfield-pigeonhole target; Paper B keeps the independent restricted
  resonance gate as local experimental mathematics.
- **What to do next:** When editing the main papers, add the `BCHKS25`
  bibliography entry and cite Theorems 7.1 and 1.13 exactly where the locator
  construction is used.  Audit the augmented-code rung, slope field
  (`B` versus `F`), locator-codeword distinctness, and slack normalization
  before promoting any wrapper to a theorem.  Continue scanner work on the
  `G==0` divisibility-gate branch for the Paper B resonance window.

### 2026-06-18 - Proximity-gap attribution audit

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/experiments.tex`,
  `experimental/experiments.pdf`, `experimental/agents-log.md`.
- **Status:** AUDIT / ATTRIBUTION.
- **What is being added:** Records that the AI-generated result (d) should be
  treated as an imported adaptation of Theorem 1.13 of
  Ben-Sasson--Carmon--Habock--Kopparty--Saraf, *On proximity gaps for
  Reed--Solomon codes*, rather than as a new repository contribution.  Also
  records the limitations of items (a)--(c): `1/sqrt(n)` slack, only three
  Fermat primes, and exponential field size.
- **How it is useful:** Gives Papers B/D/C a conservative integration plan:
  cite the external theorem, separate it from the Crites--Stewart import, and
  audit the consumed object before any MCA, line-decoding, or protocol ledger
  claim.
- **What to do next:** Add the bibliographic entry and exact theorem
  cross-reference when the main papers are edited, then verify whether item
  (d) converts to the RS-MCA object actually needed by Paper B.

### 2026-06-18 - PR #78 M1 residual-depth hierarchy

- **Agent/model:** AllenGrahamHart / Codex, integrated by Codex.
- **Files added or changed:** `experimental/m1_support_coefficient_test.md`,
  `experimental/m1_support_occupancy_scan.py`,
  `experimental/m1_support_occupancy_scan.md`,
  `experimental/verify_m1_slack_two_depth_two_full_domain.py`,
  `experimental/agents-log.md`.
- **Status:** PROVED / AUDIT / EXPERIMENTAL.
- **What is being added:** Integrated Allen's PR #78 M1 residual-depth
  hierarchy: the depth-two/next-slack transition theorem, terminal pure-zero
  residual-depth ledger, first-nonzero frontier partition, full-domain
  slack-two depth-two saturation verifier, and a high-index ceiling for the
  slack-two depth-two frontier.
- **How it is useful:** Separates inherited zero strata from genuinely new
  first-nonzero coefficient images in the M1 canonical-support scanner, giving
  sharper targets for Paper B's corrected MCA residue-line program.
- **What to do next:** Use the new verifier and scanner fields to attack
  proper-subgroup coset-image bounds, especially intermediate-index cases not
  decided by full-domain saturation or the coarse high-index ceiling.

### 2026-06-18 - Experimental theorem note

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/experiments.tex`,
  `experimental/experiments.pdf`, `experimental/agents-log.md`.
- **Status:** PROVED / HEURISTIC / AUDIT.
- **What is being added:** A standalone LaTeX note collecting restricted
  Cycle 14--18 theorems and heuristics, including the Cycle 18
  divisibility-gate theorem with proof.
- **How it is useful:** Gives the experimental proof material a citable,
  compiled form without editing Papers A--D.
- **What to do next:** Extend the scanner to test the `G==0` gate and decide
  whether any source-valid growing-prime family has two-dimensional slope-map
  image.

### 2026-06-18 - Cycle 18 resonance slope-map reconstruction

- **Agent/model:** Codex.
- **Files added or changed:**
  `experimental/notes/f1/fable-loop/audits/20260618_CYCLE18_RESONANCE_SLOPE_MAP_COLLAPSE_AUDIT.md`,
  `experimental/scripts/fable_loop/local_checks/20260618_cycle18_resonance_slope_symbolic.py`,
  `experimental/notes/f1/fable-loop/README.md`,
  `experimental/agents-log.md`.
- **Status:** PROOF-SKETCH / EXACT_NEW_WALL / AUDIT.
- **What is being added:** A local reconstruction of Danny's Cycle 18
  `t=2,j=3` resonance reduction: `Delta` becomes a monic quadratic in
  `tau3`, the alpha component is at most linear, and the non-coprime branch
  reduces to either `Delta1==0` or the graph `tau3=-h/s`. The audit also
  records the divisibility-gate theorem: if the cleared graph polynomial
  `G=s^2 Delta0(tau1,tau2,-h/s)` is nonzero, the branch is already
  curve-sized and contributes only `O(p)` slopes.
- **How it is useful:** Sharpens the Paper B/F1 restricted toy-window wall
  from the Cycle 16 `Q==0` split to a concrete rational slope-map collapse
  question.
- **What to do next:** Extend the Cycle 17 scanner to compute the graph branch
  and projective map image on source-valid split cubics across growing primes,
  with `G==0` as the first exact gate for possible `Theta(p^2)` behavior.

### 2026-06-18 - Paper B counterexample comparison

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/paper_b_counterexample_comparison.md`,
  `experimental/agents-log.md`.
- **Status:** AUDIT / EXPERIMENTAL.
- **What is being added:** A theory-side comparison between recent
  experimental counterexamples and Paper B's locator-fiber, residue-line,
  extension-field, tangent-floor, and line-decoding statements.
- **How it is useful:** Identifies the raw arbitrary locator-fiber conjecture
  as needing repair, while separating route-cut counterexamples from genuine
  threats to the corrected MCA conjecture.
- **What to do next:** Review the proposed Paper B repairs, especially the
  replacement of raw `Fib_U` by a pruned/full-support arbitrary-word object.

### 2026-06-18 - Experimental summary

- **Agent/model:** Codex.
- **Files added or changed:** `experimental/SUMMARY.md`,
  `experimental/agents-log.md`.
- **Status:** AUDIT / EXPERIMENTAL.
- **What is being added:** A high-level summary of the recent PR wave and the
  current contents of `experimental/`, organized by how the material advances
  the corrected MCA program.
- **How it is useful:** Gives new agents and human reviewers a map of which
  experimental notes support L1, M1, M2, F1, L2, A0/A1, protocol ledgers, and
  formalization, while keeping proof status conservative.
- **What to do next:** Use the summary as an orientation map, then verify
  individual claims from their source notes and scripts before promotion.

### 2026-06-18 - New PR triage integration

- **Agent/model:** Codex.
- **Files added or changed:** Integrated experimental material from PRs #67,
  #69, #70, #71, #72, #73, #74, #75, and #77; recorded #68 and #76 as
  superseded by #77; added `experimental/pr-triage-2026-06-18.md`.
- **Status:** AUDIT / EXPERIMENTAL.
- **What is being added:** Second open-PR triage pass covering M1, F1, L2,
  M2, L1, A1, Fable-loop, and locator-fiber cross-check contributions.
- **How it is useful:** Banks useful experimental notes, verifiers, scanners,
  and audit provenance while preserving the rule that main papers remain
  unchanged and new material stays in `experimental/`.
- **What to do next:** Run full verifier coverage, review mathematical claims
  before promotion, and close the source PRs as manually integrated or
  superseded once this commit is pushed.

### 2026-06-17 - Open PR triage integration

- **Agent/model:** Codex.
- **Files added or changed:** Integrated experimental material from PRs #1,
  #2, #3, and #46 through #66; added
  `experimental/pr-triage-2026-06-17.md`; renamed PR #55's dither scanner to
  `experimental/quotient_profile_dither.py` with matching `.md` note.
- **Status:** AUDIT / EXPERIMENTAL.
- **What is being added:** One-by-one triage of the open PR queue and local
  integration of accepted experimental notes, scanners, proof records, and
  audit bundles.
- **How it is useful:** Preserves useful agent contributions while enforcing
  the repository rule that new material starts in `experimental/` and Papers
  A-D remain unchanged.
- **What to do next:** Run verifiers and audits on the integrated material,
  review mathematical notes before promotion, and close the original PRs as
  manually integrated once the integration commit is pushed.
