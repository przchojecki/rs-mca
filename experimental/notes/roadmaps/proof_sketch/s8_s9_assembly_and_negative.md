# S8 + S9: the assembly contract, unconditional coverage, and the negative branches

- **Status:** consolidation; verified arithmetic; the "bets" in §4 are
  explicitly LOW-CONFIDENCE SKETCH. Nothing here claims new mathematics.
- **Parent:** `prize_proof_sketch_spine.md` S8, S9. Final content node
  before the coherence pass.

## 1. The compiler contract [engineering spec, consumes turns 1-11]

```text
INPUT:  row (p, e, n, k)  ->  q_line = p^e, q_gen = p^ord(p mod n), rho;
        sampler + endpoint conventions (S0 table); packet refs.
COLUMNS:
  gates      B*_aff = floor(q_line/2^128), B*_proj = floor((q_line+1)/2^128)
             (differ iff 2^128 | q_line + 1 — always print both);
  generating q_gen = q_line ?  else TWO-COLUMN mode (S6 imported window);
  Paid(A)    tangent staircase + quotient zones a/b/c + B_ext (S2/S6);
             zone-(b) cells are INTERVALS, never points;
  verdicts   per grid agreement A:
             SAFE(proved)        -- tangent-pinned region (envelope) only,
                                    today;
             UNSAFE(proved)      -- mechanism named: tangent, cap witness,
                                    quotient zone-(a), qcore-import;
             SAFE(conditional)   -- corridor below crossing, conditions
                                    printed: H6 = {R2 via SPI or XR,
                                    Conjecture F, zone-(b) resolution};
             UNKNOWN             -- corridor, no applicable certificate.
REFUSAL:  any prize-facing output while an S0 axis is OPEN, or any
          unconditional verdict resting on a conjectural ledger, is
          refused outside labeled conditional mode (r2 WP-7.1, enforced
          by the WP-0.4 checker, dedup as checker logic).
LIST SIDE: same contract with the S7 window, interleaved budgets
          (B <= 1.60 worst / 3.20 a-regular), q_chal denominator printed.
```

The compiler IS the uniform theorem in executable form: M6 = "every
SAFE(conditional) verdict upgrades to SAFE(proved) when H6 is proved."

## 2. Unconditional coverage today [verified]

```text
field-size split at n = 2^41 (rate 1/2):
  log2 q_line in [128, 166.4]:  FULLY PINNED (tangent staircase envelope,
      1 <= B_Q <= (n-k)/3 — the proved #147 compiler + my step-5 map);
  log2 q_line in (166.4, 256):  the open band —
      unsafe above the cap             PROVED;
      unsafe in the S7 list window     proved-shape (conventions pending);
      the corridor                     UNKNOWN pending H6;
  the pinned F_17^32 row (log2 q = 130.8) sits in the pinned zone — the
  worked example of the first line.
```

So "how much of the prize is already resolved" has a one-line answer:
everything up to `q_line ~ 2^128 * (n-k)/3`; the remaining content is a
~90-bit band of field sizes, exactly where the corridor machinery lives.

## 3. Minimal win conditions [consolidation]

```text
FULL Grand MCA (per rate, generating rows):
  (1) R2 — rigidity, via either mechanism (SPI or XR), with exponent B <= 3;
  (2) zone-(b) resolution — the e_1 value-set collision behavior
      (= prob:perfiber at sigma = 1);
  (3) S0 zero-OPEN (axes 1, 2, 4 audits; 8, 9 rules lookups).
FULL Grand List adds:
  (4) L1 ImgFib at the reserve (the petal battle = Conjecture F);
  (5) a-regularity collapse or exponent B <= 1.60.
PARTIAL ladder (each rung independently submittable):
  pinned-row package (done, pending S0) -> envelope map (done on main) ->
  window theorem at aperiodic-0 (predicted, fronts running) ->
  second-row transfer (P3) -> wall dossiers (BETA_2 frozen; Graver frozen).
```

Note (1)+(2) are BOTH instances of the one collision family (Conjecture F
and its coordinate-plane case) — the minimal win set is, at bottom, ONE
statement family plus care.

## 4. S9: the negative branches, consolidated [one line each]

```text
P1c unpaid window collision      -> new ledger in the EASIEST regime;
                                    corridor moves down; high info.
GAP-1 non-equivariant periodic   -> new column; unsafe side earlier.
Conj F fails (kernel planes)     -> alignment strictly harder than
                                    prob:perfiber; ladder measures extras.
XR/SPI fail worst-case,          -> "the prize waits on monodromy":
  averaged versions hold            BETA_2 handoff is the program.
zone (b) collision-free          -> delta* at the quotient crossing
                                    (left end); unsafe side cheap.
zone (b) heavily collided        -> delta* at tau*; unsafe side needs
                                    averaged fiber-to-slope conversion.
dither latitude (rules)          -> dyadic cores die; corridor narrows
                                    toward [tau*, cap]; mostly HELPS.
non-generating rows admissible   -> imported S7 window binds there;
                                    two-column tables.
S0 axis resolves against repo    -> constants reprint mechanically; no
                                    structural change.
```

**The one genuinely bad scenario** (irreducible non-determination): zone
(b) unresolved AND R2 unproven — then `delta*` is only bracketed, with
verified corridor widths per rate of

```text
2.17 / 2.00 / 1.12 / 1.67   grid steps of the cap reserve (2^-9, 2^-10),
```

and a determination prize is not won by a bracket. This is why the minimal
win set of §3 is what it is; every other branch still ends in a
determination (possibly of a lower threshold, with a larger ledger).

**Low-confidence bet [SKETCH, explicitly speculative]:** the only direct
evidence on zone (b) — exactness of `Acl` above the norm threshold at
small scales — points toward collision-free behavior extrapolating, i.e.
`delta*` at the QUOTIENT end of the corridor (`c_rho ~ 2 beta(rho)` in
`1/log2 q` units at `log2 q = 256`). Confidence is low; the Hooley-Katz
odd-moment lane is the cheapest way to move it.

## 5. Handoff to the FINAL pass

```text
fix list: s2_paid_ledger.md "corridor ~1.5 grid steps" -> per-rate widths
          (2.17/2.00/1.12/1.67) as verified above;
audit:    every cross-reference between the 8 nodes + spine; every label
          (PROVED-cited claims actually cite; CONJECTUREs stated as
          statements; GAPs have consumer notes); predictions P1a/b/c, P2
          (as corrected), P3, P4, P-beta collected into one ledger table
          in the spine; then terminus per the loop memory.
```
