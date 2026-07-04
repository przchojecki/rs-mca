# (A) closure assembly: the conditional theorem

- **DAG nodes:** `a_universal_trade_variety`, `a2_laurent_finiteness`,
  `a3_good_reduction_lemma` (consumed), feeding
  `h4_sparse_norm_gate` / `active_core_count_bound`.
- **Status:** CONDITIONAL theorem; the proof from the banked parts is
  complete; the two conditions are the named computational inputs
  (C1), (C2) below.  Zero new [CITATION NEEDED] items sit on the
  critical path (see "role of A2" below).
- **Verifier (arithmetic):**
  `experimental/scripts/verify_a3_good_reduction.py` (section S6;
  full replay currently 14 PASS, 0 FAIL).
- **Companion:**
  `experimental/notes/roadmaps/a3_good_reduction_lemma.md` (the new
  lemma; notation used freely here).

## 1. Banked inputs

1. **x81 + x83** (PROVED, verifier-green): minimal h-trades in mu_n
   <-> split 2h-supports with square shift; obstruction gate;
   denominator control 2^{4h-2}.
2. **X24** (PROVED): char-0 trades in mu_n(C) exist only at 2-power h
   and are full mu_h fibers (hence coset-union supports).
3. **A3(n,h)** (sibling note; PROVED given per-(n,h) certificate
   data): for p coprime to D(n,h), reduction is a bijection between
   char-0 and row anchored candidates, matching primitives with
   primitives.
4. **U2-A window arithmetic** (banked,
   `experimental/data/certificates/u2a-window-split/`): the three
   Row-C-class rows (n = 2^10; t = 5, 5, 3 at rates 1/4, 1/8, 1/16)
   are the only official rows with nonempty small-h windows; the
   prize base rows (n = 2^41, t >= 2^32 + 1) have empty windows under
   both window conventions (re-verified in S6:
   t + 1 = 4294967298 > 1681 = (log2 n)^2 > 82 = 2 log2 n).
5. **QA.22 + W4 budget** (banked certificates): the compiler
   obligation is the post-strip primitive residue in row-wise
   split-pair currency; one direct column of size n^3 per row is
   available (W4), inside a ledger that already carries a 16 n^3
   polynomial column (QA.22); Row-C rows have ~4.952e27 spare n^3
   columns of headroom (S6).
6. **Star-PTE lemma + strip taxonomy** (banked): every same-top
   residue decomposes into canonical minimal PTE trades, and
   "post-strip primitive" excludes all charged pullback classes — in
   particular the multiplicative pullbacks C(X) = C~(X^d), i.e. the
   coset-union supports.  Quotient/transported cells are paid by
   QA.22's quotient binomial column, not by this lane.
7. **Orbit/anchor accounting** (proved in the A3 note, section 1.3;
   numerically re-verified in S5): for any scaling-invariant set of
   supports, # supports = (n/2h) x # anchored supports, exactly.

## 2. Window convention

Write the row window as

```text
W(row) = [t+1, H_max(n)].
```

The task spec fixes H_max = 2 log2 n = 20 for Row-C rows (banked
upstream).  HONEST FLAG: I did not locate an in-repo derivation of
the specific 2 log2 n cap; the frozen W3 v1 grammar window of U2-A is
t < b <= (log2 n)^2 = 100.  All arithmetic below is therefore
verified at BOTH caps (20 and 100); the theorem and its budget are
insensitive to which banked window is consumed.

## 3. The named computational inputs

