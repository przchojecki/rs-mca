# WP-3.1 + WP-3.3 detail (L3): the row slate, and the second pin or the named wall

- **Status:** selection plan with machine-checked slate numbers; the
  pin-vs-wall dichotomy is stated exactly. No result claimed.
- **Executability:** AGENT (row construction, descriptor runs, the Row-C
  experiment); the pin itself inherits the minimal win set (H6).
- **Parents:** r2 WP-3.1/3.3; consumes wp3_2 (descriptor), s2/s5_s0
  (corridors), s6 (why no non-generating candidate exists at scale).

## 1. WP-3.1: the row slate (rate 1/2 flagship; other rates by descriptor)

```text
Row A  "Prime192":  n = 2^20, p = smallest prime = 1 mod 2^20 above
       2^191 (Dirichlet-abundant; certified primality standard).
       Verified: envelope pins only to log2 q = 145.4 -> Row A is IN
       the open band; B* = 2^64; corridor reserves quot 0.01238 /
       tau* 0.00521 / cap 0.00195 (the corridor is WIDER at 192 bits —
       reserve ~ beta/(log2 q - 128) grows as the field shrinks toward
       2^128). Zone-(a) is SILENT here (max proved quotient mass 2^49.1
       < B* = 2^64): Row A's unsafe side currently rests on the cap
       alone — the cleanest possible test of the corridor machinery.
Row B  "top-of-range": n = 2^41 (k = 2^40 max), log2 q ~ 255 prime.
       The extreme admissible row; master-table corridor; everything
       symbolic via the descriptor (no enumeration at this n).
Row C  "small-n probe": n = 2^10, log2 q ~ 250. IN band with B* = 2^122;
       its role is EXPERIMENTAL: the only slate row where zone-(b) can
       be MEASURED — e_1 value-set densities at N' = 64..256 by
       birthday-collision sampling (~sqrt(V) samples; V ~ 2^60 needs
       ~2^30 evaluations, feasible offline; enumeration is impossible,
       C(256,129) ~ 2^252).
Row D  "generating extension" (optional): p^e with ord(p mod n) = e at
       log2 q ~ 250 — exercises the S6-degenerate path. NOTE: no
       non-generating candidate exists at prize scale BY THEOREM-shape
       (s6: admissibility forces q_gen < 2^128 for non-generating rows)
       — the slate documents this instead of hunting for one.
```

**Selection criteria (each row tests a named plan question):** Row A =
transfer test for P2/P2.5 machinery (its `t/(j+1)` profile printed per
r2) + the corridor with a silent zone-(a); Row B = symbolic-scaling
regression at full size; Row C = the zone-(b) measurement instrument;
Row D = the S6 path. **Acceptance test:** descriptor outputs for all
four rows committed as a table; Row A's prime found and certified; the
Row-C sampling harness spec'd with pinned seeds and a collision-count
-> value-set-density estimator with stated confidence intervals.

## 2. WP-3.3: the second pin, or the wall named on a concrete row

**The dichotomy, exactly.** A second (prize-scale) pin at Row A needs
its corridor decided — which is the minimal win set {R2, zone-(b)}
restricted to one row. So WP-3.3 has exactly two end states:

```text
PIN:   the compiler (wp7_1 contract) emits adjacent SAFE/UNSAFE verdicts
       for Row A with H6 discharged for that row — the first prize-scale
       pin, and the transfer proof for the whole program; or
WALL:  the "Row-A corridor question" wall note per standing order 8:
       frozen statement (the corridor bracket with Row A's numbers),
       consumer theorem (Row-A pin <= R2|_{RowA} + zone-(b)|_{RowA}),
       toy reproduction chain (F_97 acid row -> pinned 17^32 row ->
       Row A), and the measured Row-C zone-(b) data as evidence either
       way.
```

**Partial rungs that do not wait for H6 (family-conditional):**

```text
- deficiency-1 charts at Row A's regular boundary (the wp2_6 machinery
  transplanted; declared families only — honest per the M3 precedent);
- Row-C measurements: an empirical zone-(b) collision curve N' vs
  estimated value-set density — the FIRST data anywhere on the
  collision question, movable evidence for the s8_s9 bet;
- norm-threshold extensions (wp3_2 item B): every improvement moves
  Row A's zone-(a) boundary toward audibility (currently silent at
  N' <= 62 vs needed ~N' > 81 for B* = 2^64).
```

**Acceptance test:** one of the two §2 deliverables exists and passes
the WP-0.4 checker (pin packet) or the standing-order-8 completeness
check (wall note: statement + consumer + toy + scan data). **Failure
branches:** Row A's prime search stalls (take the next 2-power level
n = 2^19 — nothing depends on the specific n); Row-C sampling shows
value sets FULL (collision-free) -> the s8_s9 bet strengthens toward
the quotient end and the unsafe side of the corridor becomes
constructively provable at Row C's parameters first; sampling shows
heavy collisions -> the FM/tau* end binds and averaged-conversion work
(s2 fork F2) is promoted.

## 3. What this buys

The slate turns "transfer to prize scale" from an aspiration into four
named rows with verified numbers, one designed experiment (Row C — the
only place zone-(b) is measurable today), and a milestone whose two
possible outcomes are both defined deliverables rather than success/
failure — the wall, if named, arrives with its consumer theorem and the
first empirical collision data attached.
