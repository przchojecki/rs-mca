# S3a: the regular window — the crystallization testbed, and 4515 vs 6

- **Status:** SKETCH on verified arithmetic; predictions are falsifiable by
  the already-scheduled scans (WP-2.1/2.2). NOT rigorous.
- **Parent:** `prize_proof_sketch_spine.md` S3a. Numerics machine-checked.

## 1. What the window is for [orientation]

Per §1.2 of the roadmap, the regular window (`385 <= A <= 426`, pinned row)
can never decide a prize-band transition; and per S2, the pinned row's
threshold is tangent-pinned anyway. The window's actual role in the sketch:
it is the cheapest place where the full safe-side chain — eliminant, paid
subtraction, crystallization — gets an END-TO-END audit against ground
truth. Every window outcome is evidence about the in-band mechanisms.

## 2. The 4515-vs-6 reconciliation [verified arithmetic]

The `4515` is the DEGREE CAPACITY of the window (sum of eliminant degree
bounds `j+1`), not a count of anything. FM (Lemma FM1, exact) gives the
expected number of aligned locators per generic pair:

```text
A=385: log2 E = 409.2 - 128*130.8 = -16333
A=406: log2 E = 372.2 - 149*130.8 = -19117
A=426: log2 E = 329.9 - 169*130.8 = -21775
window sum ~ 2^-16328;  by Markov, the fraction of ALL pairs carrying ANY
window alignment is <= ~2^-16000 (conservatively rounded).
```

So the chain reads:

```text
4515 (a-priori eliminant capacity)
  -> canonical gcd/lcm ledger (v10, removes selected-minor slack)
  -> paid subtraction (M4: tangent + quotient roots)
  -> predicted UNPAID residue: 0     [crystallization prediction, P1]
  vs budget B* = 6.
```

Every genuine alignment in the window must come from a
measure-`<= 2^-16000` structured family; the crystallization premise says
structured = paid. The window theorem the roadmap asks for
(`f17_32_window_theorem.md`) should therefore end, like the A=506/507 smoke
packet, with **aperiodic numerator 0 across the window** — that is the
sketch's concrete, checkable prediction for the whole M3/M4/M5 campaign.

## 3. Front alpha in this language [SKETCH]

An alpha failure (`gcd(Phi_{m,r,0}, Phi_{m,r,1}) != 1`) is an alignment
surviving the shift move — the window-direction exchange (turn 3). Generic
heuristic: two degree-`~m` polynomials over `F_17^32` share a root with
probability `~ m^2/q = 2^-116.8` (verified) — so unstructured collisions
essentially do not exist, and any collision the scan finds is structured.
The mechanisms then predict it is PAID (tangent/quotient-compatible).
Refinement of prediction P1:

```text
P1a: the full-grid alpha scan returns gcd = 1 everywhere, OR
P1b: every collision found factors through a paid family (checkable by
     running the collision's root against the tangent/quotient ledgers).
An unpaid collision — P1c — would be a candidate_new_obstruction found in
the EASIEST (overdetermined) regime, falsifying crystallization where it
should be strongest; the in-band program would inherit a new ledger column
before it even starts (S9 posture, but with high evidential weight).
```

## 4. Front beta in this language [SKETCH, verified codimension]

The rank-6 ambient sharpness example (PR #171: six finite roots + one
projective endpoint coexisting) lives in the AMBIENT pencil class of
dimension `2 t (j+1) = 29580` (at A=426), while realizable Hankel pencils
form a `2(t+j) = 512`-dimensional subfamily — codimension `~29068`
(verified). Generic ambient phenomena are overwhelmingly non-realizable;
realizability must be FORCED by structure, and forced structure is (by
crystallization) paid structure. Prediction:

```text
P-beta: the ambient sharpness example is either not Hankel-realizable, or
realizable only within a paid family whose contribution the M4 subtraction
already prices. The realizability search (WP-2.2 step 1) decides this.
```

## 5. What the window CAN teach the in-band program [assessment]

```text
- the paid-subtraction bookkeeping (M4 dedup) gets exercised on cases with
  known answers — the checker hardening earns trust transferable in-band;
- the crystallization premise gets its cheapest falsification shots
  (P1a/b/c, P-beta) — surviving them is real evidence, though never proof,
  for the in-band form (the regimes differ: kernel trivial vs kernel huge);
- the exchange calculus (#152-style ledgers, shift-transfer identities) is
  developed on ground where every claim is machine-checkable end-to-end.
What it cannot teach: anything about fiber growth (kernels are trivial in
the window) — Conjecture F's plane-section content is invisible here; the
deficiency ladder (WP-2.6 / PR #172) is the only current probe of that.
```

## 6. Forks

```text
F1 = P1c (unpaid alpha collision): new ledger column; crystallization
     demoted from premise to per-stratum hypothesis; in-band prediction
     widens the S2 bracket downward. High information either way.
F2 = P-beta fails (unpaid realizable sharpness): direction-rank methods
     insufficient even in the window; M5 pivot charts become mandatory
     for the window theorem, not optional refinements.
F3: the window theorem lands aperiodic-0 on declared families but resists
     all-pairs closure: the crystallization gap localizes to the window's
     arbitrary-word question — a clean, small instance of T4 to hand to
     the bottom-up lane before the in-band version is attempted.
```
