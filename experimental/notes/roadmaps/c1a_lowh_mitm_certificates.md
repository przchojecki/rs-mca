# C1a: direct per-row minimal-h-trade certificates at the window bottom

- **DAG node:** `c1a_lowh_direct_certificates` (parent `c1_scalable_certificate`).
- **Context:** `a_closure_assembly.md`, `a3_good_reduction_lemma.md`,
  `a_pilot_wh_torsion_data.md`; harness sibling `c2_gcd_harness.md`.
- **Status:** machinery PROVED-against-ground-truth (12 validation gates
  green, including a decisive non-toral **detection** gate); exact complete
  h=4 census over finite fields at n = 16,32,64,128,256 (all clean);
  n = 1024 machinery + toral family certified + timing slice + honest
  extrapolation; h=5 feasibility measured (INFEASIBLE here).
- **Verifier / driver:** `experimental/scripts/verify_c1a_lowh_mitm.py`
  (single Python process, memory-bounded; pure stdlib).
- **Certificates:** `experimental/data/certificates/c1a-lowh-mitm/RowC_rate_*_h4.json`.

## Critical-path role

This packet supplies the direct low-`h` falsifier/certifier side of blocker
C1a in the clean-rate conditional proof path. It does **not** claim an
official-prime `n=1024` exhaustive run: the certificates are explicitly over a
labeled stand-in prime because the literal Row-C primes are not in-repo. What
it does provide is the validation-gated MITM machinery, exact finite-field
emptiness through `n=256`, a certified `n=1024` toral/slice report, and the
honest memory/time boundary for completing the row-field direct census.

## 0. Goal and the row specs (STEP 0)

**Goal.** For the official Row-C-class rows certify by DIRECT enumeration that
NO non-toral minimal h-trade exists at **h = 4** over the row field: no pair of
disjoint 4-subsets P, Q of the row domain with
`e_1(P)=e_1(Q), e_2(P)=e_2(Q), e_3(P)=e_3(Q)` and `e_4(P)!=e_4(Q)`, beyond the
paid **toral** fiber class (P, Q each a full `mu_4`-coset). Plus an honest h=5
feasibility measurement.

**The three Row-C rows** (banked, `u2a-window-split/u2a_window_split.json`),
all with domain `mu_1024` (n = 2^10):

```text
row_id            n     k    A    rate   t   h=4 vs window [t+1, H_max]
RowC_rate_1_4    1024  256  261  1/4    5   BELOW window bottom (t+1=6)
RowC_rate_1_8    1024  128  133  1/8    5   BELOW window bottom (t+1=6)
RowC_rate_1_16   1024   64   67  1/16   3   WINDOW BOTTOM       (t+1=4)
```

h=4 is the literal window bottom for the rate-1/16 row and sits just below the
window for the two t=5 rows; the h=4 trade structure lives on `mu_1024` and is
**identical for all three rows** (they share the domain), so one census serves
all three. Coset domains (per rate) reduce to `mu_1024` by the scaling symmetry
`e_j(gamma R) = gamma^j e_j(R)`.