- **(C1) [the pilot's char-0 data].**  For each h in W(row): the
  (1024, h) certificate data of A3 section 3.2 exists and passes its
  identity checks, yielding the exceptional integer D(1024, h) and
  the char-0 anchored candidate table.  Expected content (forced by
  X24): every char-0 candidate is a coset-union, i.e. the primitive
  char-0 count T^a_prim(1024, h) = 0; the pilot's table is thus a
  re-verification of X24, and its load-bearing output is D(1024, h).
  Computed ONCE per h; reusable across every Row-C row and every
  future q at n = 1024.
- **(C2) [per-row GCD tests].**  For the row prime p (odd
  automatically, since 1024 | q - 1): gcd(p, D(1024, h)) = 1 for all
  h in W(row).  Trivial arithmetic per row.

## 4. The conditional theorem

**Theorem (closure of (A) at the official rows).**  Let row =
(F_q, mu_n) be an official Row-C-class row (n = 2^10, q = p or p^2,
n | q - 1, rate in {1/4, 1/8, 1/16}, so t = 5, 5, 3).  Assume (C1)
and (C2).  Then for every h in W(row):

```text
# primitive (post-strip) minimal h-trades at the row  =  0.
```

Consequently the small-h-window contribution to the terminal
post-strip primitive residue is

```text
R_window(row) = 0 <= n^3,
```

and (A) closes at that row through the banked W4 direct column.  At
the prize rows W(row) is empty (input 4), so (A) closes at all six
official rows.

*Proof.*  Fix h in W(row).  By inputs 1 and 6, the primitive minimal
h-trades at the row are exactly the primitive split 2h-supports in
mu_n(F_q) with square shift, i.e. the primitive row candidates with
lambda a nonzero square; their count is (n/2h) x (anchored count)
by input 7, and anchored candidates are automatically anchored
trades (lambda = S(1)^2).  By (C1) + (C2), Theorem A3 applies at
(1024, h) and the row prime: reduction is a bijection from char-0
anchored candidates onto row anchored candidates preserving
primitivity (part (b)).  By X24 (input 2, via part (c)), there are
no primitive char-0 candidates.  Hence zero primitive anchored row
trades, hence zero primitive row trades.  Summing over h in W(row)
gives R_window(row) = 0, which the W4 column consumes (its
tail-currency condition is met trivially by an exact zero for this
lane; the lane makes no claim about content outside the window,
which is routed by the banked window/grammar arithmetic).  QED

**Fallback form (X24-independent).**  If one declines to consume X24
here, Theorem A3(b) still gives the exact count

```text
# primitive unordered h-trades = (n/2h) . T^a_prim(1024, h),
```

with T^a_prim reported by the pilot.  If the pilot reports Galois
orbits, # points <= # orbits x [Q(zeta_1024) : Q] = # orbits x 512
(the "Galois factor"; the scaling factor n/2h is the "orbit n").
The budget then closes iff

```text
sum_{h in W(row)} (n/h) . A^a_h <= n^3        (ordered split-pair currency,
A^a_h = anchored count at h),
```

i.e. iff a uniform anchored count per h stays below the tolerance
table of section 5 — five orders of magnitude above anything
observed.

## 5. Failure-mode analysis: p | D(1024, h)

Semantics first: by the exactness remark in the A3 note (section 4),
the support of D_pt is precisely the set of primes with extra row
candidates; the computable D(1024, h) has support containing
D_pt's, so a GCD failure against D is a WARNING, not yet a trade
(the conservative factors delta_i, e_j, Delta_m can contain
spurious primes).  The response ladder:

1. **Recount at the bad pair.**  For the single flagged (h, p),
   enumerate the row's anchored mod-p candidates directly (the
   mod-p RUR of A3, or the finite (S, lambda)-system over F_q; one
   finite computation per flagged pair).  If the count is 0, the
   flag was spurious (p divided a conservative factor) and the
   theorem's conclusion stands unchanged.
2. **Charge genuine extras against the n^3 column.**  If extras are
   real trades, they are counted by the enumeration (this is the
   scheme-multiplicity ledger: at bad p the fiber degree can exceed
   the generic count, and only enumeration certifies it — Gap G3 of
   the A3 note).  The banked budget absorbs them as follows
   (verified, S6): a uniform anchored-extras count E at every h in
   the window fits in ONE W4 n^3 column iff
   sum_{h in W} (n/h) E <= n^3, giving

```text
   t = 5:  E <= 797,756  (H_max = 20);   E <= 361,074  (H_max = 100)
   t = 3:  E <= 594,293  (H_max = 20);   E <= 312,630  (H_max = 100)
```

   and a single bad h alone (all other window h clean, as the exact
   zero of section 4 gives) tolerates up to h n^2 anchored extras
   (= 6,291,456 already at h = 6).  For calibration: the WORST observed
   exceptional row in the verifier's end-to-end (16,3) census
   (p = 17, the most trade-rich prime for that pair) carries 352
   unordered = 132 anchored trades in total — four to five orders
   of magnitude inside the tolerance.  Beyond the single column,
   Row-C rows hold ~4.952e27 spare n^3 columns (W4 room, S6), so
   even a re-certification consuming several columns is arithmetic,
   not mathematics.
3. **Falsifier semantics (as in the DAG node):** an official-row
   prime genuinely dividing D_pt(1024, h) at a window h IS a real
   trade at that row; it is charged, never excluded.

## 6. What is and is not closed

- **Closed (conditional on (C1)+(C2)):** the small-h window lane of
  (A) at all official rows — exact zero primitive residue, not
  merely <= n^3.
- **Role of A2 / Laurent:** packaging only, at the official rows.
  With n fixed per row class, finiteness of the char-0 candidate set
  is trivial (subsets of mu_n), and X24 supplies the classification;
  Laurent's theorem [CITATION NEEDED — see A3 note, Gap G2] is
  needed only for the n-uniform statement ("C(h) independent of n"),
  which no official row consumes.  This removes the citation from
  the critical path.
- **Not closed here:** content at h > H_max (routed by the banked
  grammar/window arithmetic to other lanes); the h-only uniform
  exceptional set (A3 note, section 6: naive form false, corrected
  form open as Gap G4 — not needed); the existence of the concrete
  (1024, h) certificates, which is exactly condition (C1) (the
  pilot's deliverable, running in parallel).
- **Dependency shape:** (A) = [banked chain] + A3 (proved) +
  (C1: one-time computation per h) + (C2: per-row GCD).  Both
  conditions are finite, explicit, and reusable — the "fallback that
  always works" exit of the DAG node, now with the lemma actually
  proved rather than targeted.

## 7. Verification

Run:

```bash
python3 experimental/scripts/verify_a3_good_reduction.py
```

Current replay: **14 PASS, 0 FAIL**, including (S4) the end-to-end
A3 biconditional at (16,3) over all rows q = p <= 700 and the
extension rows q = p^2 in {49, 529} (exceptional set found:
{7, 17, 97}, matching brute-force trades exactly), (S5) the orbit
accounting identity on every trade-bearing row, and (S6) all budget
arithmetic quoted above against the banked QA.22/W4 certificates.
