# The four enumeration routes — how the complete obstruction class gets produced

- **Status:** AUDIT / route map. Companion to the prize DAG's enumeration
  pipeline nodes and `redteam_attack_plan.md`.
- **The point:** a finished proof does not rule out adversarial mechanisms
  one by one — the right templates produce an obstruction class that is
  COMPLETE BY CONSTRUCTION, then classify it. `payment_completeness` is
  therefore rewired as the classification OUTPUT of whichever route wins
  (any-gate over the four classification nodes), not a standing assumption.
- **Conservation of hardness (the honest headline):** none of the four
  templates removes the difficulty; each LOCATES it and guarantees list
  completeness. The core resurfaces once per route, in that route's
  dialect — knowing exactly where is most of this note's value.

## Route XR — the inverse-theorem paradigm (Gowers / Green-Tao shape)

```text
stage 1 [xr_gvn, RIPE]      Generalized von Neumann: define iterated
        exchange energies E_k (k-fold Johnson-scheme correlations;
        averaged_xr IS the k = 2 case) and prove FM-excess is controlled
        by some E_k. Mechanics: Cauchy-Schwarz chains over exchange
        moves — template-standard; ingredients proved (exchange calculus,
        the exact Johnson gap).
stage 2 [xr_inverse]        THE INVERSE THEOREM: E_k large => correlation
        with an explicit class C_XR, complete by construction. Expected
        content at low k: folded/equivariant words (quotient) and
        common-codeword structure (tangent). Start at k = 3: odd moments
        — the Hooley-Katz input is exactly the k = 3 shadow, and the
        even-moment foreclosure (prob:perfiber) says k = 2 CANNOT
        suffice, which the template converts from an obstacle into a
        prediction: the inverse content begins at odd order.
stage 3 [xr_crystallization] classify C_XR members as paid or new.
WHERE THE CORE HIDES: stage 2 at higher k (the Gowers-inverse analogue;
historically a decade of work — but a NAMED, finite problem).
```

## Route SPI — algebraic component decomposition (Noetherian finiteness)

```text
stage 1 [spi_component_control]  Effective Bezout: the alignment variety
        and its structure-loci intersections have boundedly many
        components of bounded degree, explicit in (n, t, j). The
        component LIST is the finite enumeration.
stage 2 [spi_point_counting]     Low-dimensional components meet D_j in
        poly many points. HONEST: this is where the core resurfaces —
        D_j is a special finite set, so Lang-Weil-style counting does
        not apply verbatim; the divisor structure must enter (this is
        Conjecture F at component level).
stage 3 [spi_exceptional_class]  High-dimensional components map into
        paid strata (or name the new ledger).
WHERE THE CORE HIDES: stage 2. The deficiency ladder (PR #172) is this
route's base-case laboratory.
```

## Route ES — the algebraic regularity lemma as an off-the-shelf enumerator

```text
[es_regularity] Formulate alignment as a definable relation of bounded
description complexity; apply an F_q algebraic-regularity / ES-type
theorem: structure-vs-pseudorandomness with power savings and ALGEBRAIC
exceptional sets, classifiable by stage-3 machinery shared with SPI.
WHERE THE CORE HIDES: "bounded description complexity" — our degrees
grow with t. The dimension-free obstacle in regularity clothing. A
feasibility memo (can the relation be re-encoded at bounded complexity,
e.g. via the V^T D V factorization's fixed shape?) is the cheap first
step and is queued.
```

## Route monodromy — group classification (the repo's own worked example)

```text
stage 0 [monodromy_realization, THE unmapped step]  Express the general
        aperiodic alignment count as the trace function of an explicit
        sheaf family. BETA_2 did this for ONE slack-line instance and
        then executed stages 1-3 completely (local data PROVEN-EXACT;
        classification via Kantor/ADW enumerates ALL possible monodromy
        groups and kills them wholesale — the cleanest existing example
        of 'enumerate all obstructions systematically').
stages 1-3: pin local data; the big-monodromy input; classification.
WHERE THE CORE HIDES: stage 0 for the general problem, plus the known
(I)/(II) residues for any specific realization.
```

## Cross-route facts worth exploiting

```text
- stage-3 machinery is SHARED: classification of structured escapes is
  one body of work consumed by all four routes (xr_crystallization and
  spi_exceptional_class are cross-linked for this reason).
- the even-moment foreclosure is a PREDICTION under route XR: inverse
  content must begin at odd k — aligning exactly with the Hooley-Katz
  attack vector already in the repo's roadmap.
- the red-team program (R1-R7) is the empirical PREVIEW of every
  route's stage 2/3: whatever C contains, the constructions find first.
- a new class member discovered at any stage 2 is the S9 protocol firing
  INSIDE the strategy: the route itself names the fifth mechanism, its
  ledger is added at the single edit point (payment_completeness), and
  the program continues. Discovery-and-revision is built in.
```

## Queue additions

```text
QE.1 [xr_gvn] (M, RIPE)  Build the iterated exchange-energy functional
     and the Cauchy-Schwarz chain (k = 2 exists as averaged_xr; extend
     to k = 3). Acceptance: toy-verified inequality FM-excess <= f(E_3).
QE.2 [spi_component_control] (M)  Effective component/degree bounds for
     the alignment variety; acceptance: explicit formulas + toy check
     against direct decomposition at n = 16.
QE.3 [es_regularity feasibility memo] (S)  Can alignment be encoded at
     bounded description complexity (V^T D V shape)? A yes/no memo with
     the encoding or the obstruction, before anyone invests further.
QE.4 [monodromy_realization scoping] (M)  What sheaf family would carry
     the general alignment count? A scoping note mapping the gap between
     BETA_2's instance and the general problem (expert-consultable).
```