**LOUD FLAG — the literal official primes are NOT in-repo.** The repository
pins Row-C only as `log2 q = 250, 1024 | q-1`, and uses the *idealized*
`q = 2^250` as a stand-in (see `xr_budget_audit.md:27` "prime unpinned — qa3
flag C1(b)", `qx14_xr_coverage_table.md:40` "q := 2^250 used as an
idealisation"). There is **no** `experimental/data/certificates/xr-budget-audit/`
directory (only the note `xr_budget_audit.md`). No literal ~250-bit prime with
`1024 | q-1` exists anywhere in-repo. The pipeline therefore runs on a
**clearly-labeled STAND-IN prime**

```text
p* = 1809251394333065553493296640760748560207343510400633813116524750123642699777
   = first prime >= 2^250 with p* == 1 (mod 1024)   (251-bit; log2 p* ~ 250.0)
```

so that `mu_n subset F_{p*}` for every `n | 1024` (one prime serves
n = 16..1024, exactly the Row-C regime). The machinery re-runs on the real
primes in minutes by swapping this one constant.

## 1. Validation gates FIRST (STEP 1, mandatory) — all green

The pipeline reproduces known ground truth before any large run:

```text
GATE (a)  h=3 census counts       n=16 F17 -> 352 unordered trades  (a3 note)
                                  n=16 F97 ->  16 unordered trades  (a3 note)
GATE (a') x12 h=3 anchored cores   n=128 p=17921 -> 18   (x12_h3 census)
                                  n=256 p=65537 -> 129  (x12_h3 census)
GATE (c)  DECISIVE non-toral       n=16 F17 (EXCEPTIONAL prime for (16,4)):
          DETECTION                FULL census -> 120 non-toral + 6 toral;
                                  MITM -> anchored 60 non-toral + 3 toral,
                                  orbit-lift x2 -> 120 + 6, 0 fp false-positives
GATE (b)  h=4 toral C(n/4,2)       n=16 ->6, n=32 ->28, n=64 ->120; non-toral=0
          non-toral=0 (a_pilot)    (FULL census AND MITM agree via the lift)
```

Gate (c) is the load-bearing one: it is the only gate whose row actually
*contains* non-toral trades, so it is the only gate that proves the anchored
MITM (and its h=4 fast prefix path) genuinely **sees** non-toral trades rather
than always reporting zero. (During development a sign-convention mismatch
between the hash side and the h=4 fast path — signed locator coefficients
`(-e_1, e_2, -e_3)` vs. unsigned elementary-symmetric `(e_1, e_2, e_3)` — passed
every toral gate yet was blind to non-toral trades; gate (c) now locks the
single convention in place. See the verifier's `sig_general` docstring.)

Any gate mismatch STOPS the run.

## 2. h=4 production: anchored meet-in-the-middle (STEP 2)

**Signature / fingerprint.** For an h-subset A of `mu_n subset F_{p*}` the
signature is the elementary-symmetric tuple `(e_1,...,e_{h-1})` of its locator
(computed once per subset in exact `F_{p*}` arithmetic); its 8-byte
`fp64(e_1,e_2,e_3)` is a lossy hash used **only** for bucketing — every
fingerprint collision is re-checked in exact `F_{p*}` arithmetic, so false
positives are harmless (and, empirically, absent: at every scale `fp_hits`
equals the number of genuine signature matches).

**Anchored MITM.**
- hash side = anchored 4-subsets P with `1 in P` (exponent 0 present):
  `C(n-1, 3)` entries. Stored as *packed exponents only* (the exact signature
  is recomputed on the rare fingerprint hit), so the footprint is ~C(n-1,3)
  small ints — well inside 2 GB up through n = 256.
- probe side = stream every 4-subset Q of the exponents `[1, n-1]` (0 not in
  Q, so Q can be disjoint from an anchored P). The h=4 hot loop fixes a prefix
  triple and varies the 4th point: only 3 field multiplications per probe.

**Orbit justification (the certificate is per-orbit and lifts by n).** Under the
finite-row scaling action `R -> gamma.R` (`gamma in mu_n`), the trade property
is preserved: `e_j(gamma R) = gamma^j e_j(R)`, so `e_j(gamma P) = e_j(gamma Q)`
whenever `e_j(P) = e_j(Q)`. Every trade orbit therefore has a representative
with `1` in one endpoint (scale by any `gamma in P^{-1}`), and that
representative is itself a genuine trade in the *same* fixed field with the
other endpoint some 4-subset of `[1, n-1]`. Hence **anchored-P x streaming-Q
catches at least one representative of every trade orbit** — so
`anchored non-toral = 0` implies `non-toral = 0` outright. Toral totals lift by
the exact orbit identity `#T = (n/2h) . #(anchored members)` (A3 note sec 1.3 /
`a_closure_assembly` input 7); for h=4, `2h = 8 | n`, so the lift is an exact
integer. Both directions are checked against the FULL two-endpoint census at
n <= 64 and against the exceptional-prime count at F17.

**Fiber (toral) class.** A 4-subset has signature `(0,0,0)` iff its locator is
`X^4 + c_0`, i.e. its roots are a full `mu_4`-coset; the toral trades are the
`C(n/4,2)` coset pairs (`x82`-style: the paid multiplicative-pullback fibers).
They are counted and reported separately, never as primitive residue.

**Exact complete census over finite fields** (over the ~250-bit stand-in prime,
h=4, `anchored non-toral = 0` at every scale; toral = C(n/4,2)):

```text
 n     probes C(n-1,4)   probe rate/s   toral (lifted)  non-toral
 16              1,365      682,142              6            0
 32             31,465      825,997             28            0
 64            595,665      813,184            120            0
128         10,334,625      785,840           496            0
256        172,061,505      698,191          2016            0
```

No non-toral 4-trade at any tested scale — the pilot's char-0 finding (empty
non-toral through n=64) now confirmed **directly over finite fields** two
octaves further, to n=256.

### n = 1024 (the official Row-C domain)

A COMPLETE exact census at n=1024 is single-process-infeasible on this machine
(see below); we deliver, over the stand-in prime:

1. **Machinery validated** — a primitive 1024th root of order exactly 1024 over
   the 251-bit prime; full signature/fingerprint pipeline instantiated.
2. **Toral family certified** — all 256 `mu_4`-cosets carry signature `(0,0,0)`
   with distinct `e_4`, giving exactly `C(256,2) = 32640` toral trades; the
   anchored MITM detects them (anchored coset `mu_4` trades with all 255
   disjoint cosets, orbit-lift 128 -> 32640).
3. **Spot slice** — a genuine exhaustive sub-census over the first 160 roots of
   unity (`25,637,001` probes): non-toral = 0.
4. **Full-run extrapolation** (single pure-Python process):
   - probe count `C(1023,4) = 45,367,119,105`; at the measured rate
     `~698,191/s` => probe-side wall time `~18 h` (`~0.8 days`);
   - hash-side entries `C(1023,3) = 177,910,271`; at ~90 B/entry
     `~16.0 GB` — **exceeds the 2 GB ceiling**, so a complete run needs
     the e_1-bucketed two-pass (process one e_1 residue class of the hash side
     at a time; each pass re-streams the probe side, computing only e_1 until a
     bucket match). Because `q ~ 2^250 >> C(1024,4)`, real signature collisions
     are only the structured (toral / genuine) ones — random collisions are
     ~`C(1024,4)^2 / 2^250 ~ 0`.

The **unconditional** "zero non-toral at n=1024" is supplied by the banked
`a3_good_reduction_lemma` + X24 (`a_closure_assembly.md`): for any row prime
with `gcd(p, D(1024,4)) = 1`, reduction is a bijection char-0 <-> row candidates
matching primitive with primitive, and X24 forces zero primitive char-0
candidates. C1a is the **direct corroborating harness and re-runnable check**
for that structural result, exact and complete through n=256 and validated at
n=1024, ready to run to completion on the literal primes (bucketed, off-box).

## 3. h=5 feasibility (STEP 3) — measured, NOT launched

Ground-truth sanity: h=5 in `mu_{2^s}` has no `mu_5` (5 does not divide n) so no
toral trades, and X24 forbids non-toral char-0 trades — the census is empty.
Verified by a complete exact h=5 census at n=64 (`7,028,847` probes, empty).

Full-run extrapolation to n=1024:

```text
 probe count C(1023,5) = 9,245,818,873,599   (~9.2e12)
 measured probe rate (h=5) ~ 134,767/s   =>  ~19,057 h  (~2.2 yr)
 hash-side entries C(1023,4) = 45,367,119,105  =>  ~4,083 GB
```

**VERDICT:** full h=5 at n=1024 is INFEASIBLE on this machine, in both time and
the 2 GB ceiling. NOT launched (matches the task instruction). h=5 non-existence
at the rows is instead delivered structurally: h=5 is not a power of two, so X24
gives an empty char-0 fiber and A3(b) gives `T^a_prim(1024,5) = 0` directly, no
enumeration required — the h=5 window rungs are already closed by the banked
chain, and this note records the honest cost of the brute alternative.

## 4. Certificate format (harness-compatible)

Schema `c1a-lowh-mitm-certificate/v1`, one JSON per Row-C row under
`experimental/data/certificates/c1a-lowh-mitm/`. Key fields:

```text
row, h=4, result.non_toral_primitive_trades (= 0, EXPECTED),
result.signature_collisions_beyond_fiber (= 0),
result.toral_fiber_paid_total (= C(256,2) = 32640),
prime_status (STAND-IN, loud), standin_prime, standin_prime_minus_1_mod_1024,
exact_scan_over_finite_fields (n=16..256, each anchored_nontoral=0),
n1024 (machinery/toral/slice/extrapolation block),
h5_feasibility, harness_compat (coordinates with c2-gcd-certificate/v1),
h4_window_position (per-row).
```

Coordination with `c2_gcd_harness.md`: C2 supplies the `gcd(p, D(n,h))`
good-reduction test (the structural side); C1a supplies the DIRECT row-field
trade census (the falsifier side). Both consume the same three Row-C rows; a
row is fully closed when C1a is clean (or C2 certifies good reduction and X24
supplies zero).

## 5. Verification

```bash
python3 experimental/scripts/verify_c1a_lowh_mitm.py              # gates + self-test
python3 experimental/scripts/verify_c1a_lowh_mitm.py --verify-cert # re-check emitted certs
python3 experimental/scripts/verify_c1a_lowh_mitm.py --production # + n=16..256 + emit
python3 experimental/scripts/verify_c1a_lowh_mitm.py --n1024      # + n=1024 report
python3 experimental/scripts/verify_c1a_lowh_mitm.py --h5         # + h=5 feasibility
python3 experimental/scripts/verify_c1a_lowh_mitm.py --all        # everything (writes certs)
```

For maintainer review, the light commands are the default validation replay
(`13 PASS`, about 18 seconds here) and `--verify-cert` (`4 PASS`, instant).
The heavier `--all` replay re-runs production scans, n=1024 reporting, h=5
measurement, certificate emission, and verification.

Current replay: **27 PASS, 0 FAIL** (wall ~407 s: gates + exact n=16..256 +
n=1024 report + h=5 measurement + certificate emit/verify).
